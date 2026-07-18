#!/usr/bin/env python3
"""Tests for stock-filter handler"""
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
    def test_fetch_by_symbol_ignores_board(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("600519.SH", "star", None, 1, 5)
        url = mock_open.call_args[0][0]
        self.assertIn("/api/v1/market/data/stock-list/filter", url)
        self.assertIn("symbol=600519.SH", url)
        self.assertNotIn("board=", url)
        self.assertIn("page=1", url)
        self.assertIn("page_size=5", url)

    @patch.object(handler, "safe_urlopen")
    def test_fetch_by_board(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch(None, "star", "20200101", 1, 5)
        url = mock_open.call_args[0][0]
        self.assertIn("board=star", url)
        self.assertIn("listing_date_since=20200101", url)
        self.assertNotIn("symbol=", url)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json_for_symbol(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        with patch.object(sys, "argv", ["handler.py", "--symbol", "600519.SH", "--page", "1", "--page_size", "5"]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                self.assertEqual(json.loads(fake_out.getvalue()), [])

    def test_main_requires_symbol_or_board(self):
        with patch.object(sys, "argv", ["handler.py"]):
            with self.assertRaises(SystemExit):
                handler.main()


if __name__ == "__main__":
    unittest.main()
