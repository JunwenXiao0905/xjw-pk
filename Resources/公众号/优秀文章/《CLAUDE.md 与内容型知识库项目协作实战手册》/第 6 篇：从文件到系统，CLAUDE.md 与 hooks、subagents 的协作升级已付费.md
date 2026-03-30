# 第 6 篇：从文件到系统，CLAUDE.md 与 hooks、subagents 的协作升级已付费

原创 阿森 前端达人

 _2026年3月22日 12:46_ _河南_ 听全文


> 📌 本篇核心目标：把前五篇搭建的"规则体系 + 验证机制"升级为"系统级协作"。掌握 hooks 的配置方法和适用场景，理解 subagents 在内容项目中的使用策略，以及如何把三者组合成一个完整的 AI 协作操作系统。

# 你已经走到了哪里

如果你跟着前五篇做下来，你现在拥有了：

- 一份精简的 CLAUDE.md（规则入口）
    
- 6 份 docs/ 专项文档（按需加载的细则库）
    
- 一套 frontmatter 规范和 schema 定义（内容治理的基础）
    
- 三套检查清单（质量兜底）
    

这套体系已经比 90% 的项目强了。但它有一个本质局限：

**所有规则的执行，都依赖 Claude "记住并遵守"。**

Claude 大部分时候会遵守。但正如第 5 篇讲的——它偶尔会遗漏步骤、跳过验证、忘记跑构建命令。

在人类团队中，我们不会把代码质量完全寄托在"开发者记得跑 lint"上——我们用 pre-commit hook 自动执行。我们不会把代码审查完全寄托在"审查者仔细看了每一行"上——我们用 CI pipeline 自动检查。

同样的逻辑适用于 AI 协作：

**规则由 CLAUDE.md 定义，但执行不应该只靠 Claude 的"自觉"。**

这就是 hooks 和 subagents 的作用——把"Claude 应该做的事"变成"系统自动做的事"。

# Hooks：给 Claude Code 装上自动执行的神经系统

## Hooks 是什么

Hooks 是 Claude Code 提供的自动化机制——在 Claude 工作流的特定节点，自动运行你预设的脚本或命令。

你可以把它理解为 Git hooks 的 Claude Code 版本：

`Git hooks：在 commit/push 等节点自动运行脚本   Claude Code hooks：在 Claude 使用工具/完成任务等节点自动运行脚本   `

关键区别在于：hooks 是**确定性的**。

CLAUDE.md 里的规则，Claude 遵守的概率是 70%-95%（取决于规则清晰度和上下文复杂度）。而 hooks 执行的概率是 100%——因为它不是靠 Claude "记住"，而是由系统自动触发。

用原文作者的话说：

> 如果在 CLAUDE.md 里写"不要执行 rm -rf"，Claude 大约 70% 的情况会遵守。如果用 hook 拦截这个命令，遵守率是 100%。

## Hook 的三要素

每个 hook 由三部分组成：

`事件（Event）    → 什么时候触发？   匹配器（Matcher）→ 匹配哪个工具或操作？   动作（Action）   → 触发后执行什么？   `

## Claude Code 支持的核心事件

Claude Code 提供了多个生命周期事件，对内容型项目最有用的是这几个：

`PreToolUse       → Claude 使用某个工具之前触发                      可以拦截操作、拒绝执行      PostToolUse      → Claude 使用完某个工具之后触发                      可以做后置检查、自动格式化      Stop             → Claude 完成回复时触发                      可以做最终验证、发送通知      SubagentStop     → subagent 完成任务时触发                      可以检查 subagent 的工作结果      SessionStart     → 会话开始时触发                      可以加载上下文、初始化环境   `

## 怎么配置 Hooks

Hooks 在 Claude Code 的 settings.json 中配置，或者通过 `/hooks` 命令交互式创建。

配置格式：

