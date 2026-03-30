# 通读84.7k stars的superpowers：国内开发者都怎么用它写代码？

原创 浪漫人生自由行 上升ing

 _2026年3月15日 22:14_ _浙江_ 9人

> 说真的，我用superpowers之后，原来2小时的工作现在10分钟就能搞定。

前阵子朋友问我："你最近怎么开发速度这么快？"

我说："其实没啥秘诀，就是用了个Claude Skill叫superpowers。"

他一听来了兴趣："这玩意儿是啥？哪找的？怎么用？"

我想了想，这不就是很多人都在问的问题——知道Claude有Skill，但不知道哪些真正好用、去哪找靠谱的。

今天这篇，我详细聊聊superpowers这个Skill——GitHub上84.7k stars的神器，国内开发者怎么用它提升效率的。

## 01 superpowers到底是啥？

先说人话，它不是什么高大上的东西。

**简单说**：superpowers是套完整的软件开发工作流，帮你把开发过程标准化、自动化。

**核心思想**就几个：

**TDD（测试驱动开发）**：先写测试，看它挂了，再写代码。

**YAGNI（You Aren't Gonna Need It）**：别写你不需要的代码。

**DRY（Don't Repeat Yourself）**：别重复造轮子，能复用就复用。

**还有一堆工程实践**：代码审查、根因追踪、代码质量保证、Git分支管理...

**说人话**：它不是某个单独功能，而是把高级开发者的经验打包成Skill，让Claude按这些最佳实践帮你干活。

**84.7k stars说明啥**？说明有84,700个人在用，而且维护活跃。这不是个小众工具。

## 02 国内开发者都在用它解决啥问题？

我花了些时间，看了GitHub Issues、Reddit r/ClaudeAI、知乎上的讨论，总结了几个核心场景。

### 场景1：新功能开发——"我不会写代码了，帮我想想"

**真实案例**：全栈开发者 @iiian-crayon 分享

他之前接了个新项目，需求是"用户注册流程"，但不知道怎么设计。加载了superpowers里的brainstorming Skill，Claude反问他：

- 用户注册流程的核心环节是哪些？
    
- 每个环节的边界条件是啥？
    
- 异常情况怎么处理？
    
- 需要验证哪些数据？
    

**Claude帮他设计了完整的流程图**：

```
用户输入 → [选择注册方式] → 验证手机号 → 验证验证码 → [填写表单] → 完成注册            ↓              ↓             ↓            ↓[发送验证码][验证用户身份][创建账户]
```

然后加载了writing-plans Skill，Claude把整个流程拆成了6个2-5分钟的任务，每个任务都有：

- 具体要做什么
    
- 用哪些文件
    
- 验收标准
    
- 可能的坑点
    

**他说**："以前接这种需求，我要查一堆文档、想半天。现在描述一遍，Claude自动给我完整方案，从设计到数据库都有了。代码质量比我自己写的高"

**关键点**：brainstorming不是帮你写需求文档，而是帮你"想清楚要干什么"，避免一上来就写代码。

### 场景2：代码质量保证——"写的代码没人review，怎么搞？"

**真实案例**：团队开发者 @FYZAFH 分享

他们团队之前代码质量问题严重——代码不规范、测试覆盖率低、Code Review没人认真看。

用了superpowers的test-driven-development Skill之后：

**第一步：Claude自动先写测试**

```
// 假设要写个用户服务describe('should return user', () => {constresult = getUser(1);expect(result).toBe({id: 1,name: '张三',email: 'zhangsan@example.com'  });});
```

**第二步：测试不通过就报错，阻止写代码**

superpowers会强制执行TDD——测试不通过，代码直接删除，不允许提交。

**第三步：写最小代码让测试通过**

```
functiongetUser(id: number) {// 只实现最简单的逻辑if (id === 1) {return { id: 1, name: '张三', email: 'zhangsan@example.com' };  }thrownewError('User not found');}
```

**第四步：测试通过后才能继续写下一个功能**

