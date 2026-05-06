---
id: "0002"
title: "Exported animations can be embedded in RevealJS presentations with no manual post-processing"
status: "Proposed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
related_tenets:
- "web-native-output"
- "unchanged-authoring"
stakeholders:
- "academics giving talks with RevealJS slides"
- "educators using web-based presentation tools"
tags:
- revealjs
- presentation
- embedding
---

# REQ-0002: Exported animations can be embedded in RevealJS presentations with no manual post-processing

## Description

A scene author should be able to render a scene to SVG frames and then embed the result in a RevealJS presentation without any manual file manipulation, format conversion, or custom server setup. The integration should be a "drop in frames directory, add a script tag" workflow.

Note: `manim-slides` already provides RevealJS export using video. This requirement is specifically about SVG-based embedding, which offers scalability and smaller file sizes for scenes with simple geometry. The two approaches are complementary.

**Why this matters**: Aligns with `web-native-output` (compose naturally with standard web tooling) and `unchanged-authoring` (the author's job ends at render time; post-processing is not their problem).

**Who benefits**: Academics and educators who use RevealJS for presentations and want Manim animations without video hosting overhead.

## Acceptance Criteria

- [ ] A JavaScript plugin exists that can be included in a RevealJS presentation with a single `<script>` tag
- [ ] A slide author can point the plugin at a frames directory using a `data-` attribute on a `<section>` element
- [ ] The animation plays automatically when the slide becomes active and stops when the slide is left
- [ ] The animation loops or stops at the final frame based on a configurable attribute
- [ ] No build step, bundler, or Node.js server is required to use the plugin

## Notes

The plugin is a thin JS layer over the SVG frame format defined in REQ-0001. It has no dependency on Manim itself — any tool producing SVG frames with the same naming convention and manifest format could use it.

## References

- **Related Tenets**: `web-native-output`, `unchanged-authoring`
- **Related Requirements**: REQ-0001 (defines the SVG frame format this requirement depends on)

## Progress Updates

### 2026-05-06
Requirement created. Status: Proposed.
