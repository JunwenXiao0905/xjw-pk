# Claude Code 入门指南看这篇就够了

原创 红薯的Java私房菜 Java一条人

 _2026年1月13日 21:17_ _天津_ 13人

> 最近救急帮朋友开发一个小程序，我对前端开发的知识储备有限，最近很多人也在尝试从 `Cursor` 转向 `Claude Code` ，我寻思以此为契机深度体验一下，没想到它的表现远超我的预期。  
> 这篇文章除了我的原创，还参考了 @oran_ge 等大神的文章，特此声明。

`Claude Code` 是基于 **`Anthropic Claude`** 模型的高级代码理解与生成组件，旨在帮助开发者快速完成代码撰写、调试和优化。与传统的代码补全工具不同，`Claude Code` 依托大语言模型的深度推理能力，不仅能理解复杂的代码上下文，还能进行多轮交互式编程。

`Claude Code` 自 `2025` 年 `2` 月发布预览版以来，历经 `IDE` 集成、`SDK` 发布、`MCP` 通信支持等关键迭代，逐步从工具进化为 **「智能代理」**。其核心优势在于深度上下文理解、多语言支持和宪法式 AI 安全机制，能显著提升开发效率并降低学习门槛。 所以，**`Claude Code` 虽然叫 `Code`，但它的功能绝对不止是写代码，而是一款真正意义上的通用****`Agent`**。

## 1. 基础准备

- • 科学上网环境
    
- • 安装最新版本的 Node.js（如果已安装，可以下载后直接覆盖安装）
    
- • Windows 用户还需要额外安装 Git for Windows
    

## 2. 正式安装 CC

在电脑上搜索 “终端” 然后打开，输入以下命令并回车：

`npm install -g @anthropic-ai/claude-code`

回车后命令下方有一个小方块在转动，就说明开始安装了，耐心等待大概 `1` 分钟左右就安装好了：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHWCckorvMnmQz5JicKpiaFBdjYQgPNG7ObE4RRWTRaWWYcGyUT5j4abBQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=0 "null")

  

然后在终端输入 `claude --version` 如果出现版本号，说明已经安装成功了：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHF3NX8J7g3iaVIUmMG1gDaVVe6LEibSNNeXnDB6xibj5NaeNdWgImWsCUw/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=1 "null")

  

## 3. 购买 CC 服务器的套餐

直接订阅 `CC` 官方的大模型套餐非常容易被封号，建议直接用国内的大模型，国内对 `CC` 支持比较好的模型有三个：`GLM 4.7`、`MiniMax M2.1`、`Kimi K2` 。  
我选择使用 `GLM 4.7`，可以直接在智普开放平台官方购买套餐，最近正是年终大促；也可以使用硅基流动，硅基流动不是订阅制，用多少充多少。（现在注册即送 `2000` 万 `Tokens` ，邀请好友赚 `2000` 万 `Tokens` —— 但历史的代金券是无法用于 `GLM-4.7` 模型的，我还不确定后续赠送的代金券能否使用）。

### 硅基流动

1. 1. 注册账号。访问**硅基流动官网**（https://cloud.siliconflow.cn/i/WjytiH1p），使用手机号注册。
    
2. 2. 新建 `API` 密钥。在账户管理 -> `API` 密钥页面（https://cloud.siliconflow.cn/me/account/ak），点击新建 `API` 密钥，建好密钥复制备用。
    
3. 3. 余额充值。硅基流动不是订阅制，用多少充多少。现在新建账号赠送 `2000` 万 `Tokens` ，如果是平时排查问题什么的够用一段时间了，但是历史的代金券是无法用于 `GLM-4.7` 模型的。
    

### 智普

1. 1. 注册账号。访问 **智普开放平台**（https://open.bigmodel.cn/），使用手机号注册。
    
2. 2. 新建 `API` 密钥。在个人中心页面，点击 `API Keys` （https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys），新建 `API Key`，复制备用。
    
