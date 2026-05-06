---
id: "2026-05-06_cip0001-step7-revealjs-plugin"
title: "CIP-0001 Step 7: RevealJS plugin (js/manim-svg.js)"
status: "Completed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
owner: ""
dependencies:
- "2026-05-06_cip0001-step6-filewriter-manifest"
related_cips:
- "0001"
tags:
- cip0001
- revealjs
- javascript
- plugin
---

# Task: CIP-0001 Step 7 — RevealJS Plugin (js/manim-svg.js)

## Description

Write a vanilla JS RevealJS plugin that reads the `animation.json` manifest and cycles through SVG frames at the declared fps. The plugin is ~60 lines, requires no build step, and is included with a single `<script>` tag. It lives in `js/manim-svg.js` in this fork; it will move to a standalone `manim-svg` package in a future CIP.

## Acceptance Criteria

- [x] Plugin registered as `ManimSVG` with `id: 'manim-svg'`; loads with `plugins: [ManimSVG]`
- [x] Animation starts on `slidechanged` and stops when slide is left
- [x] `data-manim-loop="true"` loops; default stops at last frame
- [x] `data-manim-fps` overrides fps from `animation.json`
- [x] No build step required — single `<script>` tag, vanilla JS
- [x] Example HTML file created at `js/example.html` (covers single animation, loop, fps override, side-by-side, fragment-triggered)
- [x] Fragment events (`fragmentshown`/`fragmenthidden`) supported for step-by-step reveals
- [x] Nested `[data-manim-svg]` containers supported (multiple animations per slide)
- [x] Frames preloaded as blob URLs for instant display
- [ ] Browser compatibility testing — deferred to manual validation

## Implementation Notes

Plugin structure:
```javascript
const ManimSVG = {
  id: 'manim-svg',
  init(deck) {
    deck.on('slidechanged', ({ currentSlide, previousSlide }) => {
      stopAnimation(previousSlide);
      startAnimation(currentSlide);
    });
    // Also handle the first slide on load
    startAnimation(deck.getCurrentSlide());
  }
};

async function startAnimation(slide) {
  if (!slide) return;
  const dir = slide.dataset.manimSvg;
  if (!dir) return;
  const manifest = await fetch(`${dir}/animation.json`).then(r => r.json());
  const fps = parseInt(slide.dataset.manimFps ?? manifest.fps);
  // Preload frames as <img> elements
  // setInterval to cycle through them
}
```

Note: `data-manim-svg` maps to `dataset.manimSvg` in JS (camelCase). Confirm naming is consistent with REQ-0002 acceptance criteria.

The plugin file path `js/manim-svg.js` is a placeholder location in this fork. Future: moves to a `manim-svg` npm/PyPI package.

## Related

- CIP: 0001 (Step 7 of 8)
- Requirements: REQ-0002 (RevealJS embedding with no manual post-processing)

## Progress Updates

### 2026-05-06
Task created. Status: Proposed (depends on Step 6 for manifest format).

Implemented js/manim-svg.js (~210 lines, vanilla JS, no dependencies):
- Reads animation.json manifest via fetch()
- Preloads all frames as blob URLs (instant display, no per-frame fetch lag)
- WeakMap state per slide enables multiple simultaneous animations
- Handles: slide transitions, fragment events, loop, fps override, autoplay flag
- findAnimationTargets() supports data-manim-svg on section or nested containers
- Example HTML at js/example.html shows all common usage patterns

Status: Completed.
