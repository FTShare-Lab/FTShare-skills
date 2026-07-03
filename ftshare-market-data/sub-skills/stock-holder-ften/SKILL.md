---
name: stock-holder-ften
description: "查询单票所有公告期 10 大流通股东。当用户需要获取 A 股上市公司单只股票所有公告期的十大流通股东信息，支持沪深京股票，或了解单票所有公告期 10 大流通股东时使用。"
---

# 查询单票所有公告期 10 大流通股东

## 接口说明

| 项目     | 说明                                                                 |
|----------|----------------------------------------------------------------------|
| 接口名称 | 查询单票所有公告期 10 大流通股东                                     |
| 外部接口 | `/api/v1/market/data/holder/stock-holder-ften`                  |
| 请求方式 | GET                                                                  |
| 适用场景 | 获取 A 股上市公司单只股票所有公告期的十大流通股东信息，支持沪深京股票 |

## 请求参数

| 参数名     | 类型   | 是否必填 | 描述         | 取值示例  | 备注                                                                                       |
|------------|--------|----------|--------------|-----------|--------------------------------------------------------------------------------------------|
| stock_code | string | 是       | 单个股票代码 | 603323.SH | 支持沪深京股票，A 股需为 6 位数字+后缀（SH=上交所，SZ=深交所，BJ=北交所），单次仅支持一个代码 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 查询 603323.SH 所有公告期十大流通股东
python <RUN_PY> stock-holder-ften --stock_code 603323.SH
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "items": [
        {
            "stock_code": "603323.SH",
            "stock_name": "苏农银行",
            "publish_date": "2024-09-30",
            "share_holding": 23.15,
            "fen_holders": [
                {
                    "rank": 1,
                    "shareholder_name": "香港中央结算有限公司",
                    "shareholder_type": "境外法人",
                    "share_type": "A股",
                    "shareholding": 55000000.0,
                    "share_ratio": 3.90,
                    "limit_num": null,
                    "unlimit_num": null,
                    "change_shares": 1200000.0,
                    "change_type": "增持",
                    "change_percentage": 2.23
                }
            ]
        }
    ],
    "total_pages": 1,
    "total_items": 21
}
```

### 顶层字段说明

| 字段名      | 类型  | 是否可为空 | 说明                             |
|-------------|-------|------------|----------------------------------|
| items       | Array | 否         | 公告期列表（每个元素对应一个公告期） |
| total_pages | int   | 否         | 总页数                           |
| total_items | int   | 否         | 总记录数                         |

### TopTenHolders 字段说明

| 字段名        | 类型   | 是否可为空 | 说明                                       | 单位 |
|---------------|--------|------------|--------------------------------------------|------|
| stock_code    | String | 否         | 股票交易代码，固定携带 .SZ/.SH/.BJ 市场后缀 | -    |
| stock_name    | String | 否         | 上市公司对应股票名称                       | -    |
| publish_date  | String | 否         | 公告截止日期，固定格式为 YYYY-MM-DD         | -    |
| share_holding | float  | 否         | 十大流通股东持股合计（占股本比例总和）       | %    |
| fen_holders   | Array  | 否         | 十大流通股东明细列表                       | -    |

### HolderDetail 字段说明（fen_holders 数组元素）

| 字段名            | 类型   | 是否可为空 | 说明                                       | 单位 |
|-------------------|--------|------------|--------------------------------------------|------|
| rank              | int    | 否         | 股东名次                                   | -    |
| shareholder_name  | String | 否         | 股东名称                                   | -    |
| shareholder_type  | String | 否         | 股东性质                                   | -    |
| share_type        | String | 否         | 股份类型，固定为"A股"                       | -    |
| shareholding      | float  | 否         | 持股数                                     | 股   |
| share_ratio       | float  | 否         | 占股本持股比例                             | %    |
| limit_num         | float  | 是         | 限售数量                                   | 股   |
| unlimit_num       | float  | 是         | 无限售数量，流通股东此字段固定为 null        | 股   |
| change_shares     | float  | 否         | 增减股数（与上期对比）                       | 股   |
| change_type       | String | 是         | 变动类型：新进、增持、减持、不变              | -    |
| change_percentage | float  | 是         | 变动比例（与上期对比），无上期数据时返回 null | %    |

### 变动类型说明

- **新进**：上期不存在该股东
- **增持**：本期持股数大于上期
- **减持**：本期持股数小于上期
- **不变**：本期持股数等于上期

## 注意事项

- `stock_code` 为必填项，单次仅支持一个股票代码
- 股票代码需携带市场后缀（`.SH` / `.SZ` / `.BJ`）
- `unlimit_num` 对流通股东固定返回 `null`
- `limit_num`、`change_type`、`change_percentage` 可能为 `null`，展示时需做空值处理
- 该接口返回该股票所有历史公告期数据，通常 `total_pages` 为 1
