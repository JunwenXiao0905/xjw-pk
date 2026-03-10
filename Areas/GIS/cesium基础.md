## cesium基础
官方文档阅读指南

`viewer.entities.add(options)` 相当于就是 `new Cesium.Entity(options)` 。内部运行：调用`Entity `的构造函数，将`options`赋值给`Entity `的属性。所以，`options `怎么写，就看`Entity.ConstructorOptions` 

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1732625875718-0726e40f-a1ed-4295-8a91-9d118c5248ad.png)

而，要查看已经实例化后的 `Entity` 对象的属性和方法，就往下翻阅

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1732625883067-f71712e4-86fd-4dcf-afdb-cc3d1f0d53b8.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1732625886172-6cfec4e8-7d01-4bf2-b15b-ce09b5764aaa.png)



[CesiumJS-0318.pdf](https://www.yuque.com/attachments/yuque/0/2026/pdf/34655355/1768885819108-7a145ead-c749-4cd0-9203-63b8be40dd0e.pdf)

## 一、heml页面实现cesium加载
1、下载1.99版本（这样下载是歪货，应该直接找GitHub）

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1732625910120-a5061cac-fa64-4ce4-aeca-5209a5737e09.png)

2、拿到token

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1732625947498-a5096844-a7b6-4a1b-8350-415027959e01.png)

3、cesium包认识

既是js包，也是一个完整的项目，可以直接启动

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1732625951810-71cd6276-cc0f-4eed-98f6-46d8b58ef960.png)

4、html中加载

我猜测是这个包的问题，导致无法识别 js 和css 包。也有可能是token的问题，毕竟当成项目直接打开1.99这个版本，会报错显示 token 不合法

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1732625957316-516fdbcf-3152-4940-a0cf-03ebafd0d8d0.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1732625961161-9728e11f-8cd2-4950-8b4d-a3a30456803b.png)



## 二、vue-cesium
## 1、使用vite启动Cesium
安装1.99版本，并在vite.config中配置

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1732625965875-0204ae43-cf99-44af-9ff2-d94651b24274.png)



## 2、使用cdn


## 3、直接引用


## 4.加载底图
### 4.1 天地图
#### 基本介绍
[http://lbs.tianditu.gov.cn/server/MapService.html](http://lbs.tianditu.gov.cn/server/MapService.html)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/34655355/1772521876650-4c941e66-b855-406e-838a-a580f1ce7784.png)

天地图的 WMTS 服务必须按照 OGC WMTS 标准拼接完整的请求参数（也就是`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">SERVICE=WMTS&REQUEST=GetTile...</font>`这一串），只使用基础地址加密钥是无法获取瓦片数据的。这些不同图层（vec_c、cva_c、img_c 等），本质是替换 WMTS 请求参数中的`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">LAYER</font>`值，并匹配对应的`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">TILEMATRIXSET</font>`（投影类型）。

示例

```typescript
http://t1.tianditu.gov.cn/vec_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=vec&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=
```

#### <font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">参数拆解与验证</font>
```plain
http://t1.tianditu.gov.cn/vec_w/wmts?
service=wmts               # 固定值，声明WMTS服务（大小写不敏感）
&request=GetTile           # 固定值，声明获取瓦片（核心）
&version=1.0.0             # 固定值，WMTS版本
&LAYER=vec                 # 核心：图层名，vec对应矢量底图
&tileMatrixSet=w           # 核心：投影类型，w=球面墨卡托（c=经纬度）
&TileMatrix={TileMatrix}   # 核心：瓦片层级（对应z）
&TileRow={TileRow}         # 核心：瓦片行号（对应y）
&TileCol={TileCol}         # 核心：瓦片列号（对应x）
&style=default             # 固定值，图层样式
&format=tiles              # 固定值，瓦片格式
&tk=你的密钥               # 核心：天地图密钥（必填，否则403）
```

**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">关键验证点（确保能获取数据）：</font>**

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">参数完整性：以上 9 个参数缺一不可，少一个都会返回错误（如 400/404）；</font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">参数匹配规则</font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">：</font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">地址中的</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">vec_w</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">：</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">vec</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">必须和</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">LAYER=vec</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">一致，</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">w</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">必须和</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">tileMatrixSet=w</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">一致；</font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">若换成经纬度投影（</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">vec_c</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">），需同步修改</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">tileMatrixSet=c</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">；</font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">大小写兼容：WMTS 标准对参数名大小写不敏感（如</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">service=WMTS</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">和</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">service=wmts</font>`<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">效果一致），天地图均支持。</font>

#### <font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">Cesium加载的完整代码</font>
```typescript
try {
  if (basemap === 'tianditu-vec') {
    // Tianditu Base Layer
    const imgProvider = new Cesium.WebMapTileServiceImageryProvider({
      url: `http://t1.tianditu.gov.cn/vec_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=vec&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=${TIANDITU_TOKEN}`,
      layer: 'img',
      style: 'default',
      format: 'tiles',
      tileMatrixSetID: 'w',
      maximumLevel: 18,
    });
    viewer.imageryLayers.addImageryProvider(imgProvider);

    // Tianditu Annotation Layer
    const ciaProvider = new Cesium.WebMapTileServiceImageryProvider({
      url: `http://t1.tianditu.gov.cn/cva_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=cva&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=${TIANDITU_TOKEN}`,
      layer: 'cia',
      style: 'default',
      format: 'tiles',
      tileMatrixSetID: 'w',
      maximumLevel: 18,
    });
    viewer.imageryLayers.addImageryProvider(ciaProvider);
  } else if (basemap === 'tianditu-img') {
    // Tianditu Satellite Layer
    const imgProvider = new Cesium.WebMapTileServiceImageryProvider({
      url: `http://t1.tianditu.com/img_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=img&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=${TIANDITU_TOKEN}`,
      layer: 'img',
      style: 'default',
      format: 'tiles',
      tileMatrixSetID: 'w',
      maximumLevel: 18,
    });
    viewer.imageryLayers.addImageryProvider(imgProvider);

    const ciaProvider = new Cesium.WebMapTileServiceImageryProvider({
      url: `http://t1.tianditu.gov.cn/cia_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=cia&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=${TIANDITU_TOKEN}`,
      layer: 'cia',
      style: 'default',
      format: 'tiles',
      tileMatrixSetID: 'w',
      maximumLevel: 18,
    });
    viewer.imageryLayers.addImageryProvider(ciaProvider);
  } else if (basemap === 'tianditu-ter') {
    // Tianditu Terrain Layer
    const terProvider = new Cesium.WebMapTileServiceImageryProvider({
      url: `http://t1.tianditu.gov.cn/ter_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=ter&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=${TIANDITU_TOKEN}`,
      layer: 'ter',
      style: 'default',
      format: 'tiles',
      tileMatrixSetID: 'w',
      maximumLevel: 18,
    });
    viewer.imageryLayers.addImageryProvider(terProvider);

    const ctaProvider = new Cesium.WebMapTileServiceImageryProvider({
            url: `http://t1.tianditu.gov.cn/cta_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=cta&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=${TIANDITU_TOKEN}`,
            layer: 'cta',
            style: 'default',
            format: 'tiles',
            tileMatrixSetID: 'w',
            maximumLevel: 18,
          });
          viewer.imageryLayers.addImageryProvider(ctaProvider);
        } else if (basemap === 'tianditu-ibo') {
          // Tianditu IBO Layer
          const imgProvider = new Cesium.WebMapTileServiceImageryProvider({
            url: `http://t1.tianditu.gov.cn/ibo_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=ibo&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=${TIANDITU_TOKEN}`,
            layer: 'ibo',
            style: 'default',
            format: 'tiles',
            tileMatrixSetID: 'w',
            maximumLevel: 18,
          });
          viewer.imageryLayers.addImageryProvider(imgProvider);
        }
      } catch (error) {
        console.error('Failed to load basemap:', error);
      }
```

## 4、控件显示
### 2.1 取消logo
```bash
viewer.cesiumWidget.creditContainer.style.display = "none";
```

直接找到 logo 所在 div 的类，添加样式。

注意：加了 scope 后，会在 template 中的元素中添加随机数，以防止不同组件的同名组件的样式污染。这也会导致一个问题，不是自己代码中写的标签在渲染时并不会有随机数，所以 在scope 里面写的样式不会起作用。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730015071232-f47b9509-6eac-490d-9431-61c5ce0fc24d.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730015076201-6c260e7e-aa31-4100-83be-40a1666a6dbe.png)

### 2.2 取消控件
```javascript
  let  viewer = new Cesium.Viewer("viewer",{
    imageryProvider: esri,//手动指定图层  默认是谷歌的影像图层
    // terrainProvider: Cesium.createWorldTerrain({
    //   requestWaterMask: true//水面特效
    // }) //地形图层 (高程数据)
    animation: false,//隐藏动画控件
    timeline: false,//隐藏时间轴
    geocoder: false,//隐藏搜索按钮
    homeButton: false,//隐藏主页按钮
    sceneModePicker: false,//隐藏投影方式按钮
    baseLayerPicker: false,//隐藏图层选择按钮
    navigationHelpButton: false,//隐藏帮助按钮
    fullscreenButton: false,//隐藏全屏按钮
  });
```

### 2.3 切换图层
```javascript
  // ArcGIS影像图层
  const esri = new Cesium.ArcGisMapServerImageryProvider({
    url: "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer",
    enablePickFeatures: false,
  });
...
  let  viewer = new Cesium.Viewer("viewer",{
    imageryProvider: esri,//手动指定图层  默认是谷歌的影像图层

  });
```

### 2.4 Home控件
要在 Cesium 中自定义 “Home” 按钮点击后跳转的视角，最有效的方法是覆盖或替换默认的 Home 按钮行为。以下是推荐的两种实现方案：

---

#### ✅ 方法一：使用 `Cesium.Camera.DEFAULT_VIEW_RECTANGLE` 控制位置（但不支持角度）
如果你只需要指定位置（经纬度范围），可以如下设置：

```plain
Cesium.Camera.DEFAULT_VIEW_RECTANGLE = Cesium.Rectangle.fromDegrees(west, south, east, north);
Cesium.Camera.DEFAULT_VIEW_FACTOR = 0;

const viewer = new Cesium.Viewer('cesiumContainer', { /* 其它参数 */ });
```

##### 🧭 `Cesium.Camera.DEFAULT_VIEW_RECTANGLE`
+ **作用**：设置 **Home（默认视图）按钮**初始视野所展示的地理范围（一个矩形区域）。
+ **类型**：`Rectangle`，通常通过 `Cesium.Rectangle.fromDegrees(west, south, east, north)` 构造，参数单位为度。
+ **用途**：指定 Viewer 创建完成后或点击 Home 时，摄像机会“尽量”将该矩形区域整体纳入视野（尤其在 3D 模式中）[lightning.umd.edu+3Cesium+3Stack Overflow+3](https://cesium.com/downloads/cesiumjs/releases/1.23/Build/Documentation/Camera.html?utm_source=chatgpt.com)[Cesium+5Cesium+5GitHub+5](https://cesium.com/learn/ion-sdk/ref-doc/Camera.html?utm_source=chatgpt.com)[Stack Overflow+1GIS 论坛+1](https://stackoverflow.com/questions/28709007/how-to-set-the-default-view-location-cesium-1-6?utm_source=chatgpt.com)。

**示例**：

```plain
Cesium.Camera.DEFAULT_VIEW_RECTANGLE =
  Cesium.Rectangle.fromDegrees(-120, 35, -118, 37);
```

此例将视野框限定为西经 120° 至 118°，北纬 35° 至 37° 的区域。

---

##### 🎯 `Cesium.Camera.DEFAULT_VIEW_FACTOR`
+ **作用**：控制相机与上述矩形之间的距离 **缩放因子**。换句话说，是相机在渲染该矩形后，会“退后”还是“靠近”。
+ **类型**：`Number`。
+ **含义**：
    - 设置为 `0`：相机精确贴合 `DEFAULT_VIEW_RECTANGLE`，矩形正好填满视野；
    - 大于 `0`：相机会退得更远（即看到更宽广范围，但目标矩形显得更小）；
    - 小于 `0`（不常用）：相机会更靠近目标矩形[cesium.xin](https://cesium.xin/cesium/cn/Documentation1.95/Camera.html?utm_source=chatgpt.com)[Google Groups+3osgl.grf.bg.ac.rs+3GitHub+3](https://osgl.grf.bg.ac.rs/cesium/Build/Documentation/Camera.html?utm_source=chatgpt.com)。

默认值通常为 `1.5`（Cesium 早期版本）到 `2.5`（新版）不等，意味着默认 Home 视图会稍微显示更大的范围，而不是精准的矩形视野[osgl.grf.bg.ac.rs](https://osgl.grf.bg.ac.rs/cesium/Build/Documentation/Camera.html?utm_source=chatgpt.com)[Cesium](https://cesium.com/downloads/cesiumjs/releases/1.23/Build/Documentation/Camera.html?utm_source=chatgpt.com)[Cesium](https://cesium.com/downloads/cesiumjs/releases/1.8/Build/Documentation/Camera.html?utm_source=chatgpt.com)。

---

#### ⚙️ 方法二：完全自定义 Home 按钮命令（支持全自定义视角，包括位置和角度）
直接覆盖 Home 按钮的执行命令（内部 `_command` 或 `viewModel.command.beforeExecute`）：

```plain
viewer.homeButton.viewModel.command.beforeExecute.addEventListener(function(e) {
  e.cancel = true;
  viewer.camera.flyTo({
    destination: Cesium.Rectangle.fromDegrees(west, south, east, north), // 或 Cartesian3.fromDegrees(x, y, height)
    orientation: {
      heading: Cesium.Math.toRadians(yourHeading),
      pitch: Cesium.Math.toRadians(yourPitch),      // 负值为俯视
      roll: Cesium.Math.toRadians(yourRoll)
    },
    duration: 1.5 // 飞行时长，可自定义
  });
});
```

这是一个广泛推荐的做法，可完全控制目标位置 + 方向参数 ([Stack Overflow](https://stackoverflow.com/questions/28709007/how-to-set-the-default-view-location-cesium-1-6?utm_source=chatgpt.com))。

---

#### 🎯 选哪个方法？
| 目标需求 | 推荐方式 |
| --- | --- |
| 仅设置大致位置（无角度） | 使用 DEFAULT_VIEW_RECTANGLE |
| 设置位置 + 自定义角度（更专业） | 覆盖 Home 按钮命令 |


---

#### 📌 示例代码（定制 Home 视角）的完整参考：
```plain
const viewer = new Cesium.Viewer('cesiumContainer', { /* options */ });

