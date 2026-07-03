---
name: stock-cashflow-single-stock-all-periods
description: Get all periods' cash flow statement (现金流量表) for a single stock. Use when user asks about 现金流量表, 单只股票现金流量表, cash flow statement, single stock all report periods.
---

# 查询单只股票所有报告期现金流量表

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单票所有报告期现金流量表 |
| 外部接口 | GET /api/v1/market/data/finance/cashflow |
| 请求方式 | GET |
| 适用场景 | 获取 A 股上市公司单只股票所有报告期的现金流量表，支持沪深京股票 |

## 请求参数

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
  "items": [ { "stock_code", "stock_name", "year", "report_type", "report_type_cn", "publish_date", "detail_report_type", "cash_equ_inc", ... } ],
  "total_pages": 1,
  "total_items": 21
}
```

### 字段说明（CashflowItem）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| stock_code | String | 否 | 股票交易代码，带 .SZ/.SH/.BJ 后缀 | - |
| stock_name | String | 否 | 上市公司股票名称 | - |
| year | int | 否 | 报告所属年度 | - |
| report_type | String | 否 | 报告期类型：q1/q2/q3/annual | - |
| report_type_cn | String | 否 | 报告期类型中文：一季报/半年报/三季报/年报 | - |
| publish_date | String | 否 | 报告发布日期，YYYY-MM-DD | - |
| detail_report_type | String | 否 | 报告明细类型：合并未调整/合并调整 | - |
| cash_equ_inc | float | 否 | 现金及现金等价物净增加额（核心净现金流） | 元 |
| cash_equ_inc_yoy | float | 是 | 净现金流同比增长率，无上期时为 null | % |
| net_oper_cash_flow | float | 否 | 经营活动产生的现金流量净额 | 元 |
| net_oper_cash_flow_ratio | float | 是 | 经营性现金流量净额占净现金流比例 | % |
| goods_sale_render_service_cash | float | 否 | 销售商品、提供劳务收到的现金 | 元 |
| goods_sale_render_service_cash_ratio | float | 是 | 销售商品、提供劳务收到现金占净现金流比例 | % |
| net_invest_cash_flow | float | 否 | 投资活动产生的现金流量净额 | 元 |
| net_invest_cash_flow_ratio | float | 是 | 投资性现金流量净额占净现金流比例 | % |
| invest_proceeds | float | 否 | 取得投资收益收到的现金 | 元 |
| invest_proceeds_ratio | float | 是 | 取得投资收益收到现金占净现金流比例 | % |
| fix_intan_long_pay_cash | float | 否 | 购建固定资产、无形资产等长期资产支付的现金 | 元 |
| fix_intan_long_pay_cash_ratio | float | 是 | 购建长期资产支付现金占净现金流比例 | % |
| net_fin_cash_flow | float | 否 | 筹资活动产生的现金流量净额 | 元 |
| net_fin_cash_flow_ratio | float | 是 | 融资性现金流量净额占净现金流比例 | % |

## 注意事项

- 股票代码格式：6 位数字 + 市场后缀（SH=上交所，SZ=深交所，BJ=北交所），单次仅支持一个代码。
- report_type 取值：q1（一季报）、q2（半年报）、q3（三季报）、annual（年报）。
- 金额类字段单位为元；比率类字段单位为 %，可为 null。
