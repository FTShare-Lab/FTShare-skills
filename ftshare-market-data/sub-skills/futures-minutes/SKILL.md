---
name: futures-minutes
description: 查询单个期货合约的历史分钟 K 线，支持周期、时间范围和数量限制。
---

# 期货分钟 K 线

调用 `/api/v3/market/data/futures_minutes`，使用 GET 查询单个期货合约的历史分钟 K 线。

```bash
python <RUN_PY> futures-minutes --symbol A2609.DCE --interval 1min --limit 5
```

参数：`--symbol` 必填；可选 `--interval`、`--start`、`--end`、`--limit`。`start` 与 `end` 为毫秒时间戳，`limit` 范围为 1～1000。

API key 从环境变量 `FTSHARE_API_KEY` 读取，并作为请求头发送。
