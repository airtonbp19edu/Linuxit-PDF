#!/usr/bin/env python3
"""Cross-check selected UI routes and declared states; never execute the original."""
import argparse
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/windows-evidence/foxit-rea'
SOURCE = '90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6'
SELECTED = [
    (88, 57601, '0x803920'), (88, 57607, '0x861470'),
    (88, 1289, '0x85d1a0'), (88, 1360, '0x85ddd0'),
    (88, 1362, '0x85de30'), (645, 1275, '0x80eab0'),
    (6359, 7913, '0x1788db0'), (6359, 7911, '0x1788db0'),
    (6359, 8036, '0x1788e10'), (6359, 7921, '0x1788d70'),
]


def catalog(target, metadata_path):
    raw = target.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE:
        raise ValueError('Target identity differs from the preserved reference')
    metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
    if metadata['source_sha256'] != SOURCE:
        raise ValueError('Decompilation metadata has a different source identity')
    functions = {entry['entry_va'].lower(): entry for entry in metadata['entries']}
    ui = json.loads((EVIDENCE / 'ui-command-map.json').read_text(encoding='utf-8'))
    if ui['target_sha256'] != SOURCE:
        raise ValueError('UI metadata has a different source identity')
    routes = []
    for resource, control, handler in SELECTED:
        matches = [(item, route) for item in ui['items']
                   if item['resource_id'] == resource and item['id'] == control
                   for route in item.get('candidate_routes', [])
                   if route['handler_va'].lower() == handler]
        if len(matches) != 1:
            raise ValueError(f'Expected one selected contextual route: {resource}/{control}/{handler}')
        item, route = matches[0]
        offset = int(route['map_file_offset'], 16)
        message, code, first, last, signature, pointer = struct.unpack_from('<6I', raw, offset)
        if not (message == 0x111 and code == int(route['notification'], 16)
                and first <= control <= last and pointer == int(handler, 16)):
            raise ValueError('Message-map bytes disagree with the retained UI inventory')
        function = functions[handler]
        if not function.get('decompile_completed'):
            raise ValueError('Selected function has no completed decompilation')
        routes.append({'source': item['source'], 'resource_id': resource,
                       'language': item['language'], 'control_id': control,
                       'label': item['label'], 'handler_va': handler,
                       'map_file_offset': route['map_file_offset'],
                       'message': '0x111', 'notification': hex(code),
                       'id_range': [first, last], 'signature_enum': signature,
                       'table_bytes_verified': True,
                       'decompilation_result': function['result'],
                       'decompilation_sha256': function['result_sha256'],
                       'registration_class_verified': False,
                       'runtime_availability_observed': False,
                       'status': 'structural route and function body examined; runtime/class join pending'})
    fx = json.loads((EVIDENCE / 'selected-fx-ui-controls.json').read_text(encoding='utf-8'))
    declared = []
    keys = {'enabled', 'visible', 'checked', 'checkable', 'default', 'autoDefault', 'shortcut', 'focusPolicy'}
    for file in fx['files']:
        widgets = file.get('widgets', [])
        names = {widget['name'] for widget in widgets}
        states = [{'name': w['name'], 'class': w['class'],
                   'declarations': {k: v for k, v in w.get('properties', {}).items() if k in keys}}
                  for w in widgets if keys.intersection(w.get('properties', {}))]
        connections = [{k: c[k] for k in ('sender', 'signal', 'receiver', 'slot')}
                       for c in file.get('connections', [])]
        for connection in connections:
            connection['endpoints_present_in_metadata'] = (
                connection['sender'] in names and connection['receiver'] in names)
        declared.append({'path': file['path'], 'source_sha256': file['source_sha256'],
                         'widgets_in_existing_metadata': len(widgets),
                         'explicit_states': states, 'declared_connections': connections,
                         'runtime_instantiation_observed': False})
    return {'schema': 'linuxit-ui-availability-static-v1', 'source_sha256': SOURCE,
            'decompilation_metadata': metadata_path.name,
            'selected_contextual_routes': routes,
            'distinct_handlers': len({r['handler_va'] for r in routes}),
            'retained_fx_declarations': declared,
            'original_executed': False, 'dynamic_interactions_observed': 0,
            'limitations': [
                'Identical control IDs in different dialogs/classes do not prove identical behavior.',
                'Message-map bytes and examined function bodies do not identify the active runtime class.',
                'Template enabled/checked/focus declarations may be changed by code or feature availability.',
                'Connections and control existence do not prove that a dialog is reachable in Reader.',
                'This static inventory does not complete the stage-11 runtime interaction criterion.',
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--decompilation-metadata', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Use a new output file to preserve previous evidence')
    result = catalog(args.target, args.decompilation_metadata)
    with args.output.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'contextual_routes': len(result['selected_contextual_routes']),
                      'distinct_handlers': result['distinct_handlers'],
                      'fx_metadata_files': len(result['retained_fx_declarations']),
                      'dynamic_interactions_observed': 0}))


if __name__ == '__main__':
    main()
