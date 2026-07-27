# GeoServer

> GeoServer 是空间数据**发布服务器**(publishing server),把数据发布成 OGC web 服务(WMS/WFS/WCS/瓦片)给前端地图用。**它不是数据库**——存储归 PostGIS 管。

## 角色:发布层

```
数据存储层:PostGIS(真正存数据、做空间查询)
   ↑(读)
发布服务层:GeoServer(把数据发布成 WMS/WFS/WCS 给前端)
   ↓
前端:Leaflet / OpenLayers / MapLibre / 高德
```

## GeoServer vs PostGIS

| | PostGIS | GeoServer |
|---|---|---|
| 角色 | 空间数据库(存储 + 计算) | 空间数据服务器(发布 + 服务) |
| 存数据? | 是,本职 | **否**,引用外部数据(PostGIS / shapefile / GeoTIFF) |
| 数据在哪 | PG 表里 | 它连接的 Store(指向 PostGIS / 文件) |
| 能改数据? | SQL 直接改 | 只矢量,且通过 **WFS-T**(底层改 PG);栅格不能 |
| 核心能力 | 空间存储 + 空间查询/分析 | 发布 WMS / WFS / WCS / 瓦片 |

## GeoServer 能"存储"上传数据吗?——半能半不能
- **没有自己的数据库引擎**。
- 有个 **data_dir(数据目录)**:上传 shapefile/GeoTIFF,它把**文件**丢进去、注册成 Store 指向这个文件。本质是"文件存放 + 引用",不是数据库存储。
- 真存储/管理:数据放 PostGIS,GeoServer 只连过去读(**PostGIS Store**)。

## 能用 GeoServer 改数据吗?——能,但有限
- **矢量**:通过 **WFS-T**(Web Feature Service - Transactional)协议 INSERT/UPDATE/DELETE 要素,底层改 PostGIS。QGIS 之类能这样编辑。
- **栅格**:基本不能(WCS 只读出图)。
- 生产里多数:**应用后端直接写 PostGIS**,GeoServer 只读着发。WFS-T 多用于轻量 GIS 工作流。

## OGC 服务(发布的几种)

| 服务 | 出什么 |
|---|---|
| WMS | 地图图片(出图) |
| WFS | 矢量特征(可查 / 可 WFS-T 改) |
| WCS | 栅格 |
| WMTS | 瓦片(缓存) |

## 什么时候用 GeoServer、什么时候不用

| 场景 | 选 |
|---|---|
| 要 OGC 标准接口、多源发布、样式集中管(SLD)、企业级 | **GeoServer** |
| 只是给现代前端出矢量瓦片、定制 API、想轻量 | PostGIS 直出 + Martin(见 [[PostGIS矢量瓦片(MVT)]]) |

## 面试金句
> "PostGIS 是存储与计算层,GeoServer 是发布层;GeoServer 不替代数据库,它连接 PostGIS(或文件)把数据发布成 OGC 服务;写数据一般后端直连 PG,GeoServer 主读,必要时矢量可走 WFS-T。"
