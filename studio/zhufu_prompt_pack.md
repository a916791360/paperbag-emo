# 《我总是祝福着你》Mode C 外置生图提示词包（Prompt Pack for Gemini Nano Banana 2.5 / Midjourney / 即梦）

> **针对抖音算法查重与留存做的 4 项专项优化**：
> 1. **首镜彻底打破前 4 条的「居中静坐 + 右下角黑猫」模板**：**图 1** 采用**右侧三分之一人物倚窗 + 左侧大面积暖琥珀城市流光雨窗 + 左下窗台黑猫望窗外**的反差构图，首帧像素指纹与前 4 条完全区隔，彻底避开同质化模板查重，同时首帧自带大面积暖琥珀高光抓取划屏注意力。
> 2. **6 张母图支撑 8 幕流畅叙事（27.2 秒黄金完播时长）**：其中第 3 幕（从图 2 推近）与第 7 幕（从图 5 推近）已接入新升级的 **`camera_morph` 2.5D 无重影平滑推镜**，彻底杜绝双头重影。
> 3. **100% 具象化对应文案物象**：**图 4** 精准落地文案中的**「一首歌曲、一张照片」**（暖光台灯下泛黄的旧拍立得合照相框 + 亮着音乐播放界面的手机与有线耳机），**图 5** 精准落地**「一个你再也无法见到的人」**（末班车驶离后空荡的对面站台长椅），零中世纪违和道具、零穿帮。
> 4. **参考图上传规则**：除 **图 4（歌曲与旧照片微距空镜）** 无人物无需上传参考图外，其余 **图 1、图 2、图 3、图 5、图 6** 请在生图时同时上传 [assets/master_ref.jpg](../assets/master_ref.jpg) 作为角色特征锚点，全部使用 **`9:16` 竖屏**，生成后放入 `studio/scenes/zhufu/` 目录即可一键渲染。

---

## 图 1（对应第 1 幕开场：「很久很久以后，你或许会突然意识到，」）
- **目标保存路径**：`studio/scenes/zhufu/s1_time_passing_window.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与防查重构图设计**：**右偏三分之一半侧面倚窗近景（打破前 4 条的居中偏左坐姿模板！）**。画面左侧是大扇沾满雨珠的高层玻璃窗，窗外流淌着温润明亮的暖琥珀色车流光带与城市散景；纸袋人站在画面**右侧**斜倚着窗框，暖琥珀窗光从左侧打亮他的圆框眼镜与半边纸袋轮廓；小黑猫蹲坐在**左下侧**窗台上安静地望着窗外流逝的灯火。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人（折叠牛皮纸袋头、锯齿底边、细黑圆框眼镜、小黑点眼睛、炭黑连帽卫衣、白色漫画手）与圆润黑猫设定，绘制一张 9:16 竖屏深夜王家卫/新海诚式 Lo-Fi 独立动画电影剧照。
打破居中构图，采用不对称冷暖光影叙事：画面左侧三分之二是一扇巨大的深夜雨夜玻璃窗，窗外远处的城市高架桥流淌着温暖明亮的暖琥珀色车流光轨与柔和散景光斑（Soft Analog Halation），温暖的金琥珀色光芒透过玻璃斜射进幽暗的深青色室内；纸袋人位于画面中下部偏右侧，半侧身安静地斜倚在窗框边，双手自然插在炭黑连帽卫衣口袋里，左侧射入的暖琥珀光清晰照亮他半边牛皮纸袋头套、圆框眼镜的金属高光以及若有所思、平静温和的眉眼；圆润的小黑猫蹲坐在画面左下侧的窗台木沿上，背对镜头歪头望着窗外流逝的金色光带（象征漫长岁月的流逝）。手绘炭笔墨线、水彩光影晕染、细腻圆形半调网点阴影与 35mm 胶片颗粒感。画面上方三分之一保持深邃通透的午夜深青暗部留白用于放置电影字幕，严禁任何文字与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film still (Wong Kar-wai / Makoto Shinkai / Lo-Fi indie animation atmosphere) matching the Paperbag protagonist and chubby Black Cat from the reference image. Asymmetric off-center composition with dramatic 80/20 warm-amber and slate-teal lighting: on the left side of the frame, a large rain-misted apartment window overlooks a late-night city highway where warm golden-amber traffic light trails and glowing bokeh orbs stream through the night mist with soft analog halation. Positioned in the lower-right third leaning calmly against the window frame in three-quarter profile, the kraft-paperbag-head protagonist keeps both hands tucked in their dark charcoal hoodie pocket as warm amber window light illuminates the left side of the paper bag, round black wire glasses, and reflective, gentle eyes. On the lower-left windowsill sits the chubby black cat gazing out at the passing golden light streams. Hand-drawn charcoal ink outlines, organic watercolor-ink wash, circular halftone shading, and 35mm film grain. Clean deep midnight slate-teal negative space across the upper third for film subtitles. No text, no watermark.
```

