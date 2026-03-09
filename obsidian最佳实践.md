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