`{   "hooks": {       "PostToolUse": [         {           "matcher": "Write",           "hooks": [             {               "type": "command",               "command": "npm run lint"             }           ]         }       ]     }   }   `

这个配置的含义是：每次 Claude 写入文件之后，自动运行 `npm run lint`。

三种 hook 类型：

- **command**：运行 shell 命令（最常用）
    
- **prompt**：发送一段提示词给 Claude 模型做单轮评估
    
- **agent**：启动一个 subagent 做深度检查
    

# 内容型项目最值得配置的 5 个 Hooks

不是所有 hook 都对你的项目有用。以下 5 个是内容型知识库项目中投入产出比最高的。

## Hook 1：写入内容文件后自动校验 frontmatter

**事件**：PostToolUse  
**匹配器**：Write（当 Claude 写入文件时）  
**动作**：如果写入的文件在 `content/` 目录下，运行 frontmatter 校验脚本

`{     "hooks": {       "PostToolUse": [         {           "matcher": "Write",           "hooks": [             {               "type": "command",               "command": "if echo \"$TOOL_INPUT\" | grep -q 'content/'; then npm run content:validate; fi"             }           ]         }       ]     }   }   `

**为什么这个 hook 最值得做**：

第 5 篇讲过，frontmatter 不完整是内容项目最高频的错误。之前靠 Claude "记得跑校验"——现在不需要了，每次它写入 content/ 目录的文件，校验自动运行。

如果校验失败，Claude 会看到错误输出，自动修正问题。

## Hook 2：写入文件后自动 lint

**事件**：PostToolUse  
**匹配器**：Write  
**动作**：运行 lint

`{     "hooks": {       "PostToolUse": [         {           "matcher": "Write",           "hooks": [             {               "type": "command",               "command": "npm run lint --quiet"             }           ]         }       ]     }   }   `

这就是第 2 篇讲的"不要把代码风格规则写进 CLAUDE.md"的落地方案。lint 规则交给 ESLint，执行交给 hook。CLAUDE.md 里完全不需要出现任何代码风格相关的规则。

## Hook 3：拦截危险的 bash 命令

**事件**：PreToolUse  
**匹配器**：Bash  
**动作**：检查 Claude 要执行的命令是否包含危险操作

`{     "hooks": {       "PreToolUse": [         {           "matcher": "Bash",           "hooks": [             {               "type": "command",               "command": "echo \"$TOOL_INPUT\" | python3 scripts/check-dangerous-commands.py"             }           ]         }       ]     }   }   `

你的 `check-dangerous-commands.py` 可以检查：是否包含 `rm -rf`、是否操作 `generated/` 目录（那个不该手动修改的目录）、是否操作生产环境配置文件。

如果脚本返回 exit code 2，Claude Code 会阻止这个命令执行。

## Hook 4：任务完成时自动运行内容构建

**事件**：Stop  
**匹配器**：无（每次 Claude 完成回复时都触发）  
**动作**：检查本次会话是否修改了 content/ 下的文件，如果是，自动运行内容构建

这个 hook 解决的是第 5 篇提到的问题："Claude 改完内容后忘了运行 content:build"。有了这个 hook，构建自动触发，不依赖 Claude 的"记忆"。

## Hook 5：会话开始时加载项目上下文

**事件**：SessionStart  
**匹配器**：无  
**动作**：在会话开始时输出当前 git 状态、最近修改的文件列表、待处理的内容任务

这个 hook 的价值在于：Claude 进入项目后，不只是读 CLAUDE.md，还能立刻看到"项目当前的状态"。比如有哪些文件最近被修改、有没有未完成的构建、git 上有没有未合并的分支。

# CLAUDE.md 和 Hooks 的分工

到这里，一个关键问题浮现出来：

**CLAUDE.md 和 hooks 各自负责什么？会不会重复？**

答案很清晰：

