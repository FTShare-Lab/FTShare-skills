#!/usr/bin/env python3
"""Tests for index-candlesticks-batch handler"""
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


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_post_to_index_batch_endpoint(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch(["000300.XSHG", "399001.XSHE"], "Day", 1, "None",
                      None, 1756791000000, 2)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "POST")
        self.assertIn("/api/v1/market/data/index-candlesticks/batch", req.full_url)
        body = json.loads(req.data.decode())
        self.assertEqual(body["symbols"], ["000300.XSHG", "399001.XSHE"])
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")


if __name__ == "__main__":
    unittest.main()
