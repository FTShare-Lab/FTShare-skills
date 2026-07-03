---
name: economic-china-forex-gold-monthly
description: Get China forex and gold reserves monthly data (中国外汇与黄金储备 月度). Use when user asks about 外汇储备, 黄金储备, 国家外汇储备, 中国外汇, 中国黄金储备, China forex gold reserves.
---

# 中国经济 - 外汇与黄金储备（月度）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 外汇与黄金储备（月度汇总计算结果） |
| 外部接口 | GET /api/v1/market/data/economic/china-forex-gold |
| 请求方式 | GET |
| 适用场景 | 获取中国国家外汇储备与黄金储备月度数据，含当月值、同比、环比等 |

## 2. 请求参数

说明：该接口无需请求参数。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| - | - | - | 无需参数 | - | - |

## 3. 用法

直接执行：

```bash
python script/handler.py
```

脚本输出 JSON 数组，按时间倒序，每项含 `month`（如 2025年03月份）、`forex_current`（外汇储备当月值）、`forex_yoy`/`forex_mom`（外汇同比/环比 %）、`gold_current`（黄金储备当月值，万盎司）、`gold_yoy`/`gold_mom`（黄金同比/环比 %）、`unit`、`currency`，以表格展示给用户。

## 4. 响应说明

返回值为外汇与黄金储备月度计算结果列表，按时间倒序。

### ForexGoldComputed 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| month | String | 否 | 月份，格式如 2025年03月份 | - |
| forex_current | float | 是 | 国家外汇储备当月值 | 见 unit |
| forex_yoy | float | 是 | 外汇同比 | % |
| forex_mom | float | 是 | 外汇环比 | % |
| gold_current | float | 是 | 黄金储备当月值 | 万盎司 |
| gold_yoy | float | 是 | 黄金同比 | % |
| gold_mom | float | 是 | 黄金环比 | % |
| unit | String | 否 | 货币单位 | - |
| currency | String | 否 | 货币种类 | - |

## 5. 请求示例

```
GET /api/v1/market/data/economic/china-forex-gold
```

## 6. 注意事项

- 返回按月份汇总，格式如「2025年03月份」，列表已按时间倒序，最新月份在前。
- 外汇单位见 `unit`（通常为亿美元），黄金为万盎司，同比/环比单位为 %，各数值字段可为 null。
