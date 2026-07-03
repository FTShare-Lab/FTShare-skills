---
name: ftshare-market-data
description: 非凸科技金融数据技能集。覆盖 A 股股票列表、全字段/实时行情列表、分时价格、IPO、大宗交易、融资融券、单股行情估值、可转债、ETF、基金、指数（含分页指数描述、下载描述 PDF、权重汇总/成份明细、下载权重 xlsx、详情/K 线/分时）、宏观经济，以及港股公司介绍/估值分析/基础视图/K线、东财美股列表/历史K线/最新行情、native 美股基础信息/利润表/现金流量表/资产负债表、港股财报三表(利润/现金流/资产负债)/东财港股指数日K线等接口（market.ft.tech / ftai.chat）。用户询问 A 股、港股、美股的代码、行情、估值、K线、指数权重/描述、新闻与宏观数据时使用。
---

# FT AI Market Data Skills

本 skill 是 `ftshare-market-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> `market.ft.tech` 接口默认使用内置基础地址，接口路径统一从 `/api/v1` 开始；可通过 `FTSHARE_BASE_URL` 覆盖。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> stock-list-all-stocks
python <RUN_PY> stock-ipos --page 1 --page_size 20
python <RUN_PY> stock-ipos --all
python <RUN_PY> block-trades
python <RUN_PY> margin-trading-details --page 1 --page_size 20
python <RUN_PY> margin-trading-details --all
python <RUN_PY> semantic-search-news --query 人工智能
python <RUN_PY> semantic-search-news --query 人工智能 --limit 10 --year 2026 --start_time 2026-03-01T00:00:00+08:00 --end_time 2026-03-15T23:59:59+08:00
python <RUN_PY> cb-lists
python <RUN_PY> cb-base-data --symbol_code 110070.SH
python <RUN_PY> etf-pcfs --date 20260309
python <RUN_PY> etf-pcf-download --filename pcf_159003_20260309.xml --output pcf.xml
python <RUN_PY> fund-basicinfo-single-fund --institution-code 000001
python <RUN_PY> fund-cal-return-single-fund-specific-period --institution-code 159619 --cal-type 1Y
python <RUN_PY> fund-nav-single-fund-paginated --institution-code 000001 --page 1 --page-size 50
python <RUN_PY> fund-overview-all-funds-paginated --page 1 --page-size 20
python <RUN_PY> fund-support-symbols-all-funds-paginated --page 1 --page-size 20
python <RUN_PY> get-nth-trade-date --n 5
python <RUN_PY> financial-calendar --start-date 2026-05-01 --end-date 2026-05-07
python <RUN_PY> company-hk --trade_code 00700.HK
python <RUN_PY> hk-valuatnanalyd --trade_code 00700.HK --page 1 --page_size 20
python <RUN_PY> hk-view --hk_code 00700.HK
python <RUN_PY> hk-candlesticks --trade-code 00700.HK --interval-unit day --until-date 2026-03-24 --since-date 2026-03-01 --limit 20
python <RUN_PY> northbound --date 20250101
python <RUN_PY> southbound --date 20250101
python <RUN_PY> index-description-paginated --page 1 --page-size 20
python <RUN_PY> index-description-download --url-hash <url_hash> --output ./index-desc.pdf
python <RUN_PY> index-weight-summary --index-code 000300 --page 1 --page-size 20
python <RUN_PY> index-weight-list --index-code 000300 --page 1 --page-size 20
python <RUN_PY> index-weight-download --url-hash <url_hash> --output ./index-weights.xlsx
python <RUN_PY> eastmoney-concept-boards
python <RUN_PY> eastmoney-board-daily-ohlc --board_code BK1024 --start_date 2021-01-01 --end_date 2021-12-31 --page 1 --page_size 20
python <RUN_PY> eastmoney-board-daily-ohlc --board_code BK1024 --all
python <RUN_PY> eastmoney-board-latest-ohlc --board_code BK1024
python <RUN_PY> eastmoney-board-latest-ohlc --all
python <RUN_PY> eastmoney-board-constituents --board_code BK1024
python <RUN_PY> 10jqk-board-list
python <RUN_PY> 10jqk-board-list --module concept
python <RUN_PY> 10jqk-board-list --search 人工智能
python <RUN_PY> 10jqk-board-kline --board-code 885311 --page 1 --page-size 20
python <RUN_PY> 10jqk-board-all-kline --start-date 2026-05-20 --end-date 2026-05-25
python <RUN_PY> stock-rank-xueqiu --rank-group follow --period 7d --page 1 --page-size 20
python <RUN_PY> stock-rank-eastmoney --rank-group hot --market A
python <RUN_PY> stock-comment-index
python <RUN_PY> stock-comment-score --symbol 000001
python <RUN_PY> stock-comment-org-participate --symbol 000001
python <RUN_PY> stock-comment-desire --symbol 000001
python <RUN_PY> stock-comment-focus --symbol 000001
python <RUN_PY> stock-daec-stocks --board all --page 1 --page_size 5 --order_by "change_rate desc"
python <RUN_PY> stock-realtime-list --board chi-next --page 1 --page_size 5
python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --range Today
python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --compat v2 --since TODAY
python <RUN_PY> stock-ohlcs --symbol 600000.XSHG --compat v2 --span DAY1 --limit 5
python <RUN_PY> limit-up-pool
python <RUN_PY> limit-up-pool-yesterday
python <RUN_PY> limit-up-break-pool
python <RUN_PY> limit-down-pool
python <RUN_PY> shareholder-meeting
python <RUN_PY> shareholder-meeting --page 1 --page_size 50
python <RUN_PY> stock-unlock-by-stock --stock_code 000001
python <RUN_PY> stock-unlock-by-date --start_date 2026-06-01 --end_date 2026-06-30
python <RUN_PY> major-contract-by-date --start_date 20260526 --end_date 20260526
python <RUN_PY> major-contract-by-symbol --symbol 601668
python <RUN_PY> major-contract-summary
python <RUN_PY> eastmoney-stock-valuation --symbol 000001 --page 1 --page_size 10
python <RUN_PY> eastmoney-stock-valuation --symbol 000001 --start_date 2026-06-01 --end_date 2026-06-09
python <RUN_PY> eastmoney-stock-valuation --start_date 2026-06-01 --end_date 2026-06-09 --all
python <RUN_PY> eastmoney-market-valuation --market_code 000300 --page 1 --page_size 10
python <RUN_PY> eastmoney-market-valuation --market_code 000001 --start_date 2026-06-01 --end_date 2026-06-09
python <RUN_PY> eastmoney-market-valuation --start_date 2026-06-01 --end_date 2026-06-09 --all
python <RUN_PY> eastmoney-us-stock-list
python <RUN_PY> eastmoney-us-stock-list --page 1 --page_size 50
python <RUN_PY> eastmoney-us-stock-list --all
python <RUN_PY> eastmoney-us-stock-daily-ohlc --stock_code AAPL --page 1 --page_size 50
python <RUN_PY> eastmoney-us-stock-daily-ohlc --stock_code AAPL --start_date 2026-01-01 --end_date 2026-06-10
python <RUN_PY> eastmoney-us-stock-daily-ohlc --stock_code AAPL --start_date 2026-01-01 --end_date 2026-06-10 --all
python <RUN_PY> eastmoney-us-stock-latest-ohlc --stock_code AAPL --page 1 --page_size 20
python <RUN_PY> eastmoney-us-stock-latest-ohlc --page 1 --page_size 50
python <RUN_PY> eastmoney-us-stock-latest-ohlc --all
python <RUN_PY> stock-capital-flows --page 1 --page-size 50
python <RUN_PY> stock-capital-flows --date 20260616 --time 1530 --page 1 --page-size 50
python <RUN_PY> stock-capital-flows --date 20260616 --all
python <RUN_PY> stock-capital-flows --date 20260616 --symbol 601138.SH
python <RUN_PY> stock-capital-flows --symbol 601138.SH
python <RUN_PY> us-basic --stock_code NVDA
python <RUN_PY> us-basic --page 1 --page_size 50
python <RUN_PY> us-income --stock_code NVDA --period 2024 --report_type Q4
python <RUN_PY> us-cashflow --stock_code AAPL --period 2024 --report_type Q4
python <RUN_PY> us-balance --stock_code NVDA --period 2024 --report_type Q4
python <RUN_PY> hk-income --trade_code 00700.HK --year 2024 --report_type annual
python <RUN_PY> hk-income --trade_code 2388 --company_type bank
python <RUN_PY> hk-cashflow --stock_code 00700.HK --year 2024 --report_type annual
python <RUN_PY> hk-balance --trade_code 00700.HK --year 2024 --report_type annual
python <RUN_PY> eastmoney-hk-index-daily-kline --index_code HSI --page 1 --page_size 5
python <RUN_PY> eastmoney-hk-index-daily-kline --index_code HSCEI --start_date 2026-06-01 --end_date 2026-06-15
python <RUN_PY> hsi-daily-weight --index_slug HSI --page 1 --page_size 200
python <RUN_PY> hsi-daily-weight --trade_date 20260529 --index_slug HSCEI
python <RUN_PY> hsi-daily-weight --stock_code 0700
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

所有 `market.ft.tech` handler 默认使用内置基础地址。本地或内网服务可通过环境变量切换 API 地址：

```bash
FTSHARE_BASE_URL=http://127.0.0.1:8000/ python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --compat v2 --since TODAY
```

---

## 能力总览

### 0. 交易日工具

- **`get-nth-trade-date`**：获取当前日期的前 N 个交易日。必填：`--n`（≥1）。用户查「近 N 天」K 线时先调本接口得到 `nth_trade_date`（YYYYMMDD），可直接作为 stock-ohlcs / etf-ohlcs / index-ohlcs 的 `--since`（cb-candlesticks 仍需转为毫秒时间戳）。

### 0.5. 财经日历

- **`financial-calendar`**：按日期范围查询财经日历（华尔街见闻 + 百度财经），涵盖宏观数据公布、IPO 日程、财报时间、交易提醒等。必填：`--start-date`、`--end-date`（格式 `YYYY-MM-DD`）。**注意：多日范围可能因响应过大导致服务端截断，建议每次仅查询单日，多日需逐日调用后合并。**

### 1. 股票数据（A 股）

- **`stock-list-all-stocks`**：获取全部 A 股股票的代码和名称列表（沪深京），自动返回最新交易日数据。无需任何参数。

- **`stock-quotes-list`**：查询 A 股行情列表（分页），支持按板块筛选、多字段排序。必填参数：`--order_by`、`--page_no`、`--page_size`；可选 `--filter`、`--masks`。请求头需携带 `X-Client-Name: ft-claw`（脚本已内置）。

- **`stock-daec-stocks`**：查询 A 股行情列表 daec 全字段族，覆盖全市场、上证 A 股、深证 A 股、北证 A 股。必填：`--board`（all/xshg/xshe/bjse）；可选 `--page`、`--page_size`、`--filter`、`--order_by`、`--all`。

- **`stock-realtime-list`**：查询 A 股 stock-list 实时精简族，覆盖创业板、科创板、新股。必填：`--board`（chi-next/star/new）；可选 `--page`、`--page_size`、`--all`。**注意：该接口族没有 all 板块，全市场用 `stock-daec-stocks --board all`。**

- **`stock-intraday-prices`**：查询指定 A 股标的 1 分钟分时数据，直接映射 daec 参数。必填：`--symbol`；可选 `--range`（Today/FiveDays）、`--days`、`--ts_ms`、`--compat v2`、`--since`、`--since_ts_ms`。如需旧版 `--stock --since` 契约，可继续用 `stock-prices`。

- **`stock-ipos`**：获取 A 股 IPO 列表，含发行价格、发行数量、申购日期、上市日期等，支持分页查询。必填参数：`--page`、`--page_size`；支持 `--all` 自动翻页拉取全量数据。

- **`block-trades`**：查询 A 股大宗交易列表，含买卖方营业部、成交价、成交量、溢价率等。无需任何参数，直接返回数组。

- **`margin-trading-details`**：获取 A 股融资融券明细列表，含融资余额、融资买入额、融资偿还额、融券余量等，按融资净买入额降序排列，支持分页查询。必填参数：`--page`、`--page_size`；支持 `--all` 自动翻页拉取全量数据。

- **`stock-security-info`**：查询单只股票的实时行情与估值指标，含开高低收、多周期涨跌幅、市盈率、市净率、每股净资产等。必填参数：`--symbol`（带市场后缀，如 `600519.SH`）。接口域名为 `https://ftai.chat`（脚本内 URL 校验已允许该域名）。

