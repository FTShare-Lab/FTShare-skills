#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v2/market/data/intraday-auction-volume'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='连续竞价成交量')
    parser.add_argument("--trade_date")
    parser.add_argument("--page")
    parser.add_argument("--page_size")
    parser.add_argument("--page_num", required=True)
    parser.add_argument("--total", required=True)
    parser.add_argument("--ts_millis", required=True)
    parser.add_argument("--overall", required=True)
    parser.add_argument("--xshg", required=True)
    parser.add_argument("--xshe", required=True)
    parser.add_argument("--bjse", required=True)
    parser.add_argument("--volume", required=True)
    parser.add_argument("--volume_ratio", required=True)
    parser.add_argument("--turnover", required=True)
    parser.add_argument("--turnover_ratio", required=True)
    args = parser.parse_args()
    params = {}
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.page is not None: params["page"] = args.page
    if args.page_size is not None: params["page_size"] = args.page_size
    if args.page_num is not None: params["page_num"] = args.page_num
    if args.page_size is not None: params["page_size"] = args.page_size
    if args.total is not None: params["total"] = args.total
    if args.ts_millis is not None: params["ts_millis"] = args.ts_millis
    if args.overall is not None: params["overall"] = args.overall
    if args.xshg is not None: params["xshg"] = args.xshg
    if args.xshe is not None: params["xshe"] = args.xshe
    if args.bjse is not None: params["bjse"] = args.bjse
    if args.volume is not None: params["volume"] = args.volume
    if args.volume_ratio is not None: params["volume_ratio"] = args.volume_ratio
    if args.turnover is not None: params["turnover"] = args.turnover
    if args.turnover_ratio is not None: params["turnover_ratio"] = args.turnover_ratio
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