3. 3. 订阅套餐。用了套餐之后，可以尽情使用，再也不用担心账号欠费背刺。现在正在搞跨年特惠，三个月 `54` 和不要钱一样。可以在这里购买（https://www.bigmodel.cn/glm-coding?ic=UPSLUNXO8X）
    

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHk2QaLFLnLVic81QWH8ccu8Mric7RqRFlFrM1saAjSbw0AJ86LXkcXQMA/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=2 "null")

  

如果硅基流动的代金券可以使用 `GLM-4.7` ，或者你愿意用代金券可用模型，那就用硅基流动试试手；如果是准备长期用那就无脑选择智普官方的年终大促吧！

## 4. 配置 CC 服务器

### 硅基流动

#### 方式一：一键安装及配置脚本

1. 1. 在终端中运行以下命令：
    

`bash -c "$(curl -fsSL https://sf-maas-uat-prod.oss-cn-shanghai.aliyuncs.com/sample/ccsf_v251226.sh)"`

1. 2. 提示输入 `API Key` 时，粘贴你的 `SiliconFlow API Key`
    

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHt8s87Zy6vVvgpGfEAgDEoo1ibdgyXfRd0ibCQyj9OzLUnr8sCDTtTP3g/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=3 "null")

  

1. 3. 提示选择模型时，使用方向键选择要在 `Claude Code` 中使用的模型，或选择自定义，从模型广场复制粘贴想用的模型名称：
    

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHb6YMfRFAO3JAwdULicibSFb6QsR3I9icgM8Uv0fvoKk3ORXUOFicsrWtQw/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=4 "null")

  

1. 4. 根据提示，复制相应命令并重启终端运行，应用配置：
    

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLH1JibI14auPR2oCHxOUomH7yAcfRscjmrY4YvYRvLVkXLtexzeiacpCyw/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=5 "null")

  

1. 5. 执行 claude 命令，进入 Claude Code 并使用
    

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLH9Om3D9n2iciaFVVXjY58dyPSqSdiaVU4ia2qlGGuD2Eibkkm7XlkKAwuNibQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=6 "null")

  

**切换模型使用**目前 `Claude Code` 并不支持添加多个自定义模型（`Custom Model`），您可以再次执行上述 `1～5` 步，选择并更新 `ANTHROPIC_MODEL` 环境变量的方式切换模型

#### 方式二：手动配置 Claude Code 环境变量

如果你想手动配置 `Claude Code` 的环境变量，可以在终端中运行下列命令：

`export ANTHROPIC_BASE_URL="https://api.siliconflow.cn/"   export ANTHROPIC_MODEL="moonshotai/Kimi-K2-Instruct-0905"    # 可以自行修改所需模型   export ANTHROPIC_API_KEY="YOUR_SiliconFlow_API_KEY"    # 请替换 API Key`

### 智普

在购买了智普的 `Coding` 套餐后，就可以配置使用了。这里要用到一个新的工具 `Coding Tool Helper` ，用这个工具可以方便地把 `GML` 的服务器配置导入到 `CC` 里。

1. 1. 在终端运行以下命令：
    

`npx @z_ai/coding-helper`

下方块大概转 `2` 分钟工具就安装好了。

2. 这时候你会看到一个亲切的中文界面，按照提示选择：  
界面语言选择中文  
编码套餐选择 `GLM 4.7`  
`API Key` 输入上面生成的 `API Key`

启动方式与硅基流动配置后一样，在终端输入 `claude` ，然后回车，`claude` 就启动成功了。

## 5. 基本功能

成功启动 `Claude Code` 之后就可以开始使用了，我们上面的大模型无论选择的是硅基流动还是智普，都支持中文问答，比如输入“你可以帮我解决什么问题呢？”正常回答如下所示：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHLUON6ZSS4icSrNQzpS8GcgHlk5Or0JOUIgc3hRkoeWrWllO8yrIY3Lw/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=7 "null")

  

使用硅基流动的朋友，如果账号里只有以前的代金券（不能用于 `GLM-4.7`），到这里可能会遇到一个问题：

`claude 配置硅基流动 API Error: 403 This model/service is available exclusively to paid users or organizations. Please top up to proceed.`

