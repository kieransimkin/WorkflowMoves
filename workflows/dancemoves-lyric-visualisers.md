# DanceMoves lyric visualisers on EPKs

Use the song's existing timed lyric attachment and canonical player. This guide
covers live EPKs. Use FrameRudiments for encoded lyric videos and visualisers.

## Choose a page and a treatment

1. Read the fresh saved EPK and inspect the public page while its master plays.
   For a first adoption, prefer a page with a verified timed lyric attachment
   and no existing on-page playback-synced lyric display. Check both built-in
   pop-up settings and page-owned terminals or callbacks. Record an existing
   transcript and separate lyric videos. Keep the readable transcript available.
2. Reconcile the installed and served DanceMoves versions with the verified
   release. Inline scroll requires DanceMoves 3.5.0 or later. If the live plugin
   is older, use the verified release files in an isolated local preview and
   record the required plugin deployment separately.
3. Read the campaign's current visual-language assessment and inspect the
   canonical cover and EPK. Write down which existing type roles, colours,
   textures, motifs, spacing and motion decisions inform the new frame. Scope
   the CSS to the release and use the current page's type and colour tokens
   where suitable. Place it near the matching player and keep artwork, controls
   and the reading order clear. The mask and track remain DanceMoves-owned.

## Connect the exact source

Add one `<div data-dance-moves-lyric-scroll></div>` inside the DanceMoves root.
Identify the canonical master with `data-dance-moves-master` on a page with
multiple players. WordPress supplies the selected LRC from EPK Timing.
Preserve the attachment, literal lyric wording, blank cues, source time and any
verified playback mappings. Keep existing pop-up and `lyricStage()` behaviour
for pages that use those treatments. Scope any new style to the inline frame.

![A long centred lyric wraps in the DanceMoves 3.5.0 test at phone width](https://raw.githubusercontent.com/kieransimkin/DanceMoves/v3.5.0/examples/lyric-scroll/mobile.png)

[Watch the actual synthetic browser demo](https://github.com/kieransimkin/DanceMoves/blob/v3.5.0/examples/lyric-scroll/demonstration.webm).
The previous and upcoming lines occupy the outer rows while the new line
moves into the centre. This fixture demonstrates the renderer. Each song needs
its own listening and presentation checks.

## Preview before the public save

- Bind the exact candidate and released JS/CSS to the actual EPK response.
  Play the hosted song and compare the frame with the selected LRC during
  consecutive lines and blank intervals. Check forward and backward seeks,
  pause and resume, the first and last lines, and a wrapped lyric. Keep
  source-clock checks distinct from an attended check of sung onset accuracy.
- Measure the frame and adjacent controls at desktop, tablet and phone widths.
  Check that three lyric rows fit, the current line settles in the centre, and
  nothing overlaps the player or leaks outside the mask. Verify instant
  updates under reduced motion and forced colours. Apply the existing
  [responsive EPK gate](epk-responsive-layout-qa.md) and keep existing
  playable videos and native controls usable.
- Show actual desktop and mobile captures and, when helpful, a short capture
  of the frame moving with the song. Record the style sources, candidate and
  baseline hashes, package identity, audio and LRC evidence, and whether the
  phone is emulated. Keep song-specific preview assets in their own release
  record. The screenshot above documents the shared renderer; each campaign
  preview supplies its own visual evidence.
- Obtain exact approval for the EPK change and any necessary WordPress plugin
  deployment. After authorised publication, independently verify the installed
  and served version, the preserved timing source and the signed-out result.

## Verify the optional beat countdown

When using `data-dance-moves-lyric-gap="countdown"`, verify the exact served
DanceMoves 3.6.1 runtime or qualify the installed successor. For a gap of two
beats or less, the upcoming lyric remains visible with the centre empty. A
longer gap shows its remaining beats in parentheses through `(2 beats)` and
`(1 beat)`. Derive the countdown from the existing master clock and verified
tempo. Preserve the original lyric attachment and lyric timing.

Play through a short or exact two-beat gap, a longer gap and a song without a
qualifying gap. Pause during the count, resume and seek into its final beat.
Check both the current and upcoming rows at desktop and phone widths. If the
campaign styles the count, scope the colour to the release and check contrast
against the actual frame. Repeat the checks on the signed-out page after any
authorised rollout. The released [browser fixture](https://github.com/kieransimkin/DanceMoves/blob/v3.6.1/tests/shared/lyric-scroll-browser.mjs)
covers the boundary cases, and the [public demo](https://github.com/kieransimkin/DanceMoves/blob/v3.6.1/examples/lyric-scroll/index.html)
shows how to select countdown mode.

## Potential problems

- **An earlier display appears only while the song plays.** Inspect the actual
  page during native playback and look for page-owned render callbacks before
  choosing it. Two timed displays compete for attention.
- **The new host stays empty.** Check the served runtime and stylesheet, then
  verify the master association, resolved attachment and parser readiness.
  Preserve the existing readable lyrics when timing is unavailable.
- **Long lyrics move nearby controls.** Check the actual campaign type at
  compact widths, including font loading. Keep the equal-row mask and let
  words wrap. Test the nearby player and following section in the same view.
