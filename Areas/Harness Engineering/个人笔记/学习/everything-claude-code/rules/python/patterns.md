---
paths:
  - "**/*.py"
  - "**/*.pyi"
---
# Python 模式

> 此文件扩展了 [common/patterns.md](../common/patterns.md)，包含 Python 特定内容。

## Protocol（鸭子类型）

```python
from typing import Protocol

class Repository(Protocol):
    def find_by_id(self, id: str) -> dict | None: ...
    def save(self, entity: dict) -> dict: ...
```

## Dataclass 作为 DTO

```python
from dataclasses import dataclass

@dataclass
class CreateUserRequest:
    name: str
    email: str
    age: int | None = None
```

## Context Manager 与 Generator

- 使用 context manager（`with` 语句）进行资源管理
- 使用 generator 进行惰性求值和内存高效迭代

## 参考

参见 skill：`python-patterns` 了解包括装饰器、并发和包组织的全面模式。