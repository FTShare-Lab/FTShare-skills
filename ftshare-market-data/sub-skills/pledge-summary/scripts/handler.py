#!/usr/bin/env python3
"""查询 A 股市场所有报告期的股权质押总揽数据"""
import json
import sys
import urllib.error
import urllib.request
import urllib.parse
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

ENDPOINT = "/api/v1/market/data/pledge/pledge-summary"


def fetch() -> list:
    url = f"{BASE_URL}{ENDPOINT}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def _to_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def normalize(items: list) -> list:
    result = []
    for item in items:
        result.append({
            "trade_date": item.get("trade_date", ""),
            "pledge_total_ratio": _to_float(item.get("pledge_total_ratio", 0)),
            "pledge_company_count": int(item.get("pledge_company_count", 0)),
            "pledge_deal_count": int(item.get("pledge_deal_count", 0)),
            "pledge_total_shares": _to_float(item.get("pledge_total_shares", 0)),
            "pledge_total_market_value": _to_float(item.get("pledge_total_market_value", 0)),
            "hs300_index": _to_float(item.get("hs300_index", 0)),
            "hs300_week_change_ratio": _to_float(item.get("hs300_week_change_ratio", 0)),
        })
    return result


def main():
    raw = fetch()
    result = normalize(raw)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
