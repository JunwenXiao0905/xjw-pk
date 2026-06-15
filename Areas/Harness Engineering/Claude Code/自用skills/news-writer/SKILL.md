---
name: News Writer
description: 按固定格式撰写【世界500强】系列新闻总结文。搜索→核实→成文→落地图数据，四步流程。适用于任何世界500强公司在某一国家/地区的产业布局分析。
read_when:
  - 撰写【世界500强】系列文章
  - 写企业产业布局分析文章
  - 需要按标准格式输出新闻总结
  - 数据中心/云区域/AI基础设施相关的产业分析
---

# News Writer — 【世界500强】系列文章写作流程

这是一个标准化的四步写作流程，用于撰写【世界500强】系列的企业产业布局分析文章。

---

## 〇、前置准备

### 参考已有文章

写作前先阅读同系列已有文章，确保格式一致：

```bash
cat "【世界500强】Microsoft AI产业-数据中心产业-马来西亚/【世界500强】Microsoft AI产业-数据中心产业-马来西亚.txt"
```

### 文章格式规范

| 要素 | 规范 |
|------|------|
| **标题** | `【世界500强】{公司名} {主题}-{地区}` |
| **导语** | 一段总起，概括该公司在该地区的战略意义 |
| **分节** | 一、核心布局 → 二、投资与时间线 → 三、客户生态 → 四、经济影响 → 五、扩展布局 |
| **链接格式** | 事实陈述段落后 `——https://...`（两个全角破折号 + URL） |
| **数据来源** | 所有信息必须从真实网页核实，不接受搜索摘要的二次转述 |
| **目录结构** | 每篇文章单独建文件夹：`【世界500强】{公司名} {主题}-{地区}/` |

---

## 一、研究阶段

### 1.1 初步搜索

先用搜索引擎了解目标公司在目标地区的基本布局：

```
搜索关键词模板：
  公司名 + 国家/地区 + 数据中心 / 投资 / 云区域
  公司名 + 国家/地区 + investment / data center / cloud region

中文搜索 → 内置 WebSearch
英文/国际 → Chrome MCP + Google 搜索
```

### 1.2 信息框架

确认需要覆盖的五个维度：

| 维度 | 核心问题 |
|------|---------|
| **核心布局** | 在哪里？规模多大？技术架构？ |
| **投资与时间线** | 投了多少钱？什么时候宣布/动工/上线？ |
| **客户生态** | 锚定客户是谁？覆盖哪些行业？ |
| **经济影响** | GDP贡献？就业岗位数量？技能培训？ |
| **扩展布局** | 是否有第二云区域/数据中心规划？ |

---

## 二、核实阶段

所有信息必须通过**真实网页**核实。不接受搜索摘要中的二次转述。

### 2.1 优先使用 Chrome DevTools MCP

```
navigate_page <URL>
take_snapshot          → 从无障碍树获取页面完整内容
evaluate_script "document.body.innerText.substring(0, 50000)"  → 直接拿全文
```

关键信息来源（按优先级）：
- **公司官方博客/新闻稿**（如 `googleblog.com`、`news.microsoft.com`）
- **权威行业媒体**（如 `datacenterdynamics.com`、`theedgemalaysia.com`）
- **官方云区域页面**（如 `cloud.google.com/about/locations`）
- **政府投资促进机构**（如 `mida.gov.my`）

### 2.2 Chrome MCP 被拦截 → CDP 降级

当 Chrome MCP 被 Cloudflare 等反爬机制拦截时，引导用户启动可调试 Chrome：

```
用户执行：
  Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--remote-debugging-port=9222 --user-data-dir=$env:TEMP\chrome-debug"

用户手动访问目标网址并完成验证后：
  1. curl http://127.0.0.1:9222/json/list → 确认页面已打开
  2. node CDP 脚本 → document.body.innerText → 获取页面全文
```

### 2.3 信息记录模板

核实每条信息时，记录来源 URL 和关键字段：

