# LangGraph 学习笔记

## StateGraph

`StateGraph` 用于定义一张基于共享状态的执行图。初始化时传入状态模式，随后注册节点与边，最后编译为可执行对象。

```python
builder = StateGraph(ArticleState)
```

这行代码的含义是：当前图以 `ArticleState` 作为共享状态的结构约束。后续注册到图中的节点，都围绕这份 state 进行读取与更新。

典型构建流程如下：

```python
builder = StateGraph(ArticleState)

builder.add_node("make_outline", make_outline)
builder.add_node("write_article", write_article)

builder.add_edge(START, "make_outline")
builder.add_edge("make_outline", "write_article")
builder.add_edge("write_article", END)

graph = builder.compile()
```

其中：

+ `add_node()` 注册节点
+ `add_edge()` 定义固定执行路径
+ `compile()` 将图定义编译为可执行 graph

## State Schema

LangGraph 中通常先显式定义 state schema，再基于该 schema 组织节点逻辑。这里使用 `TypedDict` 描述共享状态：

```python
from typing import TypedDict


class ArticleState(TypedDict):
    topic: str
    outline: list[str]
    article: str
```

该定义表示：

+ `topic` 为主题字符串
+ `outline` 为提纲列表
+ `article` 为文章正文

运行时传递的对象本质上仍然是 `dict`，但通过 schema 可以明确状态字段、提升可读性，并为类型检查提供依据。

## Node

节点是图中的最小执行单元，通常实现为一个函数。节点接收当前 state，并返回一个状态更新对象。

```python
def make_outline(state: ArticleState) -> dict:
    topic = state["topic"]
    return {
        "outline": [
            f"{topic} 是什么",
            f"{topic} 解决什么问题",
            f"{topic} 最核心的组成部分",
        ]
    }
```

```python
def write_article(state: ArticleState) -> dict:
    lines = "\n".join(f"- {item}" for item in state["outline"])
    return {
        "article": f"# {state['topic']}\n\n{lines}"
    }
```

这里需要注意两点：

+ 节点读取的是“当前完整 state”
+ 节点返回的不是完整 state，而是“本节点产生的状态更新”

例如初始 state 为：

```python
{
    "topic": "LangGraph",
    "outline": [],
    "article": "",
}
```

`make_outline` 返回：

```python
{
    "outline": [
        "LangGraph 是什么",
        "LangGraph 解决什么问题",
        "LangGraph 最核心的组成部分",
    ]
}
```

随后该更新会被合并回当前 state，供后续节点继续使用。`write_article` 的返回值也遵循同样的规则。

因此，在 LangGraph 中更准确的表述是：

+ 节点不直接“构造完整 state”
+ 节点返回的是 partial state update
+ graph 负责将各节点的返回结果合并到共享状态中

## Execution

图编译完成后，可通过 `invoke()` 传入初始 state 并执行：

```python
result = graph.invoke(
    {
        "topic": "LangGraph",
        "outline": [],
        "article": "",
    }
)
```

执行结束后，返回值为最终 state。当前示例中，可直接读取：

```python
result["article"]
```

## Reading Guide

读取一个 LangGraph 示例时，可以按下面的顺序理解：

1. 先看 state schema，确认共享状态包含哪些字段
2. 再看 node，确认每个节点读取哪些字段、更新哪些字段
3. 再看 edge，确认节点之间的流转关系
4. 最后看 `invoke()`，确认初始 state 与最终输出
