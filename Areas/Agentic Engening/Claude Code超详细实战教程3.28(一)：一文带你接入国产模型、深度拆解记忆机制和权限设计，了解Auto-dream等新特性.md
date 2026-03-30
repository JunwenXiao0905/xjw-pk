---
theme: default
themeName: "默认主题"
title: "Claude Code超详细实战教程3.28(一)：一文带你接入国产模型、深度拆解记忆机制和权限设计，了解Auto-dream等新特性"
---


如果你正在为这些问题苦恼：
- Claude 官方订阅每月 $20，国内支付困难，账号稳定性存疑
- 听说 Claude Code 很强，但不知道怎么在国内用起来
- 想要尝试又怕出现安全问题，大模型直接删盘跑路
- 更新迭代太快，又有好多新特性

那这篇文章就是为你准备的。

> 本教程使用 **MiniMax Coding Plan** 作为模型服务，starter套餐<30￥/月
> 开发环境为 **Windows 11 + WSL2 (Ubuntu)**，更安全，更好的体验
> 更新时间：**2026/3/29**，涵盖 /loop、Auto-dream 等新特性
> Claude Code版本：**2.1.86**，跟紧版本，别掉队
>
> 💡 干货过多，建议**收藏后再阅读**，方便随时查阅命令和配置。

## 目录

**一、Windows 下的开发环境与工具推荐**

**二、Claude Code 安装与启动**

**三、基础使用方法**

**四、进阶功能**

1. CLAUDE.md 与记忆机制

2. 消息传递机制

3. 存储机制

4. 权限设计

5. Skills 技能

6. MCP Tools

7. 插件（Plugins）

8. 后台任务

9. Hooks 钩子

10. SubAgents

11. Git Worktrees 并行会话

12. Agent Teams

13. 自定义 Slash Commands

14. /loop 定时任务

15. 2026 能力升级

**五、总结**


---

# 一、Windows 下的开发环境与工具推荐

本教程的开发环境基于 **Windows 11 + WSL2 (Ubuntu)**。以下是推荐的开发工具：

![[Pasted image 20260329111651.png]]

| 工具            |  运行位置   | 用途        | 说明                                                       |
| ------------- | :-----: | --------- | -------------------------------------------------------- |
| **WSL2**      | Windows | Linux 子系统 | 在 Windows 中运行 Ubuntu Linux 环境。避免误删除文件，同时配合docker，开发体验更佳。 |
| **Alacritty** | Windows | GPU 加速终端  | 连接 WSL，极致的 GPU 渲染，毫秒级启动                                  |
| **Zed**       | Windows | 高性能编辑器    | 编辑 WSL 中的代码，GPU 渲染，VSCode 1GB+ vs Zed < 100MB            |
| **tmux**      |   WSL   | 终端复用      | 后台运行 Claude Code，断开连接后继续执行                               |
| **cc-switch** |   WSL   | 配置切换器     | 图形化切换不同的模型服务配置                                           |

## 1. WSL2 简介

WSL2（Windows Subsystem for Linux 2）是 Windows 的 Linux 子系统，提供接近原生的 Linux 性能。本教程使用 **Ubuntu** 发行版。

**安装方法**：

```powershell
# 在 PowerShell（管理员）中执行
wsl --install -d Ubuntu
```

安装完成后，重启电脑，按提示设置用户名和密码。


**拷贝文件**
在 Windows 文件管理器地址栏输入 `\\wsl$\Ubuntu\home\你的用户名\` 即可访问 WSL 文件系统，像操作本地文件一样直接拷贝。

**关闭/重启wsl**
```
	wsl --shutdown
```

## 2. Alacritty 简介（Windows 端）

Alacritty 是一个 GPU 加速的终端模拟器，在 **Windows 端运行**，用于连接 WSL。

**为什么选择 Alacritty？**
- **GPU 渲染**：利用显卡加速，滚动、渲染流畅无卡顿
- **极小内存占用**：相比传统终端，内存占用可忽略不计
- **毫秒级启动**：几乎感觉不到启动延迟

**安装方法**：

1. 从 Alacritty 官网 下载 Windows 版本安装
2. 按 `Win+R`，输入 `%APPDATA%`，在打开的文件夹中新建 `alacritty` 文件夹
3. 在 `alacritty` 文件夹中新建 `alacritty.toml` 文件（注意扩展名是 `.toml`，不是 `.txt`）
4. 将以下内容添加到`alacritty.toml`中，确保启动直达 WSL：

```
# 指定 Alacritty 默认启动的程序 = WSL Ubuntu
[terminal]
shell = { program = "wsl.exe", args = ["-d", "Ubuntu","-u","yourname","--cd", "~"] }

# 窗口外观配置
[window]
opacity = 0.9
dimensions = { columns = 100, lines = 30 }

[font]
size = 12.0

# 文本选择配置
[selection]
# 选中文字自动复制到剪贴板
save_to_clipboard = true
```

> **操作提示**：Alacritty 的操作逻辑与传统终端有所不同：
> - 选中文字后**自动复制**到剪贴板（无需 Ctrl+C）
> - 粘贴使用 **Ctrl+Shift+V**，而非 Ctrl+V
> - Ctrl+V 在终端中表示"等待输入下一个字符"（传统终端行为）

## 3. Zed 编辑器简介（Windows 端）

Zed 是新一代高性能编辑器，在 **Windows 端运行**，可直接编辑 WSL 中的代码。

**为什么选择 Zed？**
- **GPU 渲染**：整个编辑器使用 GPU 加速，滚动流畅
- **极致轻量**：内存占用极低。实测：同一 React 项目，VSCode 占用 1.2GB，Zed 仅 80MB
- **AI 集成**：内置 AI 助手，支持 Claude 等模型
- **启动速度**：冷启动仅需数百毫秒

**安装方法**：
从 官网 下载 Windows 版本安装

**编辑 WSL 项目**：
在 Zed 中打开远程路径 `\\wsl$\Ubuntu\home\你的用户名\projects\` 即可编辑 WSL 中的代码。

## 4. tmux 简介（WSL 端）

tmux 是一个终端复用工具，在 **WSL 中运行**，可以让 Claude Code 在后台持续运行。

**安装方法**：

```bash
sudo apt update
sudo apt install tmux -y
```
**创建配置文件**  
在 WSL 终端中运行以下命令，在 home 目录创建一个空白配置文件：

```
touch ~/.tmux.conf
```

**添加基础配置**  
用你喜欢的编辑器（如 `nvim` 或 `nano`）打开这个文件，可以粘贴一些常用配置来测试效果，例如修改前缀键和启用鼠标支持 ：

```
# 修改前缀键为 Ctrl+a (默认是 Ctrl+b)
# set -g prefix C-a
# unbind C-b
# bind C-a send-prefix

