# Choose FrameRudiments rendering and visualisation features

Start with the intended picture, what should drive it, and where it will play.
Use FrameRudiments for encoded Shorts, Canvas-style clips and visualisers.
Use DanceMoves for live playback, input, scrolling and page effects. Reuse the
authorised audio, timing, motion or artwork across the two when their contracts
match. Verify each destination with its own runtime and playback checks.
For live use, choose the released DanceMoves clock, motion and layer/input
primitives for the surface, then check actual cadence and interaction at
delivery widths. [DanceMoves](https://github.com/kieransimkin/DanceMoves) ·
[Live lyric visualisers](dancemoves-lyric-visualisers.md).

## Discover the installed features

Check the current stable release against the exact interpreter used by the
launcher or DanceFlow adapter. These commands enumerate the current native
registry, sprite atlases and declared optional visualiser pins without
rendering. In My Songs, invoke `Tools/FrameRudiments.ps1` in place of
`framerudiments`.

```sh
framerudiments --version
framerudiments renderers
framerudiments sprites
framerudiments visualisers
```

The 0.4.32 registry lists 223 native renderer IDs. The Atlas explains the view
families and source data. Use the gallery to audition their appearance, then
look up the selected ID, input contract and options in the source for the
installed release. Optional runtime entries describe pins. Open and exercise
the selected runtime before relying on it. The native registry, compositor
stages and feedback presets are separate inventories.
[Visualisation Atlas](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/visualisation-atlas.md) ·
[Renderer gallery](https://kieransimkin.github.io/FrameRudiments/) ·
[Project format](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/project-format.md).

For a new scene, try a small set of supported views against the same audio
window and framing. Change one choice at a time when comparing a renderer,
effect stage or signal. Retain the selected renderer ID, input hash, axes or
calibrated band contract, parameter values and a matching checkpoint.

## Match the image to its source signal

| Intended result | Native route and what to verify |
| --- | --- |
| Music-synchronised choreography, sprite motion and plotted trails | Choose a named, table, composite or matched DanceRudiment, or a bounded native recording. Select explicit axes, time origin, limits and history. Use native `particles`, signed bars, paths, waveform or phase views for motion channels. Label their data accordingly. [Rudiment renderers](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/rudiment-renderers.md). |
| Audio-frequency bars, circular plots, spectrograms, waterfalls and peak holds | Use saved, calibrated StemLab Fourier bands for the exact programme and interval. Choose band scale, history, palette and peak/hold style. Retain the per-frame analysis sidecar where produced. Keep uncalibrated motion, audio true peak and measured band data distinct. [Spectrum](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/spectrum.md) · [Annular views and modulation](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/annular-modulation.md). |
| Illustrated motion, native vector petals, sparks, smoke and weather | Use sprite or atlas layers with pinned hashes, `rangoli` for vector petal geometry, or cue/continuous/hybrid emitters. Choose opacity, bounds, sprite raster scale, source/cue gates and particle lifetime. Inspect full extent and clear frames. [Sprite visualisations](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/sprite-visualisations.md) · [Rangoli](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/rangoli.md) · [Emitters](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/particle-smoke.md) · [Fire and ice](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/natural-materials.md). |
| Multiple stems influencing the same scene | Pin each recording and map each source to a visible control, viewport or independently drawn layer. Use `stem_sources` and `stem_blend` with compatible native dimensions. Keep calibrated bands on their supported spectral route. [Multi-stem modulation](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/multi-stem-modulation.md). |
| 3D surfaces, lighting and music-reactive meshes | Audition wireframe, depth-buffered solid or music-reactive torus, sphere and terrain. Supply the native controls and the required calibrated spectral history for frequency geometry. Verify depth, occlusion, light, fog and any optional GPU path at the intended viewport. [Spatial renderers](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/spatial-renderers.md) · [Solid 3D](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/solid-spatial-renderers.md) · [Music-reactive 3D](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/music-reactive-3d.md). |
| Line lyrics, active words, lyric art and readable titles | Use pinned LRC/CUE, word timing and approved art with the existing caption ledger. Choose text styling, per-word effects, sprite indicators and clean overlays. Inspect exact caption onsets, clears, wraps, punctuation and phone-safe areas. [Word timing](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/variable-bpm-word-subtitles.md) · [Rich lyrics](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/rich-lyric-effects.md). |

![Native vector petal rings and caption in an actual synthetic FrameRudiments frame](https://raw.githubusercontent.com/kieransimkin/FrameRudiments/v0.4.32/docs/media/rangoli.png)

The synthetic rangoli example combines native motion axes, petal geometry and
pinned typography. [Play the demonstration](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/media/rangoli.mp4) ·
[Transcript](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/media/rangoli-transcript.md).

## Choose where to apply each effect

| Intended result | Native route and what to verify |
| --- | --- |
| Mask, key, crop or move one layer | Use earlier-surface alpha/luma track mattes, keyframed masks, layer animation, clips and displacement. For a graph, bind an isolated layer, background or composed frame as appropriate. Check visible and original alpha through mask, key, despill, edge cleanup and transformed geometry. [Project compositing](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/phase3-compositing.md) · [Graph mattes and keying](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/effect-graph-m3-mattes-and-keying.md). |
| Stylise or generate a surface | Choose a scoped post effect or a graph node for alpha-derived shadow/glow/bevel/relief, overlays and blending, blur and colour treatments, pixelation, pixel sorting, dithering, scanlines, CRT or glitch. Use procedural fields and the fractal library for deterministic textures, masks, control maps and Julia, Mandelbrot and related surfaces. Inspect alpha, clipping, seams, seeds and authored parameter extremes. [Scoped passes](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/scoped-post-effects.md) · [Layer styles](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/effect-graph-m6-5-style-contract.md) · [Raster effects](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/effect-graph-m7-4-raster-effects.md) · [Fields](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/effect-graph-m7-5-procedural-fields.md) · [Fractals](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/fractal-library.md). |
| Change between two sources | Choose matte, spectral, geometric or rain wash transitions. Compose chains and use the project beat or source-beat clock when the transition needs easing, reversal or repeats. Inspect both ends and the midpoint across audio repeat boundaries. [Transition chains](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/effect-graph-m5-4-transition-chains.md) · [Beat timing](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/effect-graph-m5-5-beat-timed-transitions.md) · [Rain wash](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/raindrop-ripples.md#wash-away-transition). |
| Deform a layer, a map or the full frame | Use `spatial_warp` for wave, turbulence, swirl, radial, mirror, kaleidoscope, polar unwrap/wrap, RGBA map displacement and raindrop rings/droplets/storm. Spectral colour-band displacement operates on image colours. Resolve the border, map channels, amplitude, centre and other controls against the tagged reference. Inspect original-alpha alignment, the polar seam and contrasting source edges. [GPU spatial warps and comparisons](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/effect-graph-m8-9-gpu-spatial.md) · [Spectral colour-band displacement](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/effect-graph-m4-spectral.md). |
| Give selected material a feedback history | Use ordered Butterchurn or projectM `effects` with pinned authorised presets and verified PCM mapping. Use feed windows, clean overlays and stage injections deliberately. Inspect the applicable stage input, feedback writeback, output grade/key/matte/underlay and preset timeline. Replay preceding frames for any comparison. [Routing](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/visualiser-routing.md) · [Feedback stages and processing scale](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/visualisers.md). |

The CPU rain wash mixes two sources. The GPU raindrop layer warp refracts one
source. Choose the operation by its compositing role. A clean caption can use
its own layer or the documented feedback overlay route. Inspect the encoded
result with the effect active. For exact node fields and backend support, use
the released project format and the relevant tagged graph contract.
[Graph milestones and released scope](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/unified-effects-transitions-rendering-roadmap.md).

## Choose and verify the effect-graph backend

- `cpu` is the default and supplies the reference. Use `auto` for new or
  revised projects when a supported GPU path is useful and CPU fallback is
  acceptable. `auto` can combine GPU islands with CPU nodes. Use `gpu` for a
  required GPU route or an isolated qualification. Install the optional
  `gpu` extra into the exact interpreter and confirm a working OpenGL context.
  The project-level field is `"effect_graph_backend": "auto"` alongside the
  existing `effect_graph`. Butterchurn/projectM and 3D have their own runtime
  checks. [Mixed graph support](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/effect-graph-m8-8-gpu-islands.md).
- Run the project `plan`, then an appropriately sized sequential `preflight`
  at representative dimensions and temporal settings. Exercise the difficult
  values, seams, fades and cue changes. `--max-frames` checks only an opening
  prefix. For a later state, continue the true sequence through it when
  history matters. Retain pinned input hashes and the resulting composition
  report with the render. [Bounded preflight](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/bounded-preflight.md).
- Inspect `composition.effect_graph_backend` in the manifest. Record
  `requested`, `actual`, the active renderer where present, `last_dispatch`
  and `last_transport`. Use the dispatch counts to distinguish a GPU context
  from actual GPU work and CPU fallback. When `sampling.scope` is
  `last_subframe`, the dispatch and transport describe that last temporal
  sample. Retain both sample and encoded fps. Warm target reuse and retained
  RGBA payload describe the pool. Optional NVIDIA/ATI memory snapshots have
  their own device or pool scope and can be unavailable. [Pool, transfer and memory contract](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/effect-graph-m8-9-gpu-resources.md).
- To accept a new GPU host or driver for the warp path, use the matching 0.4.32+ wheel and source
  archive, using the same interpreter that renders. Run the command below
  from the source root with a fresh receipt path and an expected model
  substring for that host. The small fixtures cover all ten warp types.
  The selected size applies to the stress and pooling checks. Start at 1080p
  and repeat at 4K for that delivery size where practical. Keep the OS
  adapter/model/driver inventory for physical acceptance. Mesa/EGL software
  validation and an actual AMD or Intel GPU are different test environments.
  The fixture timings exclude the rest of composition and encoding.
  [Host qualification](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/effect-graph-m8-9-gpu-resources.md#qualify-another-opengl-renderer).

```sh
python integration/qualify_effect_graph_m8_9.py --size hd --expect-vendor nvidia --expect-renderer "RTX 4060 Ti" --output new-host-hd.json
```

![Identical benchmark pixels with target allocation versus reuse on a warm RTX 4060 Ti frame](https://raw.githubusercontent.com/kieransimkin/FrameRudiments/v0.4.32/docs/media/effect-graph-m8-9-resources.png)

The actual benchmark image shows two fresh targets with pooling disabled
and two reused targets with pooling enabled. The 60 fps recording shows
the counters across changing frames. [Play the target-reuse demonstration](https://kieransimkin.co.uk/2026/11/13/framerudiments-reusing-gpu-render-targets/).

## Author, audition and finish

Use the matching released authoring workspace and React Timeline Sequence for
timeline editing, keyframes and exported draft changes. A fast interactive
preview helps author isolated scenes. Use the real sequential renderer to
compare feedback history. Put release-specific drawing in the project's
trusted scene hook when the built-in layers need a custom layout. Keep the
shared frame loop, timing, effects and encoder. For a new preset experiment, use bounded
`presets-profile` or the tagged source tools for a small controlled audio
response and contact-sheet comparison. Reuse existing captures and measured
temporal evidence first. Limit new processing to the conditions needed.
[Authoring](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/authoring-workspace.md) ·
[Preset profiling](framerudiments-preset-profiling.md) ·
[Hybrid preset analysis](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/hybrid-preset-analysis.md).

Retain the 60 fps target for previews and final motion. Record the chosen
dimensions, spatial scale, subframe sampling, AA, preset scale and actual
runtime separately. When cost matters, measure a representative bounded
comparison at those settings before choosing the render owner. Use the
native chunk/resume/cache path when appropriate, with the frozen project and
sequential state replay. Inspect matching pre-effect, post-effect and decoded
checkpoints where available, then play the exact encoded motion and check
captions, safe areas, seams, cadence and soundtrack. Retain the exact file
hash, native technical health and separate human review evidence.
[Render workflow](framerudiments-rendering.md) ·
[Encoded verification](rendered-video-verification.md) ·
[Spatial and temporal sampling](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/spatiotemporal-supersampling.md).

![Generated diagram showing an opening sequential preflight and its untested remainder](https://raw.githubusercontent.com/kieransimkin/FrameRudiments/v0.4.32/docs/media/bounded-preflight.svg)

The illustration describes the prefix scope. It explains which later frames
still need inspection.

## Potential problems

- **A plan reports `GPU matte effects need the optional moderngl GPU extra`.**
  Check the interpreter used by the failing launcher or DanceFlow adapter and
  import ModernGL there. A separate older runtime can fail even when the direct
  launcher works. Select the verified environment through the owning config,
  then run the same plan in a fresh process and verify the actual route in
  preflight. Keep the running job's pinned environment.
- **Strict GPU rejects `warp_precision_limit_exceeded`.** Check resolved
  settings and the active driver. A polar radius below 16 pixels or extreme
  rain can need `GL_ARB_gpu_shader5`. Where fallback is acceptable, preflight
  a new `auto` candidate and compare those states with the CPU reference.
  Record the actual fallback and measure its render cost. Keep the authored
  range when the pixels pass. Where GPU is required, retain the failure and
  qualify the intended host. [Precision settings](https://github.com/kieransimkin/FrameRudiments/blob/v0.4.32/docs/effect-graph-m8-9-gpu-spatial.md#full-range-warps).
- **An effect appears in the plan while the picture looks unchanged.** Check
  source IDs, visibility, bounds, mix, clean overlay order and actual backend
  dispatch. Compare time-matched source and decoded frames around onset and
  extrema. Use a fresh sequential prefix for a stateful scene and verify the
  intended runtime/source before changing the preset.
- **A fixture passed and the production graph behaves differently.** Repeat
  the project preflight with its actual parameters, resolution, temporal
  sampling and layers. Check which cases and frames were observed. Use exact
  final encode checks for the film.
- **The launcher reports `work_cache requires a complete peak reserve_bytes estimate`.**
  Check for a configured working-cache path, including one supplied by the
  launcher. Pass `--reserve-gib` with the estimated complete peak payload and
  check available cache and final capacity. The My Songs synthetic fixture
  passed with an explicit project-local `--work-cache` and a bounded
  reservation. Verify final promotion and an empty cache after handoff.
  [Cache and reservation workflow](framerudiments-rendering.md#use-a-separate-fast-working-cache-when-final-storage-is-contended).
