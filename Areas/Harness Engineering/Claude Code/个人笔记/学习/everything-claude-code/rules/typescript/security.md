---
paths:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
  - "**/*.jsx"
---
# TypeScript/JavaScript 安全

> 此文件扩展了 [common/security.md](Areas/Harness%20Engineering/Claude%20Code/个人笔记/学习/everything-claude-code/rules/common/security.md)，包含 TypeScript/JavaScript 特定内容。

## 密钥管理

```typescript
// 错误：硬编码密钥
const apiKey = "sk-proj-xxxxx"

// 正确：环境变量
const apiKey = process.env.OPENAI_API_KEY

if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}
```

## Agent 支持

- 使用 **security-reviewer** skill 进行全面安全审计