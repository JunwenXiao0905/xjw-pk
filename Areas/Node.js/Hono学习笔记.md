---
theme: default
themeName: "默认主题"
title: "Hono 学习笔记"
---

## 目录

- [[#第1章 概述与生态]]
  - [[#1.1 什么是 Hono]]
  - [[#1.2 生态地位]]
  - [[#1.3 设计理念]]
- [[#第2章 路由与匹配]]
  - [[#2.1 基础路由方法]]
  - [[#2.2 路径参数与通配符]]
  - [[#2.3 路由分组 app.route]]
  - [[#2.4 Router 实现]]
  - [[#2.5 Presets]]
- [[#第3章 Context 与 Request/Response]]
  - [[#3.1 Context 对象]]
  - [[#3.2 HonoRequest API]]
  - [[#3.3 响应方法 c.json c.text c.html c.redirect]]
  - [[#3.4 上下文变量 c.set c.get c.var]]
  - [[#3.5 c.header c.status c.res]]
- [[#第4章 中间件]]
  - [[#4.1 内置中间件全览]]
  - [[#4.2 自定义中间件]]
  - [[#4.3 第三方中间件]]
  - [[#4.4 执行顺序与 await next]]
- [[#第5章 校验与类型安全]]
  - [[#5.1 Validator]]
  - [[#5.2 集成 Zod]]
  - [[#5.3 RPC 模式与 hc]]
- [[#第6章 Helpers]]
  - [[#6.1 html / JSX]]
  - [[#6.2 Streaming]]
  - [[#6.3 Cookie / JWT / SSG]]
  - [[#6.4 其他 Helpers]]
- [[#第7章 常用中间件参考]]
  - [[#7.1 认证类]]
  - [[#7.2 缓存与压缩]]
  - [[#7.3 安全]]
  - [[#7.4 可观测]]
  - [[#7.5 其他]]
- [[#第8章 部署与运行时]]
  - [[#8.1 Cloudflare Workers / Pages]]
  - [[#8.2 Deno / Bun]]
  - [[#8.3 Node.js]]
  - [[#8.4 Vercel / Next.js]]
  - [[#8.5 AWS Lambda / Lambda@Edge]]
  - [[#8.6 其他平台]]
- [[#第9章 工程实践与坑点]]
  - [[#9.1 最佳实践]]
  - [[#9.2 常见坑点]]
  - [[#9.3 测试]]
  - [[#9.4 FAQ]]

---

# 第1章 概述与生态

## 1.1 什么是 Hono

Hono（日语"火焰"🔥）是一个基于 Web Standards 的 TypeScript Web 框架。核心定位：**轻量、极速、跨运行时**的 API server 框架。

**最小案例：**

```ts
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.text('Hono!'))

export default app
```

- `new Hono()` 创建应用实例
- `app.get(path, handler)` 注册路由
- handler 接收 `Context`（`c`），通过 `c.text()` / `c.json()` 等方法返回 `Response`
- `export default app` 供运行时入口调用

**关键事实：**

| 项              | 值                                                                                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| npm 版本         | v4.12.26                                                                                                                                  |
| GitHub Stars   | 31k+                                                                                                                                      |
| 依赖数            | 零依赖                                                                                                                                       |
| `hono/tiny` 体积 | <14KB minified（Express 572KB）                                                                                                             |
| TypeScript     | first-class，路径参数自动推导字面量类型                                                                                                                 |
| 运行时            | Cloudflare Workers/Pages、Deno、Bun、Fastly、Vercel、Next.js、Netlify、AWS Lambda、Lambda@Edge、Azure、GCP、Supabase、阿里云、WASM、Service Worker、Node.js |

## 1.2 生态地位

Hono 是 **Edge Computing 场景下 TypeScript Web 框架事实标准**。Cloudflare 自家产品（D1、Workers KV、cdnjs）内部都用 Hono 做 API server。

| 类别 | 项目 | 关系 |
|------|------|------|
| **Cloudflare 自有** | Cloudflare D1 / Workers KV / cdnjs | 内部 API server 使用 Hono |
| **认证** | Unkey / Clerk | API server 使用 Hono |
| **监控** | OpenStatus | API server 使用 Hono（Bun 运行时） |
| **AI** | BaseAI | API server 使用 Hono |
| **运行时基准** | Deno Benchmarks | 使用 Hono 做性能基准测试 |
| **Validator 集成** | `@hono/zod-validator` | 官方中间件，连接 Zod 与 Hono |
| **RPC 类型共享** | `hono/client` (`hc`) | 客户端读取服务端路由类型，实现端到端类型安全 |

与 Express 的区别：Express 是 Node.js 专属框架；Hono 基于 Web Standards（`Request` / `Response` / `Headers` / `URL` 等 Fetch API 对象），同一段代码可在全部支持 Web Standards 的运行时上跑。Node.js 需通过 `@hono/node-server` 适配。

## 1.3 设计理念

### 1.3.1 Web Standards-first

Hono 只使用 Web Standards API — `Request`、`Response`、`Headers`、`URL`、`URLSearchParams`。这些是 Fetch API 定义的基础对象，Cloudflare Workers / Deno / Bun 原生支持。

不使用 Node.js 专属 API（如 `http.IncomingMessage`、`http.ServerResponse`）。这让同一份代码跨运行时运行无需改动。Node.js 需 `@hono/node-server` 适配器将 Node.js 的 HTTP 对象转成 Web Standards 对象。

一个不依赖 Hono 的 Web Standards 服务端写法（Cloudflare Workers / Bun 原生可跑）：

```ts
export default {
  async fetch() {
    return new Response('Hello World')
  },
}
```

Hono 在这之上加了路由、中间件、类型推导等能力。

WinterCG（Cloudflare / Deno / Shopify 等发起的 WinterCG 小组）推动 Web Standards 在不同运行时间的互操作性。Hono 跟随这一方向。

### 1.3.2 Multi-runtime

同一段 Hono 代码跑在所有支持 Web Standards 的运行时上。差异只在入口文件（如何把 Hono app 接入运行时的 fetch handler）：

```ts
// Cloudflare Workers / Pages / Vercel (edge-light)
export default app  // app 本身就是 { fetch } 形式

// Deno
export default app  // 同上

// Bun
export default {
  port: 3000,
  fetch: app.fetch,
}

// Node.js (需 @hono/node-server)
import { serve } from '@hono/node-server'
serve(app, (info) => { console.log(info.port) })
```

### 1.3.3 RegExpRouter — 单次正则匹配

Hono 的默认路由策略是 `SmartRouter` + `RegExpRouter` + `TrieRouter` 组合。

**RegExpRouter** 的机制：在路由注册阶段，把所有路由模式编译成**一个大的正则表达式**，请求到来时做一次正则匹配即可定位路由，不做线性遍历。

```
                  传统路由（Express / path-to-regexp）
                  ─────────────────────────────────
                  逐条遍历路由列表 → 每条做一次正则匹配
                  路由越多越慢

                  RegExpRouter
                  ─────────────────────────────────
                  注册阶段：所有路由 → 合并为一个大正则
                  请求阶段：一次 .match() → 直接拿到结果
                  路由数量对匹配性能影响小
```

RegExpRouter 不支持所有路由模式（复杂通配符场景可能回退），因此 Hono 默认用 SmartRouter 检测路由特征，自动在 RegExpRouter 和 TrieRouter 间选择最快的。

### 1.3.4 零依赖 + 按需打包

`hono` 包零依赖。中间件和适配器是独立子路径导入（`hono/logger`、`hono/etag` 等），仅在实际 import 时才被 bundler 打进产物。`hono/tiny` preset 进一步裁剪路由实现，将体积压到 <14KB。

### 1.3.5 TypeScript-first — 路径参数字面量类型推导

```ts
const app = new Hono()

app.get('/entry/:date/:id', (c) => {
  const { date, id } = c.req.param()
  //          ^? string  — 类型安全
  //   date 和 id 在路径中定义了，TypeScript 自动推导为字面量联合类型
  return c.json({ date, id })
})
```

配合 `hc`（Hono Client）和 Zod Validator，可实现端到端类型安全：服务端路由类型通过 `export type AppType = typeof route` 导出，客户端 `hc<AppType>(baseUrl)` 读取该类型，调用时自动补全路径、参数类型和返回值类型。