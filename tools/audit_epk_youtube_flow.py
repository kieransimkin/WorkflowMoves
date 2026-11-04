"""Validate recorded EPK YouTube reveal states without operating the browser."""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

WIDTHS = (320, 375, 390, 414, 430, 760, 768, 900, 1440)
STATES = ('idle', 'playing', 'restored')
VIDEO_ID = re.compile(r'^[\w-]{11}$', re.ASCII)


def edges(box, width):
    if not isinstance(box, dict):
        return None
    left, right, top, bottom = (box.get(key) for key in ('left', 'right', 'top', 'bottom'))
    if not all(type(value) in (int, float) and math.isfinite(value) for value in (left, right, top, bottom)):
        return None
    return (left, right, top, bottom) if -1 <= left < right <= width + 1 and top < bottom else None


def order(first, second):
    if first[1] <= second[0] + 1:
        return 'left'
    if second[1] <= first[0] + 1:
        return 'right'
    if first[3] <= second[2] + 1:
        return 'above'
    if second[3] <= first[2] + 1:
        return 'below'
    return 'overlap'


def audit_transition(entry, width, label):
    states = entry.get('states')
    if not isinstance(states, dict) or set(states) != set(STATES):
        return [f'{label}: record the idle, playing and restored states']
    if entry.get('input') not in ({'touch'} if width <= 430 else {'mouse', 'keyboard'}):
        return [f'{label}: open and close with the required viewport input']
    failures, boxes, identities = [], {}, {}
    for phase in STATES:
        state = states[phase]
        if not isinstance(state, dict):
            failures.append(f'{label}: missing {phase} observation')
            continue
        prefix = f'{label}, {phase}'
        if state.get('video_id') != entry.get('video_id') or state.get('viewport_width') != width:
            failures.append(f'{prefix}: unexpected YouTube ID or measured viewport')
        if state.get('horizontal_overflow') is not False:
            failures.append(f'{prefix}: horizontal overflow or missing viewport measurement')
        playing = phase == 'playing'
        copy = state.get('copy')
        if not isinstance(copy, dict) or not copy:
            failures.append(f'{prefix}: declare the title, release copy and actions')
            continue
        following_selector = state.get('following_selector')
        identities[phase] = (tuple(copy), following_selector if isinstance(following_selector, str) else None)
        frame = edges(state.get('frame'), width)
        poster = edges(state.get('poster'), width)
        opener = edges(state.get('opener'), width)
        close = edges(state.get('close'), width)
        following = edges(state.get('following'), width)
        text = {selector: edges(box, width) for selector, box in copy.items()}
        if any(box is None for box in text.values()):
            failures.append(f'{prefix}: release copy or links are hidden, clipped or missing')
        if not following or not isinstance(following_selector, str) or not following_selector.strip():
            failures.append(f'{prefix}: the following content section was not measured')
        if playing:
            if not frame or not close or poster or opener or state.get('frame_count') != 1:
                failures.append(f'{prefix}: require one visible frame, its return control and the covered poster')
        elif not poster or not opener or close or state.get('frame_count') != 0:
            failures.append(f'{prefix}: require visible artwork and opener with the player and return control removed')
        media = frame if playing else poster
        if media is None or following is None or any(box is None for box in text.values()):
            continue
        boxes[phase] = (media, text, following)
        if following[2] < max(box[3] for box in [media, *text.values(), *([close] if close else [])]) - 1:
            failures.append(f'{prefix}: the hero overlaps the following section')
        if playing and any(order(media, box) == 'overlap' for box in text.values()):
            failures.append(f'{prefix}: the playing frame covers release copy or links')
        if phase == 'restored' and state.get('focus_on_opener') is not True:
            failures.append(f'{prefix}: keyboard focus did not return to the opener')
    if len(boxes) == len(STATES):
        if len(set(identities.values())) != 1:
            failures.append(f'{label}: check the same copy and following section in all states')
            return failures
        poster, idle_copy, next_idle = boxes['idle']
        frame, playing_copy, _ = boxes['playing']
        restored, restored_copy, next_restored = boxes['restored']
        close = edges(states['playing'].get('close'), width)
        if close and frame[1] - frame[0] > poster[1] - poster[0] + 4 and order(frame, close) == 'overlap':
            failures.append(f'{label}: the return control overlaps the expanded YouTube frame')
        heading = next(iter(idle_copy))
        idle_order = order(poster, idle_copy[heading])
        expected = entry.get('playing_order') if idle_order == 'overlap' else idle_order
        if expected not in ('left', 'right', 'above', 'below') or order(frame, playing_copy[heading]) != expected:
            failures.append(f'{label}: opening changes the declared flow of the player and heading')
        idle_boxes = [poster, *idle_copy.values(), next_idle]
        restored_boxes = [restored, *restored_copy.values(), next_restored]
        if any(abs(a - b) > 4 for before, after in zip(idle_boxes, restored_boxes) for a, b in zip(before, after)):
            failures.append(f'{label}: closing leaves the artwork, copy or following section out of place')
    return failures


