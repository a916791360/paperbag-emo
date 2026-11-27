# 《悄无声息的告别》Mode C 升级版生图提示词包（Prompt Pack for Gemini Nano Banana 2.5 / Midjourney / 即梦）

> **导演拆解与 Mode C 2.1（方式二升级版）适配设计说明**：
> 1. **黄金完播时长**：文案共 98 字，拆解为 **7 幕高留存节奏分镜**（推荐 `74 BPM`，全片约 `25s`），由 **5 张定制母图** 支撑（第 4 幕与第 6 幕通过引擎 `camera_morph` 无重影推近特写）。
> 2. **首镜彻底防查重**：**图 1** 采用**纯物件微距空镜（深夜酒馆两只半满琥珀酒杯）**开场，与前作的天桥背影、窗边人物完全区隔，同时 100% 具象化首句「喝一场大酒」。
> 3. **天然适配升级版微动态**：图 2、图 3、图 4 均保留清晰圆框眼镜瞳孔（用于自动生成 3 帧 **5 阶平滑低频眨眼**）；图 2、图 3、图 4、图 5 的小黑猫均留有清晰独立轮廓（用于像素锁死 `cat_box` 呼吸起伏 + `cat_ear_box` 错拍轻抖耳）；图 5 预留宽阔江面灯火倒影（用于 `water_shimmer` 波光与 `mist_drift` 江雾）。
> 4. **参考图上传规则**：除 **图 1（酒杯微距空镜）** 无人物无需上传参考图外，其余 **图 2、图 3、图 4、图 5** 生图时请上传 [assets/master_ref.jpg](../assets/master_ref.jpg) 作为角色锚点，全部 **`9:16` 竖屏**，生成后放入 `studio/scenes/wusheng/` 即可一键渲染。

---

## 分镜节奏总览（Director Breakdown）

| 幕次 | 对应母图 | 景别 / 运镜 / 动效 | 字幕文案 |
| :--- | :--- | :--- | :--- |
| 第 1 幕 | 图 1 `s1_midnight_drinks_cutaway.jpg` | 纯物件斜俯近景（防查重钩子） | 一直觉得这世上告别仪式挺多，比如喝一场大酒、 |
| 第 2 幕 | 图 2 `s2_station_platform_tears.jpg` | 车站长椅侧面中景（夜雾+慢眨眼+猫微动） | 来一场旅行，又或者情不自禁在车站大哭一场。 |
| 第 3 幕 | 图 3 `s3_quiet_dusk_window.jpg` | 暮色窗边偏左中景（情绪骤静+微尘+猫呼吸） | 可是后来才知道，人生中大部分的告别， |
| 第 4 幕 | 图 3（`camera_morph` 推近） | 窗光半侧脸特写（5 阶平滑慢眨眼） | 是悄无声息的。 |
| 第 5 幕 | 图 4 `s4_ordinary_last_glance.jpg` | 黄昏寻常街角远中景（路人渐远+夜雾） | 原来某天的相见，竟已是最后一面， |
| 第 6 幕 | 图 4（`camera_morph` 推近） | 纸袋人微怔回望特写（5 阶平滑慢眨眼） | 此后即便不是隔山隔水， |
| 第 7 幕 | 图 5 `s5_same_city_river_lights.jpg` | 同城深夜江畔灯火大远景（波光+江雾+猫抖耳） | 也没有再重逢。 |

---

## 图 1（第 1 幕开场空镜：「一直觉得这世上告别仪式挺多，比如喝一场大酒、」）
- **目标保存路径**：`studio/scenes/wusheng/s1_midnight_drinks_cutaway.jpg`
- **是否上传参考图**：**否（纯现代生活物件微距空镜，无人物无动物）**
- **构图设计**：深夜街边温暖小酒馆木桌斜俯近景。一盏低垂的暖琥珀色暖光吊灯洒下柔和光晕，照亮木桌上两只喝到一半、透着温润琥珀色微光与细碎气泡的玻璃酒杯（一只略空、一只半满，桌上散落一两张揉皱的餐巾纸角，无多余杂物），四周 80% 沉入深邃静谧的午夜冷青暗影中。

