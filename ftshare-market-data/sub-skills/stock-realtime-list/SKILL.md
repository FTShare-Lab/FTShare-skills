---
name: stock-realtime-list
description: 查询 A 股行情列表 stock-list 实时精简族，覆盖创业板、科创板、新股。Use when user asks about 创业板行情, 科创板行情, 新股行情, realtime stock list, stock-list board quotes.
---

# 查询 A 股行情列表（stock-list 实时族）

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | A 股行情列表（stock-list 实时族） |
| 外部接口 | `GET /api/v1/market/data/stock-list/{board}` |
| 请求方式 | GET |
| 适用场景 | 查询创业板、科创板、新股的实时行情精简字段列表 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 示例 |
|---|---|---|---|---|
| `--board` | string | 是 | 板块：`chi-next` / `star` / `new` | `chi-next` |
| `--page` | int | 否 | 页码 | `1` |
| `--page_size` | int | 否 | 每页条数，最大 200 | `50` |
| `--all` | flag | 否 | 自动翻页获取全量 | - |

## 执行方式

```bash
python <RUN_PY> stock-realtime-list --board chi-next --page 1 --page_size 5
python <RUN_PY> stock-realtime-list --board star --page 1 --page_size 5
python <RUN_PY> stock-realtime-list --board new --page 1 --page_size 5
```

## 响应结构

服务端分页信封：

```json
{
  "items": [
    {
      "symbol": "300750.XSHE",
      "symbol_name": "宁德时代",
      "close": "180.00",
      "change_rate": 0.0123,
      "volume": 12345678,
      "turnover": "1234567890.00"
    }
  ],
  "total_pages": 20,
  "total_items": 1000
}
```

## 注意事项

- `stock-list/*` 族没有 `all` 板块；全市场/沪深京行情请使用 `stock-daec-stocks --board all`。
- 本接口字段较精简；需要市值、PE、换手率等字段时使用 `stock-daec-stocks`。
