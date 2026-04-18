

enterWorktree

 工作流程：
  1. EnterWorktree — 创建新的 worktree（在 .claude/worktrees/ 目录下），切换当前会话进去
  2. 在新环境中工作、提交
  3. ExitWorktree — 退出时选择 keep（保留）或 remove（删除）

  和普通 git worktree 的区别：
  - 普通 git worktree add 只是创建目录
  - EnterWorktree 会同步切换 Claude Code 会话的工作目录、重置上下文缓存、更新任务目录等
