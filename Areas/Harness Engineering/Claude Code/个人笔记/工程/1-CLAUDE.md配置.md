

rules
在rules中加上对这些skill的联动，应该比手动调用或者ai自动调用更方便，命中率、更高

.claude/CLAUDE.md
```
# 启动服务规则

## 启动任何服务前

1. **先阅读 @../../README.md** 获取官方启动流程和环境配置
    
2. **使用 tmux 管理多服务日志** - 具体参考 `/tmux-services` skill
    
3. **环境变量配置** - 参考 `@../../.envs/README.md` 快速完成配置
   
禁止后台运行
   
   
   
1.本项目使用的react ts nest shadcn tailwindcss nx langgraph python
编程语言：ts py。必须遵守@xxrules
前端框架：React shadcd tailwindcss。参照@xxxskills
后端框架：nestjs postgres prisma redis minio。参照
智能体：langgraph
GIS：postgis maplibre GDAL

2.本项目的结构设计@xx.md

3.架构设计与决策文档参考

4.分流机制
	openspec
	superpower
	
```


用户目录下的CLAUDE.md放置思想钢印，关闭讨好型人格。

项目目录下的CLAUDE.md放置文档索引，还需要维护
docs/architecture.md
docs/anti-patterns.md


还有git规范
**三、分支命名规范**

```
main                        ← 受保护，禁止直接 push
├── feature/<编号>-<描述>    ← 功能开发
├── fix/<编号>-<描述>        ← Bug 修复
└── release/<版本>          ← 发布准备（按需）
```

**规则：**

- **禁止** 直接 push 到 `main` 分支
- 通过 **Pull Request** 提交所有变更
- PR 合并前 **至少 1 人 Approve**
- 分支合并后 **24 小时内删除**

**四、Commit message 格式**

参考 [Conventional Commits](https://alidocs.dingtalk.com/preview?spaceId=28659819444&dentryId=223896223926&uid=1084232599&bizType=markdown&operate=preview&previewAtta=-1&cdnDownload=1&scene=driveSpace&ext=md&fileName=k8s_gitlab_notice.md&orgId=236067083&parentFrame=uni-preview&disableAssistant=true#) 规范（业界通用标准）：

```
<type>(<scope>): <简短描述>

<详细描述>
```

**type 取值：**

|type|何时用|示例|
|---|---|---|
|`feat`|新功能|`feat(auth): add OAuth2 login`|
|`fix`|Bug 修复|`fix(api): prevent SQL injection`|
|`docs`|文档|`docs(readme): update guide`|
|`style`|格式调整|`style(ui): format code`|
|`refactor`|重构|`refactor(db): extract builder`|
|`perf`|性能优化|`perf(api): add cache`|
|`test`|测试|`test(auth): add login tests`|
|`chore`|构建/依赖|`chore(deps): upgrade axios`|
|`security`|安全修复|`security(jwt): upgrade jjwt`|

**五、代码审查清单（Review 时逐项检查）**

- [ ]  逻辑正确性
- [ ]  无安全漏洞（SQL 注入、XSS、CSRF）
- [ ]  无硬编码密码
- [ ]  依赖版本无已知 CVE 漏洞（结合实际项目），如必须引入需要说明原因（如：这是最新的开源版本）
- [ ]  Commit message 符合格式规范
- [ ]  无调试代码、console.log、注释掉的无用代码
- [ ]  无 `.pem` / `.key` 等敏感文件，可以保留`.env`

**六、安全红线（零容忍）**

以下行为**直接拒绝合并**：

1. ❌ 硬编码密码、API Key、Token
2. ❌ 提交 `.pem` / `.key` 文件
3. ❌ 使用有已知 CVE 漏洞的依赖版本
4. ❌ 关闭安全配置（禁用 SSL、注释认证、关闭 CSRF）
5. ❌ 在 commit message 中写敏感信息
6. ❌ 提交 `node_modules` / `vendor` / `target` 等构建产物
7. ❌ Force push 到 `main` 分支