### 2. 新闻 / 可转债 / ETF PCF

- **`semantic-search-news`**：语义搜索新闻，数据仅支持当年、最近半个月。必填：`--query`；可选 `--limit`、`--year`。展示时需含来源（source_site）与文章链接，并提示数据仅半个月内。
- **`cb-lists`**：可转债全量列表，无参数，数据为前一交易日。
- **`cb-base-data`**：单只可转债基础信息（转股价、转股价值、到期日等）。必填：`--symbol_code`（如 110070.SH）。若用户仅给名称，先通过 `cb-lists` 映射代码再查。
- **`etf-pcfs`**：指定日期 ETF PCF 列表。必填：`--date`（YYYYMMDD）；可选 `--page`、`--page_size`。
- **`etf-pcf-download`**：按文件名下载 PCF XML。必填：`--filename`；可选：`--output`（仅允许当前工作目录下路径）。**filename 须先由 `etf-pcfs` 列表接口取得**，勿在自动化测试中硬编码。
- **`etf-component`**：查询单只 ETF 成份股列表（代码与名称）。必填：`--symbol`（如 510300.XSHG）；接口报错或未找到时将接口返回的错误信息原样输出到 stderr。
- **`etf-pre-single`**：查询单只 ETF 盘前数据（申购赎回单位、净值、现金差额等）。必填：`--symbol`；可选：`--date`（YYYYMMDD，不传为当日 CST）；接口报错或未找到时将接口返回的错误信息原样输出到 stderr。非盘前时段可能失败，**冒烟测试建议传已知交易日 `--date`**。

### 3. 基金

- **`fund-basicinfo-single-fund`**：查询指定基金基础信息（名称、管理人、经理、类型、投资目标等）。必填：`--institution-code`（6 位基金代码）。若用户仅给基金名称，先通过 `fund-support-symbols-all-funds-paginated` 或 `fund-overview-all-funds-paginated` 映射代码再查。
- **`fund-cal-return-single-fund-specific-period`**：查询指定基金在指定区间的累计收益率时间序列。必填：`--institution-code`、`--cal-type`（1M/3M/6M/1Y/3Y/5Y/YTD）。建议先完成名称到代码映射后再调用。
- **`fund-nav-single-fund-paginated`**：查询指定基金净值历史（分页）。必填：`--institution-code`；可选：`--page`、`--page-size`。建议先完成名称到代码映射后再调用。
- **`fund-overview-all-funds-paginated`**：查询所有基金概览信息（分页）。可选：`--page`、`--page-size`。
- **`fund-support-symbols-all-funds-paginated`**：查询所有支持基金的标的列表（分页）。可选：`--page`、`--page-size`。

### 4. 港股

- **`company-hk`**：按港股交易代码查询公司介绍（名称、成立日期、注册资本、主营业务等）。必填：`--trade_code`（如 `00700.HK`）。
- **`hk-valuatnanalyd`**：分页查询港股估值分析（PE/PB/PS、股息率、换手率等）。可选：`--trade_code`、`--page`、`--page_size`。
- **`hk-view`**：按港股代码查询单票基础视图（板块、上市状态、股本、市值、估值指标）。必填：`--hk_code`。
- **`hk-candlesticks`**：按港股代码查询日/月/季/年 K 线。必填：`--trade-code`、`--interval-unit`、`--until-date`；可选：`--since-date`、`--adjust-kind`、`--interval-value`、`--limit`。
- **`northbound`**：查询指定交易日北向资金（沪股通、深股通）交易汇总数据。必填：`--date`（YYYYMMDD）。返回合计成交额及分市场（SH/SZ）成交额与笔数。
- **`southbound`**：查询指定交易日南向资金（港股通沪、港股通深）交易汇总数据。必填：`--date`（YYYYMMDD）。返回合计及分市场的买入额、卖出额、净买入额与成交笔数。

### 5. 东财板块数据

- **`eastmoney-concept-boards`**：查询东财概念板块列表，返回全量板块代码、名称及成分标的代码。无需任何参数，直接返回数组。板块代码（BK 前缀）可用于后续 K 线查询。
- **`eastmoney-board-constituents`**：查询东财指定板块的全部成分股代码和名称。必填：`--board_code`（如 BK1024）。板块代码对行业和概念板块通用。
- **`eastmoney-board-daily-ohlc`**：查询东财单板块历史 OHLC（开高低收、成交量、成交额、涨跌幅等），支持日期范围过滤与分页。必填：`--board_code`（如 BK1024）；可选：`--start_date`、`--end_date`（YYYY-MM-DD 或 YYYYMMDD）、`--page`、`--page_size`；支持 `--all` 自动翻页。板块代码对行业和概念板块通用。
- **`eastmoney-board-latest-ohlc`**：查询东财单板块最新 OHLC 行情数据，支持分页。可选：`--board_code`（不传则返回全部板块最新数据）、`--page`、`--page_size`；支持 `--all` 自动翻页。

### 6. 同花顺板块数据

- **`10jqk-board-list`**：同花顺全量板块列表（概念/证监会/行业/地域），无需参数。可选 `--module` 过滤类型（concept/csrc/industry/region）、`--search` 搜索名称/代码。板块代码用于后续 K 线查询。
- **`10jqk-board-kline`**：指定同花顺板块历史日 K 线（开高低收、成交量）。必填：`--board-code`（由 `10jqk-board-list` 获取）；可选：`--page`、`--page-size`。
- **`10jqk-board-all-kline`**：全板块 K 线按日期范围查询（分页）。可选：`--start-date`、`--end-date`（YYYY-MM-DD 或 YYYYMMDD）、`--page`、`--page-size`。

