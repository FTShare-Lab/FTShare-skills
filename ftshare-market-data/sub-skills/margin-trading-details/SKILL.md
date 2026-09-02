---
name: margin-trading-details
description: "获取融资融券明细。当用户需要获取 A 股融资融券明细列表，按融资净买入额降序排列，支持分页查询，或了解融资融券明细时使用。"
---

# 获取融资融券明细

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 获取融资融券明细 |
| 外部接口 | `/api/v1/market/data/margin-trading-details` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股融资融券明细列表，按融资净买入额降序排列，支持分页查询 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `page` | int | 是 | 页码，从 1 开始 | `1` | 必须大于等于 1 |
| `page_size` | int | 是 | 每页记录数 | `20` | 必须大于等于 1，建议不超过 100 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 获取第 1 页，每页 20 条
python <RUN_PY> margin-trading-details --page 1 --page_size 20

# 指定分页参数
python <RUN_PY> margin-trading-details --page 2 --page_size 50

# 自动翻页获取全量数据
python <RUN_PY> margin-trading-details --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "items": [
        {
            "date": "2026-03-09",
            "margin_trading_balance": 2440891073,
            "margin_trading_buying_amount": 1423221922,
            "margin_trading_repayment_amount": 874371294,
            "securities_lending_balance_volume": 409500,
            "securities_lending_repayment_volume": 25800,
            "securities_lending_selling_volume": 34500,
            "total_balance": 2453438153,
            "symbol": "600989.SH",
            "symbol_name": "宝丰能源"
        }
    ],
    "total_pages": 99,
    "total_items": 1970
}
```

### 顶层字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `items` | Array | 否 | 当前页融资融券明细列表 |
| `total_pages` | int | 否 | 总页数 |
| `total_items` | int | 否 | 总记录数（未分页前） |

### items 元素字段说明（MarginTradingDetail）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| `date` | String | 否 | 交易日期，格式 `YYYY-MM-DD` | - |
| `margin_trading_balance` | int | 否 | 融资余额 | 元 |
| `margin_trading_buying_amount` | int | 否 | 融资买入额 | 元 |
| `margin_trading_repayment_amount` | int | 否 | 融资偿还额 | 元 |
| `securities_lending_balance_volume` | int | 否 | 融券余量 | 股 |
| `securities_lending_repayment_volume` | int | 否 | 融券偿还量 | 股 |
| `securities_lending_selling_volume` | int | 否 | 融券卖出量 | 股 |
| `total_balance` | int | 否 | 融资融券余额 | 元 |
| `symbol` | String | 否 | 标的代码，带市场后缀 | - |
| `symbol_name` | String | 否 | 标的名称 | - |

## 注意事项

- `page` 和 `page_size` 为必填项
- 返回结果已按**融资净买入额**（`margin_trading_buying_amount - margin_trading_repayment_amount`）降序排列，无需客户端再排序
- 如需全量数据，使用 `--all` 参数自动翻页合并，或按 `page` 递增循环至 `total_pages`
- 金额字段单位为**元**，展示时可按需转换为万元或亿元
