---
name: futures-minutes-batch
description: 批量查询多个期货合约的历史分钟 K 线，支持重复或逗号分隔的合约参数。
---

# 批量期货分钟 K 线

调用 `/api/v3/market/data/futures_minutes/batch`，使用 GET 查询多个期货合约的历史分钟 K 线。

```bash
python <RUN_PY> futures-minutes-batch --symbols A2609.DCE --symbols IF2608.CFE --interval 1min --limit 5
```

参数：`--symbols` 至少传一次，最多 20 个；可选 `--interval`、`--start`、`--end`、`--limit`。`start` 与 `end` 为毫秒时间戳，`limit` 范围为 1～1000。

API key 从环境变量 `FTSHARE_API_KEY` 读取，并作为请求头发送。
