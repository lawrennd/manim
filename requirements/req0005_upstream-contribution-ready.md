---
id: "0005"
title: "The Python renderer component is suitable for proposal to the ManimCE upstream project"
status: "Proposed"
priority: "Medium"
created: "2026-05-06"
last_updated: "2026-05-06"
related_tenets:
- "design-for-contribution"
- "unchanged-authoring"
stakeholders:
- "ManimCE maintainers"
- "Manim community users who would benefit from SVG export"
tags:
- upstream
- open-source
- manimce
- contribution
---

# REQ-0005: The Python renderer component is suitable for proposal to the ManimCE upstream project

## Description

The `SVGRenderer` and `SVGCamera` classes developed in this fork should meet the technical bar required to open a pull request against the ManimCE repository. This means the code follows their conventions, is tested, and does not introduce hard dependencies that would affect all Manim users.

This requirement is explicitly scoped to the Python renderer (`manim/renderer/svg_renderer.py`, `manim/camera/svg_camera.py`, and related changes). The JS RevealJS plugin (`js/manim-svg.js`) is out of scope for upstream contribution — it will live in a separate `manim-svg` package.

**Why this matters**: The `design-for-contribution` tenet exists specifically to avoid the common failure mode where a promising fork diverges so far from upstream conventions that a PR becomes impossible to review. By treating upstream-readiness as a requirement rather than a nice-to-have, we keep the option open without committing to actually submitting the PR.

**Who benefits**: The broader Manim community who would get SVG export without needing to install a separate fork. ManimCE maintainers who would receive a well-structured, testable contribution.

## Acceptance Criteria

- [ ] All new Python code passes `ruff` linting with the project's existing configuration
- [ ] All new public functions and classes have `mypy`-compatible type annotations
- [ ] Tests for `SVGRenderer` are written using the `@frames_comparison` decorator pattern used in `tests/`
- [ ] `svgwrite` is declared as an optional dependency in `pyproject.toml` (e.g. `pip install manim[svg]`)
- [ ] No existing public API signatures are modified
- [ ] The `SVGRenderer` follows the same structural pattern as `CairoRenderer` and `OpenGLRenderer`

## Notes

Meeting this requirement does not commit to actually submitting a PR — that decision is deferred to `cip0002`. The requirement simply ensures the option is preserved.

## References

- **Related Tenets**: `design-for-contribution`, `unchanged-authoring`
- **External Links**: [ManimCE contribution guide](https://docs.manim.community/en/stable/contributing/index.html)

## Progress Updates

### 2026-05-06
Requirement created. Status: Proposed.
