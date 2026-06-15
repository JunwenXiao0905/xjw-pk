# TS 全栈单体化仓库模板

调研日期：2026-06-06

## 目标

面向中小型业务系统的 TypeScript 全栈 monorepo。前端、后端、共享类型、共享 UI、工程配置放在同一个仓库里，优先保证：

- 端到端类型安全；
- 本地开发启动简单；
- 共享包边界清晰；
- 后续可拆分部署；
- 不被 Next.js 全栈模式绑定。

## 推荐基线

- 包管理：`pnpm workspace`
- 前端：`React + TypeScript + Vite 8`
- 路由：`TanStack Router`
- 服务端状态：`TanStack Query`
- API：`Fastify`
- API 类型契约：`ts-rest + Zod`
- UI：`Tailwind CSS + shadcn/ui`
- 数据库：`Drizzle` 或 `Prisma`
- 测试：`Vitest`，API 侧补 `supertest` 或框架原生测试工具
- 代码质量：`Biome` 做 formatter + 基础 lint，`tsc --noEmit` 做类型检查；复杂 React/类型感知规则再补 ESLint
- 任务编排：小仓库先用 `pnpm -r`，任务变多后加 `Turborepo`

## pnpm workspace

根目录必须有 `pnpm-workspace.yaml`。内部包依赖优先写 `workspace:*`，避免 pnpm 在本地包版本不匹配时回退到 npm registry。

```yaml
packages:
  - apps/*
  - packages/*
```

```json
{
  "dependencies": {
    "@repo/contracts": "workspace:*",
    "@repo/ui": "workspace:*"
  }
}
```

## 目录结构

```txt
apps/
  web/              # React + Vite
  api/              # Fastify/Hono/NestJS
packages/
  contracts/        # API contract: ts-rest/tRPC router/Zod schema
  db/               # schema, migrations, db client
  ui/               # shadcn/ui components
  config/           # tsconfig, biome, tailwind, vitest shared config
  utils/            # shared pure utilities
pnpm-workspace.yaml
package.json
turbo.json          # 可选
```

`packages/contracts` 是前后端类型安全的核心边界。API 实现消费 contract，前端 client 也消费 contract，避免手写重复 DTO。

## API 契约选型

默认选 `ts-rest + Zod`。它适合偏 REST、未来可能开放给外部系统的业务 API。它保留 HTTP method、path、status code、schema 这些 REST 语义，同时让前端获得类似 RPC 的类型推断。

`tRPC` 不作为第一版默认项。它适合同一个 TS 体系内的前后端一体应用，开发体验直接，但协议和生态更偏 TypeScript 内部系统；如果未来要做公开 API，需要额外设计 REST/OpenAPI 层。

## Zod

TypeScript 只在编译期生效，不能验证运行时数据。凡是来自系统边界的数据，都应使用 `Zod` 定义 schema 并在进入业务逻辑前解析。

重点边界：

- API request body、query、params
- API response
- 表单提交数据
- URL search params
- 环境变量
- 数据库外部导入数据

`Zod` schema 同时作为运行时校验和静态类型来源：

```ts
const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  role: z.enum(["admin", "member"]),
})

type User = z.infer<typeof UserSchema>
```

不要手写一份 `interface User` 再手写一份校验规则。优先从 schema 推导类型，避免类型定义和运行时校验漂移。

在 `ts-rest` 路线中，`packages/contracts` 应以 `Zod` schema 为中心组织 API contract。前端 `TanStack Query` 调用 contract client，后端 `Fastify` 实现 contract handler。

## Vite 8

Vite 8 已发布稳定版，核心变化是使用 Rolldown 作为统一 Rust bundler。新模板可以直接按 Vite 8 设计，但要固定 Node 版本：`20.19+` 或 `22.12+`。

`@vitejs/plugin-react` v6 使用 Oxc 做 React Refresh transform，Babel 不再是默认依赖。需要 React Compiler 时再显式接入 Babel/Rolldown 插件链。

