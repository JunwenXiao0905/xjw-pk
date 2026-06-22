# 目录

- [[#1. 全景与定位|1. 全景与定位]]
  - [[#1.1 五者各是什么|1.1 五者各是什么]]
  - [[#1.2 它们其实不在同一条赛道|1.2 它们其实不在同一条赛道]]
  - [[#1.3 一句话选型|1.3 一句话选型]]
- [[#2. 数据对比（调查所得）|2. 数据对比（调查所得）]]
  - [[#2.1 npm 周下载量与增长|2.1 npm 周下载量与增长]]
  - [[#2.2 GitHub 活跃度|2.2 GitHub 活跃度]]
  - [[#2.3 包体积与依赖数|2.3 包体积与依赖数]]
  - [[#2.4 性能基准|2.4 性能基准]]
  - [[#2.5 怎么读这些数据|2.5 怎么读这些数据]]
- [[#3. 逐框架拆解|3. 逐框架拆解]]
  - [[#3.1 Express|3.1 Express]]
  - [[#3.2 Fastify|3.2 Fastify]]
  - [[#3.3 Hono|3.3 Hono]]
  - [[#3.4 NestJS|3.4 NestJS]]
  - [[#3.5 Next.js|3.5 Next.js]]
- [[#4. 关键问题逐一对比|4. 关键问题逐一对比]]
  - [[#4.1 编码手感：Hono vs Fastify|4.1 编码手感：Hono vs Fastify]]
  - [[#4.2 企业级能力：Nest 甜点 vs Hono 自建|4.2 企业级能力：Nest 甜点 vs Hono 自建]]
  - [[#4.3 类型安全与 schema：Zod 当通用契约|4.3 类型安全与 schema：Zod 当通用契约]]
  - [[#4.4 Hono 企业级怎么搭|4.4 Hono 企业级怎么搭]]
  - [[#4.5 可迁移性：前期 Hono 后期 Nest？|4.5 可迁移性：前期 Hono 后期 Nest？]]
  - [[#4.6 Next.js 的坑|4.6 Next.js 的坑]]
  - [[#4.7 「成熟就迁 Go」命题的真伪|4.7 「成熟就迁 Go」命题的真伪]]
- [[#5. 当代 TS 全栈通用形状|5. 当代 TS 全栈通用形状]]
  - [[#5.1 收敛的架构|5.1 收敛的架构]]
  - [[#5.2 Nest 概念到 Hono 的替换表|5.2 Nest 概念到 Hono 的替换表]]
- [[#6. 选型决策框架|6. 选型决策框架]]
  - [[#6.1 三区模型|6.1 三区模型]]
  - [[#6.2 zone 3 是语言题，不是框架题|6.2 zone 3 是语言题，不是框架题]]
  - [[#6.3 场景速查表|6.3 场景速查表]]
  - [[#6.4 给后端新手 / TS-first 小团队|6.4 给后端新手 / TS-first 小团队]]
- [[#附录：数据来源|附录：数据来源]]

# 1. 全景与定位

## 1.1 五者各是什么

```text
Express   —— 最经典的 Node HTTP 框架，事实标准，但已老
Fastify   —— Node 上轻量、高性能的 HTTP 框架，性能标杆
Hono      —— 运行时无关的轻量 HTTP 框架（Node/Bun/Deno/Edge），未来式
NestJS    —— 全功能企业框架（DI+模块+装饰器），可挂 Express 或 Fastify
Next.js   —— React meta-framework（SSR/SSG/RSC），内容向 + 全栈一体
```

## 1.2 它们其实不在同一条赛道

把五个名字放一起比较，最容易踩的坑是**当成同一类东西比性能**。它们分三层：

```text
渲染 / meta 层        Next.js
                 （负责页面、SEO、首屏；它的"后端"是 route handler / server action）

全功能企业后端层      NestJS
                  （DI、模块、横切构件；真对手是 Java/Go，不是 Hono）

轻量 HTTP 框架层      Hono / Fastify / Express
                  （只管接 HTTP 返回 JSON；Nest 可以挂在 Fastify 上面）
```

两条推论：

- **Nest 和 Hono 不直接竞争**：Nest 可以把 Hono/Fastify 当底层；Nest 的真正比较对象是 Java(Spring)/Go，见 [[#6.2 zone 3 是语言题，不是框架题|6.2]]。
- **Hono 和 Fastify 才是直接对手**：同在"轻量 HTTP 框架"层，二选一是真问题，见 [[#4.1 编码手感：Hono vs Fastify|4.1]]。

## 1.3 一句话选型

```text
要 SEO / 首屏 / 内容站        → Next.js
要轻、快、API、原型           → Hono（默认）或 Fastify（纯 Node 重型单体）
要长期重业务后端 + TS-first   → NestJS（非 TS-first 则考虑 Java/Go）
```

# 2. 数据对比（调查所得）

> 全部数据自取自 npm registry 与 GitHub API，周下载区间 **2026-06-10 ~ 06-16**。性能基准来自第三方基准文章，标注来源。数据会过期，结论的方向比数字本身更重要。

## 2.1 npm 周下载量与增长

| 包                            | 周下载量        | YoY（2025-06 → 2026-06）   |
| ---------------------------- | ----------- | ------------------------ |
| **zod**（契约层）                 | **1.999 亿** | —                        |
| **express**                  | 1.119 亿     | —                        |
| **hono**                     | 4561 万      | 118 万 → 4561 万，**×38.7** |
| **@nestjs/common**           | 1201 万      | —                        |
| **@nestjs/core**             | 1155 万      | —                        |
| **@nestjs/platform-express** | 844 万       | —                        |
| **fastify**                  | 869 万       | 275 万 → 869 万，**×3.16**  |
| **prisma**                   | 1343 万      | —                        |
| **drizzle-orm**              | 1151 万      | —                        |
| **@trpc/server**             | 393 万       | —                        |
| **@hono/zod-validator**      | 294 万       | —                        |
| **@hono/zod-openapi**        | 102 万       | —                        |
| **@ts-rest/core**            | 55 万        | —                        |

读法：

- **zod 2 亿、express 1.1 亿**是"生态地基"——它们被全生态当依赖拉，反映安装图权重，不是主动选择人数。
- **判断主动采用，看 `@nestjs/core`(~1155 万) 和 `@nestjs/common`(~1201 万)**——只有主动用 Nest 才会装。
- **hono 的 ×38.7 vs fastify 的 ×3.16**：一年前 hono 还不到 fastify 一半，现在反超 5 倍。势头碾压。
- **@trpc/server 393 万 vs @ts-rest/core 55 万**：tRPC 仍是类型穿透的主流方案之一；ts-rest 是小众玩家（社区体量小两个量级，踩坑时资料少）。

## 2.2 GitHub 活跃度

| 仓库 | Stars | Forks | Open issues | 创建 | 最近推送 |
|---|---|---|---|---|---|
| nestjs/nest | **75.9k** | — | — | — | — |
| expressjs/express | 69.2k | — | — | — | — |
| fastify/fastify | 36.5k | 2734 | 150 | 2016-09 | 2026-06-17 |
| honojs/hono | 31.0k | 1128 | 373 | 2021-12 | 2026-06-18 |

读法：

- **Nest stars 最高（75.9k）**，企业心智份额最强。
- **Fastify 比 Hono 老 5 年**（2016 vs 2021），forks 多一倍、open issues 少一半 → 更成熟、维护更稳。
- **Hono 4 年追到 31k**，且仍在每天推送，增速远超 Fastify。

## 2.3 包体积与依赖数

| 框架 | 运行时依赖 | 解压体积 | 文件数 |
|---|---|---|---|
| **hono** | **0** | 1.41 MB | 563 |
| **fastify** | 15（pino、ajv、find-my-way…） | 2.78 MB | 355 |

- hono **零运行时依赖**是它"轻量"最硬的证据，也意味着供应链更短、冷启更快、更透明。
- fastify 把日志(pino)、校验(ajv)、路由(find-my-way)硬捆进来——更"开箱"，但更重。

（express 体积介于两者之间，但已不作为新项目首选，故略。）

## 2.4 性能基准

同机器、autocannon，纯路由吞吐（来源见附录）：

| 组合                              | 约略 req/s             |
| ------------------------------- | -------------------- |
| Express                         | ~30,000              |
| Nest + Express 适配器（默认）          | ~28,000              |
| **Fastify**                     | ~45,000（优化场景可破 10 万） |
| **Nest + Fastify 适配器**          | ~45,000              |
| Hono（Node）                      | ~38,900 ~ ~70,000    |
| Hono（Bun）                       | ~80,000              |
| Hono（Cloudflare Workers / edge） | 100,000+             |

读法：

- **Nest 不是天生慢**：默认挂 Express 才 ~28k，换成 Fastify 适配器直接回到 ~45k。慢的是适配器，不是架构。
- **纯 Node 上 Fastify 和 Hono 基本平手**（Fastify 官方基准里 Fastify ~42k 微胜 Hono ~39k）。Hono 的性能优势在 **Bun / edge / 冷启**，不在纯 Node。
- **别被"Hono 更快"的标题骗**：纯 Node 跑，它和 Fastify 是一个量级。

## 2.5 怎么读这些数据

1. **下载量含大量传递安装**。express 1.1 亿、zod 2 亿不代表这么多主动用户，是"被当依赖拉"。判断主动采用看**只有主动才装的包**（如 `@nestjs/core`）。
2. **性能基准高度依赖环境**：机器、路由复杂度、中间件、是否 CPU/IO 密集。数字看量级和相对关系，别当绝对值。
3. **势头比存量重要**：hono ×38.7 的增速，说明生态在往哪走；但 fastify/nest 的存量意味着文档、插件、岗位短期不可替代。

# 3. 逐框架拆解

## 3.1 Express

- **定位**：Node HTTP 框架的鼻祖，事实标准。
- **优势**：生态最大、文档最全、几乎所有 Node 教程的默认例子。
- **代价**：基于 callback、无原生 TS、性能最弱（~30k）、维护节奏慢、新项目基本不该选。
- **适合谁**：维护老项目、学 Node 原理时读它的源码。新项目无理由选它。

## 3.2 Fastify

- **定位**：Node 上轻量、高性能 HTTP 框架，schema 声明式（ajv）+ 封装上下文。
- **优势**：纯 Node 性能标杆、成熟稳定（10 年）、插件生态大、JSON 序列化极快。
- **代价**：Node 锁死（上不了 edge/Bun 原生）、要理解 `register` 的封装上下文概念、schema 是 JSON Schema/TypeBox 体系。
- **适合谁**：纯 Node 的长期重型单体 API、团队吃 ajv/JSON Schema 那套。

## 3.3 Hono

- **定位**：运行时无关的轻量 HTTP 框架，`c` 上下文 + 函数式 `return` + 中间件当参数链。
- **优势**：零依赖、多运行时（Node/Bun/Deno/Edge/Workers）、`hc` 内置类型穿透、配 Zod 一条 schema 出"校验+类型+OpenAPI+客户端"。未来式。
- **代价**：**无内置 DI、无模块系统、无装饰器**——企业级结构要自己搭；纯 Node 性能不比 Fastify 强。
- **适合谁**：轻量 API、快速原型、edge/serverless、愿意自己组织结构的中小项目。

## 3.4 NestJS

- **定位**：全功能企业框架，DI + 模块 + 装饰器 + 横切构件（Guard/Pipe/Interceptor/Filter/Middleware）。详见 [[Node后端-NestJS工程化实操]]。
- **优势**：结构化、约定兜底、可挂 Fastify 拿性能、Swagger/auth/微服务/队列全家桶、岗位市场大、DI 心智模型可迁移到 Java/Spring。
- **代价**：重、装饰器+元数据魔法多、默认 DTO 是 class-validator（非 schema-first）、企业级心智负担。
- **真对手**：Java(Spring)/Go，不是 Hono。
- **适合谁**：长期重业务后端、大团队、TS-first 团队、**后端新手建立工程结构感**。

## 3.5 Next.js

- **定位**：React meta-framework，SSR/SSG/RSC + 全栈一体。
- **优势**：SEO/首屏、图片字体优化、metadata API、生态成熟、招人容易、一仓搞定。
- **代价**：Vercel 锁定、App Router/RSC/缓存是"会动的魔法"、全栈耦合后端焊死、dev/build 慢、重客户端库（Cesium）错配。详见 [[#4.6 Next.js 的坑|4.6]]。
- **适合谁**：内容站/营销站/官网/需 SEO 的页面。**不适合**扛核心后端和重客户端交互（Cesium 大屏）。Cesium 集成的痛见 [[Next.js集成Cesium完整方案]]。

# 4. 关键问题逐一对比

## 4.1 编码手感：Hono vs Fastify

同一 POST 接口，差异最直观的是四点：

| 差异点  | Hono                                       | Fastify                              |
| ---- | ------------------------------------------ | ------------------------------------ |
| 上下文  | 单个 `c`（`c.req`/`c.json`/`c.set`）           | 双对象 `(request, reply)`               |
| 响应方式 | 只能 `return c.json(...)`（函数式）               | 可变 `reply`，`.send()` 或 `return`      |
| 校验写法 | 中间件当位置参数 `app.post(p, zValidator(...), h)` | schema 声明在路由选项 `{ schema:{ body } }` |
| 类型穿透 | 内置 `hc<AppType>()`                         | 靠 TypeBox / ts-rest / codegen        |
| 路由组织 | `app.route()` 函数组合                         | `register(plugin, {prefix})` 封装上下文   |

```ts
// Hono:一个 c + 函数式 return + 中间件当参数
app.post('/notes', zValidator('json', CreateNote), (c) => {
  const body = c.req.valid('json')        // 已校验+类型推断
  return c.json({ id: 1, ...body }, 201)  // 没有 reply,只能 return
})

// Fastify:request/reply + schema 声明 + 命令式 send
app.post('/notes', { schema: { body: CreateNote } }, async (req, reply) => {
  const note = { id: 1, ...req.body }
  return reply.code(201).send(note)       // 可变 reply
})
```

一句话：**Hono 函数式、好组合、类型穿透白送；Fastify 命令式、reply 可控、插件封装上下文企业级。**

## 4.2 企业级能力：Nest 甜点 vs Hono 自建

哪些业务 Nest 原生顺手、Hono 要自己造（这是 Nest 的重量买单之处）：

| 业务                             | Nest                                        | Hono                        | 评价            |
| ------------------------------ | ------------------------------------------- | --------------------------- | ------------- |
| 微服务/MQ（Kafka/RabbitMQ/gRPC 抽象） | `@nestjs/microservices` `@MessagePattern`   | 自己接 kafkajs/BullMQ          | ❌ Nest 碾压     |
| 多策略认证（session+JWT+OAuth）       | `@nestjs/passport` + 多 Strategy             | 自己搭策略机                      | ❌ Nest 碾压     |
| 可替换 provider + 测试替身            | token + useFactory/useValue                 | 装配根手写 if/else               | ✅ Nest 更顺     |
| 跨模块深依赖装配                       | `@Module` 自动                                | 手工/Awilix                   | ✅ Nest 更顺     |
| 定时任务 / 队列 worker               | `@Cron` / `@nestjs/bull @Processor`         | node-cron / BullMQ 手动       | ⚠️ Nest 省事    |
| WebSocket / 实时推送               | `@WebSocketGateway`                         | ws / Bun WS 手动              | ⚠️ Nest 省事    |
| 声明式事务 + 多 service 编排           | TypeOrmModule + CLS                         | 手动事务传播                      | ⚠️ Nest 省事    |
| CQRS / 事件总线                    | `@nestjs/cqrs`                              | 自己写 bus                     | ❌ Nest 碾压     |
| Swagger 文档                     | `@nestjs/swagger` `@ApiProperty`（重复 schema） | `@hono/zod-openapi`（一条 Zod） | ✅ **Hono 更顺** |
| DTO 校验/组合                      | class-validator `PartialType`               | Zod `.partial()/.pick()`    | ✅ Hono 更顺     |

规律：**"非 HTTP 协议 + 声明式横切 + provider 可替换/可测"三类业务 Nest 碾压；纯 HTTP + schema 那类 Hono 不输甚至更顺。**

## 4.3 类型安全与 schema：Zod 当通用契约

- **zod 周下载 2 亿**（比 express 还大）——TS 生态的事实标准契约层。无论后端用哪个框架，Zod 都是地基。
- **DTO 是否被 Zod 取代**：Nest 默认 DTO 是 class-validator（class + 装饰器元数据，靠 `ValidationPipe` 实例化），但**可用 Zod 替代校验层**（`ZodValidationPipe` / `nestjs-zod`）。class-validator 不会被踢出默认，但 schema-first 的 Zod 是趋势。
- **三套类型穿透方案**：tRPC(共享 router 类型) / Hono `hc`(标准 HTTP 上做类型穿透) / ts-rest(小众)。Hono `hc` 把 tRPC 的 DX 放回标准 HTTP，不绑协议。

## 4.4 Hono 企业级怎么搭

Hono 刻意不带 DI/模块/装饰器（作者设计如此）。企业级打法是**自己当架构师**，落六边形/端口-适配器：

```text
src/
├── domain/          # 框架无关核心(service/repo/schema),不 import 'hono' —— 迁移本钱
├── infra/           # 基础设施适配器(db/auth/config),实现 domain 端口
├── http/hono/       # HTTP 适配层:routes + middlewares + onError
├── jobs/            # 后台:cron / BullMQ worker
├── container.ts     # 装配根:手工 DI(主流模板不用 Awilix)
└── main.ts          # 接 runtime(Node/Bun/Workers)
```

关键模式：

- **路由工厂**：`const notesRoutes = (deps: { service }) => { const app = new OpenAPIHono(); ... return app }`
- **Guard 当中间件**：`createMiddleware` + `c.set('user', ...)`，`requireRole('admin')` 当位置参数
- **异常映射**：`app.onError((err, c) => ...)` 替代 `@Catch`
- **装配**：`buildApp()` 里 `new XxxService(new XxxRepo(db))` 手工构造注入

现成模板（已核真实）：[Joker666/hono-starter](https://github.com/Joker666/hono-starter)、[elieteyssedou/clean-boilerplate-26](https://github.com/elieteyssedou/clean-boilerplate-26)。

## 4.5 可迁移性：前期 Hono 后期 Nest？

**可行，且 Hono→Nest 比 Nest→Hono 顺**，但有个硬前提：**业务核心零框架依赖（六边形）**。

| 能搬过去（框架无关） | 必须重写（框架特有） |
|---|---|
| Zod schema、service/repository、领域类型、单测 | 路由层、中间件、装配、`onError`、OpenAPI 路由定义 |

迁移成本 ∝ 业务逻辑泄漏进框架特定代码的程度。守不住六边形 = 重写。最大隐藏成本：**前端 `hc` 类型客户端**（迁 Nest 后类型穿透没了）+ **部署假设**（Hono 上 Workers/Nest 上不了）。

**别按时间迁，按需求迁**：只有撞进 Nest 甜点（[[#4.2 企业级能力：Nest 甜点 vs Hono 自建|4.2]]）且"在 Hono 自建成本 > 迁移成本"时才迁。否则 Hono 可一辈子不迁。

## 4.6 Next.js 的坑

1. **Vercel 锁定**：ISR/Image Opt/Edge/middleware 在 Vercel 开箱，自建降级或复杂（OpenNext 才能上 AWS/CF）。
2. **App Router/RSC/缓存是会动的魔法**：Next 13/14 默认强缓存 fetch，15 又改回不缓存；RSC 边界对很多人是黑盒。
3. **全栈耦合**：业务塞 server actions/route handlers → 后端焊死，要拆出迁 Go 很疼。
4. **dev/build 慢**：大项目 dev 卡顿常见。
5. **重客户端库错配**：Cesium 等 import 时碰 `window` 的库，要 `'use client'` + `ssr:false` + 手动拷静态资源 + 设 `CESIUM_BASE_URL`。Vite 无此包袱且有插件。详见 [[Next.js集成Cesium完整方案]]。
6. **AI 时代红利贬值**：文件即路由等"省打字"卖点，在 AI 代写时代价值下降；而它的魔法（缓存/RSC 边界）反而让 AI 生成的代码更难调。**省打字贬值、省调试升值**，Next 的价值相对缩水。

## 4.7 「成熟就迁 Go」命题的真伪

> 说法："快速开发选 fastify，业务成熟直接迁 go，用 nestjs 既不快后续也得迁。"

逐条判：

- **"fastify 快"** ✅ 真（纯 Node 性能标杆）。
- **"nest 既不快"** ⚠️ 夸大：Nest+Fastify 适配器 ≈ Fastify 原生（~45k），慢的是默认 Express 适配器，不是架构。
- **"成熟直接迁 go"** ⚠️ 夸大：Go 裸性能/并发/内存确实 > Node，但多数后端是 I/O 密集，Node 有竞争力。迁 Go 的强动机是**持续内存问题/CPU 密集/并发瓶颈/压成本**，不是"成熟了就该迁"。
- **"后续也得迁"** ❌ 最弱：无内在原因必须迁；幸存者偏差（写出来的都是迁了的）。

## 5. 当代 TS 全栈通用形状

## 5.1 收敛的架构

没有唯一栈，但**形状高度收敛**（= 六边形/端口-适配器在 TS 全栈的当代形态）：

```text
monorepo (pnpm / Turborepo)
├── packages/shared/      # 共享 Zod schema —— 通用契约层（地基）
├── apps/api/             # 薄适配器(Hono/Fastify) + 框架无关 domain + ORM
└── apps/web/             # 前端,用 hc/ts-rest/codegen 消费 schema
```

四个不变量：

1. **契约层 = Zod**（共享包，前后端唯一真相源）
2. **HTTP = 薄适配器**（可换，不进 domain）
3. **domain = 框架无关**（可迁移本钱）
4. **类型流 = hc / ts-rest / codegen 三选一**

这正是 [[TS全栈单体化仓库模板]] 的基线（pnpm + React+Vite + Fastify + ts-rest + Zod + Drizzle/Prisma）。Hono 时代唯一可选优化：Fastify+ts-rest → Hono（`hc`+`zod-openapi` 把 ts-rest 角色折叠进框架，少一个依赖）。

## 5.2 Nest 概念到 Hono 的替换表

| NestJS | Hono 等价 | 评价 |
|---|---|---|
| `@Controller` + `@Get/@Post` | `new Hono()` 子应用 + `app.get/post` | ✅ |
| `@Param/@Query/@Body` | `c.req.param/query/json` | ✅ |
| `ValidationPipe` + DTO class | `zValidator('json', schema)` + Zod | ✅ 更顺 |
| `@Module({providers,imports,exports})` | 目录模块 + `app.route()` + 装配根 | ✅ 手工 |
| `@Injectable()` + 构造注入 | 普通 class + 构造注入 | ✅ |
| `@UseGuards` / `@Roles` | 路由中间件链 + `requireRole()` | ✅ |
| `@Catch` 异常过滤器 | `app.onError` | ✅ |
| `@nestjs/swagger` `@ApiProperty` | `@hono/zod-openapi` | ✅ 更顺 |
| `@nestjs/microservices` `@MessagePattern` | ❌ 自己接 kafkajs/BullMQ | ❌ 替换不掉 |
| 多策略认证 `@nestjs/passport` | 自己搭策略机 | ⚠️ |
| `@nestjs/cqrs` | 自己写 bus | ❌ |

规律见 [[#4.2 企业级能力：Nest 甜点 vs Hono 自建|4.2]]。

# 6. 选型决策框架

## 6.1 三区模型

```text
① 内容驱动（SEO/首屏）        → Next.js
② 轻量 API / 原型             → Hono（默认）/ Fastify（纯 Node 重型单体）
③ 长期重业务后端              → 见 6.2，这是语言题不是框架题
```

## 6.2 zone 3 是语言题，不是框架题

NestJS 本质是 Spring 的 Node 移植（DI/模块/装饰器同源）。zone 3 里 Nest 的真对手是 **Java(Spring)/Go**。选谁取决于**团队是什么语言生态**：

| 情况 | 选 | 理由 |
|---|---|---|
| 全栈 TS、前后端一种语言、共享 Zod、人能跨栈 | **NestJS** | 留在 TS 拿 Spring 级结构 |
| 已有 JVM 沉淀 / 超大型长期 / 金融政企 / 要 20 年成熟 | **Java(Spring)** | JVM 深度、成熟度、人才库 |
| 高并发 / 云原生微服务 / 压成本 / CPU 密集 | **Go** | 并发原生、占用低、单二进制 |

> **Nest 在 zone 3 唯一不能被 Java/Go 替代的理由 = "TS-first"。** 非 TS-first，Java/Go 做严肃后端通常更强。

## 6.3 场景速查表

| 场景 | 选 |
|---|---|
| 官网/落地页/需 SEO | Next.js |
| Cesium 大屏 / 重客户端交互 | Vite + SPA（**别用 Next 全栈**） |
| 轻量 API / 快速 demo / edge | Hono |
| 纯 Node 重型单体 API、吃 ajv | Fastify |
| 长期重业务后端 + TS-first | NestJS（+ Fastify 适配器） |
| 长期重业务后端 + 非 TS-first | Java / Go |
| 高并发 / 云原生 / 压成本 | Go |

## 6.4 给后端新手 / TS-first 小团队

**新手起点选 NestJS**，不是因为最快最轻，而是：

1. **它教你工程结构**：DI、分层（controller/service/repository）、模块边界、横切构件——这套是被验证的、可迁移的心智模型（和 Java/Spring、企业级后端同构）。新手最需要的是"被框架约束着学会怎么组织代码"。
2. **约定兜底**：`nest g resource` 直接生成完整 CRUD 模块，文档/教程最全，踩坑资料最多。
3. **岗位市场大**：Nest 是企业 Node 的主流，学它对接真实代码库和招聘。
4. **进可攻退可守**：性能不够换 Fastify 适配器（不用重写）；结构感建立后，再学 Hono 的轻量/六边形是降维。

**Hono 的"自由"对新手是负担**：没有 DI/模块/装饰器，新手反而不知道怎么分层、怎么组织依赖。Hono 适合"已经懂结构、想极致轻量"的人，不是"正在学结构"的人。

**结论**：新手 → Nest 建立结构感 → 想做轻量/edge 再用 Hono → 内容站用 Next。三区分工，Nest 是地基。

# 附录：数据来源

**自取（npm registry / GitHub API，2026-06-10~16）：**
- npm 周下载量、YoY：`api.npmjs.org/downloads/point/`
- 包体积/依赖数：`registry.npmjs.org/<pkg>/latest`（`dependencies` / `unpackedSize` / `fileCount`）
- GitHub stars/forks/issues：`api.github.com/repos/<owner>/<repo>`
- Nest+Hono 适配器存在性：`registry.npmjs.org`（仅 `nestjs-platform-hono@0.1.0-next.0` 预发布，无 stable）

**第三方基准/分析（含 req/s、迁移、生态）：**
- [Encore – NestJS vs Fastify vs Hono 2026](https://encore.dev/articles/nestjs-vs-fastify-vs-hono)
- [Fastify 官方基准](https://fastify.io/benchmarks/)
- [Meduzzen – NestJS vs Fastify vs Express 2026](https://meduzzen.com/blog/nestjs-vs-fastify-vs-express-backend-2026/)
- [NestJS 官方文档 – Performance](https://docs.nestjs.com/techniques/performance)
- [Yalantis – Go vs Node.js](https://yalantis.com/blog/golang-vs-nodejs-comparison/)
- [Cloudflare Blog – Hono 设计哲学](https://blog.cloudflare.com/the-story-of-web-framework-hono-from-the-creator-of-hono/)
- [Joker666/hono-starter](https://github.com/Joker666/hono-starter) / [elieteyssedou/clean-boilerplate-26](https://github.com/elieteyssedou/clean-boilerplate-26)

**关联笔记：**
- [[Node后端-NestJS工程化实操]] —— Nest 深度参考
- [[TS全栈单体化仓库模板]] —— 当代通用形状的实例
- [[Next.js集成Cesium完整方案]] —— Next 重客户端库集成的痛
- [[后端基础-认证与登录]] —— 认证相关概念
