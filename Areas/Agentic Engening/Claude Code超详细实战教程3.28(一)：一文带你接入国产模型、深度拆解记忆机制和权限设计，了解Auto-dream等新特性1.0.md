
如果你正在为这些问题苦恼：
- Claude 官方订阅每月 $20，国内支付困难，账号稳定性存疑
- 听说 Claude Code 很强，但不知道怎么在国内用起来
- 想要尝试又怕出现安全问题，大模型直接删盘跑路
- 更新迭代太快，又有好多新特性

那这篇文章就是为你准备的。

> 本教程使用 **MiniMax Coding Plan** 作为模型服务，starter套餐<30￥/月
> 开发环境为 **Windows 11 + WSL2 (Ubuntu)**，更安全，更好的体验
> 更新时间：**2026/3/26**，Auto-dream、/btw等特性都有介绍 
> Claude Code版本：**2.1.84**，跟紧版本，别掉队
> 
> 💡 干货过多，建议**收藏后再阅读**，方便随时查阅命令和配置。

## 目录

- [一、Windows 下的开发环境与工具推荐](#一windows-下的开发环境与工具推荐)
- [二、Claude Code 安装与启动](#二claude-code-安装与启动)
- [三、基础使用方法](#三基础使用方法)
- [四、进阶功能](#四进阶)
- [五、OpenSpec](#五openspec)
- [六、Everything-claude-code](#六everything-claude-code)
- [七、常见问题与排错](#七常见问题与排错)

---

# 一、Windows 下的开发环境与工具推荐

本教程的开发环境基于 **Windows 11 + WSL2 (Ubuntu)**。以下是推荐的开发工具：

![](优秀文章/diagrams/dev-environment.excalidraw)

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
通过win的资源管理器打开Ubuntu文件路径
（todo：补充一下）

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

1. 从 [Alacritty 官网](https://alacritty.org/) 下载 Windows 版本安装
2. 按 `Win+R`，输入 `%APPDATA%`，在打开的文件夹中新建 `alacritty` 文件夹
3. 在 `alacritty` 文件夹中新建 `alacritty.toml` 文件（注意扩展名是 `.toml`，不是 `.txt`）
4. 将一下内容添加到`alacritty.toml`中，确保启动直达 WSL：

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
从 [官网](https://zed.dev/download) 下载 Windows 版本安装

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

**安装方法**：详见 [三、cc-switch](#三cc-switch)

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

需要先安装 [Node.js](https://nodejs.org/en/download/)（v18.0 或更高版本）：

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

👉 此链接可享9折优惠：https://platform.minimaxi.com/subscribe/token-plan?code=7qlZPXuhpp&source=link

初次开发者，可以选择购买 Starter 套餐：600次模型调用 / 5小时，支持最新 MiniMax M2.7。
![[Pasted image 20260328140644.png]]



## 3.安装cc-switch

3.1 下载Ubuntu安装包

[https://github.com/farion1231/cc-switch/releases](https://github.com/farion1231/cc-switch/releases)

![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1772505180697-308d5d1b-afda-465b-88e4-5132c6fc479c.png)

下载到`~`目录，执行以下命令以安装

```
sudo dpkg -i CC-Switch-*.deb
```

提示输入密码。可能会出现报错

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

3.2 创建配置文件

在图形化界面中选择`Claude` ，点击+号，选择MinMax提供商

![[Pasted image 20260328141012.png]]

![[Pasted image 20260328143557.png]]

添加 key，并配置模型。
![[Pasted image 20260328141340.png]]


点击启用。

![[Pasted image 20260328141318.png]]
## 4.绕过登录

初次使用 claude code 时，可能会强制要求登录 Anthropic 账户。

![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1772419462306-5c618bd8-cc85-49bb-b2cc-3fe96155bc52.png)

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

![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1772419755877-c3bb45c3-3330-409f-bc0b-02e90bd029b8.png)

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

>到这里你已经可以使用claude code协助任务了。可以试试（todo：描述一个应用场景）

# 三、基础使用方法

> 掌握以下方法，才能充分发挥 Claude Code 的实力。
### 1.常见命令

以下命令在 Claude Code 的**输入框中输入**调用：

> 🆕 标注的是近期新增的命令。⭐是必须掌握的命令

(todo:查询截至到目前的更新日志，补齐。我记得是有一个/loop命令。并且对此表格进行分类)

| 命令             | 说明                                             | 备注                     |
| -------------- | ---------------------------------------------- | ---------------------- |
| `/help`        | 显示帮助和可用命令                                      |                        |
| `/clear`       | 清除对话历史                                         | 别名：`/reset`、`/new`     |
| ⭐`/init`       | 初始化项目，生成 CLAUDE.md 文件                          |                        |
| `/status`      | 查看版本、模型、账户、连接状态                                |                        |
| `/model`       | 切换 AI 模型                                       | 支持 Opus、Sonnet、Haiku   |
| `/config`      | 打开设置界面                                         | 别名：`/settings`         |
| ⭐`/memory`     | 编辑 CLAUDE.md 记忆文件                              |                        |
| `/compact`     | 压缩对话历史                                         | 可附加指令聚焦压缩              |
| `/cost`        | 显示 Token 使用统计                                  |                        |
| `/doctor`      | 诊断安装和设置问题                                      |                        |
| `/mcp`         | 管理 MCP 服务器连接                                   |                        |
| `/skills`      | 列出可用的技能                                        |                        |
| `/agents`      | 管理子代理配置                                        |                        |
| `/hooks`       | 查看钩子配置                                         |                        |
| `/permissions` | 查看或更新权限                                        | 别名：`/allowed-tools`    |
| `/resume`      | 恢复之前的对话                                        | 别名：`/continue`         |
| ⭐`/rewind`     | 回滚对话或代码                                        | 别名：`/checkpoint`       |
| ⭐`/plan`       | 进入规划模式                                         |                        |
| ⭐`/diff`       | 打开差异查看器                                        | 显示未提交的更改               |
| `/context`     | 可视化当前上下文使用情况                                   | 🆕                     |
| `/effort`      | 设置模型努力级别（Claude Opus 4.6 和 Claude Opus 4.5 支持） | 🆕 low/medium/high/max |
| `/fast`        | 切换快速模式                                         | 🆕                     |
| `/theme`       | 更改颜色主题                                         |                        |
| `/vim`         | 切换 Vim 编辑模式                                    |                        |
| `/voice`       | 切换语音听写                                         | 需要 Claude.ai 账户        |
| ⭐`/btw`        | 提问而不添加到对话                                      | 🆕 旁注问题                |
| `/export`      | 导出当前对话                                         |                        |
| ⭐`/branch`     | 创建对话分支                                         | 别名：`/fork`             |
| `/rename`      | 重命名当前会话                                        |                        |
| `/exit`        | 退出 CLI                                         | 别名：`/quit`             |


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

| 快捷键                     | 功能说明                 |
| ----------------------- | -------------------- |
| ⭐`!`                    | 进入 Bash 模式           |
| ⭐`/`                    | 显示命令列表               |
| ⭐`@`                    | 输入文件路径               |
| ⭐`\` + `Enter`          | 换行输入（alter+enter 也可） |
| `Esc` `Esc`             | 清空输入（Bash 模式下双击）     |
| `Shift` + `Tab`         | 切换权限模式（自动接受编辑）       |
| `Ctrl` + `O`            | 显示详细输出               |
| `Ctrl` + `V`            | 粘贴图片                 |
| `Ctrl` + `S`            | 暂存当前输入               |
| ⭐`Ctrl` + `G`           | 在编辑器中编辑输入            |
| ⭐`Ctrl` + `Z`           | 关闭当前会话               |
| `Ctrl` + `C` double     | 关闭当前会话               |
| ⭐`Ctrl` + `Shift` + `-` | 撤销输入                 |
| `Ctrl` + `U`            | 清除整行                 |
| `Ctrl` + `W`            | 删除前一个词               |
| `Ctrl` + `T`            | 切换任务视图               |
| `Meta` + `P`            | 切换模型                 |

> **提示**：`Meta` 键在 Windows/Linux 上通常是 `Alt`，在 macOS 上是 `Cmd`。

### 3.启动历史对话

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

Claude Code 内置了丰富的工具集，以下是完整的工具列表（截至 2026年3月）：
（todo:是否建议分个类？）

| 工具 | 用途 | 需要权限 |
|------|------|:--------:|
| **Agent** | 生成子代理处理独立任务 | ❌ |
| **AskUserQuestion** | 向用户提问以澄清需求 | ❌ |
| **Bash** | 执行 shell 命令 | ✅ |
| **CronCreate** 🆕 | 在当前会话中调度周期性任务 | ❌ |
| **CronDelete** 🆕 | 取消调度的任务 | ❌ |
| **CronList** 🆕 | 列出会话中所有调度任务 | ❌ |
| **Edit** | 对文件进行针对性编辑 | ✅ |
| **EnterPlanMode** | 切换到规划模式设计实现方案 | ❌ |
| **EnterWorktree** | 创建隔离的 git worktree | ❌ |
| **ExitPlanMode** | 提交方案审批并退出规划模式 | ✅ |
| **ExitWorktree** | 退出 worktree 会话 | ❌ |
| **Glob** | 基于模式匹配查找文件 | ❌ |
| **Grep** | 在文件内容中搜索模式 | ❌ |
| **ListMcpResourcesTool** | 列出 MCP 服务器暴露的资源 | ❌ |
| **LSP** 🆕 | 语言服务器代码智能（类型错误、跳转定义等） | ❌ |
| **NotebookEdit** | 修改 Jupyter notebook 单元格 | ✅ |
| **Read** | 读取文件内容 | ❌ |
| **ReadMcpResourceTool** | 通过 URI 读取 MCP 资源 | ❌ |
| **Skill** | 在主对话中执行技能 | ✅ |
| **TaskCreate** 🆕 | 在任务列表中创建新任务 | ❌ |
| **TaskGet** 🆕 | 获取特定任务的完整详情 | ❌ |
| **TaskList** 🆕 | 列出所有任务及其状态 | ❌ |
| **TaskOutput** 🆕 | 获取后台任务的输出 | ❌ |
| **TaskStop** 🆕 | 终止运行中的后台任务 | ❌ |
| **TaskUpdate** 🆕 | 更新任务状态、依赖、详情 | ❌ |
| **TodoWrite** | 管理会话任务清单 | ❌ |
| **ToolSearch** 🆕 | 搜索并加载延迟工具 | ❌ |
| **WebFetch** | 获取指定 URL 的内容 | ✅ |
| **WebSearch** | 执行网络搜索 | ✅ |
| **Write** | 创建或覆盖文件 | ✅ |

> 💡 **说明**：权限可在 `/permissions` 或 [permission settings](https://code.claude.com/docs/en/settings#available-settings) 中配置。🆕 标记为近期新增功能。

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

![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1774370119667-77f9b99a-e0e3-459f-8a40-33c549dbb980.png)

**自定义加载词**（需要手动修改源码）（todo：使用原生安装的似乎不行？只有npm安装的可以修改吗）：

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

# 四、进阶
## 1.CLAUDE.md 与 记忆机制(todo:编号统一)

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
也可以每个目录都可以添加一份。（todo:优化一下，表达清楚是什么在哪里）

> 作为用户消息在系统提示之后传递，而不是系统提示本身的一部分。Claude 读取它并尝试遵循它，但没有严格遵守的保证，特别是对于模糊或冲突的指令。

### 5.1 逐层加载机制

Claude Code 会从当前目录逐级向上查找 `CLAUDE.md` 文件，并将所有找到的内容合并加载。子目录中的 CLAUDE.md 文件在 Claude 读取这些目录中的文件时按需加载。

（todo:这是加载顺序还是决策的优先级？）**加载顺序**（优先级从高到低）：

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
（todo：表达方式不顺畅）此示例排除顶级 CLAUDE.md 和来自父文件夹的规则目录。将其添加到 `.claude/settings.local.json` 以使排除保持本地到你的机器：

```
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

### 5.2 创建和修改记忆

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

### 5.3 编写有效指令

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
### 5.3 推荐的 CLAUDE.md 模板

以下是一个经过验证的 CLAUDE.md 模板，包含：

- **工作流编排**：何时规划、何时委托
- **子智能体策略**：如何有效使用 Agent
- **自我优化循环**：从错误中学习
- **完成前校验**：确保质量
- **核心原则**：简洁、安全、可维护

![[Pasted image 20260328145723.png]]

内容过长，可私信或留言获取。

### 5.4 rules

对于较大的项目，你可以使用 `.claude/rules/` 目录将指令组织到多个文件中。这使指令保持模块化并更容易让团队维护。

规则在每个会话或打开匹配文件时加载到上下文中。对于不需要始终在上下文中的特定任务指令，改用 [skills](https://code.claude.com/docs/zh-CN/skills)，它仅在你调用它们或 Claude 确定它们与你的提示相关时加载。

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

用户级规则

`~/.claude/rules/` 中的个人规则适用于你机器上的每个项目。使用它们来处理不是项目特定的偏好：

```
~/.claude/rules/
├── preferences.md    # 你的个人编码偏好
└── workflows.md      # 你的首选工作流
```

用户级规则在项目规则之前加载，给予项目规则更高的优先级。
****
### 5.5 /memory 功能

运行 `/memory` 命令可以：

| 操作  | 说明                             |
| --- | ------------------------------ |
| 查看  | 显示所有已加载的记忆来源                   |
| 编辑  | 打开对应文件进行编辑                     |
| 切换  | 开启/关闭 Auto-memory 和 Auto-dream |
![[Pasted image 20260328150133.png]]
### 5.6 Auto-memory

自动记忆会在以下情况触发：

| 触发条件 | 示例 |
|----------|------|
| 用户明确偏好 | "我喜欢用 tab 缩进" |
| 项目关键信息 | "这个项目用的是 PostgreSQL" |
| 重复出现的问题 | "每次都要问数据库配置" |
| 用户主动说"记住" | "记住：我是 GIS 工程师" |

> **存储位置**：`~/.claude/projects/<project>/memory/`，每个项目独立存储。

### 5.7 Auto-dream

Auto-dream 是 Auto-memory 的增强功能，允许 Claude 在会话空闲时自动整理和优化记忆内容。

**开启方式**：运行 `/memory`，在界面中切换 Auto-dream 开关。

**作用**：
- 自动整理碎片化记忆
- 合并相似内容
- 清理过时信息

> **注意**：Auto-dream 需要 Claude Code v2.1.59 或更高版本。
## 6.消息传递机制

当你向 Claude Code 发送消息时，实际传递的内容比你想的更多。以下是完整的消息结构：

### 6.1 消息结构概览

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


## 7.存储机制

Claude Code 使用**作用域系统**来管理配置，决定配置应用的范围和共享对象。

### 7.1 配置作用域

| 作用域 | 位置 | 影响范围 | 是否共享 |
|--------|------|----------|----------|
| **Managed** | 系统级 `managed-settings.json` | 本机所有用户 | 是（IT 部署） |
| **User** | `~/.claude/` | 你，跨所有项目 | 否 |
| **Project** | 项目 `.claude/` | 该项目的所有协作者 | 是（提交到 git） |
| **Local** | `.claude/settings.local.json` | 你，仅此项目 | 否（gitignore） |

**作用域优先级**（从高到低）：
1. Managed（最高）— 无法被覆盖
2. 命令行参数 — 临时会话覆盖
3. Local — 覆盖项目和用户设置
4. Project — 覆盖用户设置
5. User（最低）— 默认设置

### 7.2 配置文件位置

| 功能 | 用户级位置 | 项目级位置 |
|------|------------|------------|
| **Settings** | `~/.claude/settings.json` | `.claude/settings.json` |
| **Subagents** | `~/.claude/agents/` | `.claude/agents/` |
| **MCP Servers** | `~/.claude.json` | `.mcp.json` |
| **Plugins** | `~/.claude/settings.json` | `.claude/settings.json` |
| **CLAUDE.md** | `~/.claude/CLAUDE.md` | `CLAUDE.md` 或 `.claude/CLAUDE.md` |

### 7.3 对话历史存储

对话历史是 Claude Code 最重要的存储内容之一，存储在以下位置：

| 位置 | 内容 | 格式 |
|------|------|------|
| `~/.claude/projects/<project-hash>/` | 项目级会话历史 | `.jsonl` 文件 |
| `~/.claude/sessions/` | 会话记录索引 | `.json` 文件 |

**会话文件命名规则**：
```
~/.claude/projects/<project-path-hash>/<session-id>.jsonl
```

**JSONL 文件结构**（每行一条消息）：
```jsonl
{"type":"user","content":"帮我创建一个 React 组件","timestamp":"2026-03-25T10:00:00Z"}
{"type":"assistant","content":"好的，我来帮你创建...","timestamp":"2026-03-25T10:00:05Z"}
{"type":"tool_use","tool":"Write","args":{"path":"src/Button.tsx","content":"..."}}
{"type":"tool_result","output":"已创建文件 src/Button.tsx"}
```

**恢复历史对话**：
```bash
# 查看历史会话
claude --resume

# 或在 Claude Code 中使用命令
你：/resume
Claude：请选择要恢复的会话：
  1. 2026-03-25 10:00 - 创建 React 组件
  2. 2026-03-24 15:30 - 修复登录 Bug
```

**会话清理**：
```json
// settings.json 中配置清理周期
{
  "cleanupPeriodDays": 30  // 30天后自动清理
}
```

> 💡 **提示**：对话历史文件可能包含敏感信息（如代码、API Key 等），建议定期清理或配置 `cleanupPeriodDays`。

### 7.4 其他存储位置

| 位置 | 内容 |
|------|------|
| `~/.claude/` | 主配置目录 |
| `~/.claude/projects/` | 项目级配置和记忆 |
| `~/.claude/sessions/` | 会话历史（.jsonl 文件） |
| `~/.claude/skills/` | 全局技能（SKILL.md 文件） |
| `~/.claude/plans/` | 规划模式生成的计划文件 |
| `项目/.claude/` | 项目级配置（commands/、skills/） |
| `项目/memory/` | 自动记忆（MEMORY.md） |
| `~/.claude.json` | 偏好设置、OAuth 会话、MCP 配置、缓存 |

### 7.4 settings.json 配置项

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `permissions` | 权限规则（allow/deny/ask） | `{"allow": ["Bash(npm run lint)"]}` |
| `env` | 环境变量 | `{"FOO": "bar"}` |
| `hooks` | 生命周期钩子 | 详见 Hooks 章节 |
| `model` | 覆盖默认模型 | `"claude-sonnet-4-6"` |
| `language` | 响应语言 | `"japanese"` |
| `theme` | 颜色主题 | `"dark"` |
| `alwaysThinkingEnabled` | 默认启用扩展思考 | `true` |
| `cleanupPeriodDays` | 会话清理周期 | `30` |

> **提示**：在 settings.json 中添加 `$schema` 可以在编辑器中获得自动补全：
> ```json
> { "$schema": "https://json.schemastore.org/claude-code-settings.json" }
> ```

## 8.权限设计

### 8.1 Claude Code 4种权限（todo：我记得好像有啥更新，新增了一种？）

- **default**: 默认只读，需要执行写命令时进行询问
- **plan**: 只读+计划，通常不会执行
- **acceptEdits**: 具有读写文件的权限，无需批准。但是执行 Bash 命令时仍然需要批准
- **bypassPermissions**: 读写权限+Bash 命令执行权限，跳过所有权限提示

**_提示：_** _上述四种权限中_ `_default_`_、_`_plan_`_、_`_acceptEdits_` _可以通过_ `_Shift+Tab_` _快捷键在 Claude Code 内部进行切换。_`_bypassPermissions_` _权限需要在启动 Claude 时添加_ `_--dangerously-skip-permissions_` _参数。_

### 8.2 权限控制

上述的四种模式提供了宏观的控制，在 `settings.json` 文件中可以进行更加细微的权限控制。对于具体的命令，有 3 种权限，分别是 `deny`、`allow` 和 `ask`。`deny` 的命令一定不执行，`allow` 的命令允许执行，`ask` 的命令需要问了才知道。

**配置示例：**
（todo:可以通过/permission吗，这个步骤要详细一下）
```
{ 
  "permissions": { 
    "allow": [ 
      "Read(*.java)",      // 总是允许读取 Java 文件 
      "mcp__github"        // 总是允许使用名为 'github' 的 MCP 服务器的所有工具 
    ], 
    "ask": [ 
      "Edit(*.yml)"        // 编辑 yml 文件时总是询问 
    ], 
    "deny": [ 
      "Bash(rm:-rf:*)",           // 绝对禁止 `rm -rf` 
      "Bash(git:push:--force)"    // 绝对禁止强制推送 
    ] 
  } 
}
```

**【重要】Read/Edit 规则的路径模式非常讲究：**

- `path`**或**`./path`: 相对于当前工作目录。例如：`Read(*.java)` 会匹配当前目录下的 `.java` 文件。
- `/path`: 相对于 `settings.json` 文件所在目录。例如：在项目级的 `./.claude/settings.json` 中，`Deny(Read(/config/**))` 会禁止读取项目根目录下的 `config` 文件夹。
- `~/path`: 相对于用户主目录。例如：`Deny(Read(~/.ssh/id_rsa))` 会禁止 AI 读取你的 SSH 私钥。
- `//path`: 文件系统的绝对路径。例如：`Deny(Read(//etc/passwd))` 会禁止 AI 读取系统的密码文件 `/etc/passwd`。请务必区分，错误的路径模式可能会导致你的安全规则失效！

**其他注意事项：**

- `Read`/`Write`/`Edit` 使用的是类似 `.gitignore` 的语法，`Bash` 使用的是基于前缀匹配的规则（不是 glob 或 regex）。
- `WebFetch` 和 `MCP` 也可以加入到权限控制当中（MCP 权限规则不支持通配符 `*`。要允许一个服务器的所有工具，请直接使用服务器名，如 `mcp__github`)。

## 9. Skills 技能

### 9.1 Skills 是什么

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

### 9.2 安装 Skills

**方式一：自然语言安装**
```
你：帮我安装一个 skill，地址是 https://github.com/anthropics/skills/tree/main/skills/pptx
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

访问 [SkillHub](https://skillhub.tencent.com/) 或 [SkillsMP](https://skillsmp.com/zh)，搜索并安装所需 Skills。

### 9.3 热门 Skills 推荐

| Skill | 功能 | 来源 |
|-------|------|------|
| **brainstorming** | 创意工作前的头脑风暴 | Superpowers |
| **test-driven-development** | TDD 工作流 | Superpowers |
| **systematic-debugging** | 系统化调试 | Superpowers |
| **requesting-code-review** | 请求代码审查 | Superpowers |
| **pptx** | PowerPoint 演示文稿 | Anthropic 官方 |
| **pdf** | PDF 文件操作 | Anthropic 官方 |
| **docx** | Word 文档操作 | Anthropic 官方 |
| **playwright** | 浏览器自动化 | Anthropic 官方 |

> 💡 **提示**：安装 Skills 后，Claude Code 会自动识别并在合适场景调用。

### 9.4 Skills 与 MCP 的区别

| 特性 | Skills | MCP |
|------|--------|-----|
| **本质** | Prompt 模板/工作流 | 外部服务 API 封装 |
| **运行方式** | 注入到当前上下文 | 独立进程 |
| **调用方式** | 自动匹配或 `/skill-name` | 自动调用工具 |
| **典型用途** | 开发流程、代码审查、测试 | GitHub 操作、数据库查询 |

---

## 10. MCP Tools

### 10.1 MCP 是什么

MCP (Model Context Protocol) 是连接 Claude Code 与外部服务的协议。通过 MCP，Claude 可以：
- 操作 GitHub 仓库
- 查询数据库
- 发送 Slack 消息
- 访问 Google Drive 文件

### 10.2 安装 MCP

```bash
# 安装 GitHub MCP
claude mcp add github -- npx -y @anthropic-ai/mcp-server-github

# 查看已安装的 MCP
claude mcp list

# 删除 MCP
claude mcp remove github
```

### 10.3 热门 MCP 工具推荐

**开发工具类**

| MCP        | 功能               | 安装命令                                                              |
| ---------- | ---------------- | ----------------------------------------------------------------- |
| **GitHub** | 仓库操作、Issue、PR 管理 | `claude mcp add github -- npx -y @anthropic-ai/mcp-server-github` |
| **GitLab** | GitLab 项目管理      | `claude mcp add gitlab -- npx -y @anthropic-ai/mcp-server-gitlab` |
| **Docker** | 容器管理             | `claude mcp add docker -- npx -y @anthropic-ai/mcp-server-docker` |

**数据库类**

| MCP | 功能 | 安装命令 |
|-----|------|----------|
| **PostgreSQL** | PostgreSQL 数据库操作 | `claude mcp add postgres -- npx -y @anthropic-ai/mcp-server-postgres` |
| **SQLite** | SQLite 数据库操作 | `claude mcp add sqlite -- npx -y @anthropic-ai/mcp-server-sqlite` |

**文档协作类**

| MCP        | 功能          | 安装命令                                                              |
| ---------- | ----------- | ----------------------------------------------------------------- |
| **Slack**  | Slack 消息发送  | `claude mcp add slack -- npx -y @anthropic-ai/mcp-server-slack`   |
| **Notion** | Notion 文档管理 | `claude mcp add notion -- npx -y @anthropic-ai/mcp-server-notion` |

**搜索类**

| MCP              | 功能     | 安装命令                                                                          |
| ---------------- | ------ | ----------------------------------------------------------------------------- |
| **Brave Search** | 网页搜索   | `claude mcp add brave-search -- npx -y @anthropic-ai/mcp-server-brave-search` |
| **Puppeteer**    | 浏览器自动化 | `claude mcp add puppeteer -- npx -y @anthropic-ai/mcp-server-puppeteer`       |

> 💡 **提示**：部分 MCP 需要配置 API Key，请参考各 MCP 的官方文档。

---

## 11. 插件（Plugins）

### 11.1 插件是什么

插件是打包好的功能集合，可以包含：
- Skills（技能）
- Commands（命令）
- Hooks（钩子）
- Agents（子代理）

### 11.2 推荐插件

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

## 12. Hooks 钩子

### 12.1 Hooks 是什么

Hooks 让你在 Claude Code 执行操作前后自动运行代码。

**典型用途**：
- 文件保存后自动格式化（Prettier）
- 编辑后自动类型检查
- 提交前自动 lint

### 12.2 可用事件

| 事件名 | 触发时机 | 使用场景 |
|--------|----------|----------|
| **SessionStart** | 会话开始 | 加载开发上下文、设置环境变量 |
| **PreToolUse** | 工具执行前 | 验证或阻止危险命令 |
| **PostToolUse** | 工具执行后 | 代码格式化、运行测试 |
| **Stop** | 响应完成时 | 检查任务是否完成 |
| **SessionEnd** | 会话结束 | 清理任务、记录统计 |

### 12.3 配置 Hooks

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

**常用配置示例**：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx eslint --fix $FILE_PATH"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash(rm:-rf:*)",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Dangerous command blocked' && exit 1"
          }
        ]
      }
    ]
  }
}
```

---

（todo:后台任务相关内容，怎么启动，怎么关闭，怎么查看等）
## 13.SubAgents
（todo：完善这一块）

## 14. Agent Teams

Agent Teams 是一组协作的 AI 代理，每个代理有自己的角色、工具和上下文。

### 14.1 创建团队

```
你：/team-create
Claude：请输入团队名称：frontend-team
       请输入团队描述：前端开发团队
       团队已创建！
```

### 14.2 创建和分配任务

```
你：/task-create
Claude：请输入任务名称：实现登录页面
       请输入任务描述：使用 React 实现登录页面

你：帮我把这个任务分配给 reviewer
Claude：任务已分配给 reviewer 代理
```

### 14.3 协作模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **并行执行** | 多代理同时处理独立任务 | 大型重构、多模块开发 |
| **流水线** | 代理按顺序处理 | 代码审查 → 测试 → 部署 |
| **协作讨论** | 代理之间讨论决策 | 架构设计、技术选型 |

### 14.4 使用 tmux 管理长时间任务

```bash
# 创建会话
tmux new -s claude-team

# 启动 Claude Code
claude

# 分离会话（Ctrl+B, D）
# 重新连接
tmux attach -t claude-team
```

### 15. 自定义 Slash Commands

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

# 五、OpenSpec

[GitHub - Fission-AI/OpenSpec: Spec-driven development (SDD) for AI coding assistants.](https://github.com/Fission-AI/OpenSpec)

## 1.是什么？解决什么问题？

**OpenSpec = Spec-driven development (SDD) for AI coding assistants**

AI 编程助手很强大，但有一个痛点：当你和 AI 对齐了设计思路、实现完一个功能后，过两天打开新对话继续下一个功能，之前的所有讨论、决策、设计全部蒸发。你又要从头解释项目背景、技术栈、已有的架构约束。

还有一种情况：功能做到一半被打断了——开会、下班、切去修一个 Bug。回来打开新对话，AI 完全不知道你之前做到哪了。

OpenSpec 倡导的是一种”规格驱动开发”范式：

> **Agree before you build** — 在写任何一行代码之前，先由人类与 AI 共同协商并锁定一份机器可读、人可评审的规格文档。

## 2.安装与初始化

### 前置要求

- Node.js **20.19.0+**

### 安装

```
npm install -g @fission-ai/openspec@latest
```

### 初始化项目

```
cd your-project
openspec init
```

初始化时 CLI 会问你使用哪些 AI 工具（Claude Code、Cursor、Copilot 等），然后自动往对应目录写入 Skill 和斜杠命令文件。完成后项目里多出一个 `openspec/` 目录：

```
  openspec/
  ├── config.yaml                              # OpenSpec 配置文件
  ├── changes/                                  # 变更提案目录
  │   └── archive/                              # 已归档的变更
  │       ├── 2026-03-15-xxxx/    # 运行时可观测性事件变更
  │          ├── proposal.md                   # 变更提案文档
  │          ├── design.md                     # 技术设计文档
  │          ├── tasks.md                      # 任务清单
  │          ├── .openspec.yaml                # 变更元数据配置
  │          └── specs/
  │              └── runtime-observability/
  │                  └── spec.md               # 运行时可观测性规格说明
  └── specs/                                    # 当前生效的规格说明
      ├── auth-flow/
      │   └── spec.md                           # 认证流程规格
      ├── runtime-backed-chat/
      │   └── spec.md                           # 运行时聊天规格
      ├── docker/
      │   └── spec.md                           # Docker部署规格
      ├── chat-session-persistence/
      │   └── spec.md                           # 聊天会话持久化规格
      ├── runtime-observability/
      │   └── spec.md                           # 运行时可观测性规格
      └── environment/
          └── spec.md                           # 环境配置规格
```

OpenSpec 弃用了笨重的开发文档，转而采用一套轻量级的、面向 AI 优化的 Markdown 工件体系。每个变更（Change）都被组织在独立的文件夹中：

  
  

- **proposal.md：**描述变更的初衷（Why）和范围（What）。
- **specs/：**具体的逻辑规格，通常包含 “Scenario（场景）” 描述，通过具体的输入输出消除模糊性。
- **design.md：**技术设计方案，包括本次变更涉及的数据库变更、接口调整等。
- **tasks.md：**原子化的任务清单，作为 AI 的执行路径图。

写入的skill和斜杠命令文件

![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1773475128745-b2184482-3182-4e43-8920-c468ccf4bdeb.png)

### skills/commnd介绍

codex

在输入框中输入/opsx，可以看到/prompts:opsx-* 列表，

![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1773481839158-7269bb27-e7ea-4a61-95d1-6dd21e0df8b8.png)

来源是`~/.codex/prompts/`(这里要画成目录图）

```
  .codex/prompts/
  ├── opsx-apply.md      # 实现 OpenSpec 变更中的任务 - 执行代码实现阶段
  ├── opsx-archive.md    # 归档已完成的变更 - 检查完整性、同步规格、移动到归档目录
  ├── opsx-explore.md    # 探索模式 - 思考想法、调查问题、澄清需求（只读，不实现代码）
  └── opsx-propose.md    # 提议新变更 - 创建变更目录并生成所有工件
```

项目目录下的skills

```
  .codex/skills/
  ├── openspec-propose/
  │   └── SKILL.md               # 一键创建变更提案，生成设计文档、规格和任务清单
  ├── openspec-apply-change/
  │   └── SKILL.md               # 实现 OpenSpec 变更中的任务，开始或继续开发
  ├── openspec-explore/
  │   └── SKILL.md               # 探索模式，深入思考想法、调查问题、澄清需求（只读）
  ├── openspec-archive-change/
      └── SKILL.md               # 归档已完成的变更，在实现完成后进行归档
```

两者之间的关系：

```
  ~/.codex/prompts/
    -> 决定你输入 / 时能看到哪些命令入口
    -> 所以会显示 /prompts:opsx-apply 这类项
```

项目/.codex/skills/

```
    -> 决定 Codex 在这个仓库里有哪些可用技能
    -> 给模型提供具体的工作流和执行规则
    -> 但不会直接以 /opsx 形式出现在命令菜单里
```

claude

在输入框中输入/opsx:，可以看到/opsx: 列表，

![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1774277670507-e3573ec8-40c8-4997-aebd-ee9bbb8a6ac7.png)

```

  ┌───────────────┬────────────────────┬──────────────────────────────────┐
  │     命令      │        作用        │               产出               │
  ├───────────────┼────────────────────┼──────────────────────────────────┤
  │ /opsx:explore │ 探索想法、澄清需求 │ 无固定产出，可能创建 artifacts   │
  ├───────────────┼────────────────────┼──────────────────────────────────┤
  │ /opsx:propose │ 创建变更提案       │ proposal.md, design.md, tasks.md │
  ├───────────────┼────────────────────┼──────────────────────────────────┤
  │ /opsx:apply   │ 实现任务           │ 代码实现 + 更新 tasks.md         │
  ├───────────────┼────────────────────┼──────────────────────────────────┤
  │ /opsx:archive │ 归档完成的变更     │ 更新 specs/ 目录                 │
  └───────────────┴────────────────────┴──────────────────────────────────┘
```

具体存放位置是在：

```
  .claude/commands/
  └── opsx/                       # 子目录名 = 命名空间前缀
      ├── propose.md              # /opsx:propose
      ├── apply.md                # /opsx:apply
      ├── explore.md              # /opsx:explore
      └── archive.md              # /opsx:archive
```

不仅可以使用command，还以直接选择skills:

![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1774277689792-ba553196-b538-49c7-ac8e-7e08d906f691.png)

```
  .claude/skills/
  ├── openspec-propose/
  │   └── SKILL.md                              # 一键创建变更提案，生成设计文档、规格和任务清单
  ├── openspec-apply-change/
  │   └── SKILL.md                              # 实现 OpenSpec 变更中的任务，开始或继续开发
  ├── openspec-explore/
  │   └── SKILL.md                              # 探索模式，深入思考想法、调查问题、澄清需求（只读）
  ├── openspec-archive-change/
      └── SKILL.md                              # 归档已完成的变更，在实现完成后进行归档
```

### OpenSpec CLi

```
  openspec
  ├── init [path]              # 初始化 OpenSpec 到项目
  ├── update [path]            # 更新 OpenSpec 指令文件
  ├── list                     # 列出变更（默认）或规格（--specs）
  ├── view                     # 交互式仪表盘
  ├── change                   # 管理变更提案
  ├── archive [change-name]    # 归档已完成的变更
  ├── spec                     # 管理规格说明
  ├── config                   # 查看和修改配置
  ├── schema                   # 管理工作流 schema（实验性）
  ├── validate [item-name]     # 验证变更和规格
  ├── show [item-name]         # 显示变更或规格详情
  ├── status                   # 显示 artifact 完成状态
  ├── instructions [artifact]  # 输出创建 artifact 的指令
  ├── templates                # 显示模板路径
  ├── schemas                  # 列出可用的 workflow schemas
  ├── new                      # 创建新项目
  ├── feedback <message>       # 提交反馈
  └── completion               # Shell 补全管理
```

在 Skills/Commands 中的被动调用：

```

  ┌──────────────────────────────────────────────────────────┬─────────────────────────────────┬─────────────────────────┐
  │                         CLI 命令                         │            调用位置             │          用途           │
  ├──────────────────────────────────────────────────────────┼─────────────────────────────────┼─────────────────────────┤
  │ openspec new change "<name>"                             │ propose                         │ 创建新变更目录结构      │
  ├──────────────────────────────────────────────────────────┼─────────────────────────────────┼─────────────────────────┤
  │ openspec list --json                                     │ propose, apply, archive,        │ 获取可用变更列表        │
  │                                                          │ explore                         │                         │
  ├──────────────────────────────────────────────────────────┼─────────────────────────────────┼─────────────────────────┤
  │ openspec status --change "<name>" --json                 │ propose, apply, archive         │ 检查 artifact 完成状态  │
  ├──────────────────────────────────────────────────────────┼─────────────────────────────────┼─────────────────────────┤
  │ openspec instructions <artifact> --change "<name>"       │ propose, apply                  │ 获取创建 artifact       │
  │ --json                                                   │                                 │ 的指令                  │
  └──────────────────────────────────────────────────────────┴─────────────────────────────────┴─────────────────────────┘

```

调用流程图：

```
  /opsx:propose <name>
      │
      ├─→ openspec new change "<name>"        # 创建变更目录
      ├─→ openspec status --json              # 检查需要哪些 artifacts
      └─→ openspec instructions proposal --json   # 获取创建 proposal.md 的指令
              ↓
          openspec instructions design --json      # 获取创建 design.md 的指令
              ↓
          openspec instructions tasks --json       # 获取创建 tasks.md 的指令

  /opsx:apply <name>
      │
      ├─→ openspec list --json                # 列出可用变更
      ├─→ openspec status --json              # 检查 artifact 状态
      └─→ openspec instructions apply --json  # 获取执行任务的指令

  /opsx:archive <name>
      │
      ├─→ openspec list --json                # 列出可用变更
      └─→ openspec status --json              # 验证所有 artifacts 已完成
```

总结： CLI 是底层引擎，Skills/Commands 是封装层，通过 --json 输出获取结构化数据供 Claude 解析和执行。

```
openspec new change "fix-buffer-analysis-geo-layer"
   创建 opsx 变更提案
```

```
openspec status --change "fix-buffer-analysis-geo-layer" --json
   获取变更状态和工件顺序
```

```
openspec instructions proposal --change "fix-buffer-analysis-geo-layer" --json
   获取 proposal 工件指令
```

```
 openspec instructions design --change "fix-buffer-analysis-geo-layer" --json
   获取 design 工件指令
```

## 3.工作流：提案、应用、归档

**在项目根目录下的**`**openspec/**`**中能真正窥探到其管理方法**

```
openspec/
├── specs/          ← "系统现在是什么样的"
│   ├── auth/
│   ├── payments/
│   └── ...
└── changes/        ← "我们打算改什么"
    ├── add-dark-mode/
    └── fix-login-bug/
```

**Specs（主规格）** 是系统当前行为的权威描述——"源真相"。它回答的是"系统**现在**是怎么运作的"。

**Changes（变更）** 是你正在进行的修改——每个功能、每个 Bug 修复独立一个文件夹，互不干扰。它回答的是"我们**打算怎么改**"。

- **Proposal 阶段：**建立一个独立的变更上下文，让 AI 只关注当前变更。
- **Apply 阶段：**AI 严格按照 tasks.md 执行，避免了盲目扫描全库导致的 Token 浪费。
- **Archive 阶段：**任务完成后，临时变更文档被移入归档，核心规格更新至主规格文件。这保证了 AI 始终在一个 “卫生” 的上下文环境下工作，同时也为项目留下了可追溯的决策链路。

当一个变更完成并归档后，它里面的规格变化会合并进 specs——主规格因此更新，变更则移入归档目录。这样，specs 始终反映系统的"最新真实状态"。

## 4.实际使用场景

完整流程

- 新需求来了：先建 openspec/changes/<change>/...

- AI 主要写 proposal.md、design.md、tasks.md、changes/.../specs/...

- 功能完成并确认后：archive

- archive 之后，主 openspec/specs/... 才更新

这个分离设计有一个很大的好处：你可以同时推进多个变更而互不冲突——它们各自在自己的文件夹里工作，不会互相干扰 specs。

例子“用 Vite+ 给现有项目做初始化/接管”

那 OpenSpec 里通常这样走：

1. 如果你还在评估值不值得上、怎么上、风险是什么  
    用 explore
2. 一旦决定要做这个 change  
    用 propose
3. 方案确认后开始落代码  
    用 apply
4. 做完并验收通过  
    用 archive

## 5.进阶能力

# 六、Everything-claude-code

> **Anthropic 黑客马拉松优胜项目**，一套完整的 AI 智能体性能优化系统。

GitHub: https://github.com/affaan-m/everything-claude-code

## 1. 是什么？

Everything Claude Code (ECC) 是针对 Claude Code、Codex 和 Cursor 等工具的 AI 智能体组件性能优化系统。包含技能、直觉、记忆优化、持续学习和安全扫描功能。

## 2. 核心能力

| 特性 | 数量 | 说明 |
|------|------|------|
| **Agents** | 28 个 | planner, architect, tdd-guide, code-reviewer, security-reviewer, build-error-resolver, e2e-runner 等 |
| **Skills** | 125 项 | continuous-learning, tdd-workflow, backend-patterns, frontend-patterns, verification-loop 等 |
| **Commands** | 60 条 | 快捷命令，覆盖各种开发场景 |

**核心能力**：
- 记忆持久化
- 持续学习
- 验证循环
- Token 优化

## 3. 安装方式

**方式一：插件安装（推荐）**

```bash
/plugin marketplace add affaan-m/everything-claude-code
/plugin install everything-claude-code@everything-claude-code
```

**方式二：脚本安装**

```bash
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code

# Linux/macOS
./install.sh typescript

# Windows
.\install.ps1 typescript
```

## 4. 包含的组件

### Agents（智能体）

| Agent | 用途 |
|-------|------|
| planner | 实现规划 |
| architect | 系统设计 |
| tdd-guide | 测试驱动开发 |
| code-reviewer | 代码审查 |
| security-reviewer | 安全分析 |
| build-error-resolver | 构建错误修复 |
| e2e-runner | E2E 测试 |
| refactor-cleaner | 代码清理 |
| doc-updater | 文档更新 |

### Skills（技能）

| Skill | 用途 |
|-------|------|
| continuous-learning | 持续学习 |
| tdd-workflow | TDD 工作流 |
| backend-patterns | 后端模式 |
| frontend-patterns | 前端模式 |
| verification-loop | 验证循环 |
| golang-patterns | Go 语言模式 |
| django-patterns | Django 模式 |
| security-scan | 安全扫描 |
| springboot-patterns | Spring Boot 模式 |

### Hooks（钩子）

| Hook | 触发时机 |
|------|----------|
| memory-persistence | 记忆持久化 |
| strategic-compact | 战略压缩 |
| session-start | 会话开始 |
| session-end | 会话结束 |
| pre-compact | 压缩前 |
| suggest-compact | 建议压缩 |
| evaluate-session | 评估会话 |

## 5. 支持的语言

TypeScript、Python、Go、Java、Rust 等多种语言的开发规则。

---

# 七、常见问题与排错

## 1. 启动问题

### Q: 启动时报错 "Unable to connect to Anthropic services"

**原因**：首次启动时强制要求登录 Anthropic 账户。

**解决方案**：

1. 打开 `~/.claude.json` 文件（Windows: `C:\Users\%USERNAME%\.claude.json`）
2. 设置 `hasCompletedOnboarding` 为 `true`：

```json
{
  "hasCompletedOnboarding": true
}
```

3. 保存后重新启动 Claude Code

### Q: 启动后显示模型不可用

**原因**：配置的模型与当前服务商不匹配。

**解决方案**：

1. 使用 `/status` 检查当前配置
2. 确认 `ANTHROPIC_MODEL` 与服务商支持的模型一致
3. 阿里百炼支持的模型：`qwen3.5-plus`、`qwen3-coder-next` 等

## 2. 配置问题

### Q: 配置后 API Key 不生效

**原因**：配置文件格式错误或路径不对。

**解决方案**：

1. 确认配置文件路径：`~/.claude/settings.json`
2. 检查 JSON 格式是否正确
3. 使用 `/status` 验证配置是否生效

### Q: Skills 安装后不显示

**原因**：Skills 未正确放置或格式错误。

**解决方案**：

1. 确认 Skills 目录：`~/.claude/skills/` 或项目 `.claude/skills/`
2. 每个 Skill 需要包含 `SKILL.md` 文件
3. 重启 Claude Code 使配置生效

## 3. MCP 问题

### Q: MCP 服务器连接失败

**原因**：网络问题或 MCP 服务不可用。

**解决方案**：

1. 检查网络连接
2. 使用 `/mcp` 查看 MCP 状态
3. 部分海外 MCP 可能需要代理

### Q: MCP 工具调用报错

**原因**：权限未授权或 API Key 无效。

**解决方案**：

1. 检查 MCP 配置中的 API Key
2. 使用 `claude mcp list` 查看已安装的 MCP
3. 查看 MCP 官方文档确认配置要求

## 4. 性能问题

### Q: 响应速度很慢

**原因**：模型选择或网络延迟。

**解决方案**：

1. 使用更快的模型：`/model haiku` 或 `/model qwen3.5-plus`
2. 检查网络连接
3. 使用 `/compact` 压缩上下文

### Q: Token 消耗过快

**原因**：上下文过大或频繁重复操作。

**解决方案**：

1. 使用 `/clear` 清除不必要的历史
2. 使用 `/compact` 压缩上下文
3. 将大型任务拆分为多个小任务

## 5. 其他问题

### Q: 如何查看当前会话的 Token 使用量？

**解决方案**：使用 `/cost` 命令查看（部分服务商可能不支持）

### Q: 如何恢复之前中断的对话？

**解决方案**：使用 `claude --resume` 启动历史对话

### Q: 如何切换不同的服务商？

**解决方案**：修改 `~/.claude/settings.json` 中的 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN`

---

# Source

[OpenSpec 完全使用指南：用规格驱动 AI 编码](https://www.notemi.cn/openspec-complete-user-guide--driving-ai-encoding-with-specifications.html)