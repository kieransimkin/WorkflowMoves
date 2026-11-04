# EPK responsive layout QA

Use for every EPK creation, edit, publication and recurring audit. The supported Browser skill governs browser control. These helpers only inspect DOM-backed observations and validate records; they do not launch another browser, mutate a page or publish it.

## Required matrix

| CSS width | Purpose |
| --- | --- |
| 320 | Narrow phone and long identifiers |
| 375 | Compact phone |
| 390 | Standard phone |
| 414 | Larger phone |
| 430 | Wider phone; catches gaps above a 420px rule |
| 760 | Existing mobile layout boundary |
| 768, 900 | Tablet |
| 1440 | Desktop preservation |

Use representative heights (for example 740px at 320, 844px at 390, and 900px for wider captures), record them exactly, and test extra widths immediately below/at/above a changed CSS breakpoint. These are CSS-pixel test sizes, not verified device models. Test enlarged text, reduced motion, menu/calendar expansion, player reveal/close and relevant motion extremes separately at narrow and wide phone sizes. Preserve intentional layout differences.

## Acquire real observations

1. Capture fresh saved editor source and anonymous public HTML; hash both. Inventory the retained features and timing metadata. Use the exact candidate against the captured public response for local QA, then independently repeat after an approved public save.
2. Reuse the correct tab or create an owned test tab. Read the Browser viewport/CDP capability documentation. Apply the browser viewport size **after creating the tab**; where native mobile metrics are needed, first navigate to a harmless local HTTP starting page and then use the supported CDP emulation capability. Verify actual `innerWidth`, `clientWidth` and `innerHeight` on the tested page. Never count an unapplied override as a phone pass. If raw CDP is unavailable while a response is paused, use a fresh owned starting tab and supported viewport controls; do not bypass the browser or keep retrying the blocked command.
3. Await the documented load-state helper, inspect font/artwork readiness and stable hero positions, then collect DOM measurements. A screenshot with missing artwork or an unfinished entrance is not acceptance evidence. Scroll through the page so lazy media and below-fold sections are reviewed; return to the declared capture state. Dynamic pages need representative settled and relevant extreme/open-state checks.
4. Load the installed `collect_epk_layout.js` as text through the permitted file tool. In the Browser session, pass an expression shaped `"(" + collectorSource + ")(" + JSON.stringify(options) + ")"` to `tab.playwright.evaluate`. `options.alignments` declares unique target/container selectors, `expected` (`center`, `start`, `end` or `fill`) and an optional 0-4px tolerance. Check the artwork wrapper and the principal content container; do not treat every heading as centered. For transformed art, select its layout wrapper or record the approved neutral state. The collector is read-only and examines laid-out content throughout the document, including text inside clipping ancestors.
5. Read the current document-space capture origin with `const position = await tab.playwright.evaluate(() => ({x:scrollX,y:scrollY}))`, then capture through `tab.screenshot({clip:{...position,width,height}})`. At the top this is 0,0; after scrolling, reuse the actual current scroll position so a hero capture cannot be mistaken for below-fold evidence. Confirm the intended section is visible. Explicit framing also prevents desktop scrollbar exclusion from shrinking the entire capture. Wrap each collected result with `width`, `height`, `evidence_kind` (`emulated` or `physical`), `below_fold_reviewed`, and `screenshot: {path,width,height,reviewed}`. Read dimensions from the actual JPEG/PNG artifact, not the requested viewport. A maximum one-pixel rounding difference per dimension is allowed; larger discrepancies fail. A verified 375x900 CSS viewport captured at 375x899 is acceptable, while a 430x900 page captured as a miniature on a 430x242 canvas is not. Correct the supported viewport/capture setup; never resize an incorrect screenshot afterward to manufacture a pass. Use `.jpg` for Browser JPEG captures. Record review only after viewing it. Review intentional `scrolling_descendants` using touch and keyboard (`scrolling_containers_reviewed:true`) and offscreen skip links after focus (`focus_links_reviewed:true`). No page-wide overflow suppression or blanket exclusion can replace these checks.
6. Save one private record per page/candidate/state: `{page_id, source_sha256, candidate_sha256, widths:[...]}`. Additional widths are allowed; duplicates are not. Run `python "Tools/EPK Motion QA/audit_epk_layout.py" <evidence.json>`. The combined motion/timing checker uses the same required layout gate. A missing array or measurement means unknown and fails; it is never converted to zero.
7. Check source/candidate feature parity, exact metadata-derived timing, Unicode, keyboard/preference behavior and applicable mobile input separately. Before saving, re-read the exact editor source and obtain the existing narrow confirmation. After saving, reload the editor and run the same matrix on fresh anonymous persisted content. Reconcile mirrors only after that live verification.
8. Retain source/candidate hashes, observations, screenshots, explicit exceptions and publication state privately. Close completed owned/borrowed tabs, verify disappearance, and reset temporary viewport overrides. Preserve unsaved work and deliberate handoffs.

## Check that separate content panels do not overlap

Supply a non-empty `options.panel_pairs` list to the layout collector at every tested width. Each entry names two unique CSS selectors for separate, visible content boxes. Check the hero heading or audio panel against the next release section where the boxes must stay apart. Reuse the same pairs at every width of one evidence record. For another player or menu state, collect a separate record.

For example, add `"panel_pairs": [{"first": ".hero-audio", "second": ".release-summary"}]` to the collector options beside the existing alignment checks. Use selectors scoped to the real release root when needed. Select the actual content panel and the adjacent section. A fixed-height ancestor can report that it ends before the next section while its child spills into that section. Leave decorative layers, intentional poster layering and parent-child pairs outside these separation checks.

The collector records the two viewport-derived rectangles. The gate fails if either selector is missing, ambiguous or has no visible non-empty box, if a pair changes across widths, or if the boxes intersect by more than one CSS pixel on both axes. A page can fail here while horizontal overflow stays at zero. Recollect old layout evidence before using it for a new publish decision.

The public [before-and-after compact hero correction](https://kieransimkin.co.uk/2026/10/26/putting-the-cover-at-the-front-of-a-song-page/#chips-and-ketchup-correction) shows the kind of collision this check catches. The portable JSON example uses synthetic measurements.

## Regression cases

The gate must reject a 430px layout whose document reports no horizontal scroll but whose heading/actions extend beyond the screen. It must also reject a narrower artwork wrapper anchored to one edge, a phone override that still measures a desktop viewport, a 430px document captured as a miniature on a 430x242 canvas instead of the declared 430x900 screenshot, clipped long recording identifiers, and a rotated disclosure icon that creates document overflow.

The checker validates evidence structure and measurements; declarations are not independent proof of human review, physical sensor delivery, playback, accessibility or public persistence. Keep those states and limitations explicit.
