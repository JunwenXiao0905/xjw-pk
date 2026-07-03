# Agent 代码执行隔离 — 行业调研

> 调研对象：工业级代码 agent（Claude Code / Codex / Cursor / Devin / Aider）如何隔离与执行 LLM 生成的代码，以及"agent 运行代码"的隔离技术谱系。
> 背景：自研 GIS 代码 agent（GeoLens CoderAgent）当前用 Python subprocess + 路径/命令白名单 + 超时，评估够不够、如何升级。
> 方法：deep-research（108 子代理、26 源、25 条声明对抗式验证，22 确认 / 3 驳回）。日期：2026-07-03。

## TL;DR
- 隔离是**多层谱系，没有银弹**：应用层白名单 < OS 级 syscall 过滤（seccomp/Seatbelt/bubblewrap/nsjail）< 容器（Docker）< 用户态内核（gVisor）< 完全虚拟化（VM/Kata/Firecracker microVM）。
- **纯应用层命令白名单不足以隔离 agent 代码**：控制权一旦交给子进程，应用失去可见性，间接调用即可绕过——Cursor **CVE-2026-22708** 已实证"空白名单也能被打穿"（shell 内建 + `PAGER/PYTHONWARNINGS/PERL5OPT` 环境变量投毒 → RCE）。
- **网络出口是第一攻击面**，比 syscall 过滤更关键；隔离工具默认不做网络隔离。
- **共享内核沙箱（含 Docker）不是可靠安全边界**：内核 LPE 可逃逸（Claude Code bubblewrap **CVE-2026-25725** 实证）。跑不可信/多租户代码才必须上完全虚拟化。
- **CoderAgent 现状定位**：subprocess + 路径/命令白名单 + 超时 = 谱系最弱端（纯应用层）。对本地、非敌对、自己用的 GIS 任务"够用但不达标"。

## 1. 隔离谱系（弱→强）

| 层 | 代表 | 机制 | 隔离边界 | 逃逸面 |
|---|---|---|---|---|
| 应用层白名单 | CoderAgent 现状、旧版 Cursor | 命令名/路径匹配 | 子进程派生后失控 | 间接调用、env 投毒、shell 内建（CVE-2026-22708） |
| OS 级 syscall | seccomp、macOS Seatbelt、bubblewrap、nsjail | 内核强制过滤系统调用 + 挂载/命名空间 | 文件系统、网络、能力 | 内核 LPE（CVE-2026-25725） |
| 容器 | Docker/runc + AppArmor + seccomp | 命名空间 + cgroups | 进程/文件系统/资源 | **共享内核** → 内核 CVE 逃逸（AWS 明确"容器非安全边界"） |
| 用户态内核 | gVisor | Go 实现的 user-space kernel 中介 syscall | 弱于 VM、强于共享内核 | 攻击面更小但非零；有性能开销 |
| 完全虚拟化 | VM / Kata / **Firecracker microVM** | 硬件虚拟化，独立内核 | 最强 | 虚拟化层（极小，Firecracker VMM 仅 ~40 syscall + seccomp + jailer） |

Ptacek 给新设计的菜单只有四个：nsjail、非特权 Docker + 更严 seccomp、gVisor、Firecracker/Kata；**非敌对代码首选 nsjail**（ROI 最高）。

## 2. 主流代码 agent 实际用哪一层

- **Claude Code**：OS 级 Bash 子进程强制（macOS Seatbelt / Linux+WSL2 bubblewrap + 可选 seccomp）。**单进程**架构：agent 运行时与多数工具同进程；只有 Bash 及其子进程进沙箱，Read/Write/Edit/Glob/Grep 走应用层 permission。默认只写工作目录 + 会话临时目录；网络默认不放行任何域名，由沙箱外代理按主机白名单。**官方明说"不是完整隔离边界"**（代理不终止 TLS、可 domain fronting）。
- **OpenAI Codex CLI**：macOS sandbox-exec(seatbelt) / Linux Docker + iptables 把 egress 限到 OpenAI API 端点。
- **Cursor**：应用层命令白名单——被 CVE-2026-22708 打穿，**反面教材**。
- **Devin**：控制平面/数据平面分离（Brain 在 Cognition Cloud + Devbox 每会话独立隔离机器），Enterprise Cloud 每会话独立机器、单租户隔离。
- **NVIDIA OpenShell**：内核级——特权 Docker 内跑 K3s，每沙箱一个 pod + 声明式 egress YAML（文件限制 + 能力降权 + 网关进程隔离 + 二进制作用域规则）。
- **Aider**：**无沙箱**，直接写你工作目录，靠 git undo 兜底（定位是本地 pair programmer，不托管执行）。
- **云沙箱平台**：E2B = Firecracker microVM（snapshot-restore 创建 5–30ms）；Modal = gVisor 容器；Daytona / Morph 同类。

## 3. 威胁模型 / 已知逃逸

