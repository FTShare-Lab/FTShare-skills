# ftshare-market-data

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

`ftshare-market-data` 是非凸科技（FT）金融行情数据的 **Skill 集**——不是 Python SDK，无需 `pip install`，**直接作为 Skill 加载到 Claude Code、Codex、OpenClaw 等 Agent 运行时即可使用**。

它覆盖 A 股 / 港股 / 美股行情、财报、指数、ETF、基金、板块、资金流与宏观经济等数据：运行时读取本目录 `SKILL.md` 的 frontmatter（`name` + `description`）来决定何时触发，再通过统一的 `run.py` 路由入口执行对应子 skill（共 153 个，每个对应一条 FTShare 数据接口），子 skill 向标准输出打印 **JSON**，由运行时直接读取并交给上层投研工作流。

## 在 ftshare 生态中的位置

`ftshare-market-data` 处于 ftshare 生态的 **数据 Skill 层**。它向下连接 FTShare 数据服务（`market.ft.tech`），向上为投研任务、MCP 工具和 Agent 应用提供结构化、可直接调用的行情/财报/宏观数据。

```text
FTShare 数据服务 (market.ft.tech)
    ↓  HTTP GET（Python 标准库 urllib）
ftshare-market-data        # run.py 统一路由 + 122 个子 skill
    ↓
Claude Code / Codex / OpenClaw   # Agent 运行时加载本 Skill
    ↓
用户                       # 自然语言提问 → JSON 结果
```

