#!/usr/bin/env python3
"""Consolidate function metadata without original code or inferred signatures."""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
ev=ROOT/'docs/windows-evidence/foxit-rea'
entries={}
subject_names={}
manifests=[ev/'analysis-manifest.json',*sorted(ev.glob('analysis-manifest-*.json'))]
for manifest_path in manifests:
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'));subjects=manifest['targets']
    subject_names.update({sha:subject['name'] for sha,subject in subjects.items()})
    for f in manifest['function_dossiers']:
        key=(f['subject_sha256'],f['entry_va'].lower())
        item=entries.setdefault(key,{'module':subjects[key[0]]['name'],'address':key[1],'evidence':[],'state':'REA/Ghidra dossier'})
        item['evidence'].append(f['query'])
headless=[ev/'headless-cross-checks.json',*sorted(ev.glob('headless-cross-checks-*.json'))]
for manifest_path in headless:
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    for f in manifest['entries']:
        key=(manifest['source_sha256'],f['entry_va'].lower())
        if key[0] not in subject_names:
            raise ValueError('Headless subject missing from pinned inventory: '+key[0])
        module=subject_names[key[0]]
        if manifest.get('source_module',module)!=module:
            raise ValueError('Headless module differs from pinned subject: '+key[0])
        item=entries.setdefault(key,{'module':module,'address':key[1],'evidence':[],'state':'Supplementary direct Ghidra'})
        item['evidence'].append(f['result'])
with (ROOT/'engenharia-reversa/funcoes.csv').open('w',newline='',encoding='utf-8') as stream:
    writer=csv.DictWriter(stream,fieldnames=['id','module','address','subsystem','parameters','outputs','dependencies','state','confidence','evidence'],lineterminator='\n');writer.writeheader()
    for (sha,va),item in sorted(entries.items()):
        subsystem={'fxLuceneLib.dll':'index/search','lucene++.dll':'index/search','Bookmark.fpi':'bookmarks/plugin','CommentsSummary.fpi':'annotations/comment summary','agnosticuilib.dll':'UI format/translations'}.get(item['module'],'main commands/helpers')
        writer.writerow({'id':sha[:12]+':'+va,'module':item['module'],'address':va,'subsystem':subsystem,'parameters':'Partially reconstructed; exact types/signatures unverified','outputs':'See technical report; not generally verified','dependencies':'See analysis-manifest.json callees and dispatch-catalog.json','state':item['state'],'confidence':'Code observation; semantic confidence varies by contract','evidence':';'.join(item['evidence'])})
print('Distinct observed entries:',len(entries))
