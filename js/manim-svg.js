/**
 * manim-svg.js — RevealJS plugin for Manim SVG animations
 *
 * Usage
 * -----
 * 1. Export your Manim scene with --renderer svg (or config.renderer = RendererType.SVG).
 *    This produces:
 *      media/svg/SceneName/
 *        animation_0/
 *          frame_0000.svg ... frame_NNNN.svg
 *          animation.json   { fps, frame_count, width, height }
 *        animation_1/ ...
 *
 * 2. In your RevealJS presentation, include the plugin and add data attributes to slides:
 *
 *    <script src="js/manim-svg.js"></script>
 *    <script>
 *      Reveal.initialize({
 *        plugins: [ManimSVG]
 *      });
 *    </script>
 *
 * 3. On a slide `<section>`, add:
 *
 *    data-manim-svg="media/svg/MyScene/animation_0"
 *
 *    Optional modifiers:
 *      data-manim-loop="true"       — loop continuously (default: false, stops at last frame)
 *      data-manim-fps="10"          — override fps from animation.json
 *      data-manim-autoplay="false"  — don't start automatically (default: true)
 *
 * The plugin creates an <img> element inside the slide that cycles through the
 * SVG frames.  The container is positioned to fill the slide area.
 *
 * Notes
 * -----
 * - No build step, bundler, or Node.js required.
 * - SVG frames are fetched via relative URL; serve from the same origin as the HTML.
 * - Tested with RevealJS 4.x.
 */

'use strict';

const ManimSVG = (() => {
  /** Map from slide element to its active animation state. */
  const _state = new WeakMap();

  /**
   * Pad a number to `width` digits with leading zeros.
   * @param {number} n
   * @param {number} width
   * @returns {string}
   */
  function zeroPad(n, width) {
    return String(n).padStart(width, '0');
  }

  /**
   * Load the animation.json manifest from `dir`.
   * @param {string} dir  Path to the animation directory (no trailing slash).
   * @returns {Promise<{fps: number, frame_count: number, width: number, height: number}>}
   */
  async function loadManifest(dir) {
    const url = `${dir}/animation.json`;
    const resp = await fetch(url);
    if (!resp.ok) {
      throw new Error(`manim-svg: failed to fetch ${url} (${resp.status})`);
    }
    return resp.json();
  }

  /**
   * Pre-load all SVG frames for an animation directory.
   * Returns an array of blob-URL strings so frames display instantly.
   *
   * @param {string} dir
   * @param {number} frameCount
   * @returns {Promise<string[]>}
   */
  async function preloadFrames(dir, frameCount) {
    const urls = Array.from({ length: frameCount }, (_, i) =>
      `${dir}/frame_${zeroPad(i, 4)}.svg`
    );
    // Fetch all frames in parallel; create blob URLs for instant display.
    const blobs = await Promise.all(
      urls.map(url =>
        fetch(url)
          .then(r => {
            if (!r.ok) throw new Error(`manim-svg: failed to fetch ${url}`);
            return r.blob();
          })
          .then(blob => URL.createObjectURL(blob))
      )
    );
    return blobs;
  }

  /**
   * Stop any running animation on `slide` and clean up its interval.
   * @param {HTMLElement|null} slide
   */
  function stopAnimation(slide) {
    if (!slide) return;
    const s = _state.get(slide);
    if (s) {
      clearInterval(s.intervalId);
      s.intervalId = null;
    }
  }

  /**
   * Start the animation declared on `slide` via `data-manim-svg`.
   * Creates an <img> container if one does not already exist.
   *
   * @param {HTMLElement|null} slide
   */
  async function startAnimation(slide) {
    if (!slide) return;
    const dir = slide.dataset.manimSvg;
    if (!dir) return;

    // Stop any previous run.
    stopAnimation(slide);

    let s = _state.get(slide);
    if (!s) {
      // First visit: load manifest + preload frames.
      let manifest, frames;
      try {
        manifest = await loadManifest(dir);
        frames = await preloadFrames(dir, manifest.frame_count);
      } catch (err) {
        console.error(err);
        return;
      }

      // Create the display <img> element.
      const img = document.createElement('img');
      img.style.cssText =
        'position:absolute;top:0;left:0;width:100%;height:100%;object-fit:contain;';
      img.setAttribute('aria-label', `Manim animation: ${dir}`);
      slide.style.position = 'relative';
      slide.appendChild(img);

      s = {
        manifest,
        frames,
        img,
        currentFrame: 0,
        intervalId: null,
      };
      _state.set(slide, s);
    }

    // Parse per-slide overrides.
    const fps = parseInt(slide.dataset.manimFps ?? s.manifest.fps, 10) || s.manifest.fps;
    const loop = slide.dataset.manimLoop === 'true';
    const autoplay = slide.dataset.manimAutoplay !== 'false';

    if (!autoplay) {
      // Show first frame statically.
      s.img.src = s.frames[0];
      s.currentFrame = 0;
      return;
    }

    // Reset to start.
    s.currentFrame = 0;
    s.img.src = s.frames[0];

    if (s.frames.length <= 1) return;  // single-frame — nothing to animate

    const intervalMs = 1000 / fps;

    s.intervalId = setInterval(() => {
      s.currentFrame += 1;
      if (s.currentFrame >= s.frames.length) {
        if (loop) {
          s.currentFrame = 0;
        } else {
          // Stop at last frame.
          clearInterval(s.intervalId);
          s.intervalId = null;
          s.currentFrame = s.frames.length - 1;
        }
      }
      s.img.src = s.frames[s.currentFrame];
    }, intervalMs);
  }

  /**
   * Scan `slide` for any child `[data-manim-svg]` containers in case the
   * attribute is on a nested element rather than the section itself.
   * Falls back to the slide itself.
   *
   * @param {HTMLElement|null} slide
   * @returns {HTMLElement[]}
   */
  function findAnimationTargets(slide) {
    if (!slide) return [];
    // The attribute may be on the section or on inner containers.
    const inner = Array.from(slide.querySelectorAll('[data-manim-svg]'));
    if (inner.length > 0) return inner;
    if (slide.dataset.manimSvg) return [slide];
    return [];
  }

  return {
    id: 'manim-svg',

    /**
     * Called by RevealJS during initialisation.
     * @param {object} deck  The Reveal deck instance.
     */
    init(deck) {
      // Handle slide transitions.
      deck.on('slidechanged', ({ currentSlide, previousSlide }) => {
        findAnimationTargets(previousSlide).forEach(stopAnimation);
        findAnimationTargets(currentSlide).forEach(startAnimation);
      });

      // Handle fragment visibility (useful for step-by-step reveals).
      deck.on('fragmentshown', ({ fragment }) => {
        findAnimationTargets(fragment).forEach(startAnimation);
      });
      deck.on('fragmenthidden', ({ fragment }) => {
        findAnimationTargets(fragment).forEach(stopAnimation);
      });

      // Start animations on the initial slide.
      findAnimationTargets(deck.getCurrentSlide()).forEach(startAnimation);
    },
  };
})();

// Support both ES-module and classic <script> inclusion.
if (typeof module !== 'undefined') {
  module.exports = ManimSVG;
}
