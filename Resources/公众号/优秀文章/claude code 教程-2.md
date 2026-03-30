# Claude Code 一篇带你从入门到精通

原创 红薯的Java私房菜 Java一条人

 _2026年1月26日 21:16_ _天津_ 649人

虽然 **Claude Code** 名字中带有 "Code"，但它的功能绝不仅仅局限于写代码，而是一款真正意义上的通用 **Agent**。上一篇我们分享了 **[Claude Code 入门指南](https://mp.weixin.qq.com/s?__biz=Mzg2NTc4NDcyNw==&mid=2247485048&idx=1&sn=4442679ec7a5214abeda5af549e32047&scene=21#wechat_redirect)**，看完后你应该已经能够上手使用了。但是对于开发者来说，仅掌握这些基础功能是远远不够的，本篇文章我们将深入研究 Claude Code 的高级技能。

## 1. 记忆增强

你是否遇到过这样的情况：每次启动 Claude Code 后与它对话，感觉它就像一个失忆的天才。让它帮忙开发一个小程序时，它每次都会询问你是要创建微信小程序还是其他类型，后端使用 Java 还是 Python 等等这些基础的技术栈问题。次数多了就变得非常繁琐——这就是没有配置 `CLAUDE.md` 的 Claude Code。

### 1.1 CLAUDE.md 是什么？

它是一个特殊的 Markdown 文件，Claude Code 每次启动都会自动读取。写入其中的内容会被注入到 Claude 的系统提示（System Prompt）中，成为它思考的底层背景。

你可以在 CLAUDE.md 中写入常用的技术栈和开发规范等内容，这样每次重新打开 Claude 时就不需要重复交代这些信息了。此外，你还可以与 Claude 对话，输入"将 Java 开发规范、API 设计规范输出到 CLAUDE.md 文件"，让 Claude 自动为你生成一份 CLAUDE.md 文件。

### 1.2 创建 CLAUDE.md 文件

CLAUDE.md 不会自动创建，需要用户手动创建。创建方式很简单，主要有 3 种方式：`/init` 命令初始化、`/memory` 命令直接编辑，以及通过 `#` 操作符写入。

#### 使用 /init 初始化

在项目根目录打开 Claude，然后输入 `/init` 命令，Claude 会自动分析你的项目，并创建一个包含基本信息的 CLAUDE.md 文件：

`/init`

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia25mNBM89ZeFO4fpUvST4hwXge3ks1Tsjxzzp9ibs6Lv8jv0e4VjqK1kEtRiab8krkxUpy3dFksqaIw/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=0 "null")

  

#### 使用 /memory 编辑

任何时候你都可以在 Claude 对话窗口输入 `/memory` 命令，它会直接在编辑器里打开 CLAUDE.md 文件，让你进行更详细的编辑和整理：

`/memory`

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia25mNBM89ZeFO4fpUvST4hwLqjGbPqxW3xTlffTYOejIDGK4NdvFm3dOnA42yC8Shfqyu37uNakoQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=1 "null")

  

这里列出了 2 个选项，分别对应 2 个不同级别的 CLAUDE.md 文件：项目级和用户级，它们对应的作用和存放的内容也有所不同。

#### 使用 # 操作符写入

除了上述两种方式，还可以在对话中使用 `#` 号加上需要 Claude 记忆的内容。例如：`# 记住 Python 教学书籍：《Python 工匠》`，Claude 会自动将内容存入 CLAUDE.md：

`# 记住 Python 教学书籍：《Python 工匠》`

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia25mNBM89ZeFO4fpUvST4hwiaHszbWZYIE1hbZSTOkOmmZzUNuBYxWNDhu4ib9bRiciaUlMKujdGkGQVQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=2 "null")

  

### 1.3 记忆分层

在使用 `/memory` 命令时提到了两种 CLAUDE.md 文件，实际上共有 3 种 CLAUDE.md 文件：

- • **项目记忆**：保存在项目根目录下的 `CLAUDE.md`，保存项目的架构、技术栈和开发规范等，可以提交到 Git 与其他成员共享，**仅在当前项目中生效**
    
- • **用户记忆**：保存在用户空间的 `~/.claude/CLAUDE.md`，一般保存用户个人的偏好设置，**在所有项目中生效**
    
- • **企业记忆**：保存在 Claude 部署目录下（`/Library/Application Support/ClaudeCode/Claude.md`），存放公司级的安全、合规要求，由管理员配置
    

三个文件的加载顺序是：**企业 → 项目 → 用户**，后面的配置会覆盖前面的。因此，你的个人偏好拥有最高优先级！

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia25mNBM89ZeFO4fpUvST4hw1mmrHHQiaC4IgVFKZSNRIYiaLWjEVibbbFwcY7NkibL9OUTorGfqgciaYHQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=3 "null")

  

### 1.4 模块化记忆

如果项目过于复杂，CLAUDE.md 可能会变得臃肿。此时可以使用 `@` 导入语法，将其他文件的内容引入 CLAUDE.md，实现记忆的模块化管理。例如，我的项目根目录 CLAUDE.md：

``## Project Structure      minimall/   ├── backend/ # Spring Boot backend   ├── frontend/ # uni-app mini-program   ├── admin/ # Vue 3 admin console   ├── docker/ # Docker configurations   └── docker-compose.yml # Full stack orchestration      ## Module-Specific Documentation      For detailed information about each module, see:      - **Backend**: See `@backend/.claude/CLAUDE.md` for Spring Boot architecture, JPA conventions, API endpoints   - **Frontend**: See `@frontend/.claude/CLAUDE.md` for uni-app structure, Vue components, API integration   - **Admin**: See `@admin/.claude/CLAUDE.md` for Vue 3 setup, Element Plus, Pinia stores   ``

根目录的 CLAUDE.md 放置项目概览和快速启动命令，backend、frontend 和 admin 分别放置各自的项目架构、技术细节和开发规范等。这样组织就显得非常简洁、优雅！

---

## 2. Skills

Skills 现在非常火热，提到大模型就离不开 Skills 和 MCP 等概念，开发者在研究，管理者也在天天谈论它们的应用前景。本节我们将讲解什么是 Skills，以及如何快速上手。

### 2.1 什么是 Agent Skills

> Skill 是一个 Markdown 文件，它教 Claude 如何做特定的事情：使用你的团队标准审查 PR、以你喜欢的格式生成提交消息，或查询你公司的数据库架构。当你要求 Claude 做与 Skill 目的相匹配的事情时，Claude 会自动应用它。

先通过一个最简单的案例来理解：前段时间我在飞书上发布了一个 AI 知识库《Java 面试小绿书》，支持通过兑换码开通阅读权限。我一口气生成了 100 个兑换码，当小红书有用户下单后，我需要手动组织一段话放到物流详情里，模板如下：

> 【Java面试小绿书】知识库地址：https://ask.feishu.cn/shared-space/7472172092759474180  
> 兑换码：`Q3J3P************EZU`

每次发货时都需要把真实的兑换码替换到上面的模板中，非常不便。现在我想让 Claude 帮我简化这件事：

- • **输入**：从飞书导出的兑换码 Excel 文件和一个物流详情模板
    
- • **输出**：包含真实物流详情的 Excel 文件
    

让 Claude 帮我预组装 100 条物流详情并保存到新的 Excel 中。

我首先创建了一个模板文件 `logistics-template.md`，内容如下：

`【Java面试小绿书】知识库地址：https://ask.feishu.cn/shared-space/7472172092759474180    兑换码：${redeem-code}`

然后让 Claude 开始工作：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

稍等片刻就完成了：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

