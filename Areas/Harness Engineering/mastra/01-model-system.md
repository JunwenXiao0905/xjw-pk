# Mastra 模型系统：多厂商支持与模型切换

## 1. 模型字符串格式

Mastra 使用统一的 `"provider/model-name"` 格式来指定模型：

```typescript
// 示例
"openai/gpt-5.5"
"anthropic/claude-sonnet-4-6"
"deepseek/deepseek-v4-flash"
"google/gemini-2.5-pro"
```

在你的项目中，weather-agent 就是用的这种格式：

```typescript
// src/mastra/agents/weather-agent.ts
model: "deepseek/deepseek-v4-flash",
```

## 2. 多厂商支持的核心机制：Provider Registry

Mastra 通过一个**内置的 Provider Registry**（`@mastra/core/dist/provider-registry.json`）来支持多厂商模型。当前版本内置了 **122 个 Provider**。

### 每个 Provider 的数据结构

```json
{
  "apiKeyEnvVar": "OPENAI_API_KEY",   // 从哪个环境变量读取 API Key
  "name": "OpenAI",                    // 显示名称
  "models": ["gpt-5.5", "gpt-4o", ...], // 支持的模型列表
  "docUrl": "https://platform.openai.com/docs/models",
  "gateway": "models.dev",             // 使用的网关
  "npm": "@ai-sdk/openai"             // 底层 AI SDK 包名
}
```

### Provider 与 API Key 环境变量的映射（重要！）

**Mastra 通过 Provider Registry 自动关联模型和环境变量**：当你指定 `model: "deepseek/deepseek-v4-flash"`，Mastra 查到 DeepSeek 的 `apiKeyEnvVar` 是 `DEEPSEEK_API_KEY`，就会自动从 `process.env.DEEPSEEK_API_KEY` 读取密钥。**必须在 `.env` 中设置正确的环境变量名，否则认证失败。**

常用厂商的映射：

| Provider Key | 环境变量 | 备注 |
|---|---|---|
| `openai` | `OPENAI_API_KEY` | |
| `anthropic` | `ANTHROPIC_API_KEY` | |
| `deepseek` | `DEEPSEEK_API_KEY` | |
| `google` | `GOOGLE_API_KEY` 或 `GOOGLE_GENERATIVE_AI_API_KEY` | 两个都支持 |
| `groq` | `GROQ_API_KEY` | |
| `mistral` | `MISTRAL_API_KEY` | |
| `xai` | `XAI_API_KEY` | |
| `alibaba` | `DASHSCOPE_API_KEY` | **例外**：不是 `ALIBABA_API_KEY` |
| `zhipuai` | `ZHIPU_API_KEY` | |
| `openrouter` | `OPENROUTER_API_KEY` | |
| `togetherai` | `TOGETHER_API_KEY` | |
| `siliconflow` | `SILICONFLOW_API_KEY` | |

**完整链路**：

```
model: "deepseek/deepseek-v4-flash"
         ↓
parseModelString() → provider: "deepseek"
         ↓
查 provider-registry.json → apiKeyEnvVar: "DEEPSEEK_API_KEY"
         ↓
process.env["DEEPSEEK_API_KEY"] → 读 .env 中的 Key
         ↓
用 Key 调 DeepSeek API
```

### 查看所有 Provider 和模型

```bash
# 列出所有可用 Provider
node .agents/skills/mastra/scripts/provider-registry.mjs --list

# 列出某 Provider 的所有模型（按版本降序排列）
node .agents/skills/mastra/scripts/provider-registry.mjs --provider openai
node .agents/skills/mastra/scripts/provider-registry.mjs --provider anthropic
node .agents/skills/mastra/scripts/provider-registry.mjs --provider deepseek
```

### 部分已支持的厂商（共122个）

| 厂商 Key     | 名称                | 模型数 |
| ---------- | ----------------- | --- |
| openai     | OpenAI            | 52  |
| anthropic  | Anthropic         | 23  |
| google     | Google            | 21  |
| deepseek   | DeepSeek          | 4   |
| groq       | Groq              | 17  |
| mistral    | Mistral           | 28  |
| xai        | xAI               | 8   |
| alibaba    | Alibaba           | 49  |
| zhipuai    | Zhipu AI          | 12  |
| together   | Together AI       | 18  |
| vercel     | Vercel AI Gateway | 243 |
| openrouter | OpenRouter        | 358 |
| ...        | ...               | ... |

## 3. 模型路由的完整流程

```
用户指定 "deepseek/deepseek-v4-flash"
          │
          ▼
  parseModelString() 解析
   → { provider: "deepseek", modelId: "deepseek-v4-flash" }
          │
          ▼
  getProviderConfig("deepseek") 查注册表
   → { apiKeyEnvVar: "DEEPSEEK_API_KEY", gateway: "models.dev", npm: "@ai-sdk/deepseek", ... }
          │
          ▼
  Gateway.buildUrl() 构建实际 API URL
          │
          ▼
  Gateway.resolveLanguageModel() 返回 AI SDK 的 LanguageModel 实例
          │
          ▼
  Agent 调用该模型进行推理
```