`CLAUDE.md 负责：                    Hooks 负责：   ────────────────                   ────────────────   告诉 Claude 规则是什么               自动执行机械检查   提供项目背景和上下文                  拦截危险操作   定义工作流步骤                       后置校验和格式化   指向专项文档                         构建触发和环境初始化   设定高层级的行为边界                  确定性地执行重复任务   `

一个简单的判断标准：

> **如果一件事需要 Claude "理解"才能做对——写进 CLAUDE.md。**  
> **如果一件事只需要"机械执行"就能做对——交给 hooks。**

比如"新增内容时要先搜索是否已有类似内容"——这需要理解和判断，只能写进 CLAUDE.md 的 Workflow。

但"写入 content/ 下的文件后要跑 frontmatter 校验"——这是纯机械动作，交给 hook 最合适。

**在 CLAUDE.md 中标注 hook 的存在**：

`## Standards      代码必须通过 lint 检查。   PostToolUse hook 会在每次写入文件后自动运行 lint，无需手动检查格式问题。   `

这样 Claude 知道"有 hook 在替我做 lint"，就不会浪费时间自己做格式检查，而是专注在真正需要判断力的工作上。

# Subagents：给复杂任务分配独立的"专项工人"

## Subagents 是什么

Subagent 是 Claude Code 启动的一个独立 Claude 实例。它有自己的上下文窗口，做完任务后把结果返回给主会话。

你可以把它理解为：

`主 Claude 会话 = 项目经理   Subagent     = 被派出去做专项任务的专员      专员做完后写一份报告交给项目经理。   项目经理只看报告，不需要知道专员过程中查了哪些资料。   `

## 为什么需要 Subagents

主要解决两个问题：

**问题一：上下文污染**

当 Claude 在一个长会话中做了很多事——读了 20 个文件、修改了 5 个组件、调试了 3 个 bug——它的上下文窗口已经被大量信息填满。这时候你再让它做一个精细的任务（比如"审查所有内容文件的 frontmatter 一致性"），它的注意力已经被稀释了，容易遗漏。

Subagent 在一个干净的上下文中启动，不受主会话历史的干扰。

**问题二：任务隔离**

有些任务不应该和当前工作流共享上下文。比如安全审查——审查者不应该受到实现者的思路影响。用 subagent 做安全审查，它只看代码和规则，不看你和 Claude 之前讨论的实现细节。

## 在内容型知识库项目中怎么用 Subagents

以下是 4 个最适合用 subagent 处理的任务场景：

**场景 1：内容一致性审查**

让 subagent 扫描所有内容文件，检查：

- frontmatter 字段是否一致
    
- category 是否都在合法清单内
    
- tags 有没有同义词问题
    
- slug 有没有冲突
    
- 有没有内容文件缺少必填字段
    

这个任务涉及读取大量文件并逐一校验，如果在主会话中做，会占用大量上下文空间。用 subagent 做，主会话保持干净，subagent 做完后返回一份"审查报告"。

**场景 2：搜索索引完整性检查**

让 subagent 对比内容文件列表和搜索索引，找出：

- 哪些内容在索引中缺失
    
- 哪些索引条目对应的内容已不存在
    
- draft 内容是否被错误收录
    

**场景 3：代码探索**

当你接手一个不熟悉的代码模块——比如内容解析函数——让 subagent 先去阅读代码、理解逻辑、写一份分析报告。你看完报告后再决定怎么改。

这样做的好处是：探索过程产生的大量代码片段不会塞满你的主会话。你只看结论。

**场景 4：文档更新提案**

当你做了一次较大的结构变更（比如新增了一种内容类型），让 subagent 检查 docs/ 目录下的文档，找出哪些文档需要更新，并给出更新建议。

Subagent 可以读取 docs/content-rules.md、docs/data-schema.md 等文件，对比当前代码的实际结构，生成一份"文档同步建议"。

## Subagent 的使用原则

**原则一：subagent 适合"读多写少"的任务**