viewer.homeButton.viewModel.command.beforeExecute.addEventListener(function(e) {
  e.cancel = true;
  viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(lon, lat, height),
    orientation: {
      heading: Cesium.Math.toRadians(heading),
      pitch: Cesium.Math.toRadians(pitch),
      roll: Cesium.Math.toRadians(roll)
    },
    duration: 2.0
  });
});
```

替换 `lon`, `lat`, `height`, `heading`, `pitch`, `roll` 为你所需的具体视角数值。

---

总之：

+ 对简单位置跳转，可设置 `DEFAULT_VIEW_RECTANGLE`；
+ 对复杂角度与位置控制，推荐重写 Home 按钮命令，自定义飞行视角。

如果你还想查看官方文档或最新 Cesium 版本是否已有内置支持，可再找我，我可以帮你进一步查询～



## 5、坐标转换
### 5.0 坐标系统对比
#### 1. Cesium屏幕坐标（Cartesian2）
+ 原点 ：Canvas元素的左上角（0, 0）
+ 范围 ：相对于Canvas元素的像素坐标
+ 用途 ：Cesium内部的屏幕坐标计算

#### 2. 浏览器视口坐标（Viewport Coordinates）
+ 原点 ：浏览器可视区域的左上角（0, 0）
+ 范围 ：相对于整个浏览器窗口的可视区域
+ 获取方式 ： event.clientX 、 event.clientY

#### 3. 文档坐标（Document Coordinates）
+ 原点 ：整个HTML文档的左上角（0, 0）
+ 范围 ：包含滚动区域的完整文档
+ 获取方式 ： event.pageX 、 event.pageY

### 3.1 实例化一个笛卡尔空间直角坐标系
```javascript
  // 实例化一个笛卡尔坐标(x轴，y轴，z轴) z轴不是高度
  const position = new Cesium.Cartesian3(100, 100, 100)
  console.log(position)
```

### 3.2 经纬度转笛卡尔坐标
```javascript
// 经纬度转笛卡尔(经度，纬度，高度)  高度可以不传  默认是0  高度是相对于地表高度 单位是米
  const Cartesian1 = Cesium.Cartesian3.fromDegrees(110, 20)
  const Cartesian2 = Cesium.Cartesian3.fromDegrees(110, 20, 100)
  console.log(Cartesian1)
  console.log(Cartesian2)
```

小提问：为什么实例化坐标系的时候，需要 new ，而在经纬度转笛卡尔坐标系的时候，不需要  new

> 答：可以按住 ctrl 键，进入Cartesian3 源码部分来看，这就是一个类，实例化当然就要 new!
>
> <!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730015274982-0d11cf07-67d9-46a3-a956-032bc9cee2b1.png)
>
> 而 fromGegrees 是一个方法
>
> <!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730015277206-123bf328-3a45-42d6-b68b-98936b70bdfb.png)
>

### 3.3 笛卡尔转经纬度
```javascript
  // 笛卡尔转经纬度(分两步)
  // 1、笛卡尔转弧度坐标
  const Cartographic = Cesium.Cartographic.fromCartesian(Cartesian3)
  console.log(Cartographic) //高度在弧度坐标中
  // 2、弧度坐标转角度坐标
  let lon = Cesium.Math.toDegrees(Cartographic.longitude)
  let lat = Cesium.Math.toDegrees(Cartographic.latitude)
  // let lon = 180 / Math.PI * Cartographic.longitude   // 数学方法
  // let lat = 180 / Math.PI * Cartographic.latitude    // 数学方法
  console.log(lon, lat)
  // js小数位精度问题 0.1 + 0.2 != 0.3
```

经典面试题：为什么 0.1 +0.2 != 0.3

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730015405080-197c145c-5c4a-4dc0-a021-e3630b8ddd67.png)

### 3.4 获取cartesian3对应的cartesian2
`<font style="color:rgb(0, 0, 0);">viewer.scene.cartesianToCanvasCoordinates(position,result)</font>`

| <font style="color:rgb(0, 0, 0);">方法</font> | <font style="color:rgb(0, 0, 0);">输入类型</font> | <font style="color:rgb(0, 0, 0);">返回类型</font> | <font style="color:rgb(0, 0, 0);">描述</font> |
| --- | --- | --- | --- |
| `<font style="color:rgb(0, 0, 0);">scene.cartesianToCanvasCoordinates(Cartesian3 position, Cartesian2 result)</font>` | `<font style="color:rgb(0, 0, 0);">Cartesian3</font>`<br/><font style="color:rgb(0, 0, 0);"> 世界坐标</font> | `<font style="color:rgb(0, 0, 0);">Cartesian2</font>`<br/><font style="color:rgb(0, 0, 0);"> 画布像素坐标（屏幕坐标）</font> | <font style="color:rgb(0, 0, 0);">将三维点投影为 Canvas 上的像素坐标，用于定位 HTML 覆盖层(</font>[lightning.umd.edu](https://lightning.umd.edu/~mpeterson/Build/Documentation/Scene.html?utm_source=chatgpt.com)<br/><font style="color:rgb(0, 0, 0);">)</font> |
| `<font style="color:rgb(0, 0, 0);">SceneTransforms.worldToWindowCoordinates(scene, position)</font>` | <font style="color:rgb(0, 0, 0);">同上</font> | `<font style="color:rgb(0, 0, 0);">Cartesian2</font>`<br/><font style="color:rgb(0, 0, 0);"> 窗口坐标</font> | <font style="color:rgb(0, 0, 0);">兼容大多数情况下的屏幕坐标</font> |
| `<font style="color:rgb(0, 0, 0);">SceneTransforms.worldToDrawingBufferCoordinates(scene, position)</font>` | <font style="color:rgb(0, 0, 0);">同上</font> | `<font style="color:rgb(0, 0, 0);">Cartesian2</font>`<br/><font style="color:rgb(0, 0, 0);"> 绘图缓冲区坐标</font> | <font style="color:rgb(0, 0, 0);">当存在浏览器缩放或设备像素比高时，返回更准确的像素位置(</font>[Cesium](https://cesium.com/learn/cesiumjs/ref-doc/SceneTransforms.html?utm_source=chatgpt.com)<br/><font style="color:rgb(0, 0, 0);">)</font> |


### 3.5 通过点击获取cartesian2、浏览器坐标
```javascript
  viewer.scene.canvas.addEventListener('click', function (e) {
    console.log(e, 'e')
    const windowPosition = new Cesium.Cartesian2(e.clientX, e.clientY)
    console.log(windowPosition, 'windowPosition')
    
```

```javascript
{
  "isTrusted": true,
  "altKey": false,
  "altitudeAngle": 1.5707963267948966,
  "azimuthAngle": 0,
  "bubbles": true,
  "button": 0,
  "buttons": 0,
  "cancelBubble": false,
  "cancelable": true,
  "clientX": 583,
  "clientY": 327,
  "composed": true,
  "ctrlKey": false,
  "currentTarget": null,
  "defaultPrevented": false,
  "detail": 1,
  "eventPhase": 0,
  "fromElement": null,
  "height": 1,
  "isPrimary": false,
  "layerX": 385,
  "layerY": 298,
  "metaKey": false,
  "movementX": 0,
  "movementY": 0,
  "offsetX": 385,
  "offsetY": 298,
  "pageX": 583,
  "pageY": 327,
  "persistentDeviceId": 0,
  "pointerId": 1,
  "pointerType": "mouse",
  "pressure": 0,
  "relatedTarget": null,
  "returnValue": true,
  "screenX": 583,
  "screenY": 414,
  "shiftKey": false,
  "sourceCapabilities": {"firesTouchEvents": false},
  "srcElement": "canvas",
  "tangentialPressure": 0,
  "target": "canvas",
  "tiltX": 0,
  "tiltY": 0,
  "timeStamp": 695129.2000000477,
  "toElement": null,
  "twist": 0,
  "type": "click",
  "view": {"window": "Window", "self": "Window", "document": "document", "name": "", "location": "Location"},
  "which": 1,
  "width": 1,
  "x": 583,
  "y": 327
}
```

原生click事件的 e.clientX 和 e.clientY 是相对于整个浏览器窗口的坐标，而不是相对于canvas的坐标；ScreenSpaceEventHandler获取的事件对象是cartesian2，是相对于canvas的坐标。

```javascript
  // 使用Cesium的ScreenSpaceEventHandler而不是原生canvas事件
  clickHandler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas)
  clickHandler.setInputAction(function (movement) {
    const windowPosition = movement.position
    console.log(windowPosition, 'windowPosition - cartesian2坐标')
  })
    
```

### 3.5 通过屏幕坐标获取三维坐标
```javascript
const pickRay = viewer.camera.getPickRay(Cartesian2)
const carto = viewer.scene.globe.pick(pickRay, viewer.scene)
```

### 3.4 屏幕显示鼠标坐标
思路：鼠标移动事件——转换坐标——可视化

## 4、相机
### 4.1 setView
```javascript

  const position = Cesium.Cartesian3.fromDegrees(110, 20, 20000)

  // setView通过定义相机的目的地，直接跳转到目的地
  viewer.camera.setView({
    destination: position, //相机坐标
    orientation: { //默认(0,-90,0)
      heading: Cesium.Math.toRadians(0),
      pitch: Cesium.Math.toRadians(0),
      roll: Cesium.Math.toRadians(0),
    }
  })
```



### 4.2 flyTo
```javascript
  // flyTo跟setView相比带飞行动画，可以设置飞行时长
  viewer.camera.flyTo({
    destination: position,
    duration: 3//飞行时长
  })
```



### 4.3 lookAt
```javascript
  // lookAt将相机固定在设置的点位上，可以选择视角，不能改变位置 ,range表示距离该点的距离
 const position2 = Cesium.Cartesian3.fromDegrees(110, 20)
  viewer.camera.lookAt(
    position2,
    new Cesium.HeadingPitchRange(
      Cesium.Math.toRadians(0),
      Cesium.Math.toRadians(-90),
      20000
    )
  )
```

```typescript
// 解除锁定，恢复相机的自由控制
baseMapRef.value.viewer.camera.lookAtTransform(Cesium.Matrix4.IDENTITY)
```

## 5、实体
```javascript
<template>
  <div id="cesiumContainer">
  </div>

</template>

<script setup>
import * as Cesium from 'cesium'
import { onMounted } from 'vue'

Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJmMDY1ZmUxNi1mMGNhLTQ1NDEtYTU2YS0wNTUwZDJhOWNkNmEiLCJpZCI6MTE1MTg3LCJpYXQiOjE3MDA0NDUxNDB9.wdc1z2bc8UV2q_FpcuB5QKtRx8OYLKq4KI3gDs6-gA8'
onMounted(() => {
  // viewer是操控地图api的开始
  const viewer = new Cesium.Viewer('cesiumContainer', {
    selectionIndicator: false,//隐藏选中框
    infoBox: false//隐藏右上角信息框
  })
  // 二维：    要素---->数据源---->图层---->地图
  // 三维：    实体---->地图

  // 点
  // 写法一：
  const point = new Cesium.Entity({
    position: Cesium.Cartesian3.fromDegrees(120, 30),
    id: 'point', //唯一且必要
    point: {
      color: Cesium.Color.BLUE, //颜色
      pixelSize: 10//像素大小
    }
  })
  console.log(point)
  viewer.entities.add(point)  //地图添加实体
   consloe.log(viewer.Entities)  //地图已有实体
    
  // 直接使用笛卡尔坐标
  // {x: -4130585.9558334257, y: 2898223.430728178, z: -3888142.9475070233}
  viewer.entities.add({
    position: new Cesium.Cartesian3(
      -4130585.9558334257,
      2898223.430728178,
      -3888142.9475070233
    ),
    point: {
      color: Cesium.Color.RED, //颜色
      pixelSize: 50, //像素大小
    },
  });
  // 写法二：
  const point2 = viewer.entities.add({
    position: Cesium.Cartesian3.fromDegrees(120, 31),
    id: 'point2',
    point: {
      color: Cesium.Color.RED, //颜色
      pixelSize: 10//像素大小
    }
  })
  // 标注
  const billboard = viewer.entities.add({
    position: Cesium.Cartesian3.fromDegrees(116, 40, 30),
    billboard: {
      image: '/src/assets/position.png',
      scale: 0.3,
      color: new Cesium.Color(255 / 255, 0 / 255, 0 / 255) // 1对应255
    }
  })

  // 文本
  const label = viewer.entities.add({
    position: Cesium.Cartesian3.fromDegrees(112, 30),
    label: {
      text: 'Cesium',
      showBackground: true,
      backgroundColor: new Cesium.Color(0.165, 0.165, 0.165, 0.8),
      fillColor: Cesium.Color.YELLOWGREEN
    }
  })

  // 线  
  const polyline = viewer.entities.add({
    polyline: {
      positions: Cesium.Cartesian3.fromDegreesArray([120, 20, 121, 20, 121, 21]), //得到一个笛卡尔坐标数组
      width: 10,
      material: Cesium.Color.fromCssColorString('#fff'), //颜色字符串
    }
  })


  // 多边形
  const polygon = viewer.entities.add({
    polygon: {
      hierarchy: {
        positions: Cesium.Cartesian3.fromDegreesArray([120, 25, 121, 25, 121, 26]),
      },
      material: Cesium.Color.fromRandom().withAlpha(0.5), //随机颜色   带透明度
      height: 100000, //指定多边形相对于椭球表面的高度
      extrudedHeight: 200000, //指定多边形的凸出面相对于椭球面的高度
      outline: true,
      outlineColor: Cesium.Color.fromCssColorString('#fff'),
      fill: false //是否填充
    }
  })

  // 盒子
  const box = viewer.entities.add({
    position: Cesium.Cartesian3.fromDegrees(118, 30, 3000),
    box: {
      dimensions: new Cesium.Cartesian3(100, 200, 300),
      material: Cesium.Color.YELLOWGREEN
    }
  })


  // 椭圆
  const ellipse = viewer.entities.add({
    position: Cesium.Cartesian3.fromDegrees(119, 30),
    ellipse: {
      semiMajorAxis: 500,
      semiMinorAxis: 300,
      rotation: Math.PI / 4,
      material: Cesium.Color.BLUEVIOLET
    }
  })

  //矩形
  const rectangle = viewer.entities.add({
    rectangle: {
      coordinates: Cesium.Rectangle.fromDegrees(120, 40, 123, 45),  //左下右上
      extrudedHeight: 30000,
      material: '/src/assets/dog.jpg'  //可以用自定义图片填充
    }
  })
  viewer.zoomTo(rectangle) //跳转到实体
})
</script>

<style scoped>
#cesiumContainer {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
</style>

```



### 5.1 点实体
```javascript
console.log(point);
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730017620506-f4b5402c-9877-4c75-ada5-57e5e0354f70.png)

