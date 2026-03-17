---
name: feature-development
description: Use when starting or continuing feature development in this Nx monorepo, especially when requirements are still vague, multiple design and implementation documents must stay aligned, or the work will span multiple sessions.
---

# Feature Development Workflow (Nx Monorepo)

Nx 单体化仓库的功能开发工作流，从模糊需求到具体实现的完整流程。

## When to Use

- 开始新功能开发
- 需求模糊需要具象化
- 跨多个会话跟踪开发进度

## Nx Monorepo 目录结构

```
libs/
├── features/
│   └── {feature-name}/
│       ├── src/                    # 源代码
│       └── docs/                   # 功能文档
│           ├── PRD.md              # 产品需求文档
│           ├── ARCHITECTURE.md     # 技术架构设计
│           ├── UI-SPEC.md          # UI 规范
│           ├── UX-DESIGN.md        # UX 设计
│           └── technical/          # 技术实现细节
│               ├── {topic-1}.md
│               └── {topic-2}.md
│
└── shared/                         # 共享资源
    └── ui/                         # 共享 UI 组件

apps/
├── {app-name}/                     # 应用
│   ├── api/                        # 后端
│   └── web/                        # 前端
```

## Workflow Stages

### Stage 1: 需求具象化

**目标**：将模糊需求转化为清晰的 PRD 文档

**步骤**：
1. 通过对话澄清用户意图
2. 识别核心用例和边缘情况
3. 定义验收标准
4. 记录技术约束

**产出**：`libs/features/{feature}/docs/PRD.md`

### Stage 2: 架构设计

**目标**：在编码前设计技术架构

**步骤**：
1. 确定涉及的 apps/libs
2. 设计数据流和状态管理
3. 规划 API 契约
4. 考虑 Nx 依赖图

**Nx 特有考虑**：
```bash
# 查看依赖图
nx graph

# 检查受影响的项目
nx affected:graph
```

**产出**：`libs/features/{feature}/docs/ARCHITECTURE.md`

### Stage 3: UI/UX 规范

**目标**：定义界面和交互规范

**产出**：
- `libs/features/{feature}/docs/UI-SPEC.md`
- `libs/features/{feature}/docs/UX-DESIGN.md`

### Stage 4: 实现规划

**目标**：拆分为可执行的任务

**Nx 命令参考**：
```bash
# 生成库
nx g @nx/react:lib {lib-name} --directory=libs/features/{feature}

# 生成组件
nx g @nx/react:component {ComponentName} --project={project}

# 运行开发服务器
nx serve {app-name}

# 运行测试
nx test {project}

# 检查受影响的项目
nx affected:test
```

### Stage 5: 增量实现

**原则**：
- 核心功能优先
- 逐步添加增强功能
- 每次重要变更后测试
- 同步更新文档

### Stage 6: 调试优化

参考 `/systematic-debugging` skill

## Document Templates

### PRD.md 模板

```markdown
# {功能名称} - 产品需求文档

## 状态
- [ ] 草稿
- [ ] 评审中
- [ ] 已确认
- [ ] 已实现

## 1. 功能概述
简要描述功能目的和价值。

## 2. 用户故事
作为 [角色]，我希望 [行为]，以便 [价值]。

### 核心场景
1. 场景一：描述
2. 场景二：描述

### 边缘场景
1. 场景一：描述

## 3. 功能需求

### 3.1 功能清单
| 优先级 | 功能点 | 描述 | 状态 |
|--------|--------|------|------|
| P0 | xxx | xxx | [ ] |
| P1 | xxx | xxx | [ ] |

### 3.2 验收标准
- [ ] 标准 1
- [ ] 标准 2

## 4. 非功能需求
- 性能要求
- 安全要求
- 兼容性要求

## 5. 范围外
明确不在本期实现的内容。

## 6. 更新日志
| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| YYYY-MM-DD | v1.0 | 初始版本 | xxx |
```

### ARCHITECTURE.md 模板

```markdown
# {功能名称} - 技术架构设计

## 状态
- [ ] 设计中
- [ ] 评审中
- [ ] 已确认
- [ ] 已实现

## 1. 架构概览
[架构图]

## 2. 模块划分

### 2.1 涉及的 Nx 项目
```
apps/{app-name}/
├── api/                    # 后端 API
│   └── src/{feature}/
│       ├── {feature}.controller.ts
│       ├── {feature}.service.ts
│       └── {feature}.dto.ts
└── web/                    # 前端
    └── src/pages/{Feature}/
        ├── {Feature}Page.tsx
        └── components/

