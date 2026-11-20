#!/usr/bin/env python3
"""Render a beat-synced 9:16 Paperbag Emo explainer video using Pillow + FFmpeg.

No external LLM, image, or video API keys required.
Outputs both:
  - <out>_silent.mp4 (ready for Douyin in-app music selection)
  - <out>_beat_preview.mp4 (with synthesized subtle Lo-Fi BPM pulse for beat verification)
Optionally muxes a user-provided audio file via --audio.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import struct
import subprocess
import tempfile
import wave
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH = 1080
HEIGHT = 1920

DEFAULT_FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
]

BG_TOP = (44, 58, 64)       # muted slate-teal
BG_BOTTOM = (21, 29, 34)    # deep late-night charcoal-teal
TEXT_WHITE = (242, 238, 230)
AMBER = (244, 184, 96)
TEAL_ACCENT = (130, 188, 192)
MUTED_GRAY = (158, 170, 174)


def ease_out_cubic(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return 1.0 - (1.0 - x) ** 3


def ease_out_back(x: float) -> float:
    x = max(0.0, min(1.0, x))
    c1 = 1.70158
    c3 = c1 + 1.0
    return 1.0 + c3 * ((x - 1.0) ** 3) + c1 * ((x - 1.0) ** 2)


def find_font(font_path: str | None, size: int) -> ImageFont.FreeTypeFont:
    candidates = [font_path] if font_path else []
    candidates.extend(DEFAULT_FONT_PATHS)
    for path in candidates:
        if path and Path(path).is_file():
            try:
                return ImageFont.truetype(path, size=size, index=0)
            except Exception:
                try:
                    return ImageFont.truetype(path, size=size)
                except Exception:
                    continue
    return ImageFont.load_default()


def build_base_backdrop(seed: int = 42) -> Image.Image:
    """Pre-bake the vertical gradient, subtle paper grain, and warm floor line."""
    img = Image.new("RGBA", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    for y in range(HEIGHT):
        ratio = y / (HEIGHT - 1)
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # Subtle paper speckle grain (fast deterministic scatter)
    rng = random.Random(seed)
    grain_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    grain_draw = ImageDraw.Draw(grain_layer)
    for _ in range(9000):
        gx = rng.randint(0, WIDTH - 1)
        gy = rng.randint(0, HEIGHT - 1)
        tone = 255 if rng.random() > 0.5 else 0
        alpha = rng.randint(4, 12)
        grain_draw.point((gx, gy), fill=(tone, tone, tone, alpha))
    img = Image.alpha_composite(img, grain_layer)

    # Subtle comic desk horizon line near lower third
    horizon = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(horizon)
    hdraw.line([(120, 1650), (WIDTH - 120, 1650)], fill=(18, 22, 25, 190), width=4)
    hdraw.line([(200, 1664), (WIDTH - 200, 1664)], fill=(18, 22, 25, 90), width=2)
    img = Image.alpha_composite(img, horizon)
    return img


def build_warm_glow(radius: int = 460) -> Image.Image:
    """Create a soft warm amber lamp halo sprite."""
    size = radius * 2
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    for step in range(40, 0, -1):
        frac = step / 40.0
        cur_r = int(radius * frac)
        alpha = int(46 * ((1.0 - frac) ** 1.8))
        draw.ellipse(
            [radius - cur_r, radius - cur_r, radius + cur_r, radius + cur_r],
            fill=(244, 184, 96, alpha),
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


def draw_highlighted_line(
    draw: ImageDraw.ImageDraw,
    text: str,
    highlights: list[str],
    font: ImageFont.FreeTypeFont,
    center_x: int,
    y: int,
    alpha: int,
    underline_progress: float,
) -> None:
    if alpha <= 0:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    total_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    start_x = center_x - total_w // 2

    # Split text into styled spans
    spans: list[tuple[str, bool]] = []
    idx = 0
    while idx < len(text):
        matched = None
        for kw in highlights:
            if kw and text.startswith(kw, idx):
                if matched is None or len(kw) > len(matched):
                    matched = kw
        if matched:
            spans.append((matched, True))
            idx += len(matched)
        else:
            if spans and not spans[-1][1]:
                spans[-1] = (spans[-1][0] + text[idx], False)
            else:
                spans.append((text[idx], False))
            idx += 1

    cur_x = start_x
    for segment, is_hi in spans:
        seg_box = draw.textbbox((0, 0), segment, font=font)
        seg_w = seg_box[2] - seg_box[0]
        color = (*AMBER, alpha) if is_hi else (*TEXT_WHITE, alpha)
        # Subtle shadow for readability
        draw.text((cur_x + 2, y + 3), segment, font=font, fill=(10, 14, 16, int(alpha * 0.55)))
        draw.text((cur_x, y), segment, font=font, fill=color)

        if is_hi and underline_progress > 0.01:
            line_y = y + text_h + 14
            end_x = cur_x + int(seg_w * max(0.0, min(1.0, underline_progress)))
            draw.line(
                [(cur_x, line_y), (end_x, line_y)],
                fill=(*AMBER, int(alpha * 0.9)),
                width=5,
            )
        cur_x += seg_w


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
                # Warm soft sub-thump (110Hz -> 55Hz)
                freq = 55.0 + 65.0 * math.exp(-dt * 28.0)
                env = math.exp(-dt * 18.0) * (1.0 - math.exp(-dt * 250.0))
                buf[pos] += 0.42 * env * math.sin(2.0 * math.pi * freq * dt)
            else:
                # Subtle soft rim/wood tick
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


def render_video(
    timeline_path: Path,
    out_prefix: Path,
    fps: int = 30,
    font_path: str | None = None,
    audio_path: Path | None = None,
) -> tuple[Path, Path]:
    data: dict[str, Any] = json.loads(timeline_path.read_text(encoding="utf-8"))
    bpm = float(data.get("bpm", 84))
    beat_sec = 60.0 / bpm
    header_tag = data.get("tag", "")
    scenes = data["scenes"]

    base_dir = timeline_path.parent
    skill_dir = Path(__file__).resolve().parent.parent

    # Resolve timeline start/end times in exact beats
    compiled_scenes: list[dict[str, Any]] = []
    cur_beat = 0.0
    sticker_cache: dict[str, Image.Image] = {}

    for sc in scenes:
        beats = float(sc.get("beats", 4))
        start_t = cur_beat * beat_sec
        end_t = (cur_beat + beats) * beat_sec
        cur_beat += beats

        raw_sticker = Path(sc["sticker"])
        if not raw_sticker.is_file():
            alt = base_dir / sc["sticker"]
            alt2 = skill_dir / sc["sticker"]
            if alt.is_file():
                raw_sticker = alt
            elif alt2.is_file():
                raw_sticker = alt2
            else:
                raise FileNotFoundError(f"Sticker not found: {sc['sticker']}")
        key = str(raw_sticker.resolve())
        if key not in sticker_cache:
            sticker_cache[key] = load_and_trim_sticker(raw_sticker)

        compiled_scenes.append({
            **sc,
            "start_t": start_t,
            "end_t": end_t,
            "beats": beats,
            "sticker_img": sticker_cache[key],
        })

    total_duration = cur_beat * beat_sec
    total_frames = max(1, int(round(total_duration * fps)))

    backdrop = build_base_backdrop()
    warm_glow = build_warm_glow(440)
    font_main = find_font(font_path, 58)
    font_tag = find_font(font_path, 28)

    # Pre-generate deterministic drifting dust motes
    rng = random.Random(101)
    motes = [
        (
            rng.uniform(80, WIDTH - 80),
            rng.uniform(180, 1650),
            rng.uniform(2.5, 5.5),
            rng.uniform(0.3, 0.9),
            rng.uniform(0, 2 * math.pi),
        )
        for _ in range(22)
    ]

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
    for f_idx in range(total_frames):
        t = f_idx / fps
        while scene_idx + 1 < len(compiled_scenes) and t >= compiled_scenes[scene_idx]["end_t"]:
            scene_idx += 1
        sc = compiled_scenes[scene_idx]
        local_t = max(0.0, t - sc["start_t"])
        local_beat = local_t / beat_sec
        beat_phase = (t / beat_sec) % 1.0
        beat_pulse = math.exp(-7.0 * beat_phase)  # sharp pulse at each exact beat!

        frame = backdrop.copy()

        # Subtle warm amber glow pulsing gently behind character
        glow_scale = 0.96 + 0.08 * beat_pulse
        gw = int(warm_glow.width * glow_scale)
        gh = int(warm_glow.height * glow_scale)
        glow_resized = warm_glow.resize((gw, gh), Image.Resampling.BILINEAR)
        frame.alpha_composite(glow_resized, (WIDTH // 2 - gw // 2, 1280 - gh // 2))

        # Drifting ambient dust motes
        mote_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        mdraw = ImageDraw.Draw(mote_layer)
        for mx0, my0, mr, mspeed, mphase in motes:
            mx = mx0 + 18.0 * math.sin(t * mspeed + mphase)
            my = (my0 - t * 18.0 * mspeed) % 1620
            malpha = int(45 + 35 * math.sin(t * 1.4 + mphase) + 30 * beat_pulse)
            mdraw.ellipse(
                [mx - mr, my - mr, mx + mr, my + mr],
                fill=(244, 210, 145, max(10, min(140, malpha))),
            )
        frame = Image.alpha_composite(frame, mote_layer)

        # Compute IP sticker transform strictly from beat timeline
        motion = sc.get("motion", "beat_nod")
        sticker: Image.Image = sc["sticker_img"]
        scale_f = 1.0
        dx = 0.0
        dy = 0.0
        angle = 0.0

        if motion == "bounce_in":
            p = ease_out_back(min(1.0, local_t / (beat_sec * 0.55)))
            scale_f = 0.85 + 0.15 * p + 0.015 * beat_pulse
            dy = (1.0 - p) * 55.0
        elif motion == "beat_nod":
            scale_f = 1.0 + 0.025 * beat_pulse
            dy = 8.0 * beat_pulse
        elif motion == "zoom_punch":
            punch = math.exp(-7.5 * local_t)
            scale_f = 1.0 + 0.12 * punch + 0.015 * beat_pulse
        elif motion == "sigh_sway":
            sway = math.sin(math.pi * local_beat / 2.0)
            angle = 1.6 * sway
            dy = 10.0 * (0.5 - 0.5 * math.cos(math.pi * local_beat / 2.0))
            scale_f = 1.0 + 0.012 * math.sin(math.pi * local_beat)
        elif motion == "calm_float":
            scale_f = 1.0 + 0.014 * math.sin(math.pi * local_beat / 2.0)
            dy = 5.0 * math.sin(math.pi * local_beat / 2.0)

        sw = max(1, int(round(sticker.width * scale_f)))
        sh = max(1, int(round(sticker.height * scale_f)))
        cur_sticker = sticker.resize((sw, sh), Image.Resampling.BILINEAR)
        if abs(angle) > 0.05:
            cur_sticker = cur_sticker.rotate(angle, resample=Image.Resampling.BILINEAR, expand=True)

        # Anchor bottom of character cleanly around the desk horizon (y = 1648)
        paste_x = int(WIDTH // 2 - cur_sticker.width // 2 + dx)
        paste_y = int(1648 - cur_sticker.height + dy)
        frame.alpha_composite(cur_sticker, (paste_x, paste_y))

        # Draw typography & progress UI
        text_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        tdraw = ImageDraw.Draw(text_layer)

        # Subtle top header tag & beat progress bar
        if header_tag:
            tbox = tdraw.textbbox((0, 0), header_tag, font=font_tag)
            tw = tbox[2] - tbox[0]
            tdraw.text(
                (WIDTH // 2 - tw // 2, 165),
                header_tag,
                font=font_tag,
                fill=(*MUTED_GRAY, 180),
            )

        bar_w = 180
        bar_x0 = WIDTH // 2 - bar_w // 2
        bar_y = 218
        tdraw.line([(bar_x0, bar_y), (bar_x0 + bar_w, bar_y)], fill=(120, 140, 145, 70), width=3)
        prog = min(1.0, t / max(0.01, total_duration))
        tdraw.line(
            [(bar_x0, bar_y), (bar_x0 + int(bar_w * prog), bar_y)],
            fill=(*AMBER, 200),
            width=3,
        )

        # Scene kinetic lines
        lines: list[str] = sc.get("lines", [])
        highlights: list[str] = sc.get("highlight", [])
        text_anim = sc.get("text_anim", "beat_lines")
        line_spacing = 104
        base_text_y = 500 - (len(lines) * line_spacing) // 2

        for idx_l, line_str in enumerate(lines):
            if text_anim == "beat_lines":
                appear_beat = idx_l * max(1.0, sc["beats"] / max(1, len(lines)) * 0.75)
                if local_beat < appear_beat:
                    continue
                lt = (local_beat - appear_beat) * beat_sec
                p = ease_out_cubic(min(1.0, lt / 0.28))
                alpha = int(255 * p)
                y_off = int((1.0 - p) * 26)
                ul_prog = ease_out_cubic(min(1.0, max(0.0, (local_beat - appear_beat - 0.35) / 0.65)))
            elif text_anim == "slam_center":
                p = ease_out_cubic(min(1.0, local_t / 0.22))
                alpha = int(255 * p)
                y_off = int((1.0 - p) * 14)
                ul_prog = ease_out_cubic(min(1.0, max(0.0, (local_beat - 0.8) / 0.8)))
            else:
                p = ease_out_cubic(min(1.0, local_t / 0.45))
                alpha = int(255 * p)
                y_off = int((1.0 - p) * 20)
                ul_prog = ease_out_cubic(min(1.0, max(0.0, (local_beat - 0.6) / 0.8)))

            draw_highlighted_line(
                tdraw,
                line_str,
                highlights,
                font_main,
                WIDTH // 2,
                base_text_y + idx_l * line_spacing + y_off,
                alpha,
                ul_prog,
            )

        # Subtle bottom beat dot indicator (4-beat measure pulse)
        cur_measure_beat = int(t / beat_sec) % 4
        dot_gap = 28
        dots_start_x = WIDTH // 2 - (3 * dot_gap) // 2
        for bi in range(4):
            cx = dots_start_x + bi * dot_gap
            cy = 1755
            is_cur = (bi == cur_measure_beat)
            r = 5 if is_cur else 3
            col = (*AMBER, int(190 + 60 * beat_pulse)) if is_cur else (*MUTED_GRAY, 85)
            tdraw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

        frame = Image.alpha_composite(frame, text_layer)
        proc.stdin.write(frame.convert("RGB").tobytes())

    proc.stdin.close()
    stderr = proc.stderr.read() if proc.stderr else b""
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {stderr.decode('utf-8', errors='ignore')}")

    # Mux beat preview audio (or user-provided audio)
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
    parser.add_argument("--timeline", type=Path, required=True, help="Timeline JSON file")
    parser.add_argument("--out", type=Path, required=True, help="Output file prefix")
    parser.add_argument("--fps", type=int, default=30, help="Frame rate (default: 30)")
    parser.add_argument("--font", type=str, default=None, help="Optional TTF/TTC font path")
    parser.add_argument("--audio", type=Path, default=None, help="Optional custom audio/BGM file")
    args = parser.parse_args()

    silent_mp4, preview_mp4 = render_video(
        args.timeline,
        args.out,
        fps=args.fps,
        font_path=args.font,
        audio_path=args.audio,
    )
    print(f"Rendered silent (Douyin-ready): {silent_mp4}")
    print(f"Rendered beat preview: {preview_mp4}")


if __name__ == "__main__":
    main()
