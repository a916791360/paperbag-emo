# Paperbag Emo (`paperbag-emo`)

> **深夜纸袋人 & 慵懒黑猫（Paperbag & Black Cat）** —— 统一炭笔墨线、圆形半调网点与深夜电影感配色的 **AI Agent 个人 IP 图片与短视频创作 Skill**。  
> 从**一图流科普/情绪解释图**、**无白边透明插画素材**到 **9:16 漫画电影感 BPM 卡点短视频**，全流程本地可复现（`Python + Pillow + FFmpeg`），零外部付费视频 API 依赖，采用 **MIT** 协议开源。

[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](LICENSE)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-007808)

---

## 这个项目可以干什么？（图片 + 视频全链路创作）

`paperbag-emo` 围绕同一套 IP 视觉语言，严格划分为**图片创作（Mode A / Mode B）**与**视频创作（Mode C）**三大生产模式：

### 1. 图片创作：做解释图 & 可复用透明素材

- **Mode A — 概念 / 机制 / 情绪一图流解释图（Explanatory Image）**
  - **适用场景**：公众号文章配图、小红书干货/情绪图文、产品机制拆解、双态对比图。
  - **核心能力**：先产出 8 字段结构化 `Visual Brief`，再以 `Text (verbatim)` 逐字锁定中英文标签直接成图；通过真实物件、光影对比与清晰路径（1 个核心动作、至多 3 个视觉区块），让读者在 **10 秒内看懂一个概念或情绪转折**。支持标签错字单点纠错重试。
- **Mode B — 无白边可复用透明插画资产（Transparent RGBA PNG）**
  - **适用场景**：PPT 演讲插图、视频前景贴纸、文章装饰元素、封面与海报排版。
  - **核心能力**：支持单独绘制**纸袋人**、**慵懒黑猫**、**二者组合**或**纯炭笔墨线独立物件**（台灯、咖啡杯、笔记本、雨伞、时钟等）。配合内置抠图脚本 [scripts/cutout.py](scripts/cutout.py) 去绿幕（`#00FF00` / `#FF00FF`）与去色溢处理，专门保护暖棕牛皮纸袋与炭黑卫衣不透光（`--non-key-opaque-threshold 115`），且**不加白色贴纸描边**，在深暗青夜幕和米白手账底色上都能干净融合。

### 2. 视频创作：做 9:16 漫画电影感卡点短视频

- **Mode C — 9:16 漫画电影感 BPM 卡点视频（`cinema_emo` Motion Comic）**
  - **适用场景**：抖音 / 视频号 / 小红书竖屏深夜 emo 独白、金句短片、情绪故事、节奏化口播/字幕短剧。
  - **核心能力**：输入一段文案，Agent 自动完成**「一文案一分镜」导演拆解**与本地视频合成：
    - **双生图协作路径**：支持 **Path A 外置生图协作**（一键生成适配 Gemini Nano Banana 2.5 / Midjourney / 即梦的中英文 `Prompt Pack`，收回母图后由脚本自动裁切 B 机位特写并接入眨眼帧），也支持 **Path B 本地透明贴纸直出**。
    - **文案驱动节奏与景别轮换**：按文案字数动态决定镜头数与总时长（短句 `10–15s` / 中段独白 `16–28s` / 长叙事 `30–55s`），强制相邻两幕景别轮换（远景确立 → 物件空镜 → 中近景动作 → B 机位极近景特写 → 回眸/光影收尾），并支持中文标点智能断句与 `--validate` 可读性校验。
    - **电影感视听渲染（[scripts/render_emo_video.py](scripts/render_emo_video.py)）**：纯本地 `Python + Pillow + FFmpeg` 渲染 `1080×1920` 竖屏成片，集成 80/20 强明暗 `35mm midnight_emo` 调色、零 HUD 纯净电影画幅（`hud: "none"`）、舞台与字幕解耦转场、逐字入场动效、关键词暖琥珀光晕与手绘笔刷下划线、人/猫自然眨眼（`natural_blink`）、2.5D 视差、自动暖光源定位（`light_pos: "auto"`）及雨丝/景深散景/热气/黑猫 `z Z z` 呼噜波纹/路灯闪烁等微动态，导出抖音无声成片（`_silent.mp4`）与本地节拍预览版（`_beat_preview.mp4`）。