## TanStack Router + TanStack Query

`TanStack Router` 管页面路由和 URL 状态。`TanStack Query` 管 API 数据在前端的缓存、加载、错误、刷新和 mutation 后失效。

推荐边界：

- URL 参数、页面嵌套、导航守卫：`TanStack Router`
- 服务端列表、详情、分页、mutation：`TanStack Query`
- 表单临时状态：`React Hook Form`
- 请求传输、token、baseURL、错误归一化：`axios` 或 `fetch` wrapper
- 响应数据和输入数据校验：`Zod`

不要用 axios wrapper 代替 `TanStack Query`。axios wrapper 负责“请求怎么发”，`TanStack Query` 负责“服务端数据在前端怎么缓存和刷新”。

## shadcn/ui monorepo

shadcn/ui CLI 已支持 monorepo 初始化：

```bash
pnpm dlx shadcn@latest init --monorepo
```

官方模板会生成 `apps/web` 和 `packages/ui`，并用 Turborepo 做任务编排。适合作为 UI 包组织方式参考；不一定要全盘采用它生成的技术栈。

## ESLint 替代

`Biome` 可以覆盖格式化、import 组织和一部分 lint，适合作为模板默认值，减少 Prettier + ESLint 的配置成本。

仍保留 `tsc --noEmit`，因为 Biome/Oxlint 不是 TypeScript 类型检查器。需要以下能力时再加 ESLint：

- `eslint-plugin-react-hooks`
- 复杂类型感知规则；
- 框架专用规则；
- 已有团队规则迁移成本低。

`Oxlint` 是高性能 JS/TS linter，可作为后续替代或补充观察项；现阶段模板默认用 Biome 更稳。

## 参考仓库

- [firxworx/ts-rest-workspace](https://github.com/firxworx/ts-rest-workspace)：最贴近目标。`pnpm workspace + Fastify + React/Vite + ts-rest + Zod + TanStack Query + Tailwind + shadcn/ui`。
- [AmanVarshney01/create-better-t-stack](https://github.com/AmanVarshney01/create-better-t-stack)：可组合脚手架。可参考它如何暴露前端、后端、API、数据库、鉴权、monorepo、Biome/Oxlint 等选项。
- [kuubson/react-vite-trpc](https://github.com/kuubson/react-vite-trpc)：`React + Vite + Express + tRPC + pnpm + Turborepo`，适合参考 tRPC 路线和 TS project references。
- [t3-oss/create-t3-turbo](https://github.com/t3-oss/create-t3-turbo)：Next/Expo/tRPC 方向，适合参考多端共享和 T3 生态，不作为当前主模板。
- [Turborepo examples](https://turborepo.dev/docs/getting-started/examples)：官方示例库，可查 Vite + React、Nest.js、Biome、Tailwind 等 monorepo 组合。

## 初始模板建议

第一版不要做成“大而全生成器”。先固定一条主线：

```txt
React + Vite 8 + TanStack Router + TanStack Query
Fastify + ts-rest + Zod
pnpm workspace + Tailwind + shadcn/ui + Biome + Vitest
```

第一版先固定技术栈，不做生成器式可选项。可选技术只作为后续模板变体，不进入默认主线。

## 待决策

- 默认数据库 ORM：`Drizzle` 还是 `Prisma`
- 是否内置鉴权：`better-auth`、`Auth.js`，或先不内置
- 是否从第一版就引入 `Turborepo`
- 是否维护一套自己的 `packages/config`

## 来源

- [pnpm workspace](https://pnpm.io/workspaces)
- [Vite 8 announcement](https://vite.dev/blog/announcing-vite8)
- [shadcn/ui monorepo](https://ui.shadcn.com/docs/monorepo)
- [Zod](https://zod.dev/)
- [Biome](https://biomejs.dev/)
- [Oxlint](https://oxc.rs/docs/guide/usage/linter.html)
