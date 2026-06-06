# Agent开源项目集

更新时间：2026-06-06

---

## 一、深入学习（推荐精读）

| 项目           | 定位                                 | 技术栈         | Stars     | 首次 release | Releases | 推荐理由                                       |
| ------------ | ---------------------------------- | ----------- | --------- | ---------- | -------- | ------------------------------------------ |
| LangGraph    | 有状态、可恢复、可人工介入的 agent orchestration | Python / JS | 33,966 ⭐  | 2024-06    | 544      | 生产级 Agent 编排事实标准，Uber/JPMorgan/LinkedIn 在用 |
| Pi           | 极简可扩展 coding agent 框架，仅 4 个内置工具    | TypeScript  | 60,046 ⭐  | 2025-12    | 226      | 激进极简主义，Armin Ronacher 维护，半年 226 releases   |
| Mastra       | TS 生态现代 Agent / AI app framework   | TypeScript  | 24,798 ⭐  | 2025-04    | 94       | 内置 OTel + Eval，框架中立，Gatsby 团队出品            |
| Hermes Agent | 长期运行、自我成长、技能沉淀型 agent              | Python      | 182,120 ⭐ | 2026-03    | 16       | Agent 上限设计参考，Gateway+Plugin 架构             |

---

## 二、项目集总览

### 2.1 教程类

系统化学习 Agent 开发的入门教程和教学项目。

| 项目           | 定位                       | 技术栈    | Stars    | 首次 release | Releases | 备注                     |
| ------------ | ------------------------ | ------ | -------- | ---------- | -------- | ---------------------- |
| Hello-Agents | 从零构建智能体系统教程，Datawhale 出品 | Python | 56,768 ⭐ | 2025-11    | 2        | 16 章 5 大部分，含手写框架 + 面试题 |

### 2.2 Code Agent（代码/开发辅助场景）

专注于软件工程任务的 Agent，以代码生成、调试、部署为核心能力。

| 项目        | 定位                                  | 技术栈        | Stars     | 首次 release | Releases | 备注                              |
| --------- | ----------------------------------- | ---------- | --------- | ---------- | -------- | ------------------------------- |
| ClawCode  | Claude Code 的 Rust 重写，史上最快破 50k 星项目 | Rust       | 193,318 ⭐ | —          | —        | 无 GitHub Releases，9 crates 架构清晰 |
| Codex CLI | OpenAI 官方 coding agent CLI，全开源      | Rust       | 88,898 ⭐  | 2025-04    | 813      | TS→Rust 重写，Skills + MCP 原生支持    |
| Aider     | 终端 AI 结对编程，Git 原生、Architect 双模型模式   | Python     | 45,801 ⭐  | 2023-06    | 93       | 老牌项目，适合看 Git 集成 + 双模型降本         |
| Pi        | 极简可扩展 coding agent 框架，仅 4 个内置工具     | TypeScript | 60,046 ⭐  | 2025-12    | 226      | 激进极简主义，热重载扩展，Armin Ronacher 维护  |
| OpenHands | 面向软件开发场景的 coding agent 产品           | Python     | 75,901 ⭐  | 2024-06    | 102      | 功能完整，适合看产品形态                    |

### 2.3 通用 Agent / Agent 产品

面向通用场景的完整 Agent 产品，强调长期运行、技能沉淀、多渠道路由。

| 项目                 | 定位                                 | 技术栈    | Stars     | 首次 release | Releases | 备注                        |
| ------------------ | ---------------------------------- | ------ | --------- | ---------- | -------- | ------------------------- |
| OpenClaw           | 多渠道、技能化、平台化的 personal AI assistant | Python | 377,026 ⭐ | 2025-11    | 197      | 产品架构参考，不适合第一站             |
| Hermes Agent       | 长期运行、自我成长、技能沉淀型 agent              | Python | 182,120 ⭐ | 2026-03    | 16       | 见"深入学习"章节                 |
| open_deep_research | 用 LangGraph 做的 deep research agent | Python | 11,599 ⭐  | —          | —        | 无 GitHub Releases，适合看应用形态 |

### 2.4 Agent 应用开发框架

构建 Agent 所需的运行时、编排、工具调用等基础设施。

