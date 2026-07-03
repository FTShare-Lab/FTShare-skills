---
name: etf-component
description: 查询单只 ETF 成份。用户问某只 ETF 成份股、ETF 持仓、510300 成份、沪深300ETF 成份列表时使用。
---

# 查询单只 ETF 成份

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单只 ETF 成份 |
| 外部接口 | `GET /api/v1/market/data/etf-component` |
| 请求方式 | GET |
| 适用场景 | 根据标的代码查询单只 ETF 的成份股列表（成份股代码与名称）；未找到或报错时接口返回相应错误信息 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | ETF 标的代码，带交易所后缀 | 510300.XSHG、159915.XSHE | 支持 510300.XSHG、510300.SH 等格式 |

## 3. 响应说明

返回单条 ETF 成份结构，与全量接口 `etf-components-all` 中单条结构一致。

```json
{
  "symbol": "510300.SH",
  "components": ["600000.SH", "601318.SH", "600519.SH"],
  "components_name": ["浦发银行", "中国平安", "贵州茅台"]
}
```

### 根字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| symbol | string | 否 | ETF 标的代码，带市场后缀 |
| components | array | 否 | 成份股代码列表，与 components_name 一一对应 |
| components_name | array | 否 | 成份股名称列表，与 components 一一对应 |

## 4. 用法

通过主目录 `run.py` 调用（必填 `--symbol`）：

```bash
python <RUN_PY> etf-component --symbol 510300.XSHG
python <RUN_PY> etf-component --symbol 159915.XSHE
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON；接口报错或未找到时，将接口返回的错误信息原样输出到 stderr 并退出码 1。

## 5. 请求示例

```
GET /api/v1/market/data/etf-component?symbol=510300.XSHG
```

## 6. 数据更新时间与注意事项

- 数据更新时间以接口/数据源为准。
- 成份列表与名称以接口返回为准；展示时 `components` 与 `components_name` 按索引一一对应。