### 5.2 地图实体
```javascript
console.log(viewer.Entities)
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730017632290-ae8a8a78-6235-4521-bfab-3d0858de0bf3.png)

### 5.3 颜色对象
```javascript
  console.log(Cesium.Color.RED)
  console.log(new Cesium.Color(1,0,0)); // 1对应255，也可以这样写（255/255 ， 0/255 ， 0/255）
  Cesium.Color.fromCssColorString('#fff'), //颜色字符串
  Cesium.Color.fromRandom().withAlpha(0.5), //随机颜色   带透明度
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730017640488-02d43360-52f4-4585-a9c9-2e9ba7f8eb8d.png)

### 5.4 线实体
```javascript
  // 线
  const polyline = viewer.entities.add({
    polyline:{
      positions:Cesium.Cartesian3.fromDegreesArray([114.40,30,114.80,30,114.80,31]),// 一维数组
        // 得到一个笛卡尔坐标数组
      width: 10,
      material: Cesium.Color.fromCssColorString('#fff'), //颜色字符串
    }
  })

```



### 5.疑难杂症
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730017776185-f85cc956-5075-4d16-a12d-93e3beaf9be1.png)

有时候会自动添加这些引入，可能会报错，不需要就直接删除了

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730017782854-750f5f7b-ae47-491e-b0ba-6c69248db837.png)



## 6、组合实体
```javascript
<template>
  <div id="cesiumContainer">
  </div>

</template>

<script setup>
import * as Cesium from 'cesium'
import { onMounted } from 'vue'

Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJmMDY1ZmUxNi1mMGNhLTQ1NDEtYTU2YS0wNTUwZDJhOWNkNmEiLCJpZCI6MTE1MTg3LCJpYXQiOjE3MDA0NDUxNDB9.wdc1z2bc8UV2q_FpcuB5QKtRx8OYLKq4KI3gDs6-gA8'
onMounted(() => {
  // viewer是操控地图api的开始
  const viewer = new Cesium.Viewer('cesiumContainer', {
    selectionIndicator: false,//隐藏选中框
    infoBox: false//隐藏右上角信息框
  })
  // 二维  {type:'point'}
  // 三维  {point:{},polygon:{}} 这样写的好处就是一个实体可以串联多个对象
  // 组合式的实体
  const entity = viewer.entities.add({
    position: Cesium.Cartesian3.fromDegrees(120, 30, 100),
    label: {
      text: 'xx小区',
      // 像素偏移，（左负右正，上负下正）
        // 注意，需要new
      pixelOffset: new Cesium.Cartesian2(0, -50)
    },
    billboard: {
      image: '/src/assets/position.png',
      scale: 0.3,
      color: Cesium.Color.YELLOW
    },
    polyline: {
      positions: Cesium.Cartesian3.fromDegreesArrayHeights([120, 30, 0, 120, 30, 100]) //每三个元素构成一个笛卡尔坐标
    }
  })
  console.log(viewer.entities)
  viewer.zoomTo(entity)

})
</script>

<style scoped>
#cesiumContainer {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
</style>

```

## 7、实体删除
```javascript
<template>
  <div id="cesiumContainer">
  </div>

  <button @click="toDel" class="btn">删除</button>

</template>

<script setup>
import * as Cesium from 'cesium'
import { onMounted } from 'vue'
// 二维：    100红点---->数据源---->图层---->地图  100蓝点---->数据源---->图层---->地图
// 三维：    把空数组当数据源使用
let redList = []
const toDel = () => {
  // 1、直接删除
  // viewer.entities.remove(point)
  // 2、通过ID删除
  // viewer.entities.removeById('point666')
  // 3、先查后删
  // const entity = viewer.entities.getById('point666')
  // viewer.entities.remove(entity)
  // 4、全部删除
  // viewer.entities.removeAll()
  // 5、分类删除
  // redList.forEach(item => {
  //   viewer.entities.remove(item)
  // })
  // redList = []  //地图上的实体确实删除了，但是数组中的数据并没有删除，所以不要忘了
}
// 在onMounted中定义的变量自然是不能在外面拿到的，所以先在外面定义变量，再onMounted中赋值
let viewer, point
Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJmMDY1ZmUxNi1mMGNhLTQ1NDEtYTU2YS0wNTUwZDJhOWNkNmEiLCJpZCI6MTE1MTg3LCJpYXQiOjE3MDA0NDUxNDB9.wdc1z2bc8UV2q_FpcuB5QKtRx8OYLKq4KI3gDs6-gA8'
onMounted(() => {
  // viewer是操控地图api的开始
  viewer = new Cesium.Viewer('cesiumContainer', {
    selectionIndicator: false,//隐藏选中框
    infoBox: false//隐藏右上角信息框
  })

  point = viewer.entities.add({
    id: 'point666',
    position: Cesium.Cartesian3.fromDegrees(121, 30),
    point: {
      pixelSize: 20,
      color: Cesium.Color.RED
    }
  })
  redList.push(point)
  let red1 = viewer.entities.add({
    position: Cesium.Cartesian3.fromDegrees(121.0001, 30),
    point: {
      pixelSize: 20,
      color: Cesium.Color.RED
    }
  })
  redList.push(red1)
  let red2 = viewer.entities.add({
    position: Cesium.Cartesian3.fromDegrees(121.0002, 30),
    point: {
      pixelSize: 20,
      color: Cesium.Color.RED
    }
  })
  redList.push(red2)

  viewer.entities.add({
    position: Cesium.Cartesian3.fromDegrees(121.0004, 30),
    point: {
      pixelSize: 20,
      color: Cesium.Color.BLUE
    }
  })
  viewer.zoomTo(point)
})
</script>

<style scoped>
#cesiumContainer {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
.btn {
  position: absolute;
  left: 50px;
  top: 50px;
  z-index: 999;
}
</style>

```



## 8、CallbackProperty
```javascript
  const polyline = viewer.entities.add({
    polyline:{
     positions: new Cesium.CallbackProperty(() => {
        console.log(1)
        num += 0.001
        num2 +=0.003
        lon = 120 + num
        lat = 30 + num2
        if (lon < 121) {
          return Cesium.Cartesian3.fromDegreesArray([120, 30, lon, lat])
        } else {
          // 这个函数的性质就是return后会重复执行
          // 所以给positions赋值一个新的对象,不再需要CallbackProperty提供了，以此跳出循环   
          polyline.polyline.positions = Cesium.Cartesian3.fromDegreesArray([120, 30, 121, 31])
        }
      }, false),
      width: 6,
      material: Cesium.Color.YELLOW
    }
  })
```

## 9、datasource
### 9.1 geojson
```javascript
  // 利用turf转一个GeoJson数据
  const linestring = turf.lineString([
    [-24, 63],
    [-23, 60],
    [-25, 65],
    [-20, 69],
  ]);
  // 返回的是 promise 对象
  const promise = Cesium.GeoJsonDataSource.load(linestring); // 可以加载url
  promise.then((res) => {
    // res是一个datasource，有entities属性
    const entity = res.entities.values[0];
    viewer.entities.add(entity);
    // entities 和 dataSources 都是viewer的两大属性，dataSource属性是一个 DataSourceCollection 对象
    console.log(viewer.dataSources);
  });


  const polygon = turf.polygon([
    [
      [-5, 52],
      [-4, 56],
      [-7, 54],
      [-5, 52],
    ],
  ]);
  Cesium.GeoJsonDataSource.load(polygon).then((res) => {
    // 除了entities可以add实体，dataSource同样可以add
    viewer.dataSources.add(res);
    // zoomTo不仅可以跳entitie,还可以跳datasource
    viewer.zoomTo(res);
  });


  const multiLine = turf.multiLineString([
    [
      [0, 0],
      [4, 4],
    ],
    [
      [6, 6],
      [10, 10],
    ],
  ]);
  const promise1 = Cesium.GeoJsonDataSource.load(multiLine);
  // 可以直接添加promise对象
  viewer.dataSources.add(promise);
  // 同样可以直接跳转到promise对象
  //  zoomTo(target: Entity | Entity[] | EntityCollection | DataSource  | Promise<Entity |
  viewer.zoomTo(promise);
```

如果geojson中是点数据，会默认转为billboard

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730019057815-a45395c4-a2e1-4b28-907d-d61350f60b38.png)

### 9.2 topojson
```javascript
  // 加载topoJson数据
  const promise = Cesium.GeoJsonDataSource.load('/src/assets/usa.topojson')
  viewer.dataSources.add(promise)
  viewer.zoomTo(promise)
```



### 9.3 KML
```javascript
  // 加载kml数据
  const promise2 = Cesium.KmlDataSource.load("/src/assets/gdp2008.kmz");
  viewer.dataSources.add(promise);
  viewer.zoomTo(promise);

```



### 9.4 czml数据
```javascript
    viewer  = new Cesium.Viewer("viewer", {
    infoBox: false,
    // animation: false, //不隐藏动画控件
    // timeline: false, //不隐藏时间轴
    shouldAnimate:true,// 开启场景动画
  });
...
// 加载czml数据
  Cesium.CzmlDataSource.load("/src/assets/Vehicle.czml").then((res) => {
    viewer.dataSources.add(res);
    let entity = res.entities.getById("Vehicle");
    viewer.trackedEntity = entity; // trackedEntity 可以实现一直移动相机跟踪entity目标
  });
```



## 10、primitive图元
```javascript
  // entity
  // 调用方便，封装完美
  // 是基于primitive

  // primitive
  // 更接近底层，性能消耗较小，要素很多时使用primitive
  // 可以绘制高级图形
  // 由Geometry（几何形状）、（Apperance）外观组成

  // 1、椭圆实体
  let primitive = new Cesium.Primitive({
    // primitive包括geometryIntances和appearance
    geometryInstances: new Cesium.GeometryInstance({
      geometry: new Cesium.EllipseGeometry({
        center: Cesium.Cartesian3.fromDegrees(-100.0, 20.0),
        semiMinorAxis: 500000.0,
        semiMajorAxis: 1000000.0,
        rotation: Cesium.Math.PI_OVER_FOUR,
        vertexFormat: Cesium.VertexFormat.POSITION_AND_ST,
      }),
    }),
    appearance: new Cesium.EllipsoidSurfaceAppearance({
      // fromType 可以从很多预制好的样式中选择
      // material: Cesium.Material.fromType("Checkerboard"),
      material: Cesium.Material({
        fabric: {
          type: "Color",
          uniforms: {
            color: new Cesium.Color(1.0, 1.0, 0.0, 1.0),
          },
        },
      }),
    }),
  });

  viewer.scene.primitives.add(primitive);

  // 2. Draw different instances each with a unique color
  // 2.1 矩形实例
  let rectangleInstance = new Cesium.GeometryInstance({
    geometry: new Cesium.RectangleGeometry({
      rectangle: Cesium.Rectangle.fromDegrees(-140.0, 30.0, -100.0, 40.0),
      vertexFormat: Cesium.PerInstanceColorAppearance.VERTEX_FORMAT,
    }),
    id: "rectangle",
    attributes: {
      color: new Cesium.ColorGeometryInstanceAttribute(0.0, 1.0, 1.0, 0.5),
    },
  });

  // 2.2 多边形实例
  let plygonInstance = new Cesium.GeometryInstance({
    geometry:new Cesium.PolygonGeometry({
    polygonHierarchy: new Cesium.PolygonHierarchy(
      Cesium.Cartesian3.fromDegreesArray([
      -100.0, 45.0,-100.0,25.0,-90.0,35
      ])
    ),
  }),
    attributes: {
      color: new Cesium.ColorGeometryInstanceAttribute(0.0, 1.0, 1.0, 0.5),
    },
  });
  // 椭球实例
  // var ellipsoidInstance = new Cesium.GeometryInstance({
  //   geometry: new Cesium.EllipsoidGeometry({
  //     radii: new Cesium.Cartesian3(500000.0, 500000.0, 1000000.0),
  //     vertexFormat: Cesium.VertexFormat.POSITION_AND_NORMAL,
  //   }),
  //   modelMatrix: Cesium.Matrix4.multiplyByTranslation(
  //     Cesium.Transforms.eastNorthUpToFixedFrame(
  //       Cesium.Cartesian3.fromDegrees(-95.59777, 40.03883)
  //     ),
  //     new Cesium.Cartesian3(0.0, 0.0, 500000.0),
  //     new Cesium.Matrix4()
  //   ),
  //   id: "ellipsoid",
  //   attributes: {
  //     color: Cesium.ColorGeometryInstanceAttribute.fromColor(Cesium.Color.AQUA),
  //   },
  // });
  viewer.scene.primitives.add(
    new Cesium.Primitive({
      // 组合实体
      geometryInstances: [rectangleInstance, plygonInstance],
      appearance: new Cesium.PerInstanceColorAppearance(),
    })
  );

```



## 11、3DTiles加载
### 11.1 添加官方三维瓦片数据
需要先登录

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730019518283-636628bb-6f93-46bd-a936-468f69809ef5.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730019522259-3541f9f6-a976-4bff-bbc0-507ab80e289e.png)

