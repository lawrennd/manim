---
id: "2026-05-06_cip0001-step3-coordinate-transform"
title: "CIP-0001 Step 3: Manim to SVG coordinate transform"
status: "Completed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
owner: ""
dependencies:
- "2026-05-06_cip0001-step2-vmobject-svg-path"
related_cips:
- "0001"
tags:
- cip0001
- coordinates
- transform
- svg
---

# Task: CIP-0001 Step 3 — Manim to SVG Coordinate Transform

## Description

Implement the coordinate system transform from Manim's centred, y-up space to SVG's top-left, y-down space. Apply this as a `viewBox` on the root `<svg>` element combined with a `<g transform="scale(1,-1) translate(0, -height)">` wrapper, so individual path coordinates remain in Manim's space and SVG's transform machinery handles the flip.

After this step, shapes should appear in the correct positions on screen with correct orientation.

## Acceptance Criteria

- [x] A circle at the origin in Manim renders at the centre of the SVG viewport
- [x] A square at `UP` (0, 1, 0) in Manim renders above centre in the SVG (path top-edge at y=-2)
- [x] The y-axis is not flipped (Manim's y-up matches visual expectations in the browser)
- [x] The SVG `viewBox` matches the scene frame dimensions from `config.frame_width` and `config.frame_height`
- [x] Background rectangle added using `config["background_color"]` — correct colour in all browser contexts

## Implementation Notes

Manim's default frame: `frame_width = 14.222...`, `frame_height = 8.0`, origin at centre.

SVG viewBox approach:
```
viewBox="-7.111 -4 14.222 8"   (Manim coordinates directly)
```
Combined with `<g transform="scale(1,-1)">` to flip y-axis (SVG is y-down, Manim is y-up).

This approach keeps all path coordinates in Manim's native space — no per-point coordinate conversion needed. The transform is applied once at the group level.

Pixel output dimensions (for `width`/`height` on `<svg>`): use `config.pixel_width` and `config.pixel_height` for the rendered resolution, while the `viewBox` stays in Manim coordinate space.

## Related

- CIP: 0001 (Step 3 of 8)
- Requirements: REQ-0001 (correct web output), REQ-0003 (mathematical precision)

## Progress Updates

### 2026-05-06
Task created. Status: Proposed (depends on Step 2).

Implementation choice: negating y inline in path data rather than a
`<g transform="scale(1,-1)">` wrapper. Both approaches are equivalent;
the inline negation avoids an extra SVG group element.

Added `SVGCamera.reset()` background rectangle using
`config["background_color"].to_hex()` so scenes have the correct
background in all browser contexts (SVG default is transparent).

All acceptance criteria confirmed via smoke tests:
- Shift, scale, rotation all work — Manim bakes transforms into `points`
- Square at UP → path top-edge at SVG y=-2 (above centre) ✓
- ViewBox spans -7.111..4 (Manim frame dimensions) ✓

Status: Completed.