def audit(record, expected_ids=()):
    failures = []
    rows = record.get('widths')
    if not isinstance(rows, list) or any(not isinstance(row, dict) or type(row.get('width')) is not int for row in rows):
        return ['Record explicit viewport observations for the YouTube reveal gate']
    widths = [row['width'] for row in rows]
    missing = sorted(set(WIDTHS) - set(widths))
    if missing or len(widths) != len(set(widths)):
        failures.append(f'Expected one row per viewport. Missing widths: {missing}')
    declared = None
    declared_players = None
    for row in rows:
        width = row['width']
        prefix = f'{width}px'
        inventory, entries = row.get('youtube_cover_ids'), row.get('youtube_reveals')
        if not isinstance(inventory, list) or any(not isinstance(v, str) or not VIDEO_ID.fullmatch(v) for v in inventory):
            failures.append(f'{prefix}: the detected YouTube cover inventory must be explicit')
            continue
        if not isinstance(entries, list) or any(not isinstance(e, dict) for e in entries):
            failures.append(f'{prefix}: the YouTube reveal checks must be explicit')
            continue
        if declared is None:
            declared = sorted(inventory)
        if sorted(inventory) != declared:
            failures.append(f'{prefix}: detected YouTube covers differ across viewports')
        ids, selectors = [e.get('video_id') for e in entries], [e.get('player') for e in entries]
        if (any(not isinstance(v, str) or not VIDEO_ID.fullmatch(v) for v in ids)
                or any(not isinstance(s, str) or not s.strip() for s in selectors)):
            failures.append(f'{prefix}: invalid YouTube player identity')
            continue
        if len(set(selectors)) != len(selectors) or any(ids.count(v) < inventory.count(v) for v in set(inventory)):
            failures.append(f'{prefix}: every detected cover needs its own reveal check')
        players = set(zip(selectors, ids))
        if declared_players is None:
            declared_players = players
        elif players != declared_players:
            failures.append(f'{prefix}: check the same YouTube players across viewports')
        if any(ids.count(v) < expected_ids.count(v) for v in set(expected_ids)):
            failures.append(f'{prefix}: the checks omit a YouTube cover in the reviewed editor source')
        for entry in entries:
            failures.extend(audit_transition(entry, width, f'{prefix} {entry["player"]}'))
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path)
    parser.add_argument('--page-id', required=True, type=int)
    parser.add_argument('--source-sha256', required=True)
    parser.add_argument('--candidate-sha256', required=True)
    parser.add_argument('--expected-video-id', action='append', default=[])
    args = parser.parse_args()
    record = json.loads(args.evidence.read_text(encoding='utf-8-sig'))
    identity = (args.page_id, args.source_sha256, args.candidate_sha256)
    if not isinstance(record, dict) or tuple(record.get(k) for k in ('page_id', 'source_sha256', 'candidate_sha256')) != identity:
        failures = ['Evidence does not match the page ID, reviewed source and candidate hashes']
    else:
        failures = audit(record, args.expected_video_id)
    print(json.dumps({'status': 'failed' if failures else 'passed', 'failures': failures}, indent=2))
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