### 11.2 primitive添加
```javascript
  // 3d瓦片加载在 primitive里面
  const tileset = viewer.scene.primitives.add(
    new Cesium.Cesium3DTileset({
      // url:Cesium.IonResource.fromAssetId(69380)
      url:Cesium.IonResource.fromAssetId(75343)
    })
  )
  // zoomTo也可以直接跳转到3D瓦片那里
  viewer.zoomTo(tileset)
  
  // 加载自己的瓦片资源
  const tileset1 = viewer.scene.primitives.add(
    new Cesium.Cesium3DTileset({
      url:'/src/assets/b3dm/tileset.json'
    })
  )
  viewer.zoomTo(tileset1)
```

### 11.3 效果展示
纽约建筑白模数据

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730019579678-11f39866-317c-489c-a6f0-162414a9cb7a.png)

曼哈顿倾斜摄影数据

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730019584896-d934d2e8-094a-4c3e-8221-2ab97eb55165.png)

高精度瓦片数据

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730019590832-b125aaf5-6607-4370-8a6d-bcdecc88bea7.png)





## terrain数据加载
[https://juejin.cn/post/7429245024230228009](https://juejin.cn/post/7429245024230228009)

## 栅格瓦片加载
> 关于不同的瓦片切分规则，见 /GIS基础知识/OGC
>

#### **加载瓦片的两种核心方法**
Cesium提供两种主要方式加载栅格瓦片：`UrlTemplateImageryProvider` 和 `TileMapServerImageryProvider`。



### **1. UrlTemplateImageryProvider**
**适用场景**：灵活自定义瓦片URL模板，支持TMS、Google等多种格式。  
**核心原理**：通过URL模板拼接瓦片坐标（X, Y, Z），需手动处理坐标系差异。  

#### **常用属性**
| 属性名 | 说明 |
| --- | --- |
| `url` | 瓦片URL模板，支持`{z}`, `{x}`, `{y}`等变量，需匹配坐标系。 |
| `tilingScheme` | **关键属性**：指定瓦片坐标系方案（默认`WebMercatorTilingScheme`）。 |
| `rectangle` | 瓦片覆盖的地理范围（经纬度矩形）。 |
| `tileWidth/tileHeight` | 瓦片像素尺寸（默认256x256）。 |
| `customTags` | 自定义URL参数转换函数（如Y轴翻转）。 |


#### **加载TMS服务的代码示例**
**问题分析**：TMS原点在左下角（Y轴向上），而Cesium默认使用左上角原点（Y轴向下），需翻转Y坐标。  

```javascript
// 方法1：通过tilingScheme指定地理坐标系（适用于非Web Mercator投影的TMS）
const tmsProvider1 = new Cesium.UrlTemplateImageryProvider({
  url: 'http://your-tms-server/{z}/{x}/{y}.png', // TMS原始URL（Y向上）
  tilingScheme: new Cesium.GeographicTilingScheme(), // 使用经纬度坐标系（WGS84）
  rectangle: Cesium.Rectangle.fromDegrees(73, 18, 135, 54), // 中国区域范围
  tileWidth: 256,
  tileHeight: 256
});

// 方法2：强制转换Y轴（适用于Web Mercator投影的TMS，需与Cesium投影一致）
const tmsProvider2 = new Cesium.UrlTemplateImageryProvider({
  url: 'http://your-tms-server/{z}/{x}/{y_reversed}.png', // 自定义Y变量名
  tilingScheme: new Cesium.WebMercatorTilingScheme(), // 使用Web Mercator投影
  rectangle: Cesium.Rectangle.fromDegrees(73, 18, 135, 54),
  customTags: {
    // 关键：将Cesium的Y（向下）转换为TMS的Y（向上）
    y_reversed: (provider, x, y, level) => {
      const maxY = Math.pow(2, level) - 1; // 层级Z对应的最大Y值
      return maxY - y; // 翻转Y坐标
    }
  }
});

// 添加到场景
viewer.imageryLayers.addImageryProvider(tmsProvider2);
```



### **2. TileMapServerImageryProvider**
**适用场景**：直接加载符合TMS规范的服务，自动处理坐标系转换（需服务遵循标准）。  
**核心原理**：基于TMS标准接口，内部封装了Y轴翻转逻辑，简化调用。  

#### **常用属性**
| 属性名 | 说明 |
| --- | --- |
| `url` | TMS服务根URL（如`http://your-tms-server/`）。 |
| `credit` | 数据来源标注（可选）。 |
| `maximumLevel` | 最大加载层级（默认自动获取）。 |
| `projection` | 投影方式（默认与Cesium一致，即Web Mercator）。 |


#### **加载TMS服务的代码示例**
```javascript
// 直接指定TMS服务URL（无需手动处理Y轴）
const tmsProvider = new Cesium.TileMapServerImageryProvider({
  url: 'http://your-tms-server/', // TMS服务根路径，需包含瓦片层级/坐标路径
  // 可选：若TMS服务使用非Web Mercator投影，需指定projection
  // projection: new Cesium.GeographicProjection()
});

// 添加到场景
viewer.imageryLayers.addImageryProvider(tmsProvider);
```



#### **关键对比与注意事项**
| 方法 | 优势 | 劣势 | 适用场景 |
| --- | --- | --- | --- |
| `UrlTemplateImageryProvider` | 高度灵活，支持任意URL格式 | 需手动处理坐标系转换逻辑 | 非标准TMS服务、自定义URL结构 |
| `TileMapServerImageryProvider` | 自动适配TMS规范，代码简洁 | 依赖服务严格遵循TMS标准 | 标准OGC-TMS服务（如GeoServer） |


**注意**：  

+ 若TMS服务使用**Web Mercator投影**（与Cesium一致），优先用`UrlTemplate`并翻转Y轴。  
+ 若TMS服务使用**经纬度投影**（如WGS84），需通过`GeographicTilingScheme`或`GeographicProjection`指定。  
+ 调试时可通过浏览器F12查看请求的瓦片URL，确认X/Y/Z是否匹配数据源。

<font style="color:rgb(34, 34, 38);"></font>

## 12、地图交互
### 12.1 点击获取坐标并添加点
```javascript
    // 点击交互
    let handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
    handler.setInputAction((event) => {
      // 拾取坐标
      let position = viewer.scene.pickPosition(event.position);
      // 点击添加点
      // 通常都会加上判断，当坐标存在时再执行后续代码
      if (position) {
        console.log(position);
        viewer.entities.add({
          position,
          point: {
            color: Cesium.Color.RED, //颜色
            pixelSize: 10, //像素大小
          },
        });
      }
    }, Cesium.ScreenSpaceEventType.LEFT_CLICK);
```



### 12.2 点击获取实体并将点高亮
```javascript
    // 点击交互
    let handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
    handler.setInputAction((event) => {
      // 拾取对象
    let pick = viewer.scene.pick(event.position)
    console.log(pick);
    if(pick && pick.id){  // pick.id 是那个实体，pick.id.id才是实体的id值
      pick.id.point.color = Cesium.Color.BLUE
    }
    }, Cesium.ScreenSpaceEventType.LEFT_CLICK);
```



获取实体

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730020312653-252be9ad-5c91-43d4-bb0e-2590de6bd4c7.png)



这里的 id 值的属性是一个实体（加载的瓦片图层里面没有 id 属性）

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730020307183-0f419727-abe5-482f-8a71-46d87728918a.png)

在Cesium中，`viewer.scene.pick`和`viewer.pickPosition`是两个用于与场景交互的不同的方法，它们的主要区别在于功能和应用场景。

1. `viewer.scene.pick`：
    - 功能：这个方法用于在给定的窗口坐标下选择一个场景中的对象（如实体、3D模型、几何体等）。
    - 返回值：如果指定的屏幕坐标上有一个对象，它返回一个`PickResult`对象，该对象包含了被选中对象的详细信息，如.primitive（图元）、.id（标识符）和.intersection（交点）等。
    - 用途：通常用于确定用户点击了场景中的哪个对象，以及在交互式应用中获取对象的属性或触发事件。
2. `viewer.pickPosition`：
    - 功能：这个方法用于获取与屏幕坐标相对应的地球表面的世界坐标（Cartesian3）。
    - 返回值：返回一个`Cartesian3`对象，表示屏幕坐标在地球表面的位置。如果无法确定位置（例如，如果屏幕坐标在地球背面或者没有地球表面与之对应），则返回`undefined`。
    - 用途：通常用于获取用户点击的地球表面的确切位置，比如在绘制几何体或放置标记时。

简而言之，`viewer.scene.pick`关注于“选择”场景中的对象，而`viewer.pickPosition`关注于获取屏幕坐标在地球表面的具体位置。在实际应用中，根据需要交互的内容选择合适的方法。例如，如果你需要知道用户点击了哪个特定的模型或物体，你会使用`viewer.scene.pick`；而如果你只是需要知道点击位置在地球上的坐标，那么`viewer.pickPosition`会是更合适的选择。

### 12.3 销毁事件
```javascript
  handler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_CLICK)
```

### 12.4 简易版画笔
```javascript
onMounted(() => {
...
  // 加载瓦片数据
  const tileset = viewer.scene.primitives.add(
    new Cesium.Cesium3DTileset({
      url: Cesium.IonResource.fromAssetId(69380),
    })
  );
  viewer.zoomTo(tileset);

    // 空数组存放坐标
  let arr = [];
  const polyline = viewer.entities.add({
    polyline: {
      positions: [],
      width: 15,
      material: Cesium.Color.BLUE,
      clampToGround:true // 贴地
    },
  });

  // 点击交互
  handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
  handler.setInputAction((event) => {

    // 拾取坐标
    let position = viewer.scene.pickPosition(event.position);
    // 点击添加点
    // 通常都会加上判断，当坐标存在时再执行后续代码
    if (position) {
      viewer.entities.add({
        position,
        point: {
          color: Cesium.Color.RED, //颜色
          pixelSize: 10, //像素大小
        },
      });
        // 将坐标保存到数组中
      arr.push(position);
        // 更新线的坐标而不是重新添加一个线实体
      polyline.polyline.positions = arr
    }
  }, Cesium.ScreenSpaceEventType.LEFT_CLICK);
    
    // 一个变量可以存放多个事件
  handler.setInputAction(() => {
    alert('结束绘制')
    viewer.entities.removeAll();// 清除所有不妥当
    viewer.entities.add(polyline);
      // 将左右鼠标的事件都清除
    handler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_CLICK)
    handler.removeInputAction(Cesium.ScreenSpaceEventType.RIGHT_CLICK)
  }, Cesium.ScreenSpaceEventType.RIGHT_CLICK);
});
```



在 Cesium 中绑定右键点击事件时，为了防止浏览器默认的右键菜单（context menu）弹出，你需要**阻止浏览器的默认行为**。有两种常见方法可以实现这一点：

---

### ✅ 方法一：在绑定事件时阻止默认行为（推荐）
给 Cesium 容器绑定 `contextmenu` 事件并调用 `event.preventDefault()`：

```javascript
// 假设你的 Viewer 是这样创建的
const viewer = new Cesium.Viewer('cesiumContainer');

// 阻止浏览器右键菜单
const canvas = viewer.scene.canvas;
canvas.addEventListener('contextmenu', function (e) {
  e.preventDefault();
});
```

这样就不会再弹出右键菜单了。

---

### ✅ 方法二：使用 Cesium 自带的右键事件 + 阻止菜单
Cesium 本身支持右键事件（`ScreenSpaceEventType.RIGHT_CLICK`）：

```javascript
const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);

handler.setInputAction(function (click) {
  // 你自己的右键逻辑
  console.log("右键点击了", click.position);
}, Cesium.ScreenSpaceEventType.RIGHT_CLICK);

// 同样也要阻止默认右键菜单
viewer.scene.canvas.addEventListener('contextmenu', function (e) {
  e.preventDefault();
});
```



### 12.5 建筑高亮
小知识：

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730021097208-c97def39-aa7b-41e5-9998-ddbdfc595181.png)

```javascript
...
onMounted(() => {
...
  // 点击交互
  handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
  let lastpick 
  handler.setInputAction((event) => {
    // 拾取对象
    let pick = viewer.scene.pick(event.endPosition) // 没有 position，只有endPosition
    if(pick){
      // 是否可以取名为防御性编程
      if(lastpick){
        lastpick.color = Cesium.Color.WHITE
      }
      pick.color = Cesium.Color.BLUE
      lastpick = pick
    }
    // 思考一：应该可以找到方法，获取到 scene上的全部实体
    // 获取全部实体，肯定对性能消耗极大
    // 只需要获取上一个实体就好了
  }, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
});
</script>


```



### 12.6 保存图片
①在地图初始化时，设置`preserverDrawingBuffer`属性为true

```tsx
    const viewer = new Cesium.Viewer("csiumContain", {
        homeButton: false,//是否显示Home按钮
        animation: false,//是否显示动画控件
        timeline: false,//是否显示时间线控件
        fullscreenButton: false,
        baseLayerPicker: false,//是否显示图层选择控件
        sceneModePicker: true, //是否显示投影方式控件
        navigationHelpButton: false, //是否显示帮助信息控件
        geocoder: false, //是否显示地名查找控件
        sceneModePicker: false,//是否显示3D/2D选择器
        contextOptions: {
            webgl: {
                alpha: true,
                depth: true,
                stencil: true,
                antialias: true,
                premultipliedAlpha: true,
                //通过canvas.toDataURL()实现截图需要将该项设置为true
                preserveDrawingBuffer: true,
                failIfMajorPerformanceCaveat: true
            }
        }
      
    })
```

②获取到viewer的canvas，然后通过a标签下载

```tsx
  // 保存当前视角影像数据
  function saveCurrentView(filename = "下载图像") {
    const canvas = viewer.current.scene.canvas;
    const imageDataUrl = canvas.toDataURL("image/png");
    const a = document.createElement("a");
    a.download = filename;
    a.href = imageDataUrl;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
```

### 12.7 Popup
点击获取到对应的屏幕坐标和经纬度坐标

使用DOM操作

随着视角移动，popup也跟随移动

## 13、三维模型
### 13.1 glTF
### 13.2 model
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730021408958-5f4e3587-b8a9-4708-8b44-1100bec177f9.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730021410707-2769a0ee-8cbe-4f6f-9853-e932cad21ea3.png)

