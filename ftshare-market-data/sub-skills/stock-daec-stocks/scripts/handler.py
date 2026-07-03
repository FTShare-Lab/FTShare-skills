#!/usr/bin/env python3
"""查询 A 股行情列表 daec 全字段族。"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT_PREFIX = "/api/v1/market/data/daec/stocks"

SAFE_URLOPENER = urllib.request.build_opener()

HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}


def safe_urlopen(req_or_url):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != urllib.parse.urlparse(BASE_URL).scheme or parsed.netloc != urllib.parse.urlparse(BASE_URL).netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    return SAFE_URLOPENER.open(req_or_url, timeout=60)


def build_params(page: int = 1, page_size: int = 20, filter_: str = "", order_by: str = "") -> dict:
    params = {"page": page, "page_size": page_size}
    if filter_:
        params["filter"] = filter_
    if order_by:
        params["order_by"] = order_by
    return params


def fetch_page(board: str, page: int = 1, page_size: int = 20, filter_: str = "", order_by: str = "") -> dict:
    params = build_params(page, page_size, filter_, order_by)
    qs = urllib.parse.urlencode(params)
    board_path = urllib.parse.quote(board.strip(), safe="")
    url = f"{BASE_URL}{ENDPOINT_PREFIX}/{board_path}?{qs}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with safe_urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def fetch_all(board: str, page_size: int = 200, filter_: str = "", order_by: str = "") -> dict:
    first = fetch_page(board, 1, page_size, filter_, order_by)
    items = list(first.get("items", []))
    total_pages = first.get("total_pages", 1)
    for page in range(2, total_pages + 1):
        data = fetch_page(board, page, page_size, filter_, order_by)
        items.extend(data.get("items", []))
    return {
        "items": items,
        "total_pages": total_pages,
        "total_items": first.get("total_items", len(items)),
    }


def main():
    parser = argparse.ArgumentParser(description="查询 A 股行情列表 daec 全字段族")
    parser.add_argument("--board", required=True, choices=["all", "xshg", "xshe", "bjse"], help="板块：all/xshg/xshe/bjse")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始")
    parser.add_argument("--page_size", type=int, default=20, help="每页条数，默认 20")
    parser.add_argument("--filter", default="", help='筛选表达式，如 close > 10 或 name.contains("银行")')
    parser.add_argument("--order_by", default="", help='排序规则，如 change_rate desc')
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量")
    args = parser.parse_args()

    if args.fetch_all:
        result = fetch_all(args.board, args.page_size, args.filter, args.order_by)
    else:
        result = fetch_page(args.board, args.page, args.page_size, args.filter, args.order_by)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