# 开启鼠标支持 (可以用鼠标点击切换窗格、调整大小)
set -g mouse on

# 设置窗口索引从 1 开始 (默认是 0)
set -g base-index 1
setw -g pane-base-index 1
```

**自动启动（可选）**
在 `~/.bashrc` 末尾添加 `[[ -z "$TMUX" ]] && exec tmux`。

**常用命令**：
你必须记住 **Prefix（前缀键）**：`Ctrl + b`。 在 tmux 中，几乎所有指令都需要先按这个组合键，松开后再按功能键。

tmux 的核心逻辑在于分层：**Session（会话）** > **Window（窗口）** > **Pane（窗格）**。

| 命令                            | 说明              |
| ----------------------------- | --------------- |
| `tmux new -s claude`          | 创建名为 claude 的会话 |
| `tmux attach -t claude`       | 连接到 claude 会话   |
| `tmux ls`                     | 列出所有会话          |
| `tmux kill-session -t claude` | 终止 claude 会话    |
| `Ctrl+b, D`                   | 分离当前会话（会话继续运行）  |
| `Ctrl+b,c`                    | 新建窗口            |
| `Ctrl+b,%`                    | 左右平分窗口          |
| `Ctrl+b,"`                    | 上下平分窗口          |
| `Ctrl+d`                      | 关闭窗口            |
**错误提醒**：新手常犯的错误是在 tmux 会话里嵌套输入 `tmux` 命令。如果你已经在会话中，想创建新会话，请先 `exit` 出来，或者使用快捷键。
## 5. cc-switch 简介

cc-switch 是一个 Claude Code 配置切换器，提供图形化界面管理不同的模型服务配置。

**安装方法**：详见 三、cc-switch

> 💡 **提示**：本教程后续所有 Claude Code 实战操作均在本章配置的 Ubuntu 环境中进行。建议先完成环境搭建，再继续阅读。

---

# 二、Claude Code 安装与启动

## 1.安装

**方式一：原生安装（推荐）**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

原生安装无需 Node.js 环境，启动更快，是官方推荐的方式。

**方式二：npm 安装**

需要先安装 Node.js（v18.0 或更高版本）：

```bash
npm install -g @anthropic-ai/claude-code
```

**查看版本号**：

```bash
# 查看已安装版本
claude --version

# 查看 npm 最新版本
npm view @anthropic-ai/claude-code version

# 原生安装更新
claude --update
```

## 2.获取MinMax coding plan

👉 MiniMax Coding Plan 可享优惠

初次开发者，可以选择购买 Starter 套餐：600次模型调用 / 5小时，支持最新 MiniMax M2.7。
![[Pasted image 20260328140644.png]]



## 3.安装cc-switch

### 3.1 下载Ubuntu安装包


【请在此处插入图片】

下载到`~`目录，执行以下命令以安装

```
sudo dpkg -i CC-Switch-*.deb
```

根据提示输入密码。可能会出现报错

```
dpkg: error processing package cc-switch (--install):
 dependency problems - leaving unconfigured
Processing triggers for hicolor-icon-theme (0.17-2) ...
Errors were encountered while processing:
 cc-switch
```

**deb 包依赖缺失问题**，系统提示 `cc-switch` 需要 `libayatana-appindicator3-1` 和 `libwebkit2gtk-4.1-0` 这两个库，但当前系统里没有安装，

```
sudo apt-get update && sudo apt-get -f install -y
```

验证是否安装成功

```
dpkg -l | grep cc-switch
```

运行

```
cc-switch
```

### 3.2 创建配置文件

在图形化界面中选择`Claude` ，点击+号，选择MinMax提供商

![[Pasted image 20260328141012.png]]

![[Pasted image 20260328143557.png]]

添加 key，并配置模型。
![[Pasted image 20260328141340.png]]


点击启用。

![[Pasted image 20260328141318.png]]
## 4.绕过登录

初次使用 claude code 时，可能会强制要求登录 Anthropic 账户。

【请在此处插入图片】

请按以下步骤操作以跳过该流程：

定位用户主目录下的 `.claude.json` 文件，具体路径：wsl: `~/.claude.json`

将`hasCompletedOnboarding` 字段的值设置为 `true`，保存文件

```
{
  "hasCompletedOnboarding": true
}
```

## 5.启动

打开终端，并进入项目所在的目录。运行以下命令启动程序 Claude Code：

```
cd path/to/your_project
claude
```

启动后，需要授权 Claude Code 执行文件。

【请在此处插入图片】

输入`/status`确认模型、Base URL、API Key 是否配置正确。

![[Pasted image 20260328143148.png]]

## 6. 切换模型

