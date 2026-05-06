"""Tests for the SVG renderer (CIP-0001).

These tests verify:
- SVGCamera geometry (path data, coordinate transform, background)
- SVGRenderer pipeline (frame output, manifest, frozen-frame handling)
- RendererType.SVG constant and is_svg_format() utility

Tests are unit-level where possible: they exercise the camera and renderer
in isolation without a real scene, avoiding slow LaTeX compilation.
Integration smoke tests use simple geometric scenes.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import tempfile

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_config_svg(tmp_dir: str) -> None:
    """Configure Manim globals for SVG rendering into *tmp_dir*."""
    from manim import config
    from manim.constants import RendererType

    config.renderer = RendererType.SVG
    config.frame_rate = 4
    config.pixel_width = 320
    config.pixel_height = 180
    config.media_dir = tmp_dir
    config.background_color = "#000000"


# ---------------------------------------------------------------------------
# RendererType and is_svg_format
# ---------------------------------------------------------------------------

class TestRendererType:
    def test_svg_member_exists(self) -> None:
        from manim.constants import RendererType

        assert hasattr(RendererType, "SVG")
        assert RendererType.SVG.value == "svg"

    def test_is_svg_format_true_when_renderer_svg(self) -> None:
        from manim import config
        from manim.constants import RendererType
        from manim.utils.file_ops import is_svg_format

        original = config.renderer
        try:
            config.renderer = RendererType.SVG
            assert is_svg_format() is True
        finally:
            config.renderer = original

    def test_is_svg_format_false_when_renderer_cairo(self) -> None:
        from manim import config
        from manim.constants import RendererType
        from manim.utils.file_ops import is_svg_format

        original = config.renderer
        try:
            config.renderer = RendererType.CAIRO
            assert is_svg_format() is False
        finally:
            config.renderer = original


# ---------------------------------------------------------------------------
# SVGCamera — unit tests
# ---------------------------------------------------------------------------

class TestSVGCameraInit:
    def test_requires_svgwrite(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """ImportError is raised when svgwrite is not installed."""
        import builtins

        real_import = builtins.__import__

        def mock_import(name: str, *args, **kwargs):  # type: ignore[no-untyped-def]
            if name == "svgwrite":
                raise ImportError("svgwrite not installed")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)
        # Re-import after patching so the lazy import triggers.
        import importlib
        import manim.camera.svg_camera as mod
        importlib.reload(mod)
        with pytest.raises(ImportError, match="svgwrite"):
            mod.SVGCamera()
        importlib.reload(mod)  # restore


class TestSVGCameraReset:
    def setup_method(self) -> None:
        from manim import config
        from manim.constants import RendererType

        config.renderer = RendererType.SVG
        config.pixel_width = 320
        config.pixel_height = 180
        config.background_color = "#1a1a2e"

    def _make_camera(self):  # type: ignore[no-untyped-def]
        from manim.camera.svg_camera import SVGCamera

        return SVGCamera()

    def test_reset_creates_drawing(self) -> None:
        cam = self._make_camera()
        cam.reset()
        assert cam._current_drawing is not None

    def test_reset_sets_viewbox(self) -> None:
        cam = self._make_camera()
        cam.reset()
        svg_str = cam.get_drawing().tostring()
        assert 'viewBox' in svg_str

    def test_reset_adds_background_rect(self) -> None:
        cam = self._make_camera()
        cam.reset()
        svg_str = cam.get_drawing().tostring()
        # Background rect should contain the configured color.
        assert "#1A1A2E" in svg_str.upper() or "1a1a2e" in svg_str.lower()

    def test_get_drawing_auto_resets(self) -> None:
        cam = self._make_camera()
        assert cam._current_drawing is None
        drawing = cam.get_drawing()
        assert drawing is not None


# ---------------------------------------------------------------------------
# SVGCamera — path conversion
# ---------------------------------------------------------------------------

class TestVMobjectToSVGPath:
    def setup_method(self) -> None:
        from manim import config
        from manim.constants import RendererType

        config.renderer = RendererType.SVG
        config.pixel_width = 640
        config.pixel_height = 360

    def _camera(self):  # type: ignore[no-untyped-def]
        from manim.camera.svg_camera import SVGCamera

        cam = SVGCamera()
        cam.reset()
        return cam

    def test_square_path_has_M_and_C(self) -> None:
        """Square path data should start with M and contain C commands."""
        from manim import Square

        cam = self._camera()
        sq = Square()
        path_data = cam._vmobject_to_svg_path_data(sq)
        assert path_data.startswith("M ")
        assert " C " in path_data

    def test_square_is_closed(self) -> None:
        """A square (closed shape) path should end with Z."""
        from manim import Square

        cam = self._camera()
        path_data = cam._vmobject_to_svg_path_data(Square())
        assert path_data.strip().endswith("Z")

    def test_line_is_not_closed(self) -> None:
        """An open path (Line) should not end with Z."""
        from manim import Line

        cam = self._camera()
        line = Line()
        path_data = cam._vmobject_to_svg_path_data(line)
        assert not path_data.strip().endswith("Z")

    def test_y_coordinate_is_negated(self) -> None:
        """A square centred at origin: top edge in Manim is y=+1, should be -1 in path data."""
        from manim import Square

        cam = self._camera()
        # Unit square: top-right corner is at Manim (1, 1).
        # In SVG path, y should be negated: -1.
        path_data = cam._vmobject_to_svg_path_data(Square())
        # First M command: M x,y — y should be negative for the top edge.
        m_match = re.search(r"M\s+([\d.+-]+),([\d.+-]+)", path_data)
        assert m_match is not None
        y_val = float(m_match.group(2))
        # Top-right corner: x≈1, y≈-1 (negated from Manim y=+1)
        assert y_val < 0, f"Expected negative y for top corner, got {y_val}"

    def test_shifted_mobject_coordinates_correct(self) -> None:
        """Square shifted RIGHT*2 should have path x-coords around 1..3."""
        from manim import RIGHT, Square

        cam = self._camera()
        sq = Square().shift(RIGHT * 2)
        path_data = cam._vmobject_to_svg_path_data(sq)
        # Extract first M x value.
        m_match = re.search(r"M\s+([\d.+-]+),", path_data)
        assert m_match is not None
        x_val = float(m_match.group(1))
        assert 0.9 < x_val < 3.1, f"Expected x in [1, 3], got {x_val}"

    def test_empty_mobject_returns_empty_string(self) -> None:
        from manim import VMobject

        cam = self._camera()
        empty = VMobject()
        assert cam._vmobject_to_svg_path_data(empty) == ""


# ---------------------------------------------------------------------------
# SVGCamera — ImageMobject
# ---------------------------------------------------------------------------

class TestImageMobjectRendering:
    def setup_method(self) -> None:
        from manim import config
        from manim.constants import RendererType

        config.renderer = RendererType.SVG
        config.pixel_width = 640
        config.pixel_height = 360

    def test_image_mobject_produces_image_element(self) -> None:
        from manim import ImageMobject
        from manim.camera.svg_camera import SVGCamera

        cam = SVGCamera()
        cam.reset()

        data = np.zeros((4, 4, 4), dtype=np.uint8)
        data[:, :] = [255, 0, 0, 255]
        img = ImageMobject(data)
        img.height = 2

        cam._render_image_mobject(img)
        svg_str = cam.get_drawing().tostring()
        assert "<image" in svg_str
        assert "data:image/png;base64," in svg_str


# ---------------------------------------------------------------------------
# Integration: full scene renders via SVGRenderer
# ---------------------------------------------------------------------------

class TestSVGRendererIntegration:
    def test_square_scene_produces_svg_files(self) -> None:
        """End-to-end: Square scene → SVG files and animation.json manifest."""
        with tempfile.TemporaryDirectory() as tmp:
            _make_config_svg(tmp)

            from manim import Scene, Square
            from manim.constants import RendererType

            class _SquareScene(Scene):
                def construct(self) -> None:
                    self.play(__import__("manim").Create(Square()))

            scene = _SquareScene()
            scene.render()

            svg_dir = pathlib.Path(tmp) / "svg" / "_SquareScene"
            anim_dirs = sorted(svg_dir.iterdir())
            assert len(anim_dirs) >= 1

            first_anim = anim_dirs[0]
            svgs = sorted(first_anim.glob("frame_*.svg"))
            assert len(svgs) > 0

            manifest = json.loads((first_anim / "animation.json").read_text())
            assert manifest["frame_count"] == len(svgs)
            assert manifest["fps"] == 4

    def test_svg_frames_contain_path_elements(self) -> None:
        """SVG frames from a Square scene must contain <path> elements."""
        with tempfile.TemporaryDirectory() as tmp:
            _make_config_svg(tmp)

            from manim import Scene, Square
            from manim.constants import RendererType

            class _PathScene(Scene):
                def construct(self) -> None:
                    self.add(Square())
                    self.wait(1)

            _PathScene().render()

            svg_dir = pathlib.Path(tmp) / "svg" / "_PathScene"
            # Check last frame of the only animation.
            frames = sorted((svg_dir / "animation_0").glob("frame_*.svg"))
            last_frame = frames[-1].read_text()
            assert "<path" in last_frame
            assert 'd="M' in last_frame

    def test_multiple_play_calls_produce_separate_animation_dirs(self) -> None:
        """Two self.play() calls → two animation_N/ directories."""
        with tempfile.TemporaryDirectory() as tmp:
            _make_config_svg(tmp)

            from manim import Circle, Scene, Square

            class _MultiScene(Scene):
                def construct(self) -> None:
                    self.play(__import__("manim").Create(Square()))
                    self.play(__import__("manim").Create(Circle()))

            _MultiScene().render()

            svg_dir = pathlib.Path(tmp) / "svg" / "_MultiScene"
            anim_dirs = sorted(svg_dir.iterdir())
            assert len(anim_dirs) == 2
            assert (anim_dirs[0] / "animation.json").exists()
            assert (anim_dirs[1] / "animation.json").exists()

    def test_wait_produces_correct_frame_count(self) -> None:
        """self.wait(1) at 4 fps → 4 frames in the animation directory."""
        with tempfile.TemporaryDirectory() as tmp:
            _make_config_svg(tmp)

            from manim import Scene, Square

            class _WaitScene(Scene):
                def construct(self) -> None:
                    self.add(Square())
                    self.wait(1)

            _WaitScene().render()

            svg_dir = pathlib.Path(tmp) / "svg" / "_WaitScene"
            frames = list((svg_dir / "animation_0").glob("frame_*.svg"))
            assert len(frames) == 4

    def test_background_rect_present_in_frame(self) -> None:
        """Every frame should contain a background <rect> element."""
        with tempfile.TemporaryDirectory() as tmp:
            _make_config_svg(tmp)
            from manim import config

            config.background_color = "#ff0000"

            from manim import Scene, Square

            class _BgScene(Scene):
                def construct(self) -> None:
                    self.add(Square())
                    self.wait(1)

            _BgScene().render()

            svg_dir = pathlib.Path(tmp) / "svg" / "_BgScene"
            frame = (svg_dir / "animation_0" / "frame_0000.svg").read_text()
            assert "<rect" in frame
            assert "FF0000" in frame.upper()
