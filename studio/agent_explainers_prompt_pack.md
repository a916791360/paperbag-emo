# Paperbag Emo Mode A v2 · 《AI Agent 工程底层三部曲》解释图套装 & 提示词包

> **选题主线**：跳出“Agent = 大模型 + 工具”的浅层科普，直击真实工程落地最核心的 3 个底层机制：
> 1. **单会话衰减**：《Agent 上下文腐烂（Context Rot）》— 已生成并核验：`studio/explainers_agent/01_context_rot.png`
> 2. **执行态自纠**：《Agent 自纠闭环（ReAct Loop）》— 见下方完整可复制中/英文 Prompt（因内置生图模型触发 429 配额上限待补跑，可直接贴入外置模型生成）
> 3. **多体架构真相**：《多 Agent 上下文隔离（Context Isolation）》— 已生成并核验：`studio/explainers_agent/03_multi_agent_isolation.png`

---

## 图 1｜《Agent 上下文腐烂》（已成图）

- **成品路径**：`studio/explainers_agent/01_context_rot.png`
- **参考图**：`assets/master_ref.jpg` + `examples/mode_a_context_window.png`
- **主体配置**：纸袋人（左过载工位）+ 黑猫（右清爽工位）
- **语义双色**：**陶土橙**（噪声堆积与过载刻度表）vs **雾灰绿**（压缩摘要卡片与健康低载表盘）
- **图内已核验实体标签（5 个）**：`Agent 上下文腐烂`、`全程堆日志`、`指令被淹没`、`压缩后交接`、`注意力聚焦`

---

## 图 2｜《Agent 自纠闭环（ReAct Loop）》（完整可直接复制外置生图）

- **目标输出路径**：`studio/explainers_agent/02_react_loop.png`
- **建议画幅**：`3:4` 竖图
- **建议上传参考图**：`assets/master_ref.jpg`（锁定纸袋人特征）+ `examples/mode_a_survivorship_bias.png`（锁定 Mode A v2 铆钉墙牌与半调质感）
- **主体配置**：纸袋人独角（无黑猫）
- **语义双色**：**陶土橙**（上层无反馈盲跑的断轨火花与残次箱）vs **雾灰绿**（下层闭环修正后的绿勾闸门与达标托盘）
- **图内实体标签（6 个）**：`Agent 自纠闭环`、`无反馈盲跑`、`错漏直出`、`调用工具`、`看报错修正`、`验证后交付`

### English Prompt（推荐直接粘贴到 Gemini / Nano Banana 2.5，附上述两张参考图）
```text
Create a 3:4 vertical Mode A editorial manga-ink knowledge-explainer illustration explaining the engineering core of an AI Agent: an open-loop single pass blindly pushes broken output straight out when hitting an error (upper track), whereas a true Agent runs a ReAct Observe-Verify-Retry feedback loop that inspects real tool errors, loops back to fix them, and delivers verified output (lower track).

Character & style anchor: Strictly match the Paperbag protagonist from the character reference image (folded kraft-brown paper bag head with jagged bottom rim, thin round black wire glasses, dot eyes, oversized dark charcoal hoodie, simple white manga hands). Render ONLY the Paperbag protagonist — STRICTLY NO black cat. Match the clean varied charcoal-black ink outlines, classic circular halftone screentone shadows, grounded editorial workshop aesthetic, and riveted wall signboards of the benchmark diagram.

Grounded real environment: Finished off-white lightly textured editorial workshop split cleanly into an upper track band and a larger lower feedback-loop workbench section, with subtle floor/shelf lines, circular halftone shadows, and an overhead hanging lamp casting a subtle warm-amber glow onto the lower inspection station.

Upper section (Open-loop blind run — muted terracotta-orange):
- Mounted on the upper-left wall is a crisp framed riveted wall plaque reading "无反馈盲跑".
- A straight one-way mechanical rail runs left to right across the upper band. A document/gear module rolls blindly straight past a cracked obstacle with muted terracotta-orange error sparks ignored, tumbling directly into a crooked muted terracotta-orange output bin on the upper right with crisp text printed directly on its front face reading "错漏直出".

Lower section (ReAct feedback loop — Paperbag protagonist + muted sage-green verified delivery):
- A clean, unmistakable circular mechanical workbench track forms a visible feedback loop across the lower half:
  1. Left station: a compact mechanical arm holding a wrench/terminal executes an action beside a crisp riveted plaque reading "调用工具".
  2. Center inspection station (lit by the subtle warm-amber hanging lamp): when the item hits a small error flag/hurdle, the Paperbag protagonist alone leans closer holding a magnifying glass inspecting the real error output.
  3. Below the track, a bold clear curved return arrow loops smoothly back from the inspection station to the tool station, bearing a crisp riveted loop plaque reading "看报错修正".
  4. Right exit (muted sage-green): after looping and fixing, the corrected item passes smoothly through a raised green checkmark gate along a muted sage-green exit arrow into a sturdy muted sage-green delivery tray resting on the lower-right workbench, with crisp text printed directly on its front face reading "验证后交付".

Semantic color discipline: Charcoal ink black, off-white textured paper, circular halftone gray, kraft-brown (Paperbag head), dark charcoal (hoodie), subtle warm-amber lamp glow over the inspection station, plus strictly TWO muted editorial state colors: muted terracotta-orange (upper blind-run sparks & broken bin) and muted sage-green (lower verified gate, exit arrow, & finished tray).

Text (verbatim): Render these exact labels as part of the bitmap illustration:
"Agent 自纠闭环", "无反馈盲跑", "错漏直出", "调用工具", "看报错修正", "验证后交付".
Use each phrase exactly once. Do not translate, paraphrase, misspell, repeat, or add any other text. Use crisp modern Chinese sans-serif medium/bold typography, large and readable at mobile size. Mount "Agent 自纠闭环" on the centered top framed riveted wall signboard; mount "无反馈盲跑" on the upper-left wall plaque; print "错漏直出" on the front of the upper-right terracotta-orange bin; mount "调用工具" on the riveted plaque at the lower-left tool station; mount "看报错修正" on the riveted plaque along the curved return loop; print "验证后交付" on the front of the lower-right sage-green tray. Do not float bare text in empty whitespace.

No 3D, no glossy gradients, no photorealism, no generic card grid, no dashboard, no tiny text, no watermark.
```

