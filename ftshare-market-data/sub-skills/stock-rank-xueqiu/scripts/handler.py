#!/usr/bin/env python3
"""查询雪球平台股票排行榜（market.ft.tech）"""
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
    parser = argparse.ArgumentParser(description="查询雪球平台股票排行榜")
    parser.add_argument("--rank-group", type=str, default=None, help="榜单组: follow/tweet/deal")
    parser.add_argument("--period", type=str, default=None, help="周期: 7d/total")
    parser.add_argument("--trade-date", type=str, default=None, help="交易日期 YYYY-MM-DD")
    parser.add_argument("--page", type=int, default=None, help="页码，从1开始")
    parser.add_argument("--page-size", type=int, default=None, help="每页条数，最大100")
    args = parser.parse_args()

    params = {}
    if args.rank_group:
        params["rank_group"] = args.rank_group
    if args.period:
        params["period"] = args.period
    if args.trade_date:
        params["trade_date"] = args.trade_date
    if args.page is not None:
        params["page"] = args.page
    if args.page_size is not None:
        params["page_size"] = args.page_size

    url = BASE_URL + "/api/v1/market/data/xueqiu-rank"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET")

    try:
        with safe_urlopen(req) as resp:
            chunks = []
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                chunks.append(chunk)
            raw = b"".join(chunks).decode()
        data = json.loads(raw)
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(body, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
