# Zod 知识笔记

## 1. 概述

Zod 是一个 TypeScript-first schema 声明与验证库。核心思想：用代码定义数据结构，自动推导 TypeScript 类型，同时提供运行时校验拦截非法数据。

> GitHub: https://github.com/colinhacks/zod
>
> Stars: 42.9k

**TypeScript-first**：Zod 的设计优先级是"先有 TS 类型"，而不是"先有 JS 验证"。传统验证库（如 Joi）在 JS 里写校验规则，类型需要额外维护接口。Zod 反过来——写 schema，TS 类型自动从 schema 推导（`z.infer`），不用再写一遍 `interface`。schema 改则类型自动跟着改，不会不一致。

**Schema**：意思是"数据结构的定义/蓝图"。来自数据库和 JSON Schema 标准。

一个 Zod schema 同时干三件事：
① 文档——一眼看出数据长什么样；
② 运行时校验——`.parse()` 检查真实数据是否符合描述；
③ 类型推导——`z.infer` 把它变成 TS 类型。


**最小案例：**

```ts
import { z } from 'zod';

// 定义 schema — 同时是类型源头和运行时校验器
const UserSchema = z.object({
  name: z.string().min(2).max(20),
  age: z.number().int().positive(),
  email: z.email(),
});

// 推导 TypeScript 类型（编译时）
type User = z.infer<typeof UserSchema>;
//    ^? { name: string; age: number; email: string }

// 运行时校验 — 拦截非法数据
const result = UserSchema.safeParse({ name: 'A', age: -1, email: 'bad' });
//    ^? { success: false, error: ZodError }
// result.error.issues → [
//   { path: ['name'], message: 'Invalid input: expected string, received number' }
//   ...
// ]
```

作用：**一份定义同时解决两个问题**——编译期 TypeScript 类型安全 + 运行时数据校验（API 入参、表单、配置文件等场景）。

### 生态地位

Zod 的生态辐射极广，几乎覆盖了整个 TypeScript 后端和全栈领域。npm 上 **96,903 个包直接依赖它**，周下载量约 **9.74 亿**。

| 类别 | 项目 | 关系 |
|------|------|------|
| **后端框架** | **Express / Fastify / Hono** | 用 Zod 校验 API 请求参数（body / query / params） |
| **AI Agent** | **Vercel AI SDK** | tool schema 和结构化输出的标准定义方式 |
| | **Mastra** | tool/workflow/scorer 全部依赖 Zod |
| | **LangChain.js** | 结构化输出使用 Zod schema |
| **ORM** | **Prisma** | 社区标准实践：Prisma 定义数据库模型 → Zod 做 API 层运行时校验 |
| **前端** | **Next.js / Remix** | Server Action 的参数校验，T3 Stack 的核心组件 |
| | **React Hook Form** | 官方提供 `@hookform/resolvers/zod`，直接用 Zod schema 做表单验证 |

一句话总结：Zod 已经超出了"一个库"的范畴，变成了 **TypeScript 生态中 schema 定义的通用语言**——就像 JSON 是数据交换的通用格式一样，Zod 是 TS 世界描述"数据长什么样"的标准方式。

---

## 2. 设计理念

### TypeScript-first，schema 即类型源头

传统做法是分别写接口定义和验证逻辑，容易不一致。Zod 反过来：schema 是唯一事实源，`z.infer` 从 schema 推导出 TS 类型，杜绝双重维护。

### 链式、不可变、追加校验

Zod 的方法都不修改原实例，而是返回一个新实例。这就是"不可变"（immutable）。

因为每次都返回同类型的新实例，所以可以把调用串起来写——这就是"链式调用"（chain calling）。

每次调用（`.min()` `.max()` `.email()` 等）都在内部往 `checks` 数组追加一条校验规则。

```ts
const n1 = z.string();
// n1 → ZodString { _def: { type: 'string' } }

const n2 = n1.min(2);
// n2 → ZodString { _def: { type: 'string', checks: [ $ZodCheckMinLength {} ] } }

n1 === n2  // false — n1 没变，n2 是全新实例
```

