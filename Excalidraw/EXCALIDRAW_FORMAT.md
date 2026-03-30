# Excalidraw 文件格式说明

## 问题背景

在 Obsidian 的 Excalidraw 插件中打开 .excalidraw 文件时报错：
```
Error loading drawing: Cannot read properties of undefined (reading 'hasOwnProperty')
```

## 原因分析

Excalidraw 文件需要完整的 JSON 结构，缺少关键字段会导致解析失败。之前的文件存在以下问题：

1. **缺少必要字段**：`angle`, `strokeColor`, `backgroundColor`, `fillStyle`, `strokeWidth`, `strokeStyle`, `roughness`, `opacity`, `groupIds`, `frameId`, `roundness`, `seed`, `version`, `versionNonce`, `isDeleted`, `boundElements`, `updated`, `link`, `locked` 等

2. **`source` 字段错误**：应设置为 `"https://excalidraw.com"`，而不是自定义描述

3. **缺少 `appState` 和 `files`**：根对象需要包含这两个字段

## 正确格式

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "id": "unique-id",
      "type": "rectangle|text|arrow|ellipse|line",
      "x": 100,
      "y": 100,
      "width": 200,
      "height": 100,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": {"type": 3},
      "seed": 1,
      "version": 1,
      "versionNonce": 1,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1,
      "link": null,
      "locked": false,
      // 文本元素额外需要：
      "fontSize": 16,
      "fontFamily": 1,
      "text": "文本内容",
      "textAlign": "center",
      "verticalAlign": "top",
      "containerId": null,
      "originalText": "文本内容",
      "lineHeight": 1.25
    }
  ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## 必要字段清单

### 根对象
| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | string | 固定值 `"excalidraw"` |
| `version` | number | 固定值 `2` |
| `source` | string | 固定值 `"https://excalidraw.com"` |
| `elements` | array | 图形元素数组 |
| `appState` | object | 应用状态 |
| `files` | object | 文件对象（可为空） |

### 元素通用字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一标识 |
| `type` | string | 元素类型：rectangle/text/arrow/ellipse/line |
| `x`, `y` | number | 坐标位置 |
| `width`, `height` | number | 尺寸 |
| `angle` | number | 旋转角度，通常为 0 |
| `strokeColor` | string | 描边颜色，如 `"#1e1e1e"` |
| `backgroundColor` | string | 背景色，如 `"#a5d8ff"` 或 `"transparent"` |
| `fillStyle` | string | 填充样式：`"solid"` / `"hachure"` / `"cross-hatch"` |
| `strokeWidth` | number | 描边宽度 |
| `strokeStyle` | string | 描边样式：`"solid"` / `"dashed"` / `"dotted"` |
| `roughness` | number | 粗糙度 0-2 |
| `opacity` | number | 不透明度 0-100 |
| `groupIds` | array | 所属分组 ID |
| `frameId` | null | 帧 ID |
| `roundness` | object/null | 圆角 `{"type": 3}` |
| `seed` | number | 随机种子 |
| `version` | number | 版本号 |
| `versionNonce` | number | 版本随机数 |
| `isDeleted` | boolean | 是否删除 |
| `boundElements` | null | 绑定元素 |
| `updated` | number | 更新时间戳 |
| `link` | null | 链接 |
| `locked` | boolean | 是否锁定 |

### 文本元素额外字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `fontSize` | number | 字体大小 |
| `fontFamily` | number | 字体：1=手写, 2=代码, 3=标准 |
| `text` | string | 文本内容 |
| `textAlign` | string | 对齐：`"left"` / `"center"` / `"right"` |
| `verticalAlign` | string | 垂直对齐：`"top"` / `"middle"` |
| `containerId` | null | 容器 ID |
| `originalText` | string | 原始文本 |
| `lineHeight` | number | 行高，通常 1.25 |

## 验证方法

1. 在浏览器打开 https://excalidraw.com
2. 将 .excalidraw 文件拖入页面
3. 能正常显示则格式正确

## 注意事项

- 所有字段都必须存在，即使是 null 或默认值
- `source` 必须是 `"https://excalidraw.com"`
- 颜色格式为 hex 字符串，如 `"#1e1e1e"`
- 文本换行使用 `\n`