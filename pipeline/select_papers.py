"""Paper selection: 500 open-access papers, 100 from each of 5 fields with no active automated checker.

Usage (network step, polite, cached):
  python3 -I pipeline/select_papers.py <data_dir> search                -> <data_dir>/candidates_v2/<field>.json (frozen)
  python3 -I pipeline/select_papers.py <data_dir> select <field> [...]  -> papers/, selection_v2/<field>.json
  python3 -I pipeline/select_papers.py <data_dir> finalize              -> key.json, list.tsv
Two select processes may run at the same time on different fields (each keeps >= 0.6 s between its requests, so
the total stays under NCBI's 3 requests/s without a key).
The rule is in selection/rule.md. Short form:
  1. Candidates: for each journal of a field, the Europe PMC query
       JOURNAL:"<j>" AND OPEN_ACCESS:y AND IN_EPMC:y AND (PUB_YEAR:2025 OR PUB_YEAR:2026)
       AND PUB_TYPE:"research-article"
     first PER_JOURNAL results in Europe PMC order. The union is frozen in candidates_v2/<field>.json on the
     first run and is never searched again (reproducible from that file).
  2. Order: sha1("t391:" + pmcid) ascending (the fixed salt of the published list), inside each field.
  3. In that order, fetch the JATS full text (NCBI efetch, cached) and keep a paper when its body text has
     >= 8000 characters and count_tests() finds >= 5 reported test statistics with a p-value (t, F, z, W, U, H,
     r or chi-square, optional df, "= value", then p within 60 characters, as in "F1,23 = 4.5, P = 0.03").
     v1 used psystat.py (APA format only) and kept 3.5% of ecology papers: these fields write tests differently.
  4. Stop a field at 100 kept papers.
Downloaded XML is untrusted data. It is parsed with lxml and never executed.
"""
import hashlib, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_epmc as F  # noqa: E402
import psystat  # noqa: E402

F.GAP_S = 0.75  # two parallel processes stay under 3 requests/s

FIELDS = {
    "ecology_environment": ["Ecol Evol", "BMC Ecol Evol", "Glob Chang Biol", "Insects"],
    "agri_food_vet": ["Animals (Basel)", "Front Vet Sci", "Poult Sci", "Foods"],
    "sports_exercise": ["Front Sports Act Living", "Sports (Basel)", "BMC Sports Sci Med Rehabil",
                        "J Funct Morphol Kinesiol"],
    "nursing_public_health": ["BMC Nurs", "Nurs Open", "BMC Public Health", "Front Public Health"],
    "wetlab_biology": ["Front Pharmacol", "Front Microbiol", "Microbiol Spectr", "Cells"],
}
PER_JOURNAL = 1500
PER_FIELD = 100
MIN_TESTS = 5
MIN_CHARS = 8000
FILTER = ' AND OPEN_ACCESS:y AND IN_EPMC:y AND (PUB_YEAR:2025 OR PUB_YEAR:2026) AND PUB_TYPE:"research-article"'


STAT = r"(?:\b[tFzZWUH]|χ2|χ²|X2|\bchi2|\bchi-squared?|\bKruskal-Wallis H|\br)"
DF = (r"(?:\s*\(\s*\d+(?:\.\d+)?(?:\s*,\s*\d+(?:\.\d+)?)?\s*\)|\s*\d{1,4}(?:\.\d+)?\s*,\s*\d{1,5}(?:\.\d+)?"
      r"|\s*\[\s*\d+[^\]]{0,12}\])?")
TEST_RX = re.compile(STAT + DF + r"\s*=\s*-?\d*\.?\d+[^.;\n]{0,60}?\b[Pp]\s*(?:-?value)?\s*[<=>≤≥]\s*0?\.\d+")


def count_tests(text):
    for a, b in (("−", "-"), ("–", "-"), ("\u2009", " "), ("\u00a0", " "), ("\u202f", " ")):
        text = text.replace(a, b)
    return len(TEST_RX.findall(text))


def order_key(pmcid):
    return hashlib.sha1(("t391:" + pmcid).encode()).hexdigest()


