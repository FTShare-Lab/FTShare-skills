#!/usr/bin/env python3
"""查询单只 ETF 分钟级分时价格（market.ft.tech）"""
import argparse
import json
import re
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
ENDPOINT = "/api/v1/market/data/daec/history/prices"

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

_TRADE_DAYS_AGO_RE = re.compile(r"TRADE_DAYS_AGO\((\d+)\)")


def tm_ms_to_iso(ms: Optional[int]) -> Optional[str]:
    """将毫秒时间戳转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）。"""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S")


def build_params(since: Optional[str], since_ts_ms: Optional[int]) -> dict:
    """将对外契约 --since/--since_ts_ms 映射为 daec history/prices 的时间参数。

    daec 三选一：range=Today/FiveDays、days=N、ts_ms=<毫秒>，三者互斥。
    """
    if since is None and since_ts_ms is None:
        raise ValueError("since 与 since_ts_ms 二选一，必须提供其一")
    if since is not None and since_ts_ms is not None:
        raise ValueError("since 与 since_ts_ms 二选一，不能同时传递")

    if since_ts_ms is not None:
        return {"ts_ms": str(since_ts_ms)}

    s = since.strip()
    if s == "TODAY":
        return {"range": "Today"}
    if s == "FIVE_DAYS_AGO":
        return {"range": "FiveDays"}
    m = _TRADE_DAYS_AGO_RE.fullmatch(s)
    if m:
        return {"days": m.group(1)}
    raise ValueError(
        f"不支持的 since 取值: {since!r}（支持 TODAY / FIVE_DAYS_AGO / TRADE_DAYS_AGO(n)）"
    )


MAX_RETRIES = 5
_SLEEP_BASE = 0.3  # 指数退避基准秒


def _get_json(url: str):
    """发起 GET 并解析 JSON。

    daec 多日分时响应较大，偶发 IncompleteRead / 连接中断（间歇性，非稳定），
    故对传输类错误重试（指数退避）；HTTP 业务错误（4xx/5xx）不重试，直接退出。
    """
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


def fetch(etf: str, since: Optional[str], since_ts_ms: Optional[int]) -> dict:
    params = build_params(since, since_ts_ms)
    params["symbol"] = etf
    url = f"{BASE_URL}{ENDPOINT}?{urllib.parse.urlencode(params)}"
    data = _get_json(url)

    # daec 返回裸数组，统一包装为 {"prices": [...]} 兼容既有调用方；
    # 将每条 ts_ms（毫秒）转为北京时间 ISO 字符串。
    prices = data if isinstance(data, list) else data.get("prices", [])
    for rec in prices:
        if isinstance(rec, dict) and "ts_ms" in rec:
            rec["ts_ms"] = tm_ms_to_iso(rec["ts_ms"])
    return {"prices": prices}


def main():
    parser = argparse.ArgumentParser(description="查询单只 ETF 分时价格（一分钟级别）")
    parser.add_argument(
        "--etf",
        required=True,
        help="ETF 标的键，带市场后缀，如 510050.XSHG、159915.XSHE、920036.BJ",
    )
    parser.add_argument(
        "--since",
        default=None,
        help="时间范围起点：TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(n)；与 since_ts_ms 二选一",
    )
    parser.add_argument(
        "--since_ts_ms",
        type=int,
        default=None,
        help="时间范围起点（毫秒时间戳）；不传 since 时必传",
    )
    args = parser.parse_args()

    try:
        result = fetch(args.etf, args.since, args.since_ts_ms)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
