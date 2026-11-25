"""Pool the flags of every arm, judge them once with the same judge, and score the arms.

  python3 -I swarm/pool.py pool  --out J/pool.json --data D --swarm-db S/board.sqlite --pipe P:sonnet,P2:haiku
                                 [--psystat D/psystat.json] [--papers N] [--with-unevidenced]
  python3 -I swarm/pool.py judge --pool J/pool.json --run J --data D [--opus-share 0.7]   (model calls)
  python3 -I swarm/pool.py score --pool J/pool.json --run J --swarm-db S/board.sqlite --pipe P:sonnet,P2:haiku

Arms (the "sources" of a claim):
  swarm        evidenced, non-duplicate findings of the swarm board (quote in the paper, evidence in the sandbox log)
  swarm_unev   swarm findings that failed the evidence gate (judged only with --with-unevidenced, never counted)
  pipe_<v>     flags of the fixed pipeline's lens skim variant v that its own routing rule sends to the costly check
  rule         material inconsistencies from the deterministic statcheck (psystat.py), the ground-truth candidates
The judge sees one paper and all its claims at once, in a shuffled order, without the arm names. It gives a tier, a
code check from the sandbox, an issue number (claims about the same error share it) and an error type.
A REAL ERROR = tier A or B, and code_confirms = true (a sandbox check that the judge ran shows the error).
"""
import argparse, hashlib, json, os, random, re, sqlite3, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import coordinator as C  # noqa: E402


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip().lower()


# ---------------------------------------------------------------- pool
def pipes(a):
    """--pipe 'RUN:variant,RUN2:variant2' -> [(RUN, variant), ...]"""
    return [tuple(x.rsplit(":", 1)) for x in (a.pipe or "").split(",") if x]


def pool(a):
    if a.paper_list:  # one batch
        papers = [x.strip() for x in open(a.paper_list) if x.strip()]
    else:
        papers = C.papers(a.data, 0)[:a.papers] if a.papers else C.papers(a.data, 0)
    items = defaultdict(list)          # oid -> [claim dicts]

    def add(oid, arm, ref, location, quote, claim):
        for it in items[oid]:
            if norm(it["quote"]) == norm(quote) and norm(quote):
                it["sources"].append({"arm": arm, "ref": ref})
                return
        items[oid].append({"location": location or "", "quote": quote or "", "claim": claim,
                           "sources": [{"arm": arm, "ref": ref}]})

    if a.swarm_db:
        db = sqlite3.connect(a.swarm_db); db.row_factory = sqlite3.Row
        for r in db.execute("SELECT * FROM findings ORDER BY id"):
            if r["paper"] not in papers or r["dup_of"] is not None:
                continue
            if not r["evidenced"] and not a.with_unevidenced:
                continue
            arm = "swarm" if r["evidenced"] else "swarm_unev"
            add(r["paper"], arm, f"F{r['id']}", r["location"], r["quote"],
                f"{r['claim']} Paper value: {r['paper_value']}. Recomputed: {r['recomputed_value']}.")
    if a.pipe:
        import exp  # noqa: E402
        for run, v in pipes(a):
            for oid in papers:
                if not os.path.isdir(os.path.join(run, "skim-" + v)):
                    continue
                for f in exp.skim_flags(run, v, oid, a.data):
                    if f["opus"]:
                        add(oid, "pipe_" + v, f["id"], f.get("location"), f.get("quote"),
                            f"{f.get('title', '')}. Claimed: {f.get('claimed', '')}. Corrected: {f.get('corrected', '')}. "
                            f"{f.get('reasoning', '')}")
    if a.psystat:
        ps = json.load(open(a.psystat))
        for oid in papers:
            for k, h in enumerate(ps.get(oid, [])):
                if h.get("material"):
                    add(oid, "rule", f"S{k}", "", h["quote"],
                        f"The reported p does not follow from the test statistic: {h['test']} with df {h['df1']}"
                        f"{', ' + str(h['df2']) if h['df2'] else ''} = {h['stat']} gives a two-tailed p between "
                        f"{h['p_lo']:.4g} and {h['p_hi']:.4g}, but the paper reports p {h['op']} {h['p']}.")
    out = []
    for oid in papers:
        rng = random.Random(oid)
        its = items.get(oid, [])
        rng.shuffle(its)
        for k, it in enumerate(its, 1):
            out.append({"id": f"{oid}/c{k}", "oid": oid, **it})
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"pool: {len(out)} claims in {len({i['oid'] for i in out})} papers;",
          dict(Counter(s["arm"] for i in out for s in i["sources"])))


