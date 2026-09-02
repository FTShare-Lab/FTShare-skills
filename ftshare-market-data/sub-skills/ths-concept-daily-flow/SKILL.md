---
name: ths-concept-daily-flow
description: 查询同花顺概念板块资金流日度。接口：GET /api/v2/market/data/ths-concept-daily-flow。所有请求必须设置 FTSHARE_API_KEY。
---

# 同花顺概念板块资金流日度

接口：GET `/api/v2/market/data/ths-concept-daily-flow`。参数和响应以 `ftshare-doc/api-doc/股票数据/资金流向数据/同花顺概念板块资金流日度.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。
