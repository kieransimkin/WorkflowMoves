# Fourier frequency buckets as DanceRudiments dimensions

Use released StemLab 1.6.0 through `Z:\My Songs\Tools\StemLab.ps1`, with native DanceRudiments 0.3.0 or a later compatible verified release. One input master or stem is measured in N frequency buckets; exactly N ascending-frequency dimensions (`band_000` onward) are exported. A 32-bucket analysis produces 32 dimensions. No instrument separation or model download runs.

```powershell
& 'Z:\My Songs\Tools\StemLab.ps1' record-rudiment '<master-or-stem.wav>' --bpm 145 --frequency-bands 32 --fft-size 2048 --normalize global --output '<new-output-folder>'
& 'Z:\My Songs\Tools\StemLab.ps1' record-rudiment '<saved-analysis>' --frequency-bands 32 --frequency-source htdemucs_6s/drums --normalize global --output '<new-output-folder>'
```

Replace illustrative BPM/source/path values with verified input authority. Reuse existing saved stems; preserve original recording identity, source hashes, programme length and canonical BPM/timing. An explicit BPM remains estimated unless it is actually confirmed; BPM confirmation does not confirm beat phase. Keep supplied/estimated/unverified phase states accurate.

Defaults are 32 when explicitly requested, linear equal-width bands from 0 Hz to the selected source's Nyquist frequency, and a 2048-source-frame periodic-Hann FFT. `--frequency-bands` accepts 1..1024 buckets within recording/cache and FFT-resolution limits; it is not enabled implicitly. Use `--frequency-min`, `--frequency-max`, `--frequency-scale linear|log` and `--fft-size` only for an actual analysis need. Log spacing requires a positive minimum; FFT size must be a power of two in 16..65536.

Each native pip contains calibrated band RMS from one centered real FFT. Average channel powers preserve antiphase stereo energy. Existing `EnvelopeBank.compose` maps non-silent amplitude to bipolar [-1,+1] using the selected reference; fully silent axes stay at 0. `global` retains relative band strength, `none` uses PCM-unity RMS, and `per-axis` can expand weak leakage/noise. Signed per-band `--gain` follows the same existing projection.

The source-rate, rational 64-pip clock is unchanged. A larger FFT improves frequency resolution at the cost of temporal resolution; its centered window reads earlier/later samples inside the selected excerpt. Zero outside excerpt/source boundaries lowers edge-window energy; it never wraps. This is band-level motion data, not reconstructed band WAVs, instrument identities or a new live DanceMoves adapter. Keep technical, creative, listening and publication outcomes distinct.

Retain the recording JSON and exact source/report hashes, selected source, frequency edges, FFT-bin bounds, window/calibration, sample rate, channel policy, excerpt, BPM/phase, normalization, gains and native sampling checks. Existing JSON export, source-change checks, new-directory transactions, value budgets and shared X-Y/per-dimension bar harness are reused. Review actual visible consumers and mappings before new choreography; the extracted values alone do not approve a design, soundtrack, loop or publication.

## Potential problems

- An empty/unresolved band is an error. Reduce bucket count, increase FFT size or widen the frequency range; never interpolate/invent a frequency bucket to make the count pass. Log bands near 20 Hz often need a larger window, such as 16384 source frames.
- Fourier mode cannot combine with time-domain axis/filter/mode/smoothing flags. Use the existing source selector and per-band gains; conflicting options fail explicitly.
- Standalone stems use the positional input. A saved analysis may select an unambiguous source or exact `MODEL/STEM`; do not silently choose among duplicate stem names or rerun separation.
- Legacy XYZ exports remain limited to at most three dimensions. N-D recordings are non-looping and retain native sample bounds; general-purpose C#/TypeScript/live support is not implied by an offline native recording.
- Keep the old runtime and prior evidence. Install and hash-verify the released 1.6.0 package in a new environment before changing the launcher; a private candidate or stale source checkout is not the production runtime.

Technical authority: [StemLab 1.6.0 recording guide](https://github.com/kieransimkin/stemlab/blob/v1.6.0/docs/rudiment-recordings.md) and [DanceRudiments 0.3.0 recordings](https://github.com/kieransimkin/DanceRudiments/blob/v0.3.0/docs/recordings.md). Use current released/installed identities at action time; source instructions and saved prompts do not prove later execution.
