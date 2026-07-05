# GeoLens 面试深挖 Q&A

> 基于简历 GeoLens 项目的 5 条 bullet，按面试官追问视角整理。
> 每个回答控制在 30 秒内可讲完（约 100 字），追问可展开。

---

## 一、多智能体编排

### Q1: 为什么用多智能体，不用单 Agent + tool calling？

单 Agent 的 prompt 要同时干两件事——理解用户意图（自然语言）+ 规划空间分析步骤（结构化）——两者 prompt 方向冲突，一个面向人、一个面向系统。拆开后 InteractionAgent 聚焦意图理解，Manager 聚焦任务规划，各自 prompt 更精准。

另外 Reviewer 做质量闭环——单 Agent 自己审自己不靠谱（生成者和审阅者是同一个 LLM，认知盲区重叠）。多智能体让 Reviewer 用独立 prompt + 独立上下文审，能抓到执行者漏的问题。

### Q2: 为什么用 LangGraph，不用 CrewAI / AutoGen？

社区共识是"无聊的确定性工作流胜过自主 agent"。LangGraph 的 StateGraph 是**确定性状态机 + 条件路由**——每一步走哪条边是代码定义的（`add_conditional_edges`），可控可审计。CrewAI/AutoGen 是 agent 之间自由对话协商，行为不可预测，GIS 分析需要"每一步可复现"。

LangGraph 还自带 checkpointing（AsyncSqliteSaver）、interrupt/resume（HITL）、原生 streaming——生产特性齐全，不用自己造轮子。

### Q3: InteractionAgent 和 Manager 为什么分开？

两者面向的对象不同：
- **InteractionAgent** 面向用户——理解自然语言意图、发澄清卡片/追问、生成最终人话回复
- **Manager** 面向系统——拆子任务、按 `task_type` 路由到 subagent、收敛结构化结果

prompt 完全不同：一个教 LLM 怎么跟人沟通，一个教 LLM 怎么调度机器。合在一起会让 LLM 两头都做不好。

### Q4: Reviewer 返工上限怎么防死循环？

`max_reviewer_failures=3`——一个硬计数器（在 `guardrails` dict 里），每次 Reviewer 返回 REVISION 就 +1，超限即 `GuardrailFailure(kind=BUDGET)` 抛异常终止整个 graph run。不是靠 LLM 自觉——是 OS 层强制。

### Q5: 确定性控制流和 LLM 判定怎么分？

原则：**能确定的事绝不让模型决定。**

- 取消 / 确认 / 修订 / 卡片点击 → 用户已显式表达，走确定性分支（结构化 decision 字段）
- 自由文本意图 → LLM 单次分类（InteractionAgent 的 `_understand_user_need`）
- task_type 路由 → Manager 按 `detailed_spec.task_type` 确定性路由到 AmapAgent / CoderAgent

### Q6: 复合任务（buffer→intersect→count）怎么拆的？

InteractionAgent 理解意图后产 `detailed_spec.operations`（多步列表）。Manager 按列表逐个 dispatch：subtask 1 (buffer) → CoderAgent → Reviewer → Manager → subtask 2 (intersect) → CoderAgent → Reviewer → Manager → 全部完成 → Executor 加载所有结果。

子任务间数据传递通过 `_augment_agent_input`：前序 CoderAgent 的 `output_layers` URL 被解析成文件路径，注入下一个子任务的 `input_geojson`。

---

## 二、可靠性设计

### Q1: 硬预算护栏具体是什么？

四个独立计数器，每个有上限：
- `agent_steps` ≤ 30（图节点执行次数）
- `llm_calls` ≤ 20（LLM 调用次数）
- `tool_calls` ≤ 30（工具/AmapAgent 执行次数）
- `map_actions` ≤ 12（加载到地图的动作数）

每次对应操作前 `increment_guardrail_counter` 检查。超限 → `GuardrailFailure(kind=BUDGET)` → graph 终止 → SSE 推 error 事件给前端。

还有超时护栏：每个 agent 有独立 timeout（LLM 120s、CoderAgent 60s、tool 30s），超时即 `GuardrailFailure(kind=TIMEOUT)`。

### Q2: 为什么选 Langfuse 不选 LangSmith？

三个原因：
1. **开源自托管**（Apache-2.0）——数据不出域；LangSmith 自托管仅 Enterprise
2. **一平台三件事**——trace + per-token cost + eval experiment runner
3. 免费档 5k traces/月 + 14 天保留，生产不够用

