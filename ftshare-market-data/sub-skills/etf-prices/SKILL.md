---
name: etf-prices
description: 单只 ETF 分钟级分时价格（market.ft.tech）。用户问某只 ETF 分时、当日走势、多日分时、一分钟行情时使用。
---

# ETF 分时价格 - 查询单只 ETF 分钟级分时

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单只 ETF 分时价格（一分钟级别） |
| 外部接口 | `GET /api/v1/market/data/daec/history/prices` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股指定 ETF 在指定时间范围内的分时数据（一分钟一根），用于分时图、当日/多日走势；每条含该分钟的价格、成交量、成交额、均价、时间戳；支持从今天起、从五日前起、从 N 个交易日前起或从指定毫秒时间戳起 |

> 已从 v2（`/app/api/v2/etfs/:etf/prices`）迁移至 daec 统一标的接口（`daec/history/prices?symbol=`）。对外参数契约不变（`--since`/`--since_ts_ms`），脚本内部映射为 daec 的 `range`/`days`/`ts_ms`。

## 2. 请求参数

说明：`etf` 为路径参数（必填）；时间范围由 `since` 或 `since_ts_ms` 二选一指定。脚本内部映射：TODAY→`range=Today`、FIVE_DAYS_AGO→`range=FiveDays`、TRADE_DAYS_AGO(n)→`days=n`、since_ts_ms→`ts_ms=<毫秒>`。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| etf | string | 是 | ETF 标的键（路径参数，带市场后缀） | 510050.XSHG、159915.XSHE、920036.BJ | 沪 .XSHG、深 .XSHE、北交所 .BJ |
| since | string | 条件必填 | 时间范围起点（语义） | TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(10) | 见下方取值说明；与 since_ts_ms 二选一 |
| since_ts_ms | long | 条件必填 | 时间范围起点（毫秒时间戳） | 1735689600000 | 须属于“今天”或“最近一个交易日”；不传 since 时必传 |

**`since` 取值说明**：

| 取值 | 含义 |
|------|------|
| TODAY | 从今天（或最近一个交易日）的第一条分时数据开始 |
| FIVE_DAYS_AGO | 从五个交易日前的第一条分时数据开始（含今天） |
| TRADE_DAYS_AGO(n) | 从 n 个交易日前的第一条分时数据开始（含今天），n 为正整数 |

## 3. 响应说明

返回指定 ETF 的分时价格列表，包装为 `{"prices": [...]}`（daec 返回裸数组，脚本统一包装）：

```json
{
    "prices": [
        { "price": 3.005, "avg_price": 3.003, "volume": 12499680, "turnover": 37543462.22, "ts_ms": "2026-06-22T09:35:00" }
    ]
}
```

### 分时单条（prices 元素）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| price | float | 否 | 该分钟价格 | 元 |
| avg_price | float | 是 | 该分钟均价 | 元 |
| volume | long | 否 | 该分钟成交量 | 份 |
| turnover | float | 否 | 该分钟成交额 | 元 |
| ts_ms | string | 否 | 该分钟时间（北京时间 ISO） | - |

> 注：daec 接口不再返回 `prev_close`（昨收）与 `today`（当前交易日），如需请改用其他接口。

## 4. 用法

通过主目录 `run.py` 调用（必填 `--etf`，且必填 `--since` 或 `--since_ts_ms` 其一）：

```bash
python <RUN_PY> etf-prices --etf 510050.XSHG --since TODAY
python <RUN_PY> etf-prices --etf 159915.XSHE --since FIVE_DAYS_AGO
python <RUN_PY> etf-prices --etf 510050.XSHG --since "TRADE_DAYS_AGO(10)"
python <RUN_PY> etf-prices --etf 510050.XSHG --since_ts_ms 1735689600000
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 注意事项

- `since` 与 `since_ts_ms` 二选一；不传 `since` 时必须传 `since_ts_ms`
- `since_ts_ms` 须属于“今天”或“最近一个交易日”
- 分时为一分钟一根，数据量随时间范围增大而增加
- 执行方式：脚本将每条 `ts_ms`（毫秒）转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）；`since` 与 `since_ts_ms` 二选一，两个都不传或两个都传时报错退出
- **已知问题**：daec 多日分时响应较大（~100KB+）时，服务端偶发传输中断（IncompleteRead），脚本内置 5 次指数退避重试；如仍失败会非零退出
