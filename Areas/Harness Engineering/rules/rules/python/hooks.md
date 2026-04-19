---
paths:
  - "**/*.py"
  - "**/*.pyi"
---
# Python Hooks

> This file extends [common/hooks.md](Areas/Harness%20Engineering/rules/rules/common/hooks.md) with Python specific content.

## PostToolUse Hooks

Configure in `~/.claude/settings.json`:

- **black/ruff**: Auto-format `.py` files after edit via `uv run`
- **mypy/pyright**: Run type checking after editing `.py` files via `uv run`

## Warnings

- Warn about `print()` statements in edited files (use `logging` module instead)
