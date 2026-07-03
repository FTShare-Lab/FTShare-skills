---
name: stock-holder-nums
description: "查询单票所有公告期股东人数信息。当用户需要获取 A 股上市公司单只股票所有公告期的股东人数信息，支持沪深京股票，或了解单票所有公告期股东人数信息时使用。"
---

# 查询单票所有公告期股东人数信息

## 接口说明

| 项目     | 说明                                                             |
|----------|------------------------------------------------------------------|
| 接口名称 | 查询单票所有公告期股东人数信息                                   |
| 外部接口 | `/api/v1/market/data/holder/stock-holder-nums`              |
| 请求方式 | GET                                                              |
| 适用场景 | 获取 A 股上市公司单只股票所有公告期的股东人数信息，支持沪深京股票 |

## 请求参数

| 参数名     | 类型   | 是否必填 | 描述         | 取值示例  | 备注                                                                                       |
|------------|--------|----------|--------------|-----------|--------------------------------------------------------------------------------------------|
| stock_code | string | 是       | 单个股票代码 | 603323.SH | 支持沪深京股票，A 股需为 6 位数字+后缀（SH=上交所，SZ=深交所，BJ=北交所），单次仅支持一个代码 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 查询 603323.SH 所有公告期股东人数
python <RUN_PY> stock-holder-nums --stock_code 603323.SH
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "items": [
        {
            "stock_code": "603323.SH",
            "stock_name": "苏农银行",
            "publish_date": "2024-10-15",
            "report_date": "2024-09-30",
            "holder_num": 45230,
            "holder_num_change_ratio": -2.15,
            "per_capita_circ_share": 3120.5,
            "per_capita_share_change_ratio": null,
            "chip_concentration": null,
            "close_price": 5.82,
            "per_capita_hold_amount": 18160.31,
            "ten_holder_ratio": 46.32,
            "ften_holder_ratio": 23.15
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

### HolderCountAnnouncement 字段说明

| 字段名                        | 类型   | 是否可为空 | 说明                                               | 单位 |
|-------------------------------|--------|------------|----------------------------------------------------|------|
| stock_code                    | String | 否         | 股票交易代码，固定携带 .SZ/.SH/.BJ 市场后缀         | -    |
| stock_name                    | String | 否         | 上市公司对应股票名称                               | -    |
| publish_date                  | String | 否         | 信息发布日期，固定格式为 YYYY-MM-DD                 | -    |
| report_date                   | String | 否         | 报告截止日期，固定格式为 YYYY-MM-DD                 | -    |
| holder_num                    | int    | 否         | 股东总人数                                         | 人   |
| holder_num_change_ratio       | float  | 是         | 股东人数变化率（与上期对比），无上期数据时返回 null  | %    |
| per_capita_circ_share         | float  | 是         | 人均流通股数，无数据时返回 null                     | 股   |
| per_capita_share_change_ratio | float  | 是         | 人均持股变化率，当前暂为 null                       | %    |
| chip_concentration            | String | 是         | 筹码集中度，当前暂为 null                           | -    |
| close_price                   | float  | 否         | 报告截止日期收盘价                                 | 元   |
| per_capita_hold_amount        | float  | 否         | 人均持股金额（人均流通股数 × 收盘价）               | 元   |
| ten_holder_ratio              | float  | 是         | 十大股东持股合计（占股本比例），无数据时返回 null    | %    |
| ften_holder_ratio             | float  | 是         | 十大流通股东持股合计（占股本比例），无数据时返回 null | %    |

## 注意事项

- `stock_code` 为必填项，单次仅支持一个股票代码
- 股票代码需携带市场后缀（`.SH` / `.SZ` / `.BJ`）
- `per_capita_share_change_ratio` 与 `chip_concentration` 当前接口固定返回 null
- `holder_num_change_ratio`、`per_capita_circ_share`、`ten_holder_ratio`、`ften_holder_ratio` 可能为 null，展示时需做空值处理
- 该接口返回该股票所有历史公告期数据，通常 `total_pages` 为 1
