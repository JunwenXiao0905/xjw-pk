# LangGraph 学习笔记

## 目录

- [第1章 模块分布与产品分层](#第1章-模块分布与产品分层)
  - [1.1 `langchain_core`、`langchain`、`langgraph`、provider packages、`langsmith`](#11-langchain_corelangchainlanggraphprovider-packageslangsmith)
  - [1.2 常见导入对照](#12-常见导入对照)
  - [1.3 导入判断规则](#13-导入判断规则)
  - [1.4 LangChain、LangGraph、Deep Agents、LangSmith](#14-langchainlanggraphdeep-agentslangsmith)
  - [1.5 Agent 构建思路](#15-agent-构建思路)
- [第2章 StateGraph 最小骨架](#第2章-stategraph-最小骨架)
  - [2.1 `StateGraph`](#21-stategraph)
  - [2.2 `State Schema`](#22-state-schema)
  - [2.3 `Node`](#23-node)
    - [节点执行机制：三种形式封装方式](#节点执行机制三种封装方式)
  - [2.4 `START`、`END` 与图内起止点](#24-startend-与图内起止点)
  - [2.5 `add_conditional_edges`](#25-add_conditional_edges)
  - [2.6 `Command(goto=...)` 与 `destinations`](#26-commandgoto-与-destinations)
- [第3章 聊天状态与工具调用](#第3章-聊天状态与工具调用)
  - [3.1 `MessagesState`](#31-messagesstate)
  - [3.2 `model.bind_tools()`、`ToolNode`、`tools_condition`](#32-modelbind_tools-toolnode-tools_condition)
  - [3.3 `tools_condition` 与隐式 `END`](#33-tools_condition-与隐式-end)
  - [3.4 `create_agent` — ReAct Agent 工厂](#34-create_agent--react-agent-工厂)
- [第4章 记忆、暂停与执行](#第4章-记忆暂停与执行)
  - [4.1 `checkpointer`](#41-checkpointer)
  - [4.2 `interrupt()` 与 `Command(resume=...)`](#42-interrupt-与-commandresume)
    - [代码模板：Pydantic 校验 + interrupt 循环](#代码模板pydantic-校验--interrupt-循环)
  - [4.3 `invoke()`、`stream()` 与执行入口](#43-invokestream-与执行入口)
  - [4.4 输出形态](#44-输出形态)
  - [4.5 示例阅读顺序](#45-示例阅读顺序)
  - [4.6 递归限制与步数管理](#46-递归限制与步数管理)
    - [`recursion_limit` 的两种配置方式](#recursion_limit-的两种配置方式)
    - [`IsLastStep` 与 `RemainingSteps`](#islaststep-与-remainingsteps)
    - [分层保护实践](#分层保护实践)
- [第5章 并行执行](#第5章-并行执行)
  - [5.1 为什么需要并行](#51-为什么需要并行)
  - [5.2 `Send`](#52-send)
  - [5.3 分发函数](#53-分发函数)
  - [5.4 并行写入：`Annotated` + reducer](#54-并行写入annotated--reducer)
  - [5.5 完整示例](#55-完整示例)
  - [5.6 与条件路由的区别](#56-与条件路由的区别)
- [第6章 调试与观测](#第6章-调试与观测)
  - [6.1 本地调试：`print` / `stream` / `get_state`](#61-本地调试print--stream--get_state)
  - [6.2 LangSmith：官方云平台](#62-langsmith官方云平台)
  - [6.3 LangFuse：开源替代](#63-langfuse开源替代)

- [第7章 子图](#第7章-子图)
  - [7.1 子图是什么](#71-子图是什么)
  - [7.2 状态共享](#72-状态共享)
  - [7.3 观测差异](#73-观测差异)
  - [7.4 完整示例](#74-完整示例)
  - [7.5 与普通节点的区别](#75-与普通节点的区别)
- [第8章 持久化存储（SqliteSaver）](#第8章-持久化存储sqlitesaver)
  - [8.1 与 InMemorySaver 的区别](#81-与-inmemorysaver-的区别)
  - [8.2 接入方式](#82-接入方式)
  - [8.3 时间旅行](#83-时间旅行)
  - [8.4 完整示例](#84-完整示例)
- [第9章 Multi-Agent Supervisor](#第9章-multi-agent-supervisor)
  - [9.1 架构模式](#91-架构模式)
  - [9.2 Supervisor 节点](#92-supervisor-节点)
  - [9.3 Worker 节点](#93-worker-节点)
  - [9.4 图结构与循环](#94-图结构与循环)
  - [9.5 完整示例](#95-完整示例)
  - [9.6 与子图的区别](#96-与子图的区别)
  
- [第10章 LangGraph Platform与前后端集成](#第10章-langgraph-platform与前后端集成)
  - [10.1 LangGraph Platform是什么](#101-langgraph-platform是什么)
  - [10.2 Resume机制核心原理](#102-resume机制核心原理)
  - [10.3 Resume的核心能力](#103-resume的核心能力)
  - [10.4 前端集成完整示例](#104-前端集成完整示例)
  - [10.5 Resume的进阶用法](#105-resume的进阶用法)
  - [10.6 LangGraph Platform API Endpoints](#106-langgraph-platform-api-endpoints)
  - [10.7 与第4章interrupt的区别](#107-与第4章interrupt的区别)
  - [10.8 实际应用场景](#108-实际应用场景)
  - [10.9 与传统前后端通信的区别](#109-与传统前后端通信的区别)
  - [10.10 快速启动指南](#110-快速启动指南)
  - [10.11 参考链接](#111-参考链接)


## 参考链接

- LangGraph 官方文档：<https://langchain-ai.github.io/langgraph/>
- LangGraph API 参考：<https://reference.langchain.com/python/langgraph>
- LangChain v1 文档：<https://docs.langchain.com/oss/python/langchain>
- LangChain API 参考：<https://reference.langchain.com/python/langchain>
- LangSmith 平台：<https://smith.langchain.com/>


## 第1章 模块分布与产品分层

### 1.1 生态结构树与常用 API

这里更适合把它看成“职责结构树”，不是 Python 包的真实嵌套树。

```text
LangChain 生态
├─ langchain_core                          # 基础抽象层：消息、工具、Runnable
│  ├─ messages                            # 聊天消息类型
│  │  ├─ HumanMessage                     # 用户消息
│  │  ├─ AIMessage                        # 模型消息
│  │  ├─ SystemMessage                    # 系统提示消息
│  │  └─ ToolMessage                      # 工具执行结果消息
│  ├─ tools
│  │  └─ @tool                            # 把 Python 函数声明成工具
│  └─ runnables
│     ├─ Runnable                         # 可组合调用抽象
│     └─ RunnableConfig                   # 调用配置
│
├─ provider packages                      # 具体模型/Embedding 厂商接入
│  ├─ langchain_openai                    # OpenAI 接入包
│  │  ├─ ChatOpenAI                       # OpenAI 聊天模型客户端
│  │  └─ OpenAIEmbeddings                 # OpenAI 向量模型客户端
│  └─ 其他模型包
│     └─ 例如 langchain_anthropic         # Anthropic 接入包
│
├─ langgraph                              # 运行时层：状态图、记忆、中断恢复
│  ├─ graph
│  │  ├─ StateGraph                       # 自定义共享状态图
│  │  ├─ MessagesState                    # 聊天消息状态 schema
│  │  ├─ START                            # 图起点
│  │  └─ END                              # 图终点
│  ├─ prebuilt
│  │  ├─ ToolNode                         # 执行模型发起的工具调用
│  │  ├─ tools_condition                  # 判断是否流转到工具节点
│  │  └─ create_react_agent               # LangGraph 提供的预构建 ReAct agent
│  ├─ checkpoint.memory
│  │  └─ InMemorySaver                    # 内存版 checkpointer
│  └─ types
│     ├─ interrupt                        # 在节点中暂停 graph
│     └─ Command                          # resume / goto / update 控制对象
│
├─ langchain                              # 高层 agent framework
│  └─ agents
│     └─ create_agent                     # 更高层的 agent 入口
│
└─ langsmith                              # 平台层：观测、评测、部署
   ├─ observability                       # tracing / debug
   ├─ evaluation                          # 评测与数据集
   └─ deployment                          # 部署与托管运行
```

按这一棵树理解：

- `langchain_core` 放基础抽象。先定义“消息长什么样、工具长什么样、Runnable 如何调用”。
- `provider packages` 放具体模型接入。模型客户端通常不在 `langgraph` 里。
- `langgraph` 放 runtime。这里解决 state、节点、边、工具流转、持久化、中断恢复。
- `langchain` 放更高层 agent 入口。它不是 `langgraph` 的替代品，而是建立在 runtime 之上的 framework。
- `langsmith` 放 tracing、evaluation、deployment。它不是你日常在 graph 代码里大量 import 的模块。

如果只看当前学习路径，最常碰到的导入来源是：

- `langchain_core.messages`
- `langchain_core.tools`
- `langchain_openai`
- `langgraph.graph`
- `langgraph.prebuilt`
- `langgraph.checkpoint.memory`
- `langgraph.types`

### 1.2 常见导入对照

```python
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

from langchain.agents import create_agent
```

这组导入背后的分工是：

- 消息和工具来自 `langchain_core`
- 模型客户端来自 provider package
- 图运行时来自 `langgraph`
- 更高层的 agent 入口通常来自 `langchain`

### 1.3 导入判断规则

导入判断可以按问题来做：

- “这个对象是不是跨框架都能复用的基础抽象？”如果是，先看 `langchain_core`
- “我是不是想快速起一个 agent，而不是手写 graph？”如果是，先看 `langchain`
- “我是不是要控制 state、节点、边、记忆、暂停恢复？”如果是，先看 `langgraph`
- “我是不是要接具体模型？”如果是，去 provider package
- “我是不是要 tracing、评测、部署？”如果是，去看 `LangSmith`

一个简单记忆法：

- `langchain_core` 解决“对象长什么样”
- `langchain` 解决“高层 agent 怎么搭”
- `langgraph` 解决“运行时怎么流转、暂停、恢复、持久化”
- provider packages 解决“模型从哪里来”
- `langsmith` 解决“如何观测、评测、部署”

### 1.4 LangChain、LangGraph、Deep Agents、LangSmith

按官方当前产品分层，可以这样理解：

- LangChain：framework。提供模型、工具、agent loop、middleware 等高层抽象，适合快速起步。
- LangGraph：runtime。提供 durable execution、streaming、human-in-the-loop、thread persistence、low-level orchestration。
- Deep Agents：harness。是在 LangGraph 之上再加一层“带电池”的 agent 套件，内置规划、文件系统、subagents、上下文管理。
- LangSmith：平台。提供 observability、evaluation、deployment。它是框架无关的，不要求必须用 LangChain 或 LangGraph。

关系不要记反：

- LangChain agents 构建在 LangGraph runtime 之上
- Deep Agents 构建在 LangGraph runtime 之上，并复用 LangChain 的部分基础构件
- LangSmith 不是 LangGraph 的一个 Python 子模块，而是独立的平台产品

当前官方命名里，原来的 LangGraph Platform 已并入 LangSmith Deployment。

### 1.5 Agent 构建思路

从模块分布反推 agent 的构建路径：

1. 先选模型客户端。通常来自 `langchain_openai`、`langchain_anthropic` 等 provider package。
2. 再定义消息和工具。通常来自 `langchain_core`。
3. 决定 orchestration 层：
   - 快速起步：`langchain.create_agent`
   - 自定义状态流转：`langgraph`
   - 复杂自主任务：`deepagents`
4. 如果需要持久化、人工审批、长流程恢复，核心 runtime 在 `langgraph`
5. 如果需要 tracing、评测、线上部署，核心平台在 `LangSmith`

所以“agent 的构建思路”不是只看一个包，而是看分层：

- abstraction：LangChain / langchain_core
- runtime：LangGraph
- harness：Deep Agents
- platform：LangSmith

## 第2章 StateGraph 最小骨架

### 2.1 `StateGraph`

`StateGraph` 用于定义一张基于共享状态的执行图。初始化时传入状态 schema，随后注册节点与边，最后编译为可执行对象。

```python
builder = StateGraph(ArticleState)
```

这里最需要区分的是：

- `ArticleState` 传进去的是 schema 类型对象
- 它不是某一份运行时 state 数据
- 这里传的不是 `{"topic": ...}` 这种具体对象

更严格地说，`ArticleState` 在 Python 里是 `TypedDict` 定义出来的类型对象；但在 `StateGraph(ArticleState)` 这行代码里，它扮演的是“状态结构说明书”，不是运行时实例。

这行代码的含义是：当前图以 `ArticleState` 作为共享状态的结构约束。后续注册到图中的节点，都围绕这份 state 进行读取与更新。

典型构建流程：

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

- `add_node()` 注册节点
- `add_edge()` 定义固定执行路径
- `compile()` 将图定义编译为可执行 graph

### 2.2 `State Schema`

LangGraph 中通常先显式定义 state schema，再基于该 schema 组织节点逻辑。这里使用 `TypedDict` 描述共享状态：

```python
from typing import TypedDict


class ArticleState(TypedDict):
    topic: str
    outline: list[str]
    article: str
```

该定义表示：

- `topic` 是主题字符串
- `outline` 是提纲列表
- `article` 是文章正文

要区分三样东西：

- `ArticleState`：schema 类型对象
- `state: ArticleState`：类型标注，表示这个参数应满足该 schema
- `{"topic": "...", "outline": [], "article": ""}`：运行时真正传递的 state 数据

运行时传递的对象本质上仍然是 `dict`，但 schema 明确了状态字段，也让节点更新边界更清楚。

**Reducer：字段合并策略**

Schema 里不标 `Annotated` 的字段，节点返回时默认**覆盖**旧值。如果需要**追加**而不是覆盖，要用 `Annotated` 指定 reducer：

```python
from typing import TypedDict, Annotated
import operator


class MyState(TypedDict):
    sections: Annotated[list[str], operator.add]   # 用 + 拼接
    topic: str                                      # 默认覆盖
```

假设当前 state 是：

```python
{"sections": ["a", "b"], "topic": "hello"}
```

节点返回：

```python
{"sections": ["c"], "topic": "world"}
```

合并后：

```python
{"sections": ["a", "b", "c"], "topic": "world"}
#  ↑ 用 operator.add 拼接到旧列表    ↑ 直接覆盖
```

- `sections`：经过 `operator.add(old, new)`，等价于 `old + new`
- `topic`：没有 reducer，直接用新值覆盖

`operator.add` 之所以能充当 reducer，是因为它满足 reducer 的函数签名：`(old_value, new_value) -> merged_value`。

LangGraph 内置的 `MessagesState` 就是对这个模式的使用——`messages` 字段用了一个追加式 reducer，所以消息列表才会跨节点自动拼接，而不是每步被覆盖。

如果字段注释为 `Annotated[list[str], operator.add]`，并不是 LangGraph 自动“推导出 reducer”；而是你在写 schema 时就显式指定了合并策略，LangGraph 只负责在节点返回时读取并执行它。

### 2.3 `Node`

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

这里要记住：

- 节点读取的是当前完整 state
- 节点返回的是 partial state update，不是完整 state
- graph 负责把多个节点的返回结果合并回共享状态

例如初始 state：

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

随后该更新被合并回当前 state，供后续节点继续使用。

**节点执行机制：三种封装方式**

`add_node("name", x)` 时，`x` 可以是三种形式：

| 形式 | 例子 | 特点 |
|------|------|------|
| 普通函数 | `def f(state) -> dict` | 最简单，返回部分状态更新 |
| Runnable | `ToolNode(TOOLS)` | 本身是 Runnable，有 `.invoke()` |
| Runnable | `ChatOpenAI(...)` | 同上 |

LangGraph 内部不关心你传的是哪种 — 它会把一切统一包装成 `RunnableCallable`，运行时统一调 `.invoke(state)`：

```text
add_node("foo", my_func)      ─→  包装成 RunnableCallable  ─→  runtime: .invoke(state)
add_node("tools", ToolNode)   ─→  已是 Runnable，免包     ─→  runtime: .invoke(state)
add_node("bot", ChatOpenAI)   ─→  已是 Runnable，免包     ─→  runtime: .invoke(state)
```

所以 `ToolNode(TOOLS)` 不用包一层也能直接当节点函数 — 它有 `.invoke()`，正好是 LangGraph 要的接口。

那为什么有些代码会手动包一层？

```python
TOOL_NODE = ToolNode(TOOLS)

def tools_runner(state: MessagesState) -> dict:
    print(state)                     # 在工具执行前插入逻辑
    return TOOL_NODE.invoke(state)   # 手动调真正的 ToolNode
```

这不是为了兼容 LangGraph，而是为了在节点前后插入额外逻辑（日志、校验、副作用）。包一层后传给 `add_node` 的 `tools_runner` 仍然是普通函数，LangGraph 照常包装它。

因此：**LangGraph 的节点调用统一走 `.invoke()`，开发者手动调 `TOOL_NODE.invoke(state)` 只是 Runnable 的正常用法，和框架执行机制无关。**

返回值合并规则不变：
- 节点 `return {"field": new_value}`
- LangGraph 将 `new_value` 合并回共享 state
- 下一个节点读到的 state 已包含此更新

### 2.4 `START`、`END` 与图内起止点

`START` 和 `END` 是 graph 内部的逻辑起止点，不是 Python 侧的调用入口。

例如：

```python
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
```

这里表达的是：

- 图从 `START` 流转到 `chatbot`
- `chatbot` 执行完后流转到 `END`

要区分两层概念：

- `invoke()` / `stream()`：Python 侧如何启动 graph
- `START` / `END`：graph 内部从哪里开始、到哪里结束

因此：

- `START` 解决“图内部第一步去哪里”
- `END` 解决“图内部到哪里算执行完成”
- 它们不等于外部调用入口

### 2.5 `add_conditional_edges`

`add_conditional_edges` 用于定义动态路由：根据当前 state 决定下一步去哪个节点。

它和 `add_edge` 的核心区别：

- `add_edge("A", "B")`：编译时写死，A 执行完永远去 B
- `add_conditional_edges("A", route)`：运行时动态决定，每次根据 state 计算出目标节点

**函数签名**

```python
builder.add_conditional_edges(source, condition_fn, path_map=None)
```

其中：

- `source`：出发节点名
- `condition_fn`：路由函数，签名为 `(state) -> str`，返回目标节点名
- `path_map`：可选映射字典，把 condition_fn 的返回值映射到实际节点名

最简写法不传 `path_map`，condition_fn 直接返回节点名。

**condition_fn 规范**

```python
def route(state: RouterState) -> str:
    keyword = state["keyword"]
    if "write" in keyword:
        return "writer"
    elif "chat" in keyword:
        return "chatbot"
    else:
        return "fallback"
```

规范是：

- 接收当前 state（类型与 StateGraph 的 state schema 一致）
- 必须返回一个字符串
- 这个字符串就是目标节点名

路由逻辑纯由业务决定。返回值写什么，图就流转到对应的已注册节点。

**完整示例**

基于 `router_graph.py` 的关键词路由：

```python
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class RouterState(TypedDict):
    keyword: str


def router_node(state: RouterState) -> dict:
    return state


def writer(state: RouterState) -> dict:
    return state


def chatbot(state: RouterState) -> dict:
    return state


def fallback(state: RouterState) -> dict:
    return state


def route(state: RouterState) -> str:
    keyword = state["keyword"]
    if "write" in keyword:
        return "writer"
    elif "chat" in keyword:
        return "chatbot"
    else:
        return "fallback"


builder = StateGraph(RouterState)

builder.add_node("router", router_node)
builder.add_node("writer", writer)
builder.add_node("chatbot", chatbot)
builder.add_node("fallback", fallback)

builder.add_edge(START, "router")
builder.add_conditional_edges("router", route)
builder.add_edge("writer", END)
builder.add_edge("chatbot", END)
builder.add_edge("fallback", END)

graph = builder.compile()
```

执行时，`route(state)` 拿到当前 state 的 `keyword` 字段，根据内容返回不同字符串，图据此分流到 writer、chatbot 或 fallback。

图中的边结构是：

```text
START -> router
router -> writer   # keyword 包含 "write"
router -> chatbot  # keyword 包含 "chat"
router -> fallback # 其他情况
writer -> END
chatbot -> END
fallback -> END
```

**与 `tools_condition` 的关系**

`tools_condition` 就是一个预制的 condition_fn，符合 `(state) -> str` 规范。

```python
builder.add_conditional_edges("chatbot", tools_condition)
```

等价于手写：

```python
def my_tools_condition(state: MessagesState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "__end__"

builder.add_conditional_edges("chatbot", my_tools_condition)
```

因此 `tools_condition` 不是独立 API，它只是一个符合 condition_fn 规范的内置函数。理解了 `add_conditional_edges` 的机制后，`tools_condition` 就不再神秘。

**path_map 的使用场景**

如果 condition_fn 返回的内部标识和目标节点名不同，用 path_map 做映射：

```python
builder.add_conditional_edges(
    "router",
    route,
    path_map={
        "write": "writer_node",
        "chat": "chatbot_node",
        "fallback": "fallback_node",
    },
)
```

此时 condition_fn 返回 `"write"`，但图去的是 `"writer_node"`。通常不需要 path_map，直接让 condition_fn 返回目标节点名更直观。

### 2.6 `Command(goto=...)` 与 `destinations`

`add_edge` 和 `add_conditional_edges` 都是"边决定路由"：节点返回普通 `dict`，图根据边声明决定下一步去哪。

`Command(goto=...)` 是第三种路由方式：**节点自己决定下一步去哪**。节点直接返回包含目标节点名的 `Command` 对象，不再返回 `dict`。

**示例**

```python
from langgraph.types import Command


def approve_tools(state: MessagesState) -> Command:
    last_message = state["messages"][-1]
    tool_calls = getattr(last_message, "tool_calls", [])

    if not tool_calls:
        return Command(goto="chatbot")          # 无工具调用，回到 chatbot

    decision = interrupt(...)
    if decision.approved:
        return Command(goto="tools")            # 批准，去执行工具
    else:
        return Command(goto="finish_rejected")  # 拒绝，去结束节点
```

一个节点有三个分支，每个 `return` 指向不同目标。这些目标不是写在 `add_conditional_edges` 上，而是写在 `return Command(goto=...)` 里。

**`destinations` 参数**

由于路由写在节点内部，LangGraph 编译时不知道这个节点能去哪。因此需要在 `add_node` 时声明：

```python
builder.add_node(
    "approve_tools",
    approve_tools,
    destinations=("tools", "finish_rejected", "chatbot"),
)
```

三个 `goto` 目标对应三个 `destinations` 值。不声明的话编译可能报错，因为图拓扑不完整。

**`Command(update=..., goto=...)` 同时更新状态并路由**

如果节点既要修改 state 又要控制路由：

```python
def approve_tools(state) -> Command:
    ...
    return Command(
        update={"messages": [AIMessage(content="已拒绝。")]},
        goto="finish_rejected",
    )
```

这里 `update` 替代了普通节点 `return {"messages": [...]}` 的职责，`goto` 同时指定目标节点。

**三种路由方式对比**

| 方式 | 节点返回 | 路由声明位置 | 路由由谁决定 |
|------|---------|------------|------------|
| `add_edge("A","B")` | `dict` | 边上 | 编译时写死 |
| `add_conditional_edges("A", fn)` | `dict` | condition_fn 返回值 | 运行时，condition_fn |
| `Command(goto="B")` | `Command` | 节点内部 `return` | 运行时，节点自身 |

前两种节点返回 `dict`，路由由边控制。第三种节点返回 `Command`，路由由节点内部控制。

**何时用 Command 路由**

- `Command(resume=...)` 用于恢复中断（见 4.2）
- `Command(goto=...)` 用于节点内部有复杂分支逻辑，且用 `add_conditional_edges` 表达不够直观时
- 两者可以出现在同一节点：先 `interrupt(...)` 暂停，恢复后用 `Command(goto=...)` 决定去向

## 第3章 聊天状态与工具调用

### 3.1 `MessagesState`

`MessagesState` 是 LangGraph 内置的聊天状态 schema，适合 tool-calling graph。

它的关键不是“有个 `messages` 字段”这么简单，而是：

- `messages` 使用了追加式 reducer
- 节点返回新的消息后，LangGraph 会把它合并进已有消息列表

因此：

- `MessagesState` 负责“消息列表如何合并”
- `checkpointer` 负责“整份 state 是否跨轮保存”

不要混淆：

- 多轮消息追加，不是 `InMemorySaver` 的功能
- `InMemorySaver` 只负责把 state 按 `thread_id` 存起来

### 3.2 `model.bind_tools()`、`ToolNode`、`tools_condition`

LangGraph 里最常见的工具调用组合是：

- `model.bind_tools(TOOLS)`
- `ToolNode(TOOLS)`
- `tools_condition`

标准循环：

```python
chatbot -> tools -> chatbot
```

职责分工：

- 模型节点负责决定“要不要调工具”
- `ToolNode` 负责真的执行工具
- `tools_condition` 负责检查最后一个 `AIMessage` 里有没有 tool calls

如果有 tool calls，流转到 `tools`；如果没有，就结束或进入下一段流程。

### 3.3 `tools_condition` 与隐式 `END`

`tools_condition` 不只是判断“去不去 tools”，它还内置了结束路由。

它的标准返回逻辑是：

- 最后一个 `AIMessage` 有 tool calls：返回 `"tools"`
- 最后一个 `AIMessage` 没有 tool calls：返回 `"__end__"`

因此下面这段图定义：

```python
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")
```

实际等价于：

```text
chatbot -> tools   # 有 tool calls
chatbot -> END     # 无 tool calls
tools -> chatbot
```

所以 tool-calling graph 不一定需要显式写：

```python
builder.add_edge("chatbot", END)
```

因为 `tools_condition` 已经通过返回 `__end__` 表达了”结束”。

### 3.4 `create_agent` — ReAct Agent 工厂

`create_agent` 是 LangChain v1 提供的 ReAct Agent 工厂函数（前身是 `langgraph.prebuilt.create_react_agent`，已于 LangGraph v1 废弃）。调用它，自动返回一个编译好的 `CompiledStateGraph`，内部实现标准的 Reason → Act → Reason → Act → ... → Final Answer 循环。

```python
from langchain.agents import create_agent

agent = create_agent(
    model=”openai:gpt-4o”,
    tools=[check_weather],
    system_prompt=”You are a helpful assistant.”,
)
```

返回的 `agent` 是一个**可直接调用的子图**，可以作为普通节点嵌入更大的父图。

**内部结构：仍是 2 节点 LangGraph 子图**

`create_agent` 本质是 LangGraph 的上层封装，底层编译出来的图结构不变：

```
┌──────────┐     ┌──────────┐
│  model   │────▶│  tools   │
│ (LLM)    │◀────│ (exec)   │
└──────────┘     └──────────┘
```

| 节点 | 做什么 |
|------|--------|
| `model` | 调用 LLM。LLM 返回两种可能：① `AIMessage`（纯文本，循环结束）② `AIMessage` + `tool_calls`（要求调工具） |
| `tools` | 执行 LLM 要求的工具调用，结果包装成 `ToolMessage` 返回 model 节点 |

循环逻辑：LLM 思考 → 要调工具？→ 是 → 执行工具 → 结果喂回 LLM → LLM 再思考 → 还要调工具？→ 否 → 输出最终回答。

等价手写代码（底层就是这张图）：

```python
builder = StateGraph(MessagesState)
builder.add_node(“model”, model.bind_tools(tools))
builder.add_node(“tools”, ToolNode(tools))
builder.add_edge(START, “model”)
builder.add_conditional_edges(“model”, tools_condition)
builder.add_edge(“tools”, “model”)
graph = builder.compile()
```

**关键参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | `str \| BaseChatModel` | 推理用大模型。支持字符串 `”openai:gpt-4o”` 或 `ChatOpenAI()` 实例。内部自动 `bind_tools(tools)` |
| `tools` | `list[BaseTool] \| None` | 可调用工具列表。`None` 或空列表时不启用工具循环，退化为单次 LLM 调用 |
| `system_prompt` | `str \| SystemMessage \| None` | **仅接受静态字符串或 SystemMessage**。注入到消息列表开头 |
| `middleware` | `list[AgentMiddleware]` | 钩子系统，替代旧 `state_modifier` 的动态 Prompt 能力（见下方） |
| `state_schema` | `type[AgentState] \| None` | 自定义 State schema，必须继承 `AgentState`。用于添加业务字段 |
| `response_format` | `PydanticModel \| dict \| None` | 结构化输出 schema，Agent 最终回复按此格式返回 |
| `checkpointer` | `Checkpointer \| None` | 持久化。提供后，同一 `thread_id` 累积历史消息 |

**`system_prompt`：静态 Prompt 注入**

```python
# 字符串 — 自动转为 SystemMessage
agent = create_agent(model, tools, system_prompt=”You are a GIS assistant.”)

# SystemMessage — 直接传入
agent = create_agent(
    model, tools,
    system_prompt=SystemMessage(content=”You are a GIS assistant.”),
)
```

`system_prompt` 只接受静态内容。如果 Prompt 需要从 state 中动态拼接（如 GeoAgent 的 `_modify_planState`），改用 **middleware**。

**`middleware`：动态钩子系统**

middleware 是 `create_agent` 的核心新增能力，统一了旧 `state_modifier`、`pre_model_hook`、`post_model_hook` 的职责。

```python
from langchain.agents.middleware import AgentMiddleware

class PlanMiddleware(AgentMiddleware):
    “””每次 LLM 调用前，从 state 中提取业务字段拼入 Prompt。”””

    def before_model(self, state, runtime):
        task_desc = state.get(“task_description”, “”)
        plan_text = state.get(“plan_text”, “”)
        prompt = f”任务: {task_desc}\n已有计划: {plan_text}”
        return {“messages”: [SystemMessage(content=prompt)]}
        # 返回的 messages 会插入到 LLM 输入中

agent = create_agent(
    model, tools,
    middleware=[PlanMiddleware()],
)
```

middleware 可用的钩子点：

| 钩子 | 触发时机 | 典型用途 |
|------|---------|---------|
| `before_model` | LLM 调用前 | 动态拼 System Prompt、消息裁剪、上下文注入 |
| `after_model` | LLM 调用后 | 输出校验、内容过滤、guardrails |
| `before_tools` | 工具执行前 | 人工审批、参数改写、权限检查 |
| `after_tools` | 工具执行后 | 结果后处理、日志记录 |
| `wrap_tool_call` | 单个工具调用前后 | 超时控制、重试、结果缓存 |

**`state_schema`：扩展业务字段**

默认 `AgentState` 只有 `messages` 一个字段。要添加业务字段，定义继承 `AgentState` 的 TypedDict：

```python
from langchain.agents import AgentState

class CodeAgentState(AgentState):
    code: str
    target_file_name: str
    working_directory: str
    execution_result: str

agent = create_agent(
    model, tools,
    state_schema=CodeAgentState,  # 现在 Agent 能读写这些业务字段了
)
```

GeoAgent 的等价场景：每个 Agent 类型（Planner/Coder/Cartographer）定义自己的 `XxxAgentState`，把 `code`、`target_file_name` 等字段加进去。

**结束条件**

LLM 什么时候停止循环？两个条件：

1. **LLM 主动结束**：LLM 输出纯 `AIMessage`（不含 `tool_calls`），表示”回答完了”
2. **递归限制**：达到 `recursion_limit`，LangGraph 抛 `GraphRecursionError`。Agent 内部在最后 3 步注入 `”You have X steps remaining”` 提醒消息，催促 LLM 收尾

**作为子图嵌入父图**

`create_agent` 返回的是 `CompiledStateGraph`，可以像普通节点一样嵌入更大的图：

```python
# 每个 Agent 是一个独立子图
planner_agent = create_agent(plan_model, plan_tools, system_prompt=”你是任务规划师。”)
coder_agent = create_agent(code_model, code_tools, state_schema=CodeAgentState)

# 嵌入父图
builder = StateGraph(ParentState)
builder.add_node(“planner”, planner_agent)
builder.add_node(“coder”, coder_agent)
builder.add_edge(“planner”, “coder”)
```

**与手写子图的对比**

| 维度 | 手写多节点子图（GeoAgent Coder） | `create_agent` |
|------|-------------------------------|----------------|
| 节点数 | 5（CodeWriter/Reviewer/Executor/...） | 2（model + tools） |
| 调试循环 | 固定 1-2 次，硬编码 | LLM 自主决定几次 |
| 错误修复 | 依赖 Reviewer 节点一次判断 | LLM 看到错误 → 修改 → 再执行，直到正确 |
| 代码量 | ~200 行 | ~5 行 |
| 钩子插入 | 每个节点前后手动加 | middleware 统一管理 |

选择规则：

- `create_agent`：标准 tool-calling 场景，LLM 自主决策何时调工具、调几次
- 手写 StateGraph：需要在 agent ⇄ tools 循环**之间**插入固定步骤（如每次工具执行后必须走审批）
- 混合：`create_agent` 作为子图嵌入父图，父图在子图前后加自定义节点（GeoAgent 的架构模式）

## 第4章 记忆、暂停与执行

### 4.1 `checkpointer`

`checkpointer` 是 graph 的存档系统，负责保存和恢复 state。

典型写法：

```python
memory = InMemorySaver()
graph = builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "study-thread"}}
```

要点：

- `checkpointer` 保存的是 graph state，不是某个 Python 变量
- `thread_id` 是会话线程标识；同一个 `thread_id` 会复用上一轮 state
- `result = graph.invoke(...)` 里的 `result` 只是返回值；真正被持久化的是 invoke 结束后的 state

因此可以这样理解：

- `MessagesState` 解决“消息怎么合并”
- `checkpointer` 解决“这份 state 怎么跨轮保存”

### 4.2 `interrupt()` 与 `Command(resume=...)`

`interrupt(...)` 用于在节点内部暂停 graph，并把一个值暴露给外部调用方。

```python
decision = interrupt({"question": "Do you approve this task?"})
```

第一次运行到这里时：

- 当前节点中断
- graph 暂停
- 外部会收到 `__interrupt__`
- 后续节点不会继续执行

恢复时用：

```python
Command(resume={"approved": True})
```

要点：

- `interrupt(...)` 不是普通输出，而是控制流暂停点
- `__interrupt__` 是 LangGraph 运行时暴露给外部的中断事件格式
- 恢复后不是从下一行“接着跑栈帧”，而是重新进入该节点
- 重新进入节点后，`interrupt(...)` 会直接返回 `resume` 的值

因此：

- `interrupt` 依赖 checkpointer
- `resume` 依赖同一个 `thread_id`
- `interrupt` 前面的副作用代码可能在恢复时再执行一次

如果执行完第一次中断后调用：

```python
snapshot = graph.get_state(config)
print(snapshot.next)
```

看到的是：

```python
('review_task',)
```

这不是因为 LangGraph 随便决定“把这个节点再跑一次”，而是因为当前图还停在 `review_task` 这一步，没有成功走出这个节点。

实际流转是：

1. `START -> review_task`
2. 进入 `review_task`
3. 执行到 `interrupt(...)`
4. 当前运行立刻暂停
5. `review_task` 还没有正常返回
6. 图因此还不能沿着边流转到 `apply_decision`

所以这时 `snapshot.next` 仍然是 `review_task`。它表示：

- 如果现在继续执行，下一步要跑的还是 `review_task`

恢复时也不是从 `interrupt(...)` 下一行直接接着跑 Python 调用栈，而是重新进入该节点；只是这一次 `interrupt(...)` 会直接返回 `Command(resume=...)` 里提供的值。只有等 `review_task` 真正执行完，图才会继续流转到后续节点。

真实项目里，`resume` 输入通常不能默认相信。  
`interrupt(...)` 只负责把一个 payload 暴露给外部，LangGraph 不会自动保证 `Command(resume=...)` 送回来的值符合你期望的结构。

因此如果节点需要人工输入，通常要自己做输入校验。常见做法是：

1. 节点第一次 `interrupt(...)`，给外部一个输入协议
2. 恢复后先校验 `resume` 值
3. 如果输入合法，继续后续路由
4. 如果输入不合法，不继续执行，而是再次 `interrupt(...)`
5. 新的中断 payload 里补充错误信息、收到的错误输入、期望格式

这类模式本质上是一个“可恢复的输入校验回路”。

例如审批节点可以在 payload 里约定：

```python
{
    "kind": "approval_request",
    "question": "是否批准这些工具调用？",
    "tool_calls": [...],
    "expected_resume_format": {
        "approved": True,
        "comment": "可选备注",
    },
}
```

如果外部恢复时传回的值格式不对，就不要静默兜底继续执行，而是再次中断，并附带：

- `error`：错误说明
- `received`：收到的错误输入
- `expected_resume_format`：期望结构

这样前端或调用方就可以把这次中断渲染成“表单校验失败，请重新填写”的反馈，而不是直接把异常暴露给用户。

如果项目需要更稳定的输入契约，推荐用 Pydantic 或等价 schema 做 `resume` 校验，而不是只靠 `dict.get(...)` 和 `bool(...)` 做宽松解析。这样可以避免把错误输入悄悄解释成批准或拒绝。

**代码模板：Pydantic 校验 + interrupt 循环**

以下模板来自 `approved_tool_calling_graph.py`，展示人工审批工具调用的完整模式。

第一步：用 Pydantic 定义 resume 输入契约。

```python
from pydantic import BaseModel


class ApprovalDecision(BaseModel):
    approved: bool
    comment: str = ""
```

第二步：写审批节点，包含校验回路。

```python
from langgraph.types import interrupt, Command


def review_tool_calls(state: MessagesState) -> dict:
    """在工具执行前暂停，请求人工审批。输入不合法时循环重试。"""

    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls

    while True:
        # 暂停 graph，把工具调用信息暴露给外部
        decision_raw = interrupt(
            {
                "kind": "approval_request",
                "question": "Approve these tool calls?",
                "tool_calls": [
                    {"name": tc["name"], "args": tc["args"]}
                    for tc in tool_calls
                ],
            }
        )

        # 用 Pydantic 校验外部输入
        try:
            decision = ApprovalDecision.model_validate(decision_raw)
        except Exception:
            # 校验失败：再次中断，附带错误信息提示外部重新输入
            continue

        # 校验通过：根据审批结果路由
        if decision.approved:
            return {}  # 正常返回，图继续去 tools 节点
        else:
            # 拒绝：跳过工具执行，返回占位消息直接去 chatbot
            return {
                "messages": [
                    AIMessage(
                        content=f"Tool calls rejected: {decision.comment}"
                    )
                ]
            }
```

第三步：把审批节点插入 chatbot → tools 之间。

```python
builder.add_node("chatbot", chatbot)
builder.add_node("review", review_tool_calls)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_conditional_edges(
    "review",
    lambda state: (
        "tools"
        if hasattr(state["messages"][-1], "tool_calls")
        and state["messages"][-1].tool_calls
        else "__end__"
    ),
)
builder.add_edge("tools", "chatbot")
```

第四步：外部调用方如何响应中断。

```python
config = {"configurable": {"thread_id": "approval-demo"}}

# 第一次 invoke：会停在 review 节点的 interrupt
graph.invoke({"messages": [HumanMessage(content="multiply 3 and 5")]}, config=config)

# 检查是否有待处理的中断
snapshot = graph.get_state(config)
if snapshot.interrupts:
    # 外部（人或 UI）做出决定
    resume_value = {"approved": True, "comment": "ok"}
    # 恢复执行
    graph.invoke(Command(resume=resume_value), config=config)
```

完整流转：

```text
START -> chatbot -> (有 tool call) -> review
                                       review: interrupt, 等待外部
                                       外部: Command(resume={"approved": True})
                                       review: Pydantic 校验通过, 返回 {}
                                       -> tools -> chatbot -> END
```

如果外部传了不合法输入，Pydantic 校验失败后 `continue` 会再次 `interrupt(...)`，形成"校验失败 → 再次中断 → 等待重新输入"的循环，直到输入合法为止。

### 4.3 `invoke()`、`stream()` 与执行入口

`invoke()` 和 `stream()` 都是 Python 侧执行入口。

它们的共同点：

- 都会启动 graph 执行
- 首次执行时通常都会让 graph 从 `START` 开始流转

它们的区别：

- `invoke()`：跑完整个 graph，再一次性返回最终结果
- `stream()`：边执行边返回中间事件

因此要区分：

- “执行入口” 是 `invoke()` / `stream()`
- “图内起点” 是 `START`

恢复执行时还要再注意一层：

- 如果配合 `checkpointer`、同一个 `thread_id`、`Command(resume=...)`
- 那么 `invoke()` / `stream()` 虽然仍然是执行入口
- 但 graph 内部不一定重新从 `START` 开始
- 它可能从上一次保存的 pending state 继续

**`stream()` 的参数**

```python
events = graph.stream(input, config, stream_mode="values")
```

三个参数：

| 参数 | 含义 |
|------|------|
| `input` | 初始 State，传给图的 START 节点 |
| `config` | `{"configurable": {"thread_id": "..."}, "recursion_limit": N}` |
| `stream_mode` | 控制每次事件输出什么（见下表） |

`stream_mode` 四种取值：

| 模式 | 每次事件输出 | 适用场景 |
|------|------------|---------|
| `"values"` | 完整当前 State | 需要看到完整上下文 |
| `"updates"` | 只有本次改动（默认） | 只关心发生了什么变化 |
| `"messages"` | 逐 token / 逐消息 | 聊天流式打字效果 |
| `"custom"` | 节点内部自定义事件 | 节点主动曝露状态 |

以 GeoAgent 为例，用 `"values"` 是为了打印完整 State 的最后一条消息：

```python
events = graph.stream(input, config, stream_mode="values")
for s in events:
    message = s["messages"][-1]       # s 是完整 state
    print(message.content)
```

**`stream()` 不影响节点间传值**

节点之间的 state 传递走的是图内部的合并机制，`stream()` 只是**向外观察**——等图内部完成一次合并后，把当前 state 拷贝一份抛出来。关掉 `print_stream()` 图照样跑。

### 4.4 输出形态

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

如果是聊天 graph，则常见输入是：

```python
graph.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
```

如果使用 `stream()`，除了普通节点更新外，还可能收到：

- 节点更新事件
- `__interrupt__`
- checkpoints
- tasks

### 4.5 示例阅读顺序

读取一个 LangGraph 示例时，建议按下面顺序看：

1. 先看 state schema，确认共享状态有哪些字段
2. 再看节点，确认每个节点读取哪些字段、写回哪些字段
3. 再看边和条件路由，确认状态如何流转
4. 再看是否用了 `ToolNode`、`checkpointer`、`interrupt`
5. 最后看 `invoke()` / `stream()` 的输入、`thread_id`、输出格式

### 4.6 递归限制与步数管理

**`recursion_limit` 的两种配置方式**

`recursion_limit` 限制单次 `invoke()`/`stream()` 调用中图谱可执行的**超步（superstep）**数量，默认 25。达到限制时抛出 `GraphRecursionError`。

两种设置方式：

```python
# 方式一：运行时 config（旧写法，各平台通用）
graph.invoke(input, {"recursion_limit": 50})

# 方式二：编译时设置（LangGraph 1.x 新写法，更清晰）
graph = builder.compile(recursion_limit=50)
```

**`IsLastStep` 与 `RemainingSteps`**

LangGraph 提供两个由运行时自动管理的状态值，从 `langgraph.managed` 导入。两者在 2025 年中后标记为 `NotRequired`——State 中可包含也可省略。

```python
from langgraph.managed import IsLastStep, RemainingSteps

class State(TypedDict):
    messages: list
    is_last_step: IsLastStep        # bool：当前是否到最后一步
    remaining_steps: RemainingSteps  # int：还剩多少步，每步自动减 1
```

| | `IsLastStep` | `RemainingSteps` |
|---|---|---|
| 类型 | `bool` | `int` |
| 含义 | 当前是否到达最后一步 | 还剩多少步 |
| 用法 | `True` → 强制结束 | 倒计时用于提前退出 |

两者都是**运行时注入的只读值**，不能在节点返回中手动修改。`RemainingSteps` 可以设初始值：

```python
class State(TypedDict):
    remaining_steps: RemainingSteps = 25  # 从 25 开始倒数
```

**分层保护实践**

`recursion_limit` 是安全网，不是退出策略。真正的退出策略应该通过条件边路由到 `END`。

```text
Layer 1: 状态计数器（业务逻辑硬限制）
         → 条件路由主动检查 iteration_count >= max，返回 END

Layer 2: 编译时 recursion_limit（框架安全网）
         → graph = builder.compile(recursion_limit=50)

Layer 3: 超时保护（基础设施层兜底）
         → asyncio.wait_for(graph.ainvoke(...), timeout=300)
```

实际用法：条件路由里先查计数器，再查 `remaining_steps`，剩余 ≤ 3 步时主动结束而不是撞墙报错：

```python
def should_continue(state: State) -> Literal["loop", "end"]:
    if state["iteration_count"] >= state["max_iterations"]:
        return "end"                        # 业务逻辑：够了，退出
    if state["remaining_steps"] <= 3:
        return "end"                        # 框架预警：快超了，优雅退出
    return "loop"
```

与 `IsLastStep` 的区别：`IsLastStep` 只在倒数第一步才为 `True`，是"撞墙之前最后一次机会"。`RemainingSteps` 可以在还有余量时提前结束，体验更好。

## 第5章 并行执行

- [5.1 为什么需要并行](#51-为什么需要并行)
  - [5.2 `Send`](#52-send)
  - [5.3 分发函数](#53-分发函数)
  - [5.4 并行写入：`Annotated` + reducer](#54-并行写入annotated--reducer)
  - [5.5 完整示例](#55-完整示例)
  - [5.6 与条件路由的区别](#56-与条件路由的区别)

### 5.1 为什么需要并行

典型场景：根据一个 topic 生成 N 个子主题，每个子主题各自独立写一段，最后合并成完整文章。

顺序执行：

```text
planner → writer_1 → writer_2 → writer_3 → reviewer
```

三个 writer 串行排队，总耗时 = 三个 writer 之和。

并行执行：

```text
                      ┌→ writer(subtopic=A) ─┐
planner ──→ Send() ──→├→ writer(subtopic=B) ─┼──→ reviewer → END
                      └→ writer(subtopic=C) ─┘
```

`planner` 产出子主题列表后，通过 `Send` 扇出到三个并行的 `writer`，每个收到不同 `subtopic`。全部完成后汇合到 `reviewer`。总耗时 ≈ 最慢的那个 writer。

### 5.2 `Send`

`Send(node, arg)` 创建一个并行执行实例：

```python
from langgraph.types import Send

Send("writer", {"subtopic": "核心原理"})
```

- `node`：目标节点名
- `arg`：dict，会和当前 state 合并后传给目标节点

`Send` 不是直接调用，而是把一个"待执行的任务"返回给 LangGraph。LangGraph 收集所有 `Send` 后并行执行。

### 5.3 分发函数

分发函数是放在 `add_conditional_edges` 里的 condition_fn，但它返回 `list[Send]` 而不是字符串：

```python
def continue_to_writers(state: ArticleState) -> list[Send]:
    return [
        Send("writer", {"subtopic": subtopic})
        for subtopic in state["subtopics"]
    ]

builder.add_conditional_edges("planner", continue_to_writers)
```

LangGraph 看到返回 `list[Send]` 时，行为不再是二选一的路由，而是扇出：有多少个 `Send` 就创建多少个并行分支。所有 `Send` 指向同一个节点 `"writer"`，但每个携带不同的 `subtopic` 值。

`planner` 产出 3 个子主题 → `continue_to_writers` 返回 3 个 `Send` → 3 个 `writer` 并行跑。

### 5.4 并行写入：`Annotated` + reducer

并行分支都返回 `{"sections": [...]}`，如果同时写入同一个字段，后写入的会覆盖先写入的。需要用 **reducer** 来合并而不是覆盖：

```python
import operator
from typing import Annotated, TypedDict


class ArticleState(TypedDict):
    topic: str
    subtopics: list[str]
    subtopic: str
    sections: Annotated[list[str], operator.add]
    final_article: str
```

`sections: Annotated[list[str], operator.add]` 拆开看：

- `list[str]`：真实类型
- `operator.add`：reducer 函数。多个分支返回时，用 `operator.add`（即 `list + list`）把新值追加到已有列表末尾，而不是覆盖

因此三个 writer 各返回：

```python
{"sections": ["## 定义与背景\n..."]}
{"sections": ["## 核心原理\n..."]}
{"sections": ["## 应用场景\n..."]}
```

LangGraph 自动合并为：

```python
["## 定义与背景\n...", "## 核心原理\n...", "## 应用场景\n..."]
```

如果不写 `Annotated[..., operator.add]`，最终 `sections` 只会保留最后完成的那个 writer 的结果。

### 5.5 完整示例

基于 `parallel_graph.py`：

```python
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class ArticleState(TypedDict):
    topic: str
    subtopics: list[str]
    subtopic: str
    sections: Annotated[list[str], operator.add]
    final_article: str


def planner(state: ArticleState) -> dict:
    """生成子主题列表。"""
    topic = state["topic"]
    return {
        "subtopics": [
            f"{topic} 的定义与背景",
            f"{topic} 的核心原理",
            f"{topic} 的应用场景",
        ]
    }


def continue_to_writers(state: ArticleState) -> list[Send]:
    """每个子主题一个 Send，分发到 writer 并行执行。"""
    return [
        Send("writer", {"subtopic": subtopic})
        for subtopic in state["subtopics"]
    ]


def writer(state: ArticleState) -> dict:
    """并行分支，处理自己收到的 subtopic。"""
    subtopic = state["subtopic"]
    return {"sections": [f"## {subtopic}\n\n关于「{subtopic}」的阐述。"]}


def reviewer(state: ArticleState) -> dict:
    """汇总所有并行结果。"""
    sections_text = "\n\n".join(state["sections"])
    return {"final_article": f"# {state['topic']}\n\n{sections_text}"}


def build_graph():
    builder = StateGraph(ArticleState)
    builder.add_node("planner", planner)
    builder.add_node("writer", writer)
    builder.add_node("reviewer", reviewer)

    builder.add_edge(START, "planner")
    builder.add_conditional_edges("planner", continue_to_writers)
    builder.add_edge("writer", "reviewer")
    builder.add_edge("reviewer", END)

    return builder.compile()
```

图的实际流转：

```text
START
  └→ planner  (生成 3 个子主题)
        └→ continue_to_writers  (返回 3 个 Send)
              ├→ writer(subtopic=A)  ─┐
              ├→ writer(subtopic=B)  ─┼→ reviewer  (合并 sections)
              └→ writer(subtopic=C)  ─┘        └→ END
```

关键边：

- `add_conditional_edges("planner", continue_to_writers)`：分发函数返回 `list[Send]` 时自动扇出
- `add_edge("writer", "reviewer")`：所有并行 `writer` 完成后，统一进入 `reviewer`。LangGraph 自动等待全部完成，不需要手动计数

### 5.6 与条件路由的区别

`add_conditional_edges` 有两种用法，取决于 condition_fn 返回什么：

| | 返回 `str`（条件路由） | 返回 `list[Send]`（Send API） |
|------|------|------|
| 行为 | 选一条路 | 所有分支并行跑 |
| 分支性质 | 互斥 | 并行 |
| state 写入 | 单节点写入 | 需要 reducer 合并 |
| 汇合时机 | 继续流转 | 所有 Send 完成后自动继续 |

同一个 `add_conditional_edges` API，完全不同的两种行为，取决于返回值类型。

## 第6章 调试与观测

### 6.1 本地调试：`print` / `stream` / `get_state`

不依赖任何外部工具，LangGraph 自带三种本地观测手段。

**节点内 `print`**

在节点函数中打印 state 快照，最直接的方式。`approved_tool_calling_graph.py` 中已有实践：

```python
from pprint import pformat


def print_node_state(node_name: str, state: MessagesState) -> None:
    print(f"\n【节点 {node_name}】当前 state：")
    print(pformat(state, width=100, sort_dicts=False))


def chatbot(state: MessagesState) -> dict:
    print_node_state("chatbot", state)
    ...
```

输出：

```text
【节点 chatbot】当前 state：
{'messages': [HumanMessage(content='multiply 6 by 7')]}

【节点 tools】当前 state：
{'messages': [HumanMessage(...), AIMessage(..., tool_calls=[...])]}
```

优点：零依赖，想看哪个节点就加一行。缺点：大量调用时刷屏，需要手动 grep。

**`stream()`**

`stream()` 边执行边产出事件，不用在每个节点加 print：

```python
for chunk in graph.stream(input, config):
    print(f"事件：{chunk}")
```

每次有节点完成时产出一次事件，格式为 `{node_name: state_update}`：

```python
事件：{'chatbot': {'messages': [AIMessage(...)]}}
事件：{'tools': {'messages': [ToolMessage(...)]}}
事件：{'chatbot': {'messages': [AIMessage(content='6 × 7 = 42')]}}
```

事件类型包括：

| 事件 | 含义 |
|------|------|
| `{node: update}` | 节点完成，产出 state 更新 |
| `__interrupt__` | 图在执行中暂停（见 4.2） |

**`graph.get_state(config)`**

在任意时刻检查图的当前状态，不需要等执行结束：

```python
snapshot = graph.get_state(config)
print(snapshot.values)   # 当前 state 数据
print(snapshot.next)     # 下一步要执行的节点
print(snapshot.interrupts)  # 待处理的中断
```

与 `stream()` 的区别：`stream()` 是被动接收事件，`get_state()` 是主动查询。两者可以组合使用：`stream()` 触发执行，`get_state()` 随时检查当前状态。

三种手段的使用场景：

| 手段 | 场景 |
|------|------|
| 节点内 `print` | 开发时快速看某个节点的输入输出 |
| `stream()` | 看完整执行流程的事件序列 |
| `get_state()` | 中断排查、人工审批循环中检查状态 |

### 6.2 LangSmith：官方云平台

LangSmith 是 LangChain 官方提供的托管观测平台（[smith.langchain.com](https://smith.langchain.com)），与 LangGraph 共享生态，集成最深。

**接入方式**

设三个环境变量，代码无需 import 变更，所有 `graph.invoke()` 自动产生 trace：

```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."       # 从 smith.langchain.com 获取
os.environ["LANGCHAIN_PROJECT"] = "langgraph-study"
```

常用写法：有 key 才开启，无 key 照常运行不上报：

```python
langsmith_key = os.getenv("LANGCHAIN_API_KEY")
if langsmith_key:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = langsmith_key
    os.environ.setdefault("LANGCHAIN_PROJECT", "langgraph-study")
```

**trace 结构**

一次 `graph.invoke()` 生成的调用树：

```text
Project: langgraph-study
  └─ Trace: multiply 6 by 7            ← 整个 invoke() 的顶层容器
       ├─ Span: chatbot                 ← 节点 chatbot
       │    └─ Span: ChatOpenAI         ←   模型调用
       ├─ Span: tools                   ← 节点 tools（ToolNode）
       │    └─ Span: multiply           ←   工具函数
       └─ Span: chatbot                 ← 节点 chatbot（第二次，工具结果传回后）
            └─ Span: ChatOpenAI
```

树结构完全对应图的实际执行顺序。每个 span 含输入 state 快照、输出 state 快照、耗时和 metadata。

**配置项**

| 配置 | 作用 |
|------|------|
| `LANGCHAIN_TRACING_V2` | 开启自动 tracing |
| `LANGCHAIN_API_KEY` | 平台认证 key |
| `LANGCHAIN_PROJECT` | 项目名，同一项目的 trace 聚合在一起 |
| `invoke(config={"metadata": ...})` | 自定义键值对，UI 中可搜索 |
| `invoke(config={"tags": [...]})` | 标签列表，UI 中可按 tag 筛选 |

**定位**

LangSmith 是闭源云平台，免费层有限额。集成最深（同公司），但数据在外。适合深度使用 LangGraph 的团队。示例代码见 `traced_graph.py`。

### 6.3 LangFuse：开源替代

LangFuse 是开源 LLM 观测平台（MIT 协议），Docker 自托管，数据不出机房。框架无关，支持 LangChain、LlamaIndex、OpenAI SDK 等 10+ 框架。

**接入方式**

```python
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()

graph.invoke(
    input,
    config={"callbacks": [langfuse_handler]},
)
```

自托管需要 Docker（ClickHouse + Redis + Postgres），不是 `pip install` 就行。

**与 LangSmith 对比**

| | LangSmith | LangFuse |
|---|---|---|
| 协议 | 闭源 | MIT 开源 |
| 部署 | 云平台 | Docker 自托管 |
| LangGraph 集成 | 原生，同公司 | 走 generic callback 层 |
| 集成质量 | 节点名、state 快照、metadata 完整 | 部分字段丢失（tags/session_id 等有已知 bug） |
| 框架支持 | LangChain/LangGraph 最深 | 框架无关，10+ 框架 |
| 何时选 | 深度 LangGraph 用户，接受云平台 | 多框架混用，数据合规要求 |

**现状**

LangFuse SDK v3 重写为 OpenTelemetry 底层后，与 LangGraph 的集成有已知问题：tags 和 metadata 不传递、streaming 阻断、session_id 丢失。v2.x 更稳定但已不维护。

**结论**

对当前学习阶段，LangFuse 的 Docker 部署成本和集成 bug 不值得。优先用 6.1 的本地调试三件套；需要云端 trace 时直接用 LangSmith 免费层。

## 第7章 子图

### 7.1 子图是什么

子图就是**把一个编译好的 graph 当作另一个 graph 的节点**。

```python
# 构建并编译子图
research_graph = build_research_subgraph()  # 返回 builder.compile()

# 父图中：子图作为节点
builder.add_node("research", research_graph)
```

对父图来说，`"research"` 就是一个节点。但这个节点内部有自己完整的 START → 节点 → 节点 → END 流转，只是父图看不到。

父图视角 vs 实际执行：

```text
父图视角：               实际执行：
START                    START
  ↓                        ↓
research (一个节点)       search_topic
  ↓                        ↓
make_outline             summarize_findings
  ↓                        ↓
write_article            (子图结束，回到父图)
  ↓                        ↓
END                      make_outline
                           ↓
                         write_article
                           ↓
                         END
```

### 7.2 状态共享

父图和子图通过 state 中**同名字段**自动传递数据。

```python
# 子图的 state
class ResearchState(TypedDict):
    topic: str           # ← 与父图共享
    research_done: bool  # ← 与父图共享


# 父图的 state
class ArticleState(TypedDict):
    topic: str           # ← 与子图共享
    research_done: bool  # ← 与子图共享
    outline: list[str]   #   仅在父图
    article: str         #   仅在父图
```

规则：

- **同名字段**：父图 `invoke()` 时传入的值 → 自动进入子图。子图写回的值 → 自动回到父图。不需要手动映射
- **仅父图有的字段**：子图不可见，不会影响子图执行
- **仅子图有的字段**：子图内部可用，子图结束后被丢弃（不合并回父图）

例子：父图传入 `{"topic": "LangGraph", "research_done": False, "outline": [], "article": ""}` → 子图收到 `topic` 和 `research_done`，写入 `research_done=True` → 父图后续节点拿到 `research_done=True`

**关键：结构化字段 vs 消息文本**

子图需要向父图传递结构化信息时，**在子图 Schema 里加同名字段，让节点直接返回**，而不是把信息塞进消息文本再让父图解析。

```python
# ✅ 正确：子图节点直接返回结构化字段
class SubState(TypedDict):
    messages: Annotated[list, add_messages]
    process_decision: str   # ← 与父图同名，自动传回

def sub_node(state: SubState):
    return {"process_decision": '{"next": "Coder"}'}  # 直接写字段

# ❌ 错误：塞进消息文本，父图再抠出来解析
def sub_node(state: SubState):
    return {"messages": [AIMessage(content='{"next": "Coder"}')]}
    # 父图被迫 messages[-1].content → json.loads → 提取字段
```

同名字段自动传递就是 LangGraph 子图的 native 机制。需要 wrapper 翻译层就说明子图 Schema 设计有遗漏。

### 7.3 观测差异

`stream()` 不加参数 vs `stream(subgraphs=True)`，行为完全不同。

**`stream()`（默认）**：子图是黑盒，整个子图执行完只产出一条事件。

```python
for chunk in graph.stream(input):
    print(chunk)

# 输出：
# {'research': {'research_done': True, 'topic': 'LangGraph'}}
# {'make_outline': {'outline': [...]}}
# {'write_article': {'article': '...'}}
```

子图内部的 `search_topic`、`summarize_findings` 完全不可见，只看到 `research` 作为一个节点的最终输出。

**`stream(subgraphs=True)`**：子图内部节点以命名空间形式暴露。

```python
for chunk in graph.stream(input, subgraphs=True):
    print(chunk)

# 输出（关键差异）：
# (('research:<uuid>',), {'search_topic': {'research_done': True}})
# (('research:<uuid>',), {'summarize_findings': None})
# ((), {'research': {'research_done': True, ...}})
# ((), {'make_outline': ...})
# ((), {'write_article': ...})
```

事件格式为 `(namespace, event)`：

- 子图内部事件：`namespace` 是 `('research:<uuid>',)`，标识来自哪个子图实例
- 父图事件：`namespace` 为空元组 `()`

### 7.4 完整示例

基于 `subgraph.py`：

```python
from typing import TypedDict
from langgraph.graph import END, START, StateGraph


# ── 子图 ──
class ResearchState(TypedDict):
    topic: str
    research_done: bool


def search_topic(state: ResearchState) -> dict:
    return {"research_done": True}


def summarize_findings(state: ResearchState) -> dict:
    return {}


def build_research_subgraph():
    builder = StateGraph(ResearchState)
    builder.add_node("search_topic", search_topic)
    builder.add_node("summarize_findings", summarize_findings)
    builder.add_edge(START, "search_topic")
    builder.add_edge("search_topic", "summarize_findings")
    builder.add_edge("summarize_findings", END)
    return builder.compile()


# ── 父图 ──
class ArticleState(TypedDict):
    topic: str
    research_done: bool
    outline: list[str]
    article: str


def make_outline(state: ArticleState) -> dict:
    topic = state["topic"]
    return {"outline": [f"{topic} 的定义", f"{topic} 的原理", f"{topic} 的应用"]}


def write_article(state: ArticleState) -> dict:
    lines = "\n".join(f"- {item}" for item in state["outline"])
    return {"article": f"# {state['topic']}\n\n{lines}"}


def build_parent_graph():
    research_graph = build_research_subgraph()

    builder = StateGraph(ArticleState)
    builder.add_node("research", research_graph)   # 子图作为节点
    builder.add_node("make_outline", make_outline)
    builder.add_node("write_article", write_article)

    builder.add_edge(START, "research")
    builder.add_edge("research", "make_outline")
    builder.add_edge("make_outline", "write_article")
    builder.add_edge("write_article", END)

    return builder.compile()
```

### 7.5 与普通节点的区别

|      | 普通节点                     | 子图                                 |
| ---- | ------------------------ | ---------------------------------- |
| 注册方式 | `add_node("name", func)` | `add_node("name", compiled_graph)` |
| 内部结构 | 单个函数                     | 完整 graph（节点 + 边 + START/END）       |
| 对父图  | 一个叶子步骤                   | 一个黑盒步骤                             |
| 状态交互 | 函数参数直接接收 state           | 同名字段自动双向传递                         |
| 内部观测 | 不需要                      | `stream(subgraphs=True)` 穿透        |
| 适用场景 | 简单处理逻辑                   | 可复用的、内部有多个步骤的流程                    |
|      |                          |                                    |

子图的本质是**封装**：把一个多步流程打包成一个可复用节点，父图只关心输入输出，不关心中间步骤。

## 第8章 持久化存储（SqliteSaver）

### 8.1 与 InMemorySaver 的区别

笔记 4.1 学的 `InMemorySaver` 把 state 存在内存中。`SqliteSaver` 写到 `.sqlite` 文件。

|      | `InMemorySaver` | `SqliteSaver`                     |
| ---- | --------------- | --------------------------------- |
| 存储位置 | 内存              | `.sqlite` 文件                      |
| 进程重启 | 数据丢失            | 按 `thread_id` 自动恢复                |
| 适合场景 | 开发调试、单轮测试       | 生产对话、长期多轮会话                       |
| 并发   | 单线程             | `check_same_thread=False` 支持简单多线程 |

`SqliteSaver` 适合轻量级生产场景：不需要额外部署 Postgres，但进程重启后对话依然完整。

### 8.2 接入方式

只需要三行变化：

```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver


# 创建 SQLite 连接
conn = sqlite3.connect("data/memory.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

graph = builder.compile(checkpointer=memory)
```

之后所有 `invoke()` 调用自动存档。用同一个 `thread_id` 再次调用，会自动加载上一轮的 state。

如果连接串方式（注意：`from_conn_string` 是 generator，用 `with` 管理生命周期）：

```python
with SqliteSaver.from_conn_string("data/memory.sqlite") as memory:
    graph = builder.compile(checkpointer=memory)
    ...
```

生产环境推荐直接传 `sqlite3.Connection`，生命周期由应用自己管理。

### 8.3 时间旅行

`SqliteSaver` 按 `thread_id` 存历史，每次 `invoke()` 都产生一个新的 checkpoint。这意味着：

**查看历史**

```python
for state in graph.get_state_history(config):
    print(state.config, state.values)
```

按时间倒序返回所有 checkpoint，最新的在前。

**回滚到历史状态**

拿到任意 checkpoint 的 `config`，传给 `invoke()` 就能从那个状态继续：

```python
# 拿到最早的 checkpoint
states = list(graph.get_state_history(config))
first_checkpoint = states[-1].config

# 从那个状态继续（模拟"如果当时说了另一句话"）
result = graph.invoke(
    {"messages": [HumanMessage(content="新的消息...")]},
    config=first_checkpoint,
)
```

这会产生新的分支历史，但不会覆盖已有的 checkpoint。本质上是"时间旅行 + 新建分支"。

### 8.4 完整示例

基于 `sqlite_graph.py`，演示多轮对话记忆 + 时间旅行回滚：

```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, MessagesState, StateGraph
from langchain_core.messages import HumanMessage

# ── 连接与构建 ──
conn = sqlite3.connect("data/memory.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

builder = StateGraph(MessagesState)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile(checkpointer=memory)

# ── 第1轮：正常对话 ──
config_a = {"configurable": {"thread_id": "demo-user-1"}}
result = graph.invoke({"messages": [HumanMessage(content="你好，我是 Alice。")]}, config_a)

# ── 第2轮：同一 thread，模型记得 Alice ──
result = graph.invoke({"messages": [HumanMessage(content="我叫什么名字？")]}, config_a)
# AI: 你叫 Alice！

# ── 第3轮：新 thread，全新对话 ──
config_b = {"configurable": {"thread_id": "demo-user-2"}}
result = graph.invoke({"messages": [HumanMessage(content="我叫什么名字？")]}, config_b)
# AI: 抱歉，我不知道您的名字...

# ── 时间旅行：查看历史 ──
for state in graph.get_state_history(config_a):
    print(state.config)

# ── 时间旅行：回滚到早期继续 ──
states = list(graph.get_state_history(config_a))
first = states[-1].config
result = graph.invoke(
    {"messages": [HumanMessage(content="我是 Bob。")]},
    config=first,
)
```

## 第9章 Multi-Agent Supervisor

### 9.1 架构模式

Multi-Agent 是 LangGraph 的进阶编排模式。核心思路：**一个 supervisor LLM 负责决策，多个 worker 负责执行**。

```text
                  ┌→ writer ────────┐
                  ├→ researcher ────┤
START → supervisor ┤                └→ supervisor → ... → END
                  └→ reviewer ──────┘
```

与传统单 Agent 的区别：

- 单 Agent：一个 LLM 既思考又执行
- Supervisor 模式：一个 LLM 只负责路由决策，具体工作交给专门的 worker

### 9.2 Supervisor 节点

supervisor 是图里唯一的决策节点。它的工作不是"干活"，而是"分活"。

```python
SUPERVISOR_SYSTEM = SystemMessage(
    "你是任务调度中心。根据用户请求，决定调用哪个 worker。"
    "只返回 worker 名称或 END。"
    "- writer: 写代码/文章"
    "- researcher: 查找资料/解释概念"
    "- reviewer: 检查代码/找 bug"
)


def supervisor(state: MessagesState) -> dict:
    model = build_model()
    # 让模型根据对话历史决定下一步去哪个 worker
    response = model.invoke([SUPERVISOR_SYSTEM, *state["messages"]])
    # 解析返回结果，提取 worker 名称
    next_node = parse_worker_name(response.content)  # writer/researcher/reviewer/END
    return {"messages": [HumanMessage(content=f"路由到: {next_node}")]}
```

supervisor 的输出是一个路由消息，告诉图下一步去哪个 worker。

### 9.3 Worker 节点

每个 worker 是独立的执行节点，有自己专门的 system prompt。

```python
WRITER_SYSTEM = SystemMessage("你是一个代码/文章写作者。简洁回答。")


def writer(state: MessagesState) -> dict:
    model = build_model()
    response = model.invoke([WRITER_SYSTEM, *state["messages"]])
    return {"messages": [HumanMessage(content=response.content, name="writer")]}
```

worker 的特点：
- 有专门的 system prompt，限定其角色和输出格式
- 完成后把结果写回 state 的 messages 列表
- 不负责路由决策，只执行具体任务

### 9.4 图结构与循环

关键在边的设计：

```python
# supervisor → 动态路由 → worker
builder.add_conditional_edges("supervisor", route_after_supervisor)

# worker → supervisor（每个 worker 完成后回到 supervisor）
for worker in ["writer", "researcher", "reviewer"]:
    builder.add_edge(worker, "supervisor")
```

这形成了一个**循环**：

```
supervisor → writer → supervisor → researcher → supervisor → END
```

supervisor 每次决定去哪个 worker，worker 完成后回到 supervisor，supervisor 再次决定。直到 supervisor 决定 END 为止。

**防止无限循环**

因为图有循环，需要设置最大步数：

```python
graph = builder.compile()
graph = graph.with_config({"recursion_limit": 10})
```

`recursion_limit` 限制图的最大执行步数，超过就报错，而不是无限循环。

### 9.5 完整示例

基于 `multi_agent_supervisor.py`：

```python
from typing import Literal
from langgraph.graph import END, START, MessagesState, StateGraph

# ── Supervisor ──
def supervisor(state: MessagesState) -> dict:
    model = build_model()
    response = model.invoke([SUPERVISOR_SYSTEM, *state["messages"]])
    # 解析：如果包含 "writer" 就去 writer，包含 "researcher" 就去 researcher...
    for worker in WORKERS:
        if worker in response.content.lower():
            return {"messages": [HumanMessage(content=f"路由到: {worker}")]}
    return {"messages": [HumanMessage(content="路由到: END")]}


# ── Workers ──
def writer(state: MessagesState) -> dict:
    model = build_model()
    response = model.invoke([WRITER_SYSTEM, *state["messages"]])
    return {"messages": [HumanMessage(content=response.content, name="writer")]}


# ── 路由函数 ──
def route_after_supervisor(state: MessagesState) -> Literal["writer", "researcher", "reviewer", "__end__"]:
    last = state["messages"][-1]
    for worker in WORKERS:
        if worker in last.content.lower():
            return worker
    return "__end__"


# ── 构建图 ──
builder = StateGraph(MessagesState)
builder.add_node("supervisor", supervisor)
builder.add_node("writer", writer)
builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", route_after_supervisor)
builder.add_edge("writer", "supervisor")  # worker 完成后回到 supervisor
graph = builder.compile().with_config({"recursion_limit": 10})
```

### 9.6 与子图的区别

| | Supervisor 模式 | 子图模式 |
|---|---|---|
| 决策方式 | LLM 动态决定下一步 | 边/condition 静态或半静态决定 |
| 节点关系 | supervisor 和 worker 都在同一个图里 | 子图是独立的，父图把它当一个节点 |
| state 共享 | 所有节点共享同一份 MessagesState | 子图和父图通过同名字段传递 |
| 适合场景 | 需要 LLM 智能路由的复杂任务 | 可复用的、封装好的流程 |
| 循环控制 | supervisor 决定何时 END | 子图内部有独立的 START/END |

简单记：

- Supervisor = **LLM 负责路由**
- 子图 = **代码负责路由**

## 第10章 LangGraph Platform与前后端集成

### 10.1 LangGraph Platform是什么

LangGraph Platform 是 LangGraph 的部署和运行平台，核心组件：

| 组件 | 作用 |
|------|------|
| **LangGraph Server** | API Server，自动提供 REST API + SSE streaming |
| **LangGraph Studio** | GUI 调试界面，可视化查看 graph 执行流程 |
| **LangGraph CLI** | 命令行工具，`langgraph up` 一行启动 API Server |
| **LangGraph SDK** | 前端 Client 库，封装了与 API Server 的通信 |

关键点：

- LangGraph Server 是**后端 API Server**（默认端口 2024），不是前端库
- 提供 REST API endpoints：`/threads`、`/runs`、`/stream`
- 支持 SSE（Server-Sent Events）流式推送
- 自动处理 interrupt/resume 机制

### 10.2 Resume机制核心原理

**核心问题**：interrupt 暂停 graph 后，如何让前端提供数据并恢复执行？

**LangGraph Platform 的解决方案**：

```text
┌─────────────────────────────────────────────────────────┐
│ 前端                                          │
│  ├─ SSE连接: GET /threads/{thread_id}/runs/{run_id}/stream│
│  │   └─ 接收: LLM流式输出 + interrupt事件               │
│  │                                                       │
│  ├─ HTTP POST: POST /threads/{thread_id}/runs            │
│  │   └─ 发送: command: {resume: data} 恢复执行           │
│  │                                                       │
│  └─ LangGraph SDK Client                                 │
│     client.runs.stream(...); // SSE监听                  │
│     client.runs.create({command: {resume: ...}}); // 恢复 │
└─────────────────────────────────────────────────────────┘
                    ↕ HTTP/SSE
┌─────────────────────────────────────────────────────────┐
│ LangGraph API Server (端口2024)                          │
│  ├─ REST API endpoints                                   │
│  ├─ SSE streaming support                                │
│  └─ Thread/Run management                                │
└─────────────────────────────────────────────────────────┘
                    ↕ 调用Python graph
┌─────────────────────────────────────────────────────────┐
│ Python Backend (你的graph定义)                           │
│  ├─ StateGraph with interrupt()                          │
│  ├─ Checkpointer (保存暂停时的state)                      │
│  └─ graph.compile()                                      │
└─────────────────────────────────────────────────────────┘
```

**关键流程**：

1. **SSE推送interrupt事件**：当 graph 执行到 `interrupt()` 时，LangGraph Server 通过 SSE 推送 interrupt 事件给前端
2. **前端展示UI**：前端收到 interrupt，展示表单/对话框让用户输入数据
3. **HTTP POST resume**：前端通过 `POST /threads/{thread_id}/runs` 发送 `command: {resume: data}`
4. **graph恢复执行**：LangGraph Server 接收 resume 数据，调用 `graph.invoke(Command(resume=data))`
5. **interrupt返回数据**：`interrupt()` 函数返回前端提供的数据，graph 继续执行
6. **SSE继续推送**：后续的 LLM 输出继续通过 SSE 推送

### 10.3 Resume的核心能力

**可以做什么**：

| 场景 | interrupt请求 | resume数据 | 用途 |
|------|--------------|-----------|------|
| **审批决策** | `"是否执行此操作？"` | `{approved: true/false}` | 人工审批工具调用 |
| **数据补充** | `"需要当前viewport"` | `{lat: 30.5, lon: 120.3}` | Agent请求前端状态 |
| **参数调整** | `"请确认渲染参数"` | `{resolution: "high", style: "dark"}` | 用户调整Agent输出 |
| **选择分支** | `"选择哪个数据源？"` | `{source: "database"}` | 人工选择执行路径 |
| **内容编辑** | `"请修改生成的文本"` | `"修改后的文本内容"` | 人工编辑Agent输出 |
| **信息输入** | `"请提供用户ID"` | `"user-123"` | Agent缺少必要信息 |

**核心价值**：

- ✅ Agent主动请求前端数据（而不是前端轮询推送）
- ✅ 按需获取，避免无效请求
- ✅ 支持复杂的表单输入（Pydantic校验）
- ✅ 可循环多次interrupt直到输入合法

### 10.4 前端集成完整示例

**后端：Python graph定义**

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel

class ViewportData(BaseModel):
    """前端需要提供的数据格式"""
    lat: float
    lon: float
    zoom: int

def render_node(state: MessagesState) -> dict:
    """Agent节点：需要前端提供viewport数据"""
    
    # 第1步：interrupt请求前端数据（会暂停graph）
    viewport_raw = interrupt({
        "kind": "request_viewport",
        "question": "需要当前地图的viewport信息",
        "expected_format": ViewportData.model_json_schema()
    })
    
    # 第2步：Pydantic校验前端输入（如果不合法会再次interrupt）
    while True:
        try:
            viewport = ViewportData.model_validate(viewport_raw)
            break  # 校验成功
        except Exception as e:
            # 校验失败，再次interrupt请求重新输入
            viewport_raw = interrupt({
                "kind": "validation_error",
                "error": str(e),
                "expected_format": ViewportData.model_json_schema()
            })
    
    # 第3步：使用前端提供的数据执行渲染
    render_result = f"基于viewport({viewport.lat}, {viewport.lon})渲染完成"
    
    return {
        "messages": [{"role": "ai", "content": render_result}]
    }

# 定义graph
graph = StateGraph(MessagesState)
    .add_node("render", render_node)
    .add_edge(START, "render")
    .add_edge("render", END)
    .compile(checkpointer=MemorySaver())
```

**langgraph.json配置**

```json
{
  "python_version": "3.11",
  "dependencies": ["./requirements.txt"],
  "graphs": {
    "render_agent": "./src/agent.py:graph"
  },
  "env": ".env"
}
```

**启动API Server**

```bash
langgraph up
# API Server启动在 http://127.0.0.1:2024
```

**前端：React完整实现**

```typescript
import { Client } from "@langchain/langgraph-sdk";
import { useState, useEffect } from "react";

function RenderAgentApp() {
  const [client] = useState(() => new Client({ 
    apiUrl: "http://127.0.0.1:2024" 
  }));
  const [threadId, setThreadId] = useState<string | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [interrupted, setInterrupted] = useState(false);
  const [interruptData, setInterruptData] = useState<any>(null);

  useEffect(() => {
    // 创建thread
    client.threads.create().then(thread => {
      setThreadId(thread.thread_id);
    });
  }, [client]);

  const startAgent = async () => {
    if (!threadId) return;

    // 创建run（开始执行）
    const run = await client.runs.create(
      threadId,
      "render_agent",
      { input: { messages: [{ role: "user", content: "渲染地图" }] } }
    );

    // ⭐ SSE监听（LLM输出 + interrupt事件）
    const stream = client.runs.stream(threadId, run.run_id);
    
    for await (const chunk of stream) {
      console.log("SSE chunk:", chunk);
      
      // 检查是否是interrupt
      if (chunk.event === "interrupt" || chunk.data?.__interrupt__) {
        setInterrupted(true);
        setInterruptData(chunk.data?.__interrupt__?.[0] || chunk.data);
        break;  // 暂停，等待用户输入
      }
      
      // 正常LLM输出
      if (chunk.data?.messages) {
        setMessages(prev => [...prev, ...chunk.data.messages]);
      }
    }
  };

  const handleResume = async (viewportData: any) => {
    if (!threadId) return;

    setInterrupted(false);
    setInterruptData(null);

    // ⭐ HTTP POST resume（恢复执行）
    const resumeRun = await client.runs.create(
      threadId,
      "render_agent",
      {
        command: { resume: viewportData }  // ⭐ 关键：发送resume数据
      }
    );

    // ⭐ SSE继续监听后续输出
    const stream = client.runs.stream(threadId, resumeRun.run_id);
    
    for await (const chunk of stream) {
      if (chunk.event === "interrupt") {
        // 可能还有更多interrupt
        setInterrupted(true);
        setInterruptData(chunk.data);
        break;
      }
      
      if (chunk.data?.messages) {
        setMessages(prev => [...prev, ...chunk.data.messages]);
      }
    }
  };

  return (
    <div>
      <button onClick={startAgent}>开始渲染</button>
      
      <div>
        {messages.map(msg => (
          <div key={msg.id}>{msg.content}</div>
        ))}
      </div>
      
      {/* ⭐ Interrupt对话框 */}
      {interrupted && interruptData?.kind === "request_viewport" && (
        <ViewportDialog onSubmit={handleResume} />
      )}
      
      {/* ⭐ 校验失败对话框 */}
      {interrupted && interruptData?.kind === "validation_error" && (
        <ValidationErrorDialog 
          error={interruptData.error}
          expectedFormat={interruptData.expected_format}
          onSubmit={handleResume}
        />
      )}
    </div>
  );
}

// Viewport输入对话框
function ViewportDialog({ onSubmit }) {
  const [lat, setLat] = useState(30.5);
  const [lon, setLon] = useState(120.3);
  const [zoom, setZoom] = useState(10);

  return (
    <div className="modal">
      <h3>Agent需要viewport数据</h3>
      <input value={lat} onChange={e => setLat(parseFloat(e.target.value))} />
      <input value={lon} onChange={e => setLon(parseFloat(e.target.value))} />
      <input value={zoom} onChange={e => setZoom(parseInt(e.target.value))} />
      
      <button onClick={() => onSubmit({ lat, lon, zoom })}>
        提交并继续
      </button>
    </div>
  );
}
```

### 10.5 Resume的进阶用法

**1. 多次interrupt循环**

```python
def approval_node(state):
    """循环审批直到输入合法"""
    
    while True:
        decision_raw = interrupt({
            "question": "请批准以下操作",
            "action": state["action_details"]
        })
        
        try:
            decision = ApprovalDecision.model_validate(decision_raw)
            break
        except:
            # 校验失败，自动再次interrupt
            continue
    
    # 使用合法的decision继续执行
    if decision.approved:
        return Command(goto="execute")
    else:
        return Command(goto="cancel")
```

前端会收到多次interrupt事件，每次都展示UI，直到输入合法。

**2. 并行interrupt处理**

```python
def parallel_requests(state):
    """同时请求多个前端数据"""
    
    # 并行节点各自interrupt
    answer_a = interrupt("question_a")
    answer_b = interrupt("question_b")
    
    return {"results": [f"a:{answer_a}", f"b:{answer_b}"]}
```

前端收到 `__interrupt__: [{id: "...", value: "question_a"}, {id: "...", value: "question_b"}]`

Resume时需要提供map：
```typescript
await client.runs.create(threadId, "agent", {
  command: {
    resume: {
      "interrupt-id-a": "answer for question_a",
      "interrupt-id-b": "answer for question_b"
    }
  }
});
```

**3. Interrupt中携带复杂payload**

```python
def complex_request(state):
    """发送复杂的数据请求"""
    
    data = interrupt({
        "kind": "multi_field_request",
        "fields": {
            "viewport": {"lat": float, "lon": float, "zoom": int},
            "layers": {"roads": bool, "buildings": bool},
            "style": {"color_scheme": str, "opacity": float}
        },
        "context": {
            "reason": "需要这些数据来渲染地图",
            "current_state": state["progress"]
        }
    })
    
    # data包含前端提供的所有字段
    viewport = data["viewport"]
    layers = data["layers"]
    
    return {"render_config": {...}}
```

前端展示复杂表单，收集所有字段后一次性resume。

### 10.6 LangGraph Platform API Endpoints

**核心API**（默认端口2024）：

| Endpoint | Method | 作用 |
|----------|--------|------|
| `/threads` | POST | 创建thread（会话） |
| `/threads/{thread_id}` | GET | 查询thread状态 |
| `/threads/{thread_id}/runs` | POST | 创建run / resume执行 |
| `/threads/{thread_id}/runs/{run_id}/stream` | GET (SSE) | ⭐ 流式监听（LLM输出 + interrupt） |
| `/threads/{thread_id}/runs/{run_id}` | GET | 查询run状态 |
| `/assistants` | GET | 列出所有assistants（graph） |

**Resume的关键**：

- `POST /threads/{thread_id}/runs` 时传递 `command: {resume: data}`
- SSE会推送 interrupt 事件（`event: interrupt`）
- 前端监听SSE，收到interrupt后展示UI，然后POST resume

### 10.7 与第4章interrupt的区别

第4章讲的是**本地Python环境**中的interrupt用法：

```python
# 本地调用
stream = graph.stream_events(input, config)
if stream.interrupted:
    decision = get_user_input(stream.interrupts[0])  # 本地函数
    graph.invoke(Command(resume=decision), config)
```

第10章讲的是**前后端分离**场景：

```typescript
// 前端通过LangGraph Platform
const stream = client.runs.stream(threadId, runId);
if (chunk.event === "interrupt") {
    const decision = await showUIDialog(chunk.data);  // 前端UI
    client.runs.create(threadId, "agent", {
        command: { resume: decision }  // HTTP POST
    });
}
```

**区别**：

| 维度 | 本地调用 | LangGraph Platform |
|------|---------|-------------------|
| **通信方式** | Python函数调用 | HTTP API + SSE |
| **interrupt通知** | `stream.interrupts` | SSE event: `interrupt` |
| **resume数据** | `Command(resume=...)` 参数 | HTTP POST body |
| **前端交互** | Python `input()` | React/Vue UI组件 |
| **适用场景** | 本地测试、CLI工具 | 生产环境、Web应用 |

### 10.8 实际应用场景

**1. 智能地图渲染Agent**

```python
def render_agent(state):
    # Agent分析用户需求
    analysis = llm.invoke(state["messages"])
    
    # ⭐ 请求前端地图状态
    viewport = interrupt({
        "kind": "request_viewport",
        "reason": "需要知道当前地图位置才能智能渲染"
    })
    
    # 根据viewport智能调整渲染策略
    if viewport["zoom"] > 15:
        # 高zoom：渲染详细建筑
        return {"render_command": "render_buildings_detail"}
    else:
        # 低zoom：渲染区域概览
        return {"render_command": "render_region_overview"}
```

前端：Agent主动请求当前地图状态 → 用户确认 → Agent智能渲染

**2. 数据查询审批Agent**

```python
def query_approval_agent(state):
    # Agent生成SQL查询
    sql = llm.invoke(f"生成SQL: {state['user_request']}")
    
    # ⭐ 请求人工审批
    approved = interrupt({
        "kind": "approval",
        "sql": sql,
        "risk_level": "high",
        "question": "此SQL可能修改数据，是否批准执行？"
    })
    
    if approved:
        # 执行SQL
        result = database.execute(sql)
        return {"result": result}
    else:
        return {"messages": ["查询被拒绝"]}
```

前端：Agent生成SQL → 展示审批对话框 → 用户批准/拒绝 → Agent执行或取消

**3. 多轮数据补充Agent**

```python
def data_collection_agent(state):
    collected_data = {}
    
    # ⭐ 多次interrupt收集不同字段
    collected_data["user_id"] = interrupt("请提供用户ID")
    collected_data["time_range"] = interrupt("请提供时间范围")
    collected_data["metrics"] = interrupt("请选择要分析的指标")
    
    # 使用所有数据生成报告
    report = analytics.generate_report(collected_data)
    return {"report": report}
```

前端：Agent逐步请求数据 → 用户分步填写 → Agent最终生成报告

**4. 交互式代码生成Agent**

```python
def code_gen_agent(state):
    # 生成初始代码
    code = llm.invoke(state["requirement"])
    
    # ⭐ 请求用户编辑
    edited_code = interrupt({
        "kind": "code_edit",
        "initial_code": code,
        "instruction": "请检查并修改生成的代码"
    })
    
    # 使用编辑后的代码
    return {"final_code": edited_code}
```

前端：Agent生成代码 → 展示代码编辑器 → 用户修改 → Agent使用修改后的代码

### 10.9 与传统前后端通信的区别

**传统方式**（前端推送所有数据）：

```typescript
// 前端主动推送
await fetch("/api/render", {
  method: "POST",
  body: JSON.stringify({
    viewport: getCurrentViewport(),
    layers: getVisibleLayers(),
    style: getStyleConfig(),
    // 所有数据都推送，不管Agent是否需要
  })
});
```

**LangGraph Platform方式**（Agent主动请求）：

```typescript
// Agent决定何时需要数据
const stream = client.runs.stream(...);

for await (const chunk of stream) {
  if (chunk.event === "interrupt") {
    // ⭐ Agent说"我现在需要viewport"
    const viewport = getCurrentViewport();
    
    await client.runs.create(threadId, "agent", {
      command: { resume: { viewport } }  // 按需提供
    });
  }
}
```

**核心优势**：

| 传统方式 | LangGraph Platform |
|---------|-------------------|
| 前端推送所有数据 | Agent按需请求 |
| 数据可能过期/无效 | 数据实时获取 |
| 前端逻辑复杂 | 前端只响应interrupt |
| 无法处理缺失数据 | Agent自动请求缺失项 |
| 单向数据流 | 双向交互循环 |

### 10.10 快速启动指南

**1. 本地开发**

```bash
# 安装CLI
pip install "langgraph-cli[inmem]"

# 创建项目
langgraph new my-agent --template new-langgraph-project-python

# 编写graph（添加interrupt）
# src/agent.py

# 配置langgraph.json

# 启动API Server
cd my-agent
langgraph up

# API Server启动在 http://127.0.0.1:2024
# Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

**2. 前端集成**

```bash
# 安装SDK
npm install @langchain/langgraph-sdk

# 使用Client
const client = new Client({ apiUrl: "http://127.0.0.1:2024" });

# 监听SSE
const stream = client.runs.stream(threadId, runId);

# 处理interrupt
if (chunk.event === "interrupt") {
  await client.runs.create(threadId, "agent", {
    command: { resume: userInput }
  });
}
```

**3. 生产部署**

```bash
# 部署到LangSmith Cloud
langgraph deploy

# 或自托管（Docker）
langgraph up --docker
```

### 10.11 参考链接

- LangGraph Platform Overview: https://docs.langchain.com/oss/python/langgraph/local-server
- LangGraph JavaScript SDK: https://reference.langchain.com/javascript/langchain-langgraph-sdk
- LangGraph Python SDK: https://docs.langchain.com/langsmith/langgraph-python-sdk
- API Reference: https://docs.langchain.com/langsmith/server-api-ref
- Frontend Integration Example: https://github.com/langchain-ai/langgraph/tree/main/examples/frontend_integration