### Q3: trace 粒度是什么？

三层嵌套：
- **Root span**：一次对话回合
- **Chain span**：每个 agent 节点进出（InteractionAgent / Manager / CoderAgent / Reviewer）
- **Generation span**：每次 LLM 调用（含 model name + token usage + 完整 prompt + response）

### Q4: 接入 LangGraph 怎么做的？

核心一行：`config["callbacks"] = [CallbackHandler()]`。LangGraph 跑在 LangChain 的 callback 体系上，CallbackHandler 自动把图里的 LLM 调用 / 工具调用 / 节点进出变成 Langfuse span。

每请求新建一个 handler（不能复用——#3491 bug：复用会导致并发请求的 span 父子关系错乱）。

### Q5: per-token 成本怎么配的？

Langfuse UI → Models → 新建：
- `matchPattern`: `(?i)^deepseek-v4-flash$`（正则匹配 trace 里的 model name）
- `inputPrice` / `outputPrice`：USD per 1M tokens

配完后新 trace 自动算 cost——per-run / per-trace / per-agent 都能看到。注意只对新 trace 生效，老 trace 不回溯。

### Q6: 18 题 eval 怎么设计的？

覆盖 6 类意图分类边界：
- 数据/能力清单提问（4 题）
- 超范围（3 题）
- 需澄清（2 题）
- 可执行 POI/route（3 题）
- 识别/缓冲路由（2 题）
- 边界用例（2 题）

二元 pass/fail LLM-judge（不给连续分——研究证明二元更可靠，`continuous scale score evaluations do not usually work`）。

回归集 baseline 13/18，分类边界全过。改 prompt 前手动跑一遍防回归。

### Q7: 二元 judge 为什么比连续打分可靠？

LLM 打 73 vs 82 这种连续分漂移大（位置偏差、冗长偏好、分数漂移）；二元（通过/不通过）方差小、可重复。MT-Bench 论文实证 GPT-4 pairwise judge 与人类一致率 >80%，与人人一致率相当。

构建 judge 的校准目标：用 30-50 条人工标注做 ground truth，迭代 judge prompt 到 Pearson r > 0.7。

### Q8: 接入过程踩了什么坑？

**#13023 async 根 span 丢失**：CallbackHandler 在 FastAPI + astream 场景下，根 trace 只在进程退出时才导出。根因是 LangChain 的 `on_chain_end` 被 `run_in_executor(copy_context().run)` 调度到另一个 context，OTel contextvar 丢了。

我的验证方式：写了 smoke test（最小 2 节点 LangGraph + DeepSeek），确认 trace 实时落库。实测我们的最小配置（只注入 CallbackHandler）靠后台批量 flush 是通的。

**#8025 DeepSeek token 降级**：报告说 ChatOpenAI + 自定义 base_url 可能只产 span 不产 generation → token/cost 丢。实测**没命中**——DeepSeek 返回的是 GENERATION 类型，usage 自动捕获。

---

## 三、CoderAgent

### Q1: 为什么不只用预置工具，要代码生成？

GIS 分析需求无限（buffer + intersect + count + clip + overlay + statistics + ...），预置工具永远不够。代码生成让能力边界 = shapely/geopandas/rasterio 能做的一切，不限于固定 N 个工具。

高频已知任务（buffer、POI 搜索）有 materialized 快路径（纯 shapely 计算，不走 LLM）；只有未预制需求才走代码生成。兼顾能力可扩展与成本/稳定。

### Q2: Docker 沙箱怎么加固的？

```
docker run --rm
  --network none           # 断网
  --read-only              # 只读根文件系统
  --user 1001:1001         # 非 root
  --cap-drop ALL           # 丢所有 Linux capabilities
  --security-opt no-new-privileges
  --memory 1g --cpus 1 --pids-limit 64   # 资源限额
  --tmpfs /tmp:rw,size=64m               # 只能写 /tmp 和 /work
  --env PYTHONUNBUFFERED=1 --env PYTHONIOENCODING=utf-8  # env 白名单（不传密钥）
```

调研结论：纯应用层白名单不够——子进程派生后失控（CVE-2026-22708 Cursor 白名单绕过，shell 内建 + env 投毒 → RCE）。OS 层容器强制才是可靠边界。