### 7. 涨跌停股池

- **`limit-up-pool`**：当日涨停股池（标的代码、涨停价、封板时间、炸板次数）。无需参数。
- **`limit-up-pool-yesterday`**：昨日涨停股池，数据结构与当日相同。无需参数。
- **`limit-up-break-pool`**：当日炸板股池（涨停后又打开的股票）。无需参数。
- **`limit-down-pool`**：当日跌停股池（标的代码、跌停价、翘板次数、封单资金）。无需参数。

### 8. 股票热度排行榜

- **`stock-rank-xueqiu`**：查询雪球平台股票排行榜（关注/讨论/交易）。可选：`--rank-group`（follow/tweet/deal）、`--period`（7d/total）、`--trade-date`（YYYY-MM-DD）、`--page`、`--page-size`（最大 100）。
- **`stock-rank-eastmoney`**：查询东方财富股票排行榜（人气榜/飙升榜），支持 A 股/港股/美股。可选：`--rank-group`（hot/up）、`--market`（A/HK/US）、`--trade-date`（YYYY-MM-DD）。

### 9. 公司行动（股东大会 / 限售解禁 / 重大合同）

#### 股东大会

- **`shareholder-meeting`**：查询 A 股上市公司股东大会信息（会议日期、股权登记日、投票日期、提案内容等），支持分页。可选：`--page`、`--page_size`。

#### 限售解禁

- **`stock-unlock-by-stock`**：按证券代码查询限售解禁批次及股东明细（解禁日期、解禁市值、占总股本比例、股东明细等），支持分页。必填：`--stock_code`（6 位代码）；可选 `--page`、`--page_size`。
- **`stock-unlock-by-date`**：按解禁日期范围查询限售解禁批次及股东明细，支持分页。必填：`--start_date`、`--end_date`（格式 YYYY-MM-DD）；可选 `--page`、`--page_size`。

#### 重大合同

- **`major-contract-by-date`**：按公告日期范围查询 A 股重大合同（签约方、合同金额、合同类型、占营收比例等）。必填：`--start_date`、`--end_date`（格式 YYYYMMDD）。
- **`major-contract-by-symbol`**：按股票代码查询重大合同历史，按公告日期降序，支持分页。必填：`--symbol`（6 位代码）；可选 `--page`、`--page_size`。
- **`major-contract-summary`**：近一年个股重大合同汇总排名（合同数量、合同总额、占营收比），按合同总额降序，支持分页。可选：`--page`、`--page_size`。

### 10. 千股千评

- **`stock-comment-index`**：查询东方财富千股千评综合诊断主表，含收盘价、涨跌幅、换手率、市盈率、主力成本、机构参与度、综合评分、排名、关注指数。无参数，返回全量（约 5000+ 条）。
- **`stock-comment-score`**：查询指定股票的历史综合评分走势。必填：`--symbol`（6 位代码）。
- **`stock-comment-org-participate`**：查询指定股票的历史机构参与度走势。必填：`--symbol`（6 位代码）。
- **`stock-comment-desire`**：查询指定股票的市场参与意愿及 5 日均值变化。必填：`--symbol`（6 位代码）。
- **`stock-comment-focus`**：查询指定股票的市场热度用户关注指数、排名及变动。必填：`--symbol`（6 位代码）。

### 11. 估值分析数据

- **`eastmoney-stock-valuation`**：查询东财个股日估值数据（PE TTM/LYR、PB、市现率、市销率、PEG、总市值、流通市值、收盘价等）。可选：`--symbol`、`--trade_date`、`--start_date`、`--end_date`、`--page`、`--page_size`；支持 `--all` 自动翻页。**推荐使用区间查询**（`--start_date` + `--end_date`），当前单日查询可能返回空。
- **`eastmoney-market-valuation`**：查询东财市场日估值数据（上证指数/沪深300/深证成指/创业板指/科创50/北证50 的 PE、总市值、流通市值、收盘点位等）。可选：`--market_code`、`--trade_date`、`--start_date`、`--end_date`、`--page`、`--page_size`；支持 `--all` 自动翻页。**推荐使用区间查询**。

### 12. 东财美股数据

- **`eastmoney-us-stock-list`**：获取东财美股全量列表（~5700+ 只），含代码、名称、市值、最新价、涨跌幅、市盈率等，支持服务端分页（500 条/页）。可选：`--page`、`--page_size`；`--all` 返回全量。**注意**：不覆盖苹果等美股大盘蓝筹，以东财中小盘和中概股为主。
- **`eastmoney-us-stock-daily-ohlc`**：查询东财美股历史日 K 线（开高低收、成交量、成交额、振幅）。有日期范围时按 3 天窗口分批请求避免服务端 500，无日期范围时全量拉取。必填：`--stock_code`（东财美股代码如 `AAL`）；可选：`--start_date`、`--end_date`（YYYY-MM-DD 或 YYYYMMDD）、`--page`、`--page_size`；支持 `--all`。**注意**：全部数值字段按字符串返回。
- **`eastmoney-us-stock-latest-ohlc`**：查询东财美股最新一根日 K 线行情，支持分页与单票过滤。可选：`--stock_code`（不传返回全部美股）、`--page`、`--page_size`；支持 `--all` 自动翻页。**注意**：价格字段为字符串，成交量/振幅为数值。

### 13. 资金流向（15 分钟切片）

- **`stock-capital-flows`**：查询 A 股股票资金流向（主力净流入，15 分钟级别）。**凡问"分钟级 / 15 分钟级 / 分时资金流"一律用本 skill。**不传 `--date` 返回当前实时快照；传入 `--date`（YYYYMMDD）返回该日指定 15 分钟切片快照，默认 `--time 1530`（日终），`--time` 分钟须为 00/15/30/45。可选 `--page`、`--page-size`；支持 `--all` 自动翻页；支持 `--symbol 601138.SH` 单股定位（逐页扫描，返回全市场排名 + 单条记录，可叠加 `--date`/`--time` 查某只票某切片）。仅 A 股（不含 ETF/指数），按主力净流入降序；金额字段以字符串返回，单位元。

### 14. 美股基础信息与财报（native）

> 与 `eastmoney-us-stock-list`（东财**行情**：最新价/市值/PE）区别：本节为 native **基础信息 + 财报三表**。

- **`us-basic`**：查询美股基础信息（代码、中英文名、上市/退市日期），~5315 只。可选 `--stock_code`（纯代码如 `NVDA`，传则精确查单股）、`--page`、`--page_size`；支持 `--all`。查"美股有哪些/代码/名称/上市日期"用本接口。
- **`us-income`**：查询美股利润表（长表 EAV）。必填 `--stock_code`；可选 `--period`（财年）、`--report_type`（`Q1/Q2/Q3/Q4/H1`）、`--start_date`/`--end_date`（YYYYMMDD）、`--page`/`--page_size`；支持 `--all`。
- **`us-cashflow`**：查询美股现金流量表（长表 EAV），参数同 `us-income`。
- **`us-balance`**：查询美股资产负债表（长表 EAV，时点数据），参数同 `us-income`。
- 财报三表共用要点：**长表 EAV**（每行一科目）、**按报告期分页**（`page_size` 限报告期数，`items` 行数可能 ≫ `page_size`，`total_items` 是报告期数）、**Q4/Q3 返回累计+单季两套**、**美股财年非自然年**（`period` 匹配 `stmt_year`）、数值为字符串、只输出非 0 科目。

### 15. 港股财报与港股指数（native + 东财）

> 与 §4 港股（公司介绍/估值/视图/K线）互补：本节为**港股财报三表**与**东财港股指数日K线**。