**他说**："以前大家写完代码就提PR，review不认真也过了。现在不行——测试不通过就跑不起来，代码直接被删。而且因为写了最小代码，代码质量反而更高"

**关键点**：TDD不是形式主义，不是为了测试而测试。它的价值是——**确保你写的每个功能都有测试覆盖，而且测试能真实运行**。

### 场景3：重构老代码——"这代码我看不懂，改还是不改？"

**真实案例**：维护者 @FYZAFH 分享

接手了个3年前的老项目，代码复杂，没人敢动。用了superpowers的systematic-debugging Skill，Claude帮他分析：

**第一步：根因追踪**

Claude问了他几个问题：

- 哪个功能经常出bug？
    
- 上次出问题是怎么排查的？
    
- 有没有文档说明这个逻辑？
    

然后生成了4阶段根因分析：

```
问题现象 → [查看日志] → [分析代码路径] → [定位代码块] → [定位具体行]              ↓            ↓           ↓        ↓[添加调试日志][单步调试][阅读注释][搜索相关代码]
```

**第二步：条件断点调试**

Claude说："这是个文件处理函数，建议按条件设置断点"

```
// Claude生成的调试代码functionprocessFile(filePath: string) {console.log('[DEBUG] Starting to process file:', filePath);if (!fs.existsSync(filePath)) {console.error('[DEBUG] File not found');return;  }// 条件断点1if (filePath.endsWith('.tmp')) {console.log('[DEBUG] File is tmp, skipping');return;  }// 条件断点2console.log('[DEBUG] File is valid, proceeding...');// 继续处理逻辑}
```

**第三步：系统化错误处理**

Claude说："为每个错误类型定义统一的处理方式"

```
classErrorHandler {handle(error: Error, context: string) {if (error instanceofFileNotFoundError) {console.log(`[ERROR] File not found in ${context}`);    } elseif (error instanceofValidationError) {console.log(`[ERROR] Validation failed in ${context}`);    } else {console.log(`[ERROR] Unexpected error in ${context}:`, error.message);    }  }}
```

**他说**："我以前排查这种问题，要在各个地方加console.log，跑完了再找。现在Claude帮我加了系统的断点，而且每个关键逻辑点都标记了调试日志，排查效率提升了5倍"

**关键点**：systematic-debugging不是简单"加日志"，而是**系统化地帮你定位问题**——它有4个阶段流程：根因追踪、深度调试、条件等待、完成验证。

### 场景4：Code Review——"PR太多了，review不过来"

**真实案例**：开发团队 @LanternCX 分享

他们项目每周有20+个PR，靠人工review根本来不及。

用了superpowers的requesting-code-review和receiving-code-review Skills：

**自动化Code Review流程**：

```
1. 提PR → Claude自动触发review2. 检查清单（基于规则）：   - 代码风格   - 错误处理   - 性能问题   - 安全隐患   - 测试覆盖率   - 按严重程度分类（Critical/High/Medium/Low）3. 生成review报告（Markdown格式）4. 自动@开发团队确认5. 保存review历史
```

**他说**："Claude帮我们建立了review规则库，包含了团队所有的编码规范。现在每个PR都有自动review，只有Critical问题才需要人工确认。review效率提升了300%"

**关键点**：这个Skill不是帮你写代码，而是**帮你建立代码质量标准，并自动化执行review流程**。

## 03 为什么superpowers火了？84.7k stars不是盖的

从GitHub数据看，superpowers有几个特点让它脱颖而出：

### 原因1：解决真实痛点

**痛点**：开发者的真实问题，不是"我想写个酷炫的功能"。

从上面的案例看，superpowers解决的痛点：

- 新手开发者：不知道怎么开始（brainstorming）
    
- 代码质量：测试没人写、代码不规范（test-driven-development）
    
- 老项目维护：看不懂代码、重构风险大（systematic-debugging）
    
- 团队协作：PR review不过来（requesting-code-review）
    

这些痛点，每个都特别痛。

### 原因2：可组合的Skills体系

superpowers不是单一功能，而是14个可组合的Skills：

- brainstorming（头脑风暴）
    
- using-git-worktrees（Git分支管理）
    
