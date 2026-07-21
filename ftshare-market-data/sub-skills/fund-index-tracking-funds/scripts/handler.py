#!/usr/bin/env python3
"""指数跟踪基金"""
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

ENDPOINT = "/api/v1/market/data/fund/index-fund"

def build_params(args):
    params = {}
    if args.index_code is not None:
        params["index_code"] = args.index_code
    if args.scope is not None:
        params["scope"] = args.scope
    return params

def fetch(args):
    params = urllib.parse.urlencode(build_params(args))
    url = f"{BASE_URL}{ENDPOINT}?{params}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="指数跟踪基金")
    parser.add_argument("--index_code", required=True, help="指数代码，支持裸码（如 000300）或带后缀（如 000300.SH）")
    parser.add_argument("--scope", required=False, help="all 全市场（默认）/ etf 仅场内 ETF")
    args = parser.parse_args()

    result = fetch(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
