---
id: "0004"
title: "The scene authoring API is unchanged — existing scenes export to SVG with only a flag change"
status: "Proposed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
related_tenets:
- "unchanged-authoring"
- "design-for-contribution"
stakeholders:
- "all existing Manim scene authors"
- "ManimCE project maintainers (backward compatibility)"
tags:
- api
- backward-compatibility
- authoring
---

# REQ-0004: The scene authoring API is unchanged — existing scenes export to SVG with only a flag change

## Description

Any existing Manim scene that currently renders to video should be renderable to SVG frames by changing only the render command (e.g. adding `--format svg`), with no changes to the scene's Python source. The `Scene` base class, `construct()` method, `self.play()`, `self.wait()`, `self.add()`, and all standard animation and mobject APIs remain unchanged.

This requirement protects the existing Manim user base and is a prerequisite for the SVG renderer being accepted as an upstream contribution to ManimCE. A renderer that requires API changes cannot be merged without breaking existing code.

**Why this matters**: Aligns with `unchanged-authoring` (the author's only visible change is a flag) and `design-for-contribution` (ManimCE will not accept a PR that breaks existing scenes).

**Who benefits**: All existing Manim scene authors; the ManimCE community who depend on API stability.

## Acceptance Criteria

- [ ] The example scene `SquareToCircle` (from `example_scenes/`) renders to SVG without any modification to the scene file
- [ ] No new base class is required for SVG export (authors use `Scene` as before)
- [ ] No new methods on `Scene` are required during `construct()` for SVG export
- [ ] The existing `Animation` subclasses (`FadeIn`, `Transform`, `Create`, `Write`, etc.) work without modification
- [ ] The SVG renderer does not change default frame rate, coordinate system, or camera defaults

## Notes

Limitations of the SVG renderer (e.g. unsupported mobject types, 3D scenes) should be surfaced as warnings or errors at render time, not as API changes that affect the author's `construct()` method.

## References

- **Related Tenets**: `unchanged-authoring`, `design-for-contribution`

## Progress Updates

### 2026-05-06
Requirement created. Status: Proposed.
