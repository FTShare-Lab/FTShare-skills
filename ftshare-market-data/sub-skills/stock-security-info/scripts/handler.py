#!/usr/bin/env python3
"""查询单只股票/基金/指数信息（ftai.chat）"""
import argparse
import json
import sys
import urllib.error
import urllib.request
import urllib.parse
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = "https://ftai.chat"

def safe_urlopen(req_or_url):
    """本接口域名固定为 ftai.chat，与 market.ft.tech 白名单区分。"""
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "ftai.chat":
        print(f"Invalid URL for stock-security-info (expected https://ftai.chat): {url}", file=sys.stderr)
        sys.exit(1)
    return SAFE_URLOPENER.open(req_or_url)



def main():
    parser = argparse.ArgumentParser(description="查询单只股票/基金/指数信息")
    parser.add_argument("--symbol", required=True, help="标的代码，带市场后缀，如 600519.SH")
    args = parser.parse_args()

    url = f"{BASE_URL}/api/v1/market/security/{args.symbol}/info"

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
