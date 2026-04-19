---
paths:
  - "**/*.py"
  - "**/*.pyi"
---
# Python Coding Style

> This file extends [common/coding-style.md](Areas/Harness%20Engineering/rules/rules/common/coding-style.md) with Python specific content.

## Standards

- Follow **PEP 8** conventions
- Use **type annotations** on all function signatures

## Project Management

Use **uv** as the unified Python project management tool:

- Manage dependencies and lockfiles with `uv`
- Manage virtual environments with `uv`
- Run Python tools and scripts with `uv run`
- Do not use `pip`, `poetry`, `pipenv`, or `conda` for project management unless explicitly required

## Immutability

Prefer immutable data structures:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str
    email: str

from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
```

## Formatting

- **black** for code formatting via `uv run black`
- **isort** for import sorting via `uv run isort`
- **ruff** for linting via `uv run ruff`

## Reference

See skill: `python-patterns` for comprehensive Python idioms and patterns.
