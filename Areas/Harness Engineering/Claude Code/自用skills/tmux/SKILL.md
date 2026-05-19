---
name: tmux-services
description: 使用 tmux 窗口管理多服务日志
---
---
name: tmux-services
description: 使用 tmux 窗口管理多服务日志
---

## 分屏原则

- **主服务（日志多）放左侧** - 占 60% 宽度
- **次服务放右侧** - 上下分屏，各占 50% 高度

## 参考布局（2 服务）

```bash
# 创建新窗口
tmux new-window -t 0 -n "services"

# 左右分屏 (左 60% 右 40%)
tmux split-window -h -p 60

# 启动服务 (根据实际项目调整命令)
tmux send-keys -t 0:0.0 '<后端命令>' Enter   # 左侧大窗口
tmux send-keys -t 0:0.1 '<前端命令>' Enter   # 右侧
```

## 参考布局（3 服务）

```bash
# 左右分屏
tmux new-window -t 0 -n "services"
tmux split-window -h -p 60
tmux select-pane -t right
tmux split-window -v  # 右侧上下平分

# 启动服务
tmux send-keys -t 0:0.0 '<后端命令>' Enter   # 左侧大窗口
tmux send-keys -t 0:0.1 '<前端命令>' Enter   # 右上
tmux send-keys -t 0:0.2 '<Agent 命令>' Enter # 右下
```

## 启动方式选择

### 方式 1：后台会话模式（推荐 - 无 TUI）

```bash
# 创建后台会话（-d 参数），无 TUI 干扰，纯文本日志
tmux new-session -d -s "<project>-services"
tmux new-window -t <project>-services -n "services"
tmux split-window -h -l 96 -t <project>-services:services
tmux select-pane -t right -t <project>-services:services
tmux split-window -v -l 27 -t <project>-services:services

# 启动服务
tmux send-keys -t <project>-services:services.0 '<后端命令>' Enter
tmux send-keys -t <project>-services:services.1 '<前端命令>' Enter
tmux send-keys -t <project>-services:services.2 '<Agent 命令>' Enter
```

**优点**：
- 没有 TUI 界面，纯文本日志更清晰
- 可以直接用 `capture-pane` 查看日志
- Nx 检测到非交互终端，自动不使用 TUI

### 方式 2：当前会话创建窗口（有 TUI）

```bash
S=$(tmux display-message -p "#S")
tmux new-window -t $S -n "<project>-services"
tmux split-window -h -l 96
tmux select-pane -t right
tmux split-window -v -l 27
```

**注意**：此方式在当前交互会话中创建窗口，Nx 可能显示 TUI 界面。

## 安全边界（重要）

```bash
# 禁止删除当前对话窗口
# 检查：如果窗口名是 claude* 或当前 active 窗口，绝对不能 kill
tmux list-windows -t $S  # 先列出所有窗口确认

# 只允许操作 *-services 命名的窗口
# 示例：kill-window 前必须确认窗口名
tmux list-windows | grep "services"  # 确认是 services 窗口
tmux kill-window -t $S:services      # 安全
tmux kill-window -t $S:0             # 危险！可能删除对话窗口
```

**规则**：
1. 只能操作名称匹配 `*-services` 的窗口
2. 禁止删除 active 窗口或名称为 `claude*` 的窗口
3. `kill-window` 前必须先用 `list-windows` 确认窗口名

## 常用操作

```bash
# 查看 pane 日志
tmux capture-pane -t <session>:<window>.<pane> -p -S 100

# 切换 pane
tmux select-pane -t <session>:<window>.<pane>

# 清理窗口
tmux kill-window -t <session>:<window>
```