### 中文提示词（复制即用）
```text
9:16 竖屏深夜王家卫/新海诚式 Lo-Fi 独立动画电影桌面微距叙事空镜剧照（无任何人物、手或动物出现）。80/20 强明暗冷暖对比：深夜安静的街边小酒馆深色木桌斜俯近景，80% 画面沉浸在深邃静谧的午夜深青黑暗影里，唯有画面中下部被一束从侧上方落下的暖琥珀色暖光温柔照亮（Soft Analog Halation）；暖光中央静静摆放着两只厚底玻璃酒杯，杯中残留着半杯透出温暖金琥珀色光泽的酒液与微光倒影，杯壁挂着细微水珠，桌上透出柔和的玻璃折射光斑（具象化“喝一场大酒”的告别仪式感）。手绘炭笔墨线（外轮廓略粗、细节纤细）、有机水彩墨色晕染、细腻圆形半调网点暗部与 35mm 胶片颗粒感。画面上方三分之一保留干净深邃的午夜冷青暗影留白用于放置电影字幕。严禁任何文字、酒瓶标签字母、多余纸袋与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film macro tabletop cutaway still (Wong Kar-wai / Makoto Shinkai / Lo-Fi indie animation atmosphere; zero characters, no hands, no animals). High-contrast 80/20 chiaroscuro lighting on a dark wooden pub table at midnight: 80% of the frame is steeped in deep midnight slate-teal and charcoal shadow, while a single warm amber overhead glow bathes the lower-center table with soft analog halation. Resting inside the golden pool of light are two heavy glass tumblers half-filled with glowing warm-amber drink, catching soft glass reflections, faint condensation droplets, and warm caustics on the wood—evoking a heartfelt farewell drink. Hand-drawn charcoal ink outlines with varied line weight, organic watercolor-ink wash, subtle circular halftone shadow texture, and 35mm film grain. Clean deep dark negative space across the upper third for film subtitles. No text, no bottle labels, no stray paper bags, no watermark.
```

---

