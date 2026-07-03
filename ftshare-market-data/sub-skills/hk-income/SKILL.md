---
name: hk-income
description: 查询港股利润表（港股财报：营业额/收入/毛利/营业利润/税前税后利润/归属股东利润/每股收益等）。支持一般企业(gene)/银行(bank)/保险(insur)。Use when user asks about 港股利润表, 港股营收, 港股净利润, 港股EPS, 港股财报, 某港股财务, hk income statement, hk-income. 注意是"港股"财报（区别于 A 股 stock-income / 美股 us-income）。
---

# 查询港股利润表（宽表，按公司类型分子接口）

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 对外接口-查询港股利润表 |
| 外部接口 | GET /api/v1/market/data/hk/hk-income-{gene\|bank\|insur} |
| 请求方式 | GET |
| 适用场景 | 查询港股上市公司利润表。一般企业 `gene`、银行业 `bank`、保险业 `insur` 字段不同，用 `--company_type` 选择。数据来源 ClickHouse `hkstk_income_gene/bank/insur`。 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| trade_code | string | 否 | 港股代码 | 00700.HK | 支持 `00700.HK` 或 `700` 简写 |
| year | int | 否 | 报告期年份（日历年） | 2025 | 仅当前年及前 2 年；须与 report_type 成对 |
| report_type | string | 否 | 报告类型 | annual | `annual`(年报)/`semi`(半年报)；须与 year 成对，不支持 q1/q3 |
| company_type | string | 否 | 公司类型/子接口 | gene | `gene`(一般企业,默认)/`bank`(银行)/`insur`(保险) |
| start_date | int | 否 | 起始截止日 | 20250101 | YYYYMMDD |
| end_date | int | 否 | 结束截止日 | 20251231 | YYYYMMDD |
| page / page_size | int | 否 | 分页 | 1 / 20 | 默认 1 / 20 |

> **至少需要一个过滤条件**：`trade_code`、`start_date`、`end_date`、或 `year`+`report_type`，否则 400。

## 执行方式

```bash
# 腾讯 00700 全部报告期（最近 3 年）
python scripts/handler.py --trade_code 00700.HK
# 腾讯 2024 年报
python scripts/handler.py --trade_code 00700.HK --year 2024 --report_type annual
# 全市场 2025 年报
python scripts/handler.py --year 2025 --report_type annual --page 1 --page_size 20
# 银行业（如中银香港 2388）
python scripts/handler.py --trade_code 2388 --company_type bank
```

## 响应结构（宽表，一行一个报告期）

```json
{
  "items": [
    { "trade_code": "00700.HK", "security_name": "腾讯控股", "fiscal_y": 2024,
      "rpt_period": "2024-12-31", "report_type": "annual", "publish_date": "2025-03-19",
      "end_date": "2024-12-31", "currency": "CNY",
      "turn_over": "66025688", "operat_profit": "23784512", "earning_aftax": "21909950",
      "prof_sharehlders": "21129830", "eps_basic": "22.46", "eps": "22.32", "dividend_pershare": "4.50" }
  ],
  "total_pages": 5, "total_items": 98
}
```

### 公共字段

`trade_code`、`security_name`、`fiscal_y`(财政年度)、`rpt_period`(报告期描述)、`report_type`、`publish_date`、`end_date`、`currency`。

### 主要财务字段（`gene` 一般企业，均为 Decimal 字符串或 null）

`turn_over` 营业额、`income` 收入、`salescost` 销售成本、`grossprofit` 毛利、`opeexpense_ae` 营业费用、`admexpenses_ae` 行政费用、`rnddexpenses_ae` 研发费用、`operat_profit` 营业利润、`earning_beftax` 税前利润、`tax` 税项、`earning_aftax` 税后利润、`mino_n_profit` 少数股东利润、`prof_sharehlders` 归属股东利润、`eps_basic` 基本EPS、`eps` EPS、`dividend_pershare` 每股股息。

> `bank`/`insur` 字段集不同（银行有净利息收入等，保险有净保费收入等），详见底表。

## 注意事项

- **港股财报是宽表**（一行一个报告期，所有科目为列），非长表 EAV。
- **按公司类型选子接口**：银行用 `--company_type bank`、保险用 `--company_type insur`，否则该行业专用科目为 null。
- `year` 仅支持当前年及前 2 年（如 2026 年时仅 2024/2025/2026）；`year` 与 `report_type` 必须成对。
- 排序：有 `trade_code` 时按 `end_date DESC, publish_date DESC`。
- **所有 Decimal 字段（金额、EPS 等）均为放大整数，实际值 = 返回值 ÷ 10000**（金额→元、EPS→元/股；如腾讯 2024 营收 `6602570000000000` → ÷1e4 = ¥6602.57 亿，中国移动 EPS `63500` → 6.35）。币种见 `currency` 字段（人民币/港元/美元等）。
- `trade_code` 支持简写自动标准化（`700` → `00700.HK`）。
