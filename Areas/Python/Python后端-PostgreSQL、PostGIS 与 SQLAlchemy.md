# 目录

- [[#1. 组件关系|1. 组件关系]]
- [[#2. 数据访问链路|2. 数据访问链路]]
  - [[#2.1 Python -> SQLAlchemy -> psycopg -> PostgreSQL|2.1 Python -> SQLAlchemy -> psycopg -> PostgreSQL]]
  - [[#2.2 数据库产品、驱动、ORM 的分层|2.2 数据库产品、驱动、ORM 的分层]]
- [[#3. SQLAlchemy 核心对象|3. SQLAlchemy 核心对象]]
  - [[#3.1 Engine|3.1 `Engine`]]
  - [[#3.2 sessionmaker|3.2 `sessionmaker`]]
  - [[#3.3 Session|3.3 `Session`]]
  - [[#3.4 commit、rollback、close|3.4 `commit`、`rollback`、`close`]]
- [[#4. FastAPI 中的数据库依赖|4. FastAPI 中的数据库依赖]]
  - [[#4.1 lifespan 中创建 engine 与 session_factory|4.1 `lifespan` 中创建 `engine` 与 `session_factory`]]
  - [[#4.2 get_db() 的 yield 依赖|4.2 `get_db()` 的 `yield` 依赖]]
  - [[#4.3 Depends(get_db) 注入 Session|4.3 `Depends(get_db)` 注入 `Session`]]
- [[#5. PostgreSQL、PostGIS 与 GIS 学习范围|5. PostgreSQL、PostGIS 与 GIS 学习范围]]
  - [[#5.1 SQLite 在学习项目中的位置|5.1 SQLite 在学习项目中的位置]]
  - [[#5.2 切换 PostgreSQL 时改什么|5.2 切换 PostgreSQL 时改什么]]
  - [[#5.3 当前优先掌握的范围|5.3 当前优先掌握的范围]]

# 1. 组件关系

| 组件 | 位置 | 一句话 |
| --- | --- | --- |
| `PostgreSQL` | 数据库本体 | 存数据、执行 SQL、管理事务。 |
| `PostGIS` | `PostgreSQL` 扩展 | 给 PostgreSQL 增加空间字段、空间索引、空间函数。 |
| `psycopg` | Python 驱动 | 负责 Python 和 PostgreSQL 之间的连接与通信。 |
| `SQLAlchemy` | Python 数据访问层 | 管 `Engine`、`Session`，并提供 `Core` / `ORM`。 |
| `GeoAlchemy2` | `SQLAlchemy` 空间扩展 | 让 Python/SQLAlchemy 更方便地使用 PostGIS 能力。 |

# 2. 数据访问链路

## 2.1 Python -> SQLAlchemy -> psycopg -> PostgreSQL

Python 后端常见调用链路：

```text
业务代码
-> SQLAlchemy
-> psycopg
-> PostgreSQL
```

如果启用了空间能力，则是：

```text
业务代码
-> SQLAlchemy / GeoAlchemy2
-> psycopg
-> PostgreSQL + PostGIS
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

例如：

```python
create_engine("postgresql+psycopg://user:password@localhost:5432/dbname")
```

这里：

- `postgresql`：目标数据库
- `psycopg`：底层驱动

## 3.2 `sessionmaker`

`sessionmaker` 是生成 `Session` 的工厂。

它的职责不是执行 SQL，而是“按同一套配置批量创建 Session”。

常见写法：

```python
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
```

## 3.3 `Session`

`Session` 是一次业务操作使用的数据库会话对象。

它不是：

- 数据库本身
- 全局单例
- 具体某张表

它更接近：

- 当前这次请求的数据库工作上下文
- 当前这次事务的操作入口

实际查库、写库通常都通过 `Session` 来做。

## 3.4 `commit`、`rollback`、`close`

- `commit()`：提交事务
- `rollback()`：回滚事务
- `close()`：关闭当前会话

常见模式是：

```python
db = SessionLocal()
try:
    ...
    db.commit()
except:
    db.rollback()
    raise
finally:
    db.close()
```

即使只读查询，也通常会在请求结束后 `close()`。

# 4. FastAPI 中的数据库依赖

## 4.1 `lifespan` 中创建 `engine` 与 `session_factory`

在当前学习项目里，应用启动时会先创建数据库基础设施，再挂到 `app.state` 上。

可以近似记成：

```python
engine = create_engine(...)
session_factory = sessionmaker(bind=engine)

app.state.db_engine = engine
app.state.db_session_factory = session_factory
```

这样后续依赖函数就可以从 `app.state` 里拿到这些对象。

## 4.2 `get_db()` 的 `yield` 依赖

`get_db()` 的核心作用是：

1. 为当前请求创建一个 `Session`
2. 把这个 `Session` 注入给路由函数
3. 请求结束后关闭它

典型形态：

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

这里的 `yield` 不是返回列表，也不是生成很多值；在 FastAPI 依赖里，它表示“先把值交出去，请求结束后再执行清理逻辑”。

## 4.3 `Depends(get_db)` 注入 `Session`

路由函数里常见写法：

```python
db: Annotated[Session, Depends(get_db)]
```

这里的 `db` 就是当前请求的 `Session`。

它不是：

- PostgreSQL 本体
- SQLite 本体
- `Engine`

它是基于当前数据库配置创建出来的一次会话对象。

# 5. PostgreSQL、PostGIS 与 GIS 学习范围

## 5.1 SQLite 在学习项目中的位置

当前学习项目默认用的是：

```python
sqlite+pysqlite:///:memory:
```

它的意义主要是：

- 不需要额外安装数据库服务
- 先把 FastAPI、依赖注入、Session 生命周期跑通
- 适合最小可运行示例和测试

它不是 GIS 主线数据库。

如果目标是 WebGIS，最终重点仍然是：

- `PostgreSQL`
- `PostGIS`

## 5.2 切换 PostgreSQL 时改什么

从 SQLite 切到 PostgreSQL，核心通常只改两类东西：

1. 安装 PostgreSQL 驱动

常见是：

- `psycopg`

2. 改数据库连接串

例如：

```python
postgresql+psycopg://username:password@localhost:5432/dbname
```

`get_db()`、`Session`、`Depends(get_db)` 这一层思路通常不需要重写。

## 5.3 当前优先掌握的范围

如果学习目标是 GIS 后端，当前建议先锁定这条主线：

1. `PostgreSQL` 是数据库
2. `PostGIS` 是空间扩展
3. `psycopg` 是 Python 驱动
4. `SQLAlchemy` 是数据访问层
5. `Session` 是每次请求的数据库会话
6. `FastAPI get_db()` 负责把 `Session` 注入到路由函数

等这条链稳定后，再继续：

- `GeoAlchemy2`
- `Alembic`
- SQLAlchemy ORM 模型
- PostGIS 空间字段与空间函数
