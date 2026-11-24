---
name: paperbag-emo
description: "制作统一深夜炭笔墨线与半调网点风格的纸袋人（Paperbag & Black Cat）IP 解释图、透明插画素材与卡点讲解视频。可单独绘制纸袋人、慵懒黑猫、两者组合，或同风格的物件与装饰元素；严格区分 Mode A（独立解释图）、Mode B（可复用透明资产）与 Mode C（BPM 节拍卡点视频）。不用于普通代码图表、写实照片处理或无关品牌视觉。"
---

# Paperbag Emo

Create raster visuals, reusable transparent assets, and beat-synced explainer timelines in one shared late-night manga-ink language anchored to `assets/master_ref.jpg`. Choose one output mode before generating; do not mix production paths.

## Choose the output mode

### Mode A — explanatory image

Use when the image itself must communicate an emotion, concept, mechanism, comparison, or reflection in about 10 seconds without external layout text.

- Deliver a complete PNG or WebP (or 9:16 vertical / 1:1 square frame) with a finished off-white textured paper or muted dark-slate night scene.
- Generate every essential title and label directly inside the bitmap.
- Make the relation or emotional contrast visible through objects, lighting, paths, states, or repeated materials; labels identify the evidence but do not replace it.
- Do not generate an unlabeled base and add essential words in a separate rendering step.

### Mode B — transparent illustration

Use when the Paperbag character, Black Cat, or a matching-style object/decorative element will be composed into a video timeline, slide, card, cover, or document.

- Request a genuinely transparent PNG when the selected generator supports native alpha. Otherwise use a perfectly uniform chroma-key background that does not occur in the artwork. Default to `#00FF00`; use `#FF00FF` when the subject contains green.
- Do not include explanatory labels unless the user explicitly requests text inside the illustration.
- Do not add a white die-cut sticker border around the silhouette so assets blend cleanly over both dark-slate and off-white backgrounds.
- Preserve native alpha when it is clean. For a chroma-key source, remove the background with the bundled `scripts/cutout.py`. Deliver a transparent PNG in either case.
- Check `assets/stickers/` first and reuse existing poses when they fit before generating new ones.

### Mode C — beat-synced explainer video (plugin slot)

Use when the user provides copywriting or Emo quotes and wants a dynamic 9:16 beat-synced video built purely from Mode B transparent assets and local rendering (`scripts/render_emo_video.py`), with zero external video-generation APIs.

- Compile the script into a structured `timeline.json` aligned to an integer BPM grid (e.g., `84` BPM for slow late-night emo, `120` BPM for punchy explainers).
- Keep Mode B asset extraction strictly separate from timeline composition so visual assets remain reusable across videos.

If the destination is unclear, choose Mode A when the single image must communicate the idea by itself, Mode B when another layout or Mode C timeline will compose the asset, and Mode C when rhythmic motion video is requested.

## Shared visual language

- Anchor character design to `assets/master_ref.jpg`:
  - **Paperbag protagonist**: folded kraft-brown paper bag head (jagged bottom rim), simple round black wire glasses, dot eyes, minimal curved brows/mouth line expressing emotion, oversized dark charcoal hoodie, simple white manga hands.
  - **Black cat companion**: chubby dark-charcoal short-haired cat with small pointed ears, subtle whiskers, calm or sleepy expression.
- Draw confident black charcoal/manga ink outlines with varied line weight (thick for outer contours, thin for creases and details) and restrained circular halftone screentone for shading.
- Treat the recurring characters as **optional subjects, not a required pair**. Select: the Paperbag protagonist alone, the Black Cat alone, both together, or standalone objects/decorations without any characters. Select characters only when requested or when they visibly serve the message; never add them merely to signal the style.
- For object-only artwork (e.g., desk lamp, ceramic mug, notebook, umbrella, clock, hourglass, stars), carry the exact same style through clear silhouettes, varied ink line weight, circular halftone shading, and simple material details. Do not add a person, cat, or face to make an object feel on-brand.
- When characters are present in Mode A concept explainers, keep them secondary to the visual evidence or action unless the character's emotional state is the requested subject.
- Color discipline:
  - Base: charcoal ink black, kraft paper brown, off-white, slate/halftone gray.
  - At most **two muted emotional/semantic accent colors**: **warm amber-yellow** (desk lamp glow, warmth, hope, key insight) and **muted slate-teal** (night atmosphere, calm, solitude, input/context).