`n1` 依然是 `{ type: 'string' }`，没被修改过。`n2` 多了一个 `checks` 数组。这就是"追加校验"的含义——返回新对象，新对象的 `checks` 比原对象多一条。链式调用只是把 `n1.min(2).max(20)` 写成一行而已。

---

## 3. 源码架构（v4）

```
src/v4/
├── core/          # zod/v4/core — 核心层
│   ├── core.ts    # $ZodType 基类，定义 schema 最小接口
│   ├── schemas.ts # 所有 schema 类型（ZodString / ZodNumber / ZodObject ...）
│   ├── parse.ts   # 解析引擎：深度优先遍历 schema 树，执行校验
│   ├── checks.ts  # 内置校验规则（min / max / email / regex / int ...）
│   ├── errors.ts  # ZodError / ZodIssue 错误系统
│   └── ...
├── classic/       # 用户日常使用的 API 层
│   └── schemas.ts # 在 core 之上包装链式 API（z.string().min() 等语法糖）
├── mini/          # zod/v4/mini — 可摇树优化的轻量版
└── locales/       # 国际化错误消息
```

**分层关系：**

```
core/$ZodType （最小接口：_parse / safeParse / 类型定义）
        ↑
classic/ZodType （加链式 API：.min() .max() .email() .default() ...）
        ↑
用户代码：z.object({ name: z.string().min(2) })
```

---

## 4. 运行时机制

要理解 Zod 在运行时做了什么，先要知道定义 schema 时创建了什么，然后看调用 `.parse()` 时怎么用它。

### 4.1 定义 schema 时：创建了一棵树

每个 `z.xxx()` 调用都创建一个类实例（`ZodString`、`ZodObject`、`ZodNumber`...），这些实例通过 `_def` 属性记住自己的"配置"。

```ts
const strSchema = z.string();
// strSchema 是 ZodString 实例，_def 存了 { type: 'string' }

const objSchema = z.object({
  name: z.string(),
  age: z.number().int(),
});
// objSchema 是 ZodObject 实例
// _def.shape 存了 { name: ZodString, age: ZodNumber }
```

所以 `z.object({ name: z.string(), age: z.number() })` 实际上创建了一棵对象树：

```
ZodObject
  ├── shape.name  → ZodString   { type: 'string' }
  └── shape.age   → ZodNumber   { type: 'number', checks: [...] }
```

### 4.2 `_def`：实例的"配置单"

每个 schema 实例的 `_def` 存了它的全部配置。它是 Zod 内部用 `Object.defineProperty` 在构造时挂载的（`src/v4/classic/schemas.ts:228`）。

| 字段 | 存在位置 | 含义 |
|------|----------|------|
| `type` | 所有 schema | 数据类型名，如 `'string'` `'number'` `'object'` |
| `checks` | ZodString / ZodNumber 等 | 校验规则数组，每条是一个 check 对象 |
| `shape` | ZodObject | 子 schema 的映射表 |
| `format` | ZodNumber | 数字格式约束，如 `'safeint'` |

```ts
z.string().min(2).max(20)._def
// → { type: 'string', checks: [ $ZodCheckMinLength {}, $ZodCheckMaxLength {} ] }

z.number().int().positive()._def
// → { type: 'number', checks: [ ZodNumberFormat { format: 'safeint' }, $ZodCheckGreaterThan {} ] }

z.object({ name: z.string() })._def
// → { type: 'object', shape: { name: ZodString } }
```

### 4.3 checks 数组：校验规则的积累

每次链式调用 `.min()` `.max()` `.email()` `.int()` `.positive()`，Zod 都往 `checks` 数组**追加**一个 check 对象。

```ts
z.string()              // checks: []               — 无校验
  .min(2)               // checks: [ $ZodCheckMinLength ]  — 一条规则
  .max(20)              // checks: [ $ZodCheckMinLength, $ZodCheckMaxLength ]  — 两条
  .email()              // checks: [...前两条, ZodEmail ]  — 三条
```