审查、分析、检查、报告——这些以"读取和判断"为主的任务最适合 subagent。

对于"大范围修改代码"这类任务，subagent 不如在主会话中做，因为你需要实时看到和控制修改过程。

**原则二：subagent 继承 CLAUDE.md**

Subagent 启动时会读取项目的 CLAUDE.md，所以它对项目的基础认知是有的。你不需要在调用 subagent 时重新解释项目背景。

但 subagent 不会读取你和主 Claude 之前的对话历史——这正是它的优势（干净上下文）。

**原则三：subagent 不能再启动 subagent**

Claude Code 不允许 subagent 嵌套。一个 subagent 完成任务后返回结果，不能中途再派出子 subagent。这是为了避免无限递归。

如果你需要多个 subagent 协作，应该由主会话分别启动它们，而不是让一个 subagent 启动另一个。

## 在 CLAUDE.md 中怎么写 Subagent 相关规则

`## Subagent Guidelines      当任务适合委托给 subagent 时：   - 内容一致性审查：使用 subagent，先读取 docs/content-rules.md   - 搜索索引检查：使用 subagent，先读取 docs/build-process.md   - 代码探索和分析：使用 subagent，先读取 general_index.md   - 文档更新建议：使用 subagent，读取 docs/ 下所有文档并对比当前代码   `

这样 Claude 知道哪些任务适合用 subagent，以及 subagent 应该先读哪些文档。

# 三者组合：AI 协作操作系统

把 CLAUDE.md、hooks、subagents 放在一起看，它们形成了一个三层协作系统：

`┌─────────────────────────────────────────────┐   │          CLAUDE.md + docs/                   │   │                                              │   │  定义规则：项目背景、行为边界、工作流程、       │   │  内容规范、数据结构、验证标准                  │   │                                              │   │  作用：让 Claude "知道该怎么做"               │   └─────────────────────┬───────────────────────┘                         │             ┌───────────┴───────────┐             │                       │             ▼                       ▼   ┌─────────────────┐    ┌──────────────────┐   │     Hooks        │    │   Subagents      │   │                  │    │                  │   │  自动执行：       │    │  专项隔离：       │   │  lint、校验、     │    │  审查、分析、     │   │  拦截、构建触发   │    │  探索、报告      │   │                  │    │                  │   │  作用：让机械     │    │  作用：让复杂     │   │  检查 100% 执行  │    │  任务不污染主     │   │                  │    │  会话上下文       │   └─────────────────┘    └──────────────────┘   `

**CLAUDE.md 是大脑**——它定义规则和方向。

**Hooks 是神经系统**——它自动执行确定性的机械动作。

**Subagents 是专项团队**——它在隔离环境中处理复杂的独立任务。

三者配合的一个完整场景：

`你让 Claude "给知识库新增一种'政策文件'内容类型"      第 1 步：Claude 读 CLAUDE.md，了解项目背景和工作流   第 2 步：Claude 读 docs/content-rules.md 和 docs/data-schema.md   第 3 步：Claude 创建 content/policies/ 目录，新增模板文件   第 4 步：PostToolUse hook 自动触发 frontmatter 校验 ← hooks 介入   第 5 步：Claude 更新类型定义和解析函数   第 6 步：PostToolUse hook 自动触发 lint ← hooks 介入   第 7 步：Claude 更新页面模板   第 8 步：Claude 启动 subagent 检查文档同步 ← subagent 介入            subagent 返回："docs/content-rules.md 需要新增            '政策文件'内容类型说明，docs/data-schema.md 需要            新增 Policy 实体定义"   第 9 步：Claude 根据 subagent 建议更新文档   第 10 步：Claude 按 testing.md Level 3 验证   `

每一步都有合适的机制在工作。Claude 负责需要判断力的步骤，hooks 负责机械检查，subagent 负责文档审查。没有任何一个环节完全依赖 Claude 的"记忆"。

# 长期维护：让这套系统越来越好

