---
name: futures-kline-latest
description: 查询期货合约最新一根 1 分钟 K 线（开高低收/成交量/成交额/VWAP/持仓量/结算价/涨跌停价）。用户提到「期货最新K线」「期货实时K线」「期货最新 1min」「futures kline latest」时使用。未找到数据时 data.item 为 null。
---

# 查询期货最新 K 线

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询期货最新 K 线 |
| 外部接口 | GET /api/v1/market/data/futures/kline/latest |
| 请求方式 | GET |
| 适用场景 | 从实时行情表读取指定期货合约最新一根 1 分钟 K 线 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | WIND 合约全码或表内合约代码 | `A2605.DCE` / `a2605` | - |
| interval | string | 否 | K 线周期 | `1min` | 当前仅支持 `1min`，兼容 `1m`，默认 `1min` |

## 执行方式

```bash
python <RUN_PY> futures-kline-latest --symbol A2605.DCE --interval 1min
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 响应结构

外层 `code/message/data`，`data` 为 `{ "item": object|null }`。未找到数据时 `item` 为 `null`。

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "item": {
      "bar_interval": "1min", "symbol": "A2605.DCE", "variety": "a", "exchange": "DCE",
      "datetime": 1784601060000, "trade_date": 20260721,
      "open": 3210.0, "high": 3212.0, "low": 3208.0, "close": 3211.0,
      "volume": 1234, "amount": 39621740.0, "vwap": 3210.84,
      "open_interest": 456789.0,
      "pre_settlement_price": 3198.0, "settlement_price": 3205.0,
      "high_limit_price": 3450.0, "low_limit_price": 2940.0, "pre_close_price": 3200.0,
      "updated_at": 1784601061000
    }
  }
}
```

### item 字段

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
- 单次返回单条；未找到数据时 `data.item` 为 `null`。
- 数据来自实时行情表。
