# 《没有好好道别》Mode C 外置生图提示词包（Prompt Pack for Gemini Nano Banana 2.5 / Midjourney / 即梦）

> **导演拆解与防查重设计说明**：
> 1. **原文案微调说明**：已自动修正原文本中的防屏蔽符号与错别字（`克＋制` → `克制`、`你会过的更好` → `你会过得更好`、`前路坦荡P81不用再经历遗憾` → `前路坦荡，不用再经历遗憾`），并按情绪递进精炼为 **9 幕节奏分镜**（推荐 `74 BPM`，全片约 `30s`）。
> 2. **6 张母图支撑 9 幕电影叙事**：其中第 4 幕（由图 3 推近）、第 6 幕（由图 4 推近）、第 8 幕（由图 5 推近）均由本地引擎通过 **`camera_morph` 2.5D 无重影平滑推镜**自动生成 B 机位特写，零双头重影。
> 3. **首镜防查重构图**：图 1 采用**深夜人行天桥背影 + 桥下渐远暖琥珀车尾灯流光**构图，彻底避开居中静坐模板。
> 4. **参考图上传规则**：除 **图 2（手机与未发送光标微距空镜）** 无人物无需上传参考图外，其余 **图 1、图 3、图 4、图 5、图 6** 请在生图时同时上传 [assets/master_ref.jpg](../assets/master_ref.jpg) 作为角色特征锚点，全部使用 **`9:16` 竖屏**，生成后放入 `studio/scenes/daobie/` 目录即可一键合成视频。

---

## 分镜节奏总览（Director Breakdown）

| 幕次 | 对应母图 | 景别 / 运镜 | 字幕文案 |
| :--- | :--- | :--- | :--- |
| 第 1 幕 | 图 1 `s1_quiet_fade_overpass.jpg` | 远景背影（开场钩子） | 最后的最后，我们没有好好道别，就这样慢慢淡出彼此的生活。 |
| 第 2 幕 | 图 2 `s2_no_identity_phone.jpg` | 纯物件微距空镜 | 我心里依旧放不下你，只是再也没有身份去打扰。 |
| 第 3 幕 | 图 3 `s3_crowd_drifting_apart.jpg` | 雨夜人海远中景 | 遇见你是我很珍贵的经历，人海里相遇，又悄悄走散。 |
| 第 4 幕 | 图 3（`camera_morph` 推近） | 眉眼与眼镜反光特写 | 我不知道多久才能释怀，或许永远都忘不掉。 |
| 第 5 幕 | 图 4 `s4_midnight_ache_bedside.jpg` | 深夜窗边偏左中景 | 那些心动、想念，夜里偷偷的难过全都是真的。 |
| 第 6 幕 | 图 4（`camera_morph` 推近） | 怀抱黑猫克制特写 | 故事收尾得很安静，我没有放下，只是学会了克制。 |
| 第 7 幕 | 图 5 `s5_keep_ache_alone_bench.jpg` | 路灯长椅侧面近景 | 你是我很认真爱过的人，这段相遇我不后悔。 |
| 第 8 幕 | 图 5（`camera_morph` 推近） | 按胸收下心酸特写 | 往后不会再打扰你的生活，那些想念和心酸我自己收下。 |
| 第 9 幕 | 图 6 `s6_bright_road_ahead_dawn.jpg` | 破晓晨光开阔终章 | 或许没有我，你会过得更好，愿你前路坦荡，平安喜乐。 |

---

