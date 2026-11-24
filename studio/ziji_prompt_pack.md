# 《我会救自己千千万万次》Mode C 2.0 完整提示词包（5 张 9:16 母图 + 5 段 Gemini 图生视频指令）

> **全片导演视觉弧线（从暗夜低谷爬起 → 冷雨清醒 → 攀爬长阶 → 破出隧道迎风 → 晨光自渡致敬）**：
> - 共 **5 组素材（5 张母图 → 5 段动图视频）** 驱动 **8 幕分镜**，总时长 **`25.77 秒`（78 BPM，0 可读性警告）**。
> - **制作流程**：
>   1. 先在 Gemini 用 **「生图提示词」**（上传 [assets/master_ref.jpg](../assets/master_ref.jpg) 作为角色参考图，选 **`9:16` 竖屏**）生成 5 张母图；
>   2. 再把每张母图分别喂给 Gemini 视频生成，复制对应的 **「图生视频提示词（英文优先，动作更稳不崩画风）」** 生成 5 段视频；
>   3. 生成后放到 `studio/scenes/ziji/`（或发我文件夹路径），我将用升级后的 Mode C 2.0 引擎精准截断、叠加 `camera_morph` 动态推镜与发光字幕渲染成片！

---

## 第 1 组（第 1 幕开场：「没关系，我会救自己千千万万次。」）
- **目标视频路径**：`studio/scenes/ziji/s1_rise_from_floor.mp4`
- **镜头设计**：**贴地低机位仰拍（全新开场视角！）**。深夜幽暗房间的木地板上，纸袋人刚刚从跌坐的低谷中单手用力撑地准备站起，一束斜射进来的暖琥珀色晨曦/门缝光刚好打在他撑地的白色漫画手和坚定的圆框眼镜上；小黑猫伏在他身旁仰头相伴。

### 1A. 母图生图提示词（上传 `assets/master_ref.jpg`，9:16）
```text
参考上传图片中的纸袋人（折叠牛皮纸袋头、锯齿底边、细黑圆框眼镜、小黑点眼睛、炭黑连帽卫衣、白色漫画手）与圆润黑猫设定，绘制一张 9:16 竖屏充满力量感的深夜独立动画电影贴地低机位剧照。
全新贴地低机位构图与 80/20 强明暗对比：深夜寂静的深青暗色房间木地板上，四周 80% 沉入深邃的午夜冷青阴影，一束锐利温暖的暖琥珀色光线从斜上方照亮画面中下部（Soft Analog Halation）；纸袋人原本跌坐在地板暗影里，此刻正用一只坚定的白色漫画手用力按撑在木地板上、单膝微曲发力准备自己站起来（具象化“没关系，我会救自己千千万万次”），暖光打亮他撑地的白手、半边牛皮纸袋与细黑圆框眼镜，镜片后的小黑点眼睛透出平静、倔强而绝不认输的光芒；圆润的小黑猫就蹲伏在他另一侧膝旁，眼神专注坚定地陪着他起身。手绘炭笔墨线、水彩光影晕染、细腻圆形半调网点阴影与 35mm 胶片颗粒感，画面上方三分之一保持深邃纯净的暗青色天花板与墙面阴影留白用于放置字幕。严禁任何文字与水印。
```

### 1B. Gemini 图生视频提示词（上传图 1）
```text
Strictly preserve the exact 2D hand-drawn charcoal ink illustration style, flat manga shading, and circular halftone texture—no 3D rendering, no morphing of the paperbag head. Locked low-angle camera with an ultra-slow steady upward tilt. Inside the dark room, tiny golden dust motes drift slowly through the diagonal beam of warm amber light. The paperbag-head character presses their white hand more firmly against the wooden floor, shifting their shoulders slightly upward with a calm, determined deep breath as if gathering strength to rise, blinking steadily behind their round glasses. Beside them, the chubby black cat perks its pointed ears up and slowly sways its tail with quiet loyalty. No smoke swirls, clean atmospheric 2D anime motion.
```

---

## 第 2 组（第 2 幕中景 & 第 3 幕动态推近：「别人给我上了一课，那是别人的本事。」/「如果我走不出来，那就是我的无能。」）
- **目标视频路径**：`studio/scenes/ziji/s2_cold_rain_stand_tall.mp4`（第 3 幕自动接续 `3.1s` 并执行动态 `camera_morph` 推近冷峻眉眼）
- **镜头设计**：**深夜天台/空旷街角冷雨中不打伞伫立**！没有狼狈躲雨，纸袋人笔直站在细雨微风中，双手自然垂落或微握，圆框眼镜沾着细小雨滴却眼神异常清醒冷峻；小黑猫在身旁屋檐阴影下安静凝视。

