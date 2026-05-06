---
id: "0001"
title: "Manim scenes can be exported as web-embeddable animations without rasterization"
status: "Proposed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
related_tenets:
- "mathematical-precision"
- "progressive-fidelity"
- "python-is-authoring"
stakeholders:
- "scene authors who publish to the web"
- "educators embedding animations in course materials"
tags:
- svg
- export
- vector
---

# REQ-0001: Manim scenes can be exported as web-embeddable animations without rasterization

## Description

Manim currently produces rasterized video output (MP4, WebM, GIF) or static PNG frames. For web use, these require video infrastructure (hosting, codecs, autoplay policies) and do not scale cleanly to high-resolution displays. There should be a path from a Manim scene to a web-embeddable animation that preserves the mathematical precision of the original vector geometry.

The output should be usable in any standard web context — embedded in a page with an `<img>` tag, loaded via JavaScript, or included in a presentation tool — without requiring a custom server or proprietary player.

**Why this matters**: Aligns with `mathematical-precision` (preserve vector geometry) and `python-is-authoring` (Python produces the artifact, web consumes it). Solves a real friction point for educators and technical authors who currently have to choose between video (heavy, rasterized) and static images (no animation).

**Who benefits**: Scene authors publishing to the web, educators embedding animations in HTML course notes or slides, anyone who finds video hosting overhead disproportionate for simple mathematical animations.

## Acceptance Criteria

- [ ] Running a Manim render command with a format flag produces a directory of SVG files, one per frame
- [ ] The SVG files are valid, well-formed SVG that renders correctly in major browsers (Chrome, Firefox, Safari)
- [ ] VMobject geometry (circles, lines, curves) is represented as SVG paths, not rasterized bitmaps
- [ ] The output includes a manifest file describing frame count, fps, and scene dimensions
- [ ] The SVG files are self-contained (no external dependencies, no references to local filesystem paths)

## Notes

The frame-per-SVG approach is chosen over animated SVG (SMIL) or Canvas/WebGL as the simplest correct starting point. SMIL and Canvas approaches are valid follow-on improvements but are not required to satisfy this requirement.

## References

- **Related Tenets**: `mathematical-precision`, `progressive-fidelity`, `python-is-authoring`

## Progress Updates

### 2026-05-06
Requirement created. Status: Proposed.