- **`hk-income`**：查询港股利润表（宽表）。按公司类型分子接口：`--company_type gene`(一般企业,默认)/`bank`(银行)/`insur`(保险)。可选 `--trade_code`（`00700.HK` 或 `700`）、`--year`+`--report_type`（`annual`/`semi`，须成对，仅最近 3 年）、`--start_date`/`--end_date`（YYYYMMDD）、`--page`/`--page_size`；支持 `--all`。**至少一个过滤条件**，否则 400。
- **`hk-cashflow`**：查询港股现金流量表（宽表，111 字段）。参数同上，但**股票代码用 `--stock_code`（非 `trade_code`）**。
- **`hk-balance`**：查询港股资产负债表（宽表，时点数据）。按公司类型分子接口（`--company_type gene/bank/insur`），参数同 `hk-income`。
- **`eastmoney-hk-index-daily-kline`**：查询东财港股指数（恒生 HSI / 国企 HSCEI / 恒生科技 HSTECH 等）日 K 线（开高低收、量额、振幅、涨跌幅/涨跌额、换手率）。可选 `--index_code`、`--trade_date`（YYYY-MM-DD）、`--start_date`+`--end_date`（YYYY-MM-DD）、`--page`/`--page_size`；支持 `--all`。**响应信封不同：数据在 `data.records`，非 `items`**。
- **`hsi-daily-weight`**：查询恒生系列指数**成份股权重**（HSI 恒生 / HSCEI 国企 / HSAIT）。可选 `--trade_date`（YYYYMMDD，与 start/end 互斥）、`--start_date`+`--end_date`（YYYYMMDD）、`--index_slug`、`--stock_code`（4 位如 `0700`）、`--page`/`--page_size`；支持 `--all`。**⚠️ HSAIT 的"恒生科技"映射存疑**（实测返回 40 只且含中国移动，与官方 HSTECH 的 30 只/8% 上限/不含中国移动不符）——HSI/HSCEI 可用，**HSAIT 勿当恒生科技用**。响应信封 `data.records`，`weight_pct` 为字符串百分数（未缩放）。
- 港股财报三表要点：**宽表**（一行一个报告期，科目为列，非 EAV）、`report_type` 仅 `annual`/`semi`、`year` 限最近 3 年且须与 `report_type` 成对、金额字段为 Decimal 字符串或 null、单位依 `currency`（常为千元/百万元口径）。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「能力总览」匹配对应子 skill 名称。
3. （可选）读取 `<RUN_PY>` 同级目录 `sub-skills/<子skill名>/SKILL.md` 了解接口详情与参数。
4. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出。
5. **解析并输出**：以表格或要点形式展示给用户。

---

## 子 skill 与用户问法示例

| 用户问法示例 | 子 skill 名 |
|---|---|
| 「列出所有 A 股股票」 | `stock-list-all-stocks` |
| 「A 股有哪些股票代码？」 | `stock-list-all-stocks` |
| 「获取全市场股票列表」 | `stock-list-all-stocks` |
| 「A 股行情列表、按涨跌幅排序、分页」 | `stock-quotes-list` |
| 「全市场 / 上证 / 深证 / 北证 A 股实时行情全字段」 | `stock-daec-stocks` |
| 「创业板 / 科创板 / 新股实时行情精简列表」 | `stock-realtime-list` |
| 「科创板/创业板股票行情列表」 | `stock-realtime-list` |
| 「查看 A 股 IPO 列表」 | `stock-ipos` |
| 「最近有哪些新股上市？」 | `stock-ipos` |
| 「查询某只股票的发行价格 / 申购日期」 | `stock-ipos` |
| 「查看今天的大宗交易记录」 | `block-trades` |
| 「哪些股票有大宗交易？买卖方是谁？」 | `block-trades` |
| 「大宗交易溢价率最高的是哪只？」 | `block-trades` |
| 「融资净买入最多的股票有哪些？」 | `margin-trading-details` |
| 「查看最新的融资融券明细数据」 | `margin-trading-details` |
| 「哪只股票融资余额最高？」 | `margin-trading-details` |
| 「查一下贵州茅台的股价」 | `stock-security-info` |
| 「000001.SZ 的市盈率是多少？」 | `stock-security-info` |
| 「某只股票的市值、涨跌幅、估值」 | `stock-security-info` |
| 「语义搜索新闻」「按关键词搜新闻」 | `semantic-search-news` |
| 「可转债列表」「全部可转债」「转债代码列表」 | `cb-lists` |
| 「某只可转债详情」「转股价/转股价值/到期日」 | `cb-base-data` |
| 「ETF PCF 列表」「申购赎回清单」「指定日期 PCF」 | `etf-pcfs` |
| 「下载 PCF 文件」「PCF XML 内容」 | `etf-pcf-download` |
| 「前 N 个交易日」「近 N 天交易日」「往前推 N 个交易日」（查近几天 K 线时先调再转时间戳） | `get-nth-trade-date` |
| 「财经日历」「本周有哪些经济事件」「宏观经济数据公布时间」「IPO 日程」「财报时间」「交易提醒」「分红送转提醒」 | `financial-calendar` |
| 「某只 ETF 成份股」「ETF 持仓」「510300 成份」「沪深300ETF 成份列表」 | `etf-component` |
| 「某只 ETF 盘前」「ETF 申购赎回单位」「净值/现金差额」「510300 盘前」 | `etf-pre-single` |
| 「基金基本信息」「某只基金详情」「基金管理人/基金经理」「基金类型/投资目标」 | `fund-basicinfo-single-fund` |
| 「基金累计收益率」「近1年/近3个月收益」「YTD 收益」「基金收益曲线」 | `fund-cal-return-single-fund-specific-period` |
| 「基金净值」「单位净值/累计净值」「日增长率」「基金净值历史」 | `fund-nav-single-fund-paginated` |
| 「基金概览」「所有基金信息」「基金列表概况」 | `fund-overview-all-funds-paginated` |
| 「支持的基金列表」「基金代码清单」「所有基金标的」 | `fund-support-symbols-all-funds-paginated` |
| 「港股公司简介」「00700 公司介绍」 | `company-hk` |
| 「港股估值」「港股市盈率/市净率」 | `hk-valuatnanalyd` |
| 「港股基础视图」「主板/上市状态/总市值」 | `hk-view` |
| 「港股K线」「00700 日线/月线/季线/年线」 | `hk-candlesticks` |
| 「指数描述分页」「指数简介列表」「下载指数描述 PDF（先有 url_hash）」 | `index-description-paginated` / `index-description-download` |
| 「指数权重汇总」「成份权重明细」「下载权重 Excel（先有 url_hash）」 | `index-weight-summary` / `index-weight-list` / `index-weight-download` |
| 「某只指数详情/K 线/分时」 | `index-detail` / `index-ohlcs` / `index-prices`（见下文「FT 指数数据 Skills」） |
| 「东财概念板块列表」「东财板块代码」 | `eastmoney-concept-boards` |
| 「东财板块 K 线」「东财概念历史行情」 | `eastmoney-board-daily-ohlc` |
| 「东财板块最新行情」「东财板块 OHLC」 | `eastmoney-board-latest-ohlc` |
| 「东财板块成分股」 | `eastmoney-board-constituents` |
| 「同花顺板块列表」「概念/行业/地域板块有哪些」 | `10jqk-board-list` |
| 「某板块 K 线」「5G 概念走势」「某板块历史行情」 | `10jqk-board-kline` |
| 「最近几天所有板块 K 线」「全板块行情」 | `10jqk-board-all-kline` |
| 「今天涨停」「涨停板」「涨停股池」 | `limit-up-pool` |
| 「昨天涨停」「昨日涨停股」 | `limit-up-pool-yesterday` |
| 「炸板」「涨停炸板」「打开涨停」 | `limit-up-break-pool` |
| 「今天跌停」「跌停板」「跌停股池」 | `limit-down-pool` |
| 「雪球热搜」「雪球关注榜」「雪球讨论榜」「雪球交易榜」 | `stock-rank-xueqiu` |
| 「东财人气榜」「东方财富热搜」「股票热度」「人气飙升榜」 | `stock-rank-eastmoney` |
| 「股东会」「股东大会」「近期股东大会」「股权登记日」「投票日期」 | `shareholder-meeting` |
| 「某股票限售解禁」「解禁日期」「解禁市值」 | `stock-unlock-by-stock` |
| 「近期解禁」「本月解禁」「解禁日历」 | `stock-unlock-by-date` |
| 「重大合同」「今天签了哪些大单」「合同金额」 | `major-contract-by-date` |
| 「某公司签了哪些重大合同」「某股票合同历史」 | `major-contract-by-symbol` |
| 「重大合同排行榜」「哪些公司合同金额最大」「合同总额排名」 | `major-contract-summary` |
| 「千股千评」「股票综合诊断」「股票评分排名」 | `stock-comment-index` |
| 「某股票历史评分」「综合评分走势」 | `stock-comment-score` |
| 「机构参与度」「机构关注度」 | `stock-comment-org-participate` |
| 「市场参与意愿」「散户参与度」 | `stock-comment-desire` |
| 「用户关注指数」「市场关注度排名」 | `stock-comment-focus` |
| 「股票估值」「个股市盈率」「市净率」「PEG」 | `eastmoney-stock-valuation` |
| 「某只股票估值走势」「历史PE/PB」 | `eastmoney-stock-valuation` |
| 「全市场股票估值」「某日全市场市盈率」 | `eastmoney-stock-valuation` |
| 「市场估值」「上证指数PE」「沪深300市盈率」 | `eastmoney-market-valuation` |
| 「指数估值」「市场市盈率走势」「科创50估值」 | `eastmoney-market-valuation` |
| 「创业板估值」「深证成指PE」「北证50估值」 | `eastmoney-market-valuation` |
| 「美股列表」「东财美股」「美股代码有哪些」 | `eastmoney-us-stock-list` |
| 「美股K线」「美股日线」「美股历史行情」「美股OHLC」 | `eastmoney-us-stock-daily-ohlc` |
| 「美股最新行情」「美股最新价」「某只美股最新 K 线」 | `eastmoney-us-stock-latest-ohlc` |
| 「资金流向」「主力净流入」「个股资金流」「资金流排名」 | `stock-capital-flows` |
| 「15分钟资金流」「分钟级资金流」「分时资金流」「某日某时刻资金流切片」「日终资金流」 | `stock-capital-flows` |
| 「某只票资金流」「工业富联资金流」「601138 主力净流入」 | `stock-capital-flows --symbol <代码>` |
| 「美股有哪些」「全部美股」「美股代码列表」「美股上市日期」「某美股中英文名」 | `us-basic` |
| 「美股最新价」「美股市值」「美股涨跌幅」「美股PE」「东财美股」 | `eastmoney-us-stock-list` |
| 「美股利润表」「美股营收/净利润/EPS」「某美股财报」 | `us-income` |
| 「美股现金流量表」「美股经营/投资/筹资现金流」「美股资本支出」 | `us-cashflow` |
| 「美股资产负债表」「美股资产/负债/所有者权益」 | `us-balance` |
| 「港股利润表」「港股营收/净利润/EPS」「某港股财报」 | `hk-income` |
| 「港股现金流量表」「港股经营/投资/融资现金流」 | `hk-cashflow`（用 `--stock_code`） |
| 「港股资产负债表」「港股资产/负债/所有者权益」 | `hk-balance` |
| 「港股指数K线」「恒生指数走势」「国企指数/恒生科技日线」 | `eastmoney-hk-index-daily-kline` |
| 「港股指数权重」「恒生指数成份股权重」「国企指数权重」「某股在恒指权重」 | `hsi-daily-weight`（HSAIT 存疑，见说明） |

