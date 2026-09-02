#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v2/market/data/ths-industry-daily-flow'
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr); raise SystemExit(2)
    return key
def safe_urlopen(request, timeout=30):
    url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
    parsed, base = urllib.parse.urlparse(url), urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr); raise SystemExit(1)
    if not isinstance(request, urllib.request.Request): request = urllib.request.Request(url, method="GET")
    request.add_unredirected_header("FTSHARE_API_KEY", _require_api_key())
    request.add_unredirected_header("Content-Type", "application/json")
    return SAFE_URLOPENER.open(request, timeout=timeout)
def main():
    key = _require_api_key(); parser = argparse.ArgumentParser(description='同花顺行业板块资金流日度')
    parser.add_argument("--start_date", required=True)
    parser.add_argument("--end_date", required=True)
    parser.add_argument("--sector_name")
    parser.add_argument("--page")
    parser.add_argument("--page_size")
    parser.add_argument("--total", required=True)
    parser.add_argument("--trade_date", required=True)
    parser.add_argument("--sector_index", required=True)
    parser.add_argument("--change_pct", required=True)
    parser.add_argument("--company_count", required=True)
    parser.add_argument("--inflow", required=True)
    parser.add_argument("--outflow", required=True)
    parser.add_argument("--net_amount", required=True)
    parser.add_argument("--leader_name", required=True)
    parser.add_argument("--leader_change_pct", required=True)
    parser.add_argument("--leader_price", required=True)
    args = parser.parse_args()
    params = {}
    if args.start_date is not None: params["start_date"] = args.start_date
    if args.end_date is not None: params["end_date"] = args.end_date
    if args.sector_name is not None: params["sector_name"] = args.sector_name
    if args.page is not None: params["page"] = args.page
    if args.page_size is not None: params["page_size"] = args.page_size
    if args.total is not None: params["total"] = args.total
    if args.sector_name is not None: params["sector_name"] = args.sector_name
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.sector_index is not None: params["sector_index"] = args.sector_index
    if args.change_pct is not None: params["change_pct"] = args.change_pct
    if args.company_count is not None: params["company_count"] = args.company_count
    if args.inflow is not None: params["inflow"] = args.inflow
    if args.outflow is not None: params["outflow"] = args.outflow
    if args.net_amount is not None: params["net_amount"] = args.net_amount
    if args.leader_name is not None: params["leader_name"] = args.leader_name
    if args.leader_change_pct is not None: params["leader_change_pct"] = args.leader_change_pct
    if args.leader_price is not None: params["leader_price"] = args.leader_price
    query = ("?" + urllib.parse.urlencode(params)) if params else ""
    request = urllib.request.Request(BASE_URL + ENDPOINT + query, headers={**_REQUEST_HEADERS, "FTSHARE_API_KEY": key, "Content-Type": "application/json", "X-Client-Name": "ft-claw"}, method="GET")
    try:
        with safe_urlopen(request) as response: payload = json.loads(response.read().decode())
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr); raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr); raise SystemExit(1)
if __name__ == "__main__": main()
