# EPK mobile motion verification

Use the motion and WordPress EPK publisher skills together with `Workflows/epk-pointer-regression.md`. Treat fresh saved WordPress content and the rendered page as authority. Resolve the complete current song catalogue, including alternate/review pages with suitable effects, and record exclusions explicitly.

For each effect, record its source and hash, root/subject/bounds, pointer route, phone route, permission UI, controller ID, CSS properties or render callback, neutral/reset state, motion switch, quality owner and intended lifetime. Review external scripts and styles too. Do not mistake a decorative rotation or ordinary button hover for an orientation-driven effect.

On the current published runtime, connect suitable existing pointer mappings with supported DanceMoves input composition. Prefer one sensor owner and one permission control per page. A supported existing phone provider can fan out to additional narrow appearance callbacks; do not create a second listener over it. No required sensor/page integration may live only in generated library output.

## Test EPKs across common mobile widths

- On every EPK creation, repair, publication and recurring audit, follow `Workflows/epk-responsive-layout-qa.md`. Check 320, 375, 390, 414 and 430 CSS pixels, the 760px mobile boundary, and 768/900/1440px tablet/desktop layouts. Add just below/at/above any changed breakpoint. One 390px screenshot is insufficient.
- Verify the actual inner/client width and height after applying a viewport. A requested phone override that still measures 1280px is unavailable evidence, not a mobile pass. Independently read screenshot pixel dimensions; reject miniature-page captures on a wider canvas. Keep browser emulation distinct from physical phone/Safari evidence.
- Inspect artwork and content gutters, hero/title/date/actions, below-fold media, lyrics, facts, downloads, navigation and contact controls. Check rendered text ranges and control rectangles against the viewport and clipping ancestors as well as document scroll width: `overflow:hidden` can conceal a broken layout. Verify declared centering/alignment geometrically; preserve intentional left-aligned copy, full-bleed art and release-specific compositions.
- Collect observations with `Tools/EPK Motion QA/collect_epk_layout.js` through the supported Browser, and run `Tools/EPK Motion QA/audit_epk_layout.py` on the private evidence JSON. Missing checks, missing phone widths, unapplied viewports, clipped text/controls, uneven declared gutters, unloaded artwork and wrong-size/unreviewed screenshots fail the gate. Intentional scroll navigation and offscreen skip links require explicit touch/keyboard review.
- Preview the exact candidate and repeat the same matrix against the persisted anonymous page after an approved save. Preserve source hashes, timing metadata, media, mobile input and existing publication gates. Recheck enlarged text, reduced motion and relevant player/menu open states; close completed owned test tabs and reset temporary viewport overrides. A local candidate pass is not a live repair.

Validate each path separately:

- Desktop: real pointer response at centre and opposite corners, leave-to-neutral, scroll/resize geometry, keyboard/focus parity and stable controls.
- Mobile: secure/touch eligibility; explicit permission gesture where required; denial, no readings, invalid/nonfinite readings and browser permission expiry; screen-aligned bounded output; every required visual layer changes from actual delivered samples.
- Preferences and lifecycle: motion off/on, reduced motion and forced colours before and after activation; page hiding/return, screen rotation, pagehide/pageshow, root removal and teardown; no stale/pending output, extra listener or persistent opt-out caused by suspension.
- Quality: existing downgrade/recovery and page quality predicates still govern input appearance; full-stack input storms and motion extremes stay within declared bounds. Do not infer physical smoothness from configuration or a synthetic run.

Retain exact source/package identities, hosted bundle comparison, event/mapper/visual evidence, viewport checks and screenshots under the release/audit folder in `Z:\My Songs`. Clearly label native, emulated, synthetic and unavailable evidence. An automated test cannot prove physical iPhone/Safari permission reuse or sensor delivery.

Use a fresh-source narrow merge for a repair. Preserve canonical media, timing metadata, lyrics, publicity history, controls, design and independent desktop input. Before publication, present the exact page targets and candidate hashes plus any required published plugin package for the existing action-time confirmation. After approval, save once, read back editor content and verify signed-out responsive behaviour. Update durable release sources/generators only from that verified revision. Passing pages need evidence, not a duplicate save.

The project-wide rule applies automatically to recurring EPK work through project instructions and the weekly/capability audit workflows. This document does not create a new schedule or grant public-save, rights or telemetry-upload permission.
