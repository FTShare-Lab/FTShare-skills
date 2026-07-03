#!/usr/bin/env python3
"""下载指定 PCF 文件（market.ft.tech）"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import urllib.parse
from typing import Optional
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")

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



def _safe_output_path(path: str, base_dir: Optional[str] = None) -> str:
    """将 output 规范为绝对路径，并限制在 base_dir 内，防止路径遍历。"""
    base_dir = (base_dir or os.getcwd()).rstrip(os.sep)
    base_abs = os.path.abspath(base_dir)
    resolved = os.path.abspath(os.path.normpath(path))
    if os.path.commonpath([base_abs, resolved]) != base_abs:
        print(
            json.dumps({"error": "output path must be under base directory", "base": base_abs}, ensure_ascii=False),
            file=sys.stderr,
        )
        sys.exit(1)
    return resolved


def main():
    parser = argparse.ArgumentParser(description="下载指定 PCF 文件")
    parser.add_argument(
        "--filename",
        required=True,
        help="PCF 文件名，如 pcf_159003_20260309.xml（由 PCF 列表接口 items[].filename 获得）",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="可选，保存到该文件（仅允许当前工作目录下路径）；不传则输出到 stdout",
    )
    args = parser.parse_args()

    if "/" in args.filename or "\\" in args.filename:
        print(json.dumps({"error": "filename 不得包含路径分隔符"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    path = f"/api/v1/market/data/etf-pcf/etf-pcfs/{args.filename}"
    url = BASE_URL + path
    req = urllib.request.Request(url, method="GET")

    try:
        with safe_urlopen(req) as resp:
            data = resp.read()

        if args.output is not None:
            out_path = _safe_output_path(args.output)
            with open(out_path, "wb") as f:
                f.write(data)
            print(json.dumps({"saved_to": os.path.abspath(out_path), "size_bytes": len(data)}, ensure_ascii=False))
        else:
            sys.stdout.buffer.write(data)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
