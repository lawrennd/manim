---
id: "2026-05-06_cip0001-step2-vmobject-svg-path"
title: "CIP-0001 Step 2: VMobject to SVG path conversion"
status: "Proposed"
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

- [ ] `VMobject.points` Bézier handles are converted to `<path d="M ... C ... Z">` SVG path data
- [ ] Stroke color, stroke width, and stroke opacity are applied as SVG attributes
- [ ] Fill color and fill opacity are applied as SVG attributes
- [ ] Open paths (not closed) omit the `Z` command; closed paths include it
- [ ] `VGroup` submobjects are rendered in correct z-order
- [ ] The `SquareToCircle` example scene produces per-frame SVG files that are visually correct
- [ ] Output is compared against Cairo renderer reference frames and is within acceptable tolerance

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
