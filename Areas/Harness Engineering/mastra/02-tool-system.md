# Mastra 工具系统：Tool、Zod Schema 与 MCP 集成

## 1. Tool 的作用

Mastra 的 Agent 本身负责理解用户意图、生成回答和决定下一步动作。**Tool 是 Agent 可以调用的外部能力**：查 API、读数据库、运行项目里的函数、调用远程 MCP 工具等。

本项目的天气 Agent 就是典型例子：

```typescript
// src/mastra/agents/weather-agent.ts
tools: { weatherTool },
```

`weatherAgent` 使用模型理解用户是否在问天气；当需要实时天气数据时，模型会选择调用 `weatherTool`。工具执行真实的 Open-Meteo API 请求，然后把结构化结果返回给模型，模型再组织成自然语言回答。

完整链路：

```text
用户提问
  ↓
Agent 根据 instructions + tool description + schema 判断是否需要工具
  ↓
模型生成工具调用参数
  ↓
Mastra 按 inputSchema 校验参数
  ↓
execute() 运行真实代码
  ↓
execute() 返回 outputSchema 声明的结构
  ↓
工具结果回到模型，由模型生成最终回答
```

## 2. 为什么要先理解 Zod

本项目大量使用 `zod`，不是因为 Mastra 只能用 Zod，而是因为 Mastra 的很多接口都需要 **Schema**：

- Tool 的 `inputSchema` / `outputSchema`
- Workflow / Step 的 `inputSchema` / `outputSchema`
- Scorer 分析结果的 `outputSchema`
- 结构化输出、请求上下文、暂停/恢复数据等边界

Zod 是一个 TypeScript-first 的 schema validation library。它把“数据结构定义”和“运行时校验”放在同一个对象里：

```typescript
import { z } from 'zod';

const LocationInput = z.object({
  location: z.string().describe('City name'),
});

const result = LocationInput.parse({ location: 'Beijing' });
```

这里的 `LocationInput` 同时承担三件事：

1. **描述结构**：输入必须是 `{ location: string }`
2. **运行时校验**：`.parse()` 会检查真实数据，不符合会抛出 `ZodError`
3. **类型推导**：`z.infer<typeof LocationInput>` 可以得到 TypeScript 类型

```typescript
type LocationInput = z.infer<typeof LocationInput>;
// 等价于：
// type LocationInput = { location: string }
```

### `parse()` 与 `safeParse()`

`parse()` 用于“无效就直接失败”的场景：

```typescript
LocationInput.parse({ location: 123 }); // 抛出 ZodError
```

`safeParse()` 用于“自己处理成功/失败”的场景：

```typescript
const parsed = LocationInput.safeParse({ location: 123 });

if (!parsed.success) {
  console.log(parsed.error.issues);
}
```

在 Mastra 的 Tool / Workflow API 中，通常不需要手动调用 `.parse()`；你把 Zod schema 交给 Mastra，Mastra 在工具调用、步骤执行、结构化输出等边界上使用这些 schema。

### `describe()` 的意义

Zod 字段上的 `.describe()` 不只是给人看的注释。在工具参数里，它会成为 schema 描述的一部分，帮助模型理解该字段应该填什么。

```typescript
inputSchema: z.object({
  location: z.string().describe('City name'),
}),
```

这比单纯写 `z.string()` 更适合给模型生成工具参数，因为模型能看到 `location` 不是任意字符串，而是城市名。

## 3. Mastra 使用的是 Standard JSON Schema 边界

Mastra 文档说明：`inputSchema` 和 `outputSchema` 可以用任何支持 Standard JSON Schema 的库定义，例如 Zod、Valibot、ArkType。

本项目选择 Zod：

```json
// package.json
"zod": "^4.4.3"
```

所以当前项目里的写法基本都是：

```typescript
import { z } from 'zod';
```

需要记住的边界：

- **TypeScript interface 只在编译期存在**，运行时不能校验外部输入。
- **Zod schema 是运行时对象**，Mastra 可以读取它、转换它、用它校验数据、把它暴露给模型或 Studio。
- 在 Agent / Tool 场景里，schema 既是给代码的类型约束，也是给模型的参数说明。

## 4. `createTool()` 的基本结构

Mastra 自定义工具通过 `createTool()` 定义：

```typescript
import { createTool } from '@mastra/core/tools';
import { z } from 'zod';

export const weatherTool = createTool({
  id: 'get-weather',
  description: 'Get current weather for a location',
  inputSchema: z.object({
    location: z.string().describe('City name'),
  }),
  outputSchema: z.object({
    temperature: z.number(),
    feelsLike: z.number(),
    humidity: z.number(),
    windSpeed: z.number(),
    windGust: z.number(),
    conditions: z.string(),
    location: z.string(),
  }),
  execute: async (inputData) => {
    return await getWeather(inputData.location);
  },
});
```

核心字段：

| 字段 | 作用 |
|---|---|
| `id` | 工具自身的唯一标识 |
| `description` | 给 Agent/模型判断何时使用工具 |
| `inputSchema` | 工具入参结构 |
| `outputSchema` | 工具返回值结构 |
| `execute` | 真正执行工具逻辑的函数 |

