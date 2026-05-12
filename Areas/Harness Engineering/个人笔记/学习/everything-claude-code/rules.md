
### 安装规则（必需）

> WARNING: **重要提示：** Claude Code 插件无法自动分发 `rules`，需要手动安装：

```shell
# 首先克隆仓库
git clone https://github.com/affaan-m/everything-claude-code.git

# 复制规则目录（通用 + 语言特定）
mkdir -p ~/.claude/rules
cp -r everything-claude-code/rules/common ~/.claude/rules/
cp -r everything-claude-code/rules/typescript ~/.claude/rules/   # 选择你的技术栈
cp -r everything-claude-code/rules/python ~/.claude/rules/
cp -r everything-claude-code/rules/golang ~/.claude/rules/
cp -r everything-claude-code/rules/perl ~/.claude/rules/
```

复制规则时，请复制整个目录（例如 `rules/common`、`rules/golang`），而不是复制目录内的文件；这样可以保留相对引用，并避免不同规则集中的同名文件互相覆盖。



### Rules 结构总览

```
  rules/
  ├── common/          ← 所有语言共享的根基规则
  ├── typescript/      ← 继承 common + TS 专用
  └── python/          ← 继承 common + Python 专用
```

  每份语言规则都由 4 个模块组成：coding-style / patterns / testing / security，外加一个 hooks.md  规定编辑器钩子。

  ---