## 图 1（第 1 幕开场：「最后的最后，我们没有好好道别，就这样慢慢淡出彼此的生活。」）
- **目标保存路径**：`studio/scenes/daobie/s1_quiet_fade_overpass.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **构图设计**：深夜微雾的高架人行天桥背影远景。纸袋人站在中下部偏左，双手搭在冰凉的金属栏杆上，望着桥下车道上渐渐驶远、淡入深青夜雾的暖琥珀色车尾灯流光；小黑猫蹲在右侧栏杆石墩上一起静静目送。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人（折叠牛皮纸袋头、锯齿底边、细黑圆框眼镜、小黑点眼睛、炭黑连帽卫衣、白色漫画手）与圆润黑猫设定，绘制一张 9:16 竖屏深夜王家卫/新海诚式 Lo-Fi 独立动画电影剧照。
80/20 强明暗对比：深夜微雾的城市人行天桥上，四周 80% 沉入深邃静谧的午夜冷青蓝夜幕；画面下方远处的城市马路上，零星车流拖出几道温柔而渐行渐远、慢慢消散在夜雾中的暖琥珀色车灯流光与柔和散景（Soft Analog Halation，象征“没有好好道别，慢慢淡出彼此的生活”）。纸袋人位于画面中下部偏左侧，呈背影微侧四分之三角度，宽大的炭黑连帽卫衣被晚风微微吹动，白色漫画手安静搭在冰冷的天桥栏杆上，暖琥珀色远光勾勒出纸袋边缘与圆框眼镜侧缘的微弱轮廓光；圆润的小黑猫安静蹲坐在他身旁的栏杆水泥沿上，一同望着远去的车流。手绘炭笔墨线、有机水彩墨色晕染、细腻圆形半调网点阴影与 35mm 胶片颗粒感，画面上方三分之一保留干净深邃的午夜深青夜空留白用于放置字幕。严禁任何文字、路牌字样、多余纸袋与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film still (Wong Kar-wai / Makoto Shinkai / Lo-Fi indie animation atmosphere) anchored to the Paperbag protagonist and chubby Black Cat from the reference image. 80/20 chiaroscuro lighting: on a quiet mist-shrouded urban pedestrian overpass at midnight, 80% of the frame is immersed in deep midnight slate-teal and charcoal shadow. On the road below, departing cars leave fading trails of warm amber-gold taillight bokeh and soft analog halation dissolving into the night fog—evoking drifting quietly out of each other's lives without a proper goodbye. Positioned in the lower-left third in a three-quarter back view, the kraft-paperbag-head protagonist rests their white manga hands calmly on the cold railing in an oversized dark charcoal hoodie, warm amber rim-light catching the jagged rim of the paper bag and the edge of their round black wire glasses. Beside them on the ledge sits the chubby black cat watching the fading lights. Hand-drawn charcoal ink outlines with varied line weight, organic watercolor-ink wash, subtle circular halftone shadow texture, and 35mm film grain. Generous dark negative space across the upper third for film subtitles. No text, no signage, no stray paper bags, no watermark.
```

---

## 图 2（第 2 幕纯物件空镜：「我心里依旧放不下你，只是再也没有身份去打扰。」）
- **目标保存路径**：`studio/scenes/daobie/s2_no_identity_phone.jpg`
- **是否上传参考图**：**否（纯现代生活物象微距空镜，无人物无动物）**
- **构图设计**：深夜暗青色书桌微距俯拍。暖琥珀色台灯余光外侧，一部屏幕亮着柔和微光的智能手机静静搁在桌面上，屏幕显示极简聊天框（只有空白输入栏与一道孤单闪烁的光标，无任何可读文字），具象化「写了又删、再也没有身份打扰」。

