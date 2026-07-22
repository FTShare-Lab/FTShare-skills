#!/usr/bin/env python3
"""Tests for stk-status-change handler"""
import json
import sys
import unittest
from io import StringIO
from unittest.mock import patch
import importlib.util
import os

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_fetch_by_trade_code(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("600848.SH", None, None)
        url = mock_open.call_args[0][0]
        self.assertIn("/api/v1/market/data/stk-status-change", url)
        self.assertIn("trade_code=600848.SH", url)

    @patch.object(handler, "safe_urlopen")
    def test_fetch_by_change_type(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("600848.SH", None, "上市")
        url = mock_open.call_args[0][0]
        self.assertIn("change_type=", url)

    @patch.object(handler, "safe_urlopen")
    def test_fetch_all_empty(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch(None, None, None)
        url = mock_open.call_args[0][0]
        self.assertNotIn("trade_code", url)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        with patch.object(sys, "argv", ["handler.py"]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                self.assertEqual(json.loads(fake_out.getvalue()), [])


if __name__ == "__main__":
    unittest.main()
