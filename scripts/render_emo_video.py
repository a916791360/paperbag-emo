#!/usr/bin/env python3
"""Render a beat-synced 9:16 Paperbag Emo explainer video using Pillow + FFmpeg.

No external LLM, image, or video API keys required.
Supports:
  - Cross-platform CJK font auto-detection (macOS / Windows / Linux) & FFmpeg self-check
  - Themes: late_night (charcoal-teal) and paper_cream (warm journal paper), plus --bg custom images
  - Multi-frame sprite animation ("frames" / "scene_frames") and 2.5D parallax ("fg_frames")
  - Camera push/pull ("camera"), scene transitions ("transition"), hand-drawn underlines & mood doodles
  - Beat-synced kinetic typography: typewriter_beat, beat_lines, word_pop, slam_center, fade_up

Outputs both:
  - <out>_silent.mp4 (ready for Douyin in-app music selection)
  - <out>_beat_preview.mp4 (with synthesized subtle Lo-Fi BPM pulse for beat verification)
"""

from __future__ import annotations

import argparse
import functools
import glob
import json
import math
import os
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
MAX_IMAGE_PIXELS = 4096 * 4096


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


def _platform_font_candidates(prefer_serif: bool = False) -> list[str]:
    candidates: list[str] = []
    skill_fonts = Path(__file__).resolve().parent.parent / "assets" / "fonts"
    if skill_fonts.is_dir():
        for ext in ("*.ttc", "*.ttf", "*.otf"):
            candidates.extend(sorted(str(p) for p in skill_fonts.glob(ext)))

    if sys.platform == "darwin":
        if prefer_serif:
            candidates.append("/System/Library/Fonts/Supplemental/Songti.ttc")
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
        if prefer_serif:
            candidates.append(str(win_fonts / "simsun.ttc"))
        candidates.extend([
            str(win_fonts / "msyhbd.ttc"),
            str(win_fonts / "msyh.ttc"),
            str(win_fonts / "Dengb.ttf"),
            str(win_fonts / "Deng.ttf"),
            str(win_fonts / "simhei.ttf"),
            str(win_fonts / "simsun.ttc"),
        ])
    else:
        if prefer_serif:
            candidates.extend([
                "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
                "/usr/share/fonts/noto-cjk/NotoSerifCJK-Regular.ttc",
            ])
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
                    timeout=3,
                ).strip()
                if out:
                    candidates.insert(0, out)
            except Exception:
                pass
    return candidates


def resolve_font_path(explicit_path: str | None = None, prefer_serif: bool = False) -> str | None:
    candidates = [explicit_path] if explicit_path else []
    candidates.extend(_platform_font_candidates(prefer_serif=prefer_serif))
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


@functools.lru_cache(maxsize=64)
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


def check_environment(explicit_font: str | None = None, prefer_serif: bool = False) -> tuple[bool, str | None]:
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

    font_path = resolve_font_path(explicit_font, prefer_serif=prefer_serif)
    if not font_path:
        print(
            "[WARN] No CJK font detected automatically; Chinese characters may render as boxes.\n"
            "Pass --font /path/to/font.ttc or install Noto Sans CJK / PingFang / Microsoft YaHei.",
            file=sys.stderr,
        )
    return True, font_path


@functools.lru_cache(maxsize=2)
def _build_midnight_emo_lut() -> list[int]:
    """Build 768-entry RGB S-curve LUT deepening midnight-teal shadows and warming amber highlights."""
    lut_r: list[int] = []
    lut_g: list[int] = []
    lut_b: list[int] = []
    for i in range(256):
        x = i / 255.0
        # Deeper shadow contrast S-curve (crushes flat mid-lows into rich midnight shadow)
        if x < 0.52:
            c = 0.52 * ((x / 0.52) ** 1.24)
        else:
            c = 0.52 + 0.48 * (1.0 - ((1.0 - x) / 0.48) ** 1.12)
        shadow_w = (1.0 - c) * c * 4.0  # peaks in lower midtones
        hi_w = (c ** 1.6)
        r = int(round((c * 255.0) - 7.0 * shadow_w + 8.0 * hi_w))
        g = int(round((c * 255.0) + 1.0 * shadow_w + 2.0 * hi_w))
        b = int(round((c * 255.0) + 8.0 * shadow_w - 7.0 * hi_w))
        lut_r.append(max(0, min(255, r)))
        lut_g.append(max(0, min(255, g)))
        lut_b.append(max(0, min(255, b)))
    return lut_r + lut_g + lut_b


