#!/usr/bin/env python3
"""查询期货合约日内 1 分钟 K 线序列，可按毫秒时间戳区间过滤，最大 1000 条"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/futures/kline/intraday"


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
    parser = argparse.ArgumentParser(description="查询期货日内 1 分钟 K 线")
    parser.add_argument("--symbol", required=True, help="WIND 合约全码或表内合约代码，如 rb2610 / A2605.DCE")
    parser.add_argument("--interval", default="1min", help="K 线周期，当前仅支持 1min（兼容 1m），默认 1min")
    parser.add_argument("--start", type=int, default=None, help="开始时间，毫秒时间戳，闭区间")
    parser.add_argument("--end", type=int, default=None, help="结束时间，毫秒时间戳，闭区间")
    parser.add_argument("--limit", type=int, default=600, help="最大返回条数，默认 600，范围 1~1000")
    args = parser.parse_args()

    if args.start is not None and args.end is not None and args.end < args.start:
        print("错误：--end 不得早于 --start", file=sys.stderr)
        sys.exit(1)

    params = {"symbol": args.symbol, "interval": args.interval, "limit": args.limit}
    if args.start is not None:
        params["start"] = args.start
    if args.end is not None:
        params["end"] = args.end
    qs = urllib.parse.urlencode(params)
    url = f"{BASE_URL}{ENDPOINT}?{qs}"
    try:
        with safe_urlopen(url) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
