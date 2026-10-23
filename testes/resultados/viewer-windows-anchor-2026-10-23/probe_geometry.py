"""Exercise actual presentation geometry methods without claiming GTK validation."""
import ast
import json
from pathlib import Path
from types import SimpleNamespace

root = Path(__file__).resolve().parents[3]
source = root / 'app/presentation.py'
tree = ast.parse(source.read_text(encoding='utf-8-sig'))
original = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'PresentationWindow')
names = {'_size_allocate', '_pan_bounds', '_clamp_target_pan', '_set_pan_target'}
body = [node for node in original.body if isinstance(node, ast.FunctionDef) and node.name in names]
module = ast.Module(body=[ast.ClassDef(name='Geometry', bases=[], keywords=[], body=body, decorator_list=[])], type_ignores=[])
ast.fix_missing_locations(module)
namespace = {'GLib': SimpleNamespace(timeout_add=lambda *args: 1, source_remove=lambda *args: None)}
exec(compile(module, str(source), 'exec'), namespace)
Geometry = namespace['Geometry']

def make(height=1400, anchored=True, pan=0):
    view = Geometry()
    alloc = SimpleNamespace(width=800, height=height)
    view.canvas = SimpleNamespace(get_allocation=lambda: alloc, queue_draw=lambda: None)
    view.pixbuf = SimpleNamespace(get_width=lambda: 400, get_height=lambda: 1262)
    view._controls_height = lambda: 0
    view._alloc_size = (800, height)
    view._resize_source = None
    view._top_anchor = anchored
    view.pan_x = view.target_pan_x = 0
    view.pan_y = view.target_pan_y = pan
    return view, alloc

cases = []
view, alloc = make()
alloc.height = 600
view._size_allocate(view.canvas, alloc)
cases.append({'case': 'reading page becomes taller than viewport', 'actual': view.pan_y, 'expected': 331.0})
view, alloc = make(height=600, pan=331)
view._controls_height = lambda: 80
view._size_allocate(view.canvas, alloc)
cases.append({'case': 'controls reveal without canvas size change', 'actual': view.pan_y, 'expected': 371.0})
view, alloc = make(height=600, anchored=False, pan=281)
alloc.height = 500
view._size_allocate(view.canvas, alloc)
cases.append({'case': 'manual panning stays at user position', 'actual': view.pan_y, 'expected': 281})
for case in cases:
    case['passed'] = case['actual'] == case['expected']
print(json.dumps({'scope': 'source methods with synthetic allocations; no GTK or native Windows execution', 'cases': cases}, indent=2))
raise SystemExit(0 if all(case['passed'] for case in cases) else 1)
