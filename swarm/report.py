"""Write the arm comparison table (markdown) from the judge verdicts, the pool and the swarm board.

Usage: python3 -I swarm/report.py <judge_run> <swarm_db> <out.md>
Reads <judge_run>/pool.json, <judge_run>/judge/*.json and <judge_run>/score.json (run pool.py score first).
"""
import json, os, sqlite3, sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pool as P  # noqa: E402

PIPES = ("pipe_sonnet", "pipe_haiku")


def main():
    run, db, out = sys.argv[1:4]
    items = json.load(open(os.path.join(run, "pool.json")))
    v, jcost, _ = P.load_verdicts(run)
    sc = json.load(open(os.path.join(run, "score.json")))
    real = lambda x: x and x.get("tier") in ("A", "B") and x.get("code_confirms")
    issues = defaultdict(set)      # arm -> {(oid, issue)}
    itype = {}
    claims_per_issue = defaultdict(Counter)
    judged_papers = set(jcost)
    for it in items:
        if it["oid"] not in judged_papers:
            continue
        x = v.get(it["id"])
        if not real(x):
            continue
        k = (it["oid"], x["issue"])
        itype[k] = x["error_type"] if x["error_type"] != "other" else "other: " + (x.get("error_type_detail") or "")[:50]
        for s in it["sources"]:
            issues[s["arm"]].add(k)
            claims_per_issue[s["arm"]][k] += 1
    pipes = set().union(*[issues[a] for a in PIPES])
    swarm_only = issues["swarm"] - pipes
    pipe_only = pipes - issues["swarm"] - issues["swarm_unev"]
    gt = issues["rule"]
    L = []
    L.append(f"Papers judged: {len(judged_papers)}. Judge list-price cost: ${sc['judge_usd_total']}.")
    L.append("")
    L.append("| arm | claims judged | real claims | precision | distinct real errors | of them tier A | dup claims per real error | "
             "statcheck truth recall | explore $ | judge $ | $ per real error |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sc["rows"]:
        a = r["arm"]
        dup = (r["real_claims"] - r["distinct_real_errors"]) / r["real_claims"] if r["real_claims"] else 0
        rec = len(issues[a] & gt) / len(gt) if gt else 0
        L.append(f"| {a} | {r['judged']} | {r['real_claims']} | {r['precision']:.0%} | {r['distinct_real_errors']} | "
                 f"{r['consequential_A']} | {dup:.0%} | {rec:.0%} ({len(issues[a] & gt)}/{len(gt)}) | {r['explore_usd']} | "
                 f"{r['judge_usd']} | {r['usd_per_real_error']} |")
    L.append("")
    L.append(f"- Union of all arms: {len(set().union(*issues.values()))} distinct real errors. "
             f"Swarm and any pipeline arm share {len(issues['swarm'] & pipes)}.")
    L.append(f"- Real errors that ONLY the swarm found (no pipeline arm): {len(swarm_only)}; types: "
             f"{dict(Counter(itype[k].split(':')[0] for k in swarm_only))}")
    L.append(f"- Real errors that the pipelines found and the swarm (gated or not) did not: {len(pipe_only)}; types: "
             f"{dict(Counter(itype[k].split(':')[0] for k in pipe_only))}")
    L.append(f"- Statcheck truth: {len(gt)} distinct judge-confirmed p-value errors among the material statcheck hits.")
    L.append(f"- Types by arm: " + "; ".join(f"{a}: {dict(Counter(itype[k].split(':')[0] for k in issues[a]))}" for a in sorted(issues)))
    others = sorted({itype[k] for k in set().union(*issues.values()) if itype[k].startswith("other")})
    L.append(f"- 'other' types: {others}")
    c = sqlite3.connect(db)
    q = lambda s: c.execute(s).fetchone()[0]
    L.append("")
    L.append("Swarm board: cells done " + str(q("SELECT COUNT(*) FROM cells WHERE status='done'")) +
             ", papers covered " + str(q("SELECT COUNT(DISTINCT paper) FROM cells WHERE status='done'")) +
             ", double leases " + str(q("SELECT COUNT(*) FROM (SELECT paper, check_name, COUNT(*) n FROM cells GROUP BY 1,2 HAVING n>1)")) +
             ", findings " + str(q("SELECT COUNT(*) FROM findings")) + ", evidenced " + str(q("SELECT COUNT(*) FROM findings WHERE evidenced=1")) +
             ", program-detected duplicates " + str(q("SELECT COUNT(*) FROM findings WHERE dup_of IS NOT NULL")) +
             ", cells by check " + str(dict(c.execute("SELECT check_name, COUNT(*) FROM cells WHERE status='done' GROUP BY 1").fetchall())) +
             ", leads " + str(dict(c.execute("SELECT status, COUNT(*) FROM leads GROUP BY 1").fetchall())) + ".")
    open(out, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