`execute` 的第一个参数是经过 `inputSchema` 校验后的输入数据。因此本项目可以直接写：

```typescript
execute: async (inputData) => {
  return await getWeather(inputData.location);
},
```

工具中的 TypeScript `interface` 仍然有用，但它服务的是外部 API 响应的本地类型标注：

```typescript
interface GeocodingResponse {
  results: {
    latitude: number;
    longitude: number;
    name: string;
  }[];
}
```

这里 `GeocodingResponse` 不会参与 Mastra 工具调用协议；它只是帮助 `getWeather()` 处理 Open-Meteo 返回的 JSON。

## 5. Tool 如何挂到 Agent 上

工具定义好之后，需要放进 Agent 的 `tools` 配置：

```typescript
export const weatherAgent = new Agent({
  id: "weather-agent",
  name: "Weather Agent",
  instructions: `...Use the weatherTool to fetch current weather data.`,
  model: "deepseek/deepseek-v4-flash",
  tools: { weatherTool },
});
```

Agent 判断是否调用工具时会参考：

1. 用户消息
2. Agent 的 `instructions`
3. Tool 的 `description`
4. Tool 的 `inputSchema`
5. 当前模型是否支持工具调用

所以工具说明要短而明确。`description` 负责说明“这个工具做什么”，字段 `.describe()` 负责说明“这个参数该填什么”。

## 6. `toolName` 与 `id` 的区别

Mastra 文档里有一个容易踩的点：**流式响应里的 `toolName` 由 `tools` 对象的 key 决定，不一定等于 tool 的 `id`**。

本项目现在是：

```typescript
tools: { weatherTool },
```

因此流式事件里的工具名会是：

```text
weatherTool
```

而工具自身的 `id` 是：

```typescript
id: 'get-weather'
```

如果希望流式事件里的 `toolName` 和 `id` 一致，需要用 `id` 作为对象 key：

```typescript
tools: { [weatherTool.id]: weatherTool },
// toolName: "get-weather"
```

这会影响日志、流式 UI、评估器里对工具调用名称的判断。本项目的评分器使用的是：

```typescript
createToolCallAccuracyScorerCode({
  expectedTool: 'weatherTool',
  strictMode: false,
});
```

这里的 `expectedTool` 对应当前挂载 key `weatherTool`，不是 `id: 'get-weather'`。

## 7. 运行时控制工具选择

Mastra 支持在 `.generate()` 或 `.stream()` 时控制工具使用：

```typescript
await agent.generate('Check the forecast', {
  toolChoice: 'required',
  activeTools: ['weatherTool'],
});
```

常见用途：

| 配置 | 用途 |
|---|---|
| `toolChoice` | 控制模型是否必须、自动或禁止使用工具 |
| `activeTools` | 从已注册工具中限制本次可用的工具列表 |
| `toolsets` | 运行时传入一组工具，常用于 MCP 或用户级工具 |
| `clientTools` | 客户端侧工具 |

本项目目前没有用这些运行时覆盖，工具是在 Agent 构造时静态注册的。

## 8. Workflow 与 Tool 的 schema 写法相同，但 `execute` 参数不同

Workflow Step 也使用 Zod schema：

```typescript
const fetchWeather = createStep({
  id: 'fetch-weather',
  inputSchema: z.object({
    city: z.string().describe('The city to get the weather for'),
  }),
  outputSchema: forecastSchema,
  execute: async ({ inputData }) => {
    // ...
  },
});
```

和 Tool 的区别：

```typescript
// Tool
execute: async (inputData) => {}

// Workflow Step
execute: async ({ inputData, mastra }) => {}
```

Step 的 `execute` 接收的是一个参数对象，里面除了 `inputData`，还可能有：

- `mastra`：访问已注册的 agents/tools/workflows
- `getStepResult`：读取前置步骤结果
- `getInitData`：读取 workflow 初始输入
- `suspend` / `resumeData`：暂停与恢复相关数据
- `state` / `setState`：工作流状态
- `requestContext`：请求上下文

所以不要把 Tool 的 `execute(inputData)` 直接套到 Workflow Step 上。

## 9. Zod schema 在本项目里的复用点

### Tool 输入输出

```typescript
inputSchema: z.object({
  location: z.string().describe('City name'),
}),
outputSchema: z.object({
  temperature: z.number(),
  feelsLike: z.number(),
  humidity: z.number(),
  windSpeed: z.number(),
  windGust: z.number(),
  conditions: z.string(),
  location: z.string(),
}),
```

### Workflow 数据流

```typescript
const forecastSchema = z.object({
  date: z.string(),
  maxTemp: z.number(),
  minTemp: z.number(),
  precipitationChance: z.number(),
  condition: z.string(),
  location: z.string(),
});
```

`forecastSchema` 同时作为 `fetchWeather` 的输出和 `planActivities` 的输入：

```typescript
outputSchema: forecastSchema,
inputSchema: forecastSchema,
```