查看输出文件：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

结果完全符合预期。现在，我想让 Claude 记住这个处理流程，这样当这 100 个兑换码卖完后，再来 100 个新的兑换码时，只需要告诉它按照之前的处理流程处理即可：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

然后 Claude 会整理整个过程，把之前生成的代码都整理到 `~/.claude/skills` 目录下的 `redeem-to-logistics` 文件夹中，同时告诉我们如何使用：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

这就是我们培养 Claude Code 学会的一个新技能——**自定义 Agent Skills**。

### 2.2 Agent Skills 如何工作

从上面的结果可以看出，这个 skill 被存储在 `~/.claude/skills` 目录下，名称为 `redeem-to-logistics`。所有的 skill 都会被统一存储在这个目录中。这个 skill 目录下有两个文件（根据 skill 的复杂程度可能有所不同），其中 `skill.md` 是必须存在的，其他文件都是 skill 依赖的资源文件。`skill.md` 的格式如下所示：

``---   name: redeem-to-logistics   description: 将兑换码 Excel 文件按照物流模板格式转换为物流详情 Excel 文件。生成的物流详情为单列输出，每行包含模板替换后的真实内容。   license: MIT   ---      # 兑换码转物流详情      将兑换码 Excel 文件按照物流模板格式转换为物流详情 Excel 文件。生成的物流详情为单列输出，每行包含模板替换后的真实内容。      ## 使用场景      当需要批量生成物流详情信息时，使用此工具可以快速将兑换码转换为标准格式的物流详情。      ## 参数      - `input_file`: 输入的兑换码 Excel 文件路径（默认：redeem-code/20251226Java面试小绿书兑换码.xlsx）   - `output_file`: 输出的物流详情 Excel 文件路径（默认：20251226物流详情.xlsx）   - `template_file`: 物流模板文件路径（默认：redeem-code/logistics-template.md）      ...``

一个 skill 包含以下三部分内容：

- • **元数据**：Skill 的 YAML frontmatter，开头部分以 `---` 分隔。Claude 在启动时加载此元数据并将其包含在系统提示中。这种轻量级方法意味着你可以安装许多 Skills 而不会产生上下文成本；Claude 只知道每个 Skill 的存在以及何时使用它。
    
- • **指令**：SKILL.md 的主体，包含程序知识、工作流、最佳实践和指导。当我们的请求与 Skill 描述匹配时，Claude 通过 bash 从文件系统读取 SKILL.md。只有在这种情况下，此内容才会进入上下文窗口。
    
- • **资源**：Skill 的依赖项，Claude 仅在引用时访问这些文件。主要包括指令、代码和资源三部分：
    

- • **指令**：包含专业指导和工作流的其他 markdown 文件（如 `FORMS.md`、`REFERENCE.md`）
    
- • **代码**：Claude 通过 bash 可运行的执行脚本（如 `fill_form.py`、`validate.py`）；脚本提供确定性操作而不消耗上下文
    
- • **其他资源**：参考资料，如数据库架构、API 文档、模板或示例
    

这三部分内容的整合方式如下：

|级别|加载时间|令牌成本|内容|
|---|---|---|---|
|**第 1 级：元数据**|始终（启动时）|每个 Skill 约 100 个令牌|YAML 前置数据中的 `name` 和 `description`|
|**第 2 级：指令**|触发 Skill 时|不到 5k 个令牌|包含指令和指导的 SKILL.md 主体|
|**第 3 级+：资源**|按需|实际上无限制|通过 bash 执行的捆绑文件，不将内容加载到上下文中|

整个 Agent Skills 在服务器上的执行过程如下图所示：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

Skills 在代码执行环境中运行，Claude 具有文件系统访问、bash 命令和代码执行功能。可以这样理解：Skills 就是虚拟机上的一个目录，Claude 使用计算机上的 bash 命令与目录下的文件进行交互。

触发 Skill 时，Claude 使用 bash 从文件系统读取 SKILL.md，将其指令带入上下文窗口。如果这些指令引用其他文件（如 FORMS.md 或数据库架构），Claude 也会使用其他 bash 命令读取这些文件。当指令提及可执行脚本时，Claude 通过 bash 运行它们并仅接收输出（脚本代码本身永远不会进入上下文）。

**此架构支持以下功能：**

- • **按需文件访问**：Claude 仅读取每个特定任务所需的文件，其余文件保留在文件系统上，消耗零令牌。
    
- • **高效的脚本执行**：当 Claude 运行 `validate_form.py` 时，脚本的代码永远不会加载到上下文窗口中，仅脚本的输出（如"验证通过"或特定错误消息）消耗令牌。这要比 Claude 即时生成等效代码高效得多。
    
- • **捆绑内容没有实际限制**：因为文件在访问前不消耗上下文，Skills 可以包含各种 API 文档、大型数据集、各种示例或任何需要的参考资料，对于未使用的捆绑内容没有上下文成本。
    

这种基于文件系统的模型适用于渐进式披露工作的场景，Claude 导航我们的 Skill 就像我们参考入职指南的特定部分一样，访问每个任务所需的确切内容。

### 2.3 Agent Skills 分类

在了解 Agent Skills 的分类之前，我们先了解一下 Claude 提供的几个主要产品：

- • **Claude Code**：Anthropic 官方的命令行界面工具，让开发者直接在终端中使用 Claude 辅助软件工程任务
    
- • **Claude API**：Anthropic 提供的应用程序编程接口，允许开发者将 Claude 的 AI 能力集成到自己的应用程序和服务中
    
- • **Claude Agent SDK**：用于构建自定义 AI 代理的开发工具包，帮助开发者创建能够自主执行复杂任务的 AI 智能体
    
- • **Claude.ai**：Anthropic 的官方网站，提供网页版 Claude 聊天界面，让用户直接在浏览器中使用 Claude 进行对话
    

我们在 2.2 节的示例中演示的是使用 Claude Code 创建的**自定义 Skills**。Claude 除了支持自定义 Skills 以外，还为我们提供了一些**预构建的 Agent Skills**（官方出品），这些预构建的 Skills 可以开箱即用，包括：

- • **PowerPoint (pptx)**：创建演示文稿、编辑幻灯片、分析演示文稿内容
    
- • **Excel (xlsx)**：创建电子表格、分析数据、生成带图表的报告
    
- • **Word (docx)**：创建文档、编辑内容、格式化文本
    
- • **PDF (pdf)**：生成格式化的 PDF 文档和报告
    

上面提到的四种产品，并不是都支持这两种 Skills，功能矩阵如下：

|平台|预构建的 Agent Skills|自定义 Skills|
|---|---|---|
|Claude Code|❌|✅|
|Claude API|✅|✅|
|Claude Agent SDK|❌|✅|
|Claude.ai|✅|✅|

同时，还需要理解"共享范围"的概念——不同位置的 Skills 的可见范围是不同的：

- • **Claude.ai**：仅限个人用户；每个团队成员必须单独上传
    
- • **Claude API**：工作区范围；所有工作区成员可以访问上传的 Skills
    
- • **Claude Code**：个人（`~/.claude/skills/`）或基于项目（`.claude/skills/`）
    

像我上面通过 Claude Code 生成的 Skills 放在我个人的工作空间下，其他人是无法使用的。如果想让其他人也能使用，就需要上传到 Claude.ai 或 Claude API，或者放到项目的 `.claude/skills` 目录下通过 Git 提交。需要注意的是，Claude.ai 和 Claude API 之间的 Skills 是完全独立的，所以同一个 Skill 可能要分别上传到不同的平台。

### 2.4 Agent Skills 使用

