---
name: get-nth-trade-date
description: 获取当前日期的前 N 个交易日（market.ft.tech）。用户问前 N 个交易日、近 N 天交易日、往前推 N 个交易日时使用。查「近几天」K 线时可先调本接口得到 nth_trade_date，再转为时间戳用于 K 线接口。
---

# 获取第 N 个交易日

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 获取第 N 个交易日 |
| 外部接口 | `GET /api/v1/market/data/time/get-nth-trade-date` |
| 请求方式 | GET |
| 适用场景 | 获取当前日期的前 N 个交易日，用于计算交易日相关逻辑；查「近 N 天」K 线时先调用本接口得到起止交易日，再转为毫秒时间戳请求 K 线接口 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| n | int | 是 | 前 N 个交易日 | 5 | 必须大于等于 1 |

## 3. 响应说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| current_date | string | 否 | 当前日期，YYYY-MM-DD |
| nth_trade_date | string | 否 | 前 N 个交易日，YYYY-MM-DD |
| n | int | 否 | 请求的 N 值 |

```json
{
  "current_date": "2025-01-15",
  "nth_trade_date": "2025-01-08",
  "n": 5
}
```

## 4. 用法

通过主目录 `run.py` 调用（必填 `--n`）：

```bash
python <RUN_PY> get-nth-trade-date --n 5
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 5. 注意事项

- 查询「近 N 天」或「最近 N 个交易日」K 线时：先调用本接口取 `nth_trade_date`，再将该日期（及当前日）按北京时间转为毫秒时间戳，作为 K 线接口的 `since_ts_millis` / `until_ts_millis` 使用。