`_def.checks.length` = 你链式调用了几个校验方法。

### 4.4 `.parse()` 执行时：深度优先遍历 + 收集所有错误

当调用 `schema.parse(data)`，Zod 从根节点开始深度优先遍历这棵 schema 树。对于每个节点：

```ts
schema.parse(data)
// 1. 根节点（ZodObject）：遍历 shape 的每个 key
//     ↓
// 2. name 节点（ZodString）：遍历 checks 数组
//       逐个执行：min(2) 通过？max(20) 通过？...
//       不通过 → 记下 ZodIssue { path: ['name'], ... }
//     ↓
// 3. age 节点（ZodNumber）：遍历 checks 数组
//       逐个执行：int 通过？positive 通过？...
//       不通过 → 记下 ZodIssue { path: ['age'], ... }
//     ↓
// 4. 所有节点检查完毕
//      有错误 → throw ZodError（issues 数组包含所有问题）
//      无错误 → 返回传入的数据
```

关键：**不短路**。即使 name 已经错了，age 仍然会检查，最后把所有错误一起返回。这让用户能一次看到全部问题，而不是修一个错再报下一个。

`safeParse` 和 `parse` 逻辑完全一样，区别只是：

```
.parse(data)    → 校验通过返回数据，不通过 throw ZodError
.safeParse(data) → 通过返回 { success: true, data }，不通过返回 { success: false, error: ZodError }
```

### 4.5 Schema 即配置：定义时不验证，使用时才验证

定义 schema 时只是创建了一个 ZodObject 实例，**不会触发任何验证**。验证是在调用 `.parse()` 或 `.safeParse()` 时才发生。

```ts
// ① 模块加载时：创建 schema 实例（不验证）
const weatherTool = createTool({
  inputSchema: z.object({ location: z.string() }),
  // ...
});

// ② 用户调用 tool 时：Mastra 内部做验证
// Mastra 源码大致是这样：
async function executeTool(tool, userInput) {
  const validated = tool.inputSchema.parse(userInput);  // ← 这里才真正验证
  return tool.execute(validated);
}
```

**类比：** 就像在餐厅门口贴了一张"衣冠不整禁止入内"的告示（定义 schema），但告示本身不会拦人。等顾客来了（用户调用 tool），保安才会检查（`inputSchema.parse()`）。

**为什么要这样设计？** 因为 schema 需要被多处使用：
- 传给 LLM，告诉它 tool 需要什么参数（JSON Schema）
- 运行时校验用户输入
- TypeScript 类型推导

如果验证在定义时就发生，这些用途都没法实现。

**直接使用 Zod vs 框架使用：**

| 场景 | 谁触发验证 |
|------|-----------|
| 直接用 Zod | 你写 `schema.parse()` |
| Mastra tool | Mastra 内部调用 `inputSchema.parse()` |
| Vercel AI SDK | 框架内部调用 `inputSchema.parse()` |
| React Hook Form | 框架内部调用 `schema.parse()` |

直接用 Zod 时需要自己写验证逻辑：

```ts
// API 路由 — 你自己写验证
app.post('/user', (req, res) => {
  const result = UserSchema.safeParse(req.body);  // ← 手动触发
  if (!result.success) {
    return res.status(400).json(result.error.issues);
  }
  db.user.create({ data: result.data });
});

// 表单提交 — 你自己写验证
function handleSubmit(formData: FormData) {
  const data = Object.fromEntries(formData);
  const result = FormSchema.safeParse(data);  // ← 手动触发
  if (!result.success) {
    showErrors(result.error.issues);
    return;
  }
  submit(result.data);
}
```

框架只是把 `schema.parse(data)` 藏在了内部，让你不用手写。本质是一样的。

---

## 5. 基本用法

### 定义 schema

```ts
z.string()
z.number()
z.bigint()
z.boolean()
z.date()
z.nan()
z.undefined()
z.null()
z.void()
z.never()
z.unknown()
z.any()
```

### 对象与组合