libs/features/{feature}/    # 功能库（可选）
└── src/
    └── ...
```

### 2.2 依赖关系
```
{feature} → @nx/react
{feature} → shared/ui
{feature} → api (运行时)
```

## 3. 数据流
[数据流图]

## 4. API 设计

### 4.1 端点
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/{feature} | 获取列表 |
| POST | /api/{feature} | 创建 |

### 4.2 数据模型
```typescript
interface {Feature} {
  id: string;
  // ...
}
```

## 5. 状态管理
描述前端状态管理方案。

## 6. 技术决策记录

### 决策 1: {标题}
- **背景**：
- **决策**：
- **影响**：

## 7. 更新日志
| 日期 | 变更内容 |
|------|----------|
| YYYY-MM-DD | 初始设计 |
```

### UI-SPEC.md 模板

```markdown
# {功能名称} - UI 规范

## 状态
- [ ] 设计中
- [ ] 评审中
- [ ] 已确认

## 1. 设计系统

### 1.1 颜色
| 名称 | 色值 | 用途 |
|------|------|------|
| primary | #xxx | 主要操作 |
| accent | #xxx | 强调元素 |

### 1.2 字体
| 名称 | 大小 | 行高 | 用途 |
|------|------|------|------|
| heading | 24px | 1.2 | 标题 |
| body | 16px | 1.5 | 正文 |

### 1.3 间距
使用 Tailwind 间距系统。

## 2. 组件规范

### 2.1 {组件名}
- **用途**：
- **状态**：default, hover, active, disabled
- **尺寸**：sm, md, lg

## 3. 响应式断点
| 断点 | 宽度 | 布局 |
|------|------|------|
| mobile | < 768px | 单列 |
| tablet | 768px - 1024px | 双列 |
| desktop | > 1024px | 多列 |

## 4. 页面布局
[线框图]

## 5. 更新日志
```

### UX-DESIGN.md 模板

```markdown
# {功能名称} - UX 设计

## 状态
- [ ] 设计中
- [ ] 评审中
- [ ] 已确认

## 1. 用户旅程

### 1.1 主流程
```
进入 → 选择 → 操作 → 确认 → 完成
```

### 1.2 异常处理
| 场景 | 处理方式 |
|------|----------|
| 网络错误 | 显示重试按钮 |
| 数据为空 | 显示空状态提示 |

## 2. 交互规范

### 2.1 反馈机制
| 操作 | 反馈 |
|------|------|
| 点击按钮 | 按钮状态变化 + 加载指示器 |
| 操作成功 | Toast 提示 |
| 操作失败 | 错误提示 + 恢复建议 |

### 2.2 加载状态
- 首次加载：骨架屏
| 分页加载：底部加载指示器
| 操作中：按钮禁用 + 加载动画

### 2.3 空状态
[空状态设计]

## 3. 动效规范

### 3.1 过渡动画
| 场景 | 动画 | 时长 |
|------|------|------|
| 页面切换 | fade + slide | 300ms |
| 弹窗出现 | scale + fade | 200ms |

### 3.2 手势交互
| 手势 | 场景 | 行为 |
|------|------|------|
| 下拉 | 列表页 | 刷新 |
| 左滑 | 列表项 | 显示操作 |

## 4. 无障碍
- [ ] 键盘导航支持
- [ ] 屏幕阅读器支持
- [ ] 颜色对比度符合 WCAG AA

## 5. 更新日志
```

### technical/ 实现文档模板

```markdown
# {技术主题}

## 问题陈述
解决什么问题？

## 解决方案
高层方案描述。

## 实现细节

### 关键文件
- `path/to/file.ts` - 作用说明

### 关键代码
```typescript
// 代码片段
```

### 依赖
- 外部库
- 内部依赖

## 边缘情况
| 情况 | 处理方式 |
|------|----------|
| xxx | xxx |

## 测试要点
- [ ] 测试点 1
- [ ] 测试点 2

## 参考
- 相关文档链接
```

## 文档状态管理

每个文档在 frontmatter 中声明状态：

```yaml
---
status: draft | review | confirmed | implemented
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: x.y.z
---
```

状态流转：
```
draft → review → confirmed → implemented
  ↑__________________________|
         (需要修改时)
```

## 动态完善机制

### 会话结束时
1. 更新相关文档的状态
2. 记录本次变更内容到更新日志
3. 标注下一步待办事项

### 会话开始时
1. 读取文档状态
2. 确认上次进度
3. 继续未完成的工作

