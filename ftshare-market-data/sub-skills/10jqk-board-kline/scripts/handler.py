#!/usr/bin/env python3
"""查询同花顺指定板块历史K线（market.ft.tech）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")


def main():
    parser = argparse.ArgumentParser(description="查询同花顺指定板块历史K线")
    parser.add_argument("--board-code", required=True, help="板块代码，如 885311")
    parser.add_argument("--page", type=int, default=1, help="页码，默认 1")
    parser.add_argument("--page-size", type=int, default=50, help="每页数量，默认 50")
    args = parser.parse_args()

    params = {"board_code": args.board_code, "page": args.page, "page_size": args.page_size}
    qs = urllib.parse.urlencode(params)
    url = f"{BASE_URL}/api/v1/market/data/ths-board-kline?{qs}"

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

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
