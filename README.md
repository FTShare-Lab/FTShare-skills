# FTShare Skill

[中文](README.md) | [English](README_EN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

`FTShare Skill` 是 FTShare 面向 AI Agent 提供的金融数据 Skill 接入方式。它把 FTShare 的行情、财务、宏观、指数、ETF、基金、板块与新闻数据封装成 Agent 可以识别和调用的 Skill。

将本仓库中的 `ftshare-market-data` 加载到 Claude Code、Codex、OpenClaw 等 Agent 运行时后，用户可以直接用自然语言提出数据问题。Agent 会根据 `SKILL.md` 选择对应接口，通过统一入口执行请求，并读取结构化 JSON 结果。

## FTShare 的三种接入方式

FTShare 目前提供 SDK、MCP 和 Skill 三种接入方式。三种方式连接同一套 FTShare 金融数据能力，适合不同的使用环境。

| 接入方式 | 适合场景 | 调用方式 | 项目地址 |
|---|---|---|---|
| Python SDK | Python 程序、数据分析、量化研究 | 在代码中调用，返回 pandas `DataFrame` | [FTShare-python-sdk](https://github.com/FTShare-Lab/FTShare-python-sdk) |
| MCP | 支持 MCP 的 AI 客户端与 Agent | 将 FTShare 配置为标准 MCP 工具 | [FTShare-MCP](https://github.com/FTShare-Lab/FTShare-MCP) |
| Skill | Claude Code、Codex、OpenClaw 等 Agent 运行时 | 加载 `SKILL.md`，由 Agent 自动选择并执行 | 本仓库 |

需要在 Python 项目里稳定编程时使用 SDK。需要给 AI 客户端提供标准工具接口时使用 MCP。需要让 Agent 直接理解数据能力并完成自然语言到接口调用的路由时使用 Skill。

## 当前 Skill

本仓库当前提供一个可安装的父 Skill。

```text
ftshare-market-data
```

它包含 164 个金融数据接口子路由，每个路由对应一项 FTShare 数据能力。Agent 运行时只需加载父 Skill，再由父 Skill 根据用户问题选择内部路由。

```text
用户提出金融数据问题
    ↓
Agent 读取 ftshare-market-data/SKILL.md
    ↓
选择对应的子 Skill
    ↓
通过 run.py 调用 FTShare 数据服务
    ↓
读取 JSON 并组织回答
```

## 数据能力

当前 164 个接口子路由覆盖以下方向。

| 数据域 | 代表能力 |
|---|---|
| A 股 | 股票列表、实时行情、分时、K 线、IPO、大宗交易、融资融券、资金流、涨跌停 |
| 财务与公司数据 | 利润表、资产负债表、现金流量表、业绩预告、业绩快报、股东、质押、解禁、重大合同 |
| ETF 与基金 | ETF 行情、成份、PCF、基金净值、收益、持仓、费率、风险等级 |
| 指数与板块 | 指数行情、指数权重、指数说明、东财板块、同花顺板块 |
| 港股与美股 | 行情、K 线、估值、公司资料、财务报表、恒生指数权重 |
| 可转债与期货 | 可转债资料与 K 线、期货行情与持仓排名 |
| 宏观与资讯 | 中国宏观数据、美国经济指标、财经日历、新闻语义搜索 |

完整接口、参数和字段说明见 [ftshare-market-data/README.md](ftshare-market-data/README.md) 与各子 Skill 的 `SKILL.md`。

## 安装

先克隆仓库。

```bash
git clone https://github.com/FTShare-Lab/FTShare-skills.git
cd FTShare-skills
```

将 `ftshare-market-data` 目录放入 Agent 运行时的 Skill 路径。

Claude Code 可以使用项目级或用户级目录。

```text
.claude/skills/ftshare-market-data/
~/.claude/skills/ftshare-market-data/
```

Codex 可以放入用户级 Skill 目录。

```text
~/.codex/skills/ftshare-market-data/
```

其他 Agent 运行时请将完整的 `ftshare-market-data` 目录放入对应 Skill 目录，并确保运行时能够读取其中的 `SKILL.md`、`run.py` 和 `sub-skills/`。

运行时只需要 Python 3.9 或更高版本。子 Skill 使用 Python 标准库，不需要安装 `pandas` 或 `requests`。

## 快速开始

Skill 加载完成后，可以直接向 Agent 提问。

| 用户问题 | Agent 执行的命令 |
|---|---|
| 列出所有 A 股股票 | `python3 <RUN_PY> stock-list-all-stocks` |
| 查询全市场实时行情并按涨跌幅排序 | `python3 <RUN_PY> stock-daec-stocks --board all --page 1 --page_size 5 --order_by "change_rate desc"` |
| 查询浦发银行当日分时 | `python3 <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --range Today` |
| 查询平安银行最近一个月的日 K 线 | `python3 <RUN_PY> stock-ohlcs --symbol 000001.SZ --since 20260501` |
| 查询沪深 300 成份权重 | `python3 <RUN_PY> index-weight-list --index-code 000300` |
| 查询美国最新非农数据 | `python3 <RUN_PY> economic-us-economic-by-type --type nonfarm-payroll` |

`<RUN_PY>` 表示 `ftshare-market-data/run.py` 的绝对路径。

也可以在终端直接调用。

```bash
python3 ftshare-market-data/run.py stock-list-all-stocks
python3 ftshare-market-data/run.py limit-up-pool
python3 ftshare-market-data/run.py semantic-search-news --query 人工智能
python3 ftshare-market-data/run.py company-hk --trade_code 00700.HK
```

不传子 Skill 名称时，`run.py` 会列出当前所有可用路由。

```bash
python3 ftshare-market-data/run.py
```

## 调用规则

`run.py` 是统一调度入口。标准调用格式如下。

```bash
python3 <RUN_PY> <子 Skill 名称> [参数...]
```

每个子 Skill 都有独立的说明文件。

```text
ftshare-market-data/sub-skills/<子 Skill 名称>/SKILL.md
```

说明文件包含适用场景、参数、接口路径、返回结构和调用示例。Agent 应先读取对应说明，再执行命令。

## 返回结果

子 Skill 会向标准输出打印 JSON，Agent 可以直接读取并转换成表格、摘要或后续分析所需的结构。

手工调用时可以配合 `jq` 查看结果。

```bash
python3 ftshare-market-data/run.py stock-list-all-stocks | jq '.items[0:3]'
```

分页接口通常支持单页查询。部分接口也支持 `--all` 自动翻页。

```bash
python3 ftshare-market-data/run.py stock-ipos --page 1 --page_size 20
python3 ftshare-market-data/run.py stock-ipos --all
```

## 名称与代码映射

部分接口只接受证券代码。用户只提供名称时，Agent 应先调用列表或描述接口完成映射。

| 查询目标 | 代码格式 | 推荐映射接口 |
|---|---|---|
| 指数 | `000300` 或 `000300.XSHG` | `index-description-paginated`、`index-description-all` |
| ETF | `510050.XSHG` | `etf-description-all`、`etf-list-paginated` |
| 基金 | 6 位基金代码 | `fund-overview-all-funds-paginated` |
| 可转债 | `110070.SH` | `cb-lists` |
| 港股 | `00700.HK` | `company-hk`、`hk-view` |

## Base URL

`market.ft.tech` 接口默认使用以下基础地址。

```text
https://market.ft.tech/gateway
```

本地或内网服务可以通过 `FTSHARE_BASE_URL` 切换。

```bash
FTSHARE_BASE_URL=http://127.0.0.1:8000/ python3 ftshare-market-data/run.py stock-list-all-stocks
```

少数接口使用其他 FTShare 服务地址，具体情况以对应子 Skill 的说明为准。

## 安全约束

- `run.py` 只允许执行 `sub-skills/` 中存在的 handler，避免通过名称访问其他路径。
- 使用域名校验的 handler 会检查请求协议与主机是否符合当前基础地址。
- 下载类接口会校验输出参数。建议只输出到当前工作目录，不要使用符号链接路径。
- Skill 不应读取或输出用户的密钥、令牌与其他敏感信息。

## 项目结构

```text
FTShare-skills/
  README.md
  README_EN.md
  CONTRIBUTING.md
  SECURITY.md
  ftshare-market-data/
    README.md
    SKILL.md
    run.py
    test_handlers_contract.py
    sub-skills/
      <子 Skill 名称>/
        SKILL.md
        scripts/
          handler.py
```

## 参与贡献

欢迎提交新的金融数据子 Skill、接口适配、测试、文档改进和使用示例。贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

普通问题和功能建议可以通过 GitHub Issue 提交。安全问题请按照 [SECURITY.md](SECURITY.md) 中的方式反馈。

## 社区交流

欢迎加入 FTShare 社区交流群，讨论 Skill 接入、金融数据接口、Agent 使用和项目贡献。

<img src="docs/assets/wechat-group-20260826.png" alt="FTShare 微信交流群" width="320" />

> 群内仅讨论 FTShare、金融数据、Skill 和 Agent 相关内容。Bug 与功能需求建议优先提交 GitHub Issue。

**二维码有效期至 2026 年 8 月 26 日。** 如二维码失效，请在 Issues 中留言。

## License

本项目代码采用 MIT License，详见 [LICENSE](LICENSE)。

MIT License 适用于本仓库中的代码与 Skill 实现。FTShare 数据服务的访问额度、权限和商业用途以对应服务条款为准。