现在我们退出 Claude 命令行重新打开，输入 `/skills` 命令就可以列出本地安装了哪些 skill：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

使用 Skills 有两种方法：手动调用和自动发现。

#### 手动调用

在 Claude 对话框中直接输入 `/skill-name` 就可以直接执行对应的 skill：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

这里会直接给出相关 skill 的提示，输入完整的命令后执行成功：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

#### 自动发现

我们可以与 Claude 对话让它帮我们完成指定任务，Claude 会读取 Skill 的描述，如果发现 Skill 与对话相关则加载它，通过 skill 完成任务。比如上面的示例可以改成对话形式：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

通过 Claude 的执行过程可以发现，它自动发现了 `redeem-to-logistics` 这个自定义 Skill 并用它完成了任务。

### 2.5 总结

如果说之前的 AI 是一个无所不知的“巨鲸”，那 Skill 机制则让整个生态“万物生长”。它把定义“能力”的权力，从 AI 公司交还给了每一位用户、每一个团队。我们不再只是被动的使用者，而是主动的“训练师”和“赋能者”。我们正在见证一个新时代的开启：AI 将不再是一个个孤立的“大脑”，而是能够深度融入我们工作流、理解我们独特上下文的“超级伙伴”。

如果你也想体验电脑上最智能的 AI，感受这种“人机合一”的默契，一定要试试 Claude Code 和它的 Skill 功能。

本文为了让大家对 Skills 有直观的了解并能够快速上手，讲解的内容都是基于 Claude Code。但 Skills 在 Claude API 或 Claude Agent SDK 场景下可能用法更加广泛，我会在后续的项目开发中与大家分享。

整理了一些目前非常火的 Claude Skills 供大家参考：

1. 1. **Anthropic 官方 Skills**：https://github.com/anthropics/skills
    
2. 2. **Superpowers**：1.6 万 Star 的 Skill 精选，从脑暴、写需求文档、开发、测试全包含，口碑相当好：https://github.com/obra/superpowers
    
3. 3. **Planning-with-files**：参考 Manus 的 Agent 方法写的 Skill，很适合多步骤任务：https://github.com/OthmanAdi/planning-with-files
    
4. 4. **X-article-publisher-skill**：王树义老师写的 X 文章发布 Skill，这个值得研究下：https://github.com/wshuyi/x-article-publisher-skill
    
5. 5. **NotebookLM skill**：自动上传 PDF、Youtube 链接到 NotebookLM：https://github.com/PleasePrompto/notebooklm-skill
    

## 3. Sub-Agent

我们让 AI 去完成一项任务时，一段好的提示词一般以 "你是一位旅行博主，现在帮我……" 这种形式开头。我们知道为 AI 预设一个角色它会更加擅长处理我们的任务，Claude 也是如此。这是为什么呢？

是 Sub-Agent 在背后起作用。读完本节内容，你会学会如何使用 Sub-Agent、如何创建自己的 Sub-Agent，以及它与上面学过的 Skills 有什么区别。

### 3.1 什么是 Sub-Agent

Sub-Agent（子代理）是专门处理特定类型任务的 AI 助手。每个子代理在自己的上下文窗口中运行，具有自定义系统提示、特定的工具访问权限和独立的权限。**当 Claude 遇到与 Sub-Agent 描述相匹配的任务时，它会委托给该 Sub-Agent，该 Sub-Agent 独立工作并返回结果。**

子代理可以帮助你：

- • **保留上下文**：通过将探索和实现保持在主对话之外
    
- • **强制执行约束**：通过限制子代理可以使用的工具
    
- • **跨项目重用配置**：使用用户级子代理
    
- • **专门化行为**：使用针对特定领域的聚焦系统提示
    
- • **控制成本**：通过将任务路由到更快、更便宜的模型（如 Haiku）
    

Claude 使用每个子代理的描述来决定何时委托任务。

概念对比：

- • **Main-Agent（主代理）**：Claude 本身就是一个 Agent，我们可以理解为 Main-Agent。它是主要的上下文对话，有权限调用不同的 Tools、MCP、Skills 和 Sub-Agent，目的在于完成任务。
    
- • **Skills（技能）**：是知识注入。你教会 Main Agent（Claude Code）一个新的技能，它在**当前对话上下文**中运行，本质上是给主 AI "加技能点"。
    
- • **Sub-agents（子代理）**：是任务委派。你召唤一个独立的、专业的 AI 分身去处理一个特定任务。它在**独立的上下文**中运行，拥有专属的工具权限，最终把结果返回给 Main-agent 进行处理。
    

### 3.2 内置 Sub-Agent

与 Skills 类似，Claude Code Sub-Agent 也分为两种：**内置 Sub-Agent** 和 **自定义 Sub-Agent**。

Claude Code 内置 Sub-Agent 包括 Explore、Plan 和 General-purpose 等，这些通常由 Claude 在适当时候自动调用，你不需要直接使用它们。

#### Explore

一个快速的、只读的代理，针对搜索和分析代码库进行了优化。

- • **模型**：Haiku（快速、低延迟）
    
- • **工具**：只读工具（拒绝访问写入和编辑工具）
    
- • **目的**：文件发现、代码搜索、代码库探索
    

当 Claude 需要搜索或理解代码库而不进行更改时，它会委托给 Explore。这样可以将探索结果保持在主对话上下文之外。调用 Explore 时，Claude 指定一个彻底程度：**quick** 用于有针对性的查找，**medium** 用于平衡的探索，或 **very thorough** 用于全面分析。

#### Plan

在 **计划模式** 期间用于研究计划之前收集的上下文。

- • **模型**：继承自主对话
    
- • **工具**：只读工具（拒绝访问写入和编辑工具）
    
- • **目的**：用于规划的代码库研究
    

当你处于计划模式且 Claude 需要理解你的代码库时，它会将研究委托给 Plan 子代理。这样可以防止无限嵌套（子代理无法生成其他子代理），同时仍然收集必要的上下文。

#### General-purpose

一个能够处理复杂、多步骤任务的代理，这些任务需要探索和操作。

- • **模型**：继承自主对话
    
- • **工具**：所有工具
    
- • **目的**：复杂研究、多步骤操作、代码修改
    

当任务需要探索和修改、复杂推理来解释结果或多个相关步骤时，Claude 会委托给 general-purpose。

#### 其他

|代理|模型|Claude 何时使用|
|---|---|---|
|Bash|继承|在单独的上下文中运行终端命令|
|statusline-setup|Sonnet|当你运行 `/statusline` 来配置状态行时|
|Claude Code Guide|Haiku|当你提出关于 Claude Code 功能的问题时|

### 3.3 自定义 Sub-Agent

除了内置子代理之外，你还可以创建自定义子代理，具有自定义提示、工具限制、权限模式、钩子和技能。下面演示如何创建一个代码审查 Sub-Agent，以及如何使用该 Sub-Agent 为代码库提出改进建议。

#### 创建自定义 Sub-Agent

1. 1. 打开 Sub-Agent 界面
    
    首先，在 Claude Code 中运行 /gents 命令：
    

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

1. 2. 创建新的用户级代理
    
    选择 “Create new agent” ：
    

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

`支持创建两种作用域的 Sub-Agent ：   - **项目级**：存储在项目根目录的 .claude/agents/ 目录下   - **用户级**：存储在用户根目录的 ~/.claude/agents/ 目录下`

1. 3. 使用 Claude 生成
    
    使用这里我们选择 “Personal” ：
    

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

