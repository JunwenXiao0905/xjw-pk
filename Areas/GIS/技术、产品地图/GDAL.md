# GDAL

> 地理数据界的"万能翻译器 + 螺丝刀"。开源 GIS 世界的地基：QGIS 的文件读写、Python 地理生态（geopandas / rasterio / fiona）底层都是它。
> 一句话定位：**不管什么冷门格式、什么坐标系，先翻译成统一内存模型，再随你转换、裁剪、重投影、入库。**

- 官方：https://gdal.org （OSGeo 基金会托管，1998 年 Frank Warmerdam 发起，C++）

---

## 1. 命名的历史包袱

原本是两个独立库，2015 年 GDAL 2.0 合并成一个代码库，统一叫 GDAL，但工具名保留了血统：

| 血统 | 管什么 |
|---|---|
| **GDAL**（原名，Geospatial Data Abstraction Library） | **栅格**数据（卫星影像、DEM、瓦片——像素网格） |
| **OGR**（缩写含义已失传） | **矢量**数据（点线面 + 属性表） |

记忆锚点：**工具名 ogr 前缀 = 矢量；gdal 前缀 = 大多栅格**。看名字就能猜用途。

---

## 2. 内部格局（自上而下四层）

```
┌─────────────────────────────────────────────────┐
│  utilities/  命令行工具层（直接敲的命令）           │
│  栅格: gdalinfo  gdal_translate  gdalwarp ...    │
│  矢量: ogrinfo   ogr2ogr          ogrtindex ...  │
├─────────────────────────────────────────────────┤
│  C++ API  统一抽象数据模型（库的精华）              │
│  栅格: Dataset → RasterBand（按块 block 读写+缓存）│
│  矢量: DataSource → Layer → Feature               │
│             = Geometry（几何）+ Fields（属性）     │
├─────────────────────────────────────────────────┤
│  drivers/  格式驱动层（插件式，一格式一驱动）        │
│  栅格 150+: GTiff / JPEG / PNG / COG / WMS ...   │
│  矢量 80+:  Shapefile / PostgreSQL / GeoJSON /   │
│             GPKG / KML / CSV ...                  │
├─────────────────────────────────────────────────┤
│  底层依赖（干重活的帮手）                          │
│  PROJ  坐标系定义与转换（EPSG:4326→3857 等）       │
│  GEOS  几何运算（相交/合并/简化，JTS 的 C++ 移植）  │
│  SQLite / libcurl / ...                           │
└─────────────────────────────────────────────────┘
```

核心设计就一个词：**驱动模型**。上层 API 只认抽象（"一个图层，里面有若干要素，要素 = 几何 + 属性"），不关心文件长什么样；每种格式一个驱动负责翻译。所以敢号称几百种格式——加格式不改上层，只加驱动。

另有 **alg/ 算法库**（重采样、栅格化、等高线生成）和 **语言绑定**（SWIG 生成，Python 里 `from osgeo import ogr`）——geopandas 那些好用的库，底层全站在这排绑定上。

---

## 3. 存在形式：是库，不是单个命令

**第一身份是 C++ 库**：编译产物是动态链接库（Win 的 `gdal.dll`、Linux 的 `libgdal.so`）+ 头文件。命令行工具只是链接这个库的薄壳 exe，自己几乎不含逻辑。

和 pnpm 这类自包含 CLI 的区别：

| | pnpm | GDAL |
|---|---|---|
| 本质 | 自包含 JS 程序 | C++ 库 + 一串原生依赖 dll + 命令行工具集 + 数据文件 |
| 依赖 | 自带运行时，零外部依赖 | PROJ、GEOS、SQLite、libcurl……整条原生依赖链 |
| "注册" | `npm i -g` 进 PATH 完事 | exe 要能找到 dll（同目录/PATH）+ 数据文件（环境变量） |

- **"注册"机制一样是 PATH**：敲 `ogr2ogr`，系统沿 PATH 找 `ogr2ogr.exe`。区别是 pnpm 拷哪都能跑，`ogr2ogr.exe` 单独拷走会报"缺少 dll"。
- **数据文件是第三块拼图**：GDAL 离了 `proj.db`（几千条 EPSG 坐标系定义）就不认识坐标系。靠环境变量 `GDAL_DATA`、`PROJ_DATA` 定位。

