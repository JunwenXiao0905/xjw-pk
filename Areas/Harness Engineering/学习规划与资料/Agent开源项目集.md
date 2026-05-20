# Agent开源项目集

更新时间：2026-05-20

| 项目                 | 分类                   | 定位                                         | 技术栈         | 是否适合第一深学对象 | 备注                           |
| ------------------ | -------------------- | ------------------------------------------ | ----------- | ---------- | ---------------------------- |
| Hello-Agents       | 教程 / 入门项目            | 系统化 Agent 学习教程                             | Python      | `是`        | 适合先搭最小闭环，偏教学                 |
| OpenHarness        | Harness / 运行时骨架      | 研究 Agent harness 结构的开源实现                   | Python      | `可作为第二站`   | 比完整产品轻，适合看循环、权限、组件组织         |
| DeepAgents         | Harness / 通用外壳       | batteries-included 的 agent harness         | Python      | `否`        | 偏完整，适合看通用运行壳怎么搭              |
| LangGraph          | 编排框架 / runtime       | 有状态、可恢复、可人工介入的 agent orchestration         | Python / JS | `是`        | 适合学状态流转、图编排、长流程              |
| PydanticAI         | 应用框架                 | 强类型、结构化输出、评测和观测友好的 agent framework         | Python      | `是`        | 工程感强，适合做稳一点的项目               |
| Mastra             | 应用框架                 | TS 生态里的现代 Agent / AI app framework         | TypeScript  | `是`        | 适合前后端一体路线                    |
| LlamaIndex         | RAG / Agent 框架       | 偏数据接入、检索、知识工作流                             | Python / TS | `可`        | RAG 生态强，适合知识类项目              |
| OpenHands          | 垂直产品 / Coding Agent  | 面向软件开发场景的 agent 产品                         | Python      | `否`        | 适合看 coding agent 产品形态        |
| OpenClaw           | 产品 / 个人助手平台          | 多渠道、技能化、平台化的 personal AI assistant         | Python      | `否`        | 适合看产品架构，不适合第一站               |
| Hermes Agent       | 产品 / 通用 Agent        | 长期运行、自我成长、技能沉淀型 agent                      | Python      | `否`        | 适合看上限设计，仓库较重                 |
| AutoGen            | 多 Agent 框架           | 经典多 Agent 协作框架                             | Python      | `否`        | 历史影响大，但当前不建议重投入              |
| CrewAI             | 多 Agent 框架           | 偏角色分工、团队协作式多 Agent                         | Python      | `可`        | 容易上手，但抽象较强                   |
| smolagents         | 轻量框架                 | 最小化 agent library，突出 agent loop 和 tool use | Python      | `是`        | 很适合看最小 agent 是怎么跑起来的         |
| open_deep_research | 开源应用 / Deep Research | 用 LangGraph 做的 deep research agent         | Python      | `否`        | 适合看 research agent 应用，不是底层框架 |
| Claude Code 源码思路   | 产品参考                 | coding agent / CLI agent 的产品形态参考           | -           | `否`        | 更适合借鉴架构思路，不是标准开源学习仓库         |

| 方向分类 | 代表项目 | 备注 |
|---|---|---|
| 教程型 | Hello-Agents | 先建立整体认知 |
| 最小骨架型 | smolagents, OpenHarness | 适合照着做 mini harness |
| 通用框架型 | LangGraph, PydanticAI, Mastra, LlamaIndex | 适合真正做项目 |
| 多 Agent 型 | AutoGen, CrewAI | 看协作模式和角色分工 |
| 产品型 | OpenHands, OpenClaw, Hermes Agent | 适合看完整产品长什么样 |
| Deep Research 型 | open_deep_research | 适合看研究代理应用形态 |
