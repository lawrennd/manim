---
id: "2026-05-06_cip0001-step2-vmobject-svg-path"
title: "CIP-0001 Step 2: VMobject to SVG path conversion"
status: "Completed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
owner: ""
dependencies:
- "2026-05-06_cip0001-step1-config-cli-stubs"
related_cips:
- "0001"
tags:
- cip0001
- vmobject
- svg
- bezier
---

# Task: CIP-0001 Step 2 — VMobject to SVG Path Conversion

## Description

Implement `SVGCamera.capture_mobjects` for `VMobject` and its subclasses. This is the core rendering logic: extract Bézier handles from `vmobject.points`, build SVG path strings, and apply stroke/fill styling. After this step, simple geometric scenes (circles, squares, lines, arrows) should produce visually correct SVG frames.

## Acceptance Criteria

- [x] `VMobject.points` Bézier handles are converted to `<path d="M ... C ... Z">` SVG path data
- [x] Stroke color, stroke width, and stroke opacity are applied as SVG attributes
- [x] Fill color and fill opacity are applied as SVG attributes
- [x] Open paths (not closed) omit the `Z` command; closed paths include it
- [x] `VGroup` submobjects are rendered in correct z-order
- [x] Geometric scenes (Square, Circle) produce visually correct per-frame SVG files
- [x] MathTex/LaTeX expressions render correctly (as VMobject path trees, 8.5 KB/frame for `E=mc²`)

## Implementation Notes

Key methods on `VMobject`:
- `vmobject.points` — numpy array, shape `(N, 3)`, groups of 4: `[anchor, handle_out, handle_in, anchor, ...]`
- `vmobject.get_stroke_color()`, `get_stroke_width()`, `get_stroke_opacity()`
- `vmobject.get_fill_color()`, `get_fill_opacity()`
- `vmobject.is_closed()` — whether to add `Z` to path

SVG path conversion: for each group of 4 points `[a0, h1, h2, a1]` emit `C h1x,h1y h2x,h2y a1x,a1y`. Start the path with `M a0x,a0y`.

Colors: Manim uses `ManimColor` (which can be converted to hex). `svgwrite` accepts hex color strings directly.

Note: coordinate transform (Manim centred → SVG top-left) is implemented in Step 3 and applied here as a post-processing transform rather than inline in the path math.

## Related

- CIP: 0001 (Step 2 of 8)
- Requirements: REQ-0001 (web-embeddable animations), REQ-0003 (vector geometry preserved)

## Progress Updates

### 2026-05-06
Task created. Status: Proposed (depends on Step 1).

Implemented `SVGCamera.capture_mobjects` with `_render_vmobject` and
`_vmobject_to_svg_path_data`. Key points:
- Uses `vmob.get_subpaths()` to correctly handle disconnected paths
- Iterates groups of 4 points (`nppcc`) to emit `M ... C ...` SVG path data
- Y-coordinates are negated to convert Manim y-up → SVG y-down
- `SVGRenderer.update_frame` now always renders `scene.mobjects + scene.foreground_mobjects`
  (no static-frame optimisation — SVG layers can't be composited like pixel buffers)
- Smoke tests: Square+Circle animation produces correct cubic Bézier paths;
  MathTex `E=mc²` writes and animates correctly via the existing VMobject path tree

Status: Completed.