> 这是一份 **Skill**（给 Agent 运行时消费），不是给人 `import` 的 Python 库。如果你需要在数据分析脚本里编程调用、想要 pandas `DataFrame`，用姊妹项目 [`ftshare-python-sdk`](https://github.com/ftshare-lab/ftshare-python-sdk)——两者覆盖同一批数据接口。

## 作为 Skill 加载

本目录已包含标准 Skill 描述文件 `SKILL.md`（带 `name` / `description` frontmatter），把它作为一个 Skill 放进你的 Agent 运行时即可，无需安装任何包。

**Claude Code**：将本目录放入 skills 路径——项目级 `.claude/skills/ftshare-market-data/`，或用户级 `~/.claude/skills/ftshare-market-data/`。Claude Code 会自动读取 `SKILL.md`，在用户提问匹配到行情 / 财报 / 宏观等数据需求时触发。

**Codex / OpenClaw**：同样将本目录作为一个 Skill 加载，运行时读取 `SKILL.md` 的 frontmatter 完成路由（各家具体加载命令请以对应运行时文档为准）。

获取仓库：

```bash
git clone https://github.com/ftshare-lab/ftshare-skills.git
```

运行时只需要 Python 3：子 skill 仅使用标准库 `urllib`、`json`，**零第三方依赖**，不需要 `pandas`、`requests`。

## 快速开始

加载 Skill 后，**用户用自然语言提问**即可——运行时据 `SKILL.md` 自动匹配子 skill、执行 `run.py`、把返回的 JSON 交回给用户：

| 用户提问（示例） | 运行时执行的命令 |
|---|---|
| 列出所有 A 股股票 | `python <RUN_PY> stock-list-all-stocks` |
| 全市场 A 股实时行情按涨跌幅排序 | `python <RUN_PY> stock-daec-stocks --board all --page 1 --page_size 5 --order_by "change_rate desc"` |
| 创业板实时行情 | `python <RUN_PY> stock-realtime-list --board chi-next --page 1 --page_size 5` |
| 浦发银行当日分时 | `python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --range Today` |
| 5 月有哪些财经事件 | `python <RUN_PY> financial-calendar --start-date 2026-05-01 --end-date 2026-05-31` |
| 平安银行最近一个月的日 K 线 | `python <RUN_PY> stock-ohlcs --symbol 000001.SZ --since 20260501` |
| 沪深300 权重期数 | `python <RUN_PY> index-weight-summary --index-code 000300 --page 1 --page-size 20` |
| 沪深300 成份权重 | `python <RUN_PY> index-weight-list --index-code 000300` |
| 美国最新非农数据 | `python <RUN_PY> economic-us-economic-by-type --type nonfarm-payroll` |

> `<RUN_PY>` 是本目录下 `run.py` 的绝对路径。

例如 `stock-list-all-stocks` 会返回类似 JSON：

```json
{
    "items": [
        { "stock_code": "000001.SZ", "stock_name": "平安银行" },
        { "stock_code": "000002.SZ", "stock_name": "万科A" }
    ]
}
```

## 调用方式（唯一规则）

`run.py` 是统一调度入口，与 `SKILL.md` 同级。执行时：

1. 取 `SKILL.md` 的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>`。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例
python <RUN_PY> stock-list-all-stocks
python <RUN_PY> stock-daec-stocks --board all --page 1 --page_size 5 --order_by "change_rate desc"
python <RUN_PY> stock-realtime-list --board chi-next --page 1 --page_size 5
python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --range Today
python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --compat v2 --since TODAY
python <RUN_PY> stock-ohlcs --symbol 600000.XSHG --compat v2 --span DAY1 --limit 5
python <RUN_PY> stock-ipos --page 1 --page_size 20
python <RUN_PY> stock-ipos --all
python <RUN_PY> semantic-search-news --query 人工智能
python <RUN_PY> etf-pcfs --date 20260309
python <RUN_PY> index-weight-summary --index-code 000300 --page 1 --page-size 20
python <RUN_PY> index-weight-list --index-code 000300 --page 1 --page-size 20
python <RUN_PY> hk-candlesticks --trade-code 00700.HK --interval-unit day --until-date 2026-03-24
python <RUN_PY> economic-china-cpi-monthly
python <RUN_PY> us-income --stock_code NVDA --period 2024 --report_type Q4
```

所有 `market.ft.tech` handler 默认使用 `https://market.ft.tech/gateway`。本地或内网服务可通过环境变量切换 API 地址：

```bash
FTSHARE_BASE_URL=http://127.0.0.1:8000/ python <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --compat v2 --since TODAY
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

## 返回类型

所有子 skill 一律向 **标准输出打印 JSON**，运行时（Agent）会直接读取这份 JSON，再决定如何以表格 / 要点形式展示给用户。

需要手工解析时（如冒烟测试、定时任务）：Shell 中配合 `jq`：

```bash
python run.py stock-list-all-stocks | jq '.items[0:3]'
```

响应中常见的表格数据信封包括：`data.records`、`data.items`、顶层 `items`、顶层数组。各子 skill 的 `SKILL.md` 会标注其具体响应结构与字段含义。

## 分页

分页接口同时支持传统 `--page / --page_size` 和更方便的 `--all` 自动翻页。

取单页：

```bash
python run.py stock-ipos --page 1 --page_size 20
```

自动翻页拉取全量数据：

```bash
python run.py stock-ipos --all
```

`--all` 在多个接口中可用（如 `stock-ipos`、`margin-trading-details`、`eastmoney-us-stock-list`、`eastmoney-stock-valuation`、`stock-capital-flows` 等），无需手工逐页拼接。

## 能力总览

122 个子 skill 按业务域组织（每个子 skill 的接口详情见其 `SKILL.md`）：

| 域 | 代表子 skill |
|---|---|
| **交易日 / 财经日历 / 新闻** | `get-nth-trade-date`、`financial-calendar`、`semantic-search-news` |
| **A 股行情 / 基础** | `stock-list-all-stocks`、`stock-quotes-list`、`stock-daec-stocks`、`stock-realtime-list`、`stock-security-info`、`stock-ipos`、`stock-ohlcs`、`stock-prices`、`stock-intraday-prices`、`block-trades`、`margin-trading-details` |
| **A 股财报 / 业绩** | `stock-income-*`、`stock-balance-*`、`stock-cashflow-*`、`stock-performance-express-*`、`stock-performance-forecast-*` |
| **A 股股东 / 质押 / 增减持** | `stock-holder-ten`、`stock-holder-ften`、`stock-holder-nums`、`pledge-summary`、`pledge-detail`、`stock-share-chg` |
| **A 股公司行动** | `shareholder-meeting`、`stock-unlock-by-stock`、`stock-unlock-by-date`、`major-contract-by-date`、`major-contract-by-symbol`、`major-contract-summary` |
| **A 股估值 / 千股千评 / 热度 / 资金流** | `eastmoney-stock-valuation`、`eastmoney-market-valuation`、`stock-comment-index/score/org-participate/desire/focus`、`stock-rank-xueqiu`、`stock-rank-eastmoney`、`stock-capital-flows` |
| **A 股涨跌停** | `limit-up-pool`、`limit-up-pool-yesterday`、`limit-up-break-pool`、`limit-down-pool` |
| **A 股商誉** | `stock-goodwill-detail`、`stock-goodwill-impairment`、`stock-goodwill-industry`、`stock-goodwill-market-overview`、`stock-goodwill-predict` |
| **可转债** | `cb-lists`、`cb-base-data` |
| **ETF** | `etf-detail`、`etf-description-all`、`etf-list-paginated`、`etf-ohlcs`、`etf-prices`、`etf-component`、`etf-pre-single`、`etf-pcfs`、`etf-pcf-download` |
| **基金** | `fund-basicinfo-single-fund`、`fund-cal-return-...`、`fund-nav-single-fund-paginated`、`fund-overview-all-funds-paginated`、`fund-support-symbols-all-funds-paginated` |
| **指数** | `index-detail`、`index-list-paginated`、`index-ohlcs`、`index-prices`、`index-description-all/paginated/download`、`index-weight-summary/list/download` |
| **板块（东财 / 同花顺）** | `eastmoney-concept-boards`、`eastmoney-board-constituents/daily-ohlc/latest-ohlc`、`10jqk-board-list/kline/all-kline` |
| **港股** | `company-hk`、`hk-view`、`hk-valuatnanalyd`、`hk-candlesticks`、`hk-income/cashflow/balance`、`northbound`、`southbound`、`eastmoney-hk-index-daily-kline`、`hsi-daily-weight` |
| **美股** | `eastmoney-us-stock-list/daily-ohlc/latest-ohlc`、`us-basic`、`us-income/cashflow/balance` |
| **宏观经济（中国 + 美国）** | `economic-china-gdp/cpi/ppi/pmi/lpr/...-monthly`（15 项）、`economic-us-economic-by-type`（16 类，按 `--type`） |

### 名称 → 代码映射

部分接口只接受**代码**而非名称（如 `000300`、`00700.HK`、`510050.XSHG`）。用户给出中文名时，运行时需先用对应列表接口映射到标准代码再查询：

| 目标 skill | 需要的代码格式 | 推荐映射源 |
|---|---|---|
| `index-weight-list` | 纯 6 位（`000300`） | `index-description-paginated` / `index-description-all` |
| `index-detail` / `index-ohlcs` / `index-prices` | 带后缀（`000300.XSHG`） | `index-description-all` |
| `etf-*` | 带后缀（`510050.XSHG`） | `etf-description-all` / `etf-list-paginated` |
| `fund-*` | 6 位基金代码 | `fund-overview-all-funds-paginated` |
| `cb-base-data` | 带后缀（`110070.SH`） | `cb-lists` |

## 查看可用接口

不带参数运行 `run.py` 会打印用法并列出全部可用子 skill：

```bash
python run.py
```

查看某个接口的详细参数、响应结构与字段说明：

```bash
cat sub-skills/stock-list-all-stocks/SKILL.md
```

## Base URL 配置

`market.ft.tech` 接口默认以 `https://market.ft.tech/gateway` 为基础地址，使用 HTTP GET：

```text
/api/v1/market/data/<接口路径>
```

如需切到本地或内网服务，设置 `FTSHARE_BASE_URL`。变量里是否带 `/gateway` 会原样保留：

```bash
FTSHARE_BASE_URL=http://127.0.0.1:8000/ python <RUN_PY> stock-list-all-stocks
FTSHARE_BASE_URL=http://127.0.0.1:8000/gateway/ python <RUN_PY> stock-list-all-stocks
```

少数接口使用不同域名（由对应 handler 内置，无需手工指定）：

- `stock-security-info` 使用 `https://ftai.chat`。
- 其他 `market.ft.tech` 接口均可通过 `FTSHARE_BASE_URL` 切换基础地址。
- 分页列表类接口需在请求头携带 `X-Client-Name: ft-claw`（各 handler 已内置）。

## 安全与约束

- **域名白名单**：使用 `safe_urlopen` 的 handler 会校验请求协议和主机匹配当前基础地址；设置 `FTSHARE_BASE_URL` 后按该地址校验。
- **子 skill 白名单**：`run.py` 仅允许 `sub-skills/<名称>/scripts/handler.py` 形态的子 skill，防止路径遍历。
- **下载落盘限制**：含 `--output` 的下载类接口（如 `index-description-download`、`index-weight-download`、`etf-pcf-download`）仅允许写入**当前工作目录**下的路径。
- **依赖前序接口的参数**：下载类接口的 `url_hash` / `filename` 须先由对应的列表接口取得，勿硬编码。

## 项目结构

```text
ftshare-market-data/
  SKILL.md                # Skill 入口文档：frontmatter（name/description）+ 能力总览 + 调用规则
  run.py                  # 统一调度入口：校验并执行子 skill 的 handler
  README.md               # 本文档
  sub-skills/
    <子skill名>/
      SKILL.md            # 该接口的参数、响应结构、字段说明
      scripts/
        handler.py        # 具体实现：HTTP GET → 打印 JSON
```

## 与 ftshare-python-sdk 的关系

本仓库是 **Skill（命令行驱动，给 Agent 运行时）**；`ftshare-python-sdk` 是 **Python 库（给开发者编程）**。两者覆盖同一批 FTShare 数据接口，按使用形态区分：

| | ftshare-market-data（本仓库） | ftshare-python-sdk |
|---|---|---|
| 形态 | Skill（被运行时加载） | pip 包 |
| 入口 | `python run.py <子skill>` | `ft.market_api().<方法>()` |
| 返回 | 原始 JSON（stdout） | pandas `DataFrame` |
| 消费者 | Claude Code / Codex / OpenClaw | 数据分析脚本 / 量化研究 |
| 依赖 | 仅 Python 标准库 | `pandas`、`requests` |
