# 渲染内核

渲染内核层项目的专项深拆笔记（对应《行业线索.md》§3.1 / §5）：

- Navara（路线 C：Rust+WASM headless GIS 核心 + 可替换渲染器，当前 Three.js）
- Galileo（路线 A：全 Rust + wgpu 直渲）
- MapGPU（路线 B：TS API + Rust/WASM 空间核心 + WGSL）
- maplibre-rs（路线 A，已停滞，存档观察）

主结论与优先级见 [../行业线索.md](../行业线索.md)。单个项目准备系统拆源码时，在此目录建独立笔记。
