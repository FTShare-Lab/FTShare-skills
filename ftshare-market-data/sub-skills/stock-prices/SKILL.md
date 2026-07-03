---
name: stock-prices
description: "查询单只股票分时价格（一分钟级别）。当用户需要获取 A 股指定股票在指定时间范围内的分时数据（一分钟一根），用于分时图、当日/多日走势；每条含该分钟的价格、成交量、成交额、均价、时间戳；支持从今天起、从五日前起、从 N 个交易日前起或从指定毫秒时间戳起，或了解单只股票分时价格（一分钟级别）时使用。"
---

# 查询单只股票分时价格（一分钟级别）

## 接口说明

| 项目     | 说明                                                                                                                                                                                                    |
|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 接口名称 | 查询单只股票分时价格（一分钟级别）                                                                                                                                                                        |
| 外部接口 | /api/v1/market/data/daec/history/prices                                                                                                                                                            |
| 请求方式 | GET                                                                                                                                                                                                     |
| 适用场景 | 获取 A 股指定股票在指定时间范围内的分时数据（一分钟一根），用于分时图、当日/多日走势；每条含该分钟的价格、成交量、成交额、均价、时间戳；支持从今天起、从五日前起、从 N 个交易日前起或从指定毫秒时间戳起 |

> 已从 v2（`/api/v2/stocks/:stock/prices`）迁移至 daec 统一标的接口（`daec/history/prices?symbol=`）。对外参数契约不变（`--since`/`--since_ts_ms`），脚本内部映射为 daec 的 `range`/`days`/`ts_ms`。

## 请求参数

说明：stock 为路径参数（必填）；时间范围由 since 或 since_ts_ms 二选一指定（不传 since 时必传 since_ts_ms）。脚本内部映射：TODAY→`range=Today`、FIVE_DAYS_AGO→`range=FiveDays`、TRADE_DAYS_AGO(n)→`days=n`、since_ts_ms→`ts_ms=<毫秒>`。

| 参数名      | 类型   | 是否必填 | 描述                            | 取值示例                               | 备注                                             |
|-------------|--------|----------|---------------------------------|----------------------------------------|--------------------------------------------------|
| stock       | string | 是       | 股票标的键（路径参数，带市场后缀） | 688295.XSHG、000001.SZ、920036.BJ        | 沪 .XSHG、深 .SZ、北交所 .BJ                       |
| since       | string | 条件必填 | 时间范围起点（语义）              | TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(10) | 见下方取值说明；与 since_ts_ms 二选一             |
| since_ts_ms | long   | 条件必填 | 时间范围起点（毫秒时间戳）        | 1735689600000                          | 须属于“今天”或“最近一个交易日”；不传 since 时必传 |

since 取值说明：

| 取值              | 含义                                                   |
|-------------------|--------------------------------------------------------|
| TODAY             | 从今天（或最近一个交易日）的第一条分时数据开始           |
| FIVE_DAYS_AGO     | 从五个交易日前的第一条分时数据开始（含今天）             |
| TRADE_DAYS_AGO(n) | 从 n 个交易日前的第一条分时数据开始（含今天），n 为正整数 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 从今天起的分时
python <RUN_PY> stock-prices --stock 000001.XSHG --since TODAY

# 从五日前起
python <RUN_PY> stock-prices --stock 000001.XSHG --since FIVE_DAYS_AGO

# 从 10 个交易日前起
python <RUN_PY> stock-prices --stock 000001.XSHG --since "TRADE_DAYS_AGO(10)"

# 从指定毫秒时间戳起（不传 since 时必传）
python <RUN_PY> stock-prices --stock 000001.XSHG --since_ts_ms 1735689600000
```

> `<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应说明

返回指定股票的分时价格列表，包装为 `{"prices": [...]}`（daec 返回裸数组，脚本统一包装）：

```json
{
    "prices": [
        { "price": 9.05, "avg_price": 9.03, "volume": 400700, "turnover": 3618333.0, "ts_ms": "2026-06-26T09:35:00" }
    ]
}
```

### 分时单条结构（prices 元素）

| 字段名    | 类型   | 是否可为空 | 说明                      | 单位 |
|-----------|--------|------------|---------------------------|------|
| price     | float  | 否         | 该分钟价格                | 元   |
| avg_price | float  | 是         | 该分钟均价                | 元   |
| volume    | long   | 否         | 该分钟成交量              | 股   |
| turnover  | float  | 否         | 该分钟成交额              | 元   |
| ts_ms     | string | 否         | 该分钟时间（北京时间 ISO）  | -    |

> 注：daec 接口不再返回 `prev_close`（昨收）与 `today`（当前交易日），如需请改用其他接口。

## 注意事项

- stock 为必填；since 与 since_ts_ms 二选一，必须提供其一
- 股票代码需携带市场后缀：沪市 .XSHG、深市 .SZ、北交所 .BJ
- since 为 TRADE_DAYS_AGO(n) 时需带括号和数字，如 TRADE_DAYS_AGO(10)
- 所有接口请求需携带 X-Client-Name: ft-claw 请求头
- 执行方式：脚本将每条 `ts_ms`（毫秒）转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）；`since` 与 `since_ts_ms` 二选一，两个都不传或两个都传时报 `ValueError` 并退出
- **已知问题**：daec 多日分时响应较大（~100KB+）时，服务端偶发传输中断（IncompleteRead），脚本内置 5 次指数退避重试；如仍失败会非零退出