- Avoid 3D rendering, glossy plastic gradients, photorealism, wobbly sketch lines, generic card grids, dashboards, unrelated clutter, white die-cut sticker outlines, and watermarks.

## Mode A workflow — explanatory image

### 1. Write the visual brief

```text
viewer_question: what should be understood or felt in 10 seconds?
concrete_claim: one-sentence conclusion or emo insight
real_objects: visible objects, lamps, mugs, desks, notebooks, paths, or states
relation: contrast, transformation, causality, sequence, tradeoff, or emotional shift
visual_evidence: what remains understandable when all labels are ignored?
scene: believable setting (off-white paper or muted late-night slate) + 2–4 environmental cues
semantic_colors: warm amber vs. muted teal role assignment
labels: exact short Chinese/English strings plus the evidence surface for each label
```

Keep one dominant focal action and no more than three major visual regions. For comparisons or multi-step progressions, use a clean left-to-right or top-to-bottom sequence.

### 2. Design the labels

- Prefer 2–6 labels. Use more only when the explanation truly needs them.
- Keep each label short and concrete: role, action, state, or emotion.
- Place every label on or immediately beside its evidence surface (such as a notebook cover, sticky note, coffee cup, sign, lane, or divider).
- Use modern Chinese sans-serif typography, medium or bold, large enough to read cleanly at mobile display size.
- Do not turn long paragraphs, tables, or dense copy into image text. Use deterministic layout or Mode C kinetic typography when multi-line copy is required.

Add this verbatim block to the generation prompt:

```text
Text (verbatim): Render these exact labels as part of the bitmap illustration:
"<label 1>", "<label 2>", "<label 3>".
Use each phrase exactly once. Do not translate, paraphrase, misspell, repeat,
or add any other text. Use modern sans-serif medium/bold typography, large
and readable. Place "<label 1>" on <evidence surface>; place "<label 2>" on
<evidence surface>; place "<label 3>" on <evidence surface>.
```

### 3. Build the prompt

Use this order:

1. Attach `assets/master_ref.jpg` as visual reference whenever the Paperbag protagonist or Black Cat appears.
2. State the concrete claim and shared scene task.
3. Describe the real setting, selected subjects (protagonist alone, cat alone, both, or object-only), and action.
4. Describe the evidence objects and their geometry: split, balanced, connected, contrasting, or transforming.
5. Assign semantic colors (warm amber vs. muted slate-teal).
6. Quote the exact labels and specify each placement surface.
7. Add the Mode A style anchor.

Mode A style anchor:

```text
Professional editorial manga/comic ink illustration matching the character design and linework of the reference image. Clean confident charcoal-black ink outlines with varied line weights, expressive but controlled. Use classic circular halftone screentone for gray and shadow areas, with subtle tactile paper grain. Render only the selected characters or objects; do not add the Paperbag protagonist or black cat automatically. Use a finished off-white lightly textured paper or muted slate-teal night environment, not a blank sterile canvas. Typography is modern sans-serif, medium or bold, large and readable. Color is restrained: black, white, halftone gray, kraft-brown, warm amber-yellow, and muted slate-teal (at most two accent colors). No 3D, no glossy gradients, no photorealism, no generic card grid, no dashboard, no unrelated clutter, no tiny text, no long paragraphs, no watermark.
```

### 4. Inspect and retry