---

## 图 2（对应第 2 幕中景 & 第 3 幕平滑推近特写：「谁对谁错，何是何非，由爱生疑，由疑生恨，」/「或者难以释怀的背弃，无法谅解的谎言。」）
- **目标保存路径**：`studio/scenes/zhufu/s2_tangled_doubt_shadow.jpg`（注：第 3 幕将由引擎通过 `camera_morph` 自动平滑推近至光影分割下的眉眼与微握手指特写，无任何重影）
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与情绪设计**：极具戏剧张力的**斜角明暗分割构图（Chiaroscuro Split Lighting）**！房间半掩的门缝漏进一道斜切画面的暖琥珀光束，把桌面与纸袋人分成明暗两半（隐喻「谁对谁错、何是何非、由爱生疑」的拉扯与无力感），面前放着一只早已凉透的深色马克杯。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏深夜独立动画电影中近景剧照。极具电影感的明暗分割光影（Split Chiaroscuro Lighting）：深夜幽暗的深青色房间里，半掩的走廊门缝斜斜投进一道温暖却孤单的暖琥珀色光束，将画面中下部的木桌与纸袋人切分为明暗交界的两半（具象化“谁对谁错、何是何非、由爱生疑”的内心拉扯与无力感）；纸袋人坐在桌前偏中央位置，微微垂眸，一半纸袋与一侧圆框眼镜浸在暖琥珀色光线里，另一半隐在冷青色阴影中，眉头微蹙透出深深的疲惫与无奈；一双白色漫画手搭在桌面上，指尖轻轻抵着一只早已凉透、没有热气的深青色陶瓷马克杯；小黑猫安静地趴在桌角暗影与暖光的交界处陪伴着他。手绘炭笔墨线、水彩深色晕染、细腻圆形半调网点暗部与 35mm 胶片颗粒，上方三分之一保持深邃纯净的冷青黑夜色留白。严禁任何文字与水印，地面或桌面严禁出现任何多余的纸袋。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film medium shot matching the Paperbag protagonist and Black Cat from the reference image. Dramatic diagonal split chiaroscuro lighting: in a quiet dark slate-teal room at midnight, a single beam of warm amber light from a half-open doorway cuts diagonally across the wooden table and the kraft-paperbag-head protagonist seated in the lower-center frame—dividing their paper bag head and round black wire glasses half in warm golden light and half in cool midnight shadow, symbolizing inner conflict, doubt, and quiet helplessness. Their head is slightly bowed with weary, conflicted brows; their pale white manga hands rest on the table lightly touching a cold, untouched ceramic mug (no steam). At the edge of the table along the light-shadow boundary lies the chubby black cat watching quietly. Hand-drawn charcoal ink outlines, organic watercolor-ink wash, circular halftone shadow texture, soft highlight halation, and 35mm film grain. Clean deep dark negative space in the upper third for subtitles. No extra paper bags on table or floor, no text, no watermark.
```

---

## 图 3（对应第 4 幕：「生命中会突然刺痛你的，使你感到遗憾、伤痛的，」）
- **目标保存路径**：`studio/scenes/zhufu/s3_sudden_sting_chest.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与情绪设计**：深夜街角晚风中的**「突然怔住」动态瞬间**！纸袋人走过暖琥珀色路灯下时脚步突然停住，一只手下意识轻轻按住胸口卫衣，仿佛某段回忆随晚风突然刺痛了心脏。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏深夜新海诚/王家卫式动画电影街角半身剧照。80/20 强明暗对比：深夜空旷微风的城市街角，四周 80% 沉入深邃的午夜冷青蓝夜幕，一盏散发着柔和暖琥珀色光芒的街灯从侧后方洒下温暖的边缘光（Rim Light & Soft Halation）；纸袋人位于画面中下部，正走着却突然停下脚步怔在原地，身体呈四分之三侧面，一只白色漫画手下意识地紧紧按在自己胸口的炭黑卫衣上，微微低头，圆框眼镜后的小黑点眼睛与轻蹙的眉头传递出“被某段突然涌上的记忆狠狠刺痛”的遗憾与隐痛；晚风轻轻吹动他的连帽卫衣衣角，脚边的小黑猫也跟着停下脚步，仰起头心疼地看着他。手绘炭笔墨线、水彩夜雾晕染、圆形半调网点与 35mm 胶片颗粒，上方三分之一保持深邃幽暗的冷青夜空留白。严禁文字与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film medium close-up still matching the Paperbag protagonist and Black Cat from the reference image. High-contrast 80/20 chiaroscuro lighting on a quiet windy city street corner at night: surrounded by deep midnight slate-teal darkness, a warm amber streetlamp casts a soft golden rim-light and halation bloom across the lower-center frame. Stopping abruptly mid-stride in three-quarter profile, the kraft-paperbag-head protagonist presses one white manga hand gently but tightly against the chest of their dark charcoal hoodie, head tilted slightly down as if struck by a sudden, aching memory of regret behind their round black wire glasses. Beside their sneakers, the chubby black cat pauses too and looks up attentively at them. Hand-drawn charcoal ink outlines, moody watercolor wash, circular halftone shading, and 35mm film grain. Generous dark negative space across the upper third for subtitles. No text, no watermark.
```

---

## 图 4（对应第 5 幕纯物件微距空镜：「不论是一首歌曲、一张照片，」）
- **目标保存路径**：`studio/scenes/zhufu/s4_song_and_photo_cutaway.jpg`
- **是否上传参考图**：**否（纯现代生活物象微距空镜，无人物无动物）**
- **机位与情绪设计**：100% 紧扣文案**「一首歌曲、一张照片」**！深夜书桌一角俯拍微距：暖琥珀色台灯柔光下，静静放着一张边角微卷的旧拍立得相片（画面是模糊温暖的海边日落剪影）与一部亮着音乐播放器黑胶旋转界面的智能手机及一副安静搁在旁边的有线耳机。

### 中文提示词（复制即用）
```text
9:16 竖屏深夜独立动画电影桌面微距叙事空镜剧照（无任何人物或动物出现）。80/20 强明暗冷暖对比：深夜幽暗的深青色木质书桌俯拍特写，一盏暖琥珀色小台灯在画面中下部投下一圈温柔怀旧的金色光晕（Soft Analog Halation）；光晕中央静静摆放着两件极具记忆感的现代日常旧物——左边是一张边角微微泛黄卷起的复古拍立得旧照片（照片里只隐约可见温暖模糊的夕阳海面剪影，没有任何文字），右边是一部屏幕微亮的智能手机，屏幕上正显示着极简暖琥珀色音乐播放器的声波纹与黑胶唱片图标（无任何可读文字），一副白色有线耳机自然盘绕在手机旁（具象化“生命中突然刺痛你的一首歌曲、一张照片”）。手绘炭笔墨线、水彩光影晕染、细腻圆形半调网点暗部与 35mm 胶片颗粒，画面上方三分之一保持深邃纯净的冷青暗影留白。严禁任何文字、字母与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night anime film macro tabletop cutaway still (zero characters, no animals). High-contrast 80/20 chiaroscuro lighting on a dark wooden desk at midnight: a warm amber desk lamp casts a soft golden pool of light in the lower-center frame amid deep slate-teal shadow. Inside the warm light sit two evocative objects side by side: on the left, a slightly worn vintage instant photograph showing only an abstract, blurry warm sunset horizon silhouette (zero text); on the right, a modern smartphone whose glowing screen displays a minimal warm-amber music player waveform and vinyl disc icon (zero readable text) with a pair of white wired earphones resting naturally coiled on the desk beside it—visually embodying "a song, or a photograph" that suddenly stirs an old memory. Hand-drawn charcoal ink linework, organic watercolor-ink wash, circular halftone shading, soft halation, and 35mm film grain. Clean deep dark negative space across the upper third for film subtitles. No text, no letters, no watermark.
```

---

## 图 5（对应第 6 幕远景 & 第 7 幕平滑推近近景：「或一个你再也无法见到的人，」/「事过境迁，你心中留下的，或许还是那句话：」）
- **目标保存路径**：`studio/scenes/zhufu/s5_unseen_person_platform.jpg`（注：第 7 幕「事过境迁……」将由引擎通过 `camera_morph` 自动平滑推近至站台上的纸袋人与黑猫近景）
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与情绪设计**：开阔的深夜高架轻轨站台大远景！一列散发着暖琥珀色窗光的末班列车正向右前方呼啸驶离、拖出长长的金色光影残迹（隐喻「再也无法见到的人」与「事过境迁」），站台左侧留着纸袋人与黑猫安静伫立的身影。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏深夜新海诚式露天高架车站站台远景动画电影剧照。80/20 强明暗与动态流光对比：辽阔幽暗的午夜深青色星空与城市夜雾下，画面右侧一列末班列车正疾驰驶离站台，车窗透出的暖琥珀色灯光在夜色中拉出一条长长的、温柔而怅惘的金色动态模糊光轨（Motion Blur & Soft Halation，具象化“一个你再也无法见到的人”与呼啸而过的岁月）；画面中下部偏左侧的空旷站台白线内，纸袋人双手插在炭黑卫衣口袋里安静地站着，目送那道远去的暖光，神情已经从刺痛转为彻底的平静与接受；圆润的小黑猫乖巧地坐在他脚边，尾巴轻轻贴着他的裤脚。手绘炭笔墨线、水彩大气晕染、圆形半调网点与 35mm 胶片质感，画面上方三分之一保持深邃开阔的午夜冷青夜空留白。严禁任何文字、站牌字样与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody late-night Makoto Shinkai-style anime film wide establishing shot on an open-air elevated train platform at midnight, matching the Paperbag protagonist and Black Cat from the reference image. Dramatic 80/20 chiaroscuro lighting: across the right half of the frame, a departing late-night train streaks away into the dark slate-teal mist, its glowing warm-amber windows stretching into a long, cinematic golden motion-blur light trail with soft analog halation—evoking the passage of time and someone who can never be seen again. In the lower-left foreground on the quiet platform, the kraft-paperbag-head protagonist stands calmly with hands tucked into their dark charcoal hoodie pockets, watching the fading golden trail with composed acceptance behind their round black wire glasses, while the chubby black cat sits faithfully against their ankle. Hand-drawn charcoal ink outlines, atmospheric watercolor-ink wash, circular halftone shading, and 35mm film grain. Generous deep midnight slate-teal sky negative space across the entire upper third for subtitles. No text, no signage letters, no watermark.
```

