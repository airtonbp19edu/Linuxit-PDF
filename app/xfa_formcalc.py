"""Small numeric FormCalc subset for field calculate scripts, without eval.

Arithmetic, sibling field references and Sum/Avg/Min/Max/Count/Round/Abs only.
No assignments, loops, attributes, external calls or general FormCalc VM.
"""
import ast
from decimal import Decimal, InvalidOperation, localcontext

from pdf_xfa import XFAError, _require

FUNCTIONS = {'sum', 'avg', 'min', 'max', 'count', 'round', 'abs'}


def expression(source):
    _require(isinstance(source, str) and 0 < len(source.strip()) <= 2048, 'Expressão FormCalc vazia ou acima do limite.')
    try:
        tree = ast.parse(source.strip().replace('^', '**'), mode='eval')
    except (SyntaxError, ValueError, RecursionError):
        raise XFAError('Sintaxe fora do subconjunto FormCalc numérico.') from None
    nodes = list(ast.walk(tree))
    _require(len(nodes) <= 256, 'Expressão FormCalc acima de 256 nós.')
    dependencies = set()
    def check(node, depth=0):
        _require(depth <= 32, 'Expressão FormCalc acima de 32 níveis.')
        if isinstance(node, ast.Constant):
            _require(type(node.value) in (int, float), 'FormCalc aceita somente constantes numéricas.')
        elif isinstance(node, ast.Name):
            dependencies.add(node.id)
        elif isinstance(node, ast.BinOp):
            _require(type(node.op) in (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow), 'Operador FormCalc não suportado.')
            check(node.left, depth+1);check(node.right, depth+1)
        elif isinstance(node, ast.UnaryOp):
            _require(type(node.op) in (ast.UAdd, ast.USub), 'Operador FormCalc não suportado.')
            check(node.operand, depth+1)
        elif isinstance(node, ast.Call):
            _require(isinstance(node.func, ast.Name) and node.func.id.lower() in FUNCTIONS
                     and not node.keywords and 1 <= len(node.args) <= 64, 'Função FormCalc não suportada.')
            for arg in node.args:check(arg, depth+1)
        else:
            raise XFAError('Expressão fora do subconjunto FormCalc numérico.')
    check(tree.body)
    return tree.body, dependencies


def _numeric(value):
    try:
        result = Decimal(str(value).strip() or '0')
    except (InvalidOperation, ValueError):
        raise XFAError('Campo FormCalc não contém número decimal.') from None
    _require(result.is_finite() and abs(result) <= Decimal('1e18'), 'Número FormCalc não finito ou acima do limite.')
    return result


def _evaluate(node, resolve):
    def visit(item):
        if isinstance(item, ast.Constant):result = _numeric(item.value)
        elif isinstance(item, ast.Name):result = _numeric(resolve(item.id))
        elif isinstance(item, ast.UnaryOp):
            value = visit(item.operand);result = -value if isinstance(item.op, ast.USub) else value
        elif isinstance(item, ast.BinOp):
            a, b = visit(item.left), visit(item.right)
            if isinstance(item.op, ast.Add):result = a+b
            elif isinstance(item.op, ast.Sub):result = a-b
            elif isinstance(item.op, ast.Mult):result = a*b
            elif isinstance(item.op, ast.Div):result = a/b
            else:
                _require(b == b.to_integral_value() and abs(b) <= 10, 'Expoente FormCalc fora do limite inteiro ±10.')
                result = a**int(b)
        else:
            name = item.func.id.lower();args = [visit(arg) for arg in item.args]
            if name == 'sum':result = sum(args, Decimal(0))
            elif name == 'avg':result = sum(args, Decimal(0))/len(args)
            elif name == 'min':result = min(args)
            elif name == 'max':result = max(args)
            elif name == 'count':result = Decimal(len(args))
            elif name == 'abs':
                _require(len(args) == 1, 'Abs exige um argumento.');result = abs(args[0])
            else:
                _require(len(args) in (1, 2), 'Round exige um ou dois argumentos.')
                precision = args[1] if len(args) == 2 else Decimal(0)
                _require(precision == precision.to_integral_value() and 0 <= precision <= 10, 'Precisão Round fora do limite.')
                from decimal import ROUND_HALF_UP
                result = args[0].quantize(Decimal(1).scaleb(-int(precision)), rounding=ROUND_HALF_UP)
        return _numeric(result)
    try:
        with localcontext() as ctx:
            ctx.prec = 32
            return visit(node)
    except (ArithmeticError, ValueError, RecursionError) as exc:
        if isinstance(exc, XFAError):raise
        raise XFAError('Cálculo FormCalc inválido, divisão por zero ou acima do limite.') from exc


def calculate(rows):
    fields = {r['path']:r for r in rows if r['kind'] == 'field'}
    scripts = {path:expression(row['calculate']) for path, row in fields.items() if row.get('calculate') is not None}
    _require(len(scripts) <= 128, 'Acima de 128 cálculos FormCalc.')
    done, active = set(), set()
    def run(path):
        if path in done:return fields[path]['value']
        _require(path not in active and len(active) < 64, 'Ciclo ou dependência FormCalc acima de 64 níveis.')
        if path not in scripts:return fields[path]['value']
        active.add(path)
        parent = path.rsplit('.', 1)[0]+'.' if '.' in path else ''
        tree, names = scripts[path]
        def resolve(name):
            target = parent+name+'[0]'
            _require(target in fields, 'Referência FormCalc de campo irmão ausente: '+name)
            # Repeated fields require an explicit SOM resolver, outside this subset.
            _require(parent+name+'[1]' not in fields, 'Referência FormCalc a campo repetido é ambígua.')
            return run(target)
        value = _evaluate(tree, resolve)
        text = format(value, 'f')
        if '.' in text:text = text.rstrip('0').rstrip('.')
        fields[path]['value'] = '0' if value == 0 else text
        active.remove(path);done.add(path)
        return fields[path]['value']
    for path in scripts:run(path)
    return len(scripts)
