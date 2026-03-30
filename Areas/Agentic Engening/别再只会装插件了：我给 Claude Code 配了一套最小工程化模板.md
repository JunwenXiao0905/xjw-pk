---
theme: default
themeName: "默认主题"
title: "别再只会装插件了：我给 Claude Code 配了一套最小工程化模板"
---

# 别再只会装插件了：我给 Claude Code 配了一套最小工程化模板

我一开始用 Claude Code 的路子，其实和很多人差不多：

- 先装几个热门插件
- 再收藏几段高赞提示词
- 然后直接上真实项目

一开始确实很爽。写页面、改接口、排报错，速度都比我自己手敲快。

但真正让我警觉的，是一次很小的需求。

那次我只是想给后台的订单列表加一个“异常状态”筛选，顺手把状态文案统一一下。按理说，这就是一个很普通的中小改动。结果 Claude Code 干了三件我没让它干的事：

1. 它顺手改了公共查询 hook，因为它觉得“这样更统一”
2. 它把一个前后端共用的状态常量也重命名了
3. 它最后告诉我“已经完成”，但其实根本没跑验证

当天我还没完全意识到问题，只觉得“AI 太爱发挥了”。

第二天我开了个新会话继续收尾，它又像失忆了一样，开始按另一套风格生成代码。我前一天强调过的目录边界、改动范围、交付格式，它几乎都得重新说一遍。

那一刻我才反应过来：**问题不是插件装得不够，也不是提示词写得不够花，而是我把 Claude Code 当成了一个会写代码的聊天框。**

它当然很强，但如果你不给它稳定的记忆边界和任务协议，它在连续协作里就很容易变得“不稳”。

这篇文章我不想再讲“Claude Code 有多强”，也不想盘点哪个插件最近最火。我只讲一件更基础、但我后来觉得更重要的事：

> **我是怎么把 Claude Code 从“偶尔很惊艳，但经常乱发挥”，调成“能持续协作”的。**

核心其实不复杂，就两步：

1. 把记忆分层
2. 把任务协议固定下来

---

## 一、先别急着怪模型，它本来就会“忘”

很多人第一次深用 Claude Code，都会遇到这几个现象：

- 新会话一开，又要重新交代项目背景
- 同一个项目里，今天和明天的风格不一样
- 它会主动“帮你优化”，结果改出额外风险
- 它说“完成了”，但其实只是把代码写出来了

这不是因为它笨，而是因为你给它的信息大概率都混在了对话里。

我后来复盘，发现自己之前把三种完全不同的信息，全靠临场聊天告诉它：

- 我个人长期的协作习惯
- 这个项目自己的边界和规则
- 这一次任务到底要做什么

这三类信息里，只有第三类应该放在当前对话里。前两类如果每次都靠现说，Claude Code 再强也会不稳定。

这就是我后来真正理解 `CLAUDE.md` 的地方：

**它不是项目说明文档，而是给 Claude Code 预加载的协作记忆。**

说得再直白一点，`README.md` 是写给人看的，`CLAUDE.md` 是写给 Claude 看的。

---

## 二、真正有用的不是一个 `CLAUDE.md`，而是两层记忆

我之前犯过一个很典型的错误：把所有规则都写进项目根目录那一个 `CLAUDE.md`。

后来越写越长，既有“这个仓库怎么跑”，也有“我个人更喜欢最小改动”，还有“输出时先说风险再说结论”这种个人习惯。结果就是：文件越来越胖，信号越来越杂。

后来我才理顺，一个人长期用 Claude Code，至少应该分清两层：

### 1）用户级记忆：放“你是谁，习惯怎么协作”

这个文件适合放在 `~/.claude/CLAUDE.md`。

这里不要写项目细节，只写你跨项目都成立的工作默认项，比如：

- 遇到 3 步以上的任务，先给计划再动手
- 优先最小修改，不要顺手大重构
- 修改前先列受影响文件
- 完成后必须汇报验证结果和剩余风险
- 如果有更简单的方案，优先选简单方案

我的用户级版本，最核心的其实就这几条：

```md
# My Working Defaults

- For non-trivial tasks, explain the plan before editing.
- Prefer minimal diffs over opportunistic refactors.
- Before changing code, list impacted files or modules.
- Never claim completion without showing verification.
- Summarize changes, tests, and remaining risks at the end.
```

这类规则的特点是：**换项目也成立，换语言也成立，甚至换团队大概率也成立。**

### 2）项目级记忆：放“这个仓库到底有什么边界”

项目级 `CLAUDE.md` 才应该放在仓库根目录。

它适合写的是这个项目独有的事实和约束，比如：

- 技术栈和目录结构
- 哪些目录能改，哪些目录别碰
- 测试命令、构建命令怎么跑
- 哪些改动属于高风险
- 对外接口、数据库迁移、配置文件有没有特殊要求

比如一个普通 Web 项目，我现在更愿意这样写：

```md
# Project Facts

- Monorepo with `web/`, `server/`, `tests/`
- Frontend uses `pnpm`, backend uses `pytest`

# Boundaries

- Default editable paths: `web/`, `server/`, `tests/`
- Do not modify `infra/` or release scripts unless explicitly asked
- Keep public API fields backward-compatible unless breaking change is requested

# Delivery Rules

- For medium or large tasks, first explain plan and impacted files
- After changes, report:
  - modified files
  - verification performed
  - remaining risks
```

写到这里，你会发现一个很关键的区别：

