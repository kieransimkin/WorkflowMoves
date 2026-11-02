"""Fresh-source artwork-first EPK player composition; never publishes pages."""
import re,html,hashlib,json,argparse
from pathlib import Path
from html.parser import HTMLParser
CSS='.epk-video-stable{transform:none!important}.layout-cinema .epk-cover-wrap:has([data-epk-cover-player]){height:auto!important;min-height:0!important;max-height:none!important}.layout-cinema .epk-hero:has([data-epk-cover-player]) .epk-heading{position:relative;left:auto;right:auto;bottom:auto;padding:2rem 6vw}.epk-cover-player{z-index:2;pointer-events:none;position:relative;width:100%;aspect-ratio:1/1;min-width:0;isolation:isolate}.epk-cover-player>img{display:block!important;width:100%!important;height:100%!important;object-fit:contain;margin:0!important}.epk-cover-player button,.epk-cover-player__slot{pointer-events:auto}.epk-cover-player [hidden]{display:none!important}.epk-cover-player.is-revealed>img{visibility:hidden}.epk-cover-player__slot{position:absolute;inset:0;z-index:5;background:#000}.epk-cover-player__slot iframe{position:absolute!important;inset:0!important;display:block;width:100%!important;height:100%!important;border:0}.epk-cover-player__play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:6;width:72px;height:72px;min-height:44px;border:2px solid #fff;border-radius:50%;background:rgba(0,0,0,.8);color:#fff;cursor:pointer;font:28px/1 sans-serif}.epk-cover-player__close{position:absolute;right:8px;top:8px;z-index:6;min-width:44px;min-height:44px;border:1px solid #fff;background:#111;color:#fff;cursor:pointer}.epk-cover-player button:focus-visible{outline:3px solid #ffcf49;outline-offset:4px}.epk-cover-player__watch{display:inline-block;margin-top:.4rem;font-size:.85em}@media(forced-colors:active){.epk-cover-player button{border:2px solid ButtonText;background:ButtonFace;color:ButtonText}}'
# Keep the existing cinematic hero height and title overlay.
CSS=re.sub(r'\.layout-cinema \.epk-cover-wrap:has\(\[data-epk-cover-player\]\)\{[^}]+\}', '',CSS)
CSS=re.sub(r'\.layout-cinema \.epk-hero:has\(\[data-epk-cover-player\]\) \.epk-heading\{[^}]+\}', '',CSS)
CSS+='.layout-cinema .epk-cover-player{width:auto;height:100%;max-height:100vw;aspect-ratio:1/1;margin-inline:auto;z-index:auto;isolation:auto}.layout-cinema .epk-cover-wrap:has([data-epk-cover-player])>.epk-cover-player__watch{position:absolute;right:8px;bottom:8px;z-index:4}.layout-cinema .epk-hero:has(.epk-cover-player.is-revealed) .epk-heading{visibility:hidden}.layout-cinema .epk-hero:has([data-epk-cover-player]) .epk-heading{pointer-events:none}.layout-cinema .epk-hero:has([data-epk-cover-player]) .epk-heading a{pointer-events:auto}'

def extend_direct_cover_selectors(source):
 """Retain direct cover styles in their existing media-rule context."""
 def style(match):
  def selectors(header):
   original=header[0];extra=[];existing={s.strip() for s in original.split(',')}
   for selector in original.split(','):
    adapted=re.sub(r'(\.epk-cover-wrap\s*>\s*)(\.epk-cover(?![\w-]))',r'\1.epk-cover-player>\2',selector)
    if adapted!=selector and adapted.strip() not in existing:extra.append(adapted.strip())
   return original+(','+','.join(extra) if extra else '')
  return match[1]+re.sub(r'[^{}]+(?=\{)',selectors,match[2])+match[3]
 return re.sub(r'(<style\b[^>]*>)([\s\S]*?)(</style>)',style,source)

def repair_cover_styles(source):
 """Upgrade an already composed cover without changing players or timing."""
 if 'data-epk-cover-player' not in source:raise ValueError('No composed cover')
 source=extend_direct_cover_selectors(source)
 pattern=r'(<style id="epk-cover-player-style">)[\s\S]*?(</style>)'
 if len(re.findall(pattern,source))!=1:raise ValueError('One cover stylesheet is required')
 return re.sub(pattern,lambda m:m[1]+CSS+m[2],source)

class Attributes(HTMLParser):
 def __init__(self,s):super().__init__();self.attrs={};self.feed(s)
 def handle_starttag(self,t,a):self.attrs=dict(a)
def compose(source,cover_url,cover_alt):
 if 'data-epk-cover-player' in source:raise ValueError('Already composed; re-read current source')
 widget=re.search(r'<div class="epk-campaign-featured"[^>]*data-campaign-main-video="true">[\s\S]*?</figure></div>',source)
 if not widget:raise ValueError('No added hero player')
 frame=re.search(r'<iframe\b[^>]*></iframe>',widget.group()).group();attrs=Attributes(frame).attrs;url=attrs['src'];title=attrs['title']
 if not re.fullmatch(r'https://www\.youtube(?:-nocookie)?\.com/embed/[A-Za-z0-9_-]{11}',url):raise ValueError('Unsupported video URL')
 iframe=frame.replace('loading="eager"','loading="lazy"');body=extend_direct_cover_selectors(source[:widget.start()]+source[widget.end():])
 image=None
 for hit in re.finditer(r'<img\b[^>]*>',body):
  if Attributes(hit.group()).attrs.get('src')==cover_url:image=hit;break
 original=image.group() if image else '<img src="'+html.escape(cover_url,quote=True)+'" alt="'+html.escape(cover_alt,quote=True)+'" width="1254" height="1254">'
 esc=lambda x:html.escape(x,quote=True)
 box='<div class="epk-cover-player" data-epk-cover-player="'+url.rsplit('/',1)[1]+'">'+original+'<button type="button" class="epk-cover-player__play" data-epk-video-play aria-label="Play '+esc(title)+'">&#9654;</button><div class="epk-cover-player__slot" data-epk-video-slot hidden></div><button type="button" class="epk-cover-player__close" data-epk-video-close hidden aria-label="Return to cover artwork">&#215;</button><template data-epk-video-template>'+iframe+'</template></div>'
 if image:body=body[:image.start()]+box+body[image.end():]
 else:body=body[:widget.start()]+box+body[widget.start():]
 js=Path(__file__).with_name('epk_cover_player.js').read_text(encoding='utf-8').strip()
 return body+'<style id="epk-cover-player-style">'+CSS+'</style><script data-epk-cover-runtime>'+js+'</script>'
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('--cover-url',required=True);p.add_argument('--cover-alt',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();s=compose(a.source.read_text(encoding='utf-8'),a.cover_url,a.cover_alt);a.output.write_text(s,encoding='utf-8');print(hashlib.sha256(s.encode()).hexdigest())
