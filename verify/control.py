"""Control: location pointers to random statistical passages that no register finding cites.

  python3 -I verify/control.py <sample.json> <register_dir> <data_dir> <out_dir> [--seed 399] [--n 20]
Picks n papers from the sample's papers (seeded), then one random prose sentence with a test statistic or p value
per paper. A sentence is excluded if it shares a 25-character window with any quote of any register record
(findings.jsonl and unconfirmed.jsonl) of that paper. Location = the nearest preceding markdown heading.
Writes <out>/controls.jsonl (register-like records) and <out>/control-sample.json (strict.py input).
"""
import json, os, random, re, sys

sample_f, reg_dir, data, out = sys.argv[1:5]
seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 399
n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 20
STAT = re.compile(r"(\bp\s*[<=>≤]\s*0?\.\d|\b[Ft]\s*\(\s*\d|χ2\s*[=(]|\bF\s*=\s*\d|\bt\s*=\s*-?\d|\br\s*=\s*-?0?\.\d)")
norm = lambda s: re.sub(r"\s+", " ", s or "").strip().lower()

sample = json.load(open(sample_f))["sample"]
oid_of = {}
quotes = {}
for fn in ("findings.jsonl", "unconfirmed.jsonl"):
    for line in open(os.path.join(reg_dir, fn)):
        r = json.loads(line)
        quotes.setdefault(r["oid"], []).append(norm(r.get("quote")))
for s in sample:
    oid_of[s["fid"]] = s["fid"].split("-")[1]
oids = sorted(set(oid_of.values()))
rng = random.Random(f"{seed}:control")
pick = sorted(rng.sample(oids, n))
recs = []
for oid in pick:
    text = open(os.path.join(data, "papers", oid, "paper.txt"), encoding="utf-8").read()
    heading, cands = "", []
    for line in text.splitlines():
        if line.startswith("#"):
            heading = line.lstrip("#").strip(); continue
        if "|" in line or len(line) < 40 or heading.lower() in ("abstract", "references"):
            continue
        for sent in re.split(r"(?<=[.;])\s+(?=[A-Z(])", line):
            if not STAT.search(sent) or len(sent) < 40:
                continue
            ns = norm(sent)
            if any(q and any(ns[i:i + 25] in q for i in range(0, max(1, len(ns) - 24), 5)) for q in quotes.get(oid, [])):
                continue
            if any(q and len(q) >= 25 and q[:25] in ns for q in quotes.get(oid, [])):
                continue
            cands.append((heading, sent.strip()))
    if not cands:
        continue
    h, sent = random.Random(f"{seed}:{oid}").choice(cands)
    recs.append({"fid": f"CTRL-{oid}", "oid": oid, "location": h or "(no heading)", "quote": sent, "field": "control"})
os.makedirs(out, exist_ok=True)
with open(os.path.join(out, "controls.jsonl"), "w") as f:
    for r in recs:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
json.dump({"seed": seed, "sample": [{"fid": r["fid"], "field": "control"} for r in recs]},
          open(os.path.join(out, "control-sample.json"), "w"), indent=1)
print(len(recs), "controls")
for r in recs:
    print(r["fid"], "|", r["location"], "|", r["quote"][:160])