`创建 Sub-Agent 有两种方式：   - **Generate with Claude**：跟着 Claude 的命令行交互往下走即可；   - **Manual configuration**：手动编辑 Sub-Agent 的配置文件。   这里选择 “Generate with Claude” 通过 Claude 生成。出现提示时，修改子代理的描述为：      ```sh   一个代码改进代理，扫描文件并为可读性、性能和最佳实践提出改进建议。   它应该解释每个问题、显示当前代码并提供改进版本。   ```   ![[learning/8.AI/开发工具/Claude Code/02/create-by-claude.png]]`

1. 4. 选择工具
    

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

`代码审查者应该仅赋予代码的只读权限，所以这里需要取消除 Read-only tools 之外的所有内容。如果你保持所有工具被选中，子代理将继承主对话可用的所有工具。`

1. 5. 选择模型
    
    选择子代理使用的模型。对于此示例代理，选择 **Sonnet**，它在分析代码模式的能力和速度之间取得平衡。
    

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

1. 6. 选择颜色
    
    为子代理选择背景颜色。这可以帮助我们在 UI 界面识别是哪个子代理正在运行。
    

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

`我选择 “Yellow” ，你随意。`

1. 7. 保存并尝试
    
    保存 Sub-Agent 后可以立即使用（我现在在 minimall 项目目录下），在 Claude 命令行输入一下内容：
    
    `使用 code-improver 代理为此项目提出改进建议`
    
    Claude Code 会选择使用 code-improver Sub-Agent 为项目提出建议：
    

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

#### 配置 Sub-Agent

在 Claude Code 对话的命令行再次输入 /agent 命令，会提供一个交互式界面来管理 Sub-Agent ：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

这里可以选择创建新的 Sub-Agent ，也可以选择管理已有的 Sub-Agent 。选择上面创建好的 code-improver 回车会进入该 Sub-Agent 的管理页面：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

管理页面支持预览 agent 的功能、编辑 agent 和删除 agent 。

选择 Edit agent 可以直接编辑 Sub-Agent 的 YAML frontmatter ：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

`frontmatter` 支持的字段有：

|字段|必需|描述|
|---|---|---|
|`name`|是|使用小写字母和连字符的唯一标识符|
|`description`|是|Claude 何时应委托给此子代理|
|`tools`|否|子代理可以使用的 工具。如果省略，继承所有工具|
|`disallowedTools`|否|要拒绝的工具，从继承或指定的列表中删除|
|`model`|否|模型<br><br> 使用：`sonnet`、`opus`、`haiku` 或 `inherit`。默认为 `sonnet`|
|`permissionMode`|否|权限模式<br><br>：`default`、`acceptEdits`、`dontAsk`、`bypassPermissions` 或 `plan`|
|`skills`|否|在启动时加载到子代理上下文中的 技能。注入完整技能内容，而不仅仅是使其可用于调用。子代理不继承父对话中的技能|
|`hooks`|否|限定于此子代理的 生命周期钩子|

我们上面通过 Claude Code 命令行交互创建的 Sub-Agent 已经设置过的有 name、description、tools、model 和 color 。

#### 使用 Sub-Agent

上面演示了如何使用 Sub-Agent 进行代码审查，我们在与 Claude Code 的对话中显式指定了 Sub-Agent ：

`使用 code-improver 代理为此项目提出改进建议`

其实，我们不显式指定使用哪个 Sub-Agent 也是可以的， Claude 会根据请求中的任务描述、 Sub-Agent 配置中的 `description` 字段和当前上下文自动委托任务。

此外，Sub-Agent 可以在前台（阻塞）或后台（并发）运行：

- • **前台 Sub-Aegnt**：阻塞主对话直到完成，权限提示和澄清问题（如 `AskUserQuestion`）会传递给主会话。
    
- • **后台 Sub-Agent**：在你继续工作时并发运行。它们继承父级的权限并自动拒绝任何未预先批准的内容。如果后台子代理需要它没有的权限或需要提出澄清问题，该工具调用失败但子代理继续。MCP 工具在后台子代理中不可用。
    

如果后台子代理由于缺少权限而失败，你可以在前台使用交互式提示重试 恢复它 。

有两种方式在后台运行 Sub-Agent ：

- • 要求 Claude “在后台运行”
    
- • 按 **Ctrl+B** 将运行中的任务放在后台
    

##### 常见模式

###### **（1）隔离高容量操作**

Sub-Agent 最有效的用途之一是隔离产生大量输出的操作。 运行测试、获取文档或处理日志文件可能会消耗大量上下文，此时可以将这些任务委托给 Sub-Agent ，输出的详细内容会保留在 Sub-Agent 的上下文中，而只给主对话返回相关摘要。比如：

`使用子代理运行测试套件，仅报告失败的测试及其错误消息`

###### **（2）并行运行研究**

对于彼此独立的任务，可以同时生成多个子代理并行工作：

`使用单独的子代理并行研究身份验证、数据库和 API 模块`

每个子代理独立研究各自的区域，然后 Claude 综合这些研究结果（**当研究路径彼此不依赖时，效果最好**）。

当子代理完成时，它们的结果会返回给主对话，所以运行多个子代理，由于每个都返回详细结果，这可能会消耗大量上下文。

###### **（3）链接子代理**

对于多步骤工作流，可以要求 Claude 按顺序使用多个子代理。每个子代理完成其任务并将结果返回给 Claude，然后 Claude 将相关上下文传递给下一个子代理：

`使用 code-reviewer 子代理查找性能问题，然后使用 optimizer 子代理修复它们`

##### 在子代理和主对话之间选择

在以下情况下使用**主对话**：

- • 任务需要频繁的来回或迭代改进
    
- • 多个阶段共享重要上下文（规划 → 实现 → 测试）
    
- • 你正在进行快速、有针对性的更改
    
- • 延迟很重要。子代理从头开始，可能需要时间收集上下文
    

在以下情况下使用**子代理**：

- • 任务产生您不需要在主上下文中的详细输出
    
- • 你想强制执行特定的工具限制或权限
    
- • 工作是自包含的，可以返回摘要
    

在以下情况下使用 **`Skills`** ：

- • 想要在主对话上下文中运行可重用提示或工作流而不是隔离的子代理上下文
    
- • 如果工作流需要嵌套委托（子代理无法生成其他子代理，也可使用从主对话 链接子代理）
    

##### 管理子代理上下文

###### **（1）恢复子代理**

每个子代理调用都会创建一个具有新鲜上下文的新实例。如果要继续现有子代理的工作而不是重新开始，可以要求 Claude 恢复它：

`使用 code-reviewer 子代理审查身份验证模块   [代理完成]      继续该代码审查，现在分析授权逻辑   [Claude 使用来自先前对话的完整上下文恢复子代理]`

恢复的子代理保留其完整的对话历史，包括所有以前的工具调用、结果和推理。子代理会从停止的地方继续，而不是从头开始。当子代理完成时，Claude 接收其代理 ID。

可以要求 Claude 提供代理 ID（如果您想显式引用它），或在 `~/.claude/projects/{project}/{sessionId}/subagents/` 的成绩单文件中查找 ID。每个成绩单存储为 `agent-{agentId}.jsonl`，编程使用请参阅 Agent SDK 中的子代理。

子代理成绩单独立于主对话持久化：

- • **主对话压缩**：当主对话压缩时，子代理成绩单不受影响，它们存储在单独的文件中。
    
- • **会话持久性**：子代理成绩单在其会话中持久化，可以通过恢复相同会话在重启 Claude Code 后 恢复子代理。
    
- • **自动清理**：成绩单根据 `cleanupPeriodDays` 设置进行清理（默认：30 天）。
    

