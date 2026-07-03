---
name: stock-intraday-prices
description: 查询指定 A 股标的 1 分钟分时数据。Use when user asks about 分时价格, 1分钟走势, intraday prices, minute prices, A股分时数据.
---

# 查询指定 A 股标的 1 分钟分时数据

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 标的分时数据 |
| 外部接口 | `GET /api/v1/market/data/daec/history/prices` |
| 请求方式 | GET |
| 适用场景 | 查询指定 A 股标的的 1 分钟价格、均价、成交量、成交额，用于当日或多日分时走势；支持 `compat=v2` 返回旧 v2 风格结构 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 示例 |
|---|---|---|---|---|
| `--symbol` | string | 是 | 标的代码 | `600000.XSHG` |
| `--range` | string | 否 | 预置区间，`Today` / `FiveDays` | `Today` |
| `--days` | int | 否 | 近 N 个交易日至今 | `10` |
| `--ts_ms` | int | 否 | 起始毫秒时间戳 | `1779931980000` |
| `--compat` | string | 否 | 兼容模式，传 `v2` 时启用旧 v2 响应结构 | `v2` |
| `--since` | string | 否 | v2 兼容模式起始参数：`TODAY` / `FIVE_DAYS_AGO` / `TRADE_DAYS_AGO(n)` | `TODAY` |
| `--since_ts_ms` | int | 否 | v2 兼容模式起始毫秒时间戳，优先级高于 `--since` | `1779931980000` |

时间参数优先级与服务端一致：`ts_ms` > `days` > `range`；不传时间参数时使用服务端默认区间。
v2 兼容模式下使用 `--since` / `--since_ts_ms` 传入旧 v2 风格时间参数。

## 执行方式

```bash
python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG
python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --range Today
python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --days 10
python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --ts_ms 1779931980000
python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --compat v2 --since TODAY
python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --compat v2 --since_ts_ms 1779931980000
```

## 响应结构

脚本将服务端裸数组包装为：

```json
{
  "prices": [
    {
      "ts_ms": "2026-06-26T09:35:00",
      "price": 9.05,
      "avg_price": 9.03,
      "volume": 400700,
      "turnover": 3618333.0
    }
  ]
}
```

传 `--compat v2` 时，脚本直接输出服务端兼容对象：

```json
{
  "current_time": "2026-06-29T15:03:10.123456789+08:00",
  "prev_close": 9.16,
  "prices": [
    {"p": 8.75, "v": 294200, "t": 2574250.0, "a": 8.75, "tm": 1782696600000}
  ],
  "today": 20260629
}
```

## 注意事项

- `symbol` 使用 `代码.市场` 格式，如 `600000.XSHG`。
- 原始模式返回的 `ts_ms` 已转换为北京时间 ISO 字符串；`compat=v2` 保留服务端返回字段。
- 如需旧版 `--stock --since` 参数契约，可继续使用既有 `stock-prices` 子 skill。
