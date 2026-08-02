# PostgreSQL

## 目录

- [第0章 前置基础](#第0章-前置基础)
  - [0.1 先搞清:数据库到底解决了什么](#01-先搞清数据库到底解决了什么)
  - [0.2 关系型数据库:表、关系与 SQL](#02-关系型数据库表关系与-sql)
  - [0.3 对象关系型:PostgreSQL 多了什么](#03-对象关系型postgresql-多了什么)
  - [0.4 PostgreSQL vs MySQL:核心差异](#04-postgresql-vs-mysql核心差异)
  - [0.5 生产选型:国内为何多用 MySQL](#05-生产选型国内为何多用-mysql)
  - [0.6 PostgreSQL 的生态:扩展、PostGIS、pgvector](#06-postgresql-的生态扩展postgispgvector)
  - [0.7 参考来源](#07-参考来源)
- [第1章 安装与连接](#第1章-安装与连接)
  - [1.1 用 Docker 安装 PostgreSQL](#11-用-docker-安装-postgresql)
  - [1.2 连接五要素:服务端与客户端](#12-连接五要素服务端与客户端)
  - [1.3 pgAdmin:官方图形工具](#13-pgadmin官方图形工具)
  - [1.4 VS Code 数据库插件](#14-vs-code-数据库插件)
  - [1.5 图形 vs 命令行(psql)](#15-图形-vs-命令行psql)
  - [1.6 PG 客户端工具家族](#16-pg-客户端工具家族)
  - [1.7 参考来源](#17-参考来源)
- [第2章 数据库结构](#第2章-数据库结构)
  - [2.1 层级结构](#21-层级结构)
  - [2.2 Schema 详解](#22-schema-详解)
  - [2.3 Schema 划分实践](#23-schema-划分实践)
  - [2.4 数据库操作](#24-数据库操作)
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
  - [4.5 标识符与大小写](#45-标识符与大小写)
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
- [第8章 PostGIS 专题（空间数据库）](#第8章-postgis-专题空间数据库)
  - [8.1 安装与启用](#81-安装与启用)
  - [8.2 geometry 类型与 WKT](#82-geometry-类型与-wkt)
  - [8.3 SRID 与 geometry vs geography](#83-srid-与-geometry-vs-geography)
  - [8.4 ST_ 函数家族](#84-st_-函数家族)
  - [8.5 空间索引 GiST](#85-空间索引-gist)
  - [8.6 实战查询](#86-实战查询)
  - [8.7 栅格与数据导入](#87-栅格与数据导入)
  - [8.8 面试要点速记](#88-面试要点速记)
  - [8.9 参考来源](#89-参考来源)

## 第0章 前置基础

> 本章不讲操作,先建立整体认知:**PostgreSQL 到底是什么?它和 MySQL 有什么区别?为什么国内生产多用 MySQL、而全球却在转向 PostgreSQL?** 搞懂这些,第1章起的实操才有根基。

### 0.1 先搞清:数据库到底解决了什么

最直观的对比:你平时存数据用 **Excel**,那为什么还需要"数据库"?

| 痛点 | Excel | 数据库 |
|------|-------|--------|
| 多人同时改 | 互相覆盖、锁文件冲突 | **事务** + 多版本并发,互不干扰 |
| 断电 | 可能丢数据、文件损坏 | 提交即落盘,崩溃也不丢 |
| 数据量 | 百万行就卡 | 几十亿行照查 |
| 防脏数据 | 填啥收啥 | 主键 / 外键 / 约束,乱填直接拒 |
| 安全权限 | 能开文件就能全看 | 谁能看 / 改,精细到列 |

一句话:**数据库 = 一个专为"多人同时、可靠、大规模、守规矩"地存取数据而生的后台服务程序。** 留意"**后台服务程序**"几个字——这正是第1章"为什么不能像 Word 那样双击文件打开"的伏笔。

### 0.2 关系型数据库:表、关系与 SQL

**关系(relation)= 表。** PostgreSQL 官方原话:"relation 本质上是个数学术语,指的就是『表』"[1]。一张表 = 一组**行(rows)**,每行有同样的**列(columns)**,每列有固定类型。

- **主键**:唯一标识一行的列,既唯一又非空(关系理论要求每张表都有主键)[2]。
- **外键**:某列的值必须匹配另一张表里出现的值,维护两张表的**引用完整性**[3]。这就是"关系"——表与表之间的引用关联(如 `订单.user_id → 用户.id`)。

> 💡 **"关系型"一词的由来**:1970 年 IBM 数学家 **E.F. Codd** 发表论文提出关系模型(后获图灵奖)。他说的"关系"在数学里就是"表",所以"关系型"本意是"用表组织数据的模型";日常理解成"表之间用外键互相关联"也对[4]。

**SQL** 是操作关系型数据库的标准语言(IBM 的 Chamberlin 与 Boyce 在 System R 项目中发明)。最新标准是 **SQL:2023**;PostgreSQL 在其 177 项强制特性中符合 170 项,以严格遵循标准著称[5]。

**事务与 ACID**:事务把多个操作绑成"要么全做、要么全不做"的整体。经典例子:转账 100 元 = ①你 −100 ②对方 +100,中途断电不会卡在"扣了钱却没到账"的中间态。四特性[6]:

| 字母    | 特性  | 含义                  |
| ----- | --- | ------------------- |
| **A** | 原子性 | 全做或全不做              |
| **C** | 一致性 | 从一个合法状态转到另一个(靠约束保证) |
| **I** | 隔离性 | 并发事务互不可见对方未提交的中间结果  |
| **D** | 持久性 | 提交即永久落盘,崩溃也不丢       |

### 0.3 对象关系型:PostgreSQL 多了什么

PostgreSQL 官方开篇第一句自称:**"PostgreSQL 是一个对象关系型数据库管理系统(ORDBMS)"**[7];MySQL 是**纯关系型**。多出的"对象"指**面向对象式的扩展能力**,官方列出用户可自行添加:自定义数据类型、复合类型、函数、操作符、索引方法、过程语言[7]。举两个最直观的:

- **表继承**:`CREATE TABLE 省会 INHERITS (城市)`——子表继承父表所有列,直接对应 OOP 的"继承"[8]。
- **自定义类型 + 操作符重载**:像定义"类",同一个 `+` 能按参数类型调不同实现。

一句话:**关系型是地基,对象关系型在地基上允许你像写面向对象程序一样扩展数据库。** MySQL 不提供这类能力。

### 0.4 PostgreSQL vs MySQL:核心差异

| 维度       | PostgreSQL                         | MySQL                                 |
| -------- | ---------------------------------- | ------------------------------------- |
| 归属       | 全球开源社区 PGDG(无单一公司控制)               | Oracle 公司(经 Sun,2010 年被 Oracle 收购)[9] |
| 定位       | 对象关系型(ORDBMS)                      | 纯关系型(RDBMS)                           |
| 存储引擎     | 单一(统一堆表)                           | **插件式**:InnoDB / MyISAM 等可按表切换[10]    |
| SQL 标准遵循 | 严格(170 / 177)                      | 有部分与标准的已知差异                           |
| 数据类型     | 极丰富:JSONB、数组、范围、网络地址、几何…           | 较精简(也有 JSON、ENUM)                     |
| 并发控制     | MVCC:读不阻塞写                         | MVCC(InnoDB 引擎层实现)[11]                |
| 索引类型     | B-tree / GiST / GIN / BRIN…,擅长复杂查询 | 以 B-tree 为主(+ 全文 / 空间)                |
| 扩展机制     | `CREATE EXTENSION` 是核心优势           | 插件机制(如可插拔存储引擎)                        |
| 擅长场景     | 复杂查询、复杂类型、强一致性、可扩展                 | 高并发简单事务、Web / OLTP、易部署                |

> 两者都是成熟的 ACID 开源数据库,**没有绝对优劣**,选型看具体工作负载。

### 0.5 生产选型:国内为何多用 MySQL

**国内生产多用 MySQL 是"中国特色 + 历史惯性",不代表全球趋势。**

**国内为什么 MySQL 主导:**

- **去 IOE 运动**:2009 年起阿里"用 MySQL 替代 Oracle",奠定国内互联网"默认数据库"地位[12]。
- **云厂商主推**:阿里云 PolarDB(MySQL 兼容)国内市场份额 26%、六连冠;OceanBase、TDSQL、GaussDB 等"国产数据库"普遍兼容 MySQL 协议[13]。
- **运维 / 招聘生态成熟**:中文资料、DBA 人才、工具链都最齐全。

**全球却在转向 PostgreSQL(关键数据):**

- **Stack Overflow 2025 开发者调查**:PostgreSQL **55.6%** 登顶第一,MySQL 40.5% 居第二;PG 同时拿下"最常用 + 最受赞(65.5%)+ 最想用"三冠王[14]。
- **DB-Engines 2026 年 6 月榜**:Oracle ①、MySQL ②、PostgreSQL ④,但前 7 名里 **PG 是唯一还在涨**的关系库(+7.58 / 年),MySQL 在跌(−97 / 年);PG 已 5 次当选"年度数据库"[15]。
- **AI / 向量时代加持**:pgvector 让 PostgreSQL 直接做向量检索(见 0.6),进一步推高采用。

> 💡 **务实建议**:学 PostgreSQL 不吃亏(全球趋势 + AI 方向);同时了解 MySQL(国内存量与招聘短期仍以它为主)。两者都掌握最稳。

### 0.6 PostgreSQL 的生态:扩展、PostGIS、pgvector

PostgreSQL 最强的地方是**扩展(Extension)机制**——`CREATE EXTENSION` 一条命令装上一个"功能包"(新类型 / 函数 / 索引方法),`DROP EXTENSION` 一条命令干净卸载[16]。PGXN(扩展分发网络)直言:**"PostgreSQL 已不只是数据库,而是应用开发平台"**[17]。

| 扩展              | 一句话定位                                                         |
| --------------- | ------------------------------------------------------------- |
| **PostGIS**     | 给 PG 加地理空间能力,变成空间数据库(GIS、地图、LBS、空间查询)[18]                     |
| **pgvector**    | 向量类型 + 相似度搜索,让 PG 在 AI / RAG 时代直接做向量检索(GitHub ~22k stars)[19] |
| **TimescaleDB** | 专为时序数据优化(按时间自动分区)[20]                                         |
| **Citus**       | 把 PG 扩展成分布式集群(分片)[20]                                         |

关键点:**这些重磅能力全以"扩展"形式存在,而不是塞进数据库内核**——这正是 PostgreSQL 生态繁荣的根基,也是它能在 AI 时代持续上升的原因。

### 0.7 参考来源(均为官方 / 权威一手)

**PostgreSQL 官方文档** — postgresql.org/docs/current/
- [1][7] Concepts / What is PostgreSQL:tutorial-concepts.html、intro-whatis.html
- [2][3] Constraints(主键 / 外键):ddl-constraints.html
- [5] SQL Conformance(SQL:2023,170 / 177):features.html
- [6] Transactions / ACID:tutorial-transactions.html(ACID 术语出处:Härder & Reuter 1983)
- [8] Inheritance:tutorial-inherit.html
- [11] MVCC:mvcc-intro.html
- [16] CREATE EXTENSION:extend-extensions.html

**关系模型历史**
- [4] Codd 1970 原论文:dl.acm.org/doi/10.1145/362384.362685;IBM 官方史:ibm.com/history/relational-database

**MySQL 官方文档** — dev.mysql.com/doc/
- [10] 存储引擎 / 插件式架构:storage-engines.html、pluggable-storage-overview.html
- [9] MySQL 归属变迁:en.wikipedia.org/wiki/MySQL

**市场数据**
- [12] 去 IOE:阿里云开发者社区《真实的阿里巴巴去 IOE 故事》、钛媒体王坚访谈
- [13] IDC《2024H2 中国关系型数据库市场跟踪》、墨天轮中国数据库流行度榜
- [14] Stack Overflow Developer Survey 2025:survey.stackoverflow.co/2025/technology
- [15] DB-Engines 排名:db-engines.com/en/ranking

**扩展生态**
- [17] PGXN:pgxn.org/about
- [18] PostGIS:postgis.net
- [19] pgvector:github.com/pgvector/pgvector
- [20] TimescaleDB:timescale.com;Citus:citusdata.com

## 第1章 安装与连接

> 本章把 PostgreSQL 真正跑起来，并用图形工具（pgAdmin / VS Code 插件）和命令行（psql）连上去。先会"装 + 连"，后面所有操作才有落点。

### 1.1 用 Docker 安装 PostgreSQL

**为什么用 Docker**：隔离干净、删容器即彻底卸载、一键启停、可同时跑多个版本。Windows 上用 **Docker Desktop**（WSL2 后端）。

一条命令跑起 PostgreSQL 16（后台运行、数据持久化、开机自启）：

```powershell
docker run --name pg16 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=appdb -p 5432:5432 -v pgdata:/var/lib/postgresql/data -d --restart unless-stopped postgres:16
```

> PowerShell 多行续行用反引号(backtick,且必须是行末最后一个字符),不是 bash 的反斜杠;嫌麻烦就写成一行复制即用。

逐段解释：

| 片段                                   | 含义                                                |
| ------------------------------------ | ------------------------------------------------- |
| `--name pg16`                        | 容器名，方便引用                                          |
| `-e POSTGRES_PASSWORD=postgres`      | 超管密码（**必填**，不设启动报错）                               |
| `-e POSTGRES_USER=postgres`          | 超管用户名（省略默认 `postgres`）                            |
| `-e POSTGRES_DB=appdb`               | 首次启动自动建的默认库                                       |
| `-p 5432:5432`                       | 端口映射：宿主 5432 → 容器 5432（宿主端口被占就换，如 `-p 5433:5432`） |
| `-v pgdata:/var/lib/postgresql/data` | **数据持久化**：数据放进命名卷，否则删容器数据全没                       |
| `-d`                                 | 后台运行                                              |
| `--restart unless-stopped`           | 容器 / 开机自动重启                                       |
| `postgres:16`                        | 镜像：用具体大版本（别用 `latest`，避免哪天升级出意外）                  |

> ⚠️ **持久化是重点**：Docker 容器默认把数据写在临时层，**删容器 = 删数据**，所以必须挂 `-v`。[1]（PG18 起官方数据目录路径有变，PG16/17 挂 `/var/lib/postgresql/data` 即可。[2]）

验证：

```bash
docker ps                                        # 看到 pg16 在跑
docker logs pg16                                 # 出现 ready to accept connections 即成功
docker exec -it pg16 psql -U postgres -d appdb   # 进容器连库
```

> **国内拉镜像**：2024 年起大部分公开加速器（中科大、阿里云公共源等）已失效或受限。能直连就直连；不行就在 Docker Desktop → Settings → Docker Engine 里配 `registry-mirrors`，地址**以实测当时可用为准**，别照抄网上旧教程。[3]

### 1.2 连接五要素：服务端与客户端

数据库是**后台服务**（上面 docker 里的进程），你要用**客户端**通过网络连它。任何客户端连 PostgreSQL 都填这五个字段（官方叫 libpq 连接参数）：[4]

| 要素       | 含义    | 本例的值            |
| -------- | ----- | --------------- |
| host     | 服务器地址 | `localhost`（本机） |
| port     | 端口    | `5432`          |
| database | 连哪个库  | `appdb`         |
| user     | 用户名   | `postgres`      |
| password | 密码    | `postgres`      |

> 这五个字段就是下面 pgAdmin、VS Code 插件连接时要填的东西。记住它，所有 GUI 连接界面都围绕这五项。

### 1.3 pgAdmin：官方图形工具

> 一句话：所有 GUI 工具本质都在帮你生成并执行 SQL（点按钮、填表单，背后仍是 SQL），所以学 SQL 才是根本。

**pgAdmin** 是 PostgreSQL 最流行的官方开源图形管理工具。[5] 新手用**桌面版**：去 [pgadmin.org/download](https://www.pgadmin.org/download/) 下 Windows 安装包，一路下一步装好。

连接四步：

1. 打开 pgAdmin → 顶部 **Add New Server**（或右键 Servers → Register → Server）
2. **General** 选项卡：填个名字（如 `本机PG16`）
3. **Connection** 选项卡：填**连接五要素**（Host `localhost`、Port `5432`、Maintenance database `appdb`、Username `postgres`、Password `postgres`）→ 勾 Save password
4. Save → 左侧树展开就能看到数据库、表

常用操作：右键表 → **View/Edit Data** 看数据；**Tools → Query Tool** 写 SQL（按 F5 或点 ▶ 执行，结果在下方 Data Output）。[6]

### 1.4 VS Code 数据库插件

**Database Client**——VS Code 里最常用的多数据库客户端，一个插件连 PostgreSQL / MySQL / Redis / MongoDB / SQL Server 等多种数据库 + SSH / Docker，国内开发者出品。[7]

安装：扩展市场搜 **"Database Client"**——认准**发布者显示为 "Database Client"**（网站 database-client.com）的那个；扩展 ID `cweijan.vscode-database-client2`（约 120 万安装、标 Free Trial）。

> 市场里还有个 **Database Client JDBC**——那是主插件的**组件 / 依赖**（连 Db2、Hive 等少数 JDBC 库才用），**PostgreSQL 用不到，不用单独装**，装主插件即可。

> ⚠️ **别装错**：市场搜 "database" 排第一常是微软的 **SQL Database Projects**（`ms-mssql.sql-database-projects-vscode`）——那是 **MSSQL 专用的"表结构部署"工具，既不支持 PostgreSQL、也不是连接查询用的客户端**，跟我们要做的无关。认准**发布者为 "Database Client"**（网站 database-client.com）的那个。

连接：左侧活动栏点 **Database** 图标 → 面板里点 **`+`** → 选 **PostgreSQL** → 填**连接五要素** → Connect。[7]

用法：在库上点 **Open Query** 开 SQL 编辑器，写完按 `Ctrl+Enter` 执行；点表名直接看 / 改数据（表格内增删改查）。

### 1.5 图形 vs 命令行（psql）

GUI 直观，但命令行 **psql** 同样必备——服务器上往往没 GUI，脚本 / 自动化也只能用命令行。

连接：

```bash
psql -U postgres -d appdb -h localhost -p 5432
```

参数对照连接五要素：`-U` 用户、`-d` 库、`-h` 主机、`-p` 端口；密码连接时输入。

Docker 里用 psql（进容器）：

```bash
docker exec -it pg16 psql -U postgres -d appdb
```

psql 里两类命令：

| 类型 | 前缀 | 分号 | 示例 |
|------|------|------|------|
| SQL 语句 | 无 | **需要** `;` | `SELECT * FROM users;` |
| 反斜杠命令 | `\` | **不需要** | `\dt` |

常见反斜杠命令：

| 命令 | 含义 |
|------|------|
| `\l` | 列出所有数据库 |
| `\dt` | 列出当前库所有表 |
| `\d 表名` | 查看表结构（列、类型、约束） |
| `\du` | 列出所有用户（角色） |
| `\c 库名` | 切换到另一个库 |
| `\q` | 退出 psql |

三者取舍：

| 工具 | 适合 |
|------|------|
| **pgAdmin** | 专管 PostgreSQL，功能全（备份、可视化、权限），新手浏览学习友好 |
| **VS Code 插件** | 已在写代码，顺手查库改库，不想切窗口 |
| **psql** | 服务器无 GUI、写脚本 / 自动化、轻量快速 |

### 1.6 PG 客户端工具家族

psql / pg_dump / pg_restore / pgAdmin 都是**客户端工具**，平级，连同一个 PG 服务端干活，本身都不是数据库。区别只在"各管一摊"：

```
PostgreSQL 引擎（后台服务）
   │
   │  你不直接和引擎对话，要用客户端工具连它
   │
   ├── psql         交互式写 SQL、查数据（连进去敲命令）
   ├── pg_dump      把数据库导出成 .sql 备份文件
   ├── pg_restore   从备份文件恢复
   ├── createdb / dropdb   命令行快捷建库/删库
   └── pgAdmin      图形界面（独立软件，不在引擎里）
```

| 工具 | 干什么 | 怎么用 | 出来什么 |
|------|--------|--------|----------|
| **psql** | 交互式连库写 SQL | `psql -U postgres -d appdb` 进去敲命令 | 查询结果、表结构（`\d`） |
| **pg_dump** | 导出数据库为备份文件 | `pg_dump -U postgres -d appdb > backup.sql` | 一个 `.sql` 文件（建表+插数据语句） |
| **pg_restore** | 从备份文件恢复 | `pg_restore -d appdb < backup.sql` | 把数据导回库 |

**日常就用 psql（读写数据）+ pg_dump/pg_restore（备份迁移）这两个**。Docker 里这俩工具都在镜像内：

```bash
# 进容器用 psql
docker exec -it postgis16 psql -U postgres -d gisdb

# 用 pg_dump 备份（输出重定向到宿主机文件）
docker exec postgis16 pg_dump -U postgres -d gisdb > backup.sql

# 只导某个表的建表语句（DDL）
docker exec postgis16 pg_dump -U postgres -d gisdb -t notes --schema-only
```

#### SHOW 命令差异：从 MySQL 过来的坑

**PostgreSQL 没有 MySQL 那套 `SHOW` 命令**——`SHOW DATABASES` / `SHOW TABLES` / `SHOW CREATE TABLE` 在 PG 里全失效，照搬会语法报错。PG 的设计是「**看结构 = 查元数据表**」，把这事统一成了 SELECT。

| MySQL 用的 | PG 对应 |
|------------|---------|
| `SHOW DATABASES;` | `\l`（psql）或 `SELECT datname FROM pg_database;` |
| `SHOW TABLES;` | `\dt`（psql）或 `SELECT tablename FROM pg_tables WHERE schemaname='public';` |
| `SHOW CREATE TABLE x;` | `\d x`（psql，非完整 DDL）/ pgAdmin 右键表 → Scripts → CREATE Script / `pg_dump -t x --schema-only` |
| `DESC x;` / `SHOW COLUMNS FROM x;` | `\d x`（psql）或查 `information_schema.columns` |

> ⚠️ **`SHOW` 关键字在 PG 里存在，但用法完全不同**——它用来**查看服务器配置参数**，不是看对象结构：
> ```sql
> SHOW search_path;    -- 查看当前搜索路径（配置参数）
> SHOW timezone;       -- 查看时区设置
> ```
> 习惯性敲 `SHOW CREATE TABLE` 时，PG 会按"SHOW 配置参数"理解然后报错说没这个参数，**不会直接告诉你"这命令不存在"**，容易懵。

> 💡 **pgAdmin 看 DDL**：右键表 → **Scripts → CREATE Script**，就是完整可重新执行的 `CREATE TABLE ...`，最接近 MySQL `SHOW CREATE TABLE` 的体验。

### 1.7 参考来源

- [1][2] Docker 官方 `docker run` 文档（docs.docker.com）；postgres 镜像 PGDATA 说明（hub.docker.com/_/postgres）
- [3] Docker daemon `registry-mirrors` 配置（docs.docker.com/engine/reference/commandline/dockerd/）；国内源现状以实测为准
- [4] PostgreSQL 官方 libpq 连接参数：postgresql.org/docs/current/libpq-connect.html
- [5][6] pgAdmin 官方文档（pgadmin.org/docs）：deployment、server_dialog、query_tool、editgrid
- [7] cweijan Database Client：Marketplace（marketplace.visualstudio.com/items?itemName=cweijan.vscode-database-client2）、GitHub（cweijan/vscode-database-client）

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

#### Schema 是什么 + pgAdmin 树对应

**Schema（模式）= 数据库内部的一层命名空间**，用来把表、函数等对象逻辑分组。pgAdmin 左侧树的 `数据库 → Schema → public → 表` 这个顺序，就是 PG 真实层级的如实展示：

```
数据库（database）   ← 完全隔离的数据集合
  └── schema          ← 库内的命名空间 / 文件夹
        ├── public             ← 默认 schema，不指定就建到这里
        │     └── 表 / 视图 / 序列 / 函数 ...
        ├── information_schema ← 系统自带，元数据视图（查表/列信息）
        └── pg_catalog         ← 系统自带，系统表和内置函数
```

**`public` 不是关键字，是一个真实存在、名字就叫 `public` 的 schema**。每个库自带它，建表时不写 schema 名就落这里。前面 3.3 节报的 `permission denied for schema public`，拒绝的就是这个 schema。

**不写 schema 名时，PG 按搜索路径（search_path）找表**：默认 `"$user", public`——先找跟用户同名的 schema（没有就跳过），再找 `public`。所以 `SELECT * FROM notes` 等价于 `SELECT * FROM public.notes`。

> ⚠️ **从 MySQL 过来的人会懵这层**：MySQL 没有 schema 这个独立概念，`database` 和 `schema` 是同义词（`CREATE DATABASE` ≡ `CREATE SCHEMA`），只有两层 `实例 → 库 → 表`。PG 多出来的 schema 层是标准 SQL 设计，MySQL 砍掉了。详见 2.2。

### 2.2 Schema 详解

> Schema 不只是"表的文件夹"。它是一整套数据库对象的命名空间——表、视图、序列、函数、自定义类型、索引、触发器都能放进同一个 schema。这正是 PostgreSQL「对象关系型」的体现：schema 不只装数据，还装逻辑。

#### Schema 里能放什么

| 对象 | 作用 | 例子 |
|------|------|------|
| **表（table）** | 存数据 | `notes`、`users` |
| **视图（view）** | 存一条 SELECT 查询，当虚拟表用 | 把复杂 JOIN 存成视图，查时像查表 |
| **序列（sequence）** | 自增数字生成器 | 见 4.4，自增主键的 `notes_id_seq` 就是它供数 |
| **函数（function）** | 可调用逻辑，可嵌入 SQL | 内置 `lower()`/`now()`，也可自定义 |
| **数据类型（type）** | 自定义类型 | PostGIS 的 `geometry`、`geography` |
| **索引（index）** | 加速查询（表的附属，但属 schema） | btree、GiST |
| **触发器（trigger）** | 表上事件钩子（INSERT/UPDATE 时自动跑） | 自动填 `deleted_at` 可用它 |
| **聚合、操作符、转换（cast）** | 高级扩展点 | PostGIS 让 `<->` 算空间距离，就是操作符重载 |

**关键认知**：`CREATE EXTENSION postgis` 一条命令，往（默认）`public` schema 里塞进了一整套——`geometry` 类型 + 几百个 `ST_*` 函数 + `<->`/`&&` 操作符 + GiST 索引方法实现。**这之所以可能，是因为 PG 的 schema 允许放这些非表对象**。你的 `public` schema 此刻就混着你的业务表和 PostGIS 的全套扩展对象（靠前缀和类型区分：`ST_` 开头是函数，`geometry` 是类型）。

> 这也是为什么 2.3 会说"扩展自带对象建议放独立 schema"——分开更干净，但 PostGIS 默认就进 public，大家都习惯了。

#### 这个设计模式是 PostgreSQL 特有的吗

**不是"独有"，但 PG 把 schema 做得最通用。** 各数据库对比：

| 数据库 | 对应概念 | 默认值 | 特点 |
|--------|----------|--------|------|
| **PostgreSQL** | schema | `public` | 可独立建、独立授权、能放任意对象（函数/类型/操作符） |
| **SQL Server** | schema | `dbo` | 表写 `dbo.users`；可独立建，不绑用户 |
| **Oracle** | schema | 绑定用户名 | **一个用户 = 一个 schema**，不能脱离用户独立建 |
| **MySQL** | 无 | —— | `database` ≡ `schema`（同义词），只有两层 |

SQL 标准本身定义了 schema（SQL:1999 起），所以"库 → schema → 表"是**标准设计**：PG 严格遵循、做得最通用；MySQL 砍掉这层；Oracle/SQL Server 有但绑用户或绑 owner。

### 2.3 Schema 划分实践

#### 三种分法（从最常用到最讲究）

**① 不分——中小项目全用 `public`（最常见）**

绝大多数 Web 业务项目一个 `public` schema 干到底。表不多（几十张）、团队都熟、工具默认指 public。**分了反而要在每个 SQL 里写前缀，徒增心智负担。不分是合理默认。**

**② 按扩展/模块隔离——系统级，几乎都这么干**

第三方扩展自带的对象各自圈在独立 schema，不污染 public。PostGIS 就是教科书例子（见下表）。建扩展时可指定 schema：

```sql
CREATE SCHEMA postgis;
CREATE EXTENSION postgis SCHEMA postgis;   -- 之后用 ST_* 要写 postgis.ST_*，
                                            -- 或把 postgis 加进 search_path
```

**③ 按业务模块/租户分——业务级，中大型系统才用**

一个库里有多个清晰独立的子系统或多租户需求时才切：

```
-- 按业务模块
public.users, public.orders      ← 交易域
cms.articles, cms.categories     ← 内容管理域
analytics.events                 ← 分析域

-- 按租户（SaaS 一库多客户）
tenant_acme.users, tenant_globex.users
```

代价：跨 schema JOIN 要写前缀、迁移工具要适配、权限更复杂。**除非真有强隔离需求，否则别上。**

#### PostGIS 自动建的 schema 来历

你 `CREATE EXTENSION postgis` 后会发现库里有 `tiger` / `tiger_data` / `topology` 等额外 schema——**不是你建的，是 PostGIS 相关扩展自动建的**：

| Schema | 谁建的 | 装了什么 | 你用得到吗 |
|--------|--------|----------|-----------|
| `public` | PG 默认 | 你的业务表 + PostGIS 核心函数/类型 | 用 |
| `topology` | `postgis_topology` 扩展 | 拓扑结构（路网、地块相邻关系） | 几乎用不到 |
| `tiger` / `tiger_data` | `tiger_geocoder` / `address_standardizer` | **美国**人口普查 TIGER 地址数据 + 标准化函数 | 国内项目用不到 |

> 这些 schema 是 `postgis/postgis` 官方镜像把这些扩展全预装并启用才出现的。**做普通 GIS 业务可以无视**——`tiger` 是美国地址专用，国内项目八成一辈子不碰。它们恰好示范了「扩展自带对象进独立 schema」的最佳实践。

#### 决策表

| 场景 | 怎么分 |
|------|--------|
| 普通业务项目 | **不分**，全放 `public` |
| 装了多个扩展 | 让扩展对象进各自 schema（系统级，自动发生） |
| 库里有多个独立子系统 / 多租户 | 按模块或租户分（业务级，要权衡） |

查自己库里有几个 schema：

```sql
SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;
```

### 2.4 数据库操作

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

| 属性            | 含义                         |
| ------------- | -------------------------- |
| `LOGIN`       | 能登录（有 LOGIN = 用户，没有 = 纯角色） |
| `SUPERUSER`   | 超级用户，无视所有权限检查              |
| `CREATEDB`    | 能新建数据库                     |
| `CREATEROLE`  | 能新建/删除角色                   |
| `REPLICATION` | 能做主从复制                     |

### 3.3 权限级别

权限可以精确控制到不同层级：

| 层级       | 常见权限                        | 例子                     |
| -------- | --------------------------- | ---------------------- |
| 实例级      | LOGIN、CREATEDB、SUPERUSER    | 创建角色时决定                |
| 数据库级     | CONNECT、CREATE、TEMP         | 谁能连这个库                 |
| Schema 级 | USAGE、CREATE                | 谁能在这个 schema 下建表       |
| 表级       | SELECT、INSERT、UPDATE、DELETE | 谁能查/增/改/删              |
| 列级       | SELECT、INSERT、UPDATE（按列）    | 敏感列只读（极少用）             |
| 行级       | RLS（Row-Level Security）     | 比如 user A 只能看到自己的 note |

最常用的表级权限：

```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON notes TO fastapi_user;
REVOKE DELETE ON notes FROM fastapi_user;   -- 收回某个权限
```

当数据库是用 `OWNER fastapi_user` 创建时，该用户自动拥有该库全部权限，无需逐表 GRANT。

> ⚠️ **新用户默认建不了表（PG15+ 安全变更）**：`public` schema 默认只给所有人 `USAGE`（能用），**不再给 `CREATE`**（PG15 起改的安全默认）。所以新建的普通用户（如 `app_user`）直接 `CREATE TABLE` 会报 `permission denied for schema public`。解决：`GRANT CREATE ON SCHEMA public TO app_user;`。

#### 对象属主（OWNER）与 ALTER 动词

前面那句「`OWNER fastapi_user` 创建时该用户自动拥有该库全部权限」里的 **OWNER（属主）**，是 PG 权限体系的关键概念：

**每个数据库对象（表、数据库、schema、序列、函数...）都有一个"属主"**，自动 = 创建它的那个用户。属主对该对象有**全部权限**，无需 GRANT；想彻底删/改结构也要属主或超级用户。

```
用户 touyou 执行 CREATE TABLE raw_tracks ...
  → raw_tracks 的 OWNER 自动 = touyou
  → touyou 对这张表有全部权限（DROP / ALTER / GRANT 给别人...）
```

**改属主**用 `ALTER ... OWNER TO`（pgAdmin 的 CREATE Script 里经常附带这条，用来恢复属主信息）：

```sql
ALTER TABLE IF EXISTS public.raw_tracks OWNER TO touyou;
-- IF EXISTS：表不存在时不报错（默认会报），让脚本更健壮
```

`ALTER` 是 SQL 改对象的通用动词，和 `CREATE` / `DROP` 一组：

| 动词 | 干什么 | 例子 |
|------|--------|------|
| `CREATE` | 新建 | `CREATE TABLE ...`、`CREATE USER ...` |
| `ALTER` | **修改已存在的** | `ALTER TABLE ... ADD COLUMN`、`ALTER USER ... PASSWORD` |
| `DROP` | 删除 | `DROP TABLE ...`、`DROP USER ...` |

`ALTER TABLE` 能改的事很多——加列/删列/改列类型/加约束/改属主/重命名表，都是它：

```sql
ALTER TABLE raw_tracks ADD COLUMN speed float;                      -- 加列
ALTER TABLE raw_tracks DROP COLUMN speed;                           -- 删列
ALTER TABLE raw_tracks ALTER COLUMN speed TYPE double precision;    -- 改列类型
ALTER TABLE raw_tracks ADD CONSTRAINT ... ;                         -- 加约束
ALTER TABLE raw_tracks OWNER TO touyou;                             -- 改属主
ALTER TABLE raw_tracks RENAME TO tracks;                            -- 改表名
```

> 💡 **`IF EXISTS` 的两个方向别混**：`ALTER/DROP TABLE IF EXISTS` = 表存在才执行（避免"不存在"报错）；`CREATE TABLE IF NOT EXISTS` = 表不存在才建（避免"已存在"报错）。

### 3.4 认证机制（pg_hba.conf）

为什么 `docker exec` 进容器后 `psql -U postgres` 不需要密码，但 pgAdmin / VS Code 从外部连 `localhost:5432` 必须密码？

两种连接路径：

```
Windows 宿主机
  │
  ├── pgAdmin / VS Code → localhost:5432 (TCP) → 必须密码
  │
  └── docker exec → 容器内 → Unix socket      → 免密码（本地信任）
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

Docker 容器内 `psql` 走 Unix socket → `trust` 免密码；容器外连 `localhost:5432` 走 TCP → 需要密码。

| | 认证方式 | 需要密码？ |
|----|---------|-----------|
| 容器内 docker exec | Unix socket (trust) | 不需要 |
| 容器外 TCP 连接 | scram-sha-256 | 需要 |

能连上 ≠ 能干所有事，具体权限取决于角色属性。

## 第4章 数据类型与表结构

### 4.1 常用数据类型

| PostgreSQL 类型                         | 含义                    | 对应 SQLAlchemy |
| ------------------------------------- | --------------------- | ------------- |
| `integer`                             | 32 位整数                | `Integer`     |
| `character varying(n)` / `varchar(n)` | 变长字符串，最多 n 字符，超长报错    | `String(n)`   |
| `text`                                | 变长字符串，无长度限制           | `Text`        |
| `boolean`                             | 真/假（psql 显示为 `t`/`f`） | `Boolean`     |

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

#### 元数据（metadata）与系统目录

上面 `SELECT ... FROM information_schema.columns` 查的不是笔记内容，是**元数据**——**描述数据库自身结构的信息**（有哪些表、每列什么类型、哪个是主键、有哪些索引）。

| | 是什么 | 例子 |
|---|--------|------|
| **数据** | 表里存的业务内容 | notes 表一行行笔记 |
| **元数据** | 描述这些数据怎么组织的信息 | "notes 表有 id/title/content 列，id 是主键" |

PG 把元数据存在专门的**系统目录（system catalog）**——它们本身也是表，只是系统自带、描述数据库自己的：

| 看这个 | 查什么元数据 |
|--------|-------------|
| `information_schema.columns` | 所有表的所有列信息（**SQL 标准**规定的，MySQL/PG/SQL Server 都有，代码可移植） |
| `information_schema.tables` | 所有表的信息 |
| `pg_catalog.pg_tables` | 所有表（PG 专有系统表） |
| `pg_catalog.pg_database` | 所有数据库 |
| `pg_catalog.pg_class` | 所有"表类"对象（表、索引、视图、序列…） |

**pgAdmin 左侧树看到的层级、`\d` 输出的表结构，背后全是从这些元数据表 SELECT 出来的。** PG 没有 MySQL 的 `SHOW` 命令，就是因为把"看结构"统一成了"查元数据表"——更标准，但写起来比 `SHOW CREATE TABLE` 啰嗦。

> 💡 **代码里查元数据永远查 `information_schema.*`**：写程序（Go/Python）需要知道表结构时（ORM、迁移工具、代码生成器），不要去解析 `\d` 的输出（那是 psql 客户端的快捷命令，程序里用不了），直接 `SELECT ... FROM information_schema.columns WHERE ...`。它是 SQL 标准，跨数据库可移植。

```python
# Python 示例：查 notes 表的列名和类型
rows = db.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'notes'
    ORDER BY ordinal_position;
""")
# [('id','integer'), ('title','character varying'), ...]
```

#### 查看对象占用空间（pg_relation_size 等）

PostgreSQL 提供一组系统函数用于查看**表/索引等对象**占用的磁盘空间（单位：bytes），通常会配合 `pg_size_pretty()` 做人类可读显示：

```sql
SELECT pg_size_pretty(pg_relation_size('testfragement'));
```

常用函数（建议优先记 `pg_total_relation_size`）：

| 函数 | 返回什么 | 典型用途 |
|---|---|---|
| `pg_relation_size(rel)` | 对象本体大小（常见：表数据文件或索引文件） | 快速看“表本体/某个索引”多大 |
| `pg_table_size(rel)` | 表大小（包含 TOAST 等表自身附属存储，不含索引） | 看“表自身”实际占用 |
| `pg_indexes_size(rel)` | 该表的所有索引总大小 | 判断索引是否过大 |
| `pg_total_relation_size(rel)` | 表总大小（表 + TOAST + 索引） | 看“这张表最终占多少空间”（最常用） |

更稳妥的对象引用写法（避免 schema 同名/搜索路径差异）：

```sql
SELECT pg_size_pretty(pg_total_relation_size('public.testfragement'::regclass));
```

> ⚠️ 观察空间变化时要记住：`DELETE`/`UPDATE` 往往不会立刻让文件变小（MVCC 会留下旧版本/空洞供复用）。需要“真正归还给操作系统”的场景通常要用 `VACUUM FULL`/`CLUSTER` 等重写表的操作（代价较高，且会长时间锁表）。

### 4.3 约束

| 约束            | 含义                    | 违反时        |
| ------------- | --------------------- | ---------- |
| `NOT NULL`    | 该列必须有值                | 插入 NULL 报错 |
| `PRIMARY KEY` | 主键，唯一且非空，自带 btree 索引  | 重复主键报错     |
| `UNIQUE`      | 该列值不可重复（如 `username`） | 插入重复值报错    |
| `FOREIGN KEY` | 引用完整性，值必须在被引用表中存在     | 引用不存在的值报错  |

外键约束示例：`notes.user_id` 必须是 `users.id` 中真实存在的值。
插入 `user_id=999`（users 中无此 id）会报错：

```
ERROR:  insert or update on table "notes" violates foreign key constraint "notes_user_id_fkey"
DETAIL:  Key (user_id)=(999) is not present in table "users".
```

这防止了"孤儿数据"（笔记挂在不存在的用户身上）。

**外键是双向保护**——反过来，删 `users` 里一个"还被 notes 引用着"的用户也会被拦：

```
ERROR:  update or delete on table "users" violates foreign key constraint "notes_user_id_fkey"
DETAIL:  Key (id)=(1) is still referenced from table "notes".
```

想删带笔记的用户，两条路：① 先删它的 notes 再删用户；② 建表时给外键加 `ON DELETE CASCADE`（`REFERENCES users(id) ON DELETE CASCADE`），删用户时自动连带删其笔记（订单类业务通常**不**级联，怕误删）。

### 4.4 自增主键与 Sequence

PostgreSQL 无 MySQL 的 `AUTO_INCREMENT`，自增靠 **Sequence（序列）** 实现：

- 建表时自动创建序列对象 `notes_id_seq`
- `id` 列默认值 = `nextval('notes_id_seq')`，每次插入取序列下一个值

**关键特性：序列只增不回退**。失败/回滚的事务也会消耗序列值，所以自增 id 可能跳号
（如插入失败后下一条 id 从 2 跳到 3），**不保证连续，只保证唯一递增**。

> ⚠️ 所以**别拿自增 id 当"第几条"来算**——它只是个唯一标识，会有空洞。业务需要连续序号得另外设计。

### 4.5 标识符与大小写

#### 默认情况：标识符什么都不加，字符串用单引号

```sql
-- 标识符（表名/列名）裸写，字符串值用单引号
CREATE TABLE notes (
    id serial PRIMARY KEY,
    title varchar(100),
    content text
);

SELECT id, title FROM notes WHERE title = '测试';
```

**核心规则两条，记住即可应付 95% 场景：**

1. **标识符（表名/列名）裸写，不加任何引号**——PG 自动按小写处理
2. **字符串值永远用单引号 `'...'`**

#### PG 默认折叠小写（关键机制）

**未加引号的标识符，PG 一律折叠成小写**——这是和 MySQL 最大的区别之一（MySQL 在 Linux 上大小写敏感、依文件系统；PG 永远折叠）。

```sql
CREATE TABLE Users (id int);    -- PG 实际建的是 users 表
SELECT * FROM Users;            -- 折叠成 users，能查到
SELECT * FROM USERS;            -- 同样折叠成 users，能查到
SELECT * FROM "Users";          -- ❌ 报错：没有叫 "Users"（大写 U）的表
```

**唯一能保留大小写的方式是双引号 `"..."`**——但一旦用了，之后每次访问都得加，漏一次就报错：

```sql
CREATE TABLE "Users" (id int);  -- 这次真建了叫 "Users" 的表
SELECT * FROM Users;            -- ❌ 折叠成 users，查不到
SELECT * FROM "Users";          -- ✅ 才能查到
```

#### 双引号 `"..."` 的三个被迫场景

双引号是"逃生口"，不是日常工具。只有这些场景**被迫**用：

| 场景 | 例子 | 说明 |
|------|------|------|
| **迁移来的大写表名**（最常见） | `CREATE TABLE "PartTimeRoutePointImages" (...)` | 从 MySQL 驼峰命名迁移时；**强烈建议改 snake_case**，否则全工程每次访问都要加引号 |
| **列名撞 PG 保留字** | `CREATE TABLE t ("order" int, "type" varchar)` | `order`/`from`/`select`/`user`/`type` 等当列名；**建议起名避开**（用 `order_no`、`contract_type`） |
| **标识符含空格/特殊字符**（极少） | `CREATE TABLE "my table" (...)` | 基本只在导入带空格表头的 CSV 时碰到，正常设计不会用 |

#### 从 MySQL 迁移的命名建议

MySQL 那套 PascalCase 命名（`Id`/`RouteId`/`CreateTime`）到 PG 强烈建议转 snake_case：

```
MySQL:    Id, RouteId, CreateTime, PartTimeRoutePointImages
PG 推荐:  id, route_id, create_time, part_time_route_point_images
```

一劳永逸：省掉之后所有 SQL / ORM 配置 / 迁移脚本里加双引号的麻烦，团队里有人漏一处就够头疼一天。这也是 Go/Python 主流 ORM（sqlx、GORM、SQLAlchemy）默认期待的命名风格——它们一般自动做 snake_case 映射。

#### 决策表

| 想做的事 | 怎么写 |
|---------|--------|
| 正常建表/查询 | 标识符**裸写**，字符串用**单引号** |
| 标识符必须用大写/保留字/特殊字符（迁移、老表） | 用**双引号**包，之后每次访问都得加 |
| 字符串值 | 永远**单引号** |

> 💡 **心法**：坚持「标识符全小写、避开关键字」，就一辈子不用碰双引号。需要双引号的几乎都是历史包袱（迁移来的大写表名、老系统的关键字列名），那是被迫用，不是主动用。

## 第5章 SQL 增删改查

`INSERT`/`SELECT`/`UPDATE`/`DELETE` 是 SQL 关键字（DML，数据操作语言），不是函数。

### 5.1 INSERT 插入 

```sql
INSERT INTO notes (title, content, done, user_id)
VALUES ('测试', '内容', false, 1);
-- 返回 INSERT 0 1：第一个数是 OID（已废弃，恒为 0），第二个是影响行数
```

语法结构：`INSERT INTO 表名 (列名列表) VALUES (值列表)`，值的顺序与列名一一对应。

**多行插入**：一条 INSERT 一次插多行，用逗号分隔（比循环单条插快得多）：

```sql
INSERT INTO notes (title, content, done, user_id)
VALUES ('笔记A', '内容A', false, 1),
       ('笔记B', '内容B', true,  1),
       ('笔记C', '内容C', false, 2);
```

字符串值用**单引号** `'...'`；双引号 `"..."` 用于标识符（表名/列名），不可混用。

列名可不写全，未写的列需满足之一，否则报错：
- 有默认值（如 `id` 的 nextval）→ 自动填默认值
- 允许 NULL → 自动填 NULL
- `NOT NULL` 且无默认值 → 必须提供

#### INSERT ... SELECT：把查询结果当数据源（批量插入）

PostgreSQL 常用 `INSERT INTO ... SELECT ...` 批量插入：**先用 SELECT 造出一批行，再一次性写入目标表**（造测试数据、从别表导入都靠它）。

```sql
INSERT INTO testfragement (tid, tname)
SELECT n, 'myname_' || n
FROM generate_series(1, 50000000) AS g(n);
```

关键点：

- `INSERT INTO ... (tid, tname)`：显式写列名更稳（避免表结构变更导致列顺序对不上）。
- `generate_series(1, 50000000)` 是**集合返回函数（SRF）**：返回 `SETOF integer`，可直接放在 `FROM` 里当“虚拟表数据源”。
- `AS g(n)`：`g` 是表别名，`n` 是列名（`SELECT` 里能引用 `n`，本质上是对 `FROM` 产生的那一列起名）。
- `'myname_' || n`：`||` 是字符串拼接（等价 `concat('myname_', n)`）。

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

> ⚠️ **保命习惯**：拿不准的 UPDATE/DELETE 先用 `BEGIN` 包起来，核对影响行数对了再 `COMMIT`，错了 `ROLLBACK`——这是后悔药。生产环境误删全表事故，绝大多数就是漏了 `WHERE`。

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

> ⚠️ **最大的坑**：每个业务查询都得记得加 `WHERE deleted_at IS NULL`，漏写一条就会把已删数据当正常数据查出来。靠人记不靠谱，ORM 层一般用钩子自动注入这个条件。

### 6.2 软删除的取舍

| 优点               | 缺点                                   |
| ---------------- | ------------------------------------ |
| 可恢复（误删能找回）       | 表持续增大，需定期归档/清理                       |
| 留痕，满足审计/分析       | 每个查询都得加过滤条件，漏写会查出已删数据                |
| 保护引用完整性（别表引用了该行） | 唯一约束冲突：软删的 `username` 与新注册同名撞 UNIQUE |
| 支持回收站功能          |                                      |

适用场景：重要业务数据（订单、用户、交易）几乎都用软删除；临时/日志类数据用硬删除即可。

避免每个查询手写过滤条件：ORM 层用事件钩子或 query 过滤器统一注入 `WHERE deleted_at IS NULL`。

### 6.3 两阶段软删除（回收站 + 定时清理）

中大型系统的标准做法：用状态机把"对用户不可见"与"释放存储"解耦。

字段：

| 字段                    | 作用                                 |
| --------------------- | ---------------------------------- |
| `delete_status`       | 数据所处阶段：`0` 正常 / `1` 回收站 / `2` 逻辑已删 |
| `delete_scheduled_at` | **计划**执行下一步清理的时间                   |

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

| 类型           | 中文                       | 保留哪边             |
| ------------ | ------------------------ | ---------------- |
| `INNER JOIN` | 内连接（`JOIN` 默认即此）         | 只保留两边都匹配的行       |
| `LEFT JOIN`  | 左连接（= `LEFT OUTER JOIN`） | 左表全部，右表无匹配填 NULL |
| `RIGHT JOIN` | 右连接                      | 右表全部，左表无匹配填 NULL |
| `FULL JOIN`  | 全连接                      | 两边全保留，缺的填 NULL   |

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

## 第8章 PostGIS 专题（空间数据库）

> PostGIS 是 PostgreSQL 的空间扩展，把 PG 变成**空间数据库**，是 GIS 行业的事实标准。本章覆盖面试与实战核心：几何类型、坐标系、ST_ 函数、空间索引、KNN、数据导入。

### 8.1 安装与启用

PostGIS 用独立 Docker 镜像 `postgis/postgis`（PG + PostGIS 预装）：

```powershell
docker run --name postgis16 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=gisdb -p 5435:5432 -v postgisdata:/var/lib/postgresql/data -d --restart unless-stopped postgis/postgis:16-3.4
```

每个库要**手动启用**扩展（二进制预装，但不自动开）：

```sql
CREATE EXTENSION postgis;
SELECT PostGIS_Version();   -- 返回 3.x 即成功
```

### 8.2 geometry 类型与 WKT

PostGIS 给 PG 加了 `geometry` 类型。建空间列时可约束**类型 + SRID**：

```sql
CREATE TABLE pois (
    id serial PRIMARY KEY,
    name varchar(100),
    geom geometry(Point, 4326)   -- 只能存点，SRID 锁 4326
);

INSERT INTO pois (name, geom) VALUES
  ('天安门', ST_GeomFromText('POINT(116.397 39.908)', 4326));
```

**WKT（Well-Known Text）** 是几何的文本写法：

| 几何 | WKT |
|------|-----|
| 点 | `POINT(x y)` |
| 线 | `LINESTRING(0 0, 1 1, 2 2)` |
| 面 | `POLYGON((0 0, 1 0, 1 1, 0 0))`（首尾闭合） |

> ⚠️ **经度（lon）在前，纬度（lat）在后**：`POINT(116.397 39.908)` = `POINT(经度 纬度)` = `POINT(x y)`。这是 PostGIS 最经典的坑——人脑习惯"纬度在前"，但 GIS 标准**永远是 X=经度、Y=纬度**。面试官超爱问。

`geometry` 列存的是**二进制（WKB）**，直接 SELECT 看不懂，要转文本：

- `ST_AsText(geom)` → WKT：`POINT(116.397 39.908)`
- `ST_AsGeoJSON(geom)` → GeoJSON：`{"type":"Point","coordinates":[116.397,39.908]}`

输入用 `ST_GeomFromText(WKT, SRID)`（或更快的 `ST_SetSRID(ST_MakePoint(x,y), SRID)`）。

### 8.3 SRID 与 geometry vs geography（面试高频）

**SRID（Spatial Reference ID）= 你的坐标数字是哪套坐标系**：

| SRID | 坐标系 | 单位 | 用途 |
|------|--------|------|------|
| `4326` | WGS84 | 度（经纬度） | GPS、GeoJSON 默认 |
| `3857` | Web Mercator | 米 | Web 地图（高德 / Google） |

**geometry vs geography**（核心区别）：

| | `geometry` | `geography` |
|---|---|---|
| 把地球当成 | 平面（笛卡尔） | 球面（椭球） |
| 距离 / 面积单位 | 跟坐标系的单位（4326 就是度） | **永远是米** |
| 适合 | 已投影数据（3857 米）、局部小区域 | 经纬度（4326）做全球距离 / 面积 |
| 速度 | 快 | 慢 |

> ⚠️ **经典坑**：把经纬度（4326）存成 `geometry` 再 `ST_Distance`，得到的是**度**，不是米，完全没意义。经纬度算距离 / 面积，**要么用 geography 类型，要么 `geom::geography` 转一下**。面试官爱挖："你 ST_Distance 算出 0.035，这是啥单位？"

**ST_SetSRID vs ST_Transform**（另一个面试陷阱）：

| 函数 | 作用 | 改坐标数值吗 |
|------|------|--------------|
| `ST_SetSRID(geom, 4326)` | 只是**贴标签** | **不改** |
| `ST_Transform(geom, 3857)` | 真正**重投影** | **改**（重新计算） |

### 8.4 ST_ 函数家族

| 家族 | 代表函数 | 返回 |
|------|----------|------|
| **测量** | `ST_Distance`、`ST_Length`、`ST_Area`、`ST_Perimeter` | 数值 |
| **关系（谓词）** | `ST_Intersects`、`ST_Within`、`ST_Contains`、`ST_DWithin`、`ST_Touches`、`ST_Crosses` | 布尔 |
| **生成 / 集合** | `ST_Buffer`、`ST_Intersection`、`ST_Union`、`ST_Centroid`、`ST_MakePoint` | 几何 |

- **空间连接（spatial join）**：JOIN 条件用空间函数，如 `JOIN districts d ON ST_Within(p.geom, d.geom)`——这是 GIS 查询的精髓。
- "找附近"用 `ST_DWithin`（能用索引），别用 `ST_Distance < N`。

### 8.5 空间索引 GiST（性能，面试超爱）

没索引时，空间查询**逐行扫整张表**（N 行算 N 次几何运算），大数据量慢到不能用。

**GiST（Generalized Search Tree）** 是空间索引类型：

```sql
CREATE INDEX pois_geom_gist ON pois USING GIST (geom);
VACUUM ANALYZE pois;        -- 让规划器知道新索引
```

**原理**：GiST 存每个几何的**外包框（bounding box）**。查询时先用 `&&`（外包框相交）操作符**快速粗筛**绝大多数不可能匹配的几何，只剩少量候选再做精确检测。

- 普通 btree 索引对几何**没用**（几何没"大小顺序"），空间必须 `USING GIST`。
- 空间谓词（`ST_Intersects` / `ST_Within` / `ST_DWithin`）检测到 GiST 索引就**自动走**，查询不用改。
- 建完索引要 `VACUUM ANALYZE`，否则规划器可能还全表扫。

**用 EXPLAIN 验证**：

```
建索引前：Seq Scan on pois (cost=0.00..125231)              ← 全表扫，慢
建索引后：Index Scan using pois_geom_gist (cost=0.28..20.79) ← 用索引，快 ~6000 倍
         Index Cond: geom && st_expand(...)   ← 外包框粗筛
         Filter:     st_dwithin(...)          ← 精确检测，只对候选
```

> 💡 面试经典问："ST_DWithin 查询慢怎么优化？"答：**确认 geom 列有 GiST 索引、统计信息最新（ANALYZE）**。会读 EXPLAIN 是加分项。

### 8.6 实战查询

**① KNN：找最近的 N 个**（用 `<->` 操作符）：

```sql
SELECT name,
       ST_Distance(geom::geography, ST_GeogFromText('POINT(116.397 39.908)')) AS dist_m
FROM pois
ORDER BY geom <-> ST_GeomFromText('POINT(116.397 39.908)', 4326)
LIMIT 3;
```

- `<->` 是 KNN 距离操作符，在 ORDER BY 里**能走 GiST 索引**。
- "找最近 N 个"用 `ORDER BY geom <-> 点 LIMIT N`，别用 `ORDER BY ST_Distance(...)`（全算慢）。

**② 空间连接 + 统计**（多边形内有多少点）：

```sql
SELECT count(*) FROM pois p JOIN districts d ON ST_Within(p.geom, d.geom);
```

**③ 缓冲区**（给点画 500 米圈）：

```sql
SELECT name, ST_AsGeoJSON(ST_Buffer(geom::geography, 500)) AS buffer_500m
FROM pois WHERE name IN ('天安门','故宫','天坛');
```

### 8.7 栅格与数据导入

**矢量 vs 栅格**：

| | 矢量 | 栅格 |
|---|------|------|
| 是什么 | 点 / 线 / 面 | 像素网格 |
| 典型 | POI、边界、路网 | 卫星图、高程、温度 |
| 用得多 | **99% 业务** | 影像 / 遥感 |

**数据导入**（面试常问"怎么把空间数据导进 PostGIS"）：

| 来源 | 工具 | 说明 |
|------|------|------|
| **GeoJSON** | `ST_GeomFromGeoJSON` | SQL 直接转 |
| **Shapefile** | `shp2pgsql`（PostGIS 自带 CLI） | shp → SQL 灌入 |
| **多格式直读** | `ogr_fdw` 扩展 | GeoJSON / KML / GPKG 当外表查 |
| **OpenStreetMap** | `osm2pgsql` | OSM → PostGIS |

```sql
-- 从 GeoJSON 插多边形
INSERT INTO districts (name, geom)
SELECT '从GeoJSON', ST_SetSRID(ST_GeomFromGeoJSON(
  '{"type":"Polygon","coordinates":[[[116.40,39.91],[116.43,39.91],[116.43,39.94],[116.40,39.94],[116.40,39.91]]]}'
), 4326);
```

> ⚠️ GeoJSON Polygon 坐标是**三层方括号** `[[[x,y],...]]`（多边形 → 环 → 点），少一层报错；且 `ST_GeomFromGeoJSON` 不带 SRID，要 `ST_SetSRID(..., 4326)` 补上（GeoJSON 默认 WGS84）。

### 8.8 面试要点速记

1. **PostGIS 是啥**：PG 的空间扩展，把 PG 变空间数据库；`CREATE EXTENSION postgis`。
2. **经度在前**：`POINT(lon lat)` = `POINT(x y)`。
3. **geometry vs geography**：经纬度算距离用 geography（米），否则得到度。
4. **ST_SetSRID 贴标签 / ST_Transform 真重投影**。
5. **找附近用 `ST_DWithin`**（能索引）；**找最近用 `<->` + LIMIT**（KNN，能索引）。
6. **空间索引用 GiST**（`USING GIST`），不是 btree；建完 `VACUUM ANALYZE`。
7. **GiST 原理**：外包框粗筛 → 精确检测。
8. **读 EXPLAIN**：Seq Scan（慢 / 无索引）vs Index Scan + `&&`（快 / 用上索引）。
9. **空间连接**：JOIN ON 用空间函数。
10. **导入**：GeoJSON 用 `ST_GeomFromGeoJSON`（三层括号 + 补 SRID）；shapefile 用 `shp2pgsql`。

### 8.9 参考来源（均为官方 / 权威一手）

- **PostGIS 官方文档**：postgis.net/docs（几何类型、ST_ 函数、GiST 索引、栅格全在这）
- **PostGIS 项目 / 镜像**：postgis.net、hub.docker.com/r/postgis/postgis
- **坐标系 / SRID**：spatialreference.org（EPSG 4326 / 3857 等）；PostGIS 内置 `spatial_ref_sys` 表
- **WKT / WKB 标准**：OGC Simple Features for SQL（SFS）
- **导入工具**：shp2pgsql、ogr_fdw、osm2pgsql（各自官方仓库）
