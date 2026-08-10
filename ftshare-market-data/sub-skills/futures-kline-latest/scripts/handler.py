#!/usr/bin/env python3
"""查询期货合约最新一根 1 分钟 K 线，未找到数据时 data.item 为 null"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/futures/kline/latest"


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
    parser = argparse.ArgumentParser(description="查询期货最新 1 分钟 K 线")
    parser.add_argument("--symbol", required=True, help="WIND 合约全码（如 A2605.DCE）或表内合约代码（如 a2605）")
    parser.add_argument("--interval", default="1min", help="K 线周期，当前仅支持 1min（兼容 1m），默认 1min")
    args = parser.parse_args()

    qs = urllib.parse.urlencode({"symbol": args.symbol, "interval": args.interval})
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
