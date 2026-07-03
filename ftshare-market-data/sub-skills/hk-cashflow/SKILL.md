---
name: hk-cashflow
description: 查询港股现金流量表（港股财报：经营/投资/融资活动净现金流、折旧摊销、资本支出、净现金等，共 111 字段）。Use when user asks about 港股现金流量表, 港股现金流, 港股经营现金流, 港股资本支出, 港股财报, hk cash flow statement, hk-cashflow. 注意是"港股"财报（区别于 A 股 stock-cashflow / 美股 us-cashflow）。本接口用 stock_code（非 trade_code）。
---

# 查询港股现金流量表（单一端点，宽表 111 字段）

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 对外接口-查询港股现金流量表 |
| 匹配键 | `hk-cashflow` |
| 外部接口 | GET /api/v1/market/data/hk/hk-cashflow |
| 请求方式 | GET |
| 适用场景 | 查询港股上市公司现金流量表。**注意：本接口用 `stock_code` 作为股票代码参数（与利润表/资产负债表的 `trade_code` 不同）**。数据来源 ClickHouse `hkstk_cashflow`。 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| stock_code | string | 否 | 港股代码 | 00700.HK | 支持 `00700.HK` 或 `700`；**注意是 stock_code 非 trade_code** |
| year | int | 否 | 报告期年份（日历年） | 2025 | 仅当前年及前 2 年；须与 report_type 成对 |
| report_type | string | 否 | 报告类型 | annual | `annual`/`semi`；须与 year 成对 |
| start_date | int | 否 | 起始截止日 | 20250101 | YYYYMMDD |
| end_date | int | 否 | 结束截止日 | 20251231 | YYYYMMDD |
| page / page_size | int | 否 | 分页 | 1 / 20 | 默认 1 / 20 |

> **至少需要一个过滤条件**，否则 400。

## 执行方式

```bash
# 腾讯 00700 现金流量表（最近 3 年）
python scripts/handler.py --stock_code 00700.HK
# 腾讯 2024 年报现金流
python scripts/handler.py --stock_code 00700.HK --year 2024 --report_type annual
# 全市场 2025 半年报
python scripts/handler.py --year 2025 --report_type semi --page 1 --page_size 20
```

## 响应结构（宽表，共 111 个财务字段）

```json
{
  "items": [
    { "stock_code": "00700.HK", "stock_name": "腾讯控股", "publish_date": "2025-03-19",
      "begin_date": "2024-01-01", "end_date": "2024-12-31", "rpt_period": "2024-12-31",
      "fiscal_y": 2024, "company_type": "一般企业", "report_type": "annual",
      "currency": "CNY", "account_std": "IFRS",
      "earning_bftax": "24825630", "depreciation": "3589200",
      "net_opecflow": "25863400", "net_invbscflow": "-15237800",
      "netcashf_fin": "-6212500", "net_cash": "4408100", "cash_cashequiv": "17248900" }
  ],
  "total_pages": 5, "total_items": 98
}
```

### 公共字段

`stock_code`、`stock_name`、`publish_date`、`begin_date`(报告期开始日，**现金流独有**)、`end_date`、`rpt_period`、`fiscal_y`、`company_type`、`report_type`、`currency`、`account_std`。

### 关键财务字段（共 111 个，Decimal 字符串或 null）

- 经营：`net_opecflow` **经营活动净现金流**、`depreciation`/`depr_amortzon` 折旧摊销、`earning_bftax` 税前利润
- 投资：`net_invbscflow` **投资活动净现金流**、`invt_paycash` 投资支付现金
- 融资：`netcashf_fin` **融资活动净现金流**、`dividpaid_fb` 支付股息、`issue_shares`/`issue_bonds` 发行股/债
- 汇总：`net_cash` 净现金、`beginper_cash`/`cash_endper` 期初/期末现金、`cash_cashequiv` 现金及等价物

## 注意事项

- **宽表（111 字段）**，一行一个报告期。
- **参数名是 `stock_code`（不是 `trade_code`）**，返回字段是 `stock_code`/`stock_name`（不是 `trade_code`/`security_name`）——与利润表/资产负债表不同。
- 额外返回 `begin_date`（报告期开始日）。
- `year` 仅当前年及前 2 年；`year` 与 `report_type` 必须成对；至少一个过滤条件。
- **所有 Decimal 字段（金额、EPS 等）均为放大整数，实际值 = 返回值 ÷ 10000**（金额→元；如腾讯 2024 经营现金流 `2586340000000000` → ÷1e4 = ¥2586.34 亿）。币种见 `currency` 字段。
- `stock_code` 支持简写自动标准化。
