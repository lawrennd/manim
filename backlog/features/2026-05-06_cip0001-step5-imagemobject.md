---
id: "2026-05-06_cip0001-step5-imagemobject"
title: "CIP-0001 Step 5: ImageMobject support via base64 data URI"
status: "Proposed"
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

- [ ] A scene containing `ImageMobject("path/to/image.png")` produces an SVG frame with an `<image>` element
- [ ] The image appears at the correct position and size in the frame
- [ ] The SVG file is self-contained (no external file references)
- [ ] The embedded image renders correctly in major browsers
- [ ] A warning is logged noting that `ImageMobject` content is rasterized (precision tenet acknowledgement)

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
