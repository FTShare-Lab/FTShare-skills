#!/usr/bin/env python3
"""查询港股估值分析（分页，market.ft.tech）"""
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
    parser = argparse.ArgumentParser(description="查询港股估值分析（分页）")
    parser.add_argument(
        "--trade_code",
        default=None,
        help="港股代码，可选；如 00700.HK 或 700；不传则全市场分页",
    )
    parser.add_argument(
        "--page",
        type=int,
        default=1,
        help="页码，从 1 开始，默认 1",
    )
    parser.add_argument(
        "--page_size",
        type=int,
        default=20,
        help="每页条数，默认 20",
    )
    args = parser.parse_args()

    params = {"page": args.page, "page_size": args.page_size}
    if args.trade_code is not None and str(args.trade_code).strip() != "":
        params["trade_code"] = args.trade_code.strip()

    path = "/api/v1/market/data/hk/hk-valuatnanalyd"
    url = BASE_URL + path + "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, method="GET")

    try:
        with safe_urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
