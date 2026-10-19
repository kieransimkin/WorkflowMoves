"""Private atomic send claims. No email access, sending, credentials or approval grants."""
import argparse
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

def inspect(root, key, token):
    if not key or len(key) != 64 or any(c not in '0123456789abcdef' for c in key):
        raise ValueError('Invalid claim key')
    value = read(Path(root) / (key + '.active.json'))
    if not secrets.compare_digest(value['token'], token or ''):
        raise ValueError('Claim owned by another execution')
    if hashlib.sha256(Path(value['packet']).read_bytes()).hexdigest() != value['packet_sha256']:
        raise ValueError('Approved packet changed; do not send')
    return value

def finish(root, key, token, receipt):
    value = inspect(root, key, token)
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
    p.add_argument('operation', choices=('claim', 'inspect', 'finish', 'list'))
    p.add_argument('--root', type=Path, required=True, help='Private persistent claim directory; never commit its contents')
    for option in ('account', 'venue', 'obligation', 'owner', 'packet', 'approval', 'key', 'token', 'receipt'):
        p.add_argument('--' + option)
    a = p.parse_args()
    if a.operation == 'claim':
        result = claim(a.root, a.account, a.venue, a.obligation, a.owner, a.packet, a.approval)
    elif a.operation == 'list':
        result = [read(x) for x in sorted(a.root.glob('*.active.json'))]
    elif a.operation == 'inspect':
        result = inspect(a.root, a.key, a.token)
    else:
        result = finish(a.root, a.key, a.token, a.receipt)
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
