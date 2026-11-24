# 《感谢那位特殊的人》Mode C 外置生图提示词包（Prompt Pack for Gemini Nano Banana 2.5 / Midjourney / 即梦）

> **本片专项策划与算法优化亮点**：
> 1. **黄金完播时长**：共 **5 张母图** 支撑 **7 幕分镜**，总时长精准控制在 **`22.50 秒`**（`76 BPM`，平均 `3.21 秒/幕`，0 可读性警告）。
> 2. **首镜全新视角防查重**：前几条分别用过沙发、地铁、露台和雨窗，本片 **图 1** 改用**高机位斜俯拍林荫石板路 + 暖琥珀路灯拉出的修长背影**，构图、透视、色块分布完全独立，彻底避开抖音首帧查重。
> 3. **100% 具象化紧扣文案**：**图 3（微光镜前整理衣领）** 对应「你的出现和缺席也塑造了今天的我」；**图 4（黎明前叶尖将落未落的琥珀露珠微距空镜）** 精准具象化「人的缘分朝生暮死如露水」。
> 4. **参考图上传规则**：除 **图 4（露珠微距空镜）** 无人物无需上传参考图外，其余 **图 1、图 2、图 3、图 5** 请同时上传 [assets/master_ref.jpg](../assets/master_ref.jpg) 作为角色特征锚点，全部使用 **`9:16` 竖屏**，生成后放入 `studio/scenes/ganxie/` 目录即可一键渲染。

---

