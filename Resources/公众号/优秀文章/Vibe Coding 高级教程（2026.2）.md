# Vibe Coding 高级教程（2026.2）

原创 AGI研习社 AGI研习社

 _2026年3月1日 08:00_ _北京_ 51人

> 更新时间：2026-02-28  
> 目标：把 `skills`、`MCP`、`subagent`、`multi-agent` 用成一套可落地的工程方法，而不只是“会写提示词”。

## 你将得到什么

1. 1. 一套分章节的学习路径（从单代理到多代理协作）。
    
2. 2. 可直接复制的配置模板（`AGENTS.md`、`SKILL.md`、`.codex/config.toml`）。
    
3. 3. 丰富示例（审查、重构、排障、文档核验、并行执行）。
    
4. 4. 可用于团队复用的评测与治理方法。
    

## 推荐阅读顺序

1. 1. 01-心智模型与最小环境
    
2. 2. 02-Skills 进阶
    
3. 3. 03-MCP 进阶
    
4. 4. 04-Subagent 与 Multi-agent
    
5. 5. 05-端到端实战案例
    
6. 6. 06-评测、回归与运维
    
7. 7. 07-提示词库与模式清单
    

## 总体架构图

## 快速上手（15 分钟）

1. 1. 在项目根目录创建 `AGENTS.md`，写清楚：允许改哪些目录、必须跑哪些测试、输出格式。
    
2. 2. 在 `.codex/skills/` 新建一个最小技能（例如 `pr-risk-check/SKILL.md`）。
    
3. 3. 在 `.codex/config.toml` 接入至少一个 MCP（文档类或浏览器类）。
    
4. 4. 启用 `multi_agent=true`，新增两个子代理：`explorer`（只读探索）、`reviewer`（风险审查）。
    
5. 5. 运行一次真实任务并产出结构化报告。
    

## 如何使用本教程

1. 1. 每章先看“核心概念图”，再复制“最小示例”。
    
2. 2. 每章末尾都有“常见坑”和“验收清单”，用于快速自检。
    
3. 3. 如果你只想马上落地，看第 5 章和第 7 章。
    

## 官方资料索引

- • Codex 文档首页
    
- • AGENTS.md 指南
    
- • Skills
    
- • MCP
    
- • Multi-agents
    
- • Multi-agents 概念
    
- • Skills + Shell + Compaction
    
- • Testing Agent Skills with Evals
    
- • Model Context Protocol
    

  

# 01. 心智模型与最小环境

## 1.1 什么是高级 Vibe Coding

“高级”不是写更长的 prompt，而是把 AI 变成一个可治理的工程系统：

1. 1. `AGENTS.md` 负责规则与边界。
    
2. 2. `Skills` 负责稳定复用复杂流程。
    
3. 3. `MCP` 负责连接外部能力与上下文。
    
4. 4. `Subagent/Multi-agent` 负责并行分工。
    
5. 5. `Evals` 负责质量闭环。
    

## 1.2 AGENTS.md 的优先级（官方要点）

Codex 会按目录向上查找 `AGENTS.md`，并合并/覆盖指令。  
官方还支持回退文件名：`AGENT.md`、`CLAUDE.md`。  
全局位置还可在 `~/.codex/AGENTS.md`（或 `CODEX_HOME/AGENTS.md`）。

## 1.3 最小环境模板

### 目录结构

`your-project/     AGENTS.md     .codex/       config.toml       skills/         pr-risk-check/           SKILL.md`

### `AGENTS.md` 最小模板

`# AGENTS.md      ## Scope   - 本仓库默认语言: TypeScript   - 允许修改目录: src/, tests/, docs/   - 禁止修改目录: infra/prod/, secrets/      ## Quality Gate   - 改动后必须执行:  - npm run lint  - npm test      ## Delivery Format   - 先给风险摘要，再给修改点，再给测试结果   - 所有文件引用都要带路径和行号`

## 1.4 高级心法：从“请求”到“任务协议”

把模糊请求改写成协议化任务：

