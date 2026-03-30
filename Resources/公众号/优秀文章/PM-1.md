# Claude Code + PM Skills：敏捷开发中的需求管理神器

原创 Lex 陆徐洲 硅基鹿鸣

 _2026年3月18日 07:50_ _英国_ 88人

大家好，我是陆徐洲。

我们团队五个人，前段时间做了一个检验科的实时质控系统，马上要上线商用。我一翻文档，发现事情不对。

代码写完了，回头翻需求文档，8份说明书拼不出一个完整的功能描述。

6种回归模型、4套参数推荐策略都实现了，文档覆盖度只有20%。产品经理留下一句："这块你们理解了就行。"

8份docx散落各处，互相没有关联。客户演示后的21条修改需求从没回写到说明书里。算法层的核心模块，压根没有需求文档。业务逻辑细节全在微信群聊里。

原因也简单。PM对算法不了解，这块功能我自己设计的，前端对接也是我直接沟通。写代码的时候哪有心思写文档。

眼看要上线了，验收标准在哪？测试用例依据是什么？后面换个人接手怎么办？

我就想试试，能不能用Claude Code从代码和聊天记录里，逆向还原出一份完整的PRD。

然后找到了GitHub上一个叫**Product-Manager-Skills**的开源项目，今年2月份新发布的项目，目前已经2k star了。

46个产品经理技能模板，6个命令工作流，给AI agent用的。关键是它不是填模板的工具，是个**追问框架**，后面会细说。

先说怎么开始的。

所有素材一股脑丢给Claude Code。8份需求说明书、微信群聊、UI截图、行业文献PDF，加上Python计算引擎的源码，四个微服务几千行。图片直接看，PDF直接读，代码直接分析，这块不用多说。

Claude Code读完之后，没有直接写PRD。它输出了三个文件。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/CLTbQqd0iauL89VdaicrxibAymMrWqLaBuRibIaCJWbWVLh3WRHxVF3iar3mFLwoicOOxvs3AAM5CPaOqiaYZ6MicjUJElYNIovbEGCXUCfDQg2VFuU/640?wx_fmt=png&from=appmsg&wxfrom=13&tp=wxpic#imgIndex=0)

一份需求确认清单，7个模块50多个功能点，每条标了信息来源和置信度。一份代码和文档的差异分析。一份从聊天记录里扒出来的Bug清单。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/CLTbQqd0iauKd6hyaLob28CfIFicbaqib7MW2OCndbr8GiaicBw6Uw79RMmwWDHbT6pIGm8hLp6uCJXsrxL8ia2OrDssxojqZPVdxGvicB8c4qsEl8/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1#imgIndex=1)

差异分析里有意思的是，它找到了14项代码有但文档没提的功能。回归分析最典型，代码实现了6种模型还带自动选择，文档一个字没有。5处不同来源之间的逻辑矛盾，15处信息空白。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

有人可能会问，AI整理出来的东西能信吗？

我的做法是不让它直接出PRD，而是出"待确认清单"。每条结论标信息来源和置信度，高置信度的是代码加文档双重验证，低的标红提醒要人工确认。

AI整理，人拍板。这个顺序不能反。

顺着这个确认清单，就到了我觉得最有用的环节——**苏格拉底式追问**。

PM Skills里有个技能叫problem-statement，框架是"I am / Trying to / But / Because / Which makes me feel"，强制从用户视角定义问题。我把它和确认清单结合，让Claude Code按模块对我提问。先问覆盖度最低的，回归分析20%，智能推荐40%，监控报警60%。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

针对他提出的问题依次给出回答。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

4轮下来，20个问题。有几个我自己都没意识到文档缺了，比如"忽略前20个报警点是固定的还是可配置的"，这细节只在我脑子里，代码写死了20，文档没提过。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

20个问题，整体覆盖度从55%拉到了85%。回归分析从20%到85%，智能推荐40%到85%，监控报警60%到90%。

确认清单补齐了，开始生成PRD。

PM Skills有个write-prd命令，链式调用5个技能。problem-statement定义问题，proto-persona建用户画像，prd-development走8个Phase生成主体，user-story给每个功能点加Gherkin验收标准。Given前置条件，When用户操作，Then期望结果，测试用例直接从这出。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

初稿出来后我又改了几处。比如回归分析在方案设计页面不需要单独Tab和图表，只要模型名称加启用开关就够了。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

最终PRD是1800多行，合并了原来8份说明书，补上了从没写过的算法层文档，82张原型图。半天搞定，人工做怎么也得一周。

![图片](data:image/svg+xml,%3C%3Fxml%20version='1.0'%20encoding='UTF-8'%3F%3E%3Csvg%20width='1px'%20height='1px'%20viewBox='0%200%201%201'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%20fill-opacity='0'%3E%3Cg%20transform='translate\(-249.000000,%20-126.000000\)'%20fill='%23FFFFFF'%3E%3Crect%20x='249'%20y='126'%20width='1'%20height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

后续维护的话，建议接ChatPRD的MCP协议，PRD在IDE里实时可查，改了自动同步。我们文档崩塌的根源就是迭代太快文档跟不上，更新成本降到零这个循环才能断开。

简单总结一下。

这次实践下来我最大的感受是，**AI最大的价值不是帮你写文档，是帮你发现哪些地方你以为想清楚了其实没有**。PM Skills的追问框架把模糊的"需求不清晰"变成了可以逐条回答是或否的问题。不需要PM多强，能回答问题就行。大厂靠人和制度解决的事，中小团队靠AI一样能兜住。

我是陆徐洲，一家 LIMS 公司的 AI 算法负责人。关注我，让我们一起在 AI 落地实践的路上，走得更远。

  

AI赋能千行百业 · 目录

上一篇13 门免费课 + 用量翻倍，Anthropic 这波操作值得每个人关注

阅读 6022

​

[](javacript:;)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/5GQcZ0zXKJSJCia9UR1hJWEVj43pic5CYSjY17fXck587gcEz1oIW92YHIHB6PQsGPlND392NoMXQzTicXSpzMb6A/300?wx_fmt=png&wxfrom=18)

硅基鹿鸣

关注

71

905

40

10

![](https://wx.qlogo.cn/mmopen/duc2TvpEgSRKrwicE9icxabloW41Md1WmBUBEibUbgoicG4wQiaIq4VxA3icgwOKGts9laXwJVF6CxRERrnbdmuvkGeCuIIBkT5nf28K25Ikkt9zWACAQeAvN0iaHrHDI3Jje6N/96)

复制搜一搜

复制搜一搜

暂无评论