```ts
z.object({ name: z.string(), age: z.number() })
z.array(z.string())
z.tuple([z.string(), z.number()])
z.union([z.string(), z.number()])
z.discriminatedUnion('kind', [...])
z.enum(['a', 'b', 'c'])
z.literal('hello')
z.record(z.number())
```

### 链式校验

```ts
// 字符串
z.string().min(2).max(100).email().url().uuid()
  .toLowerCase().trim()

// 数字
z.number().int().positive().min(0).max(100).finite()

// 可选 / 可空 / 默认
z.string().optional()
z.string().nullable()
z.string().nullish()
z.string().default('default')
```

### 自定义校验：.refine() / .check()

内置校验方法（`.min()` `.email()` 等）覆盖不了的场景，用 `.refine()` 写自定义逻辑。

```ts
// .refine() — 返回 true/false
const passwordSchema = z.string()
  .refine(val => val.length >= 8, '密码至少 8 位')
  .refine(val => /[A-Z]/.test(val), '密码必须包含大写字母')
  .refine(val => /[0-9]/.test(val), '密码必须包含数字');

// .check() — 更灵活，可以修改错误路径
const userSchema = z.object({
  password: z.string(),
  confirmPassword: z.string(),
}).check(ctx => {
  if (ctx.value.password !== ctx.value.confirmPassword) {
    ctx.issues.push({
      code: 'custom',
      path: ['confirmPassword'],
      message: '两次密码不一致',
    });
  }
});
```

`.refine()` 适合单字段校验，`.check()` 适合跨字段校验（如"密码和确认密码必须相同"）。

### 验证 + 转换：.transform()

`.transform()` 在验证通过后对数据做转换，**输出类型会改变**。

```ts
// 字符串 → 数字
const numSchema = z.string()
  .transform(val => parseInt(val, 10));
// z.infer<typeof numSchema> → number（输入是 string，输出是 number）

// 字符串 → Date
const dateSchema = z.string()
  .refine(val => !isNaN(Date.parse(val)), '无效日期')
  .transform(val => new Date(val));
// z.infer<typeof dateSchema> → Date

// 链式：先 trim 再转小写
const emailSchema = z.string()
  .transform(val => val.trim().toLowerCase())
  .pipe(z.string().email());
```

**`.refine()` vs `.transform()` 的区别：**

| 方法 | 作用 | 输出类型 |
|------|------|----------|
| `.refine()` | 校验，不改变数据 | 不变 |
| `.transform()` | 校验 + 转换 | 改变 |

### 解析

```ts
// 抛错模式
schema.parse(data)

// 安全模式（推荐）
const r = schema.safeParse(data);
if (!r.success) {
  r.error.issues  // 错误列表
} else {
  r.data          // 类型安全的数据
}
```

### 类型推导

`z.infer` 是 TypeScript 的类型语法，不是函数调用。`<>` 里传的是类型参数而非值参数，整个表达式在编译后完全消失，不产生任何 JavaScript 代码。

```ts
type T = z.infer<typeof schema>;
//       ^^^^^^^^  ^^^^^^^^^^^^^
//       类型名     泛型参数（typeof 从变量提取类型）
```

`z` 本身是通过 `import { z } from 'zod'` 导入的一个对象，它借助 TypeScript 的声明合并（Declaration Merging）机制，在同一个名字下同时挂了运行时存在的值（`string()`、`number()` 等工厂函数）和编译后才生效的类型（`infer`、`input`、`output`）。TypeScript 会根据上下文自动区分——后面跟 `()` 就是值空间调用函数，写在 `type` 后面就是类型空间取类型。

```ts
// Zod 源码（简化版）
export const z = {
  string: () => new ZodString(),
  number: () => new ZodNumber(),
  object: (shape) => new ZodObject(shape),
  // ... 值空间（运行时存在）
};

export namespace z {
  export type infer<T> = T['_output'];
  export type input<T> = T['_input'];
  export type output<T> = T['_output'];
  // ... 类型空间（编译后消失）
}
```

从源码来看，`infer` 实际上是 `output` 的别名，定义在 `src/v4/core/core.ts:117-120`，通过 `src/v4/classic/external.ts:13` 导出供用户使用。

