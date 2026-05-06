---
id: "0003"
title: "Mathematical text (LaTeX/MathTex) is preserved as vector content in web output"
status: "Proposed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
related_tenets:
- "mathematical-precision"
- "python-is-authoring"
stakeholders:
- "mathematics educators"
- "researchers presenting technical content"
tags:
- latex
- mathtex
- svg
- vector
- math
---

# REQ-0003: Mathematical text (LaTeX/MathTex) is preserved as vector content in web output

## Description

`MathTex` and `Tex` are among the most commonly used mobjects in Manim. They convert LaTeX expressions to SVG via a TeX → DVI → SVG pipeline and then import that SVG as a collection of `VMobject`s. In the web export, this mathematical content should remain as vector SVG, not be rasterized to a PNG.

This matters especially because mathematical notation often appears at different zoom levels in presentations. Rasterizing equations at a fixed resolution produces blurry output when slides are zoomed or projected at high resolution. The LaTeX-to-SVG pipeline Manim already uses produces exactly the right output — it just needs to survive the export step.

**Why this matters**: Aligns with `mathematical-precision` (LaTeX produces SVG; that precision should not be discarded at export time) and `python-is-authoring` (the TeX-to-SVG conversion happens in Python; the browser receives finished markup).

**Who benefits**: Mathematics educators and researchers — the primary Manim user base — who present technical content and need crisp equations at any scale.

## Acceptance Criteria

- [ ] `MathTex` and `Tex` objects appear in exported SVG frames as SVG path elements, not as embedded PNG images
- [ ] Individual glyphs within a `MathTex` expression retain their position and styling from the Manim scene
- [ ] The exported SVG renders the equation correctly in major browsers without requiring MathJax or KaTeX
- [ ] The SVG export handles the case where the LaTeX SVG cache is present (standard render workflow)

## Notes

Manim already converts LaTeX to SVG via `tex_to_svg_file` in `manim/utils/tex_file_writing.py` and imports the result via `SVGMobject`. The SVG renderer can embed these cached SVG fragments inline rather than re-rasterizing them. The sub-mobject structure (individual symbol manipulation) is preserved as long as the SVG path elements are emitted per glyph.

## References

- **Related Tenets**: `mathematical-precision`, `python-is-authoring`
- **External Links**: `manim/utils/tex_file_writing.py`, `manim/mobject/text/tex_mobject.py`

## Progress Updates

### 2026-05-06
Requirement created. Status: Proposed.
