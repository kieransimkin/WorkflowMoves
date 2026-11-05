# Publish EPK changes through WordPress REST

Use this companion for a WordPress EPK with registered REST fields and a supported publication gate. Keep credentials and host configuration in the owning project. For read-only timing checks, follow [Audit EPK timing authority](epk-timing-authority-audit.md).

1. Use an authorised, revocable Application Password over HTTPS. Read the exact page via the [documented Pages endpoint](https://developer.wordpress.org/rest-api/reference/pages/) with `context=edit`. Save decoded `content.raw` as UTF-8 without a BOM. Record its SHA-256 and the reviewed page fields and attachments. Read the signed-out presentation separately.
2. Merge into fresh editor source and hash the candidate. For a body-only update, send only `content`. Preserve unrelated fields, source mappings, controls and layout. Review the exact preview at the relevant desktop, tablet and phone widths.
3. Where the site uses Full Canvas, verify the saved template and the rendered wrapper and release-root geometry. Keep the closed site menu clear of the hero. For a future release with an Add to calendar control, verify the decoded Google, Outlook and Apple/iCal dates and keyboard use. For YouTube reveals, check idle, playing and restored states using the [responsive gate](epk-responsive-layout-qa.md#check-youtube-reveal-and-return-before-publishing). Bind evidence to the page, preview and exact candidate.
4. Require exact action authority. Re-read the page immediately before the write and compare the source hash and reviewed field values. Rebase and revalidate if anything reviewed drifted. Submit one request through the site's supported gate with only the approved fields.
5. Independently read back the authenticated source and changed fields. Verify the anonymous result, including actual playback, timing and interactions in scope. Reconcile local mirrors and generator inputs with the verified result.

## Potential problems

- **A timeout or source transformation leaves the result uncertain.** Read the persisted source and fields before any retry.
- **Raw content matches and the page still breaks.** Check anonymous rendered markup, script and stylesheet behaviour. Repeat the affected interaction.
- **The REST schema omits a required field.** Hold it until a supported route is available. Preserve the candidate and use the browser for authorised visual QA.
- **A published page needs a future update.** Schedule the authorised helper against fresh source. Setting the existing page to future can remove it from public view.

The [responsive EPK guide](epk-responsive-layout-qa.md) describes the visual evidence. The [public DanceMoves playback demo](https://github.com/kieransimkin/DanceMoves/blob/v3.5.0/examples/lyric-scroll/demonstration.webm) shows one interactive surface that needs separate runtime checks. Authenticated transport evidence stays in the private project record.
