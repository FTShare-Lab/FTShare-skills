---
name: etf-list-paginated
description: ETF 分页列表，支持分页、排序、筛选（market.ft.tech）。用户问 ETF 列表、全市场 ETF、按涨跌幅排序的 ETF、筛选某类 ETF 时使用。
---

# ETF 分页列表 - 分页、排序、筛选

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | ETF 分页列表 |
| 外部接口 | `GET /api/v1/market/data/daec/etfs` |
| 请求方式 | GET |
| 适用场景 | 分页获取 A 股 ETF 列表，支持按字段排序、按条件筛选、按需返回字段（masks）；不传分页参数时返回全部（先筛选、排序后再截断） |

## 2. 请求参数

说明：所有参数均为可选项。不传 `order_by` 且不传 `ob` 时默认按 `change_rate desc` 排序；不传分页时返回满足条件的全部 ETF。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| order_by | string | 否 | 排序方式，格式为「字段 方向」，多字段用逗号分隔 | change_rate desc、name asc | 方向：asc/a 升序，desc/d 降序；字段为 Etf 字段名 |
| ob | string | 否 | 与 order_by 同义 | 同 order_by | 与 order_by 二选一，同时传以 order_by 为准 |
| filter | string | 否 | 过滤条件表达式 | change_rate != null、name ~ "沪深" | 见下方 filter 取值说明 |
| masks | string | 否 | 字段掩码，逗号分隔，仅返回这些字段 | name,symkey,latest,change_rate | 不传则返回全部字段 |
| page_size | int | 否 | 每页条数 | 20 | 不传则不分页 |
| page_no | int | 否 | 页码，从 1 开始 | 1 | 不传且传了 page_size 时默认为 1 |
| filter_index | boolean | 否 | 是否需要指数过滤 | true、false | 默认 false |

**filter 取值说明**：表达式语法为 `字段 操作符 值`。比较操作符：`=`、`!=`、`>`、`>=`、`<`、`<=`；`~` 子串包含；`:` 包含。逻辑组合：`AND`、`OR`、`NOT`，可用 `()` 分组。值可为 `null`、`true`、`false`、数字、双引号字符串。复杂表达式可 Base64 编码后以 `_B64:` 开头传入。示例：`change_rate != null`、`change_rate >= 0 AND change_rate <= 0.1`、`name ~ "科技"`。

## 3. 响应说明

返回分页后的 ETF 列表及总数。列表中每项为单只 ETF 对象（结构同单只 ETF 详情）；不传 `masks` 时每只返回全部字段。

```json
{
    "total_size": 800,
    "etfs": [
        { "name": "上证50ETF", "symkey": "510050.XSHG", "latest": 2.85, "change_rate": 0.0018 },
        { "name": "创业板ETF", "symkey": "159915.XSHE", "latest": 1.92, "change_rate": -0.0052 }
    ]
}
```

| 字段名 | 类型 | 说明 |
|--------|------|------|
| total_size | int | 满足筛选条件的 ETF 总数（分页前） |
| etfs | array | 当前页的 ETF 列表；单条字段同「单只 ETF 详情」（name、symkey、latest、change_rate、volume、turnover 等） |

## 4. 用法

通过主目录 `run.py` 调用（参数均可选）：

```bash
python <RUN_PY> etf-list-paginated
python <RUN_PY> etf-list-paginated --order_by "change_rate desc" --page_size 20 --page_no 1
python <RUN_PY> etf-list-paginated --order_by "name asc" --masks name,symkey,latest,change_rate --page_size 50
python <RUN_PY> etf-list-paginated --filter "change_rate >= 0.01 AND change_rate <= 0.05"
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 请求示例

```
GET /api/v1/market/data/daec/etfs?order_by=change_rate%20desc&page_size=20&page=1
```

## 6. 注意事项

- 涨跌幅等比率字段可能为小数形式，展示时按需乘以 100 转为百分比
- 不传 `page_size`/`page_no` 时返回全部满足条件的 ETF，数据量大时注意响应体积
