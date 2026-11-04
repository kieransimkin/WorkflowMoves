## Check that separate content panels do not overlap

Supply a non-empty `options.panel_pairs` list to the layout collector at every tested width. Each entry names two unique CSS selectors for separate, visible content boxes. Check the hero heading or audio panel against the next release section where the boxes must stay apart. Reuse the same pairs at every width of one evidence record. For another player or menu state, collect a separate record.

For example, add `"panel_pairs": [{"first": ".hero-audio", "second": ".release-summary"}]` to the collector options beside the existing alignment checks. Use selectors scoped to the real release root when needed. Select the actual content panel and the adjacent section. A fixed-height ancestor can report that it ends before the next section while its child spills into that section. Leave decorative layers, intentional poster layering and parent-child pairs outside these separation checks.

The collector records the two viewport-derived rectangles. The gate fails if either selector is missing, ambiguous or has no visible non-empty box, if a pair changes across widths, or if the boxes intersect by more than one CSS pixel on both axes. A page can fail here while horizontal overflow stays at zero. Recollect old layout evidence before using it for a new publish decision.

The public [before-and-after compact hero correction](https://kieransimkin.co.uk/2026/10/26/putting-the-cover-at-the-front-of-a-song-page/#chips-and-ketchup-correction) shows the kind of collision this check catches. The portable JSON example uses synthetic measurements.
