#!/usr/bin/env python3
"""Tests for index-prices handler"""
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

    def test_today(self):
        self.assertEqual(handler.build_params("TODAY", None), {"range": "Today"})

    def test_five_days_ago(self):
        self.assertEqual(handler.build_params("FIVE_DAYS_AGO", None), {"range": "FiveDays"})

    def test_trade_days_ago(self):
        self.assertEqual(handler.build_params("TRADE_DAYS_AGO(10)", None), {"days": "10"})

    def test_trade_days_ago_single(self):
        self.assertEqual(handler.build_params("TRADE_DAYS_AGO(1)", None), {"days": "1"})

    def test_since_ts_ms(self):
        self.assertEqual(handler.build_params(None, 1735689600000), {"ts_ms": "1735689600000"})

    def test_none_raises(self):
        with self.assertRaises(ValueError):
            handler.build_params(None, None)

    def test_both_raises(self):
        with self.assertRaises(ValueError):
            handler.build_params("TODAY", 1735689600000)

    def test_invalid_since_raises(self):
        with self.assertRaises(ValueError):
            handler.build_params("FOO", None)


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)
        patch.object(handler.time, "sleep").start()
        self.addCleanup(patch.stopall)

    @patch.object(handler, "safe_urlopen")
    def test_url_uses_daec_endpoint_with_symbol_and_range(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("000001.XSHG", "TODAY", None)
        url = mock_open.call_args[0][0].full_url
        self.assertIn("daec/history/prices", url)
        self.assertIn("symbol=000001.XSHG", url)
        self.assertIn("range=Today", url)
        self.assertNotIn("/api/v2/", url)

    @patch.object(handler, "safe_urlopen")
    def test_url_with_trade_days_ago(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("000001.XSHG", "TRADE_DAYS_AGO(5)", None)
        url = mock_open.call_args[0][0].full_url
        self.assertIn("days=5", url)
        self.assertNotIn("range=", url)

    @patch.object(handler, "safe_urlopen")
    def test_url_with_ts_ms(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("000001.XSHG", None, 1735689600000)
        url = mock_open.call_args[0][0].full_url
        self.assertIn("ts_ms=1735689600000", url)
        self.assertNotIn("range=", url)

    @patch.object(handler, "safe_urlopen")
    def test_wraps_bare_array_and_converts_ts_ms(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'[{"ts_ms":1782092100000,"price":4082.1448,"avg_price":25.02,"volume":985724300,"turnover":24667426241.9}]'
        )
        result = handler.fetch("000001.XSHG", "TODAY", None)
        self.assertEqual(len(result["prices"]), 1)
        rec = result["prices"][0]
        self.assertEqual(rec["price"], 4082.1448)
        self.assertIsInstance(rec["ts_ms"], str)
        self.assertIn("T", rec["ts_ms"])

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "https://fake", 500, "Internal Error", {}, BytesIO(b"server error")
        )
        with self.assertRaises(SystemExit):
            handler.fetch("000001.XSHG", "TODAY", None)

    @patch.object(handler, "safe_urlopen")
    def test_retries_on_incomplete_read(self, mock_open):
        # daec 大响应偶发 IncompleteRead，应重试到成功为止
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            IncompleteRead(b"partial"),
            b'[{"ts_ms":1782092100000,"price":4082.1448}]',
        ]
        result = handler.fetch("000001.XSHG", "TODAY", None)
        self.assertEqual(mock_open.call_count, 2)
        self.assertEqual(result["prices"][0]["price"], 4082.1448)

    @patch.object(handler, "safe_urlopen")
    def test_retries_exhausted_exits(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.side_effect = IncompleteRead(b"partial")
        with self.assertRaises(SystemExit):
            handler.fetch("000001.XSHG", "TODAY", None)
        self.assertEqual(mock_open.call_count, handler.MAX_RETRIES)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_since_today(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        with patch.object(sys, "argv", ["handler.py", "--index", "000001.XSHG", "--since", "TODAY"]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                result = json.loads(fake_out.getvalue())
                self.assertEqual(result["prices"], [])

    def test_main_missing_time_exits(self):
        with patch.object(sys, "argv", ["handler.py", "--index", "000001.XSHG"]):
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
