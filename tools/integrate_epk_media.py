#!/usr/bin/env python3
"""Integrate an existing generic EPK campaign-media block into a reviewed design.

This is a source transformer only. It requires an explicit design profile, preserves
every iframe/video/audio/script byte, and never reads or writes WordPress.
"""
from __future__ import annotations

import argparse, hashlib, json, re
from html.parser import HTMLParser
from pathlib import Path


class Bounds(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False); self.stack=[]; self.sections=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs); node={"tag":tag,"attrs":d,"start":self.get_starttag_text() and self.getpos(),"offset":self.get_offset(),"end":None}
        self.stack.append(node)
    def handle_startendtag(self, tag, attrs): pass
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,-1,-1):
            n=self.stack[i]
            if n["tag"]==tag:
                n["end"]=self.get_offset()+len(f"</{tag}>")
                classes=n["attrs"].get("class","").split()
                if tag=="section" and "epk-campaign-media" in classes: self.sections.append(n)
                del self.stack[i:]; return
    def get_offset(self):
        line,col=self.getpos(); return sum(len(x) for x in self.rawdata.splitlines(True)[:line-1])+col


def media_bytes(text):
    return re.findall(r'<(?:iframe|video|audio|script)\b.*?</(?:iframe|video|audio|script)>', text, re.I|re.S)


def transform(source, profile):
    parser=Bounds(); parser.feed(source)
    if len(parser.sections)!=1: raise ValueError(f"expected one generic media section, found {len(parser.sections)}")
    n=parser.sections[0]; section=source[n['offset']:n['end']]
    original_media=media_bytes(section)
    page_id=str(profile['page_id']); title=profile['title']
    section=re.sub(r'<section\s+class="epk-campaign-media"[^>]*>',
        f'<section class="epk-campaign-media epk-campaign-media--integrated epk-campaign-media--{profile["motif"]}" data-media-design="{profile["profile_id"]}" aria-labelledby="campaign-media-{page_id}">',section,count=1)
    section=re.sub(rf'<h2\s+id="campaign-media-{re.escape(page_id)}">.*?</h2>\s*<p>.*?</p>',
        f'<header class="epk-campaign-media__header"><p class="epk-campaign-media__eyebrow">{profile["eyebrow"]}</p><h2 id="campaign-media-{page_id}">{profile["heading"]}</h2><p>{profile["intro"]}</p></header>',section,count=1,flags=re.S)
    section=re.sub(r'<div\s+style="display:grid;grid-template-columns:[^"]+">', '<div class="epk-campaign-media__grid">', section, count=1)
    def fig(m):
        block=m.group(0); kind='film' if re.search(r'aspect-ratio\s*:\s*16\s*/\s*9',block,re.I) else 'short'
        return re.sub(r'<figure\b',f'<figure class="epk-campaign-media__item epk-campaign-media__item--{kind}"',block,count=1)
    section=re.sub(r'<figure\b.*?</figure>',fig,section,flags=re.I|re.S)
    section=re.sub(r'<article\b', '<article class="epk-campaign-media__item epk-campaign-media__item--post"', section)
    css=profile['css'].replace('%S%',f'#campaign-media-{page_id}').replace('%SECTION%',f'section[aria-labelledby="campaign-media-{page_id}"]')
    styled=f'<style id="epk-media-design-{page_id}">{css}</style>\n{section}'
    without=source[:n['offset']]+source[n['end']:]
    anchor=profile['before_anchor']; pos=without.find(anchor)
    if pos<0: raise ValueError(f"placement anchor not found: {anchor}")
    result=without[:pos]+styled+'\n'+without[pos:]
    if media_bytes(result)!=media_bytes(source): raise ValueError('player/script media bytes changed')
    if result.count('epk-campaign-media--integrated')!=1: raise ValueError('integration marker count failed')
    return result


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('source'); ap.add_argument('profile'); ap.add_argument('output'); ap.add_argument('--record')
    a=ap.parse_args(); src=Path(a.source).read_text(encoding='utf-8'); profile=json.loads(Path(a.profile).read_text(encoding='utf-8'))
    out=transform(src,profile); Path(a.output).write_text(out,encoding='utf-8',newline='')
    rec={"page_id":profile['page_id'],"profile_id":profile['profile_id'],"motif":profile['motif'],"design_evidence":profile['design_evidence'],"source_sha256":hashlib.sha256(src.encode()).hexdigest(),"candidate_sha256":hashlib.sha256(out.encode()).hexdigest(),"player_blocks_preserved":len(media_bytes(src)),"placement":"before "+profile['before_anchor']}
    if a.record: Path(a.record).write_text(json.dumps(rec,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    else: print(json.dumps(rec,ensure_ascii=False))
if __name__=='__main__': main()
