# 回敬 Codex，Claude Code 推出 /goal 功能，不干完不睡觉



继 Codex 之后，Claude Code 上线了 `/goal` 命令，设定完成条件，不达目的就不停。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

不达目的不罢休

五一假期的第一天，[Codex 发布了同名的](https://mp.weixin.qq.com/s?__biz=MzA4NzgzMjA4MQ==&mid=2453483290&idx=1&sn=904eb46992f4d152d712fd963e274f9f&scene=21#wechat_redirect) `[/goal](https://mp.weixin.qq.com/s?__biz=MzA4NzgzMjA4MQ==&mid=2453483290&idx=1&sn=904eb46992f4d152d712fd963e274f9f&scene=21#wechat_redirect)`，而十天后，Claude Code 的版本也来了。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

这个功能随 2.1.139 版本发布。给 Claude 设一个目标条件，它就跨多个回合持续工作，每轮结束自动判断是否达成，没搞定就继续，直至完成了才会停。

01

## 互相致敬

Codex 的 `/goal` 上线时，灵感来自社区里的 Ralph Loop，一种让 Agent 设定目标、失败就重来、不达成就不停的循环模式。

这里也再聊一下 Ralph Loop。

这个名字来自《辛普森一家》里的 Ralph Wiggum，那个「无知、执着、乐观」的小男孩。开发者 Geoffrey Huntley 用他的名字命名了一种 Agent 循环模式：给 Agent 设定一个目标，让它自己不断迭代，失败了就重来，直到目标达成。

VentureBeat 甚至写了篇文章叫《Ralph Wiggum 如何从辛普森一家变成 AI 界最火的名字》。![Agent 换班交接](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

在社区的原始实现里，Ralph Loop 的做法比较「暴力」：每一轮结束后，Agent 从头开始一个新的上下文窗口，靠 git 记录和进度文件来保持记忆。

而 Ralph Loop 的最早实践者，恰恰是 Claude Code 的用户们。

这里有点意思的是，OpenAI 的 Codex 发布 /goal 的时候，明确说灵感来自 Claude 生态的 Ralph 脚本。那 Claude Code 现在出 /goal，为什么不说自己也是在学 Codex 呢……？![互相借鉴](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

互相借鉴

  

而就在 Codex 推出 `/goal` 之后没几天，OpenAI 又给 Codex 加了宠物功能，一个悬浮在桌面上的状态小组件，显示任务进度，能互动，能点击跳回主界面。这个功能……也是受 Claude Code 的宠物功能启发的。

**这样的互相「借鉴」，对我们来说，倒也不是个坏事。**

02

## 定好目标就开跑

在 Claude Code 里输入：

●●●

`/goal test/auth 下所有测试通过，lint 干净   `

└

一个回车后，Claude 就开始干活了。

每完成一轮，系统自动判断目标是否达成。没达成，继续下一轮；达成了，自动停止。

![定好目标就开跑](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

定好目标就开跑

运行过程中，界面上会显示一个 `◎ /goal active` 的状态面板，实时展示已运行时间、轮次数和 token 消耗。

几个辅助命令：

• `/goal`：不加参数，查看当前目标的状态、轮次、token 消耗和最新的评估理由 

• `/goal clear`：清除目标（stop、off、reset、cancel 也都行） 

目标还能跨会话保持。用 `--resume` 或 `--continue` 重新打开上次的会话，目标会自动恢复，轮次和 token 计数则重新开始。

此外还有个好用的姿势是，在非交互模式下直接跑：

●●●

`claude-p "/goal CHANGELOG.md 里有本周每个合并 PR 的记录"   `

└

一条命令，跑到完成为止。甚至还可以直接接进 CI 管道里用，也完全没有问题。

03

## 裁判分离

这是 Claude Code 和 Codex 之间最关键的设计差异。

Codex 的做法是让工作模型自己做「完成审计」：每轮结束后，系统注入一条指令，要求模型把目标拆解成检查清单，逐项验证。

干活的人，同时也是验收的人。

而 Claude Code 换了个思路。

**干活的归干活，验收的归验收。**

每轮结束后，系统把目标条件和对话记录发给一个独立的小模型（默认是 Haiku），由它来判断条件是否满足。如果没满足，它还会返回一段理由，告诉主模型哪里还差，作为下一轮的方向指引。

![双模型评估](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

双模型评估

为什么要这么设计呢？

让一个模型自己判断「我做完了没」，它很容易把「我产出了东西」等同于「我达成了目标」。

测试通过了就觉得功能完成了，代码写完了就觉得需求满足了。这其实是 Agent 循环中最隐蔽的失败模式之一。

用一个独立的模型来做评估，会多了一层制衡。

**当然不能让模型既当运动员，又当裁判。**

而且评估用的是 Haiku 的轻量模型，token 成本基本可以忽略。

04

## 目标制定

官方文档给了一些写目标条件的建议。

![好目标三要素](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

好目标三要素

一个好的目标条件，通常有三个要素：

• **一个可衡量的终态**：测试结果、构建退出码、文件数量、队列清空 

• **一个验证方式**：怎么证明完成了，比如「`npm test` 退出码为 0」或「`git status` 干净」 

• **不能破坏的约束**：过程中不能动什么，比如「不修改其他测试文件」 

条件最长支持 4000 个字符。

还有个技巧，想限制运行时长的话，可以直接写进条件里，比如「20 轮后如果没完成就停下来」。评估模型每轮都会根据对话内容来判断这个限制是否触发了。

这里有个限制是：评估模型不能独立运行命令或读文件，它只能看 Claude 在对话中展示出来的东西。所以目标条件得写成 Claude 自己的输出能证明的形式。

比如「所有测试通过」就是个好条件，因为 Claude 会去跑测试，结果自然会出现在对话里。但「代码质量提升了」就太模糊了，评估模型没法判断。

05

## 三条路

Claude Code 现在有三种让 Agent 持续工作的方式：

|方式|下一轮何时开始|何时停止|
|:--|:--|:--|
|`/goal`|上一轮结束后|独立模型确认条件达成|
|`/loop`|定时间隔触发|你手动停，或 Claude 觉得做完了|
|Stop hook|上一轮结束后|你自己的脚本或 prompt 决定|

`/goal` 和 auto mode 配合起来，效果应该是最好的。

auto mode 解决「每次工具调用都要点确认」的问题，`/goal` 解决「每轮结束都要手动发消息」的问题。

两个一起开，你只需要定义目标，然后，可以去喝咖啡了。

06

## 同版本功能

2.1.139 还带了不少其他更新。

**Agent View** 上线了（研究预览），输入 `claude agents` 就能看到所有会话的列表，正在跑的、等你回复的、已经完成的，一屏了然。

系统提示词的压缩变成了静默执行。以前长对话触发上下文压缩时会有提醒，现在不会了。

![系统提示词变更](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

系统提示词变更

这个改动，还在社区引发了一些讨论。有人担心取消压缩提醒之后，关键信息被裁掉了你都不知道，Agent 的行为可能莫名其妙地漂移。也有人指出，新版的压缩提示词会要求模型「保留敏感的用户指令」，算是在机制上做了补偿。

另外还修了 30 多个 bug，包括凭证过期导致的死锁、MCP 服务器内存泄漏（加了 16MB 上限）、深色主题下链接颜色看不清等问题。

07

## 编程即训练

回到 `/goal` 本身。

功能看起来很简洁：设定目标，循环执行，条件满足就停。

但如果我们把视角拉远一步，它其实在改变一件根本性的事情：**你和代码的关系。**

Keras 的作者 François Chollet 最近写了一段话，大意是：**足够先进的 AI 编程，本质上就是机器学习**。见我前文：[AI 编程的本质，就是机器学习](https://mp.weixin.qq.com/s?__biz=MzA4NzgzMjA4MQ==&mid=2453483677&idx=1&sn=df382d9fbcc2cb7bddc600ed4fda799e&scene=21#wechat_redirect)

仔细想想，确实如此。

你写需求文档，相当于定义 loss function。你写测试用例，相当于准备验证集。Agent 每一轮迭代，就是一个 training step。最后产出的代码库，就是训练好的模型权重。

**你会部署它，但未必会逐行去读它。**

![编程 vs 训练](https://mmbiz.qpic.cn/sz_mmbiz_png/ZKqVLiaIpzFnm46Bp5beszhiaibZ3WAfVJzPr2opennWgWCUC2Zjxbs22VTXLbZza2GuHk8vFYEkCTSkF4W9a8s9XP5hnvfD2ibqQZB770GZOrM/640?from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=8)

编程 vs 训练

而 `/goal` 做的事情，就是把这个「训练循环」正式自动化了。你设定优化目标，划定搜索空间的约束，然后让一个优化过程自动迭代，直到目标收敛。

我甚至觉得，可以直接写下这个公式：

●●●

`model.fit() = /goal`

└

而一旦接受了这个等号，你花时间的地方就彻底变了。

不再是写代码本身。

而是：我的优化目标定对了吗？我的验证标准够不够严？我的约束条件会不会让 Agent 找到某个投机取巧的捷径，测试全过但逻辑其实是歪的？

这些问题，机器学习领域已经研究了几十年了。过拟合、数据泄露、概念漂移……都是同样的坑。

Codex 有 `/goal`，Claude Code 也有了 `/goal`。两家还会继续互相「借鉴」下去。

而对我们来说，真正要练的本事，已经不是写代码了。

**是想清楚自己到底要什么，然后，定义好验收标准。**

**剩下的，交给训练循环。**

◇ ◆ ◇

相关链接：

https://code.claude.com/docs/en/goal

https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#21139

