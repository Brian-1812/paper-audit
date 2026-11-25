"""Deterministic rules on the output of the v2 judge (the fixes from the strict verification that code can enforce).

enforce(results) returns a copy of the judge's per-claim results with these rules applied, in this order:
  1. Root-cause dedup: a claim with "root_cause_of" = another claim id of the same paper gets the issue number and
     the tier of that root claim (chains are followed). So the register counts one error once.
  2. Unstated-premise rule: tier A with "holds_under_all_readings" = false becomes D (the error does not hold under
     every reading that the paper leaves open).
  3. Materiality gate: tier A needs a "flip" with a result, a "from" and a "to" that differ. Otherwise the tier is B.
Each changed result gets "rule_notes" (a list of short texts) and keeps the judge's own tier in "judge_tier".
Results of the v1 judge (no v2 fields) are returned unchanged, so old runs give the same register.
"""
import re


def _empty(s):
    s = re.sub(r"[\s.\-–—]+", " ", str(s or "")).strip().lower()
    return s in ("", "none", "n/a", "na", "no change", "nothing", "not applicable")


def flip_ok(flip):
    """True when the flip names a result and two different values."""
    if not isinstance(flip, dict):
        return False
    if _empty(flip.get("result")) or _empty(flip.get("from")) or _empty(flip.get("to")):
        return False
    norm = lambda x: re.sub(r"\s+", " ", str(x)).strip().lower()
    return norm(flip["from"]) != norm(flip["to"])


def is_v2(r):
    return "flip" in r or "holds_under_all_readings" in r or "root_cause_of" in r


def _note(r, text):
    r.setdefault("judge_tier", r.get("tier"))
    r.setdefault("rule_notes", []).append(text)


def enforce(results):
    out = [dict(r) for r in results]
    by_id = {r.get("id"): r for r in out}
    # 1. root cause: follow root_cause_of to the root (max 10 steps, no cycles)
    for r in out:
        if not is_v2(r):
            continue
        seen, cur = {r.get("id")}, r
        while True:
            nxt = by_id.get(str(cur.get("root_cause_of") or "").strip())
            if nxt is None or nxt.get("id") in seen or len(seen) > 10:
                break
            seen.add(nxt.get("id"))
            cur = nxt
        if cur is not r:
            if cur.get("issue") != r.get("issue") or cur.get("tier") != r.get("tier"):
                _note(r, f"root cause {cur.get('id')}: issue {r.get('issue')}->{cur.get('issue')}, "
                         f"tier {r.get('tier')}->{cur.get('tier')}")
            r["issue"] = cur.get("issue")
            r["tier"] = cur.get("tier")
            r["symptom_of"] = cur.get("id")
    # 2. and 3. only on tier A (the root's tier, after rule 1)
    for r in out:
        if not is_v2(r) or r.get("tier") != "A":
            continue
        if r.get("holds_under_all_readings") is False:
            _note(r, "unstated premise: the error does not hold under every open reading: A->D")
            r["tier"] = "D"
        elif not flip_ok(r.get("flip")):
            _note(r, "materiality gate: no result flips: A->B")
            r["tier"] = "B"
    # a symptom follows its root again after rules 2 and 3
    for r in out:
        root = by_id.get(r.get("symptom_of"))
        if root is not None and root.get("tier") != r.get("tier"):
            _note(r, f"symptom of {root.get('id')}: tier {r.get('tier')}->{root.get('tier')}")
            r["tier"] = root.get("tier")
    return out
