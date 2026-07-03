---
name: eastmoney-hk-index-daily-kline
description: 查询东财港股指数日K线（恒生指数 HSI / 国企指数 HSCEI / 恒生科技 HSTECH 等）：开高低收、成交量、成交额、振幅、涨跌幅、涨跌额、换手率。按指数代码/交易日/日期区间查询。Use when user asks about 港股指数K线, 恒生指数走势, 国企指数日线, 恒生科技指数, HK index kline, HSI/HSCEI/HSTECH, eastmoney-hk-index-daily-kline. 数据源东方财富。
---

# 查询东财港股指数日 K 线

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 对外接口-查询东财港股指数日K线 |
| 匹配键 | `eastmoney-hk-index-daily-kline` |
| 外部接口 | GET /api/v1/market/data/eastmoney-hk-index-daily-kline |
| 请求方式 | GET |
| 适用场景 | 查询港股指数（恒生、国企、恒生科技等）日 K 线：开高低收、成交量、成交额、振幅、涨跌幅、涨跌额、换手率。数据源东方财富，ClickHouse `em_hk_index_daily_kline`。 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| index_code | string | 否 | 指数代码 | HSI | HSI/HSCEI/HSTECH 等；不传返回全部指数 |
| trade_date | string | 否 | 交易日 | 2026-06-15 | YYYY-MM-DD；与 start_date/end_date 互斥 |
| start_date | string | 否 | 区间起始日 | 2026-06-01 | YYYY-MM-DD；需与 end_date 同时提供 |
| end_date | string | 否 | 区间结束日 | 2026-06-15 | YYYY-MM-DD；需与 start_date 同时提供 |
| page / page_size | int | 否 | 分页 | 1 / 50 | 默认 1 / 50，page_size 最大 200 |

| 模式 | 必填参数 | 说明 |
|------|----------|------|
| 按指数历史 | `index_code` | 指定指数全部历史日 K（最常用） |
| 按交易日全市场 | `trade_date` | 某交易日全部港股指数 |
| 按指数+区间 | `index_code` + `start_date` + `end_date` | 指定指数区间走势 |

## 执行方式

```bash
# 恒生指数 HSI 最近日K
python scripts/handler.py --index_code HSI --page 1 --page_size 5
# 某交易日全部港股指数
python scripts/handler.py --trade_date 2026-06-15 --page 1 --page_size 50
# 国企指数 HSCEI 区间走势
python scripts/handler.py --index_code HSCEI --start_date 2026-06-01 --end_date 2026-06-15
```

## 响应结构（信封：code/message/data.records）

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pageNum": 1, "pageSize": 5, "total": 3, "pages": 1,
    "records": [
      { "index_code": "HSCEI", "index_name": "恒生能源业指数", "secid": "124.HSCIEN",
        "trade_date": "2026-06-15", "open": "14439.65", "close": "14293.61",
        "high": "14650.26", "low": "14265.58", "volume": "629796496", "amount": "7337176832",
        "amplitude": "2.61", "change_pct": "-2.95", "change_amt": "-435.09", "turnover": "0" }
    ]
  }
}
```

> ⚠️ 当前页数据在 `data.records`，**不是顶层数组**（与其它 skill 的 `items` 不同）。

### records 字段

`index_code`、`index_name`、`secid`(东财 secid 如 `124.HSI`)、`trade_date`、`open`/`close`/`high`/`low`、`volume`(成交量)、`amount`(成交额)、`amplitude`(振幅%)、`change_pct`(涨跌幅%)、`change_amt`(涨跌额)、`turnover`(换手率%)。所有数值为字符串，无数据为空字符串 `""`。

## 注意事项

- **响应信封不同**：`{code, message, data:{pageNum,pageSize,total,pages,records}}`，数据在 `data.records`。
- 数值字段为字符串；无数据为空字符串（非 null）。
- `change_amt` 是涨跌额（绝对值），`change_pct` 是涨跌幅（%），含义不同。
- `volume`/`amount` 为原始口径；部分指数（如波幅指数 VHSI）成交量为 0 属正常。
- 全量查询数据量大，建议至少传 `index_code` 或 `trade_date`。
- 底表 `ReplacingMergeTree`，带 `FINAL` 去重，同一指数同一交易日只返回最新一条。
