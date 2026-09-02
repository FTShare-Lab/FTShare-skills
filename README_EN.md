# FTShare Skill

[中文](README.md) | [English](README_EN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

`FTShare Skill` is FTShare's financial data integration for AI agents. It packages FTShare market data, financial statements, macroeconomic data, indexes, ETFs, funds, sectors, and news as Skills that agents can discover and call.

After loading `ftshare-market-data` into Claude Code, Codex, OpenClaw, or another compatible agent runtime, users can ask data questions in natural language. The agent reads `SKILL.md`, selects the appropriate interface, runs the unified entry point, and consumes the structured JSON result.

## Three ways to connect to FTShare

FTShare provides SDK, MCP, and Skill integrations. All three connect to the same FTShare financial data capabilities and serve different environments.

| Integration | Best for | How it works | Project |
|---|---|---|---|
| Python SDK | Python applications, data analysis, and quantitative research | Called from Python and returns pandas `DataFrame` objects | [FTShare-python-sdk](https://github.com/FTShare-Lab/FTShare-python-sdk) |
| MCP | AI clients and agents that support MCP | Exposes FTShare as standard MCP tools | [FTShare-MCP](https://github.com/FTShare-Lab/FTShare-MCP) |
| Skill | Agent runtimes such as Claude Code, Codex, and OpenClaw | Loads `SKILL.md` so the agent can select and execute an interface | This repository |

Use the SDK for programmatic access in Python projects. Use MCP when an AI client needs a standard tool interface. Use Skill when an agent should understand the available data and route natural-language requests directly to the right interface.

## Available Skill

This repository currently provides one installable parent Skill.

```text
ftshare-market-data
```

It contains 164 internal financial data routes. Each route maps to one FTShare data capability. The runtime loads the parent Skill, which then selects the appropriate internal route for the user's request.

```text
User asks a financial data question
    ↓
Agent reads ftshare-market-data/SKILL.md
    ↓
Agent selects a child Skill
    ↓
run.py calls the FTShare data service
    ↓
Agent reads the JSON result and prepares the response
```

## Data coverage

The 164 internal routes currently cover the following areas.

| Data area | Representative capabilities |
|---|---|
| China A-shares | Security lists, real-time quotes, intraday prices, candlesticks, IPOs, block trades, margin trading, capital flows, limit-up and limit-down pools |
| Financial and company data | Income statements, balance sheets, cash flows, forecasts, express reports, shareholders, pledges, unlocks, and major contracts |
| ETFs and funds | ETF quotes, components, PCF files, fund NAV, returns, portfolios, fees, and risk levels |
| Indexes and sectors | Index quotes, weights, descriptions, Eastmoney sectors, and Tonghuashun sectors |
| Hong Kong and US markets | Quotes, candlesticks, valuation, company profiles, financial statements, and Hang Seng index weights |
| Convertible bonds and futures | Convertible bond profiles and candlesticks, futures quotes, and member position rankings |
| Macro and news | China macro data, US economic indicators, financial calendars, and semantic news search |

See [ftshare-market-data/README.md](ftshare-market-data/README.md) and each child Skill's `SKILL.md` for the complete interface, parameter, and field documentation.

## Installation

Clone the repository.

```bash
git clone https://github.com/FTShare-Lab/FTShare-skills.git
cd FTShare-skills
```

Place the complete `ftshare-market-data` directory in your agent runtime's Skill directory.

Claude Code can load it from a project-level or user-level directory.

```text
.claude/skills/ftshare-market-data/
~/.claude/skills/ftshare-market-data/
```

Codex can load it from the user-level Skill directory.

```text
~/.codex/skills/ftshare-market-data/
```

For other agent runtimes, place the complete directory in the corresponding Skill path and make sure the runtime can read `SKILL.md`, `run.py`, and `sub-skills/`.

Python 3.9 or later is the only runtime requirement. Child Skills use the Python standard library and do not require `pandas` or `requests`.

## Quick start

After loading the Skill, ask the agent a data question in natural language.

| User request | Command selected by the agent |
|---|---|
| List all China A-share securities | `python3 <RUN_PY> stock-list-all-stocks` |
| Rank real-time A-share quotes by price change | `python3 <RUN_PY> stock-daec-stocks --board all --page 1 --page_size 5 --order_by "change_rate desc"` |
| Get today's intraday prices for SPD Bank | `python3 <RUN_PY> stock-intraday-prices --symbol 600000.XSHG --range Today` |
| Get one month of daily candlesticks for Ping An Bank | `python3 <RUN_PY> stock-ohlcs --symbol 000001.SZ --since 20260501` |
| Get CSI 300 constituent weights | `python3 <RUN_PY> index-weight-list --index-code 000300` |
| Get the latest US nonfarm payroll data | `python3 <RUN_PY> economic-us-economic-by-type --type nonfarm-payroll` |

`<RUN_PY>` is the absolute path to `ftshare-market-data/run.py`.

You can also call the Skill directly from a terminal.

```bash
python3 ftshare-market-data/run.py stock-list-all-stocks
python3 ftshare-market-data/run.py limit-up-pool
python3 ftshare-market-data/run.py semantic-search-news --query artificial-intelligence
python3 ftshare-market-data/run.py company-hk --trade_code 00700.HK
```

Run `run.py` without a child Skill name to list every available route.

```bash
python3 ftshare-market-data/run.py
```

## Invocation contract

`run.py` is the unified dispatcher. The standard command format is shown below.

```bash
python3 <RUN_PY> <child-skill-name> [arguments...]
```

Each child Skill has its own documentation file.

```text
ftshare-market-data/sub-skills/<child-skill-name>/SKILL.md
```

The file describes when to use the Skill, its arguments, endpoint, response structure, and examples. An agent should read the matching documentation before running the command.

## Output

Child Skills print JSON to standard output. The agent can turn that result into a table, a summary, or a structure for further analysis.

For manual calls, use `jq` to inspect the result.

```bash
python3 ftshare-market-data/run.py stock-list-all-stocks | jq '.items[0:3]'
```

Paginated interfaces support single-page queries. Some also support `--all` for automatic pagination.

```bash
python3 ftshare-market-data/run.py stock-ipos --page 1 --page_size 20
python3 ftshare-market-data/run.py stock-ipos --all
```

## Name-to-code mapping

Some interfaces accept security codes only. When a user provides a name, the agent should first use a list or description interface to resolve the standard code.

| Target | Code format | Recommended mapping interface |
|---|---|---|
| Index | `000300` or `000300.XSHG` | `index-description-paginated`, `index-description-all` |
| ETF | `510050.XSHG` | `etf-description-all`, `etf-list-paginated` |
| Fund | Six-digit fund code | `fund-overview-all-funds-paginated` |
| Convertible bond | `110070.SH` | `cb-lists` |
| Hong Kong stock | `00700.HK` | `company-hk`, `hk-view` |

## Base URL

Interfaces on `market.ft.tech` use the following base URL by default.

```text
https://market.ft.tech/gateway
```

Set `FTSHARE_BASE_URL` to use a local or internal service.

```bash
FTSHARE_BASE_URL=http://127.0.0.1:8000/ python3 ftshare-market-data/run.py stock-list-all-stocks
```

A small number of interfaces use other FTShare service addresses. Refer to the matching child Skill documentation for details.

## Security constraints

- `run.py` executes only handlers that exist under `sub-skills/`, preventing a name from resolving to another path.
- Handlers with origin validation check that the request scheme and host match the configured base URL.
- Download interfaces validate output arguments. Save files only under the current working directory and avoid symbolic-link paths.
- Skills should not read or expose user keys, tokens, or other sensitive information.

## Repository structure

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
      <child-skill-name>/
        SKILL.md
        scripts/
          handler.py
```

## Contributing

Contributions are welcome for new financial data child Skills, interface adapters, tests, documentation improvements, and examples. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Use GitHub Issues for general questions and feature requests. Report security problems using the process in [SECURITY.md](SECURITY.md).

## Community

Join the FTShare WeChat community group to discuss Skill integration, financial data interfaces, agent usage, and project contributions.

<img src="docs/assets/wechat-group-20260909.png" alt="FTShare WeChat community group" width="320" />

> The group is limited to FTShare, financial data, Skills, and agents. Please submit bugs and feature requests through GitHub Issues first.

**The QR code is valid until September 9, 2026.** If it expires, please open an Issue.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).

The MIT License applies to the code and Skill implementations in this repository. FTShare data-service quotas, permissions, and commercial use remain subject to the applicable service terms.