| 项目          | 定位                                   | 技术栈         | Stars     | 首次 release | Releases | 备注                             |
| ----------- | ------------------------------------ | ----------- | --------- | ---------- | -------- | ------------------------------ |
| LangGraph   | 有状态、可恢复、可人工介入的 agent orchestration   | Python / JS | 33,966 ⭐  | 2024-06    | 544      | 见"深入学习"章节                      |
| Mastra      | TS 生态现代 Agent / AI app framework     | TypeScript  | 24,798 ⭐  | 2025-04    | 94       | 见"深入学习"章节                      |
| PydanticAI  | 强类型、结构化输出、评测和观测友好                    | Python      | 17,539 ⭐  | 2024-10    | 267      | 工程感强，适合做稳一点的项目                 |
| smolagents  | 最小化 agent library，突出 loop 和 tool use | Python      | 27,720 ⭐  | 2024-12    | 36       | HuggingFace 出品，适合看最小 agent 怎么跑 |
| LlamaIndex  | 数据接入、检索、知识工作流                        | Python / TS | 49,932 ⭐  | 2023-01    | 431      | 最老牌，RAG 生态强，适合知识类项目            |
| AutoGen     | 经典多 Agent 协作框架，微软出品                  | Python      | 58,714 ⭐  | 2023-09    | 98       | 历史影响大，当前不建议重投入                 |
| CrewAI      | 角色分工、团队协作式多 Agent                    | Python      | 52,887 ⭐  | 2023-11    | 195      | 容易上手，但抽象较强                     |
| DeepAgents  | batteries-included 的 agent harness   | Python      | 23,931 ⭐  | 2025-11    | 167      | LangChain 出品，适合看通用运行壳          |
| OpenHarness | Agent harness 结构开源实现，HKU 出品          | Python       | ~13,000 ⭐ | 2026-04    | 4        | 43+ 工具，20k 行，适合看循环/权限/组件组织     |
| Strands Agents | 模型驱动的 AI Agent SDK，AWS 出品           | Python / TS | 6,004 ⭐   | 2025-07    | 62       | 一等 MCP 支持，Amazon Q Developer 在用，极简启动 |

### 2.5 Agent Memory（记忆系统）

Agent 记忆与上下文管理的专项方案。

| 项目                     | 定位                          | 技术栈        | Stars | 首次 release | Releases | 备注        |
| ---------------------- | --------------------------- | ---------- | ----- | ---------- | -------- | --------- |
| TencentDB Agent Memory | 分层式 Agent 记忆系统，符号化短期 + 分层长期 | TypeScript | —     | 2026-04    | 7        | 见"详细内容"章节 |

---

## 三、详细内容

### 3.1 LangGraph

> **仓库**：[github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) ｜ 33,966 ⭐ ｜ Python / JS

**为什么值得深读**：LangGraph 是当前生产级 Agent 编排的事实标准。StateGraph + checkpointing + interrupt/resume 定义了"有状态 Agent"的范式。Uber、JP Morgan、LinkedIn、Klarna 等在生产环境运行。LangSmith 提供完整的可观测 + Eval 体系。

**核心学习点**：
- **图编排**：节点和边表达 agent 状态流转，支持条件分支和循环
- **Checkpointing**：任意步骤持久化，支持中断恢复和时间旅行
- **Human-in-the-loop**：`interrupt()` / `resume()` 实现人工审批节点
- **子图嵌套**：主图调用子图，recursion_limit 传播与安全

**推荐路线**：`Quick Start → StateGraph → Checkpointing → Interrupt → Streaming → 生产部署`

---

### 3.2 Pi

