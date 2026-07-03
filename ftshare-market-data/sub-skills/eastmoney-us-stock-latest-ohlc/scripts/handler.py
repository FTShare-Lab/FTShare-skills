#!/usr/bin/env python3
"""查询东财美股最新日K线，支持按股票代码过滤与分页"""
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

ENDPOINT = "/api/v1/market/data/eastmoney-us-stock-latest-ohlc"


def fetch(stock_code: str = None, page: int = 1, page_size: int = 50) -> dict:
    params = {"page": page, "page_size": page_size}
    if stock_code:
        params["stock_code"] = stock_code
    qs = urllib.parse.urlencode(params)
    url = f"{BASE_URL}{ENDPOINT}?{qs}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="查询东财美股最新日K线")
    parser.add_argument("--stock_code", default=None, help="股票代码，如 ADV；不传则返回全部美股")
    parser.add_argument("--page", type=int, default=1, help="页码（从 1 开始，默认 1）")
    parser.add_argument("--page_size", type=int, default=50, help="每页条数（默认 50）")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    args = parser.parse_args()

    if args.fetch_all:
        first = fetch(args.stock_code, 1, args.page_size)
        data = first.get("data") or {}
        records = list(data.get("records", []))
        total_pages = data.get("pages", 1)
        for p in range(2, total_pages + 1):
            page_data = fetch(args.stock_code, p, args.page_size)
            pdata = page_data.get("data") or {}
            records.extend(pdata.get("records", []))
        result = {
            "code": first.get("code", 0),
            "message": first.get("message", "success"),
            "data": {
                "pageNum": 1,
                "pageSize": args.page_size,
                "total": len(records),
                "pages": 1,
                "records": records,
            },
        }
    else:
        result = fetch(args.stock_code, args.page, args.page_size)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
