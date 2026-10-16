"""Summarize saved Foxit REA evidence; raw binaries and pseudocode remain local."""
import hashlib,json
from pathlib import Path
import argparse
parser=argparse.ArgumentParser(description="Summarize saved REA queries without redistributing pseudocode.")
parser.add_argument('--session-root',type=Path,required=True)
parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args()
root=args.session_root.resolve()
out=args.output_dir.resolve()
out.mkdir(parents=True,exist_ok=True)
queries=[];procedures=[];targets={}
directories=[root,root/'lucene',root/'bookmarks',root/'bookmarks-seeded',root/'main-focused',root/'main-seeded',root/'aui',root/'main-direct',root/'main-commands']
# Real directed sessions carry both a seed list and an analysis profile. Do not
# mix the driver's intentionally failing smoke fixtures into target coverage.
directories+=sorted(path for path in root.iterdir() if path not in directories
                    and (path/'seeds.tsv').is_file() and (path/'profile.json').is_file()
                    and (path/'queue').is_dir())
for directory in directories:
 retained={}
 bundle=directory/'evidence-bundle'
 if bundle.is_file():
  for evidence in json.loads(bundle.read_text()).get('records',[]):
   retained[evidence['evidence_id']]=evidence
 for request_path in sorted((directory/'queue').glob('*.json')):
  req=json.loads(request_path.read_text());path=directory/'results'/request_path.name
  record={'request':str(request_path.relative_to(root)),'operation':req['name'],'arguments':req['arguments'],'status':'pending'}
  if directory==root and not path.exists() and (root/'results/003-segments.json').exists():record['status']='not_executed_after_timeout'
  if path.exists():
   raw=path.read_bytes();x=json.loads(raw);record.update({'result':str(path.relative_to(root)),'result_sha256':hashlib.sha256(raw).hexdigest(),'elapsed_sec':x.get('elapsed_sec')})
   response=x.get('response',{});result=response.get('result',{});ev=None
   if x.get('error') or response.get('error') or result.get('isError'):
    record['status']='error';record['error']=x.get('error') or response.get('error') or result.get('content')
    # A transport error can leave a complete, exported Evidence record. Preserve
    # the failed RPC and describe recovery separately, without rewriting history.
    for content in result.get('content',[]):
     if content.get('type')!='text':continue
     try:error=json.loads(content['text']).get('error',{})
     except (ValueError,TypeError):continue
     limits=error.get('details',{}).get('reported_limits',{})
     ident=limits.get('evidence_id')
     if error.get('code')=='resource_constraint' and ident in retained:
      ev=retained[ident]
      record['recovered_from_export']={'path':str(bundle.relative_to(root)),'evidence_id':ident,
                                     'bundle_sha256':hashlib.sha256(bundle.read_bytes()).hexdigest()}
   else:
    record['status']='completed';ev=result.get('structuredContent',{});record['evidence_id']=ev.get('evidence_id')
   if isinstance(ev,dict):
    if ev.get('subject'):
     identity=ev['subject'];sha=identity.get('digest',{}).get('sha256');record['subject_sha256']=sha
     if sha:targets.setdefault(sha,{'name':identity['name'],'sessions':[],'overview':None});session=str(directory.relative_to(root))
     if sha and session not in targets[sha]['sessions']:targets[sha]['sessions'].append(session)
     if req['name']=='binary_overview' and sha:targets[sha]['overview']=ev['normalized_result']
    if req['name']=='analyze_function' and isinstance(ev.get('raw_result'),dict) and ev['raw_result'].get('value'):
     v=ev['raw_result']['value'];proc=v['procedure'];code=v.get('pseudocode','')
     procedures.append({'subject_sha256':record.get('subject_sha256'),'session':str(directory.relative_to(root)),'query':record['request'],'evidence_id':ev['evidence_id'],'analysis_profile_digest':ev['analysis_profile']['digest'],'entry_va':proc['address'],'provider_name_hint':proc['name'],'body':proc.get('body'),'pseudocode_sha256':hashlib.sha256(code.encode()).hexdigest(),'pseudocode_bytes':len(code.encode()),'callees':[{'address':c['address'],'provider_name_hint':c['name'],'classification':c.get('classification')} for c in v.get('callees',[])],'limitations':ev.get('limitations',[]),'recovered_from_export':record.get('recovered_from_export')})
     if not record.get('recovered_from_export'):procedures[-1].pop('recovered_from_export')
  if (directory/'cancelled.json').exists() and record['status']=='pending':record['status']='not_executed_cancelled_profile'
  if (directory/'session-ended.json').exists() and record['status']=='pending':record['status']='not_completed_session_closed'
  queries.append(record)
for sha,target in targets.items():target['distinct_decompiled_entries']=len({p['entry_va'] for p in procedures if p['subject_sha256']==sha})
manifest={'format':'print-view-foxit-rea-coverage-v1','date_utc':'2026-10-16','scope':'Foxit only; static REA/Ghidra analysis, with independent PE inventory. No product equivalence or dynamic Foxit execution is asserted.','local_evidence_root':str(root),'targets':targets,'queries':queries,'function_dossiers':procedures,'overall_status':'partial_static_investigation','linux_feature_equivalence_verified':False,'flatpak_built_this_round':False,'application_source_modified':False,'limitations':['Provider names can include Ghidra FID guesses and analyst seed labels; only import/export/RTTI evidence can establish original symbol origin.','Decompiled pseudocode is a provider reconstruction; exact variable types and signatures need confirmation.','A successfully decompiled entry is not a fully recovered feature contract or tested Linux equivalent.','Full evidence, decompilations, and source binaries are retained outside the application checkout.']}
(out/'analysis-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Queries:',{s:sum(q['status']==s for q in queries) for s in ('completed','error','pending')},'unique functions:',{t['name']:t['distinct_decompiled_entries'] for t in targets.values()})