搭好了系统，不等于完成了。你需要持续维护它。

## 维护策略一：跟着 PR 更新

把 CLAUDE.md 的维护加入你的 PR checklist：

`PR 检查清单：   - [ ] 代码改动完成   - [ ] 测试通过   - [ ] CLAUDE.md 是否需要更新？   - [ ] docs/ 文档是否需要同步？   `

不是每个 PR 都需要更新 CLAUDE.md。但养成"问一下"的习惯，能防止规则和代码逐渐脱节。

## 维护策略二：用 # 持续补充

工作中发现 Claude 重复犯同一个错误？立刻用 `#` 补一条规则。

但不要让 `#` 堆积太多。每隔两周花 10 分钟整理一次：

- 重复的规则合并
    
- 过时的规则删除
    
- 应该移到 docs/ 的规则迁移
    
- Standards 超过 15 条的话，考虑精简
    

## 维护策略三：定期审查 hooks 配置

hooks 配置好之后很容易被遗忘。每个季度检查一次：

- 所有 hook 还能正常运行吗？
    
- 有没有新的场景适合加 hook？
    
- 有没有 hook 已经不再需要？
    
- hook 执行的脚本有没有过期？
    

## 维护策略四：记录 Claude 的"高频错误模式"

每次 Claude 犯了一个你觉得"它不应该犯"的错误，记下来。

积累一段时间后，分析这些错误的规律：

- 如果是"不知道规则"导致的 → 补充 CLAUDE.md 或 docs/
    
- 如果是"知道但忘了执行"导致的 → 考虑加 hook
    
- 如果是"任务太复杂、上下文太满"导致的 → 考虑用 subagent
    

这个分析过程，其实就是在持续优化你的 AI 协作系统。

# 升级路线图：从现在到未来

最后给你一条清晰的升级路径，不需要一步到位。

## 阶段一：规则体系（你现在应该已经到了这里）

- CLAUDE.md 主文件
    
- 3-6 份 docs/ 文档
    
- 检查清单
    
- 手动验证
    

这个阶段足以应对大多数日常协作。

## 阶段二：半自动化

- 加入 2-3 个核心 hooks（lint、frontmatter 校验、危险命令拦截）
    
- 开始在合适的场景使用 subagent（内容审查、代码探索）
    
- 编写 `content:validate` 自动化校验脚本
    

这个阶段显著减少 Claude 的"遗漏性错误"。

## 阶段三：系统级协作

- hooks 覆盖所有机械检查
    
- subagent 用于所有适合隔离的专项任务
    
- 验证流程大部分自动化
    
- CLAUDE.md 和 docs/ 形成稳定的知识库
    
- 新人（或新 Claude 会话）可以通过这套规则快速进入状态
    

## 阶段四：团队协作与复用

- CLAUDE.md 和 docs/ 提交 Git，团队共享
    
- hooks 配置标准化，所有成员使用相同配置
    
- 跨项目复用规则模板
    
- 建立项目模板仓库，新项目可以快速搭建规则体系
    

## 阶段五：MCP 与更广泛的集成

- 通过 MCP 连接外部服务（数据库、CMS、搜索引擎）
    
- Claude 可以直接查询生产数据验证内容
    
- 内容发布流程端到端自动化
    
- 形成完整的 AI 驱动的内容运营闭环
    

你不需要一次到达阶段五。大多数项目在阶段二就已经能显著提升协作质量了。按自己的节奏来。

# 本篇核心认知回顾

**认知一：规则定义和规则执行是两件事**

CLAUDE.md 负责定义规则，hooks 负责自动执行机械检查。两者互补，不是替代关系。

**认知二：hooks 的核心价值是"确定性"**

CLAUDE.md 里的规则被遵守的概率是 70-95%。hooks 执行的概率是 100%。对于安全规则和机械检查，确定性比概率重要。

