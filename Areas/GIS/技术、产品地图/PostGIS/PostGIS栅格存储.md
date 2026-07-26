# PostGIS 栅格(影像)存储

> PostGIS 存影像(栅格)的机制:`raster` 类型 + 切片(tiling)+ 二进制存储。多波段影像(如多光谱卫星影像)也在此列。

## 存储模型

### raster 类型 + 二进制(WKB)
PostGIS 用 `raster` 类型存栅格,内部是 **WKB Raster 二进制格式**(类似矢量的 WKB,但是栅格版)。一个 raster 对象 = 像素网格 + 地理参考(它在地球上哪个位置)+ 元数据。

### 多波段怎么存
一个 raster 对象**自带多个波段(band)**,每个波段独立配置:

| 波段属性 | 说明 |
|---|---|
| 像素类型 | `8BUI`(8 位无符号,典型 RGB)、`16BSI`、`32BF`(浮点,存高程/温度)、`64BF` 等 |
| nodata | 透明/无效值 |
| 统计 | min/max/mean(可缓存,加速查询) |

一个 **4 波段(R,G,B,NIR)的多光谱影像 = 一个 raster 对象,4 个波段**(不是一个表 4 列)。

### 关键:切片(tiling)
大影像不会塞一行(二进制会巨大、查不动),而是切成网格状的小瓦片,**每片一行**:

```sql
CREATE TABLE sat_image (
    rid serial PRIMARY KEY,
    rast raster                  -- 一行 = 一个瓦片(可多波段)
);
CREATE INDEX sat_image_gist ON sat_image USING GIST (rast);  -- 空间索引,跟矢量一样
```

- 10000×10000 的影像切成 100×100 瓦片 = 1 万行。
- **为什么切片**:查询时用 GiST 索引只取需要区域的瓦片(不读整图);每行二进制不会太大。
- 跟矢量"一行一个要素"不同——栅格是"**一行一个瓦片(网格块)**"。

## 导入:raster2pgsql

PostGIS 自带命令行工具,把 GeoTIFF 等导入并自动切片:

```bash
raster2pgsql -s 4326 -t 100x100 input.tif myschema.sat_image | psql -d gisdb
```

- `-s 4326`:SRID;`-t 100x100`:瓦片大小;管道把生成的 SQL 灌进库。

## 库内能干啥(不用导出来)

- `ST_Value(rast, 点)` —— 取某点像素值
- `ST_Band(rast, 1)` —— 抽第 1 波段
- `ST_SummaryStats(rast, 1)` —— 波段统计(min/max/mean)
- `ST_MapAlgebra(...)` —— 波段运算/地图代数(如 NDVI = (NIR−R)/(NIR+R))
- `ST_Reclass(...)` —— 重分类

## Out-of-DB(可选)
库里只存元数据、像素留外部文件,保持库小——少见。

## 面试金句
> "PostGIS 用 `raster` 类型存栅格,一个对象可含多波段(每波段独立像素类型/nodata);大影像靠 `raster2pgsql` 切成瓦片、每片一行,配 GiST 索引按区域查询;栅格和矢量共用同一套空间索引机制。"
