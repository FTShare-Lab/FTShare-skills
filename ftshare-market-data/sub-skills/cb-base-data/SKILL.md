---
name: cb-base-data
description: 单只可转债基础信息（market.ft.tech）。用户问可转债基础信息、转债详情、某只可转债、转股价、转股价值、到期日、发行规模时使用。
---

# 单只可转债基础信息 - 查询可转债基础信息

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询可转债基础信息 |
| 外部接口 | `GET /api/v1/market/data/cb/cb-base-data` |
| 请求方式 | GET |
| 适用场景 | 根据转债代码获取单只可转债的完整基础信息；数据为前一交易日可转债基础数据 |

## 2. 请求参数

说明：`symbol_code` 为 query 参数（必填）。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol_code | string | 是 | 转债代码，可带交易所后缀 | 110070.SH、110070 | 必填 |

## 3. 响应说明

返回单条可转债基础信息；各字段均可能为 null。日期类为 YYYYMMDD 整数，金额/规模等为数值型。

```json
{
  "cb_name": "恒逸转债",
  "full_name": "恒逸石化股份有限公司可转换公司债券",
  "cb_id": 110070,
  "stock_id": 000703,
  "bond_type": "cb",
  "value_date": 20201102,
  "maturity_date": 20261101,
  "par_value": 100,
  "conversion_price": 11.29,
  "conversion_value": 98.23,
  "conversion_premium": 1.8,
  "total_issue_size": 2000000000,
  "listed_date": 20201116
}
```

### CbBaseDataItem 字段

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| cb_name | string | 否 | 债券简称 | - |
| full_name | string | 否 | 债券全称 | - |
| cb_id | int | 否 | 债券代码 | - |
| stock_id | int | 否 | 转债对应正股代码 | - |
| exchange | int | 否 | 交易所 | - |
| bond_type | string | 否 | 债券分类：cb（可转债券）、eb（可交换债券）、STb（单独交易券） | - |
| trade_type | string | 否 | 交易方式：dirty_price（全价）、clean_price（净价） | - |
| value_date | int | 否 | 起息日 | YYYYMMDD |
| maturity_date | int | 否 | 到期日 | YYYYMMDD |
| par_value | float | 否 | 面值 | - |
| coupon_rate | float | 否 | 发行票面利率 | - |
| coupon_frequency | int | 否 | 付息频率 | - |
| coupon_method | string | 否 | 债券计息方式：stepup_rate、fixed_rate | - |
| total_issue_size | float | 否 | 发行总规模 | - |
| de_listed_date | int | 否 | 债券摘牌日 | YYYYMMDD |
| conversion_start_date | int | 否 | 转换期起始日 | YYYYMMDD |
| conversion_end_date | int | 否 | 转换期截止日 | YYYYMMDD |
| redemption_price | float | 是 | 到期赎回价格 | - |
| issue_price | float | 否 | 发行价格 | - |
| call_protection | float | 否 | 强赎保护期（月计） | 月 |
| listed_date | int | 是 | 上市日，未上市为 null | YYYYMMDD |
| stop_trading_date | int | 是 | 停止交易日，未公布为 null | YYYYMMDD |
| conversion_coefficient | float | 是 | 转股系数 | - |
| conversion_value | float | 是 | 转股价值 | - |
| conversion_premium | float | 是 | 转股溢价率 | - |
| conversion_price | float | 否 | 最新转股价 | - |
| amount_converted | int | 是 | 本期转债已转股金额 | 元 |
| shares_converted | float | 是 | 本期转股股数 | - |
| remaining_amount | int | 是 | 尚未转股的转债金额 | 元 |
| total_amount_converted | int | 是 | 累计已转股金额 | 元 |
| total_shares_converted | float | 是 | 累计转股数 | - |
| issue_method | string | 否 | 发行方式 | - |
| list_announcement_date | int | 否 | 上市公告书发布日 | YYYYMMDD |

## 4. 用法

通过主目录 `run.py` 调用（必填 `--symbol_code`）：

```bash
python <RUN_PY> cb-base-data --symbol_code 110070.SH
python <RUN_PY> cb-base-data --symbol_code 110070
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON；本接口无需额外请求头。

## 5. 请求示例

```
GET /api/v1/market/data/cb/cb-base-data?symbol_code=110070.SH
```

## 6. 注意事项

- 数据为前一交易日可转债基础数据，具体以接口返回为准
- 日期字段（value_date、maturity_date、listed_date 等）为 YYYYMMDD 整数，展示时按需格式化为可读日期
- 发行总规模、转股金额等大数字展示时可按需换算单位（如万、亿）
- 若用户只给转债名称，建议先用 `cb-lists` 查到对应 `cb_id`/交易所，再拼成 `symbol_code`（如 `110070.SH`）调用本接口
