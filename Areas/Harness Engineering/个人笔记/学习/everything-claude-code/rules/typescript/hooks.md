---
paths:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
  - "**/*.jsx"
---
# TypeScript/JavaScript Hooks

> 此文件扩展了 [common/hooks.md](../common/hooks.md)，包含 TypeScript/JavaScript 特定内容。

## PostToolUse Hooks

在 `~/.claude/settings.json` 配置：

- **Prettier**：编辑 JS/TS 文件后自动格式化
- **TypeScript 检查**：编辑 `.ts`/`.tsx` 文件后运行 `tsc`
- **console.log 警告**：警告编辑文件中的 `console.log`

## Stop Hooks

- **console.log 审计**：会话结束前检查所有修改文件中的 `console.log`