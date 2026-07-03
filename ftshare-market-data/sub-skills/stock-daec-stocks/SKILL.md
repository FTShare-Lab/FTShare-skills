---
name: stock-daec-stocks
description: 查询 A 股行情列表 daec 全字段族，支持全市场、沪市、深市、北交所板块，以及 filter/order_by。Use when user asks about A股行情列表, 全市场行情, 沪深京实时行情, daec stocks, full stock quotes.
---

# 查询 A 股行情列表（daec 全字段族）

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | A 股行情列表（daec 全字段族） |
| 外部接口 | `GET /api/v1/market/data/daec/stocks/{board}` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股实时行情全字段列表，包含行情、成交、市值、PE、换手率、板块、上市日期等字段 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 示例 |
|---|---|---|---|---|
| `--board` | string | 是 | 板块：`all` / `xshg` / `xshe` / `bjse` | `all` |
| `--page` | int | 否 | 页码 | `1` |
| `--page_size` | int | 否 | 每页条数 | `20` |
| `--filter` | string | 否 | 筛选表达式，与板块内置筛选 AND 合并 | `close > 10` |
| `--order_by` | string | 否 | 排序规则 | `change_rate desc` |
| `--all` | flag | 否 | 自动翻页获取全量 | - |

## 执行方式

```bash
python <RUN_PY> stock-daec-stocks --board all --page 1 --page_size 5 --order_by "change_rate desc"
python <RUN_PY> stock-daec-stocks --board xshg --filter 'name.contains("银行")' --page 1 --page_size 5
python <RUN_PY> stock-daec-stocks --board bjse --filter "close > 5" --page 1 --page_size 5
```

## 响应结构

服务端分页信封：

```json
{
  "items": [
    {
      "symbol": "600000.XSHG",
      "name": "浦发银行",
      "close": "9.32",
      "change_rate": -0.0053,
      "turnover": "697403297.5",
      "pe_ttm": 6.2068
    }
  ],
  "total_pages": 100,
  "total_items": 5000
}
```

## 注意事项

- 板块内置筛选不可覆盖；`--filter` 会与内置筛选自动合并。
- `stock-daec-stocks` 返回全字段；如果只需要创业板/科创板/新股精简行情，用 `stock-realtime-list`。
