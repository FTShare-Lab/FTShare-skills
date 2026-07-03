---
name: hk-view
description: 按港股代码查询单票基础视图（market.ft.tech）。含证券简称、板块（主板/创业板）、上市状态、上市日期、总股本、总市值、港股市值/流通市值、关联 A 股代码及 PE/PB/PS、股息率。用户问港股基础信息、某只港股一览、市值、总股本、上市日期、是否退市、主板创业板、关联 A 股时使用。参数 hk_code 如 00700.HK；无数据时接口报错。
---

# 查询港股基础视图（hk-view）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询港股基础视图 |
| 外部接口 | `/api/v1/market/data/hk/hk-view` |
| 请求方式 | GET |
| 适用场景 | 按港股代码查询单票基础视图信息，含证券简称、板块、上市状态、股本结构、港股市值及主要估值指标等 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| hk_code | string | 是 | 港股代码 | 00700.HK | 如 `00700.HK` |

## 3. 响应说明

返回值为 **`HkStockViewResponse`** 对象；查无数据时接口报错（如 `hk_code not found`）。

### 数字/枚举字段含义（与行情侧 `HKStockDailyDataV1` 注释对齐）

线上 JSON 里部分整型枚举可能被序列化为 **字符串**（如 `"1"`），含义如下表。

| 字段 | 取值 | 含义 |
|------|------|------|
| **board_type** | `1` | 主板 |
| | `2` | 创业板 |
| **status** | `1` | 正常上市 |
| | `2` | 终止上市 |
| | `3` | 暂停上市 |
| | `4` | 未上市 |
| **listed_date** | 如 `20040616` | 上市日期，**YYYYMMDD** 整数 |
| **de_listed_date** | `0` 或缺省语义 | 无退市；若有退市则为 **YYYYMMDD** |
| **trade_date** | 如 `20260323` | 交易/计算日期，**YYYYMMDD**（东八区交易日） |

日行情结构 `HKStockDailyDataV1` 中还有 **`symbol_id`**（如整数 `700`）、**`exchange`**（交易所代码，`i16`）等；**`hk-view`** 以 `trade_code`（规范为 5 位 + `.HK`）为主键展示，不直接返回 `symbol_id` / `exchange`。**`ashare_code`** 在库中可为 `(symbol_id, exchange_id)` 二元组，接口侧常以 **字符串** 形式返回（可能为空字符串）。

### HkStockViewResponse 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| trade_code | String | 否 | 交易代码 | - |
| security_name | String | 否 | 证券简称 | - |
| trade_date | int | 否 | 交易/计算日期，YYYYMMDD | - |
| board_type | String | 否 | 板块类别，见上表 `1`/`2` | - |
| status | String | 否 | 证券状态，见上表 `1`–`4` | - |
| listed_date | int | 否 | 上市日期，YYYYMMDD | - |
| de_listed_date | int | 否 | 退市日期，YYYYMMDD（无则可为 0） | - |
| ashare_code | String | 否 | 关联 A 股代码 | - |
| total_share_num | float | 否 | 总股本 | 股 |
| total_mv | float | 否 | 总市值 | 元 |
| hshare_num | float | 否 | 港股股数 | 股 |
| hshare_limit_num | float | 否 | 港股限售股股数 | 股 |
| hshare_mv | float | 否 | 港股市值 | 元 |
| hshare_circ_mv | float | 否 | 港股流通市值 | 元 |
| nonhshare_num | float | 否 | 非港股股数 | 股 |
| ashare_num | float | 否 | A 股股数 | 股 |
| bshare_num | float | 否 | B 股股数 | 股 |
| pe_lyr | float | 否 | 静态市盈率 | - |
| forwd_pe | float | 否 | 动态市盈率 | - |
| pe_ttm | float | 否 | 滚动市盈率 | - |
| ps | float | 否 | 市销率 | - |
| ps_ttm | float | 否 | 滚动市销率 | - |
| pb | float | 否 | 市净率 | - |
| pcf | float | 否 | 市现率（经营现金流量净额） | - |
| pcf_ttm | float | 否 | 滚动市现率 | - |
| dividrt_lyr_rpt | float | 否 | 静态股息率（报告期），% | % |
| dividrt_ttm | float | 否 | 滚动股息率 | % |

## 4. 调用方式

本 handler 与上级 `FTShare-hk-data/run.py` 配合使用：

```bash
python <RUN_PY> hk-view --hk_code 00700.HK
```

其中 `<RUN_PY>` 为 `FTShare-hk-data/run.py` 的绝对路径。

### 直接执行 handler（调试）

```bash
python scripts/handler.py --hk_code 00700.HK
```

（需在 `sub-skills/hk-view` 目录下执行，或传入脚本完整路径。）

## 5. 请求示例

```
GET /api/v1/market/data/hk/hk-view?hk_code=00700.HK
```
