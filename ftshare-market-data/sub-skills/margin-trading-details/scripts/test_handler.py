#!/usr/bin/env python3
"""Tests for margin-trading-details handler"""
import json
import sys
import unittest
import urllib.error
from io import BytesIO, StringIO
from unittest.mock import patch

# Import the module under test by executing it
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("handler", __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "handler.py"))
handler = importlib.util.module_from_spec(spec)


class TestFetchPage(unittest.TestCase):
    def setUp(self):
        # Reload handler to get fresh state
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_url_without_date(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"items": [], "total_pages": 1, "total_items": 0}'
        handler.fetch_page(2, 200)
        called_url = mock_open.call_args[0][0]
        self.assertIn("page=2", called_url)
        self.assertIn("page_size=200", called_url)
        self.assertNotIn("date=", called_url)

    @patch.object(handler, "safe_urlopen")
    def test_url_with_date(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"items": [], "total_pages": 1, "total_items": 0}'
        handler.fetch_page(2, 200, "20200103")
        called_url = mock_open.call_args[0][0]
        self.assertIn("page=2", called_url)
        self.assertIn("page_size=200", called_url)
        self.assertIn("date=20200103", called_url)

    @patch.object(handler, "safe_urlopen")
    def test_returns_parsed_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"items": [{"symbol": "600000.SH"}], "total_pages": 5, "total_items": 100}'
        )
        result = handler.fetch_page(1, 1)
        self.assertEqual(len(result["items"]), 1)
        self.assertEqual(result["items"][0]["symbol"], "600000.SH")
        self.assertEqual(result["total_pages"], 5)

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "http://fake", 500, "Internal Error", {}, BytesIO(b"server error")
        )
        with self.assertRaises(SystemExit):
            handler.fetch_page(1, 20)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_single_page(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"items": [{"symbol": "000001.SZ"}], "total_pages": 3, "total_items": 50}'
        )
        with patch.object(sys, "argv", ["handler.py", "--page", "1", "--page_size", "20"]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                result = json.loads(fake_out.getvalue())
                self.assertEqual(result["total_pages"], 3)

    @patch.object(handler, "safe_urlopen")
    def test_single_page_with_date(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"items": [], "total_pages": 1, "total_items": 0}'
        )
        with patch.object(sys, "argv", ["handler.py", "--page", "1", "--page_size", "200", "--date", "20200103"]):
            handler.main()
            called_url = mock_open.call_args[0][0]
            self.assertIn("date=20200103", called_url)

    @patch.object(handler, "safe_urlopen")
    def test_fetch_all_pagination(self, mock_open):
        page1 = b'{"items": [{"symbol": "A"}, {"symbol": "B"}], "total_pages": 2, "total_items": 3}'
        page2 = b'{"items": [{"symbol": "C"}], "total_pages": 2, "total_items": 3}'
        mock_open.return_value.__enter__.return_value.read.side_effect = [page1, page2]

        with patch.object(sys, "argv", ["handler.py", "--page_size", "2", "--all"]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                result = json.loads(fake_out.getvalue())
                self.assertEqual(len(result["items"]), 3)
                self.assertEqual(result["total_pages"], 2)
                self.assertEqual(result["total_items"], 3)

    @patch.object(handler, "safe_urlopen")
    def test_fetch_all_with_date(self, mock_open):
        page1 = b'{"items": [{"symbol": "A"}], "total_pages": 2, "total_items": 2}'
        page2 = b'{"items": [{"symbol": "B"}], "total_pages": 2, "total_items": 2}'
        mock_open.return_value.__enter__.return_value.read.side_effect = [page1, page2]

        with patch.object(sys, "argv", ["handler.py", "--all", "--date", "20200103"]):
            handler.main()
            for call in mock_open.call_args_list:
                self.assertIn("date=20200103", call[0][0])


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
