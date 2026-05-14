视频地址：[3小时超快速入门Python | 动画教学【2025新版】【自学Python教程】【零基础Python】【计算机二级Python】【Python期末速成】_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Jgf6YvE8e?spm_id_from=333.788.videopod.episodes&vd_source=e9c45fdc03639b59ab05f66211ecc1cb)



# 数据类型
##   元类（metaclass）
  "创建类的类"。普通类创建对象，元类创建类。Pydantic 用元类（或 __init_subclass__）在类定义时自动读取类型注解，注入 __init__ 方法。

```python
  class NoteCreate(BaseModel):
      title: str
  # ↑ 这行执行时，元类扫描 title: str，自动生成 __init__ 方法
  # 你不用自己写构造函
```

## 数据类型转换方法
int()

float()

str()



# 交互模式


1.文件/命令行模式

## 2.交互模式
打开python控制台，或者在命令行输入python即可

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2025/png/34655355/1757946317535-b7742204-6390-40b2-9b92-3653da8baf07.png)<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2025/png/34655355/1757946390498-aa4e3d3b-7b42-45f8-9b49-bb5ef5588c2b.png)



退出交互模式

ctrl + d 或者 输入 quit()



# Python 文件结构
+ 模块本质：每个`.py`就是一个模块，导入或运行皆可。
+ 名称标识：`__name__`为模块名；脚本直接运行时为`'__main__'`。
+ 入口保护：`if __name__ == '__main__':`只在脚本运行时执行，导入不执行；用于`main()`、CLI、示例/快速测试。
+ 入口模式：
    - 定义`def main(): ...`，在入口保护中调用`main()`。
    - 避免在模块顶层做重操作（网络/数据库/I/O），延迟到`main()`或函数里。
+ 导入原则：
    - 顶层脚本用绝对导入：`from biz.llm.factory import LLMFactory`。
    - 包内模块间可用相对导入：`from .client.openai import OpenAIClient`、`from ..utils import dir_util`。
+ 名称导出：模块中可用`__all__`限制`from module import *`的导入集合；更推荐显式导入，避免星号污染。
+ 类型与依赖：复杂依赖的类型提示可用`if typing.TYPE_CHECKING:`防止运行时导入重依赖。
+ 运行方式：保持包语义用`python -m package.module`，例如`python -m biz.llm.client.openai`。

# 包管理知识
+ 包定义：目录作为包；传统包需要`__init__.py`，导入包时会执行其中代码。
+ `__init__.py`职责：
    - 轻量初始化（版本、常量）：`__version__ = '1.0.0'`。
    - 重导出统一入口：`from .factory import LLMFactory`；配合`__all__ = ['LLMFactory']`定义公共API。
    - 避免重操作（网络/扫描），降低导入开销。
+ 相对导入语义：
    - `.`当前包、`..`父包；按包层级解析，不是文件路径。
    - 不能越过顶层包，否则`ImportError: beyond top-level package`。
    - 顶层脚本不在任何包内，不能使用`from .xxx import ...`。
+ 包边界与命名空间：
    - 顶层包由导入名首段与`sys.path`上的目录共同决定（如`biz`）。
    - 模块的`__package__`标识所属包（如`biz.llm.client`）；包搜索路径见`__spec__.submodule_search_locations`。
+ 隐式包（PEP 420）：
    - 无`__init__.py`也可成为包；适合跨分发/插件化，将同名包目录在多个路径合并。
    - 顶层包不能写初始化代码；你的项目已是传统包，更直观、易维护。
+ 发布打包：
    - 传统包用`setuptools.find_packages()`；命名空间包用`find_namespace_packages()`或在`pyproject.toml`选择相应finder。
+ 最佳实践：
    - 包内用相对导入，跨包用绝对导入。
    - 明确公共API并重导出，星号导入谨慎使用。
    - `__init__.py`保持轻量；入口逻辑放到`if __name__ == '__main__'`下或独立CLI。

# 装饰器
+ 装饰器是一个“可调用对象”，接受一个函数或类，返回一个被“包装/替换”后的新对象。
+ `@` 是语法糖：把“定义时的包裹逻辑”从手写改为一行声明。
+ 典型用途：日志/统计、权限校验、缓存、重试、输入校验、注册（Flask 路由）、将函数转为类方法等。

**基本语法**

+ 无参装饰器：`@decorator` 等价于 `func = decorator(func)`。
+ 带参装饰器：`@decorator(a, b)` 等价于 `func = decorator(a, b)(func)`（外层先接参数，返回真正的装饰器）。
+ 叠加装饰器顺序（从上到下应用）：  
`@dec1`  
`@dec2`  
`def f(...): ...`  
等价于 `f = dec1(dec2(f))`（离函数最近的 `dec2` 先包裹，再被 `dec1` 包裹）。

