---
title: 盯盘工具-tradewatch手册
published: "false"
tags: [工具, 盯盘, tradewatch, 量化]
created: 2026-09-20
updated: 2026-09-20
summary: 交易决策系统tradewatch:竞价哨兵/尾盘六条筛选/盘后采集/Java API;周一作战时间线+命令速查
---

# tradewatch 交易决策系统

代码:`D:\projects\XJW-Personal Knowledge\Projects\tradewatch\`(独立git仓)。PG跑在docker容器`tradewatch-pg`(localhost:5433,库/用户/密码均tradewatch)。兄弟工具:[[盯盘工具-stockwatch]](实时行情问答,继续独立用)。

## 周一(9/21)作战时间线

| 时间 | 动作 | 谁来做 |
|---|---|---|
| 09:12 | 竞价哨兵+盘中监控+**形态监控**自动启动(后台无窗) | 计划任务tradewatch_mon_0912,**无需人工** |
| 09:15-9:25 | 昨日涨停票竞价预警:跌停附近/深低开/低开/大幅高开(≥5%),报警写`monitor/alerts/0921.log`;**五虎竞价采样**:9:20快照(识别虚假挂单)+9:25定型落`tiger_auction`表(名单=昨日涨停池∪信号票∪五虎池) | 自动 |
| 盘中全程 | **形态监控**(watchlist池5秒级):放量上攻/下杀、更高低点结构、**破位报警**、连续30分钟上升、创日内新高;watchlist.txt盘中改了即时生效 | 自动;想加票就编辑watchlist.txt |
| 14:31 | **尾盘六条全A筛选**,候选写入[[每日信息]]/0921/尾盘候选-机器生成.md+signal表 | 计划任务tradewatch_screener_1431 |
| 14:30-14:50 | 你的决策窗:**决策主干页(只放买)**:EXECUTE个股买入卡+ETF折价买入卡;备选只放数,点击跳支流页看细节 | **你** |
| **决策后30秒** | **记决策**(买了/放弃了都要记):`python tools\decision.py buy 002724 --qty 300 --note "六条全过"`(或skip/watch) | **你(新习惯,判断变数据)** |
| 15:06 | 盘后采集:快照+涨停池+池内日K入库+梯队名单生成 | 计划任务tradewatch_collect_1506 |
| **15:35** | **五虎晋级**:核实昨日预测→池子进出(断板两日移出/跌停/回撤15%)→十七因子打分→明日晋级面板md+`/tiger`页 | 计划任务tradewatch_tiger_1535(POST 8090,需Java服务在) |
| 15:45 | **多策略汇聚**:分级EXECUTE/FOCUS/WATCH→决策主干md(只放买) | 计划任务tradewatch_conf_1545(POST 8090,需Java服务在) |
| 15:55 | **异动归因素材包**:板块联动/梯队/量价/龙头/新闻五维→异动归因md | 计划任务tradewatch_attr_1555(POST 8090,需Java服务在) |
| 21:30 | ETF溢价预测检验(永赢589420>国泰589260) | ZCode定时(会话内) |
| 21:45 | ETF净值入库+全市场溢价表 | 计划任务tradewatch_etf_2145 |
| **21:50** | **自动复盘**:回填每个信号的T+1/3/5收益与回撤;已复盘≥5条自动生成`每日信息/MMDD/策略记分-机器生成.md`(按策略胜率+买vs放弃对照) | 计划任务tradewatch_review_2150(**每日循环**) |

**人工动作只有两个:14:30决策 + 决策后30秒记账。**其余全自动。

## 手动命令速查(全在项目根目录)

```bash
python tools/tiger_backfill.py 20260923  # 晚开机补救:分钟数据回放补当日竞价与触板/开板事件(缺省=今天)
python monitor/mon.py auction            # 竞价哨兵单跑(等待到9:15)
python monitor/mon.py structure          # 形态监控单跑(watchlist池,5秒级)
python monitor/mon.py intraday           # 盘中异动单跑
python screener/screener.py              # 尾盘六条(14:30后)
python tools/decision.py buy 002724 --qty 300 --note "理由"   # 记一笔买入决策
python tools/decision.py skip 002724 --note "放弃理由"        # 记一笔放弃(同样重要!)
python tools/decision.py list --days 3   # 近期决策一览+未决策信号提醒
python tools/review.py --dry-run         # 预览今晚将回填什么
python tools/stats.py                    # 策略胜率报表(控制台)
python collector/collector.py spot       # 全A快照入库
python collector/collector.py pools 20260921   # 涨停/炸板池入库
python collector/collector.py etf        # ETF行情+净值+溢价
python probe/zt_pool_probe.py 20260921 --save  # 梯队名单markdown
# Java API(可选):cd server && java -jar target/tradewatch-server-0.1.0.jar
#   GET localhost:8090/api/ladder | /api/signals | /api/etf/premium | /api/health
```

## 输出位置

- **知识库桥**:每日信息/MMDD/下`涨停梯队-机器生成.md`、`尾盘候选-机器生成.md`、`决策主干-机器生成.md`(只放买)、`异动归因-机器生成.md`(五维素材)
- 报警:`monitor/alerts/MMDD.log` | 异动流:`monitor/feed/MMDD.jsonl` | 计划任务日志:`ops/logs/*.log`
- **看板**:浏览器开`localhost:5173`(前端dev)/`localhost:8090`(Java API)。页面:决策主干(只放买)/支流信号(决策链漏斗+为什么按钮)/ETF全景/涨停梯队/监控中心/任务中心
- 数据资产:PG库(signal/decision/review表是记分本,**只增不删**)

## 已知坑(2026-09-20实测沉淀)

1. **东财WAF封Python指纹**:push2/push2his对urllib断连→脚本自动走curl.exe;更狠的是**IP级临时封禁**(触发过,持续约2小时)→快照降级push2delay(盘中滞后约15分钟,终端有警告),分时降级腾讯接口。看到警告别慌,是降级在工作。
2. **涨停池历史仅约15个交易日**:条件2"涨停基因"当前按可得窗口执行;collector每天落库board_event后窗口自动扩到30日。
3. **日K历史接口限流狠**(IP小时配额):kline-pool是增量设计,断了隔1小时重跑即自动补齐。
4. `start_mon.bat`**必须保持GBK编码**(cmd中文坑),用编辑器改别存成UTF-8。
5. ~~`ops/run_collect.bat`里写死了日期~~ **已修复**:bat经PG max(date)自解析交易日,周末拒写。
6. **schtasks路径带空格必须加引号**(2026-09-21首跑翻车根因):`XJW-Personal Knowledge`里的空格会把命令劈成`D:\projects\XJW-Personal`+参数,任务报0x80070002"找不到文件"。6个任务全部重建过,正确写法:`schtasks /Create ... /TR "\"D:\...\ops\run_xx.bat\""`。新建任务后**必须**`schtasks /Query /TN xx /XML`核对`<Command>`是完整路径。
7. **计划任务默认电池模式不启动**(DisallowStartIfOnBatteries):笔记本电池供电时15:35等任务不会触发;台式机无影响,用笔记本跑要在电源选项改或任务XML去掉该约束。
8. **五虎重放约束**:tiger任务只允许重跑最新已执行日或更晚(显式传更早日期会被拒,防止幽灵周期污染池子档案);历史缺口由任务自动按时间正序回补。竞价修正"维持"档有意放宽为"定型涨幅≥3%即维持"(含8%~未顶板的20cm票,高开不惩罚)。

## 计划任务管理

```
schtasks /Query /TN tradewatch_mon_0912        # 查状态
schtasks /Delete /TN tradewatch_mon_0912 /F    # 删除
```
现有8个:mon_0912(哨兵)/screener_1431/collect_1506/conf_1545/attr_1555/etf_2145/review_2150/kline_2330。conf与attr两个是POST 8090的Java端点,**依赖Java服务存活**(重启机器后需手动起:见"手动命令速查"末行)。

## 切换方案(Java收编Python,双轨验证后执行)

当前状态:**Python值班**(6个计划任务跑py脚本) + **Java全量对等待命**(批处理7任务+哨兵三引擎均已移植且彩排/对等验收通过,`jobs.enabled=false`、`monitor.enabled=false`默认关)。建议周二~周四观察双轨数据逐日一致后,周四晚切换:

1. 停Python值班:`schtasks /Delete /TN tradewatch_mon_0912 /F`(及screener_1431/collect_1506/etf_2145/review_2150;review_2150是DAILY需删)
2. 删中转任务conf_1545/attr_1555(Java侧cron 15:45/15:55将接管)
3. `server/src/main/resources/application.yml`: `tradewatch.jobs.enabled: true` + `tradewatch.monitor.enabled: true`
4. 重启jar;交易日早上 `POST /api/monitor/start?mode=all`(monitor即便enabled也不自启,REST显式启动)
5. 切换后Python执行层冻结退役;Python长期只做研究轨(pandas/backtrader/qlib连PG)
> ⚠️开启jobs.enabled前必须先删Python任务——两边cron同刻,会双跑(P1-5已加互斥,但仍会浪费请求配额)

## 下一步(一期-2候选)

- **盘中侧支流**:前龙头超跌反转(金健米业式)/快速拉伸速率检测/新股实时雷达进monitor
- 五虎战法(A2)+均线回踩缩量(A3)进strategy框架;F事件词典API
- 全市场日K回补(steady_climb目前只有池内39只的K线)
- review表回填(T+1/3/5自动补收益→策略胜率)——已上线,持续积累分母
