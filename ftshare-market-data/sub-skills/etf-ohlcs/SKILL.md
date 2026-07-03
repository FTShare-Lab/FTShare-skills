---
name: etf-ohlcs
description: 单只 ETF OHLC K 线（market.ft.tech）。用户问某只 ETF 的 K 线、日线/周线/月线、开高低收、前/后复权时使用。
---

# ETF K 线 - 查询单只 ETF OHLC K 线（daec，日期区间）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单只 ETF OHLC K 线 |
| 外部接口 | `GET /api/v1/market/data/daec/history/ohlcs` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股指定 ETF 在指定日期区间、周期的 K 线（开高低收、成交量、成交额），支持日/周/月线与前/后复权 |

> 已从 v2（`/app/api/v2/etfs/:etf/ohlcs`）迁移至 daec 统一标的接口（`daec/history/ohlcs?symbol=`）。**对外参数契约有变**：由 v2 的 `--span/--limit/--until_ts_ms` 改为 `--since/--until`（YYYYMMDD 日期区间）+ `--interval` + `--adjust`。注意：daec **不支持年线（YEAR1）**，响应**不再含 MA5/MA10/MA20 与 prev_close**。

## 2. 请求参数

说明：`etf` 为路径参数（必填），`since` 必填，`until`/`interval`/`adjust` 可选。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| etf | string | 是 | ETF 标的键（路径参数，带市场后缀） | 510050.XSHG、159915.XSHE、920036.BJ | 沪 .XSHG、深 .XSHE、北交所 .BJ |
| since | string | 是 | 起始日期 YYYYMMDD | 20240101 | - |
| until | string | 否 | 结束日期 YYYYMMDD | 20240131 | 不传则默认今天 |
| interval | string | 否 | K 线周期 | Day | Day（日线，默认）、Week（周线）、Month（月线）；无年线 |
| adjust | string | 否 | 复权类型 | Forward | Forward（前复权，默认）、Backward（后复权）、None（不复权） |

## 3. 响应说明

返回指定 ETF 的 K 线列表，包装为 `{"ohlcs": [...]}`（daec 返回裸数组，脚本统一包装）：

```json
{
    "ohlcs": [
        { "open": "2.85", "high": "2.865", "low": "2.84", "close": "2.862", "volume": 125000000, "turnover": "358000000.0", "open_ts_ms": "2022-04-06T09:30:00", "close_ts_ms": "2022-04-06T15:00:00" }
    ]
}
```

### Ohlc 单条（ohlcs 元素）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| open | string | 否 | 开盘价 | 元 |
| high | string | 否 | 最高价 | 元 |
| low | string | 否 | 最低价 | 元 |
| close | string | 否 | 收盘价 | 元 |
| volume | long | 否 | 成交量 | 份 |
| turnover | string | 否 | 成交额 | 元 |
| open_ts_ms | string | 否 | 该根 K 线开始时间（北京时间 ISO） | - |
| close_ts_ms | string | 否 | 该根 K 线结束时间（北京时间 ISO） | - |

> 注：daec 接口不再返回 `prev_close`、`MA5/MA10/MA20`、`has_last_empty`；价格字段为字符串类型（避免浮点精度丢失）。

## 4. 用法

通过主目录 `run.py` 调用（必填 `--etf`、`--since`）：

```bash
python <RUN_PY> etf-ohlcs --etf 510050.XSHG --since 20240101 --until 20240131
python <RUN_PY> etf-ohlcs --etf 159915.XSHE --since 20240101 --until 20260628 --interval Week
python <RUN_PY> etf-ohlcs --etf 510050.XSHG --since 20230101 --interval Month --adjust Forward
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 注意事项

- `etf`、`since` 为必填；`since`/`until` 需为 YYYYMMDD（8 位数字）
- `interval` 仅支持 Day/Week/Month（daec 无年线）；不传默认 Day
- `adjust` 可选 Forward/Backward/None，默认 Forward（前复权）；None 为不复权（v2 不支持选复权，daec 为增强）
- 执行方式：脚本将每条 `open_ts_ms`/`close_ts_ms`（毫秒）转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）
- **已知问题**：daec 大区间响应（如多年日线，~100KB+）服务端偶发传输中断（IncompleteRead），脚本内置 5 次指数退避重试；如仍失败会非零退出。建议按需缩小日期区间
