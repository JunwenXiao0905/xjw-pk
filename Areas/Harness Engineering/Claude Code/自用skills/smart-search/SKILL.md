---
name: Smart Search
description: A decision-tree-based search and content retrieval skill. Knows when WebFetch works, when Chrome MCP is enough, and when to fall back to user-assisted CDP direct connection for anti-bot sites.
read_when:
  - Searching for information online
  - Fetching content from a specific URL
  - Needing to bypass Cloudflare / anti-bot restrictions
  - Getting "blocked" or "verification required" errors from websites
allowed-tools: Bash( curl node npm npm-exec )
---

# Smart Search — 搜索与内容获取决策树

## 〇、依赖检查

在开始搜索或内容获取之前，先检查各工具的可用性：

```bash
# === 必备工具 ===
echo "=== curl ===" && curl --version | head -1
echo "=== Node.js ===" && node --version

# === 推荐工具 ===
echo "=== Chrome DevTools MCP ===" && claude mcp list 2>/dev/null | grep -i chrome || echo "❌ 未安装"
echo "=== ws (WebSocket) ===" && node -e "require('ws'); console.log('✅ 可用')" 2>/dev/null || echo "❌ 未安装"

# === 可选工具 ===
echo "=== gh ===" && gh --version 2>/dev/null | head -1 || echo "❌ 未安装"
echo "=== summarize ===" && summarize --version 2>/dev/null || echo "❌ 未安装"
```

缺了工具不要慌，按需安装即可。各工具的详细安装方法见同目录下的 [`TOOLS_INSTALL.md`](TOOLS_INSTALL.md)。

### 工具依赖速览

| 工具 | 用途 | 优先级 |
|------|------|--------|
| **curl** | 轻量 HTTP 请求（公开 API、SSR 页面） | ⭐ 必备 |
| **Node.js** | 运行 CDP 脚本 | ⭐ 必备 |
| **Chrome DevTools MCP** | 真实浏览器操作，处理 90% 的页面 | ⭐ 强烈推荐 |
| **ws** (npm) | CDP WebSocket 通信 | 🔧 推荐（CDP 降级用） |
| **gh** | GitHub 操作 | 🔧 可选（GitHub 场景用） |
| **summarize** | 视频/音频/PDF 摘要 | 🔧 可选（视频场景用） |

---

## 一、WebFetch 的限制

WebFetch 依赖 Anthropic 云端基础设施（域名安全验证在 claude.ai 进行），国内网络环境下**基本不可用**，会报错。遇到以下情况时不要反复重试：

| 场景 | 原因 |
|------|------|
| 所有 HTTP/HTTPS 页面 | 域名验证环节连不上 claude.ai |
| SPA/CSR 页面（掘金、公众号文章等） | 即使连上也只拿到空壳 HTML |
| Cloudflare 反爬站点 | 返回 403 安全质询页 |
| 需要登录态的页面 | 没有任何认证机制 |

遇到需要获取页面内容时，走下面的决策树。

---

## 二、内容获取决策树

目标是「从指定 URL 获取页面内容」。按优先级依次尝试：

### L1：curl（最轻量，适合公开接口和 SSR 页面）

```bash
# 公开 REST API
curl -sL "https://api.github.com/repos/vercel-labs/agent-browser"

# SSR 页面 + Googlebot UA（模拟爬虫绕过轻量限制）
curl -sL -A "Mozilla/5.0 (compatible; Googlebot/2.1)" "https://example.com/article"
```

适用范围：
| 类型 | 是否可行 |
|------|---------|
| 公开 REST API（GitHub API 等） | ✅ |
| SSR/服务端渲染页面 | ✅ 配合 Googlebot UA |
| 静态 HTML 页面 | ✅ |
| SPA/CSR 页面（Vue/React 渲染） | ❌ 返回空壳 |
| Cloudflare 保护页面 | ❌ 403 |

### L2：Chrome DevTools MCP（主力工具，处理 90% 情况）

对于 curl 拿不到的 SPA/CSR/动态页面，使用内置的 Chrome DevTools MCP 工具，流程如下：

