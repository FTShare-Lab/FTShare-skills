#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v3/market/data/futures_minutes"
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
SAFE_URLOPENER = urllib.request.build_opener()


def safe_urlopen(req_or_url):
    url = req_or_url.full_url if isinstance(req_or_url, urllib.request.Request) else str(req_or_url)
    base = urllib.parse.urlparse(BASE_URL)
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(req_or_url, urllib.request.Request):
        req_or_url = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    for key, value in _REQUEST_HEADERS.items():
        req_or_url.add_unredirected_header(key, value)
    return SAFE_URLOPENER.open(req_or_url)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询期货合约历史分钟 K 线")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--interval", default=None)
    parser.add_argument("--start", type=int, default=None)
    parser.add_argument("--end", type=int, default=None)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    params = {key: value for key, value in vars(args).items() if value is not None}
    url = f"{BASE_URL}{ENDPOINT}?{urllib.parse.urlencode(params)}"
    try:
        with safe_urlopen(url) as response:
            payload = json.loads(response.read().decode())
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except (urllib.error.URLError, ValueError) as error:
        print(f"Request failed: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
