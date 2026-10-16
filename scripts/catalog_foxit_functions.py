#!/usr/bin/env python3
"""Consolidate function metadata without original code or inferred signatures."""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
ev=ROOT/'docs/windows-evidence/foxit-rea'
manifest=json.loads((ev/'analysis-manifest.json').read_text());subjects=manifest['targets'];entries={}
for f in manifest['function_dossiers']:
    key=(f['subject_sha256'],f['entry_va'].lower())
    item=entries.setdefault(key,{'module':subjects[key[0]]['name'],'address':key[1],'evidence':[],'state':'REA/Ghidra dossier'})
    item['evidence'].append(f['query'])
for f in json.loads((ev/'headless-cross-checks.json').read_text())['entries']:
    key=('90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6',f['entry_va'].lower())
    item=entries.setdefault(key,{'module':'FoxitPDFReader.exe','address':key[1],'evidence':[],'state':'Supplementary direct Ghidra'})
    item['evidence'].append(f['result'])
with (ROOT/'engenharia-reversa/funcoes.csv').open('w',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=['id','module','address','subsystem','parameters','outputs','dependencies','state','confidence','evidence'],lineterminator='\n');writer.writeheader()
    for (sha,va),item in sorted(entries.items()):
        subsystem={'fxLuceneLib.dll':'index/search','Bookmark.fpi':'bookmarks/plugin','agnosticuilib.dll':'UI format/translations'}.get(item['module'],'main commands/helpers')
        writer.writerow({'id':sha[:12]+':'+va,'module':item['module'],'address':va,'subsystem':subsystem,'parameters':'Partially reconstructed; exact types/signatures unverified','outputs':'See technical report; not generally verified','dependencies':'See analysis-manifest.json callees and dispatch-catalog.json','state':item['state'],'confidence':'Code observation; semantic confidence varies by contract','evidence':';'.join(item['evidence'])})
print('Distinct observed entries:',len(entries))
