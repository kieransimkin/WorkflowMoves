# Browser tab hygiene

Use for browser work in My Songs, including campaign scheduling, dashboard checks, previews and EPK QA. This is an ownership and completion workflow, not a background tab killer or a replacement browser driver.

## Start and reuse

Read the current Browser skill. Obtain the selected browser's fresh tab list through its documented controls. Record only the IDs, non-sensitive purpose, ownership and relevant URL; avoid private query data. Reuse a suitable existing tab. Keep the browser binding while it remains connected; an empty tab list after cleanup is normal. Replace a stale tab handle from that same browser, rather than rebuilding every connection.

For shared work, check the relevant private ownership records before borrowing or closing a tab. Silence is not a release of ownership. Keep routine coordination out of user-facing messages.

## Complete and close

Retain the required evidence before cleanup. Verify a send, save, upload or schedule through the destination's independent persisted view before closing its composer. Recheck visible state immediately before closure: a formerly read-only tab can now contain a form or active upload.

Close job-created tabs once their required verification is complete. Close borrowed tabs only when their owner or Kieran has released them. Consolidate duplicate read-only pages where ownership is clear. Preserve active and unsaved work, authentication handoffs and a tab deliberately left for Kieran; record why it remains, its owner and next action. A rejected or unavailable close is a precise hold, not permission to use an alternative driver or close an entire process.

Use the documented tab close operation, then obtain a fresh tab list and verify each expected ID is absent. Keep attempted and verified closure counts separate. Do not claim that an inaccessible tab closed. Finish the cleanup during the same job; do not silently carry ordinary completed tabs into another daily run.

## Windows and retained tabs

Close a job-created browser window after its last required tab has finished, using the documented window control if the selected browser exposes one. First close the eligible tabs through their supported controls. Where only tab closure is available, verify those closures and record the remaining window limitation; never terminate a browser, app or helper process as a substitute. Preserve windows containing another owner's active work or a deliberate user handoff.

Use the documented handoff mark only for a specific next action, and the deliverable mark only for a tab intentionally left for Kieran. Do not mark every tab merely to preserve a connection. Each retained tab or window needs an owner, reason and next action; review it on the next turn and close it promptly when that purpose ends. Agent-created tabs are temporary by default in the current in-app Browser, and marks are turn-scoped; do not rely on those defaults instead of same-job verification.

Complete cleanup after each finished browser phase and before returning the final result. Record attempted and independently verified tab/window closures separately, including retained or inaccessible items. A saved rule is configuration evidence, not proof of closure, adoption by another running chat or a permanent crash repair.

## Empty inventory and visible-tab discrepancies

An empty tool inventory establishes only that the selected connection reports no accessible tabs. If Kieran or the visible app shows browser tabs, record a session/window-scope discrepancy and verify the correct documented browser selection; do not label the chat or whole app clean from that empty result. Never inspect profiles/session stores or use private app internals to repair the mismatch. Distinguish tabs the agent successfully closed and independently verified absent from tabs that disappeared through Kieran or another owner; record manual closures separately.

If current visible tabs cannot be matched to a documented controllable session, retain a precise access hold. Keep scope-specific inventories, user-reported manual cleanup, successful close acknowledgements and subsequent absence distinct. A routing error or an empty list after a stale close does not prove the agent closed every former tab.

## Recovery and acceptance

Distinguish a stale tab, disconnected browser, kernel setup error and closed tool transport. Tab cleanup may reduce unused resources but does not diagnose any of these errors. Keep recovery attempts bounded and materially different. Do not create an endless chain of replacement tabs.

A browser-tool-only restart requires an actually supported reconnect/reload operation and proof that the previously failing call now succeeds. Do not terminate an app-managed helper to simulate a restart: a stopped helper can leave its client at `Transport closed` with no replacement. Do not terminate or restart Codex/ChatGPT or automate their settings UI. Do not alter credentials, trust controls, browser permissions or profile/session data.

For a full-tab reset, require explicit authority, inventory shared ownership and checkpoint unsaved state first. Preserve already-persisted platform items and sign-ins; closing a tab never authorises cancelling or recreating a schedule. Reconnect through the current Browser skill, inspect fresh authenticated state and recheck the original operation. Follow `codex-browser-runtime-recovery.md` for its separately approved fresh-chat route when the old transport cannot be restored.

Acceptance records distinguish: tabs closed and independently absent; tabs retained with reasons; browser connection restored; intended page successfully opened in the user-facing panel; authenticated page read; and the original job completed. None implies the others. Never promise immunity from future app or credit-related failures.
