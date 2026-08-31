# WSL2 从零配置指南（安装 · 迁移D盘 · 显卡 · 网络代理）

> 目标：换一台新电脑，按本文从零配好 WSL2 + GPU + 网络。
> 实战环境：Win10 19045（22H2）+ Ubuntu 24.04 + RTX 5070，2026-08 验证通过。
> 旧笔记《WSL2 安装 Chrome + 代理配置》中 `127.0.0.1` 的代理写法仅适用 Win11 镜像网络模式，Win10 NAT 模式不通，以本文为准。

---

## 1. 前置条件

- Windows 10 21H2（19044+）或 Win11，64 位
- BIOS 开启虚拟化（Intel VT-x / AMD-V），大多数机器默认开启；装完报虚拟化错误再回来查
- 磁盘预留：Ubuntu 系统盘初始约 2GB，装 CUDA/PyTorch 后会涨到 20GB+，建议装非系统盘

## 2. 安装 WSL2 + Ubuntu

```powershell
# 管理员 PowerShell
wsl --update                                  # 先更新 WSL 本体，新版才支持 --location
wsl --install Ubuntu --location D:\WSL\Ubuntu # 直装到 D 盘
```

**常见报错：`无法从 raw.githubusercontent.com 提取通讯组列表 / WININET_E_TIMEOUT`**
新版 WSL 装发行版前要从 GitHub 拉列表，国内直连不通。两个绕法：

- 法一：代理软件开「系统代理」或 TUN 模式后重试（wsl.exe 认系统代理）
- 法二：Microsoft Store 搜 "Ubuntu 24.04 LTS" 直接安装（国内可直连），装完再迁移：
  ```powershell
  wsl --manage Ubuntu-24.04 --move D:\WSL\Ubuntu   # 发行版名以 wsl -l -v 为准
  ```

**首次启动初始化**（只出现一次）：
1. Provisioning 展开系统文件，等待即可
2. 创建 Unix 用户名 + 密码（**密码用于 WSL 内 sudo**，与 Windows 登录密码无关）
3. Canonical 遥测询问，Y/n 均可，无影响

**安装后检查**：

```powershell
wsl -l -v        # VERSION 列必须是 2；是 1 则 wsl --set-default-version 2
```

- 已有 `docker-desktop` 发行版属正常（Docker Desktop 自带），与 Ubuntu 互不干扰
- 默认发行版标记 `*` 只影响裸敲 `wsl` 进哪个系统，Docker 完全不受影响；想改：`wsl --set-default Ubuntu`
- 日常进 Ubuntu 用 Windows Terminal 的 Ubuntu 标签页，或 `wsl -d Ubuntu`

**已装到 C 盘的老 WSL 迁移**（`--manage --move` 不可用时的通用大法）：

```powershell
wsl --shutdown
wsl --export Ubuntu D:\wsl-backup\ubuntu.tar
wsl --unregister Ubuntu
wsl --import Ubuntu D:\WSL\Ubuntu D:\wsl-backup\ubuntu.tar
```
导入后默认用户变 root，在 WSL 里编辑 `/etc/wsl.conf` 加：
```ini
[user]
default=你的用户名
```
然后 `wsl --terminate Ubuntu` 重开。

## 3. 显卡直通（CUDA）

- **驱动只装 Windows 侧**（GeForce Game Ready / Studio，新版自带 WSL 支持）；**WSL 里千万不要装 Linux 驱动**
- 新架构显卡（RTX 50 系 Blackwell）需要较新驱动（570+）

验证——WSL 里跑：

```bash
nvidia-smi
```
能看到显卡型号、显存、驱动版本即成功。输出里的 Xwayland 进程是 WSLg（Linux GUI 支持）占的显存，正常。

**深度学习环境注意**：
- PyTorch 装自带 CUDA runtime 的 wheel（如 cu128）即可，**不需要**单独装 CUDA Toolkit；只有编译自定义算子（需要 nvcc）才要装
- **新架构卡 + 旧版 PyTorch = 白屏不报错**：50 系（sm_120）必须 PyTorch 2.7+ 的 cu128 及以上版本；仓库 README 钉死 torch==2.5.1 之类的，用 `pip install -e . --no-deps` 绕过再手动补依赖

## 4. 网络与代理（Win10 NAT 模式核心难点）

**原理**：WSL2 是独立虚拟机，有自己的网段。Windows 上跑的代理，WSL 里既不能用 `127.0.0.1` 访问（NAT 模式），系统代理设置也对它无效。必须指向"WSL 眼中的 Windows 主机"——即网关 IP。

**第 1 步：Windows 侧两个前提**

1. 代理软件打开「**允许局域网连接（Allow LAN）**」，并记住 HTTP/混合端口（Clash 系常见 7890/7897，v2rayN 常见 10808/10809）
2. 管理员 PowerShell 放行防火墙（**最常见的拦路虎**，症状是 WSL 里 curl 代理端口超时）：
   ```powershell
   New-NetFirewallRule -DisplayName "WSL Proxy <端口>" -Direction Inbound -Protocol TCP -LocalPort <端口> -Action Allow
   ```

