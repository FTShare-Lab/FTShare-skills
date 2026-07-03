---
name: eastmoney-board-latest-ohlc
description: "查询东财单板块最新 OHLC。当用户需要查询指定东财板块最新 OHLC 行情数据，支持分页，或了解东财单板块最新 OHLC时使用。"
---

# 查询东财单板块最新 OHLC

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询东财单板块最新 OHLC |
| 外部接口 | `/api/v1/market/data/eastmoney-board-latest-ohlc` |
| 请求方式 | GET |
| 适用场景 | 查询指定东财板块最新 OHLC 行情数据，支持分页 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `board_code` | string | 否 | 板块代码 | `BK1024` | 不传则返回全部板块最新数据 |
| `page` | int | 否 | 页码，从 1 开始 | `1` | 默认 1 |
| `page_size` | int | 否 | 每页记录数 | `20` | 默认 50 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 查询指定板块最新 OHLC
python <RUN_PY> eastmoney-board-latest-ohlc --board_code BK1024

# 查询全部板块最新数据
python <RUN_PY> eastmoney-board-latest-ohlc --page 1 --page_size 20

# 自动翻页获取全量数据
python <RUN_PY> eastmoney-board-latest-ohlc --board_code BK1024 --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "items": [
        {
            "board_code": "BK1024",
            "board_name": "绿色电力",
            "market": 90,
            "date": "2026-05-18",
            "open": "1446.8400",
            "close": "1459.3800",
            "high": "1461.6300",
            "low": "1444.9300",
            "volume": 119798642,
            "turnover": "95526017974.0000",
            "amplitude": 1.15,
            "change_rate": 0.33,
            "change": "4.7900",
            "turnover_rate": 2.34
        }
    ],
    "total_pages": 1,
    "total_items": 1
}
```

### 顶层字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `items` | Array | 否 | 当前页 OHLC 数据列表 |
| `total_pages` | int | 否 | 总页数 |
| `total_items` | int | 否 | 总记录数 |

### items 元素字段说明（BoardLatestOhlc）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| `board_code` | String | 否 | 板块代码 | - |
| `board_name` | String | 否 | 板块名称 | - |
| `market` | int | 否 | 市场编码 | - |
| `date` | String | 否 | 交易日期，格式 `YYYY-MM-DD` | - |
| `open` | String | 否 | 开盘价 | - |
| `close` | String | 否 | 收盘价 | - |
| `high` | String | 否 | 最高价 | - |
| `low` | String | 否 | 最低价 | - |
| `volume` | int | 否 | 成交量 | 股 |
| `turnover` | String | 否 | 成交额 | 元 |
| `amplitude` | float | 否 | 振幅 | % |
| `change_rate` | float | 否 | 涨跌幅 | % |
| `change` | String | 否 | 涨跌额 | - |
| `turnover_rate` | float | 否 | 换手率 | % |

## 注意事项

- 不传 `board_code` 时返回全部板块的最新 OHLC 数据
- 数值型价格和成交额字段对外序列化为字符串
- 板块代码对行业板块和概念板块通用
