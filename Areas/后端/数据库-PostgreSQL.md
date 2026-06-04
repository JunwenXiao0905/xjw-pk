# PostgreSQL

## 目录

- [第1章 连接与客户端](#第1章-连接与客户端)
  - [1.1 psql 命令行客户端](#11-psql-命令行客户端)
  - [1.2 psql 中的两类命令](#12-psql-中的两类命令)
  - [1.3 从 Docker 容器访问](#13-从-docker-容器访问)
- [第2章 数据库结构](#第2章-数据库结构)
  - [2.1 层级结构](#21-层级结构)
  - [2.2 数据库操作](#22-数据库操作)
- [第3章 用户、角色与权限](#第3章-用户角色与权限)
  - [3.1 用户与角色](#31-用户与角色)
  - [3.2 角色属性](#32-角色属性)
  - [3.3 权限级别](#33-权限级别)
  - [3.4 认证机制（pg_hba.conf）](#34-认证机制pg_hbaconf)
- [第4章 数据类型与表结构](#第4章-数据类型与表结构)
  - [4.1 常用数据类型](#41-常用数据类型)
  - [4.2 查看表结构](#42-查看表结构)
  - [4.3 约束](#43-约束)
  - [4.4 自增主键与 Sequence](#44-自增主键与-sequence)
- [第5章 SQL 增删改查](#第5章-sql-增删改查)
  - [5.1 INSERT 插入](#51-insert-插入)
  - [5.2 SELECT 查询](#52-select-查询)
  - [5.3 UPDATE 修改](#53-update-修改)
  - [5.4 DELETE 删除](#54-delete-删除)
  - [5.5 WHERE 缺失的致命坑](#55-where-缺失的致命坑)
  - [5.6 SQL 子句执行顺序](#56-sql-子句执行顺序)
  - [5.7 chain-to-SQL：SQLAlchemy 对照](#57-chain-to-sqlsqlalchemy-对照)
- [第6章 删除策略](#第6章-删除策略)
  - [6.1 硬删除与软删除](#61-硬删除与软删除)
  - [6.2 软删除的取舍](#62-软删除的取舍)
  - [6.3 两阶段软删除（回收站 + 定时清理）](#63-两阶段软删除回收站--定时清理)
- [第7章 多表连接（JOIN）](#第7章-多表连接join)
  - [7.1 为什么需要 JOIN](#71-为什么需要-join)
  - [7.2 基本语法与列前缀](#72-基本语法与列前缀)
  - [7.3 JOIN 的四种类型](#73-join-的四种类型)
  - [7.4 左表与右表](#74-左表与右表)
  - [7.5 裸表名陷阱](#75-裸表名陷阱)
  - [7.6 对照 SQLAlchemy relationship](#76-对照-sqlalchemy-relationship)

## 第1章 连接与客户端

### 1.1 psql 命令行客户端

`psql` 是 PostgreSQL 自带的命令行客户端，连接参数：

| 参数 | 含义 | 示例 |
|------|------|------|
| `-U` | 用户名 | `psql -U postgres` |
| `-d` | 数据库名 | `psql -d mydb` |
| `-h` | 主机地址 | `psql -h localhost` |
| `-p` | 端口号 | `psql -p 5433` |
| `-c` | 执行一条命令后退出 | `psql -c "SELECT 1;"` |

一条完整的连接命令：

```bash
psql -U fastapi_user -d fastapi_study -h localhost -p 5433
```

连接后提示符变化反映输入状态：

```
fastapi_study=>     等待新命令
fastapi_study->     语句未结束（换行但未敲分号），等待续行
fastapi_study">     字符串引号未闭合，等待补引号
```

### 1.2 psql 中的两类命令

psql 里输入的内容分为两类：

| 类型 | 前缀 | 分号 | 示例 |
|------|------|------|------|
| SQL 语句 | 无 | **需要** `;` | `SELECT * FROM users;` |
| psql 反斜杠命令 | `\` | **不需要** | `\dt` |

常见反斜杠命令：

| 命令 | 含义 |
|------|------|
| `\l` | 列出所有数据库 |
| `\du` | 列出所有用户（角色） |
| `\c dbname` | 切换到另一个数据库 |
| `\dt` | 列出当前库的所有表 |
| `\d 表名` | 查看表结构（列名、类型、约束） |
| `\di` | 列出所有索引 |
| `\q` | 退出 psql |

### 1.3 从 Docker 容器访问

```bash
# 查看容器
docker ps

# 方式1：容器外执行一条命令（用完即走）
docker exec txwx-postgis psql -U fastapi_user -d fastapi_study -c "\dt"

# 方式2：进入容器交互式操作
docker exec -it txwx-postgis psql -U fastapi_user -d fastapi_study
```

## 第2章 数据库结构

### 2.1 层级结构

一个 PostgreSQL 实例从上到下：

```
PostgreSQL 实例（一个 pg 进程/容器）
  ├── 数据库 fastapi_study          ← 独立命名空间，库之间完全隔离
  │   ├── Schema public              ← 默认 schema，表都放这
  │   │   ├── 表 users               ← 存用户数据
  │   │   │   ├── 列 id, username ...
  │   │   │   └── 行 (1, 'study_user', ...)
  │   │   └── 表 notes
  │   └── Schema 可再建多个 ...
  ├── 数据库 postgres                ← 系统库，存储全局元数据，不要动
  └── 数据库 txwx_db                 ← 其他项目的库
```

关键点：
- **一个 pg 实例**可挂 N 个**数据库**，互不干扰
- **一个数据库**内可有 N 个 **Schema**（默认 `public`），用于逻辑分组
- **一个 Schema** 下有 N 张**表**
- **一张表**有 N 列（字段）、N 行（数据）

### 2.2 数据库操作

```sql
-- 创建数据库，指定拥有者
CREATE DATABASE fastapi_study OWNER fastapi_user;

-- 删除数据库（需断开其他连接）
DROP DATABASE fastapi_study;
```

只有超级用户或数据库拥有者才能删除数据库。

## 第3章 用户、角色与权限

### 3.1 用户与角色

PostgreSQL 中没有独立的"账号"概念，统一叫**角色（Role）**：

```sql
CREATE ROLE myrole;                            -- 不能登录，纯角色（用于权限分组）
CREATE USER myuser WITH PASSWORD '123';        -- 能登录的用户（= CREATE ROLE ... WITH LOGIN）
```

常用操作：

```sql
-- 创建用户
CREATE USER fastapi_user WITH PASSWORD 'fastapi_pass_123';

-- 修改密码
ALTER USER fastapi_user PASSWORD 'new_password';

-- 删除用户
DROP USER fastapi_user;
```

### 3.2 角色属性

创建角色时可赋予不同属性。例如 PostGIS 镜像默认创建的 `txwx` 用户：

```sql
-- txwx 具有 SUPERUSER 属性，所以能创建新用户、新数据库
CREATE ROLE txwx WITH
    LOGIN           -- 能登录
    PASSWORD 'txms9999'
    SUPERUSER;      -- 超级管理员，无视所有权限检查
```

| 属性 | 含义 |
|------|------|
| `LOGIN` | 能登录（有 LOGIN = 用户，没有 = 纯角色） |
| `SUPERUSER` | 超级用户，无视所有权限检查 |
| `CREATEDB` | 能新建数据库 |
| `CREATEROLE` | 能新建/删除角色 |
| `REPLICATION` | 能做主从复制 |

### 3.3 权限级别

权限可以精确控制到不同层级：

| 层级 | 常见权限 | 例子 |
|------|---------|------|
| 实例级 | LOGIN、CREATEDB、SUPERUSER | 创建角色时决定 |
| 数据库级 | CONNECT、CREATE、TEMP | 谁能连这个库 |
| Schema 级 | USAGE、CREATE | 谁能在这个 schema 下建表 |
| 表级 | SELECT、INSERT、UPDATE、DELETE | 谁能查/增/改/删 |
| 列级 | SELECT、INSERT、UPDATE（按列） | 敏感列只读（极少用） |
| 行级 | RLS（Row-Level Security） | 比如 user A 只能看到自己的 note |

最常用的表级权限：

```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON notes TO fastapi_user;
REVOKE DELETE ON notes FROM fastapi_user;   -- 收回某个权限
```

当数据库是用 `OWNER fastapi_user` 创建时，该用户自动拥有该库全部权限，无需逐表 GRANT。

### 3.4 认证机制（pg_hba.conf）

为什么 `docker exec` 进容器后 `psql -U txwx` 不需要密码，但 VS Code 从外部连 `localhost:5433` 必须密码？

两种连接路径：

```
Windows 宿主机
  │
  ├── VS Code 插件 → localhost:5433 (TCP)  → 必须密码
  │
  └── docker exec → 容器内 → Unix socket   → 免密码（本地信任）
```

PostgreSQL 的认证策略由 `pg_hba.conf` 文件控制，每行一条规则：

```
# TYPE   DATABASE    USER       ADDRESS          METHOD
host     all         all        127.0.0.1/32     scram-sha-256    ← TCP 连接要密码
local    all         all                         trust            ← Unix socket 免密码
```

- `host` = TCP 连接（外部），通过 `METHOD` 指定的方式认证（如 `scram-sha-256` 密码验证）
- `local` = Unix socket 连接（本机），`trust` 表示信任，直接放行
- `METHOD` 可选值：`trust`（免密）、`password`（明文密码）、`scram-sha-256`（加密密码）、`peer`（匹配 OS 用户名）

Docker 容器内 `psql` 走 Unix socket → `trust` 免密码；容器外连 `localhost:5433` 走 TCP → 需要密码。

| | 认证方式 | 需要密码？ |
|----|---------|-----------|
| 容器内 docker exec | Unix socket (trust) | 不需要 |
| 容器外 TCP 连接 | scram-sha-256 | 需要 |

能连上 ≠ 能干所有事，具体权限取决于角色属性。

## 第4章 数据类型与表结构

### 4.1 常用数据类型

| PostgreSQL 类型 | 含义 | 对应 SQLAlchemy |
|------|------|----------------|
| `integer` | 32 位整数 | `Integer` |
| `character varying(n)` / `varchar(n)` | 变长字符串，最多 n 字符，超长报错 | `String(n)` |
| `text` | 变长字符串，无长度限制 | `Text` |
| `boolean` | 真/假（psql 显示为 `t`/`f`） | `Boolean` |

`varchar(n)` vs `text`：PostgreSQL 中两者**性能相同**，区别只是 `varchar` 多了长度校验。
有明确上限的字段（用户名、标题）用 `varchar(n)`，长度不定的内容（正文）用 `text`。

### 4.2 查看表结构

```sql
-- psql 反斜杠命令（仅 psql 可用）
\d notes

-- 标准 SQL（任何客户端可用）
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'notes'
ORDER BY ordinal_position;
```

`\d notes` 输出示例：

```
 Column  |          Type          | Nullable |              Default
---------+------------------------+----------+-----------------------------------
 id      | integer                | not null | nextval('notes_id_seq'::regclass)
 title   | character varying(100) | not null |
 content | text                   | not null |
 done    | boolean                | not null |
 user_id | integer                | not null |
Indexes:
    "notes_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "notes_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
```

### 4.3 约束

| 约束 | 含义 | 违反时 |
|------|------|--------|
| `NOT NULL` | 该列必须有值 | 插入 NULL 报错 |
| `PRIMARY KEY` | 主键，唯一且非空，自带 btree 索引 | 重复主键报错 |
| `UNIQUE` | 该列值不可重复（如 `username`） | 插入重复值报错 |
| `FOREIGN KEY` | 引用完整性，值必须在被引用表中存在 | 引用不存在的值报错 |

外键约束示例：`notes.user_id` 必须是 `users.id` 中真实存在的值。
插入 `user_id=999`（users 中无此 id）会报错：

```
ERROR:  insert or update on table "notes" violates foreign key constraint "notes_user_id_fkey"
DETAIL:  Key (user_id)=(999) is not present in table "users".
```

这防止了"孤儿数据"（笔记挂在不存在的用户身上）。

### 4.4 自增主键与 Sequence

PostgreSQL 无 MySQL 的 `AUTO_INCREMENT`，自增靠 **Sequence（序列）** 实现：

- 建表时自动创建序列对象 `notes_id_seq`
- `id` 列默认值 = `nextval('notes_id_seq')`，每次插入取序列下一个值

**关键特性：序列只增不回退**。失败/回滚的事务也会消耗序列值，所以自增 id 可能跳号
（如插入失败后下一条 id 从 2 跳到 3），**不保证连续，只保证唯一递增**。

## 第5章 SQL 增删改查

`INSERT`/`SELECT`/`UPDATE`/`DELETE` 是 SQL 关键字（DML，数据操作语言），不是函数。

### 5.1 INSERT 插入

```sql
INSERT INTO notes (title, content, done, user_id)
VALUES ('测试', '内容', false, 1);
-- 返回 INSERT 0 1：第一个数是 OID（已废弃，恒为 0），第二个是影响行数
```

语法结构：`INSERT INTO 表名 (列名列表) VALUES (值列表)`，值的顺序与列名一一对应。

字符串值用**单引号** `'...'`；双引号 `"..."` 用于标识符（表名/列名），不可混用。

列名可不写全，未写的列需满足之一，否则报错：
- 有默认值（如 `id` 的 nextval）→ 自动填默认值
- 允许 NULL → 自动填 NULL
- `NOT NULL` 且无默认值 → 必须提供

### 5.2 SELECT 查询

```sql
SELECT id, title, done          -- 要哪几列（* 表示全部）
FROM notes                      -- 从哪张表
WHERE done = false              -- 过滤行
ORDER BY id DESC;               -- 排序
```

排序方向：`ASC` 升序（默认，从小到大）、`DESC` 降序（从大到小）。
**不写 `ORDER BY` 时返回行顺序不确定**，不可依赖默认顺序。

### 5.3 UPDATE 修改

```sql
UPDATE notes SET done = true WHERE id = 1;
-- 返回 UPDATE 1（影响 1 行）；UPDATE 0 表示 WHERE 未匹配任何行
```

### 5.4 DELETE 删除

```sql
DELETE FROM notes WHERE id = 5;
-- 返回 DELETE 1
```

### 5.5 WHERE 缺失的致命坑

`UPDATE` / `DELETE` 缺少 `WHERE` 会作用于**整张表所有行**：

```sql
UPDATE notes SET done = true;   -- 改光全表
DELETE FROM notes;              -- 删光全表
```

`WHERE` 决定操作哪些行，漏写即全表操作。

### 5.6 SQL 子句执行顺序

书写顺序是 `SELECT → FROM → WHERE → ORDER BY`，但数据库**实际执行顺序**不同：

```
1. FROM       确定数据源
2. WHERE      过滤行
3. SELECT     挑选列
4. ORDER BY   排序结果
```

这解释了为什么 `WHERE` 中不能用 `SELECT` 起的列别名——WHERE 先执行，别名此时尚不存在。

### 5.7 chain-to-SQL：SQLAlchemy 对照

```python
select(Note)                     # SELECT ... FROM notes
    .where(Note.done == False)   # WHERE done = false
    .order_by(Note.id.desc())    # ORDER BY id DESC
    .offset(skip)                # OFFSET
    .limit(limit)                # LIMIT
```

ORM 的 UPDATE 走"先查后改"：

```python
note = self._get_owned(note_id, user_id)  # 先 SELECT 查出对象
note.done = True                           # 改属性
self.db.flush()                            # flush 时 ORM 对比变更，生成 UPDATE ... WHERE id=主键
```

代价是多一次 SELECT，换来改前的权限校验、关系级联与事件钩子。
WHERE 由 ORM 用主键自动生成，无需手写。

## 第6章 删除策略

### 6.1 硬删除与软删除

```sql
-- 硬删除：数据从表里真的消失，不可恢复
DELETE FROM notes WHERE id = 5;

-- 软删除：加标记列，数据仍在，只标记为"已删除"
UPDATE notes SET deleted_at = now() WHERE id = 5;
```

软删除的标记列两种常见形式：

```sql
is_deleted boolean NOT NULL DEFAULT false   -- 布尔标记
deleted_at timestamp DEFAULT NULL           -- 时间戳：NULL=未删，有值=已删（更常用，能知何时删）
```

软删除后所有业务查询必须过滤已删行：

```sql
SELECT * FROM notes WHERE deleted_at IS NULL;
```

### 6.2 软删除的取舍

| 优点 | 缺点 |
|------|------|
| 可恢复（误删能找回） | 表持续增大，需定期归档/清理 |
| 留痕，满足审计/分析 | 每个查询都得加过滤条件，漏写会查出已删数据 |
| 保护引用完整性（别表引用了该行） | 唯一约束冲突：软删的 `username` 与新注册同名撞 UNIQUE |
| 支持回收站功能 | |

适用场景：重要业务数据（订单、用户、交易）几乎都用软删除；临时/日志类数据用硬删除即可。

避免每个查询手写过滤条件：ORM 层用事件钩子或 query 过滤器统一注入 `WHERE deleted_at IS NULL`。

### 6.3 两阶段软删除（回收站 + 定时清理）

中大型系统的标准做法：用状态机把"对用户不可见"与"释放存储"解耦。

字段：

| 字段 | 作用 |
|------|------|
| `delete_status` | 数据所处阶段：`0` 正常 / `1` 回收站 / `2` 逻辑已删 |
| `delete_scheduled_at` | **计划**执行下一步清理的时间 |

状态流转：

```
0 正常
  ↓ 用户删除（进回收站，delete_scheduled_at = now() + 30天）
1 回收站  ──用户恢复──→  0 正常
  ↓ 定时任务（cron）扫描，scheduled_at 到期
2 逻辑删除（用户彻底不可见）
  ↓ 物理清理任务（更晚，连带清理 MinIO 文件、Redis 缓存等）
真正 DELETE / 归档
```

定时任务的清理查询：

```sql
UPDATE items
SET delete_status = 2
WHERE delete_status = 1
  AND delete_scheduled_at <= now();   -- 计划时间已过
```

**设计要点：用"计划时间"统一普通删除与立即删除。**

```
普通删除：scheduled_at = now() + 30天   → 回收站保留 30 天
立即删除：scheduled_at = 过往时间        → 已"过期"，下一轮扫描立即清理
```

立即删除只需把 `scheduled_at` 设为过往时间，复用同一套定时清理逻辑，无需单独的删除代码路径。

**为什么要 status=2 中间态而非直接物理 DELETE：**

| 原因 | 说明 |
|------|------|
| 解耦 | "不可见"与"释放存储"是两件事，可不同节奏执行 |
| 性能 | 物理删大量数据慢且锁表；标记 status=2 很快，物理清理放低峰期批量做 |
| 审计窗口 | status=2 后仍可保留一段时间供审计/法务 |
| 级联处理 | 一行删除常需连带清理关联文件（MinIO）、缓存（Redis）、搜索索引，需异步缓冲 |

查询约定：正常业务查 `WHERE delete_status = 0`；回收站列表查 `WHERE delete_status = 1`。

## 第7章 多表连接（JOIN）

JOIN 直译"连接"，表示按 `ON` 条件把多张表的行拼成一行。

### 7.1 为什么需要 JOIN

`notes` 表只存 `user_id`（数字），不存用户名。要在查笔记时同时显示作者名，需把两表按外键拼接：

```
notes.user_id  ──匹配──→  users.id
```

### 7.2 基本语法与列前缀

```sql
SELECT notes.id, notes.title, users.username
FROM notes
JOIN users ON notes.user_id = users.id;
```

- `FROM notes` 主表，`JOIN users` 要连接的表
- `ON notes.user_id = users.id` 连接条件：哪两列相等才算匹配
- 多表查询列名要加 `表名.列名` 前缀

列前缀规则：
- 两表有同名列（如都有 `id`）时**必须**加前缀，否则报错 `column reference "id" is ambiguous`
- 不冲突的列可省前缀，但实际开发统一全加，便于看出列归属、避免日后加同名列报错

### 7.3 JOIN 的四种类型

| 类型 | 中文 | 保留哪边 |
|------|------|---------|
| `INNER JOIN` | 内连接（`JOIN` 默认即此） | 只保留两边都匹配的行 |
| `LEFT JOIN` | 左连接（= `LEFT OUTER JOIN`） | 左表全部，右表无匹配填 NULL |
| `RIGHT JOIN` | 右连接 | 右表全部，左表无匹配填 NULL |
| `FULL JOIN` | 全连接 | 两边全保留，缺的填 NULL |

`INNER`（内）= 两表交集；`OUTER`（外）= 保留某边全部，含未匹配行。

INNER vs LEFT 实测（`empty_user` 无任何笔记）：

```sql
-- INNER JOIN：empty_user 不出现（无匹配笔记）
SELECT users.username, notes.title
FROM users JOIN notes ON users.id = notes.user_id;
-- study_user | 测试 / study_user | 测试文章

-- LEFT JOIN：empty_user 出现，title 为 NULL
SELECT users.username, notes.title
FROM users LEFT JOIN notes ON users.id = notes.user_id;
-- study_user | 测试 / study_user | 测试文章 / empty_user | (NULL)
```

未匹配处填的是 `NULL`（无值），不是空字符串 `''`。判断用 `IS NULL`，不能用 `= NULL`：

```sql
SELECT users.username FROM users
LEFT JOIN notes ON users.id = notes.user_id
WHERE notes.title IS NULL;   -- 查出没有笔记的用户
```

### 7.4 左表与右表

```
FROM A LEFT JOIN B
     ↑           ↑
     左表        右表
```

- `FROM` 后面的表 = 左表，`JOIN` 后面的表 = 右表
- `LEFT JOIN` 保左表全部，`RIGHT JOIN` 保右表全部

`A LEFT JOIN B` 与 `B RIGHT JOIN A` 结果完全相同。实际开发统一用 LEFT，把要保全的表写在前面，避免用 RIGHT 绕脑子。

### 7.5 裸表名陷阱

PostgreSQL 中 `SELECT 表名`（不带 `.列名`）会把整行打包成一个复合值：

```sql
SELECT notes FROM notes;
-- 输出一列：(3,测试,内容,f,1)   ← 整行字段拼成复合值
```

与 `SELECT * FROM notes`（所有列展开）不同。JOIN 时误写裸表名会让整行数据挤进一列，记得始终写 `表名.列名`。

### 7.6 对照 SQLAlchemy relationship

ORM 的 `relationship` 是 JOIN 的封装：

```python
# model.py
notes: Mapped[list["Note"]] = relationship(back_populates="user")
# 访问 user.notes 时，SQLAlchemy 自动生成 JOIN 或子查询拉取关联行
```
