# Python 项目管理

## 目录

- [第1章 版本管理](#第1章-版本管理)
  - [1.1 查看可用版本](#11-查看可用版本)
  - [1.2 安装指定版本](#12-安装指定版本)
  - [1.3 `.python-version`](#13-python-version)
  - [1.4 临时指定版本](#14-临时指定版本)
- [第2章 项目初始化](#第2章-项目初始化)
  - [2.1 `uv init`](#21-uv-init)
  - [2.2 src layout](#22-src-layout)
- [第3章 CLI 入口](#第3章-cli-入口)
  - [3.1 `[project.scripts]`](#31-projectscripts)
  - [3.2 `uv run` 的三种调用方式](#32-uv-run-的三种调用方式)
- [第4章 依赖管理](#第4章-依赖管理)
  - [4.1 声明 vs 安装](#41-声明-vs-安装)
  - [4.2 `uv add`](#42-uv-add)
  - [4.3 `uv sync`](#43-uv-sync)
  - [4.4 两类依赖](#44-两类依赖)
  - [4.5 `uv.lock`](#45-uvlock)
  - [4.6 常用选项](#46-常用选项)
- [第5章 Workspace](#第5章-workspace)
  - [5.1 声明](#51-声明)
  - [5.2 效果](#52-效果)
  - [5.3 目录结构](#53-目录结构)
  - [5.4 子包互引](#54-子包互引)
  - [5.5 根目录调用](#55-根目录调用)
- [第6章 导入与路径](#第6章-导入与路径)
  - [6.1 `sys.path`](#61-syspath)
  - [6.2 `python` vs `uv run`](#62-python-vs-uv-run)

## 第1章 版本管理

### 1.1 查看可用版本

```bash
uv python list
```

### 1.2 安装指定版本

```bash
uv python install cpython-3.13
```

### 1.3 `.python-version`

项目根目录下放 `.python-version` 文件，内容为版本号：

```
3.13
```

`uv run`、`uv sync` 等命令会自动读取此文件。如果该版本未安装，uv 会自动下载安装。

等效于每次手动指定 `-p 3.13`。

### 1.4 临时指定版本

```bash
uv run -p 3.14 python        # 用 3.14 打开交互界面
uv run -p 3.14 script.py     # 用 3.14 运行脚本
```

## 第2章 项目初始化

### 2.1 `uv init`

```bash
uv init -p 3.13
```

生成：

```
project/
├── pyproject.toml       # 项目元数据与依赖声明
├── .python-version      # 锁定 Python 版本
├── README.md
└── hello.py             # 示例入口
```

### 2.2 src layout

Python 工程实践推荐把源码放在 `src/` 下，防止开发时误导入未安装的代码。

```
project/
├── pyproject.toml
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── routers/
│       ├── schemas/
│       └── services/
└── tests/
```

uv 对 src layout 项目自动做可编辑安装，不需要手动配路径（详见第6章）。

## 第3章 CLI 入口

### 3.1 `[project.scripts]`

在 `pyproject.toml` 中定义命令名到函数的映射：

```toml
[project.scripts]
lg-tutorial = "lg_tutorial.main:main"
```

格式为 `命令名 = "模块路径:函数名"`。`uv sync` 后即可用：

```bash
uv run lg-tutorial
```

等价于：

```bash
uv run python -m lg_tutorial.main
```

可以定义多个入口：

```toml
[project.scripts]
lg-tutorial = "lg_tutorial.main:main"
dev = "app.main:dev"
```

### 3.2 `uv run` 的三种调用方式

```bash
uv run <script>              # 执行 [project.scripts] 中定义的命令
uv run python script.py      # 直接运行脚本（在虚拟环境中）
uv run python -m module      # 以模块方式运行
```

`uv run` 保证代码运行在项目的虚拟环境中，不需要先手动激活 `.venv`。

## 第4章 依赖管理

### 4.1 声明 vs 安装

- **声明**：写在 `pyproject.toml` 里，告诉项目"需要什么包"
- **安装**：把包下载到虚拟环境，通过 `uv sync` 或 `uv add`

### 4.2 `uv add`

```bash
uv add fastapi          # 写入 pyproject.toml + 安装
uv add --dev pytest     # 加到 dev 依赖组并安装
```

`uv add` = 改配置 + 安装。

### 4.3 `uv sync`

```bash
uv sync                 # 按 pyproject.toml 安装全部依赖
uv sync --no-dev        # 只装生产依赖（CI/CD 常用）
uv sync --frozen        # 严格按 uv.lock 装，不解析新版本
```

`uv sync` = 只安装，不修改配置。

### 4.4 两类依赖

```toml
dependencies = ["fastapi", "uvicorn"]     # 生产依赖

[dependency-groups]
dev = ["pytest"]                           # 开发依赖
```

生产部署时只装 `dependencies`，不装 `dev`。

### 4.5 `uv.lock`

`pyproject.toml` 写范围，`uv.lock` 记录精确版本：

```
pyproject.toml:  fastapi>=0.115.0,<1.0.0   # 范围
uv.lock:         fastapi==0.115.6           # 精确版本
```

`uv sync` 读 `uv.lock`，保证所有人装的都是同一个版本。`uv.lock` 应提交到 Git。

### 4.6 常用选项

```bash
uv add --dev pytest                  # 加到 dev 组
uv sync --no-dev                     # 跳过 dev 依赖
uv sync --frozen                     # 不解析版本，严格按 lock 文件安装
uv lock --upgrade-package fastapi    # 升级单个包
```

## 第5章 Workspace

### 5.1 声明

根 `pyproject.toml` 中：

```toml
[tool.uv.workspace]
members = ["core", "api"]
```

表示 `core/` 和 `api/` 各自是独立 Python 包，但同属一个 workspace。

### 5.2 效果

1. **共享依赖** — 两个包都用了 pydantic，workspace 只下载一次
2. **互相引用** — api 可以直接 `from core.utils import xxx`
3. **统一安装** — 在根目录跑 `uv sync`，所有子包的依赖一起装好
4. **独立运行** — `uv run --package api ...` 或 `uv run --package core ...`
5. **统一 lock** — 两个包共享 `uv.lock`，不会出现版本冲突

### 5.3 目录结构

```
fastapi-study/           # 根（workspace）
├── pyproject.toml       # members = ["core", "api"]
├── uv.lock              # 所有子包统一锁定
├── core/                # 子包 1：共享工具
│   ├── pyproject.toml
│   └── src/core/utils.py
└── api/                 # 子包 2：FastAPI 应用
    ├── pyproject.toml   # dependencies = ["core", "fastapi"]
    └── src/api/main.py
```

### 5.4 子包互引

`api/pyproject.toml` 中声明对 core 的依赖：

```toml
[project]
name = "api"
dependencies = [
    "core",
    "fastapi>=0.115.0,<1.0.0",
]
```

然后在 api 代码中直接 import：

```python
from core.utils import format_response
```

uv 在 `uv sync` 时看到 `"core"`，会去 workspace 成员里找 `name = "core"` 的包，把它安装到虚拟环境中。

### 5.5 根目录调用

根 `pyproject.toml` 中声明依赖子包：

```toml
dependencies = ["core", "api"]
```

之后根目录代码可以直接导入：

```python
from core.utils import format_response
from api.main import app
```

## 第6章 导入与路径

### 6.1 `sys.path`

Python 导入模块时，按 `sys.path` 列表中的目录依次查找：

```python
import sys
print(sys.path)
```

### 6.2 `python` vs `uv run`

| 运行方式 | `sys.path` 包含 | `from app import ...` |
|----------|----------------|----------------------|
| `python src/app/main.py` | `src/app/` | 失败 |
| `uv run python -m app.main` | `src/`（可编辑安装） | 成功 |

直接 `python src/app/main.py` 时，Python 只把脚本所在目录 `src/app/` 加入 `sys.path`。代码中 `from app.routers.notes import xxx` 在这个目录下找不到 `app/`。

`uv sync` 对 src layout 项目做了**可编辑安装**（editable install），把 `src/` 注册进 Python 导入路径。因此 `uv run` 启动时，Python 能直接从 `src/` 下找到 `app/` 包，不需要手动配 `PYTHONPATH`。
