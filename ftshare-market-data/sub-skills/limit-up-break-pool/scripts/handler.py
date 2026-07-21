#!/usr/bin/env python3
"""查询炸板股池（market.ft.tech）"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import os

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")

TRADE_DATE_RE = re.compile(r"^\d{8}$")


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
    parser = argparse.ArgumentParser(description="查询炸板股池")
    parser.add_argument(
        "--trade-date",
        dest="trade_date",
        default=None,
        help="交易日期，格式 YYYYMMDD；不传或传当日时查询实时数据",
    )
    args = parser.parse_args()

    params = {}
    if args.trade_date is not None and args.trade_date.strip():
        td = args.trade_date.strip()
        if not TRADE_DATE_RE.match(td):
            print(f"--trade-date 需为 YYYYMMDD：{args.trade_date}", file=sys.stderr)
            sys.exit(1)
        params["trade_date"] = td

    query = ("?" + urllib.parse.urlencode(params)) if params else ""
    url = f"{BASE_URL}/api/v1/market/data/limit-up-break-pool{query}"
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
