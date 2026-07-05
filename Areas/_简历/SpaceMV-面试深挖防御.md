# SpaceMV-CoAI-Map 简历深挖防御手册

> 用途：简历每条 bullet 的面试深挖准备。结构统一为「概念补课 → 实际怎么跑 → 追问与答 → 风险点」。
> 原则：**讲真话**，跟代码对得上；记不住的就说"记不太清"，别硬编。

---

## 第 1 条 · 异步空间数据接入与处理

> 简历原文：主导设计 BullMQ + Redis 异步接入管线，以一套 7 态状态机统一承接批量文件导入与实时 AIS/ADS-B 轨迹同步两类入库场景，内置幂等去重与失败重试。

### 一、概念补课

- **BullMQ 是什么**：Node.js/TS 生态最主流的**任务队列库**，跑在 Redis 上。把"任务(job)"丢进队列，后台 **worker** 进程异步取出执行。用途：耗时操作不卡主请求、定时任务、失败自动重试、削峰。
- **为什么 BullMQ + Redis 一对**：BullMQ 是"库"，Redis 是它存任务的"仓库"。用 Redis 的 list/hash/有序集合存任务队列、状态、延迟任务、重试次数。
- **餐厅类比**：顾客点单(API 收到上传)不等厨师做完，订单夹到队列；厨师(worker)按序取单做；顾客不用干等 → 对应 HTTP 立即返回。
- **异步管线解决什么**：GIS 文件解析+校验+入库要几十秒到几分钟。同步会 HTTP 挂死、前端超时、连接占满。异步 → API 立刻返回"处理中"，前端轮询进度。
- **状态机**：任务分阶段(解析→校验→入库→索引)，每步推进/可能失败，进度显式写进 DB，前端才能显示"25% 解析中"。7 态：`PENDING→PARSING→VALIDATING→IMPORTING→INDEXING→SUCCESS/FAILED`，映射 0/25/50/75/90/100/-1。
- **幂等去重**：同一任务可能被重复触发(用户连点)。用 `jobId = gis-${versionId}` 当唯一标识，BullMQ 对相同 jobId 的任务**不重复创建**。

### 二、实际怎么跑的

1. API 收上传 → 在 `gis-ingest` 队列入 job(versionId 当 jobId) → HTTP 立即返回。
2. `GisProcessor`(worker) 取 job → 选适配器 → 解析 → 校验 → **100 条一批写 PostGIS** → 建索引 → 清旧版本，每步推进状态机、写回 DB。
3. 前端轮询 `GET /datasets/versions/:id/status` 拿状态+进度。
4. 实时 AIS/ADS-B 走另一条 `external-data-sync` 队列，用 BullMQ **repeatable job**(定时) 按 cron 拉。
5. 两条队列共用同一套 BullMQ+Redis 底座 → "统一承接两类场景"。

### 三、追问与答

- **为什么选 BullMQ？** Node 生态主流、Redis 后端快、原生支持重试/延迟/定时/优先级、TS 支持好、有 Bull Board 可视化。RabbitMQ/Kafka 要单独部署 broker 更重，体量用不上；纯 DB 轮询吞吐低且得自己造重试。
- **BullMQ 底层怎么用 Redis？** 等待中任务用 list(LPUSH/BRPOP 消费)，任务详情存 hash，延迟/定时任务用**有序集合**按到期时间排、到期搬进等待队列，worker 用 BRPOP 阻塞等。记不住就说"大致 list 消费、有序集合做延迟调度"。
- **为什么异步不同步？** 解析入库耗时不定(大 shapefile 几十秒)，同步占死 HTTP、前端超时、并发打满线程。
- **7 个状态会不会太多？** 每个对应管线一个真实阶段+进度百分比，拆细是为了前端精确反馈。能合并但粒度粗。
- **幂等具体怎么做？** 数据集版本 ID 当 jobId，相同 jobId 不重复创建，同版本重复触发只跑一次。
- **重试会不会重复入库？** 不会。幂等 jobId + 每阶段按版本先清后写，失败重试从干净状态重来。
- **两条队列为什么分开？** 文件导入是一次性长任务，实时源是高频定时短任务，分开避免互相阻塞；同一套底座所以统一。

