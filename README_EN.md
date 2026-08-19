# FTShare Skills

[中文](README.md) | [English](README_EN.md)

![Python 3](https://img.shields.io/badge/python-3.x-blue)
![Status](https://img.shields.io/badge/status-early_stage-orange)

`FTShare-skills` is an Agent Skills repository in the FTShare open-source ecosystem. It is designed to organize financial data Skills and investment research workflow Skills.

This repository targets Agent runtimes such as Claude Code, Codex, and OpenClaw. Its goal is to package FTShare financial data capabilities and research workflows into Skills that Agents can understand, call, and reuse, helping Agents move from "calling data" toward "completing research tasks".

For international developers, this repository can be understood as **FTShare Agent Skills for financial data, market data, and investment research workflows**, serving AI finance agents, MCP tools, and automated research scenarios.

## Repository Positioning

`FTShare-skills` is not a single data-interface repository, and it is not the Python SDK.

It carries two categories of capabilities:

1. **Data-level Skills**  
   Wrap FTShare market data, financial data, macro data, index data, ETF data, fund data, Hong Kong and US stock data, news, and related interfaces so that Agents can retrieve structured financial data reliably.

2. **Business-level Skills**  
   Organize data capabilities into investment research workflows such as stock analysis, financial statement interpretation, industry analysis, post-market review, and portfolio analysis, so that Agents can do more than just "fetch data".

The currently available data-level Skill is `FTShare-market-data`. Business-level Skills for real investment research scenarios will be added gradually.

## Repository Contents

```text
FTShare-skills/
  FTShare-market-data/          # Data-level Skill: FTShare financial data interface wrapper
    README.md                   # Installation, usage, parameters, and examples
    SKILL.md
    run.py
    sub-skills/

  business-skills/              # Planned directory for business-level Skills
```

Current notes:

- The root README describes the positioning and structure of the overall Skill repository.
- For installation, usage, parameters, and examples of a specific Skill, read the README in that Skill directory.
- The currently available Skill is `FTShare-market-data`.
- Business-level Skills will be added in future versions.

## Available Skill

### FTShare-market-data

`FTShare-market-data` is the currently available data-level Skill. It allows Agents to call FTShare financial data capabilities.

It covers A-shares, Hong Kong stocks, US stocks, ETFs, funds, indexes, sectors, capital flows, macroeconomic data, financial calendars, news, and related data areas.

For detailed usage, see:

```text
FTShare-market-data/README.md
```

## Planned Business-level Skills

Future directions include:

- Stock analysis Skill
- Financial statement interpretation Skill
- Industry analysis Skill
- Post-market review Skill
- Portfolio analysis Skill
- Event analysis Skill
- Standard research data packages
- Automated report generation workflows for Agents

The goal of business-level Skills is not to expose more raw interfaces, but to organize data, logic, and output structure around real research tasks.

Example:

```text
User: Analyze Kweichow Moutai
    ↓
The business-level Skill decides what data is needed
    ↓
Calls data-level Skills / MCP tools / standard data packages
    ↓
Fetches market data, valuation, financials, shareholders, capital flows, news, and related data
    ↓
Organizes the result into a structured analysis output
```

## Current Stage

This repository is in an early construction stage.

The current focus is to build the data-level Skill, namely `FTShare-market-data`. It provides the underlying data capability for future business-level Skills.

The repository will gradually evolve from "data-level Skills" to "investment research workflow Skills".

## Scope

Please note:

- `FTShare-market-data` is a data-level Skill, not a full research report generator.
- Business-level Skills are still under construction.
- If you need to call data from Python code, use [FTShare-python-sdk](https://github.com/FTShare-Lab/FTShare-python-sdk).
- If you need a standard MCP tool entry point, use [FTShare-MCP](https://github.com/FTShare-Lab/FTShare-MCP).
- This repository focuses on Agent Skills, not traditional Python packages.

## Contributing

Contributions are welcome for new data-level Skills, business-level Skills, documentation improvements, and examples.

Before contributing, read [CONTRIBUTING.md](CONTRIBUTING.md), which covers Skill structure, documentation requirements, submission workflow, and security notes.

## Community

Chinese users are welcome to join the FTShare WeChat community group to discuss Skill usage, data-level Skills, business-level Skills, Agent-based investment research workflows, and contribution directions.

<img src="docs/assets/wechat-group-20260826.png" alt="FTShare WeChat community group" width="320" />

> **Community rules**:
> - Discussions should be related to FTShare, Skill building, financial data interfaces, or Agent research workflows
> - Advertising, promotion, and unrelated off-topic chat are not allowed
> - For bugs, feature requests, and Skill contribution ideas, please open a GitHub Issue first. The group is for quick discussion and follow-up context

**The QR code is valid until August 26, 2026.** If it expires, please open an Issue and the maintainers will update the invitation.

## Related Projects

- [FTShare-python-sdk](https://github.com/FTShare-Lab/FTShare-python-sdk): FTShare financial data Python SDK for developer-facing data access
- [FTShare-MCP](https://github.com/FTShare-Lab/FTShare-MCP): FTShare financial data MCP tool documentation and integration guide for Agent tool calls
- [FTShare-skills](https://github.com/FTShare-Lab/FTShare-skills): FTShare Agent Skills repository for data-level Skills and investment research workflow Skills

## License

This project is released under the MIT License. See [LICENSE](LICENSE).

The MIT License applies to the source code and Skill implementations in this repository. It does not mean FTShare data services are available without restriction. Access quota, permissions, and commercial use of FTShare data interfaces are subject to FTShare data service terms.
