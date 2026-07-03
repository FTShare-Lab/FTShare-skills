---
name: us-cashflow
description: 查询美股现金流量表（美股财报：经营/投资/筹资活动现金流净额、折旧摊销、资本支出等）。Use when user asks about 美股现金流量表, 美股现金流, 美股经营现金流, 美股资本支出, 美股财报, 某美股现金流, us cash flow statement, us-cashflow. 注意是"美股"财报（区别于 A 股 stock-cashflow）。
---

# 查询美股现金流量表（长表 EAV）

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 对外接口-查询美股现金流量表 |
| 匹配键 | `us-cashflow` |
| 外部接口 | GET /api/v1/market/data/us/us-cashflow |
| 请求方式 | GET |
| 适用场景 | 查询美股上市公司现金流量表（经营/投资/筹资活动现金流净额、折旧摊销、资本支出等），按**财年 + 报告期**组合查询。数据来源 ClickHouse `basedata.usstk_cashflow`。 |

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
# NVDA 2024 财年年报现金流量表
python scripts/handler.py --stock_code NVDA --period 2024 --report_type Q4
# AAPL 2024 财年年报现金流量表
python scripts/handler.py --stock_code AAPL --period 2024 --report_type Q4
# NVDA 全部历史现金流量表
python scripts/handler.py --stock_code NVDA
```

## 响应结构（长表 EAV，每行一个科目）

```json
{
  "items": [
    { "stock_code": "NVDA", "end_date": "2024-01-28", "ind_type": "Q4", "name": "英伟达",
      "ind_name": "net_operacashflow", "ind_value": "...", "report_type": "年报" },
    { "stock_code": "NVDA", "end_date": "2024-01-28", "ind_type": "Q4", "name": "英伟达",
      "ind_name": "net_investcashflow", "ind_value": "...", "report_type": "年报" }
  ],
  "total_pages": 1,
  "total_items": 2
}
```

### 字段说明（每行 EAV）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| stock_code / end_date / ind_type / name / report_type | — | 同 us-income |
| ind_name | string | 科目名（英文），如 `net_operacashflow` |
| ind_value | string | 科目值（字符串，投资/筹资常为负，带 `-`） |

### 主要科目（ind_name）

| 类别 | 科目 |
|---|---|
| 经营 | `depr_amort` 折旧摊销、`working_cap_chg` 营运资金变动、`net_operacashflow` **经营活动现金流净额** |
| 投资 | `capex` 资本性支出、`invest_purs` 投资支付、`net_investcashflow` **投资活动现金流净额** |
| 筹资 | `stock_issue` 发行股票、`stock_repur` 回购、`dividend_paid` 分红、`net_finacashflow` **筹资活动现金流净额** |
| 汇总 | `net_incr_cashequiva` 现金净增加额、`cashequiva_bp`/`cashequiva_ep` 期初/期末现金 |

## 注意事项

- **长表 EAV**、**按报告期分页**、**Q4/Q3 返回累计 + 单季两套**、**美股财年非自然年**：均同 us-income。
- 现金流科目较少（~16 个），一个报告期约展开 10~16 行；`total_items` 是报告期数。
- 数值为字符串；投资/筹资流出常为负；只输出非 0 科目。
- 错误处理：v1 层吞错成 `HTTP 500 + "获取美股现金流量表无数据"`（无原因）；查无数据返回 200 + 空 `items`。排查打 v0 `/api/v0/us/us-cashflow`。
- 覆盖主要美股与中概股，约 5000+ 只。
