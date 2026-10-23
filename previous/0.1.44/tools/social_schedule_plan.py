"""Read-only, local social calendar preflight. Never uploads or schedules posts."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html import escape
import json
from pathlib import Path
from zoneinfo import ZoneInfo

STATES = {"prepared", "uploading", "mutation_pending", "private_draft",
          "scheduled", "published", "verified_live", "terminal_hold"}
ACTIVE = STATES - {"terminal_hold"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def payload_hash(row):
    """Bind approval to the destination, slot, settings and every attachment."""
    payload = {key: row.get(key) for key in
               ("destination", "account", "local_time", "timezone", "utc",
                "files", "settings")}
    return digest(json.dumps(payload, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":")).encode("utf-8"))


def resolve_time(local_time, zone, expected_utc):
    local = datetime.fromisoformat(local_time)
    if local.tzinfo is not None:
        raise ValueError("local_time must omit an offset; supply timezone and utc")
    tz = ZoneInfo(zone)
    candidates = set()
    for fold in (0, 1):
        utc = local.replace(tzinfo=tz, fold=fold).astimezone(timezone.utc)
        if utc.astimezone(tz).replace(tzinfo=None) == local:
            candidates.add(utc)
    expected = datetime.fromisoformat(expected_utc.replace("Z", "+00:00"))
    if expected.tzinfo is None or expected.utcoffset().total_seconds() != 0:
        raise ValueError("utc must explicitly have zero offset")
    if expected not in candidates:
        raise ValueError("UTC mismatch or nonexistent local time")
    return expected


def evidence_present(value, root):
    return (isinstance(value, str) and bool(value.strip()) and
            (root / value).is_file())


def evaluate(plan, root, now):
    if plan.get("schema") != "workflowmoves.social-plan.v1":
        raise ValueError("Unsupported plan schema")
    if now.tzinfo is None:
        raise ValueError("now must include a timezone")
    items = plan.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("Plan needs a nonempty items list")
    results, identities, slots, ids = [], {}, {}, set()
    for row in items:
        if not isinstance(row, dict):
            raise ValueError("Each item must be an object")
        problems, holds = [], []
        result = {"id": row.get("id"), "destination": row.get("destination"),
                  "account": row.get("account"), "state": row.get("state"),
                  "local_time": row.get("local_time"), "timezone": row.get("timezone"),
                  "utc": row.get("utc"), "problems": problems, "holds": holds}
        results.append(result)
        for key in ("id", "destination", "account", "local_time", "timezone", "utc"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                problems.append(f"Missing {key}")
        if not isinstance(row.get("id"), str):
            raise ValueError("Item id must be text")
        if row.get("id") in ids:
            problems.append("Duplicate item id")
        ids.add(row.get("id"))
        if row.get("state") not in STATES:
            problems.append("Unknown evidence state")
        try:
            instant = resolve_time(row["local_time"], row["timezone"], row["utc"])
            if instant <= now and row.get("state") not in {"published", "verified_live", "terminal_hold"}:
                holds.append("Slot has passed: choose an authorised future slot")
        except (ValueError, KeyError, TypeError) as exc:
            problems.append(f"Invalid schedule: {exc}")
            instant = None
        files = row.get("files", {})
        if not isinstance(files, dict) or not all(k in files for k in ("video", "caption")):
            problems.append("Video and caption files are required")
            files = files if isinstance(files, dict) else {}
        for name, file in files.items():
            try:
                actual = digest((root / file["path"]).read_bytes())
                if actual != file["sha256"].lower():
                    problems.append(f"Changed {name} bytes")
            except (OSError, KeyError, TypeError) as exc:
                problems.append(f"Unavailable {name}: {exc}")
        current_hash = payload_hash(row)
        result["payload_sha256"] = current_hash
        approval = row.get("approval", {})
        if approval.get("payload_sha256") != current_hash or not evidence_present(approval.get("evidence"), root):
            holds.append("Exact payload approval evidence missing or changed")
        queue = row.get("queue_check", {})
        if not evidence_present(queue.get("evidence"), root) or not queue.get("observed_at"):
            holds.append("Independent queue inspection required before mutation")
        # A broker's pending job does not prove a native platform schedule.
        for old in row.get("replaces", []):
            if old.get("state") != "cancelled_verified" or not evidence_present(old.get("evidence"), root):
                holds.append("Prior publisher cancellation is unverified")
        window = row.get("window")
        if window and row.get("local_time", "")[:10] > window.get("last_selectable_date", ""):
            holds.append("Outside observed native date window; " +
                         ("reuse the existing private draft" if row.get("state") == "private_draft" else
                          "retain the current payload and verify any pending save before continuing"))
            result["next_action_at"] = window.get("next_check")
        state = row.get("state")
        if state in {"scheduled", "published", "verified_live"}:
            receipt = row.get("native_receipt", {})
            if (receipt.get("utc") != row.get("utc") or not receipt.get("id_or_url") or
                    not evidence_present(receipt.get("evidence"), root)):
                problems.append("Native receipt must match the exact UTC slot and retain evidence")
        if state in {"uploading", "mutation_pending"}:
            holds.append("Existing mutation pending: observe, do not resubmit")
        if state == "terminal_hold" and not row.get("reason"):
            problems.append("Terminal hold needs a precise reason")
        if state in ACTIVE:
            identity = (row.get("destination"), row.get("account"),
                        files.get("video", {}).get("sha256", "").lower())
            if identity in identities:
                problems.append(f"Same asset already handled by {identities[identity]}")
            identities[identity] = row.get("id")
            slot = (row.get("destination"), row.get("account"), instant)
            if instant and slot in slots:
                problems.append(f"Slot collision with {slots[slot]}")
            slots[slot] = row.get("id")
        result["action"] = ("invalid" if problems else
                            "already_persisted" if state in {"scheduled", "published", "verified_live"} else
                            "terminal_hold" if state == "terminal_hold" else
                            "hold" if holds else "ready_for_native_preflight")
    return {"schema": "workflowmoves.social-preflight.v1", "observed_at": now.isoformat(),
            "valid": not any(r["problems"] for r in results), "items": results,
            "limits": "Local evidence check only. Reinspect current native queues and fields before any mutation; no upload, approval or publication is performed."}


def render_html(report):
    body = []
    for row in sorted(report["items"], key=lambda r: str(r["utc"])):
        values = [row["local_time"], row["timezone"], row["utc"], row["destination"],
                  row["account"], row["state"], row["action"],
                  "; ".join(row["problems"] + row["holds"]), row.get("next_action_at", "")]
        body.append("<tr>" + "".join(f"<td>{escape(str(v))}</td>" for v in values) + "</tr>")
    return ("<!doctype html><html lang='en'><meta charset='utf-8'><title>Direct publication plan</title>"
            "<style>body{font:1rem system-ui;margin:2rem;background:#141924;color:#edf2ff}"
            "table{border-collapse:collapse;width:100%}th,td{padding:.7rem;text-align:left;border:1px solid #526079}"
            "td{overflow-wrap:anywhere}caption{font-size:1.4rem;margin:1rem}</style>"
            "<h1>Direct publication plan</h1><p>Local preflight; current platform evidence remains authoritative.</p>"
            "<table><caption>Future slots and continuation queue</caption><thead><tr>" +
            "".join(f"<th scope='col'>{h}</th>" for h in
                    ("Local time", "Timezone", "UTC", "Destination", "Account", "Evidence state", "Next action", "Reason", "Recheck")) +
            "</tr></thead><tbody>" + "".join(body) + "</tbody></table><p>" + escape(report["limits"]) + "</p></html>")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--html", type=Path)
    parser.add_argument("--now", help="Explicit ISO timestamp for reproducible checks")
    args = parser.parse_args()
    now = datetime.fromisoformat(args.now.replace("Z", "+00:00")) if args.now else datetime.now(timezone.utc)
    source = args.plan.read_bytes()
    report = evaluate(json.loads(source), args.plan.resolve().parent, now)
    report["plan_sha256"] = digest(source)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.html:
        args.html.write_text(render_html(report), encoding="utf-8")
    print(json.dumps({"valid": report["valid"], "items": len(report["items"]), "output": str(args.output)}))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
