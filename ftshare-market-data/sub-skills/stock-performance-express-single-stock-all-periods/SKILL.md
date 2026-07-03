---
name: stock-performance-express-single-stock-all-periods
description: Get all periods' performance express (业绩快报) for a single stock. Use when user asks about 业绩快报, 单只股票业绩快报, stock performance express, earnings express.
---

# 查询单只股票所有报告期业绩快报（分页）

## 参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `--stock-code` | string | 是 | 股票代码，含市场后缀 | `603323.SH` |
| `--page` | int | 否 | 页码，从 1 开始（默认 1） | `1` |
| `--page-size` | int | 否 | 每页记录数（默认 50） | `50` |

## 用法

从用户问题中提取股票代码，执行：

```bash
python scripts/handler.py --stock-code 603323.SH --page 1 --page-size 50
```

脚本输出带分页信息的 JSON，每项含 `year`、`report_type`、`eps`、`total_revenue`、`net_profit`、`roe` 等字段，以表格展示给用户。

## 注意

- 股票代码格式：6 位数字 + 市场后缀（SH/SZ/BJ）
- `report_type` 取值：`q1`（一季报）、`q2`（半年报）、`q3`（三季报）、`annual`（年报）
- 金额单位为元，同比增长率为小数（如 `-0.14` 表示 `-14%`）