1. **启动 Claude Code 时切换**：在终端执行`claude --model <模型名称>`指定模型并启动 Claude Code，例如`claude --model qwen3.5-plus。
2. **会话期间**：在对话框输入`/model <模型名称>`命令切换模型，例如`/model  MinMax-2.5`。

## 7.初始化

```
/init
```
会自动生成CLAUDE.md文件。

> 到这里你已经可以使用 Claude Code 协助任务了。比如：帮你审查代码、解释某个功能、调试 Bug，或者让它帮你写一个测试用例。

# 三、基础使用方法

> 掌握以下方法，才能充分发挥 Claude Code 的实力。
### 1.常见命令一览表

以下命令在 Claude Code 的**输入框中输入**调用：

> 🆕 标注的是近期新增的命令。⭐是必须掌握的命令

| 分类     | 命令             | 说明                                             | 备注                     |
| :----- | -------------- | ---------------------------------------------- | ---------------------- |
| **会话** | `/help`        | 显示帮助和可用命令                                      |                        |
|        | `/clear`       | 清除对话历史                                         | 别名：`/reset`、`/new`     |
|        | `/resume`      | 恢复之前的对话                                        | 别名：`/continue`         |
|        | ⭐`/branch`     | 创建对话分支                                         | 别名：`/fork`             |
|        | `/rename`      | 重命名当前会话                                        |                        |
|        | `/exit`        | 退出 CLI                                         | 别名：`/quit`             |
|        | ⭐`/btw`        | 提问而不添加到对话                                      | 🆕 旁注问题                |
|        | `/export`      | 导出当前对话                                         |                        |
| **项目** | ⭐`/init`       | 初始化项目，生成 CLAUDE.md 文件                          |                        |
|        | `/status`      | 查看版本、模型、账户、连接状态                                |                        |
|        | `/config`      | 打开设置界面                                         | 别名：`/settings`         |
|        | `/context`     | 可视化当前上下文使用情况                                   | 🆕                     |
|        | `/cost`        | 显示 Token 使用统计                                  |                        |
| **模型** | `/model`       | 切换 AI 模型                                       | 支持 Opus、Sonnet、Haiku   |
|        | `/effort`      | 设置模型努力级别（Claude Opus 4.6 和 Claude Opus 4.5 支持） | 🆕 low/medium/high/max |
|        | `/fast`        | 切换快速模式                                         | 🆕                     |
| **记忆** | ⭐`/memory`     | 编辑 CLAUDE.md 记忆文件                              |                        |
| **执行** | ⭐`/plan`       | 进入规划模式                                         |                        |
|        | ⭐`/rewind`     | 回滚对话或代码                                        | 别名：`/checkpoint`       |
|        | ⭐`/diff`       | 打开差异查看器                                        | 显示未提交的更改               |
|        | `/compact`     | 压缩对话历史                                         | 可附加指令聚焦压缩              |
| **扩展** | `/mcp`         | 管理 MCP 服务器连接                                   |                        |
|        | `/skills`      | 列出可用的技能                                        |                        |
|        | `/agents`      | 管理子代理配置                                        |                        |
|        | `/hooks`       | 查看钩子配置                                         |                        |
|        | `/permissions` | 查看或更新权限                                        | 别名：`/allowed-tools`    |
| **调试** | `/doctor`      | 诊断安装和设置问题                                      |                        |
|        | `/debug`       | 为当前会话启用调试日志记录                                  |                        |
| **界面** | `/theme`       | 更改颜色主题                                         |                        |
|        | `/vim`         | 切换 Vim 编辑模式                                    |                        |
|        | `/voice`       | 切换语音听写                                         | 需要 Claude.ai 账户        |
| **技能** | `/loop`        | 按间隔重复运行提示，轮询部署、监督 PR 等                         | 🆕 定时任务                |
|        | `/batch`       | 并行编排大规模更改，在隔离的 worktree 中生成后台代理                | 🆕                     |
|        | `/simplify`    | 审查最近更改的文件，查找代码重用、质量和效率问题                       |                        |
|        | `/claude-api`  | 加载 Claude API 参考资料                             |                        |


**调用示例**：
```
你：/status
Claude：Claude Code v2.x.x | Model: MinMax2.7 

你：/model haiku
Claude：已切换到 haiku 模型

你：/compact 请保留所有代码实现细节
Claude：正在压缩对话历史...
```

### 2.快捷键

| 分类 | 快捷键                     | 功能说明                 |
| :-- | ----------------------- | -------------------- |
| **输入** | ⭐`!`                    | 进入 Bash 模式           |
|      | ⭐`/`                    | 显示命令列表               |
|      | ⭐`@`                    | 输入文件路径               |
|      | ⭐`\` + `Enter`          | 换行输入（alter+enter 也可） |
|      | `Esc` `Esc`             | 清空输入（Bash 模式下双击）     |
|      | `Ctrl` + `V`            | 粘贴图片                 |
|      | `Ctrl` + `S`            | 暂存当前输入               |
|      | ⭐`Ctrl` + `G`           | 在编辑器中编辑输入            |
|      | ⭐`Ctrl` + `Shift` + `-` | 撤销输入                 |
|      | `Ctrl` + `U`            | 清除整行                 |
|      | `Ctrl` + `W`            | 删除前一个词               |
| **权限** | `Shift` + `Tab`         | 切换权限模式（自动接受编辑）       |
| **输出** | `Ctrl` + `O`            | 显示详细输出               |
| **会话** | ⭐`Ctrl` + `Z`           | 关闭当前会话               |
|      | `Ctrl` + `C` double     | 关闭当前会话               |
| **视图** | `Ctrl` + `T`            | 切换任务视图               |
| **模型** | `Meta` + `P`            | 切换模型                 |

> **提示**：`Meta` 键在 Windows/Linux 上通常是 `Alt`，在 macOS 上是 `Cmd`。

### 3.启动历史对话

cd 进入到工作目录，执行命令
```
claude --resume
```


### 4.图片输入

方式一：直接拖放

方式二：根据路径在对话中引用

你：@screenshot.png 分析这个页面的 UI 设计

方式三：粘贴截图

ctrl+v（不同终端可能不一样，我的是alt+v）

### 5.内置工具

Claude Code 内置了丰富的工具集（截至 2026年3月）：

| 分类     | 工具                       | 用途                      | 需要权限 |
| :----- | ------------------------ | ----------------------- | :--: |
| **文件** | **Read**                 | 读取文件内容                  |  ❌   |
|        | **Write**                | 创建或覆盖文件                 |  ✅   |
|        | **Edit**                 | 对文件进行针对性编辑              |  ✅   |
|        | **Glob**                 | 基于模式匹配查找文件              |  ❌   |
|        | **Grep**                 | 在文件内容中搜索模式              |  ❌   |
|        | **NotebookEdit**         | 修改 Jupyter notebook 单元格 |  ✅   |
|        | **LSP** 🆕               | 语言服务器代码智能（类型错误、跳转定义等）   |  ❌   |
| **命令** | **Bash**                 | 执行 shell 命令             |  ✅   |
|        | **WebFetch**             | 获取指定 URL 的内容            |  ✅   |
|        | **WebSearch**            | 执行网络搜索                  |  ✅   |
| **任务** | **TaskCreate** 🆕        | 在任务列表中创建新任务             |  ❌   |
|        | **TaskGet** 🆕           | 获取特定任务的完整详情             |  ❌   |
|        | **TaskList** 🆕          | 列出所有任务及其状态              |  ❌   |
|        | **TaskOutput** 🆕        | 获取后台任务的输出               |  ❌   |
|        | **TaskStop** 🆕          | 终止运行中的后台任务              |  ❌   |
|        | **TaskUpdate** 🆕        | 更新任务状态、依赖、详情            |  ❌   |
|        | **TodoWrite**            | 管理会话任务清单                |  ❌   |
|        | **CronCreate** 🆕        | 在当前会话中调度周期性任务           |  ❌   |
|        | **CronDelete** 🆕        | 取消调度的任务                 |  ❌   |
|        | **CronList** 🆕          | 列出会话中所有调度任务             |  ❌   |
| **代理** | **Agent**                | 生成子代理处理独立任务             |  ❌   |
|        | **EnterPlanMode**        | 切换到规划模式设计实现方案           |  ❌   |
|        | **ExitPlanMode**         | 提交方案审批并退出规划模式           |  ✅   |
|        | **EnterWorktree**        | 创建隔离的 git worktree      |  ❌   |
|        | **ExitWorktree**         | 退出 worktree 会话          |  ❌   |
|        | **ToolSearch** 🆕        | 搜索并加载延迟工具               |  ❌   |
| **交互** | **AskUserQuestion**      | 向用户提问以澄清需求              |  ❌   |
|        | **Skill**                | 在主对话中执行技能               |  ✅   |
|        | **ListMcpResourcesTool** | 列出 MCP 服务器暴露的资源         |  ❌   |
|        | **ReadMcpResourceTool**  | 通过 URI 读取 MCP 资源        |  ❌   |

> 💡 **说明**：权限可在 `/permissions` 或 permission settings 中配置。🆕 标记为近期新增功能。

**调用方式**：内置工具由 Claude Code **自动调用**，无需用户手动触发。当你的请求需要某项操作时，Claude 会自动选择合适的工具执行。

```
你：帮我读取 package.json 文件
Claude：[自动调用 Read 工具]
       已读取 package.json，内容如下...