---

## 图 6（对应第 8 幕终章收尾：「我总是祝福着你。」）
- **目标保存路径**：`studio/scenes/zhufu/s6_always_blessing_dawn.jpg`
- **是否上传 `assets/master_ref.jpg` 参考图**：**是**
- **机位与情绪设计**：全片情绪升华与和解终章！漫长黑夜终于过去，天际线破晓升起温柔澄澈的暖琥珀色晨光，晚风吹起蒲公英/微光光尘，纸袋人微微回眸，圆框眼镜后的眉眼柔和舒展——所有的怀疑、背弃与刺痛都随风散去，只留下一句最温柔体面的「我总是祝福着你」。

### 中文提示词（复制即用）
```text
参考上传图片中的纸袋人与黑猫设定，绘制一张 9:16 竖屏黑夜将尽、破晓微光升起时的治愈电影感终章近景剧照。温柔通透的 80/20 破晓光影：上方依然保留深邃静谧的深青蓝黎明夜空留白，而画面中下部远方的城市天际线正缓缓升起一片澄澈、温暖、充满释怀感的暖琥珀色破晓晨光（Warm Golden Dawn Halation），空气中漂浮着几点细碎发光的金色晨尘光斑；纸袋人站在高处开阔的观景步道旁，身体微侧并轻轻回眸望向镜头方向，清晨的第一缕暖琥珀色阳光温柔地照亮了他的牛皮纸袋头套与细黑圆框眼镜，镜片后的小黑点眼睛与完全舒展开的柔和眉线流露出一种放下所有恩怨、历尽千帆后的温柔、慈悲与真诚祝福（“我总是祝福着你”）；身旁的圆润小黑猫眯着眼睛沐浴在金色晨光里。手绘炭笔墨线、水彩暖光晕染、细腻圆形半调网点与 35mm 胶片颗粒，上方三分之一保持干净深邃的深青黎明夜空留白。严禁任何文字与水印。
```

### English Prompt (Copy-Paste)
```text
Vertical 9:16 moody-yet-healing dawn anime film finale medium close-up still matching the Paperbag protagonist and Black Cat from the reference image. Luminous 80/20 late-night-to-dawn chiaroscuro lighting: while the upper third remains a deep, tranquil dark slate-teal dawn sky for subtitles, the lower horizon glows with a pure, forgiving golden-amber sunrise halation and floating warm light motes in the morning breeze. Standing on an open overlook walkway in the lower-center frame, the kraft-paperbag-head protagonist turns gently back in a soft three-quarter glance; bathed in warm amber morning light, their round black wire glasses and softly relaxed brows express complete forgiveness, tenderness, and a quiet, heartfelt blessing after all the pain has passed. Beside them, the chubby black cat sits peacefully with eyes happily half-closed in the warm golden glow. Hand-drawn charcoal ink outlines, organic watercolor-ink wash, circular halftone shadow texture, soft analog halation, and 35mm film grain. Clean deep dark negative space across the upper third. No text, no watermark.
```
