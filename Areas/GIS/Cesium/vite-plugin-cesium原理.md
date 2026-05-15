# vite-plugin-cesium 原理

## 为什么需要这个插件？

### Cesium 的特殊性

Cesium 是一个复杂的 3D GIS 库，包含大量**不能打包进 JS bundle** 的静态资源：

```
cesium/Build/Cesium/
├── Workers/           # Web Worker 脚本（独立执行上下文）
│   ├── chunk-*.js     # 约 20 个 Worker 文件
│   └── ...
├── ThirdParty/        # WASM 二进制文件
│   ├── draco_decoder.wasm      # Draco 压缩解码
│   ├── basis_transcoder.wasm   # Basis 纹理转码
│   └── wasm_splats_bg.wasm     # Gaussian Splatting
├── Assets/            # 预定义资源索引
│   ├── Ion/
│   └── ...
└── Widgets/           # UI 控件
    ├── widgets.css
    └── ...
```

### 为什么不能打包？

**1. Web Workers 的独立性**

Worker 有独立的执行上下文，必须通过 URL 加载：

```js
// Worker 加载方式
new Worker('/cesium/Workers/cesiumTerrainProcessor.js');

// ❌ 不能这样加载
import Worker from 'cesium/Workers/cesiumTerrainProcessor.js';
new Worker(Worker);  // 错误！Worker 不是模块
```

**2. WASM 文件格式**

WASM 是二进制格式，不能嵌入 JS 字符串（某些版本尝试这样做会导致语法错误）：

```js
// ❌ 错误示例（Cesium bundled 版本的 fallback）
const wasmString = `\0asm\0\0\0...`;  // SyntaxError: Octal escape

// ✓ 正确方式：外部文件加载
fetch('/cesium/ThirdParty/draco_decoder.wasm')
  .then(res => res.arrayBuffer())
  .then(wasmBinary => WebAssembly.instantiate(wasmBinary));
```

**3. 运行时动态加载**

Cesium 在运行时根据 `CESIUM_BASE_URL` 动态请求资源：

```js
// Cesium 内部逻辑
const workerUrl = CESIUM_BASE_URL + '/Workers/cesiumTerrainProcessor.js';
const wasmUrl = CESIUM_BASE_URL + '/ThirdParty/draco_decoder.wasm';
```

## 插件核心功能

### 1. 自动复制静态资源

```js
// vite-plugin-cesium 内部逻辑（简化）
function vitePluginCesium() {
  return {
    name: 'vite-plugin-cesium',
    
    // 构建结束时复制资源
    closeBundle() {
      const cesiumPath = 'node_modules/cesium/Build/Cesium';
      const outDir = 'dist/cesium';
      
      // 复制四个目录
      fs.copy(`${cesiumPath}/Workers`, `${outDir}/Workers`);
      fs.copy(`${cesiumPath}/Assets`, `${outDir}/Assets`);
      fs.copy(`${cesiumPath}/Widgets`, `${outDir}/Widgets`);
      fs.copy(`${cesiumPath}/ThirdParty`, `${outDir}/ThirdParty`);
    }
  };
}
```

**为什么复制到 dist 而不是 public？**

- `dist/` 是 Vite 构建输出目录，生产部署时直接复制整个目录
- `public/` 在开发时可用，但需要手动同步 node_modules 更新

### 2. 注入 CESIUM_BASE_URL

```js
// vite.config.js
export default defineConfig({
  plugins: [vitePluginCesium()],
  
  // 插件自动注入
  define: {
    CESIUM_BASE_URL: JSON.stringify('/cesium')
  }
});
```

**效果**：

```js
// 编译后的代码
const CESIUM_BASE_URL = '/cesium';

// 运行时请求
fetch('/cesium/ThirdParty/draco_decoder.wasm');
```

### 3. 处理 CSS 导入

```js
// 插件自动导入 Widgets 样式
import 'cesium/Build/Cesium/Widgets/widgets.css';
```

如果不导入，Cesium 的 UI 控件（时间轴、导航按钮等）会没有样式。

### 4. externals 配置（可选）

某些场景使用 CDN 加载 Cesium：