###### **（2）自动压缩**

子代理支持使用与主对话相同的逻辑进行自动压缩。当子代理的上下文接近其限制时，Claude Code 会总结较旧的消息以释放空间，同时保留重要上下文。压缩事件记录在子代理成绩单文件中：

`{     "type": "system",     "subtype": "compact_boundary",     "compactMetadata": {       "trigger": "auto",       "preTokens": 167189     }   }`

`preTokens` 值表示压缩发生前使用了多少令牌。

### 3.4 Sub-Agent 范围

Sub-Agent 是带有 YAML frontmatter 的 Markdown 文件。根据范围将它们存储在不同位置。当多个子代理共享相同名称时，优先级较高的位置获胜。

|位置|范围|优先级|如何创建|
|---|---|---|---|
|`--agents`<br><br> CLI 标志|当前会话|1（最高）|启动 Claude Code 时传递 JSON|
|`.claude/agents/`|当前项目|2|交互式或手动|
|`~/.claude/agents/`|所有项目|3|交互式或手动|
|插件的 `agents/` 目录|启用插件的位置|4（最低）|与 插件 一起安装|

**项目子代理**（`.claude/agents/`）非常适合特定于代码库的子代理。可以提交到版本控制中，以便团队成员可以协作使用和改进它们。

**用户子代理**（`~/.claude/agents/`）是在所有项目中可用的个人子代理。

**CLI 定义的子代理**在启动 Claude Code 时作为 JSON 传递。它们仅存在于该会话中，不会保存到磁盘，使其对快速测试或自动化脚本很有用：

`claude --agents '{  "code-reviewer": {    "description": "Expert code reviewer. Use proactively after code changes.",    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",    "tools": ["Read", "Grep", "Glob", "Bash"],    "model": "sonnet"     }   }'`

`--agents` 标志接受与 frontmatter 相同字段的 JSON。对系统提示使用 `prompt`（等同于基于文件的子代理中的 markdown 正文）。有关完整 JSON 格式，请参阅 CLI 参考。

**插件子代理**来自你已安装的 插件。它们与你的自定义子代理一起出现在 `/agents` 中。有关创建插件子代理的详细信息，请参阅 插件组件参考。

### 3.5 总结

子代理机制，远不止是提升效率那么简单。它迫使我们思考：如何将复杂任务拆解？如何定义清晰的职责边界？如何设计高效的协作流程？这套方法论，不仅适用于管理 AI，同样适用于管理人类团队。

---

## 4. Claude MCP

我们的 Claude Code 现在非常聪明，但是有很多实现现在仍然无法做到。比如，它不知道我的 GitHub 项目 star 数是多少，我的飞书文档浏览量是多少等等。本节就来讲解如何通过 MCP 让 Claude Code 插上翅膀。

### 4.1 什么是 MCP

MCP（Model Context Protocol，模型上下文协议）是一个用于 AI 工具集成的开源标准，为我们提供了统一的解决方案：它将第三方服务暴露的能力按照一个统一标准封装为 MCP Server，同时提供了访问它的 MCP Client。这样，Claude Code 通过内置 MCP Client 就可以与这些三方服务通信，获取到三方服务赋予它的能力。通过 MCP，Claude Code 可以连接到数百个外部工具和数据源。

连接 MCP 服务器后，你可以要求 Claude Code：

- • **从问题跟踪器实现功能**：“添加 JIRA 问题 ENG-4521 中描述的功能，并在 GitHub 上创建 PR。”
    
- • **分析监控数据**：“检查 Sentry 和 Statsig 以检查 ENG-4521 中描述的功能的使用情况。”
    
- • **查询数据库**：“根据我们的 PostgreSQL 数据库，找到使用功能 ENG-4521 的 10 个随机用户的电子邮件。”
    
- • **集成设计**：“根据在 Slack 中发布的新 Figma 设计更新我们的标准电子邮件模板”
    
- • **自动化工作流**：“创建 Gmail 草稿，邀请这 10 个用户参加关于新功能的反馈会议。“
    

Claude Code 官方列出了一些可以连接到的常用 MCP 服务器：

1. 1. Circleback 🎯 会议智能助手 MCP
    

- • 搜索和访问会议记录、纪要
    
- • 访问日历数据和事件
    
- • 搜索邮件通信内容
    
- • 将会议上下文提供给 AI 助手
    

3. 2. bioRxiv 📚 生物学预印本论文检索 MCP
    

- • 搜索 bioRxiv 生物学预印本论文库
    
- • 访问论文元数据（标题、作者、摘要等）
    
- • 支持文献综述和自动化文献搜索
    
- • 为 AI 助手提供标准化的生物学论文检索接口
    

5. 3. ChEMBL 💊 药物发现化学数据库 MCP
    

- • 访问 ChEMBL 生物活性数据库（包含数百万药物分子数据）
    
- • 提供 22 个专业工具用于药物发现
    
- • 支持复杂的药物发现工作流
    
- • 直接与 ChEMBL REST API 集成
    
- • 进行化合物活性查询和分析
    

7. 4. Clinical Trials (AACT) 🏥 临床试验数据库 MCP
    

- • 访问 AACT 临床试验数据库
    
- • 分析临床试验数据
    
- • 跟踪临床试验趋势
    
- • 生成试验洞察和报告
    
- • 支持医疗数据分析和研究
    

9. 5. Canva 🎨 官方设计创作 MCP
    

- • AI 驱动设计创建：通过对话直接创建、编辑和预览设计作品
    
- • 自然语言操作：用文字描述就能生成专业设计
    
- • 实时预览：在对话中即时查看设计效果
    
- • 设计编辑：修改已有设计的元素、文本、图片等
    

- • ......
    

> 使用第三方 MCP 服务器需自担风险 - Anthropic 尚未验证 所有这些服务器的正确性或安全性。 确保您信任要安装的 MCP 服务器。 使用可能获取不受信任内容的 MCP 服务器时要特别小心， 因为这些可能会使您面临提示注入风险。

如果你需要特定的集成，可以到 GitHub 上找到数百个更多 MCP 服务器 ，或使用 MCP SDK 构建自己的服务器。

### 4.2 安装 MCP 服务器

MCP 服务器根据需求有三种不同的配置方式：

- • 选项 1：添加远程 HTTP 服务器
    
    **HTTP 服务器是连接到远程 MCP 服务器的推荐选项。这是云服务最广泛支持的传输方式。**
    
    `# 基本语法   claude mcp add --transport http <name> <url>      # 真实示例：连接到 Notion   claude mcp add --transport http notion https://mcp.notion.com/mcp      # 带有 Bearer 令牌的示例   claude mcp add --transport http secure-api https://api.example.com/mcp \     --header "Authorization: Bearer your-token"`
    
- • 选项 2：添加远程 SSE 服务器
    
    SSE (Server-Sent Events) 传输已弃用。请在可用的地方使用 HTTP 服务器。
    
    `# 基本语法   claude mcp add --transport sse <name> <url>      # 真实示例：连接到 Asana   claude mcp add --transport sse asana https://mcp.asana.com/sse      # 带有身份验证标头的示例   claude mcp add --transport sse private-api https://api.company.com/sse \     --header "X-API-Key: your-key-here"`
    
- • 选项 3：添加本地 stdio 服务器
    
    Stdio 服务器作为本地进程在你的计算机上运行。它们非常适合需要直接系统访问或自定义脚本的工具。
    
    `# 基本语法   claude mcp add [options] <name> -- <command> [args...]      # 真实示例：添加 Airtable 服务器   claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \     -- npx -y airtable-mcp-server` 
    