- **CVE-2026-22708（Cursor）**：空白名单也能绕过——`export/typeset/declare` 等 shell 内建 + env 投毒 → 把 allowlisted 命令变成 RCE，官方承认 systemic issue。
- **CVE-2026-25725（Claude Code Linux bubblewrap，CVSS v4.0 7.7）**：只读挂载条件取决于启动时文件是否存在 → 沙箱内代码可创建 `.claude/settings.json` 注入 SessionStart hook → 下次主机启动以**用户全权限**执行任意命令（v2.1.2 已修）。
- **配置型沙箱逃逸（CBSE，Cymulate 提出）**：沙箱被当安全边界，但"真正的边界"——主机侧配置/执行逻辑——在沙箱内可写。Gemini CLI 把 `~/.gemini`（含 `oauth_creds.json`，带 GCP cloud-platform 全 scope）读写挂载进沙箱 → 窃 OAuth 令牌账户接管；Codex CLI 的 `apply_patch` 能在沙箱内写 `.codex/config.toml` → 经沙箱外执行的 `notify` 持久化主机 RCE。
- **数据外泄**：Lasso 实测即便有容器 + K8s + egress 策略，仍能通过默认放行的授权工具（`npm install` postinstall、`node/git/gh`）把含凭证的文件以 PR 形式泄出（emoji 编码绕过密钥扫描）。
- **prompt 注入**：自适应间接 prompt 注入对 8 种已有防御 ASR >50%；GPTFuzz/GAP >90%；移动 OS agent 环境注入 93% → 应用层防御远不够。

## 4. 关键共识 — NVIDIA Red Team 三项强制
1. **限制网络出口到已知可信位置**（第一攻击面）
2. **OS 层禁止工作区之外的文件写入**
3. **无论位于何处都禁止写任何 agent 配置文件**（`.cursorrules` / `CLAUDE.md` / hooks / MCP 配置——常在沙箱外执行，投毒可持久化）

> 核心原则：**OS 层强制的价值在于它不依赖模型选了什么命令**——即使允许的命令做了超出其名所暗示的操作，边界仍成立。应用层做不到。

## 5. CoderAgent 定位与升级路径

**现状差距**：子进程派生后失去可见性（间接调用绕过白名单）、无 syscall 过滤（不防内核逃逸）、**网络完全敞开**、无 agent 配置文件写保护、无凭据文件保护（`.env`/`~/.ssh` 等仍可读）。

**分阶段（ROI 排序）**：
- **P0｜追平 Claude Code 量级**：bubblewrap/nsjail 包裹（只读根 + 可写仅工作目录/output + 降权 + 命名空间隔离）+ seccomp + **网络出口白名单代理**（默认 deny）+ 配置文件写保护 + 凭据 denyRead。
  - 其中"**网络白名单 + 凭据保护 + 配置只读**"在应用层也能先做一部分（subprocess 前清空含密 env、强制走 allowlist 代理、`.env`/settings 设只读）——不依赖 OS 沙箱，可立即动手。
- **P1｜跑相对不可信代码**：上 **gVisor 容器**（优于裸 Docker，规避共享内核 LPE）。Linux 下 `docker run --runtime=runsc` 即可。
- **P2｜多租户/完全不可信代码**：**Firecracker/Kata microVM**（E2B 路线，snapshot-restore 5–30ms 创建）。

**Windows 落地注意**：bubblewrap/nsjail 是 Linux 原生；macOS 用 Seatbelt；**Windows 原生等价物（AppContainer?）未被本批来源覆盖**。Claude Code 在 Windows 上靠 WSL2。现实路径：① CoderAgent 跑在 WSL2 / Linux 容器里用 bubblewrap/nsjail；② Docker Desktop（gVisor 支持有限）；③ 研究 Windows AppContainer。

## 局限（报告自述 caveats）
- 性能/成本量化数字（启动延迟、单次成本）部分声明被对抗验证驳回，仅定性排序可靠。
- Ptacek"四菜单 + nsjail 首选"是 2020 年专家个人意见（未被反驳、fly.io 产品印证仍 operative），非 2026 行业硬共识。
- Gemini/Codex 跨厂商漏洞未获 Google/OpenAI 官方确认（Cymulate 单方 + 部分独立审计）；Claude Code 侧 Anthropic 全面确认（CVE + GHSA + 修复）。
- 未覆盖：E2B/Daytona/Morph 工程细节、WASM（Wasmtime/Wasmer）对 GIS 重 native 扩展（GDAL/rasterio）的兼容性、GIS 工具（gdalwarp/QGIS）与 seccomp 只读挂载的兼容性。

## 主要来源
- NVIDIA AI Red Team — Practical Security Guidance for Sandboxing Agentic Workflows：https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/
- Claude Code 官方 Sandboxing 文档：https://code.claude.com/docs/en/sandboxing
- Ptacek (fly.io) — Sandboxing and Workload Isolation：https://fly.io/blog/sandboxing-and-workload-isolation/
- Cymulate — The Race to Ship AI Tools Left Security Behind (CBSE)：https://cymulate.com/blog/the-race-to-ship-ai-tools-left-security-behind-part-1-sandbox-escape/
- Lasso Security — Sandboxed AI Agents Attack Surface：https://www.lasso.security/blog/sandboxed-ai-agents-attack-surface
- Devin 部署架构：https://docs.devin.ai/enterprise/deployment/overview
- ScienceDirect — LLM agent 攻击防御综述：https://www.sciencedirect.com/science/article/pii/S2405959525001997
- 19 个云沙箱平台横评：https://rywalker.com/research/ai-agent-sandboxes
- r/LocalLLaMA — subprocess 够不够社区讨论：https://www.reddit.com/r/LocalLLaMA/comments/1l8h9wa/