```ts
// src/v4/core/core.ts:117-120
export type input<T> = T extends { _zod: { input: any } } ? T["_zod"]["input"] : unknown;
export type output<T> = T extends { _zod: { output: any } } ? T["_zod"]["output"] : unknown;
export type { output as infer };  // infer 就是 output 的别名
```

实际使用时，`z.infer` 负责在编译时从 schema 提取出静态类型，供函数签名、变量声明、接口组合等场景使用；而 `.parse()` 负责在运行时对真实数据进行校验并返回类型安全的值。两者配合使得同一个 schema 定义能同时服务于编译期类型检查和运行时数据校验。

```ts
// 1. 定义 schema
const UserSchema = z.object({ name: z.string(), age: z.number() });

// 2. 用 infer 提取类型（编译时）
type User = z.infer<typeof UserSchema>;

// 3. 用 parse 验证数据（运行时）
function createUser(data: unknown): User {
  return UserSchema.parse(data);  // ← 运行时验证，返回类型安全的值
}

// 4. 用 User 类型做其他事
const users: User[] = [];
function processUser(user: User): void { ... }
```

### 默认值与转换

```ts
z.string().default('hello')
z.number().transform(x => x.toString())
z.string().pipe(z.number())  // 先校验 string，再转 number（Codec）
```

### JSON Schema 转换

`z.toJSONSchema()` 把 Zod schema 转换成 JSON Schema 标准格式。这个转换在 AI Agent 场景中至关重要——LLM 的 tool calling 接口不接受 Zod 对象，只接受 JSON Schema，所以 Mastra 在背后自动调用 `toJSONSchema()` 将开发者写的 Zod schema 转成 LLM 能理解的参数描述。

```ts
import { z, toJSONSchema } from 'zod';

const schema = z.object({
  location: z.string().describe('City name'),
  units: z.enum(['celsius', 'fahrenheit']).default('celsius'),
});

const jsonSchema = toJSONSchema(schema);
// → {
//     "type": "object",
//     "properties": {
//       "location": { "type": "string", "description": "City name" },
//       "units": { "type": "string", "enum": ["celsius", "fahrenheit"], "default": "celsius" }
//     },
//     "required": ["location", "units"],
//     "additionalProperties": false
//   }
```

`.describe()` 在这个流程中变成了 LLM 能读懂的参数说明，这也是为什么在定义 tool 的 inputSchema 时给每个字段加 `.describe()` 很有价值——它直接影响 LLM 对参数的理解。

### Schema 组合

Zod 提供了一组方法从已有 schema 派生出新 schema，全部返回新实例，不修改原 schema。

```ts
const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  age: z.number(),
});

// .pick() — 只保留指定字段
const NameOnly = UserSchema.pick({ name: true, email: true });
// → { name: string, email: string }

// .omit() — 排除指定字段
const NoId = UserSchema.omit({ id: true });
// → { name: string, email: string, age: number }

// .partial() — 所有字段变可选
const Partial = UserSchema.partial();
// → { id?: string, name?: string, email?: string, age?: number }

// .extend() — 追加字段
const Extended = UserSchema.extend({ role: z.string() });
// → { id, name, email, age, role }

// .merge() — 合并两个 object schema
const AddressSchema = z.object({ city: z.string(), zip: z.string() });
const Merged = UserSchema.merge(AddressSchema);
// → { id, name, email, age, city, zip }
```

典型场景是定义一个基础 schema，然后通过 pick/omit/extend 派生出不同用途的子 schema，避免重复定义。比如从完整的 User schema 中 pick 出 name 和 email 作为创建接口的入参，用 partial 作为更新接口的入参（所有字段可选）。

### 判别联合：z.discriminatedUnion()

当数据的结构由某一个字段的值决定时，用 `z.discriminatedUnion()` 而不是 `z.union()`。它通过检查区分字段的值直接定位到对应的 schema，不需要逐个尝试，性能更好且错误信息更精确。