**选项顺序：**  

  
所有选项（`--transport`、`--env`、`--scope`、`--header`）必须位于服务器名称**之前**。`--`（双破折号）然后将服务器名称与传递给 MCP 服务器的命令和参数分开。

例如：

- • `claude mcp add --transport stdio myserver -- npx server` → 运行 `npx server`
    
- • `claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080` → 在环境中使用 `KEY=value` 运行 `python server.py --port 8080`
    

这可以防止 Claude 的标志与服务器标志之间的冲突。

#### 安装麦当劳 MCP 服务器

先来看一个好玩的：麦当劳官方上线了 MCP 服务，安装后可以查看麦当劳最新的日历活动，还能让 AI 帮你抢优惠券！

首先到 麦当劳 MCP 开放平台 登录（手机号+验证码）：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

登录成功后跳转回首页，“登录”按钮变成“控制台”：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

点击右上角“控制台”后，会弹出控制台弹窗，点击激活按钮，申请 MCP Token ：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

打开终端，输入一下命令在 Claude Code 配置 MCP Server ：

`claude mcp add --transport http mcd-mcp https://mcp.mcd.cn/mcp-servers/mcd-mcp \     --header "Authorization: Bearer <your-token>"`

上面的 `<your-token>` 替换成你自己的 Token ，回车，就完成了为 Claude Code 安装麦当劳 MCP 的流程。下面来试一下：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

Claude 会选择使用 mcd-mcp 查询能够领取的优惠券：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

Claude 已经给你列出了能够领取的所有优惠券，现在让它帮你领取：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

现在快去打开你的麦当劳 APP 或小程序查收一下吧！

> 大部分主流的 MCP Server 除了支持 Claude Code 接入，还支持 Cherry Studio 、Cursor 和 TRAE 等平台接入，详细接入流程参考： https://open.mcd.cn/mcp/doc

### 4.3 MCP 安装范围

MCP 服务器可以在三个不同的范围级别进行配置，每个级别都用于管理服务器可访问性和共享的不同目的。了解这些范围可以帮助您确定为特定需求配置服务器的最佳方式。

#### 本地范围

本地范围的服务器代表默认配置级别，存储在项目路径下的 `~/.claude.json` 中。这些服务器对您保持私密，仅在当前项目目录中工作时可访问。此范围非常适合个人开发服务器、实验配置或包含不应共享的敏感凭据的服务器。

`# 添加本地范围的服务器（默认）   claude mcp add --transport http stripe https://mcp.stripe.com      # 显式指定本地范围   claude mcp add --transport http stripe --scope local https://mcp.stripe.com`

#### 项目范围

项目范围的服务器通过将配置存储在项目根目录的 `.mcp.json` 文件中来启用团队协作。此文件设计为检入版本控制，确保所有团队成员都可以访问相同的 MCP 工具和服务。添加项目范围的服务器时，Claude Code 会自动创建或更新此文件，使用适当的配置结构。

`# 添加项目范围的服务器   claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp`

生成的 `.mcp.json` 文件遵循标准化格式：

`{     "mcpServers": {       "shared-server": {         "command": "/path/to/server",         "args": [],         "env": {}       }     }   }`

出于安全原因，Claude Code 在使用来自 `.mcp.json` 文件的项目范围服务器之前会提示批准。如果您需要重置这些批准选择，请使用 `claude mcp reset-project-choices` 命令。

#### 用户范围

用户范围的服务器存储在 `~/.claude.json` 中，提供跨项目可访问性，使其在您的计算机上的所有项目中可用，同时对您的用户帐户保持私密。此范围适用于个人实用程序服务器、开发工具或您在不同项目中经常使用的服务。

`# 添加用户服务器   claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic`

根据以下条件选择您的范围：

- • **本地范围**：个人服务器、实验配置或特定于一个项目的敏感凭据
    
- • **项目范围**：团队共享的服务器、项目特定的工具或协作所需的服务
    
- • **用户范围**：跨多个项目需要的个人实用程序、开发工具或经常使用的服务
    

**MCP 服务器存储在哪里：**

- • **用户和本地范围**：`~/.claude.json`（在 `mcpServers` 字段或项目路径下）
    
- • **项目范围**：项目根目录中的 `.mcp.json`（检入源代码控制）
    
- • **托管**：系统目录中的 `managed-mcp.json`（请参阅 托管 MCP 配置）
    

**范围层次结构和优先级：**

MCP 服务器配置遵循清晰的优先级层次结构。当具有相同名称的服务器存在于多个范围时，系统通过优先考虑本地范围的服务器来解决冲突，然后是项目范围的服务器，最后是用户范围的服务器。此设计确保个人配置可以在需要时覆盖共享配置。

### 4.4 管理 MCP 服务器

配置好 MCP 服务器后，可以使用这些命令管理 MCP 服务器：

`# 列出所有配置的服务器   claude mcp list      # 获取特定服务器的详细信息   claude mcp get github      # 删除服务器   claude mcp remove github      # （在 Claude Code 中）检查服务器状态   /mcp`

## 5. Plug-In

我们前面介绍的 Skills、MCP、Sub-Agent 等都是 Claude Code 强大的扩展功能，但是这些能力都比较分散。有没有一个东西能够把一套 Skills、MCP 和 Sub-Agent 整个打包到一块儿，然后彼此分享呢？这就是 Plug-In 要做的事情。本节课程我们讲解一下 Plug-In 的概念和基本使用方法，后面的章节会为大家分享一个非常厉害的开源 Plug-In。

### 5.1 什么是 Plug-In

Plug-In 即插件，如果把 Claude Code 理解为一个 AI 操作系统，那么一个 Plug-In 就是操作系统中的一个应用，这个应用五脏俱全，打包了 Skills 、MCP 和 Sub-Agent 等功能，我们可以把这个插件一键打包发布到应用市场供别人使用，同样也可以从市场下载别人发布的优秀插件。

一个 Plug-In 可以包含五种核心组件，它们共同构成了这个强大的生态系统：

- • 命令（Commands）：你主动下达的指令，如 /deploy
    
- • 技能（Skills）：它根据上下文自动出发的能力
    
- • 钩子（Hooks）：在特定事件发生时自动执行的脚本，实现“无人值守”的自动化。
    
- • 子代理（Sub-Agent）：专精于某一领域的“子人格”，让Claude 能够分身处理复杂人物。
    
- • MCP服务器：外部工具和服务集成
    

### 5.2 创建插件

本小节带大家创建自己的第一个插件，在创建之前，先确保自己的 Claude Code 版本在 1.0.33 或更高版本。

#### 创建插件目录

每个插件都位于其自己的目录中，包含清单和你的自定义命令、技能、代理或钩子。现在创建一个：

`mkdir my-first-plugin`

#### 创建插件清单

位于 `.claude-plugin/plugin.json` 的清单文件定义了你的插件的身份：其名称、描述和版本。Claude Code 使用此元数据在插件管理器中显示你的插件。在你的插件文件夹内创建 `.claude-plugin` 目录：

`mkdir my-first-plugin/.claude-plugin`

然后使用以下内容创建 `my-first-plugin/.claude-plugin/plugin.json`：

`{    "name": "my-first-plugin",    "description": "A greeting plugin to learn the basics",    "version": "1.0.0",    "author": {    "name": "Your Name"       }   }`

各字段含义如下：

|字段|用途|
|---|---|
|`name`|唯一标识符和斜杠命令命名空间。斜杠命令以此为前缀（例如 `/my-first-plugin:hello`）。|
|`description`|在浏览或安装插件时在插件管理器中显示。|
|`version`|使用语义版本控制跟踪发布。|
|`author`|可选。有助于归属。|

