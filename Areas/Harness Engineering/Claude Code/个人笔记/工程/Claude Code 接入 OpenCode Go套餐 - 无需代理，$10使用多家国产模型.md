# Claude Code 接入 OpenCode Go 套餐- 无需代理，$10使用多家国产模型

> OpenCode Go 是一项低成本的订阅服务 —— **首月 5 美元**，之后 **每月 10 美元** —— 能够稳定地访问流行的开源编程模型。

## 目录

- [[#第1章 代理架构与安装]]
  - [[#1.1 数据流与组件关系]]
  - [[#1.2 二进制安装与 PATH 配置]]
  - [[#1.3 初始化与启动]]
- [[#第2章 Claude Code 接入配置]]
  - [[#2.1 模型兼容情况]]
  - [[#2.2 cc-switch 方案配置]]
  - [[#2.3 模型切换命令]]
- [[#第3章 模型路由机制]]
  - [[#3.1 自动路由（models）]]
  - [[#3.2 强制路由（model_overrides）]]
  - [[#3.3 容灾链（fallbacks）]]
  - [[#3.4 路由优先级]]

---

# 第1章 代理架构与安装

## 1.1 数据流与组件关系

```
Claude Code → oc-go-cc (127.0.0.1:3456) → OpenCode Go → 开源模型
```

oc-go-cc 拦截 Anthropic Messages API 请求，转换为 OpenAI Chat Completions 格式转发到 OpenCode Go，响应再转回 Anthropic 格式。Claude Code 无感知。

## 1.2 二进制安装与 PATH 配置

从 [samueltuyizere/oc-go-cc](https://github.com/samueltuyizere/oc-go-cc) releases 下载 `oc-go-cc_windows-amd64.exe`，放入 PATH 目录（如 `D:\xxxx\nodejs\node_global\`）。

oc-go-cc 是 CLI 工具，依赖终端参数（如 `serve`、`init`）运行，双击无窗口会直接退出。放入 PATH 后可在任意目录直接执行命令，无需写完整路径。

验证：

```bash
oc-go-cc --version
# 0.3.0
```

## 1.3 初始化与启动

```bash
# 生成默认配置 ~/.config/oc-go-cc/config.json
oc-go-cc init
# Created default config at C:\Users\Administrator\.config\oc-go-cc\config.json
# Edit the file and add your OpenCode Go API key.
```

打开 `~/.config/oc-go-cc/config.json`，将 `api_key` 字段的值从 `${OC_GO_CC_API_KEY}` 替换为实际的 OpenCode Go API Key，保存文件。

启动代理：

**Bash：**

```bash
nohup oc-go-cc serve > /tmp/oc-go-cc.log 2>&1 &
```

**PowerShell：**

```powershell
Start-Process -NoNewWindow oc-go-cc serve
```

启动输出示例：

```
Starting oc-go-cc v0.3.0
Listening on 127.0.0.1:3456
Forwarding to: https://opencode.ai/zen/go/v1/chat/completions

Configure Claude Code with:
  export ANTHROPIC_BASE_URL=http://127.0.0.1:3456
  export ANTHROPIC_AUTH_TOKEN=unused
```

默认监听 `127.0.0.1:3456`，转发到 `https://opencode.ai/zen/go/v1/chat/completions`。需要给 Claude Code 配置 `ANTHROPIC_BASE_URL` `ANTHROPIC_AUTH_TOKEN` 环境变量

关闭服务
```
oc-go-cc stop
```

---

# 第2章 Claude Code 接入配置

## 2.1 模型兼容情况

| 模型 | 非流式 | 流式 | 备注 |
|------|--------|------|------|
| glm-5 | ✅ | ✅ | 稳定 |
| glm-5.1 | ✅ | ✅ | 稳定 |
| kimi-k2.6 | ✅ | ✅ | 稳定 |
| kimi-k2.5 | ✅ | ✅ | 稳定 |
| mimo-v2.5-pro | ✅ | ✅ | 稳定 |
| deepseek-v4-pro | ✅ | ✅ | 稳定 |
| deepseek-v4-flash | ✅ | ✅ | 稳定 |
| qwen3.7-plus | ✅ | ❌ 500 | 仅非流式可用 |
| qwen3.6-plus | ✅ | ❌ 500 | 仅非流式可用 |
| qwen3.5-plus | ✅ | ❌ 500 | 仅非流式可用 |
| minimax-m3 | ✅ | ❌ 400 | 含 tools 时不可用 |
| minimax-m2.7 | ✅ | ❌ 400 | 含 tools 时不可用 |
| minimax-m2.5 | ✅ | ❌ 400 | 含 tools 时不可用 |

Qwen 系列流式请求间歇性 500，MiniMax 在含 tools 时返回 `function name or parameters is empty (2013)`。fallback 链建议仅使用稳定模型。

## 2.2 cc-switch 方案配置

![[Pasted image 20260612004321.png]]

![[Pasted image 20260612004402.png]]

```json
{
  "name": "oc-go-cc",
  "ANTHROPIC_BASE_URL": "http://127.0.0.1:3456",
  "ANTHROPIC_AUTH_TOKEN": "unused",
  "ANTHROPIC_MODEL": "kimi-k2.6",
  "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3.7-plus",
  "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5",
  "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash"
}
```

`ANTHROPIC_BASE_URL` 指向代理地址，`ANTHROPIC_AUTH_TOKEN` 传任意值（代理不验证，使用 `OC_GO_CC_API_KEY` 访问 OpenCode Go）。

---

# 第3章 oc-go-cc 模型路由机制

## 3.1 自动路由（models）

代理根据请求内容分析场景，自动选择模型：

| 场景 | 触发条件 | 默认模型 |
|------|---------|---------|
| `default` | 普通对话 | kimi-k2.6 |
| `background` | 读文件、grep 等轻量操作 | qwen3.5-plus |
| `think` | prompt 含 "think"/"plan"/"reason" | glm-5 |
| `complex` | "architect"/"refactor" 等复杂词 | glm-5.1 |
| `long_context` | 超过 80000 token | minimax-m2.5 |
| `fast` | 流式加速 | qwen3.6-plus |

## 3.2 强制路由（model_overrides）

当请求 `model` 字段匹配 `model_overrides` 中的 key 时，跳过自动路由，直连指定模型。

```json
"model_overrides": {
  "qwen3.7-plus": {
    "provider": "opencode-go",
    "model_id": "qwen3.7-plus",
    "temperature": 0.7,
    "max_tokens": 16384
  }
}
```

## 3.3 容灾链（fallbacks）

主模型失败后按链式 fallback 尝试下一个模型。每个模型有熔断器：连续 3 次失败跳过 30 秒。

```json
"fallbacks": {
  "default": [
    { "provider": "opencode-go", "model_id": "mimo-v2.5-pro" },
    { "provider": "opencode-go", "model_id": "glm-5" }
  ]
}
```

## 3.4 路由优先级

请求到达时的选择顺序：

1. `model_overrides[<model>]` — 请求 model 字段命中 override，直连指定模型
2. `respect_requested_model` — 若启用且 `models[<model>]` 存在，使用请求模型
3. 场景路由 — 按内容分析匹配 `default` / `background` / `think` / `complex` / `long_context` / `fast`

```
model_overrides 命中？
  ├─ 是 → 直连 override 模型
  └─ 否 → 内容分析 → 场景路由 → 主模型
              ↓
         主模型失败？
              ├─ 是 → fallbacks 链式尝试
              └─ 否 → 返回响应
```
