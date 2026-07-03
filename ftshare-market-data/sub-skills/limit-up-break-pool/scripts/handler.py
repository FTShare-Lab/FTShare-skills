#!/usr/bin/env python3
"""查询当日炸板股池（market.ft.tech）"""
import json
import sys
import urllib.error
import urllib.request
import os

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")


def _is_a_share(symbol):
    """过滤非 A 股标的（B 股、可转债、基金等）。"""
    code, _, market = symbol.partition(".")
    if not code:
        return False
    if market == "XSHG":
        return code[0] == "6" or code[:3] == "688"
    if market == "XSHE":
        return code[0] in ("0", "3")
    if market == "BJSE":
        return code[0] == "8"
    return False


def main():
    url = f"{BASE_URL}/api/v1/market/data/limit-up-break-pool"
    req = urllib.request.Request(url, method="GET")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500] if e.fp else ""
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)

    data = [it for it in data if _is_a_share(it.get("symbol", ""))]
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
