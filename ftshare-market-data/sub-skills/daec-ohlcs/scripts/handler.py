#!/usr/bin/env python3
"""按标的和日期区间查询 DAEC 历史 OHLC K 线；传入 compat=v2 返回兼容版结构并附带前收盘价和 MA5/10/20"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/daec/history/ohlcs"


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
    parser = argparse.ArgumentParser(description="查询 DAEC 历史 OHLC")
    parser.add_argument("--symbol", required=True, help="标的代码，如 600000.XSHG")
    parser.add_argument("--since", default=None, help="起始日期 YYYYMMDD，标准模式必填")
    parser.add_argument("--until", default=None, help="结束日期 YYYYMMDD，标准模式必填")
    parser.add_argument("--interval", default=None, help="周期：Minute/Day/Week/Month，默认 Day")
    parser.add_argument("--adjust", default=None, help="复权：None/Forward/Backward")
    parser.add_argument("--compat", default=None, help="传 v2 启用兼容版响应")
    parser.add_argument("--span", default=None, help="兼容模式周期：DAY1/WEEK1/MONTH1，默认 DAY1")
    parser.add_argument("--limit", type=int, default=None, help="兼容模式返回数量，默认 250")
    parser.add_argument("--until_ts_ms", type=int, default=None,
                        help="兼容模式结束时间戳（毫秒），优先于默认当前日期")
    args = parser.parse_args()

    if args.compat != "v2" and (args.since is None or args.until is None):
        print("错误：标准模式下 --since 与 --until 必填", file=sys.stderr)
        sys.exit(1)

    params = {"symbol": args.symbol}
    if args.since is not None:
        params["since"] = args.since
    if args.until is not None:
        params["until"] = args.until
    if args.interval is not None:
        params["interval"] = args.interval
    if args.adjust is not None:
        params["adjust"] = args.adjust
    if args.compat is not None:
        params["compat"] = args.compat
    if args.span is not None:
        params["span"] = args.span
    if args.limit is not None:
        params["limit"] = args.limit
    if args.until_ts_ms is not None:
        params["until_ts_ms"] = args.until_ts_ms
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
