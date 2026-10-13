"""Attach explicit, verified master/player mappings to an EPK; never infer identity or publish."""
import argparse,json,math,re,html
from pathlib import Path
from urllib.parse import urlparse
def number(value,positive=False):
 if not isinstance(value,(int,float)) or isinstance(value,bool) or not math.isfinite(value) or value<0 or positive and value==0:raise ValueError('Invalid playback time')
 return value
def validate(config):
 if set(config)!={'master','players'}:raise ValueError('Only public master/player configuration is accepted')
 master=config['master'];players=config['players']
 if not isinstance(master,dict) or not isinstance(players,list):raise ValueError('Master and player list are required')
 if set(master)!={'id','duration','urls'} or not isinstance(master['id'],str) or not master['id'] or len(master['id'])>160 or any(c in master['id'] for c in ['\\','\n','\r']):raise ValueError('Invalid public master identity')
 duration=number(master['duration'],True)
 if not isinstance(master['urls'],list) or not all(isinstance(url,str) for url in master['urls']):raise ValueError('Master URLs must be a list of strings')
 for url in master['urls']:
  parsed=urlparse(url)
  if parsed.scheme!='https' or parsed.hostname!='kieransimkin.co.uk' or parsed.username or parsed.password or not parsed.path.startswith('/wp-content/uploads/'):raise ValueError('Master reference must be approved same-site media')
 seen=set()
 for player in players:
  if not isinstance(player,dict) or not isinstance(player.get('id'),str):raise ValueError('Player identity must be a string')
  if set(player)!={'kind','id','offset','duration','playerStart','masterVerified'} or player['masterVerified'] is not True:raise ValueError('Explicit verified player association is required')
  if player['id'] in seen:raise ValueError('Duplicate player asset')
  seen.add(player['id'])
  offset=number(player['offset']);length=number(player['duration'],True);number(player['playerStart'])
  if offset+length>duration+.001:raise ValueError('Clip exceeds master')
  if player['kind']=='youtube':
   if not re.fullmatch(r'[A-Za-z0-9_-]{11}',player['id']):raise ValueError('Invalid YouTube asset')
  elif player['kind']=='native':
   parsed=urlparse(player['id'])
   if parsed.scheme!='https' or parsed.hostname!='kieransimkin.co.uk' or parsed.username or parsed.password or not parsed.path.startswith('/wp-content/uploads/'):raise ValueError('Native player must use approved same-site media')
  else:raise ValueError('Unsupported player kind')
 return config
def compose(source,config):
 if 'data-epk-player-bindings' in source:raise ValueError('Already composed; merge from fresh source')
 validate(config)
 payload=json.dumps(config,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('&','\\u0026')
 runtime=' '.join(Path(__file__).with_name('bind_epk_players.js').read_text(encoding='utf-8').splitlines())
 return source+'<script type="application/json" data-epk-player-bindings>'+payload+'</script><script data-epk-playback-runtime>'+runtime+'</script>'
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('bindings',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.write_text(compose(a.source.read_text(encoding='utf-8'),json.loads(a.bindings.read_text(encoding='utf-8'))),encoding='utf-8')
