
得益于 Node.js，JavaScript 已成为前后端应用的“通用语言”。服务端涌现了 Express、Fastify、Hono 等 Web 框架，生态丰富、能快速搭起 HTTP 服务——但它们多是路由/中间件层，不解决**架构**这一核心问题。Nest 就是在这之上补的一层“架构框架”。

Nest（NestJS）是一个用于构建高效、可扩展的 [Node.js](https://nodejs.org/) 服务端应用的框架。它采用渐进式 JavaScript，使用 [TypeScript](http://www.typescriptlang.org/) 构建并全面支持 TypeScript（同时仍允许开发者使用纯 JavaScript 编码），融合了 OOP（面向对象编程）、FP（函数式编程）和 FRP（函数响应式编程）的元素。

在底层，Nest 使用了强大的 HTTP 服务器框架如 [Express](https://expressjs.com/)（默认），也可以配置使用 [Fastify](https://github.com/fastify/fastify)！

Nest 提供了一套开箱即用的应用架构，使开发者和团队能够创建高度可测试、可扩展、松耦合且易于维护的应用程序。
# 目录

- [[#1. 总览：NestJS 是怎么运转的|1. 总览：NestJS 是怎么运转的]]
  - [[#1.1 快速开始：CLI 初始化|1.1 快速开始：CLI 初始化]]
  - [[#1.2 初始化的目录结构|1.2 初始化的目录结构]]
  - [[#1.3 设计理念：你填业务，框架装配|1.3 设计理念：你填业务，框架装配]]
  - [[#1.4 概念速查|1.4 概念速查]]
  - [[#1.5 构件分布|1.5 构件分布]]
  - [[#1.6 后端依赖图|1.6 后端依赖图]]
- [[#2. 全栈架构和内容讲解|2. 全栈架构和内容讲解]]
  - [[#2.1 全栈（monorepo）结构|2.1 全栈（monorepo）结构]]
  - [[#2.2 src/ 的完整工程结构（common/ 与 config/）|2.2 src/ 的完整工程结构（common/ 与 config/）]]
  - [[#2.3 dto|2.3 dto]]
  - [[#2.4 entity 与 ORM|2.4 entity 与 ORM]]
  - [[#2.5 测试|2.5 测试]]
- [[#3. 跑起第一个服务|3. 跑起第一个服务]]
  - [[#3.1 目标|3.1 目标]]
  - [[#3.2 写模块：controller + service + module|3.2 写模块：controller + service + module]]
  - [[#3.3 装配进 app.module|3.3 装配进 app.module]]
  - [[#3.4 跑起来|3.4 跑起来]]
  - [[#3.5 这几个装饰器到底干了什么（源码视角）|3.5 这几个装饰器到底干了什么（源码视角）]]
- [[#4. 接口构件参考|4. 接口构件参考]]
  - [[#4.1 控制器与路由|4.1 控制器与路由]]
  - [[#4.2 路径参数、查询参数、请求体|4.2 路径参数、查询参数、请求体]]
  - [[#4.3 DTO 与校验|4.3 DTO 与校验]]
  - [[#4.4 Zod 校验方案|4.4 Zod 校验方案]]
    - [[#4.4.1 定义 schema|4.4.1 定义 schema]]
    - [[#4.4.2 后端：挂上校验|4.4.2 后端：挂上校验]]
    - [[#4.4.3 前端：同类型 + 同校验|4.4.3 前端：同类型 + 同校验]]
    - [[#4.4.4 选型：库与范式|4.4.4 选型：库与范式]]
  - [[#4.5 Providers 与依赖注入|4.5 Providers 与依赖注入]]
  - [[#4.6 Guard 守卫|4.6 Guard 守卫]]
  - [[#4.7 Pipe 管道|4.7 Pipe 管道]]
  - [[#4.8 Interceptor 拦截器|4.8 Interceptor 拦截器]]
  - [[#4.9 Exception Filter 异常过滤器|4.9 Exception Filter 异常过滤器]]
  - [[#4.10 Middleware 中间件|4.10 Middleware 中间件]]
- [[#5. 原理拆解|5. 原理拆解]]
  - [[#5.1 装饰器元数据机制|5.1 装饰器元数据机制]]
  - [[#5.2 依赖注入机制|5.2 依赖注入机制]]
  - [[#5.3 模块系统与依赖扫描|5.3 模块系统与依赖扫描]]
  - [[#5.4 请求生命周期|5.4 请求生命周期]]
  - [[#5.5 异常处理机制|5.5 异常处理机制]]
  - [[#5.6 应用生命周期|5.6 应用生命周期]]
  - [[#5.7 装饰器的废弃语法与 TypeScript 版本锁|5.7 装饰器的废弃语法与 TypeScript 版本锁]]
- [[#6. 工程实践|6. 工程实践]]
  - [[#6.1 分层边界|6.1 分层边界]]
  - [[#6.2 测试组织|6.2 测试组织]]
  - [[#6.3 常见反模式|6.3 常见反模式]]
- [[#7. 装饰器：JS 提案、TS 演进与 NestJS 源码视角|7. 装饰器：JS 提案、TS 演进与 NestJS 源码视角]]
  - [[#7.1 装饰器到底是什么|7.1 装饰器到底是什么]]
  - [[#7.2 JS 的两套提案：Legacy 与 Stage 3|7.2 JS 的两套提案：Legacy 与 Stage 3]]
    - [[#7.2.1 Legacy（早期 Stage 2）|7.2.1 Legacy（早期 Stage 2）]]
    - [[#7.2.2 新版（Stage 3）|7.2.2 新版（Stage 3）]]
    - [[#7.2.3 对比|7.2.3 对比]]
  - [[#7.3 TypeScript 的版本演进|7.3 TypeScript 的版本演进]]
  - [[#7.4 NestJS 用哪套 + 源码层面|7.4 NestJS 用哪套 + 源码层面]]
    - [[#7.4.1 Nest 踩的是 Legacy|7.4.1 Nest 踩的是 Legacy]]
    - [[#7.4.2 Nest 的装饰器源码在做什么|7.4.2 Nest 的装饰器源码在做什么]]
    - [[#7.4.3 DI 的来源：design:paramtypes|7.4.3 DI 的来源：design:paramtypes]]
    - [[#7.4.4 为什么切不到 Stage 3|7.4.4 为什么切不到 Stage 3]]
  - [[#7.5 Nest 的处境与出路|7.5 Nest 的处境与出路]]

# 1. 总览：NestJS 是怎么运转的

## 1.1 快速开始：CLI 初始化

Nest 提供官方 CLI 脚手架，一行命令生成一个能直接跑起来的最小工程：

```bash
pnpm dlx @nestjs/cli new my-app      # 或 npx nest new my-app
cd my-app
pnpm start:dev                        # http://localhost:3000
```

## 1.2 初始化的目录结构

下面是 `nest new my-app` **实际生成**的目录：

```text
my-app/
├── src/
│   ├── main.ts                   # 入口：创建 app、挂全局件、listen(3000)
│   ├── app.module.ts             # 根模块：装配所有子模块的入口
│   ├── app.controller.ts         # 示例控制器（GET /）
│   ├── app.controller.spec.ts    # 上面控制器的单元测试
│   └── app.service.ts            # 示例 provider（被 controller 注入）
├── test/
│   ├── app.e2e-spec.ts           # e2e 测试示例（supertest 打真实接口）
│   └── jest-e2e.json             # e2e 的 jest 配置
├── ......
└── README.md
```

`nest new` 生成的就是“入口 + 根模块 + 一组示例 controller/service”的最小骨架。`main.ts` 起步、`app.module.ts` 装配、`app.controller.ts` / `app.service.ts` 是示例业务。真实项目并不会在`app.controller.ts` / `app.service.ts` 中写业务。而是在 `src/` 下逐步长出 `modules/<业务>/`、`common/`（横切件）、`config/`（配置）等目录（见第 2 章）。

生成业务模块用 CLI：`pnpm exec nest g resource notes`（`nest` 是局部命令，见上文）会按 `module / controller / service / dto / entity` 的固定模板一次生成一整套，实际长出来的目录：

```text
src/notes/
├── notes.module.ts          # 业务模块：登记下面的 controller / service
├── notes.controller.ts      # HTTP 层：路由 + 取参
├── notes.controller.spec.ts # controller 单元测试
├── notes.service.ts         # 业务逻辑层（provider）
├── notes.service.spec.ts    # service 单元测试
├── dto/
│   ├── create-note.dto.ts   # 创建请求体类型
│   └── update-note.dto.ts   # 更新请求体类型
└── entities/
    └── note.entity.ts       # 数据库表映射（ORM 实体）
```

注意它**没**生成 `common/`、`config/`——这俩永远得手动建。
## 1.3 设计理念：你填业务，框架装配

Nest 走 **Spring 那一套**（基本是 Spring 在 Node 上的翻版）：把后端拆成一组**有标准职责的零件（构件）**（如 Controller、Service、Module、Guard、Pipe、Interceptor 等），你只写零件的业务内容，**框架负责装配它们、按固定顺序调度**。

```text
请求 → Middleware → Guard → Interceptor(前) → Pipe → Controller 方法 → Interceptor(后) → 响应
       （任何一步抛异常 → Exception Filter）
```

**那 Nest 是怎么装配起来的？** 就拿刚 `nest g resource notes` 生成、已经挂进 `AppModule` 的 notes 模块串一遍真实代码：

**`src/main.ts`** —— 入口，把根模块交给容器：

```ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);   
  // 【装配】把 AppModule 交给容器，触发扫描 + 实例化
  await app.listen(process.env.PORT ?? 3000);
  // 【监听】监听 3000 端口
}
bootstrap();
```

**`src/app.module.ts`** —— 根模块，把业务模块挂进 `imports`：

```ts
import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { NotesModule } from './notes/notes.module';

@Module({
  imports: [NotesModule],          // 【装配】把 notes 业务模块挂进模块图
  controllers: [AppController],     // 示例控制器（Hello World，可删）
  providers: [AppService],          // 示例 provider（可删）
})
export class AppModule {}
```

**`src/notes/notes.module.ts`** —— 业务模块，声明“我这有哪些零件”：

```ts
import { Module } from '@nestjs/common';
import { NotesService } from './notes.service';
import { NotesController } from './notes.controller';

@Module({
  controllers: [NotesController],  // 【装配】要实例化的控制器
  providers: [NotesService],       // 【装配】能注入的 provider （框架自动实例化）
})
export class NotesModule {}
```

**`src/notes/notes.controller.ts`** —— 贴标签（路由 + 取参）+ 声明依赖：

```ts
import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { NotesService } from './notes.service';
import { CreateNoteDto } from './dto/create-note.dto';
import { UpdateNoteDto } from './dto/update-note.dto';

@Controller('notes')                           // 【贴标签】控制器，前缀 /notes
export class NotesController {
  constructor(private readonly notesService: NotesService) {}   
  // 【声明依赖】要 NotesService，配合 providers: [NotesService]、@Injectable()

  @Post()                           // 【贴标签】POST /notes
  create(@Body() createNoteDto: CreateNoteDto) { return this.notesService.create(createNoteDto); }

  @Get(':id')                       // 【贴标签】GET /notes/:id
  findOne(@Param('id') id: string) { return this.notesService.findOne(+id); }
  // 还有 findAll / update / remove，写法一样
}
```

**`src/notes/notes.service.ts`** —— 贴 provider 标签，写业务（生成的是桩，后续接库）：

```ts
import { Injectable } from '@nestjs/common';
import { CreateNoteDto } from './dto/create-note.dto';

@Injectable()                       // 【贴标签】可注入 provider
export class NotesService {
  create(createNoteDto: CreateNoteDto) { return 'This action adds a new note'; }   // 桩，先不接库
  findOne(id: number) { return `This action returns a #${id} note`; }
  // 还有 findAll / update / remove
}
```

**串起来看装配：** 

```text
从main.ts中NestFactory.create(AppModule)起
  → 扫描器从根模块AppModule沿 imports 递归，收集所有 @Module
  → 读元数据建"模块图"
  → 容器按依赖链把所有 provider / controller 实例化、注入
  → 从 controller 的 @Get / @Post 生成路由表
  → app.listen()
```

这条链里 **装饰器贴标签 + 容器读标签装配 + 流水线处理请求**——一件没少。每个业务模块都是这条链的复制品，挂进根模块的 `imports` 即生效。

## 1.4 概念速查

真实代码的装配追踪见 [[#1.3 设计理念：你填业务，框架装配|1.3]]。这一节用一张大白话表，把第 1 章反复出现的核心概念一行一个钉死：

| 概念           | 一句话                                                                                               |
| ------------ | ------------------------------------------------------------------------------------------------- |
| **容器**       | `@nestjs/core` 里的运行时登记簿，一个应用只有一个；按配方造实例、管单例                                                       |
| **模块**       | `@Module` 标注的声明单元，说清“我这有哪些 controller / provider，导入谁、导出谁”                                         |
| **依赖**       | A 干活要用到 B，B 就是 A 的依赖（写在构造函数参数里，如：`constructor(private readonly notesService: NotesService) {} ` ） |
| **provider** | 登记进容器的“造 B 配方”（类 / 值 / 工厂），告诉容器“我能造 B”                                                            |
| **DI（依赖注入）** | 别自己 `new`——容器把造好的依赖，自动塞进构造函数                                                                      |
| **装配**       | 启动时容器读元数据，按依赖链（`design:paramtypes`）把所有实例造好、注入，再生成路由表                                              |
| **装饰器**      | 一个 `@xxx` 函数，定义时介入类/方法/参数——本质能**包装/重写**它们（如 `@log`）；Nest 里基本只用来贴元数据                               |
| **贴标签**      | 装饰器执行时往目标贴元数据；`@Module/@Controller/@Injectable/@Get/@Body` 都是在贴标签，框架据此装配                          |

**装饰器这一层，单独说清楚**

Nest 满屏的 `@Module`、`@Controller`、`@Injectable`，这套“装饰器语法”到底怎么回事？

它是一套 ES 提案，但 **JS 至今不原生支持**。Nest 用的是**早期 Stage 2 那套（Legacy）**——这套提案后来被推翻重做了，JS 引擎从没实现过；是 **TypeScript 从 1.5 起**靠 `experimentalDecorators` 开关提前实现的。最新的**新提案（Stage 3）**TS 5.0+ 已支持、引擎也在实现，但它和 Legacy **不兼容**，Nest 没用它（详见第 7 章）。

所以跑 Nest，tsconfig 必须开两个开关：`experimentalDecorators`（让 TS 认 `@xxx` 语法）、`emitDecoratorMetadata`（让 TS 把类型信息也编译进去）。

**tsc 把装饰器编译成了什么？就是普通函数调用。** 拿真实的 `NotesController` 看，你写的是：

```ts
@Controller('notes')
export class NotesController {
  constructor(private readonly notesService: NotesService) {}
}
```

tsc 编译出来是：

```js
NotesController = __decorate([
  Controller('notes'),                                  // 你写的装饰器 → 函数调用
  __metadata("design:paramtypes", [NotesService])       // tsc 因 emitDecoratorMetadata 自动加的，你没写
], NotesController);
```

`__decorate` 是 TS 自带 helper，把数组里两项依次 apply 到 `NotesController` 上——**这步不需要任何库**。运行时模块加载、这行代码执行时，两项分别跑：

**第一项 `Controller('notes')`** ——它的源码就两行（Nest 真实的 `@Controller`，去掉校验、简化 key 名）：

```ts
export const Controller = (prefix = '') =>
  (target) => {
    Reflect.defineMetadata('nest:controller', true, target);   // 贴“我是控制器”
    Reflect.defineMetadata('nest:path', prefix, target);       // 贴前缀 /notes
  };
```

执行时就在 `NotesController` 上贴了 `nest:controller = true`、`nest:path = 'notes'` 两条。

**第二项 `__metadata(...)`** ——内部调 `Reflect.metadata`（reflect-metadata 提供），贴 `design:paramtypes = [NotesService]`。

三条元数据都进了 reflect-metadata 的 WeakMap，挂在 `NotesController` 上。**没装 reflect-metadata，第二项就静默空操作**（`__metadata` 返回 undefined 被 `__decorate` 跳过），类型丢了但不报错。

**容器什么时候来读？** 启动时扫描器发现 `NotesController`，容器用 `Reflect.getMetadata` 把那三条读出来：读 `nest:controller` 确认“这是控制器”、读 `nest:path` 拿前缀 `notes`、读 `design:paramtypes` 拿 `[NotesService]` → 于是去造 `NotesService`、塞进构造函数。

（先说清一个前提：构造参数的类型不管是**普通类、接口、还是 `number`/`string` 这种原始类型**，tsc 都会往 `design:paramtypes` 里记一个值（类记成类本身、原始类型记成 `Number`/`String`、接口记成 `Object`）——**照记不误**，跟它是不是 provider、有没有 `@Injectable` 都无关。但 Nest 能不能据此注入是另一回事：容器拿着记下来的 token 去找 provider，是已登记的类才注入；若是没登记的普通类、或接口（`Object`）/原始类型这种对不上的——启动报 `Nest can't resolve dependencies of the NotesController (?, ?)`。**记（tsc）和登记（providers）是两回事**，详见 [[#5.2 依赖注入机制|5.2]]。）

所以**同一个 `@Controller`，从你写下到容器用上，就是“贴标签（tsc + reflect-metadata 存）→ 读标签（容器 getMetadata）”一条链**。其他装饰器（`@Module` / `@Injectable` / `@Get` / `@Body`）同理，本质都是 `Reflect.defineMetadata` 贴键值对——完整源码见 [[#7.4.2 Nest 的装饰器源码在做什么|7.4.2]]。

回到那句话：**装饰器语法靠 TS（`experimentalDecorators`），类型元数据靠 reflect-metadata（`emitDecoratorMetadata` 生成代码、运行时执行）**，所以 Nest 的 tsconfig 三件套（`experimentalDecorators` + `emitDecoratorMetadata` + `import 'reflect-metadata'`）缺一不可。

**记住一句：Nest = 装饰器贴标签 + 容器按标签装配 + 固定流水线处理请求。** 以后看到任何 Nest 概念，先问它属于这三件里的哪一件。

## 1.5 构件分布

NestJS 把后端拆成一组可装配的"构件"，几乎每一个都对应一个装饰器：

```text
应用对象
├── @Module()           # 模块：声明一组 providers / controllers / imports / exports
├── @Controller()                # 控制器：聚合一组路由
└── @Injectable()                # provider 标记：可被 DI 容器管理的类

路由与参数
├── @Get @Post @Put @Patch @Delete   # 路由处理器
├── @Param @Query @Body            # 取路径参数 / 查询参数 / 请求体
├── @Headers @Ip @Session          # 取协议层信息
└── @Req @Res                      # 原始 Express / Fastify 对象

横切构件（按请求生命周期顺序）
├── Middleware                    # 中间件：最外层，能拿到Request/Response
├── Guard                         # 守卫：决定请求是否被允许进入
├── Interceptor                   # 拦截器：方法执行前后都能介入
├── Pipe                          # 管道：参数转换或校验
└── Exception Filter              # 异常过滤器：异常到响应的映射

异常与响应
├── HttpException 及其子类      # 内置异常：BadRequestException、NotFoundException 等
├── @Catch()                      # 自定义异常过滤器的作用范围
└── @Render()                     # 模板渲染（SSR 场景）
```

这些构件的关系压成一句：

```text
平台适配器(Express/Fastify) -> Nest app -> Module -> Controller -> Guard -> Interceptor -> Pipe -> Service
```

## 1.6 后端依赖图

NestJS 本身只是"装配框架"，真正的 HTTP 能力来自底层平台，校验、ORM 等都靠生态包。典型依赖主线：

```text
框架核心
├── @nestjs/common               # 装饰器、构件接口、工具
├── @nestjs/core                 # DI 容器、NestFactory、扫描器、实例加载器
└── @nestjs/platform-express     # 默认 HTTP 平台（基于 Express）
   └── express                   # 底层 Web 框架

元数据基础设施（DI 能工作的前提）
├── reflect-metadata             # 装饰器元数据的运行时存储
└── tsconfig: emitDecoratorMetadata + experimentalDecorators  # 编译期把类型信息写进元数据

配置层
└── @nestjs/config               # 读 .env / 环境变量，注入 ConfigService

数据校验层
├── class-validator              # 装饰器驱动的字段校验
├── class-transformer            # 普通对象 -> DTO 类实例
└── ValidationPipe               # Nest 自带管道，串起上面两个

数据库层
├── @nestjs/typeorm + typeorm    # TypeORM 集成（最主流）
├── @prisma/client / Prisma      # 或 Prisma
└── @nestjs/mongoose             # 或 Mongoose
```

这一组覆盖了 Nest 后端的最小闭环：路由、配置、DI、校验、数据库、测试。扩展到更完整的大型后端时还会长出：

```text
认证授权层
├── @nestjs/jwt                  # JWT 签发与校验
├── @nestjs/passport + passport  # 护照策略集成（本地 / JWT / OAuth）
└── bcrypt / argon2              # 密码哈希

缓存与消息层
├── @nestjs/cache-manager        # 缓存抽象
├── @nestjs/bull / BullMQ        # 队列
└── @nestjs/microservices        # 微服务 / RPC（TCP、Redis、gRPC、Kafka）

运维与启动层
├── @nestjs/swagger              # 自动生成 OpenAPI 文档
├── @nestjs/cli                  # 脚手架与构建
└── pm2 / docker                 # 进程管理 / 容器化
```

# 2. 全栈架构和内容讲解

第 1 章用真实代码把单应用的骨架和装配讲透了。本章往工程化再走一步：① 把后端演进成前后端共享类型的全栈（monorepo）结构；② 补上 `nest new` 不生成、真实工程要自己建的 `common/`、`config/`；③ 讲清业务模块里的 `dto`、`entity` 和测试。

## 2.1 全栈（monorepo）结构

上面的 `src/` 是**后端单应用**结构。一旦前端要复用后端的类型与校验（见 [[#4.3 DTO 与校验|4.3]] / [[#4.4 Zod 校验方案|4.4]]），就把它演进成 monorepo——后端挪进 `apps/api/`、前端放 `apps/web/`、共享的 schema/DTO 抽到 `packages/schemas/`：

```text
my-app/                              # 工作区根（pnpm workspaces）
├── package.json                     # 声明 workspaces + 公共 dev 脚本
├── pnpm-workspace.yaml              # 列出 apps/* 和 packages/*
├── tsconfig.base.json               # 所有子包 extends 的基础 TS 配置
│
├── apps/
│   ├── api/                         # Nest 后端（内部就是上面的 src/ 结构）
│   │   ├── package.json             #   "@my/api"，依赖 @my/schemas
│   │   ├── tsconfig.json
│   │   └── src/ …                   #   main.ts / app.module.ts / modules/ …
│   └── web/                         # 前端（Vite / Next / React）
│       ├── package.json             #   "@my/web"，依赖 @my/schemas
│       └── src/ …
│
└── packages/
    └── schemas/                     # ★ 共享契约层（单一事实源）
        ├── package.json             #   "@my/schemas"
        ├── tsconfig.json
        └── src/
            ├── index.ts
            └── notes.schema.ts      #   Zod schema / class DTO，前后端都 import
```

工作区管理器（pnpm workspaces / npm workspaces）把 `apps/` 和 `packages/` 绑成一个整体：`@my/schemas` 是独立包，api 和 web 都用 `"@my/schemas": "workspace:*"` 依赖它。

关键认知：**类型共享发生在 build 时，不是运行时**。两端打包器各自把 `@my/schemas` 编译进自己的 bundle，运行时是两份独立副本——所以 api 和 web 部署到不同服务器也不影响共享，它们靠网络传 JSON 通信，类型一致是因为源自同一个源文件。

工具选择：api + web 两个 app 起步用 pnpm workspaces 即可；等 app > 2 或 CI 构建变慢，再考虑 turborepo（别一上来就上 nx）。

## 2.2 src/ 的完整工程结构（common/ 与 config/）

`nest new` 只给骨架（`main.ts` / `app.module` / 示例 controller+service），`nest g resource` 只给一个业务模块。真实工程里还有两块**两个命令都不生成、必须自己建**的目录——`common/` 和 `config/`。把 `src/` 长完整是这样：

```text
src/
├── main.ts / app.module.ts              # 入口 + 根模块（nest new 生成）
├── app.controller.ts / app.service.ts   # 示例，可删（nest new 生成）
├── common/                              # ★ 横切件，自己建
│   ├── filters/                           #   全局/局部异常过滤器
│   ├── interceptors/                      #   日志 / 缓存 / 响应包装
│   ├── pipes/                             #   自定义校验（如 ZodValidationPipe）
│   ├── guards/                            #   鉴权
│   └── decorators/                        #   自定义装饰器
├── config/                              # ★ 配置，自己建（@nestjs/config 读 .env）
│   └── configuration.ts
└── modules/                             # 业务模块（nest g resource 生成）
    └── notes/
        ├── notes.module / controller / service
        ├── dto/                           #   请求/响应类型
        └── entities/                      #   ORM 实体
```

- **`common/`**：放跨业务的横切件——全局过滤器、拦截器、管道、守卫、自定义装饰器。它们也是 provider（带 `@Injectable()`），但服务所有模块，所以集中放这。每种是什么、怎么挂全局，见第 4 章。
- **`config/`**：放配置。配 `@nestjs/config` 的 `ConfigModule.forRoot({ isGlobal: true })` 读 `.env`，业务里通过 `ConfigService` 取值——根模块 `imports` 里挂它（Ch1 1.3 的 app.module 没挂，真实项目会挂）。

`common/` 和 `config/` 没有强制结构（子目录名是约定、不是框架要求），但社区基本都这么放，照着来就行。

## 2.3 `dto`

DTO（Data Transfer Object）对应 FastAPI 的 Pydantic 模型，放在 `modules/<业务>/dto/`。

一组接口的 DTO 通常分几类：

- `CreateXxxDto`：创建请求体
- `UpdateXxxDto`：更新请求体（常基于 `PartialType(CreateXxxDto)`）
- 响应类型：可用 TS 接口或 `class`，需要进 Swagger 文档时用带装饰器的 `class`

与 FastAPI 的关键区别：FastAPI 的 `BaseModel` 框架原生解析并强校验；Nest 的 DTO 是普通类，校验由 `class-validator` 装饰器驱动，**必须显式挂上 `ValidationPipe` 才会校验**，否则请求体只是被 `class-transformer` 转成一个实例（甚至直接是普通对象），字段约束全部失效。

## 2.4 `entity 与 ORM`

实体是数据库表的映射，放在 `modules/<业务>/entities/`。

- TypeORM：`@Entity()` + `@Column()` 装饰器定义表
- Prisma：实体定义在 `schema.prisma`，运行时用生成的 `PrismaClient`

`repository` 封装对实体的操作，和 FastAPI 的 `repository.py` 角色一致。

## 2.5 `测试`

Nest 自带测试工具 `@nestjs/testing`，测试分两类：

- 单元测试（`*.spec.ts`）：用 `Test.createTestingModule` 构建一个最小模块，用 `useValue` / `useFactory` 替换真实依赖（如把 service 依赖的 repository 换成 mock 对象）
- 端到端测试（`test/*.e2e-spec.ts`）：用 `NestFactory.createApplicationContext` 或 `supertest` 直接打真实 HTTP 接口

测试替身机制见 [[#5.2 依赖注入机制|5.2 依赖注入机制]]，原理和 FastAPI 的 `app.dependency_overrides` 同构。

# 3. 跑起第一个服务

第 1 章用 CLI 生成了骨架，第 2 章讲了文件分工。这一章亲手把一个最小业务接口“写出来 → 装进去 → 跑起来”，过程中用源码视角看清几个关键装饰器到底做了什么。跑通这一遍，Nest 的“贴标签 + 装配 + 流水线”就不再是概念，而是你能复现的东西。

## 3.1 目标

实现一个接口：`POST /notes`，传 `{ title, content }`，返回创建好的笔记。这里先不接数据库，service 里直接造一条返回——重点放在“模块怎么写、怎么装、路由怎么通”。

## 3.2 写模块：controller + service + module

三个文件，放 `src/modules/notes/`。

**`notes.controller.ts`** —— HTTP 层，贴路由标签：

```ts
import { Body, Controller, Post } from '@nestjs/common';
import { NotesService } from './notes.service';

@Controller('notes')                 // 【贴标签】控制器，路由前缀 /notes
export class NotesController {
  constructor(private readonly notes: NotesService) {}   // 【声明依赖】要 NotesService

  @Post()                            // 【贴标签】POST /notes
  create(@Body() body: { title: string; content?: string }) {
    return this.notes.create(body);  // 交给 service，controller 不写业务
  }
}
```

**`notes.service.ts`** —— 业务层，贴 provider 标签：

```ts
import { Injectable } from '@nestjs/common';

@Injectable()                        // 【贴标签】可注入的 provider
export class NotesService {
  create(body: { title: string; content?: string }) {
    return { id: Date.now(), ...body };   // 暂不接库，直接造一条返回
  }
}
```

**`notes.module.ts`** —— 把上面两个登记成一个模块：

```ts
import { Module } from '@nestjs/common';
import { NotesController } from './notes.controller';
import { NotesService } from './notes.service';

@Module({
  controllers: [NotesController],    // 【装配】要实例化的控制器
  providers: [NotesService],         // 【装配】能造、能注入的 provider
})
export class NotesModule {}
```

## 3.3 装配进 app.module

模块写好不会自动生效，必须挂进根模块的 `imports`：

```ts
// src/app.module.ts
import { Module } from '@nestjs/common';
import { NotesModule } from './modules/notes/notes.module';

@Module({ imports: [NotesModule] })
export class AppModule {}
```

这一步是装配链的关键一环：`main.ts` 把 `AppModule` 交给容器 → 容器沿 `imports` 扫到 `NotesModule` → 实例化它的 controller/service → 从 `@Controller`/`@Post` 元数据生成 `POST /notes` 路由。少挂一个 `imports`，接口就 404。

## 3.4 跑起来

```bash
pnpm start:dev
```

另开终端验证：

```bash
curl -X POST http://localhost:3000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"hello","content":"第一条"}'
# => {"id":1747...,"title":"hello","content":"第一条"}
```

能返回，说明“贴标签 → 容器装配 → 路由表 → 流水线”整条链路通了。

## 3.5 这几个装饰器到底干了什么（源码视角）

上面用到的 `@Controller` / `@Post` / `@Body` / `@Module` / `@Injectable`，去掉框架错误处理后，本质都是“往目标上贴 metadata 的普通函数”。以 `@Controller` / `@Post` 为例：

```ts
// @Controller('notes') 本质是：一个接收前缀、返回“类装饰器”的函数
export const Controller = (prefix = '') =>
  (target) => {
    Reflect.defineMetadata('nest:controller', true, target);   // 标记“这是控制器”
    Reflect.defineMetadata('nest:path', prefix, target);       // 记下前缀 /notes
  };
// @Controller('notes') 执行时，只是在 NotesController 类上贴了两个键值对——不改类的行为，只是登记。

// @Post() 同理，只是标签贴在方法上（方法装饰器签名：target, key, descriptor）
export const Post = (path = '') =>
  (target, key, descriptor) => {
    Reflect.defineMetadata('nest:method', 'POST', target, key);
    Reflect.defineMetadata('nest:path', path, target, key);
  };
```

启动时 Nest 的扫描器遍历所有带 `nest:controller` 标记的类，读它方法的 `nest:method` / `nest:path`，据此把 `POST /notes` 注册到底层 Express。**装饰器本身不实现路由逻辑，路由逻辑在框架启动期“读 metadata”时才发生。**

- `@Body()` 是参数装饰器（签名 `(target, key, index)`），记下“第 0 个参数从请求 body 取值”，路由命中后据此从 `req.body` 提取。
- `@Injectable()` 贴“可注入”标记；构造函数要 `NotesService` 这件事，靠 TS 编译期写入的 `design:paramtypes`（见 [[#5.1 装饰器元数据机制|5.1]]），容器据此 new 并注入。
- `@Module({ controllers, providers })` 把这组元数据整个贴到类上，容器据此知道要实例化什么。

完整的装饰器提案、TS 版本演进、以及 Nest 为什么卡在旧装饰器上，见 [[#7. 装饰器：JS 提案、TS 演进与 NestJS 源码视角|第 7 章]]（尤其 [[#7.4 NestJS 用哪套 + 源码层面|7.4]]）；DI 的完整机制见 [[#5.2 依赖注入机制|5.2]]。

# 4. 接口构件参考

## 4.1 控制器与路由

入口装饰器：

- `@Controller('prefix')`：声明控制器及其路由前缀
- `@Get @Post @Put @Patch @Delete @All`：方法级路由

FastAPI 把路由拆到 `APIRouter` 再注册到 `app`；Nest 把路由写在 `@Controller()` 类的方法上，再把控制器注册到 `@Module({ controllers })`。两者的拆分粒度不同：FastAPI 是"函数 + router"，Nest 是"类 + controller"。

典型写法：

```ts
// src/modules/notes/notes.controller.ts
import { Body, Controller, Get, Param, Post, Query } from '@nestjs/common';
import { NotesService } from './notes.service';
import { CreateNoteDto } from './dto/create-note.dto';

@Controller('notes')
export class NotesController {
  // 构造函数注入：service 由 DI 容器提供
  constructor(private readonly notesService: NotesService) {}

  @Post()
  create(@Body() dto: CreateNoteDto) {
    return this.notesService.create(dto);
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.notesService.findOne(id);
  }
}
```

这里的 `notesService` 不是从请求里来的，而是 Nest 在实例化 `NotesController` 时通过构造函数注入的——见 [[#5.2 依赖注入机制|5.2]]。

## 4.2 路径参数、查询参数、请求体

Nest 通过参数装饰器显式声明取值来源，**不靠类型推断**（这点和 FastAPI 不同）：

- `@Param('id')`：路径参数，取 `:id`
- `@Param()`：拿全部路径参数对象
- `@Query('skip')`：查询参数
- `@Body()`：请求体，会被管道转成 DTO 实例
- `@Headers('authorization')`、`@Ip()`、`@Session()`：协议层信息

```ts
@Get()
findAll(@Query('skip') skip?: number, @Query('take') take?: number) {
  return this.notesService.findAll({ skip, take });
}
```

不写装饰器的参数不会被注入——FastAPI 是"看类型猜来源"，Nest 是"看装饰器定来源"。这是两套设计哲学的核心差异。

## 4.3 DTO 与校验

DTO 是带校验装饰器的普通类：

```ts
// src/modules/notes/dto/create-note.dto.ts
import { IsString, IsNotEmpty, MaxLength } from 'class-validator';

export class CreateNoteDto {
  @IsString()
  @IsNotEmpty()
  @MaxLength(200)
  title: string;

  @IsString()
  content?: string;
}
```

校验生效的前提是在 `main.ts` 全局挂上 `ValidationPipe`：

```ts
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,      // 自动剥离 DTO 上没有声明的字段（防注入额外字段）
    transform: true,      // 把普通对象转成 DTO 类实例，并按类型转换
    forbidNonWhitelisted: true, // 出现未声明字段直接报错
  }),
);
```

关键点：

- 没挂 `ValidationPipe`，`@Body()` 拿到的是普通对象，`@IsString()` 这类装饰器根本不会执行。
- `transform: true` 后，函数里拿到的才是真正的 `CreateNoteDto` 实例，而不是裸对象。
- 这套校验由 `class-transformer`（转实例）+ `class-validator`（跑校验）完成，Nest 的 `ValidationPipe` 只是调用它们，机制见 [[#5.4 请求生命周期|5.4]] 中管道这一环。

DTO 的更新复用：

```ts
import { PartialType } from '@nestjs/swagger'; // 或 @nestjs/mapped-types
export class UpdateNoteDto extends PartialType(CreateNoteDto) {}
```

## 4.4 Zod 校验方案

Zod 是 4.3 那套 class-validator 的**替代方案**，不是它的子集或插件。两者是两种范式：class-validator 是「类 + 装饰器」（校验规则和类型两套定义），Zod 是「schema 单源」（一个 schema 既是运行时校验器，又通过 `z.infer` 推导出 TS 类型）。

考虑用 Zod 的三个结构性理由：

- **schema 单源**：类型从 schema 推导（`z.infer`），改一处两端类型一起变，不存在「校验装饰器和类型对不上」的漂移。
- **纯 TS、零装饰器**：不依赖 `experimentalDecorators` / `emitDecoratorMetadata`，因此**绕开了 [[#5.7 装饰器的废弃语法与 TypeScript 版本锁|5.7]] 那条雷**。
- **跨前后端共享**：同一份 schema 前后端复用，实现同类型 + 同运行时校验（见 [[#4.4.3 前端：同类型 + 同校验|4.4.3]]）。

### 4.4.1 定义 schema

schema 放在共享层（如 monorepo 的 `packages/schemas/`）或模块内 `dto/`，一个文件同时产出 schema 和类型：

```ts
// notes.schema.ts
import { z } from 'zod';

// 请求 schema —— 校验进来的 body
export const createNoteSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().optional(),
});
export type CreateNote = z.infer<typeof createNoteSchema>;  // 类型从 schema 推导，不手写

// 响应 schema —— 给返回数据定型
export const noteSchema = z.object({
  id: z.number().int(),
  title: z.string(),
  content: z.string(),
  createdAt: z.string(),
});
export type Note = z.infer<typeof noteSchema>;
```

schema 复用（Zod 原生方法，对应 class-validator 的 `PartialType` / `PickType`）：

```ts
export const updateNoteSchema = createNoteSchema.partial();               // 全部可选
export const patchTitleSchema  = createNoteSchema.pick({ title: true });  // 只取部分字段
export const withAuthorSchema  = createNoteSchema.extend({ authorId: z.number().int() }); // 扩展
```

### 4.4.2 后端：挂上校验

**接法 A：手写 `ZodValidationPipe`（Nest 官方推荐，10 行，零第三方依赖）**

```ts
// src/common/pipes/zod-validation.pipe.ts
import { PipeTransform, Injectable, BadRequestException } from '@nestjs/common';
import { ZodSchema } from 'zod';

@Injectable()
export class ZodValidationPipe<T> implements PipeTransform<T> {
  constructor(private schema: ZodSchema<T>) {}

  transform(value: unknown): T {
    const result = this.schema.safeParse(value);
    if (!result.success) {
      throw new BadRequestException(result.error.flatten().fieldErrors); // 字段级错误
    }
    return result.data; // 已校验、已转型，类型为 T
  }
}
```

在 controller 里按参数挂（per-param）：

```ts
import { createNoteSchema, CreateNote } from './notes.schema';
import { ZodValidationPipe } from '../../common/pipes/zod-validation.pipe';

const CreateNotePipe = new ZodValidationPipe(createNoteSchema);

@Post()
create(@Body(CreateNotePipe) body: CreateNote) {
  return this.notes.create(body); // body 已被 schema 校验过
}
```

管道本身的工作机制见 [[#4.7 Pipe 管道|4.7]]（请求生命周期里位于 handler 之前）。

**接法 B：`nestjs-zod`（社区包，DTO 外壳 + 全局校验 + Swagger 桥）**

```ts
import { createZodDto } from 'nestjs-zod';
import { createNoteSchema } from './notes.schema';

export class CreateNoteDto extends createZodDto(createNoteSchema) {}
// 配合全局 ZodValidationPipe，Controller 写法退回到 @Body() body: CreateNoteDto
```

底层校验仍是那个 schema，只是套了 DTO 外壳，并附带 Zod → OpenAPI 的桥（补回 Swagger）。

**per-param vs 全局**：接法 A 是显式 per-param（每个 `@Body` 指明 schema，清晰但要写一行）；接法 B 配全局 pipe 是「声明即校验」（DTO 类自带 schema，全局 pipe 自动跑）。小项目用 A；要全局统一 + DTO 体验 + Swagger 用 B。

### 4.4.3 前端：同类型 + 同校验

同一份 schema 被前端直接 import，既当类型又当校验器——这是 Zod 相对 class-validator 最大的红利：

```ts
// 前端：react-hook-form 用 zodResolver 跑同一套校验规则
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { createNoteSchema, CreateNote } from '@my/schemas';

const { register, handleSubmit } = useForm<CreateNote>({
  resolver: zodResolver(createNoteSchema), // ★ 前端校验规则 = 后端，同一个 schema 对象
});
```

关键点：

- 前端类型 `CreateNote` 与后端是**同一个 `z.infer`**，改 schema 两端编译期一起变。
- 前端校验（`zodResolver` 内部 `safeParse`）与后端（`ZodValidationPipe` 内部 `safeParse`）跑的是**同一个 schema 对象**——不会出现「前端放过、后端拒绝」。
- 对比 class-validator：它搬到前端要带 `reflect-metadata` polyfill，且 react-hook-form 没有它的官方 resolver；Zod 是 `@hookform/resolvers` 一等支持。

### 4.4.4 选型：库与范式

**用哪个库（实测 2026-06）：**

| 指标 | `nestjs-zod`（BenLorantfy） | `@anatine/zod-nestjs` |
|---|---|---|
| 周下载 | **82 万** | 15.6 万（约 1/5） |
| GitHub stars | 1080 | — |
| open issues | 20（低） | — |
| 最近 push | 2026-06-17（活跃） | 末版 ~2025-04（停更一年多） |
| **Zod 兼容** | `^3.25 \|\| ^4.0` ✅ | `^3.20` ❌ **不支持 v4** |
| Nest 兼容 | `^10 \|\| ^11` | `^7..^11` |
| 发布可信度 | GitHub OIDC + SLSA provenance | 个人发布 |

结论：用 Zod 就直接上 `nestjs-zod`，别碰 `@anatine/zod-nestjs`（卡 Zod v3、停更一年）。安全边界：即便它停更，也只是个薄胶水库——退回接法 A 那 10 行 pipe 即可。**选社区 wrapper 的前提：薄、可替换。**

**Zod vs class-validator 怎么选：**

| 维度 | class-validator（4.3） | Zod（本节） |
|---|---|---|
| 单一事实源 | 类（校验）+ 类型，两套 | ✅ schema 一个，`z.infer` 推类型 |
| 前端表单校验 | 需 reflect-metadata + 手搓 resolver | ✅ `zodResolver` 一行 |
| Swagger/OpenAPI | ✅ `@nestjs/swagger` 自动 | ⚠️ 需 `nestjs-zod` 桥 / `zod-to-openapi` |
| TS 7 装饰器雷（见 [[#5.7 装饰器的废弃语法与 TypeScript 版本锁\|5.7]]） | ❌ 深陷其中 | ✅ 纯 TS，完全免疫 |

一句话：**重度依赖 Swagger 自动文档 / 要最小认知成本 → 留 class-validator；前端要和后端逐条一致的校验 + 在意 5.7 那条雷 + 前后端同 TS → 上 Zod。** 两者也能并存（不同模块各用各的）。

## 4.5 Providers 与依赖注入

依赖注入的入口是构造函数 + `@Injectable()`。

`@Injectable()` 标注 service：

```ts
// src/modules/notes/notes.service.ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class NotesService {
  constructor(private readonly notesRepository: NotesRepository) {}

  create(dto: CreateNoteDto) { /* 业务规则 */ }
}
```

在模块里注册：

```ts
@Module({
  controllers: [NotesController],
  providers: [NotesService, NotesRepository],
})
export class NotesModule {}
```

注册时写的是类，Nest 把它当作 token，实例化后注入到任何构造函数声明该类型的地方。`providers` 数组的简写形式等价于：

```ts
providers: [
  { provide: NotesService, useClass: NotesService },
]
```

四种 provider 注册形态：

- `useClass`：注入时 new 一个类（默认）
- `useValue`：注入一个现成对象/常量（如配置值、mock）
- `useFactory`：用工厂函数构造，可依赖其它 provider（如根据配置选不同实现）
- `useExisting`：给已有 provider 起别名

```ts
{ provide: 'CONFIG', useValue: { pageSize: 20 } }

// 注入非类 token 时用 @Inject
constructor(@Inject('CONFIG') config: { pageSize: number }) {}
```

一个实用原则（和 FastAPI 一致）：

- 业务数据走 `@Param` / `@Query` / `@Body`
- 运行时对象走构造函数注入（service、repository、config、当前用户）

底层是怎么从构造函数读出依赖并注入的，见 [[#5.2 依赖注入机制|5.2]]。

## 4.6 Guard 守卫

守卫决定请求"是否被允许进入"，返回 `boolean` / `Promise<boolean>`。返回 `false`（或抛异常）会阻止后续流程。最典型的用途是鉴权。

```ts
@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const req = context.switchToHttp().getRequest();
    return !!req.user;     // 没登录就拦截
  }
}
```

使用：

```ts
@UseGuards(AuthGuard)
@Get('profile')
getProfile() { ... }
```

`Reflector` 用来读自定义装饰器写在元数据里的标记（如 `@Roles('admin')`），机制见 [[#5.1 装饰器元数据机制|5.1]]。

## 4.7 Pipe 管道

管道做两件事：**转换**（把输入变成想要的形式）和**校验**（不合法就抛异常）。在路由方法执行前、参数拿到后运行。

内置管道：`ValidationPipe`（最常用）、`ParseIntPipe`、`ParseUUIDPipe` 等。

```ts
@Get(':id')
findOne(@Param('id', ParseIntPipe) id: number) { ... }
// id 在进入方法体前已被转成 number，非数字直接抛 400
```

自定义管道：

```ts
@Injectable()
export class IntRangePipe implements PipeTransform {
  transform(value: number) {
    if (value < 0) throw new BadRequestException('必须为正数');
    return value;
  }
}
```

挂载层级：参数级（`@Param('id', Pipe)`）、方法级（`@UsePipes`）、控制器级、全局级（`main.ts` 的 `useGlobalPipes`）。层级越靠后覆盖越广。

## 4.8 Interceptor 拦截器

拦截器是"面向切面"的构件，既能改方法返回值，也能在方法执行前后插入逻辑。用 `rxjs` 的 `tap` / `map` 操作流。

```ts
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler) {
    const now = Date.now();
    return next
      .handle()                     // 返回的是 Observable，不是直接结果
      .pipe(tap(() => console.log(`耗时 ${Date.now() - now}ms`)));
  }
}
```

`next.handle()` 返回的是 RxJS `Observable`——方法返回值是流中的一个值。要改返回值就用 `map`，要在执行后做事就用 `tap`。

典型用途：日志、缓存、响应结构统一包装（如把 `{ data }` 包成 `{ code, data, message }`）、超时控制（`timeout` 操作符）。

## 4.9 Exception Filter 异常过滤器

过滤器把异常映射成响应。Nest 自带一层全局异常处理：业务里抛 `HttpException`（及其子类），它会被自动转成对应状态码的 JSON。

```ts
throw new NotFoundException('笔记不存在');
// 自动响应: 404 { statusCode: 404, message: "笔记不存在", error: "Not Found" }
```

自定义过滤器处理非标准异常或自定义异常类型：

```ts
@Catch(BusinessError)
export class BusinessFilter implements ExceptionFilter {
  catch(exception: BusinessError, host: ArgumentsHost) {
    const res = host.switchToHttp().getResponse();
    res.status(200).json({ code: exception.code, message: exception.message });
  }
}
```

`@Catch()` 决定过滤器捕获哪些异常；不传参数则捕获所有异常。

## 4.10 Middleware 中间件

中间件是 Express/Fastify 风格的"请求包装器"，能拿到 `req / res / next`，在最外层执行。典型用途：日志、CORS、请求体预处理、写 trace id。

```ts
@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    console.log(`${req.method} ${req.url}`);
    next();
  }
}
```

中间件在模块里用 `configure(consumer)` 绑定路由：

```ts
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(LoggerMiddleware).forRoutes('notes');
  }
}
```

中间件 vs 拦截器：中间件能直接操作 `res`、能提前结束请求，但不能"在方法返回后再做事"；拦截器能改返回值但不能提前 send。两者职责互补，执行顺序见 [[#5.4 请求生命周期|5.4]]。

# 5. 原理拆解

## 5.1 装饰器元数据机制

Nest 的整套装配都建立在"装饰器写元数据 + 运行时读元数据"之上。这是理解 Nest 的地基。

TypeScript 装饰器本身只是函数。`@Injectable()`、`@Controller()`、`@Get()`、`@Module()` 这些装饰器被调用时，会把"这是一段元信息"通过 `Reflect.defineMetadata` 存到目标对象上。Nest 在启动时再把这些元数据读出来，据此搭出模块图、路由表、依赖关系。

`Reflect.defineMetadata(key, value, target)` 是 `reflect-metadata` 这个 polyfill 提供的，本质是把元信息挂在目标对象的隐藏存储（WeakMap）里。TS 编译时如果开了 `emitDecoratorMetadata: true`，还会为带装饰器的类**生成**一行 `__metadata("design:paramtypes", [构造参数类型...])`（属性类型同理是 `design:type`）；这行代码运行时靠 reflect-metadata 执行、才把类型真正写进元数据——这正是 DI 能"按类型注入"的来源。

```text
@Injectable() 执行
-> 调用 Reflect.defineMetadata('nest:injectable', ..., NotesService)
-> 把"可被容器管理"的标记挂在 NotesService 上
```

```text
Nest 实例化 NotesController 时
-> Reflect.getMetadata('design:paramtypes', NotesController)
-> 读出 [NotesRepository]  （编译期自动写入的构造参数类型）
-> 去容器里找 NotesRepository 对应的实例
-> 注入到构造函数
```

读取自定义标记的工具是 `Reflector`（一个内置 provider），它封装了 `Reflect.getMetadata`：

```ts
const roles = this.reflector.get<string[]>('roles', context.getHandler());
```

`@Roles('admin')` 这种自定义装饰器就是 `SetMetadata('roles', ['admin'])` 的封装：

```ts
export const Roles = (...roles: string[]) => SetMetadata('roles', roles);
```

关键认识：

- 装饰器在"定义阶段"执行，写的是描述信息，不是运行时逻辑。
- Nest 在"启动阶段"读这些描述信息，据此构建模块图和路由表。
- "按类型注入"依赖 TS 编译期写入的 `design:paramtypes`，所以 DI 的类型来源是编译产物，不是运行时反射——这也是为什么 Nest 项目 tsconfig 必须开 `emitDecoratorMetadata` 和 `experimentalDecorators` 并引入 `reflect-metadata`。

## 5.2 依赖注入机制

依赖注入的核心和 FastAPI 一样：对象不要在函数内部手动 `new`，而是由容器装配并注入。

Nest 的 DI 容器在 `@nestjs/core` 里。它的工作分两步：先扫描构建依赖图，再按依赖顺序实例化。

没有 DI 时，控制器里会出现这种代码：

```ts
@Controller('notes')
export class NotesController {
  private service: NotesService;

  constructor() {
    const repo = new NotesRepository();   // 装配责任泄漏到了控制器
    this.service = new NotesService(repo);
  }
}
```

问题：控制器承担了对象装配、实现写死、难以替换（测试时塞不进 mock）。

Nest 的做法是只声明"我需要什么"：

```ts
constructor(private readonly notesService: NotesService) {}
```

容器读取这个声明（靠 `design:paramtypes`），找到 `NotesService` 已注册的实例，调用 `new NotesController(service)` 完成注入。

（顺带说清几件事，免得卡住。）

**那个 `import` 干了啥？** 普通 JS 模块导入，把 `NotesService` 类引用弄进作用域。它不是 DI 的一部分，但有个关键副作用：让 `emitDecoratorMetadata` 能把**真实类引用**写进 `design:paramtypes`（写类本体，不是字符串）。容器"按类型找"靠的就是这个。

**凭什么 new、凭什么注入？** 容器能 `new NotesService` 并注入，凭的是**它被登记成 provider**（`providers: [NotesService]`），`@Injectable()` 是配套的声明标签：

- `providers: [NotesService]` —— 真正的登记，告诉容器"这是个 provider，按 useClass new 它"。**这是 new 的依据。**
- `@Injectable()` —— 贴在类上的标签，声明"我是可注入 provider"（还带 scope）。**是标记 / 约定。**

光有 `@Injectable()` 没登记 → 容器里没它 → 找不到；登记了 → 容器 new 它，且**默认只 new 一次**（单例）。

**如果注入一个没登记的类：**

```ts
@Controller('notes')
export class NotesController {
  constructor(private readonly foo: SomePlainClass) {}  // SomePlainClass 没登记、没 @Injectable
}
```

启动直接报错，Nest 拒绝 new：

```text
Error: Nest can't resolve dependencies of the NotesController (SomePlainClass, ?).
Please make sure that the argument SomePlainClass at index [0] is available in the current context.
```

**关键认知：Nest 不会因为你写了个类型就自动 new 那个类。** 类型只是"查找 token"，容器里没登记这个 token 就不认、启动失败。"能不能注入"取决于**有没有登记**，不是"有没有 import / 写没写类型"。

依赖解析顺序（容器内部）：

```text
实例化 NotesController
-> 读取 design:paramtypes = [NotesService]
-> 发现构造参数依赖 NotesService
-> 实例化 NotesService
   -> 读取 design:paramtypes = [NotesRepository]
   -> 发现构造参数依赖 NotesRepository
   -> 实例化 NotesRepository（叶子节点，无依赖）
   -> 用它构造 NotesService
-> 用 NotesService 构造 NotesController
```

所以构造函数里的依赖声明，等于声明了一条"实例化依赖链"。容器按拓扑序从叶子节点开始实例化，避免循环依赖（Nest 默认不处理循环依赖，会报错；要打破循环得用 `forwardRef`）。

provider 注册形态对应不同的注入方式：

- `{ provide: NotesService, useClass: NotesService }`：按 token 找类，`new` 出来
- `{ provide: 'CONFIG', useValue: {...} }`：直接给现成值，注入处用 `@Inject('CONFIG')` 指定 token
- `{ provide: DbClient, useFactory: (cfg: ConfigService) => new Client(cfg.url), inject: [ConfigService] }`：工厂构造，`inject` 声明工厂自身的依赖

测试里的替身就是这个机制的直接应用：

```ts
const moduleRef = await Test.createTestingModule({
  controllers: [NotesController],
  providers: [
    NotesService,
    { provide: NotesRepository, useValue: { findAll: jest.fn() } }, // mock 替身
  ],
}).compile();

const controller = moduleRef.get(NotesController);
```

容器看到 `NotesService` 依赖 `NotesRepository`，但它注册的是个现成 mock 对象，于是直接注入这个对象。和 FastAPI 的 `app.dependency_overrides[get_db] = lambda: ...` 是同一个思路：上层 service/controller 不变，底层依赖被换掉。

provider 默认是单例（整个应用一个实例）。可改作用域：

- `Scope.DEFAULT`（默认）：单例，应用级
- `Scope.REQUEST`：每个 HTTP 请求新建一个实例（注入链上相关 provider 也会变成请求级，代价大）
- `Scope.TRANSIENT`：每次注入都新建

请求级 provider 是性能陷阱——它会让整条注入链都按请求重建，非必要不用。

## 5.3 模块系统与依赖扫描

Nest 启动时不是逐个看文件，而是从根模块出发，沿着 `imports` 递归扫描，构建出一张"模块图"。

`@Module()` 的四个属性定义了一个模块的边界：

- `providers`：本模块内部用的 provider（默认对外不可见）
- `controllers`：本模块的控制器
- `imports`：依赖哪些其它模块
- `exports`：把哪些 provider 暴露给导入本模块的其它模块

`exports` 是模块的"公共 API"。一个 provider 没写进 `exports`，别的模块就算 `imports` 了它也拿不到——这是 Nest 封装模块内部实现的方式。

扫描与实例化由 `@nestjs/core` 的几个内部类完成：

- `DependenciesScanner`：从根模块沿 `imports` 递归，收集所有模块、控制器、provider
- `Container`：维护模块图，记录每个模块注册了什么、依赖什么
- `Injector` / `InstanceLoader`：按拓扑顺序实例化所有 provider 和 controller

```text
NestFactory.create(AppModule)
  -> DependenciesScanner 扫描 imports 树
  -> Container 建立模块图（每个模块的 providers / controllers / exports / imports）
  -> InstanceLoader 按拓扑序实例化
     -> 叶子 provider 先建，依赖它们的后建
  -> 所有 controller / provider 就绪
  -> 路由表从 controller 的 @Get/@Post 元数据生成
  -> app.listen() 开始接请求
```

路由表的来源也是元数据：`@Controller('notes')` + `@Get(':id')` 在定义阶段把 `{ method: 'GET', path: 'notes/:id', handlerName }` 写进控制器元数据，Nest 启动时把这些注册到底层 Express/Fastify。

全局模块：`@Global()` 装饰的模块一旦被导入，其 `providers` 全应用可见，不用每个模块重复 `imports`。`ConfigModule.forRoot({ isGlobal: true })` 就是这个用途。

## 5.4 请求生命周期

一个请求进来后，Nest 构件的执行顺序是固定的。这是 Nest 最需要记的一张图：

```text
请求进入
-> 1. Middleware              （能拿 req/res/next，能提前结束）
-> 2. Guard                    （鉴权，false 即拦截）
-> 3. Interceptor（前置）       （方法执行前）
-> 4. Pipe                     （参数转换 / 校验）
-> 5. Controller 方法          （业务，调用 service）
-> 6. Interceptor（后置）       （能改返回值）
-> 响应返回
```

如果以上任何一步抛出异常，流程跳到：

```text
-> Exception Filter           （按 @Catch 匹配的过滤器接住，转成响应）
```

几个容易踩错的顺序点：

- **Guard 在 Interceptor 前面**：拦截器的前置逻辑即使写了，也跑在鉴权之后——没权限的人根本到不了拦截器。
- **Pipe 在方法前**：参数校验失败时（`ValidationPipe` 抛 400），方法体根本不执行。这点和 FastAPI 一致：校验通过才进函数。
- **Interceptor 包裹方法**：拦截器同时有"前置"和"后置"两段，`next.handle()` 之前是前置，`.pipe(...)` 里的 `tap`/`map` 是后置。异常过滤器能接住方法抛出的异常，但默认接不住拦截器后置里抛的（除非过滤器明确 `@Catch()`）。
- **Middleware 不在 DI 主链里能感知的范围**：中间件能操作原始 `res` 直接 `send`，而拦截器不能；反过来中间件拿不到方法返回值。

构件对应的"职责边界"：

| 构件                | 能否改返回值 | 能否提前结束请求 | 典型用途           |
| ------------------- | ------------ | ---------------- | ------------------ |
| Middleware          | 否           | 能（直接 send）  | 日志、CORS、trace  |
| Guard               | 否           | 能（返回 false） | 鉴权               |
| Interceptor         | 能           | 否               | 日志、缓存、响应包装 |
| Pipe                | 否           | 能（抛异常）     | 校验、类型转换     |
| Exception Filter    | 否（只改异常响应） | 否         | 统一错误响应       |

## 5.5 异常处理机制

Nest 有一层内置的全局异常处理。流程是：业务代码抛异常 -> 框架捕获 -> 找匹配的过滤器 -> 没有就用内置处理 -> 转响应。

近似伪代码：

```ts
try {
  response = run(handler, pipes, interceptors, ...);
} catch (e) {
  for (const filter of filtersFromOutsideIn) {
    if (filter.catches(e)) return filter.handle(e);
  }
  // 兜底：HttpException 走默认映射，其它统一 500
}
```

两层：

- 内置层：`HttpException` 及其子类（`BadRequestException`、`UnauthorizedException`、`NotFoundException`...）会被映射成 `{ statusCode, message, error }`。非 `HttpException` 的异常默认变 500。
- 自定义层：`@Catch(SomeError)` 的过滤器按"从最具体到最通用"的顺序匹配，先匹配到的处理。

实际意义：

- 业务里抛语义化异常（`throw new NotFoundException(...)`）
- HTTP 层统一接住，响应结构保持一致
- 想改默认结构，就注册全局自定义过滤器

```ts
// main.ts
app.useGlobalFilters(new AllExceptionsFilter());
```

## 5.6 应用生命周期

应用除了处理请求，还有启动和关闭阶段。Nest 通过一组生命周期钩子接口暴露这些时机。

按顺序：

```text
1. 所有模块实例化完成
2. onModuleInit()        —— 实现 OnModuleInit 的 provider 在此被调用
3. onApplicationBootstrap() —— 实现 OnApplicationBootstrap 的 provider 被调用
4. app.listen()，开始接请求
...
5. 收到关闭信号
6. onModuleDestroy()     —— 实现 OnModuleDestroy 的 provider 被调用
7. onApplicationShutdown()
```

典型用途：

- `onModuleInit`：建立数据库连接、预热缓存
- `onApplicationBootstrap`：订阅消息队列、启动定时任务（此时所有模块都就绪了）
- `onModuleDestroy` / `onApplicationShutdown`：关闭连接池、清理资源

关闭钩子默认不监听系统信号，需要显式开启：

```ts
app.enableShutdownHooks(); // 监听 SIGINT/SIGTERM，触发上面的 destroy 钩子
```

## 5.7 装饰器的废弃语法与 TypeScript 版本锁

[[#5.1 装饰器元数据机制|5.1]] 建立的整套机制，踩在 `tsconfig` 的两个 flag 上，而这两个 flag 正在被 TypeScript 废弃。这是 Nest 最大的技术债，也直接决定了"跑 Nest 项目要锁 TS 版本"。

**踩的两个 flag：**

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "experimentalDecorators": true,   // 旧版装饰器规范（TC39 Stage 2，已被推翻重做）
    "emitDecoratorMetadata": true     // 把类型信息写进元数据；只对旧装饰器有效
  }
}
```

- `experimentalDecorators` 实现的是**旧版装饰器规范**，该规范当年只走到 TC39 Stage 2 就被推翻重做。新装饰器提案后来到 Stage 3，TypeScript 5.0 已支持。
- `emitDecoratorMetadata` 自动把 `design:paramtypes` 等写进元数据——这正是 Nest DI 按类型注入的数据来源（见 [[#5.1 装饰器元数据机制|5.1]]），且**只对旧装饰器有效**。

**为什么 Nest 搬不动（两个硬阻塞）：**

1. **设计期元数据缺口**：新 Stage 3 装饰器不 emit 元数据，而 Nest DI 靠它。官方阻塞在 [microsoft/TypeScript#57533](https://github.com/microsoft/TypeScript/issues/57533)。
2. **Stage 3 没有参数装饰器**：Nest 的 `@Body()`、`@Param()`、`@Query()` 全是**参数装饰器**，而新规范**故意砍掉了参数装饰器**。这意味着 Nest 要迁，不只是等元数据，而是整个取参模型都得重设计。

Nest 官方在 [nestjs/nest#5030](https://github.com/nestjs/nest/issues/5030) 跟踪此事，**没有迁移时间表**——因为语言层还没给出路。

**TS 版本现实（实测）：**

| TS 版本           | 两个 flag 的状态                      | Nest                                            |
| --------------- | -------------------------------- | ----------------------------------------------- |
| 5.x             | 正常，无警告                           | ✅ 当前主战场                                         |
| 6.0（2026-03 已发） | **正式 deprecated**，编译有警告          | ⚠️ 能跑，tsconfig 要加 `"ignoreDeprecations": "6.0"` |
| 7.0（RC，Go 原生重写） | **硬移除**（`ignoreDeprecations` 失效） | ❌ 跑不了                                           |

实测 `@nestjs/cli` 当前 peerDependency pin 的是 **`typescript: 5.9.3`**——Nest 连 TS 6 都还没跟上，而 TS 当前稳定版已是 6.0.3。所以**约束现在就生效**：跑 Nest 锁在 TS 5.9.x，既低于稳定版（6.0.3），更够不着 7.0。

**Nest 大概率的对策（推断）：**

- 短期：**pin 死 TS 6.x** + `ignoreDeprecations` 顶一阵，能买好几年。
- 技术出路：**编译期 transform（SWC/tsc 插件）注入元数据**，绕开 `emitDecoratorMetadata`——最可能的逃生路径，社区已有这类方案。
- 远期：真迁移（重设计参数解析），遥遥无期。

**实操约束（跑 Nest 必须接受）：**

- 跟着 Nest 走，**TS 锁 5.9.x**，别自己升 6/7。
- tsconfig 保持 `experimentalDecorators: true` + `emitDecoratorMetadata: true`（上 TS 6 时再加 `ignoreDeprecations: "6.0"`）。
- TS 7：Nest 官方宣布支持前**别碰**。

一句话：这不是"Nest 要崩"，是它踩废弃语法的**账单到期日**——会靠"锁 TS 6 + transform 续命"扛过去，但现在起 TS 版本就是被它锁住的。

# 6. 工程实践

## 6.1 分层边界

- `controller` 负责 HTTP：路由、参数、状态码、响应结构
- `service` 负责业务：规则、流程编排、抛业务异常
- `repository` 负责数据访问：封装 ORM / Prisma
- `module` 负责装配：声明 providers / controllers / imports / exports
- `common/*` 负责横切：通用 guard / pipe / interceptor / filter

## 6.2 测试组织

测试至少分两类：

- 单元测试：直接构造 module，用 `useValue` 注入 mock，验证 service 业务规则
- 端到端测试：用 `supertest` 打真实接口，验证路由、校验、响应

DI 的核心价值在测试里直接兑现：替换 `repository` 为 mock，`service` 不用改一行代码就能测。机制见 [[#5.2 依赖注入机制|5.2]]。

## 6.3 常见反模式

- 在控制器里写业务规则或直接操作数据库（控制器应是协议层薄壳）
- 用了 DTO 但没挂 `ValidationPipe`，以为字段校验会自动生效
- 把所有 provider 都设成 `Scope.REQUEST`，引入不必要的请求级实例化开销
- 模块不导出 `exports` 却抱怨跨模块注入不到；或把内部 provider 全导出，破坏封装
- 在拦截器里用同步逻辑改流，忘了返回 `Observable`，导致响应被吞
- 只有手测接口，没有 `supertest` 端到端测试，路由层行为无保障
- tsconfig 没开 `emitDecoratorMetadata`，DI 拿不到构造参数类型，注入直接失败

# 7. 装饰器：JS 提案、TS 演进与 NestJS 源码视角

这一章把"装饰器"从根上讲透，串起前面散落的三处：[[#5.1 装饰器元数据机制|5.1]]（元数据怎么存）、[[#5.7 装饰器的废弃语法与 TypeScript 版本锁|5.7]]（为什么被锁版本）、以及"reflect-metadata 是 JS 的"那个追问（运行时是 JS，类型信息是 TS 给的）。读完这章你会明白：Nest 为什么踩在一套"已废弃"的语法上、它源码里装饰器到底干了什么、以及为什么切不到新语法。

## 7.1 装饰器到底是什么

装饰器是**语法糖，本质是一个函数**。它不是魔法——在类/方法/参数被定义的那一刻，既运行时调用这个函数，把"标签"贴到目标上。Legacy 写法下：

```ts
@injectable()
class NotesService {}

// 等价于：
class NotesService {}
NotesService = injectable()(NotesService);   // 装饰器就是个接收类、返回（可能改造过的）类的函数
```

关键认知：**装饰器本身只是"在定义时被调用的函数"**。它做什么，完全取决于这个函数内部怎么写——Nest 的装饰器内部就是"往类上贴 metadata"（见 [[#7.4 NestJS 用哪套 + 源码层面|7.4]]）。另外，装饰器**只能贴在类与类成员（方法/属性/参数）上，贴不到独立函数**。

## 7.2 JS 的两套提案：Legacy 与 Stage 3

装饰器是 ECMAScript 提案（TC39 标准化流程），经历过一次"推翻重做"，于是有了**两套不兼容的规范**。

### 7.2.1 Legacy（早期 Stage 2）

2014–2016 年的早期提案（Yehuda Katz 等），**descriptor 风格**。

**方法/属性装饰器**——拿到方法的属性描述符 `descriptor`，直接改它：

```ts
function log(target, propertyKey, descriptor: PropertyDescriptor) {
  const orig = descriptor.value;                  // descriptor.value 就是原方法
  descriptor.value = function (...args) {
    console.log(`调用 ${propertyKey}`);           // 前置逻辑
    return orig.apply(this, args);                // 再调原方法（apply 保住 this）
  };
}

class NotesService {
  @log                                            // 等价于：log(类原型, 'findAll', 方法描述符)
  findAll() { return [...]; }
}
```

这里两个参数要拎清：

- `target` 是**方法所在的那个对象**：实例方法挂在类的原型（`NotesService.prototype`）上，所以 `target` 就是类原型；静态方法（`static`）挂在类本身，`target` 是 `NotesService`。
- `descriptor` 是**这个方法（被装饰的那个成员）自己的属性描述符**——也就是 `Object.getOwnPropertyDescriptor(NotesService.prototype, 'findAll')` 返回的那个对象（传给 `log` 的第 3 个参数就是它）；`descriptor.value` 就是那个函数本身（可读可改）。`log` 正是靠改 `descriptor.value` 来“包一层”。

`descriptor` 长这样（就是上面说的那个方法描述符的结构）：

```js
{
  value: [Function: findAll],   // 那个方法函数本身
  writable: true,               // 能否重新赋值
  enumerable: false,            // 是否出现在 for...in
  configurable: true,           // 能否删除 / 改配置
}
```

**参数装饰器**——拿到参数的位置 `index`。它和上面的方法装饰器有个关键不同：**用法带括号、带参数**（`@Inject('DB')`），所以它是个**工厂**——返回一个函数。

`@Inject('DB')` 贴在参数上时，分两步执行：

```ts
class Foo {
  constructor(@Inject('DB') db: Db, logger: Logger) {}
  //          ↑ 第 1 步：先执行 Inject('DB')，返回内层函数
  //                        ↑ 第 2 步：用内层函数去装饰“第 0 个参数”（db）
}
```

所以 `Inject` 要套两层——外层收 `token`，返回的内层才是真装饰器：

```ts
function Inject(token: string) {
  return (target, propertyKey, parameterIndex) => {   // ← 这才是真装饰器
    // target = Foo（构造函数参数的 target 是类本身）
    // propertyKey = undefined（构造函数参数没有具体方法名）
    // parameterIndex = 0（db 是第 0 个参数；logger 会是 1）
    Reflect.defineMetadata('inject:' + parameterIndex, token, target);
    // ↑ 记一条元数据：“第 0 个参数要注入 token='DB'”
  };
}
```

三个参数：

- `target` —— 参数所在的方法 / 类。**构造函数参数**时是类本身（`Foo`）；**普通方法参数**时是类的原型。
- `propertyKey` —— 属于哪个方法。构造函数参数时没有具体方法名（`undefined`）。
- `parameterIndex` —— 这个参数排第几个，从 0 数。

**它到底做了什么？** 关键：装饰器在**类定义时**就跑，那时**还没有实例、参数还没有值**——它根本拿不到运行时 `db` 是什么。它唯一能做的是**记一条元数据**（“第 0 个参数要注入 'DB'”），以后 DI 容器实例化 `Foo` 时读到这条记录，把对的依赖塞进去。

连回 Nest：`@Body()` / `@Param('id')` / `@Query()` 就是参数装饰器——记下“第 N 个参数，从请求的 body / path / query 取值”，路由时 Nest 据此从请求里提取。

特点：
 
- 能**改 descriptor**（mutation 风格）。
- **支持参数装饰器** `(target, key, index)`。
- 需要传参的装饰器用**工厂**（`@Xxx(...)` 带括号），不传参的直接用（`@log` 不带括号）。
- 配 `reflect-metadata` + `emitDecoratorMetadata` 拿类型元数据。

这套卡在 Stage 2 后被推翻重做，但 TS（1.5 起）和 Babel 早已实现，**Angular / Nest / TypeORM / MobX 全建在上面**——Legacy 装饰器因此成了事实标准，尽管它从未正式进入语言。

### 7.2.2 新版（Stage 3）

2022 年 3 月达到 Stage 3 的新提案（Daniel Ehrenberg 等），**context 风格**：

```ts
function log(value, context: DecoratorContext) {
  // context = { kind: 'method'|'class'|..., name, addInitializer, ... }
  // 不再改 descriptor，而是返回一个"替换"，或用 context.addInitializer 注册初始化逻辑
}
```

特点：

- 不改 descriptor，改用**返回替换 / `addInitializer`**（更安全、更可组合）。
- **砍掉了参数装饰器**——这是和 Nest 最相关的差异。
- **没有内置的类型元数据机制**（没有 `design:paramtypes` 的等价物）。

### 7.2.3 对比

| 维度 | Legacy（Stage 2） | 新版（Stage 3） |
|---|---|---|
| 签名 | `(target, key?, descriptor?)` | `(value, context)` |
| 改造方式 | 改 descriptor（mutation） | 返回替换 / `addInitializer` |
| **参数装饰器** | ✅ 有 `(target, key, index)` | ❌ **没有** |
| **类型元数据** | ✅ `emitDecoratorMetadata` 发 `design:paramtypes` | ❌ 无内置机制 |
| 谁在用 | Nest / TypeORM / Angular / MobX | 新项目、新库（官方推荐） |

一句话：**两套不兼容，Nest 用的是被推翻的那套（Legacy）。**

## 7.3 TypeScript 的版本演进

TS 跟着提案走，关键节点：

| TS 版本 | 装饰器状态 |
|---|---|
| 1.5（2015） | 实现 Legacy，`experimentalDecorators` 开关 |
| 2019–2022 | 提案卡住、推翻、重写 |
| Stage 3 达成（2022.03） | 提案层面定了新规范 |
| **5.0（2023.03）** | **实现 Stage 3**；两套并存，`experimentalDecorators` 开关决定用哪套（关掉=新，开着=Legacy） |
| **6.0（当前 6.0.3）** | `experimentalDecorators` + `emitDecoratorMetadata` **deprecated**；`"ignoreDeprecations": "6.0"` 抑制告警 |
| **7.0（未发布）** | **将完全移除**这两项（官方 TS 6.0 公告原话："TypeScript 7.0 [will remove them entirely]"） |
| Go 原生编译器（2025.03 宣布） | 7.0 的承载——用 Go 重写、提速 10×，顺带移除 legacy 装饰器 |

关键认知：**两套装饰器在 TS 5.0+ 可以并存，但语义完全不同。** 你 `tsconfig` 里 `experimentalDecorators` 开不开，决定了 TS 用哪套语义去编译同一份 `@xxx` 代码——这也是为什么这个"开关"这么重要。

## 7.4 NestJS 用哪套 + 源码层面

### 7.4.1 Nest 踩的是 Legacy

Nest 的 `tsconfig` 三件套（`experimentalDecorators` + `emitDecoratorMetadata` + 运行时 `import 'reflect-metadata'`），并且 `@nestjs/cli` 把 `typescript` **pin 在 5.9.x**——直接锁死在 Legacy + 5.x 上：不上 6.0（避免 deprecation 噪音），更不可能上 7.0（直接编译失败）。

### 7.4.2 Nest 的装饰器源码在做什么

**Nest 的装饰器，本质就是"给类贴 metadata 标签的普通函数"**。去掉错误处理后，`@Module()` / `@Controller()` / `@Injectable()` 长这样（代表性源码，键名做了简化）：

```ts
// @Module()：把传入的 { providers, controllers, imports, exports } 整个贴到类上
export const Module = (metadata: ModuleMetadata): ClassDecorator =>
  (target) => {
    Reflect.defineMetadata('nest:module', metadata, target);
  };

// @Controller()：贴两个标签——"我是 controller" + 路由前缀
export const Controller = (prefix = ''): ClassDecorator =>
  (target) => {
    Reflect.defineMetadata('nest:controller', true, target);
    Reflect.defineMetadata('nest:path', prefix, target);
  };

// @Injectable()：贴"我是可注入 provider"的标签
export const Injectable = (): ClassDecorator =>
  (target) => {
    Reflect.defineMetadata('nest:injectable', true, target);
  };
```

看到没——**这些装饰器不实现任何业务逻辑，只是 `Reflect.defineMetadata` 往类上贴键值对**。真正的逻辑在 Nest 启动时：

- **扫描器**遍历所有 `@Module` 标记的类，读 `Reflect.getMetadata('nest:module', cls)` 拿到 providers/controllers/imports/exports，构建模块图；
- **DI 容器**据此知道要实例化哪些 provider、按什么顺序注入。

参数装饰器（`@Body` / `@Param` / `@Query`）同理，只是标签贴在"第几个参数"上，路由匹配后据此从请求里提取：

```ts
export const Body = () =>
  (target, propertyKey, parameterIndex) => {       // ← 参数装饰器签名：(target, key, index)
    Reflect.defineMetadata('nest:param', { index: parameterIndex, type: 'body' }, target, propertyKey);
  };
```

### 7.4.3 DI 的来源：design:paramtypes

上面 `@Injectable()` 只贴了"我是可注入的"。那容器怎么知道 `NotesService` 构造时要注入哪些依赖？**靠的是 TS 编译器塞进来的 `design:paramtypes`**（详见 [[#5.1 装饰器元数据机制|5.1]] 和"reflect-metadata 是 JS"那条追问）：

```ts
@Injectable()
class NotesService {
  constructor(private repo: NotesRepository, private logger: Logger) {}
}
// emitDecoratorMetadata 让 TS 编译出：
//   __metadata("design:paramtypes", [NotesRepository, Logger])
// → Reflect.defineMetadata 把 [NotesRepository, Logger] 贴到 NotesService 上
```

Nest 容器读这个数组，递归地把 `NotesRepository`、`Logger` 也实例化并注入。**这个类型数组只有 TS 编译器能产生**（plain JS 里类型标注不存在），`reflect-metadata` 只是仓库——这正是上一条追问的答案。

### 7.4.4 为什么切不到 Stage 3

Nest 想从 Legacy 迁到新标准，撞上两堵硬墙：

1. **参数装饰器没了**。Nest 的 `@Body()` / `@Param()` / `@Query()` / `@Headers()` **全是参数装饰器**（签名 `(target, key, index)`）。Stage 3 砍掉了参数装饰器 → 整套参数提取机制失效。这是最致命的。
2. **类型元数据没了**。Stage 3 没有 `design:paramtypes` 的等价物 → DI 按类型注入的来源直接断掉。

这两点对应社区追踪的两个 issue：microsoft/TypeScript#57533（新装饰器的设计期类型元数据缺口）、nestjs/nest#5030（Nest 跟踪迁移）。**结论：Nest 无法"轻量"迁移——要么等 TS 给新装饰器补类型元数据（短期不会），要么 Nest 自己写编译期 transform 来注入（大改）。**

## 7.5 Nest 的处境与出路

把上面串起来：

- **Nest 把地基焊在了 Legacy Stage 2 装饰器 + `emitDecoratorMetadata` 上**——这套是"被推翻、已废弃"的语法。
- TS 6.0 已 deprecated → Nest **必须锁 TS 5.9.x**（加 `ignoreDeprecations` 才能上 6.0）。
- TS 7.0 要移除 → 在那之前 Nest **必须**有出路，最可能是：**写一个编译期 transform（类似 SWC/tsc 插件），在 Stage 3 装饰器之上自己注入 `design:paramtypes` 等元数据**，绕开"新装饰器无类型元数据"的缺口。这是大工程，短期不会落地。

一个旁证：**选 Zod 能绕开这整套问题**——Zod 是纯 TS、零装饰器（见 [[#4.4 Zod 校验方案|4.4]]），它的 schema 不依赖 `experimentalDecorators` 也不依赖 `design:paramtypes`。所以"用 Zod"不只是换个校验库，而是**把一部分逻辑从"装饰器地基"上挪走**，降低未来被 TS 7 卡住的面（但 Nest 本身的 `@Module`/`@Controller`/`@Injectable` 仍是装饰器，这部分短期无解）。

> 一句话：**Nest 踩在 Legacy 装饰器这个"已废弃地基"上，短期靠锁 TS 5.9.x + ignoreDeprecations 续命，长期得靠编译期 transform 自行注入元数据。这不是 Nest 的 bug，而是它"Spring 式装饰器架构"与"JS 装饰器标准化走了另一条路"的结构性冲突。**