```
navigate_page <url>   → 打开页面（等待完全加载）
take_snapshot          → 从无障碍树获取完整内容
（可选）evaluate_script "document.body.innerText"  → 直接拿纯文本
（可选）take_screenshot → 截取页面截图辅助判断
```

这个 MCP 启动的是**真实 Chrome 实例**，指纹和正常浏览器一致，能通过大部分反爬检测。

> ⚠️ **注意**：Chrome MCP 启动的是独立的 Chrome 实例，与用户日常使用的 Chrome 不共享 Cookie 和登录态。如果需要登录态，必须在 MCP 的 Chrome 中手动登录一次。

### L3：Summarize（仅限视频/音频/PDF）

```bash
summarize "https://www.bilibili.com/video/BVxxxx"
summarize "https://youtube.com/watch?v=xxxx"
```

适用范围：
| 类型 | 是否可行 |
|------|---------|
| B 站视频 | ✅ 生成文字摘要 |
| YouTube 视频 | ✅ 生成文字摘要 |
| PDF 文档 | ✅ |
| 普通网页 | ❌ 不如 curl / Chrome MCP |

### L4：gh（GitHub CLI，仅限 GitHub）

```bash
# 搜索仓库
gh search repos "AI agent framework" --language python --sort stars --limit 10

# 获取 README
gh repo view owner/repo

# 查看 Issue / PR
gh issue view 42
gh pr view 123
```

### 决策汇总表

```
要获取某个 URL 的内容 ↓
├── URL 是 GitHub 仓库/Issue/PR → gh CLI
├── URL 是 B站/YouTube 视频     → Summarize
├── URL 是公开 API（GitHub API 等）→ curl
├── URL 是 SSR/静态页面          → curl（加 Googlebot UA）
├── URL 是普通网页               → Chrome MCP ← 主力
└── Chrome MCP 被拦截            → 手动 Chrome + CDP（见第四章）
```

---

## 三、搜索决策树

目标是搜索信息（而非指定 URL），按场景选择：

### 国内内容 → 内置 WebSearch

```text
零配置，直接自然语言搜索即可：
  "搜索：马来西亚 数据中心 2024 政策"
```

Claude Code 会调用 WebSearch 工具，数据源推测为 Bing。

### 国际内容 → Chrome MCP + Google 搜索

当搜索英文资料、外网内容、或 WebSearch 覆盖不足时：

```
1. navigate_page "https://www.google.com/search?q=site:bloomberg.com+Google+Malaysia+data+center"
2. 首次需要手动过 Google 人机验证（验证一次后续不再弹出）
3. take_snapshot → 读取搜索结果
4. 点击结果链接 → 读取目标页面内容
```

> **为什么用 Google 搜索？** 内置 WebSearch 推测基于 Bing，中文覆盖弱，国际内容不够全。Google 搜索配合 Chrome MCP 是当前最可靠的国际搜索方案。

### 搜索决策汇总表

```
需要搜索 ↓
├── 中文/国内内容     → 内置 WebSearch（零配置）
├── 英文/国际/专业内容 → Chrome MCP + Google 搜索
└── 始终无法搜索      → 手动 Chrome + CDP（见第四章）
```

---

## 四、CDP 降级方案：手动 Chrome + 直连

### ⚠️ 什么时候用这个方案

当以下情况出现时，说明 Chrome MCP 的自动化实例被识别为机器人，需要降级到用户手动操作：

- Google 搜索弹出「系统检测到您的网络有异常流量」/ 无限人机验证
- Cloudflare Turnstile 无法通过（页面卡在安全验证）
- 目标网站（如 DCD、路透社等）使用高级反爬机制
- 需要已有登录态的页面（且不方便在 MCP Chrome 中重新登录）

### 工作流程

#### 步骤一：用户启动可调试 Chrome

```powershell
# 关闭所有 Chrome 窗口后，运行：
Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--remote-debugging-port=9222 --user-data-dir=$env:TEMP\chrome-debug"
```

参数说明：
| 参数 | 作用 |
|------|------|
| `--remote-debugging-port=9222` | 开启远程调试端口 |
| `--user-data-dir=$env:TEMP\chrome-debug` | 独立用户目录，不干扰日常 Chrome |

