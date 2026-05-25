# 目录

- [[#1. 工程结构总览|1. 工程结构总览]]
  - [[#1.1 目录结构图|1.1 目录结构图]]
  - [[#1.2 FastAPI 模块分布|1.2 FastAPI 模块分布]]
  - [[#1.3 后端依赖图|1.3 后端依赖图]]
- [[#2. 工程目录内容|2. 工程目录内容]]
  - [[#2.1 main.py|2.1 main.py]]
  - [[#2.2 middleware|2.2 middleware]]
  - [[#2.3 coreconfig.py|2.3 core/config.py]]
  - [[#2.4 coredb.py|2.4 core/db.py]]
  - [[#2.5 dependencies.py|2.5 dependencies.py]]
  - [[#2.6 modulesrouter.py-schemaservice.py-repository.py-model.py|2.6 modules/*/router.py schema.py service.py repository.py model.py]]
  - [[#2.7 tests|2.7 tests]]
- [[#3. 常用接口写法|3. 常用接口写法]]
  - [[#3.1 路由与路径操作|3.1 路由与路径操作]]
  - [[#3.2 路径参数查询参数请求体|3.2 路径参数、查询参数、请求体]]
  - [[#3.3 pydantic-模型|3.3 Pydantic 模型]]
  - [[#3.4 响应模型与状态码|3.4 响应模型与状态码]]
  - [[#3.5 depends|3.5 `Depends`]]
  - [[#3.6 middleware-与-exception_handler|3.6 `middleware` 与 `exception_handler`]]
- [[#4. 原理拆解|4. 原理拆解]]
  - [[#4.1 参数注入|4.1 参数注入]]
  - [[#4.2 请求体解析机制-pydantic--dataclass|4.2 请求体解析机制 (Pydantic & Dataclass)]]
  - [[#4.3 依赖注入机制|4.3 依赖注入机制]]
  - [[#4.4 异常处理机制|4.4 异常处理机制]]
  - [[#4.5 中间件调用链|4.5 中间件调用链]]
  - [[#4.6 应用生命周期|4.6 应用生命周期]]
- [[#5. 工程实践|5. 工程实践]]
  - [[#5.1 分层边界|5.1 分层边界]]
  - [[#5.2 测试组织|5.2 测试组织]]
  - [[#5.3 常见反模式|5.3 常见反模式]]

# 1. 工程结构总览

## 1.1 目录结构图

```text
src/app/
├── main.py                 # 应用入口：创建 app，注册 router / middleware / lifespan

├── core/
│   ├── config.py             # 配置对象：读取 .env / 环境变量
│   └── db.py                 # 数据库基础设施：engine、sessionmaker、ping

├── dependencies.py           # 依赖装配：get_settings、get_db、get_note_service

├── middleware/
│   └── exceptions.py         # 自定义异常类型

├── modules/
│   ├── notes/
│   │   ├── model.py          # SQLAlchemy 模型：Note 表
│   │   ├── schema.py         # Pydantic 模型：请求体 / 响应体
│   │   ├── repository.py     # 数据访问层：直接操作 Session
│   │   ├── service.py        # 业务逻辑层：组织 CRUD 规则
│   │   └── router.py         # HTTP 层：定义 /notes 接口
│   └── system/
│       ├── schema.py         # 健康检查响应模型
│       └── router.py         # /system/health 接口

└── tests/
    ├── conftest.py           # 测试环境初始化、依赖覆盖、测试数据库
    ├── test_notes_api.py     # notes 模块接口测试
    └── test_system_api.py    # system 模块接口测试
```

这个结构的核心是按业务域组织模块，再把共性的基础设施上提到 `core/`、`dependencies.py` 和 `middleware/`。

## 1.2 FastAPI 模块分布

FastAPI 工程里常见的模块分布可以画成：

```text
应用对象
├── fastapi.FastAPI                 # 应用入口对象：路由、中间件、异常、生命周期
└── fastapi.APIRouter               # 路由模块对象：拆分业务接口

参数声明
├── fastapi.Query                   # 查询参数声明
├── fastapi.Path                    # 路径参数声明
└── fastapi.Body                    # 请求体声明

依赖注入
└── fastapi.Depends     # 依赖入口：service、repository、db、settings、current_user

请求响应
├── fastapi.Request                 # 原始请求对象
├── fastapi.Response                # 原始响应对象
└── fastapi.responses.*             # 具体响应类型：JSONResponse 等

异常处理
├── fastapi.HTTPException           # 标准 HTTP 异常
└── @app.exception_handler(...)     # 自定义异常到响应的映射入口

中间件
└── @app.middleware("http")         # 请求链路包装器：日志、耗时、CORS、trace id

服务器
└── uvicorn                         # ASGI 服务器：监听端口并调用 FastAPI app
```

这些模块的关系可以压成一句：

```text
uvicorn -> FastAPI app -> router -> depends -> service -> repository
```

## 1.3 后端依赖图

先看当前这个项目已经落地的依赖主线：

```text
接口层
├── fastapi                        # Web 框架
└── uvicorn                        # ASGI 服务器

数据模型与配置层
├── pydantic                       # 请求体 / 响应体 / 数据模型
└── pydantic-settings              # .env / 环境变量配置对象

数据库层
├── sqlalchemy                     # ORM / Session / SQL 抽象
└── psycopg                        # PostgreSQL 驱动

测试层
├── pytest                         # 测试框架
├── httpx                          # 测试客户端
└── anyio / pytest-asyncio         # 异步测试支持
```

这一组已经足够覆盖一个典型后端的最小工程闭环：

- 接口定义
- 配置管理
- 数据库连接
- 依赖注入
- 接口测试

如果扩展到一个更完整的大型后端，常见依赖图还会继续长成：

```text
数据库层
├── asyncpg / pymysql 等其他数据库驱动
└── alembic                        # 数据库迁移

认证授权层
├── pyjwt / python-jose            # JWT 编解码
├── passlib / pwdlib / bcrypt      # 密码哈希
└── OAuth2 相关依赖               # 登录、鉴权、权限控制

缓存与消息层
├── redis                          # 缓存
├── celery / rq                    # 后台任务
└── kafka / rabbitmq 客户端        # 消息队列

运维与启动层
├── gunicorn（可选）               # 多 worker 部署
└── docker / compose / k8s 配套    # 容器化与编排
```

# 2. 工程目录内容

## 2.1 `main.py`

`main.py` 是应用装配层，不是业务实现层。

它主要负责：

- 创建 `FastAPI(...)`
- 注册 `router`
- 注册 `middleware`
- 注册 `exception_handler`
- 注册 `lifespan`

它和 `uvicorn` 的关系是：

```text
浏览器 -> uvicorn -> FastAPI app(main.py)
```

常见启动命令：

```bash
uv run uvicorn src.app.main:app --reload
```

各部分含义：

- `uv run`：在项目环境中运行命令
- `uvicorn`：启动 ASGI 服务器
- `src.app.main:app`：加载 `src/app/main.py` 中的 `app` 对象
- `--reload`：文件变化后自动重启，适合开发环境

不要把具体 CRUD、数据校验规则、数据库操作写进 `main.py`。

## 2.2 `middleware`

`middleware` 放横切逻辑。

当前项目里主要包括：

- 自定义异常类型
- 统一请求日志中间件

后续也可以扩展：

- trace id
- 认证前置处理
- 统一审计日志

## 2.3 `core/config.py`

`core/config.py` 负责定义配置对象结构，并从 `.env` / 环境变量中读取配置。

它解决的是：

- 配置项有哪些
- 配置值从哪里来
- 配置值怎么做类型转换与校验

这个文件的核心对象通常是 `Settings(BaseSettings)`。

典型写法：

```python
# src/app/core/config.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Todo API")
    database_url: str = Field(description="数据库连接地址")

    model_config = SettingsConfigDict(
        env_prefix="FASTAPI_",
        env_file=".env",
        extra="ignore",
    )
```

这里的关键点：

- `Settings` 继承 `BaseSettings`
- 字段定义的是配置项结构，不是手写赋值逻辑
- `SettingsConfigDict(...)` 指定配置来源和读取规则

例如：

```env
FASTAPI_DATABASE_URL=postgresql+psycopg://fastapi_user:xxx@localhost:5433/fastapi_study
```

当执行：

```python
settings = Settings()
```

时，`pydantic-settings` 会自动做映射：

```text
FASTAPI_DATABASE_URL -> database_url
```

也就是说，代码里通常不会出现：

```python
database_url = os.getenv("FASTAPI_DATABASE_URL")
```

这种手写赋值，而是由 `BaseSettings` 在实例化时自动完成“读取 -> 映射 -> 类型转换 -> 校验”。

`env_file` 用来指定 `.env` 文件位置；`env_prefix` 用来约束只读取 `FASTAPI_` 开头的变量。数据库连接这类配置通常应设为必填项，没提供就应在启动时直接报错，而不是偷偷回退到其他数据库。

## 2.4 `core/db.py`

`core/db.py` 负责数据库基础设施，而不是业务数据访问。

典型内容包括：

- 创建 `engine`
- 创建 `sessionmaker`
- 提供数据库连通性检查函数

也就是说，它只负责“数据库怎么连、会话怎么造”，不负责“笔记怎么查”。

## 2.5 `dependencies.py`

`dependencies.py` 是依赖装配中心。

典型依赖包括：

- `get_settings()`
- `get_db()`
- `get_note_repository()`
- `get_note_service()`

这个文件的重点不是写业务，而是定义对象之间的装配关系。

## 2.6 `modules/*/router.py schema.py service.py repository.py model.py`

按业务域组织的模块里，常见文件分工是：

- `router.py`
  - HTTP 层
  - 负责路径、参数、响应模型、状态码

- `schema.py`
  - Pydantic 模型
  - 负责请求体、响应体、字段校验

- `service.py`
  - 业务逻辑层
  - 负责规则、流程编排、异常抛出

- `repository.py`
  - 数据访问层
  - 负责直接操作 `Session`

- `model.py`
  - SQLAlchemy 模型
  - 负责表结构与 ORM 映射

## 2.7 `tests`

`tests` 负责验证接口行为，而不是只做“代码能跑”的演示。

当前项目测试层已经覆盖：

- notes CRUD 行为
- system health 行为
- 数据库依赖覆盖
- lifespan 启动流程

# 3. 常用接口写法

## 3.1 路由与路径操作

常用入口：

- `@app.get(...)`
- `@app.post(...)`
- `@app.put(...)`
- `@app.patch(...)`
- `@app.delete(...)`
- `APIRouter(...)`

大多数实际项目不会把所有路由写在 `app` 上，而是拆到多个 `router` 中，再由 `main.py` 统一注册。

## 3.2 路径参数、查询参数、请求体

FastAPI 通过函数签名来判断参数来源：

- 路径里声明过的参数 -> 路径参数
- 普通基础类型参数 -> 查询参数
- `BaseModel` 参数 -> 请求体

## 3.3 Pydantic 模型

在按业务域组织的项目里，Pydantic 模型通常放在 `modules/<业务>/schema.py`。

一组接口模型通常分几类：

- `XXCreate`：创建请求体
- `XXUpdate`：全量更新请求体
- `XXPartialUpdate`：部分更新请求体
- `XXResponse`：响应体

作用：

- 定义字段结构
- 做类型校验
- 自动生成文档

例如 `notes` 模块里可以写成：

```python
# src/app/modules/notes/schema.py
class NoteCreate(BaseModel):
    ...


class NoteUpdate(BaseModel):
    ...


class NotePartialUpdate(BaseModel):
    ...


class NoteResponse(BaseModel):
    ...
```

## 3.4 响应模型与状态码

常见用法：

- `response_model=...`
- `status_code=201`
- 显式返回 `JSONResponse` 或其他 `Response`

`response_model` 的作用不只是文档，更重要的是约束响应结构。

## 3.5 `Depends`

`Depends(...)` 是 FastAPI 里的依赖注入入口。

最常见的使用场景不是“传业务参数”，而是“注入运行时对象”。

常见用途：

- 注入 service
- 注入 repository
- 注入数据库 session
- 注入当前用户
- 注入配置对象

典型写法：

```python
# src/app/dependencies.py
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.modules.notes.repository import NoteRepository
from app.modules.notes.service import NoteService

def get_note_repository(
    db: Session = Depends(get_db),
) -> NoteRepository:
    return NoteRepository(db)


def get_note_service(
    repository: NoteRepository = Depends(get_note_repository),
) -> NoteService:
    return NoteService(repository)
```

```python
# src/app/modules/notes/router.py
from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_note_service
from app.modules.notes.schema import NoteCreate, NoteResponse
from app.modules.notes.service import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteResponse)
async def create_note(
    note: NoteCreate,
    service: Annotated[NoteService, Depends(get_note_service)],
):
    return service.create_note(note)
```

这里的 `service` 不是来自客户端请求，而是由 FastAPI 在执行路由函数前自动提供。

可以把 `Depends(...)` 理解成一句声明：

> 这个参数不要从请求里取，而是通过某个依赖函数生成。

开发时可以把依赖分成几类：

- 业务依赖：`service`、`repository`
- 基础设施依赖：数据库 session、缓存客户端、配置对象
- 认证授权依赖：当前用户、权限校验、租户信息
- 请求上下文依赖：trace id、语言环境、请求级状态

一个实用原则：

- 业务数据参数走路径、查询、请求体
- 运行时对象参数走 `Depends(...)`

所以像 `note_id`、`skip`、`note` 这种属于请求数据，不该用 `Depends`；而 `service`、`db`、`current_user` 这类对象，适合走 `Depends`。

在大型一点的项目里，`Depends` 通常不会直接写复杂逻辑，而是配合 `dependencies.py` 使用，把依赖装配集中管理。

这一节先把它当“接口层怎么写”来看；它在底层是怎么解析和执行的，放到 `4.3 依赖注入机制` 再展开。

## 3.6 `middleware` 与 `exception_handler`

常用接口：

- `@app.middleware("http")`
- `@app.exception_handler(...)`

前者处理横切逻辑，后者处理异常到响应的映射。

# 4. 核心机制

## 4.1 参数注入

FastAPI 在调用路由函数之前，会先分析函数签名，再为每个参数判定来源并完成注入。路由函数看起来像普通 Python 函数，但真正执行前已经过了一轮参数解析、类型转换和依赖装配。

```python
@router.get("/notes/{note_id}")
async def get_note(
    note_id: int,
    skip: int = 0,
    service: Annotated[NoteService, Depends(get_note_service)],
):
    ...
```

上面这个函数里，三个参数的来源并不一样：

- `note_id`：路径参数，来自 `/notes/{note_id}`
- `skip`：查询参数，来自 `?skip=...`
- `service`：依赖注入参数，来自 `Depends(get_note_service)`

如果是这样的写法：

```python
@router.post("/notes")
async def create_note(note: NoteCreate):
    ...
```

那么 `note` 会被识别为请求体参数，FastAPI 会从 JSON 请求体中解析数据，再实例化成 `NoteCreate`。

可以先把参数来源记成这几类：

- 路径参数：在路由路径中声明过的参数
- 查询参数：普通基础类型参数，且不在路径中出现
- 请求体参数：`BaseModel`、`dataclass` 等结构化对象
- 依赖参数：通过 `Depends(...)` 声明的参数
- 其他协议参数：`Request`、`Response`、`Header`、`Cookie`、`File`、`Form` 等特殊类型或声明

一个请求进入后，大致流程是：

```text
匹配路由
-> 读取路由函数签名
-> 判断每个参数的来源
-> 从 URL / query / body / 依赖系统中取值
-> 做类型转换和校验
-> 组装成函数调用参数
-> 执行路由函数
```

这里最关键的一点是：FastAPI 不是按参数名字硬编码取值，而是综合以下信息做判断：

- 路由路径模板
- 参数类型注解
- 参数默认值
- `Query(...)`、`Path(...)`、`Body(...)`、`Depends(...)` 这类声明

所以参数注入其实是一个总机制，后面的请求体解析和依赖注入，只是它的两个重要子场景。

## 4.2 请求体解析机制 (Pydantic & Dataclass)

FastAPI 会根据路由函数的参数类型注解，自动解析请求体 JSON 并实例化模型。这一过程发生在你的函数代码执行之前。

FastAPI 只能自动实例化带有结构化字段元数据的类：

```python
┌────────────────────┬─────────────────────────────────────────┬───────────────────────────┐
│        类型        │                  示例                   │           能力            │
├────────────────────┼─────────────────────────────────────────┼───────────────────────────┤
│ Pydantic BaseModel │ class NoteCreate(BaseModel): title: str │ ✅ 解析 + 验证 + 错误信息 │
├────────────────────┼─────────────────────────────────────────┼───────────────────────────┤
│ dataclass          │ @dataclass class NoteCreate: title: str │ ✅ 解析（不做强类型验证） │
├────────────────────┼─────────────────────────────────────────┼───────────────────────────┤
│ 普通 class         │ class NoteCreate: def __init__...       │ ❌ 不支持                 │
└────────────────────┴─────────────────────────────────────────┴───────────────────────────┘
```

为什么普通类不支持？

普通类的 `__init__` 里可以写任意逻辑，比如查库、计算、调用 API。FastAPI 无法预知如何把 JSON 映射到它上面。Pydantic 和 dataclass 则通过类型注解暴露了字段信息，FastAPI 才能读取并自动实例化。

执行流：

```text
浏览器 POST /notes，Body: {"title": "hello"}
       ↓
FastAPI 读取签名: def create(note: NoteCreate)
       ↓
FastAPI 解析 JSON -> dict
       ↓
实例化: NoteCreate(title="hello")  <- 验证在这里发生
       ↓
验证通过 -> 调用你的函数: create(note=NoteCreate实例)
验证失败 -> 直接返回 422，你的函数不执行
```

关键点：

- 实例化由 FastAPI 在幕后完成，不是 Python 原生语法
- Python 类型注解本身只起标注作用，真正消费这些信息的是 FastAPI
- 函数内拿到的参数已经是实例化后的对象，可直接调用 `.model_dump()` 等方法

## 4.3 依赖注入机制

依赖注入的核心是：对象不要在函数内部手动创建，而是交给外部装配。

如果没有依赖注入，路由函数里很容易出现这种代码：

```python
@router.post("/notes")
async def create_note(note: NoteCreate):
    repository = NoteRepository(db)
    service = NoteService(repository)
    return service.create_note(note)
```

这样会有几个问题：

- 路由层承担了对象装配责任
- 具体实现写死，后续不好替换
- 测试时不容易注入测试替身

FastAPI 的做法是：由 `Depends(...)` 声明“这个参数应该怎么获得”，路由层只声明自己需要什么。

典型写法：

```python
from sqlalchemy.orm import Session


def get_note_repository() -> NoteRepository:
    return NoteRepository(db)

def get_note_service(
    repository: NoteRepository = Depends(get_note_repository),
) -> NoteService:
    return NoteService(repository)
```

这里有两层依赖关系：

- `get_note_repository()` 提供 `NoteRepository`
- `get_note_service(...)` 依赖 `get_note_repository()`，再提供 `NoteService`

路由层只声明自己需要什么：

```python
async def create_note(
    note: NoteCreate,
    service: NoteService = Depends(get_note_service),
):
    ...
```

或者用 `Annotated` 写成更明确的形式：

```python
NoteServiceDep = Annotated[NoteService, Depends(get_note_service)]

async def create_note(
    note: NoteCreate,
    service: NoteServiceDep,
):
    ...
```

这两种写法对 FastAPI 来说含义基本一致。区别只是：

- `service: NoteService = Depends(...)`：把依赖声明写在默认值位置
- `Annotated[NoteService, Depends(...)]`：把类型和来源拆开写

`Annotated` 在这里不是普通备注，而是给 FastAPI 附加了一段会被读取的元信息：

- 这个参数的类型是 `NoteService`
- 这个参数的值由 `Depends(get_note_service)` 提供

依赖解析的大致过程是：

```text
请求进入
-> FastAPI 读取路由函数签名
-> 发现 service 参数声明了 Depends(get_note_service)
-> 调用 get_note_service(...)
-> 发现它自身又依赖 get_note_repository()
-> 先执行 get_note_repository()
-> 再用返回值构造 NoteService
-> 将 NoteService 注入到路由函数
-> 执行路由函数
```

所以 `Depends(...)` 不只是“省略手动传参”，而是在声明一条依赖链。

好处：

- 解耦
- 可替换
- 好测试

测试里的依赖覆盖就是这个机制的直接应用：

```python
app.dependency_overrides[get_db] = lambda: db_session
```

这句的意思是：在测试环境里，不再使用正式的数据库会话依赖，而是改成返回测试会话。这样上层的 repository / service / router 不用改，底层数据源就已经被替换掉了。

### 4.3.1 `Depends(...)` 返回什么

`Depends(get_token)` 在定义阶段返回的不是 `get_token()` 的执行结果，而是一个 `fastapi.params.Depends` 实例。

它记录的是依赖描述信息，例如：

- 当前依赖函数是 `get_token`
- 是否启用依赖缓存

路由函数参数里最终拿到的真实值，是 FastAPI 在请求处理阶段执行 `get_token()` 之后得到的返回值。

### 4.3.2 `analyze_param()` 与 `get_dependant()`

FastAPI 在构建路由处理器时，会先读取函数签名，再把参数声明转换成内部依赖图。

关键函数：

- `analyze_param()`：解析参数注解，识别 `Annotated[...]` 里的 `Depends(...)`、`Query(...)`、`Body(...)` 等元信息
- `get_dependant()`：把当前路由函数及其依赖整理成 `Dependant` 对象树

可以把 `Dependant` 理解成一张结构化调用说明：

- 当前要调用哪个函数
- 每个参数来自哪里
- 哪些参数还要先通过其他依赖函数生成

例如：

```python
token: Annotated[str, Depends(get_token)]
```

在这一步被读取成的大致信息是：

- 参数名是 `token`
- 参数真实类型是 `str`
- 参数值不来自请求体或查询参数，而是来自依赖函数 `get_token`

### 4.3.3 `solve_dependencies()` 与 `run_endpoint_function()`

请求真正进入后，FastAPI 才开始把依赖描述转换成真实参数值。

关键执行顺序：

1. `solve_dependencies()` 递归解决子依赖
2. 收集路径参数、查询参数、请求体、请求对象等输入
3. 调用依赖函数
4. 把依赖函数返回值按参数名放进 `values` 字典
5. `run_endpoint_function()` 再用 `dependant.call(**values)` 调用路由函数

近似伪代码：

```python
values = {}

token_value = get_token()
values["token"] = token_value

read_me(**values)
```

所以真正传进路由函数的不是 `Depends(get_token)`，而是 `get_token()` 的返回值。

如果 `get_token()` 返回字符串，那么参数拿到的是字符串；如果它返回 `User()` 实例，那么参数拿到的就是 `User` 实例。

### 4.3.4 源码定位

和依赖注入直接相关的源码入口主要在两个文件：

- `fastapi/dependencies/utils.py`
  - `analyze_param()`
  - `get_dependant()`
  - `solve_dependencies()`
- `fastapi/routing.py`
  - `run_endpoint_function()`

查源码时可以先抓这条链路：

```text
路由函数签名
-> analyze_param()
-> get_dependant()
-> solve_dependencies()
-> run_endpoint_function()
```

## 4.4 异常处理机制

### 4.4.1 伪代码

```python
class FastAPI:
    handlers = {}

    def exception_handler(self, exc_type):
        def decorator(func):
            self.handlers[exc_type] = func
            return func
        return decorator

    def handle_request(self, request):
        try:
            response = route_handler(request)
        except Exception as exc:
            handler = self.handlers.get(type(exc))
            if handler:
                return handler(request, exc)
            return JSONResponse(status_code=500, content={"detail": str(exc)})
```

### 4.4.2 完整流程

```python
@app.exception_handler(NotFoundException)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, ...)

raise NotFoundException("Note")
```

FastAPI 内部处理过程：

```text
捕获异常
-> type(exc) 是 NotFoundException
-> 找到对应 handler
-> 调用 not_found_handler(request, exc)
-> 返回 JSONResponse
```

### 4.4.3 实际意义

- 业务代码里抛异常
- HTTP 层统一接住
- 响应结构保持一致

## 4.5 中间件调用链

中间件本质上是对整个请求处理过程做一层包装：

```python
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    return response
```

调用链可以理解为：

```text
请求进入
-> middleware 前置逻辑
-> route handler
-> middleware 后置逻辑
-> 返回响应
```

## 4.6 应用生命周期

应用除了处理请求，还会有启动和关闭两个阶段。

常见用途：

- 启动时建立数据库连接池
- 启动时加载配置或模型
- 关闭时释放资源

FastAPI 中通常通过 `lifespan` 来统一管理这类逻辑。

# 5. 工程实践

## 5.1 分层边界

- `router` 负责 HTTP
- `service` 负责业务
- `repository` 负责数据访问
- `dependencies` 负责装配

## 5.2 测试组织

测试至少分两类：

- 接口测试：直接请求 API，验证行为和响应
- 业务测试：直接调用 service，验证规则逻辑

依赖注入的一个核心价值是可以在测试里覆盖依赖。

## 5.3 常见反模式

- 把业务逻辑全堆在路由函数里
- 把数据库操作直接写在 router 中
- 不区分请求模型和响应模型
- 把依赖创建逻辑散落在各处
- 只有手工调接口，没有自动化测试
