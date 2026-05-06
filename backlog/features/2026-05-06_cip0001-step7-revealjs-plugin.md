---
id: "2026-05-06_cip0001-step7-revealjs-plugin"
title: "CIP-0001 Step 7: RevealJS plugin (js/manim-svg.js)"
status: "Proposed"
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

- [ ] A RevealJS presentation with `<script src="js/manim-svg.js"></script>` and a slide marked `data-manim-svg="path/to/animation_0/"` plays the animation correctly
- [ ] The animation starts when the slide becomes active and stops (or loops) when the slide is left
- [ ] `data-manim-loop="true"` causes the animation to loop; omitting or setting to `"false"` stops at the last frame
- [ ] `data-manim-fps` overrides the fps from `animation.json` if provided
- [ ] No build step, bundler, or Node.js is required to use the plugin
- [ ] The plugin works in Chrome, Firefox, and Safari
- [ ] A minimal example HTML file (`js/example.html`) demonstrates the plugin in use

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
