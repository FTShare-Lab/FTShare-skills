#!/usr/bin/env python3
"""获取当前日期的前 N 个交易日（market.ft.tech）"""
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
    parser = argparse.ArgumentParser(description="获取当前日期的前 N 个交易日")
    parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="前 N 个交易日，必须 >= 1",
    )
    args = parser.parse_args()
    if args.n < 1:
        print("错误：n 必须大于等于 1", file=sys.stderr)
        sys.exit(1)

    url = BASE_URL + "/api/v1/market/data/time/get-nth-trade-date?" + urllib.parse.urlencode({"n": args.n})
    req = urllib.request.Request(url, method="GET")

    try:
        with safe_urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(body, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
