#!/usr/bin/env python3
"""查询单只 A 股股票所有报告期的股东增减持信息"""
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

ENDPOINT = "/api/v1/market/data/holder/stock-share-chg"


def fetch(stock_code: str, page: int, page_size: int) -> dict:
    params = urllib.parse.urlencode({
        "stock_code": stock_code,
        "page": page,
        "page_size": page_size,
    })
    url = f"{BASE_URL}{ENDPOINT}?{params}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="查询单只 A 股股票所有报告期的股东增减持信息")
    parser.add_argument(
        "--stock_code",
        required=True,
        help="股票代码，需携带市场后缀，如 603323.SH / 000001.SZ / 833171.BJ",
    )
    parser.add_argument(
        "--page",
        type=int,
        default=1,
        help="页码，从 1 开始，默认 1",
    )
    parser.add_argument(
        "--page_size",
        type=int,
        default=50,
        help="每页记录数，默认 50",
    )
    args = parser.parse_args()

    result = fetch(args.stock_code, args.page, args.page_size)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
