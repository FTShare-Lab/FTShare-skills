---
name: stock-candlesticks-batch
description: 批量获取多只股票/ETF/可转债/指数 K 线 POST 接口（market.ft.tech，stock-candlesticks/batch）。用户问多只标的的 K 线、批量日 K/周 K/月 K/年 K、混合多类证券的 K 线时使用。必填 --symbols、--interval-unit、--until-ts-millis；可选 --interval-value、--adjust-kind、--since-ts-millis、--limit。
---

# 批量股票 K 线 - 批量查询多只标的 K 线（stock-candlesticks/batch）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 批量查询多只标的 K 线（通用） |
| 外部接口 | `POST /api/v1/market/data/stock-candlesticks/batch` |
| 请求方式 | POST（JSON body） |
| 适用场景 | 一次拉取股票 / ETF / 可转债 / 指数等多只标的的分/日/周/月/年 K 线。响应为嵌套数组 `[[symbol, K线数组], ...]`。通用语义，允许不同证券类别混合查询 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbols | string[] | 是 | 标的代码列表 | 600519.SH,510300.SH,113027.SH,000300.SH | 逗号分隔；可混合股票/ETF/可转债/指数 |
| interval_unit | string | 是 | 周期单位 | Day | Minute/Day/Week/Month/Year |
| interval_value | int | 否 | 间隔数值 | 1 | 默认 1；Minute+5 表示 5 分钟 K 线 |
| adjust_kind | string | 否 | 复权类型 | Forward | None（默认）/Forward（前复权）/Backward（后复权） |
| since_ts_millis | int | 否 | 开始时间戳（毫秒） | 1756700000000 | 分钟 K 线与 until 跨度 ≤3 天 |
| until_ts_millis | int | 是 | 结束时间戳（毫秒） | 1756791000000 | - |
| limit | int | 否 | 每个标的返回条数上限 | 2 | 未传 since 和 limit 时每个标的默认最多返回 50 根 |

## 3. 响应说明

响应为二元数组列表，每项结构为 `[symbol, K线数组]`：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| [0] | string | 标的代码；响应统一使用长市场后缀（`.XSHG`/`.XSHE`/`.BJSE`） |
| [1] | array | 该标的的 K 线数组，字段同单只接口 |

K 线单根字段同 `stock-candlesticks`：open / high / low / close / ts_millis / ts_millis_open / turnover / volume。

## 4. 调用方式

```bash
python <RUN_PY> stock-candlesticks-batch --symbols 600519.SH,000001.SZ --interval-unit Day --until-ts-millis 1756791000000 --limit 2
python <RUN_PY> stock-candlesticks-batch --symbols 600519.SH,510300.SH,113027.SH --interval-unit Week --adjust-kind Forward --until-ts-millis 1756791000000 --limit 4
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 注意事项

- `symbols`、`interval_unit`、`until_ts_millis` 必填。
- `symbols` 用逗号分隔；可混合不同证券类别，不做类别校验。
- 响应中的 `symbol` 会规范化为长市场后缀。
- 分钟 K 线（`interval_unit=Minute`）的 `since/until` 跨度硬限制 ≤3 天。
- `interval_value` 仅在 `interval_unit=Minute` 时生效：不传或传 1 为 1 分钟 K，传 5/15/30/60/120 为对应多分钟 K；其他周期忽略该字段。
- 多分钟 K 按北京时间的每个交易日分别聚合，不跨交易日；以 5 分钟 K 为例，首根为 09:30—09:35，开高低收取区间首根开盘价、最高价、最低价、末根收盘价，成交量和成交额按区间求和。
- 默认不复权（None），`Forward` 前复权、`Backward` 后复权。
- 价格字段 JSON 中为字符串以避免精度丢失。
- 如仅需单类标的批量查询，推荐使用对应的专用批量接口（`etf-candlesticks-batch` / `convertible-bond-candlesticks-batch` / `index-candlesticks-batch`）。
