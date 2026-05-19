配置地址
~/.claude/hook.json

插件中的hook
hooks/hook.json


---

## matcher 匹配规则

|matcher 值|匹配范围|说明|
|---|---|---|
|`"Bash"`|Bash 工具|精准匹配单个工具|
|`"Write"`|Write 工具|精准匹配单个工具|
|`"Edit\|Write"`|Edit 或 Write|用 `\|` 分隔多个工具|
|`"Bash\|Write\|Edit\|MultiEdit"`|四个工具|多工具组合|
|`"*"`|所有工具|广播模式，接收所有工具调用事件|

---

## 两层过滤机制

Hook 系统使用两层过滤：

### 第一层：matcher 匹配工具名称

  
{  
  "matcher": "Bash",  
  "hooks": [{ "type": "command", "command": "check-script.sh" }]  
}

**作用**：只在调用 Bash 工具时触发 hook

### 第二层：hook 脚本内部检查工具参数

Hook 脚本通过 stdin 接收 JSON 数据：

  
{  
  "tool": "Bash",  
  "input": {  
    "command": "git push origin main"  
  },  
  "cwd": "/home/user/project",  
  "session_id": "abc123"  
}

脚本可以：

- 检查 `tool` 字段判断工具类型
    
- 检查 `input.command` 判断具体命令内容
    
- 返回 exit code 0（允许继续）或 非0（阻止执行）
    

---

## 示例分析

### 精准狙击型

  
{  
  "matcher": "Bash",  
  "hooks": [{ "command": "npx block-no-verify@1.1.2" }],  
  "description": "阻止 --no-verify 标志"  
}

**触发流程：**

  
Claude 准备执行 Bash 工具  
    command: "git commit --no-verify -m 'xxx'"  
    ↓  
matcher: "Bash" 匹配 → hook 触发  
    ↓  
block-no-verify 检查命令内容  
    发现 --no-verify 标志  
    ↓  
exit code 非0 → 阻止执行  
    ↓  
Claude 收到 hook 报错，不执行命令

### 广播型

  
{  
  "matcher": "*",  
  "hooks": [{ "command": "...mcp-health-check.js" }],  
  "description": "MCP 健康检查"  
}

**触发流程：**

  
任何工具调用（Bash/Read/Write/...）  
    ↓  
matcher: "*" 匹配 → hook 触发  
    ↓  
mcp-health-check.js 读取 stdin  
    检查 tool 字段是否是 MCP 相关工具  
    ↓  
如果是 MCP 工具且失败 → 执行健康检查逻辑

**注意**：matcher `"*"` 让脚本接收所有事件，但脚本内部判断是否需要处理。

---

## Claude Code 内置工具列表

|工具名称|作用|matcher 可用|
|---|---|---|
|`Bash`|执行 shell 命令|✅|
|`Read`|读取文件|✅|
|`Write`|写入文件|✅|
|`Edit`|编辑文件|✅|
|`MultiEdit`|多处编辑|✅|
|`Glob`|文件模式匹配|✅|
|`Grep`|内容搜索|✅|
|`Agent`|启动子 agent|✅|
|`Skill`|执行 skill|✅|
|`TaskCreate`|创建任务|✅|
|`WebFetch`|获取网页|✅|
|`WebSearch`|搜索网络|✅|
|`AskUserQuestion`|询问用户|✅|

---

## Hook 类型与时机

|Hook 类型|触发时机|作用|
|---|---|---|
|`PreToolUse`|Claude **准备调用工具**|门卫检查，决定是否执行|
|`PostToolUse`|Claude **执行完工具**|质检员检查，后续处理|
|`PostToolUseFailure`|工具**执行失败**|错误处理、重试逻辑|
|`SessionStart`|会话**开始时**|加载上下文、初始化|
|`PreCompact`|上下文**压缩前**|保存状态|
|`Stop`|会话**结束时**|最终验证、清理|

---

## 配置位置

Hook 配置文件位置：

- **插件级**：`~/.claude/plugins/cache/{plugin}/hooks/hooks.json`
    
- **用户级**：`~/.claude/settings.json`
    
- **项目级**：项目目录 `.claude/settings.json`
    

优先级：项目级 > 用户级 > 插件级（后加载覆盖）

---

## 总结

matcher: "Bash"           → 精准狙击 Bash 工具  
matcher: "Edit|Write"     → 精准狙击 Edit 和 Write  
matcher: "*"              → 广播给所有工具  
​  
两层过滤：  
1. matcher → 过滤工具名称  
2. 脚本逻辑 → 过滤工具参数内容