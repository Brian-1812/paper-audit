"""Counts and binomial intervals for the strict verification.  python3 -I verify/analyze.py verify/verdicts.json verify/sample.json"""
import json, math, sys
from collections import Counter, defaultdict

V = json.load(open(sys.argv[1]))["verdicts"]
S = json.load(open(sys.argv[2]))
field = {s["fid"]: s["field"] for s in S["sample"]}
assert sorted(field) == sorted(v["fid"] for v in V), "verdicts must cover the sample exactly"


def binom_cdf(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


def solve(f, lo=0.0, hi=1.0):
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) else (lo, mid)
    return (lo + hi) / 2


def clopper(k, n, a=0.05):
    lo = 0.0 if k == 0 else solve(lambda p: 1 - binom_cdf(k - 1, n, p) < a / 2)
    hi = 1.0 if k == n else solve(lambda p: binom_cdf(k, n, p) > a / 2)
    return lo, hi


def wilson(k, n, z=1.959964):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def line(name, k, n):
    cl, ch = clopper(k, n); wl, wh = wilson(k, n)
    print(f"| {name} | {k}/{n} | {k/n:.1%} | {cl:.1%} - {ch:.1%} | {wl:.1%} - {wh:.1%} |")


c = Counter(v["verdict"] for v in V)
conf = [v for v in V if v["verdict"] == "CONFIRMED"]
print("counts:", dict(c))
print("| measure | k/n | estimate | 95% exact (Clopper-Pearson) | 95% Wilson |\n|---|---|---|---|---|")
line("confirmed / all sampled (unresolved = not confirmed)", len(conf), len(V))
line("confirmed / decided (unresolved left out)", len(conf), c["CONFIRMED"] + c["REJECTED"])
line("confirmed and material (real tier A)", sum(v["material"] for v in conf), len(V))
line("confirmed by recomputation only (code_kind = recompute)", sum(v["code_kind"] == "recompute" for v in conf), len(V))
pop = S["tier_A_per_field"]
by = defaultdict(lambda: [0, 0])
for v in V:
    by[field[v["fid"]]][1] += 1
    by[field[v["fid"]]][0] += v["verdict"] == "CONFIRMED"
w = sum(pop[f] * by[f][0] / by[f][1] for f in pop) / sum(pop.values())
print("\nper field (confirmed/sampled, tier-A population):", {f: f"{by[f][0]}/{by[f][1]} (pop {pop[f]})" for f in sorted(pop)})
print(f"population-weighted confirmed share: {w:.1%}")
print("rejection and unresolved reasons:", dict(Counter((v["verdict"], v["reason"]) for v in V if v["verdict"] != "CONFIRMED")))
print("code kind of confirmed:", dict(Counter(v["code_kind"] for v in conf)), "; not material:", [v["fid"] for v in conf if not v["material"]])
