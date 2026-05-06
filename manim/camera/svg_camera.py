"""SVG camera: converts Manim scene mobjects into an svgwrite Drawing.

This module is part of CIP-0001 (SVG Renderer for Web Export).
"""

from __future__ import annotations

__all__ = ["SVGCamera"]

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

import numpy as np

from .. import config, logger

if TYPE_CHECKING:
    from ..mobject.mobject import Mobject


class SVGCamera:
    """Camera that renders the scene to an svgwrite Drawing instead of a pixel buffer.

    Each call to :meth:`reset` + :meth:`capture_mobjects` produces one SVG frame.
    The frame is accumulated in :attr:`_current_drawing` and retrieved via
    :meth:`get_drawing`.

    Coordinate system
    -----------------
    Manim uses a centred, y-up coordinate space. SVG uses a top-left, y-down space.
    This camera emits path coordinates with y negated so that Manim's y-up geometry
    displays correctly inside the SVG ``viewBox`` (which spans Manim's x-range but
    with y-down). The ``viewBox`` is set on the root ``<svg>`` element in
    :meth:`reset`.

    Attributes
    ----------
    frame_rate : float
        Frames per second, read from ``config["frame_rate"]``.
    frame_width : float
        Scene frame width in Manim coordinate units.
    frame_height : float
        Scene frame height in Manim coordinate units.
    pixel_width : int
        Output pixel width of each SVG frame.
    pixel_height : int
        Output pixel height of each SVG frame.
    use_z_index : bool
        Whether to sort mobjects by z-index (always ``True`` for SVGCamera).
    """

    def __init__(self) -> None:
        try:
            import svgwrite  # noqa: F401
        except ImportError as exc:
            raise ImportError(
                "The SVG renderer requires the 'svgwrite' package. "
                "Install it with: pip install manim[svg]"
            ) from exc

        self.frame_rate: float = config["frame_rate"]
        self.frame_width: float = config["frame_width"]
        self.frame_height: float = config["frame_height"]
        self.pixel_width: int = config["pixel_width"]
        self.pixel_height: int = config["pixel_height"]
        self.use_z_index: bool = True
        self._current_drawing: Any | None = None

    # ------------------------------------------------------------------
    # Frame lifecycle
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Create a fresh SVG drawing for the next frame.

        Coordinate system
        ~~~~~~~~~~~~~~~~~
        The SVG ``viewBox`` spans Manim's x-range (centred at 0) and the
        equivalent y-range.  Path coordinates are emitted with ``y`` negated
        (``-y``) so that Manim's y-up convention maps correctly to SVG's y-down
        convention: positive-y Manim objects appear above centre in the browser.

        This is equivalent to wrapping all paths in
        ``<g transform="scale(1,-1)">`` but avoids the extra group element.

        A solid background rectangle is added first so the scene has the
        correct background colour in any browser context (SVG default is
        transparent).
        """
        import svgwrite

        bg_color: str = config["background_color"].to_hex()

        self._current_drawing = svgwrite.Drawing(
            size=(f"{self.pixel_width}px", f"{self.pixel_height}px"),
            viewBox=(
                f"{-self.frame_width / 2} "
                f"{-self.frame_height / 2} "
                f"{self.frame_width} "
                f"{self.frame_height}"
            ),
        )

        # Background rectangle covering the full viewBox.
        self._current_drawing.add(
            self._current_drawing.rect(
                insert=(-self.frame_width / 2, -self.frame_height / 2),
                size=(self.frame_width, self.frame_height),
                fill=bg_color,
            )
        )

    def get_drawing(self) -> Any:
        """Return the current frame's SVG drawing.

        Returns
        -------
        svgwrite.Drawing
            The drawing populated by the most recent :meth:`capture_mobjects` call.
        """
        if self._current_drawing is None:
            self.reset()
        assert self._current_drawing is not None
        return self._current_drawing

    # ------------------------------------------------------------------
    # Mobject dispatch
    # ------------------------------------------------------------------

    def capture_mobjects(
        self,
        mobjects: Iterable[Mobject],
        **kwargs: Any,
    ) -> None:
        """Render *mobjects* into the current SVG drawing.

        Recurses into submobjects. Each :class:`.VMobject` with geometry is
        rendered as one or more SVG ``<path>`` elements. Other mobject types
        (``ImageMobject``, 3-D objects) emit a debug warning and are skipped
        until their dedicated implementation steps.

        Parameters
        ----------
        mobjects
            Top-level mobjects to render (submobjects are visited recursively).
        """
        if self._current_drawing is None:
            self.reset()

        for mob in mobjects:
            self._capture_mobject(mob)

    def _capture_mobject(self, mob: Mobject) -> None:
        """Dispatch a single mobject to the appropriate render method."""
        from ..mobject.types.image_mobject import AbstractImageMobject
        from ..mobject.types.vectorized_mobject import VMobject

        if isinstance(mob, AbstractImageMobject):
            self._render_image_mobject(mob)
        elif isinstance(mob, VMobject):
            self._render_vmobject(mob)
        else:
            logger.debug(
                "SVGCamera: skipping unsupported mobject type %s "
                "(will be handled in a future CIP-0001 step)",
                type(mob).__name__,
            )

    # ------------------------------------------------------------------
    # ImageMobject rendering
    # ------------------------------------------------------------------

    def _render_image_mobject(self, image_mob: Any) -> None:
        """Render an ImageMobject as a base64-encoded PNG ``<image>`` element.

        Parameters
        ----------
        image_mob
            An :class:`.ImageMobject` (or any ``AbstractImageMobject``).

        Notes
        -----
        ``ImageMobject.pixel_array`` is a uint8 RGBA numpy array of shape
        ``(H, W, 4)``.  We encode it as an in-memory PNG and embed it via a
        ``data:image/png;base64,...`` data URI so no external files are needed.

        The bounding box comes from ``image_mob.points``, which stores the
        four corner points in Manim space::

            points[0] = top-left
            points[1] = top-right
            points[2] = bottom-left
            points[3] = bottom-right

        In SVG y-down space (with y negated), the top-left insert is
        ``(points[0][0], -points[0][1])`` and the size is
        ``(width, height)``.
        """
        import base64
        import io

        from PIL import Image as PILImage

        pixel_array = image_mob.pixel_array
        if pixel_array is None or pixel_array.size == 0:
            return

        # Encode pixel_array as PNG in memory.
        pil_img = PILImage.fromarray(pixel_array.astype("uint8"), mode="RGBA")
        buf = io.BytesIO()
        pil_img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        href = f"data:image/png;base64,{b64}"

        # Bounding box from corner points (Manim space, y negated for SVG).
        points = image_mob.points
        x_left = float(points[0][0])
        y_top_svg = float(-points[0][1])  # negate y: Manim top → SVG top
        w = float(image_mob.width)
        h = float(image_mob.height)

        img_el = self._current_drawing.image(
            href=href,
            insert=(x_left, y_top_svg),
            size=(w, h),
            preserveAspectRatio="none",
        )
        self._current_drawing.add(img_el)

    # ------------------------------------------------------------------
    # VMobject rendering
    # ------------------------------------------------------------------

    def _render_vmobject(self, vmob: Any) -> None:
        """Render a VMobject and all its submobjects as SVG path elements."""
        # Render submobjects first (behind the parent).
        for submob in vmob.submobjects:
            from ..mobject.types.vectorized_mobject import VMobject

            if isinstance(submob, VMobject):
                self._render_vmobject(submob)

        # Render this vmobject's own geometry.
        if len(vmob.points) == 0:
            return

        path_data = self._vmobject_to_svg_path_data(vmob)
        if not path_data:
            return

        stroke_color = vmob.get_stroke_color()
        stroke_opacity = float(vmob.get_stroke_opacity())
        stroke_width = vmob.get_stroke_width()

        fill_color = vmob.get_fill_color()
        fill_opacity = float(vmob.get_fill_opacity())

        svg_stroke = stroke_color.to_hex() if stroke_color and stroke_opacity > 0 else "none"
        svg_fill = fill_color.to_hex() if fill_color and fill_opacity > 0 else "none"

        # Convert Manim stroke width (in coordinate units) to SVG stroke-width.
        # Manim's default stroke width is 4 (in some internal unit); scale it to
        # be visually comparable to Cairo output. A factor of ~0.03 maps Manim
        # units to SVG coordinate units at standard frame size.
        svg_stroke_width = stroke_width * self.frame_width / self.pixel_width * 4

        path_el = self._current_drawing.path(
            d=path_data,
            stroke=svg_stroke,
            stroke_width=svg_stroke_width if svg_stroke != "none" else 0,
            stroke_opacity=stroke_opacity if svg_stroke != "none" else 0,
            fill=svg_fill,
            fill_opacity=fill_opacity if svg_fill != "none" else 0,
            fill_rule="evenodd",
        )
        self._current_drawing.add(path_el)

    def _vmobject_to_svg_path_data(self, vmob: Any) -> str:
        """Convert a VMobject's Bézier geometry to an SVG path ``d`` attribute.

        Parameters
        ----------
        vmob
            A :class:`.VMobject` whose ``points`` will be serialised.

        Returns
        -------
        str
            SVG path data string, or empty string if the vmobject has no subpaths.

        Notes
        -----
        Manim stores paths as a flat array of shape ``(N, 3)`` where every group
        of four consecutive points is one cubic Bézier segment:
        ``[anchor_start, handle_out, handle_in, anchor_end]``.

        :meth:`.VMobject.get_subpaths` splits the flat array into continuous
        sub-paths (lifting the pen where anchors are not shared).

        Y-coordinates are negated to convert from Manim's y-up convention to
        SVG's y-down convention.
        """
        subpaths = vmob.get_subpaths()
        if not subpaths:
            return ""

        parts: list[str] = []
        nppcc = vmob.n_points_per_cubic_curve  # always 4

        for subpath in subpaths:
            # subpath is shape (k*4, 3); groups of nppcc are one cubic segment.
            num_segments = len(subpath) // nppcc
            if num_segments == 0:
                continue

            # First anchor: Move-to.
            a0 = subpath[0]
            parts.append(f"M {a0[0]:.6f},{-a0[1]:.6f}")

            for seg_idx in range(num_segments):
                pts = subpath[seg_idx * nppcc : (seg_idx + 1) * nppcc]
                # pts[0] = anchor_start (already moved to)
                # pts[1] = handle_out of anchor_start
                # pts[2] = handle_in  of anchor_end
                # pts[3] = anchor_end
                h1, h2, a1 = pts[1], pts[2], pts[3]
                parts.append(
                    f"C {h1[0]:.6f},{-h1[1]:.6f} "
                    f"{h2[0]:.6f},{-h2[1]:.6f} "
                    f"{a1[0]:.6f},{-a1[1]:.6f}"
                )

            # Close the subpath if its first and last anchors coincide.
            if vmob.consider_points_equals(subpath[0], subpath[-1]):
                parts.append("Z")

        return " ".join(parts)
