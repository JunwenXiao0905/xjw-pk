---
theme: default
themeName: "默认主题"
title: "Claude Code 搜索、内容获取能力优化"
---

# Claude Code 搜索、内容获取能力优化

> 环境：Claude Code + DeepSeek API
> Skill：SkillHub 商店（国内直连）

## 一、问题：WebFetch 经常挂

在平时使用 Claude Code 想要获取某网页信息时，Claude Code 会主动调用 WebFetch 工具，但是基本上都会报错，如图：

![[Pasted image 20260529162800.png]]

让 DeepSeek 分析了一下，当使用 WebFetch 工具时，背后的调用链是这样的：
```
用户发请求 → Claude Code → 
步骤1: claude.ai 域名安全验证
步骤2: 服务端抓取 URL 
步骤3: HTML→Markdown
步骤4: 小模型处理
```

步骤 1 的域名验证要连 `claude.ai`（Anthropic 云端），国内网络不通。
步骤 2-4 依赖 API 服务端内置能力。

所以不是网络问题、不是配置问题，是 WebFetch 强依赖 Anthropic 基础设施，走第三方 API 代理这条路基本无解。

---

## 二、工具链全景

内置工具中，WebFetch 不能用，但是可以用 WebSearch、以及用 Bash 执行 curl 命令来获取网页内容，还有各种 skill 可以帮助 Agent 来完成搜索、内容获取。经过一番搜查找、测试，敲定了以下工具，可以分为搜索、指定网页获取两类。强烈推荐的有：**AnySearch**、**Summarize、gh（GitHub CLI）、Chrome DevTools MCP**

### 获取指定网页连接实测结果

| 站点                  | 类型         | curl | Summarize | gh  | Agent Browser | Chrome MCP |
| ------------------- | ---------- | ---- | --------- | --- | ------------- | ---------- |
| SkillHub            | SPA        | ❌    | ❌         | —   | ✅             | ✅          |
| 掘金文章                | CSR        | ❌    | ❌         | —   | ✅             | ✅          |
| 微信公众号文章             | CSR        | ❌    | ❌         | —   | ✅             | ✅          |
| B 站视频               | 多媒体        | —    | ✅ 视频摘要    | —   | ⚠️ 仅有页面文字     | ⚠️ 仅有页面文字  |
| GitHub 仓库           | API        | ✅    | ❌         | ✅   | ✅             | ✅          |
| 小红书（登录墙）            | 登录态        | ❌    | ❌         | —   | ❌             | ✅ 登录后      |
| 微信公众号后台             | 登录态        | ❌    | ❌         | —   | ❌             | ✅ 登录后      |
| Taylor & Francis 论文 | Cloudflare | ❌    | ❌         | —   | ❌             | ✅          |
| Google 搜索           | JS 验证      | ❌    | ❌         | —   | ❌             | ✅ 验证一次后正常  |
| 知乎（具体问题页）           | 强反爬+登录态    | ❌    | ❌         | —   | ❌             | ❌ 即使登录也受限  |

### 网页搜索测试结果

| 工具                  | 数据源          | 中文   | 速度  | 代理   | 一句话                 |
| ------------------- | ------------ | ---- | --- | ---- | ------------------- |
| 内置 WebSearch        | 单一（推测 Bing）  | 弱    | 快   | 不需要  | 零配置够用，但覆盖窄          |
| Multi Search Engine | 16 搜索引擎      | 强    | 中   | 国际需要 | 多源交叉验证，国内引擎 curl 直连 |
| Exa                 | embedding 语义 | 差    | 中   | 需要   | 找"类似 X"，英文好，性价比低    |
| AnySearch           | 22 垂直领域      | 弱于英文 | ~4s | 不需要  | 结构化元数据，MCP 一行接入     |


---

## 三、泛搜索

| 工具 | 定位 | 一句话 | 需要配置 |
|---|---|---|---|
| 内置 WebSearch | 日常快速搜 | 零配置，够用 | 否 |
| Multi Search Engine | 多引擎交叉验证 | 16 引擎，中文强 | 国际搜索引擎需要网络环境 |
| Exa | 语义搜索 | "找和 X 类似的东西" | API key |
| AnySearch | 垂直领域结构搜索 | 22 领域，结构化元数据，国内直连 | MCP 一行命令 |


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

**两种使用模式**：

