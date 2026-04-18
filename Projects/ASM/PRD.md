**项目名称：** Agentic Spatial Mind (MVP) 
**项目目标：** 实现从自然语言描述到 WebGIS 分析产物的全自动流水线。

### 1. 核心业务流程 (Core Flow)

1. **输入层：** 用户通过 API 提交模糊需求（例如：“帮我分析北京二环内所有地铁站 500 米的覆盖范围”）。
    
2. **理解层：** 智能体解析地理实体（北京、地铁站）、空间关系（二环内）和算子（500 米缓冲区）。
    
3. **执行层：** 系统自动检索空间数据，调用 Python 算子进行计算，并将结果存入对象存储。
    
4. **输出层：** 返回一个唯一标识符（UUID），对应一个动态渲染的 WebGIS 页面。
    

### 2. 功能需求 (Functional Requirements)

- **Intent Parsing (意图解析)：** 基于 LangGraph 实现状态机，支持需求澄清（如果输入太模糊）。
    
- **Automated Tool Dispatching (自动化工具调度)：** 能够根据解析结果自主选择 PostGIS SQL 或 Python GeoPandas 脚本。
    
- **Data Lifecycle Management (数据生命周期)：** 空间数据在 MinIO 的自动上传与过期管理。
    
- **Dynamic Layer Rendering (动态图层渲染)：** 前端 Viewer 根据后端返回的 GeoJSON 元数据自动适配图层样式（颜色、透明度等）。
    

### 3. 验收标准 (Acceptance Criteria)

- 从提交请求到获得 URL 的端到端延迟（计算除外）控制在 5 秒内。
    
- 生成的 URL 必须是 Stateless（无状态）的，支持直接分享并查看分析产物。
    
- 系统需记录 Agent 的“思考路径（Thought Trace）”，便于调试和展示。