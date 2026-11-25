"""Offline tests of the judge fixes (no model call). Run: python3 -I swarm/testing/test_judge_rules.py [<empty work dir>]

1. judge_rules.enforce: root-cause dedup, unstated-premise rule, materiality gate; v1 results unchanged.
2. The v2 judge prompt has the three rules and the no-"#" sandbox rule; the v1 prompt is unchanged.
3. register_v2 on a synthetic run: a symptom claim merges into its root (one record), premise -> D (not real),
   no flip -> B, and the four blind-gate verdicts give A / B / B + human queue / blind_rejected.
4. gate.decide_one on the verdict classes of the strict verification.
"""
import json, os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SW = os.path.dirname(HERE)
sys.path.insert(0, SW)
from judge_rules import enforce, flip_ok  # noqa: E402
import register_v2 as R  # noqa: E402
import gate as G  # noqa: E402
import pool  # noqa: E402

fails = []


def check(ok, text):
    print(("ok   " if ok else "FAIL ") + text, flush=True)
    if not ok:
        fails.append(text)


FLIP = {"result": "group difference in outcome", "from": "not significant (p = 0.30)", "to": "significant (p = 0.003)"}


def res(i, tier="A", issue=1, **kw):
    r = {"id": f"c{i}", "tier": tier, "issue": issue, "code_confirms": True, "flip": FLIP,
         "holds_under_all_readings": True, "root_cause_of": "", "premise_readings": [],
         "checks": [{"code": "print(1)", "output": f"paper 0.30 recomputed 0.00{i + 2}", "shows": "x"}],
         "statement": f"s{i}", "impact": "i", "error_type": "p_value"}
    r.update(kw)
    return r


# 1. enforce ---------------------------------------------------------------------------------------------
out = enforce([res(1, issue=1), res(2, tier="B", issue=2, root_cause_of="c1")])
check(out[1]["issue"] == 1 and out[1]["tier"] == "A" and out[1]["symptom_of"] == "c1", "symptom takes the root's issue and tier")
out = enforce([res(1, holds_under_all_readings=False)])
check(out[0]["tier"] == "D" and out[0]["judge_tier"] == "A", "tier A that fails under an open reading -> D")
out = enforce([res(1, holds_under_all_readings=False, tier="B")])
check(out[0]["tier"] == "B", "the premise rule touches only tier A")
for bad in ({"result": "", "from": "", "to": ""}, {"result": "x", "from": "3.2", "to": "3.2"},
            {"result": "none", "from": "a", "to": "b"}, None):
    check(enforce([res(1, flip=bad)])[0]["tier"] == "B", f"no valid flip {bad} -> B")
check(flip_ok(FLIP), "a full flip passes")
out = enforce([res(1, flip={"result": "", "from": "", "to": ""}), res(2, issue=2, root_cause_of="c1")])
check(out[1]["tier"] == "B" and out[1]["issue"] == 1, "a symptom follows its root after the materiality gate")
out = enforce([res(1, root_cause_of="c2"), res(2, issue=2, root_cause_of="c1")])
check(len(out) == 2, "a root-cause cycle ends")
v1 = {"id": "c1", "tier": "A", "issue": 3, "code_confirms": True}
check(enforce([v1]) == [v1], "v1 results are unchanged")

# 2. prompts --------------------------------------------------------------------------------------------
s2, sch2 = pool.judge_prompt("v2", "/x/sbx.py")
for t in ("holds_under_all_readings", "every plausible reading", "Materiality gate", "root_cause_of",
          'never write "#" comments', "python3 -I /x/sbx.py"):
    check(t in s2, f"v2 prompt has {t!r}")
props = sch2["properties"]["results"]["items"]
check(all(k in props["required"] for k in ("flip", "holds_under_all_readings", "root_cause_of", "premise_readings")),
      "v2 schema requires the new fields")
s1, _ = pool.judge_prompt("v1", "/x/sbx.py")
root = os.path.dirname(SW)
old = open(os.path.join(root, "prompts", "judge_pool.txt")).read().strip().replace(
    "{tool_block}", open(os.path.join(root, "prompts", "tool_sbx.txt")).read().strip().replace("{sbx}", "/x/sbx.py"))
check(s1 == old and "#" not in s1.split("Code rule")[0][-50:], "v1 prompt is unchanged")

# 3. register on a synthetic run ------------------------------------------------------------------------
work = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="judgetest-")
data, run = os.path.join(work, "data"), os.path.join(work, "run")
os.makedirs(os.path.join(run, "judge", "judge"), exist_ok=True)
os.makedirs(data, exist_ok=True)
json.dump({"p1": {"field": "f"}, "p2": {"field": "f"}}, open(os.path.join(data, "key.json"), "w"))
claims = [{"id": f"p1/c{i}", "oid": "p1", "location": f"L{i}", "quote": f"q{i}", "claim": f"claim {i}",
           "sources": [{"arm": "swarm", "ref": f"F{i}"}]} for i in range(1, 7)]
