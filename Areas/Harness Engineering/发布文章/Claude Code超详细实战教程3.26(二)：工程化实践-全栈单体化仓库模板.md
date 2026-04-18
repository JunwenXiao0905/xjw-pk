
如果你正在为这些问题苦恼：
- Claude 官方订阅每月 $20，国内支付困难，账号稳定性存疑
- 听说 Claude Code 很强，但不知道怎么在国内用起来
- 想要尝试又怕出现安全问题，大模型直接删盘跑路
- 更新迭代太快，又有好多新特性

那这篇文章就是为你准备的。

> 本教程使用 **MiniMax Coding Plan** 作为模型服务，starter套餐<30￥/月
> 开发环境为 **Windows 11 + WSL2 (Ubuntu)**，更安全，更好的体验
> 更新时间：**2026/3/26**，Auto-dream、/btw等特性都有介绍 
> Claude Code版本：**2.1.84**，跟紧版本，别掉队
> 
> 💡 干货过多，建议**收藏后再阅读**，方便随时查阅命令和配置。

## 目录

- [一、Windows 下的开发环境与工具推荐](#一windows-下的开发环境与工具推荐)
- [二、Claude Code 安装与启动](#二claude-code-安装与启动)
- [三、基础使用方法](#三基础使用方法)
- [四、进阶功能](#四进阶)
- [五、OpenSpec](#五openspec)
- [六、Everything-claude-code](#六everything-claude-code)
- [七、常见问题与排错](#七常见问题与排错)

---


# 五、OpenSpec

[GitHub - Fission-AI/OpenSpec: Spec-driven development (SDD) for AI coding assistants.](https://github.com/Fission-AI/OpenSpec)

## 1.是什么？解决什么问题？

**OpenSpec = Spec-driven development (SDD) for AI coding assistants**

AI 编程助手很强大，但有一个痛点：当你和 AI 对齐了设计思路、实现完一个功能后，过两天打开新对话继续下一个功能，之前的所有讨论、决策、设计全部蒸发。你又要从头解释项目背景、技术栈、已有的架构约束。

还有一种情况：功能做到一半被打断了——开会、下班、切去修一个 Bug。回来打开新对话，AI 完全不知道你之前做到哪了。

OpenSpec 倡导的是一种”规格驱动开发”范式：

> **Agree before you build** — 在写任何一行代码之前，先由人类与 AI 共同协商并锁定一份机器可读、人可评审的规格文档。

## 2.安装与初始化

### 前置要求

- Node.js **20.19.0+**

### 安装

```
npm install -g @fission-ai/openspec@latest
```

### 初始化项目

```
cd your-project
openspec init
```

初始化时 CLI 会问你使用哪些 AI 工具（Claude Code、Cursor、Copilot 等），然后自动往对应目录写入 Skill 和斜杠命令文件。完成后项目里多出一个 `openspec/` 目录：

```
  openspec/
  ├── config.yaml                              # OpenSpec 配置文件
  ├── changes/                                  # 变更提案目录
  │   └── archive/                              # 已归档的变更
  │       ├── 2026-03-15-xxxx/    # 运行时可观测性事件变更
  │          ├── proposal.md                   # 变更提案文档
  │          ├── design.md                     # 技术设计文档
  │          ├── tasks.md                      # 任务清单
  │          ├── .openspec.yaml                # 变更元数据配置
  │          └── specs/
  │              └── runtime-observability/
  │                  └── spec.md               # 运行时可观测性规格说明
  └── specs/                                    # 当前生效的规格说明
      ├── auth-flow/
      │   └── spec.md                           # 认证流程规格
      ├── runtime-backed-chat/
      │   └── spec.md                           # 运行时聊天规格
      ├── docker/
      │   └── spec.md                           # Docker部署规格
      ├── chat-session-persistence/
      │   └── spec.md                           # 聊天会话持久化规格
      ├── runtime-observability/
      │   └── spec.md                           # 运行时可观测性规格
      └── environment/
          └── spec.md                           # 环境配置规格
```

OpenSpec 弃用了笨重的开发文档，转而采用一套轻量级的、面向 AI 优化的 Markdown 工件体系。每个变更（Change）都被组织在独立的文件夹中：

  
  

- **proposal.md：**描述变更的初衷（Why）和范围（What）。
- **specs/：**具体的逻辑规格，通常包含 “Scenario（场景）” 描述，通过具体的输入输出消除模糊性。
- **design.md：**技术设计方案，包括本次变更涉及的数据库变更、接口调整等。
- **tasks.md：**原子化的任务清单，作为 AI 的执行路径图。

写入的skill和斜杠命令文件

![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1773475128745-b2184482-3182-4e43-8920-c468ccf4bdeb.png)

### skills/commnd介绍

codex

在输入框中输入/opsx，可以看到/prompts:opsx-* 列表，

![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1773481839158-7269bb27-e7ea-4a61-95d1-6dd21e0df8b8.png)

来源是`~/.codex/prompts/`(这里要画成目录图）

```
  .codex/prompts/
  ├── opsx-apply.md      # 实现 OpenSpec 变更中的任务 - 执行代码实现阶段
  ├── opsx-archive.md    # 归档已完成的变更 - 检查完整性、同步规格、移动到归档目录
  ├── opsx-explore.md    # 探索模式 - 思考想法、调查问题、澄清需求（只读，不实现代码）
  └── opsx-propose.md    # 提议新变更 - 创建变更目录并生成所有工件
```

项目目录下的skills

```
  .codex/skills/
  ├── openspec-propose/
  │   └── SKILL.md               # 一键创建变更提案，生成设计文档、规格和任务清单
  ├── openspec-apply-change/
  │   └── SKILL.md               # 实现 OpenSpec 变更中的任务，开始或继续开发
  ├── openspec-explore/
  │   └── SKILL.md               # 探索模式，深入思考想法、调查问题、澄清需求（只读）
  ├── openspec-archive-change/
      └── SKILL.md               # 归档已完成的变更，在实现完成后进行归档
```

两者之间的关系：

```
  ~/.codex/prompts/
    -> 决定你输入 / 时能看到哪些命令入口
    -> 所以会显示 /prompts:opsx-apply 这类项
```

项目/.codex/skills/

```
    -> 决定 Codex 在这个仓库里有哪些可用技能
    -> 给模型提供具体的工作流和执行规则
    -> 但不会直接以 /opsx 形式出现在命令菜单里
```

claude

在输入框中输入/opsx:，可以看到/opsx: 列表，

![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1774277670507-e3573ec8-40c8-4997-aebd-ee9bbb8a6ac7.png)

```

  ┌───────────────┬────────────────────┬──────────────────────────────────┐
  │     命令      │        作用        │               产出               │
  ├───────────────┼────────────────────┼──────────────────────────────────┤
  │ /opsx:explore │ 探索想法、澄清需求 │ 无固定产出，可能创建 artifacts   │
  ├───────────────┼────────────────────┼──────────────────────────────────┤
  │ /opsx:propose │ 创建变更提案       │ proposal.md, design.md, tasks.md │
  ├───────────────┼────────────────────┼──────────────────────────────────┤
  │ /opsx:apply   │ 实现任务           │ 代码实现 + 更新 tasks.md         │
  ├───────────────┼────────────────────┼──────────────────────────────────┤
  │ /opsx:archive │ 归档完成的变更     │ 更新 specs/ 目录                 │
  └───────────────┴────────────────────┴──────────────────────────────────┘
```

具体存放位置是在：

```
  .claude/commands/
  └── opsx/                       # 子目录名 = 命名空间前缀
      ├── propose.md              # /opsx:propose
      ├── apply.md                # /opsx:apply
      ├── explore.md              # /opsx:explore
      └── archive.md              # /opsx:archive
```

不仅可以使用command，还以直接选择skills:

![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1774277689792-ba553196-b538-49c7-ac8e-7e08d906f691.png)

```
  .claude/skills/
  ├── openspec-propose/
  │   └── SKILL.md                              # 一键创建变更提案，生成设计文档、规格和任务清单
  ├── openspec-apply-change/
  │   └── SKILL.md                              # 实现 OpenSpec 变更中的任务，开始或继续开发
  ├── openspec-explore/
  │   └── SKILL.md                              # 探索模式，深入思考想法、调查问题、澄清需求（只读）
  ├── openspec-archive-change/
      └── SKILL.md                              # 归档已完成的变更，在实现完成后进行归档
```

### OpenSpec CLi

```
  openspec
  ├── init [path]              # 初始化 OpenSpec 到项目
  ├── update [path]            # 更新 OpenSpec 指令文件
  ├── list                     # 列出变更（默认）或规格（--specs）
  ├── view                     # 交互式仪表盘
  ├── change                   # 管理变更提案
  ├── archive [change-name]    # 归档已完成的变更
  ├── spec                     # 管理规格说明
  ├── config                   # 查看和修改配置
  ├── schema                   # 管理工作流 schema（实验性）
  ├── validate [item-name]     # 验证变更和规格
  ├── show [item-name]         # 显示变更或规格详情
  ├── status                   # 显示 artifact 完成状态
  ├── instructions [artifact]  # 输出创建 artifact 的指令
  ├── templates                # 显示模板路径
  ├── schemas                  # 列出可用的 workflow schemas
  ├── new                      # 创建新项目
  ├── feedback <message>       # 提交反馈
  └── completion               # Shell 补全管理
```

在 Skills/Commands 中的被动调用：

```

  ┌──────────────────────────────────────────────────────────┬─────────────────────────────────┬─────────────────────────┐
  │                         CLI 命令                         │            调用位置             │          用途           │
  ├──────────────────────────────────────────────────────────┼─────────────────────────────────┼─────────────────────────┤
  │ openspec new change "<name>"                             │ propose                         │ 创建新变更目录结构      │
  ├──────────────────────────────────────────────────────────┼─────────────────────────────────┼─────────────────────────┤
  │ openspec list --json                                     │ propose, apply, archive,        │ 获取可用变更列表        │
  │                                                          │ explore                         │                         │
  ├──────────────────────────────────────────────────────────┼─────────────────────────────────┼─────────────────────────┤
  │ openspec status --change "<name>" --json                 │ propose, apply, archive         │ 检查 artifact 完成状态  │
  ├──────────────────────────────────────────────────────────┼─────────────────────────────────┼─────────────────────────┤
  │ openspec instructions <artifact> --change "<name>"       │ propose, apply                  │ 获取创建 artifact       │
  │ --json                                                   │                                 │ 的指令                  │
  └──────────────────────────────────────────────────────────┴─────────────────────────────────┴─────────────────────────┘

```

调用流程图：

```
  /opsx:propose <name>
      │
      ├─→ openspec new change "<name>"        # 创建变更目录
      ├─→ openspec status --json              # 检查需要哪些 artifacts
      └─→ openspec instructions proposal --json   # 获取创建 proposal.md 的指令
              ↓
          openspec instructions design --json      # 获取创建 design.md 的指令
              ↓
          openspec instructions tasks --json       # 获取创建 tasks.md 的指令

  /opsx:apply <name>
      │
      ├─→ openspec list --json                # 列出可用变更
      ├─→ openspec status --json              # 检查 artifact 状态
      └─→ openspec instructions apply --json  # 获取执行任务的指令

  /opsx:archive <name>
      │
      ├─→ openspec list --json                # 列出可用变更
      └─→ openspec status --json              # 验证所有 artifacts 已完成
```

总结： CLI 是底层引擎，Skills/Commands 是封装层，通过 --json 输出获取结构化数据供 Claude 解析和执行。

```
openspec new change "fix-buffer-analysis-geo-layer"
   创建 opsx 变更提案
```

```
openspec status --change "fix-buffer-analysis-geo-layer" --json
   获取变更状态和工件顺序
```

```
openspec instructions proposal --change "fix-buffer-analysis-geo-layer" --json
   获取 proposal 工件指令
```

```
 openspec instructions design --change "fix-buffer-analysis-geo-layer" --json
   获取 design 工件指令
```

## 3.工作流：提案、应用、归档

**在项目根目录下的**`**openspec/**`**中能真正窥探到其管理方法**

```
openspec/
├── specs/          ← "系统现在是什么样的"
│   ├── auth/
│   ├── payments/
│   └── ...
└── changes/        ← "我们打算改什么"
    ├── add-dark-mode/
    └── fix-login-bug/
```

**Specs（主规格）** 是系统当前行为的权威描述——"源真相"。它回答的是"系统**现在**是怎么运作的"。

**Changes（变更）** 是你正在进行的修改——每个功能、每个 Bug 修复独立一个文件夹，互不干扰。它回答的是"我们**打算怎么改**"。

- **Proposal 阶段：**建立一个独立的变更上下文，让 AI 只关注当前变更。
- **Apply 阶段：**AI 严格按照 tasks.md 执行，避免了盲目扫描全库导致的 Token 浪费。
- **Archive 阶段：**任务完成后，临时变更文档被移入归档，核心规格更新至主规格文件。这保证了 AI 始终在一个 “卫生” 的上下文环境下工作，同时也为项目留下了可追溯的决策链路。

当一个变更完成并归档后，它里面的规格变化会合并进 specs——主规格因此更新，变更则移入归档目录。这样，specs 始终反映系统的"最新真实状态"。

## 4.实际使用场景

完整流程

- 新需求来了：先建 openspec/changes/...

- AI 主要写 proposal.md、design.md、tasks.md、changes/.../specs/...

- 功能完成并确认后：archive

- archive 之后，主 openspec/specs/... 才更新

这个分离设计有一个很大的好处：你可以同时推进多个变更而互不冲突——它们各自在自己的文件夹里工作，不会互相干扰 specs。

例子“用 Vite+ 给现有项目做初始化/接管”

那 OpenSpec 里通常这样走：

1. 如果你还在评估值不值得上、怎么上、风险是什么  
    用 explore
2. 一旦决定要做这个 change  
    用 propose
3. 方案确认后开始落代码  
    用 apply
4. 做完并验收通过  
    用 archive


## 5.进阶能力

# 六、Everything-claude-code

> **Anthropic 黑客马拉松优胜项目**，一套完整的 AI 智能体性能优化系统。

GitHub: https://github.com/affaan-m/everything-claude-code

## 1. 是什么？

Everything Claude Code (ECC) 是针对 Claude Code、Codex 和 Cursor 等工具的 AI 智能体组件性能优化系统。包含技能、直觉、记忆优化、持续学习和安全扫描功能。

## 2. 核心能力

| 特性 | 数量 | 说明 |
|------|------|------|
| **Agents** | 28 个 | planner, architect, tdd-guide, code-reviewer, security-reviewer, build-error-resolver, e2e-runner 等 |
| **Skills** | 125 项 | continuous-learning, tdd-workflow, backend-patterns, frontend-patterns, verification-loop 等 |
| **Commands** | 60 条 | 快捷命令，覆盖各种开发场景 |

**核心能力**：
- 记忆持久化
- 持续学习
- 验证循环
- Token 优化

## 3. 安装方式

**方式一：插件安装（推荐）**

```bash
/plugin marketplace add affaan-m/everything-claude-code
/plugin install everything-claude-code@everything-claude-code
```

**方式二：脚本安装**

```bash
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code

# Linux/macOS
./install.sh typescript

# Windows
.\install.ps1 typescript
```

## 4. 包含的组件

### Agents（智能体）

| Agent | 用途 |
|-------|------|
| planner | 实现规划 |
| architect | 系统设计 |
| tdd-guide | 测试驱动开发 |
| code-reviewer | 代码审查 |
| security-reviewer | 安全分析 |
| build-error-resolver | 构建错误修复 |
| e2e-runner | E2E 测试 |
| refactor-cleaner | 代码清理 |
| doc-updater | 文档更新 |

### Skills（技能）

| Skill | 用途 |
|-------|------|
| continuous-learning | 持续学习 |
| tdd-workflow | TDD 工作流 |
| backend-patterns | 后端模式 |
| frontend-patterns | 前端模式 |
| verification-loop | 验证循环 |
| golang-patterns | Go 语言模式 |
| django-patterns | Django 模式 |
| security-scan | 安全扫描 |
| springboot-patterns | Spring Boot 模式 |

### Hooks（钩子）

| Hook | 触发时机 |
|------|----------|
| memory-persistence | 记忆持久化 |
| strategic-compact | 战略压缩 |
| session-start | 会话开始 |
| session-end | 会话结束 |
| pre-compact | 压缩前 |
| suggest-compact | 建议压缩 |
| evaluate-session | 评估会话 |

## 5. 支持的语言

TypeScript、Python、Go、Java、Rust 等多种语言的开发规则。

---

# 七、常见问题与排错

## 1. 启动问题

### Q: 启动时报错 "Unable to connect to Anthropic services"

**原因**：首次启动时强制要求登录 Anthropic 账户。

**解决方案**：

1. 打开 `~/.claude.json` 文件（Windows: `C:\Users\%USERNAME%\.claude.json`）
2. 设置 `hasCompletedOnboarding` 为 `true`：

```json
{
  "hasCompletedOnboarding": true
}
```

3. 保存后重新启动 Claude Code

### Q: 启动后显示模型不可用

**原因**：配置的模型与当前服务商不匹配。

**解决方案**：

1. 使用 `/status` 检查当前配置
2. 确认 `ANTHROPIC_MODEL` 与服务商支持的模型一致
3. 阿里百炼支持的模型：`qwen3.5-plus`、`qwen3-coder-next` 等

## 2. 配置问题

### Q: 配置后 API Key 不生效

**原因**：配置文件格式错误或路径不对。

**解决方案**：

1. 确认配置文件路径：`~/.claude/settings.json`
2. 检查 JSON 格式是否正确
3. 使用 `/status` 验证配置是否生效

### Q: Skills 安装后不显示

**原因**：Skills 未正确放置或格式错误。

**解决方案**：

1. 确认 Skills 目录：`~/.claude/skills/` 或项目 `.claude/skills/`
2. 每个 Skill 需要包含 `SKILL.md` 文件
3. 重启 Claude Code 使配置生效

## 3. MCP 问题

### Q: MCP 服务器连接失败

**原因**：网络问题或 MCP 服务不可用。

**解决方案**：

1. 检查网络连接
2. 使用 `/mcp` 查看 MCP 状态
3. 部分海外 MCP 可能需要代理

### Q: MCP 工具调用报错

**原因**：权限未授权或 API Key 无效。

**解决方案**：

1. 检查 MCP 配置中的 API Key
2. 使用 `claude mcp list` 查看已安装的 MCP
3. 查看 MCP 官方文档确认配置要求

## 4. 性能问题

### Q: 响应速度很慢

**原因**：模型选择或网络延迟。

**解决方案**：

1. 使用更快的模型：`/model haiku` 或 `/model qwen3.5-plus`
2. 检查网络连接
3. 使用 `/compact` 压缩上下文

### Q: Token 消耗过快

**原因**：上下文过大或频繁重复操作。

**解决方案**：

1. 使用 `/clear` 清除不必要的历史
2. 使用 `/compact` 压缩上下文
3. 将大型任务拆分为多个小任务

## 5. 其他问题

### Q: 如何查看当前会话的 Token 使用量？

**解决方案**：使用 `/cost` 命令查看（部分服务商可能不支持）

### Q: 如何恢复之前中断的对话？

**解决方案**：使用 `claude --resume` 启动历史对话

### Q: 如何切换不同的服务商？

**解决方案**：修改 `~/.claude/settings.json` 中的 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN`

---

# Source

[OpenSpec 完全使用指南：用规格驱动 AI 编码](https://www.notemi.cn/openspec-complete-user-guide--driving-ai-encoding-with-specifications.html)