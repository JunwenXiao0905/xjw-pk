
| 文件                 | 作用                                                |
| ------------------ | ------------------------------------------------- |
| hooks/hook.json    | 实际的 hook 配置 JSON — 就是你要 merge 进 settings.json 的内容 |
| rules/xxx/hooks.md | 人类可读的说明文档 — 描述这个 hook 做了什么，不是配置本身                 |


  所以 rules/typescript/hooks.md 和 rules/python/hooks.md
  其实是说明书，不是配置文件本身。它们的作用是让 Claude Code 的 rules 系统能够"读懂"这些 hook
  的语义，并在相应的文件类型被编辑时触发对应的检查。

  ---
  hooks.json 的实际结构

  真正的配置在 hooks/hooks.json，它是标准 Claude Code settings JSON Schema 格式，包含 hooks
  根对象，下面的结构是：

  hooks/
  ├── PreToolUse[]     ← 工具执行前（拦截、校验、修改参数）
  ├── PostToolUse[]    ← 工具执行后（格式化、检查、记录）
  ├── PreCompact[]     ← 上下文压缩前（保存状态）
  ├── Stop[]           ← 会话结束时（批量格式化、审计）
  ├── SessionStart[]   ← 新会话开始时（加载上下文）
  ├── SessionEnd[]     ← 会话真正结束时（生命周期标记）
  └── PostToolUseFailure[] ← 工具执行失败后（MCP 健康检查）

  ---
  hooks.json 里实际在跑什么

  以 TypeScript 相关的几个关键 hook 为例：

  PreToolUse 阶段：
  - pre:bash:block-no-verify — 拦截 git commit --no-verify 防止跳过 hooks
  - pre:bash:commit-quality — 提交前 lint + 检查 console.log/secrets
  - pre:edit-write:suggest-compact — 编辑时建议手动压缩上下文

  PostToolUse 阶段：
  - post:edit:accumulator — 记录所有编辑过的 JS/TS 文件路径
  - post:edit:console-warn — 每次 Edit 后立即警告 console.log
  - post:quality-gate — 编辑后跑质量门禁检查（async，不阻塞）

  Stop 阶段（批量处理）：
  - stop:format-typecheck — 最关键：收集本轮所有编辑过的 JS/TS 文件，批量跑 Prettier +
  tsc，而不是每次 Edit 都跑（这是刻意设计的性能优化）
  - stop:check-console-log — 会话结束时检查所有修改文件里的 console.log
  - stop:session-end — 将会话状态持久化
  - stop:evaluate-session — 从会话中提取可学习的模式

  ---
  设计亮点

  1. Stop 时批量格式化 — 不是每次 Edit 后立即跑 Prettier/tsc，而是收集起来在 Stop
  时一次性跑。理由：避免每次 Edit 都阻塞响应，体验更流畅。
  2. ${CLAUDE_PLUGIN_ROOT} 变量 — 所有 hook
  命令都通过这个环境变量指向插件根目录，实现了插件的可移植性。
  3. run-with-flags.js 封装层 — 每个 hook 都通过这个 JS 包装器执行，支持 standard/strict/minimal
  等flag模式来控制行为。
  4. async hooks — stop:session-end、stop:evaluate-session 等设为 async: true，不阻塞会话结束。

