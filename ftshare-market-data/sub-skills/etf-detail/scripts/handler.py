#!/usr/bin/env python3
"""查询单只 ETF 详情（daec etf）"""
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
ENDPOINT = "/api/v1/market/data/daec/etf"

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


def build_params(symbol: str, masks: Optional[str] = None) -> dict:
    """构造 daec etf 详情查询参数。

    注：daec 当前忽略 masks（始终返回全字段），保留参数仅为兼容既有调用方。
    """
    params = {"symbol": symbol}
    if masks:
        params["masks"] = masks
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


def fetch(etf: str, masks: Optional[str] = None) -> dict:
    params = build_params(etf, masks)
    url = f"{BASE_URL}{ENDPOINT}?{urllib.parse.urlencode(params)}"
    data = _get_json(url)
    # 将交易所时间戳 ts_millis（毫秒）转为北京时间 ISO 字符串
    if isinstance(data, dict) and "ts_millis" in data:
        data["ts_millis"] = ms_to_iso(data["ts_millis"])
    return data


def main():
    parser = argparse.ArgumentParser(description="查询单只 ETF 详情（daec）")
    parser.add_argument(
        "--etf",
        required=True,
        help="ETF 标的键，带市场后缀，如 510050.XSHG、159915.XSHE、920036.BJ",
    )
    parser.add_argument(
        "--masks",
        default=None,
        help="字段掩码（逗号分隔）；注：daec 当前忽略 masks，始终返回全字段",
    )
    args = parser.parse_args()

    result = fetch(args.etf, args.masks)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