## 图 2（第 2 幕：「来一场旅行，又或者情不自禁在车站大哭一场。」）
- **目标保存路径**：`studio/scenes/wusheng/s2_station_platform_tears.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **构图设计**：深夜露天火车站/轻轨站台候车长椅侧面中景。暖琥珀色站台灯下，纸袋人坐在长椅偏左，身旁立着一只炭黑色小号登机拉杆箱（具象化「来一场旅行」），纸袋人微微垂头、眉头轻蹙，一只白色漫画手抬起轻轻停在纸袋脸颊下方（不遮挡圆框眼镜与双黑点瞳孔，方便后期制作 5 阶自然慢眨眼），眼角一滴克制微亮的细小泪光；圆润的小黑猫安静蹲在长椅旁拉杆箱边的地面上，微微仰头望着他；背景右侧是夜雾中模糊亮着暖光的列车车厢轮廓。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人（折叠牛皮纸袋头、锯齿底边、细黑圆框眼镜、小黑点眼睛、炭黑连帽卫衣、白色漫画手）与圆润黑猫设定，绘制一张 9:16 竖屏深夜新海诚/王家卫式露天车站站台动画电影中景剧照。
80/20 强明暗冷暖对比：微雾弥漫的深夜露天火车站台，四周 80% 沉入深邃的午夜冷青蓝夜幕与夜雾，头顶侧后方一盏暖琥珀色站台灯洒下温柔包裹的金色光晕（Soft Analog Halation）；背景右侧远处是一列静静停靠或缓缓滑行的模糊列车暖光车窗剪影。画面中下部偏左侧的候车长椅上，纸袋人穿着宽大炭黑连帽卫衣坐着，身旁立着一只深灰色小号登机行李箱（具象化“来一场旅行”）；他微微低头，圆框眼镜后的小黑点眼睛清晰可见（绝对不要被手遮挡眼镜），轻蹙的眉头与镜片下方纸袋面上一道极细微的反光泪痕传递出“在车站情不自禁崩溃难过”的酸楚，一只白色漫画手自然微握搭在膝上或胸口卫衣上；圆润的小黑猫安静蹲坐在画面右下侧他脚边与行李箱旁的站台地面上，独立轮廓清晰，微微仰头心疼地看着他。手绘炭笔墨线、水彩夜雾晕染、圆形半调网点阴影与 35mm 胶片颗粒，上方三分之一保留干净深邃的午夜冷青夜空留白用于放置字幕。严禁任何文字、站牌字样、多余纸袋与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film medium shot on an open-air train platform at midnight, anchored to the Paperbag protagonist and chubby Black Cat from the reference image. 80/20 chiaroscuro lighting: surrounded by deep midnight slate-teal mist, a warm amber platform lamp casts soft golden light and analog halation over the lower-left waiting bench, while blurred warm train windows glow softly in the misty right background. Seated on the bench in an oversized dark charcoal hoodie beside a compact dark carry-on rolling suitcase (evoking a solo trip), the kraft-paperbag-head protagonist tilts their head slightly down with sorrowful brows and a tiny glinting tear below their round black wire glasses—keeping both glasses lenses and dot eyes completely unobstructed and clearly visible—with white manga hands resting gently on their knees/hoodie. Sitting cleanly on the platform floor in the lower-right near their sneakers and suitcase is the chubby black cat looking up comfortingly with a clean uncluttered silhouette. Hand-drawn charcoal ink outlines, atmospheric watercolor-ink wash, circular halftone shading, and 35mm film grain. Generous deep dark negative space across the upper third for subtitles. No text, no station signs, no stray paper bags, no watermark.
```

---

## 图 3（第 3 幕中景 & 第 4 幕 `camera_morph` 推近特写：「可是后来才知道，人生中大部分的告别，」/「是悄无声息的。」）
- **目标保存路径**：`studio/scenes/wusheng/s3_quiet_dusk_window.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **构图设计**：情绪由热烈急转极静的视觉转折！傍晚暮色将尽、未开灯的安静公寓玻璃窗边。窗外是寻常得不能再寻常的深青蓝暮色城市楼群与零星亮起的暖琥珀窗灯；纸袋人位于画面中下部偏左，微微侧身安静站在窗边（双手轻插卫衣口袋，眼神平静而空落，圆框眼镜与双黑点瞳孔清晰完整），一缕极轻的暮色余光斜照在窗框与半边纸袋上；圆润的小黑猫蜷伏在画面右下侧的宽木窗台上安静闭眼小憩。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏极致安静的暮色室内窗边独立动画电影中近景剧照。80/20 强明暗静谧对比：未开灯的安静房间窗边，80% 沉浸在深邃静谧的深青蓝与炭黑暗影中；右侧一扇干净的大玻璃窗外，是傍晚晚霞刚刚褪尽的寻常深青色城市楼群天际线，远处零星亮起几扇温柔微弱的暖琥珀色窗灯（Soft Analog Halation），一缕极轻的暮色斜光透过玻璃斜落进幽暗室内（具象化“没有喧闹与眼泪、悄无声息的告别”）。纸袋人站在画面中下部偏左侧窗边，身体呈四分之三侧面，双手自然插在宽大炭黑连帽卫衣口袋里，神情平静得近乎发空，细黑圆框眼镜与两个清晰的小黑点眼睛望向窗外静默发呆；圆润的小黑猫安静地趴在画面右下侧的木质窗台上闭眼打盹，独立轮廓完整清晰。手绘炭笔墨线、有机水彩深色晕染、细腻圆形半调网点阴影与 35mm 胶片颗粒，画面上方三分之一保持干净深邃的暗青墙面与室内夜影留白用于放置字幕。严禁任何文字、多余纸袋与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 ultra-quiet moody dusk anime film medium close-up still by an unlit apartment window, anchored to the Paperbag protagonist and chubby Black Cat from the reference image. 80/20 chiaroscuro lighting: 80% immersed in deep, silent slate-teal indoor shadow; through a large window on the right, an ordinary twilight city skyline fades into dark blue-teal dusk with a few distant warm-amber lit apartment windows and soft analog halation, casting a faint diagonal dusk glow across the sill—capturing how most goodbyes happen in complete silence. Standing calmly in the lower-left third in three-quarter profile with hands tucked into their oversized dark charcoal hoodie, the kraft-paperbag-head protagonist gazes quietly toward the window with still, empty calm behind clearly visible round black wire glasses and dot eyes. Curled peacefully with closed eyes on the wooden windowsill in the lower-right is the chubby black cat with a clean, distinct silhouette. Hand-drawn charcoal ink outlines, organic watercolor-ink wash, subtle circular halftone shadow texture, and 35mm film grain. Clean deep dark negative space across the upper third for subtitles. No text, no stray paper bags, no watermark.
```

