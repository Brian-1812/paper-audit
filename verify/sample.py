"""Step 1: draw the strict-verify sample BEFORE anyone reads the findings.

  python3 -I verify/sample.py <register>/findings.jsonl <out.json> [--seed 399] [--per-field 8]
Stratified: equal count per field, simple random sample (random.Random(seed).sample) inside each field,
from the fids sorted by name. Only fid, field and the input file hash go into the output.
"""
import hashlib, json, random, sys
from collections import defaultdict

src, out = sys.argv[1], sys.argv[2]
seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 399
per = int(sys.argv[sys.argv.index("--per-field") + 1]) if "--per-field" in sys.argv else 8
raw = open(src, "rb").read()
by = defaultdict(list)
for line in raw.decode().splitlines():
    r = json.loads(line)
    if r["tier"] == "A":
        by[r["field"]].append(r["fid"])
sample = []
for field in sorted(by):
    pick = random.Random(f"{seed}:{field}").sample(sorted(by[field]), per)
    sample += [{"fid": f, "field": field} for f in sorted(pick)]
json.dump({"seed": seed, "per_field": per, "source": src, "source_sha256": hashlib.sha256(raw).hexdigest(),
           "tier_A_per_field": {k: len(v) for k, v in sorted(by.items())}, "sample": sample}, open(out, "w"), indent=1)
print(json.dumps({k: len(v) for k, v in sorted(by.items())}), len(sample))
