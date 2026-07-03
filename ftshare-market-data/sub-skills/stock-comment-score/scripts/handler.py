#!/usr/bin/env python3
"""查询指定股票的千股千评历史综合评分（market.ft.tech）"""
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
    parser = argparse.ArgumentParser(description="查询千股千评历史综合评分")
    parser.add_argument("--symbol", type=str, required=True, help="6位股票代码")
    args = parser.parse_args()

    url = BASE_URL + "/api/v1/market/data/stock-comment/score?" + urllib.parse.urlencode({"symbol": args.symbol})
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