**① curl 模式（国内引擎）** — 直接调用，无需代理：
```bash
# Bing CN，无需代理 — 搜 github 上 Rust 写的 agent-browser
curl "https://cn.bing.com/search?q=site:github.com+agent+browser+Rust"
```
实测结果：Bing CN（✅）、360 搜索（✅）、搜狗（✅）可用；Baidu（❌，验证码页）不可用。

**② Chrome MCP 模式（国际引擎）** — curl 抓国际引擎全部被拦，需借助 Chrome DevTools MCP：

| 引擎 | curl 模式 | Chrome MCP 模式 |
|---|---|---|
| Google / Google HK | JS 验证页面 | ✅ 验证一次后正常 |
| DuckDuckGo | 0 字节 | ✅ 有结果 |
| Yahoo | 0 字节 | ✅ 有结果 + AI 摘要 |
| Startpage | 无结果 | ✅ 有结果 |
| Brave | 连接被拒 | ✅ 有结果 + AI 摘要 |
| Ecosia | 无结果 | ✅ 有结果（Google 广告源） |

```
向 Claude Code 发送："用 Google 搜索：site:stackoverflow.com python tutorial"
```
Claude Code 会自动调用 MCP 打开 Google 搜索页面，拿到完整结果后整理返回。首次需要手动通过 Google 人机验证，验证一次后后续搜索不再被拦。

**结论**：日常用 Bing CN（curl）覆盖国内搜索 + Google（MCP）覆盖国际搜索。curl 抓国际引擎已全部不可用，必须走 Chrome MCP。

### L3: Exa

语义搜索。传统搜索引擎基于关键词倒排索引，Exa 基于 embedding 语义匹配。

```
适用场景：
  "推荐和 Linear 类似的项目管理工具"
  "找用 Rust 写浏览器自动化的开源项目"
  "有没有替代 Playwright 的轻量方案"
```

**实测结论**：
- **英文搜索效果好** — 搜 "Claude Code CLI architecture internals" 返回高质量技术文章（官方文档、Medium 深度分析、arXiv 论文）
- **中文搜索效果差** — 搜 "阿里云 AI 云相关的岗位和技术要求" 返回 DeepMind 专访、GPT-5.5 发布、维基百科等完全不相关的内容，零匹配
- **GitHub 搜索不靠谱** — 搜 "Python AI agent tutorial" 返回 8 个全是个人小项目（stars 个位数），远不如 `gh search` 直接搜 GitHub 靠谱
- **在国内环境性价比低** — 需要代理、中文覆盖弱、$0.01/次收费、和 Chrome MCP 搜索重叠

**结论**：在已有 `gh search` + Chrome MCP 搜索的组合下，Exa 的增量价值有限。免费额度 $10（约 1000 次搜索）用完后需付费，建议仅在有语义搜索刚需时使用。

### L4: AnySearch

AnySearch 定位与前面三者不同：不只是爬公开网页索引，而是聚合了 22 个垂直领域（金融、学术、代码、安全、法律等）的结构化数据源，智能路由查询到最合适的 provider，融合重排序返回。

**集成到 Claude Code**：采用 MCP（Streamable HTTP），一行命令即可。

```bash
# 匿名模式（无需 API key，每日免费配额）
claude mcp add --transport http --scope user anysearch https://api.anysearch.com/mcp

# 带 API key（更高配额，去 https://anysearch.com/console/api-keys 免费注册）
claude mcp add --transport http --scope user anysearch https://api.anysearch.com/mcp -H "Authorization: Bearer <key>"
```

添加后重启 Claude Code，MCP 工具自动注入：`search`、`batch_search`、`list_domains`、`extract`。

**网络**：国内直连，无需代理（`api.anysearch.com` 直连 ~4s）。

**使用体验**：搜索"TypeScript AI agent 框架"，3 个并行查询 ~3.7s 返回 30 条结构化结果（含 GitHub 仓库 stars/语言/license/最近更新等元数据），比内置 WebSearch 的纯文本 snippet 信息量大很多。适合需要结构化数据（代码仓库、学术论文、金融数据等）的场景，日常泛搜仍用内置 WebSearch 更轻量。

**与 Exa 对比**：两者都是第三方搜索 API，但匹配方式不同——Exa 靠 embedding 语义向量，AnySearch 靠垂直领域路由。关键差异：

| 维度 | Exa | AnySearch |
|---|---|---|
| 匹配方式 | embedding 语义 | 领域路由 + 关键词 |
| 代理 | 需要 | 不需要 |
| 中文 | 差 | 弱于英文但可用 |
| 接入 | API key | MCP 一行（可匿名） |
| 强项 | "找和 X 类似的东西" | 代码仓库/学术/金融等结构化搜索 |