```ts
const ToolResult = z.discriminatedUnion('type', [
  z.object({ type: z.literal('weather'), temperature: z.number(), city: z.string() }),
  z.object({ type: z.literal('search'), results: z.array(z.string()), query: z.string() }),
  z.object({ type: z.literal('error'), message: z.string(), code: z.number() }),
]);

// type: 'weather' → 匹配第一个 schema
ToolResult.parse({ type: 'weather', temperature: 25, city: 'Beijing' });
// → { type: 'weather', temperature: 25, city: 'Beijing' }

// type: 'unknown' → 没有匹配的 schema
ToolResult.safeParse({ type: 'unknown' });
// → { success: false, error: 'Invalid discriminator value. Expected "weather" | "search" | "error"' }
```

在 Agent 场景中，tool 的返回结果通常是多态的——不同 tool 返回不同结构，用 `type` 字段区分。`z.infer` 能正确推导出判别联合的类型，在 TypeScript 中通过 `result.type` 做类型收窄。

### 强制类型转换：z.coerce

`z.coerce` 在验证之前先用 JavaScript 内置转换函数把值转成目标类型，本质等价于 `.pipe()` 一个转换步骤。典型场景是 URL query 参数、HTML 表单提交、环境变量——这些来源的数据全是字符串，需要转成数字、布尔或日期。

```ts
// URL query / form 传过来的全是字符串
const input = { age: '25', active: 'true', price: '9.99' };

const schema = z.object({
  age: z.coerce.number(),      // Number('25') → 25
  active: z.coerce.boolean(),  // Boolean('true') → true
  price: z.coerce.number(),    // Number('9.99') → 9.99
});

schema.parse(input);
// → { age: 25, active: true, price: 9.99 }
```

`z.coerce.number()` 大致等价于 `z.any().pipe(z.number())`——先做类型转换，再用目标 schema 的校验规则检查转换后的值。

### 错误格式化

Zod v4 提供了五个错误格式化方法，把原始的 `issues` 数组转成不同结构。

```ts
const result = schema.safeParse({ name: 'A', age: -1, email: 'bad' });
if (!result.success) {
  // 1. error.issues — 原始数组，包含 path / code / message 等完整信息
  result.error.issues
  // → [{ path: ['name'], code: 'too_small', message: '...' }, ...]

  // 2. flattenError() — 扁平结构，适合表单场景
  z.flattenError(result.error)
  // → { formErrors: [], fieldErrors: { name: ['...'], age: ['...'] } }

  // 3. treeifyError() — 树形结构，按层级组织
  z.treeifyError(result.error)
  // → { errors: [], properties: { name: { errors: ['...'] } } }

  // 4. formatError() — 类似 treeify，用 _errors 标记
  z.formatError(result.error)
  // → { _errors: [], name: { _errors: ['...'] } }

  // 5. prettifyError() — 可读字符串，适合日志和 CLI
  z.prettifyError(result.error)
  // → "✖ Too small: expected string to have >=2 characters\n  → at name\n..."
}
```

`flattenError()` 最常用于前端表单场景，`fieldErrors` 的 key 直接对应表单字段名，方便绑定到 UI 组件上显示错误提示。`prettifyError()` 适合后端日志输出或命令行工具，直接拿到人类可读的错误描述。

### 异步校验

当校验逻辑需要查数据库、调外部 API 等异步操作时，`.refine()` 的回调可以是 `async` 函数，配合 `parseAsync()` 或 `safeParseAsync()` 使用。同步的 `.parse()` 无法处理异步校验，会抛出错误。

```ts
// 模拟异步校验（查数据库用户名是否已存在）
const checkUsernameExists = async (username: string) => {
  const taken = ['admin', 'root', 'test'];
  return taken.includes(username);
};

const schema = z.object({
  username: z.string().min(3),
  email: z.string().email(),
}).refine(async (data) => {
  const exists = await checkUsernameExists(data.username);
  return !exists;
}, { message: '用户名已被占用', path: ['username'] });

// 必须用 safeParseAsync，不能用 safeParse
const result = await schema.safeParseAsync({ username: 'admin', email: 'a@b.com' });
// → { success: false, error: { issues: [{ path: ['username'], message: '用户名已被占用' }] } }
```