`目标: 为支付模块增加幂等校验   输入: 当前分支代码 + 支付接口文档(MCP)   约束: 不改 public API，不增加数据库字段   验收: 新增单测覆盖 3 个失败场景，lint+test 全绿   输出: 变更摘要、风险点、回归建议`

这一步会显著降低“跑偏”和“返工”。

## 1.5 快速自检清单

1. 1. 是否有 `AGENTS.md`，且写了“可改/不可改目录”？
    
2. 2. 是否定义了必须执行的测试命令？
    
3. 3. 输出格式是否固定（摘要、变更、测试、风险）？
    
4. 4. 是否把需求改写成“目标-约束-验收”协议？
    

## 1.6 常见坑

1. 1. 只有 prompt 没有规则文件，代理会在大任务中漂移。
    
2. 2. 没有“负约束”（不能改什么），容易误改。
    
3. 3. 不做质量门禁，结果不可复现。
    

## 1.7 参考资料

- • AGENTS.md guide
    
- • Codex docs
    

  

# 02. Skills 进阶

## 2.1 Skills 的本质

Skill 是“可按需加载的任务说明书”，用于复用复杂流程。  
官方强调：Skill 会被自动发现，且只在相关时加载，避免上下文膨胀。

## 2.2 自动发现路径（官方）

1. 1. 项目级：`./.codex/skills/`
    
2. 2. 用户级：`$CODEX_HOME/skills/`
    
3. 3. 内置技能：Codex bundled skills
    

## 2.3 标准 Skill 结构

`.codex/skills/     pr-risk-check/       SKILL.md     migration-guardian/       SKILL.md`

`SKILL.md` 建议包含：

1. 1. 元数据（`name`、`description`）。
    
2. 2. 触发条件（When to use）。
    
3. 3. 非触发条件（Don't use when）。
    
4. 4. 执行步骤（Steps）。
    
5. 5. 输出格式（Output contract）。
    

## 2.4 好/坏 description 对比（非常关键）

坏例子：

`description: Review code`

问题：太宽泛，会误触发。

好例子：

`description: 审查 PR 的正确性/安全性/测试缺口。仅用于审查，不用于直接改代码。`

优点：路由更精确，避免在“实现需求”任务中误调用。

## 2.5 示例 1：PR 风险审查 Skill

`---   name: pr-risk-check   description: 审查 PR 的逻辑正确性、安全风险、测试覆盖缺口。仅用于 review。   ---      ## When to use   - 用户要求 review、risk-check、回归风险分析      ## Don't use when   - 用户要求直接实现新功能      ## Steps   1. 阅读改动文件与调用链   2. 识别逻辑回归、安全边界、并发问题   3. 检查测试是否覆盖关键路径   4. 按严重级别输出      ## Output contract   - Critical/High/Medium/Low   - 每条包含: 位置、触发条件、后果、修复建议`

## 2.6 示例 2：数据库迁移守护 Skill

`---   name: migration-guardian   description: 审核数据库迁移的兼容性与回滚策略，避免线上不可逆变更。   ---      ## Steps   1. 检查是否有向后兼容窗口   2. 检查读写路径是否双写/双读   3. 检查是否提供回滚脚本   4. 生成上线前检查清单`

## 2.7 显式调用 Skill（强制触发）

当自动路由不稳定时，直接在提示词里写：

`Use the pr-risk-check skill to review this branch against main.`

## 2.8 多 Skill 协作模式

## 2.9 常见坑

1. 1. Skill 文档写成“知识百科”，没有执行步骤。
    
2. 2. 缺少 `Don't use when`，导致误触发。
    
3. 3. 输出格式不固定，结果不可自动评测。
    

## 2.10 验收清单

1. 1. 每个 Skill 都有明确边界与负例。
    
2. 2. 同一任务重复运行，输出结构稳定。
    
3. 3. Skill 能单独被显式调用。
    

## 2.11 参考资料

- • Codex Skills
    
- • Skills + Shell + Compaction
    

  

