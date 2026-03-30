这份 𝗖𝗟𝗔𝗨𝗗𝗘.𝗺𝗱 文件能让你成为10倍效率工程师 👇  
  
它整合了 Claude Code 创作者分享的全部最佳实践：  
  
Anthropic 公司 Claude Code 的创作者鲍里斯·切尔尼（Boris Cherny）在 X 平台上分享了他和团队日常使用 Claude Code 时的内部最佳实践与工作流程。有人将这些推文内容整理成了结构化的 𝗖𝗟𝗔𝗨𝗗𝗘.𝗺𝗱 文件，你可以直接应用到任何项目中。  
  
文件包含：  
• 工作流编排  
• 子智能体策略  
• 自我优化循环  
• 完成前校验机制  
• 自主漏洞修复  
• 核心原则  
  
这是一套可复利迭代的系统：你每一次修正都会被记录为规则。随着时间推移，Claude 会从你的反馈中学习，错误率会不断降低。  
  
	如果你每天都在使用 AI 进行开发，这份文件能为你节省大量时间。

  

# CLAUDE.md  
  
## Workflow Orchestration  
  
### 1. Plan Node Default  
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)  
- If something goes sideways, STOP and re-plan immediately – don't keep pushing  
- Use plan mode for verification steps, not just building  
- Write detailed specs upfront to reduce ambiguity  
  
### 2. Subagent Strategy  
- Use subagents liberally to keep main context window clean  
- Offload research, exploration, and parallel analysis to subagents  
- For complex problems, throw more compute at it via subagents  
- One task per subagent for focused execution  
  
### 3. Self-Improvement Loop  
- After ANY correction from the user: update `tasks/lessons.md` with the pattern  
- Write rules for yourself that prevent the same mistake  
- Ruthlessly iterate on these lessons until mistake rate drops  
- Review lessons at session start for relevant project  
  
### 4. Verification Before Done  
- Never mark a task complete without proving it works  
- Diff behavior between main and your changes when relevant  
- Ask yourself: "Would a staff engineer approve this?"  
- Run tests, check logs, demonstrate correctness  
  
### 5. Demand Elegance (Balanced)  
- For non-trivial changes: pause and ask "is there a more elegant way?"  
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"  
- Skip this for simple, obvious fixes – don't over-engineer  
- Challenge your own work before presenting it  
  
### 6. Autonomous Bug Fixing  
- When given a bug report: just fix it. Don't ask for hand-holding  
- Point at logs, errors, failing tests – then resolve them  
- Zero context switching required from the user  
- Go fix failing CI tests without being told how  
  
---  
  
## Task Management  
  
1.  **Plan First**: Write plan to `tasks/todo.md` with checkable items  
2.  **Verify Plan**: Check in before starting implementation  
3.  **Track Progress**: Mark items complete as you go  
4.  **Explain Changes**: High-level summary at each step  
5.  **Document Results**: Add review section to `tasks/todo.md`  
6.  **Capture Lessons**: Update `tasks/lessons.md` after corrections  
  
---  
  
## Core Principles  
  
- **Simplicity First**: Make every change as simple as possible. Impact minimal code.  
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.  
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.