# PostgreSQL

## 1. psql 命令行客户端

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

在 Docker 容器中执行 psql：

```bash
# 方式1：直接在容器外执行（用完即走）
docker exec <容器名> psql -U <用户> -d <数据库> -c "<SQL命令>"

# 方式2：进入容器内部交互式操作
docker exec -it <容器名> bash     # 先进入容器
psql -U fastapi_user -d fastapi_study   # 在容器里连数据库
```

### 1.1 psql 中的两类命令

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

## 2. 层级结构

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

## 3. 用户与角色

PostgreSQL 中没有独立的"账号"概念，统一叫**角色（Role）**：

```sql
CREATE ROLE myrole;                            -- 不能登录，纯角色（用于权限分组）
CREATE USER myuser WITH PASSWORD '123';        -- 能登录的用户（= CREATE ROLE ... WITH LOGIN）
```

### 3.1 角色属性

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

常用操作：

```sql
-- 创建用户
CREATE USER fastapi_user WITH PASSWORD 'fastapi_pass_123';

-- 修改密码
ALTER USER fastapi_user PASSWORD 'new_password';

-- 删除用户
DROP USER fastapi_user;
```

### 3.2 权限级别

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

## 4. 认证机制（pg_hba.conf）

为什么 `docker exec` 进容器后 `psql -U txwx` 不需要密码，但 VS Code 从外部连 `localhost:5433` 必须密码？

### 4.1 两种连接路径

```
Windows 宿主机
  │
  ├── VS Code 插件 → localhost:5433 (TCP)  → 必须密码
  │
  └── docker exec → 容器内 → Unix socket   → 免密码（本地信任）
```

### 4.2 pg_hba.conf

PostgreSQL 的认证策略由 `pg_hba.conf` 文件控制，每行一条规则：

```
# TYPE   DATABASE    USER       ADDRESS          METHOD
host     all         all        127.0.0.1/32     scram-sha-256    ← TCP 连接要密码
local    all         all                         trust            ← Unix socket 免密码
```

- `host` = TCP 连接（外部），通过 `METHOD` 指定的方式认证（如 `scram-sha-256` 密码验证）
- `local` = Unix socket 连接（本机），`trust` 表示信任，直接放行
- `METHOD` 可选值：`trust`（免密）、`password`（明文密码）、`scram-sha-256`（加密密码）、`peer`（匹配 OS 用户名）

Docker 容器内 `psql` 走的是 Unix socket → `trust`，所以免密码。
容器外连 `localhost:5433` 走的是 TCP → 需要密码。

### 4.3 总结

| | 认证方式 | 需要密码？ | 能做啥？ |
|----|---------|-----------|---------|
| 容器内 docker exec | Unix socket (trust) | 不需要 | 看角色属性（SUPERUSER 等） |
| 容器外 TCP 连接 | scram-sha-256 | 需要 | 看角色属性 |

能连上 ≠ 能干所有事，具体权限取决于角色属性。

## 5. 数据库操作

```sql
-- 创建数据库，指定拥有者
CREATE DATABASE fastapi_study OWNER fastapi_user;

-- 删除数据库（需断开其他连接）
DROP DATABASE fastapi_study;
```

只有超级用户或数据库拥有者才能删除数据库。

## 6. 从 Docker 容器访问

```bash
# 查看容器
docker ps

# 在容器中执行 psql
docker exec txwx-postgis psql -U fastapi_user -d fastapi_study -c "\dt"

# 进入容器交互式操作
docker exec -it txwx-postgis psql -U fastapi_user -d fastapi_study
```
