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
  - [2.4 `START`、`END` 与图内起止点](#24-startend-与图内起止点)
- [第3章 聊天状态与工具调用](#第3章-聊天状态与工具调用)
  - [3.1 `MessagesState`](#31-messagesstate)
  - [3.2 `model.bind_tools()`、`ToolNode`、`tools_condition`](#32-modelbind_tools-toolnode-tools_condition)
  - [3.3 `tools_condition` 与隐式 `END`](#33-tools_condition-与隐式-end)
- [第4章 记忆、暂停与执行](#第4章-记忆暂停与执行)
  - [4.1 `checkpointer`](#41-checkpointer)
  - [4.2 `interrupt()` 与 `Command(resume=...)`](#42-interrupt-与-commandresume)
  - [4.3 `invoke()`、`stream()` 与执行入口](#43-invokestream-与执行入口)
  - [4.4 输出形态](#44-输出形态)
  - [4.5 示例阅读顺序](#45-示例阅读顺序)

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

因为 `tools_condition` 已经通过返回 `__end__` 表达了“结束”。

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