---

## 视频成片效果一览（Mode C · External Banana 2.5 + 本地合成）

> 以下分镜静帧均由 **外置生图模型（Gemini Nano Banana 2.5）生成母图** 后，经本项目 [scripts/render_emo_video.py](scripts/render_emo_video.py) 在本地完成 35mm 电影调色、微动态叠加、关键词手绘下划线与衬线字幕排版合成（零 HUD 纯净电影画幅）。

### 1. 《三千梨树六百湘水》（4 景别分镜节选 · 74 BPM · 22.30s）

对应配置：[studio/sanqian_timeline.json](studio/sanqian_timeline.json) | 提示词包：[studio/sanqian_prompt_pack.md](studio/sanqian_prompt_pack.md)

![Mode C Motion Comic Storyboard - Sanqian](examples/mode_c_motion_comic_strip.jpg)

- **远景确立**（末班车厢 + 黑猫 `cat_zzz`） → **诗意空镜**（梨花与湘水孤灯 + `luma_fade` 转场） → **中近景情绪**（掌心花瓣微光 `prop_pulse` + 自然眨眼） → **街灯回眸收尾**（`warm_dissolve` + 路灯闪烁与散景）。

### 2. 《克制与想念》&《产生怜惜》（跨文案 80/20 光影与天气微动态）

对应配置：[studio/xiangni_timeline.json](studio/xiangni_timeline.json) / [studio/lianxi_timeline.json](studio/lianxi_timeline.json)

![Mode C Cinema Works - Xiangni and Lianxi](examples/mode_c_cinema_works.jpg)

- 涵盖手机冷暖光脉冲、雨窗玻璃雨丝特写（`rain_glass`）、路灯耳机长椅、雨夜伞下递热饮（`coffee_steam` + `lamp_flicker`）等定制分镜；支持通过 `crop_box` 从单张母图自动推近裁切出 B 机位情绪极近景，减少重绘成本同时保持角色一致。

---

## IP 角色与视觉规范（Character Anchor）

所有图片与视频分镜均锁定统一视觉语言，使用外置生图模型时建议将 [assets/master_ref.jpg](assets/master_ref.jpg) 作为角色特征参考图上传：

- **主角（Paperbag）**：折叠牛皮纸袋头套（底部锯齿边缘）、细黑圆框眼镜、小黑点眉眼、宽大炭黑连帽卫衣、白色漫画手。
- **搭档（Black Cat）**：圆润炭黑短毛猫、小尖耳、极简胡须与克制神态（可按文案需求单独出现、双角色同框，或在纯空镜中隐去）。
- **色彩与线稿纪律**：炭笔黑变粗细轮廓 + 圆形半调网点阴影；全片严格克制为**暖琥珀（Warm Amber）+ 冷暗青（Muted Slate-Teal）**双强调色。

<p align="center">
  <img src="assets/master_ref.jpg" alt="Paperbag and Black Cat Character Anchor" width="280" />
</p>

> 提示：若你希望使用新的 Banana 2.5 版本补齐 **Mode A（概念/情绪解释图）**、**Mode B（透明贴纸资产）** 或重绘新版角色基准图，可直接使用已准备好的 [studio/readme_assets_prompt_pack.md](studio/readme_assets_prompt_pack.md)。

---

## 三模式能力总览

