
# MapAI Architecture

# 1. Overview

MapAI 是一个 **AI 驱动的 WebGIS 系统**，允许用户通过自然语言操作地图、查询空间数据并进行空间分析。

系统的核心目标：

- 使用 AI 解析用户的空间意图
- 将自然语言转换为 GIS 查询与分析
- 将结果映射为地图操作
- 实现 AI 与地图系统的稳定协作

系统遵循以下设计原则：

1. AI 不直接操作地图
2. AI 不直接生成 SQL
3. 所有 GIS 操作通过 Tools 执行
4. 所有地图操作通过 Command Schema 执行

核心技术：

- NestJS
- LangGraph
- PostGIS
- Web Map (MapLibre / Mapbox)
- WebSocket Streaming

---

# 2. System Architecture

整体系统结构如下：

```

User  
│  
▼  
Web UI  
│  
▼  
Chat Gateway (Nest)  
│  
▼  
Map Agent (LangGraph)  
│  
▼  
Spatial Intent Parser  
│  
▼  
GIS Planner  
│  
▼  
Map Tools  
│  
▼  
GIS Runtime  
│  
▼  
PostGIS  
│  
▼  
Query Result  
│  
▼  
Map Command Generator  
│  
▼  
Map Core  
│  
▼  
Map Rendering

```

系统核心分为 5 个层级：

```

UI Layer  
Application Layer  
AI Layer  
GIS Layer  
Rendering Layer

```

---

# 3. Monorepo Structure

项目采用 Monorepo 结构：

```

apps  
└─ map-ai  
	├─ api  
	├─ web  
	└─ gateway

libs  
├─ map-core  
├─ data-management  
├─ map-agent  
├─ spatial-intent  
├─ map-tools  
└─ gis-runtime

```

说明：

| 模块              | 作用       |
| --------------- | -------- |
| map-ai          | 产品应用入口   |
| map-core        | 地图渲染控制   |
| data-management | 数据管理     |
| map-agent       | AI Agent |
| spatial-intent  | 空间意图解析   |
| map-tools       | GIS工具    |
| gis-runtime     | GIS服务    |

---

# 4. Application Layer

位置：

```

apps/map-ai

```

结构：

```

apps/map-ai  
├─ api  
├─ web  
└─ gateway

```

职责：

### API

NestJS 后端服务：

- 用户接口
- 数据接口
- Agent调用

### Web

前端应用：

- 地图 UI
- AI Chat
- 数据管理界面

### Gateway

实时通信：

- WebSocket
- AI streaming
- Map command push

---

# 5. Map Core

位置：

```

libs/map-core

```

Map Core 负责 **地图渲染控制**。

职责：

- 图层管理
- 地图状态
- 地图操作执行

Map Core 只接受 **Map Command**。

示例：

```

{  
"type": "add-layer",  
"source": "geojson",  
"data": {...}  
}

```

或：

```

{  
"type": "zoom-to-layer",  
"layer": "schools"  
}

```

Map Core 永远不接受 AI 直接控制。

---

# 6. Map Agent

位置：

```

libs/map-agent

```

Map Agent 使用 LangGraph 实现。

职责：

- 接收用户自然语言
- 调用 Spatial Intent Parser
- 生成 GIS 执行计划
- 调用 Map Tools

结构：

```

map-agent  
├─ graph  
│ └─ map-agent-graph.ts  
│  
├─ prompts  
│ └─ spatial-prompts.ts  
│  
├─ tools  
│ └─ tool-bindings.ts  
│  
└─ agent.ts

```

LangGraph 节点：

```

User Input  
│  
▼  
Intent Parser  
│  
▼  
Planner  
│  
▼  
Tool Executor  
│  
▼  
Command Generator

```

---

# 7. Spatial Intent Parser

位置：

```

libs/spatial-intent

```

Spatial Intent Parser 负责：

```

自然语言 → 空间任务

```

示例：

用户输入：

```

找出1公里内的学校

```

解析：

```

{  
"intent": "buffer_query",  
"target_layer": "schools",  
"distance": 1000  
}

```

常见 Intent：

```

query_layer  
filter_features  
nearest_feature  
buffer_query  
spatial_intersects  
within_distance  
overlay_analysis  
density_analysis

```

结构：

```

spatial-intent  
├─ parser  
├─ schemas  
├─ planner  
└─ prompts

```

