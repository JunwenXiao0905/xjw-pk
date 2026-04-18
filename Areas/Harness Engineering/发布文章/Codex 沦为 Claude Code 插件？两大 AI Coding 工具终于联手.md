---
theme: default
themeName: "默认主题"
title: "Codex 沦为 Claude Code 插件？两大 AI Coding 工具终于联手"
---

我经常一边用 Claude Code 改代码，一边开着 Codex 写方案、做 review。  好处就是各取所长，但麻烦的就是**上下文来回复制、结果手动搬运、或者文档通信**。  刚看到这个插件的时候还真的蛮兴奋的，这不刚好是我需要的吗，这得赶紧试试啊。

总的来说：`codex-plugin-cc` 干的就一件事：**把 Codex 接进 Claude Code，让它变成可调度的外援。**

官方仓库：<https://github.com/openai/codex-plugin-cc>  
本文演示环境：WSL 安装的 Ubuntu。

# 这个插件到底有什么用？

| 命令                          | 干什么用            | 常用参数                                                                                             | 例子                                                                        |
| --------------------------- | --------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| `/codex:setup`              | 检查安装、登录和插件状态    | `--enable-review-gate`；`--disable-review-gate`                                                   | `/codex:setup`                                                            |
| `/codex:rescue`             | 把活直接丢给 Codex    | `--background` 后台跑；`--resume` 接着上次做；`--fresh` 强制新开；`--wait` 等结果；`--model` 指定模型；`--effort` 指定推理强度 | `/codex:rescue 修复当前项目的启动报错，并说明根因`                                         |
| `/codex:review`             | 让 Codex 做只读审查   | `--base main` 指定对比基线；`--background` 后台跑；`--wait` 等结果                                             | `/codex:review --base main`                                               |
| `/codex:status`             | 看后台任务跑到哪了       | 无                                                                                                | `/codex:status`                                                           |
| `/codex:result`             | 取回任务结果          | 无                                                                                                | `/codex:result`                                                           |
| `/codex:cancel`             | 取消后台任务          | 可跟任务 ID                                                                                          | `/codex:cancel`                                                           |
| `/codex:adversarial-review` | 专门挑刺，做反方 review | 可直接跟审查目标                                                                                         | `/codex:adversarial-review challenge whether this retry strategy is safe` |

最常见的流程就 4 步：**发任务、看进度、拿结果、继续改。**

它最核心的价值就这几件事：

- 你可以直接在 Claude Code 里把任务丢给 Codex
- Codex 跑完后，结果直接回到当前对话
- 长任务可以挂后台
- 同一个任务可以继续续跑，而不是每次重新解释上下文
- review、分析、修复可以接进同一条开发链路

# 和手动打开 `codex` 有啥区别

手动打开 `codex` 当然也能用。

但你只要同时在用 Claude Code 和 Codex，很快就会发现，麻烦不在模型能力，而在协作方式。

| 通过插件                     | 手动打开 `codex` |
| ------------------------ | ------------ |
| 自动继承当前工作目录               | 你要自己切目录      |
| 结果直接回到当前对话               | 你要自己复制粘贴     |
| 可用 `/codex:status` 看后台任务 | 你要自己管进度      |
| 可用 `--resume` 接着做同一任务    | 你要自己恢复会话     |
| 更像“一个SubAgent”           | 更像“再开一个独立工具” |

# 1 分钟装好

> Tips：先确认 4 件事：装了 Claude Code；本机能运行 `codex`；已经登录 Codex；Node.js 不低于 `18.18`。

```bash
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
```

如果还没登录 Codex：

```bash
!codex login
```

如果本机没装 `codex`，`/codex:setup` 检测到 `npm` 可用时也会提示安装。

装完后，通常你会看到：

- 一组 `/codex:*` 命令
- 一个 `codex:codex-rescue` 子代理

> `codex:codex-rescue`是 /codex:rescue 背后调用的子代理，平时直接用 /codex:rescue 就行。

最小验证很简单，直接跑一个只读 review：

```bash
/codex:review --background
/codex:status
/codex:result
```

能看到状态和结果，基本就通了。

# 最值得用的 3 个工作流

## 1）小任务，直接前台交给 Codex

```bash
/codex:rescue 为这个仓库补一份 README，要求简洁、可直接运行
```

适合短平快任务：修小 bug、补文档、整理说明、查问题。

## 2）长任务，挂后台慢慢跑

```bash
/codex:rescue --background 分析当前仓库的测试结构，并给出重构建议
/codex:status
/codex:result
```

最爽的是：  
**Claude Code 继续在前台写，Codex 在后台深挖。**

## 3）同一个任务，接着往下做

```bash
# 第一次
/codex:rescue 完成一份关于 X 的报告

# 第二次
/codex:rescue --resume 这份报告还缺少 Y 部分，请继续完善
```

`--resume` 最值钱的地方不是省命令，而是**省解释**。

你不用每次把背景、目标、现状、上次做到哪一步再讲一遍。

如果你明确不想延续上一次任务，可以这样：

```bash
/codex:rescue --fresh 重新分析这个问题，不继承之前上下文
```

# 还有几个细节
## 还能切回原生 Codex CLI

插件结果里在可用时会附带 `session ID`，可以直接：

```bash
codex resume <session-id>
```

## 项目里的 Codex 配置也会生效

比如根目录下的 `.codex/config.toml`：

```toml
model = "<model-name>"
model_reasoning_effort = "high"
```

插件调用 Codex 时也会读这份配置。

## review gate 很强，但别默认乱开

```bash
/codex:setup --enable-review-gate
/codex:setup --disable-review-gate
```

它会在 Claude Code 准备结束一次响应时自动触发一轮 Codex review。  
好处是更严，代价是更慢，而且更耗额度。

所以更适合关键提交前开，不适合长期默认开着。

# 最后一句

说到底，它最有用的一点就是：

**你终于不用再站在 Claude Code 和 Codex 中间当人肉中转站了。**
