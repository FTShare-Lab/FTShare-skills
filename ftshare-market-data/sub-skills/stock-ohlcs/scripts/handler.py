#!/usr/bin/env python3
"""查询单只 A 股股票 OHLC K 线（daec history/ohlcs）"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from http.client import IncompleteRead
from typing import Optional
SAFE_URLOPENER = urllib.request.build_opener()

BEIJING_TZ = timezone(timedelta(hours=8))

DEFAULT_BASE_URL = "https://market.ft.tech/gateway/"
ENDPOINT = "api/v1/market/data/daec/history/ohlcs"

def safe_urlopen(req_or_url):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    allowed = urllib.parse.urlparse(base_url())
    if parsed.scheme != allowed.scheme or parsed.netloc != allowed.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    return SAFE_URLOPENER.open(req_or_url)

HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}

_DATE_RE = re.compile(r"^\d{8}$")


def base_url() -> str:
    return os.environ.get("FTSHARE_BASE_URL", DEFAULT_BASE_URL).rstrip("/") + "/"


def build_url(params: dict) -> str:
    return urllib.parse.urljoin(base_url(), ENDPOINT) + "?" + urllib.parse.urlencode(params)


def ms_to_iso(ms: Optional[int]) -> Optional[str]:
    """将毫秒时间戳转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）。"""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S")


def build_params(
    symbol: str,
    since: Optional[str] = None,
    until: Optional[str] = None,
    interval: str = "Day",
    adjust: Optional[str] = None,
    compat: Optional[str] = None,
    span: Optional[str] = None,
    limit: Optional[int] = None,
    until_ts_ms: Optional[int] = None,
) -> dict:
    """构造 daec history/ohlcs 查询参数。原始模式校验 YYYYMMDD 日期。"""
    if compat != "v2" and not since:
        raise ValueError("since 为原始模式必填参数，格式 YYYYMMDD")
    if since and not _DATE_RE.match(since):
        raise ValueError(f"since 需为 YYYYMMDD（8 位数字）: {since!r}")
    if until and not _DATE_RE.match(until):
        raise ValueError(f"until 需为 YYYYMMDD（8 位数字）: {until!r}")

    params = {"symbol": symbol}
    if since:
        params["since"] = since
    if until:
        params["until"] = until
    if compat:
        params["compat"] = compat
    if span:
        params["span"] = span
    if limit is not None:
        params["limit"] = limit
    if until_ts_ms is not None:
        params["until_ts_ms"] = until_ts_ms
    if compat != "v2" and interval:
        params["interval"] = interval
    if adjust and (compat == "v2" or adjust != "None"):
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


def fetch(
    symbol: str,
    since: Optional[str] = None,
    until: Optional[str] = None,
    interval: str = "Day",
    adjust: Optional[str] = None,
    compat: Optional[str] = None,
    span: Optional[str] = None,
    limit: Optional[int] = None,
    until_ts_ms: Optional[int] = None,
) -> dict:
    params = build_params(symbol, since, until, interval, adjust, compat, span, limit, until_ts_ms)
    url = build_url(params)
    data = _get_json(url)

    if compat == "v2" and isinstance(data, dict):
        return data

    ohlcs = data if isinstance(data, list) else data.get("ohlcs", [])
    for o in ohlcs:
        if isinstance(o, dict):
            if "open_ts_ms" in o:
                o["open_ts_ms"] = ms_to_iso(o["open_ts_ms"])
            if "close_ts_ms" in o:
                o["close_ts_ms"] = ms_to_iso(o["close_ts_ms"])
    return {"ohlcs": ohlcs}


def main():
    parser = argparse.ArgumentParser(description="查询单只 A 股股票 OHLC K 线（daec）")
    parser.add_argument("--symbol", default=None, help="标的代码，如 600000.XSHG")
    parser.add_argument(
        "--stock",
        default=None,
        help="股票标的键，需携带市场后缀，如 688295.XSHG / 000001.SZ / 920036.BJ",
    )
    parser.add_argument(
        "--since",
        default=None,
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
        choices=["Minute", "Day", "Week", "Month"],
        help="原始模式 K 线周期：Minute、Day（日线，默认）、Week（周线）、Month（月线）",
    )
    parser.add_argument(
        "--adjust",
        default="Forward",
        choices=["Forward", "Backward", "None"],
        help="复权类型：Forward（前复权，默认）、Backward（后复权）、None（不复权）",
    )
    parser.add_argument("--compat", choices=["v2"], default=None, help="兼容模式：v2")
    parser.add_argument("--span", choices=["DAY1", "WEEK1", "MONTH1"], default=None, help="v2 兼容模式 K 线周期")
    parser.add_argument("--limit", type=int, default=None, help="v2 兼容模式返回最近 N 根 K 线")
    parser.add_argument("--until_ts_ms", type=int, default=None, help="v2 兼容模式截止毫秒时间戳")
    args = parser.parse_args()

    symbol = args.symbol or args.stock
    if not symbol:
        print("--symbol 为必填参数；仍兼容旧参数 --stock", file=sys.stderr)
        sys.exit(1)

    until = args.until or (None if args.compat == "v2" else datetime.now(tz=BEIJING_TZ).strftime("%Y%m%d"))
    try:
        result = fetch(
            symbol,
            args.since,
            until,
            args.interval,
            args.adjust,
            args.compat,
            args.span,
            args.limit,
            args.until_ts_ms,
        )
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