### 四、风险点

- **Redis 数据结构细节**：记不住就说"大致 list 消费、有序集合做延迟调度"，别硬编。
- **重试参数**：3 次、指数退避起始 1 秒(attempts:3, backoff exponential 1000ms)。
- **并发度**：worker concurrency=2，理由"控制对 PostGIS 的并发写压力"。
- **退路**：措辞可从"BullMQ"软化为"基于 Redis 的任务队列(BullMQ)"，主语放"队列模式"降低被追库细节的风险。

---

## 第 2 条 · 空间数据模型、矢量瓦片与实时编辑

> 简历原文：基于 PostGIS 设计 12 张表的空间数据模型，构建免离线预切的动态矢量瓦片服务，并解决跨瓦片标注重复合并、瓦片属性类型漂移两个渲染正确性难题；前端实现要素实时编辑（几何顶点增删 / 平移、属性修改与字段计算），编辑回写后自动失效并重载相关瓦片、保证即时可见。

### 一、概念补课

- **PostGIS**：PostgreSQL 的空间扩展，能存几何、做空间查询、生成瓦片。几何列是 PostGIS 的 geometry 类型，坐标系 EPSG:4326(WGS84 经纬度)。
- **12 张表 / 三层血缘**：核心是 `Dataset`(数据集) → `DatasetVersion`(版本，每次导入一个，带状态机字段) → `GisFeature`(单条空间要素：geometry + properties JSON)。其余：Project/ProjectState(项目与地图视图态)、ValidationReport(校验报告)、TileSource(瓦片源凭据)、WhiteboardDoc 等。被问"哪些表"就答核心三层 + 周边业务表。
- **矢量瓦片 MVT(Mapbox Vector Tile)**：把矢量数据按金字塔切成 z/x/y 小块 protobuf 二进制，浏览器只下载视口内瓦片。大数据集靠它——全量 GeoJSON 几十万要素浏览器会卡死。
- **动态生成 vs 离线预切**：传统是提前切好存盘(预切)，费存储、数据变了要重切。我们用 PostGIS `ST_AsMVT` **每次请求实时算一个瓦片**：不存预切文件、数据更新立刻生效、省存储。代价是每次算(靠 bbox 预过滤 + 空间索引扛)。
- **难题1·跨瓦片标注重复合并**：一个大省横跨多瓦片，若每瓦片独立编号，MapLibre 会在每块都放标签 → 重复省名。MapLibre 按"(图层, 要素 id)"去重，同 id 跨瓦片只出一个标签。但我们主键是 UUID(字符串)，MVT 的 id 必须是整数 → 把 UUID 哈希成**稳定 53 位整数**当 id，同一要素在所有瓦片 id 一致 → 自动去重。
- **难题2·瓦片属性类型漂移**：属性存 JSONB，数字常被存成字符串。分级渲染要按数值插值，但 MVT 把字符串原样编码，MapLibre `interpolate` 拿到字符串就报"Expected number"。解决：生成瓦片时**把数值字段强转 numeric**(脏值落 NULL)+ 前端兜底，历史脏数据不用重导。
- **实时编辑**：地图上拖顶点/改属性 → 保存写回 PostGIS → **强制重载受影响瓦片**(瓦片是缓存，几何变了不重载前端看到的还是旧的)。

### 二、实际怎么跑的

