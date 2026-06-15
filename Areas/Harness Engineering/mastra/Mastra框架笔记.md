## 目录

- [[#第1章 总览]]
  - [[#1.1 核心原语]]
  - [[#1.2 Mastra 实例与注册]]
  - [[#1.3 架构与数据流]]
- [[#第2章 模型系统]]
  - [[#2.1 模型字符串格式]]
  - [[#2.2 Provider Registry]]
  - [[#2.3 API Key 环境变量映射]]
  - [[#2.4 模型路由流程]]
  - [[#2.5 模型指定方式]]
  - [[#2.6 Gateway]]
  - [[#2.7 切换模型]]
- [[#第3章 Agent]]
  - [[#3.1 Agent 构造]]
  - [[#3.2 generate 与 stream]]
  - [[#3.3 返回值结构]]
  - [[#3.4 运行时覆盖]]
- [[#第4章 Tools]]
  - [[#4.1 调用链]]
  - [[#4.2 createTool() 结构]]
  - [[#4.3 Zod 作为统一 Schema]]
  - [[#4.4 挂载与 toolName 坑点]]
  - [[#4.5 运行时控制工具选择]]
  - [[#4.6 Tool 与 Workflow Step 的 execute 差异]]
  - [[#4.7 高级选项索引]]
  - [[#4.8 MCP 工具接入]]
- [[#第5章 评估系统 Evals]]
  - [[#5.1 Scorer 四步流水线]]
  - [[#5.2 Scorer 类型与输入形状]]
  - [[#5.3 预置 Scorer]]
  - [[#5.4 自定义 Scorer]]
  - [[#5.5 挂载与采样]]
- [[#第6章 存储与可观测性]]
  - [[#6.1 组合存储 MastraCompositeStore]]
  - [[#6.2 存储领域]]
  - [[#6.3 Logger]]
  - [[#6.4 Observability 链路]]

---

# 第1章 总览

## 1.1 核心原语

Mastra 是 TypeScript AI Agent 框架，核心原语围绕"让 LLM 在结构化流程中调用工具并产出可控输出"。

| 原语            | 职责      | 特征                                                            |
| ------------- | ------- | ------------------------------------------------------------- |
| Agent         | 开放式对话推理 | LLM + instructions + tools + memory + scorers，支持多步工具循环        |
| Workflow      | 结构化多步流程 | `createStep` 链式编排，step 间 schema 强约束，可 suspend/resume          |
| Tool          | 原子能力    | `createTool`，inputSchema/outputSchema 用 Zod，供 Agent 或 Step 调用 |
| Scorer        | 输出质量评估  | 四步流水线打分 0-1，挂载到 Agent 按 sampling 运行                           |
| Memory        | 对话记忆    | thread/resource 维度持久化，支持语义召回                                  |
| Storage       | 持久化层    | 按 domain 拆分，可组合多后端                                            |
| Observability | 链路追踪    | span 化的调用记录，exporter 导出                                       |

## 1.2 Mastra 实例与注册

所有原语在 `src/mastra/index.ts` 注册到一个 `Mastra` 实例。注册是各原语被运行时发现的前提——未注册的 agent/workflow 无法通过 `mastra.getAgent()` / Studio 访问。

```typescript
export const mastra = new Mastra({
  workflows: { weatherWorkflow },
  agents: { weatherAgent },
  scorers: { ... },
  storage: new MastraCompositeStore({ ... }),
  logger: new PinoLogger({ ... }),
  observability: new Observability({ ... }),
});
```

规则（来自 `AGENTS.md`）：所有 agent/tool/workflow/scorer 必须在 `index.ts` 注册；用 `pnpm run dev` / `pnpm run build`，不直接调 `mastra` CLI。

## 1.3 架构与数据流

```
                  ┌─────────────────────────────────────┐
                  │           Mastra 实例 (index.ts)      │
                  │  注册 agents/workflows/tools/scorers  │
                  └───────────────┬─────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▼                         ▼                         ▼
   ┌─────────┐             ┌───────────┐             ┌───────────┐
   │  Agent  │             │ Workflow  │             │  Scorer   │
   │ model + │  then()     │ step 链    │   评估       │ 4 步流水线 │
   │ tools + │ ──────►     │ schema 流转│ ◄──────────  │           │
   │ memory  │             │           │              └───────────┘
   └────┬────┘             └─────┬─────┘
        │                        │
        ▼                        ▼
   ┌─────────────────────────────────────┐
   │            Storage (Composite)        │
   │  LibSQL(default) + DuckDB(observ)    │
   └─────────────────────────────────────┘
        ▲                        ▲
        │                        │
   ┌────┴────┐             ┌─────┴─────┐
   │ Logger  │             │Observability│
   │  Pino   │             │ span+export│
   └─────────┘             └───────────┘
```

关键依赖关系：Agent 与 Workflow 都依赖 Storage 持久化、Observability 记录；Scorer 读取 Agent 的 input/output 进行评估；Tool 被 Agent 与 Workflow Step 调用。

---

# 第2章 模型系统

## 2.1 模型字符串格式

```typescript
model: "provider/model-id"
// "openai/gpt-5.5"
// "anthropic/claude-sonnet-4-6"
// "deepseek/deepseek-v4-flash"
```

provider 与 model-id 由 `/` 分隔。`parseModelString()` 解析此格式得到 `{ provider, modelId }`。

## 2.2 Provider Registry

内置静态注册表 `node_modules/@mastra/core/dist/provider-registry.json`，含 122 个 provider。每条记录字段：

```json
{
  "apiKeyEnvVar": "OPENAI_API_KEY",
  "name": "OpenAI",
  "models": ["gpt-5.5", "gpt-4o"],
  "gateway": "models.dev",
  "npm": "@ai-sdk/openai"
}
```

- `apiKeyEnvVar`：读哪个环境变量取密钥
- `models`：该 provider 支持的模型列表
- `gateway`：走哪个网关解析端点
- `npm`：底层 AI SDK 包名

查询脚本：`node .agents/skills/mastra/scripts/provider-registry.mjs --list` / `--provider openai`。

## 2.3 API Key 环境变量映射

provider 字符串 → registry 查 `apiKeyEnvVar` → 读 `process.env[apiKeyEnvVar]`。环境变量名错则认证失败。

| Provider | 环境变量 |
|---|---|
| openai | `OPENAI_API_KEY` |
| anthropic | `ANTHROPIC_API_KEY` |
| deepseek | `DEEPSEEK_API_KEY` |
| google | `GOOGLE_API_KEY` |
| xai | `XAI_API_KEY` |
| alibaba | `DASHSCOPE_API_KEY`（非 `ALIBABA_API_KEY`） |
| zhipuai | `ZHIPU_API_KEY` |
| openrouter | `OPENROUTER_API_KEY` |
| siliconflow | `SILICONFLOW_API_KEY` |

坑点：`alibaba` 的变量名是 `DASHSCOPE_API_KEY`，不符合 `大写_API_KEY` 的默认规律，单独记忆。

## 2.4 模型路由流程

```
"deepseek/deepseek-v4-flash"
   │ parseModelString()
   ▼
{ provider:"deepseek", modelId:"deepseek-v4-flash" }
   │ getProviderConfig("deepseek")
   ▼
{ apiKeyEnvVar:"DEEPSEEK_API_KEY", gateway:"models.dev", npm:"@ai-sdk/deepseek" }
   │ Gateway.resolveLanguageModel()
   ▼
AI SDK LanguageModel 实例 → 供 Agent 推理
```

## 2.5 模型指定方式

`Agent` 的 `model` 字段（类型 `DynamicArgument<MastraModelConfig>`）接受五种形态：

### 2.5.1 路由字符串

```typescript
model: "openai/gpt-5.5"   // 走 Provider Registry
```

### 2.5.2 OpenAI 兼容配置

私有部署 / vLLM / Ollama：

```typescript
model: { id: "my/model", url: "https://.../v1", apiKey: "..." }
// 或
model: { providerId: "x", modelId: "y", url: "...", apiKey: "..." }
```

### 2.5.3 直接 AI SDK 模型对象

```typescript
import { createOpenAI } from "@ai-sdk/openai";
model: createOpenAI({ apiKey })("gpt-5.5")
```

### 2.5.4 动态模型

`model` 为函数，按运行时上下文返回模型：

```typescript
model: ({ runtime }) => runtime.userPlan === "pro" ? "openai/gpt-5.5" : "openai/gpt-5-mini"
```

### 2.5.5 Fallback 链

带重试的回退，构造时归一化为内部 `ModelFallbacks`：

```typescript
model: [
  { model: "openai/gpt-5.5", retries: 2 },
  { model: "anthropic/claude-sonnet-4-6", retries: 1 },
]
```

## 2.6 Gateway

Gateway 抽象不同部署的端点解析。

| Gateway | 用途 |
|---|---|
| `models.dev` | 默认，经 Mastra 模型服务路由 |
| `netlify` | Netlify 环境 |
| `azure` | Azure OpenAI |
| `mastra` | Mastra 平台 |

Gateway 职责：构建 API URL、取 API Key、解析为 `LanguageModel`。实现位于 `dist/llm/model/gateways/`。

## 2.7 切换模型

### 2.7.1 静态切换

改构造时的 `model` 字段 + 配 `.env` 对应变量。

### 2.7.2 单次调用覆盖

`generate()` / `stream()` 接受 `model` 选项，仅本次生效：

```typescript
await agent.generate("...", { model: "anthropic/claude-sonnet-4-6" });
```

---

# 第3章 Agent

## 3.1 Agent 构造

```typescript
new Agent({
  id: "weather-agent",
  name: "Weather Agent",
  instructions: "...",                    // SystemMessage | string[] | 函数
  model: "deepseek/deepseek-v4-flash",
  tools: { weatherTool },
  memory: new Memory(),
  scorers: { ... },
  maxSteps: 5,
})
```

`instructions` 支持 `DynamicArgument`，可按 `requestContext` 动态生成。`getInstructions()` 解析最终值。

## 3.2 generate 与 stream

### 3.2.1 用法

```typescript
// generate：一次性
const res = await agent.generate("北京天气？");
const text: string = res.text;

// stream：流式
const out = await agent.stream("北京天气？");
for await (const chunk of out.textStream) { process.stdout.write(chunk); }
const full = await out.getFullOutput();   // 等价 generate 返回值
```

### 3.2.2 机制

两者调用同一 agentic loop（`MastraLLMVNext`，`dist/llm/model/model.loop.js`）。区别只在输出封装：

- `generate()` 在 loop 结束后把所有 chunk 物化为 `FullOutput`，字段直接可读。
- `stream()` 返回 `MastraModelOutput`，内部持有一个 `ReadableStream<ChunkType>`。`.textStream` / `.fullStream` 是实时流；`.text` / `.getFullOutput()` 是 `Promise`，在流结束时 resolve。

源码：`dist/agent/agent.d.ts` 第 914 行（generate）、第 957 行（stream）；输出类型 `dist/stream/base/output.d.ts`。

### 3.2.3 选用

| 场景 | 方法 |
|---|---|
| Workflow step（需完整结果传下一步） | generate |
| 聊天 UI / CLI 打字机 | stream + textStream |
| 需实时输出 + 末尾聚合 | stream → getFullOutput |
| 结构化输出 | 两者均支持 `structuredOutput` |

## 3.3 返回值结构

### 3.3.1 FullOutput（generate）

```typescript
{
  text: string,            // 全部 step 文本拼接
  toolCalls: ToolCallChunk[],
  toolResults: ToolResultChunk[],
  usage: LanguageModelUsage,
  totalUsage: LanguageModelUsage,
  finishReason: string,
  steps: LLMStepResult[],  // 每步详情
  object: OUTPUT,          // structuredOutput 结果
  messages: MastraDBMessage[],
  error: Error | undefined,
  runId, traceId, spanId,
}
```

### 3.3.2 MastraModelOutput（stream）

```
textStream       ReadableStream<string>          实时文本
fullStream       ReadableStream<ChunkType>        全部 chunk（含 tool_call 等）
objectStream     ReadableStream<Partial<OUTPUT>>  structuredOutput 增量
elementStream    ReadableStream<T>                数组输出逐元素
text             Promise<string>                  流结束后完整文本
object           Promise<OUTPUT>
toolCalls        Promise<ToolCallChunk[]>
usage            Promise<LanguageModelUsage>
getFullOutput()  Promise<FullOutput>              等价 generate 返回
```

坑点：`MastraModelOutput` 的聚合属性（`.text`、`.toolCalls`）是 Promise，需 await；直接当字符串用会拿到 `[object Promise]`。

## 3.4 运行时覆盖

`generate` / `stream` 的 options（类型 `AgentExecutionOptionsBase`，`dist/agent/agent.types.d.ts`）可在单次调用覆盖 Agent 默认值：

| 选项 | 作用 |
|---|---|
| `model` | 临时换模型 |
| `instructions` / `system` | 临时换提示词 |
| `memory` | 临时记忆配置（thread/resource） |
| `maxSteps` | 最大步数 |
| `toolChoice` | `'auto'` / `'none'` / `'required'` / 指定工具 |
| `activeTools` | 仅启用部分工具 |
| `structuredOutput` | 结构化输出 schema |
| `scorers` | 本次评估器覆盖 |
| `onStepFinish` / `onFinish` / `onChunk` | 生命周期回调 |
| `onIterationComplete` | 每轮迭代后回调，可注入 feedback 控制是否继续 |
| `abortSignal` | 中止 |
| `untilIdle` | 跨后台任务完成的续流 |

---

# 第4章 Tools

## 4.1 调用链

Tool 是 Agent 可调用的外部能力（查 API、读数据库、运行函数、调 MCP）。Agent 决策是否调用，Tool 执行真实代码并返回结构化结果。

```
用户提问
  ↓ Agent 依 instructions + tool.description + inputSchema 判断
模型生成工具参数
  ↓ Mastra 按 inputSchema 校验
execute() 运行
  ↓ 返回 outputSchema 声明的结构
结果回模型 → 自然语言回答
```

## 4.2 createTool() 结构

```typescript
import { createTool } from '@mastra/core/tools';
createTool({
  id: 'get-weather',
  description: 'Get current weather for a location',
  inputSchema: z.object({ location: z.string().describe('City name') }),
  outputSchema: z.object({ temperature: z.number(), /* ... */ }),
  execute: async (inputData) => { return await getWeather(inputData.location); },
});
```

| 字段 | 作用 |
|---|---|
| `id` | 工具唯一标识 |
| `description` | 给模型判断何时使用 |
| `inputSchema` | 入参结构 |
| `outputSchema` | 返回值结构 |
| `execute` | 执行逻辑；入参是经 inputSchema 校验后的数据 |

## 4.3 Zod 作为统一 Schema

Mastra 的所有 schema 边界（Tool/Workflow/Scorer 的 inputSchema/outputSchema、结构化输出、suspend/resume 数据）接受任何 Standard JSON Schema 库（Zod / Valibot / ArkType）。本项目用 Zod。

一个 Zod schema 对象同时承担三件事：

1. 描述结构（`{ location: string }`）
2. 运行时校验（`.parse()` 抛 `ZodError`；`.safeParse()` 返回 `{ success, data | error }`）
3. 类型推导（`z.infer<typeof X>`）

Mastra 在边界上自动用 schema 校验，业务代码一般不手动调 `.parse()`。

### 4.3.1 describe()

字段 `.describe()` 不是注释——它进入 schema 描述，帮模型理解该填什么。`location: z.string().describe('City name')` 让模型知道是城市名而非任意字符串。在 Tool 入参里尤其重要。

### 4.3.2 TypeScript interface vs Zod schema

- TS interface 仅编译期存在，运行时无法校验外部输入
- Zod schema 是运行时对象，Mastra 可读取/转换/校验/暴露给模型与 Studio
- Tool 内部的 TS interface（如 `GeocodingResponse`）服务外部 API 响应的本地类型标注，不参与工具调用协议

## 4.4 挂载与 toolName 坑点

```typescript
new Agent({ /* ... */ tools: { weatherTool } });
```

Agent 判断是否调用工具参考：用户消息、instructions、tool.description、inputSchema、模型是否支持工具调用。

### 4.4.1 toolName vs id（坑点）

流式响应里的 `toolName` 由 tools 对象的 **key** 决定，不一定等于 tool 的 `id`。

- `tools: { weatherTool }` → `toolName: "weatherTool"`（key），但 `id: 'get-weather'`
- 想一致：`tools: { [weatherTool.id]: weatherTool }` → `toolName: "get-weather"`

影响日志、流式 UI、Scorer 的工具名判断。本项目 `toolCallAppropriatenessScorer` 用 `expectedTool: 'weatherTool'` 对应挂载 key，不是 `id`。

## 4.5 运行时控制工具选择

`generate` / `stream` 的 options：

| 选项 | 用途 |
|---|---|
| `toolChoice` | `'auto'` / `'none'` / `'required'` / 指定工具 |
| `activeTools` | 本次仅启用部分已注册工具 |
| `toolsets` | 运行时传入工具集（MCP / 用户级） |
| `clientTools` | 客户端侧工具 |

## 4.6 Tool 与 Workflow Step 的 execute 差异

两者都用 Zod schema，但 execute 签名不同：

```typescript
// Tool
execute: async (inputData) => {}

// Workflow Step
execute: async ({ inputData, mastra, getStepResult, getInitData,
                  suspend, resumeData, state, setState, requestContext }) => {}
```

坑点：不要把 Tool 的 `execute(inputData)` 直接套到 Step 上。Step 的 `execute` 第一个参数是对象，`inputData` 在其中。

## 4.7 高级选项索引

| 选项 | 用途 |
|---|---|
| `strict: true` | 强制按 schema 生成参数（适配器不支持则忽略） |
| `toModelOutput` | 完整结构给应用，压缩/多模态版给模型 |
| `transform` | 对显示流/transcript 的 input/output/error 脱敏或缩减 |
| `requireApproval` | 执行前需显式批准 |
| `requestContextSchema` | 校验请求上下文里的运行时依赖/用户信息 |
| `mcp.annotations` | 暴露为 MCP 工具时的行为提示（只读/破坏性/幂等） |
| `onInputStart` / `onInputDelta` / `onInputAvailable` / `onOutput` | 工具调用生命周期 hook |

主线先掌握 `id` / `description` / `inputSchema` / `outputSchema` / `execute` 与 Agent 的 `tools` 注册，再看高级选项。

## 4.8 MCP 工具接入

`@mastra/mcp` 的 `MCPClient` 连接外部 MCP Server，把远程工具交给 Agent（本项目未安装此包）。

```typescript
const mcp = new MCPClient({
  servers: { weather: { url: new URL('http://localhost:8080/mcp') } },
});

// 静态注册
new Agent({ /* ... */ tools: await mcp.listTools() });

// 动态传入
agent.stream('...', { toolsets: await mcp.listToolsets() });
```

| 方法 | 返回 | 用途 |
|---|---|---|
| `listTools()` | 扁平化工具对象 | 构造时静态注册 |
| `listToolsets()` | 按 toolset 组织的集合 | 每次调用动态传入 |

安全边界：

- `forwardInstructions` 默认关；开启则 MCP Server 的 instructions 进 Agent system prompt，仅对可信服务器启用
- `requireToolApproval` 可对 MCP 工具调用加人工审批
- MCP annotations 只是提示，非安全边界；只有可信服务器的 `readOnlyHint` / `destructiveHint` 才适合降低审批要求

---

# 第5章 评估系统 Evals

## 5.1 Scorer 四步流水线

每个 scorer 内部是一条可组合的 step 链，`MastraScorer.run()` 把它转成 Mastra workflow 执行（`toMastraWorkflow`）。

```
ScorerRun { input, output }
   │ ① preprocess()    提取/转换数据
   ▼
   │ ② analyze()       LLM 分析（可选）
   ▼
   │ ③ generateScore()  输出 0-1 分数
   ▼
   │ ④ generateReason() 输出可读解释
   ▼
{ score: number, reason: string }
```

每步可以是**纯函数**（快、免费）或 **LLM prompt**（带 `outputSchema` + `judge.model`，智能但费 token）。

机制：`.preprocess()` / `.analyze()` 等方法返回**新的 `MastraScorer`**（不可变链式），通过泛型 `TAccumulatedResults` 累积类型，使后续步骤能按类型访问前序结果，如 `results.preprocessStepResult.userText`。源码：`dist/evals/base.d.ts`。

## 5.2 Scorer 类型与输入形状

`type` 字段决定 `run.input` / `run.output` 的形状：

| type | input | output |
|---|---|---|
| `'agent'` | Agent 输入消息 | Agent 输出（text, toolCalls, toolResults） |
| `'trajectory'` | Agent 输入 | Trajectory |
| `{ input: ZodSchema, output: ZodSchema }` | 自定义 | 自定义 |

## 5.3 预置 Scorer

来源 `@mastra/evals/scorers/prebuilt`：

```typescript
// 工具调用准确性
createToolCallAccuracyScorerCode({
  expectedTool: 'weatherTool',
  strictMode: false,   // true → 仅允许调指定工具
})

// 回答完整性（LLM 判断）
createCompletenessScorer()
```

## 5.4 自定义 Scorer

`createScorer()` 来自 `@mastra/core/evals`。完整流水线示例（`src/mastra/scorers/weather-scorer.ts`）：

```typescript
createScorer({
  id: 'translation-quality-scorer',
  type: 'agent',
  judge: { model: 'openai/gpt-5-mini', instructions: '...' },
})
  .preprocess(({ run }) => ({
    userText: getUserMessageFromRunInput(run.input) || '',
    assistantText: getAssistantMessageFromRunOutput(run.output) || '',
  }))
  .analyze({
    outputSchema: z.object({
      nonEnglish: z.boolean(),
      translated: z.boolean(),
      confidence: z.number().min(0).max(1),
    }),
    createPrompt: ({ results }) => `分析 ${results.preprocessStepResult.userText}...`,
  })
  .generateScore(({ results }) => {
    const r = results.analyzeStepResult;
    if (!r.nonEnglish) return 1;
    if (r.translated) return 0.7 + 0.3 * r.confidence;
    return 0;
  })
  .generateReason(({ results, score }) => `...score=${score}`);
```

坑点：`judge.model` 应选与 Agent 不同的模型，避免 Agent 自评自改。

## 5.5 挂载与采样

Agent 构造时挂载，按 `sampling` 决定运行频率（控制 LLM-judge 成本）：

```typescript
new Agent({
  scorers: {
    translation: {
      scorer: translationScorer,
      sampling: { type: "ratio", rate: 1 },   // 100%
    },
  },
})
```

| sampling | 含义 |
|---|---|
| `{ type: "ratio", rate: 0.1 }` | 随机 10% |
| `{ type: "ratio", rate: 1 }` | 每次都跑 |
| `{ type: "fixed", count: 100 }` | 最多 100 次 |

结果写入 Observability（见 6.4）。

---

# 第6章 存储与可观测性

## 6.1 组合存储 MastraCompositeStore

存储按 domain 拆分，`MastraCompositeStore`（`dist/storage/base.d.ts`）组合多后端：

```typescript
storage: new MastraCompositeStore({
  id: 'composite-storage',
  default: new LibSQLStore({ url: "file:./mastra.db" }),
  domains: {
    observability: await new DuckDBStore().getStore('observability'),
  },
}),
```

### 6.1.1 优先级

```
domains 显式指定 > editor 快捷方式 > default 默认
```

### 6.1.2 引擎选型

| 引擎 | 模型 | 适合 |
|---|---|---|
| LibSQL (SQLite) | 行式 OLTP | 日常 CRUD、对话历史 |
| DuckDB | 列式 OLAP | 分析查询、observability |

机制：`getStore(domain)` 返回该领域的存储接口；`init()` 委托父 store 初始化（避免并发 DDL 竞态，issue #16782）。

## 6.2 存储领域

20+ domain，每个可走不同后端：

| 领域 | 内容 |
|---|---|
| `memory` | 对话历史 |
| `workflows` | workflow 状态/快照 |
| `observability` | span、日志、评分 |
| `scores` | scorer 运行结果 |
| `agents` | Agent 配置 |
| `datasets` / `experiments` | 评估数据集/实验 |
| `blobs` | 大文件 |
| `promptBlocks` | Prompt 模板 |
| `backgroundTasks` / `schedules` | 后台/定时任务 |
| `channels` / `notifications` | 消息通道/通知 |

## 6.3 Logger

```typescript
logger: new PinoLogger({ name: 'Mastra', level: 'info' })
```

Pino 输出每行一条 JSON，level：`trace | debug | info | warn | error`。

## 6.4 Observability 链路

```typescript
observability: new Observability({
  configs: {
    default: {
      serviceName: 'mastra',
      exporters: [
        new MastraStorageExporter(),     // 写本地存储
        new MastraPlatformExporter(),    // 发 Mastra 平台（需 MASTRA_PLATFORM_ACCESS_TOKEN）
      ],
      spanOutputProcessors: [
        new SensitiveDataFilter(),       // 脱敏：密码/token/key
      ],
    },
  },
}),
```

### 6.4.1 数据流

```
Agent/Workflow 执行
   │ 生成 span（每步 LLM 调用、工具调用）
   ▼
spanOutputProcessors（脱敏/过滤）
   │
   ├── MastraStorageExporter  → DuckDB/LibSQL（本地）
   └── MastraPlatformExporter → Mastra 平台
   ▼
Studio Tracing 面板查看调用链
```

### 6.4.2 Exporter 与 Processor 职责

- **Exporter**：span 数据发往目标（存储 / 平台 / OTLP / 控制台）
- **SpanOutputProcessor**：发送前变换数据（脱敏、过滤、增强）

`Observability` 类（`@mastra/observability`，`dist/default.d.ts`）管理实例注册表，按 `configSelector` 选运行时实例。

---

## 附：源码索引

| 内容 | 路径 |
|---|---|
| Provider Registry | `@mastra/core/dist/provider-registry.json` |
| 模型配置类型 | `@mastra/core/dist/llm/model/shared.types.d.ts` |
| Gateway 实现 | `@mastra/core/dist/llm/model/gateways/` |
| createTool | `@mastra/core/dist/tools` |
| Agent 类 | `@mastra/core/dist/agent/agent.d.ts` |
| Agent 执行选项 | `@mastra/core/dist/agent/agent.types.d.ts` |
| 输出类型 FullOutput/MastraModelOutput | `@mastra/core/dist/stream/base/output.d.ts` |
| Scorer 基类 | `@mastra/core/dist/evals/base.d.ts` |
| 预置 Scorer | `@mastra/evals/dist/scorers/prebuilt` |
| 存储基类 | `@mastra/core/dist/storage/base.d.ts` |
| Observability 入口 | `@mastra/observability/dist/default.d.ts` |
