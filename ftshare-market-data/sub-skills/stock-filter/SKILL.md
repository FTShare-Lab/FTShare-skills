---
name: stock-filter
description: "A 股实时行情筛选接口。当用户需要按单标的代码（symbol）精确查询，或按板块/交易所（board）+ 上市日期起点（listing_date_since）筛选实时行情时使用。传入 symbol 时忽略 board 与 listing_date_since。"
---

# A 股实时行情筛选

## 接口说明

| 项目     | 说明                                                  |
|----------|-------------------------------------------------------|
| 接口名称 | A 股实时行情筛选                                       |
| 外部接口 | `/api/v1/market/data/stock-list/filter`          |
| 请求方式 | GET                                                   |
| 适用场景 | A 股实时行情快照筛选，支持按单标的代码或板块+上市日期筛选 |

## 请求参数

| 参数名              | 类型   | 是否必填 | 描述                | 取值示例     | 备注                                                                |
|---------------------|--------|----------|---------------------|--------------|---------------------------------------------------------------------|
| symbol              | string | 否       | 单标的代码          | 600519.SH    | 支持裸码或带后缀（.SH/.XSHG/.SZ/.XSHE/.BJ/.BJSE）；传入后忽略 board 与 listing_date_since |
| board               | string | 否       | 板块/交易所筛选     | star         | `star` 科创板 / `chi_next` 创业板 / `bjse` 北交所 / `xshg` 沪市 / `xshe` 深市 / `main` 主板 |
| listing_date_since  | string | 否       | 上市日期起点        | 20200101     | YYYYMMDD，筛选此后上市的股票                                          |
| page                | uint32 | 否       | 页码                | 1            | 不设默认/上限，原样透传                                                |
| page_size           | uint32 | 否       | 每页记录数          | 50           | 不设默认/上限，原样透传                                                |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 按单标的查询
python <RUN_PY> stock-filter --symbol 600519.SH --page 1 --page_size 5

# 按板块筛选
python <RUN_PY> stock-filter --board star --page 1 --page_size 5
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

返回扁平分页结构（无 code/message 信封）：

```json
{
    "items": [
        {
            "type": "stock",
            "symbol": "688556.SH",
            "symbol_id": "688556",
            "symbol_name": "高测股份",
            "board": "sh_star",
            "close": "8.5100",
            "open": "9.2200",
            "high": "9.2200",
            "low": "8.5000",
            "prev_close": "9.2200",
            "change": "-0.7100",
            "change_rate": -0.077,
            "amplitude": 0.0781,
            "volume": 28312089,
            "turnover": "250052129.1700",
            "change_rate_day5": -0.212,
            "change_rate_day10": -0.0301,
            "change_rate_day20": -0.2996,
            "change_rate_day60": -0.3459,
            "change_rate_ytd": -0.2469,
            "ts_nanos": 1756704000000000000
        }
    ],
    "total_pages": 122,
    "total_items": 610
}
```

### 顶层字段说明

| 字段名       | 类型  | 是否可为空 | 说明     |
|--------------|-------|------------|----------|
| items        | Array | 否         | 股票行情列表 |
| total_pages  | int   | 否         | 总页数   |
| total_items  | int   | 否         | 总记录数 |

### items 元素字段

| 字段名             | 类型   | 是否可为空 | 说明                                                              |
|--------------------|--------|------------|-------------------------------------------------------------------|
| type               | string | 否         | 标的类型（恒为 stock）                                              |
| symbol             | string | 否         | 标的代码（带交易所后缀）                                            |
| symbol_id          | string | 否         | 标的 ID（纯数字代码）                                               |
| symbol_name        | string | 否         | 标的名称                                                            |
| board              | string | 是         | 板块枚举：sh / sz / sz_chi_next / sh_star / bj                       |
| close              | string | 是         | 收盘价/最新价（元）                                                 |
| open               | string | 是         | 开盘价（元）                                                        |
| high               | string | 是         | 最高价（元）                                                        |
| low                | string | 是         | 最低价（元）                                                        |
| prev_close         | string | 是         | 前收盘价（元）                                                      |
| change             | string | 是         | 涨跌额（元）                                                        |
| change_rate        | float  | 是         | 涨跌幅（原始小数，-0.077 表示 -7.7%）                               |
| amplitude          | float  | 是         | 振幅 =(最高-最低)/前收盘                                            |
| volume             | int64  | 是         | 成交量（股）                                                        |
| turnover           | string | 是         | 成交额（元）                                                        |
| change_rate_day5   | float  | 是         | 5 日涨跌幅                                                          |
| change_rate_day10  | float  | 是         | 10 日涨跌幅                                                         |
| change_rate_day20  | float  | 是         | 20 日涨跌幅                                                         |
| change_rate_day60  | float  | 是         | 60 日涨跌幅                                                         |
| change_rate_ytd    | float  | 是         | 年初至今涨跌幅                                                      |
| ts_nanos           | int64  | 是         | 交易所时间戳（纳秒）                                                |

## 注意事项

- 必须至少指定 `--symbol` 或 `--board`/`--listing_date_since` 其一。
- 传入 `--symbol` 时直接按单标的查询，忽略 `--board` 与 `--listing_date_since`。
- 请求 `board` 取值与响应 `board` 枚举不同：请求用 `star`/`chi_next`/`bjse`/`xshg`/`xshe`/`main`，响应用 `sh`/`sz`/`sz_chi_next`/`sh_star`/`bj`。
- 涨跌幅等比率为原始小数（如 -0.077 表示 -7.7%）。
- 金额字段以字符串返回，保持精度。
- 始终排除退市股与无行情股。