**执行时机**

+ 装饰发生在“函数定义完成后、模块导入时”，不是在函数调用时。
+ 因此任何注册行为（如 Flask 的路由登记）会在导入模块时立即生效。

**Flask 中的 **`route`

+ 你的代码 `api_app = Flask(__name__)` 创建了一个 Flask 应用实例。
+ `@api_app.route('/review/webhook', methods=['POST'])` 是“带参装饰器”，用来注册视图函数到该实例。
+ 简化理解（接近 Flask 源码的伪码）：

```plain
def route(self, rule, **options):
    def decorator(f):
        endpoint = options.get('endpoint', f.__name__)
        self.add_url_rule(rule, endpoint=endpoint, view_func=f, **options)
        return f  # 通常原样返回，注册完成
    return decorator
```

+ 叠加顺序在 Flask 非常重要：  
    - 推荐把 `@api_app.route(...)` 放在“最上面”，以确保 Flask 注册的是“已经被其他装饰器包装后的最终函数”。  
    - 例如：

```plain
@api_app.route('/review/webhook', methods=['POST'])
@require_json
def handle_webhook():
    ...
```

等价于 `handle_webhook = api_app.route(...)(require_json(handle_webhook))`，路由注册的是 `require_json(handle_webhook)`（正确）。

    - 如果你写成：

```plain
@require_json
@api_app.route('/review/webhook', methods=['POST'])
def handle_webhook():
    ...
```

等价于 `handle_webhook = require_json(api_app.route(...)(handle_webhook))`，路由在装饰前已注册原函数，`require_json` 后续不会影响已注册的视图（常见坑）。

**自己写一个装饰器（与 Flask 结合）**

+ 无参版（保持函数元数据以免影响 Flask 端点名）：  

```plain
from functools import wraps
from flask import request, jsonify

def require_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Invalid data format'}), 400
        return f(*args, **kwargs)
    return wrapper

@api_app.route('/review/webhook', methods=['POST'])
@require_json
def handle_webhook():
    # 这里可以安全地读取 JSON
    data = request.get_json()
    ...
```

+ 带参版（装饰器工厂）：  

```plain
from functools import wraps

def require_header(name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            from flask import request, jsonify
            if not request.headers.get(name):
                return jsonify({'error': f'Missing header: {name}'}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator

@api_app.route('/review/webhook', methods=['POST'])
@require_header('X-GitHub-Event')  # 示例：要求存在某个头
def handle_webhook():
    ...
```

**保留函数元数据**

+ 使用 `functools.wraps` 装饰包装函数，保留原函数的 `__name__`、文档、注解等：
    - 对 Flask 很重要，因为默认端点名取自函数名；不使用 `@wraps` 时函数名可能变成 `wrapper`，影响 `url_for` 等。

**常见陷阱**

+ 忘记 `@wraps` 导致端点名/调试信息变更。
+ 包装函数没有写 `*args, **kwargs`，使签名不兼容，导致视图或被装饰函数无法接收参数。
+ 带参装饰器忘记加括号：`@retry` 与 `@retry()` 语义不同（前者是无参装饰器，后者才是带参）。
+ Flask 路由的叠加顺序写反，导致注册的不是最终包装后的函数。
+ 在导入时执行重度逻辑（装饰器里做耗时任务），会拖慢应用启动。

**内置常见装饰器**

+ `@staticmethod`、`@classmethod`、`@property`：面向对象方法语义转换。
+ `@dataclass`：为类自动生成初始化/比较等方法。
+ `@lru_cache`：缓存函数返回值。
+ `@pytest.mark.*`、`@click.command` 等：第三方框架常见的“声明式”注册用法，与 Flask 路由设计相似。

总结：`@api_app.route('/review/webhook', methods=['POST'])` 是一个带参装饰器工厂，它在模块导入时把下面的函数注册为处理 `POST /review/webhook` 的视图；叠加其他装饰器时，让路由装饰器放在最上面，使用 `@wraps` 保持函数元数据，这样 Flask 注册的就是你期望的“最终、已包装”的视图函数。**结论**

+ 可以理解为“回调函数”。在 Flask 中它更常称为“视图函数/路由处理器”，本质都是把一个函数注册给框架，框架在匹配到请求时回调执行。

**等价类比（Express.js）**

+ Python（你的代码）：
    - `@api_app.route('/review/webhook', methods=['POST'])`
    - `def handle_webhook(): ...`
+ JavaScript（Express）：