# 03. MCP 进阶

## 3.1 MCP 能解决什么

MCP（Model Context Protocol）让代理可安全访问外部工具与数据源，例如：

1. 1. 文档检索（API/SDK 文档）。
    
2. 2. 浏览器调试（截图、页面状态）。
    
3. 3. 设计稿/工单/监控系统。
    

## 3.2 官方支持的传输类型

1. 1. `stdio`：本地命令拉起 server。
    
2. 2. `SSE`：事件流连接。
    
3. 3. `Streamable HTTP`：HTTP 传输。
    

## 3.3 `.codex/config.toml` 示例（可复制）

`[mcp_servers.context7]   command = "npx"   args = ["-y", "@upstash/context7-mcp"]      [mcp_servers.devdocs]   url = "https://developers.openai.com/mcp"      [mcp_servers.chrome_devtools]   url = "http://localhost:3000/mcp"   enabled_tools = ["open", "screenshot", "click"]   startup_timeout_sec = 20   tool_timeout_sec = 45`

## 3.4 最小权限原则（强烈建议）

1. 1. 优先用 `enabled_tools` 白名单。
    
2. 2. 对危险工具加入 `disabled_tools`。
    
3. 3. 对慢工具设置合理超时，避免任务卡死。
    

## 3.5 MCP 调用实战示例

### 场景 A：查 SDK 参数变化

`Use the docs MCP server to verify whether FooClient.create() changed parameters   between v2 and v3, then list migration notes.`

### 场景 B：前端页面回归检查

`Use chrome_devtools MCP to open /checkout, take screenshots for desktop/mobile,   and report visual regressions against baseline.`

### 场景 C：日志排障

`Query incident logs via MCP, summarize top 3 error signatures in last 24h,   and map each signature to possible owning service.`

## 3.6 连接与调试命令

`codex mcp list`

用途：快速确认 MCP server 是否成功注册。

## 3.7 故障排查清单

1. 1. `codex mcp list` 看不到 server：检查 `config.toml` 路径与拼写。
    
2. 2. 工具调用超时：增大 `startup_timeout_sec` 或 `tool_timeout_sec`。
    
3. 3. 代理误用工具：收缩 `enabled_tools` 白名单。
    
4. 4. 信息过载：按任务拆分 MCP server，不要“一把梭”接全部系统。
    

## 3.8 架构建议

## 3.9 参考资料

- • Codex MCP
    
- • Model Context Protocol
    

  

# 04. Subagent 与 Multi-agent

## 4.1 两者区别

1. 1. `Subagent`：当前任务里临时委派一个子代理（一次性）。
    
2. 2. `Multi-agent`：在配置里长期定义多个角色，可反复复用。
    

## 4.2 官方启用方式（实验特性）

`[features]   multi_agent = true      [agents]   max_threads = 6   max_depth = 1      [agents.explorer]   description = "Codebase explorer specialized in fast read-only scanning."   config_file = "agents/explorer.toml"      [agents.reviewer]   description = "Strict reviewer for correctness, security, and test coverage."   config_file = "agents/reviewer.toml"`

> 官方文档指出：`max_threads` 是并行上限，`max_depth` 是委派深度上限，建议从 `max_depth=1` 开始。

## 4.3 子代理 profile 示例

`agents/explorer.toml`：

`model = "gpt-5-codex"   sandbox_mode = "read-only"   approval_policy = "never"      prompt = """   You are a read-only code explorer.   Goals:   1) map impacted files and call graph   2) identify uncertainty and missing context   3) do not propose edits   Output sections:   - Findings   - Unknowns   - Suggested next probes   """`

`agents/reviewer.toml`：

`model = "gpt-5-codex"   sandbox_mode = "read-only"   approval_policy = "never"      prompt = """   You are a strict code reviewer.   Prioritize:   1) correctness regressions   2) security and data leaks   3) missing tests   Output severity: Critical/High/Medium/Low.   """`

## 4.4 多代理常见编排模式