你：在 src 目录下创建 utils.ts 文件
Claude：[自动调用 Write 工具]
       已创建 src/utils.ts

你：搜索一下 Claude Code 的最新特性
Claude：[自动调用 WebSearch 工具]
       正在搜索...
```

### 6.内置加载词

Claude Code 在 AI 思考时会显示有趣的随机动词，比如：

```
Transmuting... (Thinking)
Swooping... (thought for 3s)
Flibbertigibbeting... (Thinking)
Shenaniganing... (thought for 5s)
```

这些加载词共 225 个，硬编码在 `cli.js` 的 `Q51` 数组中，官方没有提供配置选项。

【请在此处插入图片】

**自定义加载词**：原生安装和 npm 安装都可以修改，方法相同。

将一下提示词给到Claude Code，执行成功后重启：

```
1. 找到 cli.js 路径：
find ~/.local/share/pnpm/global -name "cli.js" -path "*claude-code*" | head -1

2. 备份原文件：
cp <cli.js路径> <cli.js路径>.bak

3. 替换 Q51 数组为自定义词：
Q51=["正在思考","正在分析","正在编码","正在优化"]
```

### 7.配置默认编辑器

直接给claude code说，配置claude code默认编辑器为zed。它会自行修改。

也可以用编辑器打开`~/.claude/settings.json`，并增加以下配置：
```
    {
       "env": {
		 其他配置.......
         "EDITOR": "zed --wait",
         "VISUAL": "zed --wait"
       },
    }
```

# 四、进阶功能
## 1. CLAUDE.md 与记忆机制

CLAUDE.md 是 Claude Code 的”记忆文件”，用于存储项目特定的指令、编码规范、架构决策等信息。一般存在以下目录：
```
your-project/  
├── CLAUDE.md              ← 项目级（团队共享，提交到 Git）  
├── .claude/  
│   └── settings.json  
├── src/  
└── package.json  
  
~/.claude/  
├── CLAUDE.md              ← 用户级（个人偏好，不进 Git）
```
你也可以在任意子目录（如 `src/`、`tests/`）中添加 CLAUDE.md 文件，这些文件会在你操作对应目录的文件时按需加载。

> 作为用户消息在系统提示之后传递，而不是系统提示本身的一部分。Claude 读取它并尝试遵循它，但没有严格遵守的保证，特别是对于模糊或冲突的指令。

### 1.1 逐层加载机制

Claude Code 会从当前目录逐级向上查找 `CLAUDE.md` 文件，并将所有找到的内容合并加载。子目录中的 CLAUDE.md 文件在 Claude 读取这些目录中的文件时按需加载。

**加载顺序**（优先级从高到低）：

```
┌─────────────────────────────────────────────────────────────────┐
│  1. 管理策略级（最高优先级）                                        │
│     Linux: /etc/claude-code/CLAUDE.md                           │
│     macOS: /Library/Application Support/ClaudeCode/CLAUDE.md    │
│     Windows: C:\Program Files\ClaudeCode\CLAUDE.md              │
│     → 组织级规则，由 IT 部署，不可被用户排除                          │
├─────────────────────────────────────────────────────────────────┤
│  2. 用户级                                                        │
│     ~/.claude/CLAUDE.md                                          │
│     → 个人偏好设置，适用于所有项目                                   │
├─────────────────────────────────────────────────────────────────┤
│  3. 项目级                                                        │
│     ./CLAUDE.md 或 ./.claude/CLAUDE.md                           │
│     → 项目架构、编码标准、常见工作流（可提交到 git 共享）               │
├─────────────────────────────────────────────────────────────────┤
│  4. 子目录级（按需加载）                                            │
│     ./src/CLAUDE.md, ./tests/CLAUDE.md 等                        │
│     → 仅在读取该目录文件时加载                                       │
└─────────────────────────────────────────────────────────────────┘
```
如果需要排除特定的 CLAUDE.md 文件或规则目录，可以配置 `claudeMdExcludes`。将其添加到 `.claude/settings.local.json` 以使排除仅作用于本地机器：

```
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

### 1.2 创建和修改记忆

**创建 CLAUDE.md**：

对于一个存量项目，可以使用 `/init` 命令自动生成：

```
你：/init
Claude：正在分析项目结构...
       已生成 CLAUDE.md，包含以下内容：
       - 技术栈信息
       - 项目结构
       - 编码规范
```

