#!/usr/bin/env python3
"""分页查询指数权重汇总（market.ft.tech）"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SAFE_URLOPENER = urllib.request.build_opener()

DEFAULT_BASE_URL = "https://market.ft.tech/gateway/"
ENDPOINT = "api/v1/market/data/index/index_weight_summary"


def base_url() -> str:
    return os.environ.get("FTSHARE_BASE_URL", DEFAULT_BASE_URL).rstrip("/") + "/"


def build_url(params: dict) -> str:
    return urllib.parse.urljoin(base_url(), ENDPOINT) + "?" + urllib.parse.urlencode(params)


def main():
    parser = argparse.ArgumentParser(description="分页查询指数权重汇总")
    parser.add_argument(
        "--index-code",
        dest="index_code",
        default=None,
        help="指数代码，如 000300；不传则分页返回全部指数权重汇总",
    )
    parser.add_argument(
        "--page",
        type=int,
        default=1,
        help="页码，从 1 开始，默认 1",
    )
    parser.add_argument(
        "--page-size",
        dest="page_size",
        type=int,
        default=20,
        help="每页条数，默认 20，最大 100",
    )
    args = parser.parse_args()

    if args.page < 1:
        print("page 须 >= 1", file=sys.stderr)
        sys.exit(1)
    if args.page_size < 1 or args.page_size > 100:
        print("page_size 须在 1～100 之间", file=sys.stderr)
        sys.exit(1)

    params = {"page": args.page, "page_size": args.page_size}
    if args.index_code:
        params["index_code"] = args.index_code
    url = build_url(params)

    req = urllib.request.Request(url, method="GET")
    req.add_header("X-Client-Name", "ft-claw")
    req.add_header("Content-Type", "application/json")

    try:
        with SAFE_URLOPENER.open(req) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"请求失败: {e.reason}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
