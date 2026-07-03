#!/usr/bin/env python3
"""查询美股利润表（长表 EAV，按财年 + 报告期）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/us/us-income"

VALID_REPORT_TYPES = {"Q1", "Q2", "Q3", "Q4", "H1"}


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


def fetch_page(page: int, page_size: int, **extra) -> dict:
    params = {"page": page, "page_size": page_size}
    params.update({k: v for k, v in extra.items() if v is not None})
    qs = urllib.parse.urlencode(params)
    url = f"{BASE_URL}{ENDPOINT}?{qs}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        print("提示：v1 错误信息被统一吞掉；排查根因可打 v0：/api/v0/us/us-income", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="查询美股利润表（长表 EAV，按财年 + 报告期）")
    parser.add_argument("--stock_code", type=str, required=True,
                        help="美股代码（纯代码，不带后缀，如 NVDA），必填")
    parser.add_argument("--period", type=int, default=None,
                        help="财年（fiscal year），如 2024；匹配 stmt_year，非自然年")
    parser.add_argument("--report_type", type=str, default=None,
                        help="报告期：Q1/Q2/Q3/Q4/H1（大小写不敏感）")
    parser.add_argument("--start_date", type=int, default=None,
                        help="报告期下界（含），格式 YYYYMMDD，如 20240101")
    parser.add_argument("--end_date", type=int, default=None,
                        help="报告期上界（含），格式 YYYYMMDD，如 20241231")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page_size", type=int, default=50, help="每页报告期数（默认 50，最大 500）")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全部报告期")
    args = parser.parse_args()

    report_type = None
    if args.report_type is not None:
        report_type = args.report_type.strip().upper()
        if report_type not in VALID_REPORT_TYPES:
            print(f"错误：--report_type 须为 Q1/Q2/Q3/Q4/H1，当前为 [{args.report_type}]", file=sys.stderr)
            sys.exit(1)

    if args.fetch_all:
        first = fetch_page(1, args.page_size, stock_code=args.stock_code, period=args.period,
                           report_type=report_type, start_date=args.start_date, end_date=args.end_date)
        all_items = list(first.get("items", []))
        total_pages = first.get("total_pages", 1)
        for p in range(2, total_pages + 1):
            page_data = fetch_page(p, args.page_size, stock_code=args.stock_code, period=args.period,
                                   report_type=report_type, start_date=args.start_date, end_date=args.end_date)
            all_items.extend(page_data.get("items", []))
        result = {
            "items": all_items,
            "total_pages": total_pages,
            "total_items": first.get("total_items", len(all_items)),
        }
    else:
        result = fetch_page(args.page, args.page_size, stock_code=args.stock_code, period=args.period,
                            report_type=report_type, start_date=args.start_date, end_date=args.end_date)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