### 文档更新触发条件
- 新增功能点 → 更新 PRD.md
- 架构变更 → 更新 ARCHITECTURE.md
- UI 调整 → 更新 UI-SPEC.md
- 交互优化 → 更新 UX-DESIGN.md
- 技术实现细节 → 创建/更新 technical/*.md

## Nx 常用命令速查

```bash
# 项目管理
nx g @nx/react:app {app-name}
nx g @nx/react:lib {lib-name}
nx g @nx/nest:app {api-name}

# 代码生成
nx g component {name} --project={project}
nx g service {name} --project={project}
nx g resolver {name} --project={project}

# 开发运行
nx serve {app}
nx build {app}
nx test {project}
nx e2e {app}-e2e

# 依赖管理
nx graph
nx affected:build
nx affected:test
nx dep-graph
```

## 与其他 Skills 协作

```
需求具象化 → /feature-development (本 skill)
遇到问题   → /systematic-debugging
写实现计划 → /writing-plans
执行计划   → /executing-plans
UI 调试    → /webapp-testing
完成验证   → /verification-before-completion
```

---

## 与 OpenSpec 协作

### 工作流定位

```
┌─────────────────────────────────────────────────────────────┐
│                      开发工作流                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   阶段 1: 探索 & 规划                                        │
│   /opsx:explore ←→ /feature-development (Stage 1-3)         │
│   (探索想法)       (需求具象化 + 架构设计 + UI/UX)            │
│                          │                                  │
│                          ▼                                  │
│   阶段 2: 创建变更提案                                       │
│   /opsx:propose                                             │
│   - 读取 feature-development 文档作为 context               │
│   - 生成 proposal.md, design.md, tasks.md                   │
│                          │                                  │
│                          ▼                                  │
│   阶段 3: 实现                                              │
│   /opsx:apply                                               │
│   - 按 tasks.md 实现                                        │
│   - 实现细节记录到 technical/*.md                            │
│                          │                                  │
│                          ▼                                  │
│   阶段 4: 归档                                              │
│   /opsx:archive                                             │
│   - 更新 openspec/specs/                                    │
│   - feature docs 保持不变（长期参考）                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 文档职责分工

| 文档 | 位置 | 职责 | 生命周期 |
|------|------|------|---------|
| PRD.md | `libs/features/{feature}/docs/` | 产品需求，用户故事 | **长期存在** |
| ARCHITECTURE.md | `libs/features/{feature}/docs/` | 技术架构设计 | **长期存在** |
| UI-SPEC.md | `libs/features/{feature}/docs/` | UI 规范 | **长期存在** |
| UX-DESIGN.md | `libs/features/{feature}/docs/` | UX 设计 | **长期存在** |
| technical/*.md | `libs/features/{feature}/docs/` | 实现细节 | **长期存在** |
| proposal.md | `openspec/changes/{change}/` | 本次变更提案 | **临时** |
| design.md | `openspec/changes/{change}/` | 本次变更设计 | **临时** |
| tasks.md | `openspec/changes/{change}/` | 本次任务清单 | **临时** |

### 推荐使用场景

| 场景 | 使用方式 |
|------|---------|
| **大型新功能** | feature-development (Stage 1-3) → opsx:propose → opsx:apply → opsx:archive |
| **功能迭代** | 直接 opsx:explore → opsx:propose → opsx:apply |
| **Bug 修复** | systematic-debugging → opsx:propose (可选) → opsx:apply |
| **文档更新** | feature-development 直接更新 feature docs |

### 文档引用示例

在 openspec artifacts 中引用 feature 文档：

```markdown
# proposal.md 示例

## 背景
详见产品需求: `libs/features/user-permissions/docs/PRD.md`

## 技术方案
详见架构设计: `libs/features/user-permissions/docs/ARCHITECTURE.md`
```

### 配置 openspec/config.yaml

```yaml
schema: spec-driven

context: |
  功能文档位于 libs/features/*/docs/
  创建 artifacts 时请先读取相关功能文档作为上下文

  Tech stack: [根据项目填写]
  Monorepo: Nx

rules:
  proposal:
    - 引用相关的 feature 文档路径
    - 明确本次变更的范围边界
  tasks:
    - 实现完成后更新 technical/*.md 记录关键细节
```

### 核心原则

- **feature-development** = 功能文档的「永久家园」，记录产品视角的完整需求
- **openspec** = 变更管理的「临时工单」，追踪具体实现过程
- 两者互补：feature docs 提供上下文，openspec artifacts 驱动实现