1. Inspect the output at original resolution.
2. Compare every label with the brief character by character. Confirm each appears once and no stray text was added.
3. Reject missing, duplicated, invented, or misspelled labels.
4. Regenerate with one targeted correction while repeating all scene and style invariants. Do not conceal an error with a separate text layer.

Use this retry instruction:

```text
Keep the scene, composition, characters, objects, colors, and all correct labels unchanged.
Change only the incorrect text "<wrong>" to the exact text "<right>".
Do not add, remove, translate, or repeat any other text.
```

## Mode B workflow — transparent illustration asset

### 1. Select the subject

Identify exactly which subjects are requested:
- the Paperbag protagonist alone,
- the Black Cat alone,
- both together, or
- a standalone object / decorative element without characters.

Describe one clear pose/expression or object silhouette, including only props essential to the action. Leave generous padding around the artwork so no outline, glasses arm, whisker, or steam curl touches the canvas border.

### 2. Build the prompt

Attach `assets/master_ref.jpg` as reference when drawing the protagonist or cat. Describe the selected subjects first, explicitly state that no unrequested person, cat, or background furniture (desk/chair/floor) should appear, then append the fixed style anchor and one background rule below:

```text
Style: professional editorial manga/comic ink illustration matching the reference character and line language. Clean confident charcoal-black ink outlines with varying line weights, thick for contours and thin for details, not wobbly or sketchy. Use classic circular halftone screentone dot patterns for gray and shadow areas. Color usage is extremely restrained: charcoal black, off-white, halftone gray, kraft paper brown on the bag when present, warm amber-yellow or muted slate-teal accents only when needed (no more than two accent colors). Render only the requested subjects. Do NOT add a white die-cut sticker border around the silhouette. Do not let halftone, ink, props, or the subject touch the image border. Keep generous padding. No text, no watermark. PNG format.
```

Use this background rule when the generator supports genuine transparency:

```text
Render on a genuinely transparent background with a clean alpha channel.
No backdrop, floor plane, cast shadow, or opaque pixels outside the artwork.
```

Otherwise replace `<KEY_COLOR>` (`#00FF00` default, or `#FF00FF` if the subject contains green) and use this rule:

```text
The background must be a perfectly uniform flat <KEY_COLOR> rectangle with zero
gradient, texture, noise, speckles, shadows, floor plane, green/magenta color spill, or lighting variation.
```

### 3. Validate and cut out

1. Inspect the source image before removal: confirm uniform key color in all four corners, no border touching, and no floor shadows.
2. For clean native RGBA, keep alpha intact. For chroma-key sources, run:
   ```bash
   python3 ~/.gemini/config/skills/paperbag-emo/scripts/cutout.py source.jpg ~/.gemini/config/skills/paperbag-emo/assets/stickers/<pose_name>.png
   ```
3. Inspect the transparent PNG:
   - Confirm RGBA mode and all four corners have alpha `0`.
   - Confirm thin details (round glasses, kraft bag jagged edge, cat ears/whiskers, steam curls, object details) are intact.
   - Confirm no green/magenta fringe remains at 100% zoom.
   - Confirm internal kraft-brown, dark charcoal hoodie, white hands, and halftone areas remain 100% opaque (`alpha = 255`).

## Mode C workflow — beat-synced Emo Cinema video assembly (`cinema_emo`)

> **Style Boundary**: Mode A and Mode B strictly keep the clean `/oil-visual` editorial manga-ink style above. **Only when entering Mode C (video mode)** does the visual language switch into **Late-Night Emo Cinema (`cinema_emo`)**: 80/20 chiaroscuro lighting, atmospheric film haze & soft highlight halation, watercolor-charcoal grain, off-center/back/POV cinematic angles, and pure HUD-free literary serif subtitles.

