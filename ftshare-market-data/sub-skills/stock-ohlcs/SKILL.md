---
name: stock-ohlcs
description: "标的K线数据。当用户需要获取 A 股指定标的在指定日期区间、周期的 K 线；支持 `compat=v2` 返回旧 v2 风格结构和均线字段，或了解单只股票 OHLC K 线（daec）、标的K线数据时使用。"
---

# 查询单只股票 OHLC K 线（daec）

## 接口说明

| 项目     | 说明                                                                                                          |
|----------|---------------------------------------------------------------------------------------------------------------|
| 接口名称 | 标的K线数据                                                                                                      |
| 外部接口 | /api/v1/market/data/daec/history/ohlcs                                                                    |
| 请求方式 | GET                                                                                                            |
| 适用场景 | 获取 A 股指定标的在指定日期区间、周期的 K 线；支持 `compat=v2` 返回旧 v2 风格结构和均线字段 |

> 已从旧 v2 路径迁移至 daec 统一标的接口（`daec/history/ohlcs?symbol=`）。原始模式使用 `--since/--until` + `--interval` + `--adjust`；`--compat v2` 可使用 `--span/--limit/--until_ts_ms` 并返回 `ma5/ma10/ma20/prev_close` 等兼容字段。当前 daec 兼容模式不支持 `YEAR1`。

## 请求参数

说明：推荐使用 `--symbol`；仍兼容旧参数 `--stock`。原始模式至少需要 `--since`，`--until` 不传时脚本默认今天；`compat=v2` 模式可不传日期区间。

| 参数名   | 类型   | 是否必填 | 描述                  | 取值示例    | 备注                                                  |
|----------|--------|----------|-----------------------|-------------|-------------------------------------------------------|
| symbol   | string | 是       | 标的代码（带市场后缀） | 600000.XSHG | 沪 .XSHG、深 .SZ、北交所 .BJ                           |
| stock    | string | 否       | `symbol` 的旧别名      | 600000.XSHG | 仅为兼容旧调用方式                                     |
| since    | string | 原始模式是 | 起始日期 YYYYMMDD     | 20240101    | v2 兼容模式可不传                                      |
| until    | string | 否       | 结束日期 YYYYMMDD     | 20240131    | 原始模式不传则默认今天                                  |
| interval | string | 否       | 原始模式 K 线周期      | Day         | Minute、Day（日线，默认）、Week、Month；无年线          |
| adjust   | string | 否       | 复权类型              | Forward     | Forward（前复权，默认）、Backward（后复权）、None（不复权） |
| compat   | string | 否       | 兼容模式              | v2          | 传 `v2` 时启用旧 v2 响应结构                            |
| span     | string | 否       | v2 兼容模式 K 线周期   | DAY1        | DAY1、WEEK1、MONTH1；不支持 YEAR1                      |
| limit    | int    | 否       | v2 兼容模式返回最近 N 根 K 线 | 5   | -                                                     |
| until_ts_ms | int | 否       | v2 兼容模式截止毫秒时间戳 | 1782748799999 | 服务端按北京时间转换为截止日期                         |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 600000.XSHG 2024-01 的日线
python <RUN_PY> stock-ohlcs --symbol 600000.XSHG --since 20240101 --until 20240131

# 周线
python <RUN_PY> stock-ohlcs --symbol 600000.XSHG --since 20240101 --until 20260628 --interval Week

# 前复权月线（until 默认今天）
python <RUN_PY> stock-ohlcs --symbol 600000.XSHG --since 20230101 --interval Month --adjust Forward

# v2 兼容模式：最近 5 根日 K，直接输出服务端兼容对象
python <RUN_PY> stock-ohlcs --symbol 600000.XSHG --compat v2 --span DAY1 --limit 5

# 旧参数仍可使用
python <RUN_PY> stock-ohlcs --stock 600000.XSHG --since 20240101 --until 20240131
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

原始模式返回 K 线列表，包装为 `{"ohlcs": [...]}`（daec 返回裸数组，脚本统一包装）：

```json
{
    "ohlcs": [
        { "open": "8.30", "high": "8.33", "low": "8.19", "close": "8.28", "volume": 60213694, "turnover": "496075055.52", "open_ts_ms": "2024-06-03T09:30:00", "close_ts_ms": "2024-06-03T15:00:00" }
    ]
}
```

### Ohlc 单条结构（ohlcs 元素）

| 字段名      | 类型   | 是否可为空 | 说明                          | 单位 |
|-------------|--------|------------|-------------------------------|------|
| open        | string | 否         | 开盘价                        | 元   |
| high        | string | 否         | 最高价                        | 元   |
| low         | string | 否         | 最低价                        | 元   |
| close       | string | 否         | 收盘价                        | 元   |
| volume      | long   | 否         | 成交量                        | 股   |
| turnover    | string | 否         | 成交额                        | 元   |
| open_ts_ms  | string | 否         | 该根 K 线开始时间（北京时间 ISO） | -    |
| close_ts_ms | string | 否         | 该根 K 线结束时间（北京时间 ISO） | -    |

`compat=v2` 模式直接输出服务端对象：

```json
{
  "current_time": "2026-06-29T15:03:10.123456789+08:00",
  "has_last_empty": false,
  "prev_close": 9.16,
  "ohlcs": [
    {"o": 8.80, "h": 8.90, "l": 8.70, "c": 8.75, "v": 68098356, "t": 588719704.13, "otm": 1782662400000, "ctm": 1782748799999}
  ],
  "ma5": [{"p": null, "ctm": 1782748799999}],
  "ma10": [{"p": null, "ctm": 1782748799999}],
  "ma20": [{"p": null, "ctm": 1782748799999}]
}
```

> 注：原始模式价格字段为字符串类型（避免浮点精度丢失）；`compat=v2` 模式的字段名和类型按服务端兼容对象输出。

## 注意事项

- `symbol` 为必填；旧 `stock` 参数仍可作为别名使用。
- 原始模式需要 `since`；`since`/`until` 需为 YYYYMMDD（8 位数字）。
- 股票代码需携带市场后缀：沪市 .XSHG、深市 .SZ、北交所 .BJ
- `interval` 支持 Minute/Day/Week/Month（daec 无年线）；不传默认 Day。
- `compat=v2` 的 `span` 支持 DAY1/WEEK1/MONTH1，不支持 YEAR1。
- `adjust` 可选 Forward/Backward/None，默认 Forward（前复权）；None 为不复权。
- 所有接口请求需携带 X-Client-Name: ft-claw 请求头
- 原始模式下，脚本将每条 `open_ts_ms`/`close_ts_ms`（毫秒）转为北京时间 ISO 字符串；`compat=v2` 保留服务端返回字段。
- **已知问题**：daec 大区间响应（如多年日线，~100KB+）服务端偶发传输中断（IncompleteRead），脚本内置 5 次指数退避重试；如仍失败会非零退出。建议按需缩小日期区间
