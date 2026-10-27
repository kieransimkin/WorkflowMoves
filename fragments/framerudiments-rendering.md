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

Choose ownership before production encoding. Use an operating-system scheduler
or service only for a full-length video or when a representative bounded
preflight predicts more than 15 minutes; keep every other render inside Codex.
High-quality settings and FrameRudiments' 30-second chunk threshold alone do not
qualify. Record the evidence, arithmetic and decision, never migrate or duplicate
a live render, and reconsider only at a safe new-attempt boundary. FrameRudiments
0.4.14+ `render-progress.json` and flushed stderr heartbeats provide regular
liveness/ETA evidence without proving completion or technical QA.

Use modular `type: "rudiment"` views for particles/trails, signed bars, waveform
traces, XY paths and calibrated Fourier spectra. Read the package's
`docs/rudiment-renderers.md` and `docs/spectrum.md`; choose axes, viewports and
bounded history explicitly. Reuse native motion and saved StemLab Fourier
calibration, preserving RMS/gain/normalization, silent bands and source clocks.
Retain `rudiment-analysis.jsonl` for per-frame peaks/holds; frequency-band peaks
and frame-sampled holds do not establish exact pitch or audio true peaks.
Extend the trusted renderer registry for a shared view; avoid another engine.

Optional ordered `effects` stages use Butterchurn 2.6.7 and projectM 4.2-dev
at exact source `349b7cc2db312d47cef6be24c6856ced6643a385`. Both process the
complete composed frame, including captions, lyric art, DanceRudiments-moving
sprites and beat-animated atlases, before encoding. Choose either engine or a
chain with original feedback, kaleidoscope and Julia-distortion presets.
Read the canonical [visualiser setup and contract](https://github.com/kieransimkin/FrameRudiments/blob/main/docs/visualisers.md).
Use `visualisers` to inspect pins and explicit `effects-setup` to provision a
runtime. Preserve exact output clocks and PCM from the same trim/repeat/fade
chain as the soundtrack. Retain preset/runtime/bridge hashes and cleanup
receipts. Feedback is sequential; recreate/replay to seek. GPU pixels vary by
driver, and pre-effect text bounds do not prove final legibility or safe zones.
Verify real shader/glyph/sprite feedback and encoded output; keep optional
engine setup, licences and trusted executable presets explicit.