### 中文提示词（复制即用）
```text
9:16 竖屏深夜独立动画电影桌面微距叙事空镜剧照（无任何人物、手或动物出现）。80/20 强明暗冷暖对比：深夜幽暗的深青黑色木质书桌俯拍近景，画面右下角边缘透出一点微弱的暖琥珀色台灯余光，中央偏下静静平放着一部屏幕微亮的现代智能手机，屏幕呈极简冷暖微光（柔光晕染 Soft Halation），隐约可见极简空白聊天输入条与一道孤单停顿的细竖光标（严禁任何可读文字、字母或符号），具象化“心里放不下却再也没有身份去打扰”的克制与沉默；手机旁静静搁着一只早已凉透的深色陶瓷马克杯与半截绕好的白色耳机线。手绘炭笔墨线、有机水彩深色晕染、细腻圆形半调网点暗部与 35mm 胶片颗粒，画面上方三分之一保持深邃纯净的午夜暗影留白用于放置电影字幕。严禁任何文字、数字、多余纸袋与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film macro tabletop cutaway still (zero characters, no hands, no animals). High-contrast 80/20 chiaroscuro lighting on a dark wooden desk at midnight: surrounded by deep slate-teal shadow, a faint warm-amber desk lamp glow grazes the lower corner while a modern smartphone rests in the lower-center frame. Its softly glowing screen with subtle halation shows only a minimal abstract blank message input bar with a single lonely vertical cursor—zero readable text, zero letters—symbolizing wanting to reach out yet having no right to disturb anymore. Beside the phone sit a cold dark ceramic mug (no steam) and loosely coiled white earphones. Hand-drawn charcoal ink outlines, organic watercolor-ink wash, circular halftone shading, and 35mm film grain. Clean deep dark negative space across the upper third for film subtitles. No text, no numbers, no watermark.
```

---

## 图 3（第 3 幕远中景 & 第 4 幕 `camera_morph` 推近特写：「遇见你是我很珍贵的经历，人海里相遇，又悄悄走散。」/「我不知道多久才能释怀，或许永远都忘不掉。」）
- **目标保存路径**：`studio/scenes/daobie/s3_crowd_drifting_apart.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **构图设计**：细雨深夜的城市十字路口人海。周围是虚化流动的冷青色陌生人撑伞剪影，唯有画面中下部偏右的纸袋人撑着一把深色透明雨伞停在原地，路灯暖琥珀光洒在他半侧牛皮纸袋头与圆框眼镜上，镜片挂着细碎雨雾反光；小黑猫安静躲在他脚边伞影里。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏深夜细雨街头独立动画电影剧照。80/20 强明暗冷暖对比：细雨蒙蒙的深夜城市十字路口，湿漉漉的柏油路面反射着远处温暖模糊的暖琥珀色街灯与红绿灯散景光晕；画面左右两侧是若干模糊流动、朝反方向走去的冷青色路人雨伞剪影，营造出“人海里相遇，又悄悄走散”的巨大孤独感。纸袋人独自停在画面中下部偏右的位置，穿着宽大炭黑连帽卫衣、手里撑着一把深色透明雨伞，呈四分之三侧面微微低头怔在原地，街灯的暖琥珀光打亮他半边牛皮纸袋头套与细黑圆框眼镜，镜片泛着细碎微光，小黑点眼睛透出深深的怅惘与难以释怀；圆润的小黑猫乖巧地蹲在他脚边的雨伞阴影里避雨。手绘炭笔墨线、水彩雨雾晕染、圆形半调网点与 35mm 胶片颗粒，上方三分之一保持深邃开阔的午夜深青雨夜天空留白。严禁文字、街边招牌字样、地面多余纸袋与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night rainy city anime film still matching the Paperbag protagonist and Black Cat from the reference image. 80/20 chiaroscuro lighting at a rain-slicked midnight crosswalk: wet asphalt reflects warm amber streetlamp and traffic-light bokeh while blurred, dark slate-teal silhouettes of faceless pedestrians holding umbrellas drift away in opposite directions, evoking meeting in a sea of people and quietly drifting apart. Standing still in the lower-right third, the kraft-paperbag-head protagonist holds a dark translucent umbrella in an oversized charcoal hoodie, three-quarter profile with head slightly bowed; warm amber streetlight catches half of the kraft paper bag and delicate raindrop glints on their round black wire glasses, conveying lingering sorrow and inability to let go. At their sneakers under the umbrella shadow sits the chubby black cat watching quietly. Hand-drawn charcoal ink outlines, organic watercolor rain mist, circular halftone shadow texture, soft analog halation, and 35mm film grain. Generous dark negative space in the upper third for subtitles. No text, no shop signs, no stray paper bags, no watermark.
```

---