```
┌────────────────────────────────────────────────────┐
│  事实: 投资金额 20亿美元                          │
│  来源: https://malaysia.googleblog.com/...         │
│  原文: "US$2 billion investment"                   │
│  日期: Oct 1, 2024                                │
└────────────────────────────────────────────────────┘
```

---

## 三、写作阶段

### 3.1 文章结构

```
【世界500强】{公司名} {主题}-{地区}

{导语段落：一句话总起，概括该公司在该地区的战略意义}

一、核心布局
{数据中心位置、架构、技术特点、服务能力}
——https://...
{AI能力/特色服务}
——https://...

二、投资与时间线
{投资金额、宣布时间、动工时间、上线时间}
——https://...
{后续扩展投资}
——https://...

三、客户生态
{锚定客户、覆盖行业、合作伙伴}
——https://...

四、经济影响
{GDP贡献、就业岗位、技能培训/人才计划}
——https://...

五、扩展布局
{第二云区域/数据中心的位置、规模、特点}
——https://...
```

### 3.2 写作规范

- **链接位置**：每段事实陈述后紧跟 `——https://...`，独占一行
- **数据精确**：金额、人数、年份等数字必须与来源原文一致
- **对比视角**：适当与本系列其他公司做横向对比（如谷歌 vs 微软的差异化策略）
- **语言风格**：客观陈述，避免主观评价；用事实和数据支撑
- **信息来源**：同一段落有多个来源时，分行列出

### 3.3 与微软篇的格式对标检查清单

```
□ 标题格式一致： 【世界500强】{公司名} AI产业-数据中心产业-{地区}
□ 导语段存在
□ 分节编号：一、二、三、四、五
□ 链接格式：——https://...
□ 所有信息来自真实网页
□ 目录结构与微软篇一致
```

---

## 四、地图数据阶段

如果文章涉及地理信息，创建 GeoJSON 文件用于地图可视化。

### 4.1 参考格式

查看微软篇的 GeoJSON 格式：

```bash
cat "【世界500强】Microsoft AI产业-数据中心产业-马来西亚/microsoft_malaysia_west_cloud_region.geojson"
```

### 4.2 字段规范

```json
{
  "type": "FeatureCollection",
  "metadata": {
    "title": "...",
    "description": "...",
    "accuracy": "approximate — exact locations not publicly disclosed for security reasons",
    "crs": "WGS84 (EPSG:4326)"
  },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "",
        "name_zh": "",
        "type": "Cloud Region | Data Center | Planned",
        "status": "",
        "investment_usd": 0,
        "operator": ""
      },
      "geometry": {
        "type": "Point | Polygon",
        "coordinates": [...]
      }
    }
  ]
}
```

### 4.3 坐标获取

通过 WebSearch 获取目标地点的真实坐标（使用 Mapcarta 等来源），并标注精度说明。

### 4.4 文件存放

GeoJSON 文件和文章放在同一目录下：

```
【世界500强】{公司名} {主题}-{地区}/
├── 【世界500强】{公司名} {主题}-{地区}.txt
├── 【世界500强】{公司名} {主题}-{地区}.docx（可选）
└── {公司缩写}_{地区}_locations.geojson
```

---

## 五、文章示例参考

### 微软篇（已发布）

```
标题：【世界500强】Microsoft AI产业-数据中心产业-马来西亚
目录： 【世界500强】Microsoft AI产业-数据中心产业-马来西亚/
文件： ├── 【世界500强】Microsoft AI产业-数据中心产业-马来西亚.txt
       ├── 【世界500强】Microsoft AI产业-数据中心产业-马来西亚.docx
       ├── microsoft_malaysia_west_cloud_region.geojson
       ├── 马来西亚/（Shapefile 地图数据）
       └── 马来西亚.zip
```

### 谷歌篇（已发布）

```
标题：【世界500强】Google AI产业-数据中心产业-马来西亚
目录： 【世界500强】Google AI产业-数据中心产业-马来西亚/
文件： ├── 【世界500强】Google AI产业-数据中心产业-马来西亚.txt
       └── google_malaysia_data_center_locations.geojson（待创建）
```
