# DanceFlow ecosystem

Confirmed scope: 19 October 2026. Public overview: https://kieransimkin.co.uk/danceflow/.

Before every new workflow, run `Tools/DanceFlow.ps1 -Releases` when the released toolkit is available, then compare the fresh official stable releases with the actual imported, installed and WordPress identities. The complete, versioned capability index and working examples live in the DanceFlow toolkit at `docs/capabilities/index.md`; the full FrameRudiments composition route is `docs/workflows/framerudiments-complete.md`. Older version notes below are historical evidence, not the current-release authority.

DanceFlow describes a family of independently useful tools. Its core path is
music understanding, rhythmic movement and rendering. Supporting tools cover
the evidence, media preparation, playback and metadata around that path.
Membership does not imply that every pair of tools has an automatic integration.

| Component | Role | Source repository |
| --- | --- | --- |
| StemLab | Music, stem, rhythm, structure, harmony, lyric and sonic analysis; inspectable timing and loop evidence | https://github.com/kieransimkin/stemlab |
| DanceRudiments | Deterministic rhythmic movement functions and a pattern visualizer | https://github.com/kieransimkin/DanceRudiments |
| FrameRudiments | Offline Python Shorts and lyric visualiser composition from DanceRudiments motion and saved StemLab evidence; released clocks, captions, 222 renderers, layers, masks, emitters, effects, GPU feedback, quality sampling and timeline authoring | https://github.com/kieransimkin/FrameRudiments |
| DanceMoves | Clocks, rendering, effects, input, scheduling, accessibility, lifecycle and adaptive quality for web motion | https://github.com/kieransimkin/DanceMoves |
| KeywordMoves | Source-specific keyword research, imports, observations and evidence comparison | https://github.com/kieransimkin/keywordmoves |
| RasterMoves | Reusable raster-media and image preparation | https://github.com/kieransimkin/RasterMoves |
| LikenessForge | Local CLI and desktop facial-likeness repair, identity LoRA training and reviewable candidate comparisons | https://github.com/kieransimkin/LikenessForge |
| PixelCue | Search and service workflows for local visual media | https://github.com/kieransimkin/PixelCue |
| PrismMoves | Evidence-labelled image visual-language profiles composed from PixelCue statistics, models and service APIs | https://github.com/kieransimkin/PrismMoves |
| ThumbMoves | Reusable thumbnail caching within the PixelCue repository | https://github.com/kieransimkin/PixelCue |
| React Timeline Sequence | React timelines, loop regions and shared audio transport | https://github.com/kieransimkin/react-timeline-sequence |
| EPK Social Metadata | WordPress EPK social and search metadata | https://github.com/kieransimkin/kieran-epk-social-metadata |
| DanceVault | Encrypted, password-controlled WordPress file delivery; stable 1.0.0 with real Apache/nginx test acceptance; destination-host acceptance still required | https://github.com/kieransimkin/DanceVault |

Kieran explicitly confirmed that **Short Shifter is entirely unrelated to
DanceFlow**. Keep it out of DanceFlow membership lists, diagrams, copy and
structured data. It remains an independent project in the site's general
project navigation and in the project-wide maintained-tool policy.

Current publication and package evidence belongs in the dated release-specific records, including `Software Releases/DanceFlow/ecosystem-2026-10-18/`; do not infer current release versions from this membership record or older marketing reports.
