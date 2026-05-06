---
id: "progressive-fidelity"
title: "Progressive Fidelity Over Perfection"
status: "Active"
created: "2026-05-06"
last_reviewed: "2026-05-06"
review_frequency: "Annual"
conflicts_with: ["mathematical-precision"]
tags:
- tenet
- architecture
- iteration
---

# Tenet: Progressive Fidelity Over Perfection

## Tenet

**Description**: A working SVG export that covers 80% of scenes today is more valuable than a theoretically perfect WebGL port that is months away. Build the simplest thing that produces correct output for the common case, ship it, then iterate. Each improvement should be a discrete step that leaves the system in a working state — never a long-branch rewrite that blocks all other progress.

This tenet is a guard against scope creep. 3D scenes, custom shaders, complex updaters, and interactive browser-side computation are all interesting problems. They are also not blockers for getting value from the SVG renderer. Scope them as explicit future CIPs rather than as requirements for the current phase.

**Quote**: *"A working export today beats a perfect port tomorrow."*

**Examples**:
- Shipping an SVG-per-frame renderer for 2D scenes before attempting SMIL animated SVG or Canvas/WebGL
- Skipping `ThreeDScene` support in the first CIP and documenting it as out of scope
- Pre-baking updater results into frames rather than trying to serialize arbitrary Python functions
- Producing a numbered SVG sequence that any `setInterval` loop can play back, rather than a custom binary format

**Counter-examples**:
- Blocking the SVG renderer release until it supports every Manim mobject type perfectly
- Trying to build a full JS animation engine in parallel with the Python renderer
- Requiring SMIL animated SVG output (single file, no JS dependency) before shipping anything
- Holding the first PR until 3D scene support is complete

**Conflicts**:
- Conflicts with `mathematical-precision` when the fast path (rasterization, approximation) would lose fidelity
- Resolution: prefer the higher-fidelity approach when the implementation cost is low; when cost is high, ship the lower-fidelity approach with a clear limitation note and a follow-on CIP
