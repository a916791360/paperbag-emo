#!/usr/bin/env python3
"""Unit & regression tests for Paperbag Emo Mode B (cutout) and Mode C (video engine)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import cutout  # noqa: E402
import render_emo_video as rev  # noqa: E402


class TestWrapCjkLines(unittest.TestCase):
    def test_zero_or_negative_max_chars_never_infinite_loops(self) -> None:
        self.assertEqual(rev._wrap_cjk_lines(["一"], max_chars=0), ["一"])
        out = rev._wrap_cjk_lines(["这是一个测试长句子"], max_chars=-5)
        self.assertGreaterEqual(len(out), 2)
        self.assertEqual("".join(out), "这是一个测试长句子")

    def test_splits_at_chinese_punctuation(self) -> None:
        out = rev._wrap_cjk_lines(["那天晚上我一个人走在回家的路上，突然想明白了很多事情"], max_chars=14)
        self.assertEqual(out, ["那天晚上我一个人走在回家的路上，", "突然想明白了很多事情"])

    def test_avoids_splitting_inside_highlight_keyword(self) -> None:
        line = "于是我决定彻底和过去告别再也不回头了"
        out = rev._wrap_cjk_lines([line], max_chars=10, highlights=["彻底和过去告别"])
        self.assertTrue(any("彻底和过去告别" in seg for seg in out), f"Highlight split across lines: {out}")

    def test_ignores_empty_strings(self) -> None:
        self.assertEqual(rev._wrap_cjk_lines(["", "   ", "晚安"]), ["晚安"])


class TestCompileAndValidateTimeline(unittest.TestCase):
    def setUp(self) -> None:
        self.base_dir = REPO_ROOT / "studio"
        self.skill_dir = REPO_ROOT

    def test_rejects_invalid_bpm(self) -> None:
        with self.assertRaises(ValueError):
            rev.compile_timeline({"bpm": 0, "scenes": [{"sticker": "assets/stickers/thinking.png"}]}, self.base_dir, self.skill_dir)
        with self.assertRaises(ValueError):
            rev.compile_timeline({"bpm": -80, "scenes": [{"sticker": "assets/stickers/thinking.png"}]}, self.base_dir, self.skill_dir)

    def test_rejects_empty_scenes(self) -> None:
        with self.assertRaises(ValueError):
            rev.compile_timeline({"bpm": 80, "scenes": []}, self.base_dir, self.skill_dir)

    def test_rejects_missing_visual_source(self) -> None:
        with self.assertRaises(ValueError):
            rev.compile_timeline({"bpm": 80, "scenes": [{"beats": 4, "lines": ["hello"]}]}, self.base_dir, self.skill_dir)

    def test_rejects_path_traversal(self) -> None:
        with self.assertRaises(ValueError):
            rev.compile_timeline(
                {"bpm": 80, "scenes": [{"beats": 4, "scene_image": "../../../../etc/passwd"}]},
                self.base_dir,
                self.skill_dir,
            )

    def test_rejects_malformed_coordinates(self) -> None:
        with self.assertRaises(ValueError):
            rev.compile_timeline(
                {
                    "bpm": 80,
                    "scenes": [{
                        "beats": 4,
                        "sticker": "assets/stickers/thinking.png",
                        "steam_pos": [0.5],
                    }],
                },
                self.base_dir,
                self.skill_dir,
            )

    def test_pacing_and_highlight_warnings(self) -> None:
        warns = rev._validate_timeline_pacing(
            [
                {
                    "start_t": 0.0,
                    "end_t": 1.5,
                    "lines": ["字数太多完全来不及看完这一整句长文案"],
                    "highlight": ["不存在的词"],
                    "_vis_src": "a.jpg",
                    "camera": "push_in",
                },
                {
                    "start_t": 1.5,
                    "end_t": 8.0,
                    "lines": ["停太久"],
                    "_vis_src": "a.jpg",
                    "camera": "push_in",
                },
            ],
            bpm=80,
        )
        tags = [w.split("]")[0] + "]" for w in warns]
        self.assertIn("[READABILITY HINT]", tags)
        self.assertIn("[HIGHLIGHT HINT]", tags)
        self.assertIn("[PACE HINT]", tags)
        self.assertIn("[DIVERSITY HINT]", tags)

    def test_crop_box_validation_and_warm_light_auto_anchor(self) -> None:
        self.assertEqual(rev._parse_crop_box([0.1, 0.2, 0.9, 0.8]), (0.1, 0.2, 0.9, 0.8))
        with self.assertRaises(ValueError):
            rev._parse_crop_box([0.8, 0.2, 0.4, 0.8])
        img = Image.new("RGB", (128, 128), (16, 24, 32))
        px = img.load()
        for y in range(75, 95):
            for x in range(25, 45):
                px[x, y] = (248, 192, 96)
        ax, ay = rev._detect_warm_light_anchor(img)
        self.assertTrue(0.18 <= ax <= 0.38, f"Expected warm anchor x around 0.27, got {ax}")
        self.assertTrue(0.55 <= ay <= 0.78, f"Expected warm anchor y around 0.66, got {ay}")

    def test_decoupled_typography_waits_for_transition_offset(self) -> None:
        sc = {
            "start_t": 3.0,
            "end_t": 6.0,
            "beats": 4.0,
            "lines": ["心都会碎，"],
            "highlight": ["心都会碎"],
            "text_anim": "slam_center",
            "hud": "none",
            "underline": True,
            "letter_spacing": 4,
            "_cinema_emo": True,
            "_is_last_scene": False,
            "scene_frames": [],
        }
        theme = rev.THEMES["late_night"]
        font_path = rev.resolve_font_path(prefer_serif=True)
        font_tag = rev.load_font(font_path, 28)
        # During transition (t=3.15 < 3.0 + 0.32), subtitle must wait and not be swallowed
        early_layer = rev._render_typography_layer(
            sc, t=3.15, beat_sec=0.75, total_duration=9.0, theme=theme,
            font_path=font_path, base_font_size=52, font_tag=font_tag, header_tag="", trans_offset=0.32,
        )
        self.assertIsNone(early_layer.getbbox())
        # After transition offset + cascade (t=3.85), subtitle and underline must be visible
        active_layer = rev._render_typography_layer(
            sc, t=3.85, beat_sec=0.75, total_duration=9.0, theme=theme,
            font_path=font_path, base_font_size=52, font_tag=font_tag, header_tag="", trans_offset=0.32,
        )
        self.assertIsNotNone(active_layer.getbbox())

    def test_first_scene_frame0_renders_full_cover_subtitle(self) -> None:
        sc = {
            "start_t": 0.0,
            "end_t": 3.0,
            "beats": 4.0,
            "lines": ["我没有不甘心，"],
            "highlight": ["没有不甘心"],
            "text_anim": "typewriter_beat",
            "hud": "none",
            "underline": True,
            "letter_spacing": 4,
            "_cinema_emo": True,
            "_is_first_scene": True,
            "_is_last_scene": False,
            "scene_frames": [],
        }
        theme = rev.THEMES["late_night"]
        font_path = rev.resolve_font_path(prefer_serif=True)
        font_tag = rev.load_font(font_path, 28)
        f0_layer = rev._render_typography_layer(
            sc, t=0.0, beat_sec=0.75, total_duration=12.0, theme=theme,
            font_path=font_path, base_font_size=60, font_tag=font_tag, header_tag="", trans_offset=0.0,
        )
        self.assertIsNotNone(f0_layer.getbbox(), "Frame 0 must contain opening cover subtitle")

    def test_same_image_crop_box_auto_upgrades_crossfade_to_camera_morph(self) -> None:
        data = {
            "bpm": 78,
            "style": "cinema_emo",
            "scenes": [
                {
                    "beats": 4,
                    "scene_image": "studio/scenes/chengyi/s3_full_sincerity_lantern.jpg",
                    "lines": ["我拿出了最大的诚意，"],
                    "transition": "crossfade",
                },
                {
                    "beats": 4,
                    "scene_image": "studio/scenes/chengyi/s3_full_sincerity_lantern.jpg",
                    "crop_box": [0.12, 0.14, 0.88, 0.86],
                    "lines": ["所以该遗憾的不是我。"],
                    "transition": "crossfade",
                },
            ],
        }
        _bpm, _theme, _bg, compiled = rev.compile_timeline(data, self.base_dir, self.skill_dir, load_images=False)
        self.assertEqual(compiled[0]["transition"], "crossfade")
        self.assertEqual(
            compiled[1]["transition"],
            "camera_morph",
            "Consecutive shots sharing the same base keyframe must use camera_morph instead of crossfade ghosting",
        )

    def test_scene_video_validation_and_same_video_camera_morph(self) -> None:
        with tempfile.TemporaryDirectory(dir=str(self.base_dir)) as tmp:
            dummy_vid = Path(tmp) / "clip.mp4"
            dummy_vid.write_bytes(b"placeholder")
            rel_vid = str(dummy_vid.relative_to(self.base_dir))
            data = {
                "bpm": 76,
                "style": "cinema_emo",
                "scenes": [
                    {
                        "beats": 4,
                        "scene_video": rel_vid,
                        "video_start": 0.0,
                        "video_speed": 1.0,
                        "video_loop": "pingpong",
                        "lines": ["一种是你曾经那么用力地爱过，"],
                    },
                    {
                        "beats": 4,
                        "scene_video": rel_vid,
                        "video_start": 3.2,
                        "crop_box": [0.12, 0.16, 0.88, 0.86],
                        "text_y": 320,
                        "transition": "crossfade",
                        "lines": ["最后却发现，那个人根本不值得。"],
                    },
                ],
            }
            _bpm, _theme, _bg, compiled = rev.compile_timeline(data, self.base_dir, self.skill_dir, load_images=False)
            self.assertEqual(compiled[1]["transition"], "camera_morph")
            self.assertEqual(compiled[1]["text_y"], 320)
            with self.assertRaises(ValueError):
                bad = {**data, "scenes": [{**data["scenes"][0], "video_loop": "invalid_mode"}]}
                rev.compile_timeline(bad, self.base_dir, self.skill_dir, load_images=False)

    def test_smooth_three_frame_natural_blink_and_delay(self) -> None:
        f_open = Image.new("RGBA", (8, 8), (10, 10, 10, 255))
        f_half = Image.new("RGBA", (8, 8), (120, 120, 120, 255))
        f_closed = Image.new("RGBA", (8, 8), (240, 240, 240, 255))
        sc = {"frame_mode": "natural_blink", "blink_interval": 4.0, "blink_delay": 1.5, "blink_duration": 0.24}
        frames = [f_open, f_half, f_closed]
        # Before blink_delay: stays open
        self.assertIs(rev._pick_frame_from_list(frames, sc, 0.0, 0.0), f_open)
        self.assertIs(rev._pick_frame_from_list(frames, sc, 1.4, 1.8), f_open)
        # 5-stage sequence: open -> half -> closed -> half -> open
        self.assertIs(rev._pick_frame_from_list(frames, sc, 1.52, 2.0), f_half)
        self.assertIs(rev._pick_frame_from_list(frames, sc, 1.60, 2.1), f_closed)
        self.assertIs(rev._pick_frame_from_list(frames, sc, 1.70, 2.2), f_half)
        self.assertIs(rev._pick_frame_from_list(frames, sc, 1.80, 2.3), f_open)

    def test_local_micro_motion_cat_breath_twitch_and_cursor(self) -> None:
        base_img = Image.new("RGBA", (200, 200), (20, 30, 40, 255))
        px = base_img.load()
        for y in range(120, 180):
            for x in range(110, 170):
                px[x, y] = (180, 140, 100, 255)
        sc = {
            "_cat_box": (0.50, 0.55, 0.90, 0.95),
            "_cat_ear_box": (0.55, 0.55, 0.85, 0.72),
            "cat_breath_period": 2.0,
            "cat_breath_amp": 0.04,
            "cat_twitch_delay": 1.0,
            "cat_twitch_interval": 3.0,
            "fx": ["cursor_blink"],
            "cursor_pos": [0.25, 0.25],
            "cursor_color": "amber",
            "cursor_len": 20,
        }
        out = rev._apply_local_micro_motion(base_img, sc, local_t=1.06, t=1.06)
        self.assertEqual(out.size, base_img.size)
        # Cursor should have painted bright amber pixel near (50, 50)
        self.assertGreater(out.getpixel((50, 50))[0], 150)


class TestCutoutPipeline(unittest.TestCase):
    def test_preserves_kraft_and_charcoal_opacity_and_removes_green_screen(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "green.png"
            dst = Path(tmp) / "out.png"
            img = Image.new("RGB", (64, 64), (0, 255, 0))
            px = img.load()
            # Kraft paper brown patch (16..31) & dark charcoal hoodie patch (32..47)
            for y in range(16, 48):
                for x in range(16, 32):
                    px[x, y] = (196, 158, 114)
                for x in range(32, 48):
                    px[x, y] = (34, 38, 42)
            img.save(src)

            key, transparent, _partial = cutout.remove_background(src, dst)
            self.assertEqual(key, (0, 255, 0))
            self.assertGreater(transparent, 0)
            self.assertTrue(dst.is_file())

            out = Image.open(dst).convert("RGBA")
            opx = out.load()
            # Corners must be fully transparent
            for corner in ((0, 0), (63, 0), (0, 63), (63, 63)):
                self.assertEqual(opx[corner[0], corner[1]][3], 0)
            # Kraft brown and charcoal hoodie interiors must stay 100% opaque
            self.assertEqual(opx[24, 32][3], 255)
            self.assertEqual(opx[40, 32][3], 255)


if __name__ == "__main__":
    unittest.main()