- **存储**：要素几何 = PostGIS geometry(SRID 4326)，属性 = JSONB。
- **发布**：前端 MapLibre vector source 拉 `/datasets/:id/mvt/:z/:x/:y`；后端一条 SQL：`ST_AsMVT` 包 `ST_AsMVTGeom(ST_Transform(geometry,3857), ST_TileEnvelope(z,x,y))`，where `geometry && 变换后瓦片范围` 预过滤。extent=4096/buffer=256。
- **空间索引**：导入流程 INDEXING 阶段用 raw SQL 动态建**版本级部分索引**——`USING GIST(geometry) WHERE versionId=...` + `USING GIN(properties) WHERE versionId=...`(`index.processor.ts:29`)。**不在 Prisma migration 里**(Prisma 表达不了空间索引)，所以是代码运行时建。
- **编辑**：双击要素 → 拉完整几何 → 进编辑态 → 拖顶点/改属性 → PUT /features/:fid → 触发 `map:reload-mvt` 重载瓦片 → 前端看到新几何。

### 三、追问与答

- **为什么用矢量瓦片不直接前端拉 GeoJSON？** 数据量大时全量 GeoJSON 几十万要素，浏览器解析+渲染都扛不住。MVT 按视口按需加载，只拉眼前几块。
- **ST_AsMVT 每次实时算性能扛得住吗？** 靠 bbox 预过滤(`geometry && 瓦片范围`)只处理落进瓦片的要素 + 几何列 GiST 空间索引。当前团队业务数据量实时算够用。
- **空间索引建了没？在 migration 里吗？** 建了——版本级部分 GiST(几何)+ GIN(属性)。**不在 migration**，是导入流程 INDEXING 阶段 raw SQL 动态建(Prisma 表达不了空间索引)；"部分索引(WHERE versionId)"是为了每版本独立索引、查当前版本更快、旧版本清理时索引一起删。
- **跨瓦片标签重复为什么不用别的方法？** MapLibre 去重机制就是靠 (layer, id)，核心是给要素**跨瓦片稳定的整数 id**。UUID 不能直接用(MVT id 要整数)，哈希成 53 位整数成本最低、前端零改动。(53 位是因为 JS 安全整数上限 2^53。)
- **53 位哈希会不会冲突？** hashtextextended 是 64 位截到 53 位，理论可能冲突但概率极低，且即使冲突最多两个要素标签少一个，不影响数据正确性，可接受。
- **属性类型漂移为什么不导入时就转好？** 历史数据已经入库(字符串)，重新导入成本高；瓦片生成时强转对存量数据即时生效，不用动库。新数据导入其实也尽量存对类型，这层是兜底。
- **编辑后为什么要"失效重载瓦片"？** 瓦片按 z/x/y 缓存(浏览器缓存 + 内容由 SQL 当下算)。几何改了不强制重载，前端 vector source 还用旧瓦片，看到的还是旧位置。加时间戳参数破缓存重载那一块。
- **实时编辑多人同时改怎么办？** (诚实) 当前是"保存即覆盖 + 重载"，没有乐观锁/冲突合并；团队业务场景基本单人编辑一个数据集，没遇到冲突。被深追就如实说"暂未做多端冲突处理"。

### 四、风险点

- **ST_AsMVT 完整 SQL 语法**：记住三件套 `ST_AsMVT + ST_AsMVTGeom + ST_Transform(4326→3857) + ST_TileEnvelope`，够说清；参数(extent/buffer)记不住就说"标准 MVT 参数"。
- **53 位 vs 64 位**：别说成 64 位——JS 安全整数是 2^53-1，所以截到 53 位。容易被追问的细节，说对加分。
- **空间索引**：别说"没建"——是建了的(运行时部分索引)。被问"在哪建的"答"INDEXING 阶段 raw SQL，不在 migration"。
- **多端编辑冲突**：真弱点，别主动提；被问到如实说场景单人编辑、暂未做冲突合并。
- **Prisma Unsupported 类型**：被问"Prisma 怎么存 geometry" → Prisma 不支持空间类型，用 `Unsupported("geometry")` 占位，读写走 `$queryRaw/$executeRaw` 原生 SQL。

---

## 第 3 条 · 栅格瓦片服务（COG 动态切片）

