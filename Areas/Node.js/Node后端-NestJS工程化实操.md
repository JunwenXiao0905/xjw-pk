# 目录

- [[#1. 工程结构总览|1. 工程结构总览]]
  - [[#1.1 目录结构图|1.1 目录结构图]]
  - [[#1.2 NestJS 构件分布|1.2 NestJS 构件分布]]
  - [[#1.3 后端依赖图|1.3 后端依赖图]]
- [[#2. 工程目录内容|2. 工程目录内容]]
  - [[#2.1 main.ts|2.1 main.ts]]
  - [[#2.2 app.module.ts|2.2 app.module.ts]]
  - [[#2.3 controller|2.3 controller]]
  - [[#2.4 service 与 provider|2.4 service 与 provider]]
  - [[#2.5 dto|2.5 dto]]
  - [[#2.6 entity 与 ORM|2.6 entity 与 ORM]]
  - [[#2.7 测试|2.7 测试]]
- [[#3. 常用接口写法|3. 常用接口写法]]
  - [[#3.1 控制器与路由|3.1 控制器与路由]]
  - [[#3.2 路径参数、查询参数、请求体|3.2 路径参数、查询参数、请求体]]
  - [[#3.3 DTO 与校验|3.3 DTO 与校验]]
    - [[#3.3.1 用 Zod 替代 class-validator（及库选型）|3.3.1 用 Zod 替代 class-validator（及库选型）]]
  - [[#3.4 Providers 与依赖注入|3.4 Providers 与依赖注入]]
  - [[#3.5 Guard 守卫|3.5 Guard 守卫]]
  - [[#3.6 Pipe 管道|3.6 Pipe 管道]]
  - [[#3.7 Interceptor 拦截器|3.7 Interceptor 拦截器]]
  - [[#3.8 Exception Filter 异常过滤器|3.8 Exception Filter 异常过滤器]]
  - [[#3.9 Middleware 中间件|3.9 Middleware 中间件]]
- [[#4. 原理拆解|4. 原理拆解]]
  - [[#4.1 装饰器元数据机制|4.1 装饰器元数据机制]]
  - [[#4.2 依赖注入机制|4.2 依赖注入机制]]
  - [[#4.3 模块系统与依赖扫描|4.3 模块系统与依赖扫描]]
  - [[#4.4 请求生命周期|4.4 请求生命周期]]
  - [[#4.5 异常处理机制|4.5 异常处理机制]]
  - [[#4.6 应用生命周期|4.6 应用生命周期]]
  - [[#4.7 装饰器的废弃语法与 TypeScript 版本锁|4.7 装饰器的废弃语法与 TypeScript 版本锁]]
- [[#5. 工程实践|5. 工程实践]]
  - [[#5.1 分层边界|5.1 分层边界]]
  - [[#5.2 测试组织|5.2 测试组织]]
  - [[#5.3 常见反模式|5.3 常见反模式]]

# 1. 工程结构总览

## 1.1 目录结构图

```text
src/
├── main.ts                       # 应用入口：创建 Nest app、注册全局管道/过滤器、监听端口
├── app.module.ts                 # 根模块：装配所有子模块
├── app.controller.ts             # （可选）根控制器示例
├── app.service.ts                # （可选）根 provider 示例
│
├── common/                       # 横切代码
│   ├── filters/                    # 全局/局部异常过滤器
│   ├── interceptors/               # 日志、缓存、响应转换等拦截器
│   ├── pipes/                      # 自定义校验管道
│   ├── guards/                     # 通用守卫（鉴权）
│   └── decorators/                 # 自定义参数/方法装饰器
│
├── config/                       # 配置：@nestjs/config 读 .env
│   └── configuration.ts
│
└── modules/                      # 按业务域组织
    └── notes/
        ├── notes.module.ts          # 模块声明：providers / controllers / imports / exports
        ├── notes.controller.ts      # HTTP 层：路由、参数、状态码
        ├── notes.service.ts         # 业务逻辑层（被 @Injectable 标注的 provider）
        ├── dto/                     # 请求体 / 响应体类型
        │   ├── create-note.dto.ts
        │   └── update-note.dto.ts
        └── entities/                # ORM 实体
            └── note.entity.ts

test/                              # 端到端测试
└── notes.e2e-spec.ts
```

这个结构的核心和 FastAPI 一致：按业务域组织模块，把共性基础设施上提到 `common/` 与 `config/`，根模块只负责装配。

Nest 的目录约定比 FastAPI 更"硬"——`nest g resource notes` 这样的脚手架命令会直接按 `module / controller / service / dto / entity` 的固定模板生成文件，所以工程结构通常高度统一。

## 1.2 NestJS 构件分布

NestJS 把后端拆成一组可装配的"构件"，几乎每一个都对应一个装饰器：

```text
应用对象
├── @Module()                    # 模块：声明一组 providers / controllers / imports / exports
├── @Controller()                # 控制器：聚合一组路由
└── @Injectable()                # provider 标记：可被 DI 容器管理的类

路由与参数
├── @Get @Post @Put @Patch @Delete   # 路由处理器
├── @Param @Query @Body            # 取路径参数 / 查询参数 / 请求体
├── @Headers @Ip @Session          # 取协议层信息
└── @Req @Res                      # 原始 Express / Fastify 对象

横切构件（按请求生命周期顺序）
├── Middleware                    # 中间件：最外层，能拿到 Request/Response
├── Guard                         # 守卫：决定请求是否被允许进入
├── Interceptor                   # 拦截器：方法执行前后都能介入
├── Pipe                          # 管道：参数转换或校验
└── Exception Filter              # 异常过滤器：异常到响应的映射

异常与响应
├── HttpException 及其子类        # 内置异常：BadRequestException、NotFoundException 等
├── @Catch()                      # 自定义异常过滤器的作用范围
└── @Render()                     # 模板渲染（SSR 场景）
```

这些构件的关系压成一句：

```text
平台适配器(Express/Fastify) -> Nest app -> Module -> Controller -> Guard -> Interceptor -> Pipe -> Service
```

## 1.3 后端依赖图

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

# 2. 工程目录内容

## 2.1 `main.ts`

`main.ts` 是应用装配层，不是业务实现层。

它主要负责：

- `NestFactory.create(AppModule)` 创建应用
- 注册全局管道（如 `ValidationPipe`）、全局过滤器、全局拦截器、全局前缀
- `app.listen(port)` 监听端口
- 可选：`enableShutdownHooks()` 启用优雅关闭

它和 HTTP 平台的关系是：

```text
浏览器 -> Express/Fastify -> Nest app(main.ts 装配出的)
```

常见启动命令（Nest 默认用 npm/pnpm 脚本封装）：

```bash
pnpm start:dev      # = nest start --watch，开发热重启
node dist/main.js   # 生产环境直接跑编译产物
```

不要把业务逻辑、数据库访问、校验规则写进 `main.ts`。它的角色等同于 FastAPI 的 `main.py`。

典型内容：

```ts
// src/main.ts
import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.setGlobalPrefix('api');                       // 所有路由加 /api 前缀
  app.useGlobalPipes(
    new ValidationPipe({ whitelist: true, transform: true }),
  );

  await app.listen(3000);
}
bootstrap();
```

## 2.2 `app.module.ts`

`app.module.ts` 是根模块，是整个依赖图的入口。Nest 从这里开始扫描所有子模块。

```ts
// src/app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { NotesModule } from './modules/notes/notes.module';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }), // 全局配置
    NotesModule,
  ],
})
export class AppModule {}
```

根模块通常只做 `imports`，不放具体业务 provider。每个业务域有自己的模块，根模块把它们拼起来——这一点和 FastAPI 在 `main.py` 里集中注册 router 的作用对等，但 Nest 把"注册"显式做成了 `@Module` 的 `imports`。

## 2.3 `controller`

控制器是 HTTP 层，职责等同 FastAPI 的 `router.py`：

- 定义路由前缀（`@Controller('notes')`）
- 声明方法与 HTTP 动词（`@Get`、`@Post`...）
- 取参数（`@Param`、`@Query`、`@Body`）
- 声明状态码、响应类型
- 把工作交给 `service`

控制器本身不写业务规则，只做协议层映射。

## 2.4 `service 与 provider`

`service` 是业务逻辑层，是 Nest 里最典型的 provider。

`provider` 是 Nest 对"可被 DI 容器管理的对象"的统称，包括：

- `service`：业务逻辑
- `repository`：数据访问（封装 TypeORM / Prisma）
- `factory` / `useValue`：配置值、第三方客户端、连接池
- `guard` / `interceptor` / `pipe` / `filter`：横切构件，本身也是 provider

provider 的标记是 `@Injectable()`。它告诉 DI 容器："这个类可以实例化、可以被注入到别的类的构造函数里。"

## 2.5 `dto`

DTO（Data Transfer Object）对应 FastAPI 的 Pydantic 模型，放在 `modules/<业务>/dto/`。

一组接口的 DTO 通常分几类：

- `CreateXxxDto`：创建请求体
- `UpdateXxxDto`：更新请求体（常基于 `PartialType(CreateXxxDto)`）
- 响应类型：可用 TS 接口或 `class`，需要进 Swagger 文档时用带装饰器的 `class`

与 FastAPI 的关键区别：FastAPI 的 `BaseModel` 框架原生解析并强校验；Nest 的 DTO 是普通类，校验由 `class-validator` 装饰器驱动，**必须显式挂上 `ValidationPipe` 才会校验**，否则请求体只是被 `class-transformer` 转成一个实例（甚至直接是普通对象），字段约束全部失效。

## 2.6 `entity 与 ORM`

实体是数据库表的映射，放在 `modules/<业务>/entities/`。

- TypeORM：`@Entity()` + `@Column()` 装饰器定义表
- Prisma：实体定义在 `schema.prisma`，运行时用生成的 `PrismaClient`

`repository` 封装对实体的操作，和 FastAPI 的 `repository.py` 角色一致。

## 2.7 `测试`

Nest 自带测试工具 `@nestjs/testing`，测试分两类：

- 单元测试（`*.spec.ts`）：用 `Test.createTestingModule` 构建一个最小模块，用 `useValue` / `useFactory` 替换真实依赖（如把 service 依赖的 repository 换成 mock 对象）
- 端到端测试（`test/*.e2e-spec.ts`）：用 `NestFactory.createApplicationContext` 或 `supertest` 直接打真实 HTTP 接口

测试替身机制见 [[#4.2 依赖注入机制|4.2 依赖注入机制]]，原理和 FastAPI 的 `app.dependency_overrides` 同构。

# 3. 常用接口写法

## 3.1 控制器与路由

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

这里的 `notesService` 不是从请求里来的，而是 Nest 在实例化 `NotesController` 时通过构造函数注入的——见 [[#4.2 依赖注入机制|4.2]]。

## 3.2 路径参数、查询参数、请求体

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

## 3.3 DTO 与校验

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
- 这套校验由 `class-transformer`（转实例）+ `class-validator`（跑校验）完成，Nest 的 `ValidationPipe` 只是调用它们，机制见 [[#4.4 请求生命周期|4.4]] 中管道这一环。

DTO 的更新复用：

```ts
import { PartialType } from '@nestjs/swagger'; // 或 @nestjs/mapped-types
export class UpdateNoteDto extends PartialType(CreateNoteDto) {}
```

### 3.3.1 用 Zod 替代 class-validator（及库选型）

class-validator 是 Nest 默认的校验方案（装饰器驱动，见上）。它有一个结构不同的替代：**Zod**。换不换是另一个话题（见 [[#4.7 装饰器的废弃语法与 TypeScript 版本锁|4.7]] 的相关性），这里只给「如果用，怎么接、选哪个库」。

**Zod 相对 class-validator 的结构性差异：**

- **schema 单源**：一个 `z.object({...})` 既是运行时校验器，又通过 `z.infer<typeof schema>` 推导出 TS 类型。class-validator 则是「校验装饰器 + 类型」两套定义。
- **纯 TS、零装饰器**：不依赖 `experimentalDecorators` / `emitDecoratorMetadata`，因此**绕开了 [[#4.7 装饰器的废弃语法与 TypeScript 版本锁|4.7]] 那条雷**。
- **跨前后端共享**：同一份 schema 可被前端直接 import（前端 `safeParse` 或喂 `zodResolver`），实现前后端同类型 + 同运行时校验。class-validator 搬到前端要带 `reflect-metadata` polyfill，且 react-hook-form 没有它的官方 resolver。

**接法一：手写 `ZodValidationPipe`（Nest 官方推荐写法，10 行）**

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
      throw new BadRequestException(result.error.flatten().fieldErrors);
    }
    return result.data; // 已校验、已转型，类型为 T
  }
}
```

```ts
// controller 里用
import { createNoteSchema } from './dto/notes.schema';
const CreateNotePipe = new ZodValidationPipe(createNoteSchema);

@Post()
create(@Body(CreateNotePipe) body: CreateNote) { /* ... */ }
```

管道机制见 [[#3.6 Pipe 管道|3.6]]。

**接法二：`nestjs-zod`（社区包，DTO 外壳 + 全局校验 + Swagger 桥）**

```ts
import { createZodDto } from 'nestjs-zod';
import { createNoteSchema } from './dto/notes.schema';
export class CreateNoteDto extends createZodDto(createNoteSchema) {}
// 然后挂全局 ZodValidationPipe，Controller 写 @Body() body: CreateNoteDto
```

**选哪个库（实测 2026-06）：**

| 指标 | `nestjs-zod`（BenLorantfy） | `@anatine/zod-nestjs` |
|---|---|---|
| 周下载 | **82 万** | 15.6 万（约 1/5） |
| GitHub stars | 1080 | — |
| open issues | 20（低） | — |
| 最近 push | 2026-06-17（活跃） | 末版 ~2025-04（停更一年多） |
| **Zod 兼容** | `^3.25 \|\| ^4.0` ✅ | `^3.20` ❌ **不支持 v4** |
| Nest 兼容 | `^10 \|\| ^11` | `^7..^11` |
| 发布可信度 | GitHub OIDC + SLSA provenance | 个人发布 |

**结论：用 Zod 就直接上 `nestjs-zod`，别碰 `@anatine/zod-nestjs`。** 前者活跃、已适配 Zod v4 + Nest 11、自带 Zod→OpenAPI 桥（补回了「换 Zod 丢 Swagger」这个最大缺点）；后者卡在 Zod v3、停更一年。

**安全边界**：即便 `nestjs-zod` 哪天停更，它也只是个薄胶水库——退回「接法一」那 10 行手写 `ZodValidationPipe` 即可，不会被绑死。这是选社区 wrapper 的前提：薄、可替换。

## 3.4 Providers 与依赖注入

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

底层是怎么从构造函数读出依赖并注入的，见 [[#4.2 依赖注入机制|4.2]]。

## 3.5 Guard 守卫

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

`Reflector` 用来读自定义装饰器写在元数据里的标记（如 `@Roles('admin')`），机制见 [[#4.1 装饰器元数据机制|4.1]]。

## 3.6 Pipe 管道

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

## 3.7 Interceptor 拦截器

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

## 3.8 Exception Filter 异常过滤器

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

## 3.9 Middleware 中间件

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

中间件 vs 拦截器：中间件能直接操作 `res`、能提前结束请求，但不能"在方法返回后再做事"；拦截器能改返回值但不能提前 send。两者职责互补，执行顺序见 [[#4.4 请求生命周期|4.4]]。

# 4. 原理拆解

## 4.1 装饰器元数据机制

Nest 的整套装配都建立在"装饰器写元数据 + 运行时读元数据"之上。这是理解 Nest 的地基。

TypeScript 装饰器本身只是函数。`@Injectable()`、`@Controller()`、`@Get()`、`@Module()` 这些装饰器被调用时，会把"这是一段元信息"通过 `Reflect.defineMetadata` 存到目标对象上。Nest 在启动时再把这些元数据读出来，据此搭出模块图、路由表、依赖关系。

`Reflect.defineMetadata(key, value, target)` 是 `reflect-metadata` 这个 polyfill 提供的，本质是把元信息挂在目标对象的隐藏属性里。TS 编译时如果开了 `emitDecoratorMetadata: true`，还会自动把构造函数参数的类型（`design:paramtypes`）、属性类型（`design:type`）一并写进元数据——这正是 DI 能"按类型注入"的来源。

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

## 4.2 依赖注入机制

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

## 4.3 模块系统与依赖扫描

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

## 4.4 请求生命周期

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

## 4.5 异常处理机制

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

## 4.6 应用生命周期

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

## 4.7 装饰器的废弃语法与 TypeScript 版本锁

[[#4.1 装饰器元数据机制|4.1]] 建立的整套机制，踩在 `tsconfig` 的两个 flag 上，而这两个 flag 正在被 TypeScript 废弃。这是 Nest 最大的技术债，也直接决定了"跑 Nest 项目要锁 TS 版本"。

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
- `emitDecoratorMetadata` 自动把 `design:paramtypes` 等写进元数据——这正是 Nest DI 按类型注入的数据来源（见 [[#4.1 装饰器元数据机制|4.1]]），且**只对旧装饰器有效**。

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

# 5. 工程实践

## 5.1 分层边界

- `controller` 负责 HTTP：路由、参数、状态码、响应结构
- `service` 负责业务：规则、流程编排、抛业务异常
- `repository` 负责数据访问：封装 ORM / Prisma
- `module` 负责装配：声明 providers / controllers / imports / exports
- `common/*` 负责横切：通用 guard / pipe / interceptor / filter

## 5.2 测试组织

测试至少分两类：

- 单元测试：直接构造 module，用 `useValue` 注入 mock，验证 service 业务规则
- 端到端测试：用 `supertest` 打真实接口，验证路由、校验、响应

DI 的核心价值在测试里直接兑现：替换 `repository` 为 mock，`service` 不用改一行代码就能测。机制见 [[#4.2 依赖注入机制|4.2]]。

## 5.3 常见反模式

- 在控制器里写业务规则或直接操作数据库（控制器应是协议层薄壳）
- 用了 DTO 但没挂 `ValidationPipe`，以为字段校验会自动生效
- 把所有 provider 都设成 `Scope.REQUEST`，引入不必要的请求级实例化开销
- 模块不导出 `exports` 却抱怨跨模块注入不到；或把内部 provider 全导出，破坏封装
- 在拦截器里用同步逻辑改流，忘了返回 `Observable`，导致响应被吞
- 只有手测接口，没有 `supertest` 端到端测试，路由层行为无保障
- tsconfig 没开 `emitDecoratorMetadata`，DI 拿不到构造参数类型，注入直接失败
