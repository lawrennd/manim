---
id: "design-for-contribution"
title: "Design for Contribution"
status: "Active"
created: "2026-05-06"
last_reviewed: "2026-05-06"
review_frequency: "Annual"
conflicts_with: ["progressive-fidelity"]
tags:
- tenet
- open-source
- quality
- upstream
---

# Tenet: Design for Contribution

## Tenet

**Description**: The Python renderer code written in this fork should be a credible upstream PR candidate for ManimCE from the start. This means following ManimCE's existing code conventions, type annotation standards, test patterns, and dependency management practices — not as an afterthought, but as a constraint on how code is written in the first place. Code that works but violates these conventions will be harder to merge and harder for the community to maintain.

In practice: use `ruff` and `mypy` with the project's existing configuration, write tests using the `@frames_comparison` decorator pattern used throughout `tests/`, declare any new dependencies as optional extras in `pyproject.toml`, and avoid changes to existing public API signatures. The JS plugin (`js/manim-svg.js`) is explicitly not an upstream contribution target — it lives in this fork and eventually moves to a separate `manim-svg` package.

**Quote**: *"Write it as if someone else has to merge it tomorrow."*

**Examples**:
- Type-annotating all new public functions and classes with `mypy`-compatible annotations
- Writing `@frames_comparison` tests for `SVGRenderer` output alongside the implementation
- Declaring `svgwrite` as an optional dependency (`pip install manim[svg]`) rather than a hard dependency
- Following the existing `CairoRenderer` / `OpenGLRenderer` class structure so the pattern is immediately recognizable to ManimCE maintainers

**Counter-examples**:
- Writing the renderer as a standalone script that patches Manim at import time
- Adding `svgwrite` as a mandatory dependency that all Manim users must install
- Skipping type annotations because "it's just a prototype"
- Using a different test infrastructure than the rest of the test suite

**Conflicts**:
- Conflicts with `progressive-fidelity` when doing things "the right way" (full type annotations, tests, optional dependencies) takes longer than a quick prototype
- Resolution: the prototype lives on a feature branch; nothing merges to main without meeting ManimCE conventions. The speed/quality trade-off is managed through branching, not by skipping conventions.