# FT A-share 公告与研报数据 Skills

本 skill 是 `FTShare-ashare-announcement-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> `market.ft.tech` 接口默认使用内置基础地址，接口路径统一从 `/api/v1` 开始；可通过 `FTSHARE_BASE_URL` 覆盖。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> stock-announcements-all-stocks-specific-date --start-date 20241231 --page 1 --page-size 20
python <RUN_PY> stock-announcements-single-stock-all-periods --stock-code 000001.SZ --page 1 --page-size 20
python <RUN_PY> stock-announcements-specific-url-hash --url-hash <hash> --output announcement.pdf
python <RUN_PY> stock-reports-all-stocks-specific-date --start-date 20241231 --page 1 --page-size 20
python <RUN_PY> stock-reports-single-stock-all-periods --stock-code 000001.SZ --page 1 --page-size 20
python <RUN_PY> stock-reports-specific-url-hash --url-hash <hash> --output report.pdf
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 能力总览

### 1. 公告

- **`stock-announcements-all-stocks-specific-date`**：指定日期全市场股票公告列表（分页）。必填参数：`--start-date`（YYYYMMDD）；可选 `--page`、`--page-size`。

- **`stock-announcements-single-stock-all-periods`**：单只股票公告历史（分页）。必填参数：`--stock-code`（带市场后缀，如 `000001.SZ`）；可选 `--page`、`--page-size`。

- **`stock-announcements-specific-url-hash`**：通过 url_hash 查询/下载单条公告 PDF。必填参数：`--url-hash`；可选 `--output`（保存文件名）。

### 2. 研报

- **`stock-reports-all-stocks-specific-date`**：指定日期全市场股票研报列表（分页）。必填参数：`--start-date`（YYYYMMDD）；可选 `--page`、`--page-size`。

- **`stock-reports-single-stock-all-periods`**：单只股票研报历史（分页）。必填参数：`--stock-code`（带市场后缀）；可选 `--page`、`--page-size`。

- **`stock-reports-specific-url-hash`**：通过 url_hash 查询/下载单条研报 PDF。必填参数：`--url-hash`；可选 `--output`（保存文件名）。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「能力总览」匹配对应子 skill 名称。
3. （可选）读取 `<RUN_PY>` 同级目录 `sub-skills/<子skill名>/SKILL.md` 了解接口详情与参数。
4. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出。
5. **解析并输出**：以表格或要点形式展示给用户。

---

## 子 skill 与用户问法示例

| 用户问法示例 | 子 skill 名 |
|---|---|
| 「今天/某天的公告列表」 | `stock-announcements-all-stocks-specific-date` |
| 「指定日期全市场公告」 | `stock-announcements-all-stocks-specific-date` |
| 「某只股票的历史公告」 | `stock-announcements-single-stock-all-periods` |
| 「下载某条公告 PDF」 | `stock-announcements-specific-url-hash` |
| 「今天/某天的研报列表」 | `stock-reports-all-stocks-specific-date` |
| 「指定日期全市场研报」 | `stock-reports-all-stocks-specific-date` |
| 「某只股票的历史研报」 | `stock-reports-single-stock-all-periods` |
| 「下载某条研报 PDF」 | `stock-reports-specific-url-hash` |

# FT AI A 股股东数据 Skills

本 skill 是 `FTShare-ashare-holder-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> `market.ft.tech` 接口默认使用内置基础地址，接口路径统一从 `/api/v1` 开始；可通过 `FTSHARE_BASE_URL` 覆盖。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>`。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> stock-holder-ten --stock_code 603323.SH
python <RUN_PY> stock-holder-ften --stock_code 603323.SH
python <RUN_PY> stock-holder-nums --stock_code 603323.SH
python <RUN_PY> pledge-summary
python <RUN_PY> pledge-detail --stock_code 603323.SH
python <RUN_PY> stock-share-chg --stock_code 603323.SH
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 能力总览

### 1. 十大股东

- **`stock-holder-ten`**：查询单只 A 股股票所有公告期的十大股东信息，含持股比例、股东明细、变动类型等。必填参数：`--stock_code`（如 `603323.SH`）。

### 2. 十大流通股东

- **`stock-holder-ften`**：查询单只 A 股股票所有公告期的十大流通股东信息，含流通持股比例、股东明细、变动类型等（`unlimit_num` 固定为 null）。必填参数：`--stock_code`（如 `603323.SH`）。

### 3. 股东人数

- **`stock-holder-nums`**：查询单只 A 股股票所有公告期的股东人数信息，含股东总人数、人数变化率、人均流通股数、人均持股金额、十大股东/流通股东持股比例等。必填参数：`--stock_code`（如 `603323.SH`）。

### 4. 股权质押总揽

- **`pledge-summary`**：查询 A 股市场所有报告期的股权质押总揽数据，含质押公司数量、质押笔数、质押总股数、质押总市值、沪深300指数及周涨跌幅。无需任何参数，返回值为数组（无分页包装）。

### 5. 股权质押个股详情

- **`pledge-detail`**：查询单只 A 股股票所有报告期的股权质押详细信息，含质押比例、质押笔数、质押市值、无限售/限售质押股数、较上年变动等。必填参数：`--stock_code`（如 `603323.SH`）；可选参数：`--page`、`--page_size`，返回值含分页信息。

### 6. 股东增减持

- **`stock-share-chg`**：查询单只 A 股股票所有报告期的股东增减持信息，含变动股东名称、变动类型（增持/减持）、变动数量、变动前后持股数量、最新股价及涨跌幅、变动日期区间、公告日期等。必填参数：`--stock_code`（如 `603323.SH`）；可选参数：`--page`、`--page_size`，返回值含分页信息。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「能力总览」匹配对应子 skill 名称。
3. （可选）读取 `<RUN_PY>` 同级目录 `sub-skills/<子skill名>/SKILL.md` 了解接口详情与参数。
4. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出。
5. **解析并输出**：以表格或要点形式展示给用户。

---

## 子 skill 与用户问法示例

| 用户问法示例 | 子 skill 名 |
|---|---|
| 「603323.SH 的十大股东是哪些？」 | `stock-holder-ten` |
| 「查看某只股票历期前十大股东变动」 | `stock-holder-ten` |
| 「某股票的大股东持股比例是多少？」 | `stock-holder-ten` |
| 「某股票最新一期十大股东有哪些新进股东？」 | `stock-holder-ten` |
| 「603323.SH 的十大流通股东是哪些？」 | `stock-holder-ften` |
| 「查看某只股票历期前十大流通股东变动」 | `stock-holder-ften` |
| 「某股票流通股东的持股比例是多少？」 | `stock-holder-ften` |
| 「603323.SH 的股东人数是多少？」 | `stock-holder-nums` |
| 「查看某只股票历期股东人数变化趋势」 | `stock-holder-nums` |
| 「某股票人均持股金额是多少？」 | `stock-holder-nums` |
| 「A 股市场整体股权质押情况如何？」 | `pledge-summary` |
| 「全市场质押公司数量和质押总市值是多少？」 | `pledge-summary` |
| 「查看历期股权质押总揽数据」 | `pledge-summary` |
| 「603323.SH 的股权质押详情是什么？」 | `pledge-detail` |
| 「某股票历期质押比例和质押笔数是多少？」 | `pledge-detail` |
| 「某股票最新一期股权质押市值是多少？」 | `pledge-detail` |
|| 「603323.SH 的股东增减持情况如何？」 | `stock-share-chg` |
|| 「某股票最近有哪些股东在减持？」 | `stock-share-chg` |
|| 「某股东对某股票的持股变动历史」 | `stock-share-chg` |

# FT A-share 业绩大全 Skills

本 skill 是 `FTShare-ashare-performance-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> `market.ft.tech` 接口默认使用内置基础地址，接口路径统一从 `/api/v1` 开始；可通过 `FTSHARE_BASE_URL` 覆盖。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> stock-performance-express-all-stocks-specific-period --year 2025 --report-type q2 --page 1 --page-size 20
python <RUN_PY> stock-performance-express-single-stock-all-periods --stock-code 000001.SZ --page 1 --page-size 50
python <RUN_PY> stock-performance-forecast-all-stocks-specific-period --year 2025 --report-type annual --page 1 --page-size 20
python <RUN_PY> stock-performance-forecast-single-stock-all-periods --stock-code 000001.SZ --page 1 --page-size 50
python <RUN_PY> stock-cashflow-single-stock-all-periods --stock-code 000001.SZ
python <RUN_PY> stock-cashflow-all-stocks-specific-period --year 2025 --report-type q2 --page 1 --page-size 20
python <RUN_PY> stock-income-single-stock-all-periods --stock-code 000001.SZ
python <RUN_PY> stock-income-all-stocks-specific-period --year 2025 --report-type q2 --page 1 --page-size 20
python <RUN_PY> stock-balance-single-stock-all-periods --stock-code 000001.SZ
python <RUN_PY> stock-balance-all-stocks-specific-period --year 2025 --report-type q2 --page 1 --page-size 20
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 能力总览