```plain
const express = require('express');
const app = express();
app.use(express.json()); // 解析 JSON 请求体

app.post('/review/webhook', (req, res) => {
  const data = req.body;
  if (!data) return res.status(400).json({ error: 'Invalid JSON' });

  const webhookSource = req.get('X-GitHub-Event');
  if (webhookSource) {
    // GitHub webhook
    return res.json({ source: 'github', event: webhookSource, ok: true });
  }
  // GitLab webhook
  return res.json({ source: 'gitlab', ok: true });
});
```

+ 语义对齐：
    - Flask 的路由装饰器把 `handle_webhook` 注册到 `POST /review/webhook`，收到请求时由框架调用。
    - Express 的 `app.post('/review/webhook', handler)` 把 `handler` 作为回调，收到请求时由框架调用。

**关键差异**

+ 注册方式
    - Flask：用装饰器语法 `@api_app.route(...)`（定义时注册，模块导入即生效）。
    - Express：把函数直接作为参数传给 `app.post(...)`（运行时注册）。
+ 请求与响应的传递
    - Flask：不传参接收 `request`，它是上下文代理；通过返回值生成响应（`return jsonify(...)`）。
    - Express：回调参数显式传入 `req`、`res`；通过调用 `res.json()`、`res.send()` 来发送响应。
+ 同步/异步
    - Flask（WSGI）默认同步；也支持 `async def`（需兼容的服务器/模式）。
    - Express/Node 回调天然面向异步；也能返回 Promise/使用 `async/await`。
+ 中间件/装饰器用法
    - Flask：装饰器叠加、`@before_request`/`@after_request` 钩子、`@errorhandler`。
    - Express：`app.use(...)` 中间件链、`next(err)` 错误处理、路由级中间件。
+ JSON 解析
    - Flask：`request.is_json` + `request.get_json()`；需 `Content-Type: application/json`。
    - Express：需先 `app.use(express.json())` 才有 `req.body`。

**术语建议**

+ 在 Python/Flask 社区更常用“视图函数”“路由处理器”“endpoint”，但把它理解为“由框架在请求到来时触发的回调函数”完全没问题，便于与前端/Node 经验建立直觉映射。

如果你愿意，我可以把这段对照示例和说明整理成一页 Markdown 小笔记，放进 `doc/`，并补充一张“请求流程图（Flask 与 Express 对照）”帮你记忆。





# Python类型


# Python模块
 每个 .py 文件自动就是模块，不需要 export。文件里定义的所有名字，导入后直接可用。

```python
# notes.py
def get_note():
    pass

def delete_note():
    pass
```

```typescript
  // JS: 需要 export
  export function getNote() {}
  export function deleteNote() {}
```

  导入方式

```python

  # 导入整个模块
  import app.routers.notes
  app.routers.notes.get_note()          # 必须带完整路径

  # 导入具体名字（最常用）
  from app.routers.notes import get_note, delete_note
  get_note()                            # 直接用

  # 导入模块并起别名
  from app.routers import notes as notes_router
  notes_router.get_note()
```

 等价 JS：

```typescript
// import 整个模块
import * as notes from './notes'
notes.getNote()

// 具名导入
import { getNote, deleteNote } from './notes'
getNote()

// 别名导入
import * as notesRouter from './notes'
```

 __init__.py 控制导出

  __init__.py 的作用类似 index.ts —— 统一暴露、控制导出范围：

```python
# routers/__init__.py
from .notes import router as notes_router   # 把子模块的名字收集到这里

__all__ = ["notes_router"]                  # 控制 from routers import * 的范围
```

 等价 JS：

```typescript
// routers/index.ts
export { router as notesRouter } from './notes'
```

  相对 vs 绝对导入

```python
# 绝对导入（推荐，从 src/ 根开始）
from app.routers.notes import get_note

# 相对导入（同级目录用 .）
from .notes import get_note          # 同目录
from ..schemas import NoteCreate     # 上一级
```

核心区别

```python
  ┌──────────┬────────────────────────────────────────┬──────────────────────────────────┐
  │          │               JavaScript               │              Python              │
  ├──────────┼────────────────────────────────────────┼──────────────────────────────────┤
  │ 标记模块 │ export                                 │ 任何 .py 文件                    │
  ├──────────┼────────────────────────────────────────┼──────────────────────────────────┤
  │ 导入     │ import { x } from './file'             │ from file import x               │
  ├──────────┼────────────────────────────────────────┼──────────────────────────────────┤
  │ 别名     │ import { x as y }                      │ from file import x as y          │
  ├──────────┼────────────────────────────────────────┼──────────────────────────────────┤
  │ 统一入口 │ index.ts                               │ __init__.py                      │
  ├──────────┼────────────────────────────────────────┼──────────────────────────────────┤
  │ 路径解析 │ ./ 当前、../ 上级、无前缀=node_modules │ . 当前、.. 上级、无前缀=sys.path │
  └──────────┴────────────────────────────────────────┴──────────────────────────────────┘
```



