---
name: etf-candlesticks-batch
description: 批量获取多只 ETF 历史 K 线 POST 接口（market.ft.tech，etf-candlesticks/batch）。用户问多只 ETF 的 K 线、批量 ETF 日 K/周 K/月 K/年 K、510300 和 159915 一起的 K 线时使用。必填 --symbols、--interval-unit、--until-ts-millis；可选 --interval-value、--adjust-kind、--since-ts-millis、--limit。
---

# 批量 ETF K 线 - 批量查询多只 ETF K 线（etf-candlesticks/batch）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 批量查询多只 ETF K 线 |
| 外部接口 | `POST /api/v1/market/data/etf-candlesticks/batch` |
| 请求方式 | POST（JSON body） |
| 适用场景 | 一次拉取多只 ETF 的分/日/周/月/年 K 线。响应为嵌套数组 `[[symbol, K线数组], ...]`。仅接受 ETF 标的，任一 symbol 非 ETF 时整体返回系统错误 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbols | string[] | 是 | ETF 代码列表 | 510300.XSHG,159915.XSHE | 逗号分隔传入；也接受 `.SH`/`.SZ` 短后缀，响应统一规范化为长后缀 |
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
| [0] | string | ETF 代码；响应统一使用 `.XSHG`、`.XSHE` 等长后缀 |
| [1] | array | 该标的的 K 线数组，字段同单只接口 |

K 线单根字段同 `etf-candlesticks`：open / high / low / close / ts_millis / ts_millis_open / turnover / volume。

## 4. 调用方式

```bash
python <RUN_PY> etf-candlesticks-batch --symbols 510300.XSHG,159915.XSHE --interval-unit Day --until-ts-millis 1756791000000 --limit 2
python <RUN_PY> etf-candlesticks-batch --symbols 510300.XSHG,159915.XSHE --interval-unit Minute --interval-value 5 --adjust-kind Forward --since-ts-millis 1756700000000 --until-ts-millis 1756791000000
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 注意事项

- `symbols`、`interval_unit`、`until_ts_millis` 必填。
- `symbols` 用逗号分隔；任一非 ETF 标的当前外部接口返回系统错误，不静默过滤。
- 响应中的 `symbol` 会规范化为长市场后缀（`.XSHG`/`.XSHE`）。
- 分钟 K 线（`interval_unit=Minute`）的 `since/until` 跨度硬限制 ≤3 天。
- 默认不复权（None），`Forward` 前复权、`Backward` 后复权。
- 价格字段 JSON 中为字符串以避免精度丢失。
