#!/usr/bin/env python3
"""查询指定基金在指定区间的累计收益率时间序列"""
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

VALID_CAL_TYPES = ["1M", "3M", "6M", "1Y", "3Y", "5Y", "YTD"]


def main():
    parser = argparse.ArgumentParser(description="查询基金累计收益率")
    parser.add_argument("--institution-code", required=True, help="6 位数字基金代码，如 159619")
    parser.add_argument("--cal-type", required=True, choices=VALID_CAL_TYPES,
                        help="区间类型：1M / 3M / 6M / 1Y / 3Y / 5Y / YTD")
    args = parser.parse_args()

    params = {"institution_code": args.institution_code, "cal-type": args.cal_type}
    url = f"{BASE_URL}/api/v1/market/data/fund/fund-cal-return?" + urllib.parse.urlencode(params)

    try:
        with safe_urlopen(url) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(body, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
