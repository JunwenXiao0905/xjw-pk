# 知识库发布控制说明

## 概述

通过发布控制，你可以决定哪些笔记在个人网站上公开显示，哪些保持私密。

---

## 快速开始

### 方式一：单篇文章控制

在文章顶部添加 `published` 字段：

```markdown
---
title: 我的技术博客
published: true
---

这篇文章会公开显示...
```

```markdown
---
title: 私人日记
published: false
---

这篇文章不会显示在网站上...
```

### 方式二：目录级别控制

在知识库根目录创建 `.knowledge-publish.yaml` 文件，批量控制整个目录。

---

## 发布规则优先级

从高到低：

| 优先级 | 规则 | 说明 |
|--------|------|------|
| 1 | `published: true/false` | 文件 frontmatter 中的字段，优先级最高 |
| 2 | 文件模式匹配 | 匹配 `ignorePatterns` 的文件隐藏 |
| 3 | 目录忽略 | 在 `ignoreDirs` 或以 `_` 开头的目录隐藏 |
| 4 | 公开目录 | 在 `publicDirs` 中的目录公开 |
| 5 | 默认规则 | 由 `defaultPublished` 决定 |

---

## 配置文件说明

配置文件路径：`.knowledge-publish.yaml`（放在知识库根目录）

### 字段说明

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `defaultPublished` | boolean | `true` | 默认是否公开 |
| `publicDirs` | string[] | `[]` | 强制公开的目录列表 |
| `ignoreDirs` | string[] | `[]` | 强制隐藏的目录列表 |
| `ignorePatterns` | string[] | `[]` | 隐藏的文件名模式（支持 `*` 通配符） |

---

## 常见场景

### 场景 1：默认公开，隐藏敏感目录

```yaml
defaultPublished: true

ignoreDirs:
  - drafts        # 草稿箱
  - private       # 私人笔记
  - secrets       # 敏感信息
```

### 场景 2：默认隐藏，只公开特定目录

```yaml
defaultPublished: false

publicDirs:
  - blog          # 博客文章
  - notes/public  # 公开笔记
```

### 场景 3：忽略特定文件

```yaml
ignorePatterns:
  - "README.md"       # 忽略所有 README
  - "*.draft.md"      # 忽略所有草稿文件
  - "_*"              # 忽略下划线开头的文件
```

---

## 下划线目录约定

以 `_` 开头的目录自动隐藏，无需配置：

```
知识库/
├── blog/           ✅ 公开
├── notes/          ✅ 公开
├── _drafts/        ❌ 隐藏（下划线前缀）
├── _templates/     ❌ 隐藏（下划线前缀）
└── _archive/       ❌ 隐藏（下划线前缀）
```

---

## 临时控制

即使目录被设置为公开，单篇文章仍然可以通过 frontmatter 覆盖：

```yaml
# .knowledge-publish.yaml
publicDirs:
  - blog
```

```markdown
# blog/draft.md
---
title: 还没写完
published: false   # 覆盖目录规则，保持隐藏
---

这篇博客在完成前不会公开...
```

---

## 资源文件

图片等资源文件遵循所在目录的规则：

- 在公开目录中的图片：可访问
- 在隐藏目录中的图片：不可访问

---

## 验证

推送后访问网站，检查：
1. 文件树中是否只显示公开内容
2. 直接访问私有文件 URL 是否返回 403

---

## 注意事项

1. **敏感信息**：不要在公开文章中引用私有文章或资源
2. **同步延迟**：推送后可能需要几秒钟才能在网站生效
3. **配置生效**：修改 `.knowledge-publish.yaml` 后需要推送才能生效