**修改 CLAUDE.md**：

使用 `/memory` 命令可以查看和编辑：

```
你：/memory
  Memory

    Auto-memory: on
    Auto-dream: off

  ~/.claude/rules/agents.md
  ~/.claude/rules/performance.md
  Project memory (./CLAUDE.md)
```
>上下箭头选中，enter通过编辑器打开

### 1.3 编写有效指令

CLAUDE.md 文件在每个会话开始时加载到上下文窗口中，与你的对话一起消耗token。因为它们是上下文而不是强制配置，你编写指令的方式会影响 Claude 遵循它们的可靠性。具体、简洁、结构良好的指令效果最好。

**大小**：每个 CLAUDE.md 文件目标在 200 行以下。较长的文件消耗更多上下文并降低遵守度。如果你的指令变得很大，使用 文件引入或 `.claude/rules/`文件进行分割。

**一致性**：如果两条规则相互矛盾，Claude 可能会任意选择一条。

**文件引入**：要引入 README、package.json 和工作流指南，在你的 CLAUDE.md 中的任何地方使用 `@` 语法引用它们：

```
有关项目概述，请参阅 @README，有关此项目的可用 npm 命令，请参阅 @package.json。

# 其他指令
- git 工作流 @docs/git-instructions.md
```

**注释**：块级 HTML 注释（`<!-- maintainer notes -->`）在 CLAUDE.md 文件中在内容注入到 Claude 的上下文之前被剥离。使用它们为人类维护者留下笔记。
### 1.4 推荐的 CLAUDE.md 模板

以下是一个经过验证的 CLAUDE.md 模板，包含：

- **工作流编排**：何时规划、何时委托
- **子智能体策略**：如何有效使用 Agent
- **自我优化循环**：从错误中学习
- **完成前校验**：确保质量
- **核心原则**：简洁、安全、可维护

![[Pasted image 20260328145723.png]]

内容过长，可私信或留言获取。

### 1.5 rules

对于较大的项目，你可以使用 `.claude/rules/` 目录将指令组织到多个文件中。这使指令保持模块化并更容易让团队维护。

规则在每个会话或打开匹配文件时加载到上下文中。对于不需要始终在上下文中的特定任务指令，改用 skills，它仅在你调用它们或 Claude 确定它们与你的提示相关时加载。

**设置规则**

在你的项目的 `.claude/rules/` 目录中放置 markdown 文件。每个文件应涵盖一个主题，具有描述性文件名，如 `testing.md` 或 `api-design.md`。所有 `.md` 文件都被递归发现，因此你可以将规则组织到子目录中，如 `frontend/` 或 `backend/`：

```
your-project/
├── .claude/
│   ├── CLAUDE.md           # 主项目指令
│   └── rules/
│       ├── code-style.md   # 代码样式指南
│       ├── testing.md      # 测试约定
│       └── security.md     # 安全要求
```


**设置路径约束**

`roules`可以使用带有 `paths` 字段的 YAML frontmatter 范围限定到特定文件。这些条件规则仅在 Claude 处理与指定模式匹配的文件时适用。

```
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---

# API 开发规则

- 所有 API 端点必须包括输入验证
- 使用标准错误响应格式
- 包括 OpenAPI 文档注释
```

**用户级规则**

`~/.claude/rules/` 中的个人规则适用于你机器上的每个项目。使用它们来处理不是项目特定的偏好：

```
~/.claude/rules/
├── preferences.md    # 你的个人编码偏好
└── workflows.md      # 你的首选工作流
```

用户级规则在项目规则之前加载，给予项目规则更高的优先级。
****
### 1.6 /memory 功能

运行 `/memory` 命令可以：

| 操作  | 说明                             |
| --- | ------------------------------ |
| 查看  | 显示所有已加载的记忆来源                   |
| 编辑  | 打开对应文件进行编辑                     |
| 切换  | 开启/关闭 Auto-memory 和 Auto-dream |
![[Pasted image 20260328150133.png]]
### 1.7 Auto-memory

自动记忆会在以下情况触发：

| 触发条件 | 示例 |
|----------|------|
| 用户明确偏好 | "我喜欢用 tab 缩进" |
| 项目关键信息 | "这个项目用的是 PostgreSQL" |
| 重复出现的问题 | "每次都要问数据库配置" |
| 用户主动说"记住" | "记住：我是 GIS 工程师" |

> **存储位置**：`~/.claude/projects/<project>/memory/`，每个项目独立存储。

### 1.8 Auto-dream

Auto-dream 是 Auto-memory 的增强功能，允许 Claude 在会话空闲时自动整理和优化记忆内容。

**开启方式**：运行 `/memory`，在界面中切换 Auto-dream 开关。

**作用**：
- 自动整理碎片化记忆
- 合并相似内容
- 清理过时信息

> **注意**：Auto-dream 需要 Claude Code v2.1.59 或更高版本。
## 2. 消息传递机制

当你向 Claude Code 发送消息时，实际传递的内容比你想的更多。以下是完整的消息结构：

### 2.1 消息结构概览

```

  ├─ System Prompt（系统提示）
  │  ├─ 系统指令（工具使用规范、行为准则等）
  │  ├─ 内置工具定义（Read, Edit, Bash 等）
  │  ├─ MCP Tools 列表
  │  └─ Skills 列表
  │
  ├─ User Message（用户消息）
  │  ├─ CLAUDE.md 内容（全局 rules + 项目级）
  │  ├─ Memory 内容（MEMORY.md + 记忆文件）
  │  ├─ 上下文信息（工作目录、平台、git 状态等）
  │  └─ 用户原始输入
```


## 3. 存储机制

Claude Code 的存储系统可以用一句话概括：**按作用域分层存储，靠优先级覆盖生效**。

### 3.1 整体框架

