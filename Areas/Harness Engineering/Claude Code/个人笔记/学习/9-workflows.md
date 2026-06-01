# 9-Workflows：多智能体编排

> Workflow 是 Claude Code 的多智能体编排工具——用脚本化的方式协调多个子智能体并行或顺序执行任务。

---

## 核心特点

| 特点 | 说明 |
|------|------|
| **脚本化编排** | JavaScript 脚本定义任务流程，确定性执行而非模型驱动 |
| **并行高效** | 多个子智能体可同时运行，适合大规模搜索、验证、迁移 |
| **可缓存/可恢复** | 相同 prompt + 相同参数 = 缓存命中，可中途编辑恢复 |
| **结构化输出** | 可强制子智能体返回 JSON Schema 格式，无需解析 |

---

## 适用场景

- **大规模搜索**：多角度并行搜索，合并结果
- **多轮验证**：每个发现用 N 个独立视角验证，投票决定是否保留
- **文件迁移**：批量文件处理，每个文件独立 worktree 隔离
- **复杂研究**：搜索 → 抓取 → 验证 → 合成报告

---

## 调用方式

```javascript
// 方式1：调用内置/已保存的 workflow
Workflow({ name: "deep-research", args: "搜索问题..." })

// 方式2：传入自定义脚本
Workflow({ script: "export const meta = {...}; ..." })

// 方式3：编辑后恢复
Workflow({ scriptPath: "path/to/script.js", resumeFromRunId: "wf_xxx" })
```

---

## 脚本结构

每个 workflow 脚本必须以 `meta` 开头：

```javascript
export const meta = {
  name: 'find-flaky-tests',
  description: 'Find flaky tests and propose fixes',
  phases: [
    { title: 'Scan', detail: 'grep test logs for retries' },
    { title: 'Fix', detail: 'one agent per flaky test' },
  ],
}

// 脚本主体
phase('Scan')
const flaky = await agent('grep CI logs for retry markers', {schema: FLAKY_SCHEMA})
...
```

**meta 必须是纯字面量**，不能有变量、函数调用、模板插值。

---

## 关键 API

| API | 作用 |
|-----|------|
| `agent(prompt, opts)` | 启动一个子智能体，返回结果或结构化对象 |
| `parallel(thunks)` | 并行执行多个任务，**带屏障**（等全部完成） |
| `pipeline(items, stage1, stage2, ...)` | 流水线处理，**无屏障**（各阶段独立流动） |
| `phase(title)` | 切换进度显示的阶段 |
| `log(message)` | 输出进度消息给用户 |
| `workflow(name, args)` | 嵌套调用另一个 workflow |
| `args` | 外部传入的参数 |
| `budget` | Token 预算控制（`budget.total`、`budget.spent()`、`budget.remaining()`） |

---

## `agent()` 选项

```javascript
await agent('prompt', {
  label: '自定义显示名',
  phase: '指定进度阶段',
  schema: { type: 'object', properties: {...} },  // 强制结构化输出
  model: 'sonnet',  // 覆盖模型（默认继承主循环）
  isolation: 'worktree',  // 独立 worktree（有文件冲突时用）
  agentType: 'Explore',   // 使用特定 subagent 类型
})
```

---

## `parallel` vs `pipeline`

### parallel（屏障）

```javascript
const all = await parallel([
  () => agent('search A'),
  () => agent('search B'),
])  // 等全部完成才继续

// 适用：阶段N真正需要全部前一阶段结果
// - 合并去重后才能下一步
// - 需要判断总数是否为0来跳过后续
```

### pipeline（流水线，推荐默认）

```javascript
const results = await pipeline(
  items,
  item => agent(`process ${item}`),     // 阶段1
  result => agent(`verify ${result}`),  // 阶段2
)
// 阶段1的 item A 到阶段2时，阶段1的 item B 可能还在跑

// 适用：各阶段独立流动，无需等待全部
// Wall-clock = 最慢的单项链，不是各阶段最慢之和
```

**原则**：默认用 `pipeline`，只有当阶段 N 真正需要全部前一阶段结果时才用 `parallel`。

---

## 质量模式（Quality Patterns）

### 对抗验证（Adversarial Verify）

