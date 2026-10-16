## Use FrameRudiments for offline rendering

For new or materially revised Shorts, Canvas-style clips and lyric visualisers,
use `Z:/My Songs/Tools/FrameRudiments.ps1` and read
`Z:/My Songs/Workflows/framerudiments-rendering.md`. The canonical package is
https://github.com/kieransimkin/FrameRudiments (`framerudiments` on PyPI).
Reuse its project/frame ledger, captions, layers, native motion adapters,
FFmpeg encoding and technical QA; keep release artwork and choreography in
project files/scene hooks. Preserve old generators for exact historic reproduction.
StemLab owns analysis and selection evidence, DanceRudiments owns native motion
and non-looping recordings, and DanceMoves owns live EPK clocks/input/lifecycle.
Keep source hashes/sample bounds, canonical timing, match windows/offsets,
64 pips versus 16 ticks, platform-safe-zone checks and attended listening gates.
Rendering does not upload, schedule or publish; existing publication and EPK
reconciliation requirements remain authoritative. Extend a demonstrated shared
gap in the proper package with tests/docs rather than copying another engine.

Use modular `type: "rudiment"` views for particles/trails, signed bars, waveform
traces, XY paths and calibrated Fourier spectra. Read the package's
`docs/rudiment-renderers.md` and `docs/spectrum.md`; choose axes, viewports and
bounded history explicitly. Reuse native motion and saved StemLab Fourier
calibration, preserving RMS/gain/normalization, silent bands and source clocks.
Retain `rudiment-analysis.jsonl` for per-frame peaks/holds; frequency-band peaks
and frame-sampled holds do not establish exact pitch or audio true peaks.
Extend the trusted renderer registry for a shared view; avoid another engine.

