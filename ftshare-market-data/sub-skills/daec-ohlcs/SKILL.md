---
name: daec-ohlcs
description: 按标的和日期区间查询历史 OHLC K 线（DAEC）。用户提到「DAEC 历史 OHLC」「DAEC K 线」「daec ohlcs」时使用。标准模式返回 K 线数组；传入 compat=v2 返回兼容版结构，并附带前收盘价和 MA5/MA10/MA20。标准模式 since/until 必填，YYYYMMDD。
---

# 查询 DAEC 历史 OHLC

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询 DAEC 历史 OHLC |
| 外部接口 | GET /api/v1/market/data/daec/history/ohlcs |
| 请求方式 | GET |
| 适用场景 | 按标的和日期区间查询历史 OHLC K 线；兼容模式可供旧前端直接消费 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | 标的代码 | `600000.XSHG` | - |
| since | string | 标准模式必填 | 起始日期 | `20260701` | YYYYMMDD |
| until | string | 标准模式必填 | 结束日期 | `20260731` | YYYYMMDD |
| interval | string | 否 | 周期 | `Day` | `Minute`/`Day`/`Week`/`Month`，默认 `Day` |
| adjust | string | 否 | 复权 | `Forward` | `None`/`Forward`/`Backward` |
| compat | string | 否 | 兼容版开关 | `v2` | 传 `v2` 启用兼容版响应 |
| span | string | 否 | 兼容模式周期 | `DAY1` | `DAY1`/`WEEK1`/`MONTH1`，默认 `DAY1` |
| limit | int | 否 | 兼容模式返回数量 | `250` | 默认 250 |
| until_ts_ms | int64 | 否 | 兼容模式结束时间戳 | `1785488400000` | 毫秒；优先于默认当前日期 |

## 执行方式

```bash
# 标准模式
python <RUN_PY> daec-ohlcs --symbol 600000.XSHG --since 20260701 --until 20260731 --interval Day --adjust Forward
# 兼容 v2 模式
python <RUN_PY> daec-ohlcs --symbol 600000.XSHG --compat v2 --span DAY1 --limit 250
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 响应结构

外层 `code/message/data`。

### 标准模式

`data` 直接为数组，每项字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| open_ts_ms / close_ts_ms | int64 | K 线开始 / 结束时间（毫秒） |
| open / high / low / close | string | 开高低收 |
| volume | int64 | 成交量 |
| turnover | string | 成交额 |

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "close_ts_ms": 1785488400000, "close": "10.25", "high": "10.36",
      "low": "10.08", "open": "10.12", "open_ts_ms": 1785461400000,
      "turnover": "126530000.00", "volume": 12345678
    }
  ]
}
```

### 兼容模式（compat=v2）

`data` 为对象，含 `current_time`/`has_last_empty`/`prev_close`/`ohlcs`/`ma5`/`ma10`/`ma20`。其中 `ohlcs` 使用缩写字段 `o/h/l/c/v/t/otm/ctm`。

## 注意事项

- 标准模式下 `since`/`until` 必填，格式 YYYYMMDD。
- 兼容模式默认 `limit=250`，`until_ts_ms` 优先于默认当前日期。
- 标准模式字段以字符串返回，`volume` 为 int64。