### 1. 业绩快报 / 业绩预告

- **`stock-performance-express-all-stocks-specific-period`**：单一报告期（如 2025Q2）全市场业绩快报列表（分页）。必填：`--year`、`--report-type`；可选 `--page`、`--page-size`。
- **`stock-performance-express-single-stock-all-periods`**：单只股票历期业绩快报（分页）。必填：`--stock-code`；可选 `--page`、`--page-size`。
- **`stock-performance-forecast-all-stocks-specific-period`**：单一报告期全市场业绩预告列表（分页）。必填：`--year`、`--report-type`；可选 `--page`、`--page-size`。
- **`stock-performance-forecast-single-stock-all-periods`**：单只股票历期业绩预告（分页）。必填：`--stock-code`；可选 `--page`、`--page-size`。

### 2. 现金流量表

- **`stock-cashflow-single-stock-all-periods`**：单只股票所有报告期现金流量表。必填：`--stock-code`。
- **`stock-cashflow-all-stocks-specific-period`**：指定报告期全市场现金流量表（分页）。必填：`--year`、`--report-type`、`--page`、`--page-size`。

### 3. 利润表

- **`stock-income-single-stock-all-periods`**：单只股票所有报告期利润表。必填：`--stock-code`。
- **`stock-income-all-stocks-specific-period`**：指定报告期全市场利润表（分页）。必填：`--year`、`--report-type`、`--page`、`--page-size`。

### 4. 资产负债表

- **`stock-balance-single-stock-all-periods`**：单只股票所有报告期资产负债表。必填：`--stock-code`。
- **`stock-balance-all-stocks-specific-period`**：指定报告期全市场资产负债表（分页）。必填：`--year`、`--report-type`、`--page`、`--page-size`。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「能力总览」匹配对应子 skill 名称。
3. （可选）读取 `sub-skills/<子skill名>/SKILL.md` 了解接口详情与参数。
4. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出。
5. **解析并输出**：以表格或要点形式展示给用户。

---

## 子 skill 与用户问法示例

| 用户问法示例 | 子 skill 名 |
|--------------|-------------|
| 「2025 年二季报/半年报业绩快报」「指定报告期全市场业绩快报」 | `stock-performance-express-all-stocks-specific-period` |
| 「某只股票历期业绩快报」 | `stock-performance-express-single-stock-all-periods` |
| 「2025 年年报业绩预告」「指定报告期全市场业绩预告」 | `stock-performance-forecast-all-stocks-specific-period` |
| 「某只股票历期业绩预告」 | `stock-performance-forecast-single-stock-all-periods` |
| 「某只股票现金流量表」「历期现金流量表」 | `stock-cashflow-single-stock-all-periods` |
| 「2025 年二季报全市场现金流量表」 | `stock-cashflow-all-stocks-specific-period` |
| 「某只股票利润表」「历期利润表」 | `stock-income-single-stock-all-periods` |
| 「2025 年二季报全市场利润表」 | `stock-income-all-stocks-specific-period` |
| 「某只股票资产负债表」「历期资产负债表」 | `stock-balance-single-stock-all-periods` |
| 「2025 年二季报全市场资产负债表」 | `stock-balance-all-stocks-specific-period` |

# FT ETF 数据 Skills

本 skill 是 `FTShare-etf-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」或「询问方式与子 skill 对应表」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> `market.ft.tech` 接口默认使用内置基础地址，请求头需携带 `X-Client-Name: ft-claw`（各子 skill 脚本已内置），接口路径统一从 `/api/v1` 开始；可通过 `FTSHARE_BASE_URL` 覆盖。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> etf-detail --etf 510050.XSHG
python <RUN_PY> etf-description-all
python <RUN_PY> etf-list-paginated --order_by "change_rate desc" --page_size 20 --page_no 1
python <RUN_PY> etf-ohlcs --etf 510050.XSHG --since 20240101 --until 20240131
python <RUN_PY> etf-prices --etf 510050.XSHG --since TODAY
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## ETF — 询问方式与子 skill 对应表

| 询问方式（用户常说的词） | 子 skill |
|------------------------|----------|
| 某只 **ETF 详情**、**510050 行情**、**上证50ETF** 涨跌幅、ETF **跟踪指数/市值**、某只 ETF 名称/盘口 | `etf-detail` |
| **全部 ETF 基础信息**、**ETF 代码与名称映射**、**按名称找 ETF 代码**、ETF **symbol 对照表** | `etf-description-all` |
| **ETF 列表**、**全市场 ETF**、**按涨跌幅排序的 ETF**、**筛选某类 ETF** | `etf-list-paginated` |
| 某只 ETF 的 **K 线**、**510050 日线/周线/月线**、ETF **开高低收**、**前/后复权** | `etf-ohlcs` |
| 某只 ETF **分时**、**510050 当日分时**、ETF **一分钟行情**、**多日分时走势** | `etf-prices` |

---

## 能力总览

- **`etf-detail`**：查询单只 ETF 详情（名称、行情、盘口、市值、涨跌幅、跟踪指数、投资类型等）。必填：`--etf`；可选 `--masks`。
- **`etf-description-all`**：查询全部 ETF 基础信息（symbol/name/asset_class 等）。无参数。用户仅给名称时，先用本接口将名称映射到唯一 `symbol` 再查详情/指标。
- **`etf-list-paginated`**：ETF 分页列表，支持分页、排序、筛选。可选：`--order_by`/`--ob`、`--filter`、`--masks`、`--page_size`、`--page_no`、`--filter_index`。
- **`etf-ohlcs`**：查询单只 ETF OHLC K 线（开高低收、成交量、成交额，daec 日期区间）。必填：`--etf`、`--since`（YYYYMMDD）；可选 `--until`（YYYYMMDD，默认今天）、`--interval`（Day/Week/Month，默认 Day）、`--adjust`（Forward/Backward）。无年线、无 MA。
- **`etf-prices`**：查询单只 ETF 分钟级分时价格。必填：`--etf`；时间范围二选一：`--since`（TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(n)）或 `--since_ts_ms`。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「询问方式与子 skill 对应表」或「能力总览」匹配子 skill 名称。
3. **若用户给的是 ETF 名称/简称**：先调用 `etf-description-all`（或 `etf-list-paginated`）获取候选，确定标准代码（如 `510050.XSHG`）。
4. （可选）读取 `sub-skills/<子skill名>/SKILL.md` 了解接口与参数。
5. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出（详情/K 线/分时等统一使用代码参数）。
6. **解析并输出**：以表格或要点形式展示给用户；若候选代码不唯一，先让用户确认再查询指标。

# FT 指数数据 Skills

以下指数相关子 skill 由 **`ftshare-market-data`** 同目录 `run.py` 统一调度（与股票、港股等子 skill 共用入口）。

根据用户问题，从下方「能力总览」或「询问方式与子 skill 对应表」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> `market.ft.tech` 接口默认使用内置基础地址，请求头需携带 `X-Client-Name: ft-claw`（各子 skill 脚本已内置），接口路径统一从 `/api/v1` 开始；可通过 `FTSHARE_BASE_URL` 覆盖。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>` 。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> index-description-all
python <RUN_PY> index-description-paginated --page 1 --page-size 20
python <RUN_PY> index-description-download --url-hash <从列表接口取得的url_hash> --output ./index-desc.pdf
python <RUN_PY> index-weight-summary --index-code 000300 --page 1 --page-size 20
python <RUN_PY> index-weight-list --index-code 000300 --date 20250320 --page 1 --page-size 20
python <RUN_PY> index-weight-download --url-hash <url_hash> --output ./index-weights.xlsx
python <RUN_PY> index-detail --index 000001.XSHG
python <RUN_PY> index-list-paginated --order_by "change_rate desc" --page_size 20 --page_no 1
python <RUN_PY> index-ohlcs --index 000001.XSHG --since 20240101 --until 20240131
python <RUN_PY> index-prices --index 000001.XSHG --since TODAY
python <RUN_PY> get-nth-trade-date --n 5
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 指数 — 询问方式与子 skill 对应表