- writing-plans（写作计划）
    
- executing-plans（执行计划）
    
- subagent-driven-development（子代理开发）
    
- test-driven-development（测试驱动开发）
    
- systematic-debugging（系统化调试）
    
- verification-before-completion（完成前验证）
    
- root-cause-tracing（根因追踪）
    
- using-superpowers（使用superpowers）
    
- dispatching-parallel-agents（并行代理调度）
    
- request-code-review（请求代码审查）
    
- receiving-code-review（接收代码审查）
    
- finishing-a-development-branch（完成开发分支）
    
- writing-skills（编写技能）
    

**灵活性**：你可以只加载需要的Skill，不是全部。做测试就加载test-driven-development，做review就加载code-review Skills。

### 原因3：持续的维护和社区反馈

**活跃的Issues**：GitHub上有63个Issues，大部分是用户反馈和功能请求。

**示例Issues**：

- "brainstorming/writing-plans SKILL efficiency" - 讨论这两个Skill的协作效率
    
- "After auto-compact, cc in subagent-driven-development mode has a high probability of forgetting to review" - 用户报告bug
    
- "How can I use Superpowers in Antigravity" - 用户询问在其他IDE中使用
    

**快速响应**：作者@obra会快速响应Issues，而且经常根据社区反馈改进Skill。

**清晰的文档和示例**：每个Skill都有完整的SKILL.md文件：说明用途、触发条件、注意事项。

**丰富的用例**：README里有很多使用示例，不是抽象文档。

**哲学清晰**：强调TDD、YAGNI、DRY，不是随意堆砌功能。

## 04 国内开发者怎么用？真实经验汇总

基于社群讨论，我总结了几个关键点。

### 最常用的Skills（按热度排序）

|Skill|用途|使用频率|适用场景|
|---|---|---|---|
|test-driven-development|测试驱动开发|⭐⭐⭐⭐|所有新功能开发|
|brainstorming|需求分析和设计|⭐⭐⭐⭐|新项目开始、需求不明确|
|systematic-debugging|系统化调试|⭐⭐⭐|旧项目维护、bug排查|
|using-git-worktrees|Git分支管理|⭐⭐⭐|多人协作、并行开发|
|subagent-driven-development|子代理开发|⭐⭐⭐|复杂项目、大型重构|
|root-cause-tracing|根因追踪|⭐⭐|生产问题排查|
|request-code-review|请求代码审查|⭐⭐⭐|团队协作、PR自动化|

**使用率统计**：test-driven-development和brainstorming是最常用的，几乎每个新项目都会用到。

### 不同类型开发者的使用习惯

**初级开发者（0-3年）**

主要用：

- brainstorming：不知道怎么开始，先让Claude帮忙想清楚
    
- test-driven-development：新手容易写bug，用TDD规范自己
    
- using-superpowers：用系统提供的完整工作流，不自己拼
    

**中级开发者（3-8年）**

主要用：

- systematic-debugging：开始接手老项目，需要系统化排查问题
    
- subagent-driven-development：项目复杂了，需要子代理分工
    
- root-cause-tracing：生产问题，需要追溯原因
    
- using-git-worktrees：团队协作多了，需要并行开发
    

**高级开发者（8年+）**

主要用：

- writing-skills：自己写Skill，扩展功能
    
- dispatching-parallel-agents：并行执行多个任务
    
- verification-before-completion：建立完整的项目交付标准
    
- 组合使用：灵活组合多个Skills解决复杂问题
    

### 国内团队 vs 个人开发者

**团队开发者**：

- 优先用：test-driven-development、request-code-review、verification-before-completion
    
- 目标：代码质量、团队协作、项目交付
    
- 价值：标准化流程、自动化review、提升团队效率
    

**个人开发者**：

- 优先用：brainstorming、systematic-debugging、using-git-worktrees
    
- 目标：提升个人开发效率、快速解决问题
    
- 价值：系统化思维、避免踩坑、加速学习
    

## 05 实用技巧：怎么用superpowers更高效？

### 技巧1：按项目阶段用Skill