**认知三：判断这个标准——需要理解的交给 CLAUDE.md，只需机械执行的交给 hooks**

"先搜索是否有类似内容"需要理解和判断 → CLAUDE.md。"写入文件后跑 lint"只需机械执行 → hooks。

**认知四：subagents 解决"上下文污染"和"任务隔离"**

大量文件扫描、一致性审查、代码探索——这些任务在干净的上下文中做更准确，而且不会污染主会话。

**认知五：三者组合是一个完整的协作操作系统**

CLAUDE.md 是大脑（定义规则），hooks 是神经系统（自动执行），subagents 是专项团队（隔离处理）。

**认知六：不需要一步到位**

从规则体系开始，逐步加入 hooks 和 subagents。每个阶段都有独立的价值。

# 本篇检查清单

- [ ] 我理解 hooks 和 CLAUDE.md 的分工（理解型 vs 机械型）
    
- [ ] 我知道内容型项目最值得配置的 hooks 有哪些
    
- [ ] 我知道 subagents 适合处理什么类型的任务
    
- [ ] 我能画出 CLAUDE.md + hooks + subagents 的三层协作模型
    
- [ ] 我知道从当前阶段到下一阶段该怎么升级
    
- [ ] 我有一个持续维护这套系统的计划
    

# 本篇练习

**练习 1：配置你的第一个 hook**

从最简单的开始——配置一个 PostToolUse hook，让 Claude 每次写入文件后自动运行 `npm run lint`。

在 Claude Code 中输入 `/hooks`，按提示完成配置。然后让 Claude 修改一个文件，观察 lint 是否自动运行。

**练习 2：用 subagent 做一次内容审查**

在 Claude Code 中让 Claude 启动一个 subagent，任务是：扫描 `content/` 目录下的所有 Markdown 文件，检查每个文件的 frontmatter 是否包含 title、slug、category、tags、date、draft 这 6 个字段，列出所有不合格的文件。

观察 subagent 返回的报告质量，以及它是否正确读取了 CLAUDE.md 中的项目背景。

**练习 3：做一次"错误归因分析"**

回顾最近一个月 Claude 在你项目中犯的错误（如果有记录的话），按以下方式分类：

- 不知道规则 → 需要补充 CLAUDE.md 或 docs/
    
- 知道但忘了执行 → 需要加 hook
    
- 上下文太复杂导致遗漏 → 需要用 subagent
    

这个分析会帮你精确定位"下一步该优化什么"。

# 全册总结

你用六篇的篇幅，从零搭建了一套完整的 AI 协作规则体系。

回顾一下你学到了什么：

**第 1 篇**：建立正确认知——CLAUDE.md 是配置文件，不是说明文档。理解 system prompt 机制、指令预算和 80% 原则。

**第 2 篇**：掌握实操方法——7 个核心模块、5 条内容项目专属规则、常见误区和成品模板。

**第 3 篇**：学会信息架构——渐进披露策略、6 份 docs/ 的职责边界、按需加载的引用方式。

**第 4 篇**：深入核心难点——frontmatter 设计方法论、slug 规则、分类标签治理、schema 思维、构建链路。

**第 5 篇**：建立质量兜底——三套检查清单、自动化与手动验证的搭配、验证嵌入工作流。

**第 6 篇**：升级到系统级——hooks 自动执行、subagents 专项隔离、三者协作模型、长期维护和升级路线。

这不只是"学会了写几个 Markdown 文件"。你学会的是一种**用工程化思维管理 AI 协作的方法**。

这套方法不只适用于 Claude Code。未来 AI 协作工具会越来越多，但"用精简规则定义行为边界 + 用自动化执行机械检查 + 用隔离机制处理复杂任务"这套思路，是通用的。

现在，翻到附录，拿到全套模板，开始在你自己的项目中落地。

> 💡 附录预告：全套 14 份模板汇总、一周落地计划、10 个常见问题解答——你需要的所有即用材料都在那里。