### 模式 A：扇出汇总（Fan-out/Fan-in）

适合：需求分析、PR 审查、故障定位。

### 模式 B：流水线

1. 1. `explorer` 先定位文件与依赖。
    
2. 2. `implementer` 再改代码。
    
3. 3. `reviewer` 最后做风险检查。
    

适合：复杂改造任务，阶段边界清晰。

### 模式 C：红蓝对抗

1. 1. `builder` 给方案。
    
2. 2. `breaker` 专门找漏洞和反例。
    
3. 3. 主代理合并“可执行 + 可防御”版本。
    

## 4.5 可直接使用的委派提示词

### 示例 1：PR 审查

`Review this branch against main.   Ask explorer to map changed call paths,   ask reviewer to identify correctness/security/test risks,   ask docs_researcher to verify API behavior via MCP docs.   Wait for all agents and return one consolidated report by severity.`

### 示例 2：重构方案

`Plan a safe refactor for payment retry logic.   Delegate:   - explorer: collect code hotspots and coupling   - architect: propose 2 designs with tradeoffs   - reviewer: challenge each design with failure scenarios   Then produce a final recommendation and migration plan.`

## 4.6 失败模式与防漂移

1. 1. 角色重叠：多个子代理做同样的事。  
    修复：在 prompt 里写清“边界”和“禁止输出”。
    
2. 2. 无休止递归委派。  
    修复：`max_depth=1` 起步；只在主代理允许时二次委派。
    
3. 3. 汇总结论冲突。  
    修复：要求每个子代理提供“证据路径 + 不确定项”。
    

## 4.7 验收清单

1. 1. 每个 agent 有明确职责与输出格式。
    
2. 2. 并行代理数量受控（不要盲目拉满）。
    
3. 3. 主代理能给出一致的最终结论，而不是拼贴文本。
    

## 4.8 参考资料

- • Codex Multi-agent
    
- • Multi-agents Concept
    

  

# 05. 端到端实战案例

## 5.1 案例目标

任务：为电商支付系统新增“幂等重试保护”，并保证上线安全。  
要求：

1. 1. 不改公开 API。
    
2. 2. 不新增数据库表。
    
3. 3. 单测覆盖成功/失败/重复请求三类场景。
    

## 5.2 角色设计

1. 1. `explorer`：定位耦合点与调用链。
    
2. 2. `implementer`：执行最小改动。
    
3. 3. `reviewer`：审查正确性、安全、测试缺口。
    
4. 4. `docs_researcher`：通过 MCP 文档核对 SDK 行为。
    

Docs Researcher(MCP)ReviewerImplementerExplorerMain AgentUserDocs Researcher(MCP)ReviewerImplementerExplorerMain AgentUser交付需求与约束探索调用链核验外部API行为影响面和风险点版本差异和限制生成最小改动方案代码修改与测试风险审查严重级别报告最终交付

## 5.3 配置样例

`.codex/config.toml`：

`[features]   multi_agent = true      [agents]   max_threads = 4   max_depth = 1      [agents.explorer]   description = "Read-only scanner for hotspots and call graphs."   config_file = "agents/explorer.toml"      [agents.implementer]   description = "Minimal-change implementer with test-first mindset."   config_file = "agents/implementer.toml"      [agents.reviewer]   description = "Strict reviewer for correctness/security/testing."   config_file = "agents/reviewer.toml"      [agents.docs_researcher]   description = "Checks API behavior against documentation via MCP."   config_file = "agents/docs-researcher.toml"      [mcp_servers.devdocs]   url = "https://developers.openai.com/mcp"`

## 5.4 一次完整执行的提示词（可复制）

`Goal:   Add idempotent retry protection for payment create flow.      Constraints:   - No public API changes   - No new DB table   - Keep backward compatibility      Delegation:   1) Ask explorer to map impacted files and call graph.   2) Ask docs_researcher to verify external SDK retry semantics via MCP docs.   3) Ask implementer to produce minimal patch and tests.   4) Ask reviewer to evaluate correctness, security, and test gaps.      Output:   - Final diff summary   - Risk report by severity   - Test evidence   - Rollout and rollback checklist`

