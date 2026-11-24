# 《爱情里的两种遗憾》Mode C 外置生图提示词包（Prompt Pack for Gemini Nano Banana 2.5 / Midjourney / 即梦）

> **本片专项策划与算法优化亮点**：
> 1. **抖音完播黄金时长（`16.18 秒` · 5 幕）**：仅需生成 **4 张母图**（其中第 3 幕通过新引擎 `camera_morph` 无重影推镜直接由图 2 推进），节奏紧凑、零废话，极适合拉高抖音完播率。
> 2. **首镜全新对称分岔路口视角（彻底防查重）**：**图 1** 采用深夜雨后十字路口/分岔街口的**低机位背影对称构图**，地面倒映左冷青、右暖琥珀两道分岔光路（直观隐喻「两种遗憾」），与之前所有视频开场完全不同。
> 3. **极强的双态叙事对比**：
>    - **图 2（第一种遗憾：用力爱过却不值得）**：大雨夜公交站亭下，浑身湿透却用双手拼命护着胸前一束鲜亮暖黄花束，最后只剩错愕与心寒；
>    - **图 3 → 图 4（第二种遗憾：没好好爱，失去后才懂珍贵）**：同一张深夜餐桌的「前后对照」——图 3 是暖灯下漫不经心忽略桌上的热菜与陪伴，图 4 是天亮后只剩对面一把空椅子与瞬间愣住的懊悔。
> 4. **参考图上传规则**：4 张图均有主角出场，请在 Gemini（Nano Banana 2.5）中全部上传 [assets/master_ref.jpg](../assets/master_ref.jpg) 作为角色锚点，画幅全部选 **`9:16` 竖屏**，生成后放入 `studio/scenes/yihan/` 目录即可一键渲染。

---

## 图 1（对应第 1 幕开场：「爱情里面有两种遗憾，」）
- **目标保存路径**：`studio/scenes/yihan/s1_two_regrets_crossroad.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与防查重构图设计**：**低机位对称背影分岔路口构图**！深夜微雨后的空旷城市分岔路口，湿漉漉的柏油路面像镜子一样倒映出前方两条方向截然不同的街灯长廊——左边是清冷寂寥的暗青色灯光，右边是温暖模糊的琥珀色灯光（象征「两种遗憾」）；纸袋人与小黑猫并肩立在画面中下部中央的斑马线前，安静地望着前方分岔的夜路。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人（折叠牛皮纸袋头、锯齿底边、细黑圆框眼镜、炭黑连帽卫衣）与圆润黑猫设定，绘制一张 9:16 竖屏深夜王家卫/新海诚式 Lo-Fi 独立动画电影低机位对称背影剧照。
全新分岔路口构图与双色光影叙事：深夜小雨刚停的空旷城市分岔街口，湿润的深色柏油路面如镜面般倒映着远处的城市夜灯——画面左前方延伸的街道浸在清冷孤寂的深青蓝雾气与冷白路灯里，右前方延伸的街道闪烁着柔和温暖的暖琥珀色街灯光晕与散景（Soft Analog Halation，具象化“爱情里面的两种遗憾”）；纸袋人位于画面中下部中央偏前，呈安静挺拔的背影四分之三视角，双手插在炭黑卫衣兜里停在斑马线边遥望前方的两条路，右侧暖琥珀光在他纸袋与肩线边缘勾出一道温柔的金色轮廓光；圆润的小黑猫乖巧地蹲坐在他右脚边一同望向远方。手绘炭笔墨线、水彩光影晕染、细腻圆形半调网点阴影与 35mm 胶片颗粒感。画面上方三分之一保持深邃纯净的午夜深青夜空留白用于放置字幕，严禁任何文字、路牌字样与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film low-angle symmetrical rear-view still (Wong Kar-wai / Makoto Shinkai / Lo-Fi indie animation atmosphere) matching the Paperbag protagonist and chubby Black Cat from the reference image. Distinct diverging-crossroad composition: at a quiet, rain-slicked city street fork at midnight, wet dark asphalt mirrors two contrasting paths stretching into the distance—the left street fades into cool, lonely slate-teal mist, while the right street glows with soft warm-amber streetlights and dreamy bokeh halation (visually symbolizing "two kinds of regret in love"). Standing poised in the lower-center foreground by the crosswalk in calm rear silhouette, the kraft-paperbag-head protagonist keeps hands tucked in their dark charcoal hoodie pockets, warm amber rim-light tracing the right edge of the paper bag and shoulders, while the chubby black cat sits loyally beside their right sneakers gazing ahead. Hand-drawn charcoal ink outlines, organic watercolor-ink wash, circular halftone shading, and 35mm film grain. Generous deep midnight slate-teal sky negative space across the upper third for subtitles. No text, no street sign letters, no watermark.
```

