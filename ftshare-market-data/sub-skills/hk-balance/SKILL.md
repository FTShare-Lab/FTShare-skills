---
name: hk-balance
description: 查询港股资产负债表（港股财报：固定资产/投资性房地产/商誉/存货/应收应付/借款/股本/留存收益/资产总计等）。支持一般企业(gene)/银行(bank)/保险(insur)。Use when user asks about 港股资产负债表, 港股资产, 港股负债, 港股所有者权益, 港股财报, hk balance sheet, hk-balance. 注意是"港股"财报（区别于 A 股 stock-balance / 美股 us-balance）。
---

# 查询港股资产负债表（宽表，按公司类型分子接口）

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 对外接口-查询港股资产负债表 |
| 外部接口 | GET /api/v1/market/data/hk/hk-balance-{gene\|bank\|insur} |
| 请求方式 | GET |
| 适用场景 | 查询港股上市公司资产负债表（时点数据）。`gene` 一般企业 150 字段、`bank` 银行 84 字段、`insur` 保险 85 字段。用 `--company_type` 选择。 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| trade_code | string | 否 | 港股代码 | 00700.HK | 支持 `00700.HK` 或 `700` |
| year | int | 否 | 报告期年份（日历年） | 2025 | 仅当前年及前 2 年；须与 report_type 成对 |
| report_type | string | 否 | 报告类型 | annual | `annual`/`semi`；须与 year 成对 |
| company_type | string | 否 | 公司类型/子接口 | gene | `gene`(默认)/`bank`/`insur` |
| start_date | int | 否 | 起始截止日 | 20250101 | YYYYMMDD |
| end_date | int | 否 | 结束截止日 | 20251231 | YYYYMMDD |
| page / page_size | int | 否 | 分页 | 1 / 20 | 默认 1 / 20 |

> **至少需要一个过滤条件**，否则 400。

## 执行方式

```bash
# 腾讯 00700 资产负债表（最近 3 年）
python scripts/handler.py --trade_code 00700.HK
# 腾讯 2024 年报资产负债表
python scripts/handler.py --trade_code 00700.HK --year 2024 --report_type annual
# 银行业
python scripts/handler.py --trade_code 2388 --company_type bank
```

## 响应结构（宽表，时点数据）

```json
{
  "items": [
    { "trade_code": "00700.HK", "security_name": "腾讯控股", "fiscal_y": 2024,
      "rpt_period": "2024-12-31", "report_type": "annual", "publish_date": "2025-03-19",
      "end_date": "2024-12-31", "currency": "CNY", "company_type": "一般企业", "account_std": "IFRS",
      "fixed_assets": "5286100", "total_assets": "128537200", "accounts_payabl": "3895200",
      "sharecapital": "94200", "retained_profit": "75321800" }
  ],
  "total_pages": 5, "total_items": 98
}
```

### 公共字段

`trade_code`、`security_name`、`publish_date`、`end_date`、`rpt_period`、`fiscal_y`、`company_type`、`report_type`、`currency`、`account_std`。

### 主要财务字段（`gene` 一般企业，Decimal 字符串或 null）

资产：`fixed_assets` 固定资产、`invest_property` 投资性房地产、`total_assets` **资产总计**、商誉、存货、应收/应付等。
负债/权益：`accounts_payabl` 应付账款、`sharecapital` 股本、`retained_profit` 留存收益、`totalintanctliability` 负债及权益总计 等（共 150 字段）。
> `bank`（现金/同业存放/发放贷款/客户存款/已发行债券 等 84 字段）、`insur`（存款/储备金/再保险资产/保险合同负债 等 85 字段）字段集不同。

## 注意事项

- **宽表、时点数据**：通常只有期末值。
- **按公司类型选子接口**（`--company_type`），否则行业专用科目为 null。
- 额外返回 `company_type`（公司类型）和 `account_std`（会计准则）。
- `year` 仅当前年及前 2 年；`year` 与 `report_type` 必须成对；至少一个过滤条件。
- **所有 Decimal 字段（金额、EPS 等）均为放大整数，实际值 = 返回值 ÷ 10000**（金额→元；如腾讯 2024 总资产 `12853720000000000` → ÷1e4 = ¥1.285 万亿）。币种见 `currency` 字段。
- `trade_code` 支持简写自动标准化。
