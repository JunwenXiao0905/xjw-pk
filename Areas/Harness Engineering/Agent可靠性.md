# Agent 可靠性三件套（Eval + 可观测性 + 成本）— 行业调研

> 调研对象：工业级 LLM/Agent 应用的评估（Eval）、可观测性（Observability）、费用/Token 监控（Cost）三件套怎么做。
> 背景：GeoLens（LangGraph 多智能体）当前有 per-run 摘要 + 硬预算护栏，缺正式 eval 集、trace、成本归集。
> 方法：deep-research（107 子代理、20 源、8 条核心发现全 high 置信、2 条被驳回）。日期：2026-07-03。

## TL;DR（三条主线共识）
1. **Eval 必须从"输出级"升到"轨迹级"**：多步 agent 里正确的最终答案会掩盖"幸运的幻觉"、错工具调用、破碎推理——只评最终输出这些故障全看不见。LLM-as-judge 是轨迹评估的事实默认。
2. **可观测性以 OpenTelemetry 为事实标准**（GenAI semconv 截至 2026-07 仍 Development，但两层 span 分类已定义）；最小闭环 = trace → 抽样 LLM-judge → dashboard → alert。
3. **成本必须实时、按 token+工具单价归集**：$47K 死循环就是靠累计账单告警才暴露。轻量 prompt 级 Budget Tracker 能在 1/10 预算下达成相当准确率、降本 31.3%——佐证硬预算护栏方向正确，但缺实时成本归集就无法在事故前阻断。

## 1. Eval（评估）
- **轨迹级是必需**：结构化 trace（query / 检索 / 工具调用含参+结果 / 组装 prompt / 响应）是任何 eval 的前置——"有 logs ≠ 有 traces"，没 trace 故障可见但原因不可诊断。
- **LLM-as-judge 是默认方法**（人工不可扩展）。它是小型 ML 项目：用 30–50 条人工标注做 ground truth → 迭代 judge prompt → 校准到 **Pearson r > 0.7**。**二元判定（pass/fail）比连续打分更可靠**；多维标准拆成多个单一维度 evaluator；跑多次判断聚合降方差。GPT-4 pairwise judge 与人类一致率 >80%。
- **离线/在线双循环飞轮**：`offline eval → deploy → online monitor → 收集失败案例 → 加入离线集 → 回归 → repeat`。offline eval 是部署任何 agent 前的最小必要步骤，可入 CI/CD 做部署门控。
- **回归集大小**：~50 条（抓大回归）到 ~200 条（对 3–5% 漂移有统计置信），>500 收益递减。

## 2. 可观测性
- **OTel 是事实标准**：推荐 = OTel 库导出 span + 手动注入属性（user_id/session_id/model_version）。
- ⚠️ **GenAI semconv 截至 2026-07 仍 Development（非 Stable）**，几乎每个 `gen_ai.*` 属性带 Development 徽章，schema 仍在 churn——生产依赖要锁版本。
- 已定义**两层 span**：Model/Client 层（Inference/Embeddings/Retrievals/Memory/Execute-tool）+ Agent/Framework 层（Create agent / Invoke agent / Invoke workflow / Plan）。
- **token-usage metric** `gen_ai.client.token.usage` 规定 used 与 billable 同时可得时 **MUST 报告 billable**，为跨厂商成本归集给中性基础。
- **最小闭环四步**：tracing → 抽样 eval（如 10% 会话跑 judge）→ dashboard（幻觉率/延迟/成本）→ alerts。
- **平台选型（关键结论）**：
  - **Langfuse**：开源自托管，单平台同时覆盖 trace + per-span token→成本 + 延迟 + 用户反馈 + 在线 LLM-judge + 离线 eval experiment runner。对中小型自研自托管 agent 最合适。
  - **LangSmith**：专有 SaaS，免费档仅 5k traces/月 + 14 天保留，Plus $39/seat/月，自托管仅 Enterprise。
  - **Arize Phoenix**：本次"ELv2 许可 + 自托管 7 天 + 功能锁 AX"声明被 **0-3 驳回**，未推荐；要考虑需独立复核许可。

