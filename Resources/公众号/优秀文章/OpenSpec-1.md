# 【开源】26.3K star，AI 写代码越来越乱？我们如何用 OpenCode + OpenSpec 把 AI 编程拉进“工业化时代”

原创 三丰 soft张三丰

 _2026年2月28日 09:30_ _河北_ 2人

# 如何用 OpenCode + OpenSpec 把 AI 编程拉进“工业化时代”

> 很多团队都有同感：AI 刚上手时很惊艳，一旦项目变大，它就开始“乱写代码、乱改逻辑、越帮越忙”。
> 
> 我们也是踩过坑之后，才意识到：
> 
> **问题不在于 AI 不够聪明，而在于我们缺少一套“工程化的玩法”。**

这篇文章，就来聊聊我们是怎么用OpenCode + OpenSpec，把“凭感觉的 Vibe Coding”，一步步升级成“规范驱动、可复制、可审计”的 AI 工程体系的。

![五类读者](https://mmbiz.qpic.cn/mmbiz_png/6wEpbjZhHQw63uqMZDDEVK8Fhb5vhMfQ7BjDP1vNZISJQeibF6n7EvgSAmKZDr0rAuDZhJkqXialEWYJZnGD5asU1ia2c7IS8JNgnXBIUKBI28/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=0)

---

# 🤯 从“真香”到“真乱”：Vibe Coding 的坑

刚开始用 AI 编程助手时，大家都是“真香”：

一句话生成一个页面

几轮对话搭起一个接口

复制粘贴报错，AI 三下五除二就帮你改好

但项目一复杂，问题就来了：

- 上下文丢失：AI 忘了前面写过什么，同一个函数改了 N 个版本，自己跟自己打架。
    
- 回归 Bug：加个新功能，旧功能莫名其妙就坏了。
    
- 风格混乱：代码库像“缝合怪”，到处是没人敢动的“祖传逻辑”。
    
- 协作困难：A 用 AI 写了一套，B 用 AI 又写了一套，风格迥异，难以维护。
    

> 研发同学最常说的吐槽是：
> 
> **“代码库越大，AI 弄得越乱。”**

这种“跟着感觉走”的Vibe Coding模式，本质上是一种不可预测的艺术，而不是可重复、可扩展的工程方法。

要真正把 AI 当成生产力，我们必须完成一次范式升级：

> **从“Vibe Coding”，走向“规范驱动开发（Spec-Driven Development）” + 专业化 AI 工程。**

---

![图片](https://mmbiz.qpic.cn/mmbiz_png/6wEpbjZhHQz86JYEefl9HzbBro6lzpvq2XTGUBseJ4Vm4BAtZOKxVCW4bJ24vjL0Eg80ItJWUF3LKZzcp5CoezAPP1rmo0SgZCfnySSog70/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=1)

# 💡 我们的解法：OpenCode + OpenSpec

坦白说，我们一开始也没想“造轮子”，只是想解决两个很朴素的问题：

AI 能不能先搞清楚“要干什么”，再动手写代码？

能不能让 AI 写代码时，老老实实遵守我们团队的规范和架构？

在试过各种方案后，我们最终把目光锁定在了OpenCode + OpenSpec的组合上。

## 1. OpenCode：不止是“代码补全”，而是“工程执行引擎”

OpenCode 不是传统意义上的代码补全工具，而是一个面向工程流程的自动化执行框架。

它的核心思路是：

把一个复杂开发任务，拆成多个步骤

按流程一步步执行，而不是“想到哪写到哪”

它内置了强大的工具能力，如文件匹配（Glob）、内容读取（Read）、精确编辑（Edit）和代码模式搜索（Grep），让 AI 能在受控范围内完成代码级操作。

> 简单说，OpenCode 更像一个“**能听懂人话、会按流程办事的工程师**”，而不是一个只会补全代码的“打字员”。

对我们来说，OpenCode 最大的吸引力在于它的模型中立性。它不绑定任何单一模型供应商，可以灵活接入智谱 GLM、阿里 Qwen 等国产大模型，这对企业级应用来说，意味着更高的灵活性和数据隐私保障。

## 2. OpenSpec：给 AI 一个“项目宪法”和“导航系统”

如果说 OpenCode 是强大的执行引擎，那 OpenSpec 就是精准的导航系统。它是一个轻量级的、对“棕地项目”（Brownfield，即已存在的项目）特别友好的规范驱动开发（Spec-Driven Development, SDD）框架。

OpenSpec 的核心是“棕地优先”，能很好地融入大型现有项目。它通过一个简单的三步工作流，确保人与 AI 在编码前对齐目标：

- Proposal (提案)：在投入编码前，开发者与 AI 共同明确需求，创建一份详细、无歧义的规范文档。
    
- Apply (实施)：AI 根据已批准的规范，有条不紊地分步生成代码、测试和文档。
    
- Archive (归档)：任务完成后，将此次变更的规范合并入项目的主规范库，使其成为一份随代码演进的“活文档”。
    

> OpenSpec 的核心价值在于，它强制我们在投入实际编码工作之前，确保人与 AI 对最终目标达成共识，从源头上避免方向性错误。

## 3. 1+1 > 2：当“施工队”遇上“蓝图”

当 OpenCode 与 OpenSpec 结合时，一场奇妙的化学反应发生了：

- OpenSpec提供了结构化的“蓝图”和“护栏”，从根本上解决了 AI 编码的“方向”问题。
    
- OpenCode则是那个强大的“施工队”，负责高效、准确地执行这份蓝图。
    

这种结合将开发过程从传统的“指令-响应”模式，提升为更高效的“监督-自主”模式。这一转变将开发者从微观管理者和代码实现者的角色中解放出来，使他们能晋升为架构师和质量保障者。

---

# 🚀 落地实践：重构企业内部的 AI 协作工作流

要成功落地这套工作流，核心在于上下文工程。正如知名 AI 团队分享的最佳实践所言：

> **LLMs is already smart enough—intelligence is not the bottleneck, context is.**
> 
> （大语言模型已经足够聪明了，瓶颈不在于智力，而在于我们给它的上下文。）

## 1. 奠定基础：建立项目“宪法”

为了给 AI 提供稳定、持久的上下文和规则，我们使用级联的规则系统和 OpenSpec 的 project.md文件，为项目建立了一套“宪法”。

- 全局规则：定义开发者个人的通用编码风格和偏好。
    
- 项目级规则：定义整个团队共享的规则，包括技术栈、核心架构模式、API 设计规范、测试覆盖率要求以及项目的 Git 工作流。
    
- 模块化规则：针对项目中的特定部分定义更细化的规则。
    

这使得 AI 能够按需加载最相关的上下文，实现“即时上下文”，既保证了精度，又节约了成本。

## 2. 核心循环：规范驱动的开发流程

在一个新功能的完整开发生命周期中，我们遵循以下四个步骤：

- 起草变更提案 (Proposal)：开发者在 OpenCode 聊天界面中使用自然语言或斜杠命令发起一个新功能的请求。OpenCode 会自动创建一个结构化的目录，其中包含 proposal.md、tasks.md以及相关的规范差异文件。
    
- 审查与验证规范 (Review & Validate)：这是人机协作的关键环节。开发者与 AI 共同讨论并迭代规范文档，直到所有细节都清晰无误。
    
- 实施任务与代码生成 (Apply)：一旦开发者批准了规范，就可以命令 AI 开始编码。OpenCode 会严格按照 tasks.md中的任务列表，逐一完成编码、创建测试、编写文档等工作。
    
- 归档与更新 (Archive)：功能开发完成、测试通过并成功部署后，执行归档命令。这一步会将此次变更的规范合并到主规范库中，形成可追溯的变更历史。
    

---

# 📖 实践案例：从零到一实现“国际化”功能

接下来，我们通过一个真实案例——为我们的知识库产品添加“国际化”功能——来完整展示上述工作流。

1. 发起提案：开发者向 OpenCode 提出初始需求，AI 迅速生成了提案的核心文件 proposal.md和技术设计文档 design.md。
    
2. 细化任务并验证：基于提案和设计，开发者与 AI 协作，将宏观目标分解为一份具体的、可执行的任务清单 tasks.md，并运行验证命令确保规范的完整性。
    
3. 自动化执行阶段：开发者执行命令后，OpenCode 系统性地创建目录、编写代码、重构 UI 字符串，并有条不紊地在 tasks.md中勾选掉每一项完成的任务。整个过程不仅是自动化的，更是透明、严谨且全程可审计的。
    
4. 完成并归档：在所有任务完成并通过测试后，开发者执行最后的归档命令。该功能的完整规范已成为项目知识库的一部分，为未来的维护和新功能的迭代提供了清晰、可靠的文档依据。
    

---

# 🌟 阶段性成效与未来展望

采用 OpenCode + OpenSpec 的工作流，已经在公司多个团队中取得了显著成效：

- 大幅提升开发速度：知识库产品开发团队反馈，前端代码约 50%、后端代码约 40% 最终由 AI 自主编写完成。
    
- 提升代码质量与一致性：规范先行确保了 AI 生成的代码严格遵守项目既定的架构和设计模式。
    
- 创建“活文档”：每次功能迭代后归档的 OpenSpec 规范，成为了项目唯一、可信的真相来源。
    
- 降低跨团队协作门槛：清晰的规范文档让安全、运维等不同背景的团队成员也能轻松理解和参与到技术项目中。
    

展望未来，随着技术的发展，AI 将在整个软件开发生命周期中扮演更核心的角色。一个更强大的 MCP 生态将创造一个世界，其中 OpenCode 可以在一个统一的工作流中无缝地编排各种研发流程相关服务。而异步 Agent 操作将允许开发者委派长时间运行的任务，如全面的代码重构或遗留系统分析。

当 AI 从一个简单的结对程序员转变为一个自主的工程伙伴时，人类最关键的技能不再是编写代码，而是架构系统并定义指导它的规范。

> 问题不再是“我们如何更快、更好地编码？”，而是“我们如何更聪明地设计？”

  

开源地址

```
https://github.com/Fission-AI/OpenSpec
```

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/6wEpbjZhHQwPbyLiaeIHiamyEEJ52qFLaUvtiae52DfibkFyqQKHfegRNOwGgHa8jt7EuGrtibvibmJuguRceSR3PP6SfC18gLl0xYDABgOlEPriaw/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=2)

猜您喜欢：

[【开源】Vibe Coding已过时？35.9K Star！一个人顶一个团队：这个AI开发框架把PRD、架构、代码全包了](https://mp.weixin.qq.com/s?__biz=MzI3MTQyNDc5MA==&mid=2247503771&idx=1&sn=c0ae78600263d4f0b2049739dc8d0737&scene=21#wechat_redirect)

[【开源】34.7K star，Claude Code该下岗了？这款AI编程神器，把Claude Code按在地上摩擦](https://mp.weixin.qq.com/s?__biz=MzI3MTQyNDc5MA==&mid=2247503840&idx=1&sn=d8391feac0f8b9141815ce784c278249&scene=21#wechat_redirect)

[【开源】58.1K star，别再让AI乱写代码了：这样一套技能库，从需求到 PR，AI 全程按规范写代码，告别返工，用流程把 AI 变成靠谱工程师](https://mp.weixin.qq.com/s?__biz=MzI3MTQyNDc5MA==&mid=2247503823&idx=1&sn=bcdf668856d06b2db231384c10b4485b&scene=21#wechat_redirect)

[开源在线版Cursor，Agent + Skills架构的Vue3低代码智能体，一句话生成完整应用](https://mp.weixin.qq.com/s?__biz=MzI3MTQyNDc5MA==&mid=2247503820&idx=1&sn=50159af4fbfa05283debe43139567188&scene=21#wechat_redirect)

[6元加入会员群，学习、项目、人脉全都有，包括90+低开平台，70+AI平台（含AI入门教程）](https://mp.weixin.qq.com/s?__biz=MzUyNDgyNTg2Ng==&mid=2247491842&idx=1&sn=09b1235e9fedb3d7766cacfd32cbfa88&scene=21#wechat_redirect)

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

  

AI · 目录

上一篇【开源】34.7K star，Claude Code该下岗了？这款AI编程神器，把Claude Code按在地上摩擦下一篇【字节开源】告别上下文地狱：为 AI Agent 而生的上下文数据库，用文件系统重构 Agent 大脑

作者提示: 个人观点，仅供参考

阅读 1435

​

**留言**

写留言

[](javacript:;)

![](https://mmbiz.qpic.cn/mmbiz_png/KmEUbWy7RO9vp33ZAIE0bZmp19NibBiaShutYFpsE2VRCzYSyqOAgzjn0rfCtic78qlnu4Q8LtMCENVZmia2hP8Tfw/300?wx_fmt=png&wxfrom=18)

soft张三丰

关注

18

213

7

写留言

![](https://wx.qlogo.cn/mmopen/duc2TvpEgSRKrwicE9icxabloW41Md1WmBUBEibUbgoicG4wQiaIq4VxA3icgwOKGts9laXwJVF6CxRERrnbdmuvkGeCuIIBkT5nf28K25Ikkt9zWACAQeAvN0iaHrHDI3Jje6N/96)

复制搜一搜

复制搜一搜

暂无评论