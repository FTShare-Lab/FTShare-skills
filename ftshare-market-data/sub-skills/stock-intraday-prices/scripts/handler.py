#!/usr/bin/env python3
"""查询指定 A 股标的 1 分钟分时数据。"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Optional

DEFAULT_BASE_URL = "https://market.ft.tech/gateway/"
ENDPOINT = "api/v1/market/data/daec/history/prices"

BEIJING_TZ = timezone(timedelta(hours=8))
SAFE_URLOPENER = urllib.request.build_opener()

HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}


def present_params(params: dict) -> list[str]:
    return [name for name, value in params.items() if value is not None]


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
    return SAFE_URLOPENER.open(req_or_url, timeout=60)


def base_url() -> str:
    return os.environ.get("FTSHARE_BASE_URL", DEFAULT_BASE_URL).rstrip("/") + "/"


def build_url(params: dict) -> str:
    return urllib.parse.urljoin(base_url(), ENDPOINT) + "?" + urllib.parse.urlencode(params)


def ms_to_iso(ms: Optional[int]) -> Optional[str]:
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S")


def build_params(
    symbol: str,
    range_: str = None,
    days: int = None,
    ts_ms: int = None,
    compat: str = None,
    since: str = None,
    since_ts_ms: int = None,
) -> dict:
    if compat is not None and compat != "v2":
        raise ValueError("compat 仅支持 v2")
    raw_time_params = present_params({"range": range_, "days": days, "ts_ms": ts_ms})
    v2_time_params = present_params({"since": since, "since_ts_ms": since_ts_ms})
    if compat == "v2":
        if raw_time_params:
            raise ValueError("compat=v2 不能与原始模式时间参数混用: " + ", ".join(raw_time_params))
        if len(v2_time_params) > 1:
            raise ValueError("v2 时间参数互斥: " + ", ".join(v2_time_params))
    elif v2_time_params:
        raise ValueError("v2 时间参数需要同时传 --compat v2: " + ", ".join(v2_time_params))
    elif len(raw_time_params) > 1:
        raise ValueError("原始模式时间参数互斥: " + ", ".join(raw_time_params))

    params = {"symbol": symbol}
    if compat:
        params["compat"] = compat
    if since_ts_ms is not None:
        params["since_ts_ms"] = since_ts_ms
    elif since:
        params["since"] = since
    elif ts_ms is not None:
        params["ts_ms"] = ts_ms
    elif days is not None:
        params["days"] = days
    elif range_:
        params["range"] = range_
    return params


def fetch(
    symbol: str,
    range_: str = None,
    days: int = None,
    ts_ms: int = None,
    compat: str = None,
    since: str = None,
    since_ts_ms: int = None,
) -> dict:
    params = build_params(symbol, range_, days, ts_ms, compat, since, since_ts_ms)
    url = build_url(params)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with safe_urlopen(req) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

    if compat == "v2" and isinstance(data, dict):
        return data

    prices = data if isinstance(data, list) else data.get("prices", [])
    for item in prices:
        if isinstance(item, dict) and "ts_ms" in item:
            item["ts_ms"] = ms_to_iso(item["ts_ms"])
    return {"prices": prices}


def main():
    parser = argparse.ArgumentParser(description="查询指定 A 股标的 1 分钟分时数据")
    parser.add_argument("--symbol", required=True, help="标的代码，如 600000.XSHG")
    parser.add_argument("--range", choices=["Today", "FiveDays"], default=None, help="预置区间：Today / FiveDays")
    parser.add_argument("--days", type=int, default=None, help="近 N 个交易日至今")
    parser.add_argument("--ts_ms", type=int, default=None, help="起始毫秒时间戳")
    parser.add_argument("--compat", choices=["v2"], default=None, help="兼容模式：v2")
    parser.add_argument("--since", default=None, help="v2 兼容模式起始参数：TODAY / FIVE_DAYS_AGO / TRADE_DAYS_AGO(n)")
    parser.add_argument("--since_ts_ms", type=int, default=None, help="v2 兼容模式起始毫秒时间戳")
    args = parser.parse_args()

    try:
        result = fetch(args.symbol, args.range, args.days, args.ts_ms, args.compat, args.since, args.since_ts_ms)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
