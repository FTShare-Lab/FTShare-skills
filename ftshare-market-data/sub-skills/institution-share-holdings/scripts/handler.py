#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v3/market/data/institution/institution-share-holdings'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='机构股本持股')
    parser.add_argument("--institution_id", required=True)
    parser.add_argument("--year", required=True)
    parser.add_argument("--report_type", required=True)
    parser.add_argument("--invest_type", required=True)
    parser.add_argument("--institution_type", required=True)
    parser.add_argument("--institution_code", required=True)
    parser.add_argument("--institution_main_code", required=True)
    parser.add_argument("--institution_name", required=True)
    parser.add_argument("--stock_holding_details", required=True)
    parser.add_argument("--top10_holding_ratio", required=True)
    parser.add_argument("--stock_code", required=True)
    parser.add_argument("--stock_name", required=True)
    parser.add_argument("--holding_shares", required=True)
    parser.add_argument("--market_value", required=True)
    parser.add_argument("--net_value_ratio")
    parser.add_argument("--circulating_shares", required=True)
    parser.add_argument("--total_shares", required=True)
    args = parser.parse_args()
    params = {}
    if args.institution_id is not None: params["institution_id"] = args.institution_id
    if args.year is not None: params["year"] = args.year
    if args.report_type is not None: params["report_type"] = args.report_type
    if args.invest_type is not None: params["invest_type"] = args.invest_type
    if args.institution_type is not None: params["institution_type"] = args.institution_type
    if args.institution_code is not None: params["institution_code"] = args.institution_code
    if args.institution_main_code is not None: params["institution_main_code"] = args.institution_main_code
    if args.institution_name is not None: params["institution_name"] = args.institution_name
    if args.stock_holding_details is not None: params["stock_holding_details"] = args.stock_holding_details
    if args.top10_holding_ratio is not None: params["top10_holding_ratio"] = args.top10_holding_ratio
    if args.stock_code is not None: params["stock_code"] = args.stock_code
    if args.stock_name is not None: params["stock_name"] = args.stock_name
    if args.holding_shares is not None: params["holding_shares"] = args.holding_shares
    if args.market_value is not None: params["market_value"] = args.market_value
    if args.net_value_ratio is not None: params["net_value_ratio"] = args.net_value_ratio
    if args.circulating_shares is not None: params["circulating_shares"] = args.circulating_shares
    if args.total_shares is not None: params["total_shares"] = args.total_shares
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
