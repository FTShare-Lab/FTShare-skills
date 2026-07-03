---
name: index-list-paginated
description: 指数分页列表，支持分页、排序、筛选（market.ft.tech）。用户问指数列表、全市场指数、按涨跌幅排序的指数、筛选某类指数时使用。
---

# 指数分页列表 - 分页、排序、筛选

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 指数列表（分页、排序、筛选） |
| 外部接口 | `GET /api/v1/market/data/daec/indices` |
| 请求方式 | GET |
| 适用场景 | 分页获取 A 股指数列表，支持按字段排序、按条件筛选、按需返回字段（masks）；不传分页参数时返回全部（先筛选、排序后再截断） |

## 2. 请求参数

说明：所有参数均为可选项。不传 `order_by` 且不传 `ob` 时默认按 `change_rate desc` 排序；不传分页时返回满足条件的全部指数。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| order_by | string | 否 | 排序方式，格式为「字段 方向」，多字段用逗号分隔 | change_rate desc、name asc | 方向：asc/a 升序，desc/d 降序；字段为 Index 字段名（如 change_rate、name、latest） |
| ob | string | 否 | 与 order_by 同义 | 同 order_by | 与 order_by 二选一，同时传以 order_by 为准 |
| filter | string | 否 | 过滤条件表达式 | change_rate != null | 对 Index 字段做条件过滤；可为 _B64: 开头 Base64 编码；语法见下方 filter 取值说明 |
| masks | string | 否 | 字段掩码，逗号分隔的字段名，仅返回这些字段 | name,symkey,latest,change_rate | 不传则返回全部字段；字段名须匹配正则 `^[a-zA-Z_][a-zA-Z0-9_]*$`，非法字段名会报错 |
| page_size | int | 否 | 每页条数 | 20 | 不传则不分页 |
| page_no | int | 否 | 页码，从 1 开始 | 1 | 不传且传了 page_size 时默认为 1 |

**filter 取值说明**（表达式语法，对应代码 crates/dom/src/core/filter.rs）：

- **基本形式**：`字段 操作符 值`。字段为 Index 的字段名（与 order_by、masks 一致，如 change_rate、name、latest、symkey）。
- **比较操作符**：`=`、`!=`、`>`、`>=`、`<`、`<=`。
- **其它操作符**：`~` 子串包含（左为字段、右为字符串）；`:` 包含（具体以实现为准）。
- **逻辑组合**：`AND`、`OR`、`NOT`，可用括号 `()` 分组。例：`(change_rate >= 0 AND change_rate <= 0.05) OR name ~ "上证"`。
- **值**：`null`、`true`、`false`、数字、双引号字符串（内部双引号用 `\"` 转义）。
- **Base64**：整段表达式做 Base64 编码后以 `_B64:` 开头传入。

示例：`change_rate != null`、`latest > 3000`、`name ~ "上证"`。

## 3. 响应说明

返回分页后的指数列表及总数，与代码 `ListIndicesReply` 一致。列表中每项为单只指数对象（结构同单只指数详情）；不传 `masks` 时每只指数返回全部字段，传 `masks` 时仅返回指定字段。

```json
{
    "total_size": 500,
    "indices": [
        { "name": "上证指数", "symkey": "000001.XSHG", "latest": 3252.30, "change_rate": 0.0020 },
        { "name": "深证成指", "symkey": "399001.XSHE", "latest": 10580.50, "change_rate": -0.0015 }
    ]
}
```

### 根字段

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| total_size | int | 否 | 满足筛选条件的指数总数（分页前） |
| indices | array | 否 | 当前页的指数列表；单条结构见下表 |

### 单条结构（indices 元素，对应 Index）

以下为部分常用字段；完整字段见代码 Index，点位类保留 4 位小数。

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

通过主目录 `run.py` 调用（参数均可选）：

```bash
python <RUN_PY> index-list-paginated
python <RUN_PY> index-list-paginated --order_by "change_rate desc" --page_size 20 --page_no 1
python <RUN_PY> index-list-paginated --order_by "name asc" --masks name,symkey,latest,change_rate --page_size 50
python <RUN_PY> index-list-paginated --filter "change_rate >= 0 AND change_rate <= 0.05"
```

或在子 skill 目录下执行：`python scripts/handler.py` 加上上述参数。脚本输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 请求示例

```
GET /api/v1/market/data/daec/indices?order_by=change_rate%20desc&page_size=20&page=1
```

### 完整请求示例（curl）

```bash
curl -X GET "<BASE_URL>/api/v1/market/data/daec/indices?order_by=change_rate%20desc&page_size=20&page=1" \
  -H 'X-Client-Name: ft-claw' \
  -H 'Content-Type: application/json'
```

## 6. 注意事项

- 涨跌幅等比率字段可能为小数形式，展示时按需乘以 100 转为百分比
- 不传 `page_size`/`page_no` 时返回全部满足条件的指数，数据量大时注意响应体积
- 完整字段以代码 Index 为准
