#!/usr/bin/env python3
"""Tests for etf-ohlcs handler"""
import json
import re
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

    def test_basic(self):
        p = handler.build_params("510050.XSHG", "20240101", "20240131")
        self.assertEqual(p["symbol"], "510050.XSHG")
        self.assertEqual(p["since"], "20240101")
        self.assertEqual(p["until"], "20240131")
        self.assertEqual(p["interval"], "Day")

    def test_interval_week(self):
        p = handler.build_params("510050.XSHG", "20240101", "20240601", interval="Week")
        self.assertEqual(p["interval"], "Week")

    def test_adjust_forward(self):
        p = handler.build_params("510050.XSHG", "20240101", "20240131", adjust="Forward")
        self.assertEqual(p["adjust"], "Forward")

    def test_no_adjust_when_none(self):
        p = handler.build_params("510050.XSHG", "20240101", "20240131")
        self.assertNotIn("adjust", p)

    def test_bad_since_raises(self):
        with self.assertRaises(ValueError):
            handler.build_params("510050.XSHG", "2024-01-01", "20240131")

    def test_bad_until_raises(self):
        with self.assertRaises(ValueError):
            handler.build_params("510050.XSHG", "20240101", "2024131")

    def test_short_date_raises(self):
        with self.assertRaises(ValueError):
            handler.build_params("510050.XSHG", "202401", "20240131")


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)
        patch.object(handler.time, "sleep").start()
        self.addCleanup(patch.stopall)

    @patch.object(handler, "safe_urlopen")
    def test_url_uses_daec_endpoint(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("510050.XSHG", "20240101", "20240131")
        url = mock_open.call_args[0][0].full_url
        self.assertIn("daec/history/ohlcs", url)
        self.assertIn("symbol=510050.XSHG", url)
        self.assertIn("since=20240101", url)
        self.assertIn("until=20240131", url)
        self.assertIn("interval=Day", url)
        self.assertNotIn("/api/v2/", url)

    @patch.object(handler, "safe_urlopen")
    def test_url_with_adjust(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("510050.XSHG", "20240101", "20240131", adjust="Forward")
        url = mock_open.call_args[0][0].full_url
        self.assertIn("adjust=Forward", url)

    @patch.object(handler, "safe_urlopen")
    def test_wraps_bare_array_and_converts_ts(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'[{"open_ts_ms":1717378200000,"close_ts_ms":1717398000000,"open":"2.85","high":"2.865","low":"2.84","close":"2.862","volume":125000000,"turnover":"350000000.0"}]'
        )
        result = handler.fetch("510050.XSHG", "20240101", "20240131")
        self.assertEqual(len(result["ohlcs"]), 1)
        rec = result["ohlcs"][0]
        self.assertEqual(rec["close"], "2.862")
        self.assertIsInstance(rec["open_ts_ms"], str)
        self.assertIn("T", rec["open_ts_ms"])

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "https://fake", 500, "Internal Error", {}, BytesIO(b"server error")
        )
        with self.assertRaises(SystemExit):
            handler.fetch("510050.XSHG", "20240101", "20240131")

    @patch.object(handler, "safe_urlopen")
    def test_retries_on_incomplete_read(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            IncompleteRead(b"partial"),
            b'[{"open_ts_ms":1717378200000,"close":"2.862"}]',
        ]
        result = handler.fetch("510050.XSHG", "20240101", "20240131")
        self.assertEqual(mock_open.call_count, 2)
        self.assertEqual(result["ohlcs"][0]["close"], "2.862")

    @patch.object(handler, "safe_urlopen")
    def test_retries_exhausted_exits(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.side_effect = IncompleteRead(b"partial")
        with self.assertRaises(SystemExit):
            handler.fetch("510050.XSHG", "20240101", "20240131")
        self.assertEqual(mock_open.call_count, handler.MAX_RETRIES)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)
        patch.object(handler.time, "sleep").start()
        self.addCleanup(patch.stopall)

    @patch.object(handler, "safe_urlopen")
    def test_main_explicit_until(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        with patch.object(sys, "argv", ["handler.py", "--etf", "510050.XSHG", "--since", "20240101", "--until", "20240131"]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                result = json.loads(fake_out.getvalue())
                self.assertEqual(result["ohlcs"], [])

    @patch.object(handler, "safe_urlopen")
    def test_main_default_until_today(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        with patch.object(sys, "argv", ["handler.py", "--etf", "510050.XSHG", "--since", "20240101"]):
            with patch("sys.stdout", new_callable=StringIO):
                handler.main()
            url = mock_open.call_args[0][0].full_url
            self.assertIsNotNone(re.search(r"until=\d{8}", url))

    def test_main_missing_since_exits(self):
        with patch.object(sys, "argv", ["handler.py", "--etf", "510050.XSHG"]):
            with self.assertRaises(SystemExit):
                handler.main()


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
