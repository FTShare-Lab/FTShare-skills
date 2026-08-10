---
name: futures-kline-intraday
description: 查询期货合约日内 1 分钟 K 线序列（开高低收/成交量/成交额/VWAP/持仓量/结算价/涨跌停价）。用户提到「期货日内K线」「期货分钟K线」「期货 1min K 线」「futures kline intraday」时使用。按毫秒时间戳区间过滤，默认 600 条，最大 1000 条；起止时间跨度不得超过 3 天。
---

# 查询期货日内 K 线

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询期货日内 K 线 |
| 外部接口 | GET /api/v1/market/data/futures/kline/intraday |
| 请求方式 | GET |
| 适用场景 | 从实时行情表查询指定期货合约的 1 分钟 K 线序列，可按毫秒时间戳区间过滤 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | WIND 合约全码或表内合约代码 | `rb2610` / `A2605.DCE` | - |
| interval | string | 否 | K 线周期 | `1min` | 当前仅支持 `1min`，兼容 `1m`，默认 `1min` |
| start | int64 | 否 | 开始时间 | `1784601060000` | 毫秒时间戳，闭区间 |
| end | int64 | 否 | 结束时间 | `1784687460000` | 毫秒时间戳，闭区间 |
| limit | int | 否 | 最大返回条数 | `600` | 默认 600，范围 1~1000 |

> 同时提供 `start` 和 `end` 时，时间跨度不得超过 3 天。

## 执行方式

```bash
# 取最新 600 根 1 分钟 K 线
python <RUN_PY> futures-kline-intraday --symbol rb2610 --interval 1min --limit 600
# 按时间区间过滤
python <RUN_PY> futures-kline-intraday --symbol rb2610 --start 1784601060000 --end 1784687460000
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 响应结构

外层 `code/message/data`，`data` 为 `{ "items": [...] }`。`items` 元素字段与「期货最新K线」的 `item` 相同。

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "bar_interval": "1min", "symbol": "rb2610", "variety": "rb", "exchange": "SHFE",
        "datetime": 1784601060000, "trade_date": 20260721,
        "open": 3210.0, "high": 3212.0, "low": 3208.0, "close": 3211.0,
        "volume": 1234, "amount": 39621740.0, "vwap": 3210.84,
        "open_interest": 456789.0,
        "pre_settlement_price": 3198.0, "settlement_price": 3205.0,
        "high_limit_price": 3450.0, "low_limit_price": 2940.0, "pre_close_price": 3200.0,
        "updated_at": 1784601061000
      }
    ]
  }
}
```

### items 元素字段

| 字段 | 类型 | 说明 |
|------|------|------|
| bar_interval | string | K 线周期 |
| symbol / variety / exchange | string | 合约代码 / 品种 / 交易所 |
| datetime | int64 | K 线时间，毫秒时间戳 |
| trade_date | int | 交易日 YYYYMMDD |
| open / high / low / close | float | 开高低收 |
| volume | int64 | 成交量 |
| amount | float | 成交额 |
| vwap | float | 成交量加权均价 |
| open_interest | float | 持仓量 |
| pre_settlement_price / settlement_price | float | 前结算价 / 结算价 |
| high_limit_price / low_limit_price | float | 涨停价 / 跌停价 |
| pre_close_price | float | 前收盘价 |
| updated_at | int64 | 实时表写入时间，毫秒时间戳 |

## 注意事项

- `interval` 当前仅支持 `1min`（兼容 `1m`）。
- 默认返回 600 条，最多 1000 条。
- `start`/`end` 同时提供时跨度不得超过 3 天，否则 400。
- 数据来自实时行情表，仅保留近期 1 分钟 K 线。
