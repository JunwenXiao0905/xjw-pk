---
paths:
  - "**/*.py"
  - "**/*.pyi"
---
# Python Hooks

> 此文件扩展了 [common/hooks.md](Areas/Harness%20Engineering/Claude%20Code/个人笔记/学习/everything-claude-code/rules/common/hooks.md)，包含 Python 特定内容。

## PostToolUse Hooks

在 `~/.claude/settings.json` 配置：

- **black/ruff**：编辑 `.py` 文件后自动格式化
- **mypy/pyright**：编辑 `.py` 文件后运行类型检查

## 警告

- 警告编辑文件中的 `print()` 语句（改用 `logging` 模块）