---

# 8. GIS Planner

GIS Planner 负责：

```

Intent → Tool Plan

```

例如：

Intent：

```

buffer_query

```

Plan：

```

1. run buffer_analysis
    
2. return features
    
3. generate map layer
    

```

输出：

```

ToolExecutionPlan

```

---

# 9. Map Tools

位置：

```

libs/map-tools

```

Map Tools 是 **AI 调用 GIS 的唯一入口**。

职责：

- GIS 查询
- GIS 分析
- GIS 数据处理

结构：

```

map-tools  
├─ query  
├─ analysis  
├─ data  
└─ tools.ts

```

示例工具：

```

query_features  
nearest_feature  
buffer_analysis  
intersect_query  
layer_statistics

```

示例 Tool：

```

tool: buffer_analysis

input:  
{  
"layer": "schools",  
"radius": 1000  
}

```

Tool 内部执行 GIS Runtime。

---

# 10. GIS Runtime

位置：

```

libs/gis-runtime

```

GIS Runtime 是系统的 **GIS 服务层**。

职责：

- PostGIS 查询
- 空间分析
- 数据转换

结构：

```

gis-runtime  
├─ database  
├─ queries  
├─ analysis  
└─ services

```

示例 SQL：

```

SELECT *  
FROM schools  
WHERE ST_DWithin(  
geom,  
ST_Point(:lon,:lat),  
:distance  
);

```

GIS Runtime 不暴露给 AI。

只被 Map Tools 调用。

---

# 11. Data Management

位置：

```

libs/data-management

```

负责数据管理：

功能：

```

数据上传  
格式转换  
数据入库  
图层管理  
metadata管理

```

支持：

```

GeoJSON  
Shapefile  
CSV

```

流程：

```

upload  
↓  
convert  
↓  
store in PostGIS

```

---

# 12. Map Command Schema

Map Command 是 **地图操作协议**。

AI 不直接控制地图。

只能生成 Command。

示例：

```

{  
"type": "add-layer",  
"layer": "query_result",  
"data": {...}  
}

```

或：

```

{  
"type": "highlight-feature",  
"ids": [12,45,77]  
}

```

常见 Command：

```

add-layer  
remove-layer  
highlight-feature  
zoom-to-layer  
zoom-to-extent  
update-style

```

---

# 13. Streaming System

AI 输出通过 Streaming 返回：

```

AI text  
Tool result  
Map commands

```

流程：

```

Agent  
↓  
Streaming Manager  
↓  
WebSocket  
↓  
Frontend

```

Frontend：

```

render chat  
execute map command

```

---

# 14. Execution Flow

完整执行流程：

```

User  
│  
▼  
Chat UI  
│  
▼  
Nest Gateway  
│  
▼  
Map Agent  
│  
▼  
Spatial Intent Parser  
│  
▼  
GIS Planner  
│  
▼  
Map Tools  
│  
▼  
GIS Runtime  
│  
▼  
PostGIS  
│  
▼  
Tool Result  
│  
▼  
Map Command  
│  
▼  
Map Core  
│  
▼  
Map Rendering

```

---

# 15. Future Evolution

未来系统可以升级为：

AI Runtime：

```

AI Runtime  
│  
├─ Router  
├─ AgentHub  
├─ ToolRuntime  
├─ Streaming  
└─ Memory

```

MapAI 将成为 Runtime 的一个模块：

```

AI Runtime  
│  
├─ Map Module  
├─ Chart Module  
└─ Document Module

```

---

# 16. Design Principles

核心原则：

### AI 不直接操作 GIS

所有操作通过 Tools。

### AI 不直接操作地图

所有操作通过 Map Command。

### GIS 与 AI 解耦

GIS Runtime 不依赖 AI。

### 地图渲染独立

Map Core 不依赖 AI。

---

# 17. Key Advantages

架构优势：

- AI 与 GIS 解耦
- GIS 逻辑可控
- 地图操作稳定
- 易扩展 AI Runtime
- 可支持复杂空间推理

---

# 18. Core Innovation

MapAI 的核心创新在于：

```

Spatial Intent Parsing

```

实现：

```

自然语言  
↓  
空间语义  
↓  
GIS分析  
↓  
地图交互

```

这是 AI + GIS 系统的关键能力。