### 2A. 母图生图提示词（上传 `assets/master_ref.jpg`，9:16）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏深夜冷雨中极具清醒力量感的独立动画电影半身近景剧照。
80/20 强明暗冷暖反差：深夜细雨飘落的城市天台边缘，四周 80% 是深邃清冷的午夜冷青蓝雨雾夜色，后侧方一盏暖琥珀色警示灯/远方楼宇暖光勾勒出人物清晰的金色肩线边缘光（Rim Light & Soft Halation）；纸袋人位于画面中下部，没有打伞，炭黑连帽卫衣被冷雨微微打湿，但他脊背挺得笔直、站姿沉稳克制，微抬着头直视前方，细黑圆框眼镜片上挂着两三颗细小水珠，镜片后的小黑点眼睛与平直冷峻的眉线毫无软弱与自怜，只有彻底清醒后的克制、冷冽与自我鞭策（“如果我走不出来，那就是我的无能”）；圆润的小黑猫端坐在画面左下角微干的矮墙边仰头注视着他。手绘炭笔墨线、水彩雨夜晕染、细腻圆形半调网点暗部与 35mm 胶片颗粒，上方三分之一保持深邃幽暗的冷青夜空留白。严禁任何文字与水印。
```

### 2B. Gemini 图生视频提示词（上传图 2）
```text
Strictly preserve the exact 2D hand-drawn charcoal ink outlines and halftone shading—no 3D, no face distortion, no extra smoke. Locked tripod camera. Fine steady midnight rain falls diagonally through the warm backlight rim, with tiny raindrops trickling slowly down the dark hoodie shoulders and off the jagged edge of the paper bag. The paperbag-head character stands completely upright and unshaken in the rain, shoulders lifting slightly with a resolute breath; halfway through the clip they blink slowly and raise their chin slightly with calm, cold determination behind the round glasses. At the lower left, the chubby black cat twitches its ear once and watches steadily. Crisp, moody 2D Lo-Fi anime motion.
```

---

## 第 3 组（第 4 幕远景 & 第 5 幕动态推近：「无需原谅或者释怀，毕竟这堂无比艰难的课，」/「真切地斩我天真，杀我幼稚，磨我心性，练我筋骨，」）
- **目标视频路径**：`studio/scenes/ziji/s3_tempering_stairs_climb.mp4`（第 5 幕自动接续 `3.5s` 并平滑推近向上攀登的背影）
- **镜头设计**：**超长地下通道/天桥混凝土台阶向上攀登的极具压迫感与蜕变感构图！** 底部是幽暗沉重的冷青长阶，台阶尽头高处透出明亮温暖的破晓金光；纸袋人一步步坚定地拾级而上（四分之三背影仰拍），小黑猫轻盈地紧跟在他身旁向上迈步。

### 3A. 母图生图提示词（上传 `assets/master_ref.jpg`，9:16）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏充满史诗克制感的独立动画电影低机位仰拍长阶梯剧照。
强烈的纵深透视与 80/20 暗明对比：一条长长的现代都市地下通道/高架混凝土台阶从画面底部的深邃冷青暗影中一路笔直向上延伸，台阶最顶端的出口处洒下耀眼而温暖的暖琥珀色清晨阳光（Warm Dawn Light & Soft Halation），在灰暗的扶手与石阶上投下层层明暗光影；纸袋人位于画面中下部阶梯中央，呈四分之三坚毅背影视角，双手插在炭黑连帽卫衣兜里、步履沉稳有力地正一步步朝上方光源攀登（具象化“斩我天真、磨我心性、练我筋骨”的艰难蜕变之路），金色的顶光勾勒出他纸袋头顶与挺拔的肩背轮廓；圆润的小黑猫正灵巧地迈着步子紧跟在他右脚侧方的上一级台阶上同行。手绘炭笔墨线、水彩光影晕染、圆形半调网点与 35mm 胶片颗粒，上方三分之一保持深邃幽暗的隧道顶部暗影留白用于放置字幕。严禁任何文字与水印。
```

### 3B. Gemini 图生视频提示词（上传图 3）
```text
Strictly preserve the exact 2D hand-drawn charcoal ink manga style and circular halftone shading—no 3D rendering, no morphing. Slow, steady low-angle camera drifting gently upward behind the character. Dust particles shimmer in the warm golden-amber morning light pouring down from the top of the long concrete staircase. The paperbag-head character takes slow, steady, determined steps upward one stair at a time, their dark hoodie swaying naturally with each firm stride. Right beside them, the chubby black cat steps gracefully upward along the stairs with its tail lifted high. Clean, inspiring, smooth 2D anime motion.
```

---

## 第 4 组（第 6 幕情绪爆发转折：「但它终将助我成长。」）
- **目标视频路径**：`studio/scenes/ziji/s4_dawn_tunnel_exit.mp4`
- **镜头设计**：**走出黑暗隧道、迎面撞上漫天破晓晨风与金光的电影高潮一镜！** 纸袋人跨出暗青通道阴影，站在开阔明亮的清晨晨风中，连帽卫衣衣角与帽绳被温暖的晨风高高吹起，满眼璀璨的暖琥珀晨光与光斑扑面而来！