```
~/.claude.json                      ← 用户全局配置（MCP 服务器、启动设置）
~/.claude/                          ← 用户级（你的所有项目）
├── settings.json                   ← 用户配置
├── CLAUDE.md                       ← 用户级记忆
├── rules/                          ← 用户级规则
├── agents/                         ← 用户级 SubAgent
├── skills/                         ← 用户级 Skills
│   └── <skill>/
│       └── references/             ← 技能参考文档
├── commands/                       ← 用户级命令
├── agent-memory/                   ← SubAgent 跨会话记忆
└── projects/                       ← 项目级会话历史
    └── <project-hash>/
        ├── <session-id>.jsonl      ← 对话历史
        └── memory/
            ├── MEMORY.md           ← 自动记忆索引
            └── *.md                ← 记忆文件

项目/.claude/                       ← 项目级（团队共享）
├── settings.json                   ← 项目配置
├── settings.local.json             ← 本地配置（gitignore）
├── CLAUDE.md                       ← 项目记忆
├── rules/                          ← 项目规则
├── agents/                         ← 项目 SubAgent
├── skills/                         ← 项目 Skills
└── commands/                       ← 项目命令

/etc/claude-code/                   ← 系统级（IT 部署，Managed）
└── managed-settings.json
```

### 3.2 对话历史存储

对话历史是 Claude Code 最重要的数据，存储在：

```
~/.claude/projects/<项目路径哈希>/
├── <会话ID1>.jsonl    ← 会话1的完整历史
├── <会话ID2>.jsonl    ← 会话2的完整历史
└── memory/
    └── MEMORY.md      ← 该项目的自动记忆

~/.claude/sessions/
└── sessions.json      ← 会话索引（ID、名称、时间）
```

**恢复历史对话**：
```bash
claude --resume                    # 命令行恢复
/init                              # 交互式选择
```

**会话清理**：在 `settings.json` 中配置 `cleanupPeriodDays`（默认 30 天）



## 4. 权限设计

### 4.1 Claude Code 4种权限模式

- **default**: 默认只读，需要执行写命令时进行询问
- **plan**: 只读+规划模式，通常不会执行实际代码
- **acceptEdits**: 具有读写文件的权限，无需批准。但是执行 Bash 命令时仍然需要批准
- **bypassPermissions**: 读写权限+Bash 命令执行权限，跳过所有权限提示（危险⚠️）

**_提示：_** _上述四种权限中_ `_default_`_、_`_plan_`_、_`_acceptEdits_` _可以通过_ `_Shift+Tab_` _快捷键在 Claude Code 内部进行切换。_`_bypassPermissions_` _权限需要在启动 Claude 时添加_ `_--dangerously-skip-permissions_` _参数。_

### 4.2 权限控制

上述的四种模式提供了宏观的控制，在 `settings.json` 文件中可以进行更加细微的权限控制。对于具体的命令，有 3 种权限，分别是 `deny`、`allow` 和 `ask`。`deny` 的命令一定不执行，`allow` 的命令允许执行，`ask` 的命令需要问了才知道。

**实战示例：将常用工具设置为自动允许**

在 `~/.claude/settings.json` 中添加以下配置，免除频繁的权限确认：

```json
{
  "permissions": {
    "allow": [
      "WebFetch",
      "WebSearch",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(git:status:*)"
    ]
  }
}
```

或使用 `/permissions` 命令交互式添加：
```
你：/permissions
Claude：当前权限配置...
       添加新规则：allow WebFetch
       添加新规则：allow WebSearch
       添加新规则：allow Bash(ls:*)
```

## 5. Skills 技能

### 5.1 Skills 是什么

Skills 是预定义的工作流或 prompt 模板，用于封装可复用的开发流程。

**特点**：
- 通过 `Skill` 工具自动或手动调用
- 在 system-reminder 中列出，每条消息都会携带完整列表
- 可包含 prompt、脚本、参考文档等

**调用方式**：

```
你：/brainstorming 我想设计一个用户认证系统
Claude：[自动调用 brainstorming skill]
       正在进行头脑风暴...
```

或通过自然语言触发：
```
你：帮我对这个功能进行头脑风暴
Claude：[检测到关键词，自动调用 brainstorming skill]
```

### 5.2 安装 Skills

**方式一：自然语言安装**
```
你：帮我安装一个 skill，地址是 GitHub 上的 pptx 仓库
Claude：正在安装 pptx skill...
       安装完成！
```

**方式二：手动安装**

下载 Skill 文件，复制到以下目录：

```
# 用户级（所有项目可用）
~/.claude/skills/
└── your-skill/
    ├── SKILL.md          # 必需：Skill 定义文件
    ├── scripts/          # 可选：脚本文件
    └── references/       # 可选：参考文档

# 项目级（仅当前项目）
.claude/skills/
└── your-skill/
    └── SKILL.md
```

**方式三：SkillHub 安装**

访问 SkillHub 或 SkillsMP，搜索并安装所需 Skills。
### 5.3 热门 Skills 推荐


**前端开发类**

| Skill                    | 说明                                                           |
| ------------------------ | ------------------------------------------------------------ |
| **frontend-design**      | ⭐ 首推。解决 Claude 生成千篇一律 UI（Inter字体+紫色渐变）的问题，强制先确定设计方向：字体、配色、动效 |
| **composition-patterns** | Vercel Labs 出品，解决组件 Boolean prop 泛滥问题，教你用组合模式设计可复用组件         |
| **react-best-practices** | React 最佳实践，hooks 使用、性能优化、组件设计                                |
| **webapp-testing**       | Web 应用测试，配合 Playwright 进行 E2E 测试                             |
| **screenshot**           | 网页截图与视觉验证，调试 UI 必备                                           |

**工作提效类**

| Skill                | 说明                                                                |
| -------------------- | ----------------------------------------------------------------- |
| **Superpowers**      | ⭐ 93k+ stars，包含 brainstorming、TDD、systematic-debugging 等 14 个自动技能 |
| **simplify**         | 代码简化工具，作为最终检查，删除冗余、提升可维护性                                         |
| **pptx**             | 生成专业 PowerPoint 演示文稿                                              |
| **pdf**              | PDF 文件操作与处理                                                       |
| **Composio/Connect** | 集成 850+ SaaS 应用（Gmail、Slack、Notion），自动处理 OAuth                    |

**安装命令**

```bash
# 官方技能包（包含 frontend-design、pptx、pdf、screenshot 等）
/plugin marketplace add anthropics/skills

# Superpowers 插件
/plugin marketplace add obra/superpowers-marketplace

# Composio 集成
/plugin marketplace add composio/connect
```

> 💡 **最佳实践**：如果你发现某个工作流需要反复向 Claude 解释，那就是创建自定义 skill 的最佳时机。使用 `/skill-creator` 交互式创建。

---

## 6. MCP Tools

### 6.1 MCP 是什么