> 简历原文：集成 TiTiler + COG 构建免预热的动态栅格瓦片服务，经 GDAL 虚拟文件系统直读对象存储中的遥感影像，与矢量底图统一接入前端瓦片栈，实现影像「上传即出图」。

### 一、概念补课

- **栅格瓦片 vs 矢量瓦片**(第 2 条是矢量，这条是栅格)：矢量瓦片 = 几何数据(protobuf)，前端可交互、可重样式化；栅格瓦片 = 预渲染图片(PNG/JPEG)，前端就是一张图、不能改样式。遥感影像/底图这类"就是一张图"的数据用栅格。
- **COG(Cloud-Optimized GeoTIFF)**：特殊内部布局的 GeoTIFF——内部按瓦片组织 + 带金字塔概览(overviews)。关键：支持 **HTTP Range 请求**，客户端只取需要的某小块/某分辨率，不用下载整个几十 MB~GB 影像。这是动态出瓦片的前提。
- **TiTiler**：DevelopmentSeed 开源的**动态栅格瓦片服务**(Python，基于 rasterio/GDAL)。给一个 COG 的 URL，按请求实时算 z/x/y 瓦片返回，不预切。
- **GDAL 虚拟文件系统 /vsis3**：GDAL/rasterio 的虚拟文件系统，把 S3 兼容对象存储(我们的 MinIO)当"本地文件"读。配合 COG 的 range 能力，TiTiler 通过 /vsis3 从 MinIO **只读所需字节**，不用整文件下载。
- **免预热**：同第 2 条"免预切"——不提前生成瓦片缓存，每次请求实时切，上传即出图。
- **统一瓦片栈**：MapLibre 同一地图里既加 vector source(PostGIS MVT)又加 raster source(TiTiler COG)，矢量数据 + 影像底图叠加。

### 二、实际怎么跑的

1. **上传转 COG**：用户传 GeoTIFF → 后端走 GDAL `gdal_translate -of COG -t_srs EPSG:3857` 一步转成 COG + Web 墨卡托投影 → 存进 MinIO。
2. **TiTiler 读 MinIO**：TiTiler 容器配 `AWS_ENDPOINT_URL=http://minio:9000` + `AWS_VIRTUAL_HOSTING=FALSE` + MinIO 凭证，通过 /vsis3 直读 COG(只 range 读所需字节)。
3. **前端拉瓦片**：MapLibre 加 raster source，瓦片 URL = `${TITILER}/cog/tiles/{z}/{x}/{y}.png?url=s3://gis-uploads/{cogKey}`；用 TileJSON 接口拿影像 bounds/minzoom 自动定位。
4. 上传完即可访问、无需预切 → "上传即出图"。

### 三、追问与答

- **为什么不预切瓦片？** COG + TiTiler 动态切，省存储、影像更新立刻生效、不用维护离线切片流水线。代价是每次请求算(靠 COG range 读 + TiTiler 内部缓存扛)。
- **COG 比普通 GeoTIFF 强在哪？** 普通 GeoTIFF 读一小块得下载整个文件；COG 内部分块 + 概览，支持 range 请求只取所需，适合云上按需读取。
- **为什么用 MinIO 不直接本地文件？** 影像大，对象存储可扩展、多服务共享；TiTiler 通过 /vsis3 range 读等于"云上随机访问"，不用搬到本地。
- **/vsis3 是什么？** GDAL/rasterio 的虚拟文件系统，把 S3 兼容存储当本地读，底层靠 HTTP range。配 `AWS_ENDPOINT_URL` 指向 MinIO、`AWS_VIRTUAL_HOSTING=FALSE`(MinIO 用 path-style)。
- **为什么投影到 3857？** Web 墨卡托是 MapLibre/OSM/Google 等 web 地图标准投影，瓦片按它的 z/x/y 切；原始影像可能是 UTM/经纬度，要重投影。
- **矢量瓦片和栅格瓦片为什么都要？** 矢量 = 可交互几何(要素、编辑、分级渲染)；栅格 = 影像/底图像素数据。数据性质不同，MapLibre 同一地图用不同 source 叠加。
- **TiTiler 读 MinIO 要鉴权吗？** MinIO 凭证配在 TiTiler 环境变量(内网信任)，浏览器不直连 MinIO，只通过 TiTiler 拿瓦片。