有关 `homepage`、`repository` 和 `license` 等其他字段，请参阅完整清单架构。

#### 添加斜杠命令

斜杠命令是 `commands/` 目录中的 Markdown 文件。文件名即为斜杠命令名称，以插件的命名空间为前缀，比如，`my-first-plugin` 插件中的 `hello.md` 文件会创建 `/my-first-plugin:hello` 斜杠命令， Markdown 内容告诉 Claude 当有人运行斜杠命令时如何响应。在你的插件文件夹中创建 `commands` 目录：

`mkdir my-first-plugin/commands`

然后使用以下内容创建 `my-first-plugin/commands/hello.md` ：

`---   description: Greet the user with a friendly message   ---      # Hello Command      Greet the user warmly and ask how you can help them today.`

#### 测试你的插件

使用 `--plugin-dir` 标志运行 Claude Code 以加载你的插件：

`claude --plugin-dir ./my-first-plugin`

使用 `--plugin-dir` 标志启动 Claude 会直接加载你的插件，无需安装，适合在开发期间测试用。所以，每次对插件进行更改后，以这种方式重启 Claude Code 即可。也可以通过多次指定标志来一次加载多个插件：

`claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two`

Claude Code 启动后，尝试你的新命令：

`/my-first-plugin:hello`

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

你会看到 Claude 用问候语回应。运行 `/help` 以查看你的命令在插件命名空间下列出：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

> **为什么要命名空间？**  
>  插件斜杠命令始终被命名空间化（如 `/greet:hello`），以防止多个插件具有相同名称的命令时发生冲突。要更改命名空间前缀，请更新 `plugin.json` 中的 `name` 字段。

#### 添加斜杠命令参数

通过接受用户输入使你的斜杠命令动态化。`$ARGUMENTS` 占位符捕获用户在斜杠命令后提供的任何文本。更新你的 `hello.md` 文件：

`---   description: Greet the user with a personalized message   ---      # Hello Command      Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.`

重启 Claude Code 以获取更改，然后尝试使用你的名字运行命令：

`/my-first-plugin:hello Alex`

Claude 将按名字向你问候。有关更多参数选项，如 `$1`、`$2` 用于单个参数，请参阅斜杠命令。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

你已成功创建并测试了一个包含以下关键组件的插件：

- • **插件清单**（`.claude-plugin/plugin.json`）：描述你的插件的元数据
    
- • **命令目录**（`commands/`）：包含你的自定义斜杠命令
    
- • **命令参数**（`$ARGUMENTS`）：捕获用户输入以实现动态行为
    

`--plugin-dir` 标志对开发和测试很有用。当你准备好与他人共享你的插件时，请参阅创建和分发插件市场。

### 5.3. 开发复杂插件

一旦你对基本插件感到满意，你就可以创建更复杂的扩展。

#### 向插件添加 Skills

插件可以包含 Agent Skills 以扩展 Claude 的功能。Skills 是 Claude 根据任务上下文自动使用它们。在插件根目录添加一个 `skills/` 目录，其中包含包含 `SKILL.md` 文件的 Skill 文件夹：

`my-plugin/   ├── .claude-plugin/   │   └── plugin.json   └── skills/       └── code-review/           └── SKILL.md`

如 2.2 节描述，每个 `SKILL.md` 需要包含 `name` 和 `description` 字段的前置内容，后跟说明：

`---   name: code-review   description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.   ---      When reviewing code, check for:   1. Code organization and structure   2. Error handling   3. Security concerns   4. Test coverage`

安装插件后，重启 Claude Code 以加载 Skills。有关完整的 Skill 编写指南，包括渐进式披露和工具限制，请参阅Agent Skills。

#### 向插件添加 LSP 服务器

> 对于 TypeScript、Python 和 Rust 等常见语言，请从官方市场安装预构建的 LSP 插件。仅当你需要支持官方 LSP 插件尚未覆盖的语言时，才创建自定义 LSP 插件。

LSP（语言服务器协议）插件为 Claude 提供实时代码智能。如果你需要支持没有官方 LSP 插件的语言，你可以通过向你的插件添加 `.lsp.json` 文件来创建自己的插件：

`{  "go": {    "command": "gopls",    "args": ["serve"],    "extensionToLanguage": {      ".go": "go"       }     }   }`

安装你的插件的用户必须在他们的机器上安装语言服务器二进制文件。有关完整的 LSP 配置选项，请参阅LSP 服务器。

#### 目录结构

对于具有许多组件的插件，按功能组织你的目录结构。关完整的目录结构如下：

`enterprise-plugin/   ├── .claude-plugin/           # 元数据目录   │   └── plugin.json          # 必需：插件清单   ├── commands/                 # 默认命令位置   │   ├── status.md   │   └── logs.md   ├── agents/                   # 默认代理位置   │   ├── security-reviewer.md   │   ├── performance-tester.md   │   └── compliance-checker.md   ├── skills/                   # 代理技能   │   ├── code-reviewer/   │   │   └── SKILL.md   │   └── pdf-processor/   │       ├── SKILL.md   │       └── scripts/   ├── hooks/                    # 钩子配置   │   ├── hooks.json           # 主钩子配置   │   └── security-hooks.json  # 其他钩子   ├── .mcp.json                # MCP 服务器定义   ├── .lsp.json                # LSP 服务器配置   ├── scripts/                 # 钩子和实用脚本   │   ├── security-scan.sh   │   ├── format-code.py   │   └── deploy.js   ├── LICENSE                  # 许可证文件   └── CHANGELOG.md             # 版本历史`

从文档结构上来看，就很直观的能够认识到 Plug-in 与 Skills 之间的区别了，Skills 是Plug-In的下位概念，而Plug-In则是Skills，MCP，Sub-Agent的上位概念。

#### 调试插件

如果你的插件不按预期工作：

1. 1. **检查结构**：确保你的目录位于插件根目录，而不是在 `.claude-plugin/` 内
    
2. 2. **单独测试组件**：分别检查每个命令、代理和钩子
    
3. 3. **使用验证和调试工具**：有关 CLI 命令和故障排除技术，请参阅调试和开发工具
    

### 5.4. 共享插件

到目前为止，你已经创建了一个比较复杂的插件了，此时如果你想把这个插件与他人共享，可以通过插件市场进行分发以供他人安装。一旦你的插件在市场中，其他人可以使用发现和安装插件中的说明安装它。有关完整的技术规范、调试技术和分发策略，请参阅插件参考。

市场也分两种：本地市场和远程市场。二者的范围不一样，本地市场仅限于本地访问，而远程市场则可以与他人共享插件。

#### 创建本地市场

上面已经创建了一个插件 my-first-plug ，只需要对此目录结构进行简单调整就可以创建出本地市场需要的目录结构了。

在 my-first-plug 目录的上层 再套一层新的目录，名为 `my-marketplace` ，作为本地市场的根目录。在根目录下创建 .claude-plugin 目录放置市场配置文件：

`mkdir -p my-marketplace/.claude-plugin`

新建 plugins 目录，把 my-first-plug 插件挪进去：

`mkdir -p my-marketplace/plugins   mv my-first-plug my-marketplace/plugins/`

将以下内容作为本地市场的配置文件 my-marketplace/.claude-plugin/marketplace.json ：

`{  "name": "my-plugins",  "owner": {    "name": "Your Name"     },  "plugins": [       {      "name": "my-first-plug",      "source": "./plugins/my-first-plugin",      "description": "Greet the user with a personalized message"       }     ]   }`

