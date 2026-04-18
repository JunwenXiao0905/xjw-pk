

安装后的目录解析

  1. 插件安装位置
```
  ~/.claude/plugins/
  ├── cache/                                    ← 正式安装的插件
  │   └── <marketplace>/
  │       └── <plugin-name>/
  │           └── <version>/
  │               └── [插件内容]
  │
  ├── marketplaces/                             ← Marketplace 元数据（git repo）
  │   ├── claude-plugins-official/
  │   ├── openai-codex/
  │   └── ...
  │
  └── installed_plugins.json                    ← 安装记录


```
 2. 插件内部结构
```

  cache/<marketplace>/<plugin>/<version>/
  ├── .claude-plugin/
  │   └── plugin.json           # 必须——插件元数据（name, version, description）
  │
  ├── agents/                   # 可选——子代理定义
  │   └── *.md
  │
  ├── commands/                 # 可选——快捷命令
  │   └── *.md
  │
  ├── skills/                   # 可选——技能定义
  │   └── <skill-name>/
  │       └── SKILL.md
  │
  ├── hooks/                    # 可选——自动加载
  │   └── hooks.json
  │
  ├── scripts/                  # 可选——执行脚本
  │   └── *.js / *.sh
  │
  ├── prompts/                  # 可选——提示模板
  │
  ├── schemas/                  # 可选——JSON Schema
  │
  ├── LICENSE
  ├── CHANGELOG.md
  └── NOTICE
```

  4. Claude Code 启动时：
     ├── 读取 installed_plugins.json
     ├── 加载每个插件的 .claude-plugin/plugin.json
     ├── 自动加载 hooks/hooks.json（如果存在）
     ├── 自动加载 agents/、commands/、skills/
     └── 这些组件立即可用


plugin可以安装到项目范围，但是不能安装到项目目录，所以为了团队协作，应当在项目目录中增加一个文档

```
  your-project/.claude/
  ├── PLUGINS.md             # 插件安装说明
  ├── hooks/
  ├── skills/
  ├── commands/
  └── settings.local.json
```

```
  PLUGINS.md：
  # Required Plugins

  bash
  claude plugin install codex@openai-codex
  claude plugin install github@claude-plugins-official

  ┌────────────────────────────────┬──────────────────────────┐
  │             Plugin             │         Purpose          │
  ├────────────────────────────────┼──────────────────────────┤
  │ codex@openai-codex             │ Code review & delegation │
  ├────────────────────────────────┼──────────────────────────┤
  │ github@claude-plugins-official │ GitHub integration       │
  └────────────────────────────────┴──────────────────────────┘
```


安装时

```
  Plugin Details

  ecc
  Version: 1.10.0

  The most comprehensive Claude Code plugin — 38 agents, 156 skills, 72 legacy command shims,
  selective install profiles, and production-ready hooks for TDD, security scanning, code review,
   and continuous learning

  By: Affaan Mustafa

  Will install:
  · Components will be discovered at installation

  ⚠Make sure you trust a plugin before installing, updating, or using it. Anthropic does not
   control what MCP servers, files, or other software are included in plugins and cannot verify
   that they will work as intended or that they won't change. See each plugin's homepage for more
    information.

  > Install for you (user scope)
    Install for all collaborators on this repository (project scope)
    Install for you, in this repo only (local scope)
    Open homepage
    Back to plugin list
```

当选择了 project scope 后， installed_plugins.json 如下：

```
  {
    "scope": "project",
    "installPath": "/home/xjw/.claude/plugins/cache/ecc/ecc/1.10.0",
    "projectPath": "/home/xjw/projects/xjw-monorepo"
  }
```

  插件确实标记为 project scope，并且记录了 projectPath。但文件存储位置在用户目录的 cache 中。

  插件安装机制解释

  1. 文件存储位置：所有插件文件都统一存储在
  ~/.claude/plugins/cache/（用户目录），避免重复下载相同版本的插件
  2. scope 控制可见性：
    - scope: "project" + projectPath → 只在指定项目中可见
    - scope: "user" → 在所有项目中可见
    - scope: "local" → 只在当前目录可见
  3. 好处：
    - 多个项目使用同一版本插件时，共享一份文件
    - 不同项目可以安装不同版本（如 ecc/1.9.0 vs ecc/1.10.0）
    - 卸载时只删除 metadata，文件保留供其他项目使用

  验证方式：如果你在另一个项目中打开 Claude Code，ecc 插件不会加载，因为它绑定了 projectPath:
  "/home/xjw/projects/xjw-monorepo"。




.claude-plugin/PLUGIN_SCHEMA_NOTES.md