> **仓库**：[github.com/earendil-works/pi](https://github.com/earendil-works/pi) ｜ 60,046 ⭐ ｜ TypeScript ｜ 226 releases

**为什么值得深读**：Pi 是激进极简主义的代表——整个 coding agent 仅 4 个内置工具（read/write/edit/bash），系统 prompt 极短，依赖模型自身 RL 训练而非冗长指令。Armin Ronacher（Flask 作者）主力维护，半年 226 个 release 迭代极快。TerminalBench 排名第二。

**核心学习点**：
- **极简内核**：4 工具 + 短 prompt，看 agent 最小可行设计
- **热重载扩展**：TypeScript 扩展运行时热加载，Agent 能自行修改扩展
- **模型无关**：会话中途可切换 provider/model，不锁定生态
- **Session 树**：分支对话历史，支持 sub-agent 模式与完整可观测

**推荐路线**：`README → pi-agent-core → pi-coding-agent → pi-ai → pi-tui`

---

### 3.3 Mastra

> **仓库**：[github.com/mastra-ai/mastra](https://github.com/mastra-ai/mastra) ｜ 24,798 ⭐ ｜ TypeScript

**为什么值得深读**：Gatsby 团队出品，TypeScript 生态中最完整的 Agent 框架。内置 OpenTelemetry 可观测、工作流编排、Eval 体系，框架中立（不绑定特定 LLM）。适合前后端一体的 TS 全栈项目

**核心学习点**：
- **内置 OTel**：Agent 可观测开箱即用，trace/span 自动采集
- **Workflow 编排**：步骤级依赖声明与并行执行
- **Eval 体系**：内置评估框架，解决 Agent 质量度量问题
- **框架中立**：可切换 LLM provider，不锁定生态

**推荐路线**：`Quick Start → Agents → Workflows → Observability → Eval`

---

### 3.4 Hermes Agent

> **仓库**：[github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) ｜ 182,120 ⭐ ｜ Python

**为什么值得深读**：目前最能代表"Agent 上限"的开源项目——长期运行、自我改进、技能自动沉淀。Gateway + Plugin 架构提供了记忆系统、技能发现、多 Agent 路由的完整方案。TencentDB Agent Memory 原生支持作为 Hermes 插件运行。

**核心学习点**：
- **Gateway 架构**：agent 能力的插件化注册与路由
- **技能沉淀**：从执行轨迹中自动提炼可复用 Skill
- **长期记忆**：跨会话的身份与知识保持
- **自我进化**：基于反馈的持续改进闭环

**推荐路线**：`README → Architecture → Gateway → Plugins → Memory → Skills`

---

### 3.5 TencentDB Agent Memory

> 腾讯云数据库团队开源。**让 Agent 沉淀经验，让人专注创造。**

**一句话定位**：不是又一个"把对话 Embedding 存进向量库"的平庸方案，而是一个有明确分层设计哲学、可追溯、可调试、经过 Benchmark 验证的 Agent 记忆系统。

**核心架构**：

```
L3 Persona（用户画像）      ← 高层：把握偏好、风格
L2 Scenario（场景块）        ← 中层：同类场景归纳
L1 Atom（结构化事实）        ← 底层：离散的知识单元
L0 Conversation（原始对话）  ← 证据层：完整原文
```

- **纵向**：L0→L3 语义金字塔，每层可沿链路下钻追溯，无不可逆摘要
- **横向**：符号化短期记忆——工具日志卸载到文件系统，上下文仅保留 Mermaid 符号图谱（Token -61%，成功率 +51%）

**技术栈**：TypeScript / Node.js，本地 SQLite + sqlite-vec，支持 TCVDB 云端向量库

**值得深入学习的点**：

| 维度 | 要点 | 说明 |
|------|------|------|
| **分层记忆架构** | L0→L3 金字塔 + 渐进式披露 | 不是扁平向量堆砌，每层有明确语义和召回策略。高层把握方向，底层保留证据 |
| **符号化短期记忆** | Mermaid 画布 + node_id 溯源 | 用拓扑图替代自然语言摘要表示任务状态，既省 Token 又保留关系。适合 GIS Agent 长任务场景 |
| **Prompt Engineering 范本** | `src/core/prompts/` 生产级 Prompt | L1 提取/去重、L2 场景归纳、L3 画像生成的完整 Prompt，工业级 Few-shot + 结构化输出 |
| **混合检索工程实现** | BM25 + 向量 + RRF 融合 | `src/core/store/` 中的完整检索链路代码，不是纸上谈兵 |
| **白盒可调理念** | 中间产物全存为 Markdown | Persona、Scenario、画布均可直接打开检查，调试不走黑盒。与 Skill 的"渐进式披露"一脉相承 |
| **生产就绪对照** | 与 9-Gate 对照 | 可观测 ✅（文件系统白盒）、持久化 ✅（checkpoint+恢复）、成本控制 ✅（Token -61%）。对 ai-webgis-agent 的 Eval 和速率限制缺口有参考价值 |

**推荐阅读路线**：`README → src/core/prompts/ → src/core/record/ → src/core/scene/ → src/core/persona/ → src/core/store/ → src/core/hooks/`

**仓库**：[github.com/TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory)

---

### 3.6 Strands Agents

> **仓库**：[github.com/awslabs/strands-agents](https://github.com/awslabs/strands-agents) ｜ 6,004 ⭐ ｜ Python（TypeScript 预览） ｜ 62 releases ｜ Apache 2.0

**为什么值得关注**：AWS 官方出品的 AI Agent SDK，已内部用于 Amazon Q Developer 等生产场景。模型驱动设计（非图编排），以最少样板代码提供完整的 Agent 循环。一等 MCP 支持，可观测（OpenTelemetry）和安全（Hooks）开箱即用。

**核心学习点**：
- **模型驱动**：声明式模型 + 工具定义，用指令而非代码定义行为，无显式图结构
- **MCP 原生**：对 Model Context Protocol 的集成是一等公民，开箱即用
- **Hooks 安全**：Agent 生命周期的拦截钩子（before/after tool call），实现审批/审计/改写
- **OpenTelemetry**：全链路可观测开箱即用，trace/span 自动采集
- **快速启动**：最少 3 行代码跑通 Agent 循环

**应该关注的点**：
- Python SDK 较成熟，TypeScript 尚在预览阶段
- 模型驱动的上限：没有 LangGraph 的图编排灵活，复杂多步骤流程需要纯代码表达
- 缺少跨请求 Checkpointing：单次会话内状态管理完善，但长周期持久任务需外部编排
- 生态系统较新：从 2025-07 第一个 release，周边工具和社区资源仍在丰富中

**推荐路线**：`Get Started （Notebook） → Agent → Tools → Hooks → MCP → Observability`

**与 Mastra 对比**：

| 维度 | Strands Agents | Mastra |
|------|---------------|--------|
| 出品方 | AWS | Gatsby / 社区 |
| 哲学 | 模型驱动：指令定义行为 | 框架中立：灵活编排 |
| Python | SDK 完善 | 仅 TypeScript |
| MCP | 一等支持 | 通过 adapter |
| 生产背书 | Amazon Q Developer | 社区为主 |
