---
name: us-income
description: 查询美股利润表（美股财报：营业收入/营业成本/毛利/研发费用/净利润/每股收益等）。Use when user asks about 美股利润表, 美股营收, 美股净利润, 美股EPS, 美股财报, 某美股财务数据, us income statement, us-income. 注意是"美股"财报（区别于 A 股 stock-income）。
---

# 查询美股利润表（长表 EAV）

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 对外接口-查询美股利润表 |
| 匹配键 | `us-income` |
| 外部接口 | GET /api/v1/market/data/us/us-income |
| 请求方式 | GET |
| 适用场景 | 查询美股上市公司利润表（营收、成本、毛利、研发费用、净利润、EPS 等），按**财年 + 报告期**组合查询。数据来源 ClickHouse `basedata.usstk_income`。 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| stock_code | string | **是** | 美股代码（纯代码，不带后缀） | NVDA | 必填 |
| period | int | 否 | **财年**（fiscal year） | 2024 | 匹配 `stmt_year`，非自然年 |
| report_type | string | 否 | 报告期类型 | Q4 | `Q1`/`Q2`/`Q3`/`Q4`/`H1`（半年报），大小写不敏感 |
| start_date | int | 否 | 报告期下界（含） | 20240101 | YYYYMMDD，过滤 `end_date` |
| end_date | int | 否 | 报告期上界（含） | 20241231 | YYYYMMDD，过滤 `end_date` |
| page | int | 否 | 页码 | 1 | 默认 1 |
| page_size | int | 否 | 每页**报告期**数 | 50 | 默认 50，最大 500 |

| 模式 | 必填参数 | 说明 |
|------|----------|------|
| 单股财年单期 | `stock_code` + `period` + `report_type` | 最常用 |
| 单股全部历史 | `stock_code` | 全部报告期，按 `end_date` 倒序 |
| 单股日期区间 | `stock_code` + `start_date` + `end_date` | 按报告期 `end_date` 范围 |
| 单股财年全期 | `stock_code` + `period` | 某财年全部报告期 |

## 执行方式

```bash
# NVDA 2024 财年年报
python scripts/handler.py --stock_code NVDA --period 2024 --report_type Q4
# AAPL 2024 财年年报
python scripts/handler.py --stock_code AAPL --period 2024 --report_type Q4
# NVDA 全部历史利润表
python scripts/handler.py --stock_code NVDA
```

## 响应结构（长表 EAV，每行一个科目）

```json
{
  "items": [
    { "stock_code": "NVDA", "end_date": "2024-01-28", "ind_type": "Q4", "name": "英伟达",
      "ind_name": "revenue", "ind_value": "60922000000", "report_type": "年报" },
    { "stock_code": "NVDA", "end_date": "2024-01-28", "ind_type": "Q4", "name": "英伟达",
      "ind_name": "net_income", "ind_value": "29760000000", "report_type": "年报" }
  ],
  "total_pages": 1,
  "total_items": 2
}
```

### 字段说明（每行 EAV）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| stock_code | string | 美股代码 |
| end_date | string | 报告期截止日 `YYYY-MM-DD` |
| ind_type | string | 报告期类型：`Q1`/`Q2`/`Q3`/`Q4`/`H1` |
| name | string | 股票中文名 |
| ind_name | string | 财务科目名（英文），如 `revenue`、`net_income` |
| ind_value | string | 科目值（字符串，负值带 `-`） |
| report_type | string | 报告类型中文：`一季报`/`中报`/`三季报`/`半年报`/`年报` |

### 主要科目（ind_name）

`revenue`/`tot_revenue` 营业收入、`sales_cost` 营业成本、`gross_profit` 毛利、`selling_admin_genexp` 销售管理费用、`researh_develop_exp` 研发费用、`operating_income` 营业利润、`net_income` 净利润、`basic_eps`/`dilute_eps` 基本/稀释每股收益。

## 注意事项

- **长表 EAV**：每行一个科目，`items` 行数 = 该页各报告期科目数之和。
- **分页基于"报告期"，不是"科目行"**：`page_size` 限制报告期数；`items` 实际行数可能 ≫ `page_size`；`total_items` 是报告期数，**不能**用来估算总行数。
- **Q4/Q3 返回累计 + 单季两套**（同 `end_date`、不同 `report_periodid`）：累计=财年初至今，单季=仅本季。`total_items=2` 即指这两套。
- **美股财年非自然年**：`period` 匹配 `stmt_year`，接口按每只股票财年末自动定位（NVDA 财年末 1 月、AAPL 9 月），无需调用方知道财末日。
- 数值字段为字符串；只输出非 0 科目。
- 错误处理：v1 层把底层错误吞成 `HTTP 500 + "获取美股利润表无数据"`（无原因）；`stock_code` 不存在/查无数据不算错误，返回 200 + 空 `items`。排查根因可打 v0 `/api/v0/us/us-income`（返回具体文本）。
- 覆盖主要美股与中概股，约 5000+ 只。
