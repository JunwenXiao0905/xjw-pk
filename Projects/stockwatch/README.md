# stockwatch — ZCode 里的低调盯盘工具

免费行情接口(东方财富为主, 腾讯自动兜底), 纯 Python 标准库, 用 `.dataenv` 的 python 直接跑, 不依赖任何第三方包。

## 用法

### 1. 对话里查一把: `/stock` 斜杠命令(推荐, 全局可用)

在 ZCode 输入框里:

```
/stock                       # 查 watchlist.txt 里的自选
/stock 600519 贵州茅台        # 查指定代码(中文名/拼音也行)
/stock 板块                   # 行业板块涨幅榜(含涨跌家数、领涨股)
/stock 概念板块               # 概念板块榜
/stock 半导体板块             # 板块成分股涨幅榜
/stock 涨幅榜 / 跌幅榜        # 个股榜单(可说"前50")
/stock 看看大盘               # 自然语言也行
```

返回一张行情表 + 一句话点评, 看起来就是一次普通的 AI 对话。

### 2. 终端持续盯盘: watch.py

```bash
python watch.py                    # 盯自选, 每10秒原地刷新
python watch.py 600519 半导体      # 盯指定代码(名称/板块也行)
python watch.py --interval 5       # 5秒一刷
python watch.py --log              # 日志模式: 每次追加一行, 伪装成任务日志
```

Ctrl+C 退出。输出 80 列宽以内, 红涨绿跌。

### 3. 板块榜单 / 个股榜单: list.py

```bash
python list.py industry            # 行业板块涨幅榜
python list.py concept             # 概念板块涨幅榜
python list.py region              # 地域板块涨幅榜
python list.py up / down           # 个股涨幅榜 / 跌幅榜
python list.py amount / turnover   # 成交额榜 / 换手率榜
python list.py board 半导体         # 板块成分股(名称或 BK1036 代码)
python list.py up 50               # 前50
python list.py board 白酒 --md     # markdown 输出
```

### 4. 自定义分组: groups.txt(同花顺"分组"平替)

在 `groups.txt` 里用 `[组名]` 分段, 每行一个代码/中文名/板块:

```
[核心资产]
贵州茅台
宁德时代

[科技观察]
中芯国际
半导体      # 板块指数也能进组
```

```bash
python list.py groups              # 所有分组总览(平均涨跌幅/涨跌家数)
python list.py group 核心资产      # 单组明细
python quote.py @科技观察          # 一次查整组(和查多只股票一样)
python watch.py @核心资产          # 持续盯整组
```

对话里: `/stock 分组` 看总览, `/stock 分组 核心资产` 看明细。

### 5. K线图: kline.py

```bash
python kline.py 贵州茅台              # 终端ASCII蜡烛图(近60日, █涨 ▒跌)
python kline.py 600519 --png          # 图片版: MA5/10/20+成交量, 存 charts/
python kline.py BK1036 --png          # 板块指数也能画
python kline.py 贵州茅台 --week       # 周K (另有 --month)
python kline.py 600519 -n 90          # 指定根数
```

### 6. 一次性快照: quote.py

```bash
python quote.py                    # 表格
python quote.py 贵州茅台 BK1036     # 名称/板块代码混查
python quote.py --no-color         # 无颜色
python quote.py --md               # markdown 表格
```

## 自选列表

编辑 `watchlist.txt`, 每行一个代码, `#` 后面是注释:

```
1.000001   # 上证指数
0.399006   # 创业板指
600519     # 贵州茅台
00700      # 腾讯控股(港股)
AAPL       # 苹果(美股)
```

代码规则: A股/ETF 用 6 位数字; 港股 4-5 位; 美股字母; 指数用 `市场.代码`(1.000001 上证、0.399001 深成、0.399006 创业板、1.000688 科创50、100.HSI 恒指); 板块用 BK 代码(BK1036 半导体); 中文名/拼音会自动搜索解析(贵州茅台 / maotai, 优先匹配股票)。

注意: 6 位 `000001` 会被当成深市平安银行, 想查上证指数请写 `1.000001`; 查板块行情建议用 BK 代码(中文名可能搜到同名 ETF)。

## 文件

- `quote.py` — 快照 + 取数/渲染公共逻辑(名称解析、重试、腾讯兜底)
- `list.py` — 板块榜/个股榜/板块成分股/自定义分组
- `kline.py` — K线(终端ASCII蜡烛图 / matplotlib 图片)
- `watch.py` — 持续盯盘(原地刷新 / 日志模式)
- `watchlist.txt` — 默认自选(未分组的)
- `groups.txt` — 自定义分组定义
- `charts/` — K线图片输出目录
- `C:\Users\PC\.zcode\commands\stock.md` — `/stock` 全局命令(用户级, 所有会话可用)
