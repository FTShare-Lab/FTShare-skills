---
name: intraday-auction-volume
description: 查询连续竞价成交量。接口：GET /api/v2/market/data/intraday-auction-volume。所有请求必须设置 FTSHARE_API_KEY。
---

# 连续竞价成交量

接口：GET `/api/v2/market/data/intraday-auction-volume`。参数和响应以 `ftshare-doc/api-doc/股票数据/特色数据/连续竞价成交量.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。
