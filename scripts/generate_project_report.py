#!/usr/bin/env python3
"""Generate an unabridged project dossier from an immutable Git snapshot."""
import argparse
import ast
from collections import Counter, defaultdict
import csv
from datetime import datetime
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
from urllib.parse import quote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
REPORT_NAME = 'RELATORIO-COMPLETO-LINUXIT-PDF-2026-10-19'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-commit', required=True)
    parser.add_argument('--output', type=Path, default=ROOT/'docs'/(REPORT_NAME+'.md'))
    parser.add_argument('--review', type=Path, default=ROOT/'testes/resultados/relatorio-completo-2026-10-19/review.json')
    args = parser.parse_args()
    args.output=args.output.resolve()
    args.review=args.review.resolve()
    base = subprocess.check_output(['git','rev-parse',args.base_commit+'^{commit}'],cwd=ROOT,text=True).strip()
    assert re.fullmatch('[0-9a-f]{40}',base)
    for target in (args.output,args.review):
        if not target.resolve().is_relative_to(ROOT):raise ValueError('Output must stay in the authorized repository')
        if target.exists():raise ValueError('Use new output paths to preserve the earlier report')
    tree = subprocess.check_output(['git','ls-tree','-rl',base],cwd=ROOT,text=True).splitlines()
    tracked=[]
    for line in tree:
        metadata,name=line.split('\t',1);mode,kind,identity,size=metadata.split()
        tracked.append(dict(path=name,mode=mode,kind=kind,git_object=identity,bytes=int(size)))
    manifests=sorted([t['path'] for t in tracked if re.fullmatch(r'releases/manifest-\d+\.\d+\.\d+\.json',t['path'])],key=lambda p:tuple(map(int,re.search(r'(\d+)\.(\d+)\.(\d+)',p).groups())))
    paths=['docs','progresso','app','tests','scripts','engenharia-reversa','testes','.github','README.md','AGENTS.md','LICENSE','releases/manifest.json','releases/SHA256SUMS','releases/runtime-packages-0.1.16.tsv','releases/runtime-source-access-0.1.16.json']+manifests
    archive=subprocess.check_output(['git','archive','--format=tar',base,*paths],cwd=ROOT)
    blobs={}
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        for member in bundle.getmembers():
            if member.isfile():blobs[member.name]=bundle.extractfile(member).read()
    del archive
    used={}
    def raw(name):
        content=blobs[name];used[name]=hashlib.sha256(content).hexdigest();return content
    def text(name):return raw(name).decode('utf-8-sig')
    def data(name):return json.loads(text(name))
    def link(name,label=None):
        return '['+(label or name)+'](https://github.com/airtonbp19edu/Linuxit-PDF/blob/'+base+'/'+quote(name,safe='/')+')'
    def compact(value):
        if value is None:return 'não comprovado (`null`)'
        if value is True:return 'sim'
        if value is False:return 'não'
        if isinstance(value,(dict,list)):return json.dumps(value,ensure_ascii=False)
        return str(value)
    def cell(value):return compact(value).replace('|','&#124;').replace('\n','<br>')
    def local_time(value):
        return datetime.fromisoformat(value.replace('Z','+00:00')).astimezone(ZoneInfo('America/Sao_Paulo')).strftime('%Y/%m/%d às %H:%M:%S') if value else 'não registrado'
    lines=[];counts=Counter()
    def add(*values):lines.extend(str(v) for v in values)
    def para(value):add(value,'')
    def bullets(values):
        for value in values:add('- '+compact(value))
        add('')
    def table(headers,rows):
        add('| '+' | '.join(headers)+' |','|'+'|'.join('---' for _ in headers)+'|')
        for row in rows:add('| '+' | '.join(cell(x) for x in row)+' |')
        add('')
    def fence(value,language='json'):
        value=value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2)
        delimiter='`'*(max([len(m.group()) for m in re.finditer(r'`+',value)]+[2])+1)
        add(delimiter+language,value.rstrip('\n'),delimiter,'')
    def detail(title,value,language='json'):
        add('<details>','<summary>'+title+'</summary>','');fence(value,language);add('</details>','')
    def section(number,title):add('<a id="sec-'+str(number)+'"></a>','',f'## {number}. {title}','')
    def marker(kind,identity):add('<!-- '+kind+': '+str(identity)+' -->');counts[kind]+=1
    progress=data('progresso/progresso.json');catalog=data('progresso/inventario-operacoes-v1.json');spec=data('docs/especificacao-funcional.json')
    arch=data('docs/arquitetura-componentes.json');pending=data('progresso/pendencias-analises.json');plan=data('progresso/plano-continuidade.json')
    execution=data('progresso/execucao-plano.json');nonvm=data('progresso/execucao-sem-vm.json');manifest=data('releases/manifest.json')
    context_path=ROOT/'docs/relatorios/2026-10-19/contexto-editorial.md';assessment_path=ROOT/'docs/relatorios/2026-10-19/avaliacao-familias.json'
    pending_assessment_path=ROOT/'docs/relatorios/2026-10-19/avaliacao-pendencias.json';timing_path=ROOT/'docs/relatorios/2026-10-19/tempos-ci.json'
    context=context_path.read_text(encoding='utf-8');assessment=json.loads(assessment_path.read_text(encoding='utf-8'))
    pending_assessment=json.loads(pending_assessment_path.read_text(encoding='utf-8'));timings=json.loads(timing_path.read_text(encoding='utf-8'))
    assert assessment['snapshot_commit']==base
    assert pending_assessment['snapshot_commit']==base and len(pending_assessment['criteria'])==19
    families=spec['families'];assert set(assessment['families'])=={f['id'] for f in families}
    own=data('testes/resultados/0.1.16/source-intermediate.json');suites={'Fonte Linux':own['test_runs'][0],'Payload':data('testes/resultados/0.1.16/payload-tests.json'),'Flatpak instalado':data('testes/resultados/0.1.16/sandbox-tests.json')}
    for suite in suites.values():assert suite['run']==suite['passed']==564 and all(suite[k]==0 for k in ('failures','errors','skipped'))
    for name,identity in manifest['report_hashes'].items():assert hashlib.sha256(raw('testes/resultados/0.1.16/'+name)).hexdigest()==identity
    integrity=data('testes/resultados/0.1.16/source-payload-integrity.json')
    for row in integrity['files']:assert hashlib.sha256(raw('app/'+row['file'])).hexdigest()==row['sha256']
    assert manifest['version']=='0.1.16' and len(families)==25 and len(catalog['operations'])==111 and len(arch['modules'])==75
    criteria=[(s,c) for s in progress['stages'] for c in s['checks']];assert len(criteria)==58 and sum(c['status']=='done' for _,c in criteria)==39
    original_cases=data('testes/cenarios-dinamicos.json');ui_cases=data('testes/cenarios-interface.json');comparative=data('testes/plano-comparativo.json')
    rollup=data('testes/resultados/p03-2026-10-19-0113/comparison-rollup.json')
    static_rows=list(csv.DictReader(io.StringIO(text('engenharia-reversa/funcoes.csv'))));assert len(static_rows)==329
    now=datetime.now(ZoneInfo('America/Sao_Paulo'))
    add('# Linuxit PDF — relatório completo de trabalho, pendências e conclusão','')
    para('Elaborado em **'+now.strftime('%Y/%m/%d às %H:%M')+' (America/Sao_Paulo, UTC-03:00)**. Fotografia técnica: `'+base+'`. Este relatório não executou o Foxit, não acessou a VM e não repetiu as suítes do aplicativo. Ele examinou os registros, seus vínculos e hashes e organizou o conteúdo preservado.')
    titles=['Leitura do relatório e significado de conclusão','Identidade, escopo, entrega atual e medição','Todas as 25 famílias e 111 operações conhecidas','As 21 etapas e seus 58 critérios','Os 19 critérios ainda abertos','Planos P01–P10, lotes B01–B10 e tarefas S01–S12','Engenharia reversa e catálogo estático completo','VM, observações, 20 casos dinâmicos e 10 casos de interface','Os 17 recortes comparativos e seus limites','Os 564 testes próprios da entrega atual','Todas as versões e provas de entrega','Arquitetura: 75 módulos, 60 interfaces e dependências','Por que ainda está demorando','Caminho até um fechamento verificável','Divergências documentais e pendências antigas','Cronologia Git e notas de continuidade completas','Documentos técnicos completos da fotografia','Dados estruturados integrais e relatórios atuais','Inventário completo de arquivos versionados','Proveniência, cobertura e conferência do relatório']
    add('### Navegação','')
    for i,title in enumerate(titles,1):add(f'- [{i}. {title}](#sec-{i})')
    add('')
    para('Na versão HTML, os anexos extensos podem ser expandidos. Todo o conteúdo está no próprio arquivo, inclusive os textos integrais dos documentos históricos e dos registros estruturados. As referências externas são links de conferência; não são necessárias para ler o conteúdo já incorporado. Use a busca do navegador/editor por um ID, funcionalidade ou arquivo. Nenhum trecho foi substituído por reticências para reduzir o inventário.')
    introduction,rest=context.split('# Por que ainda está demorando',1)
    delay,closure=rest.split('# O que precisa acontecer até um fechamento verificável',1)
    section(1,titles[0]);add(re.sub(r'(?m)^#', '###',introduction).strip(),'')
    section(2,titles[1]);project=data('progresso/projeto.json')
    table(['Campo','Valor'],[['Referência',project['target']],['SHA-256 original fixado',project['reference_sha256']],['Revisão da fotografia',base],['Aplicativo/pacote','0.1.16/devel, desenvolvimento'],['Fonte do pacote',manifest['source_commit']],['Tamanho Flatpak',manifest['artifact']['bytes']],['SHA-256 Flatpak',manifest['artifact']['sha256']],['ID/arquitetura/runtime',manifest['application_id']+' / '+manifest['architecture']+' / '+manifest['runtime']],['Arquivos app comparados',manifest['source_payload_matched_files']],['Arquivos dependências / ELF / pacotes Debian',f"{manifest['bundled_runtime_files_audited']} / {manifest['bundled_elf_files_audited']} / {manifest['bundled_debian_packages']}"],['Suíte por ambiente','564/564, sem falhas/erros/skips'],['Checklist histórico',str(progress['general_progress_percent'])+'%;39done/19abertos'],['Conclusão global de reconstrução',progress['implementation_completion_percent']],['Famílias integralmente equivalentes','0/25; universo global ainda aberto'],['Todas as tarefas sem VM encerradas',nonvm['all_non_vm_work_complete']],['Nuvem direta', 'adiada pelo usuário'],['Assistente IA/generativa','excluída'],['Original/VM','Testes suspensos; sem inspeção nova para este relatório']])
    for name in ['releases/manifest-0.1.16.json','testes/resultados/0.1.16/validation-review.json','testes/resultados/0.1.16/audit/review.json','testes/resultados/0.1.16/desktop/review.json','testes/resultados/0.1.16/download-integrity-2026-10-19.json']:para('Evidência: '+link(name))
    para('Pacote público: ['+manifest['artifact']['file']+']('+manifest['distribution']['download_url']+'). O asset publicado é o mesmo arquivo aprovado, sem rebuild na auditoria. A identidade do pacote não é uma assinatura digital nem declaração de versão estável.')
    para('Fórmula do checklist: `peso da etapa × soma dos pesos internos done / soma de todos os pesos internos`. Critérios parciais não pontuam nesse índice. Não se calcula97/111,23/25 ou329/denominador desconhecido como porcentagem de código reconstruído.')
    section(3,titles[2]);para('Cada família apresenta a avaliação atual, os limites, o trabalho restante e todas as suas operações. Os campos antigos são preservados com esse rótulo para não substituir a realidade posterior por uma descrição histórica. A existência de código ou de testes relacionados não altera automaticamente o estado de aceitação integral da operação.')
    groups={f['id']:f for f in catalog['families']}
    for number,family in enumerate(families,1):
        fid=family['id'];current=assessment['families'][fid];record=groups[fid];marker('family',fid)
        add(f'### 3.{number}. {family["name"]} — `{fid}`','')
        for key,label in [('feito','Realizado nos recortes atuais'),('parcial','O que continua parcial ou limitado'),('falta','O que falta para fechar o escopo amplo'),('dependencias','Ambiente e dependências')]:add('#### '+label,'');bullets(current[key])
        para('Implementação registrada na matriz atual: '+family['matrix_implementation'])
        para('Observação original preservada: '+record['original_recorded_subset_summary'])
        para('Questões abertas no inventário (texto da fonte, que pode conter partes posteriormente esclarecidas): '+record['open_questions'])
        add('#### Contrato e casos de aceitação registrados','')
        para('Os campos de contrato abaixo são reproduzidos da fonte estruturada, que contém trechos legados. Quando divergem de uma entrega posterior, consultar a avaliação atual acima e a reconciliação do capítulo15; não interpretar automaticamente uma recusa histórica como limitação nova do código0.1.16.')
        for key,label in [('inputs','Entradas'),('outputs','Saídas'),('errors','Erros'),('state_and_side_effects','Estado e efeitos')]:
            add('**'+label+'**','');value=family[key];bullets(value if isinstance(value,list) else [value])
        para('Campo `scope` legado, mantido para rastreabilidade; a avaliação atual acima tem prioridade quando há evolução posterior: '+family['scope'])
        for case in family['acceptance_cases']:
            marker('acceptance',case['id']);add('##### '+case['id']+' — '+case['kind'],'')
            table(['Aspecto','Registro'],[['Dado',case['given']],['Ação',case['when']],['Resultado esperado próprio',case['expected_linuxit']],['Base',case['expected_basis']],['Execução integral',case['execution_status']],['Esperado Foxit',case['foxit_expected']],['Observado Foxit',case['foxit_observed']]])
        add('#### Todas as operações desta família','')
        for operation in [o for o in catalog['operations'] if o['family_id']==fid]:
            marker('operation',operation['id']);add('##### `'+operation['id']+'` — '+operation['title'],'')
            state={'bounded_source_present':'Código de um recorte presente; operação/família integral não aceita','pending_or_target_characterization':'Pendente ou contrato/disponibilidade do alvo ainda a caracterizar','deferred_by_user':'Adiado pelo usuário'}[operation['implementation_state']]
            para('**Estado:** '+state+'.')
            para('**Contrato registrado:** '+operation['output_and_acceptance'])
            para('**Entradas/contexto:**');bullets(operation['input_context'])
            for evidence in operation['source_evidence']:para('Código: '+link(evidence['path'])+' — `'+evidence['symbol']+'`, linhas'+str(evidence['line'])+'–'+str(evidence['end_line'])+'; SHA-256 `'+evidence['file_sha256']+'`.')
            para('Aceitação integral nova: `'+operation['operation_acceptance_new_execution']+'`. Comparação: `'+operation['comparison_state']+'`. Pacote de continuidade indicado: `'+operation['next_package']+'`.')
            detail('Registro integral desta operação:todos os campos, vínculos, testes históricos e hashes',operation)
        detail('Contrato integral da família, incluindo todas as referências de fonte/testes/fixtures e limites do original',family)
    section(4,titles[3]);para('Os estados a seguir pertencem ao roteiro original. São58critérios,39done e19abertos. Evidência histórica suficiente para um critério específico não comprova que toda a funcionalidade atual esteja integralmente reconstruída. Nenhum peso/estado foi alterado pela produção deste relatório.')
    earned=Fraction()
    for stage in progress['stages']:
        marker('stage',stage['id']);add(f'### Etapa {stage["id"]} — {stage["title"]}','')
        internal=sum(c['weight'] for c in stage['checks']);done=sum(c['weight'] for c in stage['checks'] if c['status']=='done');fraction=Fraction(done,internal);earned+=stage['weight_percent']*fraction
        para(f'Peso no roteiro:{stage["weight_percent"]}%. Fração verificada pelos critérios:{done}/{internal}. Contribuição ao índice:{float(stage["weight_percent"]*fraction):.6f}pontos percentuais. Esses números não são percentual de implementação da família.')
        for index,check in enumerate(stage['checks'],1):
            marker('criterion',str(stage['id'])+'/'+str(index));add('#### '+check['criterion'],'');para('Estado:`'+check['status']+'`; peso interno:'+str(check['weight'])+'.')
            if check.get('note'):para('Nota preservada: '+check['note'])
            bullets([link(name) for name in check['evidence']]);detail('Registro completo do critério',check)
        detail('Registro completo da etapa, incluindo revisões/entregas históricas adicionais',stage)
    assert round(float(earned),2)==progress['general_progress_percent']
    section(5,titles[4]);para('Esta é a lista completa dos19critérios ainda abertos, com seus bloqueios e próximos passos registrados. Alguns próximos passos antigos já tiveram avanço parcial posterior:essa divergência é explicitada no capítulo15. Ler a lista junto da avaliação atual por família e das evidências0.1.16, sem repetir automaticamente operações já implementadas.')
    for i,item in enumerate(pending['unfinished_criteria'],1):
        marker('unfinished',i);add(f'### Pendência {i} — etapa {item["stage_id"]}: {item["criterion"]}','')
        para('Estado:`'+item['criterion_status']+'`. Categorias de bloqueio: '+', '.join(item['blocker_categories'])+'.')
        current=pending_assessment['criteria'][i-1];assert (current['stage_id'],current['criterion'])==(item['stage_id'],item['criterion'])
        marker('current_open_criterion_review',i)
        para('**O que já foi realizado, em linguagem atual:** '+current['realizado'])
        para('**O que realmente falta para encerrar:** '+current['falta'])
        para('**Dependência atual:** '+current['dependencia'])
        para('Próxima ação registrada na fonte: '+item['next_action']);bullets([link(p) for p in item['evidence_refs']]);detail('Registro completo da pendência, sem omitir evidências ou causa de interrupção',item)
    section(6,titles[5]);para('As três filas abaixo são camadas de organização do mesmo projeto. Não devem ser somadas como se fossem funcionalidades diferentes, nem substituir as21etapas. O snapshot inicial de um plano pode descrever uma versão anterior:as execuções posteriores têm suas próprias identidades.')
    for title,items,kind in [('Pacotes P01–P10',plan['steps'],'package'),('Lotes B01–B10',plan['implementation_batches'],'batch'),('Execução sem VM S01–S12',nonvm['tasks'],'no_vm_task')]:
        add('### '+title,'')
        for item in items:
            marker(kind,item['id']);add('#### '+item['id']+' — '+item['title'],'');detail('Conteúdo integral:status,tarefas,dependências,entregas,critérios de fechamento e evidências',item)
    add('### Execução efetivamente registrada de P01–P03','');fence(execution)
    add('### Backlog original completo das25famílias no plano de continuidade','');para('Este backlog preserva textos antigos como B01/combo editável e P09/planned. A0.1.15/0.1.16 já avançou em vários deles; a classificação atual está no capítulo3.');fence(plan['family_backlog'])
    section(7,titles[6]);para('Catálogo publicável:329entradas distintas,152REA e177diretas exclusivas segundo os relatórios examinados. São observações de código com confiança variável; não são329funções integralmente recodificadas. Protótipos e saídas não comprovados permanecem explicitamente não verificados. Slots e auxiliares por salto não são somados automaticamente como funções únicas.')
    para('Ferramentas registradas:REA6.5.0,Ghidra12.1.4,TemurinJDK21,Capstone5.0.6 e pefile2024.8.26. As rodadas diretas `-noanalysis` não são apresentadas como novas observações MCP. O executável e a DLL permanecem identificados pelos hashes dos relatórios.')
    para('Rodada de18/10:48entradas novas em oito lotes,6.830instruções e25.919bytes selecionados. Rodadas posteriores de19/10:seis entradas novas,266instruções e803bytes. Esses totais pertencem às rodadas descritas; não representam todo o binário. A ressalva de fronteira de37bytes e os recortes sem semântica completa continuam válidos.')
    for module in sorted({r['module'] for r in static_rows}):
        add('### Módulo original: '+module,'')
        for row in [r for r in static_rows if r['module']==module]:
            marker('static_function',row['id']);add('#### `'+row['id']+'`','');table(['Campo original','Conteúdo'],[[k,v] for k,v in row.items()])
    section(8,titles[7]);para('Os testes do original foram interrompidos quando o relógio deixou de avançar. Último checkpoint documentado:09:54:23 de19/10/2026. Não houve inspeção/entrada/rede/restart para este levantamento. P02 foi validada offline; P03 permanece parcial. Há observações posteriores aos arquivos iniciais de cenário, portanto status `not_run` de um plano inicial não deve apagar uma observação posterior, nem uma observação parcial deve aprovar todas as variantes.')
    for title,source,kind in [('Campanha dinâmica D01–D20',original_cases,'dynamic_case'),('Campanha de interface UI01–UI10',ui_cases,'ui_case')]:
        add('### '+title,'')
        for case in source['cases']:marker(kind,case['id']);add('#### '+case['id'],'');fence(case)
        detail('Regras,precondições,campos de registro e conclusão da campanha',{k:v for k,v in source.items() if k!='cases'})
    para('As notas de continuidade e documentos VM/P02/P03 completos estão nos capítulos16–17. Eles preservam as ações confirmadas, resultados desconhecidos, permissões de manutenção/reinício e paradas. Um estado `running` do host não comprova resposta do guest.')
    section(9,titles[8]);para('Consolidado preservado:13medições distintas iguais,zero divergências medidas nesse consolidado e quatro inconclusivas. São17recortes de comparação, não17casos completos de família. Parte das medidas veio de rodadas e revisões anteriores; elas não são uma nova comparação do código0.1.16 completo contra o Foxit. A divergência de autoria foi corrigida no marco próprio e tem sua evidência separada.')
    by_id={c['id']:c for c in rollup['cases']}
    for case in comparative['cases']:
        marker('comparison',case['id']);add('### '+case['id'],'');fence(case);para('Resultado preservado no consolidado:');fence(by_id[case['id']])
    detail('Consolidado completo e proveniência',rollup)
    section(10,titles[9]);para('Cada linha é um método executado na suíte própria da0.1.16. Os564IDs foram preservados nos três ambientes, todos aprovados. Não são564funcionalidades e não são os50planos completos S12. A execução foiCI39339330479, fonte `'+manifest['source_commit']+'`.490IDs anteriores foram preservados e74novos incluídos.')
    table(['Ambiente','Tempo total registrado da suíte, em segundos'],[[name,suite['elapsed_sec']] for name,suite in suites.items()])
    indexed={name:{c['id']:c for c in suite['cases']} for name,suite in suites.items()};ids=sorted(indexed['Fonte Linux'])
    assert all(set(mapping)==set(ids) for mapping in indexed.values())
    rows=[]
    for i,identity in enumerate(ids,1):
        marker('own_test',identity);rows.append([i,identity,*[mapping[identity]['status'] for mapping in indexed.values()],*[f"{mapping[identity].get('elapsed_sec',0):.6f}s" for mapping in indexed.values()]])
    table(['Nº','ID integral','Fonte','Payload','Sandbox','Tempo fonte','Tempo payload','Tempo sandbox'],rows)
    for title,name in [('Auditoria independente','testes/resultados/0.1.16/audit/review.json'),('Desktop duas repetições','testes/resultados/0.1.16/desktop/review.json')]:add('### '+title,'');fence(data(name))
    para('A auditoria do pacote acrescentou11controles,5verificações de funcionamento e3testes GTK. Ela não repetiu os564métodos. O desktop executou9controles em cada um de dois ambientes novos. O Windows da fonte teve5controles próprios em revisão anterior, não toda a suíte0.1.16 nem um instalador final Windows.')
    section(11,titles[10]);para('A tabela conserva os manifestos de0.1.0 a0.1.16. Os schemas iniciais são diferentes:smoke sandbox não foi convertido em suíte completa quando esse número não foi registrado. As quantidades de testes mudaram; não são uma régua de porcentagem do produto.')
    release_rows=[]
    for name in manifests:
        item=data(name);v=item['validation'];version=item['version'];artifact=item['artifact']
        def summary(keys):
            for k in keys:
                if isinstance(v.get(k),dict) and 'run' in v[k]:return str(v[k].get('passed'))+'/'+str(v[k]['run'])+'; skips='+str(v[k].get('skipped','não registrado'))
            return 'não registrado nesse schema como suíte completa'
        release_rows.append([version,summary(['source','source_regressions']),summary(['payload','payload_regressions','fixed_payload_regressions']),summary(['sandbox']),artifact.get('bytes'),artifact.get('sha256'),item.get('source_commit','ver o manifesto original')])
        marker('release',version)
    table(['Versão','Fonte','Payload','Sandbox completo','Bytes','SHA-256','Commit fonte registrado'],release_rows)
    for name in manifests:detail(name+' — manifesto integral',data(name))
    add('### Relatórios selados da0.1.16','');table(['Arquivo','SHA-256'],manifest['report_hashes'].items())
    add('### Todas as dependências de runtime da0.1.16 por pacote e versão','')
    runtime_packages=list(csv.DictReader(io.StringIO(text('releases/runtime-packages-0.1.16.tsv')),delimiter='\t'))
    table(['Pacote binário','Versão binária','Pacote fonte','Versão fonte'],[[row[k] for k in ('binary_package','version','source_package','source_version')] for row in runtime_packages])
    para('A auditoria verificou297avisos e as versões/origens fonte correspondentes. A presença dos avisos de copyright é atribuição de dependências distribuídas, não297infrações. Os links e versões fonte foram confrontados com o build; a auditoria não baixou todas as fontes de todos os pacotes. O inventário completo de3684arquivos de runtime e seus hashes está incorporado no capítulo18.')
    section(12,titles[11]);para('São75módulos próprios documentados e60interfaces/referências explícitas. Isso não equivale a75componentes do Foxit recuperados. A lista exclui vendor como se fosse código novo próprio, mas os arquivos de terceiros continuam nos manifestos e na proveniência. Os símbolos abaixo vêm do AST da fotografia, sem executar GTK ou o original.')
    for module in arch['modules']:
        marker('module',module['id']);add('### '+module['id']+' — '+link(module['path']),'');para('Fronteira:`'+module['boundary']+'`. Responsabilidade: '+module['responsibility'])
        source=text(module['path']);syntax=ast.parse(source,filename=module['path']);api=[]
        for node in syntax.body:
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):api.append([node.lineno,node.end_lineno,node.name+'('+ast.unparse(node.args)+')'])
            elif isinstance(node,ast.ClassDef):
                api.append([node.lineno,node.end_lineno,'class '+node.name+'('+', '.join(ast.unparse(b) for b in node.bases)+')'])
                for method in node.body:
                    if isinstance(method,(ast.FunctionDef,ast.AsyncFunctionDef)):api.append([method.lineno,method.end_lineno,node.name+'.'+method.name+'('+ast.unparse(method.args)+')'])
        table(['Linha inicial','Linha final','Símbolo/assinatura Python'],api)
        constants=[]
        for node in syntax.body:
            if isinstance(node,ast.Assign):
                names=[t.id for t in node.targets if isinstance(t,ast.Name) and t.id.isupper()]
                if names and isinstance(node.value,(ast.Constant,ast.List,ast.Tuple,ast.Set,ast.Dict,ast.BinOp,ast.UnaryOp)):constants.append([','.join(names),ast.unparse(node.value)])
        if constants:add('Constantes literais/expressões declaradas no módulo:','');table(['Nome','Valor expresso no código'],constants)
        para('Linhas no arquivo:'+str(len(source.splitlines()))+'. SHA-256:`'+hashlib.sha256(raw(module['path'])).hexdigest()+'`. Contagem descritiva, sem uso como porcentagem de reconstrução.')
    add('### Todas as60interfaces documentadas','');table(['Nº','Arquivo','Símbolo'],[[i,link(ref['path']),ref['symbol']] for i,ref in enumerate(arch['interface_refs'],1)])
    add('### Acoplamentos e limitações de arquitetura','');fence(arch['known_couplings']);fence(arch['runtime_limitations']);fence(data('docs/proveniencia-base.json'))
    section(13,titles[12]);add(re.sub(r'(?m)^##', '###',delay).strip(),'')
    add('### Tempos concretos de CI preservados','')
    para('As datas a seguir vieram de respostas da API do GitHub salvas durante as execuções. O intervalo é entre os passos registrados do job: não é controle de horas humanas e não inclui automaticamente a fila anterior. Dois jobs paralelos não são somados como se tivessem sido sequenciais. Os dados integrais estão incorporados logo após a tabela.')
    timing_rows=[]
    for run in timings['runs']:
        for job in run['jobs']:timing_rows.append([run['id'],run['head_sha'],job['name'],job['conclusion'],local_time(job['first_step_started_at']),local_time(job['last_step_completed_at']),job['observed_step_span_seconds']])
    table(['Execução','Revisão','Job','Resultado','Primeiro passo São Paulo','Último passo São Paulo','Intervalo observado,segundos'],timing_rows)
    para('Na execução aprovada39339330479, as suítes registraram138,35s na fonte,142,69s no payload e379,73s no sandbox:aproximadamente660,77s de execução das três suítes. Isso ajuda a explicar o custo de uma revalidação completa. Não é tempo gasto escrevendo código ou prova de que toda a demora do projeto foi CI.')
    detail('Registros integrais dos passos e horários dos cinco workflows selecionados',timings)
    section(14,titles[13]);add(re.sub(r'(?m)^##', '###',closure).strip(),'')
    section(15,titles[14]);para('Estas divergências foram examinadas durante a montagem do relatório. O texto da fonte foi preservado nos anexos; a existência da divergência não revoga os resultados posteriores. É necessária reconciliação dos campos atuais antes de usá-los automaticamente como próxima fila de implementação.')
    discrepancies=[
      ['docs/especificacao-funcional.json','scope de forms ainda descreve0.1.10 e eventos/combo editável como pendentes','Combo editável0.1.15 e cálculos declarativos0.1.16 existem; XFA/JavaScript geral continuam abertos.'],
      ['docs/especificacao-funcional.json','scope de search-language diz stemming/idiomas pendentes','36algoritmos Snowball explícitos estão implementados; equivalência Lucene e tokenização universal continuam abertas.'],
      ['docs/especificacao-funcional.json','scope de accessibility diz sem voz','WAV local e reprodução controlada existem; leitor de tela/áudio físicos e semântica universal permanecem pendentes.'],
      ['docs/especificacao-funcional.json','scope de layers-media descreve só listagem de OCG','Há alternância,visibilidade salva,mídia/PCM e extração3D; renderizador3D continua ausente.'],
      ['docs/especificacao-funcional.json','scope de signatures nega assinatura,cadeia,CRL e tempo','Há PEM e política offline CA/CRL/token de assinatura; não há PAdES-LTV integral ou DocTimeStamp independente.'],
      ['docs/especificacao-funcional.json','scope de annotations ainda nega popup,respostas e desenho livre','Ink/respostas e novas geometrias/popup/conversas foram acrescentados; edição universal continua aberta.'],
      ['docs/especificacao-funcional.json','scope de security ainda diz abertura cifrada integrada pendente','A sessão autenticada foi implementada na0.1.14 e edição/impressão ampliadas na0.1.16; RMS continua pendente.'],
      ['docs/especificacao-funcional.json','scope de measurement diz sem calibração','Calibração e outros recortes de medida foram acrescentados; não há encaixe universal em vetores nem paridade completa.'],
      ['progresso/pendencias-analises.json','vários next_action ainda pedem combo editável ou concluir P02 e citam relógios anteriores','Não reiniciar essa implementação/coleta como se faltasse tudo; consultar a0.1.16,P02validada e a parada posterior09:54:23.'],
      ['progresso/plano-continuidade.json','snapshot0.1.13 e P06/P09planned, B01combo editável primeiro','É o contexto de criação do plano. Houve entregas0.1.14–0.1.16; falta encerramento integral, não ausência completa de execução.'],
      ['progresso/projeto.json','local_folder_workflow contém desktop_portal_interaction_tested=false','Esse registro foi criado antes dos probes novos; non_vm_execution_followup e desktop0.1.16 registram persistência/revogação9/9. Cliente sincronizador real continua pendente.'],
      ['docs/MEDICAO-PROGRESSO.md','trechos históricos usam43,93% e versões antigas','A revisão explica a limitação do método; a seção posterior registra45,13%. Nenhum desses índices mede código reconstruído.'],
      ['progresso/tarefas-pendentes.md','tabela antiga cita entrega0.1.13 e portal/combo ainda pendentes','A abertura atual do arquivo e os relatórios0.1.16 têm prioridade temporal; a tabela histórica não é uma fila atual reconciliada.'],
      ['progresso/sincronizacao-git.json','guarda um commit de publicação técnica anterior ao último commit de notas','É intencional para evitar autorreferência; a confirmação final foi feita por ls-remote em recibo fora da árvore. Não confundir com falta de push.']]
    table(['Fonte','Texto/situação legado','Leitura correta na fotografia'],discrepancies)
    section(16,titles[15]);log_text=subprocess.check_output(['git','log',base,'--reverse','--format=%H%x09%aI%x09%cI%x09%s'],cwd=ROOT,text=True)
    commits=[row.split('\t',3) for row in log_text.splitlines()];para('Há'+str(len(commits))+'commits no histórico alcançável dessa fotografia. Datas de autor e de commit são preservadas. A primeira revisão disponível já registra o marco0.1.1; não se presume que ela contenha todo o trabalho anterior. Intervalos entre commits não são controle de horas.')
    table(['Nº','Commit','Data autor São Paulo','Data commit São Paulo','Descrição integral'],[[i,row[0],local_time(row[1]),local_time(row[2]),row[3]] for i,row in enumerate(commits,1)])
    detail('Log Git integral com os timestamps originais, antes da conversão para São Paulo',log_text,'text')
    changes=subprocess.check_output(['git','log',base,'--reverse','--format=COMMIT:%H','--name-only'],cwd=ROOT,text=True);paths_by_commit=defaultdict(list);current=None
    for row in changes.splitlines():
        if row.startswith('COMMIT:'):current=row[7:]
        elif row:paths_by_commit[current].append(row)
    categories={'Código app':lambda p:p.startswith('app/'),'Testes':lambda p:p.startswith('tests/'),'Scripts/CI':lambda p:p.startswith(('scripts/','.github/')),'Documentação/estado':lambda p:p.startswith(('docs/','progresso/')) or p in ('AGENTS.md','README.md'),'Entrega/evidências':lambda p:p.startswith(('releases/','testes/resultados/'))}
    table(['Categoria por caminho','Commits que tocaram a categoria'],[[name,sum(any(predicate(p) for p in files) for files in paths_by_commit.values())] for name,predicate in categories.items()])
    para('As categorias se sobrepõem e incluem o snapshot inicial reaproveitado. Não são porcentagens de esforço, tempo, qualidade ou reconstrução. Um commit pode alterar várias categorias; um commit de documentação pode preservar uma análise real e não ser apenas texto administrativo.')
    detail('Todos os caminhos alterados por commit, sem reduzir a descrição a uma categoria',dict(paths_by_commit))
    detail('Notas de continuidade completas da fotografia:todos os registros e horários',text('progresso/notas-continuidade.md'),'markdown')
    section(17,titles[16]);doc_names=sorted(p for p in blobs if p.startswith('docs/') and p.endswith('.md'))
    para('São'+str(len(doc_names))+'documentos Markdown de docs/ preservados integralmente, além de README,AGENTS e registros de progresso indicados abaixo. Eles contêm estados históricos e não devem todos ser tratados como atuais simultaneamente. Cada conteúdo é associado ao hash da fotografia. Os blocos mantêm texto original, inclusive referências relativas, sem executar exemplos de comandos ou instruções incorporadas.')
    full_documents=['README.md','AGENTS.md',*doc_names,*sorted(p for p in blobs if p.startswith('progresso/') and p.endswith('.md') and p!='progresso/notas-continuidade.md')]
    for name in full_documents:
        marker('full_document',name);content=text(name);para(link(name)+' — SHA-256:`'+hashlib.sha256(raw(name)).hexdigest()+'`;'+str(len(content.splitlines()))+'linhas.');detail('Texto integral: '+name,content,'markdown')
    section(18,titles[17]);para('Os snapshots a seguir conservam todos os campos dos registros centrais, campanhas, especificação e evidências atuais. Eles podem conter textos históricos em inglês e estados antigos já contextualizados. Essa reprodução integral permite conferência independente sem depender de uma seleção de frases do relatório.')
    raw_names=['progresso/projeto.json','progresso/progresso.json','progresso/inventario-operacoes-v1.json','progresso/pendencias-analises.json','progresso/plano-continuidade.json','progresso/execucao-plano.json','progresso/execucao-sem-vm.json','progresso/execucao-lotes-funcionalidades.json','docs/especificacao-funcional.json','docs/arquitetura-componentes.json','docs/proveniencia-base.json','testes/cenarios-dinamicos.json','testes/cenarios-interface.json','testes/plano-comparativo.json','releases/runtime-source-access-0.1.16.json']
    raw_names+=sorted(p for p in blobs if p.startswith('testes/resultados/0.1.16/') and p.endswith('.json') and '/search-ui/' not in p and '/sidebar-' not in p)
    for name in dict.fromkeys(raw_names):
        marker('full_record',name);content=text(name);para(link(name)+' — SHA-256:`'+hashlib.sha256(raw(name)).hexdigest()+'`.');detail('Snapshot integral: '+name,content,'json')
    section(19,titles[18]);para('Esta é a lista de todos os arquivos versionados na fotografia, com tamanho e identificador do objeto Git. O identificador de objeto abaixo não é apresentado como SHA-256 do arquivo:ele é o ID de objeto fornecido pelo Git. O asset Flatpak0.1.16 é externo à árvore e possui identidade própria no manifesto. Arquivos ignorados,originais e projetos locais de análise não são apresentados como se estivessem publicados.')
    table(['Nº','Caminho integral','Bytes','Tipo','Objeto Git'],[[i,row['path'],row['bytes'],row['kind'],row['git_object']] for i,row in enumerate(tracked,1)])
    section(20,titles[19]);para('Os dados foram lidos de um arquivo Git da revisão fixada, sem depender do estado variável de arquivos de trabalho. A prosa editorial foi escrita para esta solicitação e é identificada separadamente. O relatório não mudou a implementação, pesos, critérios ou resultados dos testes. Não executou o original ou a VM e não gerou um novo Flatpak.')
    table(['Cobertura','Quantidade'],[['Famílias',counts['family']],['Operações',counts['operation']],['Etapas',counts['stage']],['Critérios',counts['criterion']],['Pendências amplas',counts['unfinished']],['Planos de aceitação',counts['acceptance']],['Entradas estáticas',counts['static_function']],['Casos D',counts['dynamic_case']],['Casos UI',counts['ui_case']],['Comparações delimitadas',counts['comparison']],['Métodos próprios',counts['own_test']],['Versões',counts['release']],['Módulos próprios',counts['module']],['Interfaces',len(arch['interface_refs'])],['Documentos integrais adicionais',counts['full_document']],['Snapshots estruturados integrais',counts['full_record']],['Arquivos versionados na fotografia',len(tracked)],['Commits na fotografia',len(commits)]])
    expected={'family':25,'operation':111,'stage':21,'criterion':58,'unfinished':19,'current_open_criterion_review':19,'acceptance':50,'package':10,'batch':10,'no_vm_task':12,'static_function':329,'dynamic_case':20,'ui_case':10,'comparison':17,'own_test':564,'release':17,'module':75}
    assert all(counts[key]==value for key,value in expected.items()),dict(counts)
    para('Todas as fontes efetivamente lidas para gerar o relatório:')
    table(['Arquivo','SHA-256 dos bytes da fotografia'],sorted(used.items()))
    editorial_paths=(context_path,assessment_path,pending_assessment_path,timing_path)
    para('Fontes editoriais e recorte de horários desta solicitação: '+', '.join('`'+p.relative_to(ROOT).as_posix()+'`' for p in editorial_paths)+'. O comprovante estruturado de geração registra seus hashes, a revisão base e as contagens. A publicação deste relatório terá um commit posterior à fotografia; esse novo commit não é usado como se tivesse existido antes da própria geração.')
    markdown='\n'.join(lines).rstrip()+'\n'
    assert '0.1.16' in markdown and 'esgotamento de tokens' in markdown and 'Este relatório não executou' in markdown
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(markdown.encode('utf-8'))
    review=dict(schema='linuxit-complete-project-report-review-v1',generated_at_local=now.isoformat(),snapshot_commit=base,report=args.output.relative_to(ROOT).as_posix(),report_sha256=hashlib.sha256(markdown.encode()).hexdigest(),report_bytes=len(markdown.encode()),report_lines=len(markdown.splitlines()),coverage=dict(counts),document_count=len(full_documents),structured_snapshot_count=len(dict.fromkeys(raw_names)),tracked_files=len(tracked),git_commits=len(commits),source_hashes=used,editorial_hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in editorial_paths},current_ci_seals_verified=len(manifest['report_hashes']),current_app_files_matched_to_candidate=len(integrity['files']),full_inventory_of_original_known=False,own_application_tests_rerun=False,original_executed=False,vm_inspected=False,criteria_or_weights_changed=False,report_is_complete_reconstruction=False)
    review['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.review.parent.mkdir(parents=True,exist_ok=True);args.review.write_bytes((json.dumps(review,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps({k:review[k] for k in ('snapshot_commit','report','report_bytes','report_lines','coverage','document_count','structured_snapshot_count','tracked_files','git_commits')}))


if __name__=='__main__':main()
