---
name: us-basic
description: 查询美股基础信息列表（股票代码、中英文名称、上市/退市日期）。Use when user asks about 美股有哪些, 全部美股, 美股代码列表, 美股上市日期, 某只美股基本信息/中英文名, 美股基础信息, us stock list, us-basic. 注意：本接口为 native 基础信息（名称/日期），不含最新价/市值/PE（那些用 eastmoney-us-stock-list）。
---

# 查询美股基础信息列表（native）

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 对外接口-查询美股列表 |
| 匹配键 | `us-basic` |
| 外部接口 | GET /api/v1/market/data/us/us-basic |
| 请求方式 | GET |
| 适用场景 | 查询美股基础信息（代码、中英文名称、上市/退市日期），支持全量分页或精确查单只。数据来源 ClickHouse `basedata.usstk_securityinfo`，约 5315 只。 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| stock_code | string | 否 | 美股代码（纯代码，不带交易所后缀） | NVDA | 不传返回全部（分页）；传则精确查单只（≤1 条） |
| page | int | 否 | 页码 | 1 | 默认 1，从 1 开始 |
| page_size | int | 否 | 每页条数 | 50 | 默认 50，最大 500 |

| 模式 | 必填参数 | 说明 |
|------|----------|------|
| 全量分页 | 无 | 返回全部美股（约 5315 只），按 `security_code` 升序 |
| 精确查单股 | `stock_code` | 返回指定股票基础信息（最多 1 条） |

## 执行方式

```bash
# 精确查英伟达
python scripts/handler.py --stock_code NVDA
# 分页查询美股列表
python scripts/handler.py --page 1 --page_size 50
# 全量自动翻页
python scripts/handler.py --all
```

## 响应结构

```json
{
  "items": [
    {
      "stock_code": "NVDA",
      "name": "英伟达",
      "enname": "Nvidia Corporation",
      "classify": "",
      "list_date": "1999-01-22",
      "delist_date": ""
    }
  ],
  "total_pages": 1,
  "total_items": 1
}
```

### 字段说明（UsBasicItem）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| stock_code | string | 美股代码（纯代码），如 `NVDA`、`AAPL` |
| name | string | 中文名称，如 `英伟达` |
| enname | string | 英文名称，如 `Nvidia Corporation` |
| classify | string | 分类（ADR/GDR/EQ），底表无此信息，固定空字符串 |
| list_date | string | 上市日期 `YYYY-MM-DD` |
| delist_date | string | 退市日期 `YYYY-MM-DD`，未退市为空字符串 |

## 注意事项

- 股票代码用**纯代码**（`NVDA`），不带交易所后缀（`.O`=纳斯达克、`.N`=纽交所）。
- `classify`（ADR/GDR/EQ）底表无来源，固定返回空字符串（中概股 ADR 与普通美股结构一致，无法区分）。
- `stock_code` 不存在不报错，返回 200 + `items: []`、`total_items: 0`。
- 与 `eastmoney-us-stock-list` 区别：本接口返回**基础信息**（名称/上市日期），后者返回东财**行情**（最新价/市值/涨跌幅/PE）。查"美股有哪些/代码/名称/上市日期"用本接口；查"美股最新价/市值/PE"用 `eastmoney-us-stock-list`。
- 财务三表查询用同样的纯代码 `stock_code`。
