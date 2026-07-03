---
name: 10jqk-board-kline
description: Get THS board historical K-line (同花顺指定板块 K 线). Use when user asks about 同花顺板块K线、某概念板块走势、板块历史行情.
---

# 同花顺板块历史 K 线

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询同花顺板块历史 K 线 |
| 外部接口 | `GET /api/v1/market/data/ths-board-kline` |
| 请求方式 | GET |
| 适用场景 | 查询指定同花顺板块的历史日 K 线数据 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| board_code | string | 是 | 板块代码 | 885311 | 由 10jqk-board-list 获取 |
| page | int | 否 | 页码，从 1 开始 | 1 | 默认 1 |
| page_size | int | 否 | 每页数量 | 20 | 默认 50 |

## 3. 响应说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| items | array | 分页数据列表 |
| items[].board_code | string | 板块代码 |
| items[].board_name | string | 板块名称 |
| items[].module | string | 所属模块 |
| items[].date | string | 日期 YYYY-MM-DD |
| items[].open | string | 开盘价 |
| items[].high | string | 最高价 |
| items[].low | string | 最低价 |
| items[].close | string | 收盘价 |
| items[].volume | string | 成交量 |
| total_pages | int | 总页数 |
| total_items | int | 总记录数 |

## 4. 用法

```bash
python <RUN_PY> 10jqk-board-kline --board-code 885311
python <RUN_PY> 10jqk-board-kline --board-code 885311 --page 1 --page-size 20
```

## 5. 请求示例

```
GET /api/v1/market/data/ths-board-kline?board_code=885311&page=1&page_size=20
```

## 6. 注意事项

- `board_code` 必填，可从 `10jqk-board-list` 获取
- K 线数值均为字符串，计算时需转 float
- 支持分页，默认每页 50 条
