"""Tier 0 screen: checks that cost nothing. No model calls.

Usage: python3 -I screen0.py <papers_dir>   (reads <oid>/flat.tex, writes <oid>/screen0.json)

Checks:
 1. injection   - text aimed at AI reviewers ("ignore previous instructions", "give a positive review")
 2. residue     - chatbot residue ("as an AI language model", "regenerate response")
 3. todo        - TODO / FIXME / XXX / ?? placeholders left in the source
 4. statcheck   - recompute p from t(df)=x, F(d1,d2)=x, chi2(df)=x, z=x and compare with the reported p
 5. abstract    - numbers in the abstract that never appear in the body (a weak lead, many false hits)
 6. percent     - "a of b (c%)" style statements where c != 100*a/b beyond rounding
Every hit is a LEAD for a human or a model, never a finding.
"""
import json, math, os, re, sys

# ---------- p-values without scipy (regularised incomplete beta, Numerical Recipes style) ----------
def _betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-30 else 1e-30); h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-30 else 1e-30)
        c = 1 + aa / c if abs(c) > 1e-30 else 1e30
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-30 else 1e-30)
        c = 1 + aa / c if abs(c) > 1e-30 else 1e30
        de = d * c; h *= de
        if abs(de - 1) < 1e-12:
            break
    return h

def betai(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lb = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lb) * _betacf(a, b, x) / a
    return 1 - math.exp(lb) * _betacf(b, a, 1 - x) / b

def gammq(a, x):  # upper regularised gamma, for chi2
    if x <= 0: return 1.0
    if x < a + 1:
        s, t, n = 1 / a, 1 / a, a
        for _ in range(500):
            n += 1; t *= x / n; s += t
            if abs(t) < abs(s) * 1e-12: break
        return 1 - s * math.exp(-x + a * math.log(x) - math.lgamma(a))
    b, c, d = x + 1 - a, 1e30, 1 / (x + 1 - a); h = d
    for i in range(1, 500):
        an = -i * (i - a); b += 2
        d = an * d + b; d = 1 / (d if abs(d) > 1e-30 else 1e-30)
        c = b + an / c if abs(c) > 1e-30 else 1e30
        de = d * c; h *= de
        if abs(de - 1) < 1e-12: break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h

def p_value(test, df1, df2, x):
    if test == "t":  return betai(df1 / 2, 0.5, df1 / (df1 + x * x))          # two-tailed
    if test == "F":  return betai(df2 / 2, df1 / 2, df2 / (df2 + df1 * x))
    if test == "chi2": return gammq(df1 / 2, x / 2)
    if test == "z":  return math.erfc(abs(x) / math.sqrt(2))                   # two-tailed
    raise ValueError(test)

NUM = r"(-?\d+(?:\.\d+)?)"
STAT = [
    ("t",    re.compile(r"\bt\s*\(\s*(\d+(?:\.\d+)?)\s*\)\s*=\s*" + NUM + r"[^.;]{0,40}?p\s*([<=>])\s*" + r"(\.\d+|\d\.\d+)")),
    ("F",    re.compile(r"\bF\s*\(\s*(\d+)\s*,\s*(\d+(?:\.\d+)?)\s*\)\s*=\s*" + NUM + r"[^.;]{0,40}?p\s*([<=>])\s*(\.\d+|\d\.\d+)")),
    ("chi2", re.compile(r"(?:\\chi\^?\{?2\}?|chi2|χ2|χ²)\s*\(\s*(\d+)\s*\)\s*=\s*" + NUM + r"[^.;]{0,40}?p\s*([<=>])\s*(\.\d+|\d\.\d+)")),
    ("z",    re.compile(r"\bz\s*=\s*" + NUM + r"\s*,\s*p\s*([<=>])\s*(\.\d+|\d\.\d+)")),
]

