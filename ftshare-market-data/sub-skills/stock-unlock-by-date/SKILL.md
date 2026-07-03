---
name: stock-unlock-by-date
description: 按解禁日期范围查询限售解禁批次及股东明细（market.ft.tech）。用户问近期解禁、某月解禁、解禁日历、限售股解禁时使用。
---

# 限售解禁 - 按解禁日期范围查询

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 按解禁日期范围查询限售解禁 |
| 外部接口 | `GET /api/v1/market/data/unlock/stock-unlock-by-date` |
| 请求方式 | GET |
| 适用场景 | 按解禁日期范围分页查询限售解禁批次及股东明细 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| start_date | string | 是 | 开始日期 | `2025-06-01` | 格式 YYYY-MM-DD |
| end_date | string | 是 | 结束日期 | `2025-06-30` | 格式 YYYY-MM-DD |
| page | int | 否 | 页码，从 1 开始 | `1` | 默认 1 |
| page_size | int | 否 | 每页条数 | `50` | 默认 50，最大 200 |

## 3. 响应说明

返回 `PaginatedApiResponse` 包装的 JSON 对象。`data.records` 批次结构与 [stock-unlock-by-stock](stock-unlock-by-stock) 一致。

## 4. 用法

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> stock-unlock-by-date --start_date 2025-06-01 --end_date 2025-06-30
python <RUN_PY> stock-unlock-by-date --start_date 2025-06-01 --end_date 2025-06-30 --page 1 --page_size 50
```

## 5. 请求示例

```
GET /api/v1/market/data/unlock/stock-unlock-by-date?start_date=2025-06-01&end_date=2025-06-30&page=1&page_size=50
```
