# Python 后端 — SQLite

## 目录

- [[#1. 什么是 SQLite|1. 什么是 SQLite]]
  - [[#1.1 定位|1.1 定位]]
  - [[#1.2 与服务端数据库的区别|1.2 与服务端数据库的区别]]
- [[#2. Python 标准库 sqlite3|2. Python 标准库 sqlite3]]
  - [[#2.1 连接数据库|2.1 连接数据库]]
  - [[#2.2 建表|2.2 建表]]
  - [[#2.3 插入数据|2.3 插入数据]]
  - [[#2.4 查询数据|2.4 查询数据]]
  - [[#2.5 参数化查询|2.5 参数化查询]]
  - [[#2.6 事务|2.6 事务]]
  - [[#2.7 游标|2.7 游标]]
  - [[#2.8 check_same_thread|2.8 `check_same_thread`]]
- [[#3. 存储结构|3. 存储结构]]
  - [[#3.1 单文件|3.1 单文件]]
  - [[#3.2 页组织|3.2 页组织]]
- [[#4. 常用场景|4. 常用场景]]
  - [[#4.1 适合|4.1 适合]]
  - [[#4.2 不适合|4.2 不适合]]
- [[#5. LangGraph 中的 SqliteSaver|5. LangGraph 中的 SqliteSaver]]
  - [[#5.1 接入方式|5.1 接入方式]]
  - [[#5.2 内部表|5.2 内部表]]

# 1. 什么是 SQLite

## 1.1 定位

SQLite 是一个嵌入式关系数据库。"嵌入式"的意思是：它不是独立的服务端进程，而是以 C 语言库的形式直接链接到应用程序里。

Python 标准库自带 `sqlite3` 模块，不需要安装额外软件，导入即用。

## 1.2 与服务端数据库的区别

| | SQLite | PostgreSQL / MySQL |
|---|---|---|
| 架构 | 嵌入式 C 库，无服务端 | 独立服务进程 |
| 存储 | 单个 `.sqlite` 文件 | 多文件/数据目录 |
| 并发 | 文件级锁，写互斥 | 行级锁，多用户并发 |
| 数据类型 | 少（NULL/INTEGER/REAL/TEXT/BLOB） | 多（JSONB/ARRAY/空间类型等） |
| 安装 | 零安装 | 需要安装、配置、启动 |
| 适合 | 单应用、本地存储、轻量级 | 多用户、高并发、复杂查询 |

# 2. Python 标准库 sqlite3

## 2.1 连接数据库

```python
import sqlite3

conn = sqlite3.connect("data.db")  # 文件不存在会自动创建
```

内存模式（不写文件，关闭连接后数据消失）：

```python
conn = sqlite3.connect(":memory:")
```

## 2.2 建表

```python
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
```

`AUTOINCREMENT` 让 id 自动递增。`CURRENT_TIMESTAMP` 在插入时自动填入当前时间。

## 2.3 插入数据

```python
cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", ("标题", "内容"))
conn.commit()
```

问号 `?` 是占位符，不要直接拼字符串（SQL 注入风险）。

批量插入：

```python
data = [
    ("标题1", "内容1"),
    ("标题2", "内容2"),
]
cursor.executemany("INSERT INTO notes (title, content) VALUES (?, ?)", data)
conn.commit()
```

## 2.4 查询数据

```python
cursor.execute("SELECT id, title FROM notes")
rows = cursor.fetchall()  # 返回所有行，list of tuple
for row in rows:
    print(row[0], row[1])
```

按条件查询：

```python
cursor.execute("SELECT * FROM notes WHERE title = ?", "标题")
row = cursor.fetchone()  # 返回一行，没有则返回 None
```

## 2.5 参数化查询

`sqlite3` 使用 `?` 作为占位符：

```python
# 正确 — 参数化查询
cursor.execute("SELECT * FROM notes WHERE id = ?", (1,))

# 错误 — 字符串拼接，有 SQL 注入风险
cursor.execute(f"SELECT * FROM notes WHERE id = {user_input}")
```

多个参数：

```python
cursor.execute("SELECT * FROM notes WHERE title = ? AND content LIKE ?", ("标题", "%关键%"))
```

字典风格（具名参数）：

```python
cursor.execute("SELECT * FROM notes WHERE id = :id", {"id": 1})
```

## 2.6 事务

`sqlite3` 默认自动开启事务，`execute()` 后需要 `commit()` 才能持久化。

```python
conn = sqlite3.connect("data.db")
cursor.execute("INSERT INTO notes (title) VALUES ('草稿')")
conn.commit()  # 提交，数据写入文件
conn.close()
```

回滚：

```python
try:
    cursor.execute("INSERT INTO notes (title) VALUES ('A')")
    cursor.execute("INSERT INTO notes (title) VALUES (?, '标题重复会失败')")  # 假设失败
    conn.commit()
except Exception:
    conn.rollback()  # 撤销本次事务的所有操作
```

也可以用上下文管理器自动提交或回滚：

```python
with conn:  # 自动 commit（成功）或 rollback（异常）
    cursor.execute("INSERT INTO notes (title) VALUES ('auto commit')")
```

## 2.7 游标

`cursor` 是 SQL 操作的句柄，可以复用同一个连接上的多个 cursor。

```python
c1 = conn.cursor()
c2 = conn.cursor()

c1.execute("SELECT * FROM notes")
c2.execute("SELECT count(*) FROM notes")
```

`row_factory` 可以把结果从 tuple 变成字典风格：

```python
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM notes WHERE id = 1")
row = cursor.fetchone()
print(row["title"])  # 按列名取，不是 row[1]
```

## 2.8 `check_same_thread`

`sqlite3` 默认只允许创建连接的线程使用它。跨线程使用会抛 `ProgrammingError`。

```python
# 默认：只能创建 conn 的线程使用
conn = sqlite3.connect("data.db")

# 允许多线程（需要自行处理并发安全）
conn = sqlite3.connect("data.db", check_same_thread=False)
```

LangGraph 的 `SqliteSaver` 内部用锁处理并发，所以需要设为 `False`。

# 3. 存储结构

## 3.1 单文件

整个数据库（表、索引、数据）都存储在单个文件中。拷走这个文件就等同于备份了整个数据库。

```bash
# 查看文件内有哪些表
sqlite3 data.db ".tables"

# 查看表结构
sqlite3 data.db ".schema notes"
```

## 3.2 页组织

SQLite 内部按固定大小（默认 4KB）分页存储：

```
页1: 文件头 + sqlite_master（表结构元数据）
页2+: 数据页、索引页、溢出页
```

用户不需要手动管理页，但理解分页有助于理解"为什么 SQLite 不适合大文件"。

# 4. 常用场景

## 4.1 适合

- 本地配置、缓存、日志
- 开发调试时的临时数据库
- 桌面/移动应用的内嵌数据库
- 单用户、低并发的 Web 应用
- LangGraph 的 checkpoint 存储

## 4.2 不适合

- 多用户同时写入（写互斥）
- 高并发读（虽然有 read-ahead 缓存，但不如 Postgres 的连接池）
- 大数据量（> 100GB 的文件性能下降明显）
- 需要复杂查询（JSONB、全文索引、空间查询等）

# 5. LangGraph 中的 SqliteSaver

## 5.1 接入方式

```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

conn = sqlite3.connect("data/memory.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

graph = builder.compile(checkpointer=memory)
```

之后所有 `graph.invoke()` 调用自动存档到 SQLite。

## 5.2 内部表

LangGraph 在 SQLite 中创建以下表：

| 表名 | 作用 |
|------|------|
| `checkpoints` | checkpoint 元数据（thread_id、checkpoint_id、parent_id） |
| `checkpoint_blobs` | 大字段存储（序列化的 state 快照） |
| `checkpoint_writes` | 中间写入记录（用于中断恢复、并行写入） |

可以用 `sqlite3` 命令行直接查看：

```bash
sqlite3 data/memory.sqlite ".tables"
sqlite3 data/memory.sqlite "SELECT thread_id, checkpoint_id FROM checkpoints;"
```
