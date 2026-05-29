# Claude Code 搜索、内容获取能力优化

> 环境：Claude Code + DeepSeek API
> skill：SkillHub 商店（国内直连）

## 一、问题：WebFetch 经常挂

在平时使用 Claude Code 想要获取某网页信息时，Claude Code 会主动调用 WebFetch 工具，但是基本上都会报错，如图：

![[Pasted image 20260529162800.png]]

让 DeepSeek 分析了一下，当使用 WebFetch 工具时，背后的调用链是这样的：
```
用户发请求 → Claude Code → 步骤1: claude.ai 域名安全验证 → 步骤2: 服务端抓取 URL → 步骤3: HTML→Markdown → 步骤4: 小模型处理
```

步骤 1 的域名验证要连 `claude.ai`（Anthropic 云端），国内网络不通。
步骤 2-4 依赖 API 服务端内置能力。

所以不是网络问题、不是配置问题，是 WebFetch 强依赖 Anthropic 基础设施，走第三方 API 代理这条路基本无解。

---

## 二、工具链全景

内置工具中，WebFetch 不能用，但是可以用 WebSearch、以及用 Bash 执行 crul 命令来获取网页内容，还有各种 skill 可以帮助 Agent 来完成搜索、内容获取。经过一番搜查找、测试，敲定了以下工具，可以分为搜索、指定网页获取、深度研究。

| 分类    | 场景              | 工具                        | 优点                 | 缺点                         |
| ----- | --------------- | ------------------------- | ------------------ | -------------------------- |
| 泛搜索   | 日常搜索            | 内置 WebSearch              | 零配置，直接可用           | 中文覆盖弱，无高级语法                |
| 泛搜索   | 中文搜索 / 多源验证     | Multi Search Engine       | 16 引擎，中文强，无需 key   | 国际引擎需代理                    |
| 泛搜索   | 语义搜索 / 竞品发现     | Exa                       | 模糊搜索，"找类似 X 的产品"   | 需注册 API key，有免费额度          |
| URL获取 | 公开 API / SSR 页面 | curl                      | 最轻最快，无依赖           | SPA 站点抓不到内容                |
| URL获取 | SPA / JS 渲染页面   | Agent Browser             | 完整浏览器渲染能力          | 首次需下载 Chrome（183MB）        |
| URL获取 | 视频 / 音频 / PDF   | Summarize                 | 多媒体全能；独立窗口，不影响当前会话 | 需 提供大模型的 API key，如deepseek |
| URL获取 | 登录态页面           | Agent Browser（save state） | 一次登录，后续复用          | 部分站点有反自动化检测                |
| 深度研究  | 深网结构化数据         | AnySearch                 | 搜索引擎搜不到的数据         | 尚在早期，覆盖范围有限                |

---

## 三、泛搜索

| 工具                  | 定位      | 一句话          |     需要配置     |
| ------------------- | ------- | ------------ | :----------: |
| 内置 WebSearch        | 日常快速搜   | 零配置，够用       |      否       |
| Multi Search Engine | 多引擎交叉验证 | 16 引擎，中文强    | 国际搜索引擎需要网络环境 |
| Exa                 | 语义搜索    | "找和 X 类似的东西" |   API key    |
**注意**：如果浏览器能正常打开国际站点（Google 等），但是在命令行中可能无法直接访问。可通过配置代理端口到环境变量中让终端走同一通道。

```bash
# 写入 ~/.bashrc
export https_proxy=http://127.0.0.1:10090
export http_proxy=http://127.0.0.1:10090
```

### L1: 内置 WebSearch

```
优点：零配置，直接可用
缺点：单一搜索引擎（推测 Bing），中文覆盖弱，无高级搜索语法
适用：日常快速查，"XX 是什么" 类问题
```

### L2: Multi Search Engine

这个 skill 不是独立 CLI 工具，而是一套给 AI Agent 的搜索工作流：按各引擎的 URL 模板填入关键词，搭配高级搜索语法组合成完整查询地址，再用 curl 抓取并汇总结果。覆盖 16 个搜索引擎（7 国内 + 9 国际），无需 API key。

安装 skill ：
```bash
skillhub install multi-search-engine
```

实测过的高级搜索：
```bash
# Bing CN，无需代理 — 搜 github 上 Rust 写的 agent-browser
curl "https://cn.bing.com/search?q=site:github.com+agent+browser+Rust"

# Google，需走代理 — 限过去一周内、stackoverflow 上关于 agent-browser 的讨论
curl -x http://127.0.0.1:10090 "https://www.google.com/search?q=site:stackoverflow.com+agent+browser&tbs=qdr:w"
```

**结论**：配代理后约 10 个引擎可用。日常用 Bing CN + Google 覆盖中英文。实测 baidu 不可用。

### L3: Exa

语义搜索。传统搜索引擎基于关键词倒排索引，Exa 基于 embedding 语义匹配。

```
适用场景：
  "推荐和 Linear 类似的项目管理工具"
  "找用 Rust 写浏览器自动化的开源项目"
  "有没有替代 Playwright 的轻量方案"
```

**注意**：需要注册获取 API key。低频但不可替代——其他工具都做不到"不需要知道关键词就能搜"。

---

## 四、获取指定网页链接的内容

| 工具            | 定位    | 搞定什么                  |
| ------------- | ----- | --------------------- |
| curl          | 最轻量   | 公开 API、SSR 页面、静态 HTML |
| Agent Browser | 浏览器渲染 | SPA、JS 动态页面           |
| Summarize     | 多媒体处理 | 视频、音频、PDF             |

### L1: curl

