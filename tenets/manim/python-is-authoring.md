---
id: "python-is-authoring"
title: "Python is the Authoring Tool, the Web is the Display Medium"
status: "Active"
created: "2026-05-06"
last_reviewed: "2026-05-06"
review_frequency: "Annual"
conflicts_with: ["progressive-fidelity"]
tags:
- tenet
- architecture
- python
- web
---

# Tenet: Python is the Authoring Tool, the Web is the Display Medium

## Tenet

**Description**: Manim scenes are authored in Python. The web is a display target, not a co-authoring environment. The boundary between these two worlds is a serialized artifact — SVG frames, JSON metadata, or similar — that the Python side produces and the web side consumes. No Python logic, animation computation, or scene state crosses that boundary as executable code. This keeps the authoring model simple and deterministic: what you write in Python is exactly what gets rendered, and the web layer's only job is faithful playback.

This principle prevents a class of complexity where animation logic has to be reimplemented in JavaScript to support interactivity or dynamic scenes. If a scene requires Python to compute (NumPy arrays, symbolic math, custom algorithms), it stays in Python. The web receives the result, not the computation.

**Quote**: *"Python computes, the web displays — never the other way around."*

**Examples**:
- The SVG renderer runs entirely in Python and writes files to disk; the JS plugin reads those files and displays them
- A `MathTex` expression is computed and converted to SVG by Python/LaTeX tooling; the browser receives finished SVG markup, not a MathJax instruction to render
- Updaters and scene-level Python lambdas are baked into pre-computed frames rather than serialized as JS functions

**Counter-examples**:
- Porting the `Animation.interpolate` logic to JavaScript so the browser can compute intermediate frames at runtime
- Sending symbolic math expressions to the browser to be rendered by MathJax (loses Manim's layout and sub-mobject model)
- Allowing users to write JS callbacks that modify scene state during playback

**Conflicts**:
- Conflicts with `progressive-fidelity` when the "quick" option involves rasterizing to video (which is fine) but the longer-term goal is live browser-side interpolation
- Resolution: pre-baked frames are always acceptable; live browser interpolation is an opt-in future extension, never a requirement
