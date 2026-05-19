# 性能优化

## 模型选择策略

**Haiku 4.5**（Sonnet 90% 能力，3 倍成本节省）：
- 高频调用的轻量 agent
- 结对编程和代码生成
- 多 agent 系统中的工作 agent

**Sonnet 4.6**（最佳编码模型）：
- 主要开发工作
- 编排多 agent 工作流
- 复杂编码任务

**Opus 4.5**（最深推理）：
- 复杂架构决策
- 最大推理需求
- 研究和分析任务

## 上下文窗口管理

避免在上下文窗口最后 20% 进行：
- 大规模重构
- 跨多文件的功能实现
- 复杂交互调试

低上下文敏感度任务：
- 单文件编辑
- 独立工具创建
- 文档更新
- 简单 Bug 修复

## Extended Thinking + Plan Mode

Extended thinking 默认启用，预留最多 31,999 tokens 用于内部推理。

通过以下方式控制 extended thinking：
- **切换**：Option+T (macOS) / Alt+T (Windows/Linux)
- **配置**：在 `~/.claude/settings.json` 设置 `alwaysThinkingEnabled`
- **预算上限**：`export MAX_THINKING_TOKENS=10000`
- **详细模式**：Ctrl+O 查看 thinking 输出

对于需要深度推理的复杂任务：
1. 确保 extended thinking 已启用（默认开启）
2. 启用 **Plan Mode** 采用结构化方法
3. 使用多轮批判进行彻底分析
4. 使用分角色子 agent 获取多元视角

## 构建故障排查

构建失败时：
1. 使用 **build-error-resolver** agent
2. 分析错误消息
3. 逐步修复
4. 每次修复后验证