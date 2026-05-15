# Next.js集成Cesium踩坑记录

## 1. Turbopack 不兼容

```bash
pnpm add cesium
```

项目中 `import * as Cesium from 'cesium'`，运行 `pnpm dev` 报错：

```
Error: Cesium.js is not compatible with Turbopack
```

解决：切换 webpack

```json
{
  "scripts": {
    "dev": "next dev --webpack",
    "build": "next build --webpack"
  }
}
```

## 2. 静态资源 404

再次运行，控制台报：

```
CESIUM_BASE_URL is not defined
/Workers/cesiumTerrainProcessor.js 404
```

Cesium 运行时需要 Workers/WASM/Assets，但这些文件不在项目中。

解决：复制到 public + 设置 CESIUM_BASE_URL

```bash
cp -r node_modules/cesium/Build/Cesium/* public/cesium/
```

```tsx
// app/layout.tsx
<Script id="cesium-base-url" strategy="beforeInteractive">
  {`window.CESIUM_BASE_URL = '/cesium';`}
</Script>
```

本地开发正常。

## 3. 生产 WASM SyntaxError

构建镜像部署后，页面报错：

```
Uncaught SyntaxError: Octal escape sequences are not allowed in template strings.
```

排查发现打包后的 chunk 文件包含 `\0asm`：

```bash
docker exec x-dimension-next grep -r "\\0asm" /app/.next/static/chunks/
# 710ab089.xxx.js 包含问题代码
```

**本质**：Cesium bundled 入口把 WASM 文件内容硬编码为 template literal：

```js
// Build/Cesium/index.cjs 中的代码
}(`\0asm\0\0\0...`)  // WASM magic bytes 作为字符串
```

`\0` 在 ES6 template literal 中被视为八进制转义，语法禁止，解析阶段直接报错。

## 4. Source 入口绕过

Cesium Source 入口没有 WASM 内嵌，但 package.json exports 禁止访问：

```json
{
  "exports": {
    "./Source/*.js": null
  }
}
```

解决：webpack alias 绑过 exports

```typescript
// next.config.ts
import path from "path";

const nextConfig = {
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.alias = {
        'cesium': path.resolve(__dirname, 'node_modules/cesium/Source/Cesium.js'),
      };
    }
    return config;
  },
};
```

构建后检查，仍有 `\0asm`，来源是 `@spz-loader/core`（@cesium/engine 的依赖，用于 Gaussian Splatting）。

解决：排除这个依赖

```typescript
config.resolve.alias = {
  'cesium': path.resolve(__dirname, 'node_modules/cesium/Source/Cesium.js'),
  '@spz-loader/core': false,
};
```

## 最终配置

```typescript
// next.config.ts
import path from "path";

const nextConfig = {
  output: 'standalone',
  webpack: (config, { isServer }) => {
    config.ignoreWarnings = [
      { module: /cesium/ },
      { module: /@spz-loader/ },
    ];

    if (!isServer) {
      config.resolve.alias = {
        'cesium': path.resolve(__dirname, 'node_modules/cesium/Source/Cesium.js'),
        '@spz-loader/core': false,
      };
    }
    return config;
  },
};
```

## 总结

| 问题 | 原因 | 解决 |
|------|------|------|
| Turbopack 不兼容 | Cesium CommonJS 结构 | 切 webpack |
| 静态资源 404 | Workers/WASM 未复制 | 手动复制 + CESIUM_BASE_URL |
| WASM SyntaxError | bundled 入口内嵌 `\0asm` | Source 入口 + alias 绑过 exports |
| @spz-loader 问题 | 依赖也有 WASM 内嵌 | alias 置 false |

核心教训：Cesium bundled 入口有 WASM 内嵌问题，必须用 Source 入口。package exports 限制访问，用 webpack alias 绕过。