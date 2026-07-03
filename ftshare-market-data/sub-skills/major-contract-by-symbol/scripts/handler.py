#!/usr/bin/env python3
"""按股票代码查询重大合同历史（market.ft.tech）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os

SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")

def safe_urlopen(req_or_url):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != urllib.parse.urlparse(BASE_URL).scheme or parsed.netloc != urllib.parse.urlparse(BASE_URL).netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    return SAFE_URLOPENER.open(req_or_url)


def main():
    parser = argparse.ArgumentParser(description="按股票代码查询重大合同")
    parser.add_argument("--symbol", required=True, help="股票代码（6 位），如 300500")
    parser.add_argument("--page", type=int, default=None, help="页码，从 1 开始")
    parser.add_argument("--page_size", type=int, default=None, help="每页数量，默认 50，最大 200")
    args = parser.parse_args()

    params = {"symbol": args.symbol}
    if args.page is not None:
        params["page"] = args.page
    if args.page_size is not None:
        params["page_size"] = args.page_size

    path = "/api/v1/market/data/corporate/contract/by-symbol?" + urllib.parse.urlencode(params)
    url = BASE_URL + path

    req = urllib.request.Request(url, method="GET")
    req.add_header("Content-Type", "application/json")

    try:
        with safe_urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