异步校验的典型场景包括：检查用户名/邮箱是否已存在、验证 API key 是否有效、调用第三方服务确认数据合法性等。

### 串联两个 schema：.pipe()

`.pipe()` 把前一个 schema 的输出作为后一个 schema 的输入。

```ts
// 例 1：先验证是字符串，再转成数字
z.string().pipe(z.coerce.number())
// 输入: "123" → 输出: 123

// 例 2：先 trim，再验证 email 格式
z.string()
  .transform(s => s.trim())
  .pipe(z.string().email())
// 输入: "  test@example.com  " → 输出: "test@example.com"
```

**为什么 `.transform()` 之后必须用 `.pipe()` 才能继续校验：**

```ts
// ❌ 这样写会报错
z.string()
  .transform(s => s.trim())  // 返回 ZodPipe，不再是 ZodString
  .min(3)                    // ← 没有 .min() 方法！

// ✅ 必须用 .pipe() 交给新的 schema
z.string()
  .transform(s => s.trim())
  .pipe(z.string().min(3))   // ← 新的 ZodString，有 .min()
```

**什么时候必须用 `.pipe()`：**

| 场景 | 原因 |
|------|------|
| `.transform()` 之后要再校验 | transform 返回 `ZodPipe`，链式断了，没有 `.min()` 等方法 |
| 复用已有 schema | 比如已有 `const EmailSchema = z.string().email()`，直接 pipe 进去 |
| 类型发生了根本变化 | `string → number → boolean`，每一步都是独立的 schema |

**什么时候不需要 `.pipe()`：**

```ts
// 纯链式就够了，不需要 pipe
z.string().min(3).max(100).email()
```

### interface 还是 z.object？

判断标准：**数据从不信任的地方来，还是从信任的地方来。**

| 场景 | 用什么 | 原因 |
|------|--------|------|
| API 入参（用户/LLM 传来） | `z.object()` | 数据不可信，必须运行时校验 |
| API 出参（返回给调用方） | `z.object()` | 框架需要校验返回值是否符合约定 |
| `fetch()` 的响应 | **应该用 Zod，但实际常偷懒用 interface** | 外部 API 响应不可信，`as T` 只是骗编译器 |
| Prisma 查询结果 | `interface` | ORM 已经保证了类型，数据可信 |
| 内部函数参数 | `interface` | 调用方是你自己，类型系统够用 |
| 配置文件读取 | `z.object()` | 文件内容不可信 |

**一句话：数据跨越信任边界 → Zod，同一个信任域内 → interface。**

---

## 6. Mastra 中的用法

在本项目中，Zod 不作为独立验证器出现，而是作为 **Mastra 组件的 schema 定义工具**——为 tool、workflow、scorer 提供输入输出的类型约束和运行时校验。

### weather-tool.ts

```ts
// 定义 tool 的输入和输出结构
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

Mastra 在调用 tool 时自动用 `inputSchema` 校验传入参数，用 `outputSchema` 校验返回值。

### weather-workflow.ts

```ts
// workflow 全局输入
const weatherWorkflow = createWorkflow({
  inputSchema: z.object({
    city: z.string().describe('The city to get the weather for'),
  }),
})

// step 输入输出
const fetchWeather = createStep({
  inputSchema: z.object({ city: z.string() }),
  outputSchema: forecastSchema,  // z.object({ date, maxTemp, minTemp, ... })
})
```

Mastra 在 step 间传递数据时自动校验 schema，保证上下游数据类型一致。

### weather-scorer.ts

```ts
// scorer 的分析步骤输出结构
.analyze({
  outputSchema: z.object({
    nonEnglish: z.boolean(),
    translated: z.boolean(),
    confidence: z.number().min(0).max(1).default(1),
    explanation: z.string().default(''),
  }),
})
```

Scorer 的 LLM 分析结果必须符合 `outputSchema`，否则 Zod 在运行时拦截并报错。
