# 开源 Claude Code 工程级开发插件 Superpowers 完整上手攻略

原创 兔兔AGI 技术极简主义

 _2026年3月10日 11:23_ _江苏_ 445人

在传统软件开发流程中，通常会先编写需求和设计文档，然后再进入编码阶段。但在 AI 编程场景中，很多人直接跳过这些步骤，认为 AI 能够自动化解决所有问题。实际上，AI 同样需要清晰的规范和流程来指导开发。

**Superpowers** 正是为了解决这一问题而出现的。它提供了一套面向 AI 编程的工程化开发流程。通过**子智能体驱动开发**和**技能系统化设计**，将 TDD、代码审查、设计文档等传统工程实践与 AI 智能体能力结合起来，使开发过程更加结构化，也更容易管理。

本文将从设计理念、运行机制和实践案例三个方面介绍 **Superpowers**，并说明如何用它组织 AI 编程工作流。

## 什么是 Superpowers

![图片](https://mmbiz.qpic.cn/mmbiz_png/CBgB44gdva2nrrROLR8UHXpP5PLSwviaOtdJ1CLbKFLibiaOozMXXMib4OibUTy2LOTYZ6gmwuRUNTtVlMlJ4T4qg2JJqojv8W32BPrC8dZ7Zic6I/640?wx_fmt=png&from=appmsg&wxfrom=13&tp=wxpic#imgIndex=0)

**Superpowers** 为 AI 编程智能体（如 **Claude Code**、**Cursor**、**Codex**、**OpenCode**）提供了一套完整的软件开发工作流程。它不是单一技能，而是由 20+ 个可组合 Skills 组成的系统化工作流，覆盖需求梳理、架构设计、测试驱动开发、代码审查和分支管理等开发环节。

它的核心思路，是通过一组可组合的 **Skills** 和**初始指令**，让 AI 智能体在编写代码时自动遵循最佳实践，而不是随意生成代码。

### 架构设计

**Superpowers** 采用分层架构，并以**技能（Skills）**作为核心抽象，实现模块化和可扩展性。整体可以划分为四个层次：

- • **用户层**：平台无关的设计，可以接入不同的 AI 编程智能体
    
- • **框架层**：通过 `Session Hook` 机制在会话中自动注入技能上下文，无需手动激活
    
- • **执行层**：负责子智能体调度，实现任务隔离和并行执行
    
- • **输出层**：所有产出物（设计文档、代码、测试等）统一通过 Git 管理
    

### 技能系统

在 **Superpowers** 中，**技能（Skills）是最核心的抽象单元**。每个技能描述了一类开发任务，并定义了对应的触发条件和执行流程。

技能文件使用 **YAML Frontmatter** + **Markdown** 的轻量级格式：

`---   name: subagent-driven-development   description: "Use when you have a plan.md - Executes tasks via fresh subagents with two-phase review"   ---      # Subagent-Driven Development      ## Overview   每个任务使用全新子代理，避免上下文污染...      ## The Process   1. 读取计划（仅一次）   2. For each task...`

技能系统支持**覆盖机制**，用于在不修改框架代码的情况下扩展或定制技能。

`解析顺序：   1. ~/.claude/skills/ (personal skills) - 优先级最高   2. plugin/skills/ (superpowers skills) - 默认技能库      冲突解决：   - Personal skills 自动覆盖同名的 superpowers skills   - 使用完全限定名（superpowers:skill-name）强制使用特定版本`

这种机制使开发者可以通过**自定义技能目录**覆盖默认实现，从而在保持框架稳定的同时实现灵活扩展。

## 核心创新：Subagent-Driven Development

### 设计理念：全新上下文 + 两阶段审查

在长对话的 AI 编码过程中，一个常见问题是**上下文逐渐膨胀**：随着对话轮次增加，模型需要处理的历史信息越来越多，早期决策也可能持续影响后续输出。

**Subagent-Driven Development** 通过以下创新机制来缓解这一问题：

- • **上下文隔离**：每个子智能体从全新上下文启动，仅接收当前任务描述
    
- • **职责分离**：实现子智能体负责编码，审查子智能体负责质量检查
    
- • **快速重试**：当审查未通过时，直接创建新的子智能体重新实现任务
    
- • **并行执行**：相互独立的任务可以分发给多个子智能体并行处理
    

### 两阶段审查的工程意义

在 **Subagent-Driven Development** 中，代码审查被拆分为两个独立阶段：规范合规（Spec Review）和代码质量（Code Quality Review）。

**第一阶段：规范合规审查（Spec Review）**

`核心问题：这个实现是否满足需求？   审查重点：   - ✅ 是否实现了所有要求的功能点   - ✅ 边界条件是否处理   - ✅ 测试是否覆盖规范要求   - ❌ 不关注代码风格或实现细节`

**第二阶段：代码质量审查（Code Quality Review）**

`核心问题：这个实现是否易读、可维护？   审查重点：   - ✅ 是否遵循项目代码风格   - ✅ 是否存在重复代码（DRY 原则）   - ✅ 命名是否清晰   - ✅ 是否出现过度工程化`

将审查流程拆分为两个阶段，可以避免常见的评审问题，例如：

- • 在讨论代码风格时忽略功能缺陷
    
- • 因实现「看起来不错」而放松对需求完整性的检查
    
- • 审查意见混杂，难以区分优先级
    

### 两种执行模式对比

**Superpowers** 支持两种任务执行模式，选择合适模式对架构设计和开发效率至关重要：

|维度|Subagent-Driven Development|Executing Plans|
|---|---|---|
|会话模型|当前会话内创建子智能体|并行独立会话|
|任务上下文|每个子智能体使用全新上下文|批量执行，共享上下文|
|审查机制|自动两阶段审查循环|人工检查点|
|执行速度|更快（无需人工等待）|较慢（需要人工确认）|
|适用场景|独立、明确的任务|需要中途调整策略的任务|
|失败处理|自动重试（创建新子智能体）|需要人工介入|

**使用建议**：

- • **需求明确 + 测试完整** → Subagent-Driven Development（充分利用自动化流程）
    
- • **探索性开发 + 频繁调整** → Executing Plans（保留人工决策节点）
    

## 完整工作流程

### 标准开发工作流

**Superpowers** 定义了一个完整的软件开发生命周期，每个阶段由特定的技能驱动：

`1. Brainstorming（头脑风暴）      ↓ 通过问答澄清需求      ↓ 分块展示设计方案并等待确认      ↓ 人工确认最终设计      2. Git Worktree（环境隔离）      ↓ 创建独立的 Git 工作树      3. Writing Plans（任务拆解）      ↓ 将任务拆分为 2–5 分钟的小步骤      4. Subagent Development（子智能体开发）      ↓ 每个任务启动独立子智能体      ↓ 两阶段审查：规范合规 + 代码质量      5. TDD（测试驱动开发）      ↓ 按 RED–GREEN–REFACTOR 循环实现      6. Code Review（代码审查）      ↓ 对实现进行最终质量检查      7. Finish Branch（完成）`

这种流程为每个阶段都设置了明确的输出和检查点，使 AI 编程过程更容易控制，也更容易维护。

### 关键阶段深度解析

#### 阶段1：Brainstorming（头脑风暴）

这是 **Superpowers** 工作流中的第一步。与许多鼓励「直接写代码」的 AI 编程工具不同，它要求先完成设计，再进入实现阶段。

在这个阶段，AI 会通过一系列问题逐步澄清需求：

`澄清需求：   AI: "这个认证功能需要支持哪些认证方式？"   User: "用户名密码 + OAuth"   AI: "OAuth 需要支持哪些提供商？"   User: "Google 和 GitHub"   AI: "Token 存储在哪里？过期策略是什么？"   ...      输出物：   - design.md（完整设计文档）   - 分段展示（200–300 字/段，避免 token 过长）   - 提交到 Git 的设计文档（可审查、可追溯）`

**工程上的作用**：

- • 在编码前澄清需求，减少后期返工
    
- • 设计文档作为团队沟通的基础
    
- • 新成员可以通过设计文档快速理解功能
    

#### 阶段2：Git Worktree（环境隔离）

在这个阶段，**Superpowers** 使用 **Git worktree** 来隔离开发环境，而不是依赖传统的分支切换。

`# 传统方式   git checkout main   git checkout -b feature/auth   # 工作区文件变化，IDE 重新索引   # ... 开发中 ...   git checkout main              # 再次触发索引      # Worktree 方式   git worktree add ../auth-worktree -b feature/auth   cd ../auth-worktree   # 主工作区保持不变，可以同时开发多个功能`

**这样做的好处**：

- • 避免频繁 `checkout` 带来的 I/O 和 IDE 重新索引
    
- • 不同功能可以在不同目录中同时开发
    
- • 测试和实验可以在独立环境中运行，不影响主工作区
    

#### 阶段3：Writing Plans（任务拆解）

在 **Subagent-Driven Development** 中，计划文件相当于执行阶段的输入规约。任务拆解的质量会直接影响后续执行效果。

**Superpowers** 建议将任务拆分为非常小的步骤：

`## Task 1: 创建 User 模型和数据库迁移 (2 分钟)   - 定义 User 模型（email, password_hash, created_at）   - 创建数据库迁移文件   - 运行迁移并验证表结构      验证步骤：   - [ ] 数据库中存在 users 表   - [ ] 表包含所有必需字段      ## Task 2: 实现密码哈希工具函数 (3 分钟)   - 使用 bcrypt 实现 hash_password()   - 实现 verify_password()   - 编写单元测试（正确密码、错误密码、空密码）      验证步骤：   - [ ] 测试通过   - [ ] 相同密码生成不同哈希值`

**任务拆解的基本原则**：

- • **任务粒度控制在 2–5 分钟**，更大的任务需要继续拆分
    
- • 每个任务都包含明确的**验证步骤**（可测试）
    
- • 尽量减少任务之间的**依赖关系**，便于并行执行
    

## 快速上手指南

### 快速安装

安装很简单，不需要额外的配置，也没有复杂的依赖。

整个过程在 Claude Code 里完成，只要两步。

#### 步骤一：把插件加入市场

在 Claude Code 的终端中执行：

`/plugin marketplace add obra/superpowers-marketplace`

#### 步骤二：安装插件

`/plugin install superpowers@superpowers-marketplace`

安装完成后，重启 Claude Code，就可以使用了。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 实战教程

下面通过一个简单的示例，演示 **Superpowers** 的完整工作流程。

#### 步骤一：澄清需求

`/superpowers:brainstorm 我想开发一个简单的网页端 Todo 管理应用。`

运行 Claude Code 命令：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

执行后，**Superpowers** 会先进入**需求澄清阶段**，通过连续提问收集必要信息。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

在需求收集完成后，系统通常会给出 2–3 个实现方案供选择。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

确定方案后，开始生成设计文档，并按模块逐步展示详细设计内容。

1、架构概览：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

2、数据模型：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

3、组件结构：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

4、状态管理：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

5、UI 设计

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

6、错误处理

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

#### 步骤二：编写实现计划

设计批准后，自动保存设计文档，然后开始拆解任务并生成实现计划。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

保存计划后，需要选择任务执行方式。

#### 步骤三：执行开发

确认执行模式后，系统会按照实现计划依次执行任务。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

每个任务完成后，会自动触发**两阶段代码审查流程**：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

如果审查未通过，会重新创建子智能体执行任务。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

#### 步骤四：验收成果

当所有任务完成后，项目开发流程结束。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

此时可以启动本地测试服务器，验证应用功能和界面效果。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

#### 步骤五：增加主题切换功能

继续对项目进行迭代，例如增加主题切换功能：

`/superpowers:brainstorm 给 Todo 应用添加主题。`

运行 Claude Code 命令：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

随后重复前面的流程，生成设计文档：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

编写实现计划：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

创建新的 Git 分支并执行开发任务：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

任务完成后，将功能分支合并回主分支：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

然后重新启动测试服务器进行验证。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

## 常用技巧与最佳实践

### 常用技能速查表

|技能名称|功能|使用场景|
|---|---|---|
|`brainstorming`|通过提问逐步澄清需求|需求不明确或需要补充设计时|
|`writing-plans`|将任务拆解为可执行的小步骤|大功能或复杂任务开始前|
|`executing-plans`|按计划执行任务并设置检查点|按既定计划推进开发|
|`test-driven-development`|执行 TDD 的红-绿-重构循环|功能实现阶段|
|`systematic-debugging`|进行结构化的 Bug 根因分析|出现 Bug 或异常行为时|
|`verification-before-completion`|在任务结束前进行验证|功能完成准备提交时|
|`requesting-code-review`|请求代码审查|提交代码或合并前|
|`subagent-driven-development`|使用子代理执行任务|需要并行处理子任务时|
|`using-git-worktrees`|使用 Git worktree 隔离环境|同时开发多个功能时|

### 技能最佳实践

#### 1. 明确触发关键词

**Superpowers** 的技能通过**关键词触发**。了解常见触发词，有助于在合适的场景下调用对应技能。

|技能|触发关键词|
|---|---|
|`test-driven-development`|TDD、测试驱动、先写测试|
|`brainstorming`|需求描述不明确时自动触发|
|`systematic-debugging`|调试、bug、不工作|
|`writing-plans`|制定计划、规划|

#### 2. 需要结构化流程时使用

- • 生产级代码开发 → 使用 `TDD`（测试驱动开发）
    
- • 需求尚不清晰 → 使用 `brainstorming` 澄清需求
    
- • 复杂项目或多步骤任务 → 使用 `writing-plans` 进行任务拆解
    

#### 3. 避免过度流程化

对于快速原型或一次性脚本，没有必要强制使用完整流程。**Superpowers** 更适合**需要长期维护或持续迭代的项目**，而不是短期实验代码。

#### 4. 技能可以组合使用

`用 TDD 方式实现用户认证，完成后帮我做代码审查`

这条指令会同时触发 `test-driven-development` 和 `code-review` 两个技能。

### 常见问题

#### Q1：Claude Code 没有触发任何技能，直接开始写代码

**排查步骤**：

1. 1. 确认插件是否已加载：`/plugin list`
    
2. 2. 检查 `using-superpowers` 技能是否处于激活状态
    
3. 3. 尝试手动触发技能：`“使用 brainstorming 技能来规划这个功能”`
    
4. 4. 如果仍未生效，重启当前会话再试
    

#### Q2：Claude Code 安装 superpowers 报错

**解决方案**：

`# 清除本地缓存   rm -rf ~/.cache/superpowers      # 重新安装插件   /plugin install superpowers@superpowers-marketplace --force`

#### Q3：创建 Git Worktree 失败

**解决方案**：

`# 检查 Git 版本（需要 2.5+）   git --version      # 清理残留的 worktree   git worktree prune      # 手动测试 worktree 是否可用   git worktree add ../test-worktree -b test-branch`

## 写到最后

**Superpowers** 这类工具让 AI 从单纯的代码助手，逐渐变成工程协作的一部分。通过明确的工作流和技能体系，编程任务可以被拆分并按流程执行，从而减少「代码能跑但难维护」的情况。开发者也可以把更多精力放在架构设计、业务逻辑和创新上，而不是反复修补基础实现。

对于关注工程质量的开发者和团队来说，**Superpowers** 提供了一种值得参考的开发模式。它并不是要取代开发者的创造力，而是把重复、机械、容易出错的部分系统化处理，让开发者把精力更多放在真正需要思考和创新的地方。

如果你也想在下一个项目里让 AI 协作开发更高效、更可靠，不妨试试 **Superpowers**。

**Github 地址**：https://github.com/obra/superpowers

![](http://mmbiz.qpic.cn/mmbiz_png/yvIRzTU5zy1fo3Tc1muibsVUlebQTwXRlzyMOibOfnZ2HybBhPPhJg5wEVlBmrxNfLttmFC1DGHjuiblS4VsWFNyA/300?wx_fmt=png&wxfrom=19)

**技术极简主义**

简单就是最美好的技术表现形式

48篇原创内容

公众号

**既然看到这里了，如果觉得有启发，随手点个赞、推荐、转发三连吧，你的支持是我持续分享干货的动力。**

推荐阅读：[开源多平台 AI 智能体上下文驱动开发技能 Conductor 完整上手攻略](https://mp.weixin.qq.com/s?__biz=MjM5NzA1NzMyOQ==&mid=2247486750&idx=1&sn=b4010dc1e43190da9570963d796354d1&scene=21#wechat_redirect)

![](https://mmbiz.qlogo.cn/sz_mmbiz_jpg/DhduwiaBa7lexUGao1401JxV7iawPIl3mY6aicTOLvVbSKKezAElvia3gaJj5GW0QJmHWIUGy424uFPFuYgKfqycLA/0?wx_fmt=jpeg)

兔兔AGI

钟意作者

claude教程 · 目录

上一篇深入理解 Claude Code 的项目记忆机制：Auto-Memory + CLAUDE.md

阅读 1.1万

​

[](javacript:;)

![](https://mmbiz.qpic.cn/mmbiz_png/yvIRzTU5zy1fo3Tc1muibsVUlebQTwXRlzyMOibOfnZ2HybBhPPhJg5wEVlBmrxNfLttmFC1DGHjuiblS4VsWFNyA/300?wx_fmt=png&wxfrom=18)

技术极简主义

关注

202

1905

184

24

![](https://wx.qlogo.cn/mmopen/duc2TvpEgSRKrwicE9icxabloW41Md1WmBUBEibUbgoicG4wQiaIq4VxA3icgwOKGts9laXwJVF6CxRERrnbdmuvkGeCuIIBkT5nf28K25Ikkt9zWACAQeAvN0iaHrHDI3Jje6N/96)

复制搜一搜

复制搜一搜

暂无评论