## 图 4（第 5 幕中景 & 第 6 幕 `camera_morph` 推近特写：「那些心动、想念，夜里偷偷的难过全都是真的。」/「故事收尾得很安静，我没有放下，只是学会了克制。」）
- **目标保存路径**：`studio/scenes/daobie/s4_midnight_ache_bedside.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **构图设计**：深夜幽暗卧室靠窗一角。纸袋人坐在画面中下部偏左的床边地板/靠垫上，双臂轻轻环抱着怀里打盹的小黑猫，微微垂眸克制情绪；窗外一束冷青月光与远处零星暖琥珀窗火斜斜落进来，照出满室安静而真实的想念。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏深夜卧室情绪电影感中近景剧照。80/20 强明暗对比：深夜未开灯的安静卧室一角，80% 沉浸在深邃的午夜冷青蓝暗影中，右侧半拉的窗帘缝隙间透进清冷的夜色微光与远处城市楼宇零星的暖琥珀色灯火微芒（Soft Analog Halation）。纸袋人坐在画面中下部偏左侧靠窗的床沿边，微微蜷着肩膀，一双白色漫画手轻轻却坚定地抱着蜷在膝上的圆润小黑猫；他微微垂眸，圆框眼镜后的小黑点眼睛与极轻蹙的眉线没有嚎啕大哭，只有一种安静咽下眼泪的隐忍与克制（“没有放下，只是学会了克制”）；小黑猫安静地贴在他炭黑卫衣胸口闭眼陪伴。手绘炭笔墨线、水彩深色晕染、细腻圆形半调网点暗部与 35mm 胶片颗粒，上方三分之一保留干净深邃的暗青墙面与夜影留白。严禁任何文字与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night bedroom anime film medium close-up still matching the Paperbag protagonist and Black Cat from the reference image. 80/20 chiaroscuro lighting in an unlit quiet room at midnight: 80% immersed in deep slate-teal shadow, with soft cool moonlight and distant warm-amber city window glow filtering through a partly drawn curtain on the right with subtle analog halation. Seated in the lower-left third by the bed edge, the kraft-paperbag-head protagonist gently wraps their white manga hands around the chubby black cat curled against their dark charcoal hoodie. Eyes cast softly downward behind round black wire glasses with subtly restrained brows—no dramatic crying, only quiet, genuine ache and mature self-restraint. Hand-drawn charcoal ink outlines, organic watercolor-ink wash, circular halftone shading, and 35mm film grain. Clean deep dark negative space across the upper third for subtitles. No text, no watermark.
```

---

## 图 5（第 7 幕近景 & 第 8 幕 `camera_morph` 推近特写：「你是我很认真爱过的人，这段相遇我不后悔。」/「往后不会再打扰你的生活，那些想念和心酸我自己收下。」）
- **目标保存路径**：`studio/scenes/daobie/s5_keep_ache_alone_bench.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **构图设计**：深夜温暖路灯下的公园/河畔长椅侧面近景。纸袋人一只手轻轻按在胸口炭黑卫衣上（象征「把想念和心酸自己收下，认真爱过不后悔」），另一只手轻拍身旁仰头望着他的小黑猫，神情已从酸楚转为温柔坦然。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏深夜路灯长椅动画电影近景剧照。80/20 强明暗冷暖对比：深夜静谧的河畔木质长椅，头顶侧后方一盏暖琥珀色老式路灯洒下温柔包裹的金色光晕与柔光晕染（Soft Analog Halation），四周其余 80% 融在深邃的午夜冷青蓝夜雾中。纸袋人坐在画面中下部中央偏右的长椅上，身体呈四分之三侧面，一只白色漫画手轻轻平按在自己胸口的炭黑卫衣上（具象化“认真爱过不后悔，把想念和心酸自己收下”），另一只手温柔地轻抚身旁小黑猫的背；暖琥珀灯光清晰照亮他的牛皮纸袋头套与细黑圆框眼镜，镜片后的小黑点眼睛与舒展微弯的眉眼透出坦然、深情与彻底的体面；圆润的小黑猫坐在长椅上微微仰头，安静而治愈地回望着他。手绘炭笔墨线、水彩光影晕染、细腻圆形半调网点与 35mm 胶片颗粒，上方三分之一保持深邃干净的冷青夜空留白。严禁任何文字与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film medium close-up still on a quiet riverside park bench, matching the Paperbag protagonist and Black Cat from the reference image. 80/20 chiaroscuro lighting: a warm amber streetlamp from the upper side-back bathes the lower-right bench in a tender golden pool of light and soft analog halation amid 80% deep midnight slate-teal mist. Seated in three-quarter profile, the kraft-paperbag-head protagonist rests one white manga hand gently over the chest of their dark charcoal hoodie—quietly keeping all the longing and ache to themselves with zero regret—while the other hand softly pets the chubby black cat sitting beside them. Illuminated by warm amber light, their round black wire glasses and relaxed, sincere eyes express calm dignity and heartfelt acceptance as the black cat looks up comfortingly. Hand-drawn charcoal ink outlines, organic watercolor-ink wash, circular halftone shading, and 35mm film grain. Clean deep dark negative space across the upper third for film subtitles. No text, no watermark.
```

