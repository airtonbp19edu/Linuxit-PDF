#!/usr/bin/env python3
"""Render evidence-backed weighted milestones; unknown global coverage stays null."""
from pathlib import Path
import csv,json

ROOT=Path(__file__).resolve().parents[1]
def render():
    path=ROOT/'progresso/progresso.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    if sum(stage['weight_percent'] for stage in data['stages'])!=100:
        raise ValueError('Stage weights must add to 100')
    total=0.0
    for stage in data['stages']:
        checks=stage['checks'];weight=sum(check['weight'] for check in checks)
        for check in checks:
            if check['status']=='done':
                if not check['evidence']:raise ValueError('Completed check without evidence')
                for name in check['evidence']:
                    if not (ROOT/name.split('#')[0]).exists():raise ValueError('Missing evidence: '+name)
        fraction=sum(check['weight'] for check in checks if check['status']=='done')/weight
        stage['verified_fraction']=round(fraction,6)
        stage['earned_percent']=round(stage['weight_percent']*fraction,6)
        total+=stage['weight_percent']*fraction
    data['general_progress_percent']=round(total,2)
    data['implementation_completion_percent']=None
    data['progress_interpretation']={
        'reporting_revision':2,
        'legacy_field':'general_progress_percent',
        'legacy_metric':'Weighted binary closure of original roadmap criteria; historical checklist index only.',
        'is_total_recoding_completion':False,
        'partial_criteria_contribution':0,
        'global_operation_denominator_complete':False,
        'review_ref':'docs/MEDICAO-PROGRESSO.md',
        'policy':'Report delivered features and recorded validation separately. Do not turn test, module or partial-family counts into a total completion percentage.'}
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    parity=list(csv.DictReader((ROOT/'progresso/matriz-paridade.csv').open(encoding='utf-8')))
    verified=sum(row['equivalent_to_foxit']=='verified' for row in parity)
    data['verified_functional_parity']={'percent':round(verified/len(parity)*100,2),'verified':verified,'identified_obligations':len(parity),'denominator_complete':False}
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    count=sum(1 for _ in csv.DictReader((ROOT/'engenharia-reversa/funcoes.csv').open(encoding='utf-8')))
    lines=['# Progresso e entregas verificáveis','',
        '**Conclusão total da recodificação: percentual indeterminado.** O inventário completo de operações e sua complexidade ainda não estão fechados. Não há base para publicar uma porcentagem global de implementação.',
        '',f'**Índice histórico do checklist do roteiro: {total:.2f}%.** Somente critérios integralmente `done` pontuam; avanços dentro de um critério `partial` acrescentam zero. Este índice é pouco sensível às entregas incrementais e não deve ser apresentado como porcentagem do código reconstruído. [Revisão da medição](../docs/MEDICAO-PROGRESSO.md).','']
    manifest_path=ROOT/'releases/manifest.json'
    if manifest_path.exists():
        manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
        lines += [f"**Pacote registrado:** {manifest['version']} de desenvolvimento. [Manifesto](../releases/manifest-{manifest['version']}.json).",'']
        suites=manifest.get('validation',{})
        if all(key in suites for key in ('source','payload','sandbox')):
            counts='; '.join(label+' '+str(suites[key]['passed'])+'/'+str(suites[key]['run']) for key,label in
                            (('source','fonte'),('payload','payload'),('sandbox','sandbox instalado')))
            lines += ['**Validação própria registrada nesse pacote:** '+counts+'. São evidências da entrega; este gerador não executa a suíte novamente e a quantidade de testes não mede conclusão funcional.','']
    lines += [f'**Paridade Foxit comprovada:** {verified}/{len(parity)} famílias identificadas por inteiro. O inventário funcional permanece aberto; esse contador não descreve quanto de cada família foi implementado. Testes próprios não contam como testes diferenciais.',
        '',f'**Cobertura global de engenharia reversa:** não calculável. Há {count} entradas distintas examinadas; 9.973 slots não constituem um denominador de funções únicas. Contagem de módulos também não estima cobertura de funcionalidades.',
        '','A tabela abaixo preserva os critérios, pesos e a comparabilidade do roteiro original. Fração de critérios verificados não é fração de funcionalidades pronta.','',
        '| Etapa | Peso | Fração de critérios verificados | Contribuição ao índice |','|---|---:|---:|---:|']
    for s in data['stages']:lines.append(f"| {s['id']:02d} — {s['title']} | {s['weight_percent']}% | {s['verified_fraction']*100:.1f}% | {s['earned_percent']:.2f}% |")
    lines+=['','A sincronização é medida separadamente em `sincronizacao-git.json`. O hash registrado é sempre de um commit remoto previamente confirmado; um arquivo não pode conter o hash do próprio commit. Consulte também a árvore/HEAD remotos e o estado de trabalho atual.','','Este relatório não encerra as 21 etapas. Atividades bloqueadas e parciais contribuem com zero até serem verificadas. Mudanças de critérios/pesos devem ser explicadas no histórico, preservando a comparabilidade.']
    (ROOT/'progresso/progresso.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'general_progress_percent':data['general_progress_percent'],'historical_roadmap_checklist_percent':data['general_progress_percent'],'implementation_completion_percent':None,'functional_parity':data['verified_functional_parity'],'global_reverse_engineering_coverage':None}))

if __name__=='__main__':render()
