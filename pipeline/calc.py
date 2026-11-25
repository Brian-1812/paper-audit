"""Safe calculator for the verifier model of the first pipeline (the skim-and-verify design). It is the only command that verifier may run.

Usage: python3 -I calc.py '<expression>' ['<expression>' ...]

It parses each expression with the Python ast module and evaluates only a white list:
numbers, + - * / // % **, comparisons, parentheses, lists and tuples, and the functions below.
It never calls eval() or exec(). It has no names for files, network or imports.

Functions:
  math: sqrt log log10 log2 exp sin cos tan asin acos atan pi e abs round min max sum
        floor ceil comb factorial fsum
  stats: mean(xs) sd(xs) (sample SD) se(xs)
         p_t(t, df)  p_F(F, d1, d2)  p_chi2(x, df)  p_z(z)   (two-tailed p for t and z)
         grim(mean, n, decimals) -> True if a mean of n integer scores can round to `mean`
         pct(a, b) -> 100*a/b
"""
import ast, math, operator, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from screen0 import p_value  # noqa: E402  (pure-math p-values, no scipy)


def mean(xs):
    return sum(xs) / len(xs)


def sd(xs):
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def se(xs):
    return sd(xs) / math.sqrt(len(xs))


def grim(m, n, decimals):
    """A mean of n integers is k/n. Check if some k/n rounds to m at `decimals` places."""
    k = round(m * n)
    return any(round(j / n, decimals) == round(m, decimals) for j in (k - 1, k, k + 1))


FUNCS = {
    "sqrt": math.sqrt, "log": math.log, "log10": math.log10, "log2": math.log2, "exp": math.exp,
    "sin": math.sin, "cos": math.cos, "tan": math.tan, "asin": math.asin, "acos": math.acos,
    "atan": math.atan, "abs": abs, "round": round, "min": min, "max": max, "sum": sum,
    "floor": math.floor, "ceil": math.ceil, "comb": math.comb, "factorial": math.factorial,
    "fsum": math.fsum, "mean": mean, "sd": sd, "se": se, "grim": grim,
    "pct": lambda a, b: 100.0 * a / b,
    "p_t": lambda t, df: p_value("t", df, None, abs(t)),
    "p_F": lambda F, d1, d2: p_value("F", d1, d2, F),
    "p_chi2": lambda x, df: p_value("chi2", df, None, x),
    "p_z": lambda z: p_value("z", None, None, z),
}
CONSTS = {"pi": math.pi, "e": math.e, "True": True, "False": False}
BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
       ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod, ast.Pow: operator.pow}
CMP = {ast.Lt: operator.lt, ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge,
       ast.Eq: operator.eq, ast.NotEq: operator.ne}


def ev(node):
    """Walk the parsed tree. No eval()/exec(): only the white-listed node types below run."""
    if isinstance(node, ast.Expression):
        return ev(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id in CONSTS:
        return CONSTS[node.id]
    if isinstance(node, (ast.List, ast.Tuple)):
        return [ev(x) for x in node.elts]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        v = ev(node.operand)
        return -v if isinstance(node.op, ast.USub) else v
    if isinstance(node, ast.BinOp) and type(node.op) in BIN:
        left, right = ev(node.left), ev(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise ValueError("exponent too large")
        return BIN[type(node.op)](left, right)
    if isinstance(node, ast.Compare) and len(node.ops) == 1 and type(node.ops[0]) in CMP:
        return CMP[type(node.ops[0])](ev(node.left), ev(node.comparators[0]))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in FUNCS \
            and not node.keywords:
        args = [ev(a) for a in node.args]
        if node.func.id in ("factorial", "comb") and any(abs(a) > 5000 for a in args):
            raise ValueError("argument too large")
        return FUNCS[node.func.id](*args)
    raise ValueError(f"not allowed: {ast.dump(node)[:80]}")


def calc(expr):
    if len(expr) > 2000:
        return "error: expression longer than 2000 characters"
    try:
        return repr(ev(ast.parse(expr, mode="eval")))
    except Exception as e:  # report the error to the model, never crash
        return f"error: {type(e).__name__}: {e}"


if __name__ == "__main__":
    lines = [f"{x} = {calc(x)}" for x in sys.argv[1:]]
    print("\n".join(lines))
    # Audit trail: the coordinator sets CALC_LOG, so the report can show that a calculation really ran.
    if os.environ.get("CALC_LOG"):
        with open(os.environ["CALC_LOG"], "a") as f:
            f.write("\n".join(lines) + "\n")
