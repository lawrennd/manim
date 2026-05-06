---
id: "2026-05-06_cip0001-step6-filewriter-manifest"
title: "CIP-0001 Step 6: SceneFileWriter integration and JSON manifest"
status: "Completed"
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

- [x] Output directory structure matches expected layout (`media/svg/SceneName/animation_N/frame_NNNN.svg`)
- [x] `animation.json` contains `{"fps": N, "frame_count": N, "width": N, "height": N}`
- [x] Frame numbering is zero-padded to 4 digits
- [x] Output directory is created automatically
- [x] Multiple `self.play()` calls produce separate `animation_N/` directories
- [x] `scene_finished()` handles static scenes (no `play()` calls)

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

Implemented as part of Step 1 in scene_file_writer.py:
- `open_svg_output()`, `write_svg_frame()`, `close_svg_output()` all working
- Output structure and manifest verified via smoke tests throughout Steps 2-5

Status: Completed.