|项目阶段|推荐Skills|说明|
|---|---|---|
|需求分析|brainstorming|弄清楚要干什么，别一上来就写代码|
|技术设计|writing-plans|把设计拆成可执行的任务，便于后续开发|
|开发阶段|test-driven-development|强制先写测试，避免bug堆积|
|调试阶段|systematic-debugging|系统化定位问题，不是到处加log|
|Code Review|request-code-review|自动化review流程，节省时间|
|项目交付|verification-before-completion|完成前检查，避免遗漏|

### 技巧2：和Claude对话时的一些小技巧

**1. 明确你要用哪个Skill**

不是说"帮我写代码"，而是说"加载test-driven-development Skill，帮我写个用户服务"

Claude会自动加载对应的指令和工作流。

**2. 把Skill当"规范"，不是"工具"**

很多人会问："Claude，帮我把这个代码重构一下"

但用superpowers后，应该是：  
"Claude，加载DRY原则，帮我检查这个代码有哪些重复逻辑，怎么提取成可复用的函数"

**3. 善用Skill的子功能**

比如test-driven-development Skill不光是写测试，它还包括：

- RED-GREEN-REFACTOR（重构代码）
    
- 清理未通过的测试代码
    
- 生成测试覆盖率报告
    

别只用表面功能。

**4. 定期更新Skill**

superpowers会自动更新，定期检查：  
`/plugin update superpowers`

保持最新版本，获得最新功能和bug修复。

## 06 国内开发者遇到的坑和解决方案

**坑1：技能冲突**

**问题**：同时加载了多个Skills，冲突了，Claude不知道听哪个的。

**解决方案**：superpowers的Skills设计成模块化的，冲突概率低。如果还是冲突，一次只加载一个Skill，完成任务后再加载下一个。

**坑2：测试环境问题**

**问题**：test-driven-development要求测试环境，但本地环境配置不对。

**解决方案**：superpowers的文档里有详细的测试环境配置说明，按文档配置。或者用Docker容器隔离测试环境。

**坑3：新手直接用高级功能**

**问题**：新手一开始就用subagent-driven-development，导致Claude启动太多子代理，卡死。

**解决方案**：新手先用brainstorming和test-driven-development，熟悉superpowers的工作方式后再用高级功能。

**坑4：中文文档缺失**

**问题**：superpowers的文档是英文的，新手看不懂怎么用。

**解决方案**：GitHub上有些国内开发者翻译了中文版本，可以搜索"superpowers 中文"。或者用翻译工具辅助阅读。

## 07 和其他Skill对比：什么时候该用superpowers？

|对比项|superpowers|其他常用Skills|建议|
|---|---|---|---|
|活跃性|模块化，可自由组合|通常单一功能，固定流程|复杂项目、需要自定义工作流 → 用superpowers|
|学习成本|中等偏高，需要理解设计哲学|较低，直接使用|长期用 → superpowers|
|功能完整度|非常完整，14个技能覆盖全流程|专注于某个领域|需要完整开发流程 → superpowers|
|开发者支持|63个Issues，活跃社区|文档+Issues回复|需要技术支持和社区交流 → 用superpowers|

**一句话总结**：

- 需要完整、标准化的开发流程？用superpowers
    
- 需要快速完成某个具体任务？用专门的单一Skill
    
- 个人用、小型项目？两者都行，看偏好
    

## 08 如何安装和使用？

### 安装方式

**Claude Code官方市场（推荐）**：

```
/plugin install superpowers@claude-plugins-official
```

这是官方渠道，最简单，支持自动更新。

**Cursor市场**：

```
/add-plugin superpowers
```

搜索"superpowers"安装。

**手动安装**：

1. Fork仓库：github.com/obra/superpowers
    
2. Clone到本地：`git clone https://github.com/obra/superpowers`
    
3. 在Claude Code设置中手动加载路径
    

### 首次使用建议

**第一步：先看文档**

打开：github.com/obra/superpowers

重点看：

- README.md：快速了解整体工作流
    
- skills/目录：看看有哪些Skills
    
