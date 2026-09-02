---
name: ashare-quotes-list
description: 查询A股行情列表。接口：GET /api/v1/market/data/daec/stocks/all。所有请求必须设置 FTSHARE_API_KEY。
---

# A股行情列表

接口：GET `/api/v1/market/data/daec/stocks/all`。参数和响应以 `ftshare-doc/api-doc/股票数据/行情数据/A股行情列表.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。