#### 步骤二：用户手动操作

1. 在刚打开的 Chrome 中访问目标网址
2. 完成所有验证（Cloudflare Turnstile、Google 人机验证、登录等）
3. **保持页面打开，不要关闭**

#### 步骤三：Claude 连接并读取内容

**3.1 验证 Chrome 实例是否在运行：**

```bash
curl -s http://127.0.0.1:9222/json/list | node -e "
const data = [];
process.stdin.on('data', d => data.push(d));
process.stdin.on('end', () => {
  const pages = JSON.parse(data.join(''));
  pages.forEach((p, i) => console.log(i + ':', p.title, '→', p.url));
});
"
```

输出示例：
```
0: Google Search → https://www.google.com/search?q=...
1: Data Center... → https://www.datacenterdynamics.com/...
```

记下目标页面的索引号。

**3.2 使用 CDP 读取页面内容：**

```bash
node -e "
const http = require('http');
const PAGE_INDEX = 0;  // ← 替换为目标页面的索引号

// 获取页面列表
http.get('http://127.0.0.1:9222/json/list', (res) => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    const pages = JSON.parse(data);
    const page = pages[PAGE_INDEX];
    if (!page) { console.error('Page not found'); process.exit(1); }
    
    const wsUrl = page.webSocketDebuggerUrl;
    const id = wsUrl.match(/page\/([^\/]+)/)[1];
    
    // /json/activate 只是把目标标签页前置到前台，本身不读取内容
    http.get('http://127.0.0.1:9222/json/activate/' + id, () => {});

    // 真正读取页面内容必须走 CDP WebSocket（见 3.3），HTTP /json/* API 无此能力
    
    console.log('Page:', page.title);
    console.log('URL:', page.url);
    console.log('\\nPage is open and ready. Use the methods below to extract content.');
  });
});
"
```

**3.3 获取页面全文（核心）：**

```bash
# 如果系统中已安装 ws 模块
node -e "
const http = require('http');
const WebSocket = require('ws');
const PAGE_INDEX = 0;  // ← 替换为目标页面的索引号

http.get('http://127.0.0.1:9222/json/list', (res) => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    const page = JSON.parse(data)[PAGE_INDEX];
    if (!page) { console.error('Page not found'); process.exit(1); }
    const ws = new WebSocket(page.webSocketDebuggerUrl);
    ws.on('open', () => {
      ws.send(JSON.stringify({
        id: 1,
        method: 'Runtime.evaluate',
        params: { expression: 'document.body.innerText.substring(0, 50000)', returnByValue: true }
      }));
    });
    ws.on('message', (raw) => {
      const msg = JSON.parse(raw);
      if (msg.id === 1 && msg.result) {
        console.log(msg.result.result.value);
        ws.close();
        process.exit(0);
      }
    });
    setTimeout(() => process.exit(1), 15000);
  });
});
" 2>/dev/null || echo "ws 模块未安装，请运行: npm install -g ws"
```

> **备用方法**：如果 `ws` 模块未安装，可使用 Chrome DevTools MCP 中的 `evaluate_script` 工具来执行等效操作（但需确保 MCP 的 Chrome 已通过同一验证）。

**3.4 保存完整 HTML（可选）：**

```bash
node -e "
const WebSocket = require('ws');
const http = require('http');
http.get('http://127.0.0.1:9222/json/list', (res) => {
  let d = '';
  res.on('data', c => d += c);
  res.on('end', () => {
    const page = JSON.parse(d)[0];
    const ws = new WebSocket(page.webSocketDebuggerUrl);
    ws.on('open', () => {
      ws.send(JSON.stringify({
        id: 1, method: 'Runtime.evaluate',
        params: { expression: 'document.documentElement.outerHTML', returnByValue: true }
      }));
    });
    ws.on('message', (raw) => {
      const msg = JSON.parse(raw);
      if (msg.id === 1 && msg.result) {
        require('fs').writeFileSync('page.html', msg.result.result.value);
        console.log('Saved to page.html');
        ws.close();
        process.exit(0);
      }
    });
  });
});
"
```