```js
// vite.config.js
export default defineConfig({
  plugins: [vitePluginCesium()],
  
  build: {
    rollupOptions: {
      external: ['cesium'],
      output: {
        globals: {
          cesium: 'Cesium'
        }
      }
    }
  }
});
```

配合 HTML 中的 CDN：

```html
<script src="https://unpkg.com/cesium@1.141/Build/Cesium/Cesium.js"></script>
```

## Workers 的作用详解

Cesium 用 Web Workers 处理计算密集型任务，避免阻塞 UI 渲染：

```
主线程（UI）                         Worker 线程
    │                                    │
    │  发送地形数据 ──────────────────────>│
    │                                    │  地形网格生成
    │                                    │  几何体计算
    │                                    │  投影变换
    │                                    │  Draco 解码
    │  接收处理结果 <──────────────────────│
    │                                    │
    │  渲染帧                             │
```

**关键 Worker 文件**：

| Worker | 功能 |
|--------|------|
| `cesiumTerrainProcessor.js` | 地形网格生成 |
| `dracoDecoder.js` | Draco 压缩模型解码 |
| `encodeGeohash.js` | Geohash 编码 |
| `createVerticesFromGoogleEarthEnterpriseBuffer.js` | Google Earth 数据解析 |

## 为什么 WASM 不能嵌入 JS？

### 1. WASM 文件格式

WASM 文件以 `\0asm`（magic bytes）开头，这是二进制数据：

```
00 61 73 6D  # \0asm (magic)
01 00 00 00  # version 1
...
```

### 2. Template Literal 的限制

ES6 template literal 禁止 octal escape：

```js
// ❌ 语法错误
const str = `\0asm`;  // \0 被视为 octal escape

// ✓ 正确（用 hex escape）
const str = `\x00asm`;

// ✓ 正确（用 Unicode escape）
const str = `\u0000asm`;
```

Cesium bundled 版本直接把 WASM bytes 嵌入 template literal，导致 `\0asm` 报错。

### 3. 正确的 WASM 加载方式

```js
// 外部文件加载
async function loadWasm() {
  const response = fetch('/cesium/ThirdParty/draco_decoder.wasm');
  const buffer = await response.arrayBuffer();
  const module = await WebAssembly.instantiate(buffer);
  return module.instance.exports;
}

// Base64 编码（如果必须内嵌）
async function loadWasmFromBase64(base64) {
  const binary = atob(base64);
  const buffer = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    buffer[i] = binary.charCodeAt(i);
  }
  return WebAssembly.instantiate(buffer);
}
```

## 手动配置 vs 插件自动化

理解原理后，可以手动配置：

### 开发环境

```js
// vite.config.js - 手动配置
export default defineConfig({
  define: {
    CESIUM_BASE_URL: JSON.stringify('/cesium')
  },
  
  // 复制资源（开发时）
  plugins: [
    {
      name: 'copy-cesium',
      buildStart() {
        fs.copy('node_modules/cesium/Build/Cesium', 'public/cesium');
      }
    }
  ]
});
```

### 生产环境

```bash
# 构建后手动复制
cp -r node_modules/cesium/Build/Cesium dist/cesium
```

### HTML 配置

```html
<head>
  <script>
    window.CESIUM_BASE_URL = '/cesium';
  </script>
  <link href="/cesium/Widgets/widgets.css" rel="stylesheet">
</head>
```

## vite-plugin-cesium vs Next.js 手动配置

| 方面 | vite-plugin-cesium | Next.js 手动 |
|------|-------------------|--------------|
| 资源复制 | 自动 | 手动复制到 public |
| CESIUM_BASE_URL | define 注入 | Script 标签 |
| WASM 问题 | 可能遇到 | Source 入口绕过 |
| 打包器 | Vite/Rollup | Webpack alias |
| 复杂度 | 低（插件自动化） | 高（需理解原理） |

## 总结

vite-plugin-cesium 解决的问题：
1. **自动化** - 无需手动复制资源、设置变量
2. **一致性** - 确保 CESIUM_BASE_URL 与资源路径匹配
3. **简化配置** - 一行代码完成所有配置

理解原理的意义：
- 遇到问题时能定位原因
- 在非 Vite 环境（Next.js webpack）能手动配置
- 理解 Cesium 的运行机制，更好地优化性能