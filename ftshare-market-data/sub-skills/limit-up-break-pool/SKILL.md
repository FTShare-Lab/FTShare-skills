---
name: limit-up-break-pool
description: Get today's limit-up break stock pool (当日炸板股池). Use when user asks about 炸板、涨停炸板、打开涨停、炸板股.
---

# 当日炸板股池

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询当日炸板股池 |
| 外部接口 | `GET /api/v1/market/data/limit-up-break-pool` |
| 请求方式 | GET |
| 适用场景 | 查询当前交易日涨停过且炸板过的 A 股股票列表（`limit_up_enter` 且 `limit_up_break` 均非空） |

## 2. 请求参数

无参数，返回当日全量炸板股池。

## 3. 响应说明

返回 `LimitUpBreakPoolItemResponse` 数组：

| 字段名 | 类型 | 可为空 | 说明 |
|--------|------|--------|------|
| symbol | string | 否 | 标的代码（如 300001.XSHE） |
| trade_date | string | 否 | 交易日期 YYYYMMDD |
| ready | bool | 否 | 当日涨跌停价格是否已就绪 |
| status | string | 否 | 当前状态：炸板后通常为 `normal`，也可能仍在 `limit_up`（反复封板中） |
| limit_up_price | string | 否 | 涨停价（元） |
| limit_up_enter | array[string] | 否 | 进入涨停的时间点，格式 `HH:mm:ss` |
| limit_up_break | array[string] | 否 | 炸板时间数组 |
| first_limit_up_time | string | 是 | 首次封板时间；无封板记录时为 null |
| limit_up_break_count | uint32 | 否 | 炸板次数（涨停封板后被打开的次数） |

示例响应：
```json
[
  {
    "symbol": "300001.XSHE",
    "trade_date": "20260520",
    "ready": true,
    "status": "normal",
    "limit_up_price": "25.00",
    "limit_up_enter": ["09:30:00"],
    "limit_up_break": ["09:45:00"],
    "first_limit_up_time": "09:30:00",
    "limit_up_break_count": 1
  }
]
```

## 4. 用法

```bash
python <RUN_PY> limit-up-break-pool
```

## 5. 注意事项

- 仅返回 `limit_up_enter` 和 `limit_up_break` 均非空的股票
- 炸板后 `status` 通常为 `normal`（已不再涨停），但若反复封板也可能为 `limit_up`
- `limit_up_break` 数组中的每个时间对应一次炸板，长度等于 `limit_up_break_count`
- 展示时可用 `stock-security-info`（`https://ftai.chat`）查股票名称，symbol 需转换：`.XSHG`→`.SH`，`.XSHE`→`.SZ`
