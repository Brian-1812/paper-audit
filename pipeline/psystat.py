"""Deterministic statcheck for APA-style results in psychology papers (a deterministic baseline). No model calls.

Usage:
  python3 -I psystat.py <data_dir> [<out.json>]     check every <data_dir>/papers/<oid>/paper.txt
  python3 -I psystat.py --selftest

For each reported test (t, F, r, chi2, z with its df) followed by a p-value, the program recomputes p from
the statistic and compares it with the reported p, as statcheck (Nuijten et al.) does:
  - The statistic is rounded in the paper, so p is recomputed at both ends of its rounding interval.
  - A reported "p = .03" stands for any p in [.025, .035). "p < .05" needs a computed p below .05.
  - inconsistent: no value in the rounding interval of the statistic gives the reported p.
  - gross (decision error): the reported p and the recomputed p fall on different sides of .05.
  - one_tailed_ok: the test is inconsistent as two-tailed, but half the p fits, and the same sentence says
    "one-tailed", "one-sided" or "directional". statcheck counts these as consistent; so do we.
Every hit is a lead. A model judge and a code check decide if it is a real error.
"""
import json, math, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from screen0 import p_value  # noqa: E402  (pure-math p-values, no scipy)

NUM = r"(-?\d*\.?\d+)"
P = r"[,;]?\s*(?:\w{0,3}\s*)?p\s*(?:-?value)?\s*([<=>≤≥])\s*(0?\.\d+|1(?:\.0+)?|0)(?![\d.])"
STAT = [
    ("t", re.compile(r"\bt\s*\(\s*(\d+(?:\.\d+)?)\s*\)\s*=\s*" + NUM + r"\s*" + P)),
    ("F", re.compile(r"\bF\s*\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*\)\s*=\s*" + NUM + r"\s*" + P)),
    ("r", re.compile(r"\br\s*\(\s*(\d+)\s*\)\s*=\s*" + NUM + r"\s*" + P)),
    ("chi2", re.compile(r"(?:χ|\\chi|chi|X)\s*\^?\{?(?:2|²)\}?\s*\(\s*(\d+)\s*(?:,\s*[Nn]\s*=\s*\d[\d,]*)?\s*\)\s*=\s*"
                        + NUM + r"\s*" + P)),
    ("z", re.compile(r"\b[zZ]\s*=\s*" + NUM + r"\s*" + P)),
]
ONE_TAILED = re.compile(r"one[- ]tailed|one[- ]sided|directional", re.I)


def normalize(text):
    for a, b in (("−", "-"), ("–", "-"), (" ", " "), (" ", " "), (" ", " "),
                 ("&lt;", "<"), ("&gt;", ">"), ("≤", "<"), ("≥", ">"), (" ", " ")):
        text = text.replace(a, b)
    return text


def decimals(s):
    return len(s.split(".")[1]) if "." in s else 0


def p_from(test, d1, d2, x):
    if test == "r":
        if abs(x) >= 1:
            return None
        t = abs(x) * math.sqrt(d1 / (1 - x * x)) if x * x < 1 else float("inf")
        return p_value("t", d1, None, t)
    return p_value(test, d1, d2, abs(x))


def check_one(test, d1, d2, xs, op, ps):
    """Return a dict with the computed p range and the verdict for one reported test."""
    x, dx = float(xs), decimals(xs)
    half = 0.5 * 10 ** (-dx) if dx else 0.5
    ends = [p_from(test, d1, d2, abs(x) + half), p_from(test, d1, d2, max(abs(x) - half, 0.0))]
    if None in ends:
        return None
    lo, hi = min(ends), max(ends)
    p, dp = float(ps), decimals(ps)
    ph = 0.5 * 10 ** (-dp) if dp else 0.5
    if op == "=":
        ok = lo <= p + ph and hi >= p - ph
        if p == 0:
            ok = hi < ph  # "p = .000" stands for p < .0005
    elif op == "<":
        ok = lo < p
    else:
        ok = hi > p
    sig_rep = (op == "<" and p <= 0.05) or (op == "=" and p < 0.05)
    nonsig_rep = (op == ">" and p >= 0.05) or (op == "=" and p >= 0.05)
    gross = (sig_rep and lo >= 0.05) or (nonsig_rep and hi < 0.05)
    one_ok = False
    if not ok and op == "=":
        one_ok = lo / 2 <= p + ph and hi / 2 >= p - ph
    elif not ok and op == "<":
        one_ok = lo / 2 < p
    # material: off by more than a factor 1.25 from the nearest recomputed p (or a decision error), so it is not a
    # rounding-convention quarrel such as p = .006 for a recomputed .0065.
    if op == "=" and p > 0:
        ratio = max(p / hi if hi > 0 else 99.0, lo / p)
    elif op == "<":
        ratio = lo / p if p > 0 else 99.0
    else:
        ratio = p / hi if hi > 0 else 99.0
    material = (not ok) and (gross or ratio > 1.25 or p == 0)
    return {"p_lo": lo, "p_hi": hi, "consistent": ok, "gross": (not ok) and gross, "one_tailed_fits": one_ok,
            "material": material, "ratio": ratio}


