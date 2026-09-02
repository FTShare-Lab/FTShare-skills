---
name: etf-minutes
description: ETF历史分钟行情。必填 --symbol；可选日期和分页参数。 用户询问ETF历史分钟行情时使用。
---

# ETF历史分钟行情

外部接口：`GET /api/v3/market/data/etf_minutes`。

必填 --symbol；可选日期和分页参数。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> etf-minutes
```

接口返回 JSON；HTTP 错误输出到 stderr 并以非零状态退出。
