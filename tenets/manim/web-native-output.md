---
id: "web-native-output"
title: "Web-Native Output"
status: "Active"
created: "2026-05-06"
last_reviewed: "2026-05-06"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- web
- interoperability
---

# Tenet: Web-Native Output

## Tenet

**Description**: The output of the SVG renderer should compose naturally with standard web tooling — RevealJS, plain HTML `<img>` tags, `<iframe>` embeds, static site generators — without requiring a custom runtime, a specific bundler, or a proprietary player. The SVG frame format should be self-describing and consumable by any reasonable web context.

This means: numbered SVG files with predictable naming (`frame_0001.svg`, `frame_0002.svg`, ...), a simple JSON manifest describing frame count and fps, and a JS helper that is optional rather than mandatory. A user should be able to embed an animation using nothing more than a `<img>` tag and a ten-line `setInterval` loop if they choose. The RevealJS plugin is a convenience on top of this, not a requirement.

**Quote**: *"Any web context, no custom runtime required."*

**Examples**:
- Numbered SVG files with a predictable naming scheme consumable by any script
- A JSON manifest (`animation.json`) alongside frames so the JS side knows frame count and fps without parsing filenames
- The RevealJS plugin is ~50 lines of vanilla JS with no build step required
- An author can host the SVG frames on any static file server and link to them

**Counter-examples**:
- Requiring a specific Node.js server to serve animations
- Encoding all frames into a single proprietary binary format that requires the `manim-svg` runtime to decode
- Making the RevealJS plugin depend on a specific version of webpack or a JS bundler
- Using Web Components that require a polyfill for broad browser compatibility

**Conflicts**:
- None identified at present
