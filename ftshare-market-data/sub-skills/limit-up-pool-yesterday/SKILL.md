---
name: limit-up-pool-yesterday
description: Get yesterday's limit-up stock pool (昨日涨停股池). Use when user asks about 昨日涨停、昨天涨停、前一日涨停、昨日涨停股.
---

# 昨日涨停股池

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询昨日涨停股池 |
| 外部接口 | `GET /api/v1/market/data/limit-up-pool-yesterday` |
| 请求方式 | GET |
| 适用场景 | 查询上一个交易日涨停的 A 股股票列表 |

## 2. 请求参数

无参数，返回上一交易日全量涨停股池。

## 3. 响应说明

返回 `LimitUpPoolItemResponse` 数组，字段与 `limit-up-pool` 完全相同，仅 `trade_date` 为前一交易日：

| 字段名 | 类型 | 可为空 | 说明 |
|--------|------|--------|------|
| symbol | string | 否 | 标的代码（如 600519.XSHG） |
| trade_date | string | 否 | 交易日期 YYYYMMDD（为前一交易日） |
| ready | bool | 否 | 当日涨跌停价格是否已就绪 |
| status | string | 否 | 当前状态：`normal` / `limit_up` / `limit_down` |
| limit_up_price | string | 否 | 涨停价（元） |
| limit_up_enter | array[string] | 否 | 进入涨停的时间点，格式 `HH:mm:ss` |
| limit_up_break | array[string] | 否 | 炸板时间数组（空数组表示未炸板） |
| first_limit_up_time | string | 是 | 首次封板时间；无封板记录时为 null |
| limit_up_break_count | uint32 | 否 | 炸板次数（涨停封板后被打开的次数） |

示例响应：
```json
[
  {
    "symbol": "600519.XSHG",
    "trade_date": "20260519",
    "ready": true,
    "status": "limit_up",
    "limit_up_price": "1850.00",
    "limit_up_enter": ["09:32:15", "10:45:30"],
    "limit_up_break": [],
    "first_limit_up_time": "09:32:15",
    "limit_up_break_count": 0
  }
]
```

## 4. 用法

```bash
python <RUN_PY> limit-up-pool-yesterday
```

## 5. 注意事项

- 与 `limit-up-pool` 数据结构完全相同，仅 `trade_date` 为前一交易日
- 展示时可用 `stock-security-info`（`https://ftai.chat`）查股票名称，symbol 需转换：`.XSHG`→`.SH`，`.XSHE`→`.SZ`
