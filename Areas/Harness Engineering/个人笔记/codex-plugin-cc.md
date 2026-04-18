---
theme: default
themeName: "默认主题"
title: "Codex 沦为 Claude Code 插件？两大 AI Coding 工具终于联手"
---


官方仓库：<https://github.com/openai/codex-plugin-cc>  
本文演示环境：WSL 安装的 Ubuntu。

# 这个插件到底有什么用？

| 命令                          | 干什么用            | 常用参数                                                                                             | 例子                                                              |
| --------------------------- | --------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| `/codex:setup`              | 检查安装、登录和插件状态    | `--enable-review-gate`；`--disable-review-gate`                                                   | `/codex:setup`                                                  |
| `/codex:rescue`             | 把活直接丢给 Codex    | `--background` 后台跑；`--resume` 接着上次做；`--fresh` 强制新开；`--wait` 等结果；`--model` 指定模型；`--effort` 指定推理强度 | `/codex:rescue 修复当前项目的启动报错，并说明根因`                               |
| `/codex:review`             | 让 Codex 做只读审查   | `--base main` 指定对比基线；`--background` 后台跑；`--wait` 等结果                                             | `/codex:review --base main`                                     |
| `/codex:status`             | 看后台任务跑到哪了       | 无                                                                                                | `/codex:status`                                                 |
| `/codex:result`             | 取回任务结果          | 无                                                                                                | `/codex:result`                                                 |
| `/codex:cancel`             | 取消后台任务          | 可跟任务 ID                                                                                          | `/codex:cancel`                                                 |
| `/codex:adversarial-review` | 专门挑刺，做反方 review | 可直接跟审查目标                                                                                         | /codex:adversarial-review --background "针对ADS-B和AIS的相关模块进行代码审查" |

最常见的流程就 4 步：**发任务、看进度、拿结果、继续改。**

它最核心的价值就这几件事：

- 你可以直接在 Claude Code 里把任务丢给 Codex
- Codex 跑完后，结果直接回到当前对话
- 长任务可以挂后台
- 同一个任务可以继续续跑，而不是每次重新解释上下文
- review、分析、修复可以接进同一条开发链路



```bash
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
```


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


`/codex:setup --enable-review-gate`；
这个的原理应该是构建了一个hook。

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

## 链接报错问题

codex 插件新建对话时，一直 提示 Timeout waiting for child process to exit 的原因找到了，因为codex 默认使用 WebSockets，在连接五次失败之后转成 https
把 codex 的 config.toml改成  默认 WebSockets 的设置关闭就好
