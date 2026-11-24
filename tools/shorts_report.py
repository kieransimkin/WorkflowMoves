"""Private, source-bound short-video observation ledger and local report editions.

No network, social publication, scheduling, inference of missing metrics or lease recovery.
"""
from __future__ import annotations
import argparse, contextlib, datetime as dt, hashlib, html, json, math, os, re, statistics, sys, uuid
from pathlib import Path

SCHEMA='shorts.observations.v1'
COUNTS={'views','engaged_views','likes','comments','shares','saves','follows','impressions','unique_views','link_clicks','reach','viewers'}
RATES={'completion_percent','stayed_to_watch_percent','retained_1s_percent','retained_2s_percent'}
METRICS=COUNTS|RATES|{'average_watch_s','average_percentage_viewed'}
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def encoded(d):return (json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')
def save(p,d):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_bytes(encoded(d))
def instant(v):
    q=dt.datetime.fromisoformat(v.replace('Z','+00:00'))
    if q.tzinfo is None:raise ValueError('An offset-bearing observation timestamp is required')
    return q
def contained(root,rel):
    p=(Path(root)/rel).resolve()
    if not p.is_relative_to(Path(root).resolve()):raise ValueError('Path escapes report root')
    return p
@contextlib.contextmanager
def lock(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True);p=root/'report-writer.lock';token=str(uuid.uuid4())
    try:
        with p.open('x',encoding='utf-8') as f:json.dump({'token':token,'pid':os.getpid(),'at':stamp()},f)
    except FileExistsError:raise ValueError('Report writer is owned; leave contribution pending. Do not recover another owner.')
    try:yield
    finally:
        if p.exists() and read(p).get('token')==token:p.unlink()
def validate(config,obs):
    if obs.get('schema')!=SCHEMA or obs.get('artist')!=config['artist']:raise ValueError('Schema or artist mismatch')
    platform=obs.get('platform');accounts=config['accounts'].get(platform,[])
    if obs.get('account') not in accounts:raise ValueError('Unverified platform/account identity')
    instant(obs['observed_at'])
    if not re.fullmatch(r'[A-Za-z0-9_.-]{1,150}',obs.get('run_id','')):raise ValueError('Stable safe run_id required')
    if obs.get('status') not in {'measured','unavailable','no_change'}:raise ValueError('Explicit observation status required')
    src=obs['source'];p=Path(src['path']).resolve();allowed=Path(config['evidence_root']).resolve()
    if not p.is_relative_to(allowed) or not p.is_file():raise ValueError('Evidence must be a saved file within the configured evidence root')
    if digest(p)!=src.get('sha256'):raise ValueError('Evidence hash differs')
    posts=obs.get('posts',[])
    if obs['status']!='measured' and posts:raise ValueError('Unavailable/no-change observations cannot inject measurements')
    if obs['status']=='measured' and not posts:raise ValueError('Measured observation requires posts')
    if not isinstance(obs.get('coverage'),dict) or not obs['coverage'].get('scope'):raise ValueError('Coverage scope is required')
    seen=set()
    for row in posts:
        identity=str(row['id'])
        if not identity or identity in seen:raise ValueError('Missing or duplicate native/qualified row identity')
        seen.add(identity)
        if row.get('publication_state')!='published':raise ValueError('Only verified published posts enter this ledger')
        if row.get('format_status') not in {'confirmed_9_16','candidate','unresolved','excluded'}:raise ValueError('Explicit format qualification required')
        if row['format_status']=='confirmed_9_16':
            g=row.get('geometry',{})
            if not g.get('width') or not g.get('height') or abs(g['width']/g['height']-9/16)>.005 or not g.get('source'):raise ValueError('9:16 needs source-labelled dimensions')
        if not isinstance(row.get('metrics'),dict) or not row['metrics']:raise ValueError('Post metrics required')
        for key,m in row['metrics'].items():
            if key not in METRICS:raise ValueError('Unsupported metric: '+key)
            value=m.get('value')
            if value is not None:
                if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<0:raise ValueError('Invalid metric value')
                if key in COUNTS and int(value)!=value:raise ValueError('Count must be integer')
                if key in RATES and value>100:raise ValueError('Rate exceeds100%; APV is a separate field')
            if not m.get('definition') or not m.get('unit'):raise ValueError('Metric definition/unit required')
            expected='count' if key in COUNTS else 'percent' if key in RATES or key=='average_percentage_viewed' else 'seconds'
            if m['unit']!=expected:raise ValueError('Metric unit differs from field definition')
            w=m.get('window',{})
            if w.get('kind') not in {'lifetime','period','since_published'}:raise ValueError('Explicit metric window required')
            if w['kind']=='period' and (not w.get('start') or not w.get('end')):raise ValueError('Period requires exact start/end')
            if w['kind'] in {'lifetime','since_published'} and not w.get('cutoff'):raise ValueError('Lifetime/since-published requires source cutoff')
    return obs
def series_key(m):
    w=m['window'];kind=w['kind']
    return (m['definition'],m['unit'],kind,w.get('start') if kind=='period' else None,w.get('end') if kind=='period' else None)
def order(m):
    value=m['window'].get('cutoff',m['window'].get('end',m['observed_at']))
    if len(value)==10:value+='T00:00:00+00:00'
    return (instant(value),instant(m['observed_at']))
def ingest(config,obs):
    validate(config,obs);root=Path(config['report_root']);data=encoded(obs);key=hashlib.sha256(data).hexdigest()
    with lock(root):
        folder=contained(root,'observations/'+re.sub(r'[^a-z0-9]+','-',obs['platform'].lower()))
        folder.mkdir(parents=True,exist_ok=True)
        same=list(folder.glob(obs['run_id']+'--*.json'))
        if same:
            if len(same)==1 and same[0].read_bytes()==data:return {'state':'already_saved','path':str(same[0]),'sha256':key}
            raise ValueError('run_id already has different content; reconcile rather than overwrite')
        target=folder/(obs['run_id']+'--'+key[:16]+'.json');target.write_bytes(data)
        if target.read_bytes()!=data:raise ValueError('Snapshot readback differs')
    return {'state':'saved','path':str(target),'sha256':key}
def baseline_rows(config):
    d=read(config['baseline_dataset']);out=[]
    mappings={'YouTube':{'average_percentage_viewed':'average_percentage_viewed'},'TikTok':{'completion_percent':'completion_percent','new_followers':'follows'},'Instagram':{'interactions':None},'X':{'Views':'views','Impressions':'impressions','Unique views':'unique_views','Link clicks':'link_clicks'},'LinkedIn':{'followers':'follows'},'Facebook':{}}
    for platform,rows in d.items():
        for r in rows:
            state=r.get('format_status','candidate');state='excluded' if state=='full film excluded' else 'unresolved' if 'unresolved' in state else 'candidate'
            if r.get('geometry')=='native 720x1280':state='confirmed_9_16'
            row={'platform':platform,'id':str(r['id']),'title':r.get('title',r.get('caption','')),'url':r.get('url'),'format_status':state,'publication_state':'published','published_at':r.get('published_at'),'baseline_date':r.get('date_label',r.get('date')),'metrics':{},'baseline':True}
            for key,value in r.items():
                name=mappings.get(platform,{}).get(key,key)
                if name not in METRICS or value is None:continue
                when=r.get('observed_at',r.get('analytics_observed_at','2026-11-24T00:00:00+00:00'))
                if platform=='YouTube' and key in {'average_watch_s','average_percentage_viewed','engaged_views','stayed_to_watch_percent'}:when=r.get('quality_observed_at',r.get('detail_observed_at',when))
                if platform=='TikTok' and key in {'average_watch_s','completion_percent','new_followers'}:when=r.get('analytics_observed_at',when)
                definition=platform.lower()+'.'+name
                cutoff=when
                if platform=='YouTube' and r.get('quality_observed_at') and not r.get('detail_observed_at') and key in {'average_watch_s','average_percentage_viewed','engaged_views','stayed_to_watch_percent'}:cutoff=config.get('youtube_processed_cutoff',when)
                row['metrics'][name]={'value':value,'definition':definition,'unit':'count' if name in COUNTS else 'percent' if name in RATES or name=='average_percentage_viewed' else 'seconds','window':{'kind':'lifetime','cutoff':cutoff},'observed_at':when,'source':{'path':config['baseline_dataset'],'sha256':digest(config['baseline_dataset'])},'baseline':True}
            out.append(row)
    return out
def assemble(config):
    by={(r['platform'],r['id']):r for r in baseline_rows(config)};events=[];series={}
    for key,row in by.items():
        for metric,m in row['metrics'].items():series[(key,metric,series_key(m))]=m
    files=sorted((Path(config['report_root'])/'observations').glob('*/*.json'))
    for path in files:
        obs=read(path);validate(config,obs);events.append({k:obs.get(k) for k in ['platform','account','run_id','observed_at','status','coverage','source']})
        for post in obs.get('posts',[]):
            key=(obs['platform'],str(post['id']))
            row=by.setdefault(key,{'platform':key[0],'id':key[1],'metrics':{},'baseline':False})
            meta_at=row.get('metadata_observed_at','0001-01-01T00:00:00+00:00')
            if instant(obs['observed_at'])>=instant(meta_at):
                for field in ['title','url','format_status','publication_state','published_at','geometry','native_duration_s','limitations']:
                    if field in post:row[field]=post[field]
                row['metadata_observed_at']=obs['observed_at']
            for metric,raw in post['metrics'].items():
                m={**raw,'observed_at':obs['observed_at'],'source':obs['source'],'run_id':obs['run_id'],'baseline':False};sk=(key,metric,series_key(m));old=series.get(sk)
                if old is None or order(m)>order(old):series[sk]=m
                elif old is not None and order(m)==order(old) and old.get('value')!=m.get('value'):raise ValueError('Conflicting values at identical source/observation timestamps')
    for key,row in by.items():
        row['series']={};row['metrics']={}
        for (pk,name,_),m in series.items():
            if pk!=key:continue
            row['series'].setdefault(name,[]).append(m)
        for name,values in row['series'].items():
            # Preserve multiple windows/definitions; use only the baseline-compatible lifetime series in summary cells.
            compatible=[m for m in values if m['window']['kind'] in {'lifetime','since_published'} and m['definition']==row['platform'].lower()+'.'+name]
            if compatible:row['metrics'][name]=max(compatible,key=order)
    return list(by.values()),sorted(events,key=lambda r:instant(r['observed_at']))
def fmt(v):return 'Unavailable' if v is None else f'{v:,.2f}'.rstrip('0').rstrip('.')
def esc(s):return html.escape(str(s or ''))
def publish(config):
    root=Path(config['report_root']);baseline=Path(config['baseline_report']);built=stamp()
    with lock(root):
        inputs={'config':config,'baseline_sha256':digest(config['baseline_dataset']),'baseline_report_sha256':digest(config['baseline_report']),'tests_sha256':digest(config['tests_file']) if config.get('tests_file') else None,'snapshot_hashes':[digest(p) for p in sorted((root/'observations').glob('*/*.json'))],'publisher_sha256':digest(__file__)}
        fingerprint=hashlib.sha256(encoded(inputs)).hexdigest();old_manifest=root/'latest/manifest.json'
        if old_manifest.exists():
            old=read(old_manifest)
            if old.get('input_fingerprint')==fingerprint and all((root/'latest'/n).is_file() and digest(root/'latest'/n)==h for n,h in old['files'].items()):return {'state':'already_current','path':str(root/'latest'),'edition':old['generation']}
        rows,events=assemble(config);tests=read(config['tests_file']) if config.get('tests_file') else []
        generation=contained(root,'editions/'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+uuid.uuid4().hex[:8]);generation.mkdir(parents=True)
        summaries=[]
        for platform in config['accounts']:
            r=[q for q in rows if q['platform']==platform and q.get('format_status')!='excluded'];views=[q['metrics']['views']['value'] for q in r if q.get('metrics',{}).get('views',{}).get('value') is not None]
            ev=[e for e in events if e['platform']==platform]
            summaries.append({'platform':platform,'posts':len(r),'confirmed_9_16':sum(q.get('format_status')=='confirmed_9_16' for q in r),'median_views':statistics.median(views) if views else None,'freshest_contribution':ev[-1]['observed_at'] if ev else None,'latest_status':ev[-1]['status'] if ev else 'baseline only','measured_runs':sum(e['status']=='measured' for e in ev)})
        report={'schema':'shorts.report.v1','artist':config['artist'],'built_at':built,'baseline_sha256':digest(config['baseline_dataset']),'baseline_report':str(baseline),'platforms':summaries,'observations':events,'posts':rows,'tests':tests,'privacy':'Private local report; publication here means local files only.','limits':['Baseline narrative remains dated and is not silently reinterpreted as current.','Only native-definition full-life metrics enter headline cells. Every scope/window is retained as a separate series; no automatic cross-window lift is calculated.','Native counts are not cross-platform comparable or unique-person totals.','No creative test is completed by configuring this report.','Missing and access-held values are not zero.']}
        save(generation/'report-data.json',report)
        lines=['# Shorts performance report — current edition',f"\nArtist: {config['artist']} · Built: {built}\n",'Private local report. The original retrospective is preserved as the historical baseline. New native observations and test evidence appear here; no causal winner is invented from unmatched ages or tiny samples.','\n## Platform evidence freshness\n','| Platform | Published candidates | Confirmed 9:16 | Median native views | New measured runs | Latest contribution |','|---|---:|---:|---:|---:|---|']
        for r in summaries:lines.append(f"| {r['platform']} | {r['posts']} | {r['confirmed_9_16']} | {fmt(r['median_views'])} | {r['measured_runs']} | {r['freshest_contribution'] or 'No new contribution; historical baseline'} — {r['latest_status']} |")
        lines+=['\nMedian cells can contain observations of different ages and source cutoffs. They are descriptive, not matched-age creative comparisons. Counted candidates include unresolved geometry explicitly; excluded full films remain in the data.','\n## Recent analysis updates\n']
        if not events:lines.append('No post-baseline observations have been submitted. The report infrastructure is verified; no new audience result is claimed.')
        for e in events[-18:]:lines.append(f"- {e['observed_at']} · {e['platform']} · {e['status']} · {e['run_id']} · {e['coverage']['scope']} · source `{e['source']['path']}` SHA-256 `{e['source']['sha256']}`")
        lines+=['\n## Opening tests and decisions\n','| Test | Release | Changed variable | State | Owner / next review |','|---|---|---|---|---|']
        for t in tests:lines.append('| '+' | '.join(str(t.get(k,'Unavailable')).replace('|','/').replace('\n',' ') for k in ['id','release','variable','state','owner_review'])+' |')
        lines+=['\n## Historical retrospective\n',f"[Read the original 24 November retrospective]({baseline.as_uri()})",'\nThe appended PDF baseline retains its original dates, denominators, uncertainties and proposed tests. Later observations do not retroactively establish a controlled experiment. The full current per-post metric series and exact sources are in report-data.json.']
        text='\n'.join(lines)+'\n';(generation/'REPORT.md').write_text(text,encoding='utf-8')
        body='<h1>Shorts performance report — current edition</h1><p>'+esc(config['artist'])+' · '+esc(built)+'</p><p>Private local report. Baseline and subsequent observations remain distinct. No web/social publication occurs.</p><pre style="white-space:pre-wrap">'+esc(text)+'</pre>'
        body+='<p><a href="'+baseline.as_uri()+'">Historical retrospective</a> · <a href="report-data.json">Full metric/source series</a></p><label>Filter posts <input id="filter" type="search"></label><span id="count"></span>'
        for platform in config['accounts']:
            body+='<h2>'+esc(platform)+'</h2><div class="wrap"><table><thead><tr><th>Post / format</th><th>Views</th><th>Average watch</th><th>Full watch</th><th>Follows</th><th>Metric observation dates / other series</th></tr></thead><tbody>'
            for row in sorted((r for r in rows if r['platform']==platform),key=lambda r:r['id']):
                m=row['metrics'];cells=[]
                for name in ['views','average_watch_s','completion_percent','follows']:cells.append(fmt(m.get(name,{}).get('value')))
                title=esc(row.get('title') or row['id']);title=('<a href="'+esc(row['url'])+'">'+title+'</a>') if row.get('url') else title
                dates='; '.join(name+': '+m[name]['observed_at']+' / '+m[name]['window']['kind']+' cutoff '+str(m[name]['window'].get('cutoff')) for name in m)
                body+='<tr><td>'+title+'<br>'+esc(row['id'])+' · '+esc(row.get('format_status'))+'</td>'+''.join('<td>'+esc(c)+'</td>' for c in cells)+'<td>'+esc(dates)+'<br>'+esc(sum(len(v) for v in row['series'].values()))+' retained series</td></tr>'
            body+='</tbody></table></div>'
        body+='<script>const f=document.querySelector("#filter");f.addEventListener("input",()=>{let n=0;document.querySelectorAll("tbody tr").forEach(r=>{r.hidden=!r.textContent.toLowerCase().includes(f.value.toLowerCase());if(!r.hidden)n++});document.querySelector("#count").textContent=n+" rows shown"});</script>'
        (generation/'REPORT.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shorts performance report</title><style>body{max-width:1160px;margin:auto;padding:24px;font:16px/1.55 system-ui;color:#19354b}table{border-collapse:collapse;width:100%;font-size:12px}td,th{border:1px solid #cad8e3;padding:8px;text-align:left;vertical-align:top;overflow-wrap:anywhere}td:first-child{min-width:240px}th{background:#e5eef4}.wrap{overflow:auto}pre{font:inherit;background:#f2f6f8;padding:18px}input{padding:10px;margin:15px}</style>'+body+'</html>',encoding='utf-8')
        if config.get('baseline_pdf'):
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
            from pypdf import PdfReader,PdfWriter
            front=generation/'update-pages.pdf';styles=getSampleStyleSheet();flow=[]
            for line in text.splitlines():
                if not line.strip():continue
                flow.extend([Paragraph(esc(line).replace('→','-&gt;'),styles['Heading1'] if line.startswith('# ') else styles['Heading2'] if line.startswith('## ') else styles['BodyText']),Spacer(1,5)])
            SimpleDocTemplate(str(front),title='Shorts performance report — current updates',author=config['artist']).build(flow)
            writer=PdfWriter()
            for path in [front,Path(config['baseline_pdf'])]:writer.append(str(path))
            writer.write(str(generation/'REPORT.pdf'));PdfReader(str(generation/'REPORT.pdf'))
        names=['REPORT.md','REPORT.html','report-data.json']+(['REPORT.pdf'] if config.get('baseline_pdf') else [])
        manifest={'built_at':built,'generation':str(generation),'input_fingerprint':fingerprint,'files':{n:digest(generation/n) for n in names}}
        save(generation/'manifest.json',manifest)
        # Publish the stable view only after every edition file is generated and readable.
        latest=contained(root,'latest');latest.mkdir(exist_ok=True)
        for name in names:
            temp=latest/(name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes((generation/name).read_bytes());os.replace(temp,latest/name)
        pending=latest/('manifest.'+uuid.uuid4().hex+'.tmp');pending.write_bytes(encoded(manifest));os.replace(pending,latest/'manifest.json')
        return {'state':'published_local','path':str(latest),'edition':str(generation),'files':manifest['files'],'observations':len(events),'tests':len(tests)}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--config',required=True);ap.add_argument('action',choices=['validate','ingest','publish']);ap.add_argument('--snapshot');args=ap.parse_args();config=read(args.config)
    if args.action in {'validate','ingest'}:
        if not args.snapshot:ap.error('--snapshot required')
        obs=read(args.snapshot);result=ingest(config,obs) if args.action=='ingest' else {'state':'valid','posts':len(validate(config,obs)['posts'])}
    else:result=publish(config)
    print(json.dumps(result,ensure_ascii=True,indent=2))
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError) as exc:print(json.dumps({'state':'held','error':str(exc)}));sys.exit(2)