claims += [{"id": "p2/c1", "oid": "p2", "location": "L", "quote": "q", "claim": "c", "sources": [{"arm": "swarm", "ref": "F9"}]}]
json.dump(claims, open(os.path.join(run, "judge", "pool-b000.json"), "w"))
results = [res(1, issue=1),                                       # root, tier A
           res(2, tier="A", issue=2, root_cause_of="c1"),         # symptom of c1 -> merged
           res(3, issue=3, holds_under_all_readings=False),       # premise -> D, not real
           res(4, issue=4, flip={"result": "", "from": "", "to": ""}),  # no flip -> B
           res(5, issue=5), res(6, issue=6)]
log = [{"rc": 0, "code": "print(1)", "out": f"paper 0.30 recomputed 0.00{i + 2}"} for i in range(1, 7)]
json.dump({"out": {"results": results}, "model_usage": {"claude-opus-5-5": {}}}, open(os.path.join(run, "judge", "judge", "p1.json"), "w"))
open(os.path.join(run, "judge", "judge", "p1.json.sbx.log"), "w").write("\n".join(json.dumps(x) for x in log) + "\n")
json.dump({"out": {"results": [res(1)]}, "model_usage": {}}, open(os.path.join(run, "judge", "judge", "p2.json"), "w"))
open(os.path.join(run, "judge", "judge", "p2.json.sbx.log"), "w").write(json.dumps(log[0]) + "\n")
recs, unconf, n = R.build(data, run, "TX")
check(n == 2, "two papers judged")
check(sorted(recs) == ["p1#1", "p1#4", "p1#5", "p1#6", "p2#1"], f"records {sorted(recs)}: symptom merged, premise case out")
check(recs["p1#1"]["claim_ids"] == ["c1", "c2"] and recs["p1#1"]["sources"] == ["F1", "F2"], "the merged record holds both claims")
check(recs["p1#4"]["tier"] == "B", "no flip -> tier B in the register")
gate = {"TX-p1-1": {"verdict": "CONFIRMED"}, "TX-p1-5": {"verdict": "UNRESOLVED"}, "TX-p1-6": {"verdict": "REJECTED"},
        "TX-p2-1": {"verdict": "CONFIRMED_NOT_MATERIAL"}}
summary = R.write(os.path.join(work, "reg"), "TX", recs, unconf, n, gate)
fin = {json.loads(l)["fid"]: json.loads(l) for l in open(os.path.join(work, "reg", "findings.jsonl"))}
q = [json.loads(l)["fid"] for l in open(os.path.join(work, "reg", "human_queue.jsonl"))]
rj = [json.loads(l)["fid"] for l in open(os.path.join(work, "reg", "blind_rejected.jsonl"))]
cd = [json.loads(l)["fid"] for l in open(os.path.join(work, "reg", "gate_candidates.jsonl"))]
check(fin["TX-p1-1"]["tier"] == "A" and fin["TX-p1-1"]["gate"] == "confirmed", "gate CONFIRMED -> A")
check(fin["TX-p2-1"]["tier"] == "B", "gate CONFIRMED_NOT_MATERIAL -> B")
check(fin["TX-p1-5"]["tier"] == "B" and q == ["TX-p1-5"], "gate UNRESOLVED -> B and the human queue")
check("TX-p1-6" not in fin and rj == ["TX-p1-6"], "gate REJECTED -> out of the register, into blind_rejected")
check(fin["TX-p1-4"]["gate"] == "not_run_tier_B", "the gate does not run on tier B")
check(sorted(cd) == ["TX-p1-1", "TX-p1-5", "TX-p1-6", "TX-p2-1"], "gate candidates = tier A before the gate")
check(summary["A"] == 1 and summary["B"] == 3, f"counts {summary}")
R.write(os.path.join(work, "reg2"), "TX", recs, unconf, n, {})
fin2 = [json.loads(l) for l in open(os.path.join(work, "reg2", "findings.jsonl"))]
check(sum(r["gate"] == "pending" for r in fin2) == 4, "no gate result -> tier A stays, gate 'pending'")

# 4. gate decision --------------------------------------------------------------------------------------
P = {"output_in_log": True}
it = lambda i, st, prov=P, eff="the significance flips": {"id": str(i), "status": st, "provenance": prov if st == "inconsistent" else None, "material_effect": eff}
check(G.decide_one([it(1, "inconsistent")], {"1": "same_error"})[0] == "CONFIRMED", "same error, inconsistent, logged -> CONFIRMED")
check(G.decide_one([it(1, "inconsistent", eff="none")], {"1": "same_error"})[0] == "CONFIRMED_NOT_MATERIAL", "material 'none' -> not material")
check(G.decide_one([it(1, "inconsistent", prov={"output_in_log": False})], {"1": "same_error"})[0] == "UNRESOLVED", "no log provenance -> UNRESOLVED")
check(G.decide_one([it(1, "undetermined")], {"1": "same_error"})[0] == "UNRESOLVED", "undetermined -> UNRESOLVED")
check(G.decide_one([it(1, "consistent")], {"1": "same_error"})[0] == "REJECTED", "same quantity consistent -> REJECTED")
check(G.decide_one([it(1, "inconsistent")], {"1": "unrelated"})[0] == "REJECTED", "an unrelated inconsistency does not confirm")
check(G.decide_one([], {})[0] == "REJECTED", "no items -> REJECTED")

print("FAILED: " + "; ".join(fails) if fails else "ALL OK")
sys.exit(1 if fails else 0)
