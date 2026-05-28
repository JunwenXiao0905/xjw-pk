视频地址：

[从pip到uv：一口气梳理现代Python项目管理全流程！_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV13WGHz8EEz/?spm_id_from=333.1391.0.0)

# uv
视频地址：

[让uv管理Python的一切_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Stwfe1E7s/?spm_id_from=333.1391.0.0)

文章地址：

[https://juejin.cn/post/7553547794456739879?searchId=202510082035178CFA8D70AA1A76C4C6E7](https://juejin.cn/post/7553547794456739879?searchId=202510082035178CFA8D70AA1A76C4C6E7)



## 1.版本管理
查看uv支持的所有python版本

```powershell
uv python list
```

安装指定的python版本

```powershell
uv python install cpython-3.14
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2025/png/34655355/1759929590942-52e6955f-69d3-4525-ac93-52c00f2a8674.png)

使用指定python版本运行文件【会自动安装对应版本】

```powershell
uv run  -p 3.14 <script.py>
```

使用指定版本的交互界面【会自动安装对应版本】

```powershell
uv run -p 3.14 python
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2025/png/34655355/1759930085626-f27b72cf-88ba-4fca-bd0d-367d1f00059a.png)



## 2.项目初始化
```powershell
uv init -p 3.14  
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2025/png/34655355/1759931220610-ba680c5c-113b-4b27-85e1-4099b7833742.png)



## 3.单包项目
```typescript
  fastapi-study/
  ├── pyproject.toml          ← 一个配置
  ├── src/app/                ← 源码
  │   ├── __init__.py
  │   ├── main.py             ← FastAPI 入口
  │   ├── routers/            ← 路由
  │   ├── schemas/            ← Pydantic 模型
  │   └── services/           ← 业务逻辑
  └── tests/
```

## 3.workspace
```typescript
  [project]
  name = "fastapi-study"
  version = "0.1.0"
  description = "FastAPI 学习笔记项目 — Todo 笔记 API"
  requires-python = ">=3.12"
  readme = "README.md"

  [tool.uv.workspace]
  members = ["core", "api"]
```

 意思是：core/ 和 api/ 这两个目录各自是一个独立的 Python 包，但它们属于同一个 workspace。

  具体效果

  1. 共享依赖 — 两个包都用了 pydantic，workspace 只下载一次

  2. 互相引用 — api 可以 from core.utils import xxx，不需要 pip install core

  3. 统一安装 — 在根目录跑 uv sync，所有子包的依赖一起装好

  4. 独立运行 — uv run --package api ... 或 uv run --package core ...



  具象化

```typescript
  fastapi-study/          ← 根（workspace）
  ├── pyproject.toml      ← 根配置：members = ["core", "api"]
  ├── uv.lock             ← 所有子包的依赖统一锁定
  │
  ├── core/               ← 子包 1：共享工具
  │   ├── pyproject.toml  ← 独立配置
  │   └── src/core/utils.py
  │
  └── api/                ← 子包 2：FastAPI 应用
      ├── pyproject.toml  ← 独立配置，dependencies = ["core", "fastapi", ...]
      └── src/api/main.py
```

+ 根目录的 uv sync 会同时处理 core 和 api 的依赖
    - api 的 pyproject.toml 里写 "core"，就能直接导入 core 的代码
    - 两个包共享同一个 uv.lock，不会出现 core 用 fastapi 0.114、api 用 0.115 的冲突

子包中调用

第 1 步：api 声明对 core 的依赖。

  在 api/pyproject.toml 中：

```typescript
[project]
  name = "api"
  version = "0.1.0"
  requires-python = ">=3.12"
  dependencies = [
      "core",
      "fastapi>=0.115.0,<1.0.0",
  ]
```

  关键就这一行 "core" —— 告诉 uv：这个包依赖 workspace 里的 core 包。

  第 2 步：在 api 的代码中直接 import。

api/src/api/main.py

```typescript
 from core.utils import format_response

