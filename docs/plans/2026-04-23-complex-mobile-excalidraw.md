# Complex Mobile Excalidraw Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by task.

**Goal:** 将移动端结构验证图升级为信息密集型复杂流程图，包含判断、回退、分组、角色与产出。

**Architecture:** 保持手机端纵向主阅读方向，在每个阶段内部放入小型分组和判断节点。主链路仍从上到下，复杂度通过局部横向短分支、回退标注、角色标签和产出清单体现，避免大跨度交叉线。

**Tech Stack:** Obsidian Excalidraw `.excalidraw.md`、Excalidraw JSON、Node.js 生成文件

---

### Task 1: 重构复杂移动端图

**Files:**
- Modify: `Excalidraw/Drawing 2026-04-02 16.52.59.refactored-ai.excalidraw.md`
- Create: `docs/plans/2026-04-23-complex-mobile-excalidraw.md`

**Step 1: 定义阶段**

- 输入分流
- 需求澄清
- 方案设计
- 并行实施
- 质量验证
- 沉淀发布

**Step 2: 添加复杂结构**

- 判断节点：输入类型、信息是否足够、方案是否通过、测试是否通过、评审是否通过
- 回退路径：补充信息、重做方案、修复实现、返工评审
- 分组容器：输入层、协作层、执行层、质量层、沉淀层
- 角色层：Human、AI、Agent、Reviewer

**Step 3: 生成图形**

- 单列主链
- 局部短横向分支
- 小卡片密集排列
- 关键回退用红色虚线说明，不做长距离交叉

**Step 4: 校验**

- JSON 可解析
- 主流程箭头保持向下
- 横向箭头只出现在局部分组内部