curl 是一个命令行 HTTP 客户端，几乎所有系统自带。在 Claude Code 中通过 Bash 调用，直接拿到网页原始响应。

| 网站类型        | 策略                       | 示例                                                                  |
| ----------- | ------------------------ | ------------------------------------------------------------------- |
| 公开 REST API | 直接调 API                  | `curl -sL "https://api.github.com/repos/vercel-labs/agent-browser"` |
| SSR 页面      | Googlebot UA + 解析内嵌 JSON | 知乎：`<script id="js-initialData">`                                   |
| 静态 HTML     | 直接抓                      | `curl -sL "https://httpbin.org/html"`                               |

> **什么是 Googlebot UA**：请求时把 User-Agent 伪装成 Google 爬虫的标识（`Mozilla/5.0 (compatible; Googlebot/2.1)`）。很多网站为了 SEO 会向爬虫返回完整的 SSR 渲染内容，而普通浏览器拿到的是空壳 + JS，所以 curl 配上这个 UA 就能直接拿到有内容的 HTML。


GitHub 专用技巧——用 REST API 替代页面抓取：
```bash
# 仓库信息
curl -sL -H "Accept: application/vnd.github+json" "https://api.github.com/repos/{owner}/{repo}"

# README 原文
curl -sL -H "Accept: application/vnd.github.raw+json" "https://api.github.com/repos/{owner}/{repo}/readme"
```

公开仓库无需 token，60 次/小时/IP。

SPA 站点（如 SkillHub）找站内 API：
```
F12 → Network → Fetch/XHR → 找返回 JSON 的请求 → 直接调 API
```

### L2: Agent Browser

curl 搞不定的场景——纯 CSR/SPA、JS 动态渲染、需要交互操作的页面。

安装：
```bash
skillhub install agent-browser       # 安装 skill 说明
npm install -g agent-browser         # 安装 CLI 本体
agent-browser install                # 下载 Chrome（183MB，配代理更快）
```

核心命令：
```bash
agent-browser open <url>           # 打开页面
agent-browser snapshot -i          # 获取可交互元素快照（@e1, @e2...）
agent-browser click @e2            # 点击元素
agent-browser fill @e3 "text"      # 填写输入框
agent-browser get text @e1         # 获取元素文本
agent-browser screenshot path.png  # 截图
agent-browser close                # 关闭浏览器
```

使用前配代理：
```bash
export https_proxy=http://127.0.0.1:10090
```

验收结论——同一个 SPA 站点：
- curl → 空壳 `<div id="app"></div>`
- Agent Browser → 完整 DOM，导航/标题/按钮/链接全拿到

Agent Browser vs Playwright：本质走同一套 CDP 协议，能力上限相同。Agent Browser 的 `snapshot -i` 直接把 DOM 转成带编号的可访问性树（`@e1`, `@e2`...），AI Agent 友好。Playwright 适合独立写爬虫脚本。

### L3: Summarize

Summarize 是一个 CLI 内容总结工具，支持网页、PDF、图片、音频、YouTube 等格式。底层用 yt-dlp 拉取视频字幕、用 Firecrawl 抓取网页，然后调用 LLM 生成摘要。支持 OpenAI / Anthropic / Gemini / xAI 等多种后端。

安装：
```bash
skillhub install summarize          # 安装 skill 说明
npm install -g @steipete/summarize  # 安装 CLI 本体
```

配置 API key（选一个后端即可）：
```bash
# OpenAI
export OPENAI_API_KEY="sk-xxx"

# Anthropic
export ANTHROPIC_API_KEY="sk-xxx"

# Google Gemini
export GEMINI_API_KEY="xxx"

# xAI
export XAI_API_KEY="xxx"
```

默认模型为 `google/gemini-3-flash-preview`，可在 `~/.summarize/config.json` 中修改。使用 DeepSeek 等 OpenAI 兼容后端时，需额外指定 base URL：
```bash
export OPENAI_BASE_URL="https://api.deepseek.com"
```

在我们的场景中，普通网页文章直接用 curl 抓取、在会话中分析即可，Summarize 对此没有增量价值。它真正发挥作用的地方是**会话无法直接处理的内容**——视频、音频、PDF 等多媒体文件。

实测 B 站视频：
```bash
summarize "https://www.bilibili.com/video/BV1iuVW6hEqD/" --model openai/deepseek-chat
# 5.7s · $0.0016 · 174 words — yt-dlp 拉字幕 → DeepSeek 总结
```

---

## 五、深度研究

### AnySearch

前面所有搜索工具（WebSearch、Multi Search Engine、Exa）搜的都是**公开网页索引**——Google/Bing 爬过、有人写成了文章的内容。

AnySearch 搜的是**搜索引擎之外的东西**——API 背后的数据库、代码仓库深层细节、社区讨论中的散落信息。

对比：
```
问题："OpenAI 最新估值是多少？"

WebSearch / Multi Search Engine
  → 搜公开网页 → 返回 TechCrunch 文章链接 → 你得自己点开读完才知道
AnySearch
  → 直接返回 → "估值 $8520 亿，2026-03-31 数据，来源：xxx"

问题："agent-browser 在 Reddit 上有哪些讨论？"

Multi Search Engine
  → Google 搜 site:reddit.com agent-browser → 返回帖子列表
AnySearch
  → 直接返回 → 帖子内容摘要 + 情感倾向 + 高频关键词
```

适用场景：
- 公司数据（估值、融资、股权结构）
- 代码仓库深层查询（特定函数实现、issue 讨论中的解决方案）
- 社区内容聚合（Reddit、Hacker News 的帖子和评论）
- API 可触及的专有数据库