- 用户级记忆，管的是你的长期协作风格
- 项目级记忆，管的是这个仓库的客观边界

**这两层一分开，Claude Code 才不容易把“你的习惯”和“仓库规则”搅在一起。**

这也是我觉得很多人一开始没讲透的地方：  
不是“有没有 `CLAUDE.md`”这么简单，而是**你有没有把记忆分层**。

---

## 三、插件能放大能力，但不能代替协作秩序

我不是反插件。

相反，我现在也会用插件，也认可多智能体、自动化检查、技能库这些东西的价值。

但我越来越确定一件事：

> **插件解决的是能力扩展，记忆分层和任务协议解决的是协作秩序。**

顺序反了，就很容易出现一种情况：功能越来越多，输出越来越快，但项目反而越来越乱。

因为你给 Claude Code 增加了“更多手”，却没有先给它“更清楚的边界”。

所以我现在的做法是：  
先把底座搭起来，再去加插件。  
这样插件才像放大器，而不是补丁。

---

## 四、真正让我稳定下来的，是一套固定的任务协议

只有记忆分层还不够。

因为还有第三类信息：**当前任务本身**。这一类不该写进 `CLAUDE.md`，但也不能每次随便一句话扔过去。

我现在最常用的一段任务前置话术，是这句：

```text
先别直接改代码，按这个顺序协作：
1. 用你的话复述目标
2. 列出会受影响的文件或模块
3. 给出最小执行计划
4. 开始实现
5. 结束时汇报：改了什么、怎么验证的、还有什么风险
```

这段话看起来很普通，但它解决了三个很实际的问题。

### 1）防止它一上来就乱改

很多跑偏，都是因为它还没真正理解目标，就已经开始动手了。

先让它复述目标，能立刻筛掉一批误解。

### 2）防止改动范围失控

我现在特别看重“先列受影响文件”这一步。

因为一旦它自己先把影响面说出来，你就能很快判断：  
这次改动是不是已经越界了？  
它是不是准备顺手重构不该动的地方？

### 3）防止“写完”不等于“交付”

最后那句“怎么验证的、还有什么风险”，比很多人想的都重要。

Claude Code 很擅长完成“生成”，但如果你不主动要求，它未必会自动进入“交付”状态。

而一旦你固定要求它汇报验证结果，很多任务的质量会明显上升。

---

## 五、我现在真的在用的最小落地版

如果你也想把 Claude Code 用稳，我建议别一上来搞得很重，直接从这个最小版开始。

### 第一步：先建用户级 `CLAUDE.md`

位置：

```text
~/.claude/CLAUDE.md
```

只写你跨项目都成立的默认协作规则，控制在 5 到 10 条以内。

重点写这些：

- 什么时候先计划
- 你偏好最小改动还是允许重构
- 输出结论的格式
- 完成前要不要验证

### 第二步：再建项目级 `CLAUDE.md`

位置：

```text
<project-root>/CLAUDE.md
```

只写这个仓库独有的信息：

- 技术栈
- 目录边界
- 高风险区域
- 常用命令
- 交付要求

记住一点：  
**项目级文件越像“仓库边界说明”，它就越有用；越像“什么都往里塞的备忘录”，它就越没用。**

### 第三步：把任务下法改掉

不要再直接说：

> “把这个需求做完。”

改成：

> “先复述目标，再列影响范围，再给计划，然后实现，最后汇报验证结果。”

这一步几乎零成本，但收益很高。

### 第四步：给收尾固定一个格式

我现在默认让 Claude Code 在结束时回答四个问题：

- 改了哪些文件
- 为什么改这些文件
- 做了哪些验证
- 还剩什么风险或人工确认项

如果它能稳定回答这四个问题，很多“表面完成、实际没交付”的情况会少很多。

---

## 六、如果只记一件事，就记这个

我后来对 Claude Code 的判断越来越简单：

它不是一个“你说一句，它就永远懂你”的工具。  
它更像一个能力很强、但需要明确边界的协作者。

所以真正的进阶，不是继续堆插件，也不是继续卷提示词花活，而是先把下面这两件事搭起来：

1. 用两层 `CLAUDE.md` 管好长期记忆
2. 用固定任务协议管好当前任务

这套东西听起来不炫，但它是底座。

底座稳了，插件才有意义；底座没稳，再多插件也只是让它更快地“乱发挥”。

这也是我现在更愿意分享的 Claude Code 经验：

**先把它用稳，再把它用猛。**

---

## 附：适合直接抄走的最小模板

### 1）用户级模板

```md
# My Working Defaults

- For non-trivial tasks, explain the plan before editing.
- Prefer minimal diffs over broad refactors.
- List impacted files before implementation.
- Do not mark a task complete without verification.
- End with summary, tests, and remaining risks.
```

### 2）项目级模板

```md
# Project Facts

- Monorepo with `web/`, `server/`, `tests/`
- Frontend uses `pnpm`
- Backend uses `pytest`

# Boundaries

- Editable by default: `web/`, `server/`, `tests/`
- Do not modify `infra/` or release scripts unless asked
- Keep external API compatibility unless explicitly requested

# Delivery

- Explain plan before non-trivial changes
- Report modified files, verification, and remaining risks
```

### 3）任务协议模板

```text
先别直接改代码，按这个顺序协作：
1. 复述目标
2. 列出受影响文件或模块
3. 给出最小执行计划
4. 开始实现
5. 结束时汇报：改了什么、怎么验证的、还有什么风险
```
