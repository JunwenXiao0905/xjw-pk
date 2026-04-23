# Mobile Excalidraw Structure Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 把 `Drawing 2026-04-02 16.52.59.refactored-ai.excalidraw.md` 重构成适合手机端查看的纵向单列流程图。

**Architecture:** 保留单一主链路，只验证图的层级和箭头结构，不追求业务真实性。统一卡片宽度、统一上下间距、统一纵向箭头，避免横向展开和交叉连线。

**Tech Stack:** Obsidian Excalidraw `.excalidraw.md`、Excalidraw JSON、Node.js 生成文件

---

### Task 1: 生成移动端纵向结构图

**Files:**
- Modify: `Excalidraw/Drawing 2026-04-02 16.52.59.refactored-ai.excalidraw.md`
- Create: `docs/plans/2026-04-23-mobile-excalidraw-structure.md`

**Step 1: 定义结构骨架**

- 标题
- 输入
- 规划
- 实施
- 验证
- 沉淀

**Step 2: 统一视觉约束**

- 宽度控制在手机端友好的单列范围
- 统一卡片尺寸和字体层级
- 只保留竖直主箭头

**Step 3: 重写 Excalidraw JSON**

- 用脚本生成新的 `elements`
- 保留 Obsidian `excalidraw-plugin: parsed` 包装
- 生成新的 `Text Elements`

**Step 4: 校验结果**

Run: `node` 解析 `## Drawing` 下的 JSON  
Expected: JSON 可解析，箭头数量与结构符合预期

**Step 5: 提交与推送**

```bash
git add docs/plans/2026-04-23-mobile-excalidraw-structure.md Excalidraw/Drawing\ 2026-04-02\ 16.52.59.refactored-ai.excalidraw.md
git commit -m "Simplify Excalidraw diagram for mobile layout"
git push origin main
```