```
  ---
  插件清单 Schema 注意事项

  本文档记录了 Claude Code 插件清单验证器未公开但强制执行的约束规则。

  这些规则基于真实的安装失败、验证器行为以及与已知可用插件的对比总结而来。
  它们的存在是为了防止静默故障和反复回归。

  如果你要编辑 .claude-plugin/plugin.json，请先阅读本文档。

  ---
  概要（先读这个）

  Claude 插件清单验证器是严格且固执的。
  它强制执行的规则在公开的 schema 参考文档中并未完全说明。

  最常见的失败模式是：

  ▎ 清单看起来合理，但验证器以模糊的错误如 agents: Invalid input 拒绝它

  本文档解释原因。

  ---
  必填字段

  version（必须）

  version 字段是验证器必需的，即使某些示例中省略了它。

  如果缺失，安装可能在 marketplace 安装或 CLI 验证时失败。

  示例：

  {
    "version": "1.1.0"
  }

  ---
  字段格式规则

  以下字段必须始终是数组：

  - agents
  - commands
  - skills
  - hooks（如果存在）

  即使只有一个条目，字符串也不被接受。

  无效

  {
    "agents": "./agents"
  }

  有效

  {
    "agents": ["./agents/planner.md"]
  }

  这适用于所有组件路径字段。

  ---
  路径解析规则（关键）

  Agents 必须使用显式文件路径

  验证器不接受 agents 的目录路径。

  即使这样也会失败：

  {
    "agents": ["./agents/"]
  }

  必须显式列出 agent 文件：

  {
    "agents": [
      "./agents/planner.md",
      "./agents/architect.md",
      "./agents/code-reviewer.md"
    ]
  }

  这是最常见的验证错误来源。

  Commands 和 Skills

  - commands 和 skills 接受目录路径仅在包裹在数组中时
  - 显式文件路径是最安全、最面向未来的方式

  ---
  验证器行为说明

  - claude plugin validate 比某些 marketplace 预览更严格
  - 本地验证可能通过，但安装时因路径歧义失败
  - 错误通常是通用的（Invalid input），不指出根本原因
  - 跨平台安装（尤其是 Windows）对路径假设更不宽容

  假设验证器是敌意且字面的。

  ---
  hooks 字段：不要添加

  ▎ 警告：关键：不要在 plugin.json 中添加 "hooks" 字段。这由回归测试强制执行。

  为什么这很重要

  Claude Code v2.1+ 自动加载任何已安装插件的 hooks/hooks.json（按约定）。如果你还在 plugin.json
  中声明它，会得到：

  Duplicate hooks file detected: ./hooks/hooks.json resolves to already-loaded file.
  The standard hooks/hooks.json is loaded automatically, so manifest.hooks should
  only reference additional hook files.

  反复添加/删除的历史

  这导致了本仓库中反复的修复/回退循环：

  ┌─────────┬────────────┬───────────────────────────────────┐
  │  提交   │    操作    │             触发原因              │
  ├─────────┼────────────┼───────────────────────────────────┤
  │ 22ad036 │ 添加 hooks │ 用户报告 "hooks 不加载"           │
  ├─────────┼────────────┼───────────────────────────────────┤
  │ a7bc5f2 │ 删除 hooks │ 用户报告 "重复 hooks 错误" (#52)  │
  ├─────────┼────────────┼───────────────────────────────────┤
  │ 779085e │ 添加 hooks │ 用户报告 "agents 不加载" (#88)    │
  ├─────────┼────────────┼───────────────────────────────────┤
  │ e3a1306 │ 删除 hooks │ 用户报告 "重复 hooks 错误" (#103) │
  └─────────┴────────────┴───────────────────────────────────┘

  根本原因：Claude Code CLI 版本间行为变化：
  - Pre-v2.1：需要显式 hooks 声明
  - v2.1+：按约定自动加载，重复声明报错

  当前规则（由测试强制执行）

  tests/hooks/hooks.test.js 中的测试 plugin.json does NOT have explicit hooks declaration
  防止此问题再次引入。

  如果你要添加额外的 hook 文件（非 hooks/hooks.json），那些可以声明。但标准的 hooks/hooks.json
  不能声明。

  ---
  已知反模式

  这些看起来正确但会被拒绝：

  - 字符串值而非数组
  - agents 使用目录数组
  - 缺少 version
  - 依赖推断路径
  - 假设 marketplace 行为与本地验证一致
  - 添加 "hooks": "./hooks/hooks.json" — 按约定自动加载，会导致重复错误

  不要耍聪明。要显式。

  ---
  最小已知正确示例

  {
    "version": "1.1.0",
    "agents": [
      "./agents/planner.md",
      "./agents/code-reviewer.md"
    ],
    "commands": ["./commands/"],
    "skills": ["./skills/"]
  }

  此结构已通过 Claude 插件验证器验证。

  重要：注意没有 "hooks" 字段。hooks/hooks.json 文件按约定自动加载。显式添加会导致重复错误。

  ---
  给贡献者的建议

  提交涉及 plugin.json 的更改前：

  1. Agents 使用显式文件路径
  2. 确保所有组件字段是数组
  3. 包含 version
  4. 运行：

  claude plugin validate .claude-plugin/plugin.json

  如有疑问，选择冗长而非便利。

  ---
  本文档存在的原因

  本仓库被广泛 fork 并用作参考实现。

  在此记录验证器的怪异行为：

  - 防止反复出现问题
  - 减少贡献者的挫败感
  - 随生态系统演进保持插件稳定性

  如果验证器变化，请先更新本文档。

  ---
```