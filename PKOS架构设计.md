
---
PKOS：Personal Knowledge OS

第一阶段：本地obsidian修改后，自动化推送，服务器触发更新，web页面更新
第二阶段：openclaw的回答能够依赖我的知识库

---


# 一、系统形态
```
             Obsidian
                │
                ▼
            GitHub
                │
                ▼
             NestJS
        ┌───────┼────────┐
        ▼                ▼
   Knowledge Index     Embedding
        │                │
        ▼                ▼
     Postgres          pgvector
        │                │
        └──────┬─────────┘
               ▼
          Knowledge API
               │
        ┌──────┴────────┐
        ▼               ▼
   Personal Website   OpenClaw
                         │
                         ▼
                     RAG Agent
```


# 二、基于Nx Monorepo 的代码结构

你的仓库建议这样组织：（可能和实际不符合）

```
xjw-monorepo
│
├─ apps
│   ├─ web
│   │   └─ React 网站
│   │
│   └─ api
│       └─ Nest API
│
├─ libs
│   │
│   ├─ knowledge-core
│   │   ├─ parser
│   │   ├─ obsidian
│   │   └─ graph
│   │
│   ├─ knowledge-ui
│   │   ├─ components
│   │   └─ pages
│   │
│   ├─ markdown-renderer
│   │
│   ├─ knowledge-search
│   │
│   └─ knowledge-types
│
├─ knowledge-vault
│   └─ (你的 Obsidian vault)
│
└─ tools
    └─ knowledge-indexer.ts
```

这里有一个关键点：

**knowledge vault 


```
git submodule
```

---

# 二、知识库 Indexer（核心）

真正的关键是：

**构建阶段解析 markdown。**

流程：

```
Markdown
   ↓
AST
   ↓
JSON
   ↓
Search Index
``` 

---

## Indexer 脚本

位置：

```
tools/knowledge-indexer.ts
```

核心库：

```
remark
gray-matter
fast-glob
```

示例：

```ts
import fs from "fs"
import path from "path"
import fg from "fast-glob"
import matter from "gray-matter"

const VAULT_PATH = "knowledge"

async function buildIndex() {

  const files = await fg("**/*.md", {
    cwd: VAULT_PATH
  })

  const notes = []

  for (const file of files) {

    const fullPath = path.join(VAULT_PATH, file)

    const raw = fs.readFileSync(fullPath, "utf-8")

    const { data, content } = matter(raw)

    notes.push({
      id: file.replace(".md", ""),
      title: data.title || file,
      tags: data.tags || [],
      content,
      path: file
    })
  }

  fs.writeFileSync(
    "apps/web/public/knowledge-index.json",
    JSON.stringify(notes)
  )
}

buildIndex()
```

---

# 三、知识库数据流



## 写入

```
Obsidian  
   ↓  
Git Push  
   ↓  
GitHub
```

---

## 服务器同步

```
GitHub Webhook
      │
      ▼
Nest Webhook Controller
      │
      ▼
Task Queue（任务队列）
      │
      ▼
Indexer Worker
      │
 ┌────┴───────────────┐
 ▼                    ▼
Metadata Index       Embedding
(JSON / DB)          (Vector DB)
 │                    │
 ▼                    ▼
Website API         AI / OpenClaw
```



## 索引流程

```
MD文件  
   ↓  
remark/markdown AST  
   ↓  
JSON  
   ↓  
Search Index

```
推荐工具：

- **remark**
    
- **unified**
    
- **gray-matter**
    

解析结构：
```

---  
title: Knowledge System  
tags: [pkm]  
created: 2026-03-01  
---  
  
# Heading  
content
```

转换：

```
{  
  title: "",  
  headings: [],  
  tags: [],  
  content: "",  
  links: []  
}
```
# 三、知识数据结构设计

生成 JSON：

```
knowledge-index.json
```

结构：

```json
[
  {
    "id": "ai/knowledge-system",
    "title": "Knowledge System",
    "tags": ["pkm", "ai"],
    "content": "markdown content",
    "links": ["obsidian", "ai-agent"],
    "created": "2026-03-01"
  }
]
```

---

# 四、Obsidian WikiLink 解析

Obsidian：

```
[[AI Agent]]
```

需要转换：

```
/knowledge/ai-agent
```

实现：

```
remark-wiki-link
```

或者简单 regex：

```ts
/\[\[(.*?)\]\]/g
```

