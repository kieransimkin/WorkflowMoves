# Hashtag discovery and use across the project

Use this alongside `keywordmoves-evidence-research.md`, `keyword-evidence-job-maintenance.md`, the canonical keyword register and each release's actual approved facts. It covers social captions, video descriptions, community posts, website copy and native music metadata. Each destination keeps its own evidence and controls. This is incidental to an authorised marketing/research run: preserve its lease, active-date/no-op/stop rules, batch/time limits, publication approvals and costs. Never launch catalogue-wide research on a quiet monitoring job just to satisfy this workflow.

![Evidence, review and final-copy checks](media/hashtag-planner.svg)

*Generated explanatory diagram, not evidence of publication or audience growth. The [working KeywordMoves example](https://github.com/kieransimkin/keywordmoves/blob/v0.6.0/examples/hashtag_planner.py) uses clearly synthetic captions to demonstrate the real local commands.*

## Start with the content and intended listener

Identify the exact asset/master and SHA-256, song/version, public eligibility, account, format, audience/language/market and intended action (listen, watch, save, discuss, visit). Read the release's approved genre/theme/visual and keyword records. Build candidate families from actual content: artist/release navigation, specific genre/community, truthful lyric/theme, actual format/instrument/creative process, and relevant current context. A title, one visual frame or AI suggestion does not prove a genre, affiliation, location or topical claim. Read current canonical lyric provenance before lyric-derived choices; do not disclose deliberately unreleased lyrics.

Discover natural search phrases separately from literal hashtags, native topic labels, video tags, mentions, sounds, location fields and website taxonomies. A compressed phrase is a new proposal until observed/reviewed; do not present it as a native suggestion. Use accessible CamelCase for newly composed multiword Latin tags when appropriate, retain observed/native spelling and Unicode, and check how the destination actually parses them.

## Research the intended platform

Use existing KeywordMoves Instagram/TikTok/YouTube workbenches, supported authorised APIs/exports or dated reviewed observations. Prefer native search/composer suggestions and exact tag pages, creator-search/trend tools where available, and owned search/referral evidence. Review a small bounded sample of genuinely comparable current content for language and community fit. Record when suggestions are personalised. A comparable artist's reach is not a tag's popularity. Google/vidIQ volumes and NLP are discovery leads for other platforms, never transferred measurements.

For each candidate retain subject, platform/account/format, exact literal tag, source URL/export and hash, capture time, geography/language, reporting window, actual metric/unit, rounding/censoring, availability and limitations. Distinguish:

- query demand or estimates;
- native relative trend interest/rank;
- number of posts/supply, lifetime totals or bounded sample occurrences;
- owned search/referral data and whole-post outcomes;
- local/AI proposals with unvalidated external demand.

A large lifetime post count neither proves current interest nor demonstrates achievable discovery. Inspect actual semantic results and spam/ambiguity before choosing. Record rejected candidates with a reason. An empty or inaccessible tag page is unavailable evidence; it does not prove restriction, a ban or zero demand. Do not maintain an invented universal banned-tag list. New paid collection, API eligibility, OAuth, account or model setup retains its existing approval gates. Browser rules remain those of the current job; this workflow grants no in-app-browser exception.

## Choose a small reviewed set

Use KeywordMoves >=0.6.0 `hashtag-planner` (`profiles`, `discover`, `plan`, `audit`) through `Tools/KeywordMoves.ps1`. Read the [exact document contracts](https://github.com/kieransimkin/keywordmoves/blob/v0.6.0/docs/hashtag-planner.md). `discover` extracts existing literal tags from permitted saved captures; it is not a live collector. Compose existing platform adapters for real discovery evidence. Include unvalidated local proposals only with their true provenance and explicit review.

`plan` requires a byte-hashed candidate pool, exact subject/platform/asset, planned use date, native check and explicit fit/safety/role/rationale decisions. Preserve source-specific measurements. Only direct, clear choices are eligible. Do not fill every possible slot or mandate an artist tag on every post. Brand, niche, topic, format and trend are optional roles for diversity. Reject generic reach bait such as #FYP/#Viral, unrelated celebrities/events, misleading affiliations, insensitive trend-jacking and ambiguous tags whose actual community is a poor match. Strong content and natural searchable copy remain central.

### Destination treatments

These are **project editorial starting ceilings**, not claimed platform maximums or proven optimum counts. Use fewer or zero when appropriate. Verify current native rules and account/composer controls before a save; stricter supported controls win.

| Destination | Starting range | Discovery and use |
| --- | --- | --- |
| YouTube / Shorts | 0-3 | Native hashtag suggestions, relevant hashtag pages and owned search/referral reports. Put relevant tags in the description; keep video tags, title and natural queries distinct. #Shorts is not a requirement for this workflow. |
| TikTok | 0-5 | Creator Search Insights when available, native search, Creative Center's actual region/window/industry, owned search analytics. Write truthful natural captions and use the clip's actual themes. Trends are optional and must fit. |
| Instagram | 0-5 | Native search/hashtag suggestions and comparable Reels plus owned insights. Check actual account caption controls; do not reuse obsolete 30-tag advice or infer per-tag reach from Reel totals. |
| Facebook | 0-2 | Relevant native search and own page/Reel insights. Review separately from Instagram; do not copy its whole tag block. |
| X | 0-2 | Native topic/search context. X's official best practice recommends at most two; this is not a hard platform limit. |
| Bluesky | 0-2 | Native search and relevant community/custom-feed rules. Feed matching is specific to the actual feed, not a universal tag effect. |
| Mastodon | 0-3 | Hashtag search/autocomplete within the named instance/federated visibility; respect community norms. Native tags need a letter, not numbers only. |
| LinkedIn | 0-3 | Appropriate professional subject, natural copy and native hashtag search. Do not conflate employee/life-page hashtag controls with ordinary posts. |
| Threads | No copied hash block | Optionally select one relevant native topic. Record the actual topic text and verify it persists; it may contain spaces. |
| Pinterest | No routine hash block | Relevant Pin/board titles and descriptions, Trends and available native topics. Treat these as search terms/topics, not hashtags. |
| Reddit | No routine hash block | Community rules, natural relevant title/body and permitted flair. A leading # may be Markdown formatting. Existing engagement/send gates still apply. |
| WordPress / EPK / blog | No hashtag stuffing | Natural keyword targeting, deliberate existing taxonomies and metadata. A keyword observation never authorises a new public save or mass taxonomy creation. |
| Spotify / Amazon / Apple Music | No invented hashtag field | Supported artist/pitch/distributor metadata and actual platform discovery evidence. Website/social tags do not become DSP demand. |
| Bandcamp / SoundCloud | Native tags separately | Use supported genre/native-tag fields with their actual spelling/rules. Do not paste another platform's # block. |

Review decisions expire after 14 days, discovery after 30 days, and trend/native checks after seven days under the conservative planner defaults. Refresh sooner when an event, audience meaning, policy or campaign phase changes. A far-future scheduled item needs a due-date recheck; do not redate old evidence to pass. `needs_native_recheck` is a named hold, not proof a candidate is bad. Trend selection also requires real recent native trend evidence; sample counts do not qualify.

## Register, plan, commit and read back

Maintain `Keyword Targets/keyword-targets.csv` using the existing **21-column UTF-8 BOM schema**. Store the literal #tag in `keyword`, the evidence platform in `platform`, `status=proposed` for new plausible candidates, `derivation_type=hashtag-discovered` or `hashtag-proposal`, and an explicit hashtag use/surface. Preserve the case-folded song + exact keyword + platform key and dated evidence/status history. Do not add generic platform-policy facts or force non-song subjects into this song register. Keep richer source observations, decisions, sets and outcome receipts as dated JSON beside the existing evidence. Fresh-hash guard and validate every merge; a saved row is not adoption or use.

For each proposed post retain the exact caption/description, separately reviewed topic/native tags, asset SHA-256 and plan SHA-256. Run `audit` on the final platform-specific copy; inspect `metadata.passed`, not just the process exit code. It catches changed/missing/duplicate hashtags, extra tags hidden earlier in the caption, ceiling excess, scope/asset/plan swaps, topic changes and expired/unavailable native checks. It cannot judge claims, privacy, rights, total caption length or rendered readability; the owning workflow checks those separately.

For new direct-social-plan items set `settings.require_hashtag_review=true` and attach `hashtag_audit={"path":"audit.json","sha256":"EXACT_RECEIPT_SHA256"}`. The shared planner checks a passing KeywordMoves audit against the actual video/caption bytes, platform and freshness at commitment; absent, changed, wrong-platform or stale receipts hold the item. `planned_for` in the tool review is the intended committing decision date. For a far-future publication retain a named prepublication recheck in the existing continuation queue; do not move the approved slot or create an extra automation. The optional field preserves legacy plans; adding/changing the receipt changes the payload approval hash. Refresh the review rather than weakening the check.

Preserve all exact-payload/account/publication approvals and social scheduling rules. Re-read the complete caption/topic in the composer or supported API payload before commitment and in the independent persisted queue afterwards. Store actual accepted copy/topic and its hash with post ID, account, format, native schedule/timezone and asset hash. Platform trimming or scheduler rewriting is a discrepancy to resolve, not success. At publication verify public state/playback and reconcile relevant campaign media to EPKs through the existing workflow. Never bulk-edit earlier published or scheduled items from a register proposal.

## Learn from actual outcomes

Use the existing reporting cadence; add no new automation or dashboard refresh merely for this guide. Record a baseline and comparable review ages (initially seven and 28 days when data and the campaign window allow). Capture available search/discovery referrals, non-follower reach, watch time/completion, saves/shares, meaningful comments, follows/visits, link clicks and actual listener actions. Keep unavailable values null/unavailable. A branded navigational tag can be useful with little demand; evaluate it against navigation, not global reach.

Compare similar assets/accounts/formats/markets and equivalent post ages. Retain caption, creative, timing, audio, spend and other changed variables. Test one clear hypothesis (for example, one specific community tag versus no tags) across enough comparable authorised posts; do not manufacture extra posts or duplicate uploads. Small uncontrolled samples are descriptive. Whole-post success never attributes uplift to every tag; native attributed reports retain their actual scope. No permanent winner from one viral post. Keep failed/neutral trials and retire weak choices with dated rationale rather than endlessly rotating random lists.

Minimum retained set record: subject/platform/account/format; asset and copy hashes; chosen/rejected tags and reasons; observation references/scope/dates; review/native-check expiry; hypothesis, comparator and outcome metric; actual draft/scheduled/published/verified state; next review; evidence limitations. If publication was outside scope, stop at reviewed preparation.

## Primary sources and review state

Checked 23 October 2026: [YouTube hashtags](https://support.google.com/youtube/answer/6390658), [YouTube video tags](https://support.google.com/youtube/answer/146402), [TikTok Trends](https://ads.tiktok.com/resources/help/article/how-to-use-trends?lang=en-GB), [Creator Search Insights](https://newsroom.tiktok.com/creator-search-insights?lang=en), [X](https://help.x.com/en/using-x/how-to-use-hashtags), [Threads topics](https://about.fb.com/ja/news/2023/12/threadskeywordsearch_tags/), [Pinterest](https://business.pinterest.com/en-in/blog/how-to-build-audience-pinterest/), [Bluesky](https://bsky.social/about/blog/05-31-2024-search), [Mastodon](https://docs.joinmastodon.org/user/posting/), [LinkedIn search](https://www.linkedin.com/help/linkedin/answer/a521824), [Facebook](https://www.facebook.com/help/www/2862139500770200). YouTube's documented above-60 ignore rule is a policy threshold, not a target count. The Instagram primary help page redirected to login/temporary blocking during this check: its exact current enforcement remains a native verification requirement; our ceiling of five is editorial. No unsupported organic reach percentages or universal tag-volume bands are adopted.

## Potential problems

- **Copied sets or stale evergreen templates:** reuse the research pool, then review exact content/platform/date again. Do not copy choices by title alone.
- **Only creator/sample metrics are available:** label them as sample supply or whole-post outcomes. Do not derive tag demand, competition or attributable reach.
- **Native evidence unavailable:** keep truthful proposals and exact access hold; no unsupported scrape, guessed ban or zero. Continue independent preparation under the original run limits.
- **A hashtag starts with a number or contains non-Latin text:** the shared parser handles mixed numeric-leading/Unicode tags; inspect actual destination parsing. Keep canonical source text unchanged.
- **A scheduled record predates this workflow:** do not invalidate its approval or rewrite it automatically. Assess at its next authorised edit/review, retaining exact earlier receipts and dates.
- **Shared evidence/register changed:** stage a fresh merge or retain a conflict; preserve other owners, catalogue authority, earlier evidence and state history.
- **Documentation media:** the labelled diagram plus runnable real command example explains this static process. Audience screenshots, videos and generated promotional imagery would add no verified outcome at this stage. Capture real public-safe UI/evidence when a native trial runs.

## Completion and blogworthiness

Record actual selected tools/runtime identities, source/output hashes, touched routes, tests and limits. Saved workflow/prompt text proves configuration, not adoption by an already running chat or improved reach. Assess `Blogworthiness: PASS` or `FAIL` in the existing report with evidence. A useful verified tool experiment can pass; routine tagging administration alone does not. A passing story requires duplicate review and a concrete covered/prepared/draft/published/verified/blocked next state under the maintained blog and voice skills.