### 四、风险点

- **COG 内部结构细节**(tiling/overview)：记不住就说"内部按瓦片组织 + 带金字塔概览、支持 HTTP range 按需读取"，够用。
- **/vsis3 vs 普通 S3 SDK(易混，讲清加分)**：/vsis3 是 GDAL 虚拟文件系统(给 TiTiler/rasterio 读 COG)；后端上传文件用的是 AWS S3 SDK(MinioService)。**而且 /vsis3 只读不能随机写**——所以上传走 MinioService，读取走 /vsis3。
- **TiTiler 是开源服务，不是自研**：被问如实答"集成开源 TiTiler，做了 COG 转换 + MinIO 对接 + 前端瓦片栈接入"，别夸大成"自研栅格瓦片引擎"。
- **前端怎么接**：MapLibre raster source + tile URL + TileJSON 定位，一句话说清。
- **多波段/colormap**(遥感指数、彩色映射)：当前 RGB/灰度直出，没做多波段渲染。被问就说"当前 MVP 直出，多波段在规划"。

---

## 第 4 条 · Web 制图、协同与分享

> 简历原文：以 Canvas 合成含制图要素（指北针 / 比例尺 / 图例等）的高清地图，并接入 tldraw 白板进行标注与多页导出；配套 token 鉴权的只读分享，支持地图成果嵌入第三方系统与移动端。

### 一、概念补课

- **Canvas 合成导出**：浏览器端把地图画面 + 制图要素合成成一张图。MapLibre 地图画在 `<canvas>` 上，导出时 getCanvas() 拿到它，再用 Canvas2D 叠加指北针/比例尺/图例，最后 toDataURL 出 PNG。`preserveDrawingBuffer:true` 是关键——默认 WebGL 缓冲区渲染后会被清空，开了才能稳定截图。
- **高清(devicePixelRatio)**：高 DPI(Retina) 屏 1 CSS 像素对应多个物理像素，导出按 devicePixelRatio 放大，否则糊。
- **比例尺精度**：地图上 1px 代表多少米随纬度变(Web 墨卡托高纬变形大)，按纬度余弦修正算每像素米数。
- **tldraw**：React 的开源无限画布(infinite canvas) 绘图库。我们二次开发做"地图制图白板"——地图截图当图片放进去，白板上标注/排版/加图例。
- **token 鉴权只读分享**：生成不可猜测的随机 token(192 bit) 拼进 `/share/:token`；有链接即可看(免登录) 但只读——前端 store 所有写操作在 readOnly 下直接短路，不触发鉴权写请求。

### 二、实际怎么跑的

- **导出**：框选区域 → map.triggerRepaint 等 WebGL 渲染完 → getCanvas() 按选区裁剪 → Canvas2D 叠加 6 类要素(标题/指北针/比例尺/图例/底图 logo/水印，可开关+定位) → toDataURL 出 PNG；比例尺按当前纬度算；4096px 上限保护。
- **入白板**：导出图 → base64 → tldraw image asset → 缩放到视口 80% 宽居中；标注/排版 → editor.store 订阅 5s 防抖自动保存快照；可导出 PNG 或多页 PDF(jsPDF 逐页)。
- **分享**：管理端生成 token → `/share/:token`；访问者匿名打开，前端拉 `/public/share/:token` 拿项目视图(viewport+底图+图层)，setReadOnly(true) 锁定；分享页强制 MapLibre(对 iframe/WebView 友好，不依赖 Cesium 静态资源)。

### 三、追问与答

