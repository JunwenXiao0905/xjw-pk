---
name: product-docs-governance
description: Use when governing product and architecture documentation in a monorepo, especially when docs need to be converged, core decisions must be fixed, or PRD, task, and architecture artifacts must stay aligned with real implementation.
---

# Product Docs Governance

面向 monorepo 的产品与架构文档治理工作流，目标不是“先铺一堆模板文档”，而是把需求、架构、决策、任务和实现持续收敛到一套足够小、能指导工程落地的文档体系里。

---

## 核心原则

- 先收敛文档体系，再展开细节
- 文档必须贴合当前工程现实，而不是生搬模板
- 优先固化关键决策，再拆实施任务
- 文档数量越少越好，但要覆盖产品、架构、决策、任务四个维度
- 新增文档必须有明确职责；没有职责就不要建

---

## When to Use

适用于以下场景：

- 开始一个新功能或新产品方向
- 需求还在演化，需要边讨论边固化
- 已经有一些文档，但内容发散、重复、相互冲突
- 需要把多轮对话沉淀成后续可继续开发的文档集
- 同时涉及产品边界、架构决策和工程实施路线

不适用于：

- 单一 bug 修复
- 只改一个 API 字段或局部实现细节
- 已经有稳定 spec，只需要按计划编码

---

## 默认文档收敛模型

默认只保留以下核心文档：

### 产品文档

- `PRD.md`
- `PRD-CHANGES.md`
- `TASK.md`

### 架构文档

- `ARCHITECTURE.md`
- `DECISIONS.md`

### 详细拆分目录

- `technical/`：用于高价值技术专题、架构拆分与实现细节说明

---

## 文档最小职责

### `PRD.md`

负责回答：

- 这是个什么产品 / 功能
- 用户是谁
- 对外形态是什么
- MVP 支持什么、不支持什么
- 验收标准是什么

### `PRD-CHANGES.md`

负责记录：

- 产品边界变化
- 协议与交互方式变化
- 范围收缩或收敛原因

### `TASK.md`

负责回答：

- 当前工程状态是什么
- 还差哪些主线闭环
- 推荐按什么阶段推进
- 关键任务、里程碑、风险和建议分工是什么

`TASK.md` 应以**工程实施视角**书写，而不是简单的需求 checklist。

### `ARCHITECTURE.md`

负责回答：

- 高层分层与职责边界
- 核心链路
- 部署与运行时拆分
- 与当前 monorepo 的落点关系

### `DECISIONS.md`

负责固化关键决策，例如：

- 对外协议
- 异步 / 同步模型
- 主后端框架
- 智能体运行时
- 数据输入策略
- 结果契约

凡是开发后不应反复来回讨论的内容，都应先收敛进 `DECISIONS.md`。

---

## 文档落点规则

不要强绑定到某一种目录结构。

优先根据现有工程现实选择以下之一：

### 方案 A：应用级文档

适合单个应用 / 产品，例如：

```text
apps/{app}/docs/
  PRD.md
  PRD-CHANGES.md
  TASK.md
  ARCHITECTURE.md
  DECISIONS.md
  technical/
```

### 方案 B：特性级文档

适合共享 feature library 或跨多个 app 的特性，例如：

```text
libs/features/{feature}/docs/
  PRD.md
  PRD-CHANGES.md
  TASK.md
  ARCHITECTURE.md
  DECISIONS.md
  technical/
```

选择原则：

- 如果是完整产品或 app，优先放 `apps/{app}/docs/`
- 如果是跨应用复用的 feature，优先放 `libs/features/{feature}/docs/`
- 如果现有项目已经有明确 docs 落点，应遵从已有结构，不另起一套平行体系

---

## 不推荐的默认做法

以下内容**不要在一开始就默认创建**：

- `UI-SPEC.md`
- `UX-DESIGN.md`
- 大量 `technical/*.md`
- 大量 API / acceptance / quality / checklist 顶层文档

只有在以下情况下才新增：

- 该主题复杂且会长期独立维护
- 主文档已经过长，拆分后更清晰
- 拆分后确实会被多人反复引用

如果某份文档只是主文档中的一个短章节，不要为了“看起来完整”单独拆文件。

---

## 推荐工作流

### Stage 1：识别当前现实

先确认：

- 当前 monorepo 已有哪些 app / lib
- 这次工作是产品级还是 feature 级
- 是否已有 docs 目录与历史文档
- 是否已有工程骨架需要对齐

产出：

- 确认文档落点
- 确认文档收敛范围

### Stage 2：收敛核心文档

优先形成或修订：

- `PRD.md`
- `ARCHITECTURE.md`
- `DECISIONS.md`
- `TASK.md`