### 13.3 加载飞机
```javascript
// 设置坐标
const position = Cesium.Cartesian3.fromDegrees(114.30,30.50,300)
// 设置方向 heading pitch roll
const orientation = Cesium.Transforms.headingPitchRollQuaternion(
  position,
  Cesium.HeadingPitchRoll.fromDegrees(0,0,0)
)

const model = viewer.entities.add({
  position,
  orientation,
  model:{
    uri:'/src/assets/Cesium_Air.glb',
    scale:0.5,
    minimumPixelSize:10 // 模型最小像素
  }
})
viewer.zoomTo(model)
```



## 14、粒子系统
```javascript
// 设置坐标
const position = Cesium.Cartesian3.fromDegrees(114.30,30.50,300)
// 设置方向 heading pitch roll
const orientation = Cesium.Transforms.headingPitchRollQuaternion(
  position,
  Cesium.HeadingPitchRoll.fromDegrees(0,0,0)
)

const model = viewer.entities.add({
  position,
  orientation,
  model:{
    uri:'/src/assets/Cesium_Air.glb',
    scale:0.5,
    minimumPixelSize:10 // 模型最小像素
  }
})
viewer.zoomTo(model)

// 在三维模型上添加粒子效果
// 火
viewer.scene.primitives.add(new Cesium.ParticleSystem({
  image:'/src/assets/fire.png',
  imageSize:new Cesium.Cartesian2(20,20),
  startScale:1.0,// 初始大小
  endScale:4.0 ,// 最后大小
  particleLife:3,// 设置每一个粒子存在的时间
  speed:5.0,//发射粒子的速度
  emitter:new Cesium.CircleEmitter(2),// 设置发射器（圆形发射器）
  // emitter:new Cessium.BoxEmitter(new Cesium.Cartesian3(10,10,10))
  emissionRate:5,// 粒子发射数量
  modelMatrix:model.computeModelMatrix(
    viewer.clock.startTime, // 时间控件中的起始时间
    new Cesium.Matrix4() // 4*4矩阵数据
  ), //设置位置
  lifetime:16,// 生命期属性为所需的持续时间
  // loop:false  // 只循环一次
}))

// 烟雾
viewer.scene.primitives.add(new Cesium.ParticleSystem({
  image:'/src/assets/smoke.png',
  imageSize:new Cesium.Cartesian2(20,20),
  startScale:1.0,// 初始大小
  endScale:4.0 ,// 最后大小
  particleLife:3,// 设置每一个粒子存在的时间
  speed:5.0,//发射粒子的速度
  emitter:new Cesium.CircleEmitter(2),// 设置发射器（圆形发射器）
  // emitter:new Cessium.BoxEmitter(new Cesium.Cartesian3(10,10,10))
  emissionRate:5,// 粒子发射数量
  modelMatrix:model.computeModelMatrix(
    viewer.clock.startTime, // 时间控件中的起始时间
    new Cesium.Matrix4() // 4*4矩阵数据
  ), //设置位置
  lifetime:16,// 生命期属性为所需的持续时间
  // loop:false  // 只循环一次
}))
```



## 15、点聚合
问题：加载的点过多，密密麻麻的，该如何处理

答：聚合

官方例子

[Hello World - Cesium Sandcastle](https://sandcastle.cesium.com/)

GeojsonDataSource的 clustering 属性的值就是聚合对象

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730021726651-a358f444-c3b7-44b3-b8c7-8d94c382e63f.png)

聚合对象的默认设置

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730021742872-647a4969-f9b6-4c89-9ced-0f96b0757212.png)

```javascript
// 定制不同数量的显示图片

const pinBuilder = new Cesium.PinBuilder();
const pin300 = pinBuilder.fromText("300+", Cesium.Color.RED, 48).toDataURL();
const pin100 = pinBuilder.fromText("100+", Cesium.Color.ORANGE, 48).toDataURL();
const pin50 = pinBuilder.fromText("50+", Cesium.Color.YELLOW, 48).toDataURL();
const pin30 = pinBuilder.fromText("30+", Cesium.Color.GREEN, 48).toDataURL();
const pin10 = pinBuilder.fromText("10+", Cesium.Color.BLUE, 48).toDataURL();

onMounted(() => {
...
  const promise = Cesium.GeoJsonDataSource.load("/src/assets/camera.json");
  promise.then((res) => {
    console.log(res);
    // 给dataSource 设置聚合属性
    res.clustering.enabled = true;
    res.clustering.pixelRange = 30;
    res.clustering.minimumClusterSize = 4;
    // 聚合事件
    res.clustering.clusterEvent.addEventListener(
      (clusterenEntities, cluster) => {
        cluster.billboard.show = true;
        cluster.label.show = false;
        if (clusterenEntities.length >= 300) {
          cluster.billboard.image = pin300;
        } else if (clusterenEntities.length >= 100) {
          cluster.billboard.image = pin100;
        } else if (clusterenEntities.length >= 50) {
          cluster.billboard.image = pin50;
        } else if (clusterenEntities.length >= 30) {
          cluster.billboard.image = pin30;
        } else if (clusterenEntities.length >= 10) {
          cluster.billboard.image = pin10;
        }
        // console.log(clusterenEntities,'clustterenEntities');
        // console.log(cluster,'cluster');
        // clusterenEntities  是一个由 entity 组合而成的数组
        // cluster 就是一个聚合对象，billboard默认是关闭的，lable默认是开启的，就是默认是用数子显示聚合对象
      }
    );

    // 自定义billboard
    let cameraPont = res.entities.values;
    cameraPont.forEach((item) => {
      item.billboard.image = "/src/assets/camera.png";
      item.billboard.scale = 0.1;
      // 这样子添加的entities，而不是dataSource；而聚合属性是属于dataSurce的
      // viewer.entities.add(item)
    });
    // 要想聚合显示，那当然得用 datasource 了
    viewer.dataSources.add(res);
    // 刚加载进入地图时，视图不会变，就不会发生聚合，这显然是不太好的;用flyto会由视图的变化，即可解决
    // viewer.zoomTo(res);
    viewer.flyTo(res)
  });
});
```



## 16、3DTiles 加载方法封装
load.js

注意：

> load3dtiles方法中
>
> // 数值越小，远距离观看时的模型精度越高
>
> maximumScreenSpaceError: 30,
>

> update3dtiles方法中
>
> const tz = -69; // 表示往下移动了69
>



```javascript
import * as Cesium from "cesium";

// 加载3dtiles
function load3dtiles(viewer, url, success) {
    if (!url) {
        alert("缺少模型地址");
        return;
    }
    let tp = viewer.scene.primitives.add(
        new Cesium.Cesium3DTileset({
            // 数值越小，远距离观看时的模型精度越高
            maximumScreenSpaceError: 30,
            url: url
        })
    );
    tp.readyPromise.then(function (tileset) {
        if (success) success(tileset);
    })
}


// 修改3dtiles位置
const tx = 0;
const ty = 0;
const tz = -69;
const rx = 0;
const ry = 0;
const rz = 0;
const scale = 1.3;
function update3dtiles(tileSet) {
    const cartographic = Cesium.Cartographic.fromCartesian(tileSet.boundingSphere.center);
  //将模型的笛卡尔坐标（tileSet.boundingSphere.center）转换为地理坐标（经度、纬度、高度）：
  //这样可以确定该模型在地球表面的位置。
    const surface = Cesium.Cartesian3.fromRadians(cartographic.longitude, cartographic.latitude, cartographic.height);
  // 将这个地理坐标转换为一个新的笛卡尔坐标，以便进行后续的平移或其他变换操作：
  // 这一步让你得到了一个可以以地球表面为基准进行操作的笛卡尔坐标。
  //通过这样的转换，保证了后续的变换（如平移、旋转等）是相对于地球表面进行的，
  //而不是简单地在笛卡尔坐标系内操作，这样可以确保在进行3D可视化时更符合实际地理位置的要求。
    const m = Cesium.Transforms.eastNorthUpToFixedFrame(surface);


    //平移
    const _tx = tx ? tx : 0;
    const _ty = ty ? ty : 0;
    const _tz = tz ? tz : 0;
    const tempTranslation = new Cesium.Cartesian3(_tx, _ty, _tz);
    const offset = Cesium.Matrix4.multiplyByPoint(m, tempTranslation, new Cesium.Cartesian3(0, 0, 0));
    const translation = Cesium.Cartesian3.subtract(offset, surface, new Cesium.Cartesian3());
    tileSet.modelMatrix = Cesium.Matrix4.fromTranslation(translation);


    //旋转及缩放
    if (rx) {
        const mx = Cesium.Matrix3.fromRotationX(Cesium.Math.toRadians(rx));
        const rotate = Cesium.Matrix4.fromRotationTranslation(mx);
        Cesium.Matrix4.multiply(m, rotate, m);
    }


    if (ry) {
        const my = Cesium.Matrix3.fromRotationY(Cesium.Math.toRadians(ry));
        const rotate = Cesium.Matrix4.fromRotationTranslation(my);
        Cesium.Matrix4.multiply(m, rotate, m);
    }


    if (rz) {
        const mz = Cesium.Matrix3.fromRotationZ(Cesium.Math.toRadians(rz));
        const rotate = Cesium.Matrix4.fromRotationTranslation(mz);
        Cesium.Matrix4.multiply(m, rotate, m);
    }


    if (scale) {
        const _scale = Cesium.Matrix4.fromUniformScale(scale);
        Cesium.Matrix4.multiply(m, _scale, m);
    }


    tileSet._root.transform = m;
}


export {
    load3dtiles,
    update3dtiles
}
```



使用

```javascript
  load3dtiles(viewer, '/src/assets/b3dm/tileset.json', (tileset)=>{
    update3dtiles(tileset)
    viewer.flyTo(tileset)
  })
```

✅` Cesium.Transforms.eastNorthUpToFixedFrame()`

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730028057146-51a1d15d-b7a7-4451-8f0a-3a239ea2293c.png)

`eastNorthUpToFixedFrame` 是 CesiumJS 中的一个函数，它用于生成一个表示在东向、北向和上方向的固定坐标系的变换矩阵。这个变换矩阵可以用于将一个点从地球的表面坐标转换到该坐标系。这通常是在处理与地面相关的三维模型时非常有用，确保模型坐标的正确定位和方向。

具体而言，`eastNorthUpToFixedFrame` 可以帮助开发者定义一个以地球坐标系统为基础的局部坐标系，而这个局部坐标系的方向是面对地球的东、北和向上的方向。这样，使用这个变换矩阵的点或模型会根据地理位置适当地 orientación 和放置。

✅ `<font style="color:rgb(0, 0, 0);background-color:rgb(238, 238, 238);">Cesium.Matrix4.multiplyByPoint(matrix, cartesian, result)</font>`

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730028665067-5a3e073e-c3f8-4ac1-b52b-c719791e76d2.png)

`multiplyByPoint` 是 CesiumJS 中的一个函数，它用于将一个点与一个矩阵相乘。这个操作的结果是得到一个新的坐标，该坐标是将原始点按照给定的变换矩阵进行变换后的结果。

在三维计算中，矩阵运算通常用于实现平移、旋转和缩放等变换操作。使用 `multiplyByPoint` 可以方便地将一个三维空间中的点利用矩阵进行这些变换，从而得到一个新的位置。这个函数对于处理三维模型的变换非常重要，因为它允许开发者灵活地应用各种空间变换。

✅ `primitive` 的 `modelMatrix` 属性

在 Cesium 中，`primitive` 的 `modelMatrix` 属性用于定义该对象在三维空间中的位置、方向和缩放。具体而言，`modelMatrix` 是一个 4x4 矩阵，它用于将模型的局部坐标转换为世界坐标。

设置 `modelMatrix` 为 `Cesium.Matrix4.fromTranslation(translation);` 的作用是通过一个平移矩阵来更新该模型的位置。`translation` 是一个三维向量，表示模型在三维空间中的位置偏移量。通过这种方式，你可以将模型移动到期望的位置。

具体来说，使用 `Cesium.Matrix4.fromTranslation(translation)` 可以达到以下效果：

1. 位置调整：将模型移动到一个特定的坐标点，以确保它在地图上的显示位置是正确的。
2. 坐标转换：将模型的局部坐标应用于世界坐标系，使其在场景中具有正确的相对位置。
3. 其他变换的基础：如果以后需要对模型进行旋转或缩放操作，可以以此平移为基础进行叠加。

总之，通过设置 `modelMatrix`，可以准确控制模型在三维空间中的显示位置，确保它符合实际需要的地理位置或相对位置。

✅ `primitive` 的 `modelMatrix` 属性

在 Cesium 中，`primitive` 的 `modelMatrix` 属性用于定义该对象在三维空间中的位置、方向和缩放。具体而言，`modelMatrix` 是一个 4x4 矩阵，它用于将模型的局部坐标转换为世界坐标。

设置 `modelMatrix` 为 `Cesium.Matrix4.fromTranslation(translation);` 的作用是通过一个平移矩阵来更新该模型的位置。`translation` 是一个三维向量，表示模型在三维空间中的位置偏移量。通过这种方式，你可以将模型移动到期望的位置。

具体来说，使用 `Cesium.Matrix4.fromTranslation(translation)` 可以达到以下效果：

1. 位置调整：将模型移动到一个特定的坐标点，以确保它在地图上的显示位置是正确的。
2. 坐标转换：将模型的局部坐标应用于世界坐标系，使其在场景中具有正确的相对位置。
3. 其他变换的基础：如果以后需要对模型进行旋转或缩放操作，可以以此平移为基础进行叠加。

总之，通过设置 `modelMatrix`，可以准确控制模型在三维空间中的显示位置，确保它符合实际需要的地理位置或相对位置。

✅ 如何控制primitive旋转

```javascript
        const mx = Cesium.Matrix3.fromRotationX(Cesium.Math.toRadians(rx));
        const rotate = Cesium.Matrix4.fromRotationTranslation(mx);
        Cesium.Matrix4.multiply(m, rotate, m);
```

每一步的 API 和对应的目的如下：

1. `Cesium.Matrix3.fromRotationX(Cesium.Math.toRadians(rx))`:
    - 作用: 这个方法创建一个围绕 X 轴旋转的 3x3 矩阵。`Cesium.Math.toRadians(rx)` 将角度转换为弧度，以便在数学运算中使用，因为三维变换通常使用弧度。
    - 目的: 生成一个旋转矩阵，使得可以按照 `rx` 指定的角度在 X 轴上旋转模型。