MCP (Model Context Protocol) 是连接 Claude Code 与外部服务的协议。通过 MCP，Claude 可以：
- 操作 GitHub 仓库
- 查询数据库
- 发送 Slack 消息
- 访问 Google Drive 文件

### 6.2 安装 MCP

```bash
# 安装 GitHub MCP
claude mcp add github -- npx -y @anthropic-ai/mcp-server-github

# 查看已安装的 MCP
claude mcp list

# 删除 MCP
claude mcp remove github
```

### 6.3 热门 MCP 工具推荐

| MCP | 功能 | 安装命令 |
|-----|------|----------|
| **GitHub** | 仓库操作、Issue、PR 管理 | `claude mcp add github -- npx -y @anthropic-ai/mcp-server-github` |
| **Excalidraw** | 绘制架构图、流程图、时序图 | `claude mcp add excalidraw -- npx -y @anthropic-ai/mcp-server-excalidraw` |
| **Brave Search** | 网页搜索、实时信息 | `claude mcp add brave-search -- npx -y @anthropic-ai/mcp-server-brave-search` |
| **Puppeteer** | 浏览器自动化、截图、E2E 测试 | `claude mcp add puppeteer -- npx -y @anthropic-ai/mcp-server-puppeteer` |

> 💡 **提示**：GitHub 和 Brave Search 需要配置 API Key，Excalidraw 和 Puppeteer 无需额外配置。

---

## 7. 插件（Plugins）

### 7.1 插件是什么

插件是打包好的功能集合，可以包含：
- Skills（技能）
- Commands（命令）
- Hooks（钩子）
- Agents（子代理）

### 7.2 推荐插件

**Superpowers** ⭐ 16k+ Stars

全流程覆盖的 Skills 集合，让 AI 像专业工程师一样工作。

```bash
# 注册市场
/plugin marketplace add obra/superpowers-marketplace

# 安装插件
/plugin install superpowers@superpowers-marketplace
```

**包含的 Skills**：

| 场景 | Skill |
|------|-------|
| 开始任何任务前 | using-superpowers |
| 创建功能前 | brainstorming |
| 实现功能 | test-driven-development |
| 遇到 Bug | systematic-debugging |
| 完成后请求审查 | requesting-code-review |
| 收到审查反馈 | receiving-code-review |


---


## 8. 后台任务

Claude Code 支持在后台运行长时间任务，便于你同时处理多项工作。

**启动后台任务**：Claude Code 会自动在需要时创建后台任务（如使用 `/batch` 批量处理时，自动启动前后端服务等）

**查看任务列表**：
```
你：/tasks
Claude：显示所有后台任务及其状态
```

**常用操作**：

| 命令 | 说明 |
|------|------|
| `/tasks` | 查看所有后台任务 |
| `TaskStop` | 终止运行中的后台任务 |
| `TaskOutput` | 获取后台任务的输出 |

---

## 9. Hooks 钩子

Hooks 让你在 Claude Code 执行操作前后自动运行代码。

**典型用途**：
- 文件保存后自动格式化（Prettier）
- 编辑后自动类型检查
- 提交前自动 lint

### 9.1 可用事件

| 事件名 | 触发时机 | 使用场景 |
|--------|----------|----------|
| **SessionStart** | 会话开始 | 加载开发上下文、设置环境变量 |
| **PreToolUse** | 工具执行前 | 验证或阻止危险命令 |
| **PostToolUse** | 工具执行后 | 代码格式化、运行测试 |
| **Stop** | 响应完成时 | 检查任务是否完成 |
| **SessionEnd** | 会话结束 | 清理任务、记录统计 |

### 9.2 配置 Hooks

在 `settings.json` 中配置：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

---

## 10. SubAgents

Subagents 是处理特定类型任务的专门 AI 助手。每个 subagent 在自己的 context window 中运行，具有自定义系统提示、特定的工具访问权限和独立的权限。

**查看内置 Agents**

```
/agents
```



| Agent                    | 功能          | 工具权限                    | 推荐场景         |
| ------------------------ | ----------- | ----------------------- | ------------ |
| **general-purpose**      | 通用任务处理      | 全部工具                    | 搜索代码、执行多步骤任务 |
| **Explore**              | 快速探索代码库     | 只读工具                    | 查找文件、搜索关键词   |
| **Plan**                 | 实现方案规划      | 只读工具                    | 设计架构、制定实施计划  |


**自动委托**

Claude 根据请求中的任务描述、subagent 配置中的 `description` 字段和当前上下文自动委托任务。

**主动调用**

当自动委托不够时，也可以自己请求 subagent。常用两种模式调用：

- **自然语言**：在提示中命名 subagent；Claude 决定是否委托
- **@-subagent**：保证 subagent 为一个任务运行

对于自然语言，没有特殊语法。命名 subagent，Claude 通常会委托：

```
使用 test-runner subagent 修复错误的测试
```

@subagent ：输入 `@` 并从类型提前中选择 subagent，就像 @文件一样。这确保特定 subagent 运行，而不是将选择留给 Claude：

![[Pasted image 20260329092002.png]]

**创建 SubAgent**

在 `.claude/agents/` 目录中创建 Markdown 文件，或使用 `/agents` 命令交互式创建：

**步骤一：打开界面**

```
/agents
```

**步骤二：选择位置**
- **Personal**：保存到 `~/.claude/agents/`，所有项目可用
- **Project**：保存到 `.claude/agents/`，仅当前项目可用

**步骤三：描述 SubAgent**

选择 **Generate with Claude**，输入描述：

```
一个代码改进代理，扫描文件并提出可读性、性能和最佳实践方面的改进建议。
它会解释每个问题，展示当前代码，并提供改进版本。
```

**步骤四：选择工具**

| 工具类型 | 说明 |
|----------|------|
| **Read-only tools** | 仅读取文件，适合审查者 |
| **Write/Edit tools** | 可修改文件，适合实现者 |
| **Bash tools** | 可执行命令 |

**步骤五：选择模型**

| 模型 | 适用场景 |
|------|----------|
| **Haiku** | 轻量任务，快速响应 |
| **Sonnet** | 平衡能力与速度 |
| **Opus** | 复杂推理任务 |

**步骤六：配置内存**

- **User scope**：持久记忆，存储在 `~/.claude/agent-memory/`
- **None**：不保留跨会话学习

