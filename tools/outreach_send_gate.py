"""Private atomic send claims. No email access, sending, credentials or approval grants."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import secrets


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def write_new(path, value):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())

def claim(root, account, venue, obligation, owner, packet, approval):
    if not all(str(x or '').strip() for x in (account, venue, obligation, owner, packet, approval)):
        raise ValueError('Complete owner, venue, obligation, packet and approval references required')
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    identity = account.strip().casefold() + '\n' + venue.strip().casefold()
    key = hashlib.sha256(identity.encode()).hexdigest()
    action = hashlib.sha256((identity + '\n' + obligation.strip().casefold()).encode()).hexdigest()
    packet = Path(packet).resolve(strict=True)
    value = dict(schema='outreach.send.claim.v1', created_at=datetime.now(timezone.utc).isoformat(),
                 account=account, venue=venue, obligation=obligation, owner=owner,
                 token=secrets.token_hex(24), packet=str(packet),
                 packet_sha256=hashlib.sha256(packet.read_bytes()).hexdigest(),
                 approval_reference=approval, key=key, action=action, state='claimed_not_sent')
    lock = root / (key + '.active.json')
    write_new(lock, value)  # Venue-wide mutex blocks even a different competing payload.
    try:
        write_new(root / (action + '.claim.json'), value)  # Permanent duplicate tombstone.
    except Exception:
        if read(lock).get('token') == value['token']:
            lock.unlink()  # Only this invocation's exact newly created mutex.
        raise
    return value

def _inspect(root, key, token):
    if not key or len(key) != 64 or any(c not in '0123456789abcdef' for c in key):
        raise ValueError('Invalid claim key')
    value = read(Path(root) / (key + '.active.json'))
    if not secrets.compare_digest(value['token'], token or ''):
        raise ValueError('Claim owned by another execution')
    if hashlib.sha256(Path(value['packet']).read_bytes()).hexdigest() != value['packet_sha256']:
        raise ValueError('Approved packet changed; do not send')
    return value

def inspect(root, key, token):
    transition = Path(root) / (key + '.transition.json')
    if transition.exists():
        raise ValueError('Owned claim transition pending; do not send')
    value = _inspect(root, key, token)
    if transition.exists():
        raise ValueError('Owned claim transition pending; do not send')
    return value


@contextmanager
def _transition(root, key, token):
    _inspect(root, key, token)
    path = Path(root) / (key + '.transition.json')
    nonce = secrets.token_hex(24)
    write_new(path, dict(token=token, nonce=nonce))
    try:
        yield _inspect(root, key, token)
    finally:
        if read(path).get('nonce') == nonce:
            path.unlink()


def reapprove(root, key, token, packet, approval, expected_packet_sha256, pre_send_evidence):
    """Rebind a never-sent owned obligation after explicit changed-copy approval.

    Caller evidence does not prove mailbox state or grant send permission.
    Crashed transitions fail closed; there is no automatic takeover.
    """
    with _transition(root, key, token) as value:
        if value.get('state') != 'claimed_not_sent':
            raise ValueError('Only a never-sent claim can be reapproved')
        if (Path(root) / (value['action'] + '.receipt.json')).exists():
            raise ValueError('Completed obligation cannot be reapproved')
        if value['packet_sha256'] != expected_packet_sha256:
            raise ValueError('Claim changed since review; do not send')
        packet = Path(packet).resolve(strict=True)
        packet_hash = hashlib.sha256(packet.read_bytes()).hexdigest()
        approval_path = Path(approval).resolve(strict=True)
        approved = read(approval_path)
        evidence_path = Path(pre_send_evidence).resolve(strict=True)
        evidence = read(evidence_path)
        if approved.get('packet_sha256') != packet_hash or approved.get('approved') is not True:
            raise ValueError('Exact new packet approval required')
        if (evidence.get('send_attempted') is not False or
                evidence.get('no_sufficient_sent') is not True or
                evidence.get('fully_paginated') is not True or
                evidence.get('key') != key or evidence.get('action') != value['action'] or
                not evidence.get('checked_at') or
                not evidence.get('recipient_sent_query') or not evidence.get('subject_sent_query')):
            raise ValueError('Independent pre-send reconciliation required')
        revision = int(value.get('revision', 0)) + 1
        journal = Path(root) / (value['action'] + '.reapproval.' + str(revision) + '.json')
        updated = dict(value, packet=str(packet), packet_sha256=packet_hash,
                       approval_reference=str(approval_path), revision=revision,
                       reapproval_record=str(journal),
                       reapproved_at=datetime.now(timezone.utc).isoformat())
        record = dict(schema='outreach.send.reapproval.v1', previous=value, current=updated,
                      approval_sha256=hashlib.sha256(approval_path.read_bytes()).hexdigest(),
                      pre_send_evidence=str(evidence_path),
                      pre_send_evidence_sha256=hashlib.sha256(evidence_path.read_bytes()).hexdigest())
        write_new(journal, record)
        staged = Path(root) / (key + '.revision-' + secrets.token_hex(12) + '.tmp')
        write_new(staged, updated)
        try:
            os.replace(staged, Path(root) / (key + '.active.json'))
        finally:
            if staged.exists():
                staged.unlink()
        return updated


def finish(root, key, token, receipt):
    with _transition(root, key, token) as value:
        return _finish(root, key, token, receipt, value)


def _finish(root, key, token, receipt, value):
    receipt = read(receipt)
    if receipt.get('state') not in ('sent_verified', 'submission_verified', 'final_failure', 'aborted_before_send'):
        raise ValueError('Uncertain send retains the active claim; never retry blindly')
    if receipt['state'] == 'submission_verified':
        if not receipt.get('success_observed') or not receipt.get('destination_url'):
            raise ValueError('Observed form success and destination required')
        evidence_files = receipt.get('evidence_files')
        if not isinstance(evidence_files, list) or not evidence_files:
            raise ValueError('Retained submission evidence files required')
        for evidence in evidence_files:
            evidence_path = Path(evidence.get('path', '')).resolve(strict=True)
            if not evidence_path.is_file() or hashlib.sha256(evidence_path.read_bytes()).hexdigest() != evidence.get('sha256'):
                raise ValueError('Submission evidence hash mismatch; claim retained')
    elif receipt['state'] != 'aborted_before_send' and not receipt.get('message_id'):
        raise ValueError('Persisted message ID required')
    result = dict(schema='outreach.send.receipt.v1',
                  completed_at=datetime.now(timezone.utc).isoformat(), claim=value, evidence=receipt)
    write_new(Path(root) / (value['action'] + '.receipt.json'), result)
    lock = Path(root) / (key + '.active.json')
    if read(lock)['token'] != token:
        raise ValueError('Ownership changed; lock retained')
    lock.unlink()  # Permanent claim and receipt remain; only exact owned active mutex removed.
    return result

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('operation', choices=('claim', 'inspect', 'reapprove', 'finish', 'list'))
    p.add_argument('--root', type=Path, required=True, help='Private persistent claim directory; never commit its contents')
    for option in ('account', 'venue', 'obligation', 'owner', 'packet', 'approval', 'key', 'token', 'receipt', 'expected-packet-sha256', 'pre-send-evidence'):
        p.add_argument('--' + option)
    a = p.parse_args()
    if a.operation == 'claim':
        result = claim(a.root, a.account, a.venue, a.obligation, a.owner, a.packet, a.approval)
    elif a.operation == 'list':
        result = [read(x) for x in sorted(a.root.glob('*.active.json'))]
    elif a.operation == 'inspect':
        result = inspect(a.root, a.key, a.token)
    elif a.operation == 'reapprove':
        result = reapprove(a.root, a.key, a.token, a.packet, a.approval,
                           a.expected_packet_sha256, a.pre_send_evidence)
    else:
        result = finish(a.root, a.key, a.token, a.receipt)
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
