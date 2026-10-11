"""Offline timing-source literal preflight. No network, credentials or writes."""
from __future__ import annotations
import argparse, html, json, re
from html.parser import HTMLParser
from pathlib import Path

METADATA_SCRIPT_ID = 'dance-moves-core-js-extra'

class TimingScanner(HTMLParser):
    def __init__(self, configured_urls=()):
        super().__init__(convert_charrefs=True)
        self.urls = set(u for u in configured_urls if u)
        self.hits = []
        self.script = None
        self.script_data = []

    def scan(self, text, context):
        # Whole quoted strings retain signed query parameters and encoded paths.
        strings = re.findall(r'''["'`]([^"'`\s<>]+)["'`]''', text)
        for value in strings:
            value = html.unescape(value)
            if value in self.urls or re.search(r'\.(?:lrc|cue)(?:[?#]|$)', value, re.I):
                self.hits.append({'url': value, 'context': context})

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'script':
            self.script = values.get('id', '')
            self.script_data = []
        # Only the exact plugin-owned metadata script is exempt, not the head.
        for name, value in attrs:
            if not value:
                continue
            timing_attr = bool(re.search(r'(?:lyric|cue).*?(?:url|src)|(?:url|src).*?(?:lyric|cue)', name, re.I))
            if timing_attr and value not in ('lyric', 'cue') and not value.startswith('data:'):
                self.hits.append({'url': value, 'context': f'{tag}[{name}]'})
            elif value in self.urls or re.search(r'\.(?:lrc|cue)(?:[?#]|$)', value, re.I):
                self.hits.append({'url': value, 'context': f'{tag}[{name}]'})

    def handle_data(self, data):
        if self.script is not None:
            self.script_data.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.script is not None:
            if self.script != METADATA_SCRIPT_ID:
                self.scan(''.join(self.script_data), 'inline script')
            self.script = None
            self.script_data = []

def audit(text, configured_urls=()):
    parser = TimingScanner(configured_urls)
    parser.feed(text)
    return parser.hits

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('html', type=Path)
    p.add_argument('--configured-url', action='append', default=[])
    args = p.parse_args()
    result = audit(args.html.read_text(encoding='utf-8-sig'), args.configured_url)
    print(json.dumps({'path': str(args.html), 'hardcoded_timing': result}, indent=2))
    raise SystemExit(1 if result else 0)