- **为什么前端 Canvas 合成不后端渲染？** 地图已在浏览器画好，前端直接读 canvas 截图最快、所见即所得；后端要起 headless 渲染(puppeteer 等)成本高、维护重，量不大没必要。
- **preserveDrawingBuffer 是什么？** WebGL 默认渲染后清空缓冲区(性能优化)，导致 toDataURL 拿到空白；开了才能稳定截图，代价是轻微性能损失。
- **比例尺怎么算准？** Web 墨卡托在不同纬度变形不同，1px 代表的米数随纬度变；按当前中心纬度余弦修正算每像素米数再换算比例尺。
- **为什么选 tldraw？** 成熟开源无限画布，支持图片/形状/文字/自由绘制、可定制工具栏与自定义图形，省去自己造画板。我们做二次开发(自定义工具栏+制图模板+自动保存)，不是从零写。
- **tldraw 自动保存怎么做的？** 订阅 editor.store 变更(source:user)，5s 防抖把 getSnapshot() PUT 到后端；初始 loadSnapshot 完成后才开订阅，防初始加载触发空保存。
- **分享页为什么强制只读？** 匿名访问没登录态，触发任何写操作(自动保存地图状态)会 401，api-client 的 401 拦截会把 iframe 重定向到登录页 → 分享页跳走。所以 store 所有写路径在 readOnly 下短路，根本不发写请求。
- **为什么分享页强制 MapLibre？** MapLibre 纯 JS，iframe/WebView 都能跑；Cesium 要一堆静态资源(/cesium)，WebView 里加载不稳。分享要最轻最兼容。
- **token 安全吗？** 192 bit 随机不可猜测；只读、可撤销；失效统一提示不泄露原因。

### 四、风险点

- **这条偏功能整合、不是硬核工程，别往深吹**。被问"最大技术难点"答真实但 modest 的点：Canvas 高清合成+比例尺精度、tldraw 在 React StrictMode 下重复注册(WeakSet 去重)、匿名分享 readOnly 短路防 401。
- **tldraw license**：prod 构建需 `VITE_TLDRAW_LICENSE_KEY` 否则有水印(dev 能用)。被问"线上有无水印"要知道。
- **PDF 导出**：地图导出只有 PNG；PDF 是白板侧(jsPDF 多页)。别说地图能导出 PDF。
- **分享过期时间**：API 支持 expiresAt 但 UI 没暴露设置，别说"支持过期时间管理"。
- **专题制图(分级渲染/色阶/符号)是另一条、这里没有**——别串。

---

## 第 5 条 · 渲染性能评估体系

> 简历原文：自研渲染性能基准框架，以新旧渲染引擎对比与多轮采样量化帧率、内存、瓦片传输量等关键指标，以数据驱动渲染引擎的选型与迁移决策。

### 一、概念补课

- **为什么要自建**：从旧渲染引擎迁移到新引擎(MapLibre) 需**用数据证明**新引擎在真实地图场景下更快/更省内存，不能凭感觉拍板。现成工具(Lighthouse) 测通用网页，不测地图特有指标(平移缩放 FPS、大数据集瓦片传输量、内存峰值)，所以自建地图专用基准。
- **新旧引擎对比**：同一份测试数据集，在两个引擎各跑一遍相同操作(加载图层/平移/缩放)，对比指标——这是迁移决策的依据。
- **测什么(关键指标)**：
  - **FPS**：平移/缩放流畅度。requestAnimationFrame 算每帧间隔，采样几秒，过滤 >200fps 异常(测量毛刺)。
  - **内存峰值**：Chrome performance.memory 定时采样取峰值(大地图数据集易膨胀)。
  - **瓦片传输量**：Resource Timing API 累加所有瓦片请求 transferSize——衡量引擎拉了多少数据。
  - **首帧/稳定帧时间、fetch 耗时**：加载速度。
- **多轮采样 + P95**：
  - **Warmup(预热)**：正式测前先跑几遍消除 JIT 编译开销(第一次跑总慢，引擎在热身)，否则污染数据。
  - **多次迭代**：跑 N 轮取均值。
  - **P95(95 分位)**：均值掩盖卡顿尖峰；P95 抓尾部("95% 帧低于 X")，反映真实体验下限。