**步骤七：保存并测试**

按 `s` 或 `Enter` 保存，然后测试：

```
使用 code-improver agent 分析这个项目的代码
```



## 11. Git Worktrees 并行会话

当你需要同时处理多个任务时，每个 Claude 会话需要独立的代码副本。Git worktrees 创建隔离的工作目录，让多个 Claude 会话并行工作而不冲突。

使用 `--worktree`（`-w`）标志创建隔离的 worktree 并在其中启动 Claude。传递的值成为 worktree 目录名称和分支名称：

```bash
# 方式一：使用 --worktree 标志创建并进入
claude --worktree feature-auth

# 方式二：在会话中让 Claude 自动创建
你：创建一个 worktree 来处理新功能
```

**工作原理**：
- Worktree 在 `.claude/worktrees/<name>/` 创建
- 自动从默认分支创建新分支
- 退出时：无更改自动清理；有更改提示保留或删除

**Tip**：将 `.claude/worktrees/` 添加到 `.gitignore`

### 11.1 /batch 批量并行处理

`/batch` 命令用于大规模并行修改，自动为每个任务创建独立的 worktree：

```
你：/batch 修复以下文件的类型错误：
- src/components/Button.tsx
- src/components/Input.tsx
- src/components/Modal.tsx
```

**工作流程**：

```
/batch 触发
    ↓
创建多个独立 worktree（每个文件一个）
    ↓
每个 worktree 运行一个后台 Agent
    ↓
Agent 并行处理各自任务
    ↓
汇总结果，合并更改到主分支
```

**适用场景**：
- 批量修复多个文件的同类问题
- 多模块并行开发
- 大规模重构

**注意**：`/batch` 适合互不依赖的独立任务，有依赖关系的任务请使用 `/plan` 或 Agent Teams。

---

## 12. Agent Teams

Agent Teams 是一组协作的 AI 代理，每个代理有自己的角色、工具和上下文。

### 12.1 创建团队

```
你：/team-create
Claude：请输入团队名称：frontend-team
       请输入团队描述：前端开发团队
       团队已创建！
```

### 12.2 创建和分配任务

```
你：/task-create
Claude：请输入任务名称：实现登录页面
       请输入任务描述：使用 React 实现登录页面

你：帮我把这个任务分配给 reviewer
Claude：任务已分配给 reviewer 代理
```

### 12.3 协作模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **并行执行** | 多代理同时处理独立任务 | 大型重构、多模块开发 |
| **流水线** | 代理按顺序处理 | 代码审查 → 测试 → 部署 |
| **协作讨论** | 代理之间讨论决策 | 架构设计、技术选型 |

### 结合tmux使用

**提示词模板**：

```
组建三人团队，使用tmux管理，联系不上的及时kill，模型明确选择haiku/sonnet/opus。
任务描述：
1. xxx
2. 测试驱动
```


---

## 13. 自定义 Slash Commands

自定义 slash command 就是把你反复使用的 prompt 打包成命令。

**位置**：
- **项目级**：`./.claude/commands/`
- **用户级**：`~/.claude/commands/`

一个自定义指令对应一个 markdown 文件，文件名就是命令名称。

**参数类型**：

| 类型 | 语法 | 使用场景 |
|------|------|----------|
| 单参数 | `$ARGUMENTS$` | 不确定长度的自然语言描述 |
| 多参数 | `$1`, `$2`, `$3` | 固定顺序的结构化参数 |

**示例**（`.claude/commands/review.md`）：

```markdown
请对以下代码进行审查：
$ARGUMENTS$

重点关注：
- 代码规范
- 潜在 Bug
- 性能问题
```

**使用**：
```
你：/review src/auth.ts
Claude：正在审查 src/auth.ts...
```

---

## 14. /loop 定时任务

`/loop` 是 2026年3月 最实用的新功能之一，将 Claude Code 从"一次性对话助手"变成"持续运行的后台工作者"。

### 14.1 基本用法

```bash
# 每 5 分钟检查部署状态
/loop 5m 检查 staging 环境部署是否成功

# 每 30 分钟检查 PR
/loop 30m 检查所有开放的 PR，有新评论时通知我

# 每 1 小时生成代码质量报告
/loop 1h 扫描 src/ 目录的代码质量并总结潜在问题

# 默认间隔 10 分钟
/loop 监控 CI 流水线状态
```

### 14.2 典型应用场景

| 场景 | 命令示例 | 价值 |
|------|----------|------|
| **PR 监控** | `/loop 15m 检查 PR 是否有新评论或 CI 失败` | 自动化代码审查跟进 |
| **部署监控** | `/loop 5m 检查部署状态` | 实时检测部署失败 |
| **代码安全** | `/loop 1h 扫描新代码的安全问题` | 持续安全审计 |
| **日报生成** | `/loop 24h 总结昨天的代码变更` | 自动化团队日报 |

### 14.3 限制说明

- 单会话最多 50 个并发定时任务
- 任务 3 天后自动过期
- 会话关闭时所有任务终止
- 可通过环境变量禁用

---

## 15. 2026 能力升级

除了用户可见功能，底层能力也有重大升级：

### 15.1 模型与上下文

| 能力 | 说明 |
|------|------|
| **默认模型升级** | Opus 4.6 成为默认模型，推理能力大幅提升 |
| **128K 最大输出** | Opus 4.6 默认 64K，最大可达 128K tokens |
| **上下文压缩** | 自动压缩上下文，保持超长会话连贯性 |

### 15.2 功能时间线

| 功能 | 发布时间 | 状态 |
|------|----------|------|
| **Auto-dream** | 2026.03 | 灰度推送中 |
| **/loop** | 2026.03 | GA |
| **Background Agent** | 2026.02 | GA |
| **Plugins** | 2026.02 | GA |

> 💡 **说明**：Computer Use、Voice Mode、Remote Control 等功能需要 Claude Pro/Max 订阅，国产模型接入用户暂不可用。

---

# 五、总结

本教程从环境搭建、模型接入、基础操作到进阶功能，带你全面了解了 Claude Code 的核心用法。掌握了这些，你已经可以在日常开发中大幅提升效率。后续将推出工程化实践篇，介绍 Superpowers、OpenSpec 等插件和工具，打造真正的 AI 工作流。

*更新日期：2026/3/29*