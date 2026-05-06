---
id: "mathematical-precision"
title: "Mathematical Precision: Preserve Vector Geometry"
status: "Active"
created: "2026-05-06"
last_reviewed: "2026-05-06"
review_frequency: "Annual"
conflicts_with: ["progressive-fidelity"]
tags:
- tenet
- quality
- vector
- svg
---

# Tenet: Mathematical Precision: Preserve Vector Geometry

## Tenet

**Description**: Manim's core strength is that it produces mathematically precise animations from exact geometric descriptions. Bézier curves, precise stroke widths, and exact color values should survive the journey from Python to the browser as faithfully as possible. The SVG format is a natural home for this — SVG paths are Bézier curves, colors are exact, and the output scales to any resolution without loss. This precision should not be sacrificed for convenience.

In practice this means: prefer SVG paths over rasterized PNGs, prefer inline SVG over `<img>` tags where sub-element access matters, and never approximate a Bézier curve as a polyline when the curve itself can be expressed directly. When precision must be traded for practicality (e.g. rasterizing a complex shader effect), document the limitation explicitly.

**Quote**: *"Don't rasterize what can stay as curves."*

**Examples**:
- Converting `VMobject.points` Bézier handles directly to SVG `<path d="M ... C ...">` rather than sampling the curve and drawing line segments
- Embedding TeX SVG output inline rather than as a PNG screenshot
- Preserving stroke width as an SVG attribute rather than baking it into the geometry
- Using exact RGBA values rather than rounding to 8-bit web colors

**Counter-examples**:
- Rasterizing all mobjects to PNG per frame when SVG paths are available (loses scalability, increases file size)
- Sampling Bézier curves into polylines for "simplicity"
- Discarding sub-mobject structure when embedding TeX (makes individual symbol animation impossible)
- Approximating gradient fills with a nearest solid color

**Conflicts**:
- Conflicts with `progressive-fidelity` when achieving full precision is expensive
- Resolution: precision is the default; approximations are explicitly documented and scoped to a follow-on CIP