要么在硅基流动充值，要么就购买智普官方的大模型（硅基流动切换智普：我的实践是重新执行一遍硅基流动的初始化脚本，就是上面 `bash -c "$(curl ...` 的命令，然后再按照智普的安装过程重新执行一遍，然后提示模型不可用是，修改一下项目跟目录）～～

好了，接下来我们了解一下进入 `Claude Code` 一些常用的命令。比如，我们可以使用 `cost` 命令查看当前会话使用了多少费用或 `token` ：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHOcSibJcYWT1G8QaQst6iauMCnQKH91e1o5SQFIMrmhCiaf2ic1nDzlKVpg/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=8 "null")

  

（如果你使用的是硅基流动，这个命令是用不了的）

使用 `doctor` 命令查看当前 `Claude Code` 服务部署的健康情况：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHW6uVunz6jSvNMFicZcwsVoNkU6rlv7sqic8ShRCK24Yn9ibT00ju9alYA/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=9 "null")

  

使用 `clear` 命令清空当前会话的上下文记忆，避免历史对话干扰新的问题。比如，我先测试一下 `Claude Code` 的记忆能力：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHe42uW68MMScWEKIMYRiaX75vHzcIZINN9VEuic4rjNia8QYribp814KicEQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=10 "null")

  

执行 `clear` 命令后再检查：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHibiaRKGcXczxOMnzn5icesDzMW2U8E6wV8BXWUdicoEUV4qwZL0SHpNiajQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=11 "null")

  

它并不能记起 `clear` 之前的问题，说明 `clear` 已经生效了。

还可以使用 `compact` 命令将当前对话压缩并带到一个新的对话中：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHY5GcFLQQ7N7NTCXGIjpGcSL9NHv8OCr6DZHYEXDDwnr20F6RPqq1hQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=12 "null")

  

通过 `ctrl + o` 可以查看所有历史对话。其他命令我就不一一列举了，大家安装好之后可以挨个尝试一下，常用命令如下表所示：

|命令|解释|使用场景|
|---|---|---|
|/clear|清空上下文|如果需要重新开始，或者是担心历史对话会对新问题造成影响|
|/compact|压缩对话|重开对话，但是不希望丢掉之前的记忆|
|/cost|花费|当前会话话费的费用，订阅用户无所谓，API 用户（例如硅基流动）需要关注|
|/login /logout|登录登出|切换账号|
|/model|切换模型|只限于订阅了 Claude 套餐的用户进行切换，如果是硅基流动想换智普的用不了这个命令，需要从头开始初始化或手动修改配置。|
|/status|状态|查看当前 CC 的状态|
|/doctor|检测|检测 CC 的安装状态|

## 6. 项目开发

这部分我们围绕项目开发展开，讲解项目开发过程中 `Claude Code` 的一些典型用法和小技巧。

### 6.1. 核心模式

`Claude Code` 有三种工作模式：自动编辑模式、 `Plan` 模式和 `Yolo` 模式。

#### 自动编辑模式

自动编辑模式适合无需逐次确认的文件创建、修改场景。按下 `Shift + Tab` 即可开启，此时 `Claude` 会自动执行编辑操作，不过也可能需要我们在刚开始进行必要的确认，此后就会直接生成文件并修改，省去反复确认的时间：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHYb2bJdgn6brPz4tIGFKiafTQlWjAiakfTia4tniapMFKOzzQ1S2aw2PibRQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=13 "null")

  

> 任务执行过程中也是可以切换模式的，例如任务执行开始后你发现手动模式很麻烦，每一步都要自己确认，此时可以直接切换自动模式。

`GLM-4.7` 确实强大，上面的任务执行不到 `3` 分钟就帮我创建了一个非常美观的 `Web` 应用：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHsPVtnFaXh9rduu8H6wIYqoeqDDxEAwKWH4EvZJpQD92tk2CENiaicnJg/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=14 "null")

  

#### 计划模式

面对项目搭建或复杂问题时，用 `Shift + Tab` 两次开启 `plan` 模式。它会先梳理方案框架，自动生成技术栈、页面结构、适配方案等，确认后才会动手实现。如果不满意还可以重新规划，直到符合预期。示例如下：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHOtxFA1SeEhY7iaSUebdVEhPOQFtrtRI3ZOedg1GfmiaCON1FTYX5uBuQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=15 "null")

  

