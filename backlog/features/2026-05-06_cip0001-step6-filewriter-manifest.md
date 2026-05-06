---
id: "2026-05-06_cip0001-step6-filewriter-manifest"
title: "CIP-0001 Step 6: SceneFileWriter integration and JSON manifest"
status: "Proposed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
owner: ""
dependencies:
- "2026-05-06_cip0001-step2-vmobject-svg-path"
related_cips:
- "0001"
tags:
- cip0001
- filewriter
- manifest
- output
---

# Task: CIP-0001 Step 6 — SceneFileWriter Integration and JSON Manifest

## Description

Fully implement `write_svg_frame()`, `open_svg_output()`, and `close_svg_output()` in `SceneFileWriter`. After the last frame of each animation block, write an `animation.json` manifest file describing frame count, fps, and scene dimensions. Establish the final output directory structure.

## Acceptance Criteria

- [ ] Output directory structure matches:
  ```
  media/svg/SceneName/
    animation_0/
      frame_0000.svg
      frame_0001.svg
      ...
      animation.json
    animation_1/
      frame_0000.svg
      ...
      animation.json
  ```
- [ ] `animation.json` contains `{"fps": N, "frame_count": N, "width": N, "height": N}`
- [ ] Frame numbering is zero-padded to 4 digits
- [ ] The output directory is created if it does not exist
- [ ] `scene_finished()` on `SVGRenderer` calls `close_svg_output()` correctly
- [ ] Multiple `self.play()` calls produce separate `animation_N/` directories

## Implementation Notes

Animation block boundaries: `SVGRenderer.play()` calls `open_svg_output()` at start and `close_svg_output()` (which writes the manifest) at end. The animation index increments per `play()` call, matching how partial movie files are numbered in the Cairo renderer.

The manifest is written as:
```python
import json
manifest = {
    "fps": config.frame_rate,
    "frame_count": self._svg_frame_count,
    "width": config.pixel_width,
    "height": config.pixel_height,
}
(output_dir / "animation.json").write_text(json.dumps(manifest, indent=2))
```

## Related

- CIP: 0001 (Step 6 of 8)
- Requirements: REQ-0001 (web-embeddable output format), REQ-0002 (RevealJS embedding — manifest enables the JS plugin)

## Progress Updates

### 2026-05-06
Task created. Status: Proposed (can begin as soon as Step 2 is in place).