### Windows 安装出名地麻烦的三个原因

1. **dll 依赖链**：exe 和十几个 dll 必须整整齐齐待在一起；
2. **环境变量**：PATH 之外还要 `GDAL_DATA`/`PROJ_DATA` 指对数据目录；
3. **没有统一包管理器兜底**：Linux `apt install gdal-bin` 一条命令全配好，Windows 各发行渠道各管一段。

所以 Windows 的 GDAL 发行版，本质都是**别人帮你打包好的"库 + dll + 工具 + 数据文件 + 环境变量"整套环境**。

### 安装渠道对比（2026-09 实测：本机有 Docker/scoop，无 conda/choco，scoop 无 gdal 包）

| 方式 | 评价 |
|---|---|
| **Docker**（`ghcr.io/osgeo/gdal` 镜像） | 零安装零污染，偶尔用最优解；代价是命令多一层 `docker run` 包装 |
| **OSGeo4W 安装器** | 官方推荐。osgeo4w.com 下 setup.exe，Advanced 模式勾 GDAL。装完用 "OSGeo4W Shell"，或把 `C:\OSGeo4W\bin` 加 PATH（Git Bash 加 `~/.bashrc`：`export PATH="/c/OSGeo4W/bin:$PATH"`） |
| GISInternals 解压版 | zip 解压 + 跑 SDKShell.bat。免管理员，偶尔缺依赖 |
| conda（`conda install -c conda-forge gdal`） | 最省心的命令行装法，但为个工具装 conda 值不当 |
| choco / scoop | 看运气，本机 scoop 实测无 gdal 包 |

**结论：偶尔用（灌库、格式转换）→ Docker；高频用（天天批量处理/写 Python 地理脚本）→ OSGeo4W。**

Docker 用法两个要点：容器连宿主库用 `host.docker.internal`（不是 localhost）；挂载 Git Bash 下写 `-v "D:/data:/data"`。

---

## 4. ogr2ogr：矢量转换的瑞士军刀

在格局中的位置：**最顶上命令行工具层、矢量（OGR 血统）转换类**。自己什么都不会，是个调度员：

```
ogr2ogr（薄壳，解析命令行参数）
   ├─ 源驱动：ESRI Shapefile driver  读 .shp → 翻译成 Feature 流
   ├─ PROJ：-t_srs EPSG:4326 → 算坐标怎么转
   ├─ GEOS：-nlt PROMOTE_TO_MULTI / -simplify / -clip 等几何加工
   └─ 目标驱动：PostgreSQL driver → 拼 INSERT/COPY 写进 PostGIS
```

### 常用参数速查

| 参数 | 作用 | 不加会怎样 |
|---|---|---|
| `-f PostgreSQL` | 目的地驱动 | 必填（写入库） |
| `PG:"host=... dbname=... user=... password=..."` | 连接串 | |
| `-nln 表名` | 目标表名 | 用源文件名当表名（可能是中文） |
| `-append` | 追加进已存在的表 | 默认试图建新表 |
| `-nlt PROMOTE_TO_MULTI` | Polygon 自动升格 MultiPolygon | 表约束 MultiPolygon 时单面要素插入失败 |
| `-t_srs EPSG:xxxx` | 坐标转到目标坐标系 | 源是 CGCS2000/投影坐标时数据错位 |
| `-s_srs` | 手动声明源坐标系 | 源缺坐标系声明时 |
| `-select "A AS x, B AS y"` | 字段映射（没提的源字段被丢弃） | 源字段名和表列名对不上时插错/失败 |
| `-lco GEOMETRY_NAME=geom` | 几何列名 | 新建表时叫 `wkb_geometry` |
| `--config PG_USE_COPY YES` | COPY 批量写 | 逐条 INSERT，几万行慢好几倍 |
| `-progress` | 进度条 | 大文件干等没反馈 |
| `--config SHAPE_ENCODING CP936` | 属性表编码 | 中文 .dbf 乱码 |
| `-overwrite` | drop 重建表 | **危险**：约束索引全丢；结构自己管的场景永远用 `-append` |

配套侦察工具 `ogrinfo -so -al 文件.shp`：看几何类型 / 要素数 / 坐标系 / 字段名。**拿到任何数据第一步先侦察。**

---

