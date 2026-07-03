#!/usr/bin/env python3
"""Tests for etf-detail handler"""
import json
import sys
import unittest
import urllib.error
from http.client import IncompleteRead
from io import BytesIO, StringIO
from unittest.mock import patch

import importlib.util
import os

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


class TestBuildParams(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_symbol_only(self):
        self.assertEqual(handler.build_params("510050.XSHG"), {"symbol": "510050.XSHG"})

    def test_with_masks(self):
        p = handler.build_params("510050.XSHG", "name,close")
        self.assertEqual(p, {"symbol": "510050.XSHG", "masks": "name,close"})

    def test_empty_masks_ignored(self):
        self.assertEqual(handler.build_params("510050.XSHG", ""), {"symbol": "510050.XSHG"})


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)
        patch.object(handler.time, "sleep").start()
        self.addCleanup(patch.stopall)

    @patch.object(handler, "safe_urlopen")
    def test_url_uses_daec_endpoint_with_symbol(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        handler.fetch("510050.XSHG")
        url = mock_open.call_args[0][0].full_url
        self.assertIn("daec/etf", url)
        self.assertIn("symbol=510050.XSHG", url)
        self.assertNotIn("/api/v2/", url)

    @patch.object(handler, "safe_urlopen")
    def test_url_with_masks(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        handler.fetch("510050.XSHG", "name,close")
        url = mock_open.call_args[0][0].full_url
        self.assertIn("masks=name", url)

    @patch.object(handler, "safe_urlopen")
    def test_converts_ts_millis_to_iso(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"symbol":"510050.XSHG","close":"4.868","ts_millis":1780300809000}'
        )
        result = handler.fetch("510050.XSHG")
        self.assertEqual(result["close"], "4.868")
        self.assertIsInstance(result["ts_millis"], str)
        self.assertIn("T", result["ts_millis"])

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "https://fake", 404, "Not Found", {}, BytesIO(b"not found")
        )
        with self.assertRaises(SystemExit):
            handler.fetch("510050.XSHG")

    @patch.object(handler, "safe_urlopen")
    def test_retries_on_incomplete_read(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            IncompleteRead(b"partial"),
            b'{"symbol":"510050.XSHG","ts_millis":1780300809000}',
        ]
        result = handler.fetch("510050.XSHG")
        self.assertEqual(mock_open.call_count, 2)
        self.assertEqual(result["symbol"], "510050.XSHG")


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)
        patch.object(handler.time, "sleep").start()
        self.addCleanup(patch.stopall)

    @patch.object(handler, "safe_urlopen")
    def test_main_basic(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"symbol":"510050.XSHG"}'
        with patch.object(sys, "argv", ["handler.py", "--etf", "510050.XSHG"]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                result = json.loads(fake_out.getvalue())
                self.assertEqual(result["symbol"], "510050.XSHG")


class TestSafeUrlopen(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_rejects_non_https(self):
        with self.assertRaises(SystemExit):
            handler.safe_urlopen("http://market.ft.tech/api")

    def test_rejects_wrong_host(self):
        with self.assertRaises(SystemExit):
            handler.safe_urlopen("https://evil.com/api")


if __name__ == "__main__":
    unittest.main()