print(format_response({"hello": "world"}))
```

  原理

  uv 在 uv sync 时看到 "core"，会去找：

1. workspace 成员里有没有叫 core 的包？有 → core/pyproject.toml 里 name = "core"
2. 把它安装到虚拟环境中，作为可导入的包

  所以你写的 from core.utils import format_response 就能正常工作，不需要额外配置路径。



根目录调用

根的 pyproject.toml

```typescript
\ dependencies = ["core", "api"]
```

 # main.py（根目录）

```typescript
  from core.utils import format_response
  from api.main import app

  print(format_response({"status": "ok"}))
```



## 5.依赖管理
  声明 vs 安装

  声明：告诉项目"我需要什么包" —— 写在 pyproject.toml 里

  安装：把包下载到虚拟环境 —— 跑 uv sync 或 uv add



  两类依赖

```typescript
  dependencies = ["fastapi", "uvicorn"]        ← 生产依赖，代码运行时需要的
  [dependency-groups]
  dev = ["pytest"]                              ← 开发依赖，测试/构建时用的
```

  区别：生产部署时只装 dependencies，不装 dev（类似 dependencies vs devDependencies）。



  两个命令

```typescript
┌────────────────┬────────────────────────────────┬──────────────────┐
  │      命令      │            做了什么            │       类比       │
  ├────────────────┼────────────────────────────────┼──────────────────┤
  │ uv add fastapi │ 写入 pyproject.toml + 安装     │ pnpm add fastapi │
  ├────────────────┼────────────────────────────────┼──────────────────┤
  │ uv sync        │ 按 pyproject.toml 声明安装全部 │ pnpm install     │
  └────────────────┴────────────────────────────────┴──────────────────┘
```

  关系：uv add = 改配置 + 安装；uv sync = 只安装（不修改配置）



  --dev 和 --frozen

```typescript
  uv add --dev pytest           # 加到 dev 组并安装
  uv sync --no-dev              # 只装生产依赖（CI/CD 常用）
  uv sync --frozen              # 严格按 uv.lock 装，不解析新版本（保证可重复）
```



  uv.lock 的作用

  pyproject.toml 写:  fastapi>=0.115.0,<1.0.0    ← 范围

  uv.lock 记录:       fastapi==0.115.6            ← 精确版本



  uv sync 读 uv.lock，保证所有人装的都是同一个版本。





## 6.模块导入与路径解析
  **核心概念：sys.path**

  Python 导入模块时，会按 sys.path 列表中的目录依次查找。查看方式：

```python
  import sys
  print(sys.path)
```

**  Python 默认行为**

  运行 python src/app/main.py 时，Python 只把脚本所在目录 加进 sys.path，也就是 src/app/。

  此时代码中写 from app.routers.notes import xxx，Python 去 src/app/ 下找 app/ 目录 → 找不到 →

  ModuleNotFoundError。



**  uv run 做了什么**

  uv sync 时做了可编辑安装（editable install），把 src/ 注册进 Python 的导入路径。所以 uv run

  启动时，Python 能直接从 src/ 下找到 app/ 包。



**  对比表**

```python
  ┌─────────────────────────────┬────────────────────┬──────────────────────────┐
  │          运行方式           │   sys.path 包含    │ 能否 from app import ... │
  ├─────────────────────────────┼────────────────────┼──────────────────────────┤
  │ python src/app/main.py      │ src/app/           │ ❌                       │
  ├─────────────────────────────┼────────────────────┼──────────────────────────┤
  │ uv run uvicorn app.main:app │ src/（可编辑安装） │ ✅                       │
  └─────────────────────────────┴────────────────────┴──────────────────────────┘
```



**  src layout**

  Python 工程实践推荐把源码放在 src/ 下，防止开发时误导入未安装的代码。uv 的 src layout

  项目自动处理可编辑安装，不需要手动配路径

# conda


# 
# 编辑器
## pyCharm


### 
## vscode