| 询问方式（用户常说的词） | 子 skill |
|------------------------|----------|
| **全部指数基础信息**、**指数列表（PB/PE）**、**有哪些指数**、指数 **简称/全称**、**市净率/市盈率 TTM**、**指数名称查代码**（带交易所后缀） | `index-description-all` |
| **指数描述分页**、**指数简介列表**、**url_hash**（下载描述文件前查列表）、**指数名称查代码**（纯 6 位代码） | `index-description-paginated` |
| **下载指数描述**、**指数说明 PDF**、**指数简介文件**（需先有 url_hash） | `index-description-download` |
| **指数权重汇总**、**权重期数**、**权重 date/url_hash**（下载权重文件前查列表） | `index-weight-summary` |
| **指数成份权重**、**权重明细**、**沪深300 成份权重**、单期权重列表 | `index-weight-list` |
| **下载指数权重**、**权重 xlsx**、**成份权重 Excel**（需先有 url_hash） | `index-weight-download` |
| 某只 **指数详情**、**上证指数行情**、**沪深300** 点位/涨跌幅、指数名称/成交 | `index-detail` |
| **指数列表**、**全市场指数**、**按涨跌幅排序的指数**、**筛选某类指数** | `index-list-paginated` |
| 某只指数的 **K 线**、**上证指数日线/周线/月线**、指数 **开高低收**、**前/后复权** | `index-ohlcs` |
| 某只指数 **分时**、**上证指数当日分时**、指数 **一分钟行情**、**多日分时走势** | `index-prices` |
| **前 N 个交易日**、**近 N 天交易日**、**往前推 N 个交易日**（查近几天 K 线时先调此接口再转时间戳） | `get-nth-trade-date` |

---

## 能力总览

- **`get-nth-trade-date`**：获取当前日期的前 N 个交易日。必填：`--n`（≥1）。查「近 N 天」K 线时先调本接口得到 `nth_trade_date`（YYYYMMDD），可直接作为 index-ohlcs 的 `--since`。
- **`index-description-all`**：查询全部指数基础信息（symbol、全称、简称、pb、pe_ttm）。无需参数；`GET /api/v1/market/data/index-description-all`。
- **`index-description-paginated`**（描述链 ①）：分页查询指数描述列表（`index_code`、`index_name`、`index_intro`、`url_hash` 等）。可选：`--page`（默认 1）、`--page-size`（默认 20，最大 100）；`GET /api/v1/market/data/index/index_description`。
- **`index-description-download`**（描述链 ②）：按 `url_hash` 下载指数描述 PDF。必填：`--url-hash`；可选：`--output`（须在当前工作目录下）；`GET /api/v1/market/data/index/index_description/{url_hash}`。**须先用 `index-description-paginated` 取得 `url_hash`**。
- **`index-weight-summary`**（权重链 ①）：分页查询指数权重汇总（按 `index_code` 列出各期 `date` 与 `url_hash`）。可选：`--index-code`、`--page`、`--page-size`（默认 20，最大 100）；`GET /api/v1/market/data/index/index_weight_summary`。
- **`index-weight-list`**（权重链 ②）：分页查询指数成份权重明细。必填：`--index-code`；可选：`--date`（YYYYMMDD）、`--page`、`--page-size`（默认 20，最大 100）；`GET /api/v1/market/data/index/index_weight`。可先通过 `index-weight-summary` 确认期数与日期。
- **`index-weight-download`**（权重链 ③）：按 `url_hash` 下载指数权重 xlsx。必填：`--url-hash`；可选：`--output`（须在当前工作目录下）；`GET /api/v1/market/data/index/index_weight/{url_hash}`。**须先用 `index-weight-list` 或 `index-weight-summary` 取得 `url_hash`**。
- **`index-detail`**：查询单只指数详情（名称、行情点位、成交、涨跌幅、多周期涨跌幅等）。必填：`--index`；可选 `--masks`。若用户仅给名称，先通过 `index-description-all` 或 `index-list-paginated` 确认代码再查。
- **`index-list-paginated`**：指数分页列表，支持分页、排序、筛选。可选：`--order_by`/`--ob`、`--filter`、`--masks`、`--page_size`、`--page_no`。
- **`index-ohlcs`**：查询单只指数 OHLC K 线（开高低收、成交量、成交额，daec 日期区间）。必填：`--index`、`--since`（YYYYMMDD）；可选 `--until`（YYYYMMDD，默认今天）、`--interval`（Day/Week/Month，默认 Day）、`--adjust`（Forward/Backward）。无年线、无 MA。建议先完成名称到代码映射后再调用。
- **`index-prices`**：查询单只指数分钟级分时价格。必填：`--index`；时间范围二选一：`--since`（TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(n)）或 `--since_ts_ms`。建议先完成名称到代码映射后再调用。

---

## 典型调用流程

### 指数描述链（查简介 → 下载 PDF）

```
index-description-paginated  ──取 url_hash──▸  index-description-download
```

1. `index-description-paginated --page 1 --page-size 20` → 获取 `url_hash`
2. `index-description-download --url-hash <上一步的 url_hash> --output ./desc.pdf`

### 指数权重链（查期数 → 查明细 → 下载 xlsx）

```
index-weight-summary  ──取 index_code/date/url_hash──▸  index-weight-list  ──取 url_hash──▸  index-weight-download
```

1. `index-weight-summary --index-code 000300 --page 1 --page-size 20` → 获取 `index_code` + 各期 `date` 与 `url_hash`
2. `index-weight-list --index-code 000300 --page 1 --page-size 20` → 获取成份明细，每条含 `url_hash`
3. `index-weight-download --url-hash <上一步的 url_hash> --output ./weights.xlsx`

> `index-weight-download` 的 `url_hash` 也可直接从 `index-weight-summary` 的 `periods[].url_hash` 取得，跳过第 2 步。

### 名称→代码映射（重要）

用户经常给出中文名称（如"沪深300""上证指数"）而非代码。**描述分页、权重列表等接口只接受代码参数**时，需先完成映射。

| 目标 skill | 需要的代码格式 | 推荐映射源 | 映射源返回的字段 |
|---|---|---|---|
| `index-weight-list` | 纯 6 位代码（`000300`） | `index-description-paginated` | `index_code` + `index_name` |
| `index-detail` / `index-ohlcs` / `index-prices` | 带交易所后缀（`000300.XSHG`） | `index-description-all` | `symbol` + `name` / `full_name` |

**映射步骤**（以"查沪深300成份权重"为例）：先 `index-description-paginated --page 1 --page-size 100` 按 `index_name` 匹配 → 取 `index_code` → 再 `index-weight-list --index-code <code>`。

> 若 `index-description-all` 已有结果，也可从 `symbol` 截取前 6 位（去掉 `.XSHG` / `.XSHE` / `.BJSE`）作为 `index_code`。

### 通用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「询问方式与子 skill 对应表」或「能力总览」匹配子 skill 名称。
3. **若用户给的是指数名称/简称**：按上方「名称→代码映射」表格选择合适的映射源，先获取代码，再调用目标 skill。若候选代码不唯一，让用户确认后再继续。
4. （可选）读取 `sub-skills/<子skill名>/SKILL.md` 了解接口与参数。
5. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出。
6. **解析并输出**：以表格或要点形式展示给用户。

# FT AI A 股 K 线数据 Skills

本 skill 是 `FTShare-kline-data` 的**统一路由入口**。

