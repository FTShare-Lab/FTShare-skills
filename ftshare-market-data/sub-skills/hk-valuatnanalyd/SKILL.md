---
name: hk-valuatnanalyd
description: 分页查询港股估值分析（market.ft.tech）。可按 trade_code 过滤单票，不传则全市场分页；含 PE/PB/PS、股息率、换手率、市值、波动率等。用户问港股估值、市盈率、市净率、市销率、市现率、股息率、换手率、港股估值列表、00700 PE TTM、港股全市场估值时使用。
---

# 查询港股估值分析（分页）（hk-valuatnanalyd）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询港股估值分析（分页） |
| 外部接口 | `/api/v1/market/data/hk/hk-valuatnanalyd` |
| 请求方式 | GET |
| 适用场景 | 分页查询 `hkstk_valuatnanalyd` 估值分析明细；可按 `trade_code` 过滤单票，不传则返回全市场分页数据 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| trade_code | string | 否 | 港股代码 | 00700.HK | 支持 `700` 或 `00700.HK`，内部规范为 5 位 + `.HK` |
| page | int | 否 | 页码（从 1 开始） | 1 | 默认 `1` |
| page_size | int | 否 | 每页条数 | 20 | 默认 `20` |

## 3. 响应说明

返回值为分页结构 **`PaginatedResponse<HkStkValuatnAnalydItem>`**：`items`、`total_pages`、`total_items`。数值类字段在 JSON 中多为字符串形式（`ApiDecimal` 序列化）。

### PaginatedResponse 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| items | Array | 否 | 当前页数据列表 | - |
| total_pages | int | 否 | 总页数 | - |
| total_items | int | 否 | 总记录数（未分页前） | - |

### HkStkValuatnAnalydItem 结构（items 元素）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| security_name | String | 否 | 证券简称 | - |
| id | int64 | 否 | 记录 ID | - |
| security_id | String | 否 | 证券 ID | - |
| trade_code | String | 否 | 交易代码 | - |
| trade_date | int | 否 | 计算日期，YYYYMMDD（东八区交易日） | - |
| price_close | String | 否 | 收盘价 | 元 |
| minprice_chg | String | 否 | 最小变动价格 | 元 |
| volume | String | 否 | 成交股数 | 股 |
| amount | String | 否 | 成交额 | 元 |
| volatility_y | String | 否 | 波动率（一年） | % |
| hshare_num | String | 否 | 港股股数 | 股 |
| hshare_limit_num | String | 否 | 港股限售股股数 | 股 |
| hshare_mv | String | 否 | 港股市值 | 元 |
| hshare_circ_mv | String | 否 | 港股流通市值 | 元 |
| nonhshare_num | String | 否 | 非港股股数 | 股 |
| ashare_num | String | 否 | A 股股数 | 股 |
| bshare_num | String | 否 | B 股股数 | 股 |
| turnover_rt | String | 否 | 换手率 | % |
| pe_lyr | String | 否 | 静态市盈率 | - |
| forwd_pe | String | 否 | 动态市盈率 | - |
| pe_ttm | String | 否 | 滚动市盈率 | - |
| ps | String | 否 | 市销率 | - |
| ps_ttm | String | 否 | 滚动市销率 | - |
| pb | String | 否 | 市净率 | - |
| pcf | String | 否 | 市现率（经营现金流量净额） | - |
| pcf_ttm | String | 否 | 滚动市现率 | - |
| dividrt_lyr_rpt | String | 否 | 静态股息率（报告期） | % |
| dividrt_ttm | String | 否 | 滚动股息率 | % |
| op_mode | int | 否 | 操作模式 | - |
| update_time | int64 | 否 | 更新时间（东八区），如 20260324120000 → 2026-03-24 12:00:00 +08:00 | - |

## 4. 调用方式

本 handler 与上级 `FTShare-hk-data/run.py` 配合使用：

```bash
# 单票
python <RUN_PY> hk-valuatnanalyd --trade_code 00700.HK --page 1 --page_size 20

# 全市场分页（不传 trade_code）
python <RUN_PY> hk-valuatnanalyd --page 1 --page_size 20
```

其中 `<RUN_PY>` 为 `FTShare-hk-data/run.py` 的绝对路径。

### 直接执行 handler（调试）

```bash
python scripts/handler.py --trade_code 00700.HK --page 1 --page_size 20
```

（需在 `sub-skills/hk-valuatnanalyd` 目录下执行，或传入脚本完整路径。）

## 5. 请求示例

```
GET /api/v1/market/data/hk/hk-valuatnanalyd?trade_code=00700.HK&page=1&page_size=20
```

全市场分页（不传 `trade_code`）：

```
GET /api/v1/market/data/hk/hk-valuatnanalyd?page=1&page_size=20
```