它会先扫描当前工作空间的目录结构，发现是一个空目录，然后我的需求又比较复杂，不确定因素比较多，此时它会产生一个需要我们补充信息的交互：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHm4WJGVWeAqVzRJfdstqjdriakKiaT5DAfOWGY2FebYRIKV0AdFgyXclw/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=16 "null")

  

每一项按需选择后，回车确认，每一项按左右键切换。所有项选择完毕，提交：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHjxcOO2FYnvNmE3aVMdAsPkJrNeCLXfsjvcrdPzv7ZYbHX5cJHuSzCw/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=17 "null")

  

提交后它就开始执行计划了，期间会花费一些时间，我这里大概经过了 `5min` 左右任务完成了，此时需要我们手动确认：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHgPVpfxYNruEVdc0313e64icBhhIe6Gt4WvvUxQPp1cdukUGRxDniazjQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=18 "null")

  

这里有 `3` 个选项：

1. 1. 自动接受计划
    
2. 2. 手动接受计划
    
3. 3. 告诉 `Claude` 哪里需要调整
    

我先选择第 `3` 项对方案进行了调整：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLH8Ss8JFMicibZ8unl0wrdMDNGu7VJy9Jc7rlicxO5cwIwMRC5H05XarqibA/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=19 "null")

  

待调整完成后，再选择第 `1` 项自动接受，`Claude` 会将生成的任务保存到指定的目录：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLH4dSyhsHUXNIhRl5du1ibs7AFaB5iciaBwiboxddkRpkPYDmrgoIg2hY9FA/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=20 "null")

  

> 注意：我们的计划最终并没有被保存到当前目录的 `plan.md` 文件，而是被保存到了 `.claude/plans` 目录下，这是 `Claude Code` 的默认行为，是为了更好地统一管理所有计划。

此时我们可以开始执行计划了，`Claude Code` 为我们将计划执行分为 `4` 步，这样逐步搭建能够避免很多 `BUG` 。这里我直接选择输入 “1” 并回车，开始执行第一步……

> 如果我们的计划比较简单，可能并没有这一步，选择了 【1. 自动接受计划】选项，Claude 生成计划后会直接自动执行计划。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLH10goTP7nQ1hZsAgtQgqK9feU3gPpmVJIdZUT5mXBHMHUG2nKfwVqdQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=21 "null")

  

完成第 `1` 步之后，我们可能想着接着让 `Claude` 完成第 `2` 步呗。不过 `Claude` 并不建议这样做，它的建议是先配置数据库，然后安装依赖，启动开发环境，将整个流程先运行起来。

接下来就是一个反复调试和对话的过程，直到复合我们的预期，然后再让它帮我们完成下一步，直到生成一个完整的小程序为止。这是我最终生成的小程序：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/cP7UCqK5cia1eoY7qQtsoibBkX2dU3TNLHCtVoic6QAulvFjhSDX4O2Jq74GbFiabYmnwuImiaegVglwAXMG6a0NrYQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=22 "null")

  

我会在后面的课程中与大家分享生成过程中遇到的一些问题，以及解决方案，大家可以一起探讨。

#### Yolo 模式

启动 `Claude` 时使用 `claude --dangerously-skip-permissions` 命令进入 `Yolo` 模式，此时 `Claude` 拥有更高的权限，可以直接执行更多操作，例如删除文档等。

`Yolo` 模式一般在重构代码、启动新项目或修复复杂 `bug` 时可能用到，需要注意安全，建议在沙箱环境使用。进入 `Yolo` 模式后，仍然可以使用 `Shiflt + Tab` 调整模式，灵活切换权限粒度。

## 7. 总结

本文主要讲解了 `Claude Code` 快速入门的相关内容，包括在国内如何选择套餐，如何安装 `CC` 以及基本功能的体验，同时通过几个典型的项目开发带大家快速熟悉 `Claude Code` 开发模式。对于开发者来说，掌握了这些内容还不太够，还需要了解记忆增强、`Sub-Agent` 和 `MCP` 等内容，这些内容我会在后面的进阶课程中继续探讨。
