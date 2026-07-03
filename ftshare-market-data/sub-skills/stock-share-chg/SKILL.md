---
name: stock-share-chg
description: "查询单票股东增减持。当用户需要获取 A 股上市公司单只股票所有报告期的股东增减持信息，支持沪深京股票，支持分页查询，或了解单票股东增减持时使用。"
---

# 查询单票股东增减持

## 接口说明

| 项目     | 说明                                                                            |
|----------|---------------------------------------------------------------------------------|
| 接口名称 | 查询单票股东增减持                                                              |
| 外部接口 | `/api/v1/market/data/holder/stock-share-chg`                               |
| 请求方式 | GET                                                                             |
| 适用场景 | 获取 A 股上市公司单只股票所有报告期的股东增减持信息，支持沪深京股票，支持分页查询 |

## 请求参数

| 参数名     | 类型   | 是否必填 | 描述            | 取值示例  | 备注                                                                                     |
|------------|--------|----------|-----------------|-----------|------------------------------------------------------------------------------------------|
| stock_code | string | 是       | 单个股票代码    | 603323.SH | 支持沪深京股票，A股需为6位数字+后缀（SH=上交所，SZ=深交所，BJ=北交所），单次仅支持一个代码 |
| page       | int    | 否       | 页码，从 1 开始 | 1         | 默认值为 1，必须大于等于 1                                                               |
| page_size  | int    | 否       | 每页记录数      | 50        | 默认值为 50，必须大于等于 1                                                              |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-share-chg --stock_code 603323.SH
python <RUN_PY> stock-share-chg --stock_code 603323.SH --page 2 --page_size 20
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

接口返回带分页信息的对象：

```json
{
    "items": [
        {
            "trade_code": "603323",
            "stock_name": "苏农银行",
            "holder_name": "某股东名称",
            "shareholding_change_info": "增持",
            "change_quantity": 100000.00,
            "pre_change_quantity": 5000000.00,
            "pre_change_total_capital_ratio": null,
            "post_change_quantity": 5100000.00,
            "post_change_total_capital_ratio": null,
            "transfer_method": null,
            "latest_price": 6.78,
            "price_change_rate": 1.23,
            "transaction_price": null,
            "transaction_amount": null,
            "progress_description": null,
            "change_start_date": "2025-01-01",
            "change_end_date": "2025-03-31",
            "announcement_date": "2025-04-10"
        }
    ],
    "total_pages": 1,
    "total_items": 21
}
```

### HolderChangeDetail 字段说明

| 字段名                          | 类型   | 是否可为空 | 说明                                        | 单位 |
|---------------------------------|--------|------------|---------------------------------------------|------|
| trade_code                      | String | 否         | 股票交易代码，6 位数字                       | -    |
| stock_name                      | String | 否         | 上市公司官方简称                            | -    |
| holder_name                     | String | 否         | 持股变动主体，即股东名称                     | -    |
| shareholding_change_info        | String | 否         | 持股变动类型，仅包含"增持"或"减持"           | -    |
| change_quantity                 | float  | 否         | 持股变动数量，保留 2 位小数                  | 股   |
| pre_change_quantity             | float  | 否         | 变动前持股数量，保留 2 位小数                | 股   |
| pre_change_total_capital_ratio  | String | 是         | 变动前持股占总股本比例，当前暂为空值         | %    |
| post_change_quantity            | float  | 否         | 变动后持股数量，保留 2 位小数                | 股   |
| post_change_total_capital_ratio | String | 是         | 变动后持股占总股本比例，当前暂为空值         | %    |
| transfer_method                 | String | 是         | 股份转让方式，当前暂为空值                   | -    |
| latest_price                    | float  | 否         | 股票最新价格，保留 2 位小数                  | 元   |
| price_change_rate               | float  | 否         | 股票涨跌幅（与变动期间价格对比），保留 2 位小数 | %    |
| transaction_price               | String | 是         | 股份交易价格，当前暂为空值                   | 元   |
| transaction_amount              | String | 是         | 股份交易金额                                | 元   |
| progress_description            | String | 是         | 持股变动进展说明，当前暂为空值               | -    |
| change_start_date               | String | 否         | 持股变动开始日期，固定格式为 YYYY-MM-DD      | -    |
| change_end_date                 | String | 否         | 持股变动截止日期，固定格式为 YYYY-MM-DD      | -    |
| announcement_date               | String | 否         | 持股变动公告发布日期，固定格式为 YYYY-MM-DD  | -    |

## 注意事项

- `stock_code` 为必填参数，单次请求只支持一个股票代码
- 分页参数 `page` 和 `page_size` 均为可选，默认 `page=1`、`page_size=50`
- 返回值包含 `items`、`total_pages`、`total_items` 分页包装
- `shareholding_change_info` 仅为"增持"或"减持"两种取值
- `pre_change_total_capital_ratio`、`post_change_total_capital_ratio`、`transfer_method`、`transaction_price`、`transaction_amount`、`progress_description` 当前接口均暂为空值
