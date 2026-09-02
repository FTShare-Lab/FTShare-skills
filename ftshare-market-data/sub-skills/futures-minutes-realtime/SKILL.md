---
name: futures-minutes-realtime
description: 查询多个期货合约当日实时分钟 K 线，不带历史时间范围或周期参数。
---

# 期货实时分钟 K 线

调用 `/api/v4/market/data/futures_minutes/realtime`，使用 GET 查询当前北京时间交易日的实时 1 分钟 K 线。

```bash
python <RUN_PY> futures-minutes-realtime --symbols A2605.DCE --symbols M2609.DCE
```

`--symbols` 至少传一次、最多 20 个，可重复传入，也可使用逗号分隔值。API key 从环境变量 `FTSHARE_API_KEY` 读取，并作为请求头发送。
