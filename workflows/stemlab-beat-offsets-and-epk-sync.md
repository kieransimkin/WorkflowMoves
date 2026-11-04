# Beat-matched videos and EPK timing

Use saved StemLab evidence to establish tempo, beat phase and lyric/cue source
timing for the exact master. FrameRudiments owns offline rendering; DanceMoves
owns live playback clocks. A suitable package being installed does not prove
that a video or EPK actually consumes its reading.

![Actual FrameRudiments 0.2.0 encoded example: original and aligned native movement, with captions and recording bars on source time](https://raw.githubusercontent.com/kieransimkin/FrameRudiments/v0.2.0/docs/media/beat-alignment.png)

[Play the four-second synthetic demonstration](https://github.com/kieransimkin/FrameRudiments/raw/refs/tags/v0.2.0/docs/media/beat-alignment.mp4).
The first 120 BPM click is at source 0.125 seconds: its -16 pip reading puts
that beat at pip zero. Text and recorded movement keep their original timestamps.
This demonstrates clock composition, not song-analysis accuracy or listening approval.

1. Read the current ecosystem, applicable skills and Potential problems guidance.
   Verify released, installed/imported and served identities separately. Reuse
   existing master, lyric, cue, beat and loop evidence before running models.
   Keep every model weight/cache beneath its owning project's ignored `models/`.
2. Resolve exact release/track/master authority. Retain audio SHA-256, native
   sample rate/frame count, public attachment identity and any verified MPEG
   payload/ISRC association. A title or duration alone cannot identify a track.
   Preserve artist-held and missing masters as explicit holds.
3. Run `stemlab beat-offset RESULTS --output NEW --audio EXACT-MASTER` and retain
   the complete canonical/combined/fitted and half/same/double comparisons for
   consensus and every actual individual detector/source. Unknown canonical BPM
   stays unknown. Missing detections, normal half/double time and genuine tempo
   drift are distinct. Keep sequential and eligible inferred-index fits; inferred
   gaps do not add observed beats. Check the first-anchored error and points across
   the whole intended excerpt. A poor constant fit is not a verified match.
4. Select one reviewed source-bound handoff explicitly with
   `--alignment-analysis consensus --alignment-bpm-basis canonical` or a reviewed
   `combined_fit` estimate. Retain all alternatives and detector/report hashes.
   Never round fractional pips for the working clock: one native beat is 64 pips,
   while DanceMoves uses 16 ticks. The signed offset is
   `-first_beat_seconds * bpm / 60 * 64`; negative pre-beat time is valid.
5. For new offline musical videos, pin `beat-alignment.json` in
   `clock.beat_alignment` with its exact file hash. FrameRudiments 0.2+ validates
   the source and composes its existing BeatClock. Do not also supply another
   `origin` or `beat_grid`. Map excerpts/repeats/preroll to master time first,
   then apply phase once. Preserve original audio, LRC/CUE and captured recording
   clocks, including Fourier buckets. An estimated phase/BPM remains estimated.
6. For WordPress, use DanceMoves 3.3+ **EPK Timing** reading and **Analysed Master
   Audio** fields. The selected attachment supplies the URL and must match the
   reading's hash. Consumers use plugin-generated metadata, including
   `danceMovesConfig.beatAlignment`, `lyricTimingUrl` and `cueTimingUrl`.
   Never paste timing URLs or a second page-local clock/source override into
   page content. Audit existing manual phase compensation before applying a
   reading, and preserve full-master/Short/alternate-track associations.
7. Every affected EPK must have its actual BPM/phase and lyric/cue state checked
   during the same authorised job. Use fresh editor content and the exact selected
   attachment bytes, canonical wording, parser/effective-time bounds and actual
   consumers. Recover genuinely missing evidence locally when authorised; a
   speech VAD can remove singing, so compare StemLab's explicit full-audio mode.
   Keep repetition-safe decoding, the 70% canonical-word threshold, observed
   line anchors and listening QA. Do not interpolate missing lines, invent
   section labels, retime a recording or beat-snap lyrics to complete a checklist.
8. Stage the smallest exact correction batch, preserving design, media, controls,
   approved choreography, phone input, accessibility and publicity history.
   Software releases do not deploy plugins or save WordPress pages. Obtain the
   existing exact-payload/action-time approval for those public actions, then
   verify persisted editor values, anonymous configuration, hosted timing bytes,
   play/pause/seek/player switching and responsive output. Passing pages need no save.

![Actual DanceMoves source-bound clock example: source time 0.125 seconds and rhythmic position zero](https://raw.githubusercontent.com/kieransimkin/DanceMoves/v3.3.0/docs/screenshots/beat-alignment-first-beat.png)

[Watch the silent actual browser demonstration](https://github.com/kieransimkin/DanceMoves/raw/refs/tags/v3.3.0/docs/videos/beat-alignment-browser.mp4).
The browser regression separately verifies source pip 272 for a captured
recording and procedural pip 256 at source 2.125 seconds. This is synthetic
desktop evidence; physical-phone and attended-listening acceptance remain separate.

## Potential problems

- A median detector BPM can drift over a whole song. A regression using consecutive
  indices can instead misread skipped detections as a tempo change. Keep both
  interpretations, actual timestamp residuals, inferred gap counts and error guards.
- A beat at an eighth-note subdivision can be a normal double-time interpretation.
  Good subdivision compatibility does not establish metre, downbeat or first-beat
  authority. Never silently double the canonical tempo or fabricate missing beats.
- An initial detector timestamp may be an artefact. Keep its phase estimated until
  reviewed; a good later grid does not validate the first source beat automatically.
- Page-specific engines, CSS delays or an old manual offset may bypass or duplicate
  the shared phase. Trace each painted rhythmic consumer; loaded fields prove only
  availability. Keep `sourceBeats` for recordings and `rhythmicBeats` for procedural
  movement distinct.
- Multi-track EPKs need exact per-source scope. Never apply the selected master’s
  reading or timing file to an arbitrary alternate track. Preserve readable lyrics
  and an accurate unavailable timing state when evidence is missing.
- Keep a source-hashed catalogue baseline and reuse it in relevant recurring jobs;
  no unchanged page needs a new model run, render or public save. Record staged,
  awaiting approval, published and verified-live states separately, with precise holds.

Retain actual screenshots/video beside the explanation and verification record.
Generated illustration is omitted here because the actual interface and encoded
examples already demonstrate the contract. Keep models, private masters, transcripts,
rights evidence and local coordination out of public software assets.