### 4A. 母图生图提示词（上传 `assets/master_ref.jpg`，9:16）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏新海诚式走出黑夜、迎向破晓晨风的震撼动画电影中近景剧照。
极具爆发力的冷暖破晓光影：画面边缘还残留着刚刚走出的暗青色通道轮廓，而前方已是无比开阔澄澈的黎明晨空与城市远景，一轮温暖耀眼的暖琥珀色朝阳正将大片金色光芒与细碎漂浮的光尘洒满画面中下部（Strong Golden Dawn Halation）；纸袋人刚刚迈出暗影，立在画面中下部偏中位置，迎着扑面而来的清晨暖风微微昂起头，炭黑连帽卫衣的帽绳与衣摆被晨风利落地向后吹扬，温暖明亮的金色阳光照亮他整个牛皮纸袋与圆框眼镜，镜片后的小黑点眼睛清澈闪亮、充满破茧重生后的笃定与希望（“但它终将助我成长”）；脚边的圆润小黑猫迎着晨风微眯着眼、毛发与尾巴被金光照出一圈毛茸茸的暖金边。手绘炭笔墨线、通透水彩光影、圆形半调网点与 35mm 胶片质感，画面上方三分之一保持深邃清透的黎明深蓝高空留白（确保字幕清晰可读）。严禁任何文字与水印。
```

### 4B. Gemini 图生视频提示词（上传图 4）
```text
Strictly preserve the exact 2D hand-drawn charcoal ink outlines and halftone texture—no 3D, no face distortion. Ultra-slow gentle pull-out camera. Bright golden-amber sunrise dust motes and warm light flare drift across the frame as a refreshing morning breeze blows smoothly across the scene. The drawstrings and hem of the paperbag-head character's dark charcoal hoodie flutter naturally in the wind as they lift their head slightly toward the warm morning light, blinking with clear, renewed strength behind their round glasses. At their feet, the chubby black cat squints happily into the breeze while its tail sways gently. Uplifting, cinematic 2D anime motion.
```

---

## 第 5 组（第 7 幕近景 & 第 8 幕动态推近终章：「我想，在这段经历里，最重要的贵人，」/「会是那个从心脉受损的状态里，爬出来的自己。」）
- **目标视频路径**：`studio/scenes/ziji/s5_own_benefactor_sunrise.mp4`（第 8 幕自动接续 `3.5s` 并通过 `camera_morph` 推近至手按胸口、温柔坚定回望自己的特写）
- **镜头设计**：**致敬自己——清晨高处观景台暖光半身近景！** 纸袋人站在沐浴着温暖晨光的城市栏杆前，一只白色漫画手**平静而郑重地轻轻按在自己的左胸口（心脉处）**，微侧过头望向镜头方向，眼神不再有任何痛苦与迷茫，只有对自己深深的敬意与温柔笃定；小黑猫坐在旁边的栏杆石台上，安静地把爪子搭在他手腕旁。

### 5A. 母图生图提示词（上传 `assets/master_ref.jpg`，9:16）
```text
参考上传图片中的纸袋人（折叠牛皮纸袋头、锯齿底边、细黑圆框眼镜、小黑点眼睛、炭黑连帽卫衣、白色漫画手）与圆润黑猫设定，绘制一张 9:16 竖屏清晨暖阳下极具治愈力量与尊严感的动画电影终章半身近景剧照。
温柔通透的 80/20 晨光光影：上方三分之一保留深邃静谧的清晨深青蓝色高空留白用于放置字幕，画面中下部远方是沐浴在金色朝霞里的现代城市天际线与温柔漫射的暖琥珀色晨光（Warm Sunrise Halation）；纸袋人站在前景观景台栏杆前偏中央，一只白色漫画手平静、郑重而温柔地轻轻按在自己左胸口的心脏位置（具象化“致敬那个从心脉受损的状态里爬出来的自己”），头微微转向镜头方向，暖金色朝阳照亮他温润的牛皮纸袋与细黑圆框眼镜，镜片后的小黑点眼睛与舒展坚定的眉线充满劫后余生的平静、自爱与笃定力量；圆润的小黑猫端坐在他身旁的石栏杆上，微笑眯眼陪伴着这位浴火重生的主角。手绘炭笔墨线、水彩暖光晕染、细腻圆形半调网点与 35mm 胶片颗粒，严禁任何文字与水印。
```

### 5B. Gemini 图生视频提示词（上传图 5）
```text
Strictly preserve the exact 2D hand-drawn charcoal ink illustration style and circular halftone shading—no 3D rendering, no morphing of the paperbag head. Locked camera with an ultra-slow subtle breathing push-in. Warm golden morning sunlight shimmers gently over the distant city skyline as tiny golden light motes float upward in the breeze. Standing calmly by the railing, the paperbag-head character rests their white manga hand gently and steadily over their chest, taking a deep, peaceful breath; halfway through the clip they blink slowly and give a subtle, composed, proud slight nod toward the viewer behind their round glasses. Beside them on the railing, the chubby black cat blinks serenely and sways its tail gently. Calm, deeply empowering 2D anime finale.
```
