# 工具安装参考

该文档记录了 Smart Search 技能依赖的所有工具的安装方法。

---

## 1. curl（系统自带）

Windows 10+ / macOS / Linux 通常已预装。验证：

```bash
curl --version
```

如未安装：
- **Windows**: 下载 https://curl.se/windows/ 或 `winget install curl`
- **macOS**: `brew install curl`
- **Linux**: `sudo apt install curl`

---

## 2. Node.js

部分 CDP 脚本依赖 Node.js。验证：

```bash
node --version
```

安装：
- **Windows**: https://nodejs.org/ 下载 LTS 版本
- **macOS**: `brew install node`
- **Linux**: `sudo apt install nodejs npm`

---

## 3. Chrome DevTools MCP（推荐，主力工具）

Chrome 官方出品的 MCP 服务器，启动真实 Chrome 实例供 AI 操作。

```bash
claude mcp add chrome-devtools --scope user -- npx chrome-devtools-mcp@latest --no-usage-statistics
```

重启 Claude Code 后验证：

```
向 Claude 发送：打开 https://example.com/ 看看内容
```

如果能正常返回页面信息，说明连接成功。

**注意**：MCP 启动的是独立 Chrome 实例，与日常 Chrome 不共享登录态。

---

## 4. Summarize（视频/音频/PDF 摘要）

```bash
# 安装 CLI 本体
npm install -g @steipete/summarize

# 安装 skill 说明（可选）
skillhub install summarize
```

配置 DeepSeek API（推荐，国内可用）：

```json
// ~/.summarize/config.json
{
  "model": "openai/deepseek-v4-flash",
  "env": {
    "OPENAI_BASE_URL": "https://api.deepseek.com",
    "OPENAI_API_KEY": "sk-你的key"
  }
}
```

验证：

```bash
summarize "https://www.bilibili.com/video/BV1iuVW6hEqD/"
```

---

## 5. gh（GitHub CLI）

```bash
# 安装 CLI
# Windows
winget install GitHub.cli

# macOS
brew install gh

# Linux
sudo apt install gh

# 安装 skill 说明（可选）
skillhub install github
```

首次认证：

```bash
gh auth login   # 浏览器授权或 token 粘贴
```

验证：

```bash
gh search repos "AI agent" --language python --sort stars --limit 3
```

---

## 6. ws（Node.js WebSocket 模块）

用于 CDP 直连时通过 WebSocket 协议与 Chrome 调试端口通信。

```bash
npm install -g ws
```

验证：

```bash
node -e "require('ws'); console.log('ws 可用')"
```

---

## 安装检查清单

| 工具 | 用途 | 验证命令 | 必备/可选 |
|------|------|---------|----------|
| curl | 轻量 HTTP 请求 | `curl --version` | 必备 |
| Node.js | CDP 脚本运行 | `node --version` | 必备 |
| Chrome DevTools MCP | 真实浏览器操作 | 配置后向 Claude 发指令 | ⭐ 强烈推荐 |
| summarize | 视频/音频摘要 | `summarize --help` | 可选 |
| gh | GitHub 操作 | `gh --version` | 可选 |
| ws (npm) | CDP WebSocket | `node -e "require('ws')"` | 推荐（CDP 降级用） |