## 3. 成本 / Token 监控
- **实时归集**：per-run / per-agent / per-tool 的 token 与成本。统一成本公式 **C_unified = c_token(input/output/cache) + Σ c_i·P_i（每次工具调用单价）**。
- **$47K 教训**：4 个 LangChain agent A2A 循环 11 天，靠累计账单告警才暴露（$50/分钟）。实时监控才能抓"bug 导致的过度 API 循环"。
- **预算感知降本**：标准 ReAct agent 无预算感知，budget=100 饱和、用不上额外预算；轻量 prompt 级 Budget Tracker（无需训练）在 budget=10 即达成相当准确率，**降 40.4% search 调用、21.4% browse、总成本 -31.3%**。

## 4. 三者闭环
Langfuse 单平台可串起来：**生产 trace 的失败案例 → 加入离线 eval 数据集 → 回归集回归 → 触发告警**。社区公认 best-practice 飞轮（实践者多当 aspirational，普遍未达成）。

## 5. 对 GeoLens 现状的定位
现在是 **"事前硬阻断 + 事后审计"** 双层，缺 **"事中可观测 + 持续质量回归"**：

| 已有 | 角色 | 差距 |
|---|---|---|
| `build_run_summary` per-run 摘要 | 事后聚合审计 | 非 span 级 trace，无法定位某次工具调用参数错或 LLM 幻觉；25 次 deque 内存态、不持久、不可查询、无趋势看板 |
| `guardrails` 硬预算护栏 | 事前阻断（方向正确，与 Budget Tracker 论文一致） | 粗粒度——按调用次数计，不按 token+工具单价计 C_unified；无实时成本归集 |
| pytest | 确定性测试 | 无 eval 集、无 LLM-judge、无 CI 门控 |

## 6. 最小可行升级（三方面各一个高 ROI 动作）
1. **Eval 最先落地**：采 30–50 条真实样本（重点生产失败 + 各 agent 典型轨迹）→ 二元 judge prompt（校准 r>0.7）→ 纳 CI gate。
2. **可观测 = 上 Langfuse 自托管**：单平台覆盖 trace（per-LLM / per-tool / per-agent-step span）+ 成本 + 延迟 + 在线 judge。
   - ⚠️ **实现风险**："单个 CallbackHandler 即接通完整 trace" 的声明被 **1-2 驳回**——LangGraph + Langfuse 实际 wiring 不能假设一句 `config={"callbacks":[handler]}` 就够，可能要 `@observe` 装饰器或 OTel exporter。需照 Langfuse LangGraph SDK cookbook 实测验证。
3. **成本 = Langfuse 内配 per-token + per-tool 单价 + spend alert**，并对 Manager→Amap/Coder 路径做模型分层（简单意图走便宜模型）。

## 开放问题（落地要决策）
1. Langfuse + LangGraph 的 wiring 用 `@observe` / CallbackHandler / OTel exporter 哪个？三种对 span 粒度与 token 捕获（尤其国产 LLM）差异？**最该先实测**。
2. 硬护栏要不要升级"软预算告警 + 硬阻断"双层？会改多智能体终止语义。
3. GIS 轨迹级 ground truth 怎么定——评端到端产物还是评每个子 agent 轨迹？是否给每个子 agent 单独建 judge？
4. OTel GenAI semconv 仍 Development，选 OpenInference 还是 OTel GenAI 并锁版本？

## 主要来源
[LangChain 评估框架](https://langchain.com/resources/llm-evaluation-framework) · [EvidentlyAI LLM-as-judge](https://www.evidentlyai.com/llm-guide/llm-as-a-judge) · [Galtea eval guide](https://galtea.ai/blog/llm-evaluation-complete-guide) · [Microsoft AI Agents Production](https://microsoft.github.io/ai-agents-for-beginners/10-ai-agents-production/) · [OTel GenAI semconv](https://opentelemetry.io/docs/specs/semconv/gen-ai/) · [Langfuse LangGraph cookbook](https://langfuse.com/guides/cookbook/example_langgraph_agents) · [Langfuse token & cost tracking](https://langfuse.com/docs/observability/features/token-and-cost-tracking) · [arXiv Budget Tracker](https://arxiv.org/html/2511.17006v1) · [vectara awesome-agent-failures（$47K）](https://github.com/vectara/awesome-agent-failures)