2. `Cesium.Matrix4.fromRotationTranslation(mx)`:
    - 作用: 这个方法将一个 3x3 的旋转矩阵（`mx`）转换为 4x4 的变换矩阵，并将平移部分设置为零（即没有平移效果）。
    - 目的: 创建一个结合了旋转的变换矩阵，以便在后续步骤中将旋转应用于模型。
3. `Cesium.Matrix4.multiply(m, rotate, m)`:
    - 作用: 这个方法将变换矩阵 `m` 和刚刚创建的旋转矩阵 `rotate` 相乘，然后将结果存储回 `m` 中。矩阵相乘会组合这些变换效果。
    - 目的: 将之前计算的旋转效果应用到当前的变换矩阵 `m` 上，更新模型的总变换，使其同时具有之前的变换和新添加的旋转。

总结来说，这几步的目的在于将模型首先在 Y 轴上进行旋转，更新其在三维空间中的方向，以便在场景中以正确的姿态显示。这种分步处理的方式使得旋转和其他变换（如平移和缩放）可以被灵活地组合在一起。

✅ `tileSet._root.transform = m;`

在这段代码中，`tileSet._root.transform = m;` 的目的是将计算出的变换矩阵（`m`）应用到 `tileSet` 的根节点，以更新该3D Tiles对象在场景中的位置、方向和缩放属性。

相关属性的作用：

1. `tileSet`:
    - 这是一个 3D Tiles 对象，用于在 Cesium 中加载和显示三维模型。在这个对象上可以进行各种变换（如平移、旋转和缩放）以正确地显示在场景中。
2. `_root`:
    - `_root` 是 `tileSet` 对象的私有属性，表示该 3D Tiles 系统的根节点。根节点是整个模型树的起始节点，所有的变换都会以根节点为基点进行。通过修改根节点的变换矩阵，可以影响整个模型的显示。
3. `transform`:
    - 这是构成每个节点在 3D 空间中位置、方向和缩放的 4x4 变换矩阵属性。将变换矩阵赋值给 `transform` 意味着更新该节点的变换，使其在场景中的形态符合计算出的变换效果。

目的：

通过执行 `tileSet._root.transform = m;`，我们将之前计算出的包括平移、旋转和缩放效果的矩阵 `m` 应用到模型。这样，模型会按照我们在代码中指定的方式正确地显示在Cesium的场景中。这个步骤确保模型在场景中的位置和方向是准确的，并能够响应用户的交互或视角变化。

✅ 

在 Cesium 中，`tileSet.modelMatrix` 和 `tileSet._root.transform` 分别用于不同的目的，它们在处理 3D Tiles 的变换时有各自的作用。以下是它们的主要区别和适用场景：

1. `tileSet.modelMatrix`:

+ 用途: `modelMatrix` 是一个 4x4 矩阵，用于直接控制 3D 模型的位置、方向和缩放。设置这个属性会影响整个 3D Tiles 的模型表示。
+ 场景: 在平移时，使用 `tileSet.modelMatrix` 允许直接对整个模型进行位置调整，确保模型在场景中的位置是正确的。

2. `tileSet._root.transform`:

+ 用途: `_root.transform` 是针对 3D Tiles 的根节点的变换矩阵。这个矩阵用于控制该层级中的所有子节点，包括所有的 3D 模型实例。
+ 场景: 在进行旋转和缩放操作时，使用 `_root.transform` 是因为这些变换通常是基于整个模型层级的，而不仅仅是单个模型实例。因此，更新根节点的变换矩阵可以确保所有子节点（模型实例）都共同响应这些变换。

综上所述:

+ 在平移时，直接更新 `tileSet.modelMatrix` 是为了迅速调整模型在场景中的位置。
+ 在旋转和缩放时，更新 `_root.transform` 是为了确保整个模型层级的变换一致性，使得所有子节点都以根节点为参考进行正确的方向和缩放调整。

这种设计使得开发者能够更灵活和有效地管理和操作 3D Tiles 对象，在需要进行复杂变换时能更好地控制整体的可视化效果。

## 17、案例1
描述：加载倾斜摄影数据，实现点击左上角地点，就飞行到对应视角

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730032385833-6e9272d6-4683-4f6b-92b0-147034ae748a.png)

```javascript
...
let viewer;
function toggleView(o) {
 let cartesian = o.cameraPosition.split(',').map(Number);// '-2307121.4654710125,5418655.959749543,2440698.9066960206' 将字符串转换为数组
 let position =  new Cesium.Cartesian3(...cartesian)

 let orientation =  o.cameraOrt.split(',').map(Number);
  viewer.camera.flyTo({
    destination: position,
    duration: 3, //飞行时长
    orientation: {
      //默认(0,-90,0)
      heading:orientation[0],
      pitch: orientation[1],
      roll:orientation[2],
    },
  });
} 
onMounted(() => {
...
  viewer = new Cesium.Viewer("viewer", {
    selectionIndicator: false, // 隐藏选中框
    infoBox: false, // 隐藏右上角信息框
    shouldAnimate: true,
    shadows: true, // 显示阴影
  });

  load3dtiles(viewer, "/src/assets/b3dm/tileset.json", (tileset) => {
    update3dtiles(tileset);
    viewer.flyTo(tileset);
  });
});
```



## 18、案例2
描述：高亮显示、飞行视角、遮罩弹窗

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730032827011-0b6c60f9-e222-433b-9a8e-5ac929473dce.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730032829686-7c2c66ec-fe08-49fa-9242-c7c704771cba.png)

代码实现

```javascript
<template>
  <div id="cesiumContainer"></div>

  <el-dialog v-model="data.dialogTableVisible" :title="data.title">
    <div v-if="data.pickChild.peopleNum">
      <div style="float: right">人口：{{ data.pickChild.peopleNum }}</div>

    </div>

    <div v-else>业主：{{ data.pickChild.owner }}</div>

  </el-dialog>

</template>

<script setup>
import { onMounted, reactive } from 'vue'
import * as Cesium from "cesium"
import { load3dtiles, update3dtiles } from './tool/load'
import buildData from './assets/build.json'
const data = reactive({
  pickChild: null,
  dialogTableVisible: false,
  title: '',
})

Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI5YmMwMWQzMS1iZjg4LTRlZDItYTNmZC01MWEyMzk4NmYwNzEiLCJpZCI6MjQwNjA4LCJpYXQiOjE3MjYwMjAyNzR9.oHC1L475KukrHI4ppPwqjJB0rQUbV4cr4le-6m6ceHQ'
let viewer

onMounted(() => {
  // viewer是所有API的开始
  viewer = new Cesium.Viewer('cesiumContainer', {
    infoBox: false, //隐藏信息框
    selectionIndicator: false  //隐藏选中框
  })
  load3dtiles(viewer, '/src/assets/b3dm/tileset.json', (tileset) => {
    update3dtiles(tileset)
    viewer.zoomTo(tileset)
    initData()
    initHandler()
  })
})

let lastPick
const initHandler = () => {
  let handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas)
  handler.setInputAction((event) => {
    let pick = viewer.scene.pick(event.endPosition)
    // 鼠标移动到实体外时，会返回undefined；entities存放在id属性中
    if (pick && pick.id) {
      if (lastPick) {
        // 将颜色复原
        lastPick.polygon.material = Cesium.Color.fromCssColorString(buildData[lastPick.id].color).withAlpha(0.1)
      }
      pick.id.polygon.material = Cesium.Color.RED.withAlpha(0.3)
      lastPick = pick.id
    } else {
      // 鼠标移除场外时，将最后一个实体的颜色取消
      if (lastPick) {
        lastPick.polygon.material = Cesium.Color.fromCssColorString(buildData[lastPick.id].color).withAlpha(0.1)
      }
      lastPick = null
    }
  }, Cesium.ScreenSpaceEventType.MOUSE_MOVE)
  handler.setInputAction((event) => {
    let pick = viewer.scene.pick(event.position) //拾取元素
    console.log(pick,'点击了');
    if (pick && pick.id) {
      console.log('点击进去了');
      if (pick.id.polygon) {
        // 把高亮效果去除了
        viewer.entities.removeAll()
        handler.removeInputAction(Cesium.ScreenSpaceEventType.MOUSE_MOVE)
        // 定制飞行视角
        let view = buildData[pick.id.id].view // 相机的坐标和高度
        const position = view.cameraPosition.split(',').map(a => Number(a))
        const ortArr = view.cameraOrt.split(',').map(a => Number(a))
        viewer.camera.flyTo({
          destination: new Cesium.Cartesian3(...position),
          orientation: {
            heading: ortArr[0],
            pitch: ortArr[1],
            roll: ortArr[2],
          }
        })
        // 加载各个楼栋的label
        addLabel(pick.id.id)

      } else {
        // 两个点击的事件放在一个点击逻辑里面，根据情况判断来选择执行对应逻辑
        // 这一次是需要点击到label，可以对拾取的实体的id进行判断以确定点击到了谁，不过这里是根据拾取到的实体是否有 polygon来判断
        data.dialogTableVisible = true // 显示遮罩
        data.pickChild = pickPolygon.child[pick.id.id] // pick.id.id 是循环添加label时添加的id，为child数组的索引。根据点击的label，拿到对应的id，根据id所对应的索引拿到数组中的属性对象
        data.title = pickPolygon.type + '_' + data.pickChild.name
      }
      // 问题：为什么flyto底层和高层中的一个实体后，再次点击无法获得到另外一个实体，也就是飞不过去了，也就是pick.id取不到highPolygon，lowerPolygon？
      // 这个时候点击只有两种可能，一种是，id:undefind；另一种是，id:label
      // 解答：我所看到的实体只是倾斜摄影测量的数据，真正的实体是数据初始化时新建的那个，而在执行完第一次点击后就已经清除了
    }
  }, Cesium.ScreenSpaceEventType.LEFT_CLICK)
}

let pickPolygon
// 
const addLabel = (id) => {
  // 拿到当前渲染的是高层还是低层
  pickPolygon = buildData[id]
  // 使用循环添加label，
  buildData[id].child.forEach((item, index) => {
    viewer.entities.add({
      id: index,
      position: Cesium.Cartesian3.fromDegrees(...item.position),
      label: {
        text: item.name,
        font: "20px",
        fillColor: Cesium.Color.WHITE,
        backgroundColor: Cesium.Color.BLACK.withAlpha(0.5),
        showBackground: true,
      }
    })
  })
}

// 初始化数据:通过遍历对象拿到两块区域数据，并建立实体，包括了：标记、边框、区域覆盖
const initData = () => {
  for (let key in buildData) {
    viewer.entities.add({
      id: key,// 有大用
      position: Cesium.Cartesian3.fromDegrees(...buildData[key].center),
      label: {
        text: buildData[key].type,
        font: '20px'
      },
      polygon: {
        hierarchy: {
          positions: Cesium.Cartesian3.fromDegreesArray(buildData[key].range),
        },
        material: Cesium.Color.fromCssColorString(buildData[key].color).withAlpha(0.1)
      },
      polyline: {
        positions: Cesium.Cartesian3.fromDegreesArray(buildData[key].range),
        material: new Cesium.PolylineGlowMaterialProperty({
          glowPower: 0.1,
          color: Cesium.Color.fromCssColorString(buildData[key].color),
        }),
        width: 15,
        // 使线贴地
        clampToGround: true
      }
    })
  }
}
</script>

<style scoped>
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}
#cesiumContainer {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
.box-card {
  position: absolute;
  width: 300px;
  top: 40px;
  left: 40px;
}

.text {
  margin: 10px;
  cursor: pointer;
}

.text:hover {
  color: blueviolet;
}
</style>

```

✅ `Polyline`的`clampToGround`属性

一个布尔属性，指定是否应将 Polyline 夹在地面上。

## 
## 20、楼层单体化
### 1、数据准备
#### 1.1 建库
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034253295-bd0fd325-1441-43bc-9a28-7f9546bca4cf.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034256011-fe993714-0283-4abe-8835-8f716eddcdd9.png)

导入文件

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034261533-192c827e-a2bb-41bc-9ede-42b2c488690c.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034263569-a54d995b-ad3a-4576-adc0-952da0d97f78.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034265610-ddafcc83-7c53-47ab-ba29-144fdd08e32b.png)

如果添加不上，可以执行sql语句直接创建

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034270547-2fa1527d-48f6-450a-adea-03e2e2b58c19.png)

复制进去点击运行就好了

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034274262-751aff4f-c9fa-4b34-bd14-55a233d1290c.png)

#### 1.2 数据查看
sql 就有polygon类型数据

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034278990-c3259541-6bef-4dc2-badf-34cd04ba6a0b.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034283259-b2c0c9c8-f8cf-4075-b801-91a99c2b8d99.png)

### 2、后端
基本不需要改

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034290210-f0b19089-3985-4c10-8a2d-2d9a943bf747.png)

双击启动

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034293344-d357de0b-7462-46ca-969a-eca297a4fac7.png)

后端运行成功

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034296567-0cb959a6-bcea-4ea8-8a1b-9916a3b02333.png)

### 3、前端
#### 3.1 加入3DTiles数据
（就是之前练习的那个

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034303968-b7ca1322-e8a4-4ccb-8107-137200096bd4.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034305648-c4b97f7a-113c-417a-9e38-ec2cba0ec3a6.png)

#### 3.2 安装依赖
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034308505-1f75f6e4-bf3a-4e09-a09b-9efd6ceef729.png)

#### 3.3  加载三维数据
vue3 中将地图对象挂载到全局的两种方法：

第一种方法：

1、main.js 中 导出app

```javascript
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
export {app}
```

2、在变量所在组件中添加全局属性：`app.config.globalProperties.$viewer = viewer`

```javascript
let viewer
  onMounted(() => {
  viewer = new Cesium.Viewer('cesiumContainer', {
    infoBox: false, //隐藏信息框
    selectionIndicator: false,  //隐藏选中框
    timeline:false,
    animation:false
  })
      ...
  app.config.globalProperties.$viewer = viewer
})
```

3、在其他组件中使用

```javascript
import { onMounted, getCurrentInstance, } from 'vue'
let viewer // 必须在外面注册一个变量来存值，要不然传递不出 onMounted生命周期
onMounted(async () => {
  // 拿到地图对象
  const { proxy } = getCurrentInstance()
  viewer = proxy.$viewer
})
```