## 5.5 期望输出模板

`# Delivery Report      ## Diff Summary   - touched files:   - key logic changes:      ## Risk Review   - Critical:   - High:   - Medium:   - Low:      ## Test Evidence   - unit tests:   - integration tests:   - uncovered paths:      ## Rollout Plan   1.   2.   3.      ## Rollback Plan   1.   2.`

## 5.6 进阶变体

### 变体 A：先审查后实现（更稳）

1. 1. explorer + reviewer 先输出风险地图。
    
2. 2. implementer 只按批准方案修改。
    

适用：高风险改动（支付、权限、数据迁移）。

### 变体 B：并行探索（更快）

1. 1. explorer 扫代码。
    
2. 2. docs_researcher 查文档。
    
3. 3. 主代理合并后再让 implementer 施工。
    

适用：需求不清晰、外部依赖复杂。

## 5.7 实战经验

1. 1. 让 implementer 默认“最小补丁”，避免一次改太多。
    
2. 2. reviewer 输出必须带“证据路径”（文件/函数/测试名）。
    
3. 3. 最终报告强制包含“未覆盖风险”，防止虚假确定性。
    

## 5.8 验收清单

1. 1. 约束是否被严格遵守？
    
2. 2. 是否给出可执行回滚方案？
    
3. 3. 是否明确列出未覆盖场景？
    

## 5.9 参考资料

- • Codex Multi-agent
    
- • Codex MCP
    

  

# 06. 评测回归与运维

## 6.1 为什么必须做评测

Skill 和多代理流程一旦上线，很容易出现：

1. 1. 输出格式漂移。
    
2. 2. 风险判断不稳定。
    
3. 3. 版本升级后能力回退。
    

官方实践建议把评测做成持续流程，而不是“一次性手工检查”。

## 6.2 基础评测闭环

## 6.3 结构化评测命令示例

`codex exec --skip-git-repo-check --full-auto --json \  "Review this PR and output findings by severity."`

进阶：加输出 schema，保证结果格式可机读。

`codex exec --skip-git-repo-check --full-auto \     --output-schema /tmp/report_schema.json \  "Evaluate the transcript using the rubric and return JSON only."`

## 6.4 评分维度建议

1. 1. `Correctness`：是否识别真实问题。
    
2. 2. `Precision`：是否把小问题误报成高危。
    
3. 3. `Coverage`：关键路径是否覆盖。
    
4. 4. `Actionability`：建议是否可执行。
    
5. 5. `Format Stability`：输出是否稳定符合模板。
    

## 6.5 结果看板（建议字段）

`{  "run_id": "2026-02-28-nightly",  "skill": "pr-risk-check",  "accuracy": 0.83,  "false_positive_rate": 0.11,  "format_pass_rate": 0.96,  "notes": "High severity over-reporting on async timeout cases"   }`

## 6.6 运维策略

1. 1. 每次改 Skill 后跑小规模回归（smoke eval）。
    
2. 2. 每周跑全量任务集（nightly eval）。
    
3. 3. 评测失败时，不直接删 Skill，先定位是路由问题还是步骤问题。
    
4. 4. 对关键任务保留“人工审批”。
    

## 6.7 失效恢复手册

1. 1. 回退到上一个稳定 Skill 版本。
    
2. 2. 关闭高风险代理（如可写代理），仅保留只读审查链路。
    
3. 3. 暂时切到单代理保守模式，直到回归通过。
    

## 6.8 常见坑

1. 1. 只看单次跑通，不看长期波动。
    
2. 2. 没有结构化输出，导致无法自动比较。
    
3. 3. 测试集过小，评测结果虚高。
    

## 6.9 参考资料

- • Testing Agent Skills with Evals
    
- • Skills + Shell + Compaction
    

  

# 07. 提示词库与模式清单

## 7.1 使用原则