# ---------------------------------------------------------------- judge
JUDGE_FILES = {  # version -> (prompt, sandbox tool block, schema file, schema key)
    "v1": ("judge_pool.txt", "tool_sbx.txt", "schemas_swarm.json", "judge_pool"),
    # v2: the fixes from the strict verification (unstated premises, root-cause dedup, materiality gate, no "#" in sandbox code)
    "v2": ("judge_pool_v2.txt", "tool_sbx_v2.txt", "schemas_v2.json", "judge_pool_v2"),
}


def judge_prompt(version, sbx):
    """(system prompt, JSON schema) of a judge version."""
    pr, tool, sf, key = JUDGE_FILES[version]
    P = lambda f: os.path.join(ROOT, "prompts", f)
    system = open(P(pr)).read().strip().replace("{tool_block}", open(P(tool)).read().strip().replace("{sbx}", sbx))
    return system, json.load(open(P(sf)))[key]


def judge(a):
    import exp  # noqa: E402
    items = json.load(open(a.pool))
    by = defaultdict(list)
    for it in items:
        by[it["oid"]].append(it)
    system, schema = judge_prompt(a.judge_version, exp.SBX)
    tasks = []
    for oid, its in sorted(by.items()):
        model = "claude-opus-5-5" if int(hashlib.sha1(oid.encode()).hexdigest(), 16) % 100 < a.opus_share * 100 \
            else "claude-fable-5-2"
        claims = [{"id": it["id"].split("/", 1)[1], "location": it["location"], "quote": it["quote"], "claim": it["claim"]}
                  for it in its]
        extra = "\nCLAIMS TO CHECK (JSON; from other reviewers, not from the paper):\n" + json.dumps(claims, indent=1, ensure_ascii=False)
        tasks.append({"id": f"{oid}.judge", "oid": oid, "stage": "judge", "model": model,
                      "out": os.path.join(a.run, "judge", oid + ".json"),
                      "argv": exp.argv(model, system, schema, "sbx", None),
                      "input": lambda oid=oid, extra=extra: C.fence(C.read_paper(a.data, oid), extra), "timeout": 2700})
    print(f"judge: {len(tasks)} papers, opus {sum(t['model'].startswith('claude-opus') for t in tasks)}, "
          f"fable {sum(t['model'].startswith('claude-fable') for t in tasks)}", flush=True)
    a.stage = "judge"
    exp.run_tasks(a, tasks)


# ---------------------------------------------------------------- score
def load_verdicts(run):
    v, cost, model = {}, {}, {}
    d = os.path.join(run, "judge")
    for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if not fn.endswith(".json") or fn.count(".") != 1:
            continue
        r = C.load_json(os.path.join(d, fn))
        if not r:
            continue
        oid = fn[:-5]
        cost[oid] = r.get("cost_usd_list") or 0
        model[oid] = ",".join((r.get("model_usage") or {}).keys())
        for x in r["out"].get("results", []):
            v[f"{oid}/{x['id']}"] = x
    return v, cost, model


