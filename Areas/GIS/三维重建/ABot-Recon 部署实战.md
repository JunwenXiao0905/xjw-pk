# ABot-Recon 部署实战（WSL2 + RTX 5070）

> 高德开源的流式 3D 重建模型，单目 RGB 视频 → 相机轨迹 + 全局点云。
> 行业背景与模型解读 → [[Areas/赛道观察/GIS/02_技术专项/三维重建/行业线索|行业线索]]
> 环境底座（WSL2/显卡/代理）→ [[WSL2 从零配置指南]]
> 2026-08-31 全流程验证通过：142 帧，约 7 fps，效果正常。

## 1. 项目信息

- 仓库：https://github.com/amap-cvlab/ABot-Recon （中文 README：README_ZH.md）
- 论文：arXiv 2608.27529
- 权重：HuggingFace `acvlab/ABot-Recon`（约 4GB，首次运行自动下载，缓存在 `~/.cache/huggingface/`；下载需代理）
- 要求：Linux（WSL2 可）/ Python ≥3.10 / 支持 CUDA 的 GPU

## 2. 环境安装（关键坑：torch 版本）

仓库把 `torch==2.5.1` 钉死，但 **RTX 50 系（Blackwell，sm_120）必须 PyTorch 2.7+ 的 cu128**，否则 CUDA 不可用。绕法：装包不带依赖，依赖手动补。

```bash
conda create -n abot python=3.11 -y && conda activate abot

# PyTorch 用 cu128（覆盖清华源的默认版本，保证 torch/torchvision 配套）
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

git clone https://github.com/amap-cvlab/ABot-Recon.git
cd ABot-Recon
pip install -e . --no-deps          # 关键：跳过依赖解析，避免 torch 被降级
pip install "einops>=0.7" "huggingface-hub>=0.34,<1.0" "numpy>=1.24" \
  "omegaconf>=2.3" "pillow>=9.5" "safetensors>=0.4" "tqdm>=4.66"

# 验证：输出 2.x+cu128 / True / 显卡名
python -c "import torch, abot_recon; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

装完 pip 会红字报 "requires torch==2.5.1 ... incompatible"，**预期内，无视**。

## 3. 准备数据（视频抽帧）

仓库不含示例数据，`--image-dir` 要自己准备**零填充命名的 jpg 序列**（字典序=时间序）。

```bash
sudo apt install -y ffmpeg
mkdir -p ~/data/test_seq
# 横屏拍、边走边拍、场景有纵深，效果才好；竖屏/静止镜头重建会退化
ffmpeg -i "/mnt/c/Users/PC/Downloads/video.mp4" -vf fps=10,scale=504:-2 -qscale:v 2 ~/data/test_seq/%06d.jpg
```

- `fps=10`：30fps 降采样，帧数少 2/3，质量基本无损
- `scale=504:-2`：504 宽接近论文基准分辨率（504×280），速度/显存友好
- 想只取前 N 帧：加 `-frames:v 150`

## 4. 运行推理

```bash
proxy_on    # 首次要下 4GB 权重（HuggingFace 境外）
python demo.py --image-dir ~/data/test_seq --output-dir outputs/demo \
  --attention-backend auto --no-loop-closure --save-world-points
proxy_off
```

日志里 `Warning, cannot find cuda-compiled version of RoPE2D` 是可选加速组件未装（cuRoPE），自动退回慢速实现，功能正常。

## 5. 导出与可视化

输出全是 `.pt/.npy` 张量（world_points.pt 230M、colors.pt、confidence.pt、camera_poses.npy 等），用自带脚本转 PLY + BEV 轨迹图：

```bash
python scripts/export_reconstruction_ply.py \
  --output outputs/demo/recon.ply \
  --poses outputs/demo/camera_poses.npy \
  --points outputs/demo/world_points.pt \
  --colors outputs/demo/colors.pt \
  --confidence outputs/demo/confidence.pt \
  --bev-output outputs/demo/bev.png
```

- 点云太密/卡：加 `--point-stride 2` 或 `--max-points 2000000`
- 过滤低质量点：加 `--confidence-threshold`（越小越严格）

**查看方式**：从 `\\wsl$\Ubuntu\home\<用户>\projects\ABot-Recon\outputs\demo` 把 `recon.ply`、`bev.png` 拷到 Windows。
- `bev.png` 直接双击看轨迹
- `recon.ply` 用 **MeshLab**（Microsoft Store 可装）打开，点云+相机位姿锥，硬件加速流畅
- ⚠️ WSLg 里 open3d 可视化（OpenGL/GLEW）起不来，试过 `LIBGL_ALWAYS_SOFTWARE=1`、`unset WAYLAND_DISPLAY` 均无效，别再折腾，直接用 Windows 原生软件

## 6. 实测性能（RTX 5070 12GB / 504×896 竖屏）

| 指标 | 本机实测 | 官方基准（H100，504×280） |
|---|---|---|
| 速度 | ≈ 7 fps | 24.45 fps |
| 显存 | 未记录（有余量） | 6.71 GiB 峰值 |

- 显存**与视频长度无关**（流式 12 帧窗口），只随分辨率涨；默认上限 22000 帧（`--max-frames`）
- 提速三板斧：降分辨率、`fps=10` 降采样、编译 cuRoPE（需 CUDA toolkit，优先级低）
- 一万帧 ≈ 24 分钟（@7fps）

## 7. 待办 / 后续

- [ ] 换手持横屏视频重新验证重建质量（现有素材为 4.7s 竖屏，仅链路验证）
- [ ] 回环检测：需补装 `faiss-cpu opencv-python pypose scipy`，跑 `--loop-closure` 对比
- [ ] 官方训练代码 2026-09-30 前发布，届时 `git pull` 跟进
- [ ] Python API 二次开发：`ABotRecon.from_pretrained(...)` → `model.infer(images)`，返回 camera_poses / relative_poses / local_points / confidence
