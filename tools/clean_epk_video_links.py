"""Remove redundant EPK video links without rewriting surrounding source.

Only a proven matching embedded player permits removal. Styled links, original
post citations, unrelated links and link-only unavailable-video fallbacks stay.
This module prepares source; it never publishes a page.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

try:
    from .audit_campaign_media import identity
except ImportError:
    from audit_campaign_media import identity


VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
WATCH = re.compile(r'\s*(?:[—–-]\s*)?watch\s+on\s+youtube\s*$', re.I)


@dataclass
class Node:
    tag: str
    attrs: dict
    start: int
    opening_end: int
    end: int = 0
    closing_start: int = 0
    parent: Node | None = None
    children: list = field(default_factory=list)

    def descendants(self):
        for child in self.children:
            yield child
            yield from child.descendants()


class SourceTree(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.lines = [0]
        self.lines.extend(m.end() for m in re.finditer('\n', source))
        self.root = Node('', {}, 0, 0, len(source))
        self.stack = [self.root]
        self.feed(source)

    def position(self):
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def handle_starttag(self, tag, attrs):
        start = self.position()
        end = start + len(self.get_starttag_text())
        node = Node(tag, dict(attrs), start, end, end, end, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack[-1].tag == tag and tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                node = self.stack[index]
                node.closing_start = self.position()
                node.end = self.source.index('>', node.closing_start) + 1
                del self.stack[index:]
                break


def text_of(source):
    return html.unescape(re.sub(r'<[^>]*>', '', source)).strip()


def has_player(container, video):
    for node in container.descendants():
        if node.tag == 'iframe' and identity(node.attrs.get('src', '')) == video:
            return True
    # A verified native replacement retains the original YouTube asset identity.
    return (container.attrs.get('data-campaign-native') == video
            and any(n.tag == 'video' for n in container.descendants()))


def clean(source):
    """Return minimally edited source plus reversible, exact-span evidence."""
    tree = SourceTree(source)
    edits = []
    for anchor in tree.root.descendants():
        if anchor.tag != 'a' or anchor.end <= anchor.opening_end:
            continue
        video = identity(anchor.attrs.get('href', ''))
        if not video.startswith('youtube:'):
            continue
        inside = source[anchor.opening_end:anchor.closing_start]
        label = text_of(inside)
        if not WATCH.search(label):
            continue
        classes = anchor.attrs.get('class', '').split()
        if 'epk-cover-player__watch' in classes:
            if not has_player(anchor.parent, video):
                continue
            replacement, kind = '', 'cover_watch_link'
        else:
            # Preserve every styled action, even one labelled Watch on YouTube.
            if classes or anchor.attrs.get('role') == 'button':
                continue
            caption = anchor.parent
            while caption and caption.tag not in {'figcaption', 'figure', ''}:
                caption = caption.parent
            if not caption or caption.tag != 'figcaption':
                continue
            figure = caption.parent
            if not figure or figure.tag != 'figure' or not has_player(figure, video):
                continue
            replacement = html.escape(WATCH.sub('', label).strip(), quote=False)
            kind = 'caption_watch_link'
        edits.append(dict(start=anchor.start, end=anchor.end,
                          before=source[anchor.start:anchor.end], after=replacement,
                          kind=kind, asset=video))
    result = source
    for edit in reversed(edits):
        result = result[:edit['start']] + edit['after'] + result[edit['end']:]
    # The caller can prove all non-target bytes survived by reversing these spans.
    return result, edits


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--record', type=Path, required=True)
    args = parser.parse_args()
    before = args.source.read_bytes()
    result, edits = clean(before.decode('utf-8', errors='strict'))
    after = result.encode('utf-8')
    args.output.write_bytes(after)
    args.record.write_text(json.dumps(dict(
        before_sha256=hashlib.sha256(before).hexdigest(),
        candidate_sha256=hashlib.sha256(after).hexdigest(), edits=edits),
        ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'removed_links': len(edits)}))


if __name__ == '__main__':
    main()
