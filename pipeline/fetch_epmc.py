"""Polite Europe PMC fetcher for open-access papers (a statistics corpus).

Usage:
  python3 -I fetch_epmc.py <data_dir> search --query Q --max 400      -> <data_dir>/candidates.json
  python3 -I fetch_epmc.py <data_dir> fetch [--max 400]                -> <data_dir>/papers/<oid>/paper.txt

Rules:
  - Search: Europe PMC REST API (www.ebi.ac.uk/europepmc/webservices/rest), meant for programmatic use.
    Full text: NCBI E-utilities efetch db=pmc (eutils.ncbi.nlm.nih.gov, the programmatic API; Europe PMC
    fullTextXML took 17-50 s per paper when we measured it). NCBI allows 3 requests/s without a key. One request at a time, at least GAP_S seconds apart. Generic User-Agent "paper-audit/0.1".
    No personal data in any request.
  - Only open-access articles with full text in Europe PMC (OPEN_ACCESS:y AND IN_EPMC:y).
  - Every response is cached under <data_dir>/cache/. A cached response is never fetched again.
  - Blinding: each paper goes to <data_dir>/papers/<oid>/ with an opaque id. The map from the opaque id to
    the PMCID, DOI and journal is <data_dir>/key.json. Model calls never see key.json.
  - The paper text has no title, author or journal line, so a model cannot look the paper up by name.
Downloaded XML is untrusted data. This script parses it with lxml and never executes it.
"""
import argparse, hashlib, http.client, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

from lxml import etree

UA = "paper-audit/0.1"
GAP_S = 0.6
BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest"
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
_last = [0.0]


def opaque(pmcid):
    return "q" + hashlib.sha1(("pmc:" + pmcid).encode()).hexdigest()[:8]


def get(url, cache_path):
    if os.path.exists(cache_path):
        return 200, open(cache_path, "rb").read()
    if os.path.exists(cache_path + ".err"):
        return int(open(cache_path + ".err").read() or 0), b""
    wait = GAP_S - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            body = r.read()
    except urllib.error.HTTPError as e:
        if e.code in (404, 400):
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            open(cache_path + ".err", "w").write(str(e.code))
        return e.code, b""
    except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as e:
        print(f"net error {url}: {e}", file=sys.stderr)
        return 0, b""
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    open(cache_path, "wb").write(body)
    return 200, body


def search(data, query, nmax):
    out, cursor, page = [], "*", 0
    while len(out) < nmax:
        q = urllib.parse.urlencode({"query": query, "format": "json", "pageSize": 100, "resultType": "lite",
                                    "cursorMark": cursor})
        st, body = get(f"{BASE}/search?{q}", os.path.join(data, "cache", "search",
                                                          hashlib.sha1((query + cursor).encode()).hexdigest() + ".json"))
        if st != 200:
            print(f"search HTTP {st}", file=sys.stderr)
            break
        d = json.loads(body)
        rs = d.get("resultList", {}).get("result", [])
        for r in rs:
            if r.get("pmcid"):
                out.append({k: r.get(k) for k in ("pmcid", "doi", "journalTitle", "pubYear", "title")})
        page += 1
        nxt = d.get("nextCursorMark")
        if not rs or not nxt or nxt == cursor:
            break
        cursor = nxt
    return out[:nmax]


# ---------------------------------------------------------------- JATS to plain text
def text_of(el):
    """Text of an element. Superscripts and subscripts are kept inline (chi<sup>2</sup> -> chi2)."""
    s = "".join(el.itertext())
    return re.sub(r"[ \t\r\f\v]+", " ", s).strip()


def table_text(tw):
    rows = []
    cap = tw.find(".//caption")
    lab = tw.find("label")
    head = " ".join(x for x in [text_of(lab) if lab is not None else "", text_of(cap) if cap is not None else ""] if x)
    for tr in tw.iter("tr"):
        cells = [text_of(c) for c in tr if c.tag in ("td", "th")]
        if cells:
            rows.append(" | ".join(cells))
    foot = tw.find(".//table-wrap-foot")
    out = [head, "[TABLE]"] + rows + ["[/TABLE]"]
    if foot is not None:
        out.append(text_of(foot))
    return "\n".join(x for x in out if x)