def statcheck(text):
    text = normalize(text)
    out = []
    for test, rx in STAT:
        for m in rx.finditer(text):
            g = m.groups()
            if test == "F":
                d1, d2, xs, op, ps = float(g[0]), float(g[1]), g[2], g[3], g[4]
            elif test == "z":
                d1, d2, xs, op, ps = None, None, g[0], g[1], g[2]
            else:
                d1, d2, xs, op, ps = float(g[0]), None, g[1], g[2], g[3]
            op = {"≤": "<", "≥": ">"}.get(op, op)
            if test != "z" and d1 <= 0:
                continue
            r = check_one(test, d1, d2, xs, op, ps)
            if r is None:
                continue
            s0 = max(text.rfind(". ", 0, m.start()), m.start() - 400, 0)
            s1 = text.find(". ", m.end())
            sent = text[s0:(s1 if 0 <= s1 < m.end() + 400 else m.end() + 400)]
            one_tailed = bool(ONE_TAILED.search(sent)) and r["one_tailed_fits"]
            out.append({"test": test, "df1": d1, "df2": d2, "stat": xs, "op": op, "p": ps, "pos": m.start(),
                        "quote": m.group(0)[:200], **{k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()},
                        "one_tailed_in_text": one_tailed,
                        "error": (not r["consistent"]) and not one_tailed})
            out[-1]["material"] = out[-1]["error"] and r["material"]
    out.sort(key=lambda h: h["pos"])
    return out


def selftest():
    cases = [("t(28) = 2.20, p = .036", False), ("t(28) = 2.20, p = .36", True), ("F(1, 45) = 4.20, p = .046", False),
             ("F(2, 60) = 1.10, p < .05", True), ("r(48) = .32, p = .023", False), ("χ2(1, N = 100) = 3.20, p = .07", False),
             ("z = 1.96, p = .05", False), ("t(30) = 1.70, p = .05, one-tailed", False), ("t(40) = −2.10, p = .042", False)]
    bad = 0
    for s, want_err in cases:
        h = statcheck(s)
        got = h[0]["error"] if h else None
        if got is None or got != want_err:
            bad += 1
            print("FAIL", s, h)
    print(f"selftest: {len(cases) - bad}/{len(cases)} pass")
    return bad == 0


def main():
    if sys.argv[1] == "--selftest":
        sys.exit(0 if selftest() else 1)
    data = sys.argv[1]
    res = {}
    for oid in sorted(os.listdir(os.path.join(data, "papers"))):
        f = os.path.join(data, "papers", oid, "paper.txt")
        if os.path.isfile(f):
            res[oid] = statcheck(open(f, encoding="utf-8").read())
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(data, "psystat.json")
    json.dump(res, open(out, "w"), indent=1)
    n = sum(len(v) for v in res.values())
    e = sum(h["error"] for v in res.values() for h in v)
    g = sum(h["error"] and h["gross"] for v in res.values() for h in v)
    pe = sum(any(h["error"] for h in v) for v in res.values())
    mat = sum(h["material"] for v in res.values() for h in v)
    print(f"material (beyond rounding, ratio > 1.25 or decision error): {mat}")
    print(f"papers {len(res)}, tests {n}, inconsistent {e}, gross {g}, papers with >=1 inconsistency {pe}")


if __name__ == "__main__":
    main()
