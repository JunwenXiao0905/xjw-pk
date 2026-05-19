# Git 工作流

## 提交消息格式
```
<type>: <description>

<optional body>
```

类型：feat, fix, refactor, docs, test, chore, perf, ci

注：通过 ~/.claude/settings.json 全局禁用了署名。

## Pull Request 工作流

创建 PR 时：
1. 分析完整提交历史（不只是最新提交）
2. 使用 `git diff [base-branch]...HEAD` 查看所有变更
3. 起草全面的 PR 总结
4. 包含带 TODO 的测试计划
5. 新分支使用 `-u` 标志推送

> 关于 git 操作之前的完整开发过程（规划、TDD、代码审查），
> 见 [development-workflow.md](Areas/Harness%20Engineering/Claude%20Code/个人笔记/学习/everything-claude-code/rules/common/development-workflow.md)。