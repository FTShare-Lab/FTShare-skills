---
name: futures-eod-price
description: 分页查询期货日终行情（开高低收/结算价/前结算价/涨跌额/成交量/成交额/持仓量）。用户提到「期货日终行情」「期货 EOD」「期货日线行情」「futures eod price」时使用。按交易所/合约/精确交易日或日期区间过滤，分页返回，page_size 最大 200，支持 --all 翻页。
---

# 查询期货日终行情

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询期货日终行情 |
| 外部接口 | GET /api/v1/market/data/futures/eod-price |
| 请求方式 | GET |
| 适用场景 | 分页查询期货日终行情，包括开高低收、结算价、成交量、成交额和持仓量等字段 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| exchange | string | 否 | 交易所代码 | `SHFE` | 精确匹配 |
| symbol | string | 否 | 合约代码 | `rb2610` | 精确匹配 |
| trade_date | int | 否 | 精确交易日 | `20260721` | 8 位 YYYYMMDD；**与 start_date/end_date 互斥** |
| start_date | int | 否 | 起始交易日 | `20260701` | 8 位 YYYYMMDD；须与 end_date 同时提供 |
| end_date | int | 否 | 结束交易日 | `20260721` | 8 位 YYYYMMDD；须与 start_date 同时提供 |
| page | int | 否 | 页码 | `1` | 默认 1 |
| page_size | int | 否 | 每页条数 | `50` | 默认 50，最大 200 |

> `trade_date` 不可与 `start_date`/`end_date` 同时使用；同时提供起止日期时需满足 `start_date <= end_date`。

## 执行方式

```bash
# 查某合约某日日终行情
python <RUN_PY> futures-eod-price --exchange SHFE --symbol rb2610 --trade_date 20260721 --page 1 --page_size 20
# 查某合约日期区间
python <RUN_PY> futures-eod-price --symbol rb2610 --start_date 20260701 --end_date 20260721
# 自动翻页获取全量
python <RUN_PY> futures-eod-price --exchange SHFE --all
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 响应结构

返回 `code/message/data`，分页数据位于 `data.records`。

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "pageNum": 1, "pageSize": 20, "total": 1, "pages": 1,
    "records": [
      {
        "trade_date": 20260721, "exchange": "SHFE", "symbol": "rb2610",
        "open_price": "3210", "highest_price": "3212", "lowest_price": "3208", "close_price": "3211",
        "settlement_price": "3205", "pre_settlement_price": "3198",
        "up_down_1": "13", "up_down_2": "7",
        "volume": 1234, "amount": "39621740.00",
        "open_interest": "456789", "open_interest_change": "-1000",
        "updated_at": "2026-07-21 15:00:00"
      }
    ]
  }
}
```

### records 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| trade_date | int | 交易日 |
| exchange | string | 交易所 |
| symbol | string | 合约代码 |
| open_price / highest_price / lowest_price / close_price | string | 开 / 最高 / 最低 / 收 |
| settlement_price / pre_settlement_price | string | 结算价 / 前结算价 |
| up_down_1 / up_down_2 | string | 涨跌额口径一 / 口径二 |
| volume | int64 | 成交量 |
| amount | string | 成交额 |
| open_interest / open_interest_change | string | 持仓量 / 持仓量变化 |
| updated_at | string | 更新时间 |

## 注意事项

- `trade_date` 与 `start_date`/`end_date` 互斥；`start_date`/`end_date` 必须成对且 `start_date <= end_date`。
- `page_size` 最大 200，超过按 200 处理。
- 多数价格/金额字段以字符串返回，`volume` 为 int64。
- HTTP 恒为 200，业务错误通过 `code`/`message` 携带。
