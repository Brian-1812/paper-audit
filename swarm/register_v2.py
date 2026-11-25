"""Build the findings register of a run with the v2 judge and the blind second gate. No model calls.

Usage: python3 -I swarm/register_v2.py <data_dir> <run_dir> <register_dir> [<run tag, default R2>]
Input: <run_dir>/judge/pool-*.json, <run_dir>/judge/judge/<oid>.json (+ .sbx.log), and the gate results
<run_dir>/gate/verdicts.json (written by swarm/gate.py; may be missing).
Steps:
  1. The judge's results per paper go through swarm/judge_rules.enforce (root cause, unstated premise, materiality).
  2. REAL = the v1 rule (swarm/register.py): tier A or B after step 1, code_confirms, and a check output in the judge's own sandbox log.
     One record per (paper, issue). Tier A wins over B.
  3. Blind second gate on every tier-A record (swarm/gate.py, keyed by fid):
       CONFIRMED and material      -> tier A ("gate": "confirmed")
       CONFIRMED, not material     -> tier B ("gate": "confirmed_not_material")
       UNRESOLVED                  -> tier B, and a copy in human_queue.jsonl ("gate": "unresolved")
       REJECTED                    -> out of the register, into blind_rejected.jsonl ("gate": "rejected")
       no gate result yet          -> tier A with "gate": "pending" (the driver runs the gate before the register)
Output (rebuilt every time, so a rerun gives the same files):
  findings.jsonl, unconfirmed.jsonl (judge A/B without a logged code check), gate_candidates.jsonl (tier A before
  the gate: the gate's input), human_queue.jsonl, blind_rejected.jsonl, register.md.
Every record has status "possible error, unverified by humans". The register stays local (data/ is git-ignored).
"""
import glob, json, os, sys, time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from register import STATUS, logged, nl  # noqa: E402
from judge_rules import enforce  # noqa: E402


def build(data, run, tag="R2"):
    """-> (records by key, unconfirmed by key, papers judged). Records carry the judge tier before the gate."""
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
        for r in enforce(j["out"].get("results", [])):
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
                    "impact": r.get("impact"), "flip": r.get("flip"), "error_type": r.get("error_type"),
                    "error_type_detail": r.get("error_type_detail"), "judge_model": model,
                    "code_confirmed": real, "checks": [c for c in r.get("checks", []) if logged(c, log)][:3],
                    "premise_readings": r.get("premise_readings"), "rule_notes": [], "claim_ids": [],
                    "sources": [], "registered": time.strftime("%Y-%m-%d"), "run": tag}
            rec["claim_ids"].append(r["id"])
            rec["sources"] += [s["ref"] for s in it.get("sources", [])]
            rec["rule_notes"] += [f"{r['id']}: {x}" for x in r.get("rule_notes", [])]
            if r["tier"] == "A" and rec["tier"] != "A":
                # the record points at the tier-A claim: its location and quote go to the blind gate
                rec.update(tier="A", statement=r.get("statement"), impact=r.get("impact"), flip=r.get("flip"),
                           location=it.get("location"), quote=it.get("quote"), claim=it.get("claim"))
    return recs, unconf, n_judged


GATE_TIER = {"CONFIRMED": "A", "CONFIRMED_NOT_MATERIAL": "B", "UNRESOLVED": "B"}


def apply_gate(recs, gate):
    """Split pre-gate records by the gate verdicts. -> (findings, human_queue, blind_rejected), dicts by key."""
    final, queue, rejected = {}, {}, {}
    for k, r in recs.items():
        r = dict(r, judge_tier=r["tier"])
        if r["tier"] != "A":
            final[k] = dict(r, gate="not_run_tier_B")
            continue
        g = gate.get(r["fid"])
        if not g:
            final[k] = dict(r, gate="pending")
            continue
        v = g["verdict"]
        r["gate"] = v.lower()
        r["gate_detail"] = {x: g.get(x) for x in ("items", "reason", "material_effect", "verify_file")}
        if v == "REJECTED":
            rejected[k] = r
            continue
        r["tier"] = GATE_TIER[v]
        final[k] = r
        if v == "UNRESOLVED":
            queue[k] = r
    return final, queue, rejected


def write(reg, tag, recs, unconf, n_judged, gate):
    final, queue, rejected = apply_gate(recs, gate)
    os.makedirs(reg, exist_ok=True)
    cands = {k: r for k, r in recs.items() if r["tier"] == "A"}
    for name, d in (("findings.jsonl", final), ("unconfirmed.jsonl", unconf), ("gate_candidates.jsonl", cands),
                    ("human_queue.jsonl", queue), ("blind_rejected.jsonl", rejected)):
        with open(os.path.join(reg, name), "w") as f:
            for k in sorted(d):
                f.write(json.dumps(d[k], ensure_ascii=False) + "\n")
    tiers = Counter(r["tier"] for r in final.values())
    gates = Counter(r["gate"] for r in list(final.values()) + list(rejected.values()))
    by_field = Counter(r["field"] for r in final.values())
    lines = [f"# {tag} findings register (PRIVATE)", "",
             f"All entries: {STATUS}. Never post, publish or send. Built {time.strftime('%Y-%m-%d %H:%M')} UTC.", "",
             f"Papers judged: {n_judged}. Real findings: {len(final)} (tier A {tiers['A']}, tier B {tiers['B']}). "
             f"Judge tier A before the blind gate: {len(cands)}. Gate: {dict(gates)}. Human queue: {len(queue)}. "
             f"Blind-rejected (not counted): {len(rejected)}. Judge A/B without a logged code check (not counted): "
             f"{len(unconf)}.", "",
             "By field: " + ", ".join(f"{k} {v}" for k, v in sorted(by_field.items())), "",
             "| fid | field | tier | gate | type | statement |", "|---|---|---|---|---|---|"]
    for k in sorted(final, key=lambda k: (final[k]["tier"], k)):
        r = final[k]
        lines.append(f"| {r['fid']} | {r['field']} | {r['tier']} | {r['gate']} | {r['error_type']} | "
                     f"{nl(r['statement'])[:220].replace('|', '/')} |")
    open(os.path.join(reg, "register.md"), "w").write("\n".join(lines) + "\n")
    return {"papers_judged": n_judged, "real": len(final), "A": tiers["A"], "B": tiers["B"], "gate_candidates": len(cands),
            "gate": dict(gates), "human_queue": len(queue), "blind_rejected": len(rejected), "unconfirmed": len(unconf),
            "by_field": dict(by_field)}


def main():
    data, run, reg = sys.argv[1:4]
    tag = sys.argv[4] if len(sys.argv) > 4 else "R2"
    recs, unconf, n = build(data, run, tag)
    gp = os.path.join(run, "gate", "verdicts.json")
    gate = json.load(open(gp)) if os.path.exists(gp) else {}
    print(json.dumps(write(reg, tag, recs, unconf, n, gate)))


if __name__ == "__main__":
    main()
