---
published: "true"
title: obsidian最佳实践
---

# 完整 Frontmatter（非常实用）

建议你统一用这个结构：
```

---  
title: 什么是RAG  
published: true  
tags: [AI, LLM, RAG]  
created: 2026-03-06  
updated: 2026-03-06  
summary: RAG技术介绍  
---  

# 这是标题
这个文章
```
  
  在obsidian中输入：
  ```
  ---
  ```
它会自动提示。你也可以装插件：

```
- Obsidian Linter
- MetaEdit
```

可以 **自动补全 frontmatter**。

### 4.2 Vault 组织结构设计
推荐采用「PARA 法则」组织笔记（适用于个人和工作）：
```
MyVault/ 
├── Projects/ # 项目（如「Linux 学习计划」） 
├── Areas/ # 领域（如「编程」「工具」） 
├── Resources/ # 资源（如「书籍笔记」「教程摘录」） 
└── Archives/ # 归档（过期项目、旧笔记）
```
### 4.3 版本控制：用 Git 管理笔记

Obsidian 笔记是本地文件，适合用 Git 进行版本控制（防止误删、追踪修改）。

**步骤**：

1. 进入 Vault 目录初始化 Git 仓库：
```
cd ~/MyVaultgit initgit add .git commit -m "Initial commit: 初始化知识库"
```
2. 添加 `.gitignore` 文件（忽略 Obsidian 缓存和配置）：
```
.obsidian/workspace.json  # 工作区配置（无需同步）
.obsidian/cache/          # 缓存文件
.obsidian/plugins/        # 插件（可选，若插件通过社区安装）EOF
```
3. 定期提交更新：
```
git add .git commit -m "Add: Linux 命令笔记更新" 
```

## 5. AI Skill 与 Obsidian 工作流

### 5.1 记录原则

- 和 Obsidian 使用方式、文件格式、知识库组织方式相关的内容，统一记录在这篇 `obsidian最佳实践`
- 外部下载的 skill 不单独放进 `Areas/Harness Engineering/skills/` 下展开维护，只在实用清单里登记
- `Areas/Harness Engineering/skills/` 更适合放自己编写、自己维护、需要持续迭代的 skill

### 5.2 `kepano/obsidian-skills`

仓库地址：<https://github.com/kepano/obsidian-skills>

这是一个专门面向 Obsidian 工作流的 skills 集合，主要价值不是提升文笔，而是让 AI agent 更懂 Obsidian 的文件格式和知识库操作方式。

包含的主要 skill：

- `obsidian-markdown`：写 Obsidian Flavored Markdown，包括 properties、wikilink、embed、callout、tag、脚注、Mermaid 等
- `obsidian-bases`：创建和维护 Obsidian Bases，用属性、筛选器和视图把笔记变成数据库
- `json-canvas`：创建和编辑 Obsidian `.canvas` 文件，适合做知识地图、项目图谱、赛道关系图
- `obsidian-cli`：通过 Obsidian CLI 读写笔记、搜索、追加 daily note、操作 properties
- `defuddle`：把网页正文抽取成干净 Markdown，适合把外部文章整理进知识库

### 5.3 对当前知识库的价值

- `obsidian-markdown`：适合提升所有笔记的 Obsidian 兼容性
- `json-canvas`：适合做 `赛道观察`、`开源项目图谱`、`知识导航页`
- `obsidian-bases`：适合后续把项目、赛道、开源库做成可筛选数据库
- `defuddle`：适合收集网页、文章、项目介绍，并清洗成 Markdown
- `obsidian-cli`：如果本地 Obsidian CLI 配好，可以让 agent 更直接地操作 vault

### 5.4 使用边界

- 这个仓库解决的是 Obsidian 适配问题，不是通用写作方法论
- 如果目标是写 PRD、RFC、行业分析、决策文档，还需要配合专门的文档写作/分析 skill
- `json-canvas` 处理的是 Obsidian Canvas，不是 Excalidraw；Excalidraw 需要单独的 skill 或 MCP
