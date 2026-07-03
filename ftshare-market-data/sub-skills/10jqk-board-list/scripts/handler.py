#!/usr/bin/env python3
"""查询同花顺板块列表（market.ft.tech）"""
import argparse
import json
import sys
import urllib.error
import urllib.request
import os

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")


def main():
    parser = argparse.ArgumentParser(description="查询同花顺板块列表")
    parser.add_argument("--module", choices=["concept", "csrc", "industry", "region"],
                        help="板块类型过滤：concept/csrc/industry/region")
    parser.add_argument("--search", default=None, help="搜索板块名称或代码")
    args = parser.parse_args()

    url = f"{BASE_URL}/api/v1/market/data/ths-board-list"
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

    if not isinstance(data, list):
        print("Unexpected response format", file=sys.stderr)
        sys.exit(1)

    if args.module:
        data = [b for b in data if b.get("module") == args.module]

    if args.search:
        q = args.search.lower()
        data = [b for b in data if q in b.get("name", "").lower() or q in b.get("code", "")]

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