1. 1. 先写目标和约束，再写委派。
    
2. 2. 强制输出格式，避免“散文式结果”。
    
3. 3. 尽量要求“证据路径 + 不确定项”。
    

## 7.2 通用任务协议模板

`Goal:      Inputs:      Constraints:      Delegation:   - agent_a:   - agent_b:      Output Contract:   - section_1   - section_2      Acceptance:   - test commands   - risk threshold`

## 7.3 Skills 触发模板

### 自动触发友好型

`Please perform a risk-focused code review for this PR, prioritizing correctness,   security boundaries, and missing tests.`

### 显式触发型

`Use the pr-risk-check skill to review this branch against main.`

## 7.4 MCP 调用模板

### 文档核验

`Use docs MCP to verify the exact parameters and return type of FooClient.create().   If version differences exist, provide migration notes.`

### 浏览器回归

`Use browser MCP to open /checkout and /payment-result, capture screenshots,   and list UI regressions with reproducible steps.`

## 7.5 多代理模板（高频）

### 模板 A：并行审查

`Ask explorer to map impacted files,   ask reviewer to find correctness/security/test risks,   ask docs_researcher to verify external API behavior via MCP.   Wait for all and produce one merged report by severity.`

### 模板 B：方案评审

`Ask architect to provide two implementation options with tradeoffs.   Ask breaker to challenge each option with failure scenarios.   Then produce a final recommendation with rollout/rollback plan.`

### 模板 C：上线检查

`Before release:   1) verify test coverage and flaky tests   2) verify migration safety and rollback path   3) produce go/no-go decision with rationale`

## 7.6 输出格式模板

`# Executive Summary      ## What changed      ## Risk findings (Critical->Low)      ## Evidence   - file/function/test/log references      ## Unknowns      ## Next actions   1.   2.   3.`

## 7.7 防幻觉模板

`For each conclusion, attach at least one evidence path (file/function/test/log).   If evidence is missing, label it as "Hypothesis" instead of "Fact".`

## 7.8 任务模式速查表

|任务类型|推荐模式|关键配置|
|---|---|---|
|PR 风险审查|fan-out 审查|read-only subagents|
|大型重构|流水线|max_depth=1, stage gates|
|线上故障|双轨并行（代码+日志）|MCP + explorer|
|需求澄清|先探索后实现|explorer first|
|上线前评估|红蓝对抗|builder + breaker|

## 7.9 个人训练法（30 天）

1. 1. 第 1 周：只练 `AGENTS.md` + 单 Skill。
    
2. 2. 第 2 周：加一个 MCP（文档或浏览器）。
    
3. 3. 第 3 周：引入 2 个子代理并行审查。
    
4. 4. 第 4 周：接入 `codex exec` 评测并做一轮回归优化。
    

## 7.10 参考资料

- • Codex docs
    
- • Multi-agents
    
- • MCP
    

  

![](https://mmbiz.qlogo.cn/sz_mmbiz_jpg/B25AFRYiaFvOjOJria4R0WQa4exVo20N5X9KSGM263EzJ9oZglP4a9PQEticmdWW1HoiccHNcBZ6yuRQ1QdYjppN8g/0?wx_fmt=jpeg)

AGI研习社

稀罕作者

阅读 8349

​

[](javacript:;)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/0jXawkmPkLlb6pax3GJLicEuUNtpDhSo1PhHdNibT2jHUG5Rf1TNwOcAlA7C2PAnWpv0Ety4xTq200vz8F6zwoDA/300?wx_fmt=png&wxfrom=18)

AGI研习社

关注

199

1406

123

4

![](https://wx.qlogo.cn/mmopen/duc2TvpEgSRKrwicE9icxabloW41Md1WmBUBEibUbgoicG4wQiaIq4VxA3icgwOKGts9laXwJVF6CxRERrnbdmuvkGeCuIIBkT5nf28K25Ikkt9zWACAQeAvN0iaHrHDI3Jje6N/96)

复制搜一搜

复制搜一搜

暂无评论