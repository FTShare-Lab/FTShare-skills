---
name: stock-rank-xueqiu
description: 查询雪球平台股票关注度/讨论/交易排行榜（market.ft.tech）。用户问雪球热搜、雪球关注榜、雪球讨论榜、雪球交易榜时使用。
---

# 雪球股票排行榜

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 雪球排行榜 |
| 外部接口 | `GET /api/v1/market/data/xueqiu-rank` |
| 请求方式 | GET |
| 适用场景 | 查询雪球平台的股票关注度、讨论热度、交易热度排行榜 |

## 2. 请求参数

所有参数均可选。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| rank_group | string | 否 | 榜单组 | `follow` | `follow`（关注）/ `tweet`（讨论）/ `deal`（交易） |
| period | string | 否 | 周期 | `7d` | `7d`（本周新增）/ `total`（最热门） |
| trade_date | string | 否 | 交易日期 | `2026-05-26` | 格式 `YYYY-MM-DD` |
| page | int | 否 | 页码 | `1` | 从 1 开始 |
| page_size | int | 否 | 每页条数 | `20` | 最大 100 |

## 3. 响应说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| data.trade_date | string | 是 | 数据日期 |
| data.display_name | string | 是 | 榜单展示名 |
| data.metric_name | string | 是 | 核心指标名（关注度/讨论数/交易数） |
| data.total | int | 是 | 总记录数 |
| data.items[].rank_no | int | 是 | 排名 |
| data.items[].normalized_symbol | string | 是 | 统一股票代码 |
| data.items[].stock_name | string | 是 | 股票简称 |
| data.items[].metric_value | string | 是 | 核心指标值 |
| data.items[].latest_price | string | 是 | 最新价 |
| data.items[].raw_symbol | string | 是 | 雪球原始代码 |

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "trade_date": "2026-05-26",
    "display_name": "雪球关注-本周新增-A股",
    "metric_name": "关注度",
    "total": 5589,
    "items": [
      {
        "rank_no": 1,
        "normalized_symbol": "000725",
        "stock_name": "京东方A",
        "metric_value": "23366.000000",
        "latest_price": "5.770000",
        "raw_symbol": "SZ000725"
      }
    ]
  }
}
```

## 4. 用法

通过主目录 `run.py` 调用：

```bash
# 关注榜-本周新增
python <RUN_PY> stock-rank-xueqiu --rank-group follow --period 7d --page 1 --page-size 20

# 讨论榜-最热门
python <RUN_PY> stock-rank-xueqiu --rank-group tweet --period total

# 交易榜
python <RUN_PY> stock-rank-xueqiu --rank-group deal --period 7d

# 指定日期
python <RUN_PY> stock-rank-xueqiu --rank-group follow --period 7d --trade-date 2026-05-26
```

## 5. 注意事项

- 所有参数均可选，不传时由底层服务提供默认值。
- 接口带短时间缓存，短时间内相同参数的重复请求会命中缓存。
- 数值类字段以字符串形式返回以保持精度。
