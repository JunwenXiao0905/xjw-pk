---
theme: custom-1774370739308-uv8slixhn
themeName: "默认主题 (副本)"
title: "OpenSpec：AI 写代码越写越乱？这套开源工作流，正在把 Vibe Coding 拉回正轨"
---

> OpenSpec GitHub 仓库：<https://github.com/Fission-AI/OpenSpec>
> Star：33.5k

# 一、为什么 AI 一开始真香，项目一复杂就开始乱？

很多人第一次用 AI 写代码，都会有一种错觉：

- 写页面，很快
- 补接口，很快
- 修个小 Bug，也很快

于是很容易得出一个结论：

> 以后是不是只要会提需求就行了？

但项目一复杂，这种感觉很快就会消失。你大概率已经遇到过这些情况：

- 新开一个对话，AI 不记得前面为什么这么设计
- 功能做到一半被打断，回来后上下文接不上
- 让它加一个功能，它顺手把别的地方也改了
- 同一个需求，换个会话就写出另一种实现

很多人会把锅甩给模型。

但 OpenSpec 提供的是另一种视角：

> 问题往往不是模型不够聪明，而是需求、边界、设计和任务拆解，没有被稳定沉淀下来。

传统的 Vibe Coding 更像是“想到哪问到哪，写偏了再补提示词”。  
OpenSpec 的思路则是：

> 先把变更定义清楚，再让 AI 执行；先把意图固定下来，再让代码发生。

这就是它真正解决的问题。

## 二、OpenSpec 到底是什么？

如果一句话概括：

> OpenSpec 是一层放在 AI 编码工具之上的规范管理层。

如果再说得更具象一点：

> 它其实就是 `skills` + `commands` + `OpenSpec CLI` 组合出来的一套规范与工作流。

你可以先这样理解：

- `skills`：告诉模型“这类事情该怎么做”
- `commands`：给你一个直接可触发的命令入口
- `OpenSpec CLI`：在底层负责创建变更、检查状态、输出结构化指令

所以它不是一个单独的软件按钮，而是一整套“入口层 + 工作流层 + 底层引擎”的组合。

官方对它的定位很明确：

- 它是一个 **spec-driven development toolkit**
- 它强调 **Brownfield-first**，也就是对已有项目友好
- 它强调 **Tool-agnostic**，也就是不强绑某个单一工具

换句话说，它不是新的 IDE，也不是新的大模型，而是一套让 AI 在复杂项目里别乱跑的方法。

## 三、先装起来：安装和初始化到底怎么做？

### 1. 前置要求

- Node.js `20.19.0+`

### 2. 安装 OpenSpec

```bash
npm install -g @fission-ai/openspec@latest
```

### 3. 在项目里初始化

```bash
cd your-project
openspec init
```

初始化时，OpenSpec 会让你选择要集成的 AI 工具，然后自动把对应的命令入口和说明写进项目环境里。

也就是说，你不用自己手工搭这些目录和提示词骨架，OpenSpec 会先把工作流骨架装好。

初始化完成后，项目里最核心的变化是会出现一个 `openspec/` 目录。

官方文档还建议你补齐 `openspec/project.md`，把技术栈、架构约定和团队规范写进去，作为项目级上下文。

## 四、OpenSpec 真正值钱的，不是“多了几个文件”，而是这套分层

初始化之后，项目里最关键的是这个结构：

```text
openspec/
├── project.md
├── specs/
└── changes/
```

这里最重要的是 `specs/` 和 `changes/`。

| 目录 | 含义 |
| --- | --- |
| `openspec/specs/` | 系统当前已经生效的主规格 |
| `openspec/changes/` | 正在筹备、实现或等待归档的变更 |

你可以把它直接记成：

- `specs/` 是“系统现在是什么样”
- `changes/` 是“我们准备怎么改”

同时，OpenSpec 会围绕几类核心工件工作：

| 工件 | 作用 |
| --- | --- |
| `proposal.md` | 说明为什么要做这次变更 |
| `specs/**/spec.md` | 定义行为、边界和验收标准 |
| `design.md` | 说明工程上准备怎么落地 |
| `tasks.md` | 把工作拆成执行步骤 |
| `.openspec.yaml` | 变更的元数据文件，记录状态、依赖关系、生成配置 |