### 二、实际怎么跑的

- **dev 暴露**：benchmark 是开发期工具，通过 `window.runBenchmarkTest` 等触发(不在生产跑)。
- **采集器**：FPS(rAF 间隔)、Memory(performance.memory 采样)、Performance API(Resource Timing 累加瓦片传输)。
- **流程**：预热 → 多轮跑同一场景(加载/平移/缩放) → 采集 → 聚合(mean/P95) → 生成 Markdown 对比报告(含变化百分比 + 自动结论，如"要素 >1000 时新引擎更优")。
- **生产侧**：只有轻量性能 span 埋点(startPerformanceSpan，记录 maplibre.initialize 等关键阶段耗时)；重型 benchmark 框架是 dev 评估用。

### 三、追问与答

- **为什么自建不用现成工具？** Lighthouse 测通用网页(LCP/CLS)，不测地图场景的 FPS@pan、瓦片传输量、大数据集内存；迁移引擎需要地图专用数据，所以自建。
- **测了哪些指标？为什么是这些？** FPS(流畅度)、内存峰值(大数据集易膨胀)、瓦片传输量(数据量)、首帧/稳定帧(加载速度)，每个对应一类性能问题。
- **为什么用 P95 不用均值？** 均值掩盖卡顿尖峰；P95 抓尾部，反映体验下限。
- **warmup 为什么必要？** 第一次跑 JS 引擎在 JIT 编译、缓存没建，偏慢不稳定；预热消除冷启动效应才准。
- **FPS 怎么测？** requestAnimationFrame 每帧回调算间隔倒数得瞬时 FPS，采样几秒，过滤 >200fps 异常，再算 avg/min/max/P95。
- **内存怎么测？** Chrome performance.memory(非标准、仅 Chrome) 定时采样取峰值；局限是只在 Chrome 有、近似值。
- **瓦片传输量怎么测？** Resource Timing API，每个瓦片请求有 transferSize，累加——能比较不同引擎数据拉取量(MVT 按需 vs 全量 GeoJSON)。
- **这个 benchmark 在生产跑吗？** 不。重型 benchmark 是 dev 期评估工具(通过 window 触发)，用于迁移决策；生产只有轻量 span 埋点。别夸成"生产性能监控系统"。
- **迁移决策怎么用数据？** 对比报告给出两引擎各指标变化百分比 + 自动结论(要素过千时新引擎 FPS 更高、传输更少)，据此决定何时切新引擎。

### 四、风险点

- **别夸成"生产可观测平台"**：dev 评估工具 + 生产轻量埋点，不是 Prometheus/Grafana 那套。被问"生产监控怎么做"要分清：benchmark 评估用、生产 span 埋点。
- **内存采集局限**：performance.memory 非标准、仅 Chrome、近似值，被问如实说"有平台局限"。
- **benchmark 里仍含旧引擎对比代码**：迁移决策期做的对比，保留作回归参考；被问就说"迁移期对比工具，保留作回归"。
- **个别指标占位**：有少数指标(如 parseDuration) 是预留占位未完全实现，被深追个别指标就承认"部分指标预留、未完全实现"。
- **别和"渲染性能优化"混**：这条是"测量体系"，不是"优化手段"(LOD/瓦片缓存那些是工作经历里另一条)。被问"做了哪些优化"别拿 benchmark 当优化答。

---

## 收尾

5 条 Action 防御完毕。`项目背景` 是上下文(讲清业务即可、无技术深挖点)；`项目成果` 见简历 `[X]` 占位——**数字收集到后，务必能答**：「数据是什么」(项目影像 + 成果数据)、「怎么存的」(MinIO 原始文件 + PostGIS 几何)、「配图是什么」(公众号/自媒体地图配图)，跟正文一致、别讲岔。
