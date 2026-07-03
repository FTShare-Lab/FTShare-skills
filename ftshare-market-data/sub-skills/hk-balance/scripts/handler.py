#!/usr/bin/env python3
"""查询港股资产负债表（一般企业/银行/保险），宽表，按股票代码/年度+报告类型/日期范围查询"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINTS = {
    "gene": "/api/v1/market/data/hk/hk-balance-gene",
    "bank": "/api/v1/market/data/hk/hk-balance-bank",
    "insur": "/api/v1/market/data/hk/hk-balance-insur",
}
VALID_REPORT_TYPES = {"annual", "semi"}


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


def fetch_page(page: int, page_size: int, company_type: str, **extra) -> dict:
    params = {"page": page, "page_size": page_size}
    params.update({k: v for k, v in extra.items() if v is not None})
    qs = urllib.parse.urlencode(params)
    url = f"{BASE_URL}{ENDPOINTS[company_type]}?{qs}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="查询港股资产负债表（一般企业/银行/保险）")
    parser.add_argument("--trade_code", type=str, default=None,
                        help="港股代码，支持 00700.HK 或 700 简写")
    parser.add_argument("--year", type=int, default=None,
                        help="报告期年份（日历年），仅支持当前年及前 2 年；须与 --report_type 同时出现")
    parser.add_argument("--report_type", type=str, default=None,
                        help="报告类型：annual（年报）/ semi（半年报）；须与 --year 同时出现")
    parser.add_argument("--company_type", type=str, default="gene", choices=["gene", "bank", "insur"],
                        help="公司类型/子接口：gene(一般企业,默认)/bank(银行)/insur(保险)")
    parser.add_argument("--start_date", type=int, default=None, help="起始截止日期 YYYYMMDD")
    parser.add_argument("--end_date", type=int, default=None, help="结束截止日期 YYYYMMDD")
    parser.add_argument("--page", type=int, default=1, help="页码（默认 1）")
    parser.add_argument("--page_size", type=int, default=20, help="每页条数（默认 20）")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量")
    args = parser.parse_args()

    report_type = args.report_type.lower() if args.report_type else None
    if report_type is not None and report_type not in VALID_REPORT_TYPES:
        print(f"错误：--report_type 须为 annual/semi，当前为 [{args.report_type}]", file=sys.stderr)
        sys.exit(1)
    if (args.year is None) != (report_type is None):
        print("错误：--year 与 --report_type 必须同时出现或同时不出现", file=sys.stderr)
        sys.exit(1)
    if not (args.trade_code or args.start_date or args.end_date or args.year):
        print("错误：至少需要一个过滤条件：--trade_code / --start_date / --end_date / --year+--report_type", file=sys.stderr)
        sys.exit(1)

    extra = dict(trade_code=args.trade_code, year=args.year, report_type=report_type,
                 start_date=args.start_date, end_date=args.end_date)

    if args.fetch_all:
        first = fetch_page(1, args.page_size, args.company_type, **extra)
        all_items = list(first.get("items", []))
        total_pages = first.get("total_pages", 1)
        for p in range(2, total_pages + 1):
            all_items.extend(fetch_page(p, args.page_size, args.company_type, **extra).get("items", []))
        result = {"items": all_items, "total_pages": total_pages,
                  "total_items": first.get("total_items", len(all_items))}
    else:
        result = fetch_page(args.page, args.page_size, args.company_type, **extra)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
