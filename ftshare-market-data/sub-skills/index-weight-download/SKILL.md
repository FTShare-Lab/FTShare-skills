---
name: index-weight-download
description: 根据 url_hash 下载指数权重 Excel xlsx（market.ft.tech）。前置：须先通过 index-weight-list 或 index-weight-summary 取得 url_hash。用户问下载指数权重表、成份权重 xlsx、指数权重 Excel、保存权重文件时使用。
---

# 下载指数权重文件（index-weight-download）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 下载指数权重文件 |
| 外部接口 | `/api/v1/market/data/index/index_weight/{url_hash}` |
| 请求方式 | GET |
| 适用场景 | 根据「分页查询指数权重列表」或「分页查询指数权重汇总」返回的 `url_hash` 下载该期指数权重 Excel（xlsx）二进制文件 |

## 2. 请求参数

说明：`url_hash` 为路径参数，必填。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| url_hash | string | 是 | 列表或汇总接口返回的 url_hash | xyz789 | 路径参数 |

## 3. 响应说明

成功时返回 **Excel（xlsx）** 二进制流。

- 成功：HTTP 200，响应体为 xlsx 文件字节流

## 4. 调用方式

本 handler 与上级 `FTShare-index-data/run.py` 配合使用：

```bash
python <RUN_PY> index-weight-download --url-hash <url_hash>
python <RUN_PY> index-weight-download --url-hash <url_hash> --output ./weights.xlsx
```

其中 `<RUN_PY>` 为 `FTShare-index-data/run.py` 的绝对路径。

- **`--output`**：仅允许保存到**当前工作目录**下的路径；不传则默认为 `{url_hash}.xlsx`。

### 直接执行 handler（调试）

```bash
python scripts/handler.py --url-hash <url_hash> --output ./weights.xlsx
```

## 5. 链路说明

本接口为**权重链末端下载**。  
**前置**：`index-weight-summary` 的 `periods[].url_hash` 或 `index-weight-list` 的 `url_hash` → 传给本接口的 `--url-hash`。

## 6. 请求示例

```
GET /api/v1/market/data/index/index_weight/xyz789
```
