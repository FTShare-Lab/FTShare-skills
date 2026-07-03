---
name: eastmoney-us-stock-latest-ohlc
description: "查询东财美股最新日 K 线。当用户需要分页查询东财美股最新一根日 K 线（最后一行 OHLC）；可按股票代码过滤，不传则返回全部美股，或了解东财美股最新 OHLC、东财美股最新日 K 线时使用。"
---

# 查询东财美股最新 OHLC

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询东财美股最新日 K 线 |
| 外部接口 | `/api/v1/market/data/eastmoney-us-stock-latest-ohlc` |
| 请求方式 | GET |
| 适用场景 | 分页查询东财美股最新一根日 K 线（最后一行 OHLC）；可按股票代码过滤，不传则返回全部美股 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| `--stock_code` | string | 否 | 股票代码 | `ADV` | 不传则返回全部美股最新 K 线 |
| `--page` | int | 否 | 页码 | `1` | 从 1 开始，默认 1 |
| `--page_size` | int | 否 | 每页条数 | `50` | 默认 50 |

### 查询模式

| 模式 | 参数 | 说明 |
|------|------|------|
| 全量查询 | 无 | 返回全部美股最新 K 线（分页） |
| 单票查询 | `--stock_code` | 返回指定股票最新一根 K 线 |

## 执行方式

通过根目录的 `run.py` 调用：

```bash
python <RUN_PY> eastmoney-us-stock-latest-ohlc --stock_code ADV --page 1 --page_size 20
python <RUN_PY> eastmoney-us-stock-latest-ohlc --page 1 --page_size 50
python <RUN_PY> eastmoney-us-stock-latest-ohlc --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

顶层为分页包装对象：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `code` | int | 业务状态码，成功为 `0` |
| `message` | string | 业务消息 |
| `data` | object/null | 分页数据体；无数据时可能为 `null` |
| `data.pageNum` | int | 当前页码 |
| `data.pageSize` | int | 每页条数 |
| `data.total` | int | 总记录数 |
| `data.pages` | int | 总页数 |
| `data.records` | array | 当前页 K 线列表 |

`data.records[]` 单条记录字段（JSON 字段为 snake_case）：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `secid` | string | 证券 ID，格式 `{market}.{code}`，如 `105.ADV` |
| `code` | string | 股票代码 |
| `name` | string | 股票名称 |
| `market` | string | 市场编号 |
| `date` | string | 日期，格式 `YYYY-MM-DD` |
| `open` | string | 开盘价 |
| `close` | string | 收盘价 |
| `high` | string | 最高价 |
| `low` | string | 最低价 |
| `volume` | int | 成交量 |
| `amount` | string | 成交额 |
| `amplitude` | number | 振幅 |
| `klt` | int | K 线类型 |
| `fqt` | int | 复权类型 |

### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 1,
    "pages": 1,
    "records": [
      {
        "secid": "105.ADV",
        "code": "ADV",
        "name": "Advantage Solutions Inc",
        "market": "105",
        "date": "2021-01-05",
        "open": "12.34",
        "close": "12.56",
        "high": "12.78",
        "low": "12.10",
        "volume": 1234567,
        "amount": "9876543.21",
        "amplitude": 5.5,
        "klt": 101,
        "fqt": 0
      }
    ]
  }
}
```

## 注意事项

- 分页信封字段 JSON 名为 camelCase（`pageNum`、`pageSize`、`records` 等）
- `data.records[]` 内 OHLC 价格为字符串格式，成交量/振幅/K 线类型/复权类型为数值
- `data` 在错误或无数据时可能为 `null`
- `stock_code` 为东财美股代码（如 `ADV`），非 A 股 `600000.SH` 格式
- 可先通过 `eastmoney-us-stock-list` 获取有效的美股代码列表
