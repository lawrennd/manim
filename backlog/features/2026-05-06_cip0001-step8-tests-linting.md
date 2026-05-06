---
id: "2026-05-06_cip0001-step8-tests-linting"
title: "CIP-0001 Step 8: Tests, ruff, and mypy"
status: "Proposed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
owner: ""
dependencies:
- "2026-05-06_cip0001-step4-tex-svg-embedding"
- "2026-05-06_cip0001-step5-imagemobject"
- "2026-05-06_cip0001-step6-filewriter-manifest"
related_cips:
- "0001"
tags:
- cip0001
- testing
- ruff
- mypy
- upstream
---

# Task: CIP-0001 Step 8 — Tests, ruff, and mypy

## Description

Write tests for the SVG renderer using ManimCE's `@frames_comparison` decorator pattern, ensure all new code passes `ruff` linting and `mypy` type checking with the project's existing configuration, and verify REQ-0005 acceptance criteria are fully met. This is the final step before the CIP can be marked Implemented.

## Acceptance Criteria

- [ ] `pytest tests/` passes with no new failures
- [ ] `ruff check manim/renderer/svg_renderer.py manim/camera/svg_camera.py` reports no errors
- [ ] `mypy manim/renderer/svg_renderer.py manim/camera/svg_camera.py` reports no errors
- [ ] A `@frames_comparison` test covers `SVGRenderer` output for `SquareToCircle`
- [ ] A `@frames_comparison` test covers a `MathTex` scene
- [ ] A `@frames_comparison` test covers an `ImageMobject` scene
- [ ] All new public functions and classes have complete type annotations
- [ ] `svgwrite` is correctly listed as optional in `pyproject.toml`

## Implementation Notes

ManimCE's `@frames_comparison` decorator (in `tests/`) renders a scene and compares output frames against reference images. For SVG output, the comparison needs to rasterize the SVG frames first (e.g. using `cairosvg` or `playwright`) before pixel comparison.

Alternative: test the SVG structure directly (e.g. assert that `<path>` elements exist, that fill/stroke attributes are correct) rather than doing pixel comparison. This is simpler and more robust for the SVG format since pixel-perfect comparison between Cairo-rasterized and SVG-rasterized output may have minor anti-aliasing differences.

Check the existing test infrastructure:
```
tests/test_graphical_units/  # @frames_comparison tests live here
tests/conftest.py             # shared fixtures
```

## Related

- CIP: 0001 (Step 8 of 8)
- Requirements: REQ-0005 (upstream contribution readiness)

## Progress Updates

### 2026-05-06
Task created. Status: Proposed (final step, depends on Steps 4, 5, and 6 being complete).
