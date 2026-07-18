---
name: fund-daily-paginated
description: "按基金代码查询场内基金（ETF/LOF）交易行情日线。当用户需要查前收/开高低收/均价/涨跌额/幅/换手率/成交量/成交额/振幅/折溢价等，通过 trade_date 单日或 start_date+end_date 区间（互斥）查询时使用。"
---

# 基金行情日线

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 基金行情日线                                                   |
| 外部接口 | `/api/v1/market/data/fund/fund-daily`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--fund_code` | string | 是 | 基金代码 |
| `--trade_date` | string | 否 | 交易日期 YYYYMMDD（与 start/end 互斥） |
| `--start_date` | string | 否 | 起始日期 YYYYMMDD（需与 end_date 同传） |
| `--end_date` | string | 否 | 结束日期 YYYYMMDD |
| `--page` | int | 否 | 页码，默认 1 |
| `--page_size` | int | 否 | 每页记录数，默认 50，上限 200 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-daily-paginated --fund_code 510300 --trade_date 20260717 --page 1 --page_size 50
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
