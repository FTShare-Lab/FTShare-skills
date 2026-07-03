---
name: index-detail
description: Get single index detail (单只指数详情). Use when user asks about 某只指数详情、指数行情、上证指数、沪深300、指数名称/点位/涨跌幅/成交.
---

# 单只指数详情 - 查询单只指数详情

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单只指数详情 |
| 外部接口 | `GET /api/v1/market/data/daec/index?symbol=:index` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股指定指数的详情（名称、行情点位、成交、涨跌幅等）；支持通过 masks 按需返回部分字段 |

## 2. 请求参数

说明：`index` 为路径参数（必填），`masks` 为可选项。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| index | string | 是 | 指数标的键（路径参数，带市场后缀） | 000001.XSHG、399001.XSHE、920036.BJ | 沪 .XSHG、深 .XSHE、北交所 .BJ |
| masks | string | 否 | 字段掩码，逗号分隔的字段名，仅返回这些字段 | name,symkey,latest,change_rate | 不传则返回全部字段；字段名须匹配正则 `^[a-zA-Z_][a-zA-Z0-9_]*$`（首字符为字母或下划线，后续可为字母、数字、下划线），非法字段名会报错 |

## 3. 响应说明

返回单只指数对象，与代码 `Index` 一致。不传 `masks` 时返回全部字段，传 `masks` 时仅返回指定字段；各字段均可能为 null 或不存在。点位与价格类保留 4 位小数。

```json
{
    "name": "上证指数",
    "symkey": "000001.XSHG",
    "latest": 3252.30,
    "prev_close": 3245.67,
    "change": 6.63,
    "change_rate": 0.0020,
    "volume": 280000000,
    "turnover": 350000000000.0,
    "amplitude": 0.0052
}
```

### 根字段（部分常用）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| name | string | 是 | 指数名称 | — |
| symkey | string | 是 | 标的键 | — |
| symbol_id | string | 是 | 标的 ID | — |
| ex_id | string | 是 | 市场 ID | — |
| latest | float | 是 | 最新点位 | 点 |
| close | float | 是 | 收盘点位 | 点 |
| open | float | 是 | 开盘点位 | 点 |
| high | float | 是 | 最高点位 | 点 |
| low | float | 是 | 最低点位 | 点 |
| prev_close | float | 是 | 昨收点位 | 点 |
| change | float | 是 | 涨跌点位 | 点 |
| change_rate | float | 是 | 涨跌幅 | % |
| volume | long | 是 | 成交量 | — |
| turnover | float | 是 | 成交额 | 元 |
| amplitude | float | 是 | 振幅 | % |
| change_rate_5d | float | 是 | 5 日涨跌幅 | % |
| change_rate_10d | float | 是 | 10 日涨跌幅 | % |
| change_rate_20d | float | 是 | 20 日涨跌幅 | % |
| change_rate_60d | float | 是 | 60 日涨跌幅 | % |
| change_rate_120d | float | 是 | 120 日涨跌幅 | % |
| change_rate_6m | float | 是 | 6 月涨跌幅 | % |
| change_rate_1y | float | 是 | 1 年涨跌幅 | % |
| change_rate_2y | float | 是 | 2 年涨跌幅 | % |
| change_rate_3y | float | 是 | 3 年涨跌幅 | % |
| change_rate_ytd | float | 是 | 今年至今涨跌幅 | % |

## 4. 用法

通过主目录 `run.py` 调用（必填 `--index`，可选 `--masks`）：

```bash
python <RUN_PY> index-detail --index 000001.XSHG
python <RUN_PY> index-detail --index 399001.XSHE --masks name,symkey,latest,change_rate,volume,turnover
```

或在子 skill 目录下执行：`python scripts/handler.py --index 000001.XSHG`（可选 `--masks`）。`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 请求示例

```
GET /api/v1/market/data/daec/index?symbol=000001.XSHG
```

### 完整请求示例（curl）

```bash
curl -X GET "<BASE_URL>/api/v1/market/data/daec/index?symbol=000001.XSHG" \
  -H 'X-Client-Name: ft-claw' \
  -H 'Content-Type: application/json'
```

## 6. 数据更新时间与注意事项

- 数据更新时间以接口/行情源为准。
- 涨跌幅 `change_rate` 等比率字段在接口中可能为小数形式，展示时按需乘以 100 转为百分比。
- 成交量、成交额等大数字展示时可按需换算单位（如万、亿）。
- 完整字段以代码 `Index` 为准；未传 `masks` 时返回全部可用字段。
- 若用户输入的是指数名称/简称而非代码，建议先调用 `index-description-all` 或 `index-list-paginated` 映射出唯一 `symkey`，再调用本接口。