根据用户问题，从下方「能力总览」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> `market.ft.tech` 接口默认使用内置基础地址，使用 HTTP GET，并携带请求头 `X-Client-Name: ft-claw`，接口路径统一从 `/api/v1` 开始；可通过 `FTSHARE_BASE_URL` 覆盖。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>`。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> stock-ohlcs --symbol 688295.XSHG --since 20240101 --until 20240131
python <RUN_PY> stock-ohlcs --symbol 000001.SZ --since 20240101 --until 20260628 --interval Week
python <RUN_PY> stock-ohlcs --symbol 600000.XSHG --compat v2 --span DAY1 --limit 5
python <RUN_PY> stock-prices --stock 000001.XSHG --since TODAY
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 能力总览

### 1. 单只股票 OHLC K 线

- **`stock-ohlcs`**：查询单只 A 股标的 K 线（daec）。推荐必填：`--symbol`；旧 `--stock` 仍兼容。原始模式需 `--since`（YYYYMMDD），可选 `--until`、`--interval`（Minute/Day/Week/Month）、`--adjust`；`--compat v2` 模式可用 `--span`（DAY1/WEEK1/MONTH1）、`--limit`、`--until_ts_ms`，并返回 MA/prev_close 兼容字段。

### 2. 单只股票分时价格（一分钟级别）

- **`stock-prices`**：查询单只 A 股股票在指定时间范围内的分时数据（一分钟一根），用于分时图、当日/多日走势；含该分钟价格、成交量、成交额、均价、时间戳。必填参数：`--stock`；时间起点二选一：`--since`（TODAY / FIVE_DAYS_AGO / TRADE_DAYS_AGO(n)）或 `--since_ts_ms`（毫秒时间戳）。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「能力总览」匹配对应子 skill 名称。
3. （可选）读取 `<RUN_PY>` 同级目录 `sub-skills/<子skill名>/SKILL.md` 了解接口详情与参数。
4. **执行**：`python <RUN_PY> <子skill名> [参数...]`，获取 JSON 输出。
5. **解析并输出**：以表格或要点形式展示给用户。

---

## 子 skill 与用户问法示例

| 用户问法示例 | 子 skill 名 |
|---|---|
| 「688295.XSHG 某日期区间的日线」 | `stock-ohlcs` |
| 「查看某只股票的历史 K 线数据」 | `stock-ohlcs` |
| 「某股票的开盘价、最高价、最低价、收盘价」 | `stock-ohlcs` |
| 「某股票的周线 K 线」 | `stock-ohlcs` |
| 「某股票的月线走势」 | `stock-ohlcs` |
| 「某股票最近成交量和成交额是多少？」 | `stock-ohlcs` |
| 「某股票前复权/后复权的 K 线」 | `stock-ohlcs` |
| 「查询某股票截止某日期前的 K 线（--until YYYYMMDD）」 | `stock-ohlcs` |
| 「某股票今天/当日分时」 | `stock-prices` |
| 「某股票分钟级分时、分时图数据」 | `stock-prices` |
| 「某股票从五日前起的分时」 | `stock-prices` |
| 「某股票从 N 个交易日前起的走势」 | `stock-prices` |

# FT 宏观经济数据 Skills（中国 + 美国）

本 skill 是 `FTShare-macro-economy-data` 的**统一路由入口**，覆盖**中国经济**与**美国经济**指标。

根据用户问题，从下方「能力总览」或「提示词表」匹配对应子 skill，然后通过 `run.py` 执行并解析响应。

> `market.ft.tech` 接口默认使用内置基础地址，接口路径统一从 `/api/v1` 开始；可通过 `FTSHARE_BASE_URL` 覆盖。

---

## 调用方式（唯一规则）

`run.py` 与本文件（`SKILL.md`）位于同一目录。执行时：

1. 取本文件的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>`。
2. **中国经济**（15 项）：`python <RUN_PY> <子skill名>`（无额外参数）。
3. **美国经济**（1 项，按 type）：`python <RUN_PY> economic-us-economic-by-type --type <type值>`。

```bash
# 示例（<RUN_PY> 为实际绝对路径）
python <RUN_PY> economic-china-gdp-quarterly
python <RUN_PY> economic-china-pmi-monthly
python <RUN_PY> economic-china-cpi-monthly
python <RUN_PY> economic-us-economic-by-type --type nonfarm-payroll
python <RUN_PY> economic-us-economic-by-type --type cpi-mom
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

---

## 能力总览与提示词表

**匹配提示**：用户问「中国/我国 + 某经济指标」或「美国 + 某经济指标」时，先区分国别，再按下表匹配子 skill（中国 15 项无参；美国 1 项需带 `--type`）。

### 中国经济 — 提示词与子 skill 对应表

| 提示词（用户常说的词） | 子 skill |
|------------------------|----------|
| **GDP**、国内生产总值、三次产业 | `economic-china-gdp-quarterly` |
| 财政收入、财政月度 | `economic-china-fiscal-revenue-monthly` |
| **LPR**、贷款市场报价利率、房贷利率、1年期/5年期 | `economic-china-lpr-monthly` |
| **PMI**、采购经理人指数、制造业/非制造业PMI | `economic-china-pmi-monthly` |
| **PPI**、工业品出厂价格指数、生产者价格指数 | `economic-china-ppi-monthly` |
| 信贷、**新增信贷**、新增人民币贷款、贷款增量 | `economic-china-credit-loans-monthly` |
| 外汇储备、黄金储备、**外储** | `economic-china-forex-gold-monthly` |
| 社会消费品零售总额、**社零**、零售总额、消费零售 | `economic-china-retail-sales-monthly` |
| 全国税收收入、税收收入、税收月度 | `economic-china-tax-revenue-monthly` |
| **CPI**、居民消费价格指数、消费价格指数、城市/农村CPI | `economic-china-cpi-monthly` |
| **M0、M1、M2**、货币供应量、广义货币、狭义货币 | `economic-china-money-supply-monthly` |
| 海关进出口、**进出口、外贸**、出口、进口 | `economic-china-customs-trade-monthly` |
| 工业增加值、工业增长 | `economic-china-industrial-added-value-monthly` |
| 存款准备金率、**存准率、RRR**、准备金率 | `economic-china-reserve-ratio-monthly` |
| 城镇固定资产投资、**固投**、固定资产投资 | `economic-china-fixed-asset-investment-monthly` |

### 美国经济 — 提示词与 type 对应表

子 skill 固定为 `economic-us-economic-by-type`，执行：`python <RUN_PY> economic-us-economic-by-type --type <type值>`。

| 提示词（用户常说的词） | type 值 |
|------------------------|---------|
| 美国 **ISM 制造业**、美国制造业PMI | `ism-manufacturing` |
| 美国 **ISM 非制造业**、美国服务业PMI | `ism-non-manufacturing` |
| 美国**非农**、非农就业、非农人数 | `nonfarm-payroll` |
| 美国**贸易帐**、贸易赤字/盈余 | `trade-balance` |
| 美国**失业率** | `unemployment-rate` |
| 美国 **PPI**、生产者物价月率 | `ppi-mom` |
| 美国 **CPI 月率**、消费者物价月率 | `cpi-mom` |
| 美国 **CPI 年率**、消费者物价年率 | `cpi-yoy` |
| 美国**核心 CPI 月率** | `core-cpi-mom` |
| 美国**核心 CPI 年率** | `core-cpi-yoy` |
| 美国**新屋开工** | `housing-starts` |
| 美国**成屋销售** | `existing-home-sales` |
| 美国**耐用品订单**、耐用品订单月率 | `durable-goods-orders-mom` |
| 美国**咨商会信心指数**、消费者信心 | `cb-consumer-confidence` |
| 美国 **GDP 年率**、GDP 初值、季度GDP | `gdp-yoy-preliminary` |
| 美国**联邦基金利率**、美联储利率、利率决议上限 | `fed-funds-rate-upper` |

---

## 子 skill 列表（路径说明）

所有子 skill 位于本包 `sub-skills/<子skill名>/`，接口详情见各子 skill 的 `SKILL.md`。

**中国经济（15 项）**

- `economic-china-gdp-quarterly` — 中国 GDP 季度
- `economic-china-fiscal-revenue-monthly` — 中国财政收入月度
- `economic-china-lpr-monthly` — 中国 LPR 月度
- `economic-china-pmi-monthly` — 中国 PMI 月度
- `economic-china-ppi-monthly` — 中国 PPI 月度
- `economic-china-credit-loans-monthly` — 中国信贷月度
- `economic-china-forex-gold-monthly` — 中国外汇与黄金储备月度
- `economic-china-retail-sales-monthly` — 中国社零月度
- `economic-china-tax-revenue-monthly` — 中国税收收入月度
- `economic-china-cpi-monthly` — 中国 CPI 月度
- `economic-china-money-supply-monthly` — 中国货币供应量 M0/M1/M2 月度
- `economic-china-customs-trade-monthly` — 中国海关进出口月度
- `economic-china-industrial-added-value-monthly` — 中国工业增加值月度
- `economic-china-reserve-ratio-monthly` — 中国存款准备金率月度
- `economic-china-fixed-asset-investment-monthly` — 中国城镇固定资产投资月度

**美国经济（1 项，按 type 区分 16 类）**

- `economic-us-economic-by-type` — 美国经济指标统一接口，必填 `--type`（见上表 type 值）。

---

## 使用流程

1. **记录本文件绝对路径**，将 `/SKILL.md` 替换为 `/run.py` 得到 `<RUN_PY>`。
2. **理解用户意图**，从「中国经济 — 提示词与子 skill 对应表」或「美国经济 — 提示词与 type 对应表」匹配子 skill 及（美国）`--type`。
3. （可选）读取 `sub-skills/<子skill名>/SKILL.md` 了解接口与参数。
4. **执行**：中国 `python <RUN_PY> <子skill名>`；美国 `python <RUN_PY> economic-us-economic-by-type --type <type值>`。
5. **解析并输出**：以表格或要点形式展示给用户。
