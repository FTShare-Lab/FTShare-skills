---
name: index-description-download
description: 根据 url_hash 下载指数描述 PDF（market.ft.tech）。前置：须先通过 index-description-paginated 取得 url_hash。用户问下载指数描述、指数说明 PDF、指数简介文件、保存指数说明时使用。
---

# 下载指数描述文件（index-description-download）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 下载指数描述文件 |
| 外部接口 | `/api/v1/market/data/index/index_description/{url_hash}` |
| 请求方式 | GET |
| 适用场景 | 根据「分页查询指数描述列表」返回的 `url_hash` 下载对应指数描述文件（内容为 PDF） |

## 2. 请求参数

说明：`url_hash` 为路径参数，必填。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| url_hash | string | 是 | 列表接口返回的 url_hash | abc123def456 | 路径参数 |

## 3. 响应说明

成功时返回 **PDF** 二进制流。

- 成功：HTTP 200，响应体为 PDF 文件字节流

## 4. 调用方式

本 handler 与上级 `FTShare-index-data/run.py` 配合使用：

```bash
python <RUN_PY> index-description-download --url-hash <url_hash>
python <RUN_PY> index-description-download --url-hash <url_hash> --output index-desc.pdf
```

其中 `<RUN_PY>` 为 `FTShare-index-data/run.py` 的绝对路径。

- **`--output`**：仅允许保存到**当前工作目录**下的路径（防止路径遍历）；不传则默认为当前目录 `{url_hash}.pdf`。

### 直接执行 handler（调试）

```bash
python scripts/handler.py --url-hash <url_hash> --output ./desc.pdf
```

（需在 `sub-skills/index-description-download` 目录下执行，或传入脚本完整路径。）

## 5. 链路说明

本接口为**描述链第 2 步**（末端下载）。  
**前置**：`index-description-paginated` → 取得 `url_hash` → 传给本接口的 `--url-hash`。

## 6. 请求示例

```
GET /api/v1/market/data/index/index_description/abc123def456
```
