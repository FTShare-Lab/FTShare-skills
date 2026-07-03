#!/usr/bin/env python3
"""查询东财美股全量列表，支持服务端分页。"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/eastmoney-us-stock-list"

SAFE_URLOPENER = urllib.request.build_opener()


def safe_urlopen(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != urllib.parse.urlparse(BASE_URL).scheme or parsed.netloc != urllib.parse.urlparse(BASE_URL).netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    return SAFE_URLOPENER.open(url, timeout=60)


def fetch_page(page: int, page_size: int) -> dict:
    params = {"page": page, "page_size": page_size}
    qs = urllib.parse.urlencode(params)
    url = f"{BASE_URL}{ENDPOINT}?{qs}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def fetch_all(page_size: int = 500) -> list:
    """全量拉取。"""
    first = fetch_page(1, page_size)
    data = first.get("data") or {}
    records = list(data.get("records", []))
    total_pages = data.get("pages", 1)
    total = data.get("total", 0)
    print(f"info: 共 {total} 只美股，{total_pages} 页，正在拉取...", file=sys.stderr)

    for p in range(2, total_pages + 1):
        page_data = fetch_page(p, page_size)
        pdata = page_data.get("data") or {}
        records.extend(pdata.get("records", []))
        if p % 3 == 0:
            print(f"info: 分页进度 {p}/{total_pages} ...", file=sys.stderr)

    print(f"info: 完成，共 {len(records)} 条", file=sys.stderr)
    return records


def main():
    parser = argparse.ArgumentParser(description="查询东财美股列表")
    parser.add_argument("--page", type=int, default=1, help="页码（从 1 开始，默认 1）")
    parser.add_argument("--page_size", type=int, default=50, help="每页条数（默认 50）")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="返回全量数据（不分页）")
    args = parser.parse_args()

    items = fetch_all(500)
    total = len(items)

    if total == 0:
        result = {"code": 0, "message": "success", "data": None}
    elif args.fetch_all:
        result = {
            "code": 0,
            "message": "success",
            "data": {
                "pageNum": 1, "pageSize": total,
                "total": total, "pages": 1,
                "records": items,
            },
        }
    else:
        start = (args.page - 1) * args.page_size
        end = start + args.page_size
        result = {
            "code": 0,
            "message": "success",
            "data": {
                "pageNum": args.page,
                "pageSize": args.page_size,
                "total": total,
                "pages": max(1, (total + args.page_size - 1) // args.page_size),
                "records": items[start:end],
            },
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
