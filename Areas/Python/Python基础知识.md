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
  - [2.6 条件表达式](#26-条件表达式)
  - [2.7 `or` 兜底](#27-or-兜底)
  - [2.8 `and` 短路](#28-and-短路)
  - [2.9 `if not x`](#29-if-not-x)
- [第3章 容器与解包](#第3章-容器与解包)
  - [3.1 `list`、`tuple`、`dict`](#31-listtupledict)
  - [3.2 列表拼接与构造](#32-列表拼接与构造)
  - [3.3 切片](#33-切片)
  - [3.4 列表解包](#34-列表解包)
  - [3.5 元组解包](#35-元组解包)
  - [3.6 `dict` 的读取、写入、更新](#36-dict-的读取写入更新)
  - [3.7 `dict.get()`](#37-dictget)
  - [3.8 `dict.keys()`、`dict.values()`、`dict.items()`](#38-dictkeysdictvaluesdictitems)
  - [3.9 遍历 `dict`](#39-遍历-dict)
- [第4章 循环与迭代](#第4章-循环与迭代)
  - [4.1 `for` 循环](#41-for-循环)
  - [4.2 `range()`](#42-range)
  - [4.3 `enumerate()`](#43-enumerate)
  - [4.4 `while` 循环](#44-while-循环)
  - [4.5 `break` 与 `continue`](#45-break-与-continue)
  - [4.6 惰性生成器](#46-惰性生成器)
- [第5章 类型标注](#第5章-类型标注)
  - [5.1 参数与返回值注解](#51-参数与返回值注解)
  - [5.2 `list[str]`、`dict[str, int]`](#52-liststrdictstr-int)
  - [5.3 `str | None`](#53-str--none)
  - [5.4 `TypedDict`](#54-typeddict)
  - [5.5 `Annotated`](#55-annotated)
  - [5.6 `Literal`](#56-literal)
  - [5.7 `operator`](#57-operator)
- [第6章 模块与导入](#第6章-模块与导入)
  - [6.1 模块](#61-模块)
  - [6.2 包与 `__init__.py`](#62-包与-__init__py)
  - [6.3 绝对导入与相对导入](#63-绝对导入与相对导入)
  - [6.4 `sys.path`](#64-syspath)
- [第7章 类与对象](#第7章-类与对象)
  - [7.1 `class`](#71-class)
  - [7.2 实例、属性、方法](#72-实例属性方法)
  - [7.3 对象属性、字典键与 `getattr()`](#73-对象属性字典键与-getattr)
  - [7.4 继承](#74-继承)
  - [7.5 类、实例与类型](#75-类实例与类型)
- [第8章 异常](#第8章-异常)
  - [8.1 `Exception`](#81-exception)
  - [8.2 `raise`](#82-raise)
  - [8.3 自定义异常](#83-自定义异常)
  - [8.4 `try` / `except`](#84-try--except)
  - [8.5 `with` 语句与上下文管理器](#85-with-语句与上下文管理器)
- [第9章 装饰器](#第9章-装饰器)
  - [9.1 `@decorator`](#91-decorator)
  - [9.2 带参数装饰器](#92-带参数装饰器)
  - [9.3 `@wraps`](#93-wraps)
  - [9.4 Flask 路由装饰器](#94-flask-路由装饰器)
  - [9.5 常见内置装饰器](#95-常见内置装饰器)
  - [9.6 `@contextmanager` 与 `@asynccontextmanager`](#96-contextmanager-与-asynccontextmanager)
- [第10章 Pydantic](#第10章-pydantic)
  - [10.1 `BaseModel`](#101-basemodel)
  - [10.2 `model_validate()`](#102-model_validate)
  - [10.3 `Field`](#103-field)
  - [10.4 `model_dump()`](#104-model_dump)
  - [10.5 `ValidationError`](#105-validationerror)
- [第11章 工程实践](#第11章-工程实践)
  - [11.1 CLI 交互循环](#111-cli-交互循环)
  - [11.2 `.env` 与 `.env.local`](#112-env-与-envlocal)
  - [11.3 `load_dotenv()`](#113-load_dotenv)
  - [11.4 常量时间比较](#114-常量时间比较)

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
- 参数种类，如位置参数、关键字参数、`*args`、单独的 `*`、`**kwargs`
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

单独的 `*` 也属于签名规则的一部分。它表示：

- `*` 后面的参数只能用关键字传参

例如：

```python
def build_prompt(*, question: str, error: str | None = None):
    return {"question": question, "error": error}
```

可以这样调用：

```python
build_prompt(question="是否继续？")
build_prompt(question="是否继续？", error="输入不正确")
```

不能这样调用：

```python
build_prompt("是否继续？")
```

这种写法常用于配置型函数，因为参数名本身就是语义的一部分。和 `*args` 不同，单独的 `*` 不是收集参数，而是把后面的参数标记成“必须写参数名”。

### 2.6 条件表达式

Python 的条件表达式写法是：

```python
A if condition else B
```

例如：

```python
return "approve_tools" if tools_condition(state) == "tools" else "__end__"
```

含义是：

- 条件成立，返回 `"approve_tools"`
- 否则，返回 `"__end__"`

等价于普通 `if/else`：

```python
if tools_condition(state) == "tools":
    return "approve_tools"
else:
    return "__end__"
```

对应的 JavaScript 写法是：

```javascript
return tools_condition(state) === "tools" ? "approve_tools" : "__end__";
```

### 2.7 `or` 兜底

`x or y` 常用于“如果左边没有合适值，就退回右边”。

```python
decision = state["human_decision"] or {}
```

这句的含义是：

- 如果 `state["human_decision"]` 有值，就用它
- 如果它是空值，就退回到 `{}`

这里的空值包括：

- `None`
- `False`
- `0`
- `""`
- `[]`
- `{}`

对应的 JavaScript 写法是：

```javascript
const decision = state.human_decision || {};
```

如果是在字典里取值，还要区分两个问题：

1. 键可能不存在
2. 键存在，但值可能是空值

只解决“键不存在”时，更直接的写法通常是：

```python
decision = state.get("human_decision", {})
```

这句表示：

- 如果键不存在，返回默认值 `{}`
- 如果键存在，返回它原本的值

如果还想把 `None`、空字符串、空列表、空字典这类空值一起兜底，才会写成：

```python
decision = state.get("human_decision") or {}
```

可以先按这个规则区分：

- `dict.get(key, default)`：优先解决“键缺失”
- `x or fallback`：优先解决“值为空”

### 2.8 `and` 短路

`x and y` 表示：

- 如果 `x` 是空值，直接返回 `x`
- 如果 `x` 有值，继续返回 `y`

它常用于“左边成立时再算右边”。

JavaScript 中最接近的写法是：

```javascript
x && y
```

### 2.9 `if not x`

`if not x:` 表示“如果 `x` 是空值，就进入分支”。

例如：

```python
if not tool_calls:
    return Command(goto="chatbot")
```

这句的含义是：

- 如果 `tool_calls` 是空列表、`None`、空字符串等空值
- 就进入这个分支

对应的 JavaScript 写法是：

```javascript
if (!tool_calls) {
  return gotoChatbot();
}
```

这里的 `not` 是逻辑取反运算。可以近似理解成：

```python
if not x:
```

先判断 `x` 的真假，再把结果取反。

例如：

```python
bool([])
```

结果是 `False`，所以：

```python
not []
```

结果是 `True`。

要和下面这种写法区分：

```python
if x is not None:
```

这里的 `is not` 是一个整体比较运算，意思是：

- 判断 `x` 不是 `None`

它不是先对 `x` 做 `not`，也不是先对 `None` 做 `not`。

可以先按下面两句区分：

- `not x`：逻辑取反，看真假
- `x is not None`：整体比较，看是不是 `None`

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

### 3.3 切片

`[start:stop:step]` 用于从 `list`、`tuple`、`str` 中截取子序列。

```python
items = [0, 1, 2, 3, 4, 5]
items[1:4]     # [1, 2, 3]   取索引 1~3
items[:3]      # [0, 1, 2]   省略 start，从开头取
items[3:]      # [3, 4, 5]   省略 stop，取到最后
items[::2]     # [0, 2, 4]   步长为 2，跳着取
items[::-1]    # [5, 4, 3, 2, 1, 0]  倒序
items[-1]      # 5           最后一个元素
items[-3:-1]   # [3, 4]      倒数第 3 个到倒数第 2 个
```

字符串同样适用：

```python
text = "hello world"
text[:5]       # "hello"
text[6:]       # "world"
text[-1]       # "d"
```

常见截断写法——防止消息过长：

```python
preview = text[:50] + "..." if len(text) > 50 else text
```

### 3.4 列表解包

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

### 3.5 元组解包

```python
a, b = (1, 2)
```

它的作用是同时取多个值，并按顺序赋给多个变量。

### 3.6 `dict` 的读取、写入、更新

字典是键值映射结构。

```python
data = {"name": "Tom"}
```

读取：

```python
data["name"]
```

写入新键：

```python
data["age"] = 18
```

更新已有键：

```python
data["name"] = "Alice"
```

这里新增的是字典键，不是对象属性。

### 3.7 `dict.get()`

`dict.get(key, default)` 用来按键读取字典值，并且可以提供默认值。

```python
data.get("name", None)
```

含义是：

- 如果字典里有 `"name"` 这个键，就返回对应值
- 如果没有，就返回默认值 `None`

例如：

```python
data = {"name": "Tom"}

data.get("name", None)
data.get("age", None)
```

和直接写：

```python
data["age"]
```

不同，后者在键不存在时会报 `KeyError`。

### 3.8 `dict.keys()`、`dict.values()`、`dict.items()`

假设：

```python
data = {"name": "Tom", "age": 18}
```

```python
data.keys()
```

返回 `dict_keys` 视图对象，表示当前字典的所有键。

```python
data.values()
```

返回 `dict_values` 视图对象，表示当前字典的所有值。

```python
data.items()
```

返回 `dict_items` 视图对象，表示当前字典的所有 `(key, value)` 对。

它们默认不是列表，而是可遍历的视图对象。因此常见写法是：

```python
list(data.keys())
list(data.values())
list(data.items())
```

对应结果分别近似为：

```python
["name", "age"]
["Tom", 18]
[("name", "Tom"), ("age", 18)]
```

这些视图对象的意义是：

- 能直接遍历
- 会反映字典的当前状态
- 需要真正列表时再手动 `list(...)`

### 3.9 遍历 `dict`

字典默认遍历的是键：

```python
for key in data:
    print(key)
```

也可以显式写成：

```python
for key in data.keys():
    print(key)
```

如果想同时拿到键和值，最常见写法是：

```python
for key, value in data.items():
    print(key, value)
```

对应的 JavaScript 写法是：

```javascript
for (const [key, value] of Object.entries(data)) {
  console.log(key, value);
}
```

## 第4章 循环与迭代

### 4.1 `for` 循环

`for` 循环逐个取出可迭代对象中的元素，对每个元素执行相同的代码块。

```python
for item in [1, 2, 3]:
    print(item)
# 1
# 2
# 3
```

`for` 可以遍历任何可迭代对象：

```python
for ch in "hello":        # 字符串
    print(ch)

for key in {"a": 1}:      # 字典（默认遍历键）
    print(key)
```

### 4.2 `range()`

`range()` 生成一个整数序列，最常见搭配 `for` 使用。

```python
range(stop)               # 从 0 开始，到 stop-1
range(start, stop)        # 从 start 开始，到 stop-1
range(start, stop, step)  # 步长为 step
```

**规则：包含 start，不包含 stop。**

```python
range(5)           # 0, 1, 2, 3, 4
range(1, 5)        # 1, 2, 3, 4
range(1, 10, 2)    # 1, 3, 5, 7, 9      步长为 2
range(10, 0, -1)   # 10, 9, 8, ..., 1   步长为负，递减
```

`range()` 是惰性生成器——只有在被遍历时才逐个产出数字。`range(1, 1000000)` 不会占 100 万个整数的内存。

常见组合：

```python
for i in range(5):
    print(i)      # 0, 1, 2, 3, 4
```

### 4.3 `enumerate()`

`enumerate()` 在遍历时同时提供索引和值。

```python
names = ["Alice", "Bob", "Charlie"]

for i, name in enumerate(names):
    print(i, name)
# 0 Alice
# 1 Bob
# 2 Charlie
```

可以指定起始索引：

```python
for i, name in enumerate(names, start=1):
    print(i, name)
# 1 Alice
# 2 Bob
# 3 Charlie
```

### 4.4 `while` 循环

`while` 在条件为真时重复执行。

```python
count = 0
while count < 3:
    print(count)
    count += 1
# 0
# 1
# 2
```

### 4.5 `break` 与 `continue`

- `break`：立即退出整个循环
- `continue`：跳过本次循环的剩余代码，进入下一次迭代

```python
for i in range(5):
    if i == 2:
        continue       # 跳过 2
    if i == 4:
        break          # 到 4 就停止
    print(i)
# 0
# 1
# 3
```

### 4.6 惰性生成器

`range()` 和 `enumerate()` 都不是列表——它们返回的是**惰性对象**，只在遍历时逐个产出值。

```python
r = range(1, 1000000)
type(r)     # <class 'range'>
len(r)      # 999999，可以取长度
r[0]        # 1，可以按索引取值
```

和列表的根本区别：列表把全部元素存在内存里，惰性对象只在需要时计算下一个值。

## 第5章 类型标注

### 5.1 参数与返回值注解

```python
def add(a: int, b: int) -> int:
    return a + b
```

这里的 `a: int`、`b: int` 是参数注解，`-> int` 是返回值注解。

### 5.2 `list[str]`、`dict[str, int]`

```python
names: list[str] = ["a", "b"]
ages: dict[str, int] = {"Tom": 18}
```

这类写法用于标注容器里元素的类型。

### 5.3 `str | None`

`str | None` 表示值可能是 `str`，也可能是 `None`。

```python
nickname: str | None = None
```

### 5.4 `TypedDict`

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

### 5.5 `Annotated`

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

### 5.6 `Literal`

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

### 5.7 `operator`

`operator` 是 Python 内置标准库模块，把运算符暴露成普通函数。

```python
import operator

operator.add(1, 2)    # 等价于 1 + 2，结果 3
operator.add([1], [2]) # 等价于 [1] + [2]，结果 [1, 2]
```

常用函数：

| 函数 | 等价运算符 |
|------|-----------|
| `operator.add(a, b)` | `a + b` |
| `operator.sub(a, b)` | `a - b` |
| `operator.mul(a, b)` | `a * b` |
| `operator.truediv(a, b)` | `a / b` |
| `operator.concat(a, b)` | `a + b`（序列拼接，与 add 等价） |

当需要把运算以函数形式传参时，`operator` 提供了直接的方式。

在实际工程里，`operator` 最常见的用途之一是配合 `Annotated` 做 LangGraph 的 **reducer**：

```python
from typing import Annotated
import operator


class MyState(TypedDict):
    sections: Annotated[list[str], operator.add]
    # 其他字段默认覆盖
    topic: str
```

这里 `operator.add` 是字段合并策略，含义在 LangGraph 笔记 2.2 中展开。

## 第6章 模块与导入

### 6.1 模块

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

### 6.2 包与 `__init__.py`

包是目录层面的组织方式，`__init__.py` 常用于：

- 把目录标识成传统包；
- 放轻量初始化；
- 提供统一导出入口。

```python
from .notes import router as notes_router

__all__ = ["notes_router"]
```

不要把重逻辑塞进 `__init__.py`。

### 6.3 绝对导入与相对导入

```python
from app.routers.notes import get_note
from .notes import get_note
from ..schemas import NoteCreate
```

跨包时优先绝对导入。包内相邻模块可用相对导入。

顶层脚本不在包内时，不能使用 `from .xxx import ...`；超过顶层包会报 `ImportError: beyond top-level package`。

### 6.4 `sys.path`

Python 导入模块时，会按 `sys.path` 里的目录顺序查找。

理解 `sys.path` 的意义，主要是为了排查“为什么这个导入能找到”或“为什么找不到”。

## 第7章 类与对象

### 7.1 `class`

`class` 用来定义类。Python 创建对象时不需要 `new`。

```python
class User:
    def __init__(self, name: str):
        self.name = name


user = User("Tom")
```

### 7.2 实例、属性、方法

- 类：模板。
- 实例：按类创建出来的对象。
- 属性：对象上的数据。
- 方法：对象上的行为。

### 7.3 对象属性、字典键与 `getattr()`

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

它处理的是对象属性，不是字典键。字典的 `get(...)`、`keys()`、`values()`、`items()` 等操作统一放在第3章。

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

### 7.4 继承

```python
class Child(Base):
    def __init__(self, name):
        super().__init__(name)
```

`super()` 用来调用父类方法。

### 7.5 类、实例与类型

类既是构造器，也是类型定义。

```python
builder = StateGraph(ArticleState)
```

这里传入的 `ArticleState` 是类型本身，不是实例。`HumanMessage` 也是同类情况：既是类，也定义了一种对象类型。

## 第8章 异常

### 8.1 `Exception`

`Exception` 是大多数 Python 异常的基类。

常见异常包括：

- `ValueError`
- `TypeError`
- `KeyError`
- `RuntimeError`

### 8.2 `raise`

`raise` 用于抛出异常。

```python
raise Exception("error")
```

### 8.3 自定义异常

自定义异常应继承 `Exception`。

### 8.4 `try` / `except`

`try` / `except` 用于捕获可能抛出的异常，防止程序直接崩溃。

```python
try:
    result = 1 / 0
except ZeroDivisionError:
    print("除数不能为零")
```

如果 `try` 块执行成功（没有异常），`except` 块直接跳过。  
如果 `try` 块执行时抛出了指定类型的异常，就进入 `except` 块。

**`as` 绑定异常对象**

```python
try:
    parsed = ApprovalDecision.model_validate(decision)
except ValidationError as exc:
    print(exc.errors())
```

`as exc` 把捕获到的异常实例绑定到变量 `exc`，之后可以在 `except` 块里读取异常的信息（如 `.errors()`、`.json()` 等）。

如果不写 `as`，就只能知道"出错了"，拿不到异常对象本身。

**捕获多种异常**

```python
try:
    data = json.loads(raw)
except (json.JSONDecodeError, TypeError) as exc:
    ...
```

多个异常类型可以写成元组。

**不匹配的异常会跳过透传**

`except` 只接住类型匹配的异常。不匹配的异常不会掉进这个 `except` 块，而是继续往外冒：

```python
try:
    parsed = ApprovalDecision.model_validate(decision)
except ValidationError as exc:
    ...                     # 只有 ValidationError 走这里
```

如果 `model_validate` 抛出的是 `TypeError`，这个 `except` 接不住，异常会跳过它继续向上透传到外层调用方。

**多个 `except` 按顺序匹配**

```python
try:
    result = do_thing()
except ValidationError as exc:
    ...                     # 校验失败
except ValueError as exc:
    ...                     # 其他值错误
except Exception as exc:
    ...                     # 兜底：其余所有异常
```

异常从上往下和各个 `except` 比对，匹配到第一个就停。因此更具体的异常要写在上方，`Exception` 这类宽泛的兜底写在最后。如果把 `except Exception` 写在了最上面，后面所有 `except` 永远不会被匹配到。

**`try` / `except` / `else` / `finally`**

```python
try:
    result = do_thing()
except ValueError:
    print("值不对")
else:
    print("成功，结果是", result)
finally:
    print("无论成功失败都执行")
```

- `try`：尝试执行的代码
- `except`：指定异常时执行
- `else`：没有异常时执行（可以拿到 try 块的结果）
- `finally`：无论是否有异常都执行（常用于关闭文件、释放连接）

它与 JavaScript 的对应关系：

| Python | JavaScript |
|--------|------------|
| `try / except` | `try / catch` |
| `except SomeError as e:` | `catch (e) { ... }` |
| `else` | 无直接对应，需在 try 块末尾手动实现 |
| `finally` | `finally` |

### 8.5 `with` 语句与上下文管理器

`with` 语句用于"获取资源 → 使用资源 → 清理资源"的三段式操作，是 `try/finally` 的语法糖。

```python
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

**等价于：**

```python
f = open("data.json", "r", encoding="utf-8")
try:
    data = json.load(f)
finally:
    f.close()  # 无论是否异常都执行
```

**`as` 绑定的是什么**

`as f` 中的 `f` 不是 `open()` 的直接返回值，而是对象 `__enter__()` 方法的返回值。

```python
with open("data.json") as f:
    ...

# 底层等价物：
_mgr = open("data.json")
f = _mgr.__enter__()
try:
    ...
finally:
    _mgr.__exit__(None, None, None)
```

**底层机制：上下文管理器协议**

任何实现了 `__enter__` + `__exit__` 方法的对象都可以放在 `with` 后面。

```python
class Door:
    def __enter__(self):
        print("开门")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("关门")
        # 返回 False = 有异常继续往外抛（默认行为）
```

- `__enter__()`：进入 `with` 时调用，返回值赋给 `as` 后面的变量
- `__exit__()`：退出 `with` 时调用，无论是否异常都执行
- `__exit__` 的三个参数：异常类型、异常值、traceback（没有异常时都是 `None`）

**常见上下文管理器**

| 对象 | `__enter__` 返回 | `__exit__` 做的事 |
|------|-----------------|-------------------|
| `open()` | 文件对象 | 关闭文件 |
| `threading.Lock()` | 锁对象 | 释放锁 |
| `requests.Session()` | Session 实例 | 关闭连接池 |

**不用 `with` 的隐患**

```python
f = open("data.json")
data = json.load(f)
f.close()  # 如果上一行抛异常，这行永远不会执行
```

长时间不关闭文件会导致**文件描述符泄漏**，超过系统限制后 `open()` 会报 `OSError: Too many open files`。

**如何创建上下文管理器**

不用手写类也能造出上下文管理器，用 `@contextmanager` 装饰器即可。详见 [9.6 `@contextmanager` 与 `@asynccontextmanager`](#96-contextmanager-与-asynccontextmanager)。

## 第9章 装饰器

### 9.1 `@decorator`

`@decorator` 等价于：

```python
func = decorator(func)
```

装饰器常用于日志、权限校验、缓存和注册。

### 9.2 带参数装饰器

`@decorator(a, b)` 等价于：

```python
func = decorator(a, b)(func)
```

### 9.3 `@wraps`

`@wraps` 用来保留原函数的 `__name__`、文档、注解等元数据。

```python
from functools import wraps
```

不使用 `@wraps` 时，被包装函数名可能变成 `wrapper`。

### 9.4 Flask 路由装饰器

`@api_app.route(...)` 是带参数装饰器。路由注册发生在模块导入时。

```python
@api_app.route('/review/webhook', methods=['POST'])
@require_json
def handle_webhook():
    ...
```

路由装饰器通常放在最上面，这样 Flask 注册到的是包装后的最终函数。

### 9.5 常见内置装饰器

- `@staticmethod`
- `@classmethod`
- `@property`
- `@dataclass`
- `@lru_cache`

`@lru_cache` 是标准库 `functools` 提供的缓存装饰器。

```python
from functools import lru_cache


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

它的作用是：第一次调用时真正执行函数，并把返回值缓存起来；后续相同调用直接返回缓存结果，不再重新执行函数体。

在没有参数的函数上，`@lru_cache` 通常等价于“把函数结果做成单例缓存”。上面的 `get_settings()` 常见于配置对象场景，目的是避免每次读取配置都重新实例化 `Settings()`。

可以把它近似理解成：

```python
_settings = None


def get_settings():
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
```

`lru_cache` 原本是“最近最少使用缓存”，适合缓存函数结果；这里只是利用了它的“记住返回值”能力。

有参数时，`@lru_cache` 会按参数值分别缓存结果，而不是只缓存一份。

```python
from functools import lru_cache


@lru_cache
def square(x: int) -> int:
    print("run")
    return x * x
```

调用：

```python
square(2)
square(2)
square(3)
square(2)
```

大致效果是：

- 第一次 `square(2)`：执行函数，缓存结果
- 第二次 `square(2)`：直接返回缓存
- `square(3)`：因为参数不同，重新执行函数并缓存另一份结果
- 再次 `square(2)`：继续返回第一次的缓存

可以近似理解成：

```python
cache = {
    (2,): 4,
    (3,): 9,
}
```

如果有多个参数，缓存键也是整组参数：

```python
@lru_cache
def add(a: int, b: int) -> int:
    return a + b
```

近似缓存形态：

```python
{
    (1, 2): 3,
    (2, 3): 5,
}
```

因此 `@lru_cache` 要求参数可哈希；像 `list`、`dict` 这类不可哈希对象通常不能直接作为缓存键。

### 9.6 `@contextmanager` 与 `@asynccontextmanager`

这两个装饰器解决同一个问题：**不用手写类，就能造出一个上下文管理器。**

#### 9.6.1 为什么需要上下文管理器

假设有一段"开门—干活—关门"的逻辑：

```python
open_door()
do_work()        # 如果这行报错，close_door() 就不会执行
close_door()
```

最简单的保证是 `try/finally`：

```python
open_door()
try:
    do_work()
finally:
    close_door()   # 天塌了也执行
```

Python 提供了一个标准语法来封装这个模式——`with`：

```python
with door():       # 进入时开门，退出时自动关门
    do_work()
```

`with` 后面跟的东西叫**上下文管理器**。

#### 9.6.2 第一层：手写类（最底层）

任何实现了 `__enter__` + `__exit__` 的类，都可以放在 `with` 后面。

```python
class Door:
    def __enter__(self):
        print("开门")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("关门")
        # 返回 False = 有异常继续往外抛

with Door():
    print("干活")
# 开门
# 干活
# 关门
```

`with` 底层做的事：

```text
1. 调用 Door().__enter__() → 返回值赋给 as 后面的变量
2. 执行 with 块里的代码
3. 不管第2步成功还是崩了，调用 Door().__exit__()
```

#### 9.6.3 第二层：`@contextmanager` + `yield`（语法糖）

每次写一个简单的开门/关门逻辑都要写类太啰嗦。`@contextmanager` 让你用**一个函数 + 一个 `yield`** 代替整个类。

```python
from contextlib import contextmanager

@contextmanager
def door():
    print("开门")       # with 进入时执行
    yield                # ← 分界点
    print("关门")       # with 退出时执行
```

这个函数经过装饰器后，**变成了一个实现了 `__enter__`/`__exit__` 的对象**。你用 `with door():` 时底层发生的事和手写类完全一样。

```text
你写的函数                    装饰器帮你生成的（等效类）
─────────────────────        ─────────────────────────
def door():                  class _DoorContext:
    print("开门")               def __enter__(self):
    yield               →           print("开门")
    print("关门")               def __exit__(self, ...):
                                    print("关门")

with door():                 with _DoorContext():
    ...                          ...
```

`yield` 在这里**不是生成器**，而是分界点——把函数切成"进"和"出"两半。

#### 9.6.4 第三层：`@asynccontextmanager`（异步版）

和上面完全一样，只是把 `with` 换成 `async with`，`__enter__`/`__exit__` 换成 `__aenter__`/`__aexit__`，函数加 `async`。

```text
同步                             异步
─────────────────────            ─────────────────────
with                              async with
__enter__ / __exit__              __aenter__ / __aexit__
@contextmanager                   @asynccontextmanager
def func():                       async def func():
```

本质是同一个协议的两套版本。

#### 9.6.5 为什么必须搭配 `try/finally`

`__exit__` 在出现异常时，会通过 `athrow()` **把异常扔到 `yield` 那一行**。没有 `try/finally` 的话：

```python
@asynccontextmanager
async def lifespan(app):
    engine = create_engine(...)
    yield                        # ← 异常扔在这一行
    engine.dispose()             # ← 永远跑不到
```

加上 `try/finally`：

```python
@asynccontextmanager
async def lifespan(app):
    engine = create_engine(...)
    try:
        yield                    # ← 异常扔到这里
    finally:
        engine.dispose()         # ← Python 的 finally：天塌了也执行
```

- `@asynccontextmanager` 保证：退出时尝试跑 `yield` 后面的代码
- `try/finally` 保证：扔了异常也能跑
- 两者组合 = 不管正常关闭还是崩了，清理逻辑必执行

#### 9.6.6 经典用法

**数据库事务：**

```python
@asynccontextmanager
async def transaction(db: Session):
    try:
        yield db
        db.commit()          # 正常结束 → 提交
    except Exception:
        db.rollback()        # 出异常 → 回滚
        raise
```

**临时覆盖依赖：**

```python
@asynccontextmanager
async def override_dependency(app, old, new):
    app.dependency_overrides[old] = new
    try:
        yield
    finally:
        del app.dependency_overrides[old]   # 一定恢复原状
```

**计时/度量：**

```python
@asynccontextmanager
async def measure(label: str):
    start = time.time()
    yield
    print(f"{label} 耗时: {time.time() - start:.2f}s")
```

三个用法的本质完全相同：**进时做 A，退出时做 B，用 `try/finally` 保证 B 一定发生**。

#### 9.6.7 两个装饰器的定位

| 装饰器 | 用在 | 函数类型 | 消费方式 |
|--------|------|----------|----------|
| `@contextmanager` | 同步上下文管理器 | `def` + `yield` | `with` |
| `@asynccontextmanager` | 异步上下文管理器 | `async def` + `yield` | `async with` |

FastAPI 的 `lifespan` 要求异步上下文管理器，所以必须用后者。

## 第10章 Pydantic

### 10.1 `BaseModel`

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

### 10.2 `model_validate()`

`model_validate(x)` 用来把一个“已经存在的原始值”按当前模型结构做校验和解析。

```python
class ApprovalDecision(BaseModel):
    approved: bool
    comment: str = ""


decision = {"approved": True, "comment": "可以执行"}
parsed = ApprovalDecision.model_validate(decision)
```

这里的 `decision` 已经是一个现成值。  
`model_validate(...)` 做的是：

- 检查它是否符合 `ApprovalDecision` 的字段结构
- 合法则返回一个 `ApprovalDecision` 实例
- 不合法则抛出校验错误

它适合的场景是：

- 你手里已经有一个字典、JSON 解析结果、外部输入对象
- 现在想“按某个模型重新检查并转成模型实例”

可以把 Pydantic 里几种常见入口区分成：

```python
note = NoteCreate(title="hello")
```

- `Model(...)`：边创建边校验

```python
note = NoteCreate.model_validate(data)
```

- `Model.model_validate(x)`：拿已有值做校验并转成模型

```python
data = note.model_dump()
```

- `instance.model_dump()`：把模型实例转回普通字典

`model_validate(...)` 在接收外部输入时尤其常见，因为这时你通常拿到的不是分散参数，而是一整份已有数据。

### 10.3 `Field`

`Field` 用来给字段补充验证规则和元数据。

```python
title: str = Field(..., min_length=1, max_length=100)
age: int = Field(..., gt=0, lt=150)
email: str = Field(..., pattern=r".+@.+")
```

这里的 `...` 表示必填。只写 `title: str` 时，只有类型信息；写了 `Field(...)` 之后，这个字段还带有长度、范围、正则等附加规则。

可以把 `Field(...)` 理解成“这个字段除了类型之外，还有额外约束”。

### 10.4 `model_dump()`

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

### 10.5 `ValidationError`

`ValidationError` 是 Pydantic 在校验失败时抛出的异常。

```python
from pydantic import ValidationError
```

它不是 Python 内置异常（如 `ValueError`、`KeyError`），而是 Pydantic 自己定义的异常类。

触发场景：

```python
from pydantic import BaseModel, ValidationError


class NoteCreate(BaseModel):
    title: str
    content: str = ""


try:
    note = NoteCreate(title=123)          # title 应该是 str，传了 int
except ValidationError as exc:
    print(exc.errors())                   # 查看具体哪些字段校验失败
```

`NoteCreate(title=123)` 和 `NoteCreate.model_validate({"title": 123})` 都会在校验失败时抛出 `ValidationError`。

**常用属性**

- `exc.errors()`：返回错误列表，每条包含 `loc`（出错字段路径）、`msg`（错误描述）、`type`（错误类型）
- `exc.json()`：返回 JSON 格式的错误详情
- `exc.error_count()`：返回错误数量

`ValidationError` 继承自 Python 的 `Exception`，因此可以像普通异常一样用 `try / except` 捕获。

## 第11章 工程实践

### 11.1 CLI 交互循环

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

### 11.2 `.env` 与 `.env.local`

是否自动读取 `.env.local`，取决于代码如何调用 dotenv。

`load_dotenv()` 默认主要读取 `.env`。如果项目使用 `.env.local`，通常需要显式指定。

### 11.3 `load_dotenv()`

```python
from dotenv import load_dotenv

load_dotenv()
```

它的作用是把环境变量从文件加载到当前进程环境中。

### 11.4 常量时间比较

```python
from hmac import compare_digest

compare_digest(input_password, correct_password)
```

普通 `==` 比较密码时，Python 逐字符比对，第一个不匹配立刻返回 `False`。攻击者可以通过"哪个密码返回 401 耗时更长"来逐步猜出正确密码（时序攻击）。

`compare_digest` 不管第几个字符不匹配，耗时都一样长，杜绝了这种侧信道攻击。属于防御性编程，通常用在登录校验、token 比对等安全敏感场景。