### 中文提示词（备用）
```text
创作一张 3:4 竖版手绘炭笔墨线 + 圆形半调网点风格的科普知识解释图，严格参考附图中的纸袋人主角造型（牛皮纸袋头套、锯齿底边、细黑圆框眼镜、小黑点眼睛、宽松炭黑连帽卫衣、白色漫画手；本图仅出现纸袋人独角，不要出现黑猫）以及参考图中的带铆钉铭牌、实景工坊地面投影和低饱和编辑色风格。

画面核心机制（上下分区对比）：
- 顶部居中墙面挂一块带铆钉边框的主招牌，写着“Agent 自纠闭环”。
- 上半区（陶土橙告警）：左上墙面挂一块铆钉标牌“无反馈盲跑”。一条笔直单向滑轨从左通向右，任务模块无视中间的裂口与陶土橙报错火花一路盲冲，直接掉进右上角歪斜的陶土橙废品箱里，箱体正面印着“错漏直出”。
- 下半区（闭环自纠 + 雾灰绿验收）：搭建一条清晰的环形工坊轨道——左侧机械工具臂旁挂着铆钉小牌“调用工具”；中央检测台上方一盏吊灯洒下柔和暖琥珀光，纸袋人举着放大镜俯身查看报错细节；轨道下方用粗壮清晰的弯曲回环箭头从检测台绕回工具站，箭头上挂着铆钉标牌“看报错修正”；修正后的模块通过右侧雾灰绿对勾闸门，顺着雾灰绿箭头稳稳落入右下角雾灰绿成品托盘，托盘正面印着“验证后交付”。

文字要求（逐字精确，禁止增删改或漂浮裸字）：图内仅出现以下 6 组现代无衬线粗体中文字样，且每组只出现一次并牢固贴在对应铭牌/箱体表面：“Agent 自纠闭环”、“无反馈盲跑”、“错漏直出”、“调用工具”、“看报错修正”、“验证后交付”。不要 3D、不要写实照片、不要炫光渐变、不要水印。
```

---

## 图 3｜《多 Agent 上下文隔离》（已成图）

- **成品路径**：`studio/explainers_agent/03_multi_agent_isolation.png`
- **参考图**：`assets/master_ref.jpg`（仅黑猫）+ `examples/mode_a_caffeine_mechanism.png`
- **主体配置**：三座厚墙隔离工坊舱 + 顶层主控台黑猫监工（无纸袋人）
- **语义双色**：**冷灰蓝**（顶层总任务单与三条下发分流管道）vs **雾灰绿**（底层经滤嘴提纯后汇合的精炼结果托盘）
- **图内已核验实体标签（6 个）**：`多 Agent 上下文隔离`、`主 Agent 调度`、`检索`、`执行`、`校验`、`只回传精炼结果`
