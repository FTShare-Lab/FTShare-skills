#!/usr/bin/env python3
"""Tests for etf-candlesticks-batch handler"""
import json
import sys
import unittest
import urllib.error
from io import BytesIO, StringIO
from unittest.mock import patch
import importlib.util
import os

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


class TestParseSymbols(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_split(self):
        syms = handler.parse_symbols("510300.XSHG,159915.XSHE,")
        self.assertEqual(syms, ["510300.XSHG", "159915.XSHE"])

    def test_empty_exits(self):
        with self.assertRaises(SystemExit):
            handler.parse_symbols(",, ")


class TestBuildBody(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_required_fields(self):
        b = handler.build_body(["510300.XSHG", "159915.XSHE"], "Day", 1, "None",
                               None, 1756791000000, None)
        self.assertEqual(b["symbols"], ["510300.XSHG", "159915.XSHE"])
        self.assertEqual(b["interval_unit"], "Day")
        self.assertEqual(b["until_ts_millis"], 1756791000000)
        self.assertNotIn("symbol", b)

    def test_optional_fields(self):
        b = handler.build_body(["510300.XSHG"], "Minute", 5, "Forward",
                               1756700000000, 1756791000000, 100)
        self.assertEqual(b["interval_value"], 5)
        self.assertEqual(b["adjust_kind"], "Forward")
        self.assertEqual(b["limit"], 100)


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_post_to_batch_endpoint(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch(["510300.XSHG", "159915.XSHE"], "Day", 1, "None",
                      None, 1756791000000, 2)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "POST")
        self.assertIn("/api/v1/market/data/etf-candlesticks/batch", req.full_url)
        body = json.loads(req.data.decode())
        self.assertEqual(body["symbols"], ["510300.XSHG", "159915.XSHE"])
        self.assertEqual(body["limit"], 2)
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "https://fake", 500, "Internal Error", {}, BytesIO(b"server error")
        )
        with self.assertRaises(SystemExit):
            handler.fetch(["510300.XSHG"], "Day", 1, "None", None, 1756791000000, None)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'[["510300.XSHG",[{"close":"4.55","ts_millis":1756710000000}]]]'
        )
        with patch.object(sys, "argv", [
            "handler.py", "--symbols", "510300.XSHG,159915.XSHE",
            "--interval-unit", "Day", "--until-ts-millis", "1756791000000", "--limit", "2"
        ]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                data = json.loads(fake_out.getvalue())
                self.assertEqual(data[0][0], "510300.XSHG")
                self.assertEqual(data[0][1][0]["close"], "4.55")


if __name__ == "__main__":
    unittest.main()
