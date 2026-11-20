#!/usr/bin/env python3
"""Render a beat-synced 9:16 Paperbag Emo explainer video using Pillow + FFmpeg.

No external LLM, image, or video API keys required.
Supports:
  - Cross-platform CJK font auto-detection (macOS / Windows / Linux) & FFmpeg self-check
  - Themes: late_night (charcoal-teal) and paper_cream (warm journal paper), plus --bg custom images
  - Multi-frame sprite animation ("frames") and procedural secondary motion ("motion")
  - Camera push/pull ("camera"), scene transitions ("transition"), hand-drawn underlines & mood doodles
  - Beat-synced kinetic typography: typewriter_beat, beat_lines, word_pop, slam_center, fade_up

Outputs both:
  - <out>_silent.mp4 (ready for Douyin in-app music selection)
  - <out>_beat_preview.mp4 (with synthesized subtle Lo-Fi BPM pulse for beat verification)
"""

from __future__ import annotations

import argparse
import glob
import json
import math
import random
import shutil
import struct
import subprocess
import sys
import tempfile
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH = 1080
HEIGHT = 1920
HORIZON_Y = 1648


@dataclass(frozen=True)
class ThemePalette:
    name: str
    bg_top: tuple[int, int, int]
    bg_bottom: tuple[int, int, int]
    text_primary: tuple[int, int, int]
    text_shadow: tuple[int, int, int]
    text_shadow_alpha: float
    accent_primary: tuple[int, int, int]
    accent_secondary: tuple[int, int, int]
    muted_ui: tuple[int, int, int]
    horizon_color: tuple[int, int, int]
    mote_color: tuple[int, int, int]
    glow_color: tuple[int, int, int]
    glow_alpha_max: int
    grain_alpha: tuple[int, int]
    paper_grid: bool = False


THEMES: dict[str, ThemePalette] = {
    "late_night": ThemePalette(
        name="late_night",
        bg_top=(44, 58, 64),
        bg_bottom=(21, 29, 34),
        text_primary=(242, 238, 230),
        text_shadow=(10, 14, 16),
        text_shadow_alpha=0.55,
        accent_primary=(244, 184, 96),
        accent_secondary=(130, 188, 192),
        muted_ui=(158, 170, 174),
        horizon_color=(18, 22, 25),
        mote_color=(244, 210, 145),
        glow_color=(244, 184, 96),
        glow_alpha_max=46,
        grain_alpha=(4, 12),
        paper_grid=False,
    ),
    "paper_cream": ThemePalette(
        name="paper_cream",
        bg_top=(246, 241, 231),
        bg_bottom=(234, 225, 209),
        text_primary=(38, 35, 32),
        text_shadow=(255, 252, 245),
        text_shadow_alpha=0.45,
        accent_primary=(212, 114, 38),
        accent_secondary=(72, 110, 120),
        muted_ui=(126, 118, 108),
        horizon_color=(56, 50, 44),
        mote_color=(178, 138, 86),
        glow_color=(244, 196, 118),
        glow_alpha_max=34,
        grain_alpha=(6, 15),
        paper_grid=True,
    ),
}


