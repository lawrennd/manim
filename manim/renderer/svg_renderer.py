"""SVG renderer: drives per-frame SVG export of Manim scenes.

This module is part of CIP-0001 (SVG Renderer for Web Export).
The renderer follows the same interface as :class:`.CairoRenderer` so that
``Scene`` can substitute it transparently when ``config.renderer == RendererType.SVG``.
"""

from __future__ import annotations

__all__ = ["SVGRenderer"]

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from ..camera.svg_camera import SVGCamera
from ..scene.scene_file_writer import SceneFileWriter
from ..utils.iterables import list_update

if TYPE_CHECKING:
    from ..animation.animation import Animation
    from ..mobject.mobject import Mobject, _AnimationBuilder
    from ..scene.scene import Scene


class SVGRenderer:
    """A renderer that exports each frame as an SVG file.

    Produces a directory of numbered SVG files alongside an ``animation.json``
    manifest for each :meth:`.Scene.play` call. A companion JavaScript plugin
    (``js/manim-svg.js``) uses these files to play the animation in a browser
    or RevealJS presentation.

    Attributes
    ----------
    num_plays : int
        Number of :meth:`.Scene.play` calls completed.
    time : float
        Elapsed scene time in seconds.
    """

    def __init__(self, skip_animations: bool = False) -> None:
        self.camera: SVGCamera = SVGCamera()
        self.skip_animations: bool = skip_animations
        self._original_skipping_status: bool = skip_animations
        self.num_plays: int = 0
        self.time: float = 0.0

    def init_scene(self, scene: Scene) -> None:
        """Attach the file writer to this renderer."""
        self.file_writer: SceneFileWriter = SceneFileWriter(
            self,
            scene.__class__.__name__,
        )

    def play(
        self,
        scene: Scene,
        *args: Animation | Mobject | _AnimationBuilder,
        **kwargs: Any,
    ) -> None:
        """Render all animations in a single :meth:`.Scene.play` call to SVG frames."""
        self.skip_animations = self._original_skipping_status

        scene.compile_animation_data(*args, **kwargs)

        self.file_writer.open_svg_output()
        self.file_writer.begin_animation(not self.skip_animations)
        scene.begin_animations()

        if scene.is_current_animation_frozen_frame():
            self.update_frame(scene)
            num_frames = max(1, round(scene.duration * self.camera.frame_rate))
            drawing = self.camera.get_drawing()
            self.file_writer.write_svg_frame(drawing, num_frames=num_frames)
            self.time += scene.duration
        else:
            scene.play_internal()

        self.file_writer.end_animation(not self.skip_animations)
        self.file_writer.close_svg_output()

        self.num_plays += 1

    def update_frame(
        self,
        scene: Scene,
        mobjects: Iterable[Mobject] | None = None,
        **kwargs: Any,
    ) -> None:
        """Rebuild the current SVG drawing from the scene's mobjects.

        Unlike :class:`.CairoRenderer`, the SVG renderer has no concept of a
        static background layer, so it always renders all visible mobjects
        (``scene.mobjects + scene.foreground_mobjects``). The ``mobjects``
        parameter is accepted for API compatibility but ignored.
        """
        if self.skip_animations:
            return
        self.camera.reset()
        all_mobjects: list[Mobject] = list_update(
            scene.mobjects, scene.foreground_mobjects
        )
        self.camera.capture_mobjects(all_mobjects, **kwargs)

    def render(
        self,
        scene: Scene,
        time: float,
        moving_mobjects: Iterable[Mobject] | None = None,
    ) -> None:
        """Render one frame and write it to disk."""
        self.update_frame(scene, moving_mobjects)
        drawing = self.camera.get_drawing()
        self.file_writer.write_svg_frame(drawing)
        dt = 1.0 / self.camera.frame_rate
        self.time += dt

    def scene_finished(self, scene: Scene) -> None:
        """Called by :meth:`.Scene.render` after ``construct()`` completes."""
        if not self.num_plays:
            # No animations were played — render a single static frame.
            self.file_writer.open_svg_output()
            self.update_frame(scene)
            drawing = self.camera.get_drawing()
            self.file_writer.write_svg_frame(drawing)
            self.file_writer.close_svg_output()