---

## 图 6（第 9 幕终章：「或许没有我，你会过得更好，愿你前路坦荡，不用再经历遗憾，平安喜乐。」）
- **目标保存路径**：`studio/scenes/daobie/s6_bright_road_ahead_dawn.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **构图设计**：破晓微光中的开阔河堤长路终章。上方仍保留深邃静谧的蓝青黎明夜空用于放字幕，下方远方一条笔直开阔的林荫长路被温柔澄澈的暖琥珀色晨光铺满，空气中飘浮细碎金色微光尘粒；纸袋人与小黑猫站在前景右侧微侧望向那条洒满晨光的前路，眉眼柔和舒展，送出最体面的祝福。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏破晓时分治愈电影感终章剧照。温柔通透的 80/20 破晓光影：画面上方三分之一依然保持深邃静谧的深青蓝黎明夜空留白用于放置字幕，而画面中下部远方一条笔直开阔的河畔林荫长路正被天际线升起的暖琥珀色破晓晨光温柔铺满（Warm Golden Dawn Halation），晨风中漂浮着细碎发光的金色光尘（象征“愿你前路坦荡，平安喜乐”）。纸袋人站在画面中下部偏右侧的路边，双手自然垂落或轻插在炭黑卫衣口袋里，侧身四分之三望向那条洒满金色晨光的开阔前路，清晨第一缕暖光照亮他的牛皮纸袋头套与圆框眼镜，柔和舒展的眉眼带着彻底释怀与真诚祝福的温柔笑意；圆润的小黑猫安静坐在他脚边，眯着眼睛沐浴在暖琥珀色晨光里。手绘炭笔墨线、水彩暖光晕染、细腻圆形半调网点与 35mm 胶片颗粒。严禁任何文字与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody-yet-healing dawn anime film finale still matching the Paperbag protagonist and Black Cat from the reference image. Luminous 80/20 late-night-to-dawn chiaroscuro lighting: while the upper third stays a deep, tranquil dark slate-teal pre-dawn sky for subtitles, the lower horizon opens into a wide, clear tree-lined riverside road bathed in pure warm golden-amber sunrise halation with delicate glowing dust motes drifting in the morning breeze—symbolizing a bright, unobstructed road ahead filled with peace and joy. Standing calmly in the lower-right foreground with hands tucked in their dark charcoal hoodie pockets, the kraft-paperbag-head protagonist gazes in soft three-quarter profile toward the sunlit road ahead, warm dawn light illuminating their kraft paper bag, round black wire glasses, and gently smiling, fully at-peace brows. Beside their sneakers sits the chubby black cat with eyes contentedly half-closed in the golden warmth. Hand-drawn charcoal ink outlines, organic watercolor-ink wash, circular halftone shading, and 35mm film grain. Clean deep dark negative space across the upper third. No text, no watermark.
```