---

## 图 4（第 5 幕远中景 & 第 6 幕 `camera_morph` 推近特写：「原来某天的相见，竟已是最后一面，」/「此后即便不是隔山隔水，」）
- **目标保存路径**：`studio/scenes/wusheng/s4_ordinary_last_glance.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **构图设计**：极具宿命感的「寻常一天竟是最后一面」街角叙事镜头！一条安静普通的城市傍晚小巷/人行道，远处转角处一盏刚亮起的暖琥珀色路灯下，一个极模糊、再普通不过的陌生/旧人远去背影正缓缓走过街角（无任何伸手或夸张姿态，只是普通转身离去）；画面前景中下部偏左，纸袋人停在路边微微停步回望，圆框眼镜映出一点微弱街灯光晕、双黑点眼睛清晰透出后知后觉的怅然；圆润小黑猫乖巧坐在他身旁偏右的台阶边一同望向街角。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏深夜黄昏交替时分的城市街角独立动画电影叙事剧照。80/20 强明暗冷暖景深对比：一条安静寻常的城市街角人行道，四周 80% 沉入深邃的午夜冷青蓝树影与暮雾中；远处街道尽头拐角处，一盏刚亮起的暖琥珀色路灯洒下温柔朦胧的金色光晕（Soft Analog Halation），暖光边缘隐约可见一个极度虚化、渐行渐远、即将拐过街角消失的普通路人背影剪影（姿态完全自然寻常，象征“那天以为只是普通一天，回头看竟已是最后一面”）。画面前景中下部偏左侧，纸袋人穿着炭黑连帽卫衣停在路边，身体呈四分之三侧转身回望街角方向，暖琥珀远光轻拂他半边牛皮纸袋头套与细黑圆框眼镜，两个小黑点眼睛与微蹙的眉线清晰可见，透出后知后觉的怔忡与安静遗憾；圆润的小黑猫安静蹲坐在他脚边偏右侧的人行道边沿上，独立轮廓清晰，一同望向远去的街角。手绘炭笔墨线、水彩夜雾晕染、圆形半调网点与 35mm 胶片颗粒，上方三分之一保持深邃开阔的午夜冷青夜空留白用于放置字幕。严禁任何文字、招牌字样、多余纸袋与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody twilight-to-night anime film narrative still on a quiet ordinary city street corner, anchored to the Paperbag protagonist and chubby Black Cat from the reference image. 80/20 chiaroscuro lighting with cinematic depth: 80% steeped in deep midnight slate-teal tree shadows and mist; far down the sidewalk at the corner, a freshly lit warm-amber streetlamp casts a soft hazy golden glow (Soft Analog Halation) where a deeply blurred, ordinary distant silhouette of someone walking away is just about to turn the corner and vanish—evoking realizing too late that an ordinary day was the final meeting. In the lower-left foreground, the kraft-paperbag-head protagonist pauses in an oversized dark charcoal hoodie in a three-quarter view gazing toward that corner, faint warm light catching half the paper bag and their round black wire glasses with clearly visible dot eyes and quietly wistful brows. Sitting cleanly beside their sneakers on the sidewalk curb to the right is the chubby black cat looking down the same lane. Hand-drawn charcoal ink outlines, organic watercolor-ink wash, circular halftone shading, and 35mm film grain. Clean deep dark midnight sky negative space across the upper third for subtitles. No text, no signage, no stray paper bags, no watermark.
```

