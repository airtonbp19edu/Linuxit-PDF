#!/usr/bin/env python3
"""Render the validated provisional inventory without approving full operations."""
import argparse
import json
from pathlib import Path

from check_operation_catalog import ROOT, validate


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def render(catalog):
    validate(catalog)
    operation_count = len(catalog['operations'])
    family_count = len(catalog['families'])
    current = catalog.get('current_own_test_evidence_ref')
    lines = ['# Inventário operacional provisório — P01', '',
        f"Revisão {catalog['revision']}, conferida em {catalog['reviewed_at_local']}. "
        f'**{operation_count} recortes conhecidos em {family_count} famílias; inventário global aberto.**', '',
        'Fonte: [catálogo estruturado](../progresso/inventario-operacoes-v1.json). '
        '[Execução dos lotes](LOTES-FUNCIONALIDADES.md).', '',
        '**Não é percentual de reconstrução.** Código delimitado, testes próprios, '
        'observações parciais do original e aceitação integral são estados distintos. '
        'Nenhuma família integral foi aprovada; todos os 50 planos completos S12 permanecem abertos.', '']
    if current:
        evidence = json.loads((ROOT / current).read_text(encoding='utf-8'))
        lines += [f"Evidência própria atual: **{evidence['source_suite_passed']} testes Linux aprovados**, "
            f"[casos e hashes](../{current}). A evidência informa separadamente os ambientes executados. "
            'Os403 testes/106 arquivos da revisão inicial são evidência histórica, sem aprovação integral das operações.', '']
    lines += ['## Estado por família', '',
        'Zero na coluna de pendências significa somente que os recortes listados têm código. '
        'Não encerra a família, seu inventário global ou suas lacunas.', '',
        '| Família | Recortes | Código delimitado | Pendentes | Adiados |',
        '|---|---:|---:|---:|---:|']
    for family in catalog['families']:
        operations = [o for o in catalog['operations'] if o['family_id'] == family['id']]
        counts = {state: sum(o['implementation_state'] == state for o in operations) for state in
                  ('bounded_source_present', 'pending_or_target_characterization', 'deferred_by_user')}
        lines.append(f"|{cell(family['name'])}|{len(operations)}|{counts['bounded_source_present']}|"
                     f"{counts['pending_or_target_characterization']}|{counts['deferred_by_user']}|")
    states = catalog['summary']['implementation_states']
    lines += [f"|Total|{operation_count}|{states['bounded_source_present']}|{states['pending_or_target_characterization']}|{states['deferred_by_user']}|"]
    for family in catalog['families']:
        lines += ['', '## ' + family['name'], '', family['original_recorded_subset_summary'], '',
            '**Lacunas da família:** ' + family['open_questions'], '',
            '| Operação | Estado do código | Aceitação e limites do recorte |', '|---|---|---|']
        for op in (o for o in catalog['operations'] if o['family_id'] == family['id']):
            status = {'bounded_source_present': 'Código em subconjunto',
                'pending_or_target_characterization': 'Pendente/caracterizar',
                'deferred_by_user': 'Adiado pelo usuário'}[op['implementation_state']]
            if op['source_evidence']:
                source = op['source_evidence'][0]
                status += f" ([fonte](../{source['path']}#L{source['line']}))"
            lines.append(f"|`{op['id']}` — {cell(op['title'])}|{status}|{cell(op['output_and_acceptance'])}|")
    lines += ['', '## Limites da medição', '',
        'As contagens não têm pesos de complexidade e o denominador completo é desconhecido. '
        'Recortes e testes relacionados não aprovam operações inteiras. '
        'Nuvem direta permanece adiada; IA generativa está excluída. '
        'A VM continua suspensa no checkpoint documentado em RETOMADA.md.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check-render', type=Path)
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'progresso/inventario-operacoes-v1.json').read_text(encoding='utf-8'))
    document = render(catalog)
    if args.check_render and args.check_render.read_text(encoding='utf-8') != document:
        raise ValueError('Rendered operational inventory is stale')
    if args.output:
        args.output.write_bytes(document.encode('utf-8'))
    print(json.dumps({'revision': catalog['revision'], 'operations': len(catalog['operations']),
                      'full_family_acceptance': False, 'original_executed': False}))


if __name__ == '__main__':
    main()