def _apply_cinema_emo_grade(img: Image.Image) -> Image.Image:
    """Pre-bake 35mm midnight-emo color grade and warm highlight halation bloom onto a scene keyframe."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    # 1. Soft analog highlight halation bloom (computed at 1/4 resolution for speed)
    sw, sh = max(16, w // 4), max(16, h // 4)
    small = rgb.resize((sw, sh), Image.Resampling.BILINEAR)
    r_ch, g_ch, b_ch = small.split()
    # Keep bright warm pixels (>150) and tint toward warm amber-gold glow
    r_hi = r_ch.point(lambda p: max(0, min(255, int((p - 145) * 1.45))) if p > 145 else 0)
    g_hi = g_ch.point(lambda p: max(0, min(255, int((p - 150) * 1.05))) if p > 150 else 0)
    b_hi = b_ch.point(lambda p: max(0, min(255, int((p - 165) * 0.55))) if p > 165 else 0)
    a_hi = r_hi.point(lambda p: min(92, int(p * 0.42)))
    bloom_small = Image.merge("RGBA", (r_hi, g_hi, b_hi, a_hi)).filter(ImageFilter.GaussianBlur(radius=14))
    bloom = bloom_small.resize((w, h), Image.Resampling.BILINEAR)

    # 2. Apply Midnight Emo S-curve LUT
    graded_rgb = rgb.point(_build_midnight_emo_lut())
    graded_rgba = graded_rgb.convert("RGBA")
    return Image.alpha_composite(graded_rgba, bloom)


def _safe_open_rgba(path: Path, max_pixels: int = MAX_IMAGE_PIXELS) -> Image.Image:
    with Image.open(path) as raw_img:
        w, h = raw_img.size
        if w <= 0 or h <= 0 or w * h > max_pixels:
            raise ValueError(f"Invalid or oversized image ({w}x{h}) at {path}")
        return raw_img.convert("RGBA")


def _cover_resize(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    src_w, src_h = img.size
    if src_w <= 0 or src_h <= 0:
        raise ValueError(f"Invalid image dimensions: {src_w}x{src_h}")
    scale = max(target_w / src_w, target_h / src_h)
    new_w = max(1, int(round(src_w * scale)))
    new_h = max(1, int(round(src_h * scale)))
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = max(0, (new_w - target_w) // 2)
    top = max(0, (new_h - target_h) // 2)
    return resized.crop((left, top, left + target_w, top + target_h))


def build_base_backdrop(
    theme: ThemePalette,
    bg_image_path: Path | None = None,
    bg_scrim_alpha: int = 120,
    seed: int = 42,
) -> Image.Image:
    """Pre-bake backdrop (theme gradient or custom image), paper grain, and desk horizon."""
    if bg_image_path is not None:
        raw_bg = _safe_open_rgba(bg_image_path)
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
            gdraw.line([(86, 90), (86, HEIGHT - 90)], fill=(198, 130, 108, 45), width=2)
            img = Image.alpha_composite(img, grid)

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
    img = _safe_open_rgba(path)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    w, h = img.size
    if w <= 0 or h <= 0:
        raise ValueError(f"Sticker image is empty after trim: {path}")
    scale = min(target_max_w / w, target_max_h / h)
    new_size = (max(1, int(round(w * scale))), max(1, int(round(h * scale))))
    return img.resize(new_size, Image.Resampling.LANCZOS)


def resolve_asset_path(
    raw: str,
    base_dir: Path,
    skill_dir: Path,
    allow_external: bool = False,
) -> Path:
    if not raw or not str(raw).strip():
        raise ValueError("Empty asset path in timeline")
    raw_path = Path(str(raw))
    allowed_roots = [base_dir.resolve(), skill_dir.resolve()]

    candidates: list[Path] = []
    if raw_path.is_absolute():
        candidates.append(raw_path)
    else:
        candidates.extend([base_dir / raw_path, skill_dir / raw_path, raw_path])

    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except Exception:
            continue
        if not allow_external and not any(resolved.is_relative_to(root) for root in allowed_roots):
            raise ValueError(f"Asset path escapes allowed workspace roots: {raw}")
        if resolved.is_file():
            return resolved
    raise FileNotFoundError(f"Asset not found: {raw}")


def _parse_pos_pair(raw: Any, default: tuple[float, float], field_name: str = "pos") -> tuple[float, float]:
    if raw is None or raw == "auto":
        return default
    if not isinstance(raw, (list, tuple)) or len(raw) != 2:
        raise ValueError(f"Field '{field_name}' must be a [x_ratio, y_ratio] pair or 'auto', got: {raw!r}")
    try:
        x = float(raw[0])
        y = float(raw[1])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Field '{field_name}' contains non-numeric coordinates: {raw!r}") from exc
    if not (math.isfinite(x) and math.isfinite(y)):
        raise ValueError(f"Field '{field_name}' contains non-finite coordinates: {raw!r}")
    return max(-0.5, min(1.5, x)), max(-0.5, min(1.5, y))


def _parse_crop_box(raw: Any, field_name: str = "crop_box") -> tuple[float, float, float, float] | None:
    if raw is None:
        return None
    if not isinstance(raw, (list, tuple)) or len(raw) != 4:
        raise ValueError(f"Field '{field_name}' must be [x0, y0, x1, y1] in [0, 1], got: {raw!r}")
    try:
        x0, y0, x1, y1 = (float(v) for v in raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Field '{field_name}' contains non-numeric coordinates: {raw!r}") from exc
    if not (all(math.isfinite(v) for v in (x0, y0, x1, y1)) and 0.0 <= x0 < x1 <= 1.0 and 0.0 <= y0 < y1 <= 1.0):
        raise ValueError(f"Field '{field_name}' must satisfy 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1, got: {raw!r}")
    return x0, y0, x1, y1


def _detect_warm_light_anchor(
    img: Image.Image,
    default: tuple[float, float] = (0.5, 0.55),
) -> tuple[float, float]:
    """Automatically detect the brightest warm light centroid (streetlamp, phone screen, candle) in a scene."""
    grid = 64
    small = img.convert("RGB").resize((grid, grid), Image.Resampling.BILINEAR)
    px = small.load()
    assert px is not None
    total_w = 0.0
    sum_x = 0.0
    sum_y = 0.0
    for gy in range(int(grid * 0.20), int(grid * 0.92)):
        for gx in range(int(grid * 0.06), int(grid * 0.94)):
            r, g, b = px[gx, gy]
            warmth = max(0, r - b) + max(0, g - b) * 0.5
            luma = 0.35 * r + 0.45 * g + 0.20 * b
            if r > 125 and warmth > 28 and luma > 105:
                weight = ((warmth / 255.0) ** 1.6) * ((luma / 255.0) ** 2.0)
                total_w += weight
                sum_x += (gx + 0.5) / grid * weight
                sum_y += (gy + 0.5) / grid * weight
    if total_w <= 1e-4:
        return default
    return round(sum_x / total_w, 3), round(sum_y / total_w, 3)


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
        # Soft warm halation aura under the brush stroke
        draw.line(pts_main, fill=(*color, int(alpha * 0.24)), width=11, joint="curve")
        draw.line(pts_main, fill=(*color, int(alpha * 0.94)), width=5, joint="curve")
    if len(pts_sub) >= 2 and progress > 0.25:
        draw.line(pts_sub, fill=(*color, int(alpha * 0.44)), width=2, joint="curve")


def _is_inside_highlight(text: str, cut_idx: int, highlights: list[str] | None) -> bool:
    if not highlights:
        return False
    for kw in highlights:
        if not kw:
            continue
        start = 0
        while True:
            pos = text.find(kw, start)
            if pos == -1:
                break
            if pos < cut_idx < pos + len(kw):
                return True
            start = pos + 1
    return False


def _wrap_cjk_lines(
    lines: list[str],
    max_chars: int = 14,
    highlights: list[str] | None = None,
) -> list[str]:
    """Safely wrap overly long copy lines at Chinese punctuation or midpoint without infinite loops."""
    max_chars = max(4, int(max_chars))
    wrapped: list[str] = []
    punc = set("，。！？、；：… ")

    for raw in lines:
        if not isinstance(raw, str):
            raw = str(raw)
        s = raw.strip()
        if not s:
            continue
        effective = len(s.replace(" ", "").replace(".", ""))
        if effective <= max_chars or len(s) <= max_chars + 2:
            wrapped.append(raw)
            continue

        pending = s
        while len(pending.replace(" ", "").replace(".", "")) > max_chars and len(pending) > 1:
            mid = max(1, min(len(pending) - 1, len(pending) // 2))
            best_split = None
            best_score = 10**9
            lo = max(1, mid - 6)
            hi = min(len(pending) - 1, mid + 7)
            for idx in range(lo, hi):
                if pending[idx] in punc and idx + 1 < len(pending):
                    cand = idx + 1
                    penalty = 100 if _is_inside_highlight(pending, cand, highlights) else 0
                    score = abs(idx - mid) + penalty
                    if score < best_score:
                        best_score = score
                        best_split = cand

            if best_split is None:
                # Choose cut near mid that avoids splitting inside a highlight keyword
                best_split = mid
                for offset in range(0, 6):
                    for cand in (mid - offset, mid + offset):
                        if 1 <= cand < len(pending) and not _is_inside_highlight(pending, cand, highlights):
                            best_split = cand
                            break
                    else:
                        continue
                    break

            cut = max(1, min(len(pending) - 1, best_split))
            left = pending[:cut].rstrip()
            right = pending[cut:].lstrip()
            if not left or not right or len(right) >= len(pending):
                hard_cut = max(1, min(len(pending) - 1, max_chars))
                wrapped.append(pending[:hard_cut])
                pending = pending[hard_cut:]
                continue
            wrapped.append(left)
            pending = right
        if pending:
            wrapped.append(pending)
    return wrapped


def _validate_timeline_pacing(compiled_scenes: list[dict[str, Any]], bpm: float) -> list[str]:
    """Check shot duration, reading speed (chars/sec), visual diversity, and highlight integrity."""
    warnings: list[str] = []
    beat_sec = 60.0 / bpm
    prev_sig: tuple[str, str] | None = None

    for idx_s, cs in enumerate(compiled_scenes, 1):
        shot_dur = cs["end_t"] - cs["start_t"]
        lines = cs.get("lines", [])
        chars = sum(len(ln.replace(" ", "").replace(".", "")) for ln in lines)
        cps = chars / max(0.1, shot_dur)

        if shot_dur > 5.5:
            warnings.append(
                f"[PACE HINT] Shot {idx_s} lasts {shot_dur:.1f}s (>5.5s); split into 2 shots for sharper rhythm."
            )
        if cps > 5.5:
            need_beats = max(2, math.ceil((chars / 3.8 + 0.8) / beat_sec))
            warnings.append(
                f"[READABILITY HINT] Shot {idx_s} has {chars} chars in {shot_dur:.1f}s ({cps:.1f} chars/s); consider >= {need_beats} beats."
            )

        for kw in cs.get("highlight", []) or []:
            if kw and not any(kw in ln for ln in lines):
                warnings.append(
                    f"[HIGHLIGHT HINT] Shot {idx_s} highlight '{kw}' not found in wrapped lines {lines}."
                )

        vis_src = str(
            cs.get("_vis_src")
            or cs.get("scene_image")
            or (cs.get("scene_frames") or [None])[0]
            or cs.get("sticker")
            or (cs.get("frames") or [""])[0]
        )
        cur_sig = (vis_src, str(cs.get("camera", "static")))
        if prev_sig is not None and cur_sig == prev_sig:
            warnings.append(
                f"[DIVERSITY HINT] Shot {idx_s} repeats the same visual & camera as Shot {idx_s - 1}; vary shot scale or motion."
            )
        prev_sig = cur_sig
    return warnings


def _fit_font_for_line(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_path: str | None,
    base_size: int,
    max_width: int = WIDTH - 140,
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    size = max(34, int(base_size))
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
    show_underline: bool = True,
    letter_spacing: int = 4,
    line_elapsed: float | None = None,
    char_step_sec: float = 0.042,
    char_fade_sec: float = 0.32,
    anim_style: str = "beat_lines",
    t: float = 0.0,
    beat_pulse: float = 0.0,
) -> None:
    if alpha <= 0 or visible_chars <= 0 or not text:
        return

    eff_spacing = max(0, int(letter_spacing))
    font = _fit_font_for_line(
        draw,
        text,
        font_path,
        base_font_size,
        max_width=WIDTH - 140 - max(0, len(text) - 1) * eff_spacing,
    )
    char_widths = [
        draw.textbbox((0, 0), ch, font=font)[2] - draw.textbbox((0, 0), ch, font=font)[0]
        for ch in text
    ]
    total_w = sum(char_widths) + max(0, len(text) - 1) * eff_spacing
    start_x = center_x - total_w // 2

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
    ascent, descent = font.getmetrics() if hasattr(font, "getmetrics") else (50, 12)
    underline_y = y + ascent + max(10, descent // 2)

    cur_x = start_x
    hi_span_start: int | None = None
    hi_span_last_idx: int = 0

    for c_idx, (ch, is_hi) in enumerate(zip(visible_text, hi_mask[:visible_chars])):
        cw = char_widths[c_idx]

        # Per-character kinetic entrance & continuous heartbeat breathing
        if line_elapsed is not None:
            c_dt = line_elapsed - c_idx * char_step_sec
            if c_dt <= 0.0:
                cur_x += cw + eff_spacing
                continue
            raw_p = min(1.0, c_dt / max(0.05, char_fade_sec))
            if anim_style in ("word_pop", "slam_center"):
                char_p = ease_out_back(raw_p)
                alpha_p = ease_out_cubic(min(1.0, c_dt / max(0.05, char_fade_sec * 0.65)))
                ent_dy = int(round((1.0 - char_p) * 26.0))
            elif anim_style == "typewriter_beat":
                char_p = ease_out_cubic(raw_p)
                alpha_p = char_p
                ent_dy = int(round((1.0 - char_p) * 18.0))
            else:
                char_p = ease_out_cubic(raw_p)
                alpha_p = char_p
                ent_dy = int(round((1.0 - char_p) * 22.0))

            char_alpha = max(0, min(255, int(round(alpha * alpha_p))))
            # Subtle continuous 80 BPM wave float so settled text never freezes into a dead static image
            idle_dy = int(round(2.4 * math.sin(t * 2.2 - c_idx * 0.24 + line_seed * 0.7)))
            hi_pop_dy = 0
            if is_hi:
                # Emotional accent lift when the highlight keyword lights up + heartbeat pulse
                hi_wave = math.sin(min(1.0, c_dt / 0.45) * math.pi)
                hi_pop_dy = -int(round(5.0 * hi_wave + 2.2 * beat_pulse))
            cy = y + ent_dy + idle_dy + hi_pop_dy
        else:
            char_alpha = alpha
            cy = y

        if char_alpha <= 2:
            cur_x += cw + eff_spacing
            continue

        # Highlight warm amber aura glow
        if is_hi:
            glow_a = max(0, min(140, int(char_alpha * (0.16 + 0.14 * beat_pulse))))
            for gx, gy in ((-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2)):
                draw.text((cur_x + gx, cy + gy), ch, font=font, fill=(*theme.accent_primary, glow_a))

        shadow_alpha = max(0, min(240, int(char_alpha * min(0.92, theme.text_shadow_alpha + 0.25))))
        for ox, oy in ((0, 2), (2, 3), (-1, 2), (0, -1)):
            draw.text((cur_x + ox, cy + oy), ch, font=font, fill=(*theme.text_shadow, shadow_alpha))

        color = (*theme.accent_primary, char_alpha) if is_hi else (*theme.text_primary, char_alpha)
        draw.text(
            (cur_x, cy),
            ch,
            font=font,
            fill=color,
            stroke_width=1 if is_hi else 0,
            stroke_fill=(*theme.accent_primary, max(0, int(char_alpha * 0.45))) if is_hi else None,
        )

        if is_hi and hi_span_start is None:
            hi_span_start = cur_x
        if is_hi:
            hi_span_last_idx = c_idx

        is_last_hi = is_hi and (c_idx + 1 == len(visible_text) or not hi_mask[c_idx + 1])
        if is_last_hi and hi_span_start is not None and show_underline:
            if line_elapsed is not None:
                span_ready_t = hi_span_last_idx * char_step_sec + char_fade_sec * 0.35
                span_ul_prog = ease_out_cubic(max(0.0, min(1.0, (line_elapsed - span_ready_t) / 0.48)))
            else:
                span_ul_prog = underline_progress
            if span_ul_prog > 0.01:
                _draw_hand_underline(
                    draw,
                    hi_span_start,
                    cur_x + cw,
                    underline_y + (cy - y),
                    span_ul_prog,
                    theme.accent_primary,
                    char_alpha,
                    seed=line_seed * 13 + c_idx,
                )
            hi_span_start = None
        elif not is_hi:
            hi_span_start = None

        cur_x += cw + eff_spacing


def draw_mood_doodles(
    draw: ImageDraw.ImageDraw,
    doodles: list[str],
    t: float,
    local_beat: float,
    beat_pulse: float,
    sticker_box: tuple[int, int, int, int],
    theme: ThemePalette,
) -> None:
    """Draw editorial manga-ink doodles around the character or upper frame onto an existing ImageDraw."""
    if not doodles:
        return
    sx, sy, sw, sh = sticker_box
    ink = theme.text_primary if theme.name == "paper_cream" else (232, 228, 220)
    amber = theme.accent_primary
    teal = theme.accent_secondary

    for kind in doodles:
        if kind == "thought_dots":
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
    if duration_sec <= 0 or bpm <= 0:
        raise ValueError(f"Invalid duration ({duration_sec}) or BPM ({bpm})")
    total_samples = max(1, int(duration_sec * sample_rate))
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
    if not frames:
        raise ValueError("Empty frame list in scene")
    if len(frames) == 1:
        return frames[0]
    mode = sc.get("frame_mode", "pingpong")
    if mode == "natural_blink":
        cycle_sec = max(0.25, float(sc.get("blink_interval", 2.5)))
        phase = (local_t + 0.6) % cycle_sec
        return frames[1] if phase < 0.16 else frames[0]
    if mode == "beat_toggle":
        beats_per = max(0.25, float(sc.get("beats_per_frame", 1.0)))
        idx = int(local_beat / beats_per) % len(frames)
        return frames[idx]
    fps_anim = max(0.1, float(sc.get("frame_fps", 4.0)))
    step = int(local_t * fps_anim)
    if mode == "pingpong" and len(frames) > 2:
        cycle = len(frames) * 2 - 2
        pos = step % cycle
        idx = pos if pos < len(frames) else cycle - pos
        return frames[idx]
    return frames[step % len(frames)]


def _build_text_scrim(text_pos: str, theme: ThemePalette) -> Image.Image:
    """Create a theme-aware subtle gradient scrim behind subtitles for full-frame illustrations."""
    scrim = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scrim)
    base_col = (244, 238, 226) if theme.name == "paper_cream" else (10, 14, 18)
    max_a_bot = 205 if theme.name == "paper_cream" else 175
    max_a_top = 190 if theme.name == "paper_cream" else 155
    if text_pos == "bottom":
        y0, y1 = 1240, HEIGHT
        for y in range(y0, y1):
            frac = (y - y0) / (y1 - y0)
            alpha = int(max_a_bot * (frac ** 1.3))
            draw.line([(0, y), (WIDTH, y)], fill=(*base_col, alpha))
    else:
        y0, y1 = 0, 740
        for y in range(y0, y1):
            frac = 1.0 - (y - y0) / (y1 - y0)
            alpha = int(max_a_top * (frac ** 1.35))
            draw.line([(0, y), (WIDTH, y)], fill=(*base_col, alpha))
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
    draw.polygon([(WIDTH - 40, 0), (WIDTH, 420), (340, HEIGHT), (60, HEIGHT)], fill=(255, 214, 146, 26))
    draw.polygon([(WIDTH - 140, 0), (WIDTH - 20, 200), (140, HEIGHT - 180), (-60, HEIGHT - 360)], fill=(255, 224, 168, 20))
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
    overlay_draw: ImageDraw.ImageDraw,
    sc: dict[str, Any],
    assets: RenderAssets,
    t: float,
    beat_pulse: float,
    theme: ThemePalette,
) -> Image.Image:
    """Apply sprite-based fx onto stage and vector-based fx onto the shared overlay_draw."""
    raw_fx = sc.get("fx", [])
    fx_list = [raw_fx] if isinstance(raw_fx, str) else list(raw_fx)
    if not fx_list:
        return stage

    for fx in fx_list:
        if fx == "coffee_steam":
            pos = _parse_pos_pair(sc.get("steam_pos"), (0.52, 0.62), "steam_pos")
            sx0 = int(WIDTH * pos[0])
            sy0 = int(HEIGHT * pos[1])
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
            offset_x = int(28 * math.sin(t * 0.55))
            stage.alpha_composite(assets.sunbeam, (offset_x, 0))

        elif fx == "bokeh_depth":
            for bx0, by0, speed, phase, is_amber in assets.bokeh_seeds:
                orb = assets.bokeh_amber if is_amber else assets.bokeh_teal
                bx = int((bx0 + 65 * math.sin(t * speed * 0.7 + phase)) % (WIDTH + 120)) - 60
                by = int((by0 - t * 48 * speed) % (HEIGHT + 120)) - 60
                stage.alpha_composite(orb, (bx - orb.width // 2, by - orb.height // 2))

        elif fx == "rain_glass":
            for rx0, ry0, rspeed, rlen in assets.rain_drops:
                ry = (ry0 + t * rspeed) % (HEIGHT - 120)
                overlay_draw.line([(rx0, ry), (rx0 - 5, ry + rlen)], fill=(176, 212, 220, 52), width=2)
                overlay_draw.ellipse([rx0 - 8, ry + rlen - 3, rx0 - 2, ry + rlen + 3], fill=(215, 236, 240, 72))

        elif fx == "cat_zzz":
            pos = _parse_pos_pair(sc.get("cat_pos"), (0.74, 0.72), "cat_pos")
            cx0 = int(WIDTH * pos[0])
            cy0 = int(HEIGHT * pos[1])
            ink_col = theme.text_primary if theme.name == "paper_cream" else (232, 236, 238)
            for idx in range(3):
                life = (t * 0.45 + idx / 3.0) % 1.0
                zx = cx0 + idx * 18 + int(14 * math.sin(life * 4.5 + idx))
                zy = cy0 - int(life * 120)
                sz = 16 + idx * 5
                alpha = int(205 * math.sin(math.pi * life))
                if alpha > 8:
                    pts = [(zx, zy), (zx + sz, zy), (zx, zy + sz), (zx + sz, zy + sz)]
                    overlay_draw.line(pts, fill=(*ink_col, alpha), width=3, joint="curve")

        elif fx == "purr_waves":
            pos = _parse_pos_pair(sc.get("cat_pos"), (0.70, 0.62), "cat_pos")
            cx0 = int(WIDTH * pos[0])
            cy0 = int(HEIGHT * pos[1])
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
                overlay_draw.line(pts, fill=(*theme.accent_primary, alpha), width=3, joint="curve")

        elif fx == "prop_pulse":
            pos = _parse_pos_pair(sc.get("prop_pos"), (0.70, 0.56), "prop_pos")
            px0 = int(WIDTH * pos[0])
            py0 = int(HEIGHT * pos[1])
            p_color = sc.get("prop_color", "teal")
            base_orb = assets.bokeh_amber if p_color == "amber" else assets.bokeh_teal
            pulse = 0.55 + 0.45 * math.sin(t * 2.2) + 0.25 * beat_pulse
            scale = 1.6 + 0.5 * pulse
            pw = max(32, int(base_orb.width * scale))
            ph = max(32, int(base_orb.height * scale))
            orb = base_orb.resize((pw, ph), Image.Resampling.BILINEAR)
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


def _render_visual_stage(
    sc: dict[str, Any],
    t: float,
    beat_sec: float,
    assets: RenderAssets,
    theme: ThemePalette,
) -> Image.Image:
    """Render ONLY the visual stage layer (background, camera motion, 2.5D parallax, FX, doodles, vignette, scrim)."""
    local_t = max(0.0, t - sc["start_t"])
    scene_dur = max(0.01, sc["end_t"] - sc["start_t"])
    scene_prog = min(1.0, local_t / scene_dur)
    local_beat = local_t / beat_sec
    beat_phase = (t / beat_sec) % 1.0
    beat_pulse = math.exp(-7.0 * beat_phase)
    cam = sc.get("camera", "static")

    scene_frames: list[Image.Image] = sc.get("scene_frames", [])
    is_full_frame = len(scene_frames) > 0
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

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

        fg_frames: list[Image.Image] = sc.get("fg_frames", [])
        if fg_frames:
            fg_raw = _pick_frame_from_list(fg_frames, sc, local_t, local_beat)
            fg_motion = sc.get("motion", "alive_idle")
            fg_base_scale = max(0.1, float(sc.get("fg_scale", 1.0)))
            fg_parallax_px = float(sc.get("fg_parallax", 1.45))
            fg_scale_mult = fg_base_scale * (1.0 + (zoom - 1.0) * fg_parallax_px)
            cur_fg = _transform_sticker(fg_raw, fg_motion, local_t, local_beat, beat_sec, beat_pulse)
            if abs(fg_scale_mult - 1.0) > 0.002:
                fw = max(1, int(round(cur_fg.width * fg_scale_mult)))
                fh = max(1, int(round(cur_fg.height * fg_scale_mult)))
                cur_fg = cur_fg.resize((fw, fh), Image.Resampling.BILINEAR)
            fg_dx = int(-pan_x * 36 * fg_parallax_px + breath_dx * 1.35 + float(sc.get("fg_offset_x", 0)))
            fg_dy = int(_sticker_dy(fg_motion, local_t, local_beat, beat_sec, beat_pulse) - pan_y * 28 * fg_parallax_px + breath_dy * 1.35)
            fx = WIDTH // 2 - cur_fg.width // 2 + fg_dx
            fy = int(sc.get("fg_bottom_y", 1710)) - cur_fg.height + fg_dy
            stage.alpha_composite(cur_fg, (fx, fy))

        if sc.get("light_pos") is not None:
            lpos = _parse_pos_pair(sc.get("light_pos"), (0.5, 0.5), "light_pos")
            flicker = 0.0
            if "lamp_flicker" in (sc.get("fx") or []):
                flicker = 0.08 * math.sin(t * 11.3) * math.cos(t * 4.7)
            glow_scale = 0.92 + 0.14 * (0.5 + 0.5 * math.sin(t * 1.7)) + 0.06 * beat_pulse + flicker
            gw = max(64, int(assets.warm_glow.width * glow_scale))
            gh = max(64, int(assets.warm_glow.height * glow_scale))
            glow_resized = assets.warm_glow.resize((gw, gh), Image.Resampling.BILINEAR)
            lx = int(WIDTH * lpos[0]) - gw // 2
            ly = int(HEIGHT * lpos[1]) - gh // 2
            stage.alpha_composite(glow_resized, (lx, ly))

        for mx0, my0, mr, mspeed, mphase in assets.motes:
            mx = mx0 + 22.0 * math.sin(t * mspeed + mphase)
            my = (my0 - t * 22.0 * mspeed) % (HEIGHT - 120)
            malpha = int(38 + 32 * math.sin(t * 1.4 + mphase) + 22 * beat_pulse)
            odraw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(*theme.mote_color, max(8, min(125, malpha))))

        stage = _apply_sensory_fx(stage, odraw, sc, assets, t, beat_pulse, theme)

        raw_doodles = sc.get("doodle", [])
        doodles = [raw_doodles] if isinstance(raw_doodles, str) else list(raw_doodles)
        if doodles:
            draw_mood_doodles(odraw, doodles, t, local_beat, beat_pulse, (140, 640, 800, 1000), theme)

        stage = Image.alpha_composite(stage, overlay)
        stage = Image.alpha_composite(stage, assets.vignette)
        text_pos = sc.get("text_pos", "top")
        if text_pos in assets.scrims:
            stage = Image.alpha_composite(stage, assets.scrims[text_pos])
    else:
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

        for mx0, my0, mr, mspeed, mphase in assets.motes:
            mx = mx0 + 18.0 * math.sin(t * mspeed + mphase)
            my = (my0 - t * 18.0 * mspeed) % 1620
            malpha = int(42 + 34 * math.sin(t * 1.4 + mphase) + 28 * beat_pulse)
            odraw.ellipse(
                [mx - mr, my - mr, mx + mr, my + mr],
                fill=(*theme.mote_color, max(10, min(140, malpha))),
            )

        sticker = _pick_frame_from_list(sc["sticker_frames"], sc, local_t, local_beat)
        motion = sc.get("motion", "alive_idle")
        cur_sticker = _transform_sticker(sticker, motion, local_t, local_beat, beat_sec, beat_pulse)
        dy = _sticker_dy(motion, local_t, local_beat, beat_sec, beat_pulse)

        paste_x = int(WIDTH // 2 - cur_sticker.width // 2)
        paste_y = int(HORIZON_Y - cur_sticker.height + dy)
        stage.alpha_composite(cur_sticker, (paste_x, paste_y))

        stage = _apply_sensory_fx(stage, odraw, sc, assets, t, beat_pulse, theme)

        raw_doodles = sc.get("doodle", [])
        doodles = [raw_doodles] if isinstance(raw_doodles, str) else list(raw_doodles)
        if doodles:
            draw_mood_doodles(
                odraw,
                doodles,
                t,
                local_beat,
                beat_pulse,
                (paste_x, paste_y, cur_sticker.width, cur_sticker.height),
                theme,
            )

        stage = Image.alpha_composite(stage, overlay)

        if abs(cam_scale - 1.0) > 0.0005 or abs(cam_dy) > 0.5:
            zw = int(round(WIDTH * cam_scale))
            zh = int(round(HEIGHT * cam_scale))
            zoomed = stage.resize((zw, zh), Image.Resampling.BILINEAR)
            crop_x = (zw - WIDTH) // 2
            crop_y = max(0, min(zh - HEIGHT, (zh - HEIGHT) // 2 + int(round(cam_dy))))
            stage = zoomed.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))

    return stage


def _render_typography_layer(
    sc: dict[str, Any],
    t: float,
    beat_sec: float,
    total_duration: float,
    theme: ThemePalette,
    font_path: str | None,
    base_font_size: int,
    font_tag: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    header_tag: str,
    trans_offset: float = 0.0,
) -> Image.Image:
    """Render kinetic typography and optional HUD onto a decoupled RGBA layer (never smeared by visual transitions)."""
    local_t = max(0.0, t - sc["start_t"])
    scene_dur = max(0.01, sc["end_t"] - sc["start_t"])
    remain_t = max(0.0, sc["end_t"] - t)
    beat_phase = (t / beat_sec) % 1.0
    beat_pulse = math.exp(-7.0 * beat_phase)
    is_full_frame = len(sc.get("scene_frames", [])) > 0

    text_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(text_layer)
    text_theme_name = sc.get("text_theme", theme.name)
    text_theme = THEMES.get(text_theme_name, theme)
    is_cinema_emo = bool(sc.get("_cinema_emo", True))
    hud_mode = str(sc.get("hud", "none" if is_cinema_emo else "full"))
    show_underline = bool(sc.get("underline", True))
    letter_spacing = int(sc.get("letter_spacing", 4 if is_cinema_emo else 0))

    # Pre-transition exit fade so old subtitle cleanly exits before next shot's transition
    exit_window = min(0.32, scene_dur * 0.14)
    if not sc.get("_is_last_scene", False) and remain_t < exit_window:
        exit_prog = ease_in_out_sine(max(0.0, min(1.0, remain_t / max(0.01, exit_window))))
    else:
        exit_prog = 1.0
    exit_dy = -int(round((1.0 - exit_prog) * 12.0))

    if hud_mode == "full":
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

    # Post-transition entrance clock: wait until visual transition passes trans_offset
    text_t = local_t - trans_offset
    if text_t >= 0.0 and exit_prog > 0.01:
        text_beat = text_t / beat_sec
        ts_label = sc.get("timestamp")
        if ts_label and hud_mode in ("full", "minimal"):
            ts_alpha = int(165 * min(1.0, text_t / 0.35) * exit_prog)
            if ts_alpha > 4:
                ts_font = load_font(font_path, 23)
                ts_box = tdraw.textbbox((0, 0), str(ts_label), font=ts_font)
                ts_w = ts_box[2] - ts_box[0]
                ts_y = 212 if hud_mode == "full" else 235
                tdraw.text((WIDTH // 2 - ts_w // 2, ts_y + exit_dy), str(ts_label), font=ts_font, fill=(*text_theme.accent_primary, ts_alpha))

        lines: list[str] = sc.get("lines", [])
        highlights: list[str] = sc.get("highlight", [])
        text_anim = sc.get("text_anim", "beat_lines")
        line_spacing = 104 if is_cinema_emo else 108
        text_pos = sc.get("text_pos", "top")
        if text_pos == "bottom":
            anchor_y = 1520
        elif text_pos == "center":
            anchor_y = 940
        else:
            anchor_y = 395 if is_cinema_emo else (430 if is_full_frame else 490)
        base_text_y = anchor_y - (len(lines) * line_spacing) // 2 + exit_dy

        eff_beats = max(1.5, (scene_dur - trans_offset) / beat_sec)
        if text_anim == "typewriter_beat":
            total_chars = max(1, sum(len(s) for s in lines))
            reveal_sec = max(0.85, min((scene_dur - trans_offset) * 0.56, total_chars * 0.095))
            char_step = reveal_sec / max(1, total_chars)
            consumed = 0
            for idx_l, line_str in enumerate(lines):
                line_start_t = consumed * char_step
                consumed += len(line_str)
                if text_t < line_start_t:
                    continue
                draw_highlighted_line(
                    tdraw,
                    line_str,
                    len(line_str),
                    highlights,
                    font_path,
                    base_font_size,
                    WIDTH // 2,
                    base_text_y + idx_l * line_spacing,
                    int(255 * exit_prog),
                    1.0,
                    text_theme,
                    line_seed=idx_l + 1,
                    show_underline=show_underline,
                    letter_spacing=letter_spacing,
                    line_elapsed=text_t - line_start_t,
                    char_step_sec=char_step,
                    char_fade_sec=0.24,
                    anim_style="typewriter_beat",
                    t=t,
                    beat_pulse=beat_pulse,
                )
        else:
            for idx_l, line_str in enumerate(lines):
                if text_anim in ("beat_lines", "fade_up"):
                    slot_beats = max(0.85, round((eff_beats * 0.62) / max(1, len(lines)) * 2.0) / 2.0) if len(lines) > 1 else 0.0
                    appear_t = idx_l * slot_beats * beat_sec
                    c_step = 0.044
                    c_fade = 0.34
                elif text_anim == "word_pop":
                    appear_t = idx_l * 0.85 * beat_sec
                    c_step = 0.036
                    c_fade = 0.30
                else:  # slam_center
                    appear_t = idx_l * 0.70 * beat_sec
                    c_step = 0.030
                    c_fade = 0.28

                if text_t < appear_t:
                    continue

                draw_highlighted_line(
                    tdraw,
                    line_str,
                    len(line_str),
                    highlights,
                    font_path,
                    base_font_size,
                    WIDTH // 2,
                    base_text_y + idx_l * line_spacing,
                    int(255 * exit_prog),
                    1.0,
                    text_theme,
                    line_seed=idx_l + 1,
                    show_underline=show_underline,
                    letter_spacing=letter_spacing,
                    line_elapsed=text_t - appear_t,
                    char_step_sec=c_step,
                    char_fade_sec=c_fade,
                    anim_style=text_anim,
                    t=t,
                    beat_pulse=beat_pulse,
                )

    if hud_mode in ("full", "minimal"):
        cur_measure_beat = int(t / beat_sec) % 4
        dot_gap = 28
        dots_start_x = WIDTH // 2 - (3 * dot_gap) // 2
        for bi in range(4):
            cx = dots_start_x + bi * dot_gap
            cy = 1765
            is_cur = (bi == cur_measure_beat)
            r = 5 if is_cur else 3
            active_a = int((155 if hud_mode == "minimal" else 190) + 55 * beat_pulse)
            idle_a = 55 if hud_mode == "minimal" else 90
            col = (*text_theme.accent_primary, active_a) if is_cur else (*text_theme.muted_ui, idle_a)
            tdraw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

    return text_layer


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
    stage = _render_visual_stage(sc, t, beat_sec, assets, theme)
    text_layer = _render_typography_layer(
        sc,
        t,
        beat_sec,
        total_duration,
        theme,
        font_path,
        base_font_size,
        font_tag,
        header_tag,
        trans_offset=0.0,
    )
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


def compile_timeline(
    data: Any,
    base_dir: Path,
    skill_dir: Path,
    theme_override: str | None = None,
    bg_override: Path | None = None,
    load_images: bool = False,
) -> tuple[float, ThemePalette, Path | None, list[dict[str, Any]]]:
    """Validate timeline schema and resolve all scene assets (shared by --validate and render_video)."""
    if not isinstance(data, dict):
        raise ValueError("Timeline JSON root must be an object")

    try:
        bpm = float(data.get("bpm", 84))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid BPM value: {data.get('bpm')!r}") from exc
    if not (math.isfinite(bpm) and 10.0 <= bpm <= 300.0):
        raise ValueError(f"BPM must be between 10 and 300, got: {bpm}")

    theme_name = theme_override or data.get("theme", "late_night")
    if theme_name not in THEMES:
        raise ValueError(f"Unknown theme '{theme_name}'. Choose from: {', '.join(THEMES)}")
    theme = THEMES[theme_name]

    bg_path = bg_override
    if bg_path is not None:
        if not bg_path.is_file():
            raise FileNotFoundError(f"Custom background not found: {bg_path}")
    elif data.get("background"):
        bg_path = resolve_asset_path(str(data["background"]), base_dir, skill_dir)

    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("Timeline 'scenes' must be a non-empty list")

    beat_sec = 60.0 / bpm
    cur_beat = 0.0
    compiled_scenes: list[dict[str, Any]] = []
    sticker_cache: dict[str, Image.Image] = {}
    scene_cache: dict[str, Image.Image] = {}
    oversample_w, oversample_h = int(WIDTH * 1.14), int(HEIGHT * 1.14)
    default_max_chars = max(4, int(data.get("max_chars_per_line", 14)))
    is_cinema_emo = str(data.get("style", "cinema_emo")) == "cinema_emo"
    default_grade = str(data.get("color_grade", "midnight_emo" if is_cinema_emo else "none"))
    default_hud = str(data.get("hud", "none" if is_cinema_emo else "full"))
    default_underline = bool(data.get("underline", True))
    default_spacing = int(data.get("letter_spacing", 4 if is_cinema_emo else 0))

    for idx_s, sc in enumerate(scenes, 1):
        if not isinstance(sc, dict):
            raise ValueError(f"Scene {idx_s} must be a JSON object")
        try:
            beats = float(sc.get("beats", 4))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Scene {idx_s} has invalid 'beats': {sc.get('beats')!r}") from exc
        if not (math.isfinite(beats) and 0.25 <= beats <= 120.0):
            raise ValueError(f"Scene {idx_s} 'beats' must be in [0.25, 120], got: {beats}")

        # Validate optional coordinate pairs and crop_box upfront
        for pos_field, pos_def in (
            ("light_pos", (0.5, 0.5)),
            ("steam_pos", (0.52, 0.62)),
            ("cat_pos", (0.74, 0.72)),
            ("prop_pos", (0.70, 0.56)),
        ):
            if sc.get(pos_field) is not None:
                _parse_pos_pair(sc.get(pos_field), pos_def, f"scenes[{idx_s}].{pos_field}")

        crop_box = _parse_crop_box(sc.get("crop_box"), f"scenes[{idx_s}].crop_box")

        # Validate positive timing floats
        for num_field, min_val in (
            ("blink_interval", 0.1),
            ("beats_per_frame", 0.1),
            ("frame_fps", 0.1),
            ("fg_scale", 0.05),
        ):
            if sc.get(num_field) is not None:
                val = float(sc[num_field])
                if not (math.isfinite(val) and val >= min_val):
                    raise ValueError(f"Scene {idx_s} '{num_field}' must be >= {min_val}, got: {val}")

        start_t = cur_beat * beat_sec
        end_t = (cur_beat + beats) * beat_sec
        cur_beat += beats

        raw_scene_list = list(sc.get("scene_frames")) if sc.get("scene_frames") is not None else (
            [sc["scene_image"]] if sc.get("scene_image") else []
        )
        raw_fg_list = list(sc.get("fg_frames")) if sc.get("fg_frames") is not None else (
            [sc["fg_image"]] if sc.get("fg_image") else []
        )
        raw_sticker_list = list(sc.get("frames")) if sc.get("frames") is not None else (
            [sc["sticker"]] if sc.get("sticker") else []
        )

        if not isinstance(raw_scene_list, list) or not isinstance(raw_fg_list, list) or not isinstance(raw_sticker_list, list):
            raise ValueError(f"Scene {idx_s} frame lists must be arrays")
        if not raw_scene_list and not raw_sticker_list:
            raise ValueError(
                f"Scene {idx_s} must specify at least one visual asset ('scene_image', 'scene_frames', 'sticker', or 'frames')"
            )

        # Auto-guard against stale blink frame when user replaces primary keyframe with external Banana 2.5 image
        if sc.get("frame_mode") == "natural_blink" and len(raw_scene_list) >= 2:
            p0 = resolve_asset_path(str(raw_scene_list[0]), base_dir, skill_dir)
            try:
                p1 = resolve_asset_path(str(raw_scene_list[1]), base_dir, skill_dir)
                if p0.stat().st_mtime > p1.stat().st_mtime + 2.0:
                    raw_scene_list = [raw_scene_list[0]]
            except FileNotFoundError:
                raw_scene_list = [raw_scene_list[0]]

        scene_frames: list[Image.Image] = []
        fg_frames: list[Image.Image] = []
        sticker_frames: list[Image.Image] = []

        shot_grade = str(sc.get("color_grade", default_grade))
        for raw_sc in raw_scene_list:
            resolved_scene = resolve_asset_path(str(raw_sc), base_dir, skill_dir)
            if load_images:
                s_key = f"{resolved_scene.resolve()}::{shot_grade}::{crop_box}"
                if s_key not in scene_cache:
                    raw_img = _safe_open_rgba(resolved_scene)
                    if crop_box is not None:
                        cw, ch = raw_img.size
                        raw_img = raw_img.crop((
                            int(cw * crop_box[0]),
                            int(ch * crop_box[1]),
                            int(cw * crop_box[2]),
                            int(ch * crop_box[3]),
                        ))
                    resized_img = _cover_resize(raw_img, oversample_w, oversample_h)
                    if shot_grade == "midnight_emo":
                        resized_img = _apply_cinema_emo_grade(resized_img)
                    scene_cache[s_key] = resized_img
                scene_frames.append(scene_cache[s_key])

        for raw_fg in raw_fg_list:
            resolved_fg = resolve_asset_path(str(raw_fg), base_dir, skill_dir)
            if load_images:
                f_key = str(resolved_fg.resolve())
                if f_key not in sticker_cache:
                    sticker_cache[f_key] = load_and_trim_sticker(resolved_fg)
                fg_frames.append(sticker_cache[f_key])

        if not raw_scene_list:
            for raw_s in raw_sticker_list:
                resolved = resolve_asset_path(str(raw_s), base_dir, skill_dir)
                if load_images:
                    key = str(resolved.resolve())
                    if key not in sticker_cache:
                        sticker_cache[key] = load_and_trim_sticker(resolved)
                    sticker_frames.append(sticker_cache[key])

        resolved_light_pos = sc.get("light_pos")
        if resolved_light_pos == "auto" and load_images and scene_frames:
            resolved_light_pos = list(_detect_warm_light_anchor(scene_frames[0]))
        resolved_prop_pos = sc.get("prop_pos")
        if resolved_prop_pos == "auto" and load_images and scene_frames:
            resolved_prop_pos = list(_detect_warm_light_anchor(scene_frames[0]))

        raw_lines = sc.get("lines", [])
        if not isinstance(raw_lines, list):
            raise ValueError(f"Scene {idx_s} 'lines' must be a list of strings")
        raw_highlights = sc.get("highlight", []) or []
        if not isinstance(raw_highlights, list):
            raise ValueError(f"Scene {idx_s} 'highlight' must be a list of strings")
        highlights = [str(h) for h in raw_highlights if h]

        max_line_chars = max(4, int(sc.get("max_chars_per_line", default_max_chars)))
        wrapped_lines = _wrap_cjk_lines([str(x) for x in raw_lines], max_chars=max_line_chars, highlights=highlights)

        primary_src = str((raw_scene_list or raw_sticker_list)[0])
        vis_src = f"{primary_src}#{crop_box}" if crop_box else primary_src
        compiled_scenes.append({
            **sc,
            "light_pos": resolved_light_pos,
            "prop_pos": resolved_prop_pos,
            "_vis_src": vis_src,
            "_cinema_emo": is_cinema_emo,
            "_is_last_scene": (idx_s == len(scenes)),
            "hud": sc.get("hud", default_hud),
            "underline": sc.get("underline", default_underline),
            "letter_spacing": sc.get("letter_spacing", default_spacing),
            "lines": wrapped_lines,
            "highlight": highlights,
            "start_t": start_t,
            "end_t": end_t,
            "beats": beats,
            "scene_frames": scene_frames,
            "fg_frames": fg_frames,
            "sticker_frames": sticker_frames,
        })

    return bpm, theme, bg_path, compiled_scenes


def render_video(
    timeline_path: Path,
    out_prefix: Path,
    fps: int = 30,
    font_path: str | None = None,
    audio_path: Path | None = None,
    theme_override: str | None = None,
    bg_override: Path | None = None,
) -> tuple[Path, Path]:
    if not (1 <= int(fps) <= 120):
        raise ValueError(f"FPS must be between 1 and 120, got: {fps}")
    if audio_path is not None and not audio_path.is_file():
        raise FileNotFoundError(f"Custom audio file not found: {audio_path}")

    data: Any = json.loads(timeline_path.read_text(encoding="utf-8"))
    is_cinema_emo = str(data.get("style", "cinema_emo") if isinstance(data, dict) else "cinema_emo") == "cinema_emo"
    ok, resolved_font = check_environment(font_path, prefer_serif=is_cinema_emo)
    if not ok:
        raise SystemExit(1)

    base_dir = timeline_path.parent
    skill_dir = Path(__file__).resolve().parent.parent

    bpm, theme, bg_path, compiled_scenes = compile_timeline(
        data,
        base_dir=base_dir,
        skill_dir=skill_dir,
        theme_override=theme_override,
        bg_override=bg_override,
        load_images=True,
    )
    beat_sec = 60.0 / bpm
    header_tag = str(data.get("tag", ""))
    base_font_size = max(34, min(120, int(data.get("font_size", 52 if is_cinema_emo else 58))))

    total_duration = compiled_scenes[-1]["end_t"]
    total_frames = max(1, int(round(total_duration * fps)))
    avg_shot_sec = total_duration / len(compiled_scenes)
    total_chars = sum(len(ln.replace(" ", "").replace(".", "")) for cs in compiled_scenes for ln in cs.get("lines", []))
    print(
        f"Timeline: {len(compiled_scenes)} shots | {total_chars} chars | "
        f"{bpm:g} BPM | {total_duration:.2f}s (avg {avg_shot_sec:.2f}s/shot)"
    )
    for warn in _validate_timeline_pacing(compiled_scenes, bpm):
        print(warn, file=sys.stderr)

    rng = random.Random(101)
    assets = RenderAssets(
        backdrop=build_base_backdrop(
            theme,
            bg_image_path=bg_path,
            bg_scrim_alpha=int(data.get("bg_scrim_alpha", 120)),
        ),
        warm_glow=build_warm_glow(theme, 440),
        vignette=_build_vignette(108 if is_cinema_emo else 82),
        scrims={
            "top": _build_text_scrim("top", theme),
            "bottom": _build_text_scrim("bottom", theme),
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
    trans_duration = max(0.0, float(data.get("transition_sec", min(0.58, beat_sec * 0.72))))

    with tempfile.TemporaryDirectory(dir=str(out_prefix.parent)) as tmp_dir:
        tmp_path = Path(tmp_dir)
        tmp_silent = tmp_path / "silent.mp4"
        tmp_preview = tmp_path / "preview.mp4"

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
            "-colorspace", "bt709",
            "-color_primaries", "bt709",
            "-color_trc", "bt709",
            "-movflags", "+faststart",
            str(tmp_silent),
        ]

        with tempfile.TemporaryFile() as stderr_file:
            proc = subprocess.Popen(
                ffmpeg_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=stderr_file,
            )
            assert proc.stdin is not None
            scene_idx = 0
            try:
                for f_idx in range(total_frames):
                    t = f_idx / fps
                    while scene_idx + 1 < len(compiled_scenes) and t >= compiled_scenes[scene_idx]["end_t"]:
                        scene_idx += 1

                    sc = compiled_scenes[scene_idx]
                    visual_frame = _render_visual_stage(sc, t, beat_sec, assets, theme)

                    transition = sc.get("transition", "crossfade")
                    has_trans = (scene_idx > 0 and trans_duration > 0.005 and transition != "cut")
                    if has_trans:
                        local_t = t - sc["start_t"]
                        if local_t < trans_duration:
                            prev_sc = compiled_scenes[scene_idx - 1]
                            prev_visual = _render_visual_stage(prev_sc, t, beat_sec, assets, theme)
                            visual_frame = _apply_transition(
                                prev_visual,
                                visual_frame,
                                transition,
                                local_t / trans_duration,
                                theme,
                            )

                    eff_trans_offset = (trans_duration * 0.56) if has_trans else 0.0
                    text_layer = _render_typography_layer(
                        sc,
                        t,
                        beat_sec,
                        total_duration,
                        theme,
                        resolved_font,
                        base_font_size,
                        font_tag,
                        header_tag,
                        trans_offset=eff_trans_offset,
                    )
                    frame = Image.alpha_composite(visual_frame, text_layer)

                    proc.stdin.write(frame.convert("RGB").tobytes())
            except BrokenPipeError:
                pass
            except Exception:
                proc.kill()
                raise
            finally:
                try:
                    proc.stdin.close()
                except Exception:
                    pass
                proc.wait()

            if proc.returncode != 0:
                stderr_file.seek(0)
                err_msg = stderr_file.read().decode("utf-8", errors="ignore")
                raise RuntimeError(f"FFmpeg video encode failed (exit {proc.returncode}): {err_msg}")

        audio_source = audio_path
        if audio_source is None:
            synth_wav = tmp_path / "beat_preview.wav"
            synthesize_beat_wav(synth_wav, total_duration, bpm)
            audio_source = synth_wav

        mux_cmd = [
            "ffmpeg",
            "-y",
            "-i", str(tmp_silent),
            "-i", str(audio_source),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(tmp_preview),
        ]
        res = subprocess.run(mux_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Audio mux failed: {res.stderr}")

        os.replace(tmp_silent, silent_mp4)
        os.replace(tmp_preview, preview_mp4)

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
    parser.add_argument("--validate", action="store_true", help="Validate timeline schema, assets, wrapping & pacing")
    args = parser.parse_args()

    if args.check:
        ok, font = check_environment(args.font)
        print(f"ffmpeg: {'OK' if ok else 'MISSING'}")
        print(f"cjk_font: {font or 'NOT FOUND (fallback to default)'}")
        raise SystemExit(0 if ok else 1)

    if args.validate:
        if not args.timeline:
            parser.error("--timeline is required with --validate")
        data = json.loads(args.timeline.read_text(encoding="utf-8"))
        base_dir = args.timeline.parent
        skill_dir = Path(__file__).resolve().parent.parent
        bpm, _theme, _bg, compiled = compile_timeline(
            data,
            base_dir=base_dir,
            skill_dir=skill_dir,
            theme_override=args.theme,
            bg_override=args.bg,
            load_images=False,
        )
        total_dur = compiled[-1]["end_t"]
        print(f"Validated {len(compiled)} shots | {bpm:g} BPM | {total_dur:.2f}s")
        for idx_s, cs in enumerate(compiled, 1):
            print(f"  Shot {idx_s} ({cs['end_t'] - cs['start_t']:.2f}s): {cs['lines']}")
        warnings = _validate_timeline_pacing(compiled, bpm)
        for w in warnings:
            print(w, file=sys.stderr)
        raise SystemExit(0)

    if not args.timeline or not args.out:
        parser.error("--timeline and --out are required unless --check or --validate is used")

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
