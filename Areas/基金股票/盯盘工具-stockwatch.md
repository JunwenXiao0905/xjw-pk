---
title: 盯盘工具-stockwatch
published: "false"
tags: [工具, 盯盘, stockwatch]
created: 2026-09-03
updated: 2026-09-03
summary: ZCode里的低调盯盘工具:/stock对话查行情、watch.py持续盯盘、板块轮动、K线、自定义分组
---

# 盯盘工具 stockwatch

解决"同花顺都永不顺"+上班看盘太张扬的问题。装在 ZCode 里,免费接口(东财为主,腾讯/新浪自动兜底),数据实时。

- 代码位置:`C:\Users\PC\ZCodeProject\stockwatch\`
- 依赖:无(纯Python标准库,matplotlib仅K线图片用)
- 详情:见该目录 README.md

## 一、对话方式(ZCode 输入框)

| 输入 | 得到 |
|---|---|
| `/stock` | 默认自选(watchlist.txt) |
| `/stock 600519` / `/stock 贵州茅台` | 个股行情(名称/拼音/代码都行) |
| `/stock 159608` | ETF实时价(比支付宝净值快,≈同花顺看到的) |
| `/stock 板块` / `/stock 概念板块` | 板块涨幅榜(涨跌家数+领涨股) |
| `/stock 半导体板块` | 板块成分股 |
| `/stock 板块轮动` | 今日/5日/20日对比+信号(高位回落/低位回升) |
| `/stock 涨幅榜 前50` / 跌幅榜/成交额榜/换手率榜 | 个股榜单 |
| `/stock 茅台的K线` | 终端ASCII蜡烛图;要图片版说"要图片" |
| `/stock 分组` / `/stock 分组 组名` | 自定义分组总览/明细 |
| `/stock 019875这种基金代码` | 查不到(基金净值不在行情接口),要看对应ETF |

## 二、终端方式

```bash
S=C:/Users/PC/ZCodeProject/stockwatch
python $S/watch.py 159608          # 持续盯,10秒原地刷新,Ctrl+C停
python $S/watch.py --log           # 日志模式,更像在跑任务,最低调
python $S/kline.py 515880 --png    # K线图片(MA5/10/20+成交量),存charts/
python $S/kline.py 515880 --week   # 周K,看大趋势
```

## 三、文件与分组

- `watchlist.txt`:默认自选,每行一个(代码/名称/BK板块)
- `groups.txt`:自定义分组(类似同花顺分组),`[组名]`+每行一个;已有:核心资产、科技观察、广发稀有金属ETF联接C(83只成分,含权重)
- 用法:`/stock 分组 核心资产`、`python $S/quote.py @科技观察`、`python $S/watch.py @核心资产`
- `boards_cache.json`/`resolve_cache.json`:自动缓存,别删

## 四、和基金池的联动

[[ETF股票池]] 持有三只 → 盯对应ETF即可:159608(稀有金属)、513120(港股创新药)、半导体ETF(待核code)。
想看基金持仓明细/领涨领跌 → 用现成分组或 `/stock 分组 广发稀有金属ETF联接C`。

## 五、已知坑

- 东财接口对高频请求限流,工具已自动重试+切腾讯/新浪;连续查询失败=限流中,过几分钟自愈
- 中文名可能搜到同名ETF(如"半导体"→半导体ETF国联安),板块请用BK代码(半导体BK1036)
- 6位`000001`是平安银行,上证指数要写`1.000001`