这表示两个 Step 之间的数据契约是同一个结构。

### Scorer 结构化分析结果

```typescript
outputSchema: z.object({
  nonEnglish: z.boolean(),
  translated: z.boolean(),
  confidence: z.number().min(0).max(1).default(1),
  explanation: z.string().default(''),
}),
```

这里的 Zod schema 约束 LLM 评估步骤的结构化输出。`min(0).max(1)` 限制置信度范围，`default(1)` / `default('')` 提供默认值。

## 10. Tool 的高级选项索引

这些不是本项目当前天气工具的主线，但读文档时会经常看到：

| 选项 | 用途 |
|---|---|
| `strict: true` | 请求支持的模型适配器严格按工具 schema 生成参数；不支持的适配器会忽略 |
| `toModelOutput` | 工具返回完整结构给应用，但只把压缩/多模态版本发给模型 |
| `transform` | 对显示流或 transcript 中的 input/output/error 做脱敏或缩减 |
| `requireApproval` | 工具执行前要求显式批准 |
| `requestContextSchema` | 校验请求上下文里的运行时依赖或用户信息 |
| `mcp.annotations` | 暴露为 MCP 工具时提供只读、破坏性、幂等等行为提示 |
| `onInputStart` / `onInputDelta` / `onInputAvailable` / `onOutput` | 工具调用生命周期 hook |

优先级建议：先掌握 `id`、`description`、`inputSchema`、`outputSchema`、`execute`、Agent 的 `tools` 注册，再看这些高级选项。

## 11. MCP 工具接入

Mastra 可以通过 `MCPClient` 连接外部 MCP Server，并把远程工具交给 Agent 使用。

当前项目的 `package.json` 还没有安装 `@mastra/mcp`。下面是 Mastra 当前嵌入式文档中的 API 形状；真正实践 MCP 时，需要先把对应包加入依赖。

静态注册方式：

```typescript
import { MCPClient } from '@mastra/mcp';
import { Agent } from '@mastra/core/agent';

const mcp = new MCPClient({
  servers: {
    weather: {
      url: new URL('http://localhost:8080/mcp'),
    },
  },
});

const agent = new Agent({
  id: 'multi-tool-agent',
  name: 'Multi-tool Agent',
  instructions: 'You have access to multiple tool servers.',
  model: 'openai/gpt-5.5',
  tools: await mcp.listTools(),
});
```

动态传入方式：

```typescript
const response = await agent.stream('How is AAPL doing?', {
  toolsets: await mcp.listToolsets(),
});
```

区别：

| 方法 | 返回形状 | 典型用途 |
|---|---|---|
| `listTools()` | 扁平化后的工具对象 | Agent 构造时静态注册 |
| `listToolsets()` | 按 toolset 组织的工具集合 | 每次 `generate()` / `stream()` 动态传入 |

MCP 工具需要特别注意安全边界：

- `forwardInstructions` 默认关闭；打开后，MCP Server 的 instructions 会进入 Agent system prompt，只应该对可信服务器启用。
- `requireToolApproval` 可对 MCP Server 的工具调用加人工审批。
- MCP annotations 只是提示，不是安全边界；只有可信服务器的 `readOnlyHint` / `destructiveHint` 等才适合用来降低审批要求。

## 12. 本项目天气工具的关键判断

`weatherTool` 是一个读外部 API 的工具：

- 有副作用吗：没有写入动作，主要是读取 Open-Meteo。
- 是否需要审批：当前不需要。
- 是否需要 `strict: true`：当前输入只有 `location: string`，可暂不加。
- 是否需要 `toModelOutput`：当前返回结构已经足够小，暂不需要。
- 是否需要 `transform`：当前没有敏感字段，暂不需要。
- 是否适合 MCP：可以改造成 MCP 工具，但本项目当前只是本地代码工具。

最重要的稳定契约是：

```typescript
inputSchema: { location: string }
outputSchema: {
  temperature: number
  feelsLike: number
  humidity: number
  windSpeed: number
  windGust: number
  conditions: string
  location: string
}
```

只要这个契约稳定，Agent 的 instructions、Scorer、Studio 展示和后续 Workflow 编排都可以围绕它工作。

## 13. 总结

Mastra 工具系统可以理解为“模型决策 + 结构化函数调用”的机制：

1. **Tool 定义能力边界**：`description` 说明何时用，`execute` 执行真实代码。
2. **Zod 定义数据契约**：`inputSchema` 约束模型传入的参数，`outputSchema` 声明工具返回的结构。
3. **Agent 注册工具**：`tools: { weatherTool }` 让模型能看到并调用工具。
4. **工具名要看对象 key**：当前流式 `toolName` 是 `weatherTool`，不是 `get-weather`。
5. **Workflow / Scorer 也复用 schema 思路**：Zod 是本项目跨 Agent、Tool、Workflow、Scorer 的统一结构描述方式。
6. **MCP 是外部工具接入层**：`MCPClient` 可以把远程 MCP Server 的工具接进 Agent，但要额外关注 instructions 注入和工具审批。
