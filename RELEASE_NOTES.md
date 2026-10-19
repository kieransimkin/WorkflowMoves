# WorkflowMoves v0.1.35

Web forms can report a successful submission without producing an email message ID. The new duplicate-send gate records verified form receipts using retained success evidence and SHA-256 checks, so cooperating callers can release their owned venue mutex while retaining the permanent original-request claim.

The standard-library CLI also supports email Sent IDs, explicit pre-send aborts and final email failures. It fails closed on competing owners, changed approved packets, uncertain outcomes, missing form success and altered evidence files. It performs no sending, account action or approval. The claim directory is explicitly supplied and remains private.

Tests cover sixteen competing claimants, permanent duplicate prevention, ownership, approved-packet integrity and web-form evidence failures. Linux and Windows CI and the tag release workflow run the complete repository tests. The archive contains only generic code, synthetic tests and documentation; campaign records, recipient data, correspondence, captures and tokens remain outside it.
