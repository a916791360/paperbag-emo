# 项目交接与上下文备忘（Paperbag Emo 个人 IP 仓库）

> **来源会话**：由无工作区会话迁移并整理至此仓库根目录 `/Users/qingmeng/Documents/Antigravity/个人IP`。

## 1. 已确定的核心方向与设计原则
- **IP 选型**：方案一「**深夜纸袋人 + 慵懒黑猫**」（基准参考图：[assets/master_ref.jpg](assets/master_ref.jpg)）。
- **核心约束**：全程由 Antigravity 内置能力 + 本地开源工具链（`python3` + `Pillow` + `ffmpeg`）闭环运行，**不调用外部大模型/生图/生视频 API Key**；音频暂时输出无声卡点视频供抖音发布时自选音乐，同时附带本地合成节拍预览版。
- **架构对齐标准**：已逆向对标 `oil-visual` 完成第一阶段静态能力对齐：
  - **Mode A**：完整概念/情绪解释图（8 字段 `visual brief` + `Text (verbatim)` 逐字防错 + 错字单点 Retry）。已通过 `examples/asc-multimodal-explainer.jpg` 实测验收。
  - **Mode B**：透明插画资产（支持纸袋人 / 黑猫 / 二者组合 / 独立炭笔墨线物件；`#00FF00` 绿幕 + `scripts/cutout.py` 含 `--non-key-opaque-threshold 115` 保护暖棕纸袋与炭黑卫衣；禁止白色贴纸描边）。
  - **Mode C**：固定 BPM 严格卡点 9:16 视频合成（`scripts/render_emo_video.py`）。

## 2. 当前仓库文件结构
- `SKILL.md`：Skill 主规范（对齐 `oil-visual` 结构 + Mode C 插槽）
- `agents/openai.yaml` & `LICENSE`：多宿主 Skill 元数据与 MIT 协议
- `assets/master_ref.jpg`：IP 唯一角色设定基准图
- `assets/stickers/`：已抠图质检通过的透明动作库（`thinking.png`、`emo_hug.png`、`calm_cup.png`）
- `scripts/cutout.py`：增强版去绿幕与去色溢脚本
- `scripts/render_emo_video.py`：9:16 BPM 卡点渲染脚本（输出 `_silent.mp4` 与 `_beat_preview.mp4`）
- `examples/asc-multimodal-explainer.jpg`：Mode A 实测成品示例
- `studio/`：示例分镜 `demo_timeline.json` 与已生成的演示成片

## 3. 下一阶段待办（Phase 2）
1. **精细化升级 Mode C 视频引擎（`scripts/render_emo_video.py`）**：
   - 跨平台中文字体自动探测（兼容 macOS / Windows / Linux，避免开源后别人运行出方块乱码）
   - 支持更多主题底色（深夜暗青 / 手账米白）与丰富转场/动效（镜头推拉、手绘箭头/划线、文字逐字卡点节奏优化）
   - 支持自定义背景图与环境依赖自检提示
2. **开源发布级打磨**：
   - 补充 `examples/` 更多代表图（Mode B 纯物件透明素材、Mode A 情绪图、Mode C 动图/截图）
   - 撰写 GitHub 开源门面 `README.md`（含视觉头图、`npx skills add` 安装方式与使用示例）
   - 若需本地同步全局 Skill，可将本仓库同步至 `~/.gemini/config/skills/paperbag-emo`
