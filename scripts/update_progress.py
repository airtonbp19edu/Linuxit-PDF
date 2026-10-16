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
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    parity=list(csv.DictReader((ROOT/'progresso/matriz-paridade.csv').open(encoding='utf-8')))
    verified=sum(row['equivalent_to_foxit']=='verified' for row in parity)
    data['verified_functional_parity']={'percent':round(verified/len(parity)*100,2),'verified':verified,'identified_obligations':len(parity),'denominator_complete':False}
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    count=sum(1 for _ in csv.DictReader((ROOT/'engenharia-reversa/funcoes.csv').open(encoding='utf-8')))
    lines=['# Progresso verificável','',f'Progresso geral do roteiro: **{total:.2f}%**. Cada etapa usa o peso do pedido; dentro dela, atividades têm pesos estimados, registrados no JSON. Somente atividades com estado `done` e evidência existente contam. Isso mede entregas do roteiro, não equivalência do aplicativo.','',f'Paridade Foxit verificada: **{verified}/{len(parity)} obrigações identificadas ({verified/len(parity)*100:.2f}%)**. O inventário funcional permanece aberto. Testes próprios não contam como testes diferenciais.','',f'Cobertura global de engenharia reversa: **não calculável** enquanto o universo de funções e seus pesos não estiver fechado. Medida parcial: quatro módulos com decompilação dirigida entre 141 PE inventariados (2,84%, peso unitário por módulo); {count} entradas distintas examinadas. 9.973 slots não constituem um denominador de funções únicas.','','| Etapa | Peso | Fração verificada | Contribuição |','|---|---:|---:|---:|']
    for s in data['stages']:lines.append(f"| {s['id']:02d} — {s['title']} | {s['weight_percent']}% | {s['verified_fraction']*100:.1f}% | {s['earned_percent']:.2f}% |")
    lines+=['','A sincronização é medida separadamente em `sincronizacao-git.json`. O hash registrado é sempre de um commit remoto previamente confirmado; um arquivo não pode conter o hash do próprio commit. Consulte também a árvore/HEAD remotos e o estado de trabalho atual.','','Este relatório não encerra as 21 etapas. Atividades bloqueadas e parciais contribuem com zero até serem verificadas. Mudanças de critérios/pesos devem ser explicadas no histórico, preservando a comparabilidade.']
    (ROOT/'progresso/progresso.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'general_progress_percent':data['general_progress_percent'],'functional_parity':data['verified_functional_parity'],'global_reverse_engineering_coverage':None}))

if __name__=='__main__':render()