### Q3: 自修复循环怎么工作？

```
LLM 生成代码 → 写入 main.py → Docker 容器执行 → subprocess 捕获 stdout/stderr/returncode
  ↓
  returncode == 0 → 成功 → 收集 output 文件 → break
  returncode != 0 → 失败 → stderr 原文包进 user message → continue 回循环顶
```

LLM 下一轮看到完整的 Python traceback（FileNotFoundError / KeyError / ...），据此修复代码。上限 10 轮，实际上大部分错误 1-2 轮就修好。

本质和人在终端看报错改代码一模一样——只是 `subprocess.run(capture_output=True)` + `messages.append(stderr)` 自动化了。

### Q4: 为什么 LLM 有时不按 aider editblock 格式输出？怎么处理？

DeepSeek V4 Flash 常吐 markdown code block（````python ... ````）而不是 aider editblock（`<<<<<< main.py ------- ======= >>>>>>`）。

我加了 fallback 解析器 `_extract_raw_code`：先试 ````python ... ```` 正则提取，再试裸 Python 检测（有 `import` + GIS 关键词），提取后直接写入 main.py。和 editblock 路径合并到同一个执行入口。

### Q5: 镜像里装了什么？为什么不装 torch？

CPU GIS 栈：shapely / pyproj / geopandas / rasterio / pyogrio / fiona / numpy。基于 python:3.11-slim + libexpat1（rasterio 运行时依赖）。

不装 torch / geoai——CoderAgent 生成的代码是数据操作（buffer / overlay / 投影），不需要 GPU 推理。GPU 密集任务（建筑提取 / 水体分割）走 target_recognition 子图的独立 GPU venv，不经 CoderAgent。

### Q6: 子任务间的数据怎么传递？

`_augment_agent_input` 在 Manager dispatch 时注入：
- **AmapAgent → CoderAgent**（已有）：POI 搜索结果物化成 GeoJSON → 注入 `input_geojson`
- **CoderAgent → CoderAgent**（新加）：前序 CoderAgent 的 `output_layers[0].url` → `file_path_for_source_url()` 解析成 host 路径 → 注入 `input_geojson`

这样 subtask 2（intersect）拿到 subtask 1（buffer）的输出文件路径。

---

## 四、地图上下文

### Q1: 地图上下文具体是什么？

前端每条消息回传**当前已加载图层列表**（id / name / type / datasetId / visible），注入 InteractionAgent 的 prompt。Agent 据此解析指代——"这些咖啡店" = 已加载的咖啡店 POI（id=amap_poi_6e586c36afee），不用追问。

另外前端也回传视口 bounds，但主要用于目标识别（"识别当前视角的建筑" → 按视口裁剪影像）。

### Q2: MapAction 契约怎么设计的？

前端 Zod + 后端 Pydantic 共同对齐一份 discriminatedUnion（12 类动作）。Executor 只透传不加工——Pydantic 序列化 → SSE → 前端 Zod 校验 → Cesium executor 消费同一 schema 渲染。

12 类：`load_geojson_layer` / `fit_bounds` / `set_layer_visibility` / `show_analysis_summary` / `poi_search_result` / `route_layer` / `request_location` / `mark_location` / `fly_to` / `add_polygon` / `remove_layer` / `measure_distance`

### Q3: discriminatedUnion 是什么？为什么用？

12 种 action 共用一个 `type` 字段做区分。Zod 在运行时自动按 `type` 选对应 schema 校验——不需要手写 if/else 判断。新增类型只需往 union 数组加一个 schema，消费端不改代码。

### Q4: 为什么 SSE 不用 WebSocket？

Agent 事件是**单向推送**（服务端 → 前端），WebSocket 的双向能力用不上。SSE 更简单：HTTP 兼容（nginx 友好）、浏览器自动重连、Content-Type: text/event-stream 即可。WebSocket 需要额外的心跳/重连逻辑。

### Q5: 用户中途断线了怎么办？

LangGraph 的 AsyncSqliteSaver 做 checkpoint 持久化——每个节点执行后状态写入 SQLite。用户断线重连后，前端 `GET /threads/{id}/state` 拉回完整状态（含 map_actions + timeline），Cesium executor 重放所有动作恢复地图。

---

## 五、架构决策追问

### Q1: 为什么 FastAPI 不用 Django/Flask？