**第 2 步：WSL 里设置代理**

```bash
export hostip=$(ip route | awk '/default/ {print $3}')   # 网关即 Windows 主机 IP
export http_proxy=http://$hostip:<端口>
export https_proxy=http://$hostip:<端口>
curl -sI https://github.com | head -1                     # 期望 HTTP/2 200
```

**第 3 步：写成开关**（`nano ~/.bashrc` 粘到底部；网关 IP 重启会变，所以动态取）：

```bash
proxy_on() {
    export hostip=$(ip route | awk '/default/ {print $3}')
    export http_proxy=http://$hostip:<端口>
    export https_proxy=http://$hostip:<端口>
    echo "proxy on -> $http_proxy"
}
proxy_off() {
    unset http_proxy https_proxy hostip
    echo "proxy off"
}
```
`source ~/.bashrc` 后即可 `proxy_on` / `proxy_off`。

**排障速查**：

| 症状 | 原因 |
|---|---|
| `Connection refused`（秒失败） | Allow LAN 没开，代理只监听 127.0.0.1 |
| 卡住超时（等满 max-time） | Windows 防火墙拦截 → 加放行规则 |
| Windows 本机 curl 代理就失败 | 端口号不对，去客户端查 HTTP/混合端口 |
| 什么都没配也能科学上网 | 代理软件开了 TUN 模式，透明接管了 WSL 流量 |

诊断命令：`curl -v --max-time 5 http://<主机IP>:<端口> 2>&1 | head -5`

## 5. 国内网络经验法则（踩坑总结）

- **教育网镜像（清华 TUNA / 中科大 USTC）会对部分家宽 IP（尤其移动）返回 403**，直连和走海外代理出口都会被拒。症状：目录页能开、文件下载 403
- 应对：
  - 大文件换**阿里云镜像**：pip 用 `-i https://mirrors.aliyun.com/pypi/simple/`，conda 用中科大/阿里云源或直接走代理用官方源
  - 或**开代理走官方源**（repo.anaconda.com、pypi.org 境外源 + 代理是正确组合）
- **核心规律：国内源必须直连（proxy_off），境外源开代理（proxy_on）**。走代理访问国内源 = 海外出口被拒 = 403
- wget 403 时可换浏览器 UA 试：`curl -A "Mozilla/5.0" -LO <url>`
- PowerShell 命令差异：`curl` 要写 `curl.exe`（否则是别名）；没有 `head`，用 `Select-Object -First 1`
- GitHub 主站国内多数网络可直连（时好时坏），`raw.githubusercontent.com` 常年不通

## 6. 文件系统与日常使用

- WSL 访问 Windows：`/mnt/c`、`/mnt/d`（如 `C:\Users\PC\Downloads` → `/mnt/c/Users/PC/Downloads`）
- Windows 访问 WSL：资源管理器地址栏 `\\wsl$\Ubuntu\home\<用户名>\`，或侧栏「Linux」
- **项目/环境放 Linux 原生文件系统（`~/`）**，别放 `/mnt/` 下——跨系统 I/O 慢数倍且权限易出怪问题
- WSLg 可弹 GUI 窗口，但 **OpenGL 程序（open3d 等）在 Wayland 下经常起不来**（GLEW 初始化失败），可视化的活交给 Windows 原生软件（MeshLab / CloudCompare）最省心
- 提示符解读：`pc@DESKTOP-XXX:/mnt/c/Windows/system32$` = 用户@主机:当前目录；从哪个目录启动 WSL 就继承哪个初始位置，`cd ~` 回家

## 7. 常用命令速查

```powershell
# Windows PowerShell
wsl -l -v                     # 列出发行版和版本
wsl -d Ubuntu                 # 进入指定发行版
wsl --shutdown                # 停掉所有 WSL 实例（改配置后用）
wsl --set-default Ubuntu      # 改默认发行版
wsl --manage Ubuntu --move D:\WSL\Ubuntu   # 迁移到其他盘
```

```bash
# WSL 内
ip route | grep default       # 查 Windows 主机（网关）IP
nvidia-smi                    # 验证显卡直通
proxy_on / proxy_off          # 代理开关（自己配的 bashrc 函数）
explorer.exe .                # 用 Windows 资源管理器打开当前目录
```

---

## 本机配置记录（2026-08-31）

| 项目 | 值 |
|---|---|
| 系统 | Win10 19045 + WSL 2.7.12 + Ubuntu 24.04 |
| WSL 位置 | `D:\WSL\Ubuntu`（ext4.vhdx） |
| 显卡 | RTX 5070 12GB，WSL 内 nvidia-smi 驱动 610.53 |
| 代理端口 | 10090（HTTP），已加防火墙放行规则 "WSL Proxy 10090" |
| 网络 | GitHub 直连可用；HuggingFace 需代理；清华/中科大镜像 403（移动 IP 被拒），pip 用阿里云源 |
| conda | `~/miniconda3`，环境 `abot`（Python 3.11） |
