# PMTiles(Protomaps)

> PMTiles 是一种**单文件瓦片归档格式**(矢量/栅格都行),核心特点:支持 **HTTP Range 请求**,可直接放**静态存储**分发,**无需瓦片服务器进程**。Protomaps 项目出品。

## 是什么 / 为什么

- 把所有瓦片打包成**一个 `.pmtiles` 文件**(类似 `.mbtiles`,但结构不同)。
- 文件内带目录索引,客户端通过 **HTTP Range 请求**(按字节范围取)只下载当前需要的那一片,**不用下整文件**。
- 因此可以放**任何静态存储 / CDN**:S3、Cloudflare R2、GitHub Pages、Nginx 静态目录……**省一个瓦片服务器进程**。
- 适合**不常变**的数据:底图、行政区划、历史数据。

## vs MBTiles

| | MBTiles | PMTiles |
|---|---|---|
| 格式 | SQLite 数据库 | 单文件 + 目录索引 |
| 分发 | 需要 server 查询(tileserver-gl、Martin 等) | 直接 HTTP Range,**纯静态**即可 |
| 云原生 | 不友好(要进程读 SQLite) | 友好(对象存储 + CDN) |

## 生成

- **tippecanoe**(Mapbox 出品):把 GeoJSON / Shapefile / PG 数据切成矢量瓦片,可直接输出 `.pmtiles`(或先出 `.mbtiles` 再转)。能控制切片级别、简化、属性等。
- **pmtiles CLI**(go-pmtiles):`.mbtiles` → `.pmtiles` 转换,也能本地起服务调试。

```bash
# tippecanoe 直接出 pmtiles
tippecanoe -o output.pmtiles -zg -l mylayer input.geojson

# 或 mbtiles 转 pmtiles
pmtiles convert input.mbtiles output.pmtiles
```

## 消费(前端)

MapLibre GL JS + pmtiles 协议插件,直接从 URL 读:

```js
import { Protocol } from 'pmtiles';
const p = new Protocol();
maplibregl.addProtocol('pmtiles', p.tile);
// 之后把 pmtiles://https://cdn.xxx/data.pmtiles 当 source 用
```

Leaflet / Mapbox GL 也有相应插件。

## 什么时候用 / 不用

| 场景 | 用 PMTiles? |
|---|---|
| 底图、行政区划等**不常变**数据,要**低成本 / 高并发** | ✅ 放 CDN,极致性价比 |
| **常变**数据(实时位置、业务数据) | ❌ 用实时生成(Martin / `ST_AsMVT`,见 [[PostGIS矢量瓦片(MVT)]]) |
| 需要 server 端逻辑 / OGC 协议 | ❌ 用 GeoServer([[GeoServer]]) |

## 面试金句
> "PMTiles 是单文件瓦片格式,靠 HTTP Range 请求按需取片,能直接放对象存储 / CDN,省掉瓦片服务器进程;适合不常变的底图 / 边界数据,常配合 tippecanee 生成、MapLibre 前端消费。"
