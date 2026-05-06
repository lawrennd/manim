---
id: "2026-05-06_cip0001-step5-imagemobject"
title: "CIP-0001 Step 5: ImageMobject support via base64 data URI"
status: "Completed"
priority: "Medium"
created: "2026-05-06"
last_updated: "2026-05-06"
owner: ""
dependencies:
- "2026-05-06_cip0001-step3-coordinate-transform"
related_cips:
- "0001"
tags:
- cip0001
- imagemobject
- raster
- base64
---

# Task: CIP-0001 Step 5 — ImageMobject Support via Base64 Data URI

## Description

Handle `ImageMobject` in `SVGCamera.capture_mobjects`. Since `ImageMobject` is inherently raster, it cannot be represented as vector paths. Instead, base64-encode the pixel array as a PNG and embed it as an SVG `<image>` element with a data URI. This keeps the SVG self-contained (no external file references).

## Acceptance Criteria

- [x] `ImageMobject` produces SVG frames with an `<image>` element containing a base64 PNG data URI
- [x] The image appears at the correct position and size (bounding box from `image_mob.points`, y-negated for SVG)
- [x] The SVG file is self-contained (no external file references — data URI only)
- [ ] Browser compatibility testing — deferred to manual validation phase
- [x] `AbstractImageMobject` check in dispatch so all subclasses are handled

## Implementation Notes

`ImageMobject` stores pixel data in `self.pixel_array` (numpy RGBA array). To embed:

```python
import base64, io
from PIL import Image

img = Image.fromarray(pixel_array)
buf = io.BytesIO()
img.save(buf, format="PNG")
b64 = base64.b64encode(buf.getvalue()).decode()
href = f"data:image/png;base64,{b64}"
```

Then emit:
```xml
<image href="..." x="..." y="..." width="..." height="..." />
```

Position and size come from the mobject's bounding box in Manim coordinates, converted via the same coordinate transform as Step 3.

Can run in parallel with Step 4 since it depends only on Step 3.

## Related

- CIP: 0001 (Step 5 of 8)
- Requirements: REQ-0001 (complete scene export)

## Progress Updates

### 2026-05-06
Task created. Status: Proposed (depends on Step 3, can run in parallel with Step 4).

Implemented `SVGCamera._render_image_mobject`:
- Uses `PIL.Image.fromarray` + `io.BytesIO` to encode pixel_array as PNG
- Embeds via `data:image/png;base64,...` href on svgwrite `<image>` element
- Position from `image_mob.points[0]` (top-left corner, y negated for SVG)
- Size from `image_mob.width` / `image_mob.height`
- Dispatch added to `_capture_mobject` via `isinstance(mob, AbstractImageMobject)` check

Tested with a 4×4 RGBA test image — correct `x=-1.5, y=-1.5` position for
a 3-unit square image centred at origin.

Status: Completed.
