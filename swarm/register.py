"""Build the findings register from the judged swarm batches. No model calls. Idempotent.

Usage: python3 -I swarm/register.py <data_dir> <run_dir> <register_dir> [<run tag, default R1>]
Input: <run_dir>/judge/pool-*.json (claims per batch) and <run_dir>/judge/judge/<oid>.json (+ .sbx.log).
A REAL finding =
  judge tier A or B, AND the judge says code_confirms, AND at least one of the judge's checks has an output that
  appears in the judge's own sandbox log of that call (a run with rc 0). The log check means that the model
  cannot only claim that code confirmed it: the output must be in the log.
One record per (paper, judge issue number). Claims of the same issue are merged; tier A wins over B.
Output (rebuilt every time, so a rerun gives the same file):
  <register_dir>/findings.jsonl     real findings (tier A and B)
  <register_dir>/unconfirmed.jsonl  judge A/B without a logged code confirmation (not counted as real)
  <register_dir>/register.md        short table
Every record has status "possible error, unverified by humans". The register stays local (data/ is git-ignored).
"""
import glob, json, os, re, sys, time
from collections import Counter

STATUS = "possible error, unverified by humans"


def nl(s):
    return re.sub(r"\s+", " ", s or "").strip()


NUM = re.compile(r"(?<![\w.])-?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")


def _nums(text):
    out = []
    for m in NUM.finditer(text or ""):
        t = m.group(0)
        try:
            out.append((t, float(t)))
        except ValueError:
            pass
    return out


def _match(tok, x, logvals):
    """A number the judge reports matches a logged number if it is that number rounded (or truncated) to the
    judge's digits, or within 1% for numbers in scientific notation."""
    if "e" in tok.lower():
        return any(abs(y - x) <= 0.01 * abs(x) + 1e-300 for y in logvals)
    d = len(tok.split(".")[1]) if "." in tok else 0
    tol = 0.5 * 10 ** -d + 1e-12
    return any(abs(y - x) <= tol or abs(abs(y) - abs(x)) <= tol for y in logvals)


def logged(check, log):
    """Provenance rule: the output that the judge reports must come from its own sandbox.
    Pass when the whole text is in one successful run (lines may be joined by '; ' or ' | '), or when every
    non-trivial number of the reported output (not a whole number below 1000) matches a number printed by one
    successful run, rounded to the reported digits. At least one non-trivial number is needed for the second path."""
    out = check.get("output") or ""
    runs = [l for l in log if l.get("rc") == 0]
    lines = [nl(x) for x in re.split(r"\n|; | \| ", out) if len(nl(x)) >= 3]
    if lines and any(all(x in nl(l.get("out")) for x in lines) for l in runs):
        return True
    want = [(t, x) for t, x in _nums(out) if not (re.fullmatch(r"-?\d+", t) and abs(x) < 1000)]
    if not want:
        return False
    for l in runs:
        vals = [x for _, x in _nums(l.get("out"))]
        if all(_match(t, x, vals) for t, x in want):
            return True
    return False


def main():
    data, run, reg = sys.argv[1:4]
    tag = sys.argv[4] if len(sys.argv) > 4 else "R1"  # the same rule for a later run, with its own run tag
    key = json.load(open(os.path.join(data, "key.json")))
    claims = {}
    for pf in sorted(glob.glob(os.path.join(run, "judge", "pool-*.json"))):
        for it in json.load(open(pf)):
            claims[it["id"]] = it
    recs, unconf = {}, {}
    n_judged = 0
    for jf in sorted(glob.glob(os.path.join(run, "judge", "judge", "*.json"))):
        if os.path.basename(jf).count(".") != 1:
            continue
        try:
            j = json.load(open(jf))
        except ValueError:
            continue
        n_judged += 1
        oid = os.path.basename(jf)[:-5]
        log = []
        if os.path.exists(jf + ".sbx.log"):
            for line in open(jf + ".sbx.log"):
                try:
                    log.append(json.loads(line))
                except ValueError:
                    pass
        model = ",".join((j.get("model_usage") or {}).keys())
        for r in j["out"].get("results", []):
            if r.get("tier") not in ("A", "B"):
                continue
            it = claims.get(f"{oid}/{r['id']}")
            if not it:
                continue
            real = bool(r.get("code_confirms")) and any(logged(c, log) for c in r.get("checks", []))
            k = f"{oid}#{r.get('issue')}"
            target = recs if real else unconf
            meta = key.get(oid, {})
            rec = target.get(k)
            if rec is None:
                rec = target[k] = {
                    "fid": f"{tag}-{oid}-{r.get('issue')}", "status": STATUS, "oid": oid, "pmcid": meta.get("pmcid"),
                    "doi": meta.get("doi"), "journal": meta.get("journalTitle"), "year": meta.get("pubYear"),
                    "field": meta.get("field"), "location": it.get("location"), "quote": it.get("quote"),
                    "claim": it.get("claim"), "tier": r["tier"], "statement": r.get("statement"),
                    "impact": r.get("impact"), "error_type": r.get("error_type"),
                    "error_type_detail": r.get("error_type_detail"), "judge_model": model,
                    "code_confirmed": real, "checks": [c for c in r.get("checks", []) if logged(c, log)][:3],
                    "sources": [], "registered": time.strftime("%Y-%m-%d"), "run": tag}
            rec["sources"] += [s["ref"] for s in it.get("sources", [])]
            if r["tier"] == "A" and rec["tier"] != "A":
                rec.update(tier="A", statement=r.get("statement"), impact=r.get("impact"))
    os.makedirs(reg, exist_ok=True)
    for name, d in (("findings.jsonl", recs), ("unconfirmed.jsonl", unconf)):
        with open(os.path.join(reg, name), "w") as f:
            for k in sorted(d):
                f.write(json.dumps(d[k], ensure_ascii=False) + "\n")
    tiers = Counter(r["tier"] for r in recs.values())
    by_field = Counter(r["field"] for r in recs.values())
    lines = [f"# {tag} findings register (PRIVATE)", "",
             f"All entries: {STATUS}. Never post, publish or send. Built {time.strftime('%Y-%m-%d %H:%M')} UTC.", "",
             f"Papers judged: {n_judged}. Real findings: {len(recs)} (tier A {tiers['A']}, tier B {tiers['B']}). "
             f"Judge A/B without a logged code check (not counted): {len(unconf)}.", "",
             "By field: " + ", ".join(f"{k} {v}" for k, v in sorted(by_field.items())), "",
             "| fid | field | tier | type | statement |", "|---|---|---|---|---|"]
    for k in sorted(recs, key=lambda k: (recs[k]["tier"], k)):
        r = recs[k]
        lines.append(f"| {r['fid']} | {r['field']} | {r['tier']} | {r['error_type']} | "
                     f"{nl(r['statement'])[:220].replace('|', '/')} |")
    open(os.path.join(reg, "register.md"), "w").write("\n".join(lines) + "\n")
    print(json.dumps({"papers_judged": n_judged, "real": len(recs), "A": tiers["A"], "B": tiers["B"],
                      "unconfirmed": len(unconf), "by_field": by_field}))


if __name__ == "__main__":
    main()