LangGraph 的 `astream` 是异步流式——需要原生 async 支持。FastAPI 基于 Starlette 的 async/event loop，天然兼容；Django 的 async 支持是后加的、Flask 是同步框架（需要 gevent 包装）。FastAPI 还自带 Pydantic 数据校验 + OpenAPI 文档生成。

### Q2: 为什么 DeepSeek 不用 OpenAI/GPT？

成本差 10-20 倍：DeepSeek V4 Flash input $0.14 / output $0.28 per 1M tokens；GPT-4o input ~$2.5 / output ~$10。功能上 DeepSeek 的 function calling + 代码生成够用。中国部署合规也是一个因素。

### Q3: 为什么 SQLite checkpointer 不用 Postgres？

单用户个人项目，SQLite 够用（零运维）。如果要 prod 多用户：Postgres（并发写 + HA）。这是"个人项目到生产"的典型迁移点——面试时主动说"这里需要改进"比被指出来好。

### Q4: 如果重做会改什么？

1. `all_results` 一开始就用 list（避免键碰撞 patch）
2. coder prompt 从第一天就注入容器路径 `/data/...`
3. eval 应该接 CI 做自动门控（现在手动跑）
4. 加 inter-subtask data flow 的自动化测试

---

## 六、最大的技术挑战

### Q: 项目中最大的技术挑战是什么？

让复合 GIS 分析（buffer → 求交 → 统计重叠 → 标记 >3 次区域）端到端跑通。表面是一个功能，实际踩了 6 层坑，每层根因不同：

1. **Agent 不认识已载数据** → 加 loaded_datasets 上下文（前端每条消息回传已加载图层列表）
2. **Agent 找不到数据文件** → 加 dataset_id → file_path 解析（inventory lookup）
3. **多个子任务结果互相覆盖** → all_results 键从 `agent_name` 改成 `agent#task_index`
4. **子任务间数据不传递** → _augment_agent_input 加 CoderAgent→CoderAgent 分支
5. **容器内路径不对** → 加 `to_container_data_path` 映射 host→container，prompt 从 `D:\...` 改 `/work` + `/data/...`
6. **前端 Zod 拒绝 bounds:null** → `.optional()` 改 `.nullish()`

只有 6 层全修好，复合分析才端到端跑通。这教会我——多智能体系统的调试是**全链路的**，不是修一个点就够。

---

## 七、竞争与定位

### Q: 这个项目和 Claude Code / CARTO Agentic GIS 有什么区别？

| 维度 | Claude Code | CARTO Agentic GIS | **GeoLens** |
|---|---|---|---|
| 用户 | 开发者 | 数据分析师 | **任何人**（不懂 GIS 和代码） |
| 输入 | 编程指令 | NL + cloud warehouse | NL + **地图上已加载的数据** |
| 输出 | 代码 / 文件 | 查询结果 | **地图上直接可见的可视化** |
| 工具集 | 无限（代码） | 固定 19 个 | **预置 + 代码生成** |
| 闭环 | 写代码→跑→得文件→自己看 | NL→查询→结果 | 需求→数据→**可视化** |

核心差异：GeoLens 不产出文件，产出的是**地图上直接可见的可视化结果**。"需求 → 数据 → 可视化"的完整闭环，零专业门槛。

### Q: 这个项目的价值在哪？

GIS 分析长期被专家工具（ArcGIS / QGIS）垄断——会 ArcPy 的人是瓶颈，不会的人排队等。即使新兴 Agentic GIS（CARTO）也受限于固定工具集。

GeoLens 用 CoderAgent 代码生成突破了固定工具集的天花板——**用户能描述的任意复合空间分析都能即时计算与可视化**。

---

## 八、待改进（主动说，比被指出来好）

1. **LLM 代码生成稳定性 ~60%** — DeepSeek V4 Flash 波动（有时不写 output 文件）；可换 V4 Pro 或加 output 路径检查
2. **中间产物和最终产物都会加载** — 用户说"不需要缓冲区"但系统还是加载了；需加选择性输出过滤
3. **prod Docker-in-Docker 未做** — CoderAgent 目前只在 host→Docker 模式下验证过；prod 需要 docker socket + 命名卷
4. **eval 没接 CI** — 改 prompt 后手动跑，应该自动化做部署门控
5. **trace 粒度不够** — 目前只有 LLM 调用有 input/output dump，Manager 的 task_description / Reviewer 的 verdict 没有结构化记录