第二种方法：

1、变量所在组件中

```javascript
import {onMounted,getCurrentInstance} from 'vue'
const {appContext} = getCurrentInstance()
const global = appContext.config.globalProperties
onMounted(()=>{
  global.$viewer = viewer
})
```

2、在其他组件中使用

```javascript
import {onMounted,getCurrentInstance} from 'vue'
const {appContext} = getCurrentInstance()
const global = appContext.config.globalProperties
onMounted(()=>{
console.log(global.$viewer,'看看设置全局变量成功没有');
})
```





疑难杂症

⚠️ 别再用相对路径了

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034318063-197afb74-e3b4-4cd3-a345-3b27ace9eeae.png)

应该是识别不到该文件

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034323719-b8c07402-2107-4f15-8243-b2e0c0d2eced.png)

这样子才对

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034327423-1aa9fc30-9b47-4710-a367-53f1d76424f3.png)

#### 3.4 试用画笔
观察封装的画笔，我们可以发现。

导出了两个方法，其中toDraw的参数包括了。。。，

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034334462-3e650a38-f2db-481f-9a5b-bdca0c74aa49.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034336758-da0cbc11-0dc4-4d59-a869-81ad76ad4708.png)

回调函数call 中的参数是刚刚添加的一个实体，所以我们可以在 call 回调中拿到绘画后的实体

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034345914-cc6fcd3c-b0b6-4ee1-8db9-95e381ca7616.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034347646-c176908c-5e82-4960-bf00-5d9928714db0.png)

绘制效果如下

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034357588-79be0dc4-0639-47f4-a8a0-38dcc38650de.png)

#### 3.5 setBuild.vue
##### 3.5.1UI设计
一个步骤组件，每一步对应一个操作

ps：有时候浮动也挺好用的，不要听信浮动已经被抛弃的谣言

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034359754-397aaae8-706e-47c6-aa98-8ebbc39b0fdc.png)

UI代码实现

```vue
<template>
  <el-card class="setbuild">
    <template #header>
      <div class="card-header">
        <span style="font-weight: 600; font-size: 18px">楼房分户</span>

        <span class="myIcon" style="float: right">
          <Refresh />
        </span>

      </div>

    </template>

    <div>
      <el-steps :active="data.active" align-center finish-status="success">
        <el-step title="区域绘制" />
        <el-step title="户型切分" />
        <el-step title="楼层分层" />
      </el-steps>

      <div style="margin: 30px 10px">
        <div>
          <span>绘制户型：</span>

          <span class="myIcon" v-show="data.active == 0" @click="drawPolygon">
            <FullScreen />
            绘制图形</span
          >

          <span class="myIcon" v-show="data.active == 1">
            <scissor />
            裁切图形</span
          >

          <span class="myIcon" v-show="data.active == 2">
            <histogram />
            楼层分层</span
          >

        </div>

        <div class="textInput">
          <el-input v-model="inputArr[0]"></el-input>

          <el-input v-model="inputArr[1]"></el-input>

          <el-input style="width: 40%" v-model="inputArr[2]"></el-input>

        </div>

        <el-button
          type="info"
          v-if="data.active < 2"
          style="margin: 12px; float: right"
          @click="next"
          >下一步</el-button
        >

        <el-button type="success" v-else style="margin: 12px; float: right" @click="toLayer"
          >楼层分层</el-button
        >

      </div>

    </div>

  </el-card>

</template>

...

<style lang="scss">
.setbuild {
  width: 25%;
  position: absolute;
  top: 4%;
  left: 4%;
  z-index: 999;

  .buildnum {
    float: right;
    width: 34%;

    .el-input {
      width: 50%;
    }
  }

  .myIcon {
    cursor: pointer;

    svg {
      width: 20px;
      position: relative;
      top: 5px;
      margin-right: 3px;
    }
  }

  .textInput {
    display: flex;

    .el-input {
      margin: 5px 1%;

      .el-input__inner {
        text-align: center;
      }
    }

    img {
      margin: 10px 4.6%;
      width: 14%;
      height: 25px;
      cursor: pointer;
    }
  }

  .pointList {
    display: flex;
    font-size: 15px;
    margin: 20px 0;
    line-height: 30px;

    .el-input {
      width: 15%;
      margin-right: 4%;
    }
  }
}
</style>

```

##### 3.5.2 功能实现
###### ①绘制图形
点击绘制，调用画笔，将绘制结果的笛卡尔坐标转换为经纬度，将所得数据添加到数组，以循环渲染到视图中

只有绘制了图形，即数据不为空时才能进行下一步

再次点击绘制图形可以重新绘制

```javascript
 <span class="myIcon" v-show="data.active == 0" @click="drawPolygon">
<FullScreen />绘制图形
</span>

```

```javascript
import { toDraw } from '@/tool/draw.js'
import * as Cesium from 'cesium'
// 绘制图形
const drawPolygon =()=>{
  toDraw(viewer,'polygon',(res)=>{
    // 1、可视化窗口中显示的是经纬度坐标
    // 2、数据库中存储的是 GeoJSON数据格式
    // 3、多边形切割时也需要 geojson数据
    // 所以需要将 笛卡尔坐标转换为经纬度
    let car3_ps = res.polygon.hierarchy._value.positions
    let arr =[]
    for(let i=0;i<car3_ps.length;i++){
      let _cartographic = Cesium.Cartographic.fromCartesian(car3_ps[i]);
      let _lat = Cesium.Math.toDegrees(_cartographic.latitude);
      let _lng = Cesium.Math.toDegrees(_cartographic.longitude);
      arr.push([_lng,_lat])
    }
    console.log(arr,'多边形的经纬度坐标');
  })
}
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034374972-2080c577-9ef8-4745-aef2-775fb25908f8.png)



###### ②多边形裁切
点击裁切图形，激活线画笔，画笔回调事件中，将实体坐标转换为经纬度坐标，生成线 GeoJSON 数据，调用裁切方法生成 polygonCollection 数据，并分别添加到实体中（添加到实体中而不是 dataSource中是因为，全部实体都在 entities中，这样好管理）。清除掉绘制的切割用的线实体（避免将绘画状态带入下一步），将需要用于展示的数据添加到对应数组中。

再次点击裁切图形，将原来的分割好的实体清除掉，加载第一次绘制的多边形

如果绘制的裁剪线并没有穿过多边形，会由 polygonCut.js 抛出一个错误，截获错误并由弹窗显示出来

如果绘制的裁剪线没有进入多边形，默认不会报错，但是需要提醒进行有效的裁剪

```javascript
// 分割多边形
const  drawLine =()=>{
  ElMessage.info('请绘制图形，右键结束绘制')
  // 进行重复裁切时，将实体恢复至原始模样
  viewer.entities.removeAll()
  viewer.entities.add(polygonEntity)

  toDraw(viewer,'line',(res)=>{
    // 转换坐标，生成geojson数据
    let car3_ps = res.polyline.positions._value
    let arr = []
    for (let i = 0; i < car3_ps.length; i++) {
      let _cartographic = Cesium.Cartographic.fromCartesian(car3_ps[i])
      let _lat = Cesium.Math.toDegrees(_cartographic.latitude)
      let _lng = Cesium.Math.toDegrees(_cartographic.longitude)
      arr.push([_lng, _lat])
    }
    // 利用turf方法生成geojson数据
    const lineGeojson = turf.lineString(arr);
    // 使用多边形裁切方法，line的绘制不合规范时(只进不出、根本不进入），会抛出错误
    let polygonCollection
    try {
      polygonCollection =  polygonCut(polygonGsojson,lineGeojson)
      if(polygonCollection.features.length ==1){
        ElMessage.error('请切割区域')
        return
      }
    } catch (error) {
      ElMessage.error(error)
      return
    }
    // 将裁切后的多边形加载成实体，原来的清除
    Cesium.GeoJsonDataSource.load(polygonCollection,{clampToGround:true}).then(info =>{
      viewer.entities.removeAll()
      data.unitArr = []
      info.entities.values.forEach((item,index) =>{
        item.polygon.material = Cesium.Color.fromRandom({alpha:0.5})
        viewer.entities.add(item)
        data.unitArr.push([
          polygonCollection.features[index].geometry.coordinates.toString(),
          data.unitArr.length +1,
          item
        ])
      })
    })

  })

}
```







###### ③定位闪烁
点击定位图标后，对应的实体高亮闪烁

优化：在连续点击时，会变成白膜并报错说找不到 color

```javascript
// 定位闪烁
let initColor
const toFlash = (entity)=>{
  // 闪烁1.5s后停止闪烁
  // 使用CallbackProperty方法
  // bug ：在连续点击时，会变成白膜并报错说找不到 color
  if(!initColor){
   initColor  = entity.polygon.material.color._value
  }
  //  initColor  = entity.polygon.material // 这样是不行的，initColor变成了callback函数，会一直执行下去

  console.log(initColor,'颜色的格式');
  // 当在闪烁期间再次点击，entity.polygon.material得到的是一个callback函数，自然是没有 color._value属性的，所以赋值为 undefined，当最近的一个计时器执行
  // entity.polygon.material 被赋值为 undefined，那再次点击时，对initColor赋值时寻找属性 .color._value会报错
  let x = 1
  let flog = true
  entity.polygon.material = new Cesium.ColorMaterialProperty(new Cesium.CallbackProperty(()=>{
    if(flog){
      x = x-0.02
      if(x<0){
        flog = false
      }
    }else {
      x = x+0.02
      if(x>=1){
        flog = true
      }
    }
    return Cesium.Color.SKYBLUE.withAlpha(x)
  },false))
  setTimeout(() => {
    if(!initColor){
      return
    }
    entity.polygon.material = initColor
    initColor = null
    // 不清空的话，之后的闪烁的结束都会变成最开始的那个面的颜色，
    // 但是在这清空的话，因为每点击一次都会开启一次定时器，当initColor被设为null后，在此之后的定时器执行赋值时就会报错
    // 加个判断刚好解决
  }, 1500);
}
```

解决bug的另一种方式

牛逼，一句话就搞定了

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034389122-266f3ae9-3978-4a1e-b12e-f413f6c64d75.png)



###### ④楼层分层
绘制点

绘制三个点，获得高度，并添加到可视化数据中，由低到高分别是，最低点、分割点、最高点

再次点击时清除三个点以及可视化数据，然后激活画笔进行二次绘制

通过input 输入框进行点高度的微调

```vue
        <!-- 楼层高度 -->
         <div class="pointList" v-show="data.active == 2">
          最低点：<el-input v-model="data.heightArr[0]"></el-input>

          分割点：<el-input v-model="data.heightArr[1]"></el-input>

          最高点：<el-input v-model="data.heightArr[2]"></el-input>

         </div>

```

```javascript
// 绘制点
const drawPoint = ()=>{
  ElMessage.info('请绘制底层，二楼以及顶楼高度点')
  // 清空上一次操作留下的点数据
  data.heightArr = []
  // 从0开始删除：有bug。这是因为，当viewer.entities.values这个数组发生变化时，会重新排序（仅限于这个数组），所以会漏掉最开始的奇数位的点数据
  // viewer.entities.values.forEach(item =>{
  //   item.point && viewer.entities.remove(item)
  // })
  // 解决方法：从末尾开始删除
  for(let i = viewer.entities.values.length -1 ;i>=0;i--){
    let item = viewer.entities.values[i]
    item.point && viewer.entities.remove(item)
  }
  toDraw(viewer,'point',(res)=>{
    // 拿到高度
    const height = Cesium.Cartographic.fromCartesian(res.position._value).height
    data.heightArr.push(height)
    if(data.heightArr.length == 3){
      data.heightArr.sort((a,b)=>a-b)
      endDraw()
    }
  })
}
```

楼层切分

检验楼层数是否正确  =>  清空绘制的点和未分层的面  =>  清除拆分后的楼层(如果有的话）  =>  因为进行了切分，所以要对裁切后的每一个实体进行遍历添加primitive  => 计算出每层楼的高度，然后通过循环嵌套，添加每一层的primitive

```javascript

// 最后一步楼层分层
let heightList = []
const toLayer = () => {
  // 进行拆分前先检验，楼层数是否正确
  if(!data.floorNumber){
    ElMessage.info('请输入楼层数')
    return
  }
  // 清空绘制的点和未分层的面
  viewer.entities.removeAll()
  // 清除拆分后的楼层(如果有的话），即primitive，但是3DTiles 也是添加的 primitive，所以不能直接 removeAll
  heightList.length && heightList.forEach(item =>{
    viewer.scene.primitives.remove(item)
 })
 heightList = []
  
// 因为进行了切分，所以要对裁切后的每一个实体进行遍历添加primitive
 // 计算出每层楼的高度，然后通过循环嵌套，添加每一层的primitive
 let itemHeight = (data.heightArr[2] - data.heightArr[1]) / (data.floorNumber - 1)
 for (let j = 0; j < data.unitArr.length; j++) {
   for(let i = 0;i<data.floorNumber;i++){
     let height,extrudedHeight
    // 第一层的高度有点不一样，所以需要单独拎出来
    if(i == 0){
      height = data.heightArr[0],
      extrudedHeight = data.heightArr[1]
    }else{
      // 这有个bug，当用户通过input框对三个点的高度进行修改后，高度值变成了 string格式，做减法或者直接赋值时会存在隐式转换，不会出问题，但是在这的加法中，会变成字符串拼接
      height = Number(data.heightArr[1]) + (i-1)*itemHeight
      extrudedHeight = Number(data.heightArr[1]) + i*itemHeight
    }
    // 新建紧贴3DTiles的primitive
     let primitive = new Cesium.ClassificationPrimitive({
       geometryInstances:new Cesium.GeometryInstance({
         geometry:new Cesium.PolygonGeometry({
           polygonHierarchy:new Cesium.PolygonHierarchy(data.unitArr[j][2].polygon.hierarchy._value.positions),
           height,
           extrudedHeight,
         }),
         attributes:{
           color:Cesium.ColorGeometryInstanceAttribute.fromColor(
             Cesium.Color.fromRandom({alpha:0.5})
           )
         }
       }),
       classificationType:Cesium.ClassificationType.CESIUM_3D_TILE
     })
     viewer.scene.primitives.add(primitive)
     heightList.push(primitive)
   }
 }
 // 当成功分层后才表示这一步成功完成
 if(heightList.length){
   data.active = 3
 }
}
```

提交数据

```javascript
// 生成并提交数据
const toAddHouse =async()=>{
  let polygonJson = JSON.stringify(polygonGsojson.geometry)
  let polygonJsonArr = polygonCollection?polygonCollection.features.map((item)=>{
    return JSON.stringify(item.geometry)
  }):[]
  let unitArr = data.unitArr.map((item) =>{
    return Number(item[1])
  })
  let heightArr = data.heightArr.map((item) =>{
    return Number(item)
  })
  const res = await addHouse({
    polygonJson,
    polygonJsonArr,
    unitArr,
    heightArr,
    name:data.buildName,
    floorNum:Number(data.floorNumber)
  })
  if(res.code == 200){
    ElMessage.success('提交成功')
    reset()
  }

}
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034401320-5eb7186f-9721-4e5b-bcb1-9678514c15ca.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034403423-6ad8245d-3da1-47a7-b91f-a8cc7a466fe4.png)