这里的 name 是市场标识符， owner 表示市场维护者信息， plugins 是可用插件列表，更多参数用法参考 创建和分发插件市场 。

值得一提的是插件列表配置，这里我保存的是上面创建好的本地插件，与本地市场在同一目录下，所以插件源 source 为插件的相对位置。这里也可以放远程仓库的插件，比如 GitHub 存储库：

`{  "name": "github-plugin",  "source": {    "source": "github",    "repo": "owner/plugin-repo"     }   }`

或者通过 url 指定 Git 存储库：

`{  "name": "git-plugin",  "source": {    "source": "url",    "url": "https://gitlab.com/team/plugin.git"     }   }`

启动 Claude Code ，然后添加市场并安装插件：

`/plugin marketplace add ./my-marketplace   /plugin install my-first-plugin@my-plugins`

以下是安装和尝试过程：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

#### 托管与市场分发

上面只是解决了如何在 Claude Code 中安装本地市场，以及在本地市场安装本地的插件。如果要与团队共享市场，官方推荐通过 GitHub 进行托管。方法很简单：

1. 1. 首先，把上面的 my-marketplace 推送到 GitHub 作为一个远程仓库，例如 wtt/my-marketplace；
    
2. 2. 团队内其他用户在自己本地的 Claude Code 执行 `/plugin marketplace add wtt/my-marketplace` 就可以添加市场。
    

### 5.5 总结

今天，我们一起重新认识了 Claude Code，将它从一个"工具"重新定义为一个"平台"。插件系统，正是 Claude Code 从"好用"到"无敌"的"点睛之笔"。它让你能够将自己的经验、团队的规范、常用的流程，全部封装成可复用、可分享的模块，为你打造一个独一无二、心意相通的伙伴。

---

## 6. 实用技巧

本章在你对 Claude Code 的扩展功能初步熟悉后，介绍一些真正能够投入生产的技巧。

### 6.1 Everything Claude Code

前面几节内容学习下来，你可能已经对 Claude Code 的一些主要能力有了感性的认识，但这仅仅是千里之行的第一步，离真正投入生产还有一定距离。那么，如何将 Claude Code 合理地投入到生产当中呢？

affaan-m/everything-claude-code 这个项目会告诉我们答案：这是 **Anthropic 黑客松冠军** 的生产级配置库。复用这套配置，可以快速搭建起一套高水平的 AI 辅助编程环境。 提供了从 TDD（测试驱动开发）到代码审查的完整自动化流程，通过配置文件强制 AI 遵守团队代码规范，大幅降低了 Review 的人工成本。

这个项目整体是一个 Claude Code 插件！可以直接安装插件，也可以手动拷贝里边的组件。作者推荐以插件形式安装：

`# 安装插件市场   /plugin marketplace add affaan-m/everything-claude-code      # 安装插件   ```shell   /plugin install everything-claude-code@everything-claude-code`

手动安装就按照 README.md 拉取代码，然后拷贝文件即可，这里不再赘述。

> Zed  
> 作者安利的 IDE Zed 非常适合搭配 Claude Code 使用，这款 IDE 是基于 Rust 开发的轻量级编辑器，看着不错，感兴趣的可以尝试一下。VSCode 也可以，看个人喜好吧。

### 6.2 NotebookLM Skills

NotebookLM 是由 Google 推出的目前最强的文档阅读器，notebooklm-skill 将其集成为一个专有的 Skill，丝滑接入Claude Code。

这个Skilk充分利用 Gemini 的长上下文能力，一口气吞下 50 多个文档，还能生成带引用的精准回答，它几乎不产生幻觉，只基于你上传的资料回答。Gemini的文档综述能力可以说是是业界天花板，它比那种基于向量检索的本地 RAG 聪明太多了，它能理解跨文档的关联。

安装非常简单：

`# 1. 创建 skill 的统一管理目录（上面 Claude Code 自动创建过的，可以跳过）   mkdir -p ~/.claude/skills      # 2. 克隆 GitHub 项目   cd ~/.claude/skills   git clone https://github.com/PleasePrompto/notebooklm-skill notebooklm`

这样一个 Skill 就安装成功了，启动 Claude Code 对话验证它能否识别到 Skill ：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

设置 NotebookLM 授权：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

Claude Code 在执行授权脚本过程中，会唤起一个 NotebookLM 登录窗口，登录你的 NotebookLM 成功就完成授权了。

通过浏览器登录 NotebookLM ，创建一个笔记本，复制上面的 URL ，将其安装到 Claude Code ：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

此时我通过浏览器上传一篇笔记到 NotebookLM 的笔记本，然后通过 Claude Code 提问关于文章的内容：

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E "null")

  

可以看到 Claude Code 提供的内容均来自于我的《Claude Code 入门指南》一文，包括特惠购买链接都是一致的。

---

## 7. 总结

本文我们深入探讨了 Claude Code 的六大高级技能，从基础的**记忆增强**（CLAUDE.md）到强大的**Skills** 系统，从智能的**Sub-Agent** 机制到开放的 **MCP** 协议，再到全能的 **Plug-In** 生态。每一个功能都在重新定义我们与 AI 协作的方式。

Claude Code 早已不再是一个简单的代码生成工具，而是一个完整的 AI 开发平台。它让每个开发者都能：

- • 通过 **CLAUDE.md** 让 AI 记住项目上下文和开发规范
    
- • 通过 **Skills** 将专业经验固化为可复用的工作流
    
- • 通过 **Sub-Agent** 实现任务的智能委派和并行处理
    
- • 通过 **MCP** 打通外部服务和数据源
    
- • 通过 **Plug-In** 构建和分享定制化的 AI 解决方案
    

我们正在见证一个编程范式的转变：从"人写代码"到"人描述意图，AI 实现代码"，再到"人定义工作流，AI 自主完成任务"。这不仅是效率的提升，更是工作方式的根本性变革。

展望未来，AI Agent 将会更加智能、更加自主、更加协作。随着 MCP 生态的繁荣、Plug-In 市场的成熟，以及更多人参与到 Skills 和 Sub-Agent 的开发中，我们将看到：

- • **更强的上下文理解能力**：AI 将能够理解更大规模、更复杂的代码库
    
- • **更自然的协作方式**：从命令行交互到语音、视频等多模态交互
    
- • **更丰富的生态系统**：各行各业的专业插件将如雨后春笋般涌现
    
- • **更低的门槛**：即使是非技术用户也能通过自然语言创建定制化的 AI 工具
    

但这并不意味着开发者会被取代，相反，开发者的角色将发生转变——从"代码编写者"变成"AI 训练师"和"工作流架构师"。我们的价值不再体现在敲击键盘的速度上，而体现在对问题的理解、对系统的设计、对 AI 的引导上。

**未来已来，只是分布尚不均匀。** 现在就开始使用 Claude Code，掌握这些高级技能，你就能在 AI 时代占据先机。让我们一起，用 AI 赋能创造力，用工具释放想象力，共同构建更智能、更高效的开发体验！

> **下一步行动建议：**
> 
> 1. 1. **实践出真知**：从本文的示例开始，动手创建你的第一个 Skill、第一个 Sub-Agent
>     
> 2. 2. **加入社区**：关注 Claude Code 官方文档和 GitHub 社区，了解最新的功能和最佳实践
>     
> 3. 3. **分享经验**：将你创建的优秀 Skills 和 Plugins 分享出来，帮助更多人提升效率
>     
> 4. 4. **持续学习**：AI 领域发展迅猛，保持学习热情，跟上技术演进的步伐
>     

让我们一起，在 AI 时代乘风破浪，探索无限可能！