# 类
## 1.类的继承写法
```python
  class 子类(父类):
      def __init__(self, ...):
          super().__init__(...)      # 调用父类的 __init__
```

+ 类似 JS 的 class Sub extends Base { constructor() { super() } }
+ super() 调用父类方法，不写就是完全覆盖父类

##  2. Python 错误基类：Exception
+ Python 所有异常的祖先类，类似 JS 的 Error
+ 自定义异常必须继承 Exception，否则 Python 不认
+ 常见内置异常：ValueError、TypeError、KeyError、RuntimeError



# raise关键字
+ Python 的 throw，抛出异常，当前函数立即停止
+ 语法：raise 异常实例

```python
raise Exception("出错了")
raise NotFoundException("Note")
```





# 内置库
## Pydantic
数据验证库。通过继承 BaseModel + 类型注解，在类实例化时自动验证数据类型和约束。

```python
from pydantic import BaseModel, Field

 class NoteCreate(BaseModel):
      title: str = Field(..., min_length=1)

  note = NoteCreate(title="hello")    # ✅ 通过
  note = NoteCreate(title=123)        # ❌ ValidationError


```

### BaseModel
####  BaseModel 的本质
  BaseModel 是一个普通的 Python 类。它的特殊之处在于：

```python
  class BaseModel:
      def __init_subclass__(cls):
          # 子类定义时自动调用
          # 读取 __annotations__
          # 注入 __init__
          # 注入 model_dump
          # 注入 model_dump_json
          ...
```



  为什么不需要自己写 __init__, 因为 Pydantic 在 BaseModel 里预置了这些方法，它们在你定义子类时自动扫描注解并注入。

你写：

```python
from pydantic import BaseModel, Field

 class NoteCreate(BaseModel):
      title: str = Field(..., min_length=1)
```



  实际发生的等价代码：

```python
  class NoteCreate:
      title: str
      content: str

      def __init__(self, title: str, content: str = ""):
          self.title = title
          self.content = content

      def model_dump(self):
          return {"title": self.title, "content": self.content}

      def model_dump_json(self):
          return '{"title": "' + self.title + '", "content": "' + self.content + '"}'
```



  核心逻辑

  Pydantic: 1. 读取 __annotations__ → {"title": str, "name": str}

            2. 生成 __init__(self, title, name)

            3. 在 __init__ 里加验证逻辑

            4. 注入 model_dump, model_dump_json 等方法



  你用:  a = A(title="hi", name="world")  ← 直接实例化，不需要自己写构造函数



  一句话：BaseModel

  是"会读注解的父类"。你定义子类时，它帮你把注解变成构造函数和工具方法。你只管声明，它帮你实现。

#### xxx.model_dump() 
 BaseModel 提供的方法。把 Pydantic 类实例转成普通的 Python 字典（dict）。

```python
note = NoteCreate(title="hello")
  # note 是一个类实例

  note.model_dump()
  # 返回: {"title": "hello", "content": "", "done": false}
  # 返回是一个普通的 dict，可以像操作普通字典一样操作它
```



  关键参数：exclude_unset=True

```python
  note = NotePartialUpdate(title="新标题")   # content 没传

  note.model_dump()
  # {"title": "新标题", "content": None, "done": None}
  # 没传的字段也被包含进来（值是 None）

  note.model_dump(exclude_unset=True)
  # {"title": "新标题"}
  # 只包含你实际传了的字段
```



  用在 PATCH 上：

```python
  # 部分更新：只改你传的字段
  for key, value in note.model_dump(exclude_unset=True).items():
      existing[key] = value
  # 没传的字段不会被覆盖成 None
```

### Field
 Pydantic 的字段约束工具。给类型注解加额外的验证规则和元数据。

```python
 title: str = Field(..., min_length=1, max_length=100)
  #         ^^^^^ 告诉 Pydantic：这个字段有规则

```

  ...（Ellipsis） — Python 的省略号对象，在这里表示必填。

```python
  ┌─────────────────────────┬────────────────┐
  │          写法           │      含义      │
  ├─────────────────────────┼────────────────┤
  │ Field(..., ...)         │ 必填           │
  ├─────────────────────────┼────────────────┤
  │ Field(default="x", ...) │ 有默认值，可选 │
  └─────────────────────────┴────────────────┘
```

 

不用Fidld，就只能做类型检查，不能加规则：

```python
  class A(BaseModel):
      title: str           # 只检查必须是 str
```

  

加上 Field 才能限制长度、范围、正则、描述等：

```python
  class A(BaseModel):
      title: str = Field(..., min_length=1, max_length=100, description="笔记标题")
      age: int = Field(..., gt=0, lt=150)       # gt = greater than
      email: str = Field(..., pattern=r".+@.+") # 正则验证
```