| 模式 | 产出类型 | 核心用途 | 输入 | 输出产物 | 核心脚本 / 规范 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mode A** | 图片（完整解释图） | 概念科普、机制对比、情绪一图流 | 主题 / 观点 + 2–6 个标签 | 完整 PNG / WebP / JPG 插画 | [SKILL.md](SKILL.md)（Visual Brief + `Text (verbatim)`） |
| **Mode B** | 图片（透明资产） | PPT、排版插图、封面、视频前景 | 动作 / 物件描述（绿幕或透明底） | 无白边 RGBA 透明 PNG | [scripts/cutout.py](scripts/cutout.py) |
| **Mode C** | 视频（9:16 竖屏） | 抖音/小红书/视频号卡点情绪短片 | 文案脚本 + `timeline.json`（+ 外置/内置画格） | `_silent.mp4` + `_beat_preview.mp4` | [scripts/render_emo_video.py](scripts/render_emo_video.py) |

---

## 快速安装与使用（Quick Start）

### 1. 环境依赖

- **Python** `3.10+` & **Pillow**（`pip install pillow`）
- **FFmpeg**（确保 `ffmpeg` 在 `PATH` 中：`brew install ffmpeg` / `winget install Gyan.FFmpeg` / `sudo apt install ffmpeg`）

### 2. 作为 Agent Skill 安装

```bash
npx skills add a916791360/paperbag-emo
```

或手动复制本仓库目录至你的 Agent Skill 目录（例如 `~/.gemini/config/skills/paperbag-emo` 或 `~/.claude/skills/paperbag-emo`）。

### 3. Mode C 视频引擎命令行用法

```bash
# 1) 检查 FFmpeg 与跨平台中文字体探测（macOS / Windows / Linux）
python3 scripts/render_emo_video.py --check

# 2) 渲染前校验分镜字数断句、高亮词、景别多样性与拍数节奏
python3 scripts/render_emo_video.py --validate --timeline studio/sanqian_timeline.json

# 3) 渲染 9:16 竖屏无声成片（上传抖音自选配乐）与节拍预览版
python3 scripts/render_emo_video.py \
  --timeline studio/sanqian_timeline.json \
  --out studio/output/sanqian_cinema \
  --theme late_night \
  --fps 30
```

> 引擎同时支持 `late_night`（深夜暗青）与 `paper_cream`（手账米白）双主题以及 `--bg` 自定义背景图；在 `cinema_emo` 模式下默认采用 `"hud": "none"` 与 `"color_grade": "midnight_emo"`。

### 4. Mode B 去绿幕与去色溢抠图用法

```bash
python3 scripts/cutout.py source.jpg assets/stickers/new_pose.png \
  --transparent-threshold 32 \
  --opaque-threshold 220 \
  --non-key-opaque-threshold 115
```

### 5. 运行单元测试

```bash
python3 -m unittest discover -s tests -v
```

---

## 仓库目录结构

```text
├── SKILL.md                           # Skill 主规范（Mode A / B / C 完整工作流与导演法则）
├── LICENSE                            # MIT 开源协议
├── agents/openai.yaml                 # 多宿主 Skill 元数据
├── assets/
│   ├── master_ref.jpg                 # IP 角色基准参考图
│   └── stickers/                      # 透明动作库（thinking / emo_hug / emo_hug_blink / calm_cup）
├── examples/                          # GitHub README 成片与分镜展示图
├── scripts/
│   ├── cutout.py                      # Mode B 去绿幕与去色溢抠图脚本
│   └── render_emo_video.py            # Mode C 9:16 漫画电影与卡点渲染引擎
├── studio/
│   ├── sanqian_timeline.json          # 示例工程 1：《三千梨树六百湘水》（+ sanqian_prompt_pack.md）
│   ├── xiangni_timeline.json          # 示例工程 2：《克制与想念》（+ xiangni_prompt_pack.md）
│   ├── lianxi_timeline.json           # 示例工程 3：《产生怜惜》（+ lianxi_prompt_pack.md）
│   ├── readme_assets_prompt_pack.md   # Mode A / B / 基准图外置生图提示词包
│   └── scenes/                        # 分镜母图与眨眼帧目录
└── tests/
    └── test_pipeline.py               # 断句、校验、裁切、字幕解耦与抠图单元测试
```

---

## License

本项目采用 [MIT License](LICENSE) 开源协议。
