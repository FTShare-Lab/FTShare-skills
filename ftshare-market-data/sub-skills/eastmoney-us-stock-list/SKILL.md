---
name: eastmoney-us-stock-list
description: "查询东财美股列表。当用户需要获取东财美股全量列表（~5700+ 只），含代码、名称、市值、最新价、涨跌幅、市盈率等字段，支持服务端分页，或了解东财美股列表时使用。"
---

# 查询东财美股列表

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询东财美股列表 |
| 外部接口 | `/api/v1/market/data/eastmoney-us-stock-list` |
| 请求方式 | GET |
| 适用场景 | 获取东财美股全量列表（~5700+ 只），含代码、名称、市值、最新价、涨跌幅、市盈率等字段，支持服务端分页 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| `--page` | int | 否 | 页码 | `1` | 从 1 开始，默认 1 |
| `--page_size` | int | 否 | 每页条数 | `50` | 默认 50 |
| `--all` | flag | 否 | 返回全量 | — | 返回全量数据（不分页） |

**说明**：`--page`/`--page_size` 为全量拉取后在客户端切片的分页参数。

## 执行方式

通过根目录的 `run.py` 调用：

```bash
python <RUN_PY> eastmoney-us-stock-list
python <RUN_PY> eastmoney-us-stock-list --page 1 --page_size 50
python <RUN_PY> eastmoney-us-stock-list --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

顶层为分页包装对象（客户端包装）：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `code` | int | 业务状态码，成功为 `0` |
| `message` | string | 业务消息 |
| `data` | object/null | 分页数据体；无数据时可能为 `null` |
| `data.pageNum` | int | 当前页码 |
| `data.pageSize` | int | 每页条数 |
| `data.total` | int | 总记录数 |
| `data.pages` | int | 总页数 |
| `data.records` | array | 当前页记录列表 |

`data.records[]` 单条记录字段（**全部字段按字符串返回**）：

| 字段名 | 类型 | 描述 | 列表接口 | latest-ohlc fallback |
|--------|------|------|---------|---------------------|
| `secid` | string | 证券 ID，如 `105.AAL` | ✅ | ✅ |
| `market` | string | 市场编号，如 `105` | ✅ | ✅ |
| `code` | string | 股票代码，如 `AAL` | ✅ | ✅ |
| `name` | string | 股票名称 | ✅ | ✅ |
| `market_value_usd` | string | 市值（美元） | ✅ | 空 |
| `latest_price` | string | 最新价 | ✅ | 取自 `close` |
| `change_pct` | string | 涨跌幅（%） | ✅ | 空 |
| `volume` | string | 成交量 | ✅ | ✅ |
| `amount` | string | 成交额 | ✅ | ✅ |
| `pe_ttm` | string | 市盈率 TTM | ✅ | 空 |

### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pageNum": 1,
    "pageSize": 50,
    "total": 5722,
    "pages": 115,
    "records": [
      {
        "secid": "105.AAL",
        "market": "105",
        "code": "AAL",
        "name": "美国航空",
        "market_value_usd": "1234567890",
        "latest_price": "13.444",
        "change_pct": "-4.59",
        "volume": "64552347",
        "amount": "874794464.0000",
        "pe_ttm": "15.6"
      }
    ]
  }
}
```

## 注意事项

- 所有数值字段均为字符串格式
- `code` 为东财美股代码（如 `AAL`），非 A 股 `600000.SH` 格式
- `data` 在错误或无数据时可能为 `null`
- 服务端分页，`--all` 时内部以 500 条/页全量拉取后合并
- 不覆盖苹果等美股大盘蓝筹，以东财中小盘和中概股为主
