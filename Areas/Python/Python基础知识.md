# Python 基础知识

## 目录

- [第1章 运行与入口](#第1章-运行与入口)
  - [1.1 交互模式与脚本执行](#11-交互模式与脚本执行)
  - [1.2 `python -m`](#12-python--m)
  - [1.3 `__name__` 与 `__main__`](#13-__name__-与-__main__)
  - [1.4 `main()` 入口模式](#14-main-入口模式)
- [第2章 参数与调用](#第2章-参数与调用)
  - [2.1 位置参数与关键字参数](#21-位置参数与关键字参数)
  - [2.2 默认参数](#22-默认参数)
  - [2.3 `*args` 与 `**kwargs`](#23-args-与-kwargs)
  - [2.4 参数展开](#24-参数展开)
  - [2.5 函数签名](#25-函数签名)
- [第3章 容器与解包](#第3章-容器与解包)
  - [3.1 `list`、`tuple`、`dict`](#31-listtupledict)
  - [3.2 列表拼接与构造](#32-列表拼接与构造)
  - [3.3 列表解包](#33-列表解包)
  - [3.4 元组解包](#34-元组解包)
- [第4章 类型标注](#第4章-类型标注)
  - [4.1 参数与返回值注解](#41-参数与返回值注解)
  - [4.2 `list[str]`、`dict[str, int]`](#42-liststrdictstr-int)
  - [4.3 `str | None`](#43-str--none)
  - [4.4 `TypedDict`](#44-typeddict)
  - [4.5 `Annotated`](#45-annotated)
  - [4.6 `Literal`](#46-literal)
- [第5章 模块与导入](#第5章-模块与导入)
  - [5.1 模块](#51-模块)
  - [5.2 包与 `__init__.py`](#52-包与-__init__py)
  - [5.3 绝对导入与相对导入](#53-绝对导入与相对导入)
  - [5.4 `sys.path`](#54-syspath)
- [第6章 类与对象](#第6章-类与对象)
  - [6.1 `class`](#61-class)
  - [6.2 实例、属性、方法](#62-实例属性方法)
  - [6.3 对象属性、字典键与 `getattr()`](#63-对象属性字典键与-getattr)
  - [6.4 继承](#64-继承)
  - [6.5 类、实例与类型](#65-类实例与类型)
- [第7章 异常](#第7章-异常)
  - [7.1 `Exception`](#71-exception)
  - [7.2 `raise`](#72-raise)
  - [7.3 自定义异常](#73-自定义异常)
- [第8章 装饰器](#第8章-装饰器)
  - [8.1 `@decorator`](#81-decorator)
  - [8.2 带参数装饰器](#82-带参数装饰器)
  - [8.3 `@wraps`](#83-wraps)
  - [8.4 Flask 路由装饰器](#84-flask-路由装饰器)
  - [8.5 常见内置装饰器](#85-常见内置装饰器)
- [第9章 Pydantic](#第9章-pydantic)
  - [9.1 `BaseModel`](#91-basemodel)
  - [9.2 `Field`](#92-field)
  - [9.3 `model_dump()`](#93-model_dump)
- [第10章 工程实践](#第10章-工程实践)
  - [10.1 CLI 交互循环](#101-cli-交互循环)
  - [10.2 `.env` 与 `.env.local`](#102-env-与-envlocal)
  - [10.3 `load_dotenv()`](#103-load_dotenv)

## 第1章 运行与入口

### 1.1 交互模式与脚本执行

Python 常见有两种运行方式：交互模式和脚本执行。

交互模式就是先启动 Python 解释器，再一行一行输入代码，解释器立刻执行并返回结果。它更像一个临时实验台，适合验证表达式、测试语法和做小段试验。

```bash
python
```

进入后通常会看到类似提示符：

```python
>>> 1 + 2
3
>>> name = "Tom"
>>> name
'Tom'
```

退出交互模式可以用 `Ctrl + D`，也可以输入：

```python
quit()
```

脚本执行则是把代码写进 `.py` 文件，再让 Python 一次性执行整个文件：

```bash
python app.py
```

交互模式偏试验，脚本执行偏正式运行。

### 1.2 `python -m`

`python -m` 的意思不是“运行某个文件路径”，而是“把某个模块当作程序入口来运行”。

最常见写法是：

```bash
python -m package.module
```

例如：

```bash
python -m http.server
```

这表示运行标准库里的 `http.server` 模块。

它和 `python path/to/file.py` 的区别在于：`-m` 会按模块导入规则来定位代码，因此更适合包内模块，也更适合需要保留包语义的场景。遇到相对导入时，`python -m ...` 通常比直接运行深层脚本更稳。

### 1.3 `__name__` 与 `__main__`

每个 Python 模块都有一个内置变量 `__name__`。

如果一个文件是被别的模块导入的，那么 `__name__` 一般是它自己的模块名。  
如果这个文件是当前程序的直接入口，那么 `__name__` 会变成 `"__main__"`。

这就是下面这类判断存在的原因：

```python
if __name__ == "__main__":
    ...
```

它的含义是：只有当这个文件是“直接运行”时，下面的代码才执行；如果只是被导入，就不执行。

### 1.4 `main()` 入口模式

常见写法是先定义一个 `main()`，再在入口判断里调用它：

```python
def main() -> None:
    print("run")


if __name__ == "__main__":
    main()
```

这样做的好处是把“定义”和“执行入口”分开。函数、类、常量可以正常放在模块里，真正要执行的逻辑集中在 `main()`，文件被导入时也不会顺手把主流程跑起来。

不要把数据库连接、网络请求、文件写入这类重逻辑直接放在模块顶层；这类逻辑更适合放进 `main()` 或其他显式调用的函数里。

## 第2章 参数与调用

### 2.1 位置参数与关键字参数

调用函数时，参数可以按位置传，也可以按名字传。

```python
def create_user(name: str, age: int) -> dict:
    return {"name": name, "age": age}


create_user("Alice", 18)
create_user(name="Alice", age=18)
create_user(age=18, name="Alice")
```

第一种写法是位置参数。Python 看到第一个值就传给 `name`，第二个值传给 `age`。

第二种和第三种是关键字参数。这里不是按顺序，而是按参数名绑定，所以顺序可以交换。

`HumanMessage(content=user_input)` 也属于同一类写法。它表示把变量 `user_input` 的值传给参数 `content`。这里的 `content` 是参数名，不是变量名。

容易混淆的一点是：

```python
HumanMessage(content)
```

这不是“省略写法”，而是把变量 `content` 当作第一个位置参数传入。

### 2.2 默认参数

参数可以带默认值。调用时如果不传，Python 就使用默认值。

```python
def greet(name: str, prefix: str = "Hi") -> str:
    return f"{prefix}, {name}"
```

这里的 `prefix` 默认是 `"Hi"`，所以这两个调用都合法：

```python
greet("Tom")
greet("Tom", "Hello")
```

需要注意的是：默认参数不是“每次调用时临时声明”，而是在函数定义阶段就已经确定。可变对象默认值会有额外陷阱，这部分后续单独整理。

### 2.3 `*args` 与 `**kwargs`

这两个写法都和“接收不定数量参数”有关。

```python
def demo(*args, **kwargs):
    return args, kwargs
```

其中：

- `*args` 把多余的位置参数收集成一个元组。
- `**kwargs` 把多余的关键字参数收集成一个字典。

例如：

```python
demo(1, 2, name="Tom")
```

大致会得到：

```python
((1, 2), {"name": "Tom"})
```

### 2.4 参数展开

定义函数时的 `*args`、`**kwargs` 是“收集参数”；调用函数时的 `*`、`**` 则是“展开参数”。

```python
def add(a, b):
    return a + b


nums = [1, 2]
add(*nums)
```

这里的 `*nums` 会把 `[1, 2]` 展开成两个位置参数，等价于：

```python
add(1, 2)
```

同理，`**` 可以把字典展开成关键字参数。

### 2.5 函数签名

函数签名是“这个函数如何被调用”的那组信息。

最常见的组成包括：

- 参数顺序
- 哪些参数必填
- 哪些参数有默认值
- 参数种类，如位置参数、关键字参数、`*args`、`**kwargs`
- 返回值注解

例如：

```python
def create_user(name: str, age: int = 18, *, active: bool = True) -> dict:
    return {"name": name, "age": age, "active": active}
```

这个签名里能读出：

- `name` 是必填参数
- `age` 有默认值 `18`
- `active` 只能用关键字传参
- 返回值注解是 `dict`

要区分“签名”和“函数体”：

- `def create_user(name: str, age: int = 18, *, active: bool = True) -> dict:` 是签名
- `return {"name": name, "age": age, "active": active}` 是函数体

Python 标准库可以直接读取函数签名：

```python
import inspect


def add(a: int, b: int = 0) -> int:
    return a + b


inspect.signature(add)
```

结果近似：

```python
(a: int, b: int = 0) -> int
```

函数签名经常会被框架读取，而不只是给人看。FastAPI 会先分析路由函数签名，再判断参数来自路径、查询参数、请求体还是依赖注入。

## 第3章 容器与解包

### 3.1 `list`、`tuple`、`dict`

这三个是最常见的容器类型。

- `list`：有序、可变。
- `tuple`：有序、不可变。
- `dict`：键值映射。

### 3.2 列表拼接与构造

常见方式有 `append`、`extend`、`+`，以及基于旧列表构造新列表。

```python
items = [1, 2]
items.append(3)
items = items + [4]
```

如果需要保留旧列表不变，更适合构造新列表，而不是原地修改。

### 3.3 列表解包

`*items` 会把可迭代对象中的元素逐个展开。

```python
items = [1, 2]
result = [*items, 3]
```

结果是：

```python
[1, 2, 3]
```

`[*messages, HumanMessage(content=user_input)]` 表示先展开旧消息列表，再追加新消息。这一写法常用于基于旧列表构造新列表，避免原地修改。

### 3.4 元组解包

```python
a, b = (1, 2)
```

它的作用是同时取多个值，并按顺序赋给多个变量。

## 第4章 类型标注

### 4.1 参数与返回值注解

```python
def add(a: int, b: int) -> int:
    return a + b
```

这里的 `a: int`、`b: int` 是参数注解，`-> int` 是返回值注解。

### 4.2 `list[str]`、`dict[str, int]`

```python
names: list[str] = ["a", "b"]
ages: dict[str, int] = {"Tom": 18}
```

这类写法用于标注容器里元素的类型。

### 4.3 `str | None`

`str | None` 表示值可能是 `str`，也可能是 `None`。

```python
nickname: str | None = None
```

### 4.4 `TypedDict`

`TypedDict` 用来描述“键集合固定的字典结构”。

```python
from typing import TypedDict


class ArticleState(TypedDict):
    topic: str
    outline: list[str]
    article: str
```

这段代码表达的是：

- 这个值本质上是 `dict`
- 这个 `dict` 应该有 `topic`、`outline`、`article` 这几个键
- 每个键对应的值类型已经写死

例如：

```python
state: ArticleState = {
    "topic": "LangGraph",
    "outline": ["定义", "结构", "执行流程"],
    "article": "",
}
```

这里 `state` 仍然是普通字典，读取方式也是：

```python
state["topic"]
state["outline"]
```

不是：

```python
state.topic
```

`TypedDict` 虽然用了 `class` 语法，但这里不是在定义常规业务类，也不是为了后面写 `ArticleState(...)` 这种实例化代码。这里借 `class` 语法列出的是“固定键名 + 每个键的值类型”。

它解决的是 `dict[str, str]` 解决不了的问题。  
`dict[str, str]` 只能说明“键是字符串，值是字符串”，不能说明必须有哪些键；`TypedDict` 可以把具体键名写出来。

它主要用于类型标注，重点是把字典结构写清楚，方便编辑器提示和类型检查。运行时使用时，通常还是普通 `dict`。

它和 Pydantic 都能描述数据结构，但侧重点不同：

- `TypedDict`：描述字典结构
- `BaseModel`：定义运行时数据模型

在 LangGraph 里，state 经常在节点之间按字典传递，并且节点通常返回局部更新字典：

```python
def decide_route(state: RouterState) -> dict:
    return {"route": "writer"}
```

这种数据形态天然适合用 `TypedDict` 描述。

### 4.5 `Annotated`

`Annotated[T, meta1, meta2]` 表示“真实类型仍然是 `T`，但额外附带一段可被外部读取的元信息”。

```python
from typing import Annotated


name: Annotated[str, "用户名"]
```

这里的关键点是：

- `str` 仍然是这个值的真实类型
- 运行时值仍然是普通 `str`，不会变成某种 `Annotated` 实例
- Python 本身通常不会自动处理后面的元信息

`Annotated` 的主要用途不是改变运行时行为，而是把“类型”和“附加声明”写在同一个类型标注里，供框架、类型检查器扩展或反射代码读取。

FastAPI 里的典型写法：

```python
from typing import Annotated

from fastapi import Depends, Query


q: Annotated[str | None, Query(min_length=3)] = None
user: Annotated[User, Depends(get_current_user)]
```

这里拆开看：

- `str | None`、`User`：真实类型
- `Query(...)`、`Depends(...)`：给 FastAPI 读取的元信息

`Annotated` 解决的是“类型”和“框架声明”混写在默认值位置不清楚的问题。它不是运行时包装器，也不会自动做校验；真正读取这些元信息并据此执行逻辑的，是 FastAPI 这类框架。

如果在普通 Python 里需要保留并读取 `Annotated` 的元信息，通常要显式开启 `include_extras=True`：

```python
from typing import Annotated, get_type_hints


def read_me(user: Annotated[str, "token"]) -> None:
    pass


get_type_hints(read_me, include_extras=True)
```

### 4.6 `Literal`

`Literal` 用来限制值只能是几个固定字面量之一。

```python
from typing import Literal


def pick_next_node(state: RouterState) -> Literal["writer", "chatbot", "fallback"]:
    return state["route"]
```

这里返回值不是普通 `str`，而是限定为这三个固定字符串之一。

它和联合类型有点像，但粒度更细：

```python
str | None
```

表示“二选一的类型”；

```python
Literal["writer", "chatbot", "fallback"]
```

表示“只能是这几个固定值之一”。

它常用于路由、分支选择、枚举式返回值。和 `TypedDict` 一样，它主要是类型标注，不是运行时对象模型。

## 第5章 模块与导入

### 5.1 模块

每个 `.py` 文件天然就是一个模块。

```python
# notes.py
def get_note():
    pass
```

导入方式：

```python
import app.routers.notes
from app.routers.notes import get_note
from app.routers import notes as notes_router
```

### 5.2 包与 `__init__.py`

包是目录层面的组织方式，`__init__.py` 常用于：

- 把目录标识成传统包；
- 放轻量初始化；
- 提供统一导出入口。

```python
from .notes import router as notes_router

__all__ = ["notes_router"]
```

不要把重逻辑塞进 `__init__.py`。

### 5.3 绝对导入与相对导入

```python
from app.routers.notes import get_note
from .notes import get_note
from ..schemas import NoteCreate
```

跨包时优先绝对导入。包内相邻模块可用相对导入。

顶层脚本不在包内时，不能使用 `from .xxx import ...`；超过顶层包会报 `ImportError: beyond top-level package`。

### 5.4 `sys.path`

Python 导入模块时，会按 `sys.path` 里的目录顺序查找。

理解 `sys.path` 的意义，主要是为了排查“为什么这个导入能找到”或“为什么找不到”。

## 第6章 类与对象

### 6.1 `class`

`class` 用来定义类。Python 创建对象时不需要 `new`。

```python
class User:
    def __init__(self, name: str):
        self.name = name


user = User("Tom")
```

### 6.2 实例、属性、方法

- 类：模板。
- 实例：按类创建出来的对象。
- 属性：对象上的数据。
- 方法：对象上的行为。

### 6.3 对象属性、字典键与 `getattr()`

对象属性和字典键不是一回事。

对象属性：

```python
user.name
```

字典键：

```python
data["name"]
```

两者都像“按名字找值”，但语法和数据结构不同：

- `user.name`：从对象上取属性
- `data["name"]`：从字典里取键对应的值

例如：

```python
class User:
    def __init__(self, name: str):
        self.name = name


user = User("Tom")
data = {"name": "Tom"}
```

这里：

```python
user.name
```

和：

```python
data["name"]
```

结果可能一样，但来源不同。

`getattr(obj, "attr", default)` 用来按属性名读取对象属性。

```python
getattr(user, "name", None)
```

含义是：

- 如果 `user` 有 `name` 属性，就返回它
- 如果没有，就返回 `None`

它处理的是对象属性，不是字典键。

字典的对应写法是：

```python
data.get("name", None)
```

两者相似处在于都可以提供默认值；区别在于：

- `getattr(...)` 读对象属性
- `dict.get(...)` 读字典键

如果直接写：

```python
user.age
```

而对象上没有这个属性，会报 `AttributeError`。  
如果写：

```python
getattr(user, "age", None)
```

就不会在这一行直接报错，而是返回 `None`。

### 6.4 继承

```python
class Child(Base):
    def __init__(self, name):
        super().__init__(name)
```

`super()` 用来调用父类方法。

### 6.5 类、实例与类型

类既是构造器，也是类型定义。

```python
builder = StateGraph(ArticleState)
```

这里传入的 `ArticleState` 是类型本身，不是实例。`HumanMessage` 也是同类情况：既是类，也定义了一种对象类型。

## 第7章 异常

### 7.1 `Exception`

`Exception` 是大多数 Python 异常的基类。

常见异常包括：

- `ValueError`
- `TypeError`
- `KeyError`
- `RuntimeError`

### 7.2 `raise`

`raise` 用于抛出异常。

```python
raise Exception("error")
```

### 7.3 自定义异常

自定义异常应继承 `Exception`。

## 第8章 装饰器

### 8.1 `@decorator`

`@decorator` 等价于：

```python
func = decorator(func)
```

装饰器常用于日志、权限校验、缓存和注册。

### 8.2 带参数装饰器

`@decorator(a, b)` 等价于：

```python
func = decorator(a, b)(func)
```

### 8.3 `@wraps`

`@wraps` 用来保留原函数的 `__name__`、文档、注解等元数据。

```python
from functools import wraps
```

不使用 `@wraps` 时，被包装函数名可能变成 `wrapper`。

### 8.4 Flask 路由装饰器

`@api_app.route(...)` 是带参数装饰器。路由注册发生在模块导入时。

```python
@api_app.route('/review/webhook', methods=['POST'])
@require_json
def handle_webhook():
    ...
```

路由装饰器通常放在最上面，这样 Flask 注册到的是包装后的最终函数。

### 8.5 常见内置装饰器

- `@staticmethod`
- `@classmethod`
- `@property`
- `@dataclass`
- `@lru_cache`

## 第9章 Pydantic

### 9.1 `BaseModel`

`BaseModel` 是 Pydantic 提供的父类。定义数据模型时，通常让自己的类继承它。

```python
from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = ""
```

这里的 `NoteCreate` 仍然是一个普通 Python 类。区别不在“它不像类”，而在于它继承的父类是 `BaseModel`。

先看普通类的情况：

```python
class NoteCreate:
    def __init__(self, title: str, content: str = ""):
        self.title = title
        self.content = content
```

这个类之所以能实例化，是因为它自己写了 `__init__`：

```python
note = NoteCreate(title="hello")
```

如果一个子类自己没有定义 `__init__`，Python 会沿继承链继续找 `__init__`。也就是说，先看子类自己有没有；没有的话，再去父类里找。

纯 Python 里，这件事可以写成：

```python
class A:
    def __init__(self, **data):
        print(data)


class B(A):
    pass


b = B(name="tom", age=18)
```

这里 `B` 自己没写 `__init__`，但 `B(...)` 仍然成立，因为实例化时实际调用的是继承来的 `A.__init__`。

`BaseModel` 的第一层机制也是这个逻辑。  
`NoteCreate` 自己通常不写 `__init__`，所以当你调用：

```python
note = NoteCreate(title="hello")
```

Python 会去调用继承来的 `BaseModel.__init__`。

可以先把它近似理解成：

```python
class BaseModel:
    def __init__(self, **data):
        ...
```

这里最关键的是 `**data`。  
它表示：实例化时传进来的关键字参数，会先被收集成一个字典。

所以：

```python
note = NoteCreate(title="hello")
```

可以近似理解成：

```python
data = {"title": "hello"}
BaseModel.__init__(note, **data)
```

也就是说，子类的参数不是先被子类接住再转发，而是因为子类没有自己的 `__init__`，Python 直接把这些关键字参数传给了继承来的父类 `__init__`。

接下来要问的是：`BaseModel.__init__` 为什么能处理这些数据？

原因在于 `BaseModel.__init__` 不是普通的赋值版构造函数。  
普通构造函数可能只是：

```python
def __init__(self, title, content=""):
    self.title = title
    self.content = content
```

但 `BaseModel.__init__` 内部会先根据当前这个子类的字段定义做校验，再决定能不能创建实例。

所以当你写：

```python
class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = ""
```

再执行：

```python
note = NoteCreate(title="hello")
```

大致发生的是：

1. Python 创建一个 `NoteCreate` 实例
2. Python 发现 `NoteCreate` 自己没有 `__init__`
3. Python 调用继承来的 `BaseModel.__init__(self, **data)`
4. 这里的 `self` 仍然是 `NoteCreate` 实例
5. 这里的 `data` 大致是 `{"title": "hello"}`
6. `BaseModel.__init__` 按 `NoteCreate` 这个类声明过的字段规则处理这些数据
7. 数据合法，实例创建成功
8. 数据不合法，抛出校验错误

例如：

```python
note = NoteCreate(title="hello")
```

这是合法实例化。

```python
note = NoteCreate(title=123)
```

这时 `title` 应该是字符串，但传入了整数，Pydantic 会在实例化阶段报校验错误。

所以这一节最核心的理解应该是：

- `BaseModel` 是父类
- `NoteCreate` 是你定义的子类
- 子类通常没有自己写 `__init__`
- 实例化时会直接调用继承来的 `BaseModel.__init__`
- 传入参数会以 `**data` 的形式进入父类 `__init__`
- `BaseModel.__init__` 不只是赋值，还会按子类字段规则做校验

### 9.2 `Field`

`Field` 用来给字段补充验证规则和元数据。

```python
title: str = Field(..., min_length=1, max_length=100)
age: int = Field(..., gt=0, lt=150)
email: str = Field(..., pattern=r".+@.+")
```

这里的 `...` 表示必填。只写 `title: str` 时，只有类型信息；写了 `Field(...)` 之后，这个字段还带有长度、范围、正则等附加规则。

可以把 `Field(...)` 理解成“这个字段除了类型之外，还有额外约束”。

### 9.3 `model_dump()`

`model_dump()` 用来把 Pydantic 模型实例转成普通字典。

```python
note = NoteCreate(title="hello")
data = note.model_dump()
```

`model_dump()` 不是子类自己声明的方法，而是继承自 `BaseModel` 的实例方法。  
当调用 `note.model_dump()` 时，Python 会沿继承链找到 `BaseModel.model_dump`，再把当前实例 `note` 作为 `self` 传入执行。

这时 `data` 就是一个普通 `dict`，适合继续交给数据库、日志、JSON 序列化逻辑或其他普通 Python 代码处理。

```python
note.model_dump(exclude_unset=True)
```

`exclude_unset=True` 只返回实际传入的字段，适合 PATCH / 局部更新场景。

```python
for key, value in note.model_dump(exclude_unset=True).items():
    existing[key] = value
```

## 第10章 工程实践

### 10.1 CLI 交互循环

`while True + input()` 是常见终端交互模式。

```python
while True:
    user_input = input("You: ").strip()
    if user_input.lower() in {"exit", "quit"}:
        break
    if not user_input:
        continue
```

这种写法常见于聊天式 CLI、调试工具和小型交互脚本。

### 10.2 `.env` 与 `.env.local`

是否自动读取 `.env.local`，取决于代码如何调用 dotenv。

`load_dotenv()` 默认主要读取 `.env`。如果项目使用 `.env.local`，通常需要显式指定。

### 10.3 `load_dotenv()`

```python
from dotenv import load_dotenv

load_dotenv()
```

它的作用是把环境变量从文件加载到当前进程环境中。