def ease_out_cubic(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return 1.0 - (1.0 - x) ** 3


def ease_in_out_sine(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return -(math.cos(math.pi * x) - 1.0) / 2.0


def ease_out_back(x: float) -> float:
    x = max(0.0, min(1.0, x))
    c1 = 1.70158
    c3 = c1 + 1.0
    return 1.0 + c3 * ((x - 1.0) ** 3) + c1 * ((x - 1.0) ** 2)


def _platform_font_candidates() -> list[str]:
    candidates: list[str] = []
    skill_fonts = Path(__file__).resolve().parent.parent / "assets" / "fonts"
    if skill_fonts.is_dir():
        for ext in ("*.ttc", "*.ttf", "*.otf"):
            candidates.extend(sorted(str(p) for p in skill_fonts.glob(ext)))

    if sys.platform == "darwin":
        candidates.extend([
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/Supplemental/Songti.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
        ])
        candidates.extend(sorted(glob.glob("/System/Library/AssetsV2/*/PingFang*.ttc")))
    elif sys.platform.startswith("win"):
        win_fonts = Path("C:/Windows/Fonts")
        candidates.extend([
            str(win_fonts / "msyhbd.ttc"),
            str(win_fonts / "msyh.ttc"),
            str(win_fonts / "Dengb.ttf"),
            str(win_fonts / "Deng.ttf"),
            str(win_fonts / "simhei.ttf"),
            str(win_fonts / "simsun.ttc"),
        ])
    else:
        candidates.extend([
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Medium.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        ])
        if shutil.which("fc-match"):
            try:
                out = subprocess.check_output(
                    ["fc-match", ":lang=zh", "-f", "%{file}"],
                    text=True,
                    stderr=subprocess.DEVNULL,
                ).strip()
                if out:
                    candidates.insert(0, out)
            except Exception:
                pass
    return candidates


def resolve_font_path(explicit_path: str | None = None) -> str | None:
    candidates = [explicit_path] if explicit_path else []
    candidates.extend(_platform_font_candidates())
    for path in candidates:
        if path and Path(path).is_file():
            try:
                ImageFont.truetype(path, size=32, index=0)
                return path
            except Exception:
                try:
                    ImageFont.truetype(path, size=32)
                    return path
                except Exception:
                    continue
    return None


def load_font(resolved_path: str | None, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if resolved_path:
        try:
            return ImageFont.truetype(resolved_path, size=size, index=0)
        except Exception:
            try:
                return ImageFont.truetype(resolved_path, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def check_environment(explicit_font: str | None = None) -> tuple[bool, str | None]:
    """Verify ffmpeg and CJK font availability, returning (ffmpeg_ok, font_path)."""
    ffmpeg_bin = shutil.which("ffmpeg")
    if not ffmpeg_bin:
        hint = (
            "  macOS:   brew install ffmpeg\n"
            "  Windows: winget install Gyan.FFmpeg\n"
            "  Linux:   sudo apt install ffmpeg"
        )
        print("[ERROR] ffmpeg not found in PATH.\nInstall ffmpeg first:\n" + hint, file=sys.stderr)
        return False, None

    font_path = resolve_font_path(explicit_font)
    if not font_path:
        print(
            "[WARN] No CJK font detected automatically; Chinese characters may render as boxes.\n"
            "Pass --font /path/to/font.ttc or install Noto Sans CJK / PingFang / Microsoft YaHei.",
            file=sys.stderr,
        )
    return True, font_path


def _cover_resize(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w = int(round(src_w * scale))
    new_h = int(round(src_h * scale))
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def build_base_backdrop(
    theme: ThemePalette,
    bg_image_path: Path | None = None,
    bg_scrim_alpha: int = 120,
    seed: int = 42,
) -> Image.Image:
    """Pre-bake backdrop (theme gradient or custom image), paper grain, and desk horizon."""
    if bg_image_path is not None:
        raw_bg = Image.open(bg_image_path).convert("RGBA")
        img = _cover_resize(raw_bg, WIDTH, HEIGHT)
        scrim_col = (*theme.bg_bottom, max(0, min(230, bg_scrim_alpha)))
        scrim = Image.new("RGBA", (WIDTH, HEIGHT), scrim_col)
        img = Image.alpha_composite(img, scrim)
    else:
        img = Image.new("RGBA", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(img)
        for y in range(HEIGHT):
            ratio = y / (HEIGHT - 1)
            r = int(theme.bg_top[0] + (theme.bg_bottom[0] - theme.bg_top[0]) * ratio)
            g = int(theme.bg_top[1] + (theme.bg_bottom[1] - theme.bg_top[1]) * ratio)
            b = int(theme.bg_top[2] + (theme.bg_bottom[2] - theme.bg_top[2]) * ratio)
            draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

        if theme.paper_grid:
            grid = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            gdraw = ImageDraw.Draw(grid)
            for gx in range(72, WIDTH - 60, 54):
                for gy in range(120, HEIGHT - 120, 54):
                    gdraw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(138, 128, 114, 42))
            # Subtle vertical journal margin rule
            gdraw.line([(86, 90), (86, HEIGHT - 90)], fill=(198, 130, 108, 45), width=2)
            img = Image.alpha_composite(img, grid)

    # Subtle paper speckle grain
    rng = random.Random(seed)
    grain_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    grain_draw = ImageDraw.Draw(grain_layer)
    a_lo, a_hi = theme.grain_alpha
    for _ in range(9500):
        gx = rng.randint(0, WIDTH - 1)
        gy = rng.randint(0, HEIGHT - 1)
        tone = 255 if rng.random() > 0.5 else 0
        grain_draw.point((gx, gy), fill=(tone, tone, tone, rng.randint(a_lo, a_hi)))
    img = Image.alpha_composite(img, grain_layer)

    # Subtle comic desk horizon line near lower third
    horizon = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(horizon)
    hc = theme.horizon_color
    hdraw.line([(120, HORIZON_Y + 2), (WIDTH - 120, HORIZON_Y + 2)], fill=(*hc, 175), width=4)
    hdraw.line([(200, HORIZON_Y + 16), (WIDTH - 200, HORIZON_Y + 16)], fill=(*hc, 80), width=2)
    return Image.alpha_composite(img, horizon)


def build_warm_glow(theme: ThemePalette, radius: int = 440) -> Image.Image:
    size = radius * 2
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    for step in range(40, 0, -1):
        frac = step / 40.0
        cur_r = int(radius * frac)
        alpha = int(theme.glow_alpha_max * ((1.0 - frac) ** 1.8))
        draw.ellipse(
            [radius - cur_r, radius - cur_r, radius + cur_r, radius + cur_r],
            fill=(*theme.glow_color, alpha),
        )
    return glow


def load_and_trim_sticker(path: Path, target_max_w: int = 760, target_max_h: int = 760) -> Image.Image:
    img = Image.open(path).convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    w, h = img.size
    scale = min(target_max_w / w, target_max_h / h)
    new_size = (max(1, int(round(w * scale))), max(1, int(round(h * scale))))
    return img.resize(new_size, Image.Resampling.LANCZOS)


def resolve_asset_path(raw: str, base_dir: Path, skill_dir: Path) -> Path:
    p = Path(raw)
    if p.is_file():
        return p
    for root in (base_dir, skill_dir):
        candidate = root / raw
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"Asset not found: {raw}")


def _draw_hand_underline(
    draw: ImageDraw.ImageDraw,
    x0: int,
    x1: int,
    y: int,
    progress: float,
    color: tuple[int, int, int],
    alpha: int,
    seed: int = 7,
) -> None:
    if progress <= 0.01 or x1 <= x0 + 4 or alpha <= 0:
        return
    span = x1 - x0
    cur_end = x0 + span * max(0.0, min(1.0, progress))
    steps = max(8, int(span / 16))
    pts_main: list[tuple[float, float]] = []
    pts_sub: list[tuple[float, float]] = []
    for i in range(steps + 1):
        frac = i / steps
        px = x0 + span * frac
        if px > cur_end:
            px = cur_end
        arch = -3.0 * math.sin(math.pi * frac)
        wobble = 1.6 * math.sin(frac * 9.5 + seed)
        pts_main.append((px, y + arch + wobble))
        pts_sub.append((px + 2.0, y + 7.0 + arch * 0.6 - wobble * 0.6))
        if px >= cur_end:
            break

    if len(pts_main) >= 2:
        draw.line(pts_main, fill=(*color, int(alpha * 0.92)), width=5, joint="curve")
    if len(pts_sub) >= 2 and progress > 0.25:
        draw.line(pts_sub, fill=(*color, int(alpha * 0.42)), width=2, joint="curve")


def _fit_font_for_line(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_path: str | None,
    base_size: int,
    max_width: int = WIDTH - 140,
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    size = base_size
    while size >= 34:
        font = load_font(font_path, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            return font
        size -= 4
    return load_font(font_path, 34)


def draw_highlighted_line(
    draw: ImageDraw.ImageDraw,
    text: str,
    visible_chars: int,
    highlights: list[str],
    font_path: str | None,
    base_font_size: int,
    center_x: int,
    y: int,
    alpha: int,
    underline_progress: float,
    theme: ThemePalette,
    line_seed: int = 1,
) -> None:
    if alpha <= 0 or visible_chars <= 0 or not text:
        return

    font = _fit_font_for_line(draw, text, font_path, base_font_size)
    full_box = draw.textbbox((0, 0), text, font=font)
    total_w = full_box[2] - full_box[0]
    start_x = center_x - total_w // 2

    # Build character-level highlight mask from full text so partial typewriter reveals stay color-stable
    hi_mask = [False] * len(text)
    idx = 0
    while idx < len(text):
        matched = None
        for kw in highlights:
            if kw and text.startswith(kw, idx):
                if matched is None or len(kw) > len(matched):
                    matched = kw
        if matched:
            for k in range(idx, idx + len(matched)):
                hi_mask[k] = True
            idx += len(matched)
        else:
            idx += 1

    visible_text = text[:visible_chars]
    spans: list[tuple[str, bool]] = []
    for ch, is_hi in zip(visible_text, hi_mask[:visible_chars]):
        if spans and spans[-1][1] == is_hi:
            spans[-1] = (spans[-1][0] + ch, is_hi)
        else:
            spans.append((ch, is_hi))

    ascent, descent = font.getmetrics() if hasattr(font, "getmetrics") else (50, 12)
    underline_y = y + ascent + max(10, descent // 2)

    cur_x = start_x
    for span_idx, (segment, is_hi) in enumerate(spans):
        seg_box = draw.textbbox((0, 0), segment, font=font)
        seg_w = seg_box[2] - seg_box[0]
        color = (*theme.accent_primary, alpha) if is_hi else (*theme.text_primary, alpha)
        shadow_alpha = int(alpha * theme.text_shadow_alpha)
        draw.text((cur_x + 2, y + 3), segment, font=font, fill=(*theme.text_shadow, shadow_alpha))
        draw.text((cur_x, y), segment, font=font, fill=color)

        if is_hi and underline_progress > 0.01:
            _draw_hand_underline(
                draw,
                cur_x,
                cur_x + seg_w,
                underline_y,
                underline_progress,
                theme.accent_primary,
                alpha,
                seed=line_seed * 13 + span_idx,
            )
        cur_x += seg_w


def draw_mood_doodles(
    layer: Image.Image,
    doodles: list[str],
    t: float,
    local_beat: float,
    beat_pulse: float,
    sticker_box: tuple[int, int, int, int],
    theme: ThemePalette,
) -> None:
    """Draw editorial manga-ink doodles around the character or upper frame."""
    if not doodles:
        return
    draw = ImageDraw.Draw(layer)
    sx, sy, sw, sh = sticker_box
    ink = theme.text_primary if theme.name == "paper_cream" else (232, 228, 220)
    amber = theme.accent_primary
    teal = theme.accent_secondary

    for kind in doodles:
        if kind == "thought_dots":
            # Three drifting manga ellipsis dots above right of character head
            base_x = sx + int(sw * 0.78)
            base_y = sy + int(sh * 0.14)
            for i in range(3):
                phase = (local_beat * 0.7 - i * 0.35) % 2.0
                bob = math.sin(t * 2.2 + i * 0.9) * 6.0
                r = 7 + i * 3
                alpha = int(120 + 95 * max(0.0, math.sin(math.pi * min(1.0, phase))))
                cx = base_x + i * 32
                cy = base_y - i * 18 + bob
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*amber, alpha), outline=(*ink, alpha), width=2)

        elif kind == "sigh_lines":
            # Subtle hand-drawn sigh wisps near shoulder
            base_x = sx + int(sw * 0.14)
            base_y = sy + int(sh * 0.32)
            breath = 0.5 + 0.5 * math.sin(local_beat * math.pi * 0.5)
            alpha = int(105 + 85 * breath)
            for idx in range(2):
                ox = base_x - idx * 20 - int(breath * 10)
                oy = base_y + idx * 24 + int(breath * 8)
                pts = [(ox, oy), (ox - 24, oy + 14), (ox - 12, oy + 32)]
                draw.line(pts, fill=(*teal, alpha), width=4, joint="curve")

        elif kind == "warm_sparks":
            # Gentle 4-point manga star sparkles in outer negative space (never over character)
            anchors = [
                (max(70, sx + int(sw * 0.05)), sy + int(sh * 0.12), 0.0),
                (min(WIDTH - 70, sx + int(sw * 0.94)), sy + int(sh * 0.16), 1.4),
                (min(WIDTH - 70, sx + int(sw * 0.97)), sy + int(sh * 0.45), 2.7),
            ]
            for ax, ay, ph in anchors:
                twinkle = 0.45 + 0.55 * math.sin(t * 2.6 + ph)
                r = 10 + 9 * twinkle + 4 * beat_pulse
                alpha = int(110 + 130 * twinkle)
                draw.line([(ax - r, ay), (ax + r, ay)], fill=(*amber, alpha), width=3)
                draw.line([(ax, ay - r), (ax, ay + r)], fill=(*amber, alpha), width=3)
                ir = r * 0.35
                draw.ellipse([ax - ir, ay - ir, ax + ir, ay + ir], fill=(*amber, alpha))

        elif kind == "steam_wisps":
            # Rising organic steam curls in upper-left negative space (safe from head)
            base_x = max(90, sx + int(sw * 0.08))
            base_y = sy + int(sh * 0.34)
            for idx in range(2):
                pts: list[tuple[float, float]] = []
                for step in range(12):
                    frac = step / 11.0
                    py = base_y - frac * 95 - ((t * 24 + idx * 40) % 40)
                    px = base_x + idx * 28 + math.sin(frac * 4.5 - t * 2.5 + idx) * 12
                    pts.append((px, py))
                alpha = int(115 + 55 * math.sin(t * 2.0 + idx))
                draw.line(pts, fill=(*ink, alpha), width=3, joint="curve")

        elif kind == "rain_streaks":
            rng = random.Random(303)
            for idx in range(16):
                rx0 = rng.randint(60, WIDTH - 60)
                ry0 = (rng.randint(0, HEIGHT) + int(t * (380 + (idx % 3) * 90))) % (HEIGHT - 320)
                length = 34 + (idx % 4) * 12
                alpha = 42 if theme.name == "paper_cream" else 55
                draw.line([(rx0, ry0), (rx0 - 6, ry0 + length)], fill=(*teal, alpha), width=2)

        elif kind == "bracket_emphasis":
            alpha = int(145 + 50 * beat_pulse)
            bx0, bx1 = 115, WIDTH - 115
            by0, by1 = 335, 650
            arm = 34
            for (x_corner, dx), (y_corner, dy) in [
                ((bx0, 1), (by0, 1)),
                ((bx1, -1), (by0, 1)),
                ((bx0, 1), (by1, -1)),
                ((bx1, -1), (by1, -1)),
            ]:
                draw.line([(x_corner, y_corner), (x_corner + dx * arm, y_corner)], fill=(*amber, alpha), width=4)
                draw.line([(x_corner, y_corner), (x_corner, y_corner + dy * arm)], fill=(*amber, alpha), width=4)


def synthesize_beat_wav(
    wav_path: Path,
    duration_sec: float,
    bpm: float,
    sample_rate: int = 44100,
) -> None:
    """Synthesize a soft Lo-Fi muted kick/wood-tick beat track for preview."""
    total_samples = int(duration_sec * sample_rate)
    beat_sec = 60.0 / bpm
    buf = [0.0] * total_samples

    beat_idx = 0
    while True:
        t0 = beat_idx * beat_sec
        if t0 >= duration_sec:
            break
        s0 = int(t0 * sample_rate)
        is_downbeat = (beat_idx % 4 == 0)
        hit_len = int(0.16 * sample_rate)
        for i in range(hit_len):
            pos = s0 + i
            if pos >= total_samples:
                break
            dt = i / sample_rate
            if is_downbeat:
                freq = 55.0 + 65.0 * math.exp(-dt * 28.0)
                env = math.exp(-dt * 18.0) * (1.0 - math.exp(-dt * 250.0))
                buf[pos] += 0.42 * env * math.sin(2.0 * math.pi * freq * dt)
            else:
                env = math.exp(-dt * 45.0) * (1.0 - math.exp(-dt * 400.0))
                buf[pos] += 0.16 * env * math.sin(2.0 * math.pi * 620.0 * dt)
        beat_idx += 1

    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        pcm = bytearray()
        for sample in buf:
            clamped = max(-0.98, min(0.98, sample))
            pcm.extend(struct.pack("<h", int(clamped * 32767)))
        wf.writeframes(bytes(pcm))


def _pick_frame_from_list(
    frames: list[Image.Image],
    sc: dict[str, Any],
    local_t: float,
    local_beat: float,
) -> Image.Image:
    if len(frames) == 1:
        return frames[0]
    mode = sc.get("frame_mode", "pingpong")
    if mode == "natural_blink":
        # Stay on frame 0 most of the time; brief ~0.16s blink on frame 1 every ~2.5s
        cycle_sec = float(sc.get("blink_interval", 2.5))
        phase = (local_t + 0.6) % cycle_sec
        return frames[1] if phase < 0.16 else frames[0]
    if mode == "beat_toggle":
        beats_per = float(sc.get("beats_per_frame", 1.0))
        idx = int(local_beat / max(0.25, beats_per)) % len(frames)
        return frames[idx]
    fps_anim = float(sc.get("frame_fps", 4.0))
    step = int(local_t * fps_anim)
    if mode == "pingpong" and len(frames) > 2:
        cycle = len(frames) * 2 - 2
        pos = step % cycle
        idx = pos if pos < len(frames) else cycle - pos
        return frames[idx]
    return frames[step % len(frames)]


def _build_text_scrim(text_pos: str) -> Image.Image:
    """Create a subtle gradient scrim behind subtitles for full-frame illustrations."""
    scrim = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scrim)
    if text_pos == "bottom":
        y0, y1 = 1240, HEIGHT
        for y in range(y0, y1):
            frac = (y - y0) / (y1 - y0)
            alpha = int(175 * (frac ** 1.3))
            draw.line([(0, y), (WIDTH, y)], fill=(10, 14, 18, alpha))
    else:
        y0, y1 = 0, 740
        for y in range(y0, y1):
            frac = 1.0 - (y - y0) / (y1 - y0)
            alpha = int(155 * (frac ** 1.35))
            draw.line([(0, y), (WIDTH, y)], fill=(10, 14, 18, alpha))
    return scrim


def _build_vignette(strength: int = 90) -> Image.Image:
    """Create a smooth photographic edge vignette with zero concentric banding."""
    vig = Image.new("RGBA", (WIDTH, HEIGHT), (8, 12, 16, strength))
    mask = Image.new("L", (WIDTH, HEIGHT), 255)
    mdraw = ImageDraw.Draw(mask)
    pad_x = int(WIDTH * 0.14)
    pad_y = int(HEIGHT * 0.14)
    mdraw.ellipse([pad_x, pad_y, WIDTH - pad_x, HEIGHT - pad_y], fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=140))
    vig_alpha = mask.point(lambda p: int(p * (strength / 255.0)))
    vig.putalpha(vig_alpha)
    return vig


def _build_bokeh_orb(radius: int, color: tuple[int, int, int], alpha: int = 44) -> Image.Image:
    size = radius * 2 + 48
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    c = size // 2
    draw.ellipse([c - radius, c - radius, c + radius, c + radius], fill=(*color, alpha))
    return img.filter(ImageFilter.GaussianBlur(radius=max(8, radius // 3)))


def _build_steam_puff() -> Image.Image:
    size = 150
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([36, 36, 114, 114], fill=(248, 244, 236, 52))
    return img.filter(ImageFilter.GaussianBlur(radius=22))


def _build_sunbeam_sprite() -> Image.Image:
    beam = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(beam)
    draw.polygon([(WIDTH - 40, 0), (WIDTH, 420), (340, HEIGHT), (60, HEIGHT)], fill=(255, 214, 146, 36))
    draw.polygon([(WIDTH - 140, 0), (WIDTH - 20, 200), (140, HEIGHT - 180), (-60, HEIGHT - 360)], fill=(255, 224, 168, 28))
    return beam.filter(ImageFilter.GaussianBlur(radius=46))


def _build_grain_tiles(count: int = 4) -> list[Image.Image]:
    """Pre-bake subtle 16mm monochrome film grain overlays for organic animation feel."""
    tiles: list[Image.Image] = []
    for seed_idx in range(count):
        rng = random.Random(900 + seed_idx)
        tile = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(tile)
        for _ in range(11000):
            gx = rng.randint(0, WIDTH - 1)
            gy = rng.randint(0, HEIGHT - 1)
            tone = 255 if rng.random() > 0.5 else 0
            draw.point((gx, gy), fill=(tone, tone, tone, rng.randint(5, 13)))
        tiles.append(tile)
    return tiles


@dataclass
class RenderAssets:
    backdrop: Image.Image
    warm_glow: Image.Image
    vignette: Image.Image
    scrims: dict[str, Image.Image]
    bokeh_amber: Image.Image
    bokeh_teal: Image.Image
    steam_puff: Image.Image
    sunbeam: Image.Image
    grain_tiles: list[Image.Image]
    motes: list[tuple[float, float, float, float, float]]
    bokeh_seeds: list[tuple[float, float, float, float, bool]]
    rain_drops: list[tuple[float, float, float, float]]


def _apply_sensory_fx(
    stage: Image.Image,
    sc: dict[str, Any],
    assets: RenderAssets,
    t: float,
    beat_pulse: float,
    theme: ThemePalette,
) -> Image.Image:
    raw_fx = sc.get("fx", [])
    fx_list = [raw_fx] if isinstance(raw_fx, str) else list(raw_fx)
    if not fx_list:
        return stage

    for fx in fx_list:
        if fx == "coffee_steam":
            pos = sc.get("steam_pos", [0.52, 0.62])
            sx0 = int(WIDTH * float(pos[0]))
            sy0 = int(HEIGHT * float(pos[1]))
            for idx in range(6):
                life = ((t * 0.42 + idx / 6.0) % 1.0)
                px = sx0 + int(24 * math.sin(life * 5.2 + idx * 1.1) + 12 * life)
                py = sy0 - int(life * 220)
                scale = 0.6 + 0.75 * life
                pw = max(16, int(assets.steam_puff.width * scale))
                ph = max(16, int(assets.steam_puff.height * scale))
                puff = assets.steam_puff.resize((pw, ph), Image.Resampling.BILINEAR)
                fade = math.sin(math.pi * life)
                alpha_band = puff.getchannel("A").point(lambda a, f=fade: int(a * f * 0.85))
                puff.putalpha(alpha_band)
                stage.alpha_composite(puff, (px - pw // 2, py - ph // 2))

        elif fx == "sunbeams":
            sway = 0.55 + 0.45 * math.sin(t * 0.85)
            beam = assets.sunbeam.copy()
            alpha_band = beam.getchannel("A").point(lambda a, s=sway: int(a * s))
            beam.putalpha(alpha_band)
            offset_x = int(28 * math.sin(t * 0.55))
            stage.alpha_composite(beam, (offset_x, 0))

        elif fx == "bokeh_depth":
            for bx0, by0, speed, phase, is_amber in assets.bokeh_seeds:
                orb = assets.bokeh_amber if is_amber else assets.bokeh_teal
                bx = int((bx0 + 65 * math.sin(t * speed * 0.7 + phase)) % (WIDTH + 120)) - 60
                by = int((by0 - t * 48 * speed) % (HEIGHT + 120)) - 60
                stage.alpha_composite(orb, (bx - orb.width // 2, by - orb.height // 2))

        elif fx == "rain_glass":
            rain_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            rdraw = ImageDraw.Draw(rain_layer)
            for rx0, ry0, rspeed, rlen in assets.rain_drops:
                ry = (ry0 + t * rspeed) % (HEIGHT - 120)
                rdraw.line([(rx0, ry), (rx0 - 5, ry + rlen)], fill=(176, 212, 220, 52), width=2)
                rdraw.ellipse([rx0 - 8, ry + rlen - 3, rx0 - 2, ry + rlen + 3], fill=(215, 236, 240, 72))
            stage = Image.alpha_composite(stage, rain_layer)

        elif fx == "cat_zzz":
            # Gentle hand-inked "z Z" floating sleep glyphs above cat_pos
            pos = sc.get("cat_pos", [0.74, 0.72])
            cx0 = int(WIDTH * float(pos[0]))
            cy0 = int(HEIGHT * float(pos[1]))
            z_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            zdraw = ImageDraw.Draw(z_layer)
            ink_col = theme.text_primary if theme.name == "paper_cream" else (232, 236, 238)
            for idx in range(3):
                life = (t * 0.45 + idx / 3.0) % 1.0
                zx = cx0 + idx * 18 + int(14 * math.sin(life * 4.5 + idx))
                zy = cy0 - int(life * 120)
                sz = 16 + idx * 5
                alpha = int(205 * math.sin(math.pi * life))
                if alpha > 8:
                    pts = [(zx, zy), (zx + sz, zy), (zx, zy + sz), (zx + sz, zy + sz)]
                    zdraw.line(pts, fill=(*ink_col, alpha), width=3, joint="curve")
            stage = Image.alpha_composite(stage, z_layer)

        elif fx == "purr_waves":
            # Soft curved manga purr / comfort vibration lines beside cat_pos
            pos = sc.get("cat_pos", [0.70, 0.62])
            cx0 = int(WIDTH * float(pos[0]))
            cy0 = int(HEIGHT * float(pos[1]))
            p_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            pdraw = ImageDraw.Draw(p_layer)
            pulse = 0.4 + 0.6 * (0.5 + 0.5 * math.sin(t * 3.8))
            alpha = int(130 * pulse)
            for idx in range(2):
                ox = cx0 + idx * 16
                oy = cy0 - idx * 14 - int(pulse * 5)
                pts = [
                    (ox, oy),
                    (ox + 12, oy - 7),
                    (ox + 22, oy + 2),
                    (ox + 34, oy - 5),
                ]
                pdraw.line(pts, fill=(*theme.accent_primary, alpha), width=3, joint="curve")
            stage = Image.alpha_composite(stage, p_layer)

        elif fx == "prop_pulse":
            # Subtle breathing ambient glow over a specific prop (e.g. phone screen, clock, streetlight)
            pos = sc.get("prop_pos", [0.70, 0.56])
            px0 = int(WIDTH * float(pos[0]))
            py0 = int(HEIGHT * float(pos[1]))
            p_color = sc.get("prop_color", "teal")
            base_orb = assets.bokeh_amber if p_color == "amber" else assets.bokeh_teal
            pulse = 0.55 + 0.45 * math.sin(t * 2.2) + 0.25 * beat_pulse
            scale = 1.6 + 0.5 * pulse
            pw = max(32, int(base_orb.width * scale))
            ph = max(32, int(base_orb.height * scale))
            orb = base_orb.resize((pw, ph), Image.Resampling.BILINEAR)
            alpha_band = orb.getchannel("A").point(lambda a, p=pulse: min(255, int(a * (0.8 + 0.7 * p))))
            orb.putalpha(alpha_band)
            stage.alpha_composite(orb, (px0 - pw // 2, py0 - ph // 2))

        elif fx == "film_grain":
            tile_idx = int(t * 12.0) % len(assets.grain_tiles)
            stage = Image.alpha_composite(stage, assets.grain_tiles[tile_idx])

    return stage


def _transform_sticker(
    sticker: Image.Image,
    motion: str,
    local_t: float,
    local_beat: float,
    beat_sec: float,
    beat_pulse: float,
) -> Image.Image:
    sx_factor = 1.0
    sy_factor = 1.0
    angle = 0.0
    if motion == "bounce_in":
        p = ease_out_back(min(1.0, local_t / (beat_sec * 0.55)))
        s = 0.85 + 0.15 * p + 0.015 * beat_pulse
        sx_factor, sy_factor = s, s
    elif motion == "beat_nod":
        sx_factor = 1.0 + 0.018 * beat_pulse
        sy_factor = 1.0 + 0.011 * beat_pulse
    elif motion == "zoom_punch":
        punch = math.exp(-7.5 * local_t)
        s = 1.0 + 0.12 * punch + 0.015 * beat_pulse
        sx_factor, sy_factor = s, s
    elif motion == "sigh_sway":
        sway = math.sin(math.pi * local_beat / 2.0)
        angle = 1.8 * sway
        sy_factor = 1.0 - 0.014 * (0.5 - 0.5 * math.cos(math.pi * local_beat))
        sx_factor = 1.0 + 0.008 * (0.5 - 0.5 * math.cos(math.pi * local_beat))
    elif motion == "calm_float":
        breath = math.sin(math.pi * local_beat / 2.0)
        sx_factor = 1.0 + 0.012 * breath
        sy_factor = 1.0 + 0.016 * breath
    else:  # alive_idle
        breath = math.sin(math.pi * local_beat)
        sx_factor = 1.0 - 0.009 * breath + 0.012 * beat_pulse
        sy_factor = 1.0 + 0.015 * breath + 0.012 * beat_pulse
        angle = 0.7 * math.sin(math.pi * local_beat / 2.0)

    sw = max(1, int(round(sticker.width * sx_factor)))
    sh = max(1, int(round(sticker.height * sy_factor)))
    out = sticker.resize((sw, sh), Image.Resampling.BILINEAR)
    if abs(angle) > 0.05:
        out = out.rotate(angle, resample=Image.Resampling.BILINEAR, expand=True)
    return out


def _sticker_dy(motion: str, local_t: float, local_beat: float, beat_sec: float, beat_pulse: float) -> float:
    if motion == "bounce_in":
        p = ease_out_back(min(1.0, local_t / (beat_sec * 0.55)))
        return (1.0 - p) * 55.0
    if motion == "beat_nod":
        return 8.0 * beat_pulse
    if motion == "sigh_sway":
        return 10.0 * (0.5 - 0.5 * math.cos(math.pi * local_beat / 2.0))
    if motion == "calm_float":
        return 5.0 * math.sin(math.pi * local_beat / 2.0)
    return 0.0


def _render_scene_layer(
    sc: dict[str, Any],
    t: float,
    beat_sec: float,
    total_duration: float,
    assets: RenderAssets,
    theme: ThemePalette,
    font_path: str | None,
    base_font_size: int,
    font_tag: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    header_tag: str,
) -> Image.Image:
    local_t = max(0.0, t - sc["start_t"])
    scene_dur = max(0.01, sc["end_t"] - sc["start_t"])
    scene_prog = min(1.0, local_t / scene_dur)
    local_beat = local_t / beat_sec
    beat_phase = (t / beat_sec) % 1.0
    beat_pulse = math.exp(-7.0 * beat_phase)
    cam = sc.get("camera", "static")

    scene_frames: list[Image.Image] = sc.get("scene_frames", [])
    is_full_frame = len(scene_frames) > 0
    if is_full_frame:
        src = _pick_frame_from_list(scene_frames, sc, local_t, local_beat)
        oversample_w, oversample_h = src.size
        base_scale = WIDTH / oversample_w
        zoom = 1.0
        pan_x = 0.0
        pan_y = 0.0
        prog_eased = ease_in_out_sine(scene_prog)

        if cam == "push_in":
            zoom = 1.0 + 0.08 * prog_eased
        elif cam == "pull_out":
            zoom = 1.08 - 0.08 * prog_eased
        elif cam == "pan_left":
            zoom = 1.06
            pan_x = 0.65 - 1.3 * prog_eased
        elif cam == "pan_right":
            zoom = 1.06
            pan_x = -0.65 + 1.3 * prog_eased
        elif cam == "pan_up":
            zoom = 1.06
            pan_y = 0.65 - 1.3 * prog_eased
        elif cam == "pan_down":
            zoom = 1.06
            pan_y = -0.65 + 1.3 * prog_eased
        elif cam == "drift_diag":
            zoom = 1.02 + 0.06 * prog_eased
            pan_x = -0.45 + 0.9 * prog_eased
            pan_y = 0.35 - 0.7 * prog_eased
        else:
            zoom = 1.03 + 0.016 * math.sin(math.pi * local_beat / 2.0)

        breath_dx = 5.0 * math.sin(t * 1.15)
        breath_dy = 6.5 * math.cos(t * 0.92)
        eff_scale = base_scale * zoom
        crop_w = WIDTH / eff_scale
        crop_h = HEIGHT / eff_scale
        slack_x = max(0.0, (oversample_w - crop_w) / 2.0)
        slack_y = max(0.0, (oversample_h - crop_h) / 2.0)
        cx = oversample_w / 2.0 + pan_x * slack_x * 0.85 + breath_dx
        cy = oversample_h / 2.0 + pan_y * slack_y * 0.85 + breath_dy
        x0 = max(0.0, min(oversample_w - crop_w, cx - crop_w / 2.0))
        y0 = max(0.0, min(oversample_h - crop_h, cy - crop_h / 2.0))
        stage = src.crop((x0, y0, x0 + crop_w, y0 + crop_h)).resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)

        # Optional 2.5D foreground parallax character/object layer moving faster than background
        fg_frames: list[Image.Image] = sc.get("fg_frames", [])
        if fg_frames:
            fg_raw = _pick_frame_from_list(fg_frames, sc, local_t, local_beat)
            fg_motion = sc.get("motion", "alive_idle")
            fg_scale_mult = float(sc.get("fg_scale", 1.0)) * (1.0 + (zoom - 1.0) * float(sc.get("fg_parallax", 1.45)))
            cur_fg = _transform_sticker(fg_raw, fg_motion, local_t, local_beat, beat_sec, beat_pulse)
            if abs(fg_scale_mult - 1.0) > 0.002:
                fw = max(1, int(round(cur_fg.width * fg_scale_mult)))
                fh = max(1, int(round(cur_fg.height * fg_scale_mult)))
                cur_fg = cur_fg.resize((fw, fh), Image.Resampling.BILINEAR)
            fg_parallax_px = float(sc.get("fg_parallax", 1.45))
            fg_dx = int(-pan_x * 36 * fg_parallax_px + breath_dx * 1.35 + float(sc.get("fg_offset_x", 0)))
            fg_dy = int(_sticker_dy(fg_motion, local_t, local_beat, beat_sec, beat_pulse) - pan_y * 28 * fg_parallax_px + breath_dy * 1.35)
            fx = WIDTH // 2 - cur_fg.width // 2 + fg_dx
            fy = int(sc.get("fg_bottom_y", 1710)) - cur_fg.height + fg_dy
            stage.alpha_composite(cur_fg, (fx, fy))

        # Dynamic breathing light bloom over lamp / sunlight anchor (with optional filament flicker)
        light_pos = sc.get("light_pos")
        if light_pos and len(light_pos) == 2:
            flicker = 0.0
            if "lamp_flicker" in (sc.get("fx") or []):
                flicker = 0.08 * math.sin(t * 11.3) * math.cos(t * 4.7)
            glow_scale = 0.92 + 0.14 * (0.5 + 0.5 * math.sin(t * 1.7)) + 0.06 * beat_pulse + flicker
            gw = max(64, int(assets.warm_glow.width * glow_scale))
            gh = max(64, int(assets.warm_glow.height * glow_scale))
            glow_resized = assets.warm_glow.resize((gw, gh), Image.Resampling.BILINEAR)
            lx = int(WIDTH * float(light_pos[0])) - gw // 2
            ly = int(HEIGHT * float(light_pos[1])) - gh // 2
            stage.alpha_composite(glow_resized, (lx, ly))

        # Ambient drifting dust motes
        mote_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        mdraw = ImageDraw.Draw(mote_layer)
        for mx0, my0, mr, mspeed, mphase in assets.motes:
            mx = mx0 + 22.0 * math.sin(t * mspeed + mphase)
            my = (my0 - t * 22.0 * mspeed) % (HEIGHT - 120)
            malpha = int(38 + 32 * math.sin(t * 1.4 + mphase) + 22 * beat_pulse)
            mdraw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(*theme.mote_color, max(8, min(125, malpha))))
        stage = Image.alpha_composite(stage, mote_layer)

        # Sensory fx (coffee_steam, sunbeams, bokeh_depth, rain_glass, film_grain)
        stage = _apply_sensory_fx(stage, sc, assets, t, beat_pulse, theme)

        raw_doodles = sc.get("doodle", [])
        doodles = [raw_doodles] if isinstance(raw_doodles, str) else list(raw_doodles)
        if doodles:
            doodle_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            draw_mood_doodles(doodle_layer, doodles, t, local_beat, beat_pulse, (140, 640, 800, 1000), theme)
            stage = Image.alpha_composite(stage, doodle_layer)

        stage = Image.alpha_composite(stage, assets.vignette)
        text_pos = sc.get("text_pos", "top")
        if text_pos in assets.scrims:
            stage = Image.alpha_composite(stage, assets.scrims[text_pos])
    else:
        # Mode B cutout sticker composition mode
        cam_scale = 1.0
        cam_dy = 0.0
        if cam == "push_in":
            cam_scale = 1.0 + 0.065 * ease_in_out_sine(scene_prog)
        elif cam == "pull_out":
            cam_scale = 1.065 - 0.065 * ease_in_out_sine(scene_prog)
        elif cam == "breathe":
            cam_scale = 1.015 + 0.02 * math.sin(math.pi * local_beat / 2.0)
        elif cam == "pan_up":
            cam_scale = 1.04
            cam_dy = 22.0 * (0.5 - ease_in_out_sine(scene_prog))
        elif cam == "pan_down":
            cam_scale = 1.04
            cam_dy = -22.0 * (0.5 - ease_in_out_sine(scene_prog))

        stage = assets.backdrop.copy()

        glow_scale = 0.96 + 0.08 * beat_pulse
        gw = int(assets.warm_glow.width * glow_scale)
        gh = int(assets.warm_glow.height * glow_scale)
        glow_resized = assets.warm_glow.resize((gw, gh), Image.Resampling.BILINEAR)
        stage.alpha_composite(glow_resized, (WIDTH // 2 - gw // 2, 1280 - gh // 2))

        mote_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        mdraw = ImageDraw.Draw(mote_layer)
        for mx0, my0, mr, mspeed, mphase in assets.motes:
            mx = mx0 + 18.0 * math.sin(t * mspeed + mphase)
            my = (my0 - t * 18.0 * mspeed) % 1620
            malpha = int(42 + 34 * math.sin(t * 1.4 + mphase) + 28 * beat_pulse)
            mdraw.ellipse(
                [mx - mr, my - mr, mx + mr, my + mr],
                fill=(*theme.mote_color, max(10, min(140, malpha))),
            )
        stage = Image.alpha_composite(stage, mote_layer)

        sticker = _pick_frame_from_list(sc["sticker_frames"], sc, local_t, local_beat)
        motion = sc.get("motion", "alive_idle")
        cur_sticker = _transform_sticker(sticker, motion, local_t, local_beat, beat_sec, beat_pulse)
        dy = _sticker_dy(motion, local_t, local_beat, beat_sec, beat_pulse)

        paste_x = int(WIDTH // 2 - cur_sticker.width // 2)
        paste_y = int(HORIZON_Y - cur_sticker.height + dy)
        stage.alpha_composite(cur_sticker, (paste_x, paste_y))

        stage = _apply_sensory_fx(stage, sc, assets, t, beat_pulse, theme)

        raw_doodles = sc.get("doodle", [])
        doodles = [raw_doodles] if isinstance(raw_doodles, str) else list(raw_doodles)
        if doodles:
            doodle_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            draw_mood_doodles(
                doodle_layer,
                doodles,
                t,
                local_beat,
                beat_pulse,
                (paste_x, paste_y, cur_sticker.width, cur_sticker.height),
                theme,
            )
            stage = Image.alpha_composite(stage, doodle_layer)

        if abs(cam_scale - 1.0) > 0.0005 or abs(cam_dy) > 0.5:
            zw = int(round(WIDTH * cam_scale))
            zh = int(round(HEIGHT * cam_scale))
            zoomed = stage.resize((zw, zh), Image.Resampling.BILINEAR)
            crop_x = (zw - WIDTH) // 2
            crop_y = max(0, min(zh - HEIGHT, (zh - HEIGHT) // 2 + int(round(cam_dy))))
            stage = zoomed.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))

    # Typography & HUD overlay
    text_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(text_layer)
    text_theme = THEMES["late_night"] if is_full_frame else theme

    if header_tag:
        tbox = tdraw.textbbox((0, 0), header_tag, font=font_tag)
        tw = tbox[2] - tbox[0]
        tdraw.text((WIDTH // 2 - tw // 2, 140), header_tag, font=font_tag, fill=(*text_theme.muted_ui, 195))

    bar_w = 180
    bar_x0 = WIDTH // 2 - bar_w // 2
    bar_y = 192
    tdraw.line([(bar_x0, bar_y), (bar_x0 + bar_w, bar_y)], fill=(*text_theme.muted_ui, 75), width=3)
    prog = min(1.0, t / max(0.01, total_duration))
    tdraw.line(
        [(bar_x0, bar_y), (bar_x0 + int(bar_w * prog), bar_y)],
        fill=(*text_theme.accent_primary, 215),
        width=3,
    )

    # Optional scene timestamp badge (e.g. "02:15 AM") for emotional passage of time
    ts_label = sc.get("timestamp")
    if ts_label:
        ts_font = load_font(font_path, 22)
        ts_box = tdraw.textbbox((0, 0), ts_label, font=ts_font)
        ts_w = ts_box[2] - ts_box[0]
        tdraw.text((WIDTH // 2 - ts_w // 2, 212), ts_label, font=ts_font, fill=(*text_theme.accent_primary, 175))

    lines: list[str] = sc.get("lines", [])
    highlights: list[str] = sc.get("highlight", [])
    text_anim = sc.get("text_anim", "beat_lines")
    line_spacing = 108
    text_pos = sc.get("text_pos", "top")
    if text_pos == "bottom":
        anchor_y = 1480
    elif text_pos == "center":
        anchor_y = 940
    else:
        anchor_y = 430 if is_full_frame else 490
    base_text_y = anchor_y - (len(lines) * line_spacing) // 2

    if text_anim == "typewriter_beat":
        total_chars = max(1, sum(len(s) for s in lines))
        reveal_beats = max(1.5, sc["beats"] * 0.62)
        char_budget = int(math.ceil(min(1.0, local_beat / reveal_beats) * total_chars))
        consumed = 0
        for idx_l, line_str in enumerate(lines):
            vis = max(0, min(len(line_str), char_budget - consumed))
            consumed += len(line_str)
            if vis <= 0:
                continue
            line_done_beat = reveal_beats * (consumed / total_chars)
            ul_prog = ease_out_cubic(min(1.0, max(0.0, (local_beat - line_done_beat) / 0.55)))
            draw_highlighted_line(
                tdraw,
                line_str,
                vis,
                highlights,
                font_path,
                base_font_size,
                WIDTH // 2,
                base_text_y + idx_l * line_spacing,
                255,
                ul_prog,
                text_theme,
                line_seed=idx_l + 1,
            )
    else:
        for idx_l, line_str in enumerate(lines):
            if text_anim == "beat_lines":
                slot = max(1.0, round((sc["beats"] * 0.72) / max(1, len(lines)) * 2.0) / 2.0)
                appear_beat = idx_l * slot
                if local_beat < appear_beat:
                    continue
                lt = (local_beat - appear_beat) * beat_sec
                p = ease_out_cubic(min(1.0, lt / 0.28))
                alpha = int(255 * p)
                y_off = int((1.0 - p) * 26)
                ul_prog = ease_out_cubic(min(1.0, max(0.0, (local_beat - appear_beat - 0.35) / 0.65)))
            elif text_anim == "word_pop":
                appear_beat = idx_l * 1.0
                if local_beat < appear_beat:
                    continue
                lt = (local_beat - appear_beat) * beat_sec
                p = ease_out_back(min(1.0, lt / 0.32))
                alpha = int(255 * min(1.0, lt / 0.16))
                y_off = int((1.0 - p) * 20)
                ul_prog = ease_out_cubic(min(1.0, max(0.0, (local_beat - appear_beat - 0.3) / 0.6)))
            elif text_anim == "slam_center":
                p = ease_out_cubic(min(1.0, local_t / 0.22))
                alpha = int(255 * p)
                y_off = int((1.0 - p) * 14)
                ul_prog = ease_out_cubic(min(1.0, max(0.0, (local_beat - 0.6) / 0.75)))
            else:  # fade_up
                p = ease_out_cubic(min(1.0, local_t / 0.45))
                alpha = int(255 * p)
                y_off = int((1.0 - p) * 20)
                ul_prog = ease_out_cubic(min(1.0, max(0.0, (local_beat - 0.55) / 0.75)))

            draw_highlighted_line(
                tdraw,
                line_str,
                len(line_str),
                highlights,
                font_path,
                base_font_size,
                WIDTH // 2,
                base_text_y + idx_l * line_spacing + y_off,
                alpha,
                ul_prog,
                text_theme,
                line_seed=idx_l + 1,
            )

    # Bottom 4-beat measure dot indicator
    cur_measure_beat = int(t / beat_sec) % 4
    dot_gap = 28
    dots_start_x = WIDTH // 2 - (3 * dot_gap) // 2
    for bi in range(4):
        cx = dots_start_x + bi * dot_gap
        cy = 1765
        is_cur = (bi == cur_measure_beat)
        r = 5 if is_cur else 3
        col = (*text_theme.accent_primary, int(190 + 60 * beat_pulse)) if is_cur else (*text_theme.muted_ui, 90)
        tdraw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

    return Image.alpha_composite(stage, text_layer)


def _apply_transition(
    prev_frame: Image.Image,
    cur_frame: Image.Image,
    transition: str,
    progress: float,
    theme: ThemePalette,
) -> Image.Image:
    p = ease_in_out_sine(progress)
    if transition == "crossfade":
        return Image.blend(prev_frame, cur_frame, p)
    if transition == "luma_fade":
        # Dip smoothly through midnight shadow in the midpoint for emotional beats
        if progress < 0.5:
            dip = ease_in_out_sine(progress * 2.0)
            shadow = Image.new("RGBA", (WIDTH, HEIGHT), (10, 14, 18, 255))
            return Image.blend(prev_frame, shadow, dip * 0.72)
        rise = ease_in_out_sine((progress - 0.5) * 2.0)
        shadow = Image.new("RGBA", (WIDTH, HEIGHT), (10, 14, 18, 255))
        return Image.blend(shadow, cur_frame, 0.28 + 0.72 * rise)
    if transition == "warm_dissolve":
        blended = Image.blend(prev_frame, cur_frame, p)
        glow_peak = math.sin(math.pi * progress)
        flash = Image.new("RGBA", (WIDTH, HEIGHT), (*theme.accent_primary, int(55 * glow_peak)))
        return Image.alpha_composite(blended, flash)
    if transition == "wipe_up":
        blended = Image.blend(prev_frame, cur_frame, min(1.0, p * 1.15))
        offset = int((1.0 - p) * 90)
        canvas = prev_frame.copy()
        canvas.paste(blended, (0, offset))
        return Image.blend(canvas, cur_frame, p)
    if transition == "ink_flash":
        flash_alpha = int(135 * (1.0 - p))
        flash = Image.new("RGBA", (WIDTH, HEIGHT), (*theme.accent_primary, flash_alpha))
        return Image.alpha_composite(cur_frame, flash)
    return cur_frame


def render_video(
    timeline_path: Path,
    out_prefix: Path,
    fps: int = 30,
    font_path: str | None = None,
    audio_path: Path | None = None,
    theme_override: str | None = None,
    bg_override: Path | None = None,
) -> tuple[Path, Path]:
    ok, resolved_font = check_environment(font_path)
    if not ok:
        raise SystemExit(1)

    data: dict[str, Any] = json.loads(timeline_path.read_text(encoding="utf-8"))
    bpm = float(data.get("bpm", 84))
    beat_sec = 60.0 / bpm
    header_tag = data.get("tag", "")
    theme_name = theme_override or data.get("theme", "late_night")
    if theme_name not in THEMES:
        raise ValueError(f"Unknown theme '{theme_name}'. Choose from: {', '.join(THEMES)}")
    theme = THEMES[theme_name]
    base_font_size = int(data.get("font_size", 58))

    base_dir = timeline_path.parent
    skill_dir = Path(__file__).resolve().parent.parent

    bg_path = bg_override
    if bg_path is None and data.get("background"):
        bg_path = resolve_asset_path(str(data["background"]), base_dir, skill_dir)

    scenes = data["scenes"]
    compiled_scenes: list[dict[str, Any]] = []
    cur_beat = 0.0
    sticker_cache: dict[str, Image.Image] = {}
    scene_cache: dict[str, Image.Image] = {}
    oversample_w, oversample_h = int(WIDTH * 1.14), int(HEIGHT * 1.14)

    for sc in scenes:
        beats = float(sc.get("beats", 4))
        start_t = cur_beat * beat_sec
        end_t = (cur_beat + beats) * beat_sec
        cur_beat += beats

        scene_frames: list[Image.Image] = []
        fg_frames: list[Image.Image] = []
        sticker_frames: list[Image.Image] = []

        raw_scene_list = sc.get("scene_frames") or ([sc["scene_image"]] if sc.get("scene_image") else [])
        for raw_sc in raw_scene_list:
            resolved_scene = resolve_asset_path(str(raw_sc), base_dir, skill_dir)
            s_key = str(resolved_scene.resolve())
            if s_key not in scene_cache:
                raw_scene = Image.open(resolved_scene).convert("RGBA")
                scene_cache[s_key] = _cover_resize(raw_scene, oversample_w, oversample_h)
            scene_frames.append(scene_cache[s_key])

        raw_fg_list = sc.get("fg_frames") or ([sc["fg_image"]] if sc.get("fg_image") else [])
        for raw_fg in raw_fg_list:
            resolved_fg = resolve_asset_path(str(raw_fg), base_dir, skill_dir)
            f_key = str(resolved_fg.resolve())
            if f_key not in sticker_cache:
                sticker_cache[f_key] = load_and_trim_sticker(resolved_fg)
            fg_frames.append(sticker_cache[f_key])

        if not scene_frames:
            raw_list = sc.get("frames") or [sc["sticker"]]
            for raw_s in raw_list:
                resolved = resolve_asset_path(str(raw_s), base_dir, skill_dir)
                key = str(resolved.resolve())
                if key not in sticker_cache:
                    sticker_cache[key] = load_and_trim_sticker(resolved)
                sticker_frames.append(sticker_cache[key])

        compiled_scenes.append({
            **sc,
            "start_t": start_t,
            "end_t": end_t,
            "beats": beats,
            "scene_frames": scene_frames,
            "fg_frames": fg_frames,
            "sticker_frames": sticker_frames,
        })

    total_duration = cur_beat * beat_sec
    total_frames = max(1, int(round(total_duration * fps)))
    avg_shot_sec = total_duration / max(1, len(compiled_scenes))
    print(f"Timeline: {len(compiled_scenes)} shots | {bpm:g} BPM | {total_duration:.2f}s (avg {avg_shot_sec:.2f}s/shot)")
    for idx_s, cs in enumerate(compiled_scenes, 1):
        shot_dur = cs["end_t"] - cs["start_t"]
        if shot_dur > 5.5:
            print(f"[PACE HINT] Shot {idx_s} lasts {shot_dur:.1f}s (>5.5s); consider splitting into 2 shots for sharper pacing.", file=sys.stderr)

    rng = random.Random(101)
    assets = RenderAssets(
        backdrop=build_base_backdrop(
            theme,
            bg_image_path=bg_path,
            bg_scrim_alpha=int(data.get("bg_scrim_alpha", 120)),
        ),
        warm_glow=build_warm_glow(theme, 440),
        vignette=_build_vignette(82),
        scrims={
            "top": _build_text_scrim("top"),
            "bottom": _build_text_scrim("bottom"),
        },
        bokeh_amber=_build_bokeh_orb(42, theme.accent_primary, alpha=38),
        bokeh_teal=_build_bokeh_orb(52, theme.accent_secondary, alpha=32),
        steam_puff=_build_steam_puff(),
        sunbeam=_build_sunbeam_sprite(),
        grain_tiles=_build_grain_tiles(4),
        motes=[
            (
                rng.uniform(80, WIDTH - 80),
                rng.uniform(180, 1650),
                rng.uniform(2.5, 5.5),
                rng.uniform(0.3, 0.9),
                rng.uniform(0, 2 * math.pi),
            )
            for _ in range(22)
        ],
        bokeh_seeds=[
            (
                rng.uniform(60, WIDTH - 60),
                rng.uniform(120, HEIGHT - 120),
                rng.uniform(0.4, 1.1),
                rng.uniform(0, 2 * math.pi),
                idx % 2 == 0,
            )
            for idx in range(7)
        ],
        rain_drops=[
            (
                rng.uniform(60, WIDTH - 60),
                rng.uniform(0, HEIGHT),
                rng.uniform(260, 520),
                rng.uniform(28, 62),
            )
            for _ in range(20)
        ],
    )
    font_tag = load_font(resolved_font, 28)

    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    silent_mp4 = out_prefix.parent / f"{out_prefix.name}_silent.mp4"
    preview_mp4 = out_prefix.parent / f"{out_prefix.name}_beat_preview.mp4"

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(silent_mp4),
    ]

    proc = subprocess.Popen(
        ffmpeg_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    assert proc.stdin is not None

    scene_idx = 0
    trans_duration = float(data.get("transition_sec", min(0.58, beat_sec * 0.72)))

    for f_idx in range(total_frames):
        t = f_idx / fps
        while scene_idx + 1 < len(compiled_scenes) and t >= compiled_scenes[scene_idx]["end_t"]:
            scene_idx += 1

        sc = compiled_scenes[scene_idx]
        frame = _render_scene_layer(
            sc,
            t,
            beat_sec,
            total_duration,
            assets,
            theme,
            resolved_font,
            base_font_size,
            font_tag,
            header_tag,
        )

        # Scene entry transition from previous scene
        if scene_idx > 0:
            transition = sc.get("transition", "crossfade")
            local_t = t - sc["start_t"]
            if transition != "cut" and local_t < trans_duration:
                prev_sc = compiled_scenes[scene_idx - 1]
                prev_frame = _render_scene_layer(
                    prev_sc,
                    t,
                    beat_sec,
                    total_duration,
                    assets,
                    theme,
                    resolved_font,
                    base_font_size,
                    font_tag,
                    header_tag,
                )
                frame = _apply_transition(prev_frame, frame, transition, local_t / trans_duration, theme)

        proc.stdin.write(frame.convert("RGB").tobytes())

    proc.stdin.close()
    stderr = proc.stderr.read() if proc.stderr else b""
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {stderr.decode('utf-8', errors='ignore')}")

    with tempfile.TemporaryDirectory() as tmp:
        audio_source = audio_path
        if audio_source is None:
            synth_wav = Path(tmp) / "beat_preview.wav"
            synthesize_beat_wav(synth_wav, total_duration, bpm)
            audio_source = synth_wav

        mux_cmd = [
            "ffmpeg",
            "-y",
            "-i", str(silent_mp4),
            "-i", str(audio_source),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(preview_mp4),
        ]
        res = subprocess.run(mux_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Audio mux failed: {res.stderr}")

    return silent_mp4, preview_mp4


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeline", type=Path, help="Timeline JSON file")
    parser.add_argument("--out", type=Path, help="Output file prefix")
    parser.add_argument("--fps", type=int, default=30, help="Frame rate (default: 30)")
    parser.add_argument("--font", type=str, default=None, help="Optional TTF/TTC font path")
    parser.add_argument("--audio", type=Path, default=None, help="Optional custom audio/BGM file")
    parser.add_argument("--theme", choices=sorted(THEMES.keys()), default=None, help="Override timeline theme")
    parser.add_argument("--bg", type=Path, default=None, help="Optional custom background image")
    parser.add_argument("--check", action="store_true", help="Check ffmpeg and CJK font setup and exit")
    args = parser.parse_args()

    if args.check:
        ok, font = check_environment(args.font)
        print(f"ffmpeg: {'OK' if ok else 'MISSING'}")
        print(f"cjk_font: {font or 'NOT FOUND (fallback to default)'}")
        raise SystemExit(0 if ok else 1)

    if not args.timeline or not args.out:
        parser.error("--timeline and --out are required unless --check is used")

    silent_mp4, preview_mp4 = render_video(
        args.timeline,
        args.out,
        fps=args.fps,
        font_path=args.font,
        audio_path=args.audio,
        theme_override=args.theme,
        bg_override=args.bg,
    )
    print(f"Rendered silent (Douyin-ready): {silent_mp4}")
    print(f"Rendered beat preview: {preview_mp4}")


if __name__ == "__main__":
    main()
