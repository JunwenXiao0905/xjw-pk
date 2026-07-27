# PostGIS 矢量瓦片(MVT)生成与分发

> PostGIS 能直接生成 MVT(Mapbox Vector Tile),配合薄服务层即可**不依赖 GeoServer** 分发矢量瓦片。

## PostGIS 的瓦片生成能力

| 函数 | 出什么 |
|---|---|
| `ST_AsMVT` + `ST_AsMVTGeom` | Mapbox Vector Tile(MVT,矢量瓦片,`.mvt`/`.pbf`) |
| `ST_AsTIFF` / `ST_AsPNG` | 栅格瓦片/图片 |
| `ST_TileEnvelope(z, x, y)` | 算某 z/x/y 瓦片的外包框 |

### MVT 生成的标准 SQL 模式(面试能写出来很加分)

```sql
SELECT ST_AsMVT(tile.*, 'pois', 4096, 'geom') AS mvt
FROM (
  SELECT name,
         ST_AsMVTGeom(geom, ST_TileEnvelope(15, x, y), 4096, 64, true) AS geom
  FROM pois
  WHERE geom && ST_TileEnvelope(15, x, y)
) AS tile;
```

- `ST_AsMVTGeom` = 把几何裁剪、变换到瓦片坐标空间;
- `ST_AsMVT` = 把这片的几何打包成 MVT 二进制;
- 结果是 bytes,前端(MapLibre / OpenLayers / Leaflet 插件)直接吃。

## 但"生成" ≠ "完整分发服务"

PostGIS 能出瓦片二进制,但**没有**:HTTP 服务、OGC 协议(WMS/WMTS)、样式管理(SLD)、瓦片缓存。**分发得补一层**。

## 分发:PostGIS 直出 + 薄服务(主流)

| 方案 | 说明 |
|---|---|
| **Martin** ⭐ | Rust,MapLibre 官方,GitHub **3.8k stars**,2025 基准**最快**;支持 PostGIS 表/函数 + PMTiles/MBTiles/GeoJSON |
| **pg_tileserv** | Go,Crunchy Data 出品,配置简单,PostGIS 专用 |
| **自建 API** | FastAPI/Go 端点调 `ST_AsMVT` 返回 bytes |

三者都是**独立运行的服务**(不是 PostGIS 插件,也不是库),连 PG 当客户端,把"瓦片协议 ↔ SQL"翻译过来。数据全在 PostGIS,自己不存。

> 对比另见同级 [[GeoServer]](企业级 OGC 发布服务器,非 PostGIS 专属)。

## 选型:按场景

| 场景 | 主流方案 |
|---|---|
| 从 PG **实时出瓦片**(数据常变) | **Martin** |
| **静态瓦片**(不常变、要极致性能/低成本) | **PMTiles**(Protomaps)+ tippecanoe,放 CDN |
| 企业 **OGC** 服务(WMS/WFS/WMTS) | **GeoServer** |
| 栅格瓦片 | TiTiler / GeoServer |

> 2024–2026 大趋势:**PMTiles 静态分发**——预生成瓦片打包成单文件,放对象存储(S3/CDN),连瓦片服务器进程都省(详见 [[PMTiles]])。Martin 也支持发 PMTiles。

## 面试金句
> "PostGIS 用 `ST_AsMVT` 能直接生成矢量瓦片,配合 Martin/pg_tileserv 或自建 API 即可不依赖 GeoServer 分发;但 OGC 协议、SLD 样式、瓦片缓存这些发布级能力还是 GeoServer 强。实时出瓦片主流是 Martin;更大趋势是 PMTiles 静态分发。"
