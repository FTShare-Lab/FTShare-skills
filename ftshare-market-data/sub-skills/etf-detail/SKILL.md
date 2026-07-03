---
name: etf-detail
description: Get single ETF detail (单只 ETF 详情). Use when user asks about 某只 ETF 详情、ETF 行情、510050 行情、上证50ETF、ETF 名称/涨跌幅/跟踪指数/市值.
---

# 单只 ETF 详情 - 查询单只 ETF 详情

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单只 ETF 详情 |
| 外部接口 | `GET /api/v1/market/data/daec/etf?symbol=:etf` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股指定 ETF 的详情（名称、行情、盘口、市值、涨跌幅、跟踪指数、投资类型等）；支持通过 masks 按需返回部分字段；带登录态时可能包含是否在默认分组 |

## 2. 请求参数

说明：`etf` 为路径参数（必填），`masks` 为可选项。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| etf | string | 是 | ETF 标的键（路径参数，带市场后缀） | 510050.XSHG、159915.XSHE、920036.BJ | 沪 .XSHG、深 .XSHE、北交所 .BJ |
| masks | string | 否 | 字段掩码，逗号分隔的字段名，仅返回这些字段 | name,symkey,latest,change_rate | 不传则返回全部字段；字段名须匹配正则 `^[a-zA-Z_][a-zA-Z0-9_]*$`，非法字段名会报错 |

## 3. 响应说明

返回单只 ETF 对象。不传 `masks` 时返回全部字段，传 `masks` 时仅返回指定字段；各字段均可能为 null 或不存在。价格类保留 4 位小数。

```json
{
    "name": "上证50ETF",
    "symkey": "510050.XSHG",
    "latest": 2.85,
    "prev_close": 2.845,
    "change_rate": 0.0018,
    "volume": 125000000,
    "turnover": 356000000.0,
    "tracking_index_symkey": "000016.XSHG"
}
```

### 根字段（部分常用）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| name | string | 是 | ETF 名称 | — |
| symkey | string | 是 | 标的键 | — |
| symbol_id | string | 是 | 标的 ID | — |
| ex_id | string | 是 | 市场 ID | — |
| tracking_index_symkey | string | 是 | 跟踪指数标的键 | — |
| latest | float | 是 | 最新价 | 元 |
| close | float | 是 | 收盘价 | 元 |
| open | float | 是 | 开盘价 | 元 |
| high | float | 是 | 最高价 | 元 |
| low | float | 是 | 最低价 | 元 |
| prev_close | float | 是 | 昨收价 | 元 |
| limit_up | float | 是 | 涨停价 | 元 |
| limit_down | float | 是 | 跌停价 | 元 |
| change | float | 是 | 涨跌额 | 元 |
| change_rate | float | 是 | 涨跌幅 | % |
| volume | long | 是 | 成交量 | 份 |
| turnover | float | 是 | 成交额 | 元 |
| turnover_rate | float | 是 | 换手率 | % |
| market_cap_total | float | 是 | 总市值 | 元 |
| market_cap_circulating | float | 是 | 流通市值 | 元 |
| invest_kind | string | 是 | 投资标的类型 | — |
| invest_strategy | string | 是 | 投资策略分类 | — |
| trade_mode | string | 是 | 交易模式 | — |
| is_in_default_choice_group | boolean | 是 | 是否在默认分组（需登录） | — |

## 4. 用法

通过主目录 `run.py` 调用（必填 `--etf`，可选 `--masks`）：

```bash
python <RUN_PY> etf-detail --etf 510050.XSHG
python <RUN_PY> etf-detail --etf 159915.XSHE --masks name,symkey,latest,change_rate,volume,turnover
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 请求示例

```
GET /api/v1/market/data/daec/etf?symbol=510050.XSHG
```

## 6. 注意事项

- 涨跌幅 `change_rate` 等比率字段在接口中可能为小数形式，展示时按需乘以 100 转为百分比
- 成交量、成交额、市值等大数字展示时可按需换算单位（如万、亿）
- 完整字段以代码 `Etf` 为准；未传 `masks` 时返回全部可用字段