def body_text(sec, depth=2):
    out = []
    for ch in sec:
        tag = ch.tag if isinstance(ch.tag, str) else ""
        if tag == "title":
            out.append("#" * depth + " " + text_of(ch))
        elif tag == "p":
            # Tables inside a paragraph: print the paragraph text without them, then the tables.
            tws = ch.findall(".//table-wrap")
            for tw in tws:
                tw.getparent().remove(tw)
            out.append(text_of(ch))
            out += [table_text(tw) for tw in tws]
        elif tag == "sec":
            out.append(body_text(ch, min(depth + 1, 6)))
        elif tag == "table-wrap":
            out.append(table_text(ch))
        elif tag == "table-wrap-group":
            out += [table_text(tw) for tw in ch.iter("table-wrap")]
        elif tag in ("list",):
            out += ["- " + text_of(li) for li in ch.iter("list-item")]
        elif tag in ("disp-formula",):
            out.append(text_of(ch))
        elif tag == "fig":
            cap = ch.find(".//caption")
            if cap is not None:
                out.append("[FIGURE] " + text_of(cap))
    return "\n\n".join(x for x in out if x)


def jats_to_text(xml):
    root = etree.fromstring(xml, parser=etree.XMLParser(resolve_entities=False, no_network=True, huge_tree=True))
    art = root if root.tag == "article" else root.find(".//article")
    if art is None:
        return None, []
    parts = []
    ab = art.find(".//front//abstract")
    if ab is not None:
        parts.append("###### Abstract\n\n" + body_text(ab, 3))
    body = art.find("body")
    if body is None:
        return None, []
    parts.append(body_text(body, 2))
    back = art.find("back")
    if back is not None:  # appendices and supplementary tables, but no reference list
        for ch in back:
            if ch.tag in ("app-group", "app", "sec"):
                parts.append(body_text(ch, 2))
    refs = []
    for r in art.iter("ref"):
        dois = [text_of(x) for x in r.iter("pub-id") if x.get("pub-id-type") == "doi"]
        refs.append({"text": text_of(r)[:600], "dois": dois})
    return "\n\n".join(p for p in parts if p), refs


def fetch(data, nmax):
    cands = json.load(open(os.path.join(data, "candidates.json")))
    keyp = os.path.join(data, "key.json")
    key = json.load(open(keyp)) if os.path.exists(keyp) else {}
    n_ok = 0
    for c in cands[:nmax]:
        pmcid = c["pmcid"]
        oid = opaque(pmcid)
        pdir = os.path.join(data, "papers", oid)
        if os.path.exists(os.path.join(pdir, "paper.txt")):
            n_ok += 1
            continue
        cp = os.path.join(data, "cache", "xml", pmcid + ".xml")
        if os.path.exists(cp):
            st, body = get("", cp)
        else:  # NCBI E-utilities efetch (programmatic API, <= 3 requests/s without a key); same JATS XML.
            st, body = get(f"{EFETCH}?db=pmc&id={pmcid[3:]}&tool=paper-audit", cp)
        if st != 200:
            print(f"{pmcid}: HTTP {st}", file=sys.stderr)
            continue
        try:
            txt, refs = jats_to_text(body)
        except etree.XMLSyntaxError as e:
            print(f"{pmcid}: bad XML {e}", file=sys.stderr)
            continue
        if not txt or len(txt) < 8000:
            print(f"{pmcid}: no body text", file=sys.stderr)
            continue
        os.makedirs(pdir, exist_ok=True)
        open(os.path.join(pdir, "paper.txt"), "w", encoding="utf-8").write(txt)
        json.dump(refs, open(os.path.join(pdir, "refs.json"), "w"))
        key[oid] = c
        n_ok += 1
        json.dump(key, open(keyp, "w"), indent=1)
        print(f"{oid} {pmcid} {len(txt)} chars", flush=True)
    print(f"papers with text: {n_ok}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("cmd", choices=["search", "fetch"])
    ap.add_argument("--query", action="append", default=[])
    ap.add_argument("--max", type=int, default=400)
    a = ap.parse_args()
    os.makedirs(a.data, exist_ok=True)
    if a.cmd == "search":
        allc, seen = [], set()
        per = max(1, a.max // max(1, len(a.query)))
        for q in a.query:
            for c in search(a.data, q, per):
                if c["pmcid"] not in seen:
                    seen.add(c["pmcid"]); allc.append(c)
        json.dump(allc, open(os.path.join(a.data, "candidates.json"), "w"), indent=1)
        print(f"candidates: {len(allc)}")
    else:
        fetch(a.data, a.max)


if __name__ == "__main__":
    main()
