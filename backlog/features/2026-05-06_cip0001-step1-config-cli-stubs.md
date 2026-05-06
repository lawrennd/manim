---
id: "2026-05-06_cip0001-step1-config-cli-stubs"
title: "CIP-0001 Step 1: Config, CLI, and renderer stubs"
status: "Ready"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
owner: ""
dependencies: []
related_cips:
- "0001"
tags:
- cip0001
- config
- cli
- scaffold
---

# Task: CIP-0001 Step 1 — Config, CLI, and Renderer Stubs

## Description

Add `RendererType.SVG` to the renderer enum, wire up `--format svg` in the CLI and config system, add `is_svg_format()` to `file_ops.py`, declare `svgwrite` as an optional dependency in `pyproject.toml`, and create stub implementations of `SVGRenderer` and `SVGCamera` that produce empty but valid SVG files.

The goal of this step is to verify the entire render pipeline runs end-to-end without errors on a simple scene (e.g. `SquareToCircle`) before any real drawing logic is implemented.

## Acceptance Criteria

- [ ] `manim render --format svg example_scenes/basic.py SquareToCircle` runs without error
- [ ] A `media/svg/SquareToCircle/` output directory is created containing numbered `.svg` files
- [ ] The SVG files are valid (empty but well-formed) XML
- [ ] `pip install manim[svg]` installs `svgwrite` as an optional dependency
- [ ] `is_svg_format()` returns `True` when `config["format"] == "svg"`
- [ ] `ruff` and `mypy` pass on all new/modified files

## Implementation Notes

Files to create:
- `manim/renderer/svg_renderer.py` — stub `SVGRenderer` with `play()`, `render()`, `update_frame()`, `scene_finished()` matching `CairoRenderer`'s interface
- `manim/camera/svg_camera.py` — stub `SVGCamera` with `capture_mobjects()` that returns an empty `svgwrite.Drawing`

Files to modify:
- `manim/renderer/__init__.py` — add `RendererType.SVG = "svg"`
- `manim/scene/scene.py` — add `elif config.renderer == RendererType.SVG: renderer = SVGRenderer()`
- `manim/scene/scene_file_writer.py` — add `open_svg_output()`, `write_svg_frame()`, `close_svg_output()` stubs; gate on `is_svg_format()`
- `manim/utils/file_ops.py` — add `is_svg_format()`
- `manim/_config/` — add `"svg"` to valid format values
- `pyproject.toml` — add `svgwrite` to `[project.optional-dependencies]` under `svg`

## Related

- CIP: 0001 (Step 1 of 8)
- Requirements: REQ-0004 (unchanged authoring API), REQ-0005 (upstream contribution readiness)

## Progress Updates

### 2026-05-06
Task created. Status: Ready.
