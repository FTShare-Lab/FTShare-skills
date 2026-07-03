#!/usr/bin/env python3
"""ETF 分页列表（daec etfs）：分页、排序、筛选"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from http.client import IncompleteRead
from typing import Optional
import os
SAFE_URLOPENER = urllib.request.build_opener()

BEIJING_TZ = timezone(timedelta(hours=8))

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/daec/etfs"

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

HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}


def ms_to_iso(ms: Optional[int]) -> Optional[str]:
    """将毫秒时间戳转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）。"""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S")


def build_params(order_by=None, ob=None, filter_=None, masks=None, page_size=None, page_no=None, filter_index=None):
    """构造 daec 分页列表查询参数。

    关键映射：v2 的 `page_no` → daec 的 `page`（daec 忽略 page_no，不转则永远返回第一页）；
    `ob` 作为 `order_by` 的别名。注：daec 当前忽略 masks（返回全字段）。
    """
    params = {}
    sort = order_by if order_by else ob
    if sort:
        params["order_by"] = sort
    if filter_:
        params["filter"] = filter_
    if masks:
        params["masks"] = masks
    if page_size is not None:
        params["page_size"] = page_size
    if page_no is not None:
        params["page"] = page_no  # v2 page_no → daec page
    if filter_index is not None:
        params["filter_index"] = filter_index
    return params


MAX_RETRIES = 5
_SLEEP_BASE = 0.3  # 指数退避基准秒


def _get_json(url: str):
    """发起 GET 并解析 JSON。daec 大响应偶发截断，对传输类错误重试。"""
    last_exc = None
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with safe_urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            print(f"HTTP {e.code}: {body}", file=sys.stderr)
            sys.exit(1)
        except (IncompleteRead, OSError) as e:
            last_exc = e
            if attempt < MAX_RETRIES - 1:
                time.sleep(_SLEEP_BASE * (2 ** attempt))
    print(f"请求失败（重试 {MAX_RETRIES} 次仍截断或网络错误）: {last_exc}", file=sys.stderr)
    sys.exit(1)


def fetch(order_by=None, ob=None, filter_=None, masks=None, page_size=None, page_no=None, filter_index=None):
    params = build_params(order_by, ob, filter_, masks, page_size, page_no, filter_index)
    url = f"{BASE_URL}{ENDPOINT}?{urllib.parse.urlencode(params)}"
    data = _get_json(url)
    for item in data.get("items", []):
        if isinstance(item, dict) and "ts_millis" in item:
            item["ts_millis"] = ms_to_iso(item["ts_millis"])
    return data


def main():
    parser = argparse.ArgumentParser(description="ETF 分页列表，支持排序、筛选、分页（daec）")
    parser.add_argument("--order_by", default=None, help="排序方式，如 change_rate desc、name asc")
    parser.add_argument("--ob", default=None, help="与 order_by 同义")
    parser.add_argument("--filter", default=None, help="过滤条件表达式，如 change_rate != null")
    parser.add_argument("--masks", default=None, help="字段掩码（daec 当前忽略，返回全字段）")
    parser.add_argument("--page_size", type=int, default=None, help="每页条数")
    parser.add_argument("--page_no", type=int, default=None, help="页码，从 1 开始")
    parser.add_argument("--filter_index", default=None, help="是否指数过滤，true/false")
    args = parser.parse_args()

    result = fetch(
        order_by=args.order_by,
        ob=args.ob,
        filter_=args.filter,
        masks=args.masks,
        page_size=args.page_size,
        page_no=args.page_no,
        filter_index=args.filter_index,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
