---
name: stock-unlock-by-stock
description: 按证券代码查询限售解禁批次及股东明细（market.ft.tech）。用户问某只股票限售解禁、解禁日期、解禁股东、解禁市值时使用。
---

# 限售解禁 - 按证券代码查询

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 按证券代码查询限售解禁 |
| 外部接口 | `GET /api/v1/market/data/unlock/stock-unlock` |
| 请求方式 | GET |
| 适用场景 | 按证券代码分页查询限售解禁批次及股东明细 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| stock_code | string | 是 | 证券代码（6 位） | `000001` | - |
| page | int | 否 | 页码，从 1 开始 | `1` | 默认 1 |
| page_size | int | 否 | 每页条数 | `50` | 默认 50，最大 200 |

## 3. 响应说明

返回 `PaginatedApiResponse` 包装的 JSON 对象。

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pageNum": 1,
    "pageSize": 50,
    "total": 1,
    "pages": 1,
    "records": [
      {
        "stockCode": "000001",
        "stockName": "平安银行",
        "unlockDate": "2025-06-15",
        "holderCount": "3",
        "ableFreeShares": "1000000",
        "currentFreeShares": "500000",
        "nonFreeShares": "500000",
        "liftMarketCap": "50000000",
        "totalRatio": "0.05",
        "freeRatio": "0.02",
        "newPrice": "12.50",
        "freeSharesType": "首发原股东限售股份",
        "b20Adjchrate": "0.03",
        "a20Adjchrate": "-0.01",
        "crawlDate": "20250601",
        "source": "eastmoney",
        "holders": [
          {
            "holderName": "张三",
            "addListingShares": "200000",
            "actualListedShares": "200000",
            "addListingCap": "2500000",
            "lockMonth": "12",
            "residualLimitedShares": "0",
            "freeSharesType": "首发原股东限售股份",
            "planFeature": "已实施"
          }
        ]
      }
    ]
  }
}
```

### data.records 元素结构（批次）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| stockCode | string | 证券代码 |
| stockName | string | 证券名称 |
| unlockDate | string | 解禁日期 |
| holderCount | string | 股东数量 |
| ableFreeShares | string | 可解禁股份 |
| liftMarketCap | string | 解禁市值 |
| totalRatio | string | 占总股本比例 |
| freeRatio | string | 占流通股本比例 |
| newPrice | string | 最新价 |
| freeSharesType | string | 限售股份类型 |
| b20Adjchrate | string | 解禁前20日涨跌幅 |
| a20Adjchrate | string | 解禁后20日涨跌幅 |
| holders | array | 股东明细列表 |

### holders 元素结构（股东明细）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| holderName | string | 股东名称 |
| addListingShares | string | 新增上市股份 |
| actualListedShares | string | 实际上市股份 |
| addListingCap | string | 新增上市市值 |
| lockMonth | string | 锁定期（月） |
| residualLimitedShares | string | 剩余限售股份 |
| freeSharesType | string | 限售股份类型 |
| planFeature | string | 方案进度 |

## 4. 用法

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> stock-unlock-by-stock --stock_code 000001
python <RUN_PY> stock-unlock-by-stock --stock_code 000001 --page 1 --page_size 50
```

## 5. 请求示例

```
GET /api/v1/market/data/unlock/stock-unlock?stock_code=000001&page=1&page_size=50
```
