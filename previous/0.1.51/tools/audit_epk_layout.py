"""Check recorded responsive EPK observations; no browser or website writes."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

REQUIRED_WIDTHS = (320, 375, 390, 414, 430, 760, 768, 900, 1440)


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def audit_widths(rows):
    failures = []
    if not isinstance(rows, list):
        return ['Responsive observations must be an explicit list']
    widths = [row.get('width') for row in rows if isinstance(row, dict)]
    if len(widths) != len(rows) or any(type(w) is not int or w <= 0 for w in widths):
        return ['Each responsive observation needs a positive integer target width']
    if len(widths) != len(set(widths)):
        failures.append('Duplicate responsive width; keep additional states in separate records')
    missing = sorted(set(REQUIRED_WIDTHS) - set(widths))
    if missing:
        failures.append(f'Missing responsive widths: {missing}')
    for row in rows:
        width = row['width']
        label = f'{width}px'
        height = row.get('height')
        if type(height) is not int or height <= 0:
            failures.append(f'{label}: missing target height')
        if row.get('evidence_kind') not in ('emulated', 'physical'):
            failures.append(f'{label}: declare emulated or physical evidence')
        if row.get('ready_state') != 'complete':
            failures.append(f'{label}: document load is not complete')
        if not finite(row.get('measured_width')) or abs(row['measured_width'] - width) > 1:
            failures.append(f'{label}: requested viewport was not actually applied')
        if not finite(row.get('measured_height')) or not finite(height) or abs(row['measured_height'] - height) > 1:
            failures.append(f'{label}: requested viewport height was not actually applied')
        client, scroll = row.get('client_width'), row.get('scroll_width')
        if not finite(client) or not finite(scroll) or client <= 0 or client > width + 1 or client < width - 24 or scroll > client + 1 or row.get('overflow') is not False:
            failures.append(f'{label}: page overflow or invalid viewport measurements')
        for field in ('content_overflow', 'text_overflow', 'clipped_text'):
            findings = row.get(field)
            if not isinstance(findings, list):
                failures.append(f'{label}: {field} was not measured')
            elif findings:
                failures.append(f'{label}: {field} has {len(findings)} finding(s)')
        alignments = row.get('alignments')
        if not isinstance(alignments, list) or not alignments:
            failures.append(f'{label}: no declared artwork/content alignment check')
        else:
            for alignment in alignments:
                if not isinstance(alignment, dict):
                    failures.append(f'{label}: invalid alignment record')
                    continue
                ident = alignment.get('selector', '?')
                expected = alignment.get('expected')
                tolerance = alignment.get('tolerance', 2)
                target, container = alignment.get('target', {}), alignment.get('container', {})
                if type(alignment.get('matches')) is not int or type(alignment.get('container_matches')) is not int or alignment['matches'] != 1 or alignment['container_matches'] != 1:
                    failures.append(f'{label}: {ident} does not resolve uniquely')
                    continue
                if not isinstance(target, dict) or not isinstance(container, dict):
                    failures.append(f'{label}: {ident} has invalid alignment rectangles')
                    continue
                values = [target.get('left'), target.get('right'), container.get('left'), container.get('right')]
                if not all(finite(v) for v in values) or not finite(tolerance) or not 0 <= tolerance <= 4 or target['right'] <= target['left'] or container['right'] <= container['left']:
                    failures.append(f'{label}: {ident} has invalid alignment measurements')
                    continue
                left, right, c_left, c_right = values
                errors = {'center': [abs((left + right - c_left - c_right) / 2)],
                          'start': [abs(left - c_left)], 'end': [abs(right - c_right)],
                          'fill': [abs(left - c_left), abs(right - c_right)]}
                if expected not in errors or max(errors[expected]) > tolerance:
                    failures.append(f'{label}: {ident} has uneven alignment/gutters')
        screenshot = row.get('screenshot', {})
        if not isinstance(screenshot, dict) or not screenshot.get('path') or type(screenshot.get('width')) is not int or type(screenshot.get('height')) is not int or abs(screenshot['width']-width)>1 or not finite(height) or abs(screenshot['height']-height)>1 or screenshot.get('reviewed') is not True:
            failures.append(f'{label}: missing reviewed screenshot at the actual target dimensions')
        if row.get('below_fold_reviewed') is not True:
            failures.append(f'{label}: below-fold content/controls have not been reviewed')
        for findings, review in (('scrolling_descendants', 'scrolling_containers_reviewed'), ('offscreen_focus_links', 'focus_links_reviewed')):
            if not isinstance(row.get(findings), list):
                failures.append(f'{label}: {findings} inventory missing')
            elif row[findings] and row.get(review) is not True:
                failures.append(f'{label}: intentional {findings} need touch/keyboard review')
        media = row.get('visible_images')
        if not isinstance(media, list):
            failures.append(f'{label}: visible artwork readiness was not checked')
        elif any(not isinstance(image, dict) or image.get('complete') is not True or not finite(image.get('natural_width')) or image['natural_width'] <= 0 for image in media):
            failures.append(f'{label}: visible artwork is not loaded')
    return failures


def audit(record):
    failures = audit_widths(record.get('widths'))
    return {'page_id': record.get('page_id'), 'status': 'failed' if failures else 'passed',
            'failures': failures, 'required_widths': list(REQUIRED_WIDTHS),
            'limits': 'Recorded layout evidence only. Screenshot dimensions and review declarations must come from the actual capture. No publication, playback or physical-phone certification.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=Path)
    options = parser.parse_args()
    records = json.loads(options.records.read_text(encoding='utf-8-sig'))
    results = [audit(record) for record in (records if isinstance(records, list) else [records])]
    print(json.dumps(results, ensure_ascii=False, indent=2, allow_nan=False))
    raise SystemExit(any(row['status'] != 'passed' for row in results))
