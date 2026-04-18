**架构原则：** TS 做调度控制流（State Machine），Python 做数据处理流（Data Pipeline）。

### 1. 技术栈拓扑 (Technology Topology)

- **Workspace:** Nx (Monorepo)
    
- **Backend:** NestJS (Framework) + LangGraph.js (Agent Orchestrator)
    
- **Data Layer:** Prisma (ORM) + PostGIS (Spatial DB) + Redis (Task Queue/Cache)
    
- **Storage:** MinIO (GeoJSON/Vector Tiles)
    
- **Analysis Engine:** Python 3.1x + GeoPandas + Shapely (Standalone Scripts)
    
- **Frontend:** React + MapLibre GL JS
    

### 2. 核心状态机设计 (LangGraph State)

定义 `AgentState` 对象，在节点间传递：


```
interface AgentState {
  originalPrompt: string;
  plan: string[];        // 拆解的步骤
  dataRefs: string[];    // 引用的中间文件路径
  currentStep: number;
  resultId?: string;     // 最终关联的数据库 ID
  error?: string;
}
```

- **Node A (Planner):** 调用 LLM 生成执行计划。
    
- **Node B (Executor):** 调度 NestJS Service 执行工具（如通过 `spawn` 运行 Python）。
    
- **Node C (Storer):** 将产物落库并上传 MinIO。
    

### 3. 系统组件通信 (Component Communication)

1. **NestJS -> Python:** 采用 `child_process.spawn` 或 `FastAPI` 微服务。初期建议使用脚本调用方式，通过 `stdin/stdout` 传递 JSON 配置，减少运维复杂度。
    
2. **GIS Script -> MinIO:** Python 脚本计算完成后直接将生成的 `result.geojson` 写入 MinIO，并将 `object_key` 返回给 NestJS。
    
3. **Frontend -> Backend:** 前端通过 `GET /results/:id` 获取 metadata，包含 MinIO 的预签名 URL（Presigned URL），直接拉取数据。
    

### 4. 数据库 Schema (Prisma)

代码段

```
model SpatialAnalysis {
  id             String   @id @default(uuid())
  prompt         String
  status         String   // PENDING, PROCESSING, COMPLETED, FAILED
  resultUrl      String?  // MinIO Key
  extent         Json?    // 空间范围 BBOX，用于前端自动定位
  agentTrace     Json?    // 存储思考过程
  createdAt      DateTime @default(now())
}
```

### 5. 扩展性设计 (Scalability)

- **计算解耦：** 未来可将 Python 脚本封装为容器，由 Redis 队列（BullMQ）进行异步调度，避免长耗时任务阻塞 NestJS 主进程。
    
- **数据预热：** 常用空间数据集（如城市行政边界）预先缓存在 PostGIS 中。