def score(a):
    items = json.load(open(a.pool))
    v, jcost, jmodel = load_verdicts(a.run)
    n_per_paper = Counter(it["oid"] for it in items)
    arms = sorted({s["arm"] for it in items for s in it["sources"]})
    real = lambda x: x and x.get("tier") in ("A", "B") and x.get("code_confirms")
    st = {arm: {"claims": 0, "judged": 0, "real_claims": 0, "issues": set(), "issues_A": set(), "types": Counter(),
                "judge_usd": 0.0} for arm in arms}
    issue_type = {}
    for it in items:
        x = v.get(it["id"])
        arms_here = {s["arm"] for s in it["sources"]}
        for arm in arms_here:
            s = st[arm]
            s["claims"] += 1
            s["judge_usd"] += jcost.get(it["oid"], 0) / n_per_paper[it["oid"]]
            if x:
                s["judged"] += 1
                if real(x):
                    key = (it["oid"], x["issue"])
                    s["real_claims"] += 1
                    s["issues"].add(key)
                    issue_type[key] = x["error_type"] if x["error_type"] != "other" else "other:" + (x.get("error_type_detail") or "")[:40]
                    if x["tier"] == "A":
                        s["issues_A"].add(key)
    for arm in arms:
        for key in st[arm]["issues"]:
            st[arm]["types"][issue_type[key].split(":")[0]] += 1
    # explorer / skim usage per arm
    use = {}
    if a.swarm_db:
        db = sqlite3.connect(a.swarm_db)
        use["swarm"] = db.execute("SELECT COALESCE(SUM(cost_usd),0) FROM cells").fetchone()[0]
    for run, v_ in pipes(a):
        f = os.path.join(run, "calls.jsonl")
        if os.path.exists(f):
            use["pipe_" + v_] = sum((json.loads(l).get("cost_usd_list") or 0) for l in open(f)
                                    if json.loads(l).get("stage") == "skim-" + v_)
    rows = []
    for arm in arms:
        s = st[arm]
        tot = use.get(arm, 0) + s["judge_usd"]
        rows.append({"arm": arm, "claims_to_judge": s["claims"], "judged": s["judged"], "real_claims": s["real_claims"],
                     "precision": round(s["real_claims"] / s["judged"], 3) if s["judged"] else None,
                     "distinct_real_errors": len(s["issues"]), "consequential_A": len(s["issues_A"]),
                     "explore_usd": round(use.get(arm, 0), 2), "judge_usd": round(s["judge_usd"], 2),
                     "usd_per_real_error": round(tot / len(s["issues"]), 2) if s["issues"] else None,
                     "types": dict(s["types"])})
    pairs = {}
    for i, x in enumerate(arms):
        for y in arms[i + 1:]:
            pairs[f"{x}&{y}"] = len(st[x]["issues"] & st[y]["issues"])
    only = {}
    for x in arms:
        others = set().union(*[st[y]["issues"] for y in arms if y != x and y != "swarm_unev"]) if len(arms) > 1 else set()
        only[x] = sorted(f"{k[0]}#{k[1]}:{issue_type[k]}" for k in st[x]["issues"] - others)
    # recall against the deterministic ground truth: issues that contain a rule claim and are real
    gt = st.get("rule", {}).get("issues", set())
    recall = {arm: (round(len(st[arm]["issues"] & gt) / len(gt), 3) if gt else None) for arm in arms}
    res = {"rows": rows, "overlap_issues": pairs, "only_this_arm": only, "recall_vs_rule_truth": recall,
           "rule_truth_real": len(gt), "judge_models": Counter(jmodel.values()), "papers_judged": len(jcost),
           "judge_usd_total": round(sum(jcost.values()), 2)}
    json.dump(res, open(os.path.join(a.run, "score.json"), "w"), indent=1, default=list)
    print(json.dumps(res, indent=1, default=list)[:6000])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["pool", "judge", "score"])
    ap.add_argument("--out"); ap.add_argument("--pool"); ap.add_argument("--run")
    ap.add_argument("--data", default="data")
    ap.add_argument("--swarm-db"); ap.add_argument("--pipe", help="RUN:variant[,RUN:variant]")
    ap.add_argument("--psystat"); ap.add_argument("--papers", type=int, default=0)
    ap.add_argument("--paper-list")
    ap.add_argument("--with-unevidenced", action="store_true")
    ap.add_argument("--opus-share", type=float, default=0.7)
    ap.add_argument("--judge-version", choices=sorted(JUDGE_FILES), default="v1")
    ap.add_argument("--start", type=int, default=4); ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--step", type=int, default=2); ap.add_argument("--mem-gb", type=float, default=2.8)
    ap.add_argument("--cores", type=float, default=4.0); ap.add_argument("--mem-source", default="auto")
    a = ap.parse_args()
    if a.run:
        os.makedirs(a.run, exist_ok=True)
    {"pool": pool, "judge": judge, "score": score}[a.cmd](a)


if __name__ == "__main__":
    main()
