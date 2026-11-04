## Check YouTube reveal and return before publishing

Run the responsive matrix on the exact preview for every YouTube player that opens from a cover or changes the page layout. Test each player independently. Use a desktop click and a phone tap away from the central play icon. Collect the idle artwork, the playing video and the restored artwork after using the actual return control. Also watch the transition in both directions, verify an advancing YouTube timeline and test keyboard return and reduced motion. Repeat against the signed-out page after saving.

Declare the cover wrapper as `player`, the title as the first `copy` selector, the release date, text and action links as additional unique copy selectors, and the next content section as `following`. In each state call the existing layout collector with `options.youtube_reveal` set to those declarations. For example:

```json
{
  "youtube_reveal": [{
    "player": ".epk-hero [data-epk-cover-player]",
    "copy": [".epk-heading h1", ".epk-heading .epk-date", ".epk-heading .epk-actions"],
    "following": ".release-overview"
  }]
}
```

The default poster, opener, iframe and return selectors match the standard EPK composer. A custom player can supply `poster`, `opener`, `frame`, `close` and its exact `video_id`. Use selectors relative to the player for these elements. Put every player that changes the layout in the record, including any custom reveal. Direct embeds that keep their place when started have no reveal cycle.

At each width, save the collector's `youtube_cover_ids` and create `youtube_reveals`, one entry per player. Each entry contains `player`, `video_id`, `input` (`mouse`, `touch` or `keyboard`), and `states` with keys `idle`, `playing` and `restored`. Each value is the matching observation from `youtube_reveal_states`. Use the same selectors in all three states. If idle artwork intentionally overlays the copy, record the playing relationship as `playing_order` (`left`, `right`, `above` or `below`), based on the approved reading order. With no reveal, both arrays are empty. Set `youtube_flow_required: true` on the responsive evidence record so the layout and combined checkers both enforce it.

Bind the evidence to `page_id`, `source_sha256` and `candidate_sha256`. For a saved draft, both hashes identify its exact reviewed body. Run the dedicated gate for the current candidate before a public save:

```powershell
python "Tools/EPK Motion QA/audit_epk_youtube_flow.py" <evidence.json> --page-id <id> --source-sha256 <base-hash> --candidate-sha256 <candidate-hash>
```

A missing state, hidden or clipped copy, overlap with the frame or following section, changed column order, unrestored artwork or focus, or sideways overflow fails the check. Retain screenshots or a short capture of the transitions alongside the geometry. Use the paired playback check to confirm the provider is actually playing.
