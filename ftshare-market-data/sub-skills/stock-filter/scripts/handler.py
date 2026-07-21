#!/usr/bin/env python3
"""A 股实时行情筛选接口。

- 传入 --symbol 时按单标的查询，忽略 --board 与 --listing_date_since。
- 否则按 --board（板块/交易所）+ --listing_date_since（上市日期起点）筛选。
"""
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

ENDPOINT = "/api/v1/market/data/stock-list/filter"


def build_params(symbol, board, listing_date_since, page, page_size):
    params = {}
    if symbol:
        params["symbol"] = symbol
    else:
        if board:
            params["board"] = board
        if listing_date_since:
            params["listing_date_since"] = listing_date_since
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size
    return params


def fetch(symbol, board, listing_date_since, page, page_size):
    params = urllib.parse.urlencode(build_params(symbol, board, listing_date_since, page, page_size))
    url = f"{BASE_URL}{ENDPOINT}?{params}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="A 股实时行情筛选")
    parser.add_argument("--symbol", help="单标的代码，如 600519 / 600519.SH / 600519.XSHG；传入后忽略 board 与 listing_date_since")
    parser.add_argument("--board", help="板块/交易所筛选：star / chi_next / bjse / xshg / xshe / main")
    parser.add_argument("--listing_date_since", help="上市日期起点 YYYYMMDD，筛选此后上市的股票")
    parser.add_argument("--page", type=int, help="页码")
    parser.add_argument("--page_size", type=int, help="每页记录数")
    args = parser.parse_args()

    if not args.symbol and not args.board and not args.listing_date_since:
        parser.error("需指定 --symbol 或 --board / --listing_date_since 至少其一")

    result = fetch(args.symbol, args.board, args.listing_date_since, args.page, args.page_size)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
