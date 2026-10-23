# DanceFlow ecosystem

Audited membership: 23 October 2026. [Public overview](https://kieransimkin.co.uk/danceflow/). Seventeen component identities plus the DanceFlow discovery/composition toolkit. Before use, run `Tools/DanceFlow.ps1 -Releases --output NEW-RUN/releases.json` and compare the exact imported/installed/served identities. Read `Workflows/DanceFlow/capabilities/index.md` and `Workflows/potbot-unity-integration.md`.

| Component | Supported role | Source |
| --- | --- | --- |
| StemLab | music, stem, rhythm, structure, harmony, lyrics, sonic features and loop evidence; StemEdit timing/word/cue editor, StemMoves gallery, source-bound beat timelines and lyric audition | https://github.com/kieransimkin/stemlab |
| DanceRudiments | deterministic rhythmic position functions, authored pattern collections and a visualizer; typed rig profiles/motions, Rigify controls and native finite capture playback | https://github.com/kieransimkin/DanceRudiments |
| FrameRudiments | offline source-bound video compositor, 223 native/spectral/sprite/3D views including rangoli petals, rich word lyrics, particles, mattes/keyframes, feedback routing, authoring UI and controlled audio-response/preset analysis | https://github.com/kieransimkin/FrameRudiments |
| DanceMoves | BPM-synchronised web motion, shared clocks, effects, input, lifecycle and adaptive quality | https://github.com/kieransimkin/DanceMoves |
| KeywordMoves | source-specific keyword research, local phrase extraction and reviewed evidence imports | https://github.com/kieransimkin/keywordmoves |
| RasterMoves | local image upscaling with catalogue plugins, PyTorch/ONNX backends and optional refinement | https://github.com/kieransimkin/RasterMoves |
| LikenessForge | local CLI and desktop facial-likeness repair, identity LoRA training and candidate comparisons | https://github.com/kieransimkin/LikenessForge |
| PixelCue | local visual-media tagging, bounded image statistics, selected visual models and REST/Socket.IO analysis APIs | https://github.com/kieransimkin/PixelCue |
| PrismMoves | image visual-language profiles and temporal-first preset descriptions composed from PixelCue measurements and bounded optional model evidence | https://github.com/kieransimkin/PrismMoves |
| ThumbMoves | cache-only thumbnail access with explicit cache misses | https://github.com/kieransimkin/PixelCue |
| React Timeline Sequence | React audio transport, sequence lanes, seeking, zoom and sample-frame loop regions; editable timing/keyframes and line/word lyric audition on the selected source transport | https://github.com/kieransimkin/react-timeline-sequence |
| EPK Social Metadata | WordPress Open Graph, X card and Schema.org music/webpage metadata from canonical page facts | https://github.com/kieransimkin/kieran-epk-social-metadata |
| WorkflowMoves | guarded workflow rules, task guides, portable agent skills, evidence gates and additive project integration | https://github.com/kieransimkin/WorkflowMoves |
| DanceVault | stable encrypted, password-controlled WordPress delivery with real Apache/nginx test acceptance; destination-host acceptance remains required | https://github.com/kieransimkin/DanceVault |
| MediaSlide | responsive React media browsing across list, details, adjustable thumbnails and double-buffered slide views, with custom renderers and bidirectional pagination | https://github.com/kieransimkin/react-mediaslide |
| Potbot | durable coding-agent tasks, evidence, model jobs, budgets and native PostgreSQL/worker APIs; source preview, DanceFlow MCP consumption planned | https://github.com/kieransimkin/potbot |
| DanceFlow for Unity | Unity 6 UPM musical clocks, GPU phases, source-bound finite recordings and preview rig playback; Editor/GPU acceptance outstanding | https://github.com/kieransimkin/DanceFlow.Unity |

Potbot (`0.5.0.dev2`) and DanceFlow for Unity (`com.kieransimkin.danceflow.unity`, `0.5.0-preview.1`, Unity 6000.0+) are source previews with no stable release at this audit. Successful official queries report `no_stable_release`; failed queries report `unavailable`. Pin reviewed commits. Potbot consuming DanceFlow MCP remains planned; Unity Editor/GPU and real-character acceptance remain outstanding. Toolkit discovery exposes references and host requirements, not execution adapters for these two hosts.

**Short Shifter is entirely unrelated to DanceFlow.** Keep it out of membership, diagrams, copy and structured data. StemEdit and StemMoves are StemLab interfaces/examples, rather than new independent component packages. Membership does not imply every pair of tools is automatically connected.

![Generated evidence-handoff illustration](media/potbot-unity-handoffs.svg)

Generated contract illustration; dashed routes require implementation or host acceptance. The [working discovery example](https://github.com/kieransimkin/DanceFlow/blob/main/examples/ecosystem_discovery.py) reads both preview components without starting their hosts. Use actual captures and native samples for runtime claims.
