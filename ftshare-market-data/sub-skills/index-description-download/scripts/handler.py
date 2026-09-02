#!/usr/bin/env python3
"""根据 url_hash 下载指数描述 PDF（market.ft.tech）"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional


def safe_urlopen(req, timeout=30):
    url = req.full_url if isinstance(req, urllib.request.Request) else str(req)
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(req, urllib.request.Request):
        req = urllib.request.Request(url, method="GET")
    for key, value in _REQUEST_HEADERS.items():
        req.add_unredirected_header(key, value)
    return SAFE_URLOPENER.open(req, timeout=timeout)

def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
PATH_PREFIX = "/api/v1/market/data/index/index_description/"


def _safe_output_path(path: str, base_dir: Optional[str] = None) -> str:
    """将 output 规范为绝对路径，并限制在 base_dir 内，防止路径遍历。"""
    base_dir = (base_dir or os.getcwd()).rstrip(os.sep)
    base_abs = os.path.abspath(base_dir)
    resolved = os.path.abspath(os.path.normpath(path))
    if os.path.commonpath([base_abs, resolved]) != base_abs:
        print(
            json.dumps(
                {"error": "output path must be under base directory", "base": base_abs},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    return resolved


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="下载指数描述 PDF（路径参数 url_hash）")
    parser.add_argument(
        "--url-hash",
        required=True,
        help="列表接口 index-description-paginated 返回的 url_hash",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="保存路径（默认当前目录下 {url_hash}.pdf）",
    )
    args = parser.parse_args()

    url_hash = args.url_hash.strip()
    if not url_hash or "/" in url_hash or "\\" in url_hash:
        print(json.dumps({"error": "url_hash 非法"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    raw_output = args.output or f"{url_hash}.pdf"
    output = _safe_output_path(raw_output)

    path = PATH_PREFIX + urllib.parse.quote(url_hash, safe="")
    url = BASE_URL + path
    req = urllib.request.Request(url, method="GET", headers=_REQUEST_HEADERS)
    req.add_header("X-Client-Name", "ft-claw")

    try:
        with safe_urlopen(req, timeout=30) as resp:
            data = resp.read()

        if len(data) < 500 and data[:1] == b"{":
            try:
                err = json.loads(data.decode())
                print(json.dumps(err, ensure_ascii=False, indent=2), file=sys.stderr)
            except Exception:
                print(data.decode(errors="replace"), file=sys.stderr)
            sys.exit(1)

        with open(output, "wb") as f:
            f.write(data)
        print(
            json.dumps(
                {"saved_to": os.path.abspath(output), "size_bytes": len(data)},
                ensure_ascii=False,
            )
        )
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err = json.loads(body)
        except Exception:
            err = {"error": body}
        print(json.dumps(err, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"请求失败: {e.reason}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
