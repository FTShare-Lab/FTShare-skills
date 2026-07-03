---
name: limit-down-pool
description: Get today's limit-down stock pool (当日跌停股池). Use when user asks about 跌停、跌停板、跌停股、今日跌停.
---

# 当日跌停股池

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询当日跌停股池 |
| 外部接口 | `GET /api/v1/market/data/limit-down-pool` |
| 请求方式 | GET |
| 适用场景 | 查询当前交易日正在跌停的 A 股股票列表（`limit_down_enter` 非空的股票），包含封板时间、翘板次数、封单资金等字段 |

## 2. 请求参数

无参数，返回当日全量跌停股池。

## 3. 响应说明

返回 `LimitDownPoolItemResponse` 数组：

| 字段名 | 类型 | 可为空 | 说明 |
|--------|------|--------|------|
| symbol | string | 否 | 标的代码（如 000001.XSHE） |
| trade_date | string | 否 | 交易日期 YYYYMMDD |
| ready | bool | 否 | 当日涨跌停价格是否已就绪 |
| status | string | 否 | 当前状态：`normal`（正常）/ `limit_up`（涨停中）/ `limit_down`（跌停中） |
| limit_down_price | string | 否 | 跌停价（元） |
| limit_down_enter | array[string] | 否 | 进入跌停的时间点，格式 `HH:mm:ss` |
| limit_down_break | array[string] | 否 | 翘板时间数组（空数组表示未被翘开） |
| last_limit_down_time | string | 是 | 最后封板时间；无封板记录时为 null |
| limit_down_break_count | uint32 | 否 | 翘板次数（跌停封板后被打开的次数，即翘板次数） |
| limit_down_seal_value | string | 否 | 封单资金（元）；跌停时累加卖一跌停价挂单额，其余为 0 |

示例响应：
```json
[
  {
    "symbol": "000001.XSHE",
    "trade_date": "20260520",
    "ready": true,
    "status": "limit_down",
    "limit_down_price": "9.50",
    "limit_down_enter": ["09:35:00", "10:00:00"],
    "limit_down_break": [],
    "last_limit_down_time": "10:00:00",
    "limit_down_break_count": 0,
    "limit_down_seal_value": "5000000.00"
  }
]
```

## 4. 用法

```bash
python <RUN_PY> limit-down-pool
```

## 5. 注意事项

- 仅返回 `limit_down_enter` 非空的股票
- `limit_down_enter` 数组中的第一个元素为首次跌停时间，`last_limit_down_time` 为最后一次封板时间
- `limit_down_break_count` 为 0 表示一字跌停（从未被翘开）
- `limit_down_seal_value` 封单资金：跌停时累加卖一跌停价挂单额，非跌停状态时为 0
- 展示时可用 `stock-security-info`（`https://ftai.chat`）查股票名称，symbol 需转换：`.XSHG`→`.SH`，`.XSHE`→`.SZ`