**结论**：Exa 在语义联想场景（竞品发现、技术选型）有独特价值，AnySearch 在结构化领域搜索更实用。日常泛搜主力仍是内置 WebSearch，Exa 和 AnySearch 按场景互补。

---

## 四、获取指定网页链接的内容

| 工具                  | 定位        | 搞定什么                                |
| ------------------- | --------- | ----------------------------------- |
| curl                | 最轻量       | 公开 API、SSR 页面、静态 HTML               |
| Summarize           | 多媒体处理     | 视频、音频、PDF                           |
| gh（GitHub CLI）      | GitHub 专用 | 仓库信息、README、Issue、PR                |
| Chrome DevTools MCP | 真实浏览器     | 强反爬站点（Cloudflare）、Google 搜索、性能/网络分析 |
| Agent Browser       | 无头浏览器     | SPA、JS 动态页面、需要交互操作的页面、登录态复用（独立 CLI） |

### L1: curl

curl 是一个命令行 HTTP 客户端，几乎所有系统自带。在 Claude Code 中通过 Bash 调用，直接拿到网页原始响应。

| 网站类型        | 策略                       | 示例                                                                  |
| ----------- | ------------------------ | ------------------------------------------------------------------- |
| 公开 REST API | 直接调 API                  | `curl -sL "https://api.github.com/repos/vercel-labs/agent-browser"` |
| SSR 页面      | Googlebot UA + 解析内嵌 JSON | 知乎：`<script id="js-initialData">`                                   |
| 静态 HTML     | 直接抓                      | `curl -sL "https://httpbin.org/html"`                               |
| CSR/SPA 页面  | 无法获取内容                   | 返回空壳 `<div id="app"></div>`，无实际内容                                   |

> **什么是 Googlebot UA**：请求时把 User-Agent 伪装成 Google 爬虫的标识（`Mozilla/5.0 (compatible; Googlebot/2.1)`）。很多网站为了 SEO 会向爬虫返回完整的 SSR 渲染内容，而普通浏览器拿到的是空壳 + JS，所以 curl 配上这个 UA 就能直接拿到有内容的 HTML。


### L2: Summarize

Summarize 是一个 CLI 内容总结工具，支持网页、PDF、图片、音频、YouTube 等格式。底层用 yt-dlp 拉取视频字幕、用 Firecrawl 抓取网页，然后调用 LLM 生成摘要。支持 OpenAI / Anthropic / Gemini / xAI 等多种后端。

**注意**：
- **SPA 站点无法获取内容** — Firecrawl 无法执行 JS，只能拿到 `<meta>` 标签，实际页面内容为空
- **Cloudflare 等反爬直接 403** — 无真实浏览器环境，无法通过人机验证
- 因此，summarize 在处理普通网页时不如 curl（curl 抓 SSR 页面 → 会话中直接分析），它的核心价值在于**视频、音频、PDF 等多媒体格式**

安装：
```bash
skillhub install summarize          # 安装 skill 说明
npm install -g @steipete/summarize  # 安装 CLI 本体
```

配置 DeepSeek API：
```json
// ~/.summarize/config.json
{
  "model": "openai/deepseek-v4-flash",
  "env": {
    "OPENAI_BASE_URL": "https://api.deepseek.com",
    "OPENAI_API_KEY": "sk-xxx"
  }
}
```

配置完成后，直接运行：
```bash
summarize "https://example.com"
```

在我们的场景中，普通网页文章直接用 curl 抓取、在会话中分析即可，Summarize 对此没有增量价值。它真正发挥作用的地方是**会话无法直接处理的内容**——视频、音频、PDF 等多媒体文件。

实测 B 站视频：
```bash
summarize "https://www.bilibili.com/video/BV1iuVW6hEqD/"
```
输出：
```
### 全自研芯片量产
比亚迪在发布会上宣布4nm全自研芯片实现量产，这是其核心技术的重大突破，标志着比亚迪在芯片领域实现自主可控。

### 智驾赔付政策
比亚迪推出智驾系统在事故中撞了全额赔付的政策，以此增强用户对自动驾驶安全性的信心，降低使用门槛。

### 行业颠覆效应
比亚迪通过芯片自研和赔付承诺，意图颠覆整个汽车行业，展现出从车厂向全产业链科技企业转型的决心。

11s · 174 words · openai/deepseek-v4-flash · ↑5.1k ↓873 Δ6.3k
```

