# 目录

- [[#1. 组件与模块总览|1. 组件与模块总览]]
  - [[#1.1 组件关系表|1.1 组件关系表]]
  - [[#1.2 SQLAlchemy 模块分布|1.2 SQLAlchemy 模块分布]]
- [[#2. 数据访问链路|2. 数据访问链路]]
  - [[#2.1 Python → SQLAlchemy → psycopg → PostgreSQL|2.1 Python → SQLAlchemy → psycopg → PostgreSQL]]
  - [[#2.2 数据库产品、驱动、ORM 的分层|2.2 数据库产品、驱动、ORM 的分层]]
- [[#3. SQLAlchemy 核心对象|3. SQLAlchemy 核心对象]]
  - [[#3.1 Engine|3.1 `Engine`]]
  - [[#3.2 sessionmaker|3.2 `sessionmaker`]]
  - [[#3.3 Session|3.3 `Session`]]
  - [[#3.4 commit、rollback、close|3.4 `commit`、`rollback`、`close`]]
- [[#4. 模型定义|4. 模型定义]]
  - [[#4.1 DeclarativeBase — 声明式基类|4.1 `DeclarativeBase` — 声明式基类]]
  - [[#4.2 mapped_column — 列定义与类型映射|4.2 `mapped_column()` — 列定义与类型映射]]
  - [[#4.3 约束：primary-key、nullable、unique、default|4.3 约束：`primary_key`、`nullable`、`unique`、`default`]]
  - [[#4.4 ForeignKey — 外键约束|4.4 `ForeignKey` — 外键约束]]
  - [[#4.5 relationship — ORM 对象导航|4.5 `relationship()` — ORM 对象导航]]
- [[#5. 查询与操作|5. 查询与操作]]
  - [[#5.1 基础查询：select 与 get|5.1 基础查询：`select()` 与 `get()`]]
  - [[#5.2 条件过滤：filter 与 where|5.2 条件过滤：`filter()` 与 `where()`]]
  - [[#5.3 关联查询与加载策略|5.3 关联查询与加载策略]]
  - [[#5.4 写操作：add、delete、commit、refresh|5.4 写操作：`add`、`delete`、`commit`、`refresh`]]
- [[#6. FastAPI 集成|6. FastAPI 集成]]
  - [[#6.1 lifespan 中创建 engine 与 session_factory|6.1 `lifespan` 中创建 `engine` 与 `session_factory`]]
  - [[#6.2 get_db 的 yield 依赖|6.2 `get_db()` 的 `yield` 依赖]]
  - [[#6.3 Depends 注入 Session|6.3 `Depends` 注入 `Session`]]
  - [[#6.4 一次请求的事务生命周期|6.4 一次请求的事务生命周期]]
- [[#7. 新增模块工作流（Alembic）|7. 新增模块工作流（Alembic）]]
- [[#8. 扩展方向|8. 扩展方向]]

# 1. 组件与模块总览

## 1.1 组件关系表

| 组件 | 位置 | 一句话 |
| --- | --- | --- |
| `PostgreSQL` | 数据库本体 | 存数据、执行 SQL、管理事务 |
| `PostGIS` | `PostgreSQL` 扩展 | 给 PostgreSQL 增加空间字段、空间索引、空间函数 |
| `psycopg` | Python 驱动 | 负责 Python 与 PostgreSQL 之间的连接与通信 |
| `SQLAlchemy` | Python 数据访问层 | 管 `Engine`、`Session`，并提供 Core / ORM |
| `GeoAlchemy2` | `SQLAlchemy` 空间扩展 | 让 Python/SQLAlchemy 更方便地使用 PostGIS 能力 |

## 1.2 SQLAlchemy 模块分布

```text
引擎与连接
├── sqlalchemy.create_engine()           # 数据库总入口，管理连接池
├── sqlalchemy.Engine                    # 连接池 + 方言配置
└── psycopg / pysqlite                   # 底层 DB-API 驱动（非 SQLAlchemy 本体）

会话管理（sqlalchemy.orm）
├── sessionmaker                         # Session 工厂，按统一配置创建 Session
├── Session                              # 一次业务操作的数据库工作上下文
└── scoped_session                       # 注册表模式，线程/协程安全的 Session 获取

模型定义（sqlalchemy.orm）
├── DeclarativeBase                      # 声明式基类，关联 metadata
├── Mapped[T]                            # 类型注解，声明列的 Python 类型
├── mapped_column(Type, ...)             # 列定义：类型、约束、默认值
├── relationship()                       # ORM 层对象导航 + 加载策略
└── back_populates=                      # 双向关系同步标识

列类型（sqlalchemy）
├── Integer / BigInteger                 # 整数
├── String(n) / Text                     # 字符串与长文本
├── Boolean                              # 布尔
├── Float / Numeric                      # 浮点与定点数
├── DateTime / Date                      # 日期时间
├── LargeBinary                          # 二进制
└── JSON                                 # JSON 列

约束（sqlalchemy）
├── ForeignKey("table.column")           # 数据库外键约束
├── primary_key=True                     # 主键
├── nullable=False                       # 非空
├── unique=True                          # 唯一索引
├── default=                             # 默认值（Python 侧）
├── server_default=                      # 默认值（数据库侧）
├── Index("ix_name", "column")           # 显式普通索引
└── CheckConstraint / UniqueConstraint   # 复合约束

查询构建（sqlalchemy + sqlalchemy.orm）
├── select(Model)                        # 查询入口
├── filter() / where()                   # 条件过滤
├── join() / outerjoin()                 # 表连接
├── order_by() / offset() / limit()      # 排序与分页
├── group_by() / having()                # 分组与聚合后过滤
└── options(selectinload(...))           # 关系加载策略

结果与写操作（sqlalchemy.orm.Session）
├── execute(stmt)                        # 执行查询，返回 Result
├── scalars() / scalar() / scalar_one()  # 结果提取
├── get(Model, pk)                       # 主键直查
├── add(obj) / add_all(objs)             # 标记新增
├── delete(obj)                          # 标记删除
├── flush()                              # 将 pending 操作刷到数据库（不提交事务）
├── commit() / rollback()                # 事务控制
└── refresh(obj)                         # 从数据库重新加载当前行

迁移
└── alembic（独立工具，非 SQLAlchemy 本体）
    ├── alembic init                     # 初始化迁移环境
    ├── alembic revision --autogenerate  # 自动生成迁移脚本
    ├── alembic upgrade head / downgrade # 执行 / 回滚迁移
    └── alembic/env.py                   # 迁移环境配置（连接 engine、读取 metadata）
```

# 2. 数据访问链路

## 2.1 Python → SQLAlchemy → psycopg → PostgreSQL

Python 后端常见调用链路：

```text
业务代码
→ SQLAlchemy
→ psycopg
→ PostgreSQL
```

如果启用了空间能力，则是：

```text
业务代码
→ SQLAlchemy / GeoAlchemy2
→ psycopg
→ PostgreSQL + PostGIS
```

## 2.2 数据库产品、驱动、ORM 的分层

这几层不要混：

- `PostgreSQL`：数据库产品
- `PostGIS`：PostgreSQL 的空间扩展
- `psycopg`：Python 驱动
- `SQLAlchemy`：ORM / 查询层 / 会话管理层

`SQLAlchemy` 和 `Prisma` 可以先粗略看成同类工具，但它们都不是数据库驱动本身。

# 3. SQLAlchemy 核心对象

## 3.1 `Engine`

`Engine` 是数据库总入口。

它知道：

- 该连哪个数据库
- 用哪个驱动
- 连接参数是什么

```python
from sqlalchemy import create_engine

create_engine("postgresql+psycopg://user:password@localhost:5432/dbname")
```

URL 里 `postgresql` 是目标数据库，`psycopg` 是底层驱动。

## 3.2 `sessionmaker`

`sessionmaker` 是生成 `Session` 的工厂。它的职责不是执行 SQL，而是按同一套配置批量创建 Session。

```python
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
```

常见配置参数：

- `autoflush=False`：关闭自动 flush，把 flush 时机交给代码显式控制
- `autocommit=False`：关闭自动提交，每次 commit 需要手动调用
- `expire_on_commit=False`：commit 后不标记对象为过期，避免 commit 后访问属性触发额外查询

## 3.3 `Session`

`Session` 是一次业务操作使用的数据库会话对象。

它不是数据库本身、不是全局单例、不是某张表。它更接近当前这次请求的"数据库工作上下文"——查库、写库都通过 Session 来做。

## 3.4 `commit`、`rollback`、`close`

```python
from sqlalchemy.orm import Session

db = SessionLocal()
try:
    db.add(obj)
    db.commit()
except Exception:
    db.rollback()
    raise
finally:
    db.close()
```

- `commit()`：提交事务，将 pending 变更写入数据库
- `rollback()`：回滚事务，撤销当前事务中的所有变更
- `close()`：关闭会话，归还连接到连接池

即使只读查询，也应在请求结束后 `close()`。

# 4. 模型定义

## 4.1 `DeclarativeBase` — 声明式基类

所有 ORM 模型必须继承同一个 `Base`，才能注册到同一个 `metadata` 中。metadata 是 SQLAlchemy 内部的"表目录"，`create_all`、Alembic 都依赖它。

```python
# src/app/core/db.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """所有 ORM 模型共享的声明式基类。"""
```

```python
# src/app/modules/notes/model.py
from app.core.db import Base

class Note(Base):
    ...
```

`Base` 必须共享是因为：

- `Base.metadata.create_all()` 根据 metadata 中注册的所有表来建表
- `relationship()` 跨表导航时，两个模型必须属于同一个 metadata，SQLAlchemy 才能找到对方
- 如果各模型各有各的 `Base`，它们就分属不同的"表目录"，相互不可见

建表时只需一行：

```python
Base.metadata.create_all(bind=engine)
```

`create_all` 会按外键依赖自动排序建表顺序（先 `users`，再 `notes`）。但前提是**模型类已被 import**——Python 代码不执行到 `class X(Base):` 那一行，SQLAlchemy 就不知道有这个表。因此 `main.py` 中需要在调用 `create_all` 之前显式导入所有模型模块。

## 4.2 `mapped_column()` — 列定义与类型映射

```python
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False, default="")
```

写法拆解：

- `Mapped[int]`：告诉静态类型检查器，这个列的 Python 类型是 `int`
- `mapped_column(Integer, ...)`：告诉 SQLAlchemy，这个列的数据库类型是 `INTEGER`，并附带约束
- 两个信息互补：`Mapped[]` 面向 Python 侧，`mapped_column()` 面向数据库侧

常见类型映射：

| Python `Mapped[]` | SQLAlchemy 列类型 | 数据库类型 |
| --- | --- | --- |
| `int` | `Integer` | `INTEGER` |
| `int` | `BigInteger` | `BIGINT` |
| `str` | `String(n)` | `VARCHAR(n)` |
| `str` | `Text` | `TEXT` |
| `bool` | `Boolean` | `BOOLEAN` |
| `float` | `Float` | `FLOAT` |
| `datetime` | `DateTime` | `DATETIME` / `TIMESTAMP` |

`String(50)` 的长度取值依赖业务语义——username 50 足够且能建索引，hashed_password（bcrypt 固定 60 字符）128 有余量，full_name 100 覆盖多语言长名。

## 4.3 约束：`primary_key`、`nullable`、`unique`、`default`

这些是**数据库层面的约束**，不是 Python 校验。

```python
id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
```

- `primary_key=True`：主键约束，唯一 + 非空，默认自动创建索引
- `autoincrement=True`：自增主键，INSERT 时由数据库自动赋值
- `unique=True`：唯一索引，数据库层面拒绝重复值
- `nullable=False`：非空约束，INSERT 或 UPDATE 为 NULL 时数据库拒绝
- `default=True`：Python 侧默认值——实例化时如果不传，SQLAlchemy 用这个值

`default=` 和 `server_default=` 的区别：

- `default=`：Python 侧默认值，ORM 实例化时生效，`create_all` 不会生成 `DEFAULT` 子句
- `server_default=`：数据库侧默认值，DDL 生成 `DEFAULT ...`，对直接执行 SQL 也生效

大多数场景用 `default=` 就够了。需要数据库原生默认值（如 `NOW()`）时，才用 `server_default=func.now()`。

## 4.4 `ForeignKey` — 外键约束

```python
from sqlalchemy import ForeignKey

user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
```

参数是字符串 `"users.id"`，不是 Python 对象。它直接映射到数据库的 `FOREIGN KEY` 约束。

关键行为：

- 插入时，数据库检查 `users` 表中是否存在对应 `id`
- 默认 `ondelete` 为 `NO ACTION`：删用户时如果他有笔记，数据库拒绝操作
- 常用级联选项：
  - `ForeignKey("users.id", ondelete="CASCADE")`：删用户时自动删笔记
  - `ForeignKey("users.id", ondelete="SET NULL")`：删用户时笔记的 `user_id` 置空（需配合 `nullable=True`）

## 4.5 `relationship()` — ORM 对象导航

`ForeignKey` 是**数据库层**的约束，`relationship()` 是 **Python 层**的对象导航。数据库里不存在 `relationship`。

```python
# notes/model.py
class Note(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="notes")

# auth/model.py
class User(Base):
    notes: Mapped[list["Note"]] = relationship(back_populates="user")
```

两个 `relationship` 通过 `back_populates` 互指，告诉 SQLAlchemy 这是**同一段关系的两端**。好处：

- 改一端时，另一端自动同步（SQLAlchemy 内部维护一致性）
- 代码里可以用 `note.user` 和 `user.notes` 双向导航

`Mapped["User"]` 用字符串而非直接 `Mapped[User]`，是为了避免循环 import——`notes/model.py` 和 `auth/model.py` 互相引用。SQLAlchemy 在 mapper 初始化阶段才解析字符串，绕开了这个循环。

`relationship()` 的加载策略先记默认行为：访问 `note.user` 时才发出查询（lazy load）。策略控制放到 5.3 节。

# 5. 查询与操作

## 5.1 基础查询：`select()` 与 `get()`

```python
from sqlalchemy import select

# 主键直查 — 先查 identity_map，未命中再查库
note = db.get(Note, 1)

# 构建查询语句
stmt = select(Note).offset(skip).limit(limit)

# 执行 + 取全部结果
notes = db.execute(stmt).scalars().all()
```

**链式调用 → SQL 映射**

SQLAlchemy 的查询构建采用链式调用，每个方法对应 SQL 里的一个子句。此时 SQL 还没执行——`stmt` 只是一个表达式对象，真正执行在 `db.execute(stmt)` 那一刻。

```python
stmt = (
    select(Note)                              # SELECT * FROM notes
    .where(Note.user_id == user_id)            # WHERE user_id = ?
    .order_by(Note.id.desc())                  # ORDER BY id DESC
    .offset(skip)                              # OFFSET ?
    .limit(limit)                              # LIMIT ?
)
```

对应的实际 SQL：

```sql
SELECT * FROM notes WHERE user_id = 1
ORDER BY id DESC LIMIT 10 OFFSET 0;
```

| 链式方法                              | 等价 SQL                | 作用      |
| --------------------------------- | --------------------- | ------- |
| `select(Note)`                    | `SELECT * FROM notes` | 指定表     |
| `.where(Note.user_id == user_id)` | `WHERE user_id = ?`   | 条件过滤    |
| `.order_by(Note.id.desc())`       | `ORDER BY id DESC`    | 排序      |
| `.offset(skip)`                   | `OFFSET ?`            | 跳过前 N 行 |
| `.limit(limit)`                   | `LIMIT ?`             | 最多取 N 行 |

这里 `Note.user_id == user_id` 左边是 SQLAlchemy 列对象，右边是 Python 变量。SQLAlchemy 重载了 `==` 运算符，产生的不是 Python 的 `True/False`，而是 SQL 表达式 `WHERE user_id = <值>`。

`get()` vs `select()`：

- `get(Model, pk)`：按主键查单条，先查 Session 缓存，最简单直接
- `select(Model)`：构建查询表达式，支持链式调用加条件，灵活但需要 `execute()`
- `scalars()` 提取每行第一列的 ORM 对象，`all()` 转成列表

## 5.2 条件过滤：`filter()` 与 `where()`

```python
from sqlalchemy import select

# WHERE 单条件
stmt = select(Note).where(Note.done == False)

# WHERE 多条件（AND）
stmt = select(Note).where(Note.user_id == 1, Note.done == False)

# OR 条件
from sqlalchemy import or_
stmt = select(Note).where(or_(Note.title == "...", Note.done == True))

# 排序
from sqlalchemy import desc
stmt = select(Note).order_by(desc(Note.id)).offset(0).limit(20)
```

`filter()` 和 `where()` 在 SQLAlchemy 2.0 中等价，统一用 `where()`。条件表达式写成 `Note.done == False` 而不是 `Note.done is False`——SQLAlchemy 重载了比较运算符来生成 SQL 表达式。

## 5.3 关联查询与加载策略

最常用的关联查询写法不是手动 `join`，而是靠 `relationship` 导航 + 控制加载策略。

```python
from sqlalchemy.orm import selectinload

# 一次查询拉出所有笔记 + 各自的用户，避免 N+1
stmt = select(Note).options(selectinload(Note.user))
notes = db.execute(stmt).scalars().all()

# 反方向：查用户时预加载他的所有笔记
stmt = select(User).options(selectinload(User.notes)).where(User.id == 1)
```

常见加载策略：

| 策略 | 行为 | 适用场景 |
| --- | --- | --- |
| 默认 lazy | 访问属性时才发查询 | 很少访问关联对象 |
| `selectinload` | 用 `IN` 子查询批量加载 | 大多数关联查询，一次搞定 |
| `joinedload` | 用 `JOIN` 一次查询 | 一对一关系，或确实需要 JOIN 的数据 |

**N+1 问题**：假如查 10 条笔记，然后循环访问 `note.user`。默认 lazy 策略会在循环里逐条查用户——1 次查笔记 + 10 次查用户 = 11 次查询。用 `selectinload(Note.user)` 则只需 2 次：1 次查笔记 + 1 次 `IN (id1, id2, ...)` 查用户。

## 5.4 写操作：`add`、`delete`、`commit`、`refresh`

```python
# 新增
note = Note(title="hello", content="world", user_id=1)
db.add(note)        # 标记为待插入
db.commit()         # 提交事务，执行 INSERT
db.refresh(note)    # 从数据库重载，拿到 id 等由数据库生成的值

# 全量更新
note = db.get(Note, note_id)
note.title = "new title"
note.content = "new content"
db.commit()
db.refresh(note)

# 部分更新
note = db.get(Note, note_id)
for key, value in update_data.items():
    setattr(note, key, value)
db.commit()
db.refresh(note)

# 删除
note = db.get(Note, note_id)
db.delete(note)     # 标记为待删除
db.commit()         # 提交事务，执行 DELETE
```

关键点：

- `add()`、`delete()` 只是**标记**操作，不是立即执行 SQL。真正执行在 `flush()` 或 `commit()` 时
- `refresh()` 重新从数据库拉取当前行，覆盖内存中的对象。INSERT 后常用它拿到自增 id
- 每个事务建议匹配一次 `commit()` 或 `rollback()`

# 6. FastAPI 集成

## 6.1 `lifespan` 中创建 `engine` 与 `session_factory`

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_engine_from_settings(settings)
    session_factory = create_session_factory(engine)
    Base.metadata.create_all(bind=engine)

    app.state.db_engine = engine
    app.state.db_session_factory = session_factory
    try:
        yield
    finally:
        engine.dispose()
```

- 应用启动时创建 engine 和 session_factory，挂到 `app.state`
- `Base.metadata.create_all()` 建全所有注册过的表
- 应用关闭时 `engine.dispose()` 释放连接池

## 6.2 `get_db()` 的 `yield` 依赖

```python
def get_db(request: Request) -> Generator[Session, None, None]:
    session_factory = request.app.state.db_session_factory
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
```

核心作用：

1. 为当前请求创建一个 `Session`
2. 把这个 `Session` 注入给路由函数
3. 请求结束后 `close()` 归还连接

这里的 `yield` 在 FastAPI 依赖里表示"先把值交出去，请求结束后再执行 `finally` 清理逻辑"。

## 6.3 `Depends` 注入 `Session`

```python
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

# 路由函数里
db: Annotated[Session, Depends(get_db)]
```

拿到的 `db` 就是当前请求的 `Session`——一次请求一个会话，请求结束自动关闭。它不是 PostgreSQL 本体、不是 `Engine`、不是全局单例。

## 6.4 一次请求的事务生命周期

`get_db()` 配合 `yield` 把整个请求包裹在一个事务里：

```python
def get_db(request: Request) -> Generator[Session, None, None]:
    db = session_factory()
    try:
        yield db          # ← 路由函数在这里执行
        db.commit()        # 正常返回 → 提交事务
    except Exception:
        db.rollback()      # 抛异常 → 回滚事务
        raise
    finally:
        db.close()         # 无论成败 → 关闭会话
```

正常请求的时间线：

```text
请求进入
├─ session_factory()         → 创建 Session，事务自动开始
├─ yield db                  → 注入 router → service → repository
│   ├─ db.add(note)          → 标记"这条要插入"（仅内存）
│   └─ db.flush()            → SQL 发到数据库（事务开着，其他连接不可见）
├─ 路由函数 return           → FastAPI 拿到返回值
├─ db.commit()               → 敲死，所有 flush 的 SQL 正式生效
├─ db.close()                → 归还连接到池
└─ 响应返回浏览器
```

路由函数抛异常时的时间线：

```text
请求进入
├─ session_factory()         → 创建 Session
├─ yield db
│   ├─ db.add(note)
│   └─ raise XxxException    → 异常沿调用栈向上传播
├─ 跳过 commit()，进入 except
│   └─ db.rollback()         → 撤销本事务内所有已发出的 SQL
│   └─ raise                 → 异常继续抛给 FastAPI exception_handler
├─ db.close()
└─ FastAPI 返回 500 / 4xx
```

**核心原则**：一个请求就是一个事务。Repository 只负责标记操作和发 SQL（`add`、`delete`、`flush`），事务的"敲死"和"撤销"由最外层的 `get_db()` 统一控制。这意味着如果后续一个 service 方法需要跨多张表操作，它们天然就在同一个事务里。

# 7. 新增模块工作流（Alembic）

当需要新增一个业务模块（一张新表）时，完整流程如下。以新增 `tags` 标签模块为例：

```text
 1. 定义 ORM 模型
    src/app/modules/tags/model.py
    → class Tag(Base): id, name, color

 2. 定义 Pydantic schema
    src/app/modules/tags/schema.py
    → TagCreate, TagResponse

 3. 注册模型到 Base.metadata（⚠️ 最容易漏的一步）
    main.py        → import app.modules.tags.model
    alembic/env.py → import app.modules.tags.model

 4. 生成迁移脚本（对比模型 vs 当前数据库）
    alembic revision --autogenerate -m "add tags table"
    → 生成 alembic/versions/xxxx_add_tags_table.py

 5. 执行迁移
    alembic upgrade head
    → tags 表创建到数据库

 6. 写 repository
    src/app/modules/tags/repository.py
    → TagRepository(db): create, list, delete

 7. 写 service
    src/app/modules/tags/service.py
    → TagService(repository): create_tag, list_tags

 8. 写 router
    src/app/modules/tags/router.py
    → POST /tags, GET /tags

 9. 注册路由
    main.py → app.include_router(tags_router)

10. 注册依赖
    dependencies.py → get_tag_repository, get_tag_service
```

**核心记忆点**：

- 第 3 步必须同时改 `main.py` 和 `alembic/env.py`，少 import 一处 alembic 就检测不到新表
- 第 4-5 步是用 `create_all` 时最缺的东西——它能"对比差异并生成增量变更"，而不是盲建
- 第 6-10 步是机械活，照着 `notes` 模块的结构抄就行

**迁移脚本维护要点**：

Alembic 目录中的文件分工：

| 文件 | 谁维护 | 频率 |
|------|--------|------|
| `alembic.ini` | 手写一次 | 几乎不改 |
| `alembic/env.py` | 手写一次 | 几乎不改 |
| `alembic/script.py.mako` | 模板，不用动 | 几乎不改 |
| `alembic/versions/*.py` | autogenerate 生成 + 人工审核补全 | 每次改模型 |

`--autogenerate` 能自动检测 90% 的结构变更（加列、删列、加表、改约束），但以下情况需要人工在迁移脚本里补 `op.execute()`：

- 给已有行的新列填默认值
- 重命名列 / 表（autogenerate 会误判为"删旧的 + 加新的"）
- 复杂索引变更

加列并填充老行数据的典型写法：

```python
def upgrade():
    # autogenerate 自动生成的结构变更
    op.add_column('notes', sa.Column('priority', sa.Integer(), nullable=True))

    # 人工补充的数据迁移
    op.execute("UPDATE notes SET priority = 0 WHERE priority IS NULL")

    # 如果需要改为必填
    op.alter_column('notes', 'priority', nullable=False)


def downgrade():
    op.drop_column('notes', 'priority')
```

日常工作流：

```text
改模型 → alembic revision --autogenerate -m "..."
       → 打开生成的 versions/*.py 看一眼
       → 需要补数据操作就手写 op.execute()
       → alembic upgrade head
```

# 8. 扩展方向

当前学习主线已覆盖：

1. `PostgreSQL` 是数据库
2. `PostGIS` 是空间扩展
3. `psycopg` 是 Python 驱动
4. `SQLAlchemy` 是数据访问层
5. `Session` 是每次请求的数据库会话
6. FastAPI `get_db()` 负责把 `Session` 注入到路由函数
7. ORM 模型定义：`Base`、`mapped_column`、约束、`ForeignKey`、`relationship`
8. 基础查询与写操作：`select`、`get`、`where`、`add`、`delete`、`commit`、`refresh`

后续按优先级扩展：

1. `GeoAlchemy2`：空间字段与空间函数
2. 高级查询：聚合、子查询、窗口函数