这套分层的意义很大：

- 避免把当前状态和待变更状态混在一起
- 让多个变更可以并行推进
- 让 AI 读到的是项目里的稳定上下文，而不是聊天记录里的碎片

### `spec.md` 不是随手备注

OpenSpec 的规格文件强调结构化表达。按官方示例，常见片段包括：

| 片段 | 用途 |
| --- | --- |
| `## ADDED Requirements` | 描述这次新增了什么能力 |
| `## MODIFIED Requirements` | 描述对已有能力的调整 |
| `## REMOVED Requirements` | 描述哪些旧行为被废弃 |
| `### Requirement:` | 每条能力约束本体 |
| `#### Scenario:` | 用具体场景把模糊话说清楚 |

这件事很关键，因为 AI 最怕“方向是对的，但边界是糊的”。  
一个 Requirement 如果没有 Scenario，最后往往会变成“看起来有道理，但实现时自由发挥空间很大”的半成品需求。

## 五、标准工作流其实就四步，但这四步比“想到哪写到哪”强太多

最稳的理解方式，是先记住标准主线：

> **提出变更 → 生成 proposal/spec/tasks（必要时补 design） → 审阅并补齐边界 → apply 实现 → 测试验收 → archive 归档**

### 1. Proposal

先把这次变更说清楚。

常见输入示例：

```text
/openspec:propose add-user-filters
```

或者使用 workflow ：

```text
/opsx:propose add-user-filters
```

这一阶段重点不是写代码，而是回答：

- 为什么做
- 做到哪里
- 什么在范围内，什么不做
- 需要新增或修改哪些规格

### 2. Review

这一步最容易被省掉，但也是最容易省出坑的一步。

它往往不是一个独立命令，而是围绕刚生成的 `proposal.md`、`spec.md`、`design.md` 来反复审阅和补充。  
如果你用的是 OPSX 扩展，也可能继续输入：

```text
/opsx:continue add-user-filters
```

重点要审的不是“文档好不好看”，而是：

- 边界有没有漏
- 旧行为会不会受影响
- 命名和拆分是否合理
- AI 有没有把“需求”和“实现方案”混在一起

### 3. Apply

这一步才是让 AI 开始干活。

常见输入示例：

```text
/openspec:apply add-user-filters
```

或者：

```text
/opsx:apply add-user-filters
```

关键区别在于：  
OpenSpec 的 `apply` 是围绕已有规格和任务执行，不是围绕一句模糊需求即兴发挥。

### 4. Archive

这是 OpenSpec 很多人会忽略，但其实非常值钱的一步。

常见输入示例：

```text
/openspec:archive add-user-filters
```

或者：

```text
/opsx:archive add-user-filters
```

归档不是简单把文件挪走，而是在做两件事：

1. 把本次变更沉淀成可追溯历史
2. 把已经确认生效的规格合并进 `openspec/specs/`

## 六、现在官方资料为什么会同时出现 `/openspec:*` 和 `/opsx:*`？在 Codex、Claude 里又是怎么落地的？

这是最近最容易把人看晕的地方。

截至 **2026 年 3 月 24 日**，官方公开资料里确实同时能看到两套入口：

| 来源 | 入口 |
| --- | --- |
| 官网 Getting Started | `/openspec:propose`、`/openspec:apply`、`/openspec:archive` |
| GitHub README 顶部 Quick Start | `/opsx:propose`、`/opsx:apply`、`/opsx:archive` |
| GitHub README Experimental Features | `/opsx:new`、`/opsx:explore`、`/opsx:continue`、`/opsx:ff` 等 |

最稳妥的理解方式是：

- `/openspec:*` 更像官网标准入门主线
- `/opsx:*` 是仓库 README 正在推进的新 workflow 和更细粒度扩展

如果你是第一次接触 OpenSpec，不要一上来被命令名绕进去。
先理解它的目录分层、工件作用和归档机制，再看命令才不容易乱。

### 1. 在 Claude Code 里，`commands` 和 `skills` 是怎么分层的？

