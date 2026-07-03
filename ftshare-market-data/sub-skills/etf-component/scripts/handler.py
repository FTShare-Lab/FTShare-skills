#!/usr/bin/env python3
"""查询单只 ETF 成份（market.ft.tech）"""
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
    parser = argparse.ArgumentParser(description="查询单只 ETF 成份")
    parser.add_argument(
        "--symbol",
        required=True,
        help="ETF 标的代码，带交易所后缀，如 510300.XSHG、159915.XSHE、510300.SH",
    )
    args = parser.parse_args()

    path = "/api/v1/market/data/etf-component?" + urllib.parse.urlencode({"symbol": args.symbol})
    url = BASE_URL + path

    req = urllib.request.Request(url, method="GET")
    req.add_header("Content-Type", "application/json")

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