###### ⑤清除地图影响
```vue
// 销毁组件时，同时清除地图影响
onUnmounted(()=>{
  reset()
})
```



#### 3.6  setInfo.vue
##### 3.6.1  整体功能描述
##### 3.6.2 UI设计
##### 3.6.3 功能实现
###### ①数据初始化
发送请求，获取数据 => 可视化渲染

```vue
// 可视化板块
    <template #header>
      <div class="card-header">
        <span style="font-weight: 600; font-size: 18px">编辑房户信息</span>

        <el-select v-model="data.pickBuild" placeholder="请选择楼栋" size="large" style="float: right;">
          <el-option
            v-for="item in data.buildArr"
            :key="item.id"
            :label="item.name"
            :value="item"
          />
        </el-select>

      </div>

    </template>

。。。
<script setup>
// 响应数据
const data = reactive({
  buildArr: [],
  pickBuild: null
})

// 初始化数据
const initData = async () => {
  const res = await getBuild()
  if (res.code == 200) {
    ElMessage.success('数据请求成功')
  }
  data.buildArr = res.data
}

onMounted(() => {
  // 初始化数据
  initData()
})
 </script>

```

###### ②选择楼栋
下拉框选择楼栋 => 视角跳转、发送请求获取对应分层数据并渲染到表格中 

```vue
<template>
  <el-card class="setinfo">
    <template #header>
      <div class="card-header">
        <span style="font-weight: 600; font-size: 18px">编辑房户信息</span>

        <el-select
          v-model="data.pickBuild"
          placeholder="请选择楼栋"
          style="float: right; width: 230px"
          @change="changeBuild"
        >
          <el-option
            v-for="item in data.buildArr"
            :key="item.id"
            :label="item.name"
            :value="item"
          />
        </el-select>

      </div>

    </template>

    <!-- 表格 -->
    <el-table :data="data.tableData" style="width: 100%" @row-click="tableClick">
      <el-table-column label="门牌号">
        <template #default="scope">
          <div style="display: flex; align-items: center; justify-content: center">
            <span style="margin-left: 10px; color: skyblue; font-weight: bold">{{
              String(scope.row.floorNum) + '0' + String(scope.row.number)
            }}</span>

          </div>

        </template>

      </el-table-column>

      <el-table-column label="单元号">
        <template #default="scope">
          <div style="display: flex; align-items: center; justify-content: center">
            <span style="margin-left: 10px">{{ scope.row.number }}<span> 单元</span></span>

          </div>

        </template>

      </el-table-column>

      <el-table-column label="楼层" prop="floorNum">
        <template #default="scope">
          <div style="display: flex; align-items: center; justify-content: center">
            <span style="margin-left: 10px">{{ scope.row.floorNum }}楼</span>

          </div>

        </template>

      </el-table-column>

      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)"> 编辑信息 </el-button>

        </template>

      </el-table-column>

    </el-table>

    <!-- 分页器 -->
    <el-pagination
      v-model:current-page="data.query.pageIndex"
      :page-size="data.query.pageNum"
      :disabled="disabled"
      :background="background"
      layout="total, prev, pager, next"
      :total="data.total"
      @current-change="getHouseData"
    />
  </el-card>

</template>

。。。
<script setup>
// 点击选项时,视角跳转、加载分层数据
const changeBuild = (item) => {
  const center = turf.center(item.polygon)
  viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(...center.geometry.coordinates, 200)
  })
  // 加载分层数据
  data.query.id = item.id
  getHouseData()
}
// 获取这栋楼的每层数据的方法封装
const getHouseData = async () => {
  const res = await getHouse(data.query)
  if (res.code == 200) {
    data.tableData = res.data.list
    data.total = res.data.total
  } else {
    ElMessage.error(res.message)
  }
}
</script>

```

###### ③点击表格行
点击表格行 => 对应户高亮，再次点击时之前的高亮消除，点击其他楼栋时高亮消除

```vue
<script setup>
    // 表格行点击时，对应户高亮
let  heightList = []
const tableClick =(row)=>{
  let arr = row.polygon.coordinates[0].flat()
  // 清除之前的高亮户
  heightList.length && heightList.forEach(item =>{
    viewer.scene.primitives.remove(item)
 })
 heightList = []
    // 新建紧贴3DTiles的primitive
    let height,extrudedHeight
    height = row.minHeight
    extrudedHeight = row.maxHeight
    let primitive = new Cesium.ClassificationPrimitive({
       geometryInstances:new Cesium.GeometryInstance({
         geometry:new Cesium.PolygonGeometry({
           polygonHierarchy:new Cesium.PolygonHierarchy(Cesium.Cartesian3.fromDegreesArray(arr)),
           height,
           extrudedHeight,
         }),
         attributes:{
           color:Cesium.ColorGeometryInstanceAttribute.fromColor(
             Cesium.Color.SKYBLUE({alpha:0.9})
           )
         }
       }),
       classificationType:Cesium.ClassificationType.CESIUM_3D_TILE
     })
     viewer.scene.primitives.add(primitive)
     heightList.push(primitive)
}
    </script>

```

###### ④编辑信息
点击编辑信息 => 发送请求获取详细的住户数据、出现遮罩弹窗 => 若有数据，则进行检查修改，若无数据，则进行填写。最后上传

<!-- 这是一张图片，ocr 内容为： -->
![](C:\Users\Administrator\Desktop\1728147195319.png)

<!-- 这是一张图片，ocr 内容为： -->
![](C:\Users\Administrator\Desktop\1111)

遗留问题

图片上传成功后，查看不了

已解决：访问路径为：[http://127.0.0.1:8090/static/](http://127.0.0.1:8090/static/).......

修改信息的api的参数不知道

已解决：正如猜想的那样，就把 submitInfo.value  上传就行，只是，性别和物业的取值都只能是数字，所以之前的尝试不成功



###### ⑤页面切换
清除高亮、页码选择器

```javascript
// 销毁组件时，同时清除地图影响
onUnmounted(() => {
  // 清除之前的高亮户
  heightList.length &&
    heightList.forEach((item) => {
      viewer.scene.primitives.remove(item)
    })
  heightList = []
  // 修正分页选择器页码
  data.query.pageIndex = 1
})
```





#### 3.7 House.vue
###### ①数据初始化
发送请求，获取数据 => 可视化渲染

```vue
// 可视化板块
    <template #header>
      <div class="card-header">
        <span style="font-weight: 600; font-size: 18px">编辑房户信息</span>

        <el-select v-model="data.pickBuild" placeholder="请选择楼栋" size="large" style="float: right;">
          <el-option
            v-for="item in data.buildArr"
            :key="item.id"
            :label="item.name"
            :value="item"
          />
        </el-select>

      </div>

    </template>

。。。
<script setup>
// 响应数据
const data = reactive({
  buildArr: [],
  pickBuild: null
})

// 初始化数据
const initData = async () => {
  const res = await getBuild()
  if (res.code == 200) {
    ElMessage.success('数据请求成功')
  }
  data.buildArr = res.data
}

onMounted(() => {
  // 初始化数据
  initData()
})
 </script>

```

###### ②选择楼栋
下拉框选择楼栋 => 视角跳转、发送请求获取对应分层数据并将 primitive 添加到楼层上

```javascript

// 点击选项时,视角跳转、加载分层数据
let heightList = []
const changeBuild = (item) => {
  const center = turf.center(item.polygon)
  viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(...center.geometry.coordinates, 200)
  })
  // 加载分层数据
  data.query.id = item.id
  getHouseData()
  // 清除之前的高亮户
  heightList.length &&
    heightList.forEach((item) => {
      viewer.scene.primitives.remove(item)
    })
  heightList = []
}
// 获取这栋楼的每层数据并加载primitive的方法封装
const getHouseData = async () => {
  const res = await getHouse(data.query)
  console.log(res, '每户数据')
  if(res.code == 200 ){
    res.data.forEach(item =>{
      let arr = item.polygon.coordinates[0].flat()
  // 新建紧贴3DTiles的primitive
  let height, extrudedHeight
  height = item.minHeight
  extrudedHeight = item.maxHeight
  let primitive = new Cesium.ClassificationPrimitive({
    geometryInstances: new Cesium.GeometryInstance({
      geometry: new Cesium.PolygonGeometry({
        polygonHierarchy: new Cesium.PolygonHierarchy(Cesium.Cartesian3.fromDegreesArray(arr)),
        height,
        extrudedHeight
      }),
      attributes: {
        color: Cesium.ColorGeometryInstanceAttribute.fromColor(Cesium.Color.fromRandom({alpha:0.8}))
      }
    }),
    classificationType: Cesium.ClassificationType.CESIUM_3D_TILE
  })
  viewer.scene.primitives.add(primitive)
  heightList.push(primitive)
    })
  }
}
```

✅ 按需添加颜色数组

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034426690-d44af1f0-d1be-4a2d-9384-2321c5252afc.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034428435-5552955d-6d35-4529-8620-9d9ee96d8b5c.png)

###### ③展示住户信息
onMOunted 中挂载事件初始化方法 => 在 initHandler()  中，新建handler对象，绑定左键点击事件 =>  在事件回调函数中，拾取图元、拾取坐标 => 根据实体 id 发送请求 => 根据坐标和请求数据渲染弹窗 （先清除弹窗）、高亮当前图元（先清除高亮）



✅ 给primitive添加id。（以确定在点击时拿到之前添加的primitive）

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034434096-26844ee3-6acf-443f-ad55-7152dc616e2b.png)

✅ cesium弹窗



✅ 左键点击事件的事件对象的坐标和拾取的坐标是不一样

`let position = viewer.scene.pickPosition(event.position)`

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034453075-666a78bc-19dc-45c9-bb39-0127439364e2.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034455141-6f7b7bf7-8104-4a6e-bbe8-d32719f29b39.png)

✅ 拾取到的对象的结构

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034460617-b8318e81-117b-47e5-bb69-8a1f5ea2e3f0.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034462088-157365e8-c90d-451d-8df7-756225347a8e.png)

✅ 给图元添加颜色

在 primitve 的原型上可以看到  `getGeometryInstanceAttributes` 这样一个方法（需要一个参数：id）

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034468324-b5533b93-54a8-49fa-8c34-eb0f98102446.png)

这个方法返回的对象是

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034472626-514293c4-68e6-4817-8127-23f0c806eb7c.png)

设置颜色

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034476227-a56f1dff-886b-4179-a358-e45f3ebd6e2d.png)

###### ④页面切换
清除 图元、 弹窗



#### 3.8 tool
##### ①bubble.js
##### ②draw.js
##### ③load3D.js
##### ④polygonCut.js
##### ⑤cesiumToZh.js
⚠️ 依赖出问题了就重新装，最快的方法就是，直接在文件夹中打开，直接删除node_module，在vscode中删除会很慢

⚠️ 3Dtiles加载不要开太高精度，电脑都得卡死，然后还会报错

之前不知道怎么的开到1了，数字越小，远距离加载时精度越高。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034484327-5d27148a-f0d0-4ddd-a46b-f472704a6bbf.png)

内存给干到99%后就报错了

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034490689-a339cab0-8ee0-4ce4-843c-e81ec2c20cca.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034492575-1dd32215-0f23-4f2e-a2c1-d728647c0adb.png)

改成30后，电脑表示悠哉游哉

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034499523-e2e42b57-411b-49b3-9783-bd8e927dfe32.png)

⚠️ 默认导出的方法或者变量，在引入时，不需要用 {}括起里

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034502904-abddf3f3-272a-4d3b-ac9f-33273065aa7d.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034505014-d3280bb7-aefd-4dc9-b415-d4201be2c7d7.png)

⚠️ turf.difference () 的参数需要是一个 FeatureCollection的Geojson数据，在老师给的封装好的工具中并没有传入正确的数据格式

解决bug的经历：一开始觉得，封装好的工具，以及引入的turf库肯定是不会出错的，那多半是我的数据有问题。排查半天，实在找不出来。后来一想到底需要什么样的数据，一直排查到 turf 的源码，但是turf的源码看不太懂，但是我肯定能确定，difference（）中传递的参数应该是一个变量，而在老师封装的 polygonCut 中，传递的参数是两个变量。我刚开始直接用数组套起来，但显然不行，最后想到去官网看，才发现应该是 FeatureCollection。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034514940-ea581385-1483-4861-a417-60650fc59510.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034516591-ccef912b-88be-4e82-b4c3-e0307b58dea6.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034518277-5a1f4122-6ab1-47be-b0ab-9405ccc3b974.png)

⚠️ element-plus 中的select组件，change事件是默认将选项的 :value 值当作参数直接传递的。不需要再单独传

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034545523-5cd105d9-a2e4-4813-b858-7bde26c56454.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034547446-6ae9c07e-d8fb-488f-a649-ef1a073eefa3.png)

这样写反而成了立即执行函数

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034551792-b5e2cfd9-0e0f-4f16-80a3-499d6d4e0ae2.png)

⚠️ 浮动是需要明确的宽度的

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034555334-31dc2b08-f166-4c42-90f3-d450eeccb448.png)

⚠️ elment-plus 的表格的插槽的使用方法

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2024/png/34655355/1730034558129-27dbd752-f707-4f5f-8c4a-b5f92e1a613c.png)

