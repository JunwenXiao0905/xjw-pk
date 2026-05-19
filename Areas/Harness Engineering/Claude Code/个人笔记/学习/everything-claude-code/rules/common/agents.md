# Agent 编排

## 可用 Agent

位于 `~/.claude/agents/`：

| Agent | 用途 | 使用场景 |
|-------|---------|-------------|
| planner | 实现规划 | 复杂功能、重构 |
| architect | 系统设计 | 架构决策 |
| tdd-guide | 测试驱动开发 | 新功能、Bug 修复 |
| code-reviewer | 代码审查 | 编写代码后 |
| security-reviewer | 安全分析 | 提交前 |
| build-error-resolver | 修复构建错误 | 构建失败时 |
| e2e-runner | E2E 测试 | 关键用户流程 |
| refactor-cleaner | 死代码清理 | 代码维护 |
| doc-updater | 文档更新 | 更新文档 |
| rust-reviewer | Rust 代码审查 | Rust 项目 |
| harmonyos-app-resolver | HarmonyOS 应用开发 | HarmonyOS/ArkTS 项目 |

## 即时 Agent 使用

无需用户提示：
1. 复杂功能请求 - 使用 **planner** agent
2. 刚编写/修改的代码 - 使用 **code-reviewer** agent
3. Bug 修复或新功能 - 使用 **tdd-guide** agent
4. 架构决策 - 使用 **architect** agent

## 并行任务执行

对于独立操作，始终使用并行 Task 执行：

```markdown
# 正确：并行执行
并行启动 3 个 agent：
1. Agent 1：auth 模块安全分析
2. Agent 2：缓存系统性能审查
3. Agent 3：工具函数类型检查

# 错误：不必要的串行执行
先 agent 1，再 agent 2，再 agent 3
```

## 多视角分析

对于复杂问题，使用分角色子 agent：
- 事实审查者
- 高级工程师
- 安全专家
- 一致性审查者
- 冗余检查者