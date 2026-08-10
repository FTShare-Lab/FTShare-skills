#!/usr/bin/env python3
"""分页查询期货日终行情（开高低收/结算价/成交量/成交额/持仓量），按交易所/合约/交易日或区间"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/futures/eod-price"


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


def fetch_page(page: int, page_size: int, **extra) -> dict:
    params = {"page": page, "page_size": page_size}
    params.update({k: v for k, v in extra.items() if v is not None})
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
    parser = argparse.ArgumentParser(description="查询期货日终行情")
    parser.add_argument("--exchange", default=None, help="交易所代码，如 SHFE/DCE/CZCE/CFFEX/INE/GFE")
    parser.add_argument("--symbol", default=None, help="合约代码，精确匹配")
    parser.add_argument("--trade_date", type=int, default=None, help="精确交易日 YYYYMMDD；与 start_date/end_date 互斥")
    parser.add_argument("--start_date", type=int, default=None, help="起始交易日 YYYYMMDD；须与 end_date 同时提供")
    parser.add_argument("--end_date", type=int, default=None, help="结束交易日 YYYYMMDD；须与 start_date 同时提供")
    parser.add_argument("--page", type=int, default=1, help="页码（默认 1）")
    parser.add_argument("--page_size", type=int, default=50, help="每页条数（默认 50，最大 200）")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量")
    args = parser.parse_args()

    if args.trade_date is not None and (args.start_date is not None or args.end_date is not None):
        print("错误：--trade_date 不可与 --start_date/--end_date 同时使用", file=sys.stderr)
        sys.exit(1)
    if (args.start_date is None) != (args.end_date is None):
        print("错误：--start_date 与 --end_date 必须同时提供", file=sys.stderr)
        sys.exit(1)

    extra = dict(exchange=args.exchange, symbol=args.symbol, trade_date=args.trade_date,
                 start_date=args.start_date, end_date=args.end_date)

    if args.fetch_all:
        first = fetch_page(1, args.page_size, **extra)
        data = first.get("data") or {}
        records = list(data.get("records", []))
        pages = data.get("pages", 1)
        for p in range(2, pages + 1):
            d = fetch_page(p, args.page_size, **extra).get("data") or {}
            records.extend(d.get("records", []))
        result = {
            "code": first.get("code"), "message": first.get("message"),
            "data": {"pageNum": 1, "pageSize": args.page_size,
                     "total": data.get("total", len(records)), "pages": pages, "records": records},
        }
    else:
        result = fetch_page(args.page, args.page_size, **extra)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
