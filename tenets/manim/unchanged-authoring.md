---
id: "unchanged-authoring"
title: "The Authoring Workflow is Unchanged"
status: "Active"
created: "2026-05-06"
last_reviewed: "2026-05-06"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- usability
- api
---

# Tenet: The Authoring Workflow is Unchanged

## Tenet

**Description**: A scene author should not need to know anything about SVG, RevealJS, or web rendering to use the SVG renderer. The only change visible to the author is a flag or configuration option at render time (`--format svg` or equivalent). Existing scenes, existing `construct()` methods, and existing animation patterns all continue to work without modification.

This tenet protects the author experience. Manim is already a complex system; adding a new rendering target should not add new concepts to the authoring layer. If a feature cannot be supported without API changes, document it as a limitation rather than changing the API.

**Quote**: *"Change the flag, not the scene."*

**Examples**:
- A scene that currently renders to MP4 can be rendered to SVG frames with only a `--format svg` flag change
- `VMobject`, `MathTex`, `ImageMobject`, and all standard mobject types work without modification
- The `construct()` method, `self.play()`, `self.wait()`, and `self.add()` patterns are unchanged
- Animation subclasses (`FadeIn`, `Transform`, `Create`, etc.) require no changes

**Counter-examples**:
- Requiring authors to subclass a new `SVGScene` base class instead of `Scene`
- Introducing a new `self.svg_play()` method that authors must remember to use instead of `self.play()`
- Requiring authors to annotate mobjects with SVG-specific metadata
- Changing the default frame rate or timing behavior when SVG format is selected

**Conflicts**:
- None identified; this tenet is a near-absolute constraint on the authoring API