如果已有零散文档，应将核心内容回收到这几份主文档，而不是继续叠加更多文档。

### Stage 3：必要时拆详细文档

仅当某一专题复杂度足够高时，才拆到：

- `technical/`

推荐拆分主题：

- experience layer
- control plane
- agent / intent
- data platform
- runtime
- result contract
- operations / quality

### Stage 4：实施对齐

文档必须与真实工程结构对齐，例如：

- 对应现有 `apps/` 和 `libs/`
- 对应真实运行时语言与框架
- 对应真实 API 入口、Job 模型、结果契约

不要写成“框架中立的漂亮文档”，却和仓库现实脱节。

### Stage 5：持续更新

每轮讨论或实现后，优先更新：

- `PRD-CHANGES.md`：边界与范围变化
- `DECISIONS.md`：已确认的关键决策
- `TASK.md`：当前状态、阶段和下一步
- 每完成一个关键 Commit，必须强制触发 `TASK.md` 的状态更新，禁止累计更新。

---

## 写作重点

### 产品文档重点

- 明确 MVP，而不是把远期能力都写进来
- 明确对外接口或接入方式
- 明确异步 / 同步模型
- 明确支持 / 不支持范围
- 验收标准必须可执行、可验证

### 架构文档重点

- 明确职责边界
- 明确运行时拆分
- 明确与当前代码仓现实的映射
- 明确结果交付边界和权限模型

### 任务文档重点

- 站在工程负责人视角
- 强调阶段、依赖、优先级、里程碑
- 明确建议分工与发布门槛
- 不写成泛泛的“待办事项大列表”

---

## 轻量模板

### `PRD.md` 最小结构

```markdown
# {Name} Product Requirement Document

## 1. 产品概述
## 2. 目标用户
## 3. 核心价值
## 4. 对外接入模型
## 5. 核心场景
## 6. MVP 能力
## 7. MVP 范围与非目标
## 8. 验收标准
```

### `PRD-CHANGES.md` 最小结构

```markdown
# PRD Changes

## YYYY-MM-DD

### 文档体系收敛
### 产品边界调整
### 对外协议调整
### 运行时或交付策略调整
```

### `ARCHITECTURE.md` 最小结构

```markdown
# {Name} Architecture

## 1. 架构原则
## 2. MVP 对齐范围
## 3. 逻辑分层
## 4. 核心链路
## 5. 运行时拆分
## 6. 推荐部署单元
## 7. 当前仓库映射
## 8. 文档地图
```

### `DECISIONS.md` 最小结构

```markdown
# Decisions

## D-001 ...
## D-002 ...
## D-003 ...
```

### `TASK.md` 最小结构

```markdown
# TASK

## 1. 当前共识
## 2. 当前工程快照
## 3. 总体交付目标
## 4. 推荐实施阶段
## 5. 关键任务清单
## 6. 最小里程碑
## 7. 建议分工
## 8. 发布门槛
## 9. 风险提醒
## 10. 完成定义
```

---

## `technical/` 命名建议

推荐使用小写英文文件名，按主题命名，例如：

- `experience-layer.md`
- `control-plane.md`
- `agent-and-intent.md`
- `data-platform.md`
- `spatial-runtime.md`
- `result-contract.md`
- `operations-and-quality.md`

## 触发新增拆分文档的条件

只有满足以下至少一条，才新增 `technical/` 下的详细文档：

- 主文档某章节已经明显过长
- 该主题有独立职责边界
- 后续会被多次单独引用
- 需要独立评审

否则优先把内容保留在主文档中。

---

## 常见错误

### 错误 1：先铺满模板文档

后果：

- 文档很多，但没人维护
- 信息重复，后续容易冲突

### 错误 2：文档结构脱离工程现实

后果：

- 文档好看，但无法指导实现
- 实现和文档逐渐分裂

### 错误 3：没有 `DECISIONS.md`

后果：

- 已讨论过的关键问题反复重开
- 团队难以判断哪些已经定了

### 错误 4：`TASK.md` 写成需求摘要

后果：

- 无法用于排期、分工和里程碑推进

### 错误 5：把详细实现文档过早拆出

后果：

- 维护成本高
- 主题收敛前就开始碎片化

---

## 与其他 Skills 协作

推荐协作顺序：

```text
需求 / 文档收敛
  → feature-development
实现计划
  → writing-plans
执行计划
  → executing-plans
遇到问题
  → systematic-debugging
完成前验证
  → verification-before-completion
```

如果任务重点已经变成“如何实现”，应从本 skill 切换到 `writing-plans` 或 `executing-plans`，而不是继续扩写文档。
