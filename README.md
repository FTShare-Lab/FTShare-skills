# FTShare Skills

[中文](README.md) | [English](README_EN.md)

![Python 3](https://img.shields.io/badge/python-3.x-blue)
![Status](https://img.shields.io/badge/status-early_stage-orange)

`FTShare-skills` 是 FTShare 开源生态中的 Agent Skill 仓库，用于沉淀金融数据 Skill 和投研业务 Skill。

本仓库面向 Claude Code、Codex、OpenClaw 等 Agent 运行时，目标是把 FTShare 的金融数据能力和投研业务流程封装成 Agent 可理解、可调用、可复用的 Skill，让 Agent 能从“调用数据”进一步走向“完成投研任务”。

面向国际开发者，本仓库也可以被理解为 **FTShare Agent Skills for financial data, market data and investment research workflows**，服务于 AI finance agents、MCP tools 和自动化投研场景。

## 仓库定位

`FTShare-skills` 不是单一数据接口仓库，也不是 Python SDK。

它主要承载两类能力：

1. **数据级 Skill**  
   封装 FTShare 行情、财务、宏观、指数、ETF、基金、港美股、新闻等数据接口，让 Agent 能稳定获取结构化金融数据。

2. **业务级 Skill**  
   基于数据能力进一步组织个股分析、财报解读、行业分析、盘后复盘、持仓分析等投研工作流，让 Agent 不只“查数据”，还能“完成任务”。

当前已提供 `FTShare-market-data` 数据级 Skill。后续会逐步补充面向真实投研场景的业务级 Skill。

## 仓库内容

```text
FTShare-skills/
  FTShare-market-data/          # 数据级 Skill：FTShare 金融数据接口封装
    README.md                   # 具体安装、调用、参数、示例请看这里
    SKILL.md
    run.py
    sub-skills/

  business-skills/              # 后续业务级 Skill 规划目录
```

当前说明：

- 根目录 README 只说明整个 Skill 仓库的定位和结构。
- 具体 Skill 的安装、调用、参数和示例，请进入对应子目录查看 README。
- 当前可用的 Skill 是 `FTShare-market-data`。
- 业务级 Skill 会在后续版本中逐步加入。

## 当前可用 Skill

### FTShare-market-data

`FTShare-market-data` 是当前已提供的数据级 Skill，用于让 Agent 调用 FTShare 金融数据能力。

它覆盖 A 股、港股、美股、ETF、基金、指数、板块、资金流、宏观经济、财经日历、新闻等数据方向。

具体使用方式请查看：

```text
FTShare-market-data/README.md
```

## 后续业务级 Skill

后续将逐步建设：

- 个股分析 Skill
- 财报解读 Skill
- 行业分析 Skill
- 盘后复盘 Skill
- 持仓分析 Skill
- 事件分析 Skill
- 标准投研数据包
- 面向 Agent 的自动化报告生成工作流

业务级 Skill 的目标不是继续暴露更多原始接口，而是围绕真实投研任务组织数据、逻辑和输出结构。

例如：

```text
用户：帮我分析一下贵州茅台
    ↓
业务级 Skill 判断需要哪些数据
    ↓
调用数据级 Skill / MCP 工具 / 标准数据包
    ↓
获取行情、估值、财务、股东、资金流、新闻等数据
    ↓
组织成结构化分析结果
```

## 当前阶段

本仓库处于早期建设阶段。

当前重点是先建设数据级 Skill，也就是 `FTShare-market-data`。它为后续业务级 Skill 提供底层数据能力。

后续会逐步从“数据级 Skill”扩展到“投研业务工作流 Skill”。

## 能力边界

需要明确：

- `FTShare-market-data` 是数据级 Skill，不是完整研报生成器。
- 当前业务级 Skill 仍在建设中。
- 如果需要 Python 编程调用数据，应使用 [FTShare-python-sdk](https://github.com/FTShare-Lab/FTShare-python-sdk)。
- 如果需要标准 MCP 工具入口，应使用 [FTShare-MCP](https://github.com/FTShare-Lab/FTShare-MCP)。
- 本仓库重点是 Agent Skill，而不是传统 Python 包。

## Contributing

欢迎提交新的数据级 Skill、业务级 Skill、文档改进和示例。

贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，其中包含 Skill 结构、文档要求、提交流程和安全注意事项。

## 社区交流

欢迎加入 FTShare 社区交流群，一起讨论 Skill 使用、数据级 Skill、业务级 Skill、Agent 投研工作流和项目贡献方向。

<img src="docs/assets/wechat-group-20260715.png" alt="FTShare 微信交流群" width="320" />

> **群规说明**：
> - 仅限 FTShare 项目、Skill 构建、金融数据接口、Agent 投研工作流相关讨论
> - 禁止广告、推广、无关闲聊
> - Bug、功能需求和 Skill 贡献建议，建议优先在 GitHub Issues 中提交，群内用于快速交流和补充说明

**二维码有效期至 2026 年 7 月 15 日。** 如二维码失效，请在 Issues 中留言，维护者会更新入群方式。

## Related Projects

- [FTShare-python-sdk](https://github.com/FTShare-Lab/FTShare-python-sdk)：FTShare 金融数据 Python SDK，面向开发者编程调用
- [FTShare-MCP](https://github.com/FTShare-Lab/FTShare-MCP)：FTShare 金融数据 MCP 工具文档与接入说明，面向 Agent 工具调用
- [FTShare-skills](https://github.com/FTShare-Lab/FTShare-skills)：FTShare Agent Skill 仓库，面向数据级 Skill 与投研业务 Skill

## License

本项目代码采用 MIT License，详见 [LICENSE](LICENSE)。

MIT License 适用于本仓库中的源代码与 Skill 实现，不代表 FTShare 数据服务本身无限制开放。FTShare 数据接口的访问额度、权限和商业用途，以 FTShare 数据服务条款为准。
