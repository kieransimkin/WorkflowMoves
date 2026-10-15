# StemLab selection of DanceRudiments for motion

Use StemLab to find matching DanceRudiments before selecting new or materially revised BPM-matched animation and visual effects for videos, Shorts, visualisers, Canvas derivatives, EPKs and audio-timed shared site effects. Preserve approved choreography as the baseline; a higher score alone does not justify replacement. Metadata-only EPK edits require no new motion analysis.

## Runtime and source authority

Invoke `Z:\My Songs\Tools\StemLab.ps1`. It selects the verified StemLab 1.4.0 wheel and official native DanceRudiments 0.2.4 wheel in `Tools/stemlab-runtime-1.4.0/.venv`. The dirty historical `Tools/stemlab` checkout is preserved. The new Python 3.11 environment shares retained analysis dependencies using `project_analysis_dependencies.pth`, while owning its StemLab/native packages separately. Record imported paths, versions, interpreter, catalogue identity and source commit; never trust a bare PATH command.

Source: [StemLab v1.4.0](https://github.com/kieransimkin/stemlab/releases/tag/v1.4.0), commit `15e6725069c2d5f8383f3d2b9503f60beb728e2f`. Method: [official rudiments documentation](https://github.com/kieransimkin/stemlab/blob/v1.4.0/docs/rudiments.md). The matcher calls independent DanceRudiments C++ `catalogue()` and `sample(name, integer_pip)` APIs. Do not copy the catalogue or movement functions into a renderer.

Resolve canonical master/stems and SHA-256 values, programme duration, accepted BPM, beat-grid evidence, cues, lyrics, intended excerpt and visual guide. Reused analysis must identify the same programme. Save new reports in dated release-local directories; retain older evidence.

## Generate candidates

Reuse saved separation and detected beats first, without rerunning models:

```powershell
& 'Z:\My Songs\Tools\StemLab.ps1' rudiments 'Z:\My Songs\Releases\<release>\analysis\<verified-results>' --top 20 --output 'Z:\My Songs\Releases\<release>\motion-matches\<dated-run>'
```

Repeat `--stem drums --stem bass` only when those names exist. Without a filter the mix and all saved stems are considered. Inspect per-stem results and `cross_stem_candidates`. The mix is not an independent vote; different models of the same physical source are not independent scientific evidence.

Saved results reuse detected grids and reject `--bpm`. Compare the grid with accepted timing and preserve disagreements. If usable saved beats/stems are absent, use the supported standalone mix-only route:

```powershell
& 'Z:\My Songs\Tools\StemLab.ps1' rudiments 'Z:\My Songs\Releases\<release>\<canonical-audio>.wav' --bpm <accepted-BPM> --output 'Z:\My Songs\Releases\<release>\motion-matches\<dated-mix-run>'
```

`--first-beat-seconds` may supply a justified regular-grid origin; the result remains `explicit_bpm_unverified_phase`, not a verified downbeat. Never supply the 120 BPM fallback as a known tempo. New analysis may opt in with `analyze ... --rudiments`; this requires deep analysis and rejects `--no-deep-analysis`.

Default search covers the full native catalogue (`--max-patterns 0`). Supported collections are `initial`, `expansion`, `atlas`, `continuum`, `club` and `dancefloor`. Record restrictions and their reasons. `--top` bounds displayed results per source; `--max-patterns` limits coverage. An `initial` demonstration does not verify the whole catalogue.

## Interpret and retain the selection

Require `report.json` with schema `stemlab.dancerudiments.candidates.v1` and `index.html`; expect `overview.png` when matches exist and plotting is enabled. Inspect measured attacks beside the sampled movement descriptors. Default windows span 16 beats every four beats, with quarter-beat phase search over at most four beats. Constant shapes and periods beyond the configured 16-beat limit are skipped explicitly.

`similarity=(1+correlation)/2` is a descriptive ranking, not probability, calibrated confidence, a recognised song rhythm or creative approval. `signal` can mean position excursion, speed or turn/acceleration; a turn match is not automatically a displacement peak or a flash instruction. Require the evidence window to intersect the intended clip/section. Never apply a local best score to the whole song.

Keep a motion-selection record containing:

- exact audio and analysis paths/hashes, report path/hash, StemLab/native versions and catalogue identity;
- source/stem or consensus, search scope, `grid_source`, pattern, `period_beats`, `signal`, similarity/correlation, `start_beat`, `end_beat`, `start_seconds`, `end_seconds` and `phase_beats`;
- chosen/rejected alternatives and creative reasons, target section/subject, coordinate mapping, amplitude, rate, affected area and maximum transformed extent;
- destination runtime, supported identifier, source clock/origin, phase conversion and rounding, cue resets, lifecycle/preference/quality results and technical/perceptual approval states.

Preview suitable alternatives with actual audio and the intended artwork. Choose for truthful musical evidence, visual identity, composition and readability. Missing native dependency, no usable grid, no candidates or an unsupported destination identifier remain explicit unavailable/rejected states. Resolve the cause; if unresolved retain approved motion or document a deliberate bounded fallback and its evidence limit.

## Carry timing into animation

DanceRudiments uses **64 integer pips per beat**; DanceMoves uses **16 ticks per beat**. One tick spans four pips; they are distinct units. At native rate 1 a cycle lasts `period_beats * 60 / BPM` seconds. Changing rate, stretching the cycle or interpolating samples changes the tested match and requires separate labelling/review.

With `B(t)` the selected grid's source beat coordinate, the local-window shape is:

```text
pip = floor(64 * (B(source_time) - start_beat + phase_beats))
native_sample = dancerudiments.sample(pattern, pip)
```

Native sampling wraps to its own period. Retain source time including excerpt offset. Check the matched descriptor as well as position. A variable detected grid can disagree with a fixed canonical-BPM renderer; record the approximation and verify the actual window. Do not time-warp audio or call this exact onset/downbeat alignment without evidence.

Offline video uses one deterministic source-time/frame ledger and native samples through the established generator. Preserve canonical lyrics/cues, default constant 60 fps, exact excerpt samples, deliberate opening and loop seam. A WordPress runtime is unnecessary offline.

Live EPKs must confirm the chosen identifier and period in the actual published, installed and served DanceMoves runtime. Use `DanceMovesRudiments.animate` with real audio, `clock:'audio'`, explicit rate/amplitude and scoped CSS. At rate 1 with fixed BPM, a window-origin candidate is `phasePips=round(64*(phase_beats-start_seconds*BPM/60))`, wrapped to the native period. Verify sign, origin and rounding against rendered samples; this does not automatically transfer a variable detected grid. DanceMoves owns clocks, seek/media lifecycle, visibility, reduced motion, forced colours, quality downgrade/recovery and teardown. Do not add page timers or media state machines. Atlas pose playback still uses `DanceMovesEffects.spritePlayback`; matching movement does not invent character poses.

## Verification and publication

Retain active/inactive and maximum-spread frames, phone crops, text contrast, alpha/blur/shadow extents, hard-edge checks and loop states. Each intermittent accent stays inside its declared subject/region; scores do not permit recurring whole-frame flashes or grading. Continuous motion retains accessibility and extent safeguards.

EPKs require play/pause, forward/backward seek, rate change, end/replay, motion off/on, offscreen recovery, reduced motion, forced colours, sustained automatic downgrade/recovery and teardown using native owners. Keep fresh-source additive merges, exact-payload approval and persisted signed-out responsive QA. Videos and Canvas retain generator approval, exact-file visual/listening QA, destination policy and upload approval. Distinguish prepared, reviewed, approved, published and verified-live states.

## Potential problems

- **Old CLI has no `rudiments`:** historical editable StemLab reports 1.2.0. Use the explicit launcher and require imported source in the installed 1.4.0 wheel. Do not reset the old checkout or point PYTHONPATH at it. Verified 11 October with native 0.2.4 (1,731 catalogue entries), eight focused tests and real bundled-audio CLI output.
- **uv/pytest returns WinError 5:** consult `stemlab-restricted-temporary-directory-recovery.md` and tool-runtime guidance. On 11 October the sandbox denied cache/environment writes and pytest's fresh temporary directory; narrowly approved execution of the unchanged commands succeeded. Use a fresh empty test path, preserve failed evidence and do not alter system permissions.
- **Window/phase misses the target section:** retain source window/grid/descriptor. Choose covering evidence or analyse a separately identified excerpt with its original source offset. A local maximum proves neither whole-song fit nor verified downbeats.

The reusable improvement is explicit composition, selection and provenance; the existing tools already provide analysis and playback, so no duplicate engine is justified.
