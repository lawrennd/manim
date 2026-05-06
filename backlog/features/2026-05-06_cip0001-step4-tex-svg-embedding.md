---
id: "2026-05-06_cip0001-step4-tex-svg-embedding"
title: "CIP-0001 Step 4: TeX and SVGMobject inline embedding"
status: "Completed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
owner: ""
dependencies:
- "2026-05-06_cip0001-step3-coordinate-transform"
related_cips:
- "0001"
tags:
- cip0001
- tex
- mathtex
- svg
- embedding
---

# Task: CIP-0001 Step 4 — TeX and SVGMobject Inline Embedding

## Description

Handle `SVGMobject`, `Tex`, and `MathTex` in `SVGCamera.capture_mobjects`. These mobjects are already backed by an SVG file on disk (produced by `tex_to_svg_file` and cached). Rather than re-rasterizing them, embed the SVG path data inline, applying the mobject's current position and transform. This satisfies REQ-0003 (LaTeX preserved as vector content).

## Acceptance Criteria

- [x] `MathTex(r"E = mc^2")` produces SVG frames where the equation is represented as SVG `<path>` elements (~8.5 KB/frame), not as an embedded PNG
- [x] The equation appears at the correct position and scale in the frame
- [x] `SVGMobject` is a subclass of `VMobject` — handled automatically by Step 2's path conversion with no additional work
- [x] Individual glyph paths are preserved in the output via the submobject tree
- [ ] Browser compatibility testing (Chrome, Firefox, Safari) — deferred to manual validation phase

## Implementation Notes

`MathTex` and `Tex` use `SVGMobject` internally. After `tex_to_svg_file` runs, the SVG is parsed into `VMobject`s via `SVGMobject._init_svg_mobject`. By the time `capture_mobjects` runs, a `MathTex` is just a tree of `VMobject`s — so Step 2's VMobject path conversion may already handle it correctly.

Key check: does the existing VMobject path conversion in Step 2 already handle TeX correctly by construction, or do the glyph paths need special treatment?

If the VMobject tree from `SVGMobject` is already fully decomposed into Bézier paths, Step 2 may satisfy this requirement with no additional work. If not, the fallback is to detect `SVGMobject` instances, read the cached SVG file, parse it with `xml.etree.ElementTree`, and emit the path elements directly with the mobject's transform applied.

Test scene:
```python
class MathScene(Scene):
    def construct(self):
        eq = MathTex(r"e^{i\pi} + 1 = 0")
        self.add(eq)
        self.wait(1)
```

## Related

- CIP: 0001 (Step 4 of 8)
- Requirements: REQ-0003 (LaTeX preserved as vector SVG)

## Progress Updates

### 2026-05-06
Task created. Status: Proposed (depends on Step 3).

As predicted by the implementation notes, `SVGMobject` (and therefore
`MathTex`/`Tex`) is a `VMobject` subclass. By the time `capture_mobjects`
is called, the SVG file has been parsed into a tree of `VMobject` path
segments. Step 2's VMobject path conversion handles all of this
automatically. Confirmed with `MathTex("E = mc^2")` producing 8.5 KB/frame
of pure SVG `<path>` elements.

Status: Completed (no additional implementation required beyond Step 2).
