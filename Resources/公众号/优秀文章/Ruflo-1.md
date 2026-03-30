# 狂揽 21.6k Star！Claude Code多智能体编排神器Ruflo开源，Token成本直降75%

原创 关注AI开源项目 智猩猩AI

 _2026年3月19日 12:18_ _北京_ 5人

![图片](https://mmbiz.qpic.cn/mmbiz_png/zJVQUll3YIYicar6GDHC64VMUEGATOTBxODbdeUVqOcHEHXICREMnwnAMFDIqxWPeaTcTibg1JxrSI0uFXqmkpPCcNKszoYDDdJpHkFgP0Dsw/640?wx_fmt=png&from=appmsg&wxfrom=13&tp=wxpic#imgIndex=0)

_4月22日，**CLI-Anything/Nanobot团队负责人黄超老师，HiClaw项目发起人、阿里云智能高级解决方案架构师付宇轩**等5位嘉宾将在OpenClaw技术研讨会带来主题报告。_

  

智猩猩AI整理

编辑：没方

  

在AI辅助开发时代，**“单兵作战”**根本扛不住软件工程的真实战场。

  

一个动辄上万行代码的企业级应用，Claude Code 却经常“**失忆**”，上下文稍长就丢掉关键信息，前后逻辑断裂。

  

明明只是格式调整、文档整理这种简单任务，却持续调用昂贵的 **Opus** 模型，造成惊人的 token 成本浪费。

  

更要命的是，多环节开发任务需要人工反复切换模型角色，每切换一次就得重新解释上下文、调整提示词，思路被打断，效率直接腰斩。

  

而今天要给大家介绍的开源项目 **Ruflo（前名 Claude Flow） 正精准破解这些难题。Ruflo** ****是一个面向 Claude Code 的多智能体编排框架**，让单打独斗的大模型变成分工协作的智能体团队。能从每一次任务执行中自主学习，留存成功的执行模式，避免灾难性遗忘问题。还能将任务智能分配至各领域相应智能体处理，API 调用成本可降低高达 75%，Claude 能力上限提升 2.5 倍。 该项目在Github上已收获 21.6k Stars。**

![图片](https://mmbiz.qpic.cn/mmbiz_png/zJVQUll3YIZBU95xezl6kSWn4qwialP4r5Owiabnp1yebSMJEtg1Xc7NRSExzguukI8JgWVCa4biaaiaKb1efyuSeIzeAMnEqtGd3IGyaljIL8M/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=1)

  

- 项目链接：  
    
    https://github.com/ruvnet/ruflo
    
      
    

_**01**_

**项目介绍  
**

  

Ruflo 是专为 Claude Code 量身打造的原生多智能体编排框架，通过蜂群式（Hive Mind）架构协调多个智能体完成软件开发任务。采用 Queen-Worker 层级调度，并支持多种共识算法自动解决多智能体协作中的冲突。

  

Ruflo 内置 **60+专业智能体**，覆盖编码、测试、安全审计、架构设计、文档撰写等全开发链路，像真实团队一样各司其职。此外，Ruflo 通过 **MCP 协议**无缝接入 Claude Code，用户不用离开聊天界面，就能直接召唤蜂群（多个专业智能体组成）、初始化任务、检索记忆，整个开发流程非常丝滑，还能一键解锁 170+ 专业工具。

  

****针对大模型的 “失忆” 问题，Ruflo 内置 RuVector 持久化向量记忆库，基于 PostgreSQL 与 HNSW 算法实现高速向量搜索。还结合了自进化神经架构 SONA 与 EWC++ 防遗忘技术，****Ruflo**** 会自动提炼并存储任务经验，在后续相似需求中实现记忆复用，持续提升协作效果。****

  

性能方面，Ruflo 设计了三级智能路由降低 API 成本。简单格式调整等任务用 WASM 本地秒处理；中等任务交给轻量模型；只有真正复杂的部分才调用 Opus 等高端模型。

  

_**02**_

**使用**

  

环境要求：Node.js 20+（必需）npm 9+ /pnpm/bun（ 包管理器）。

  

（1）安装 Claude Code

  

```
# 1. 全局安装 Claude Code
```

  

（2）npm/npx 安装：

  

```
# 快速启动（无需提前安装）
```

  

（3）基本使用

  

```
# 初始化项目
```

  

（4）升级

  

```
# 更新 helpers 和 statusline（保留你的数据）
```

  

（5）Claude Code MCP 集成

  

```
# 将 ruflo 添加为 Claude Code 的 MCP 服务器
```

  

添加完成后，Claude Code 可直接使用 Ruflo 的全部 175+ MCP 工具，例如：

  

- swarm_init - 初始化智能体蜂群
    
- agent_spawn - 生成专业智能体
    
- memory_search - 使用 HNSW 向量搜索模式
    
- hooks_route - 智能任务路由
    
- 以及 170+ 其他工具
    

  

_**03**_

**群体智能的涌现  
**

  

Ruflo正在解锁的，正是多智能体系统的核心价值——群体智能的涌现。这不仅是其区别于其他AI开发工具的核心竞争力，更精准契合了2026年“从单点应用到群体协同”的产业趋势。单个智能体的能力终究受限于模型边界，但多智能体群体通过分工协作、经验复用、冲突自解，正在突破这一物理极限。

**END**

  

✦

✦

**大会推荐**

✦

_4月21-22日，智猩猩主办的**2026中国生成式AI大会**将举行，设有开幕式，AI算力基础设施、大模型、AI智能体3大专题论坛，以及OpenClaw、LLM强化学习、大模型记忆等6场技术研讨会。其中，**OpenClaw最强轻量平替nanobot团队负责人黄超、Claw-R1项目负责人程明月**等学者专家将带来报告分享。_

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

  

✦

✦

**入群申请**

✦

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

  

**智猩猩矩阵号各专所长，点击名片关注**

![](http://mmbiz.qpic.cn/sz_mmbiz_png/DPAHibibAl3vRucibjtBRsFa4OaXd2L5oNOTxyXO8G9fC42Ic8lYEySicttZIQNhNWem4xr9QHRcs7KoWUfsAf2Yvg/300?wx_fmt=png&wxfrom=19)

**智猩猩AI**

关注大模型驱动的AI浪潮，报道AI研究前沿与产品开发。

761篇原创内容

公众号

  

![](http://mmbiz.qpic.cn/sz_mmbiz_png/ZTOmVNZ2cBPaHDdDLsdMwHibU5rSWcp1DPvj1T0HLrOQ2as4lNXeREdoeB8bEL40MuicJSagwX6c82HibxmHImKdg/300?wx_fmt=png&wxfrom=19)

**智猩猩芯算**

关注AI芯片的星辰大海，报道智算的黄金篇章

109篇原创内容

公众号

AI开源项目 · 目录

上一篇暴涨15.8k Stars！港大开源命令行神器CLI-Anything，让任意软件一键接入OpenClaw/Claude Code

阅读 6129

​

[](javacript:;)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/DPAHibibAl3vRucibjtBRsFa4OaXd2L5oNOTxyXO8G9fC42Ic8lYEySicttZIQNhNWem4xr9QHRcs7KoWUfsAf2Yvg/300?wx_fmt=png&wxfrom=18)

智猩猩AI

关注

134

1089

93

4

![](https://wx.qlogo.cn/mmopen/duc2TvpEgSRKrwicE9icxabloW41Md1WmBUBEibUbgoicG4wQiaIq4VxA3icgwOKGts9laXwJVF6CxRERrnbdmuvkGeCuIIBkT5nf28K25Ikkt9zWACAQeAvN0iaHrHDI3Jje6N/96)

复制搜一搜

复制搜一搜

暂无评论