### L3: gh（GitHub CLI）

gh 是 GitHub 官方提供的命令行工具，将 GitHub 的仓库管理、Issue 与 Pull Request 协作、CI 工作流状态查询以及 API 调用等功能整合进终端环境中，使用者无需打开浏览器即可完成大部分 GitHub 日常操作。
与使用 curl 获取 github 仓库信息相比，gh 内置了认证管理和自动分页机制，配合 `--jq` 参数可对返回结果进行结构化过滤，在需要频繁获取仓库信息或进行复杂查询的场景下更为便捷。

**安装 skill 和 gh CLI：**
```bash
skillhub install github

# Windows (winget)
winget install GitHub.cli

# macOS
brew install gh

# Linux
sudo apt install gh
```

**认证（首次使用）：**
```bash
gh auth login   # 浏览器授权或 token 粘贴
```

**使用场景-仓库搜索：**
```bash
# 按 star 排行搜索 Python 写的 AI agent 框架
gh search repos "AI agent framework" --language python --sort stars --limit 10

# 搜索本月新建的热门仓库
gh search repos "created:>2026-05-01" --sort stars --limit 20

```
### L4: Chrome DevTools MCP

**Chrome DevTools MCP** 是 Google Chrome 官方出品的 MCP 服务器，让 AI 编码助手能直接控制一个真实 Chrome 浏览器实例。底层走 CDP 协议，启动的是**完整 Chrome**（非无头精简版），浏览器指纹和正常用户一致，可以通过 Cloudflare 等反爬验证。

**安装（MCP 服务器）：**
```bash
claude mcp add chrome-devtools --scope user -- npx chrome-devtools-mcp@latest --no-usage-statistics
```

重启 Claude Code 后验证连接：向 Claude 发送"打开 https://example.com/ 网页，看看内容"。成功返回页面信息说明连接正常。

**核心工作流**：
```
navigate_page <url>     → 打开页面
take_snapshot           → 拿到可访问性树（uid=1_0, uid=1_1...）
click / fill @uid       → 操作元素
evaluate_script "..."   → 执行 JS（如获取完整 HTML）
```

**为什么能过 Cloudflare/Google 人机验证**：
- curl / Agent Browser → 全新启动无头浏览器 → 自动化指纹被识别 → 拦截
- Chrome DevTools MCP → 启动**真实 Chrome 实例** → 浏览器指纹正常 → 直接放行

**注意：MCP 浏览器与日常 Chrome 不共享登录态**

MCP 启动的是一个独立的 Chrome 实例，自带独立的 `--user-data-dir`（用户数据目录）。它与用户日常使用的 Chrome 是两个不同的 profile，两者之间的 Cookie 不共享，因此登录态不互通。

这意味着：你在日常 Chrome 中已登录的账号（如 GitHub、微信公众平台后台等），在 MCP 浏览器中需要重新登录一次。但登录一次后，MCP 会保存该状态，后续无需重复登录。

实测对比：

| 站点 | curl | Agent Browser | Chrome MCP |
|---|---|---|---|
| Taylor & Francis（Cloudflare） | 安全质询 | 人机验证 | ✅ 完整页面 |
| Google 搜索 | JS 验证 | 人机验证 | ✅ 人工验证一次后正常 |

**与 Agent Browser 的关系**：
- 两者都走 CDP 协议，能力上限相同
- Agent Browser 独有：`state save/load`（登录态持久化到文件）、视频录制、不依赖 MCP 客户端的独立 CLI
- 日常优先用 MCP；需要跨 session 复用登录态或在无 MCP 环境（纯 CLI）中使用时，用 Agent Browser


### L5: Agent Browser

**Agent Browser** 是基于 Rust 的无头浏览器 CLI 封装。底层走 CDP（Chrome DevTools Protocol），和 Playwright、Puppeteer 走同一套协议。核心差异是专门优化了 **AI Agent 友好**的交互方式， 直接把 DOM 转成带编号的可访问性树，AI 不需要自己写 CSS 选择器或 XPath，直接对编号发指令即可。

安装：
```bash
skillhub install agent-browser       # 安装 skill 说明
npm install -g agent-browser         # 安装 CLI 本体
agent-browser install                # 下载 Chrome（183MB，配代理更快）
```