---

## 图 2（对应第 2 幕中近景 & 第 3 幕平滑推近特写：「一种是你曾经那么用力地爱过，」/「最后却发现，那个人根本不值得。」）
- **目标保存路径**：`studio/scenes/yihan/s2_loved_too_hard_rain.jpg`（注：第 3 幕「最后却发现，那个人根本不值得。」将由引擎通过 `camera_morph` 自动平滑推近至被雨水打湿的眉眼与怀中花束特写）
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与情绪设计**：极具心酸反差的**雨夜护花半身近景**！倾盆大雨的深夜街头屋檐下，纸袋人卫衣双肩已被冷雨淋湿，白色漫画手却依然小心翼翼地把一束用旧报纸包好的暖黄色小野花紧紧护在胸口，生怕淋湿一瓣；可圆框眼镜后的眉眼却微微垂下，透出一种掏心掏肺后才看清对方根本不值得的疲惫与心寒。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人（折叠牛皮纸袋头、锯齿底边、细黑圆框眼镜、小黑点眼睛、炭黑连帽卫衣、白色漫画手）与圆润黑猫设定，绘制一张 9:16 竖屏深夜雨幕独立动画电影半身近景剧照。
80/20 强明暗冷暖反差：大雨滂沱的深夜冷青色街角屋檐下，四周 80% 沉入冰冷潮湿的深青黑雨夜阴影，头顶一盏微弱的暖琥珀色街灯透过雨丝洒下柔和光晕（Soft Halation）；纸袋人位于画面中下部，炭黑连帽卫衣的肩头已被雨水淋湿发沉，却依然用一双白色漫画手在胸前紧紧护着一束用浅棕牛皮纸/旧报纸仔细包好的暖黄色小雏菊/向日葵花束（绝不让雨水打湿花朵，具象化“曾经那么用力地爱过”）；然而他微垂着头，圆框眼镜后的小黑点眼睛与轻蹙下垂的眉线透出彻底清醒后的疲惫、心寒与苦涩（“最后却发现那个人根本不值得”）；圆润的小黑猫紧挨在他脚边屋檐避雨，心疼地仰头看着他。手绘炭笔墨线、水彩雨夜晕染、圆形半调网点与 35mm 胶片颗粒，上方三分之一保持深邃纯净的冷青黑雨夜暗部留白。严禁任何文字与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film medium close-up still in pouring rain, matching the Paperbag protagonist and Black Cat from the reference image. High-contrast 80/20 chiaroscuro lighting under a dim midnight street awning: surrounded by cold slate-teal downpour and deep charcoal shadow, a lone warm amber streetlamp casts a soft halation glow through the rain. Standing in the lower-center frame with damp hoodie shoulders, the kraft-paperbag-head protagonist cradles a bright warm-yellow bouquet of daisies wrapped in plain paper tightly against their chest with both white manga hands, shielding it carefully from the rain (symbolizing having loved with all their might); yet behind their round black wire glasses, their downcast eyes and weary, heavy brows reveal the quiet heartbreak and disillusionment of realizing the other person was never worth it. Sheltering beside their sneakers, the chubby black cat looks up sympathetically. Hand-drawn charcoal ink outlines, moody watercolor wash, circular halftone shading, and 35mm film grain. Clean deep dark negative space in the upper third for subtitles. No text, no watermark.
```

---

## 图 3（对应第 4 幕：「另一种是你没有好好地去爱，」）
- **目标保存路径**：`studio/scenes/yihan/s3_neglected_cold_room.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与情绪设计**：现代日常里最扎心的**「理所当然与漫不经心」场景**！深夜温暖的室内餐桌前，暖琥珀色吊灯照亮桌上一碗早已放凉的家常热汤/马克杯，而纸袋人却懒散地斜靠在椅子上扭头刷着手机（屏幕发出冷青光），对近在咫尺的温暖漫不经心；小黑猫蹲在桌子另一头安静地看着那碗冷掉的温情。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏深夜现代室内日常电影感中景剧照。
极具叙事张力的冷暖光影对比：深夜安静的现代小公寓木质餐桌前，上方一盏暖琥珀色吊灯投下一圈柔和温暖的暖黄光晕，照亮餐桌中央摆放整齐的一碗早已没有热气的温情夜宵与两只陶瓷杯；然而位于画面中下部右侧的纸袋人却漫不经心地斜靠在椅背上，身体微微侧转低头单手刷着散发冷青蓝色微光的智能手机，圆框眼镜后的神情显得习以为常、疏离而敷衍（具象化“拥有时习以为常，没有好好地去爱”）；圆润的小黑猫蹲坐在画面左侧的木椅/桌角边缘，静静地看着桌面上那份被冷落的暖光。手绘炭笔墨线、水彩光影晕染、细腻圆形半调网点暗部与 35mm 胶片颗粒，上方三分之一保持深邃纯净的冷青色室内暗壁留白。严禁任何文字与水印，地面或桌面严禁出现多余纸袋。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night modern apartment anime film medium shot matching the Paperbag protagonist and Black Cat from the reference image. Expressive warm-vs-cold lighting contrast at a quiet wooden dining table at night: a warm amber pendant lamp illuminates a neatly prepared, already-cooled late-night meal and two ceramic mugs in the center of the table. Yet sitting slumped back casually in the lower-right chair, the kraft-paperbag-head protagonist leans away, distractedly scrolling a smartphone that casts a cool pale slate-blue glow onto their round glasses—looking indifferent and taking the warmth right beside them for granted (symbolizing failing to love properly while having it). On the left edge of the table, the chubby black cat watches the neglected warm meal quietly. Hand-drawn charcoal ink outlines, organic watercolor-ink wash, circular halftone shading, and 35mm film grain. Clean deep dark negative space across the upper third for subtitles. No extra paper bags, no text, no watermark.
```

---

## 图 4（对应第 5 幕终章：「失去了才发现，那是一个真正值得的人。」）
- **目标保存路径**：`studio/scenes/yihan/s4_lost_empty_chair.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与情绪设计**：与图 3 形成**撕心裂肺的前后呼应**！同一张木质餐桌，此刻只剩清晨清冷微暗的晨雾光从窗外照进来，一束淡淡的暖琥珀色晨光斜斜落在**对面那把彻底空荡荡的木椅**上（桌上只剩一只孤单的杯子）；纸袋人放下手机，呆呆地望着对面的空座位，眉头深深锁起、眼神里满是无法挽回的错愕与懊悔，小黑猫把小脑袋轻轻蹭在他的手臂旁安慰他。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏清晨微暗薄雾下的电影感治愈伤痛终章近景剧照（与前一张室内餐桌形成强烈的前后空寂对比）。
80/20 清冷晨光与孤单暖影对比：同一间安静的小公寓木质餐桌前，此时窗外已是微凉清冷的深青色清晨，一缕微弱而刺眼的暖琥珀色清晨阳光穿过微飘的窗帘，恰好孤单地照在画面右侧那把彻底空荡荡、再也没人坐的木质餐椅上（餐桌上只剩一只孤单的杯子）；纸袋人坐在画面中下部左侧，早已收起手机，一双白色漫画手无力地垂放在空荡荡的桌面上，身体微微前倾，隔着细黑圆框眼镜呆呆地凝视着对面那把被晨光照亮的空椅子，眉头深深微蹙，眼神里写满了“失去之后才惊觉那是一个真正值得的人”的深深懊悔与酸楚；圆润的小黑猫心疼地凑到他手边，轻轻用小脑袋蹭着他的卫衣袖口安慰他。手绘炭笔墨线、水彩晨雾晕染、细腻圆形半调网点与 35mm 胶片颗粒，上方三分之一保持深邃静谧的深青暗壁留白。严禁任何文字与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody early-dawn anime film finale medium close-up still inside the same apartment dining room, matching the Paperbag protagonist and Black Cat from the reference image. Heartbreaking before-and-after contrast: in the cool dark slate-teal quiet of early morning, a single pale golden-amber ray of sunrise drifts through a gently swaying curtain and falls squarely onto the completely empty wooden chair on the right side of the table (only one solitary mug remains on the wood). Seated in the lower-left foreground, the kraft-paperbag-head protagonist has put away the phone; both white manga hands rest helplessly on the bare table as they stare intently at the sunlit empty chair across from them—brows deeply furrowed behind their round black wire glasses with stunned, aching regret ("only realizing after losing them that they were truly worth it"). Beside them, the chubby black cat gently nuzzles its head against their dark hoodie sleeve in quiet comfort. Hand-drawn charcoal ink outlines, atmospheric watercolor-ink wash, circular halftone shading, soft halation, and 35mm film grain. Clean deep dark negative space across the upper third for subtitles. No text, no watermark.
```