- docs/目录：详细使用说明
    

**第二步：从简单开始**

先不加载所有Skills，选1-2个试试：

- 新手：用test-driven-development或brainstorming
    
- 有需求：用writing-plans
    
- 要review：用request-code-review
    

**第三步：理解工作流**

superpowers的核心工作流是7步：

1. brainstorming（需求分析）
    
2. using-git-worktrees（创建独立分支）
    
3. writing-plans（制定计划）
    
4. subagent-driven-development or executing-plans（开发）
    
5. test-driven-development（测试）
    
6. verification-before-completion（验证）
    
7. finishing-a-development-branch（完成）
    

不是每步都要用，根据你的需求选择。

**第四步：看Claude的输出**

Claude触发Skill后，会有详细的日志输出，告诉你它做了什么。关注这些日志，理解它的决策过程。

## 09 国内社区资源

### 中文文档和教程

目前国内中文资源还不多，但有一些：

1. **GitHub中文翻译**
    
    ：搜索"superpowers 中文"，有些开发者会翻译关键文档
    
2. **技术博客**
    
    ：掘金、知乎、少数派上有用户分享使用经验
    
3. **微信群**
    
    ：加入"Claude Code用户群"，经常有讨论
    
4. **YouTube**
    
    ：搜索"superpowers Claude"，有英文视频教程
    

### 推荐关注

**GitHub仓库**：github.com/obra/superpowers

- 关注Issues更新
    
- 参与讨论
    
- 查看最新动态
    

**技术社群**：

- r/ClaudeAI：国际社区，讨论更深入
    
- 掘金：国内技术分享平台
    
- 知乎：搜索"superpowers claude"，有使用心得
    

## 10 最后想说的话

聊了这么多，核心就三点：

**第一，superpowers不是什么神奇的黑科技**，它是把资深开发者的经验和方法论打包成Skill，让Claude按这些最佳实践帮你干活。84.7k stars说明大家认可它的价值。

**第二，国内开发者用它的核心场景**：新项目开始、代码质量保证、老项目维护、团队协作。这些都是开发者的真实痛点，superpowers正好解决了这些问题。

**第三，选择适合自己的工具**。不是所有人都需要superpowers——如果你是个人开发者、做简单功能、快速解决问题，用其他Skill可能更直接。但如果你是团队协作、需要标准化开发流程、处理复杂项目，superpowers可能是最佳选择。

**最后，建议你这样做**：

今天看完这篇文章，如果你是开发者，试试从test-driven-development或brainstorming这两个最常用的Skill开始。用了之后，在评论区分享你的体验——是好是坏、提升了多少效率、遇到了什么坑。

这样我们一起把superpowers用得更好，让更多国内开发者受益。

---

你在用superpowers吗？最常用的Skill是哪个？有没有遇到过特别好用的组合？欢迎在留言分享，大家一起交流。

---

  

![](https://mmbiz.qlogo.cn/sz_mmbiz_jpg/DhduwiaBa7leO1plpRLRYfjjw9iaTrPghbENQ0a2gQdbBoMCvX2iaCdlicPtCKnab5DVYuc6tyiaC6f96OwWnBV9YpA/0?wx_fmt=jpeg)

浪漫人生自由行

喜欢作者

阅读 2127

​

[](javacript:;)

![](https://mmbiz.qpic.cn/mmbiz_png/Cn6yRibcia5s0qNN7yww7KG7HlIHnjjibNhT72mU7A8IhXFbtPEoe50lBoULiaer1Iw160gSNzGFtqG6nbFLU0P1WQ/300?wx_fmt=png&wxfrom=18)

上升ing

关注

17

310

15

5

![](https://wx.qlogo.cn/mmopen/duc2TvpEgSRKrwicE9icxabloW41Md1WmBUBEibUbgoicG4wQiaIq4VxA3icgwOKGts9laXwJVF6CxRERrnbdmuvkGeCuIIBkT5nf28K25Ikkt9zWACAQeAvN0iaHrHDI3Jje6N/96)

复制搜一搜

复制搜一搜

暂无评论