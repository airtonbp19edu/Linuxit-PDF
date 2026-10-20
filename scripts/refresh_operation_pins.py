#!/usr/bin/env python3
"""Refresh code pins of progresso/inventario-operacoes-v1.json after source edits.

A pin whose cited symbol body is unchanged (it only moved, or other code in the
file changed) is refreshed automatically. A pin whose body changed is listed as
needing review and is only refreshed when named with --accept OPERATION_ID,
after confirming that the operation's contract text still describes the code.
Without --apply nothing is written.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'progresso' / 'inventario-operacoes-v1.json'


def locate(path, symbol):
    data = (ROOT / path).read_bytes();text = data.decode('utf-8');node = ast.parse(text)
    for part in symbol.split('.'):
        matches = [n for n in node.body if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name == part]
        if len(matches) != 1:
            return None
        node = matches[0]
    body = '\n'.join(text.splitlines()[node.lineno - 1:node.end_lineno])
    return dict(file_sha256=hashlib.sha256(data).hexdigest(), line=node.lineno, end_line=node.end_lineno,
                excerpt_sha256=hashlib.sha256(body.encode()).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--accept', action='append', default=[], help='Operation id whose changed excerpt was reviewed')
    parser.add_argument('--reviewed-at', help='ISO time with zone recorded as reviewed_at_local when applying')
    args = parser.parse_args()
    raw = CATALOG.read_text(encoding='utf-8');catalog = json.loads(raw)
    moved, changed, missing = [], [], []
    for operation in catalog['operations']:
        for source in operation['source_evidence']:
            current = locate(source['path'], source['symbol'])
            if current is None:
                missing.append((operation['id'], source['symbol']));continue
            if all(source[k] == current[k] for k in current):
                continue
            if current['excerpt_sha256'] == source['excerpt_sha256']:
                moved.append((operation['id'], source['symbol']));source.update(current)
            elif operation['id'] in args.accept:
                changed.append((operation['id'], source['symbol'], 'accepted'));source.update(current)
            else:
                changed.append((operation['id'], source['symbol'], 'needs_review'))
    pending = [c for c in changed if c[2] == 'needs_review']
    print(json.dumps({'moved_refreshed': moved, 'changed': changed, 'missing_symbols': missing}, ensure_ascii=False, indent=1))
    if args.apply:
        if missing or pending:
            raise SystemExit('Revise os trechos alterados (use --accept) ou os símbolos ausentes antes de aplicar.')
        if args.reviewed_at:
            catalog['reviewed_at_local'] = args.reviewed_at
        CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    return 1 if (missing or pending) and not args.apply else 0


if __name__ == '__main__':
    raise SystemExit(main())