**核心工作流**：四步循环
```
open <url>       → 打开页面
snapshot -i      → 拿到可交互元素清单（@e1, @e2...）
click/fill @eN   → 对编号元素操作
get text @e1     → 获取元素文本
snapshot -i      → 页面变化后重新快照，获取新编号
```

验收结论——同一个 SPA 站点：
- curl → 空壳 `<div id="app"></div>`
- Agent Browser → 完整 DOM，导航/标题/按钮/链接全拿到

---

### L6: CDP 直连

当目标网站（如 DCD、路透社等）使用 Cloudflare Turnstile 等反爬机制时，MCP 自动化浏览器无法通过验证。此时可通过 **手动 Chrome + CDP 协议** 作为降级方案。

```
MCP 自动化浏览器 --被 Cloudflare 拦截--> ❌
手动 Chrome（已通过真人验证）--通过 CDP 连接--> ✅
```

**操作步骤**

**步骤一：启动可调试的 Chrome 实例**

关闭所有 Chrome 窗口，然后运行：

```powershell
Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--remote-debugging-port=9222 --user-data-dir=$env:TEMP\chrome-debug"
```

| 参数 | 作用 |
|------|------|
| `--remote-debugging-port=9222` | 开启远程调试端口，CDP 通过该端口连接 |
| `--user-data-dir=...` | 指定独立用户数据目录，避免与正在运行的 Chrome 冲突 |

**步骤二：手动打开目标网址**

在刚启动的 Chrome 中手动访问需要验证的网站，完成：

- Cloudflare Turnstile 勾选"我不是机器人"
- 其他 CAPTCHA 验证

页面正常加载后，**保持标签页打开**，不要关闭。

**步骤三：通过 CDP 协议连接并操作**

**3.1 查看已打开的标签页**

```bash
curl http://127.0.0.1:9222/json/list
```

返回示例：

```json
[
  { "id": "9BF582B8...", "title": "Microsoft details...", "url": "https://..." }
]
```

记录目标页面的 `id`。

**3.2 读取页面内容**

```javascript
const ws = new WebSocket('ws://127.0.0.1:9222/devtools/page/{pageId}');

ws.addEventListener('open', () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: {
      expression: 'document.body.innerText.substring(0, 20000)',
      returnByValue: true
    }
  }));
});

ws.addEventListener('message', (event) => {
  console.log(event.data);
  ws.close();
});
```

**3.3 其他常用 CDP 操作**

| 操作 | CDP 方法 | 说明 |
|------|---------|------|
| 导航新页面 | `Page.navigate` | `params: { url: "..." }` |
| 截图 | `Page.captureScreenshot` | 返回 base64 图片 |
| 执行 JS | `Runtime.evaluate` | 任意 JS 代码 |
| 获取控制台日志 | `Runtime.consoleAPICalled` | 需先监听事件 |
| 获取页面标题 | `Runtime.evaluate` | `expression: "document.title"` |

**适用场景**

| 场景 | MCP 可直接处理 | 需手动 Chrome + CDP |
|------|:-------------:|:-------------------:|
| 无反爬的普通网站 | ✅ | ❌ |
| Cloudflare Turnstile | ❌ | ✅ |
| DataDome CAPTCHA | ❌ | ✅ |
| Google 系验证码 | ❌ | ✅ |
| 需要登录态/SSO 的网站 | ⚠️ 部分支持 | ✅ 复用已登录会话 |

**注意事项**

1. **端口冲突**：若 9222 被占用，可改用其他端口（如 9223）
2. **用户数据目录**：每次用完 `$env:TEMP\chrome-debug` 可手动删除，避免缓存干扰下次使用
3. **安全性**：远程调试端口开放期间，本机任何进程都可控制该浏览器，用完建议关闭 Chrome
4. **CDP 无状态**：每次操作需通过 WebSocket 发送完整 JSON 命令，MCP 封装的便利性（click、fill、screenshot 等）在此方案中需自行实现

**对比：MCP vs 裸 CDP**

| 维度 | MCP chrome-devtools | 手动 Chrome + CDP |
|------|-------------------|-------------------|
| 配置复杂度 | 低，一行配置即可 | 中，需启动 Chrome + 手写代码 |
| 绕过 Cloudflare | ❌ | ✅ |
| 工具丰富度 | 40+ 封装好的工具 | 需手写所有命令 |
| AI 友好度 | AI 直接调 tool | 需生成 JS 代码执行 |
| 适用场景 | 日常自动化 | Cloudflare 等反爬场景的降级方案 |