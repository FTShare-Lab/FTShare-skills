---
name: stock-income-single-stock-all-periods
description: Get all periods' income statement (利润表) for a single stock. Use when user asks about 利润表, 单只股票利润表, income statement, single stock all report periods.
---

# 查询单只股票所有报告期利润表

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单票所有报告期利润表 |
| 外部接口 | GET /api/v1/market/data/finance/income |
| 请求方式 | GET |
| 适用场景 | 获取 A 股上市公司单只股票所有报告期的利润表，支持沪深京股票 |

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
  "items": [ { "stock_code", "stock_name", "year", "report_type", "report_type_cn", "publish_date", "report_form_type", "t_revenue", "n_profit", ... } ],
  "total_pages": 1,
  "total_items": 23
}
```

### 字段说明（IncomeItem）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| stock_code | String | 否 | 股票交易代码，带 .SZ/.SH/.BJ 后缀 | - |
| stock_name | String | 否 | 上市公司股票名称 | - |
| year | int | 否 | 报告所属年度 | - |
| report_type | String | 否 | 报告期类型：q1/q2/q3/annual | - |
| report_type_cn | String | 否 | 报告期类型中文：一季报/半年报/三季报/年报 | - |
| publish_date | String | 否 | 报告发布日期，YYYY-MM-DD | - |
| report_form_type | String | 否 | 报表类型：合并未调整/合并调整 | - |
| t_revenue | float | 否 | 营业总收入 | 元 |
| t_revenue_yoy | float | 是 | 营业总收入同比增长率，无上期时为 null | % |
| cost | float | 否 | 营业支出（主营业务成本） | 元 |
| cost_yoy | float | 是 | 主营业务成本同比增长率 | % |
| t_cost | float | 否 | 营业总支出 | 元 |
| t_cost_yoy | float | 是 | 营业总支出同比增长率 | % |
| sale_expense | float | 否 | 销售费用 | 元 |
| sale_expense_yoy | float | 是 | 销售费用同比增长率 | % |
| manag_expense | float | 否 | 管理费用 | 元 |
| manag_expense_yoy | float | 是 | 管理费用同比增长率 | % |
| financial_cost | float | 否 | 财务费用 | 元 |
| financial_cost_yoy | float | 是 | 财务费用同比增长率 | % |
| profit | float | 否 | 营业利润 | 元 |
| profit_yoy | float | 是 | 营业利润同比增长率 | % |
| t_profit | float | 否 | 利润总额 | 元 |
| t_profit_yoy | float | 是 | 利润总额同比增长率 | % |
| n_profit | float | 否 | 净利润 | 元 |
| n_profit_yoy | float | 是 | 净利润同比增长率 | % |
| parcomp_n_profit | float | 否 | 扣非归母净利润 | 元 |
| parcomp_n_profit_yoy | float | 是 | 扣非归母净利润同比增长率 | % |

## 注意事项

- 股票代码格式：6 位数字 + 市场后缀（SH=上交所，SZ=深交所，BJ=北交所），单次仅支持一个代码。
- report_type 取值：q1（一季报）、q2（半年报）、q3（三季报）、annual（年报）。
- 金额类字段单位为元；同比类字段单位为 %，无上期数据时为 null。
