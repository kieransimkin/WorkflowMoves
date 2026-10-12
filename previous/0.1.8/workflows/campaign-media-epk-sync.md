# Campaign media EPK reconciliation

Apply the project rule during publishing, campaign/platform monitoring, reply audits and weekly release sync.

1. Reconcile current catalogue, release records, publishing receipts/queues and original public items. Record exact song/campaign and page IDs. Related press/alternate pages receive only material appropriate to their actual version.
2. Build one ledger row per distinct creative asset. Record exact render hash or explicit verified cross-post mapping, all platform IDs, format and publication date. Prefer the verified public YouTube publication of a cross-posted video. Preserve different edits and versions. Never infer same asset from titles.
3. Verify public availability and public-safe reuse separately from scheduling, receipts, playback and permission to embed. YouTube oEmbed identifies an item and offered embed but does not prove playback. Record unavailable sources/uncertain associations as holds. Artist social promotion belongs under campaign media, separately attributed from independent coverage.
4. Inspect anonymous current output and fresh saved editor content. Count visible links/players; ignore metadata, hidden markup and script strings. A video reference in metadata or a watch link alone is not an embed. The offline Tools/EPK Campaign Media/audit_campaign_media.py checker reports identity/coverage candidates; actual rendered visibility and playback need separate checks.
5. Stage a narrow cumulative merge. Preserve hero, artwork, controls, timing attachments/configuration, lyrics/cues, motion, downloads, publicity and design. Use a titled standard https://www.youtube.com/embed/VIDEO_ID player or supported privacy-enhanced host. Match aspect ratio, lazy load below fold, retain fullscreen/direct watch links and avoid autoplay. Respect minimum player dimensions and consent. Shorts use the same embed ID contract in a portrait container. Record restrictions with factual link fallback; never remove an age restriction to make an embed work.
6. Validate complete candidate hashes, UTF-8, timing literals and retained features. Inspect desktop/tablet/mobile layout, controls, keyboard access and actual progression. Apply Workflows/epk-mobile-motion.md and existing evidence gates without adding motion to static media cards. Label synthetic/local rendering and physical device limits.
7. Use the existing exact candidate public-save confirmation unless this exact addition independently meets limited standing publicity permission. Re-read editor immediately before save; re-merge and revalidate if changed. Save once, reopen and match exact payload/unchanged metadata, then verify anonymous source and responsive retained features. A save notice alone is not completion.
8. Update release-local ledger, mirrors and generator inputs. Preserve history. Keep recorded, staged, awaiting approval, published and verified-live states distinct. Do not resave passing pages. Scheduled publication creates a pending reconciliation action, never a live claim.

## Checker contract

Input ledger JSON rows contain epk_id, url, kind (video/short/post), publication_state (verified_public only after original-source review), optional asset_group and embed_blocked_reason. Public-use eligibility, visible rendering and actual playback are separate evidence. Grouping requires an explicit asset identity; prefer YouTube once per group. Compare content.rendered in a WordPress catalogue by exact platform item identity.

Run: python "Z:/My Songs/Tools/EPK Campaign Media/audit_campaign_media.py" ledger.json catalogue.json --output coverage.json

Primary embedding references reviewed 12 October 2026: https://support.google.com/youtube/answer/171780?hl=en-GB and https://developers.google.com/youtube/player_parameters . Age-restricted items may require watching on YouTube; do not bypass this.
