# StemLab audio-derived movement recordings

Use this route when the design needs movements derived directly from audio amplitude, separate stem roles or filtered frequency bands. Continue to use `stemlab-rudiment-motion-selection.md` to rank existing named catalogue movements before new rhythmic choreography. These are complementary routes: recordings capture measured envelopes; catalogue matching ranks reusable patterns. Neither decides creative suitability.

## Released runtime and ownership

Use `& 'Z:\My Songs\Tools\StemLab.ps1' <command>`. The 15 October 2026 baseline is [StemLab 1.5.0](https://github.com/kieransimkin/stemlab/releases/tag/v1.5.0), commit `9225b7494e361a653e60d71be95e8339c46a4c9e`, and [DanceRudiments 0.3.0](https://github.com/kieransimkin/DanceRudiments/releases/tag/v0.3.0), commit `b89d1b80fcd8a8d8e02394ec718b6f4debd97b94`. Check actual imported package paths and versions. Old editable checkouts and already-exported HTML do not acquire new APIs automatically. Preserve earlier environments and exports.

StemLab owns separation, filtering, envelope extraction and batch provenance. DanceRudiments owns the `dancerudiments.recording` schema, native C++/Python non-looping sampler and shared WASM comparison harness. Use those APIs rather than a copied DSP or movement renderer. Named legacy patterns remain XYZ, integer-pip and looping. The new arbitrary-dimensional recording format does not add general N-D C# or TypeScript bindings, or imply an installed DanceMoves adapter.

## Choose the smallest useful route

| Need | Command | Work performed |
| --- | --- | --- |
| One explicitly routed movement | `record-rudiment` | Reuses saved stems or supplied files; any number of named axes. |
| A bounded variety of sources and filters | `generate-batch` | Reuses files; seeded combinations and reported coverage. No separation. |
| Two different stem roles on X/Y | `generate-stem-batch` | Reuses saved analysis; raw audio separates once, default `htdemucs_6s`. |
| Controlled smoothing comparison | `generate-average-comparison` | Fixes pair, orientation, filters, gains and normalization reference across peak/average/smoothing settings. Raw audio separates unless `--master-only`. |
| Existing movement matching | `rudiments` | Ranks catalogue candidates; preserves source/window/grid/phase evidence. |

Reuse saved analysis first. Record master/stem hashes, separator/role and original clock. Use `MODEL/STEM` when a stem alias is ambiguous. Two byte-identical sources or the master relabelled as a stem are not independent stem roles. Do not run a full analysis or download models merely to explore movement. Raw separation retains its normal dependency, weight-download and licence requirements.

## Clock and signal decisions

Raw audio requires a justified `--bpm`; use `--bpm-confirmed` only with artist-approved authority. Saved analysis may supply an estimated BPM; `--beat-model` selects an existing detector explicitly. Keep BPM status separate from beat-zero provenance. `--beat-zero` is supplied phase evidence, not automatic verification; absent evidence remains unverified. Never use a 120 BPM fallback as fact.

Recordings use a constant clock at **64 pips per quarter-note beat**:

`time(i) = beat_zero_seconds + (start_pip + i) * 60 / (64 * BPM)`.

Retain negative start pips, original excerpt offsets and exact sample bounds. Files must share a time origin; unequal durations fail unless a deliberate `pad`/`trim` policy is recorded. The API does not align edits or implement a variable-tempo map. Native recording sampling stops outside the captured extent instead of wrapping. One DanceMoves tick is four native pips; never interchange units or truncate negative positions towards zero.

`peak` is maximum absolute amplitude per pip; `average` is mean absolute amplitude per pip. `moving-average` is centered offline smoothing of that rectified envelope over a separate beat window. These are not pitch, RMS, signed-waveform means or detected onsets. Filtering occurs before rectification. Record cutoff/order/phase, channel handling, normalization, gains, clipping and unscaled peaks. Zero-phase filtering can ring at edges; causal filtering adds delay. Per-axis normalization can amplify quiet residual noise.

Smoothing defaults to 1/4 beat; use positive widths up to 64 beats. Widths round half-up to integer pips: .125/.25/.5/1 beat give 8/16/32/64 pips. One pip equals `average`; edges use available bins without wrap. Smoothing changes values, not BPM, duration or resolution. Do not use it to disguise an incorrect source clock.

## Local examples

Replace the paths and confirmed values with the actual release authority. Always choose a new output directory. Omit `--include-audio` unless a private exact copy of the master is useful; derived movement data may also be private.

```powershell
& 'Z:\My Songs\Tools\StemLab.ps1' record-rudiment 'Z:\My Songs\Releases\<release>\analysis\<saved>' --bpm 145 --bpm-confirmed --axis x=drums --axis y=bass --mode moving-average --moving-average-beats .25 --axis-window-beats y=.5 --output 'Z:\My Songs\Releases\<release>\motion\<new-pair>'
& 'Z:\My Songs\Tools\StemLab.ps1' generate-stem-batch 'Z:\My Songs\Releases\<release>\analysis\<saved>' --bpm 145 --max-candidates 30 --output 'Z:\My Songs\Releases\<release>\motion\<new-stems>'
& 'Z:\My Songs\Tools\StemLab.ps1' generate-average-comparison 'Z:\My Songs\Releases\<release>\analysis\<saved>' --bpm 145 --max-pairs 4 --window-beats .125 --window-beats .25 --window-beats .5 --window-beats 1 --output 'Z:\My Songs\Releases\<release>\motion\<new-comparison>'
```

The numerical BPM above is an example. When preparing raw-audio stem pairs, use `--analysis-output <new-analysis-directory>` to retain separation for reuse; otherwise temporary stems are removed. `record-rudiment` and `generate-batch` do not separate audio. Single-recording filter options use `NAME=Hz`; batch presets use numeric Hz. Check the installed command's `--help` before choosing options.

Bound expensive batches and excerpt duration explicitly. General batches require capacity for two baseline candidates per source. Stem-pair batches default to 120; a six-stem source offers 30 ordered raw pairs. Average comparisons preserve complete setting groups: four smoothing windows plus peak/average make six candidates per pair. Maximum 1,024 candidates and 32 million scalar values per batch; one recording is limited to 8,388,608 values/64 MiB and the shared harness to 128 MiB unique columns. Report skipped filters, duplicates, static routes, coverage and any limiting reason; bounded exploration is not exhaustive search or ranking.

## Review the actual shared viewers

Open generated `index.html` with its `report.json`, audit JSON and `recordings/` companions. The packaged DanceRudiments viewer supports searchable cards, four-way comparison, Keep/Maybe/Skip notes and portable review JSON. X-Y projection selects visible axes; **Bar graph** shows all named signed dimensions on the same -1..+1 scale. The display amplitude slider changes geometry only. Verify the mode switch preserves playback, seek position and review state. Regenerate a new export for new controls; retain previous snapshots.

When exact audio is loaded, native movement follows its media clock. Verify no autoplay, play/pause, forward/backward seek, pip stepping, end-of-capture stop, tab-hide pause, axis projection, review export/import and native sample equality. Display-decimated traces do not replace full stored samples. Browser decoding or an advancing clock is not attended listening QA. In-memory/Blob browser tests are labelled synthetic transport evidence and do not prove local-file loading.

StemLab's real timeline now groups waveform/spectrogram for each master or separator/stem into one lane: Waveform, Spectrogram or Both. Use aligned NPZ data, not stretched chart PNGs. Wheel pans time; Ctrl/Command+wheel zooms time; Alt+wheel resizes the hovered lane; Shift+wheel scrolls channels. Heading height sliders/reset remain available. Display operations do not change evidence. Native/browser rendering must be inspected before claiming the UI works locally.

For new analysis, BeatNet and BeatThis run after separation on the master **and every explicitly labelled drum/percussion stem**. Keep each separator/source/hash result distinct. Beat Transformer uses its real demixed streams once; All-In-One structure stays master-based. Consensus permits one vote per detector family per cluster, preventing many stems from manufacturing independent support. Saved old analysis remains old evidence; do not claim it contains newly routed passes or rerun it without a question that warrants the cost.

## Hand off to a render or EPK

Retain recording/report/harness hashes, imported versions, source identities, BPM/phase status, exact captured extent, axis/filter/mode settings, normalization scale, projection, chosen review and bounded appearance mapping. Offline rendering samples the native non-looping recording from absolute source time; do not wrap a full-song envelope or silently interpolate it. A legacy pack requires explicit 1..3-axis selection and at most 65,535 samples; it loops and retains a seam warning.

A live EPK needs verified support in the exact served DanceMoves runtime before using a new recording. An installed Python package or offline harness does not establish that support. Keep the shared clock, lifecycle, mobile inputs, reduced motion, forced colours, quality adaptation and cleanup owners; page callbacks map existing appearance only. Preserve metadata-only timing authority and exact-payload public-save approval. Continue safe preparation if the adapter is unavailable, retain approved live motion and record the precise hold.

Every repetitive audio effect remains inside declared subject bounds. Check full transformed alpha/blur/shadow extents, phone crops, readability, first/last frames and any loop seam. Control-data quality, aesthetic selection, final listening, generator approval, scheduled publication and verified live state remain distinct.

## Release maintenance and potential problems

- **Missing recording API:** native 0.2.4 predates it, despite the unchanged 1,731-entry catalogue. Install verified official 0.3.0 wheels with StemLab 1.5.0 in a new environment; verify `SampledRecording`, authoring imports and actual CLI exports. Do not copy source into PYTHONPATH or silently fall back to old code. Preserve the old environment.
- **Old exported page lacks bar view:** HTML is an immutable snapshot. Regenerate to a new directory using the released shared assets and recheck native/audio/review behavior; package installation alone does not update it.
- **Apparent stronger movement after smoothing:** controlled comparisons hold the unsmoothed peak normalization reference fixed. Inspect unscaled values and complete groups; separately normalized exports are not controlled smoothing comparisons.
- **Restricted Windows write/cache/temp errors:** use `stemlab-restricted-temporary-directory-recovery.md` and scoped approved execution for the unchanged command. Keep caches and test outputs under My Songs; never change system ACLs or treat an access error as a DSP failure.
- **Publishing companion updates:** release React Timeline Sequence, then DanceRudiments, then StemLab. Follow the tagged [released-viewer guide](https://github.com/kieransimkin/stemlab/blob/v1.5.0/docs/released-viewers.md). Production builds resolve latest stable official registry releases into one immutable build snapshot; no sibling-source/vendor archive substitute. Keep locks, release/build receipts and rebuilt frontend together. The coordinator defaults to preview; execution/release/deployment needs its applicable authorization. A stale old-tag freshness failure never permits retagging. Do not start duplicate Arcadians analysis while its tagged combined build is running. Package, registry, Pages and listening verification are separate outcomes.

Technical authority: tagged [recording](https://github.com/kieransimkin/stemlab/blob/v1.5.0/docs/rudiment-recordings.md), [stem-pair and smoothing](https://github.com/kieransimkin/stemlab/blob/v1.5.0/docs/recording-pairs.md), [beat-routing](https://github.com/kieransimkin/stemlab/blob/v1.5.0/docs/beat-inputs.md), [viewer-controls](https://github.com/kieransimkin/stemlab/blob/v1.5.0/docs/viewer-controls.md) and [native recording API](https://github.com/kieransimkin/DanceRudiments/blob/v0.3.0/docs/recordings.md) documentation. Historical patch/unreleased wording in these tagged files is superseded by verified release assets and imports, not by assumptions about checkout state.