### Core principles
1. **Bespoke scenes per script (`一文案一分镜`)**: Never lazily reuse the same 3 stock stickers or another script's `studio/scenes/` folder for a new copywriting prompt. Every new script must first extract its own setting, weather, time progression, lighting arc, and concrete props from the copy's semantics.
2. **Zero-latency opening hook & cross-video opening diversity (`前1.5秒黄金钩子与首镜防查重`)**:
   - Strip zero-information filler intros (e.g. `"最近看到一句话："` or `"突然觉得"` as a standalone 3-second first shot); Shot 1 must open directly with a concrete conflict, emotional reversal, or relatable life slice.
   - Frame 0 (`t = 0.00s`) automatically renders Shot 1's complete opening subtitle + glowing underline so Douyin's default cover thumbnail and 0-second feed view are immediately readable.
   - Never open consecutive videos with the same centered sitting pose + cat sleeping at bottom-right (`[0.72, 0.75]`). Rotate Shot 1 across macro object cutaways, window reflections, back/over-shoulder silhouettes, high-angle room views, or warm desk lighting to avoid platform template-deduplication throttling.
3. **Length-driven duration & pacing (`文案定长，无配音纯字幕优先控制在 12–22s`)**: Scale scene count and video duration dynamically with copy length (keeping average shot duration `2.0–4.0s` so visuals never stagnate; for Douyin pure-subtitle videos without voiceover, prioritize `12–22s` for maximum completion rate):
   - **Short quote (≤ 25 Chinese chars / 2–3 lines)**: `3–4` shots · `10–15s` (`4–5` beats/shot).
   - **Medium monologue (26–65 chars / 4–7 lines)**: `5–7` shots · `15–22s` (`3–4` beats for transitions, `4–5.5` beats for emotional landings).
   - **Long narrative (65–130+ chars / 8–14 lines)**: `8–12` shots · `24–38s` (recommend pairing with voiceover or brisk `3.5–4.5` beats/shot; never replay an earlier shot's image out of chronological order after moving to a new location).
4. **Shot scale & angle diversity (`相邻景别轮换与同图 B 机位平滑推镜`)**: Never place two consecutive shots in the same framing, and avoid generic centered front-facing standing poses. Alternate across:
   - `Wide / Lonely Space` (establishing vast late-night environment, silhouette, back view, or window reflection),
   - `Medium / Off-Center Action` (character in lower/side third with deep shadow headroom),
   - `Object Cutaway` (hands, cold mug, glowing phone, raindrops merging on glass, umbrella shadow boundary — zero face),
   - `Emotional Close-up` (half-shadowed face, rain on glasses, hand over chest + natural blink),
   - `Back / POV Finale` (warm streetlamp or dawn light release).
   - When a shot uses `crop_box` on the same `scene_image` as the preceding shot (B-cam close-up), NEVER alpha-blend (`crossfade`) them (which causes double-headed ghosting); use `"transition": "camera_morph"` (automatic default for same-image consecutive shots) or `"cut"`.
5. **Worldbuilding & physical logic guardrails (`世界观与防 AI 幻觉铁律`)**:
   - **No decapitated paper-bag props**: Because the kraft paper bag is the protagonist's head, NEVER generate an empty crumpled kraft paper bag lying on the floor, street, or rain puddle as trash.
   - **No phantom interactions**: In solo or protagonist-plus-cat scenes, NEVER depict the protagonist extending a coffee cup, umbrella, or dangling wired earbud toward empty air where no human recipient exists.
   - **Physical & era consistency**: Keep props grounded in contemporary urban life (smartphone, convenience store hot drink, subway handrail, desk lamp, umbrella); avoid physically impossible AI hallucinations (such as a lit matchstick burning inside a rain puddle) or anachronistic medieval props (wax-sealed letters, 19th-century camping oil lanterns) unless the script is explicitly period fantasy.
6. **Companion & prop micro-interactions**: Pair protagonist motion (`natural_blink`, `fg_parallax`) with black cat and prop life (`cat_zzz`, `purr_waves`, cat blink, `prop_pulse` on phone/clock/lamp, `coffee_steam`, `rain_glass`, `sunbeams`).

### Mode C Emo Cinema Prompt Style Anchor (for Mode C scene generation only)

When building prompts for Mode C `scene_image` keyframes (whether via external Prompt Pack or built-in generator), attach `assets/master_ref.jpg` as character reference and append this **Mode C Cinema Emo Anchor** instead of the Mode A explainer anchor:

```text
Moody late-night anime film still (Wong Kar-wai / Makoto Shinkai / Lo-Fi indie animation atmosphere) anchored to the Paperbag & Black Cat character design of the reference image. 80/20 chiaroscuro lighting: 80% of the frame immersed in deep midnight slate-teal and charcoal shadow, illuminated only by a single emotional light source (warm amber streetlamp, desk lamp rim-light, or cold smartphone glow) with soft analog highlight halation and atmospheric mist/rain haze. Hand-drawn charcoal ink outlines with organic watercolor-ink wash, subtle circular halftone shadow texture, and 35mm film grain. Cinematic composition with generous dark negative space in the upper third for film subtitles. Vertical 9:16 aspect ratio. No text, no subtitles, no speech bubbles, no watermark.
```

### Three execution paths for Mode C video production

Choose the path that matches the user's input assets and production tier (all three share the exact same `timeline.json` engine and can be freely **hybrid-mixed** inside a single video):

#### Path A — Image-to-Video Local Motion Comic (`外置母图 → 本地漫画电影合成`, zero video API cost)
1. Produce the **Director Breakdown** and write a ready-to-copy **Prompt Pack Markdown file** (`studio/<project>_prompt_pack.md`) containing for each hero keyframe:
   - Target filename (e.g. `studio/scenes/<project>/s1.jpg`), aspect ratio (`9:16`), and whether to upload `assets/master_ref.jpg` as reference image;
   - Copy-pasteable **Chinese Prompt** and **English Prompt** (incorporating the 80/20 chiaroscuro Mode C Cinema Emo Anchor and upper-third subtitle negative space);
   - Which shots in the timeline will use the full image vs. B-cam `camera_morph` close-up push-in.
2. Pause and hand the Prompt Pack to the user.
3. Once the user drops the generated images into `studio/scenes/<project>/` (or supplies a folder path), generate surgical `natural_blink` frames (verifying pupil erasure & eyelid placement visually), validate with `--validate` (0 warnings), and render the final video.

#### Path B — Built-in Auto Generation (`内置透明贴纸/内置生图一键直出`)
1. Generate hero keyframes via `image-generator` using the Mode C Cinema Emo Anchor above (or compose Mode B transparent stickers), then proceed directly to B-cam `camera_morph`, blink frame generation, and video rendering.

#### Path C — Live Anime I2V Finishing & Hybrid Assembly (`图生视频 → AI 审片避坑与电影级终版精剪`, Mode C 2.0 flagship)
Use when the user converts keyframes into real animated clips (`.mp4` / `.mov` / `.webm` / `.gif`) via **Gemini Veo / 即梦 / 可灵 / 海螺** and hands the raw clips to the Agent for final assembly:
1. Include **paired Keyframe Image Prompt + I2V Animation Prompt** in `studio/<project>_prompt_pack.md` (always locking 2D charcoal ink + halftone texture, zero 3D conversion, locked/subtle camera, no erratic smoke/morphing).
2. **Mandatory Raw-Clip Director Inspection (`先逐秒审片抓穿帮`)**: Before writing the final `timeline.json`, inspect every raw `.mp4` clip second-by-second via `read_file` to catch AI video glitches (e.g. stray smoke swirls, back-of-head glasses flicker, late-clip morphing) and locate peak emotional beats (eye opening, sighing, cat paw raise, smiling cat).
3. **Surgical Trimming & Live `camera_morph` Assembly**:
   - Use `"video_start"`, `"video_speed"`, and `"video_loop": "clamp"` to slice ONLY the cleanest, highest-emotion window of each clip;
   - Pair consecutive shots from the same `"scene_video"` with `"crop_box"` + `"transition": "camera_morph"` (keeping upper headroom `y0 <= 0.04`) for ghost-free live-action 2.5D push-ins;
   - Tune `"text_y"` per shot so subtitles sit cleanly in dark ceiling/sky headroom and NEVER overlap the character's paperbag head, glasses, or bright sunlit sky.
4. **Mandatory Post-Render Verification (`成片逐秒二次复检`)**: Watch the rendered `_beat_preview.mp4` via `read_file` from `00:00` to the final second; if any subtitle collides with the character's head or bright sky, refine `crop_box` / `text_y` and re-render before delivering.

### Video assembly & `cinema_emo` rendering steps

1. Run dependency and cross-platform CJK font self-check if needed:
   ```bash
   python3 scripts/render_emo_video.py --check
   ```
2. Configure `timeline.json` (defaults to `"style": "cinema_emo"`):
   - `"style": "cinema_emo"` (default):
     - **Mode C 2.0 Live Anime Hybrid (`scene_video` + `scene_image`)**: Any scene can now supply `"scene_video"` (`.mp4` / `.mov` / `.webm` / `.gif` generated via Gemini Veo / Kling / Jimeng I2V) instead of a static image, with `"video_start"` (seconds offset to trim straight to the cleanest action window), `"video_speed"` (playback multiplier, default `1.0`), `"video_loop"` (`"pingpong"` / `"loop"` / `"clamp"`), and optional `"text_y"` vertical subtitle anchor override. `scene_video` clips natively share unified `midnight_emo` color grading, `camera_morph` B-cam push-ins (zero ghosting across consecutive shots from the same clip), `luma_fade`/`warm_dissolve` transitions, and glowing kinetic typography.
     - **I2V Animation Prompt Discipline (for Gemini Veo / external video generators)**: Always lock `"Strictly preserve the exact 2D hand-drawn charcoal ink outlines and circular halftone shading—no 3D rendering, no face/paperbag morphing. Locked tripod camera or ultra-slow subtle push-in. Subtle, calm Lo-Fi 2D anime micro-motion"` so characters and the black cat move organically (breathing, blinking, tail swishing, ear twitching, rain falling, curtain swaying) without breaking the IP's 2D manga identity.
     - **Decoupled stage & typography transitions**: Visual transitions (`crossfade`, `luma_fade`, `warm_dissolve`, `camera_morph`) apply strictly to the visual stage layer; outgoing subtitles fade out cleanly before the cut, and incoming subtitles start their entrance cascade **after** the visual transition passes its midpoint (`trans_offset = 0.56 * transition_sec`), preventing swallowed entrance motion or text ghosting. Frame 0 (`t = 0.00s`) always renders Shot 1's complete opening subtitle + underline so the video carries a built-in Douyin cover title.
     - **Per-character kinetic cascade & highlight soul**: Literary serif typography (`Songti` / `SimSun` / `NotoSerifCJK`, default `60px`) with `+4px` character tracking cascades in character-by-character; `highlight` keywords light up with a warm amber aura glow, a beat-synced upward accent lift, and an organic glowing hand-brush underline (`"underline": true`), while settled characters gently breathe with the BPM pulse.
     - **Zero-HUD pure cinema frame (`"hud": "none"` by default)**: Hides the top title banner, progress bar, timestamp, and bottom beat dots so the frame stays 100% focused on the illustration and kinetic subtitles (use `"hud": "minimal"` to show timestamp + beat dots, or `"hud": "full"` for full explainer HUD).
     - **35mm Midnight Emo color grade & B-cam `camera_morph` auto-adaptation**: Pre-bakes lifted slate-teal midtones + soft warm highlight halation bloom (`"color_grade": "midnight_emo"`), supports dynamic B-cam close-up cropping via `"crop_box": [x0, y0, x1, y1]` (automatically upgrading consecutive same-image transitions from `crossfade` to smooth 2.5D viewport interpolation `camera_morph` with zero double-exposure ghosting), supports `"light_pos": "auto"` / `"prop_pos": "auto"` to automatically lock breathing glow onto the warmest light source in newly dropped external images, and automatically guards against stale `_blink.jpg` frames when primary keyframes are replaced.
   - Per-scene motion & camera: `motion` (`alive_idle`, `bounce_in`, `beat_nod`, `zoom_punch`, `sigh_sway`, `calm_float`), `camera` (`push_in`, `pull_out`, `drift_diag`, `pan_left`, `pan_right`, `pan_up`, `pan_down`, `breathe`, `static`), and `transition` (`camera_morph`, `crossfade`, `luma_fade`, `warm_dissolve`, `wipe_up`, `ink_flash`, `cut`).
   - Smooth low-frequency `natural_blink`: prefer 3-frame sequences (`[open, half_blink, blink]`) for organic 5-stage blinks (`open -> half -> closed -> half -> open`), with calm defaults (`blink_interval: 3.8`, `blink_delay: 1.45`, `blink_duration: 0.24`).
   - Source-locked local micro-motion (zero drift across `camera_morph` / pan / zoom): `cat_box` (`[x0, y0, x1, y1]` bottom-anchored gentle cat breathing with `cat_breath_amp` / `cat_breath_period`), `cat_ear_box` (`[x0, y0, x1, y1]` staggered subtle ear twitch with `cat_twitch_delay` / `cat_twitch_interval`), and `"cursor_blink"` (`cursor_pos`, `cursor_angle`, `cursor_len`, `cursor_color`) for pulsing smartphone input cursors.
   - Sensory & companion micro-effects (`fx`): `coffee_steam` (`steam_pos`), `sunbeams`, `bokeh_depth`, `rain_glass` (dual-layer depth rain), `mist_drift` (`mist_y`), `dust_drift`, `water_shimmer` (`shimmer_box`), `cursor_blink`, `lamp_flicker`, `cat_zzz` (`cat_pos`), `purr_waves` (`cat_pos`), `prop_pulse` (`prop_pos`, `prop_color`), `film_grain`.
   - Kinetic text (`text_anim`): `fade_up`, `beat_lines`, `typewriter_beat`, `word_pop`, `slam_center`.
3. Validate pacing, line-wrapping, and asset paths before rendering:
   ```bash
   python3 scripts/render_emo_video.py --validate --timeline timeline.json
   ```
4. Render both the Douyin-ready silent MP4 and local beat-preview MP4:
   ```bash
   python3 scripts/render_emo_video.py \
     --timeline timeline.json \
     --out output/video \
     --fps 30
   ```

## Output handling

- Save reusable approved stickers inside `assets/stickers/` and project deliverables inside the active project directory.
- Use versioned filenames instead of overwriting approved project deliverables unless requested.
- Report the output mode, final file paths, and any prompt/cutout/BPM choices used.

## Quality gate

For every output:
- The subject is recognizable in about 3 seconds.
- Only requested characters appear; standalone objects remain free of unrequested characters.
- Line work, circular halftone, and warm-amber/muted-teal restraint remain consistent with `assets/master_ref.jpg`.

For Mode A:
- One claim, one focal action, and at most three visual regions.
- Visual evidence communicates the relation even if labels are ignored.
- Every required label is exact, appears once, and sits cleanly on its evidence surface.

For Mode B:
- Real RGBA transparency with clean edges, no white die-cut border, no chroma spill, and fully opaque character/object interiors.

For Mode C:
- Every scene cut, sticker motion, and keyword highlight aligns strictly to the BPM beat grid; both silent and beat-preview MP4 outputs validate cleanly.