---

## 图 5（第 7 幕终章：「也没有再重逢。」）
- **目标保存路径**：`studio/scenes/wusheng/s5_same_city_river_lights.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **构图设计**：全片情感落点终章！辽阔深夜城市滨江步道远景——宽阔静谧的深青色江面横亘在画面中下部，对岸是同一座城市绵延闪烁的万家暖琥珀色灯火与倒映在江面上的粼粼金色微光（具象化「即便不是隔山隔水，就在同一座城里，也没有再重逢」）；前景偏右的纸袋人背侧身靠在江边铁护栏旁静静远眺对岸灯火，圆润小黑猫安静坐在左侧护栏石台边缘陪着他吹晚风。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏深夜城市滨江步道大远景终章独立动画电影剧照。80/20 强明暗冷暖对比：辽阔静谧的深夜城市江畔，上方三分之一是极其干净深邃的午夜冷青蓝夜空留白（用于放置字幕）；画面中部至中下部横亘着宽阔平静的深青色江面，对岸同一座城市低矮绵延的楼宇剪影上闪烁着细密、温暖却遥远的暖琥珀色万家灯火（Soft Analog Halation），暖金色灯火在平静江面上拖出柔和微亮的波光倒影（具象化“明明在同一座城、并非隔山隔水，却再也没有重逢”的辽阔孤独与释然）。前景中下部偏右侧，纸袋人穿着宽大炭黑连帽卫衣，呈四分之三背侧身姿态轻轻靠在江边深色铁护栏旁，双手插在口袋里安静眺望对岸的万家灯火，暖琥珀色江光勾勒出他纸袋侧缘与圆框眼镜的微弱轮廓光；前景中下部偏左侧的江畔护栏石墩上，圆润的小黑猫安静端坐着，独立轮廓清晰，尾巴微微收拢陪他一同望着对岸灯火。手绘炭笔墨线、有机水彩夜色晕染、细腻圆形半调网点与 35mm 胶片颗粒。严禁任何文字、广告牌字样、多余纸袋与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film wide finale still along a quiet urban riverside promenade, anchored to the Paperbag protagonist and chubby Black Cat from the reference image. 80/20 chiaroscuro lighting: across the upper third lies an expansive, clean deep midnight slate-teal night sky for subtitles; across the middle-lower frame stretches a wide, calm dark-teal river reflecting soft golden-amber ripples from the distant, continuous warm city lights along the opposite riverbank (Soft Analog Halation)—evoking living under the same city lights without mountains or seas between you, yet never meeting again. In the lower-right foreground, the kraft-paperbag-head protagonist leans calmly against the dark riverside railing in three-quarter back profile with hands tucked in their oversized dark charcoal hoodie, warm city reflections catching the edge of the paper bag and round wire glasses. Perched cleanly on a stone railing pillar to the lower-left sits the chubby black cat with a crisp silhouette gazing quietly across the water beside them. Hand-drawn charcoal ink outlines, atmospheric watercolor-ink wash, circular halftone shading, and 35mm film grain. No text, no billboards, no stray paper bags, no watermark.
```