### 完整 CDP 使用流程

```
用户收到提示 ↓
用户启动 Chrome（port 9222）并访问目标网址 ↓
用户完成验证/登录并保持页面打开 ↓ ─── 后续所有搜索都优先用此实例
Claude 验证连接：
  curl http://127.0.0.1:9222/json/list  ← 确认实例在运行
Claude 读取内容：
  node CDP 脚本 → 获取页面全文 ↓
Claude 分析和整理信息
```

### 多页面操作

在一个已打开的页面中执行 JS 来导航：

```javascript
// 导航到新页面
await page.navigate('https://example.com');

// 获取新页面内容
const text = document.body.innerText;
```

具体通过 CDP 协议发送 `Page.navigate` 命令即可在不打开新标签页的情况下切换页面。

### 注意事项

1. **端口冲突**：若 9222 被占用，改用 9223 等其他端口
2. **一次性使用**：`$env:TEMP\chrome-debug` 用完可手动删除
3. **安全风险**：远程调试端口开放期间，本机任何进程都可控制该浏览器，用完建议关闭 Chrome
4. **验证持久化**：在 `--user-data-dir` 指定的独立 Chrome 中通过验证后，下次启动同一目录时验证状态仍在，无需重复验证

---

## 五、完整工作流示例

### 示例：搜索并获取一篇关于 Google 马来西亚数据中心的外媒报道

```
1. 内置 WebSearch 初步搜索
   → 找到 Datacenter Dynamics 的链接

2. 尝试 Chrome MCP 打开
   → navigate_page "https://www.datacenterdynamics.com/..."
   → 发现 Cloudflare 拦截

3. 告知用户启动手动 Chrome + CDP
   → 用户启动 Chrome:9222，手动访问该链接，过 Cloudflare

4. 验证连接
   → curl http://127.0.0.1:9222/json/list
   → 确认页面已打开

5. 读取内容
   → node CDP 脚本 → document.body.innerText
   → 拿到完整文章内容

6. 整理信息并输出
```

### 示例：搜索谷歌云竞争对手信息

```
1. 内置 WebSearch 搜索 "Google Cloud Malaysia competitor analysis"
   → 结果不够

2. Chrome MCP + Google 搜索
   → navigate_page "https://www.google.com/search?q=Google+Cloud+Malaysia+competitor+2025"
   → 首次需要过验证，后续正常

3. 点击搜索结果
   → 仔细阅读每篇文章

4. 汇总信息
```

---

## 六、常用网址模板

### Google 搜索模板

```
# 普通搜索
https://www.google.com/search?q={关键词}

# 限定站点
https://www.google.com/search?q=site:{域名}+{关键词}

# 限定时间范围
https://www.google.com/search?q={关键词}&tbs=qdr:y1  # 过去一年
https://www.google.com/search?q={关键词}&tbs=qdr:m6  # 过去6个月

# 限定文件类型
https://www.google.com/search?q={关键词}+filetype:pdf
```

### Bing CN 搜索（curl 直连，无需代理）

```bash
# 无需 Googlebot UA，Bing CN 可直接访问
curl -sL "https://cn.bing.com/search?q=site:bloomberg.com+Google+Malaysia+data+center"
```

---

## 七、工具选择速查表

### 搜索类

| 场景 | 工具 | 配置 |
|------|------|------|
| 中文/国内内容 | 内置 WebSearch | 零配置 |
| 国际/英文内容 | Chrome MCP + Google | 首次需过验证 |
| 被拦截 | 手动 Chrome + CDP | 用户启动 Chrome:9222 |

### 内容获取类

| 场景 | 工具 | 备选 |
|------|------|------|
| GitHub 仓库/Issue/PR | `gh` CLI | curl + GitHub API |
| B站/YouTube 视频 | `summarize` | — |
| 公开 API | `curl` | — |
| SSR/静态页面 | `curl` + Googlebot UA | — |
| SPA/动态页面 | Chrome MCP | 手动 Chrome + CDP |
| 被 Cloudflare 拦截 | 手动 Chrome + CDP | — |
| 需登录态页面 | 手动 Chrome + CDP（用户已登录） | — |