转换为：

```html
<a href="/knowledge/$1">
```

---

# 五、React Knowledge UI

你的 React 页面：

```
/knowledge
```

结构：

```
KnowledgeLayout
   │
   ├─ Sidebar
   │     └─ NoteTree
   │
   ├─ Content
   │     └─ MarkdownRenderer
   │
   └─ SearchPanel
```

---

## 页面示例

```
/knowledge/ai-agent
```

页面：

```
KnowledgeNotePage
```

伪代码：

```tsx
export function KnowledgeNotePage() {

  const { slug } = useParams()

  const note = useNote(slug)

  return (
    <div className="flex">

      <Sidebar />

      <article className="prose">

        <MarkdownRenderer>
          {note.content}
        </MarkdownRenderer>

      </article>

    </div>
  )
}
```

---

# 六、Markdown Renderer

推荐：

```
react-markdown
remark-gfm
rehype-highlight
```

组件：

```tsx
import ReactMarkdown from "react-markdown"

export function MarkdownRenderer({ children }) {

  return (
    <ReactMarkdown>
      {children}
    </ReactMarkdown>
  )
}
```

未来可扩展：

- code highlight
    
- math
    
- mermaid
    
- callout
    

---

# 七、知识搜索（重要）

推荐：

**FlexSearch**

优点：

- 极快
    
- 前端搜索
    
- 不需要服务端
    

实现：

```
flexsearch
```

示例：

```ts
import { Index } from "flexsearch"

const index = new Index({
  tokenize: "forward"
})

notes.forEach(note => {
  index.add(note.id, note.content)
})
```

---

# 八、Obsidian Graph（杀手功能）

解析：

```
[[note]]
```

得到：

```
A → B
```

Graph 数据：

```json
{
  "nodes": [],
  "edges": []
}
```

前端：

```
react-force-graph
```

效果：

类似：

Obsidian Graph View。

---

# 九、Nest API（可选）

其实：

**知识库不需要 API。**

但如果你要 AI / 搜索：

可以加：

```
/api/knowledge/search
```

```
/api/knowledge/note
```

# 十三、一个非常重要的优化建议

在 markdown frontmatter 里加：

```
published: true
```

这样：

私人笔记  
公开文章
可以分开。


# 十、OpenClaw 接入（非常关键）

你的知识库可以变成：

**AI Agent 的长期记忆**

方式：

### 方法1

直接读取：

```
knowledge/*.md
```

---

### 方法2（推荐）

生成：

```
embedding
```

流程：

```
markdown
   ↓
chunk
   ↓
embedding
   ↓
pgvector
```

因为你已经有：

```
Postgres
```

安装：

```
pgvector
```

OpenClaw 查询：

```
RAG
```

---

# 十一、最终系统架构

最终系统会是：

```
Obsidian
   ↓
GitHub
   ↓
Server
   ↓
Indexer
   ↓
JSON
   ↓
React Website
```

AI：

```
Knowledge
   ↓
Embedding
   ↓
pgvector
   ↓
OpenClaw
```

---

# 十二、性能策略（很多人做错）

**不要实时解析 markdown。**

正确：

```
build step
```

生成：

```
knowledge-index.json
```

React 直接读取。

网站会：

**非常快。**

---

# 十三、未来可升级

你的系统未来可以升级为：

### Personal Knowledge OS

增加：

```
tasks
daily notes
AI summarizer
knowledge graph
AI search
```

---

# 十四、如果做到这个阶段

你的系统会接近：

这些产品的结合：

- Obsidian
    
- Notion
    
- Logseq
    

但：

**完全 self-hosted。**

---

# 十五、下一步（最重要）

接下来有三个 **非常关键的升级**：

### 1️⃣ Obsidian Graph Web 复刻

很多人梦寐以求。

### 2️⃣ AI Knowledge Search

你的知识库可以：

```
问答
总结
写作
```

### 3️⃣ OpenClaw 数字分身

AI 可以：

- 读你所有知识
    
- 自动整理
    
- 自动写文章
    

---

如果你愿意，我可以下一步直接给你：

**一套完整的代码级实现：**

1️⃣ `knowledge-indexer` **完整工业级版本**  
2️⃣ **Obsidian Graph Web 实现方案**  
3️⃣ **OpenClaw + RAG 接入架构（真正数字分身）**

这一部分其实是：

**整个系统最核心的灵魂。**