#!/usr/bin/env python3
"""Check the full dossier, its Git source hashes and the standalone HTML text."""
import hashlib
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
NAME='RELATORIO-COMPLETO-LINUXIT-PDF-2026-10-19'


def sha(content):return hashlib.sha256(content).hexdigest()


class ReportHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.ids=[];self.detail_starts=0;self.detail_ends=0;self.pre=None;self.blocks=[];self.external_resources=[];self.scripts=0;self.text=[]
    def handle_starttag(self,tag,attrs):
        attributes=dict(attrs)
        if 'id' in attributes:self.ids.append(attributes['id'])
        if tag=='details':self.detail_starts+=1
        if tag=='pre':
            assert self.pre is None,'Nested preformatted blocks';self.pre=[]
        if tag=='script':
            self.scripts+=1
            if attributes.get('src'):self.external_resources.append(attributes['src'])
        if tag in ('img','iframe','link') and (attributes.get('src') or attributes.get('href')):self.external_resources.append(attributes.get('src') or attributes.get('href'))
    def handle_endtag(self,tag):
        if tag=='details':self.detail_ends+=1
        if tag=='pre':
            assert self.pre is not None;self.blocks.append(''.join(self.pre));self.pre=None
    def handle_data(self,data):
        self.text.append(data)
        if self.pre is not None:self.pre.append(data)


def canonical(value):return value.replace('\r\n','\n').rstrip('\n')


def main():
    metadata_path=ROOT/'testes/resultados/relatorio-completo-2026-10-19/review.json'
    metadata=json.loads(metadata_path.read_text(encoding='utf-8'))
    report=(ROOT/metadata['report']).read_bytes();assert sha(report)==metadata['report_sha256'] and len(report)==metadata['report_bytes']
    markdown=report.decode('utf-8');base=metadata['snapshot_commit']
    markers={}
    for kind,identity in re.findall(r'^<!-- ([a-z_]+): (.*?) -->$',markdown,re.M):markers.setdefault(kind,[]).append(identity)
    for kind,count in metadata['coverage'].items():assert len(markers[kind])==len(set(markers[kind]))==count,(kind,count)
    names=sorted(metadata['source_hashes'])
    result=subprocess.run(['git','cat-file','--batch'],input=''.join(base+':'+name+'\n' for name in names).encode(),capture_output=True,cwd=ROOT,check=True)
    stream=io.BytesIO(result.stdout);source={}
    for name in names:
        header=stream.readline().decode().split();assert len(header)==3 and header[1]=='blob',name
        raw=stream.read(int(header[2]));assert stream.read(1)==b'\n';assert sha(raw)==metadata['source_hashes'][name],name;source[name]=raw
    assert stream.read()==b''
    for name,identity in metadata['editorial_hashes'].items():assert sha((ROOT/name).read_bytes())==identity,name
    assert sha((ROOT/'scripts/generate_project_report.py').read_bytes())==metadata['generator_sha256']
    original=json.loads(source['progresso/inventario-operacoes-v1.json']);spec=json.loads(source['docs/especificacao-funcional.json']);architecture=json.loads(source['docs/arquitetura-componentes.json'])
    assert markers['operation']==[o['id'] for f in spec['families'] for o in original['operations'] if o['family_id']==f['id']]
    assert markers['family']==[f['id'] for f in spec['families']]
    assert markers['acceptance']==[c['id'] for f in spec['families'] for c in f['acceptance_cases']]
    assert markers['module']==[m['id'] for m in architecture['modules']]
    suite=json.loads(source['testes/resultados/0.1.16/source-intermediate.json'])['test_runs'][0]
    assert markers['own_test']==sorted(c['id'] for c in suite['cases'])
    html_path=ROOT/'docs'/(NAME+'.html');html=html_path.read_bytes();parsed=ReportHTML();parsed.feed(html.decode('utf-8'));parsed.close()
    assert parsed.pre is None and parsed.detail_starts==parsed.detail_ends and parsed.detail_starts>200
    assert not parsed.external_resources and parsed.scripts==1
    assert all('sec-'+str(i) in parsed.ids for i in range(1,21))
    assert len(parsed.ids)==len(set(parsed.ids)),'Duplicate HTML anchors'
    body=''.join(parsed.text)
    assert all(identity in body for identity in markers['own_test'])
    block_hashes={sha(canonical(block).encode()) for block in parsed.blocks}
    incorporated=markers['full_document']+markers['full_record']+['progresso/notas-continuidade.md']
    for name in incorporated:
        expected=canonical(source[name].decode('utf-8-sig'))
        assert sha(expected.encode()) in block_hashes,'Missing/truncated standalone source text: '+name
    assert metadata['own_application_tests_rerun'] is False and metadata['original_executed'] is False and metadata['vm_inspected'] is False and metadata['criteria_or_weights_changed'] is False
    metadata.update(html_file=html_path.relative_to(ROOT).as_posix(),html_sha256=sha(html),html_bytes=len(html),renderer_sha256=sha((ROOT/'scripts/render_project_report.ps1').read_bytes()),verification=dict(passed=True,git_source_hashes_verified=len(names),editorial_hashes_verified=len(metadata['editorial_hashes']),unique_markers_verified={key:len(value) for key,value in markers.items()},standalone_source_texts_preserved=len(incorporated),html_preformatted_blocks=len(parsed.blocks),html_details_balanced=parsed.detail_starts,all_twenty_chapter_anchors_present=True,duplicate_html_anchors=False,all_564_test_ids_present_in_html=True,external_resource_dependencies=False))
    metadata_path.write_bytes((json.dumps(metadata,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps({k:metadata[k] for k in ('report_bytes','report_lines','html_bytes','verification')}))


if __name__=='__main__':main()
