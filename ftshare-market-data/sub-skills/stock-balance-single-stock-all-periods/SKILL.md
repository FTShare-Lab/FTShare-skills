---
name: stock-balance-single-stock-all-periods
description: Get all periods' balance sheet (资产负债表) for a single stock. Use when user asks about 资产负债表, 单只股票资产负债表, balance sheet, single stock all report periods.
---

# 查询单只股票所有报告期资产负债表

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单票所有报告期资产负债表 |
| 外部接口 | GET /api/v1/market/data/finance/balance |
| 请求方式 | GET |
| 适用场景 | 获取 A 股上市公司单只股票所有报告期的资产负债表，支持沪深京股票 |

## 请求参数

说明：stock_code 为必填项，仅支持单次请求一个股票代码。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| stock_code | string | 是 | 单个股票代码 | 603323.SH | A 股需为 6 位数字+后缀（SH/SZ/BJ），单次仅支持一个代码 |

## 执行方式

```bash
python scripts/handler.py --stock-code 603323.SH
```

## 响应结构

返回报表信息数组及分页信息：

```json
{
  "items": [ { "stock_code", "stock_name", "publish_date", "year", "report_type", "report_type_cn", "report_form_type", "t_assets", "t_equity", ... } ],
  "total_pages": 1,
  "total_items": 23
}
```

### 字段说明（BalanceItem）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| stock_code | String | 否 | 股票交易代码，带 .SZ/.SH/.BJ 后缀 | - |
| stock_name | String | 否 | 上市公司股票名称 | - |
| publish_date | String | 否 | 报告发布日期，YYYY-MM-DD | - |
| year | int | 否 | 报告所属年度 | - |
| report_type | String | 否 | 报告期类型：q1/q2/q3/annual | - |
| report_type_cn | String | 否 | 报告期类型中文：一季报/半年报/三季报/年报 | - |
| report_form_type | String | 否 | 报表类型：合并未调整/合并调整 | - |
| t_assets | float | 否 | 资产总计 | 元 |
| total_assets_yoy | float | 是 | 总资产同比增长率，无上期时为 null | % |
| t_fixed_assets | float | 否 | 固定资产合计 | 元 |
| cash_equivalents | float | 否 | 货币资金 | 元 |
| monetary_funds_yoy | float | 是 | 货币资金同比增长率 | % |
| account_receivable | float | 否 | 应收账款 | 元 |
| accounts_receivable_yoy | float | 是 | 应收账款同比增长率 | % |
| inventory | float | 否 | 存货 | 元 |
| inventory_yoy | float | 是 | 存货同比增长率 | % |
| t_liability | float | 否 | 负债总计 | 元 |
| total_liabilities_yoy | float | 是 | 总负债同比增长率 | % |
| accounts_payable | float | 否 | 应付账款 | 元 |
| accounts_payable_yoy | float | 是 | 应付账款同比增长率 | % |
| advance_receipts | float | 是 | 预收账款 | 元 |
| advance_receipts_yoy | float | 是 | 预收账款同比增长率 | % |
| t_equity | float | 否 | 所有者权益合计 | 元 |
| total_equity_yoy | float | 是 | 所有者权益合计同比增长率 | % |
| asset_liability_ratio | float | 是 | 资产负债率（衍生） | % |

## 注意事项

- 股票代码格式：6 位数字 + 市场后缀（SH=上交所，SZ=深交所，BJ=北交所），单次仅支持一个代码。
- report_type 取值：q1（一季报）、q2（半年报）、q3（三季报）、annual（年报）。
- 金额类字段单位为元；同比、比率类字段单位为 %，无上期数据时可为 null。
