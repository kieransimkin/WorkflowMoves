# StemLab phrase auditions and source-clock recovery

Use the verified `Tools/StemLab.ps1` launcher. The 15 October 2026 baseline is released StemLab 1.5.0. Both routes reuse local evidence without separation, learned-model inference or downloads. Preserve strict loop reports, source audio, prior exports and all listening/publication gates.

## Phrase-complete audition candidates

Use `phrase-loops` when the task asks which complete lyric passages are worth auditioning for a satisfying restart. Conservative `loops` remains the route for technically eligible seamless-loop hypotheses. Phrase suggestions do not upgrade a failed strict loop. Explicit `canonical.json` line starts/ends are required; do not fabricate them from untimed lyrics or silently copy an unrelated LRC.

```powershell
& 'Z:\My Songs\Tools\StemLab.ps1' phrase-loops 'Z:\My Songs\Releases\<release>\analysis\<saved>' --min-seconds 5 --max-seconds 30 --top 6 --export-audio
& 'Z:\My Songs\Tools\StemLab.ps1' phrase-loops 'Z:\My Songs\Releases\<release>\analysis\<saved>' --min-seconds 20 --max-seconds 30 --max-bar-phase-error .125 --feedback 'Z:\My Songs\Releases\<release>\analysis\artist-ratings.json' --export-audio
```

Inspect `deep/phrase_loops/phrase_loops.json`, schema `stemlab.phrase_loops.v1`, separately from `deep/loops/loops.json` (`stemlab.loops.v1`). Preserve pre-run reports/manifests because these commands add or refresh analysis outputs. Verify master hash, native start-inclusive/end-exclusive frames, exact lyric occurrences, context/attack features, measured beat/bar phase, vocal/waveform gates and every remaining hold. Exported float32 WAVs are exact decoded master slices at native rate; there is no snap, fade, normalization or stretch. Use repeated auditions and the existing narrative, breath/tail and seam review before selection.

The bar-phase filter is optional, uses the selected detector's measured bar grid and requires enclosing downbeats/consistent detected meter. `.125` is an example chosen tolerance, not a universal threshold or proof of cadence. Unknown coverage/changing meter remains held. Line completeness, score and time precision cannot establish a satisfying restart or vocal clearance. The strict-loop timeline does not display these as accepted loop regions.

Capture artist feedback only for an explicit listening decision. JSON schema `stemlab.loop_feedback.v1` requires exact `source_sha256`, native `start_sample`/`end_sample`, `rating` (`good`, `okay`, `bad`) and `reason` (`unknown`, `musical_restart`, `section_unsuitable`). Never translate a view, automated score or silence into a rating. Near-duplicates already rated are suppressed; `bad`/`section_unsuitable` also excludes overlapping cuts and exact repeated-word passages. Good/okay durations are soft references and do not approve later changed cuts or another recording.

## Match an existing clip to its source clock

Use this when verified video/render receipts need an independent soundtrack-offset check, or when an existing clip's mapping is unresolved. Start with the exact candidate master and original upload/render file, including their hashes and programme authority.

```powershell
& 'Z:\My Songs\Tools\StemLab.ps1' match-clip 'Z:\My Songs\Releases\<release>\<master>.wav' 'Z:\My Songs\Releases\<release>\<original-render>.mp4' --output 'Z:\My Songs\Releases\<release>\analysis\<new-match>.json'
```

Use `--clip-start`/`--clip-end` only for an evidenced soundtrack interval that excludes actual preroll/outro. A matched report supplies `offset`, `duration` and `playerStart`: source offset refers to the selected interval's start; playerStart is its time in the clip. Retain both hashes, interval, precision, correlations, uniqueness margin and independent timing checks. Match with original render/trim receipts before staging a DanceMoves player binding; verify the resulting advancing song clock and selected canonical lyric/cue consumers after any authorized save.

Default measurement is 8 kHz (0.125 ms grid), not guaranteed native-frame or browser-clock accuracy. Require at least two seconds; decoded inputs are limited to 30 minutes. Repeated passages, discontinuous loops, speed changes, alternate performances or conflicting offsets can remain unresolved. A report is saved and exit code 2 means unresolved; it is evidence, not a tool crash. Never lower thresholds or infer a mapping from a title/duration. New output files refuse replacement.

Compressed video/audio needs the verified FFmpeg route; supported WAV can use libsndfile. Stereo is preserved for antiphase sources. A waveform match does not establish exact master bytes, artist approval, rights or canonical track identity. Those retain independent provenance and permissions. Do not upload private masters or publish bindings merely because matching succeeded.

## Potential problems

- **Historical checkout lacks commands:** invoke the explicit released launcher and verify imports/help. Preserve the old editable source; do not patch it to mimic installed features.
- **No phrase suggestions:** confirm exact canonical timing, available recorded context, minimum line count/duration and selected detector coverage. Missing data and rejected candidates are valid results; never invent lyric ends or relax musical gates to populate a list.
- **Repeated chorus yields ambiguous clip match:** retain all correlation/uniqueness evidence and inspect original creation records. A precise grid is not a unique source occurrence. Keep the binding on hold when receipts cannot resolve it.
- **FFmpeg/model/temp unavailable:** use supported project tooling and the existing restricted-temp recovery. Do not rerun heavy separation or bypass access restrictions for these lightweight routes.

Authority: [phrase-loop behavior and feedback schema](https://github.com/kieransimkin/stemlab/blob/v1.5.0/docs/phrase-loops.md), [clip matching and limitations](https://github.com/kieransimkin/stemlab/blob/v1.5.0/docs/clip-matching.md). Synthetic demo success is technical verification only; a real-song listening decision remains separate.
