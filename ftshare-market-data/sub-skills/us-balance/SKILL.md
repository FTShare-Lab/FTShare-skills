---
name: us-balance
description: 查询美股资产负债表（美股财报：货币资金/应收/存货/固定资产/商誉/资产总计/负债/所有者权益等）。Use when user asks about 美股资产负债表, 美股资产, 美股负债, 美股所有者权益, 美股财报, 某美股资产负债, us balance sheet, us-balance. 注意是"美股"财报（区别于 A 股 stock-balance）。
---

# 查询美股资产负债表（长表 EAV）

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 对外接口-查询美股资产负债表 |
| 匹配键 | `us-balance` |
| 外部接口 | GET /api/v1/market/data/us/us-balance |
| 请求方式 | GET |
| 适用场景 | 查询美股上市公司资产负债表（资产、负债、所有者权益各科目），按**财年 + 报告期**组合查询。数据来源 ClickHouse `basedata.usstk_balance`。 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| stock_code | string | **是** | 美股代码（纯代码，不带后缀） | NVDA | 必填 |
| period | int | 否 | **财年**（fiscal year） | 2024 | 匹配 `stmt_year`，非自然年 |
| report_type | string | 否 | 报告期类型 | Q4 | `Q1`/`Q2`/`Q3`/`Q4`/`H1`（半年报），大小写不敏感 |
| start_date | int | 否 | 报告期下界（含） | 20240101 | YYYYMMDD |
| end_date | int | 否 | 报告期上界（含） | 20241231 | YYYYMMDD |
| page | int | 否 | 页码 | 1 | 默认 1 |
| page_size | int | 否 | 每页**报告期**数 | 50 | 默认 50，最大 500 |

| 模式 | 必填参数 | 说明 |
|------|----------|------|
| 单股财年单期 | `stock_code` + `period` + `report_type` | 最常用 |
| 单股全部历史 | `stock_code` | 全部报告期，按 `end_date` 倒序 |
| 单股日期区间 | `stock_code` + `start_date` + `end_date` | 按报告期范围 |

## 执行方式

```bash
# NVDA 2024 财年年报资产负债表
python scripts/handler.py --stock_code NVDA --period 2024 --report_type Q4
# AAPL 2024 财年年报资产负债表
python scripts/handler.py --stock_code AAPL --period 2024 --report_type Q4
# NVDA 全部历史资产负债表
python scripts/handler.py --stock_code NVDA
```

## 响应结构（长表 EAV，每行一个科目）

```json
{
  "items": [
    { "stock_code": "NVDA", "end_date": "2024-01-28", "ind_type": "Q4", "name": "英伟达",
      "ind_name": "tot_assets", "ind_value": "...", "report_type": "年报" },
    { "stock_code": "NVDA", "end_date": "2024-01-28", "ind_type": "Q4", "name": "英伟达",
      "ind_name": "tot_liab", "ind_value": "...", "report_type": "年报" }
  ],
  "total_pages": 1,
  "total_items": 1
}
```

### 字段说明（每行 EAV）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| stock_code / end_date / ind_type / name / report_type | — | 同 us-income |
| ind_name | string | 科目名（英文），如 `tot_assets` |
| ind_value | string | 科目值（字符串，负债类可能为负） |

### 主要科目（ind_name）

| 类别 | 科目 |
|---|---|
| 资产 | `tot_cash` 货币资金、`shortterm_invest` 短期投资、`tot_receivable` 应收、`inventory` 存货、`tot_curr_assets` 流动资产合计、`net_propplantequ` 固定资产净额、`goodwill` 商誉、`tot_assets` **资产总计** |
| 负债 | `short_borrowing` 短期借款、`accts_payable` 应付账款、`tot_curr_liab` 流动负债合计、`longterm_debt` 长期借款、`tot_liab` **负债合计** |
| 权益 | `common_stock` 普通股、`add_paidincapital` 资本公积、`retained_profit` 留存收益、`treasury_stock` 库存股、`tot_eq` **所有者权益合计** |

## 注意事项

- **资产负债表是时点数据**：通常只有期末累计值，Q4 一般 `total_items=1`（无单季值），`items` 为该期全部科目（可能几十行）。
- **长表 EAV**、**按报告期分页**、**美股财年非自然年**：均同 us-income。
- 数值为字符串；只输出非 0 科目。
- 错误处理：v1 层吞错成 `HTTP 500 + "获取美股资产负债表无数据"`（无原因）；查无数据返回 200 + 空 `items`。排查打 v0 `/api/v0/us/us-balance`。
- 覆盖主要美股与中概股，约 5000+ 只。
