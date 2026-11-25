"""Strict, blind re-verification of a sample of register findings.

  python3 -I verify/strict.py run   --sample S.json --register R/findings.jsonl --data D --run RUN   (model calls)
  python3 -I verify/strict.py check --sample S.json --register R/findings.jsonl --data D --run RUN   -> RUN/check.json

The verifier (Opus 5.5) gets the paper and a location pointer (the finding's location string and its verbatim
quote from the paper). It never gets the explorer's claim, the judge's statement, tier, type or impact.
Its default is "consistent". "inconsistent" needs a sandbox check (R1-R5 in verify/verifier.txt).
'check' adds mechanical provenance: every inconsistent item's code must be in the call's sandbox log with the same
printed output, and every input source_quote must occur in the paper text.
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import coordinator as C  # noqa: E402
import exp  # noqa: E402

MODEL = "claude-opus-5-5"
SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["location_found", "items", "summary"],
    "properties": {
        "location_found": {"type": "boolean"},
        "summary": {"type": "string"},
        "items": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["id", "what", "status", "paper_value", "recomputed", "inputs", "code", "output",
                         "misread_check", "explained_elsewhere", "design_applies", "material_effect", "reason"],
            "properties": {
                "id": {"type": "string"},
                "what": {"type": "string"},
                "status": {"enum": ["consistent", "inconsistent", "undetermined"]},
                "paper_value": {"type": "string"},
                "recomputed": {"type": "string"},
                "inputs": {"type": "array", "items": {
                    "type": "object", "additionalProperties": False, "required": ["value", "source_quote"],
                    "properties": {"value": {"type": "string"}, "source_quote": {"type": "string"}}}},
                "code": {"type": "string"},
                "output": {"type": "string"},
                "misread_check": {"type": "string"},
                "explained_elsewhere": {"type": "string"},
                "design_applies": {"type": "string"},
                "material_effect": {"type": "string"},
                "reason": {"type": "string"}}}}}}


def load(a):
    sample = json.load(open(a.sample))["sample"]
    reg = {}
    for line in open(a.register):
        r = json.loads(line)
        reg[r["fid"]] = r
    return sample, reg


def run(a):
    sample, reg = load(a)
    tool = open(os.path.join(HERE, "tool_sbx_strict.txt")).read().strip().replace("{sbx}", exp.SBX)
    system = open(os.path.join(HERE, "verifier.txt")).read().strip().replace("{tool_block}", tool)
    os.makedirs(os.path.join(a.run, "verify"), exist_ok=True)
    tasks = []
    for s in sample:
        r = reg[s["fid"]]
        pointer = {"location": r["location"], "passage": r["quote"]}   # nothing else from the register
        extra = ("\nLOCATION POINTER (JSON; the passage is copied from the paper):\n"
                 + json.dumps(pointer, indent=1, ensure_ascii=False))
        tasks.append({"id": s["fid"], "oid": r["oid"], "stage": "strict", "model": MODEL,
                      "out": os.path.join(a.run, "verify", s["fid"] + ".json"),
                      "argv": exp.argv(MODEL, system, SCHEMA, "sbx", None),
                      "input": lambda oid=r["oid"], extra=extra: C.fence(C.read_paper(a.data, oid), extra),
                      "timeout": 2700})
    print(f"strict: {len(tasks)} calls, model {MODEL}", flush=True)
    a.stage = "strict"
    exp.run_tasks(a, tasks)


def nums(s):
    return re.findall(r"\d+(?:\.\d+)?", s or "")


def check(a):
    sample, reg = load(a)
    res = []
    for s in sample:
        fid = s["fid"]; r = reg[fid]
        f = os.path.join(a.run, "verify", fid + ".json")
        d = C.load_json(f) if os.path.exists(f) else None
        if not d:
            res.append({"fid": fid, "field": s["field"], "state": "no_output"}); continue
        out = d["out"]
        paper = C.norm_ws(C.read_paper(a.data, r["oid"]))
        sbx = [json.loads(l) for l in open(f + ".sbx.log")] if os.path.exists(f + ".sbx.log") else []
        items = []
        for it in out.get("items", []):
            prov = None
            if it["status"] == "inconsistent":
                code_ok = any(C.norm_ws(x["code"]) == C.norm_ws(it["code"]) and x["rc"] == 0 for x in sbx)
                outs = [x["out"] for x in sbx if x["rc"] == 0]
                # the reported output must be printed by some run (numbers in the same order)
                on = nums(it["output"])
                out_ok = bool(on) and any(" ".join(on) in " ".join(nums(o)) for o in outs)
                q_ok = [C.quote_in_paper(i["source_quote"], paper) for i in it["inputs"]]
                prov = {"code_in_log": code_ok, "output_in_log": out_ok,
                        "quotes_in_paper": f"{sum(q_ok)}/{len(q_ok)}", "all_quotes_ok": all(q_ok) and bool(q_ok)}
            items.append({**it, "provenance": prov})
        res.append({"fid": fid, "field": s["field"], "state": "ok", "location_found": out.get("location_found"),
                    "summary": out.get("summary"), "n_sbx_runs": len(sbx), "cost": d.get("cost_usd_list"),
                    "items": items})
    json.dump(res, open(os.path.join(a.run, "check.json"), "w"), indent=1, ensure_ascii=False)
    for x in res:
        inc = [i for i in x.get("items", []) if i["status"] == "inconsistent"]
        print(x["fid"], x["state"], "items", len(x.get("items", [])), "inconsistent", len(inc),
              [(i["provenance"]["code_in_log"], i["provenance"]["output_in_log"], i["provenance"]["quotes_in_paper"]) for i in inc])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "check"])
    ap.add_argument("--sample"); ap.add_argument("--register"); ap.add_argument("--data"); ap.add_argument("--run")
    ap.add_argument("--start", type=int, default=4); ap.add_argument("--max", type=int, default=8)
    ap.add_argument("--step", type=int, default=2); ap.add_argument("--mem-gb", type=float, default=2.8)
    ap.add_argument("--cores", type=float, default=4.0); ap.add_argument("--mem-source", default="auto")
    a = ap.parse_args()
    os.makedirs(a.run, exist_ok=True)
    {"run": run, "check": check}[a.cmd](a)


if __name__ == "__main__":
    main()
