# 开发流程

> 此文件扩展了 [common/git-workflow.md](./git-workflow.md)，涵盖 git 操作之前的完整功能开发过程。

功能实现流程描述开发管道：研究、规划、TDD、代码审查，然后提交到 git。

## 功能实现流程

0. **研究与复用** _(任何新实现前的强制步骤)_
   - **GitHub 代码搜索优先**：运行 `gh search repos` 和 `gh search code` 在编写新代码前查找已有实现、模板和模式。
   - **库文档其次**：使用 Context7 或主要供应商文档确认 API 行为、包用法和版本特定细节后再实现。
   - **Exa 仅在前两者不足时使用**：GitHub 搜索和主要文档之后，使用 Exa 进行更广泛的网络研究或发现。
   - **检查包注册表**：编写工具代码前搜索 npm、PyPI、crates.io 等注册表。优先久经考验的库而非手工解决方案。
   - **搜索可适配的实现**：寻找能解决 80%+ 问题且可 fork、移植或包装的开源项目。
   - 当满足需求时，优先采用或移植已验证的方法而非编写全新代码。

1. **先规划**
   - 使用 **planner** agent 创建实现计划
   - 编码前生成规划文档：PRD、architecture、system_design、tech_doc、task_list
   - 识别依赖和风险
   - 分阶段拆解

2. **TDD 方法**
   - 使用 **tdd-guide** agent
   - 先写测试（RED）
   - 实现以通过测试（GREEN）
   - 重构（IMPROVE）
   - 验证覆盖率 80%+

3. **代码审查**
   - 编写代码后立即使用 **code-reviewer** agent
   - 处理 CRITICAL 和 HIGH 问题
   - 尽可能修复 MEDIUM 问题

4. **提交与推送**
   - 详细的提交消息
   - 遵循 conventional commits 格式
   - 提交消息格式和 PR 流程见 [git-workflow.md](./git-workflow.md)

5. **审查前检查**
   - 验证所有自动化检查（CI/CD）通过
   - 解决所有合并冲突
   - 确保分支与目标分支保持同步
   - 仅在这些检查通过后请求审查