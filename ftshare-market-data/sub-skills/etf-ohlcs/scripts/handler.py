#!/usr/bin/env python3
"""查询单只 ETF OHLC K 线（daec history/ohlcs，日期区间）"""
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
ENDPOINT = "/api/v1/market/data/daec/history/ohlcs"

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

_DATE_RE = re.compile(r"^\d{8}$")


def ms_to_iso(ms: Optional[int]) -> Optional[str]:
    """将毫秒时间戳转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）。"""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S")


def build_params(symbol: str, since: str, until: str, interval: str = "Day", adjust: Optional[str] = None) -> dict:
    """构造 daec history/ohlcs 查询参数。since/until 为 YYYYMMDD。"""
    if not _DATE_RE.match(since):
        raise ValueError(f"since 需为 YYYYMMDD（8 位数字）: {since!r}")
    if not _DATE_RE.match(until):
        raise ValueError(f"until 需为 YYYYMMDD（8 位数字）: {until!r}")
    params = {"symbol": symbol, "since": since, "until": until, "interval": interval}
    if adjust and adjust != "None":
        params["adjust"] = adjust
    return params


MAX_RETRIES = 5
_SLEEP_BASE = 0.3  # 指数退避基准秒


def _get_json(url: str):
    """发起 GET 并解析 JSON。

    daec 大区间响应较大，偶发 IncompleteRead / 连接中断（间歇性，非稳定），
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


def fetch(etf: str, since: str, until: str, interval: str = "Day", adjust: Optional[str] = None) -> dict:
    params = build_params(etf, since, until, interval, adjust)
    url = f"{BASE_URL}{ENDPOINT}?{urllib.parse.urlencode(params)}"
    data = _get_json(url)

    # daec 返回裸数组，统一包装为 {"ohlcs": [...]}；
    # 将每条 open_ts_ms / close_ts_ms（毫秒）转为北京时间 ISO 字符串。
    ohlcs = data if isinstance(data, list) else data.get("ohlcs", [])
    for o in ohlcs:
        if isinstance(o, dict):
            if "open_ts_ms" in o:
                o["open_ts_ms"] = ms_to_iso(o["open_ts_ms"])
            if "close_ts_ms" in o:
                o["close_ts_ms"] = ms_to_iso(o["close_ts_ms"])
    return {"ohlcs": ohlcs}


def main():
    parser = argparse.ArgumentParser(description="查询单只 ETF OHLC K 线（daec，日期区间）")
    parser.add_argument(
        "--etf",
        required=True,
        help="ETF 标的键，带市场后缀，如 510050.XSHG、159915.XSHE、920036.BJ",
    )
    parser.add_argument(
        "--since",
        required=True,
        help="起始日期，格式 YYYYMMDD，如 20240101",
    )
    parser.add_argument(
        "--until",
        default=None,
        help="结束日期，格式 YYYYMMDD；不传则默认今天",
    )
    parser.add_argument(
        "--interval",
        default="Day",
        choices=["Day", "Week", "Month"],
        help="K 线周期：Day（日线，默认）、Week（周线）、Month（月线）",
    )
    parser.add_argument(
        "--adjust",
        default="Forward",
        choices=["Forward", "Backward", "None"],
        help="复权类型：Forward（前复权，默认）、Backward（后复权）、None（不复权）",
    )
    args = parser.parse_args()

    until = args.until or datetime.now(tz=BEIJING_TZ).strftime("%Y%m%d")
    try:
        result = fetch(args.etf, args.since, until, args.interval, args.adjust)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
