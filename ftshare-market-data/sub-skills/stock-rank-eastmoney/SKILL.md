---
name: stock-rank-eastmoney
description: 查询东方财富股票人气榜/飙升榜（market.ft.tech），支持 A 股/港股/美股。用户问东财人气榜、东方财富热搜、股票热度飙升时使用。
---

# 东方财富股票排行榜

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 东方财富排行榜 |
| 外部接口 | `GET /api/v1/market/data/eastmoney-rank` |
| 请求方式 | GET |
| 适用场景 | 查询东方财富的股票人气榜、飙升榜，支持 A 股/港股/美股 |

## 2. 请求参数

所有参数均可选。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| rank_group | string | 否 | 榜单组 | `hot` | `hot`（人气榜）/ `up`（飙升榜） |
| market | string | 否 | 市场 | `A` | `A`（A股）/ `HK`（港股）/ `US`（美股） |
| trade_date | string | 否 | 交易日期 | `2026-05-26` | 格式 `YYYY-MM-DD` |

## 3. 响应说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| data.trade_date | string | 是 | 数据日期 |
| data.display_name | string | 是 | 榜单展示名 |
| data.metric_name | string | 是 | 核心指标名（人气分/排名变化） |
| data.total | int | 是 | 返回记录数 |
| data.items[].rank_no | int | 是 | 当前排名 |
| data.items[].rank_change | int | 是 | 排名变化 |
| data.items[].normalized_symbol | string | 是 | 统一股票代码 |
| data.items[].stock_name | string | 是 | 股票简称 |
| data.items[].hot_score | string | 是 | 人气分 |
| data.items[].latest_price | string | 是 | 最新价 |
| data.items[].change_amount | string | 是 | 涨跌额 |
| data.items[].change_pct | string | 是 | 涨跌幅（%） |
| data.items[].raw_symbol | string | 是 | 东财原始代码 |

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "trade_date": "2026-05-26",
    "display_name": "东方财富人气榜-A股",
    "metric_name": "人气分",
    "total": 100,
    "items": [
      {
        "rank_no": 1,
        "rank_change": 0,
        "normalized_symbol": "600584",
        "stock_name": "长电科技",
        "hot_score": "38613573.055414",
        "latest_price": "88.190000",
        "change_amount": "8.020000",
        "change_pct": "10.000000",
        "raw_symbol": "600584"
      }
    ]
  }
}
```

## 4. 用法

通过主目录 `run.py` 调用：

```bash
# A 股人气榜
python <RUN_PY> stock-rank-eastmoney --rank-group hot --market A

# A 股飙升榜
python <RUN_PY> stock-rank-eastmoney --rank-group up --market A

# 港股人气榜
python <RUN_PY> stock-rank-eastmoney --rank-group hot --market HK

# 美股飙升榜
python <RUN_PY> stock-rank-eastmoney --rank-group up --market US

# 指定日期
python <RUN_PY> stock-rank-eastmoney --rank-group hot --market A --trade-date 2026-05-26
```

## 5. 注意事项

- 所有参数均可选，不传时由底层服务提供默认值。
- 接口带短时间缓存，短时间内相同参数的重复请求会命中缓存。
- 数值类字段以字符串形式返回以保持精度。
