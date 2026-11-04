"""Validate recorded EPK motion/timing evidence. No browser, network or writes."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from audit_epk_layout import audit_widths

RESETS = ('motion_off', 'reduced_motion', 'forced_colours', 'hidden', 'rotation', 'teardown')

def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

def audit_motion(motion):
    failures = []
    required = motion.get('required_consumers', [])
    routes = motion.get('routes', [])
    if not required:
        if not motion.get('intentional_static_reason'):
            failures.append('No motion consumers declared and no intentional-static reason')
        return failures
    if len(required) != len(set(required)):
        failures.append('Duplicate required motion consumer')
    for consumer in required:
        matching = [r for r in routes if r.get('consumer') == consumer]
        if len(matching) != 1:
            failures.append(f'{consumer}: expected one complete phone route')
            continue
        route = matching[0]
        if not route.get('controller') or type(route.get('sensor_owner_count')) is not int or route['sensor_owner_count'] != 1:
            failures.append(f'{consumer}: missing controller or competing sensor owners')
        if route.get('evidence_kind') not in ('synthetic', 'emulated', 'physical'):
            failures.append(f'{consumer}: unknown evidence kind')
        sample = route.get('sample', {})
        x, y = sample.get('x'), sample.get('y')
        if not finite(x) or not finite(y) or max(abs(x), abs(y)) > 1 or max(abs(x), abs(y)) <= .1:
            failures.append(f'{consumer}: missing meaningful bounded delivered sample')
        if not route.get('visual_before') or not route.get('visual_after') or route['visual_before'] == route['visual_after']:
            failures.append(f'{consumer}: no painted response to the delivered sample')
        if route.get('extent_within_bounds') is not True:
            failures.append(f'{consumer}: motion extent not verified')
        resets = route.get('resets', {})
        for name in RESETS:
            point = resets.get(name, {})
            if not finite(point.get('x')) or not finite(point.get('y')) or max(abs(point['x']), abs(point['y'])) > .001:
                failures.append(f'{consumer}: {name} neutral/reset evidence missing')
        if route.get('desktop_pointer_preserved') is not True:
            failures.append(f'{consumer}: independent desktop pointer parity missing')
    return failures

def audit_timing(timing):
    failures = []
    if not isinstance(timing.get('hardcoded_literals'), list) or not isinstance(timing.get('configured'), dict) or not isinstance(timing.get('consumers'), list):
        failures.append('Timing source scan, configuration and consumer inventory must be explicit')
    if timing.get('hardcoded_literals'):
        failures.append('Hardcoded timing source outside plugin-generated metadata')
    configured = timing.get('configured', {})
    consumers = timing.get('consumers', [])
    ids = [c.get('id') for c in consumers]
    if any(not i for i in ids) or len(ids) != len(set(ids)):
        failures.append('Missing or duplicate timing consumer identity')
    for consumer in consumers:
        ident = consumer.get('id', '?')
        kind = consumer.get('kind')
        if kind not in ('lyric', 'cue'):
            failures.append(f'{ident}: unknown timing kind')
            continue
        track = consumer.get('track')
        selected = timing.get('tracks', {}).get(track, {}).get(kind) if track else configured.get(kind)
        if timing.get('multi_track') is True and not track:
            failures.append(f'{ident}: multi-track consumer has no exact track association')
        if selected:
            if consumer.get('resolved_url') != selected:
                failures.append(f'{ident}: source differs from selected metadata (exact URL required)')
            if consumer.get('state') != 'ready' or not isinstance(consumer.get('parsed_count'), int) or isinstance(consumer.get('parsed_count'), bool) or consumer['parsed_count'] <= 0:
                failures.append(f'{ident}: hosted/parser readiness not verified')
        elif consumer.get('state') != 'unavailable' or consumer.get('download_disabled') is not True or consumer.get('audio_and_readable_lyrics_retained') is not True:
            failures.append(f'{ident}: missing metadata needs an accurate unavailable fallback')
    if any(c.get('resolved_url') for c in consumers) and timing.get('metadata_only_change_proved') is not True:
        failures.append('Metadata-only timing change has not reached every dependent consumer')
    return failures

def audit(record):
    failures = audit_motion(record.get('motion', {})) + audit_timing(record.get('timing', {}))
    failures.extend(audit_widths(record.get('widths')))
    kinds = sorted({r.get('evidence_kind') for r in record.get('motion', {}).get('routes', []) if r.get('evidence_kind')})
    return {'page_id': record.get('page_id'), 'status': 'failed' if failures else 'passed',
            'failures': failures, 'motion_evidence_kinds': kinds,
            'physical_sensor_evidence_declared': bool(kinds) and kinds == ['physical'],
            'limits': 'Recorded evidence only. A pass does not certify publication, physical frame rate, rights or keyword demand.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=Path)
    args = parser.parse_args()
    records = json.loads(args.records.read_text(encoding='utf-8-sig'))
    if isinstance(records, dict):
        records = [records]
    results = [audit(record) for record in records]
    print(json.dumps(results, ensure_ascii=False, indent=2, allow_nan=False))
    raise SystemExit(any(result['status'] != 'passed' for result in results))
