---
id: "2026-05-06_cip0001-step8-tests-linting"
title: "CIP-0001 Step 8: Tests, ruff, and mypy"
status: "Completed"
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

- [x] `pytest tests/test_svg_renderer.py` passes: 20/20 tests pass
- [x] `ruff check` reports no errors in new files (fixed 1: removed unused numpy import)
- [x] `mypy` reports no errors in `svg_camera.py` or `svg_renderer.py`
- [x] 20 tests cover: RendererType, is_svg_format(), SVGCamera init/reset/background, path conversion (open/closed/shifted/rotated/empty), ImageMobject, and end-to-end integration (frame output, manifest, multiple animations, wait frame count)
- [x] SVG structure tested directly (path elements, d= attributes, background rect) — simpler and more robust than pixel comparison for SVG output
- [x] All new public functions and classes have complete type annotations
- [x] `svgwrite` correctly listed as optional `[svg]` extra in `pyproject.toml`

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

20/20 tests written and passing in tests/test_svg_renderer.py:
- TestRendererType (3), TestSVGCameraInit (1), TestSVGCameraReset (4),
  TestVMobjectToSVGPath (6), TestImageMobjectRendering (1),
  TestSVGRendererIntegration (5)
Ruff fixed 1 unused import; mypy clean on new files.

Status: Completed.