def search(data):
    os.makedirs(os.path.join(data, "candidates_v2"), exist_ok=True)
    for field, journals in FIELDS.items():
        out = os.path.join(data, "candidates_v2", field + ".json")
        if os.path.exists(out):
            print(f"{field}: frozen, {len(json.load(open(out))['candidates'])} candidates")
            continue
        seen, cands = set(), []
        for j in journals:
            q = f'JOURNAL:"{j}"' + FILTER
            for c in F.search(data, q, PER_JOURNAL):
                if c["pmcid"] not in seen:
                    seen.add(c["pmcid"])
                    cands.append(dict(c, query_journal=j))
        json.dump({"field": field, "journals": journals, "filter": FILTER, "per_journal": PER_JOURNAL,
                   "searched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "candidates": cands},
                  open(out, "w"), indent=1)
        print(f"{field}: {len(cands)} candidates frozen")


def select(data, fields):
    os.makedirs(os.path.join(data, "selection_v2"), exist_ok=True)
    for field in fields:
        cands = json.load(open(os.path.join(data, "candidates_v2", field + ".json")))["candidates"]
        cands.sort(key=lambda c: order_key(c["pmcid"]))
        selp = os.path.join(data, "selection_v2", field + ".json")
        st = json.load(open(selp)) if os.path.exists(selp) else {"kept": [], "seen": {}, "meta": {}}
        for c in cands:
            if len(st["kept"]) >= PER_FIELD:
                break
            pmcid = c["pmcid"]
            if pmcid in st["seen"]:
                continue
            oid = F.opaque(pmcid)
            cp = os.path.join(data, "cache", "xml", pmcid + ".xml")
            for k in range(6):  # network errors are not a property of the paper: wait and try again
                code, body = F.get("" if os.path.exists(cp) else
                                   f"{F.EFETCH}?db=pmc&id={pmcid[3:]}&tool=paper-audit", cp)
                if code != 0:
                    break
                time.sleep(30 * (k + 1))
            if code == 0:
                print(f"{pmcid}: network error 6 times; skip for now (not marked seen)", file=sys.stderr, flush=True)
                continue
            why, n, n_apa = None, 0, 0
            if code != 200:
                why = f"http {code}"
            else:
                try:
                    txt, refs = F.jats_to_text(body)
                except Exception as e:  # noqa: BLE001  (bad XML: skip the paper, keep going)
                    txt, refs, why = None, [], f"bad xml {type(e).__name__}"
                if not why and (not txt or len(txt) < MIN_CHARS):
                    why = "short or no body text"
                if not why:
                    n = count_tests(txt)
                    if n < MIN_TESTS:
                        why = f"{n} tests < {MIN_TESTS}"
            st["seen"][pmcid] = why or "kept"
            if why is None:
                n_apa = len(psystat.statcheck(txt))
                pdir = os.path.join(data, "papers", oid)
                os.makedirs(pdir, exist_ok=True)
                open(os.path.join(pdir, "paper.txt"), "w", encoding="utf-8").write(txt)
                json.dump(refs, open(os.path.join(pdir, "refs.json"), "w"))
                st["meta"][oid] = dict(c, field=field, n_tests=n, n_apa_tests=n_apa)
                st["kept"].append(oid)
                print(f"{field} {len(st['kept'])}/{PER_FIELD} {oid} {pmcid} tests {n} apa {n_apa}", flush=True)
            tmp = selp + ".tmp"
            json.dump(st, open(tmp, "w"), indent=1)
            os.replace(tmp, selp)
        print(f"{field}: kept {len(st['kept'])}, examined {len(st['seen'])}", flush=True)


def finalize(data):
    key, rows = {}, ["oid\tfield\tpmcid\tdoi\tjournal\tyear\tn_tests\tn_apa_tests"]
    for field in FIELDS:
        st = json.load(open(os.path.join(data, "selection_v2", field + ".json")))
        if len(st["kept"]) != PER_FIELD:
            sys.exit(f"{field}: {len(st['kept'])} kept, need {PER_FIELD}")
        for oid in st["kept"]:
            k = st["meta"][oid]
            key[oid] = k
            rows.append("\t".join(str(x) for x in (oid, field, k["pmcid"], k.get("doi") or "", k.get("journalTitle") or "",
                                                   k.get("pubYear") or "", k["n_tests"], k["n_apa_tests"])))
    if len(key) != PER_FIELD * len(FIELDS):
        sys.exit(f"{len(key)} distinct papers, need {PER_FIELD * len(FIELDS)}")
    json.dump(key, open(os.path.join(data, "key.json"), "w"), indent=1)
    open(os.path.join(data, "list.tsv"), "w").write("\n".join(rows) + "\n")
    print(f"list: {len(rows) - 1} papers -> {os.path.join(data, 'list.tsv')}")


if __name__ == "__main__":
    cmd = sys.argv[2]
    if cmd == "search":
        search(sys.argv[1])
    elif cmd == "select":
        select(sys.argv[1], sys.argv[3:] or list(FIELDS))
    else:
        finalize(sys.argv[1])