## 5. 实战：shapefile 灌 PostGIS（透游项目村界入库）

> 背景：透游把 4 万+ 四川行政村界（shapefile）灌进 PostGIS 的 `village_boundaries` 表，
> 供路线归属村判定（ST_Contains）和 [[PostGIS]] ST_AsMVT 矢量瓦片渲染用。

### 四步工作流

**第 0 步：先让表存在**。后端 `init_schema` 建好带约束的表（`geometry(MultiPolygon,4326) NOT NULL`）+ GiST 索引，再灌库——类型和索引自己说了算，不让工具按 shapefile 猜。

**第 1 步：侦察**
```bash
docker run --rm -v "D:/data:/data" ghcr.io/osgeo/gdal:ubuntu-small-3.8.4 \
  ogrinfo -so -al /data/村界.shp
```

**第 2 步：灌库**
```bash
docker run --rm -v "D:/data:/data" ghcr.io/osgeo/gdal:ubuntu-small-3.8.4 \
  ogr2ogr \
    -f PostgreSQL PG:"host=host.docker.internal port=5432 dbname=touyou user=touyou password=touyou" \
    /data/村界.shp \
    -nln village_boundaries \
    -append \
    -nlt PROMOTE_TO_MULTI \
    -t_srs EPSG:4326 \
    -lco GEOMETRY_NAME=geom \
    --config PG_USE_COPY YES \
    -progress
```
追加模式关键行为：**列按名字匹配**，表里源数据没有的列（自增 id、默认 created_at）自动用默认值。

**第 3 步：验证**
```sql
SELECT count(*) FROM village_boundaries;  -- 和 ogrinfo 的 Feature Count 对账
EXPLAIN ANALYZE SELECT * FROM village_boundaries
 WHERE geom && ST_MakeEnvelope(103.9, 30.5, 104.0, 30.6, 4326);
-- 看到 Bitmap Index Scan on ..._geom 说明 GiST 索引生效
```

**第 4 步：刷新下游聚合表**（该项目的市/区县/乡镇 ST_Union 聚合，灌完手动调，4 万面约几分钟）。

### 坑清单（按踩中概率排序）

1. **中文乱码**：国内 .dbf 常是 GBK → `--config SHAPE_ENCODING CP936`
2. **字段名对不上**：源叫 `XZQDM`/`XZQMC` → `-select "XZQDM AS village_code, ..."`
3. **坐标系没转**：自然资源系数据常见 CGCS2000(EPSG:4490)或高斯克吕格 → 不看坐标系直接灌，整体偏移几百米或飞掉
4. **`-overwrite` 手滑**：drop 自己的表按工具方式重建，约束索引全丢
5. **重复灌**：`-append` 跑两遍数据翻倍，重灌前先 `TRUNCATE`

---

## 6. 同家族工具速览

| 工具 | 血统 | 用途 |
|---|---|---|
| `ogrinfo` | 矢量 | 侦察：格式/字段/坐标系/要素数 |
| `ogr2ogr` | 矢量 | 转换/入库/导出/字段映射/裁剪 |
| `gdalinfo` | 栅格 | 侦察影像：尺寸/波段/范围/统计值 |
| `gdal_translate` | 栅格 | 格式转换（TIFF→PNG，ogr2ogr 的栅格版） |
| `gdalwarp` | 栅格 | 重投影/镶嵌/裁切 |
| `gdalbuildvrt` | 栅格 | 一堆影像拼虚拟镶嵌（不复制像素） |

---

## 7. 在生态里的位置

- **GDAL 管"数据进出"侧**（文件 ↔ 库的 ETL，一次性活）；库里的空间能力（ST_AsMVT / ST_Contains）是 **[[PostGIS]]** 提供的——PROJ/GEOS 同宗师兄弟，长在数据库里。
- Python 生态：geopandas / rasterio / fiona 底层是 GDAL 绑定；纯 pip 装 GDAL 本体很痛苦（要编译），走 conda-forge 或带捆绑依赖的 wheel。
- QGIS 的文件读写也是它。
- 切瓦片相关：PostGIS ST_AsMVT 是服务端实时切；离线预切生态见 [[PMTiles]] / [[GeoServer]]。

---
*沉淀自 2026-09 透游村界灌库学习（来源：与 AI 的链路走读对话）。*