```javascript
const votes = await parallel(Array.from({length: 3}, () => () =>
  agent(`Try to refute: ${claim}. Default to refuted=true if uncertain.`, {schema: VERDICT})
))
const survives = votes.filter(Boolean).filter(v => !v.refuted).length >= 2
```

**用途**：防止"看起来合理但实际上错误"的发现存活。

### 视角多样验证

```javascript
const judged = await parallel(fresh.map(b => () =>
  parallel(['correctness', 'security', 'repro'].map(lens => () =>
    agent(`Judge "${b.desc}" via ${lens} lens`, {schema: VERDICT})
  ))
))
```

**用途**：一个发现可能以多种方式失败，不同视角覆盖不同失败模式。

### 循环至干（Loop-until-dry）

```javascript
const seen = new Set(), confirmed = []
let dry = 0
while (dry < 2) {
  const found = await parallel(FINDERS.map(f => () => agent(f.prompt, {schema: BUGS})))
  const fresh = found.filter(b => !seen.has(key(b)))
  if (!fresh.length) { dry++; continue }
  dry = 0; fresh.forEach(b => seen.add(key(b)))
  // 验证并加入 confirmed...
}
```

**用途**：未知规模的发现任务（bugs、issues、edge cases），直到连续 K 轮无新发现。

### 多模态扫荡

```javascript
const results = await parallel([
  () => agent('search by container'),
  () => agent('search by content'),
  () => agent('search by entity'),
  () => agent('search by time'),
])
```

**用途**：一个搜索角度无法覆盖全部，多角度互补盲区。

### 完整性批评者

```javascript
const missing = await agent('What was not covered? What sources were not read?', {schema: MISSING})
// 下一轮工作...
```

**用途**：最后检查"漏了什么"，发现的内容成为下一轮输入。

---

## Token 预算控制

用户可用 `+500k` 等指令设置 token 目标：

```javascript
// 动态扩容
while (budget.total && budget.remaining() > 50_000) {
  const result = await agent('Find bugs', {schema: BUGS})
  bugs.push(...result.bugs)
  log(`${bugs.length} found, ${Math.round(budget.remaining()/1000)}k remaining`)
}

// 静态缩放
const FLEET = budget.total ? Math.floor(budget.total / 100_000) : 5
```

---

## 内置 Workflow

| Workflow | 用途 |
|----------|------|
| **deep-research** | 多角度搜索 → 抓取 → 对抗验证 → 合成报告 |
| **review** | 多维度评审代码变更 |

---

## 与 Agent 工具的区别

| | Workflow | Agent |
|--|----------|-------|
| 控制流 | 脚本化、确定性 | 模型驱动、灵活 |
| 并行度 | 可编排多智能体 | 单个智能体 |
| 适用场景 | 大规模、多阶段、需要验证 | 单个复杂任务、搜索 |
| 用户介入 | 需显式 opt-in（"workflow"关键字） | 直接调用 |

---

## 并发与限制

- 并发上限：`min(16, cpu cores - 2)`
- 智能体总数上限：1000（防 runaway loop）
- 脚本禁用：`Date.now()`、`Math.random()`、argless `new Date()`（会破坏缓存恢复）

---

## 查看进度

运行 `/workflows` 查看实时进度。每个 workflow 会返回：
- `runId`：用于恢复
- `task_id`：用于停止
- `scriptPath`：脚本持久化路径

---

## 实战示例

### deep-research 结构

```javascript
export const meta = {
  name: 'deep-research',
  description: 'Fan-out search, fetch, verify, synthesize',
  phases: [
    { title: 'Scope', detail: 'decompose question' },
    { title: 'Search', detail: '5 parallel angles' },
    { title: 'Fetch', detail: 'extract claims' },
    { title: 'Verify', detail: '3-vote adversarial' },
    { title: 'Synthesize', detail: 'merge and cite' },
  ],
}

phase('Scope')
// 分解搜索角度...

phase('Search')
const searches = await parallel(ANGLES.map(a => () => agent(a.prompt)))

phase('Fetch')
// 抓取源页面，提取可验证论断...

phase('Verify')
// 每个论断 3 智能体对抗验证...

phase('Synthesize')
// 合成报告，引用来源...
```

---

## 相关文档

- [[8-worktree]]：Worktree 与 Workflow 配合实现并行文件修改隔离
- [[5-MCP]]：MCP 工具可在 workflow agent 中使用
- [[4-hook]]：Workflow 完成可触发 hook