## 4. 三种模型指定方式

### 方式一：模型路由字符串（最常用）

```typescript
new Agent({
  model: "openai/gpt-5.5",          // 自动走 Provider Registry
})

new Agent({
  model: "anthropic/claude-sonnet-4-6",
})
```

只需设置对应的环境变量（如 `OPENAI_API_KEY`、`ANTHROPIC_API_KEY`）即可。

### 方式二：OpenAI 兼容端点

适用于自定义部署（如 vLLM、Ollama、私有化部署）：

```typescript
new Agent({
  model: {
    id: "my-provider/my-model",     // 任意 provider/model 标识
    url: "https://my-endpoint.com/v1",
    apiKey: "sk-xxx",
    headers: { "X-Custom": "value" },
  },
})

// 或者用 providerId/modelId 分开写
new Agent({
  model: {
    providerId: "my-provider",
    modelId: "my-model",
    url: "https://...",
    apiKey: "...",
  },
})
```

### 方式三：直接传入 AI SDK 模型对象

```typescript
import { createOpenAI } from "@ai-sdk/openai";

const openai = createOpenAI({ apiKey: "..." });

new Agent({
  model: openai("gpt-5.5"),  // 直接传 AI SDK 的 LanguageModel
})
```

### 方式四：动态模型（Dynamic Model）

```typescript
// model 可以是函数，根据运行时上下文动态选择
new Agent({
  model: ({ runtime }) => {
    if (runtime.userPlan === "pro") {
      return "openai/gpt-5.5";
    }
    return "openai/gpt-5-mini";
  },
})
```

### 方式五：Model Fallbacks（带重试的模型回退）

```typescript
new Agent({
  model: [
    { model: "openai/gpt-5.5", retries: 2 },
    { model: "anthropic/claude-sonnet-4-6", retries: 1 },
  ],
})
// 先从 gpt-5.5 开始，失败2次后切换到 claude-sonnet-4-6
```

## 5. 如何切换模型

### 静态切换

直接修改 Agent 构造时的 `model` 字段：

```typescript
// 从 DeepSeek 切到 OpenAI
export const weatherAgent = new Agent({
  model: "openai/gpt-5.5",  // 改这一行即可
  // ...
})
```

并在 `.env` 中设置对应的 API Key：

```env
OPENAI_API_KEY=sk-xxx
```

### 运行时切换（Per-Call Override）

Agent 的 `.generate()` 和 `.stream()` 方法都支持传入临时 model：

```typescript
const agent = mastra.getAgentById("weather-agent");

// 本次调用临时用另一个模型
const response = await agent.generate("What's the weather?", {
  model: "anthropic/claude-sonnet-4-6",
});

// 或者 stream 时切换
const stream = await agent.stream("What's the weather?", {
  model: "google/gemini-2.5-pro",
});
```

### 通过请求上下文动态切换

Mastra 支持 **Request Context** 机制，可以根据请求动态注入 model 配置，适合多租户场景。

## 6. Gateway（网关）层

Mastra 用 Gateway 抽象来处理不同部署场景下的模型访问：

| Gateway | 用途 |
|---|---|
| `models.dev` | 默认网关，通过 Mastra 的模型服务路由 |
| `netlify` | Netlify 部署环境 |
| `azure` | Azure OpenAI 服务 |
| `mastra` | Mastra 平台网关 |

Gateway 负责：构建 API URL、获取 API Key、解析为可执行的 LanguageModel。

## 7. 关键文件位置

| 作用 | 路径 |
|---|---|
| Provider Registry JSON | `node_modules/@mastra/core/dist/provider-registry.json` |
| Provider Registry 查询脚本 | `.agents/skills/mastra/scripts/provider-registry.mjs` |
| 类型定义 | `node_modules/@mastra/core/dist/llm/model/shared.types.d.ts` |
| Gateway 实现 | `node_modules/@mastra/core/dist/llm/model/gateways/` |
| 生成的 Provider 类型 | `node_modules/@mastra/core/dist/llm/model/provider-types.generated.d.ts` |

## 8. 总结

Mastra 的多厂商支持是一个**注册表驱动 + 网关抽象**的架构：

1. **统一格式**：所有模型用 `provider/model` 字符串表示
2. **注册表**：122 个 Provider 的元数据（API Key 变量名、模型列表、底层 SDK 包）
3. **网关**：负责连接到实际的模型服务端点
4. **灵活切换**：支持静态配置、运行时覆盖、动态选择、fallback 链四种切换方式
5. **自定义端点**：通过 OpenAI 兼容配置支持私有化部署
