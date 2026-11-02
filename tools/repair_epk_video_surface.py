"""Guarded, byte-preserving picture-play repair. Local preparation only; no publishing."""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from compose_epk_cover import Attributes, HIT_CSS, runtime_text

PICTURE_CSS='.epk-video-picture{position:relative;width:100%;height:100%;aspect-ratio:inherit;min-width:0;isolation:isolate}.epk-video-picture:not(.is-revealed){cursor:pointer}.epk-video-picture>img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}.epk-video-picture [hidden]{display:none!important}.epk-video-picture.is-revealed>img{visibility:hidden}.epk-video-picture__slot{position:absolute;inset:0;background:#000;z-index:1}.epk-video-picture__slot iframe{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;border:0}.epk-video-picture__play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:2;width:72px;height:72px;min-height:44px;border:2px solid #fff;border-radius:50%;background:rgba(0,0,0,.8);color:#fff;cursor:pointer;display:grid;place-items:center;padding:20px}.epk-video-picture__play svg{display:block;width:100%;height:100%;fill:currentColor}.epk-video-picture__play:focus-visible{outline:3px solid #ffcf49;outline-offset:4px}.epk-video-stable{transform:none!important}@media(forced-colors:active){.epk-video-picture__play{border-color:ButtonText;background:ButtonFace;color:ButtonText}}'


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def native_runtime():
    code=''.join(line.strip() for line in Path(__file__).with_name('epk_native_video_surface.js').read_bytes().decode('utf-8').splitlines())
    if '<' in code or '&' in code:
        raise ValueError('WordPress-unsafe native runtime')
    return code


def repair(source, profile):
    if set(profile)-{'cover','native_sources','provider_starts'}:
        raise ValueError('Unknown profile fields')
    if type(profile.get('cover',False)) is not bool:
        raise ValueError('cover must be boolean')
    edits=[]
    def replace(old,new,label):
        nonlocal source
        if old==new:
            return
        if source.count(old)!=1:
            raise ValueError('Ambiguous edit: '+label)
        source=source.replace(old,new,1)
        edits.append({'label':label,'old':old,'new':new})
    additions=[]
    providers=profile.get('provider_starts',[])
    for player in providers:
        if set(player)!={'id','poster'} or not re.fullmatch(r'[A-Za-z0-9_-]{11}',player['id']):
            raise ValueError('Explicit provider ID and poster required')
        poster=urlparse(player['poster'])
        if poster.scheme!='https' or not poster.netloc:
            raise ValueError('Poster must use HTTPS')
        if re.search(r'data-epk-cover-player=["\']'+re.escape(player['id'])+r'["\']',source):
            continue
        matches=[]
        for match in re.finditer(r'<iframe\b[^>]*>\s*</iframe>',source,re.I):
            url=urlparse(Attributes(match[0]).attrs.get('src',''))
            if url.scheme=='https' and url.hostname in ('www.youtube.com','www.youtube-nocookie.com') and url.path=='/embed/'+player['id']:
                matches.append(match[0])
        if len(matches)!=1:
            raise ValueError('Provider target is not unique: '+player['id'])
        iframe=matches[0]
        title=Attributes(iframe).attrs.get('title','video')
        esc=lambda s:html.escape(s,quote=True)
        wrapper='<div class="epk-video-picture" data-epk-cover-player="'+player['id']+'"><img src="'+esc(player['poster'])+'" alt="" loading="lazy"><button type="button" class="epk-video-picture__play" data-epk-video-play aria-label="Play '+esc(title)+'"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3v18l15-9z"/></svg></button><div class="epk-video-picture__slot" data-epk-video-slot hidden></div><template data-epk-video-template>'+iframe+'</template></div>'
        replace(iframe,wrapper,'provider '+player['id'])
    if profile.get('cover') or providers:
        if 'data-epk-cover-player=' not in source:
            raise ValueError('No explicit cover player')
        script='<script data-epk-cover-runtime>'+runtime_text()+'</script>'
        scripts=re.findall(r'<script\b[^>]*\bdata-epk-cover-runtime(?:="")?[^>]*>[\s\S]*?</script>',source,re.I)
        if len(scripts)>1:
            raise ValueError('Multiple cover runtimes')
        if scripts:
            replace(scripts[0],script,'cover runtime')
        else:
            additions.append(script)
        style='<style id="epk-video-picture-hit-area">'+HIT_CSS+(PICTURE_CSS if providers else '')+'</style>'
        styles=re.findall(r'<style\b[^>]*\bid="epk-video-picture-hit-area"[^>]*>[\s\S]*?</style>',source,re.I)
        if len(styles)>1:
            raise ValueError('Multiple repair styles')
        if styles:
            replace(styles[0],style,'picture hit area')
        else:
            additions.append(style)
    sources=profile.get('native_sources',[])
    if not isinstance(sources,list) or len(sources)!=len(set(sources)):
        raise ValueError('Native source list must be explicit and unique')
    for url in sources:
        if urlparse(url).scheme!='https':
            raise ValueError('Native sources must use HTTPS')
        found=False
        for match in re.finditer(r'<video\b[^>]*>[\s\S]*?</video>',source,re.I):
            attrs=Attributes(match[0].split('>')[0]+'>').attrs
            if 'controls' in attrs and (attrs.get('src')==url or any(Attributes(s).attrs.get('src')==url for s in re.findall(r'<source\b[^>]*>',match[0],re.I))):
                found=True
        if not found:
            raise ValueError('Native source missing from controlled video: '+url)
    if sources:
        config=json.dumps({'sources':sources},ensure_ascii=True,separators=(',',':')).replace('<','\\u003c').replace('&','\\u0026')
        block='<script type="application/json" data-epk-native-surface>'+config+'</script><script data-epk-native-surface-runtime>'+native_runtime()+'</script>'
        current=re.findall(r'<script\b[^>]*data-epk-native-surface(?:="")?\s*>[\s\S]*?</script>\s*<script\b[^>]*data-epk-native-surface-runtime(?:="")?[^>]*>[\s\S]*?</script>',source,re.I)
        if len(current)>1:
            raise ValueError('Multiple native surface runtimes')
        if current:
            replace(current[0],block,'native surface runtime')
        else:
            additions.append(block)
    if additions:
        added=''.join(additions)
        source+=added
        edits.append({'label':'appended resources','old':'','new':added})
    return source,edits


def verify_preservation(before,after,edits):
    restored=after
    for edit in reversed(edits):
        if edit['old']:
            if restored.count(edit['new'])!=1:
                raise ValueError('Cannot reverse '+edit['label'])
            restored=restored.replace(edit['new'],edit['old'],1)
        else:
            if not restored.endswith(edit['new']):
                raise ValueError('Appended resource moved')
            restored=restored[:-len(edit['new'])]
    if restored!=before:
        raise ValueError('Unrelated source changed')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('--profile',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--receipt',type=Path,required=True)
    args=parser.parse_args()
    before=args.source.read_bytes().decode('utf-8')
    profile=json.loads(args.profile.read_bytes().decode('utf-8-sig'))
    after,edits=repair(before,profile)
    verify_preservation(before,after,edits)
    args.output.write_bytes(after.encode('utf-8'))
    receipt={'source_sha256':digest(before),'candidate_sha256':digest(after),'unrelated_bytes_preserved':True,'edits':[{'label':e['label'],'before_sha256':digest(e['old']),'after_sha256':digest(e['new'])} for e in edits]}
    args.receipt.write_bytes((json.dumps(receipt,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(receipt))


if __name__=='__main__':
    main()
