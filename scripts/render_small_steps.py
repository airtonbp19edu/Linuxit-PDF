#!/usr/bin/env python3
"""Validate progresso/etapas-pequenas.json and render docs/ETAPAS-PEQUENAS.md.

The JSON is the single source; the page is generated so the two never drift.
A step marked concluida must name its evidence and the publishing commit.
"""
import argparse
from datetime import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'progresso' / 'etapas-pequenas.json'
PAGE = ROOT / 'docs' / 'ETAPAS-PEQUENAS.md'
STATUSES = {'pendente': 'Pendente', 'em_andamento': 'Em andamento', 'concluida': 'Concluída',
            'bloqueada': 'Bloqueada', 'aguardando_usuario': 'Aguardando você', 'decidida': 'Decidida'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(data):
    require(data.get('schema') == 'linuxit-small-steps-v1', 'Unknown schema')
    for key in ('created_at_local', 'updated_at_local'):
        require(datetime.fromisoformat(data[key]).utcoffset() is not None, key + ' needs a time zone')
    ids = [step['id'] for step in data['steps']]
    require(len(ids) == len(set(ids)), 'Duplicate step id')
    for step in data['steps']:
        require(step['status'] in STATUSES, step['id'] + ': unknown status')
        require(all(step[k].strip() for k in ('title', 'goal', 'verification', 'block', 'requires')), step['id'] + ': empty field')
        if step['status'] == 'concluida':
            require(step.get('evidence') and step.get('commit'), step['id'] + ': concluded without evidence and commit')
            for name in step['evidence']:
                require((ROOT / name).is_file(), step['id'] + ': missing evidence ' + name)
    for decision in data['decisions']:
        require(decision['status'] in STATUSES, decision['id'] + ': unknown status')
        require(decision['status'] != 'decidida' or decision.get('answer'), decision['id'] + ': decided without answer')
        require(not decision.get('step') or decision['step'] in ids, decision['id'] + ': unknown step')
    return {status: sum(s['status'] == status for s in data['steps']) for status in STATUSES}


def render(data, counts):
    lines = ['# Etapas pequenas do que falta', '',
             'Gerado de `progresso/etapas-pequenas.json` por `scripts/render_small_steps.py`. A ordem é a prioridade: '
             'o que não precisa da VM vem primeiro. Situação geral e avisos: [AVISOS-E-STATUS.md](AVISOS-E-STATUS.md).', '',
             f"Atualizado em {data['updated_at_local']}. "
             + ', '.join(f'{STATUSES[s]}: {n}' for s, n in counts.items() if n) + '.', '',
             '**Regras**', '', *['- ' + rule for rule in data['rules']], '',
             '| # | Etapa | Bloco | Precisa de | Situação |', '|---|---|---|---|---|']
    for step in data['steps']:
        lines.append(f"| {step['id']} | {step['title']} | {step['block']} | {step['requires']} | {STATUSES[step['status']]} |")
    lines += ['', '## Detalhes', '']
    for step in data['steps']:
        lines += [f"### {step['id']} — {step['title']}", '', f"**Objetivo:** {step['goal']}", '',
                  f"**Como verificar:** {step['verification']}", '', f"**Situação:** {STATUSES[step['status']]}."]
        if step.get('note'):
            lines += ['', step['note']]
        if step['status'] == 'concluida':
            lines += ['', 'Evidência: ' + ', '.join(f'[{n}](../{n})' for n in step['evidence']) + f". Commit `{step['commit']}`."]
        lines.append('')
    lines += ['## Decisões', '']
    for decision in data['decisions']:
        line = f"- **{decision['id']}** ({STATUSES[decision['status']]}): {decision['question']}"
        if decision.get('answer'):
            line += f" **Resposta:** {decision['answer']}" + (f" Etapa {decision['step']}." if decision.get('step') else '')
        lines.append(line)
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if the rendered page is stale')
    args = parser.parse_args()
    data = json.loads(SOURCE.read_text(encoding='utf-8'))
    counts = validate(data)
    page = render(data, counts)
    if args.check:
        require(PAGE.read_text(encoding='utf-8') == page, 'docs/ETAPAS-PEQUENAS.md is stale')
    else:
        PAGE.write_text(page, encoding='utf-8', newline='\n')
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