def statcheck(text):
    out = []
    for test, rx in STAT:
        for m in rx.finditer(text):
            g = m.groups()
            if test == "t":   df1, df2, x, op, p = float(g[0]), None, float(g[1]), g[2], float(g[3])
            elif test == "F": df1, df2, x, op, p = float(g[0]), float(g[1]), float(g[2]), g[3], float(g[4])
            elif test == "chi2": df1, df2, x, op, p = float(g[0]), None, float(g[1]), g[2], float(g[3])
            else:             df1, df2, x, op, p = None, None, float(g[0]), g[1], float(g[2])
            # Rounding interval of the reported statistic (statcheck rule): x +/- half a unit in its last digit.
            dec = len(g[1 if test in ("t", "chi2") else (2 if test == "F" else 0)].split(".")[1]) if "." in m.group(0) else 0
            half = 0.5 * 10 ** (-dec) if dec else 0.5
            lo, hi = sorted([p_value(test, df1, df2, abs(x) + half), p_value(test, df1, df2, max(abs(x) - half, 0))])
            ok = (op == "=" and lo - 0.0005 <= p <= hi + 0.0005) or (op == "<" and lo < p) or (op == ">" and hi > p)
            gross = (op in "=<" and p < 0.05 and lo >= 0.05) or (op in "=>" and p >= 0.05 and hi < 0.05)
            if not ok:
                out.append({"quote": m.group(0)[:200], "recomputed_p_range": [round(lo, 4), round(hi, 4)],
                            "gross": gross})
    return out

INJECT = re.compile(r"ignore (all )?(previous|prior) instructions|give (a )?positive review|"
                    r"do not highlight any negatives|as a language model reviewer", re.I)
RESIDUE = re.compile(r"as an ai language model|regenerate response|as of my last knowledge update|"
                     r"certainly! here is|i hope this helps", re.I)
TODO = re.compile(r"\b(TODO|FIXME|XXX)\b|\?\?\?")
PCT = re.compile(r"(\d[\d,]*)\s+(?:of|out of)\s+(\d[\d,]*)\s*\(\s*(\d+(?:\.\d+)?)\s*\\?%")

def abstract_numbers(text):
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S) or \
        re.search(r"\\abstract\{(.*?)\}\s*\n", text, re.S)
    if not m: return []
    ab = m.group(1)
    body = text[m.end():]
    nums = set(re.findall(r"(?<![\w.^_{])(\d+\.\d+|\d{2,})(?![\w.])", ab))
    return sorted(n for n in nums if n not in body and not re.fullmatch(r"(19|20)\d\d", n))

def percent_check(text):
    bad = []
    for m in PCT.finditer(text):
        a, b, c = (float(s.replace(",", "")) for s in m.groups())
        if b > 0 and a <= b:
            dec = len(m.group(3).split(".")[1]) if "." in m.group(3) else 0
            if abs(100 * a / b - c) > 0.5 * 10 ** (-dec) + 1e-9:
                bad.append({"quote": m.group(0), "implied_pct": round(100 * a / b, 3)})
    return bad

def screen(text):
    return {
        "chars": len(text),
        "injection": [m.group(0) for m in INJECT.finditer(text)],
        "residue": [m.group(0) for m in RESIDUE.finditer(text)],
        "todo": len(TODO.findall(text)),
        "statcheck": statcheck(text),
        "abstract_numbers_not_in_body": abstract_numbers(text),
        "percent": percent_check(text),
    }

if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        # Known values: t(28)=2.20 -> p~0.036; F(1,30)=4.17 -> p~0.050; chi2(1)=3.84 -> p~0.050; z=1.96 -> p~0.050
        for args, want in [(("t", 28, None, 2.20), 0.036), (("F", 1, 30, 4.17), 0.050),
                           (("chi2", 1, None, 3.84), 0.050), (("z", None, None, 1.96), 0.050)]:
            got = p_value(*args); print(args, round(got, 4), "ok" if abs(got - want) < 0.002 else "FAIL")
        demo = "We found t(28) = 2.20, p < .01 and F(1, 30) = 4.17, p = .05. Of 40 cells, 12 of 40 (35%) died."
        print(json.dumps(screen(demo), indent=1))
        sys.exit()
    root = sys.argv[1]
    for oid in sorted(os.listdir(root)):
        f = os.path.join(root, oid, "flat.tex")
        if os.path.isfile(f):
            r = screen(open(f, encoding="utf-8", errors="replace").read())
            json.dump(r, open(os.path.join(root, oid, "screen0.json"), "w"), indent=1)
            print(oid, json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in r.items()}))
