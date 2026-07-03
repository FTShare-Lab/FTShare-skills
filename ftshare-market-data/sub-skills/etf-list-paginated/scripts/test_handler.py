#!/usr/bin/env python3
"""Tests for etf-list-paginated handler"""
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

    def test_page_no_mapped_to_page(self):
        p = handler.build_params(page_no=2, page_size=10)
        self.assertEqual(p["page"], 2)
        self.assertNotIn("page_no", p)

    def test_ob_to_order_by(self):
        self.assertEqual(handler.build_params(ob="change_rate desc"), {"order_by": "change_rate desc"})

    def test_filter_index_kept(self):
        p = handler.build_params(filter_index="true")
        self.assertEqual(p["filter_index"], "true")

    def test_empty_omitted(self):
        p = handler.build_params(filter_="", masks="")
        self.assertNotIn("filter", p)
        self.assertNotIn("masks", p)


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)
        patch.object(handler.time, "sleep").start()
        self.addCleanup(patch.stopall)

    @patch.object(handler, "safe_urlopen")
    def test_url_uses_daec_etfs_with_page(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"items":[]}'
        handler.fetch(order_by="change_rate desc", page_no=2, page_size=10)
        url = mock_open.call_args[0][0].full_url
        self.assertIn("daec/etfs", url)
        self.assertIn("page=2", url)
        self.assertNotIn("page_no", url)
        self.assertNotIn("/api/v2/", url)

    @patch.object(handler, "safe_urlopen")
    def test_items_ts_millis_converted(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"items":[{"symbol":"510050.XSHG","close":"3.005","ts_millis":1782460797000}],"page":1,"total_pages":1,"total_items":1}'
        )
        result = handler.fetch(page_no=1, page_size=10)
        self.assertIsInstance(result["items"][0]["ts_millis"], str)

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "https://fake", 500, "Internal Error", {}, BytesIO(b"server error")
        )
        with self.assertRaises(SystemExit):
            handler.fetch(page_no=1)

    @patch.object(handler, "safe_urlopen")
    def test_retries_on_incomplete_read(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            IncompleteRead(b"partial"),
            b'{"items":[],"page":1,"total_pages":1,"total_items":0}',
        ]
        handler.fetch(page_no=1, page_size=10)
        self.assertEqual(mock_open.call_count, 2)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)
        patch.object(handler.time, "sleep").start()
        self.addCleanup(patch.stopall)

    @patch.object(handler, "safe_urlopen")
    def test_main_basic(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"items":[],"page":1,"total_pages":1,"total_items":0}'
        with patch.object(sys, "argv", ["handler.py", "--page_no", "1", "--page_size", "3", "--order_by", "change_rate desc"]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                result = json.loads(fake_out.getvalue())
                self.assertEqual(result["page"], 1)

    @patch.object(handler, "safe_urlopen")
    def test_main_ob_alias(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"items":[],"page":1,"total_pages":1,"total_items":0}'
        with patch.object(sys, "argv", ["handler.py", "--ob", "change_rate desc", "--page_no", "1"]):
            handler.main()
            url = mock_open.call_args[0][0].full_url
            self.assertIn("order_by=change_rate", url)


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
