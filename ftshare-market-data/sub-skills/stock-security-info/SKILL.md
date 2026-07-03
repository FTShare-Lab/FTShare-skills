---
name: stock-security-info
description: "查询单只股票/基金/指数信息。当用户需要按标的代码查询单只股票、基金或指数的实时行情、多周期涨跌幅及估值指标（市盈率、市净率、每股净资产等），或了解单只股票/基金/指数信息时使用。"
---

# 查询单只股票/基金/指数信息

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询单只股票/基金/指数信息 |
| 外部接口 | `https://ftai.chat/api/v1/market/security/{symbol}/info` |
| 请求方式 | GET |
| 适用场景 | 按标的代码查询单只股票、基金或指数的实时行情、多周期涨跌幅及估值指标（市盈率、市净率、每股净资产等） |

> 注意：本接口域名为 `https://ftai.chat`，与其他子 skill 的 `https://market.ft.tech` 不同。

## 请求参数

说明：标的代码通过路径参数 `{symbol}` 传入，无需 Query 参数。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| symbol | string | 是 | 标的代码（路径参数） | 600519.SH | 带市场后缀，如 600519.SH、000001.SZ |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-security-info --symbol 600519.SH
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应说明

返回值为单只股票/基金/指数信息对象，包含实时行情、多周期涨跌幅及估值指标。数据模型如下：

```json
{
    "type": "stock",
    "symbol": "600519.SH",
    "symbol_id": "600519",
    "symbol_name": "贵州茅台",
    "board": "sh",
    "open": "1402.99",
    "high": "1405.99",
    "low": "1398.02",
    "close": "1400.97",
    "prev_close": "1401.88",
    "change": "-0.91",
    "change_rate": -0.000649128313407709,
    "avg": 1401.147216194,
    "amplitude": 0.00568522270094447,
    "volume": 1116784,
    "turnover": "1564778792.69",
    "turnover_rate": 0.000891807524145258,
    "ts_nanos": 1773197525000000000,
    "limit_up": "1542.07",
    "limit_down": "1261.69",
    "change_rate_day5": -0.0176834783584235,
    "change_rate_day10": -0.0448800109080993,
    "change_rate_day20": -0.0182410651716889,
    "change_rate_day60": 0.000676417458856033,
    "change_rate_ytd": -0.0175525946704067,
    "shares": 1252270215,
    "float_a_shares": 1252270215,
    "market_cap": "1754393003108.55",
    "float_a_market_cap": "1754393003108.55",
    "bvps": "181.3261",
    "eps_ttm": "71.8913",
    "pe_ttm": 19.4873371325877,
    "pb": 7.72624569766846,
    "ps_ttm": 9.82430926018285,
    "roe_ttm": 0.350206,
    "bid_ask_ratio": -0.735294117647059,
    "introduction": ""
}
```

### 响应结构（字段说明）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| type | String | 否 | 标的类型。取值：stock（股票）、index（指数）、etf（基金） | - |
| symbol | String | 否 | 标的代码，带市场后缀 | - |
| symbol_id | String | 否 | 标的 ID，不含市场后缀的数字代码 | - |
| symbol_name | String | 否 | 标的名称（股票/基金/指数名称） | - |
| board | String | 是 | 股票板块。取值：sh（上交所主板）、sz（深交所主板）、sz_chi_next（深交所创业板）、sh_star（上交所科创板）、bj（北交所）、hk（港股） | - |
| open | String | 是 | 开盘价 | 元 |
| high | String | 是 | 最高价 | 元 |
| low | String | 是 | 最低价 | 元 |
| close | String | 是 | 收盘价或最新价；公式 = 收盘价.or(最新价).or(前收盘价) | 元 |
| prev_close | String | 是 | 前收盘价。上市首日为发行价；除权(息)日为除权(息)参考价 | 元 |
| change | String | 否 | 涨跌额；公式 = 最新价 - 前收盘价 | 元 |
| change_rate | float | 否 | 涨跌幅；公式 = 涨跌额 / 前收盘价 | 小数 |
| avg | float | 是 | 均价；公式 = 成交额 / 成交量 | 元 |
| amplitude | float | 否 | 振幅；公式 = (最高价 - 最低价) / 前收盘价 | 小数 |
| volume | int | 否 | 成交量 | 股 |
| turnover | String | 否 | 成交额 | 元 |
| turnover_rate | float | 是 | 换手率；公式 = 成交量 / 流通股本 | 小数 |
| ts_nanos | number | 否 | 交易所时间戳，单位纳秒 | - |
| limit_up | String | 是 | 涨停价 | 元 |
| limit_down | String | 是 | 跌停价 | 元 |
| change_rate_day5 | float | 是 | 5 日涨跌幅 | 小数 |
| change_rate_day10 | float | 是 | 10 日涨跌幅 | 小数 |
| change_rate_day20 | float | 是 | 20 日涨跌幅 | 小数 |
| change_rate_day60 | float | 是 | 60 日涨跌幅 | 小数 |
| change_rate_ytd | float | 是 | 年初至今涨跌幅 | 小数 |
| shares | int | 是 | 股本（总股本） | 股 |
| float_a_shares | int | 是 | 流通 A 股股本 | 股 |
| market_cap | String | 是 | 市值；公式 = 股本 × 最新价 | 元 |
| float_a_market_cap | String | 是 | 流通 A 股市值；公式 = 流通 A 股股本 × 最新价 | 元 |
| bvps | String | 是 | 每股净资产 | 元/股 |
| eps_ttm | String | 是 | 每股收益（TTM） | 元/股 |
| pe_ttm | float | 是 | 市盈率（TTM） | - |
| pb | float | 是 | 市净率 | - |
| ps_ttm | float | 是 | 市销率（TTM） | - |
| roe_ttm | float | 是 | 净资产收益率（TTM） | 小数 |
| bid_ask_ratio | float | 是 | 委比；公式 = (买盘量 - 卖盘量) / (买盘量 + 卖盘量) | 小数 |
| introduction | String | 是 | 公司中文简介 | - |

## 注意事项

- 涨跌幅、换手率、振幅等比率字段均为小数形式，展示时乘以 100 转为百分比
- `market_cap`、`turnover` 等大数字为字符串，展示时可按需转换为亿元（除以 1e8）
- `introduction` 可为空字符串 `""`，展示时做空值判断
