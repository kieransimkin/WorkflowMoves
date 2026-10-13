"""Offline campaign-media coverage by exact item identity; no public writes."""
import argparse, json, re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

def identity(url):
    p=urlsplit(url); host=(p.hostname or '').lower()
    if host in {'youtube.com','www.youtube.com','m.youtube.com','youtube-nocookie.com','www.youtube-nocookie.com','youtu.be'}:
        bits=p.path.strip('/').split('/')
        video=bits[0] if host=='youtu.be' else (bits[1] if len(bits)>1 and bits[0] in {'embed','shorts','live'} else parse_qs(p.query).get('v',[''])[0])
        if re.fullmatch(r'[A-Za-z0-9_-]{11}',video): return 'youtube:'+video
    return url.rstrip('/')

class VisibleMedia(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack=[]; self.links=set();self.embeds=set();self.deferred_embeds=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); inherited=any(item[1] for item in self.stack)
        hidden=inherited or tag in {'script','style','template','noscript','head'} or 'hidden' in a or a.get('aria-hidden')=='true' or bool(re.search(r'display\s*:\s*none|visibility\s*:\s*hidden',a.get('style',''),re.I))
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}: self.stack.append((tag,hidden,tag=='template' and 'data-epk-video-template' in a))
        if hidden:
            if tag=='iframe' and a.get('src') and any(item[2] for item in self.stack):self.deferred_embeds.add(identity(a['src']))
            return
        if tag=='a' and a.get('href'):self.links.add(identity(a['href']))
        if tag=='iframe' and a.get('src'):self.embeds.add(identity(a['src']))
        if tag in {'video','source'} and a.get('src'):self.embeds.add(identity(a['src']))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                del self.stack[i:];break

def audit(ledger,pages):
    if not isinstance(ledger,list) or not isinstance(pages,list):raise ValueError('Ledger and catalogue must be JSON lists')
    page_map={int(x['id']):x for x in pages}
    groups=defaultdict(list)
    for item in ledger:
        if not all(k in item for k in ('epk_id','url','kind','publication_state')):raise ValueError('Missing item fields')
        # Pending items cannot displace a verified public representative.
        state=item['publication_state']
        key=(int(item['epk_id']),item.get('asset_group') or identity(item['url']),state=='verified_public')
        groups[key].append(item)
    out=[]
    for (page_id,group,verified),items in sorted(groups.items(),key=lambda x:str(x[0])):
        chosen=sorted(items,key=lambda x:(not identity(x['url']).startswith('youtube:'),x['url']))[0]
        row={**chosen,'asset_group':group,'publication_urls':list(dict.fromkeys(x['url'] for x in items)),'deduplicated':len(items)-1}
        if not verified:row['coverage']='needs_publication_verification'
        elif page_id not in page_map:row['coverage']='epk_unavailable'
        else:
            content=page_map[page_id].get('content',{}).get('rendered')
            if not isinstance(content,str):raise ValueError('Page lacks rendered content')
            parser=VisibleMedia();parser.feed(content);id_=identity(chosen['url'])
            if chosen.get('kind') in {'video','short'} and id_.startswith('youtube:'):
                if id_ in parser.embeds:row['coverage']='embedded_source_present'
                elif id_ in parser.deferred_embeds:row['coverage']='deferred_embed_source_present'
                elif chosen.get('embed_blocked_reason'):
                    native=chosen.get('wordpress_url')
                    row['coverage']='native_fallback_source_present' if native and chosen.get('source_hash_verified') is True and identity(native) in parser.embeds else 'missing_native_fallback'
                else:row['coverage']='missing_embed'
            else:row['coverage']='linked_or_embedded_source_present' if id_ in parser.links|parser.embeds else 'missing_content'
        out.append(row)
    return {'schema_version':1,'items':out,'limits':['Source presence is not rendered visibility, public persistence, playback, rights or approval evidence.','Cross-platform grouping is supplied evidence; identical titles alone never group items.']}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('ledger',type=Path);p.add_argument('catalogue',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=audit(json.loads(a.ledger.read_text(encoding='utf-8-sig')),json.loads(a.catalogue.read_text(encoding='utf-8-sig')))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'items':len(result['items']),'deduplicated':sum(x['deduplicated'] for x in result['items'])}))
