"""SVG camera: converts Manim scene mobjects into an svgwrite Drawing.

This module is part of CIP-0001 (SVG Renderer for Web Export).
"""

from __future__ import annotations

__all__ = ["SVGCamera"]

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from .. import config

if TYPE_CHECKING:
    from ..mobject.mobject import Mobject


class SVGCamera:
    """Camera that renders the scene to an svgwrite Drawing instead of a pixel buffer.

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

    def reset(self) -> None:
        """Create a fresh SVG drawing for the next frame."""
        import svgwrite

        self._current_drawing = svgwrite.Drawing(
            size=(f"{self.pixel_width}px", f"{self.pixel_height}px"),
            viewBox=(
                f"{-self.frame_width / 2} "
                f"{-self.frame_height / 2} "
                f"{self.frame_width} "
                f"{self.frame_height}"
            ),
        )

    def capture_mobjects(
        self,
        mobjects: Iterable[Mobject],
        **kwargs: Any,
    ) -> None:
        """Render mobjects into the current SVG drawing.

        .. note::
            This is a stub implementation (CIP-0001 Step 1). Full VMobject-to-SVG
            path conversion is implemented in Step 2.
        """
        if self._current_drawing is None:
            self.reset()

    def get_drawing(self) -> Any:
        """Return the current frame's SVG drawing, creating one if needed.

        Returns
        -------
        svgwrite.Drawing
            The drawing populated by the most recent :meth:`capture_mobjects` call.
        """
        if self._current_drawing is None:
            self.reset()
        assert self._current_drawing is not None
        return self._current_drawing
