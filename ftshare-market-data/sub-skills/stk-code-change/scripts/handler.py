#!/usr/bin/env python3
"""查询 A 股代码变更历史（market.ft.tech）"""
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


ENDPOINT = "/api/v1/market/data/stk-code-change"


def build_params(trade_code, start_date, end_date):
    params = {}
    if trade_code:
        params["trade_code"] = trade_code
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return params


def fetch(trade_code, start_date, end_date):
    params = urllib.parse.urlencode(build_params(trade_code, start_date, end_date))
    url = f"{BASE_URL}{ENDPOINT}?{params}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="查询 A 股代码变更历史")
    parser.add_argument(
        "--trade_code",
        required=True,
        help="股票代码（带 .SZ/.SH 后缀），支持逗号分隔多个，如 001872.SZ",
    )
    parser.add_argument("--start_date", help="过滤区间起始日期，YYYYMMDD 格式")
    parser.add_argument("--end_date", help="过滤区间结束日期，YYYYMMDD 格式")
    args = parser.parse_args()

    result = fetch(args.trade_code, args.start_date, args.end_date)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