在 Claude Code 里，你会看到 `/opsx:propose`、`/opsx:apply` 这类命令。它们对应的通常是：

```text
.claude/commands/
└── opsx/
    ├── propose.md
    ├── apply.md
    ├── explore.md
    └── archive.md
```

同时项目里也会有：

```text
.claude/skills/
├── openspec-propose/
│   └── SKILL.md
├── openspec-apply-change/
│   └── SKILL.md
├── openspec-explore/
│   └── SKILL.md
└── openspec-archive-change/
    └── SKILL.md
```

一句话记住两者关系：

> 命令层负责"你怎么触发"，技能层负责"模型具体怎么执行"。

### 2. OpenSpec CLI 才是底层引擎

如果再往下看一层，真正干活的是 OpenSpec CLI：

```text
openspec
├── init [path]
├── update [path]
├── list
├── view
├── change
├── archive [change-name]
├── spec
├── config
├── schema
├── validate [item-name]
├── show [item-name]
├── status
├── instructions [artifact]
├── templates
├── schemas
├── new
├── feedback <message>
└── completion
```

这里面对大多数人最重要的其实就是这几个：

| CLI 命令 | 作用 |
| --- | --- |
| `openspec init` | 初始化 OpenSpec |
| `openspec update` | 更新工具集成与指令文件 |
| `openspec list` | 查看可用变更或规格 |
| `openspec status` | 查看 artifact 完成状态 |
| `openspec instructions` | 输出创建某类 artifact 的结构化指令 |
| `openspec validate` | 校验规格或变更 |
| `openspec archive` | 归档已完成变更 |

所以这一层最值得记住的总结就是：

> CLI 是底层引擎，Skills/Commands 是封装层；上层命令通过 `--json` 取回结构化数据，再交给模型去执行。

## 七、OPSX 值不值得先行尝试？

值得，但别一上来就把它当默认起点。

OPSX 更适合这些场景：

- 需求还不稳定，想一个 Artifact 一个 Artifact 地推进
- 团队里要先审 proposal，再审 spec，再审 design
- 你想更强地控制模板、依赖关系和生成顺序

其中 `/opsx:explore` 是一个值得单独介绍的入口：它用于进入"探索模式"，在需求还不清晰时深入思考、调查问题、澄清边界。探索模式下 AI 只读不写，帮你理清思路，但不直接生成代码或创建变更。

它的大致思路像这样：

> `/opsx:new` → `/opsx:continue` 或 `/opsx:ff` → `/opsx:apply` → `/opsx:archive`

但如果你现在只是想把 OpenSpec 跑顺，标准主线通常已经够用了。

## 八、一个最直观的例子：为什么它比“直接让 AI 改代码”更稳？

假设你要给后台用户列表增加筛选能力：

- 按角色筛选
- 按团队筛选
- 支持组合筛选
- 刷新后保留筛选条件

普通 Vibe Coding 的做法通常是：

> “帮我给用户列表加个筛选功能，支持角色和团队。”

然后 AI 会开始猜：

- 用什么状态管理
- 过滤条件怎么组织
- URL 是否要持久化
- 接口参数怎么改
- 边界情况如何处理

而 OpenSpec 的做法是先把这件事拆清楚：

> **创建 change → 写 proposal → 补 spec → 补 design → 拆 tasks → apply 实现 → archive**

这样，当 AI 真正开始实现时，它拿到的就不是一句模糊需求，而是一套已经明确边界的执行依据。

## 九、OpenSpec 最值得学的，不是工具，而是习惯

说到底，OpenSpec 真正值钱的地方，不是某个命令，也不是某个截图里长什么样。

它真正改变的是一种协作习惯：

- 从“想到哪问到哪”变成“先对齐再动手”
- 从“上下文在聊天里”变成“上下文在项目里”
- 从“AI 一次次猜我想干什么”变成“AI 围绕明确规格执行”
- 从“会话结束就蒸发”变成“可追溯、可复用、可归档”

这也是为什么我更愿意把它理解为：

> 它不是让 AI 更像天才，而是让 AI 更像一个守流程、懂边界、能接班的工程协作者。