## 图 1（对应第 1 幕开场 & 第 2 幕平滑推近：「最后我要感谢一位特殊的人，」/「虽然他只匆匆陪我走了一段路，」）
- **目标保存路径**：`studio/scenes/ganxie/s1_special_person_walk.jpg`（注：第 2 幕将由引擎自动通过 `camera_morph` 平滑推近）
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与防查重构图设计**：**高机位斜俯拍（High-Angle Overhead）**！一条微湿安静的城市林荫人行道斜向延伸，一盏暖琥珀色复古街灯洒下大片温暖明亮的金色光晕，纸袋人双手插兜独自走在路灯光影里，身后拉出一条长长的影子（隐喻“只匆匆陪我走了一段路”），圆润的小黑猫迈着轻快的步子走在他右前方陪他前行。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人（折叠牛皮纸袋头、锯齿底边、细黑圆框眼镜、小黑点眼睛、炭黑连帽卫衣）与圆润黑猫设定，绘制一张 9:16 竖屏深夜新海诚/王家卫式 Lo-Fi 独立动画电影高机位斜俯拍剧照。
全新斜俯拍透视构图：深夜微凉安静的城市林荫石板人行道自左下向右上斜向延伸，一盏温暖明亮的暖琥珀色街灯在画面中下部投下一大片金黄色的圆形光晕与柔和光晕溢出（Soft Analog Halation）；纸袋人位于画面中下部偏左，呈四分之三后侧俯拍视角，双手插在炭黑连帽卫衣兜里从容独自向前走着，暖琥珀灯光在湿润的石板路与落叶上拉出他修长而坦然的影子（具象化“虽然只匆匆陪我走了一段路，却曾照亮过这一程”）；圆润的小黑猫翘着尾巴轻快地走在他的右前方几步处领路。手绘炭笔墨线、水彩光影晕染、细腻圆形半调网点阴影与 35mm 胶片颗粒感。画面上方三分之一保持深邃通透的午夜冷青暗影树冠与夜空留白用于放置字幕，严禁任何文字与水印，地面严禁出现多余的纸袋。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film high-angle three-quarter overhead still (Makoto Shinkai / Wong Kar-wai / Lo-Fi indie animation atmosphere) matching the Paperbag protagonist and chubby Black Cat from the reference image. Distinct diagonal top-down street composition: a quiet, rain-dampened tree-lined stone footpath stretches diagonally from lower-left toward upper-right. A single warm amber streetlamp casts a luminous golden pool of light with soft analog halation across the lower-center pavement and scattered autumn leaves. Seen from an elevated three-quarter rear angle, the kraft-paperbag-head protagonist walks calmly forward with hands in their dark charcoal hoodie pockets, casting a long poised shadow behind them—evoking someone who walked beside them for a brief stretch of road. Ahead to their right, the chubby black cat trots lightly forward with its tail curled up. Hand-drawn charcoal ink outlines, organic watercolor-ink wash, circular halftone shading, and 35mm film grain. Generous deep midnight slate-teal negative space across the upper third for subtitles. No extra paper bags on the ground, no text, no watermark.
```

---

## 图 2（对应第 3 幕：「但有失终会有得，你也教会了我许多道理，」）
- **目标保存路径**：`studio/scenes/ganxie/s2_lost_and_gained_desk.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与情绪设计**：深夜暖光书桌前近景！暖琥珀色护眼台灯照亮翻开的空白手账笔记本与一只冒着淡淡热气的深青色马克杯，纸袋人握着一支笔安静地微偏头思考，圆框眼镜后的神情沉稳而通透（成长与沉淀），黑猫趴在桌角暖光里打盹。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人（折叠牛皮纸袋头、锯齿底边、细黑圆框眼镜、小黑点眼睛、炭黑连帽卫衣、白色漫画手）与圆润黑猫设定，绘制一张 9:16 竖屏深夜温暖治愈风独立动画电影中近景剧照。
80/20 暖冷对比光影：深夜安静的书房木桌前，一盏暖琥珀色金属小台灯照亮画面中下部，温暖的金黄色灯光温柔漫射（Soft Halation）；纸袋人坐在书桌前，一只白色漫画手轻轻握着一支黑色钢笔停在一本摊开的复古手账本上方（纸页上只有极简手绘线条，严禁出现任何可读文字），另一侧放着一杯冒着淡淡白烟的温热清茶，圆框眼镜后的小黑点眼睛与舒展平和的眉线透出一种历经失去后沉淀下来的通透、清醒与成长；圆润的小黑猫舒舒服服地蜷在书桌右角暖光边缘闭眼休息。手绘炭笔墨线、水彩暖暗对比晕染、细腻圆形半调网点与 35mm 胶片颗粒，上方三分之一保持深邃纯净的冷青色书房暗壁留白。严禁任何文字与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody yet warm late-night anime film medium close-up still matching the Paperbag protagonist and Black Cat from the reference image. 80/20 chiaroscuro lighting at a quiet wooden study desk at night: a warm amber metal desk lamp bathes the lower-center frame in soft golden halation against deep slate-teal shadows. Seated calmly at the desk, the kraft-paperbag-head protagonist holds a dark pen lightly over an open vintage journal (blank/minimal sketch lines only, zero readable text), beside a ceramic mug with subtle warm tea steam; behind their round black wire glasses, their eyes and relaxed brows convey quiet wisdom, clarity, and hard-earned growth after loss. At the right corner of the desk, the chubby black cat rests peacefully at the edge of the warm light pool. Hand-drawn charcoal ink outlines, watercolor-ink wash, circular halftone shading, and 35mm film grain. Clean deep dark negative space across the upper third for subtitles. No text, no watermark.
```

---

## 图 3（对应第 4 幕：「你的出现和缺席，也塑造了今天的我。」）
- **目标保存路径**：`studio/scenes/ganxie/s3_mirror_shaped_me.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与情绪设计**：极具电影高级感的**微光镜前近景（Mirror Portrait）**！纸袋人站在玄关/房间的一面木框穿衣镜前，用白色漫画手平静地整理自己的连帽卫衣衣领，镜子里映出他挺拔、沉静、已经完整独立起来的自己（具象化「你的出现和缺席也塑造了今天的我」）。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏充满电影叙事感的深夜镜前近景动画剧照。
80/20 强明暗冷暖光影：深夜柔和的室内玄关角落，一面简约复古的窄边木框镜子占据画面中下部，走廊一侧漏进温暖的暖琥珀色侧逆光（Warm Amber Rim Light & Soft Halation），勾勒出镜框与人物轮廓；纸袋人站在镜前，双手白色漫画手正平静、从容地轻轻整理自己炭黑连帽卫衣的领口与抽绳，透过镜面清晰映出他端正的牛皮纸袋头套、细黑圆框眼镜以及镜片后笃定、沉静、坦然接纳自我的眼神（具象化“你的出现和缺席，也塑造了今天的我”）；镜子下方角落里隐约映出坐在地板上仰头看着他的圆润小黑猫。手绘炭笔墨线、水彩光影晕染、细腻圆形半调网点暗部与 35mm 胶片颗粒，上方三分之一保持深邃幽暗的冷青暗壁留白。严禁任何文字与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 cinematic late-night anime film mirror-reflection close-up still matching the Paperbag protagonist and Black Cat from the reference image. 80/20 warm-amber and slate-teal lighting in a quiet hallway corner at night: framed inside a minimalist dark wooden wall mirror in the lower-center frame, the kraft-paperbag-head protagonist gently adjusts the collar and drawstrings of their dark charcoal hoodie with both pale white manga hands. A soft warm amber side-light blooms with analog halation along the mirror edge and glasses, illuminating their steady, self-possessed, quietly resilient gaze—symbolizing being shaped into who they are today by both someone's presence and absence. In the lower corner of the mirror reflection, the chubby black cat sits on the floor looking up calmly. Hand-drawn charcoal ink outlines, moody watercolor wash, circular halftone shading, and 35mm film grain. Clean deep dark negative space across the upper third for subtitles. No text, no watermark.
```

---

## 图 4（对应第 5 幕纯物件微距空镜：「人的缘分，朝生暮死如露水，」）
- **目标保存路径**：`studio/scenes/ganxie/s4_morning_dew_cutaway.jpg`
- **是否上传参考图**：**否（纯自然诗意微距空镜，无人物无动物）**
- **机位与情绪设计**：100% 精准落地**「朝生暮死如露水」**！黎明破晓前深青色微寒的晨雾中，一根纤细的深色枝叶尖端，悬垂着一颗晶莹剔透、折射出第一缕暖琥珀色晨光的圆润露珠，将落未落——极致的脆弱、短暂与温柔美感。

### 中文提示词（复制即用）
```text
9:16 竖屏新海诚式清晨微距叙事空镜动画电影剧照（无任何人物或动物出现）。
极具诗意的 80/20 黎明冷暖微距光影：破晓前的深青蓝色晨雾背景中，画面中下部斜斜伸出一片带着炭笔墨线质感的深青色湿润树叶，叶尖正悬垂着一颗饱满、晶莹剔透、将落未落的圆润晨露露珠；远方天际升起的第一缕暖琥珀色晨光穿过薄雾，在露珠内部折射出璀璨温柔的暖金色微光与柔和光晕溢出（Soft Analog Halation & Bokeh），背景散落着几点虚化的暖金色与冷青色清晨光斑（完美具象化“人的缘分，朝生暮死如露水”的短暂与美感）。手绘炭笔墨线、通透水彩晕染、细腻圆形半调网点暗部与 35mm 胶片颗粒，画面上方三分之一保持深邃静谧的黎明冷青色虚化暗部留白。严禁任何文字与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 Makoto Shinkai-style poetic dawn macro cutaway anime film still (zero characters, no animals). Luminous 80/20 chiaroscuro lighting in the cool slate-teal mist just before sunrise: extending delicately into the lower-center frame is a single damp dark teal leaf drawn with confident charcoal ink outlines. Hanging poised at the very tip of the leaf, about to fall, is one crystal-clear morning dewdrop catching the very first ray of warm golden-amber dawn sunlight, glowing internally with soft analog halation amid dreamy bokeh light orbs—visually embodying "human destiny is as fleeting as morning dew." Hand-drawn charcoal ink linework, translucent watercolor-ink wash, subtle circular halftone shadow texture, and 35mm film grain. Clean deep dark slate-teal blurred negative space across the upper third for film subtitles. No text, no watermark.
```

---

## 图 5（对应第 6 幕远景 & 第 7 幕平滑推近终章：「依旧祝你一切都好，」/「即使我们不再相见。」）
- **目标保存路径**：`studio/scenes/ganxie/s5_wish_you_well_horizon.jpg`（注：第 7 幕「即使我们不再相见。」将由引擎自动通过 `camera_morph` 平滑推近至温柔释怀的侧脸与眯眼黑猫特写）
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与情绪设计**：开阔宁静的**破晓海滨/江边防波堤**！晨雾散去，暖琥珀色日出在海平面尽头铺开一条波光粼粼的金色水路；纸袋人站在防波堤栏杆旁，微侧过脸望向远方，眼神彻底松弛温柔，小黑猫坐在身旁眯眼沐浴晨光——体面告别，各自奔赴山海。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏黑夜散尽、海面日出破晓时的治愈动画电影终章剧照。
开阔温柔的 80/20 破晓海景光影：上方依然保持深邃静谧的深青蓝黎明高空留白，画面中下部是一片辽阔安静的微风海面与石质海滨防波堤；远方海平线正升起一轮温柔明亮的暖琥珀色朝阳，在水面上铺开一条细碎闪烁的暖金色波光与柔和晨雾漫射（Warm Dawn Halation）；纸袋人站在防波堤木栏杆旁，身体微微朝向大海、脸微侧四分之三，晨光温柔照亮他的牛皮纸袋头套与细黑圆框眼镜，镜片后的小黑点眼睛与舒展柔和的眉线带着毫无怨怼、真挚而平静的祝福（“依旧祝你一切都好，即使我们不再相见”）；身旁的圆润小黑猫乖巧地坐在栏杆旁的石墩上，眯着眼睛安静地吹着清凉的晨风。手绘炭笔墨线、水彩暖光晕染、细腻圆形半调网点与 35mm 胶片颗粒，上方三分之一保持干净深邃的黎明深青高空留白。严禁任何文字与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 healing dawn anime film finale still at an open seaside pier, matching the Paperbag protagonist and Black Cat from the reference image. Luminous 80/20 late-night-to-sunrise lighting: while the upper third remains a tranquil deep slate-teal dawn sky for subtitles, the lower horizon opens onto a calm ocean where a soft golden-amber sunrise casts a shimmering path of warm light across the water with gentle morning mist halation. Standing calmly beside the weathered stone pier railing in the lower-center frame in a gentle three-quarter profile, the kraft-paperbag-head protagonist looks peacefully toward the sunlit horizon; bathed in warm golden morning light, their round black wire glasses and relaxed, tender brows convey pure, ungrudging goodwill and quiet closure ("still wishing you all the best, even if we never meet again"). Beside them on the stone bollard sits the chubby black cat with eyes happily half-closed in the morning breeze. Hand-drawn charcoal ink outlines, watercolor-ink wash, circular halftone shading, and 35mm film grain. Clean deep dark negative space across the upper third. No text, no watermark.
```
