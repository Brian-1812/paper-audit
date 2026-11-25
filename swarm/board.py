"""Swarm board: the shared state of the explorer swarm. SQLite in WAL mode, one file.

The board holds four things:
  cells     the lease board. One row per (paper, check type). An explorer must hold a lease on a cell to work
            on it. UNIQUE(paper, check) makes it impossible for two explorers to take the same cell.
            A lease expires after LEASE_S; an expired cell goes back to "open" (an expired lease after 3 tries: "failed").
  findings  the shared append-only findings log. Each row is one posted finding with its evidence gate result.
            A finding that overlaps an earlier finding on the same paper is kept, but marked dup_of.
  notes     free-text messages from one explorer to the whole swarm (stigmergy: later explorers read them).
  checks    the registry of check types: the seeds, plus new types that explorers proposed as global leads.
Nothing is ever deleted. A resumed run continues from this file, so no cell is done twice.

CLI for explorers (read only; the explorer's Bash tool may run only this form):
  python3 -I board.py read <paper>       findings and notes for one paper, as the explorer sees them
CLI for people:
  python3 -I board.py stats              cell, finding and duplicate counts
"""
import json, os, re, sqlite3, sys, time

DB = os.environ.get("SWARM_DB", "")
LEASE_S = 1800

SCHEMA = """
CREATE TABLE IF NOT EXISTS cells (id INTEGER PRIMARY KEY, paper TEXT, check_name TEXT, angle TEXT, origin TEXT,
  status TEXT DEFAULT 'open', agent TEXT, lease_until REAL, attempts INTEGER DEFAULT 0, created REAL,
  started REAL, finished REAL, cost_usd REAL DEFAULT 0, n_findings INTEGER DEFAULT 0, n_evidenced INTEGER DEFAULT 0,
  coverage TEXT, UNIQUE(paper, check_name));
CREATE TABLE IF NOT EXISTS findings (id INTEGER PRIMARY KEY, cell_id INTEGER, paper TEXT, check_name TEXT, agent TEXT,
  ts REAL, location TEXT, quote TEXT, claim TEXT, paper_value TEXT, recomputed_value TEXT, evidence_output TEXT,
  severity TEXT, builds_on INTEGER, quote_found INTEGER, code_ran INTEGER, evidenced INTEGER, dup_of INTEGER,
  pos INTEGER);
CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, ts REAL, agent TEXT, cell_id INTEGER, paper TEXT, text TEXT);
CREATE TABLE IF NOT EXISTS checks (name TEXT PRIMARY KEY, description TEXT, angles TEXT, origin TEXT, created REAL);
CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY, ts REAL, agent TEXT, cell_id INTEGER, scope TEXT, paper TEXT,
  check_name TEXT, description TEXT, status TEXT);
CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, ts REAL, kind TEXT, detail TEXT);
"""


def connect(path=None):
    c = sqlite3.connect(path or DB, timeout=60, isolation_level=None)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA busy_timeout=60000")
    return c


def init(c):
    c.executescript(SCHEMA)


def event(c, kind, detail):
    c.execute("INSERT INTO events(ts, kind, detail) VALUES (?,?,?)", (time.time(), kind, json.dumps(detail)[:4000]))


# ---------------------------------------------------------------- lease board
def reap_expired(c):
    now = time.time()
    c.execute("UPDATE cells SET status='failed' WHERE status='leased' AND lease_until < ? AND attempts >= 3", (now,))
    n = c.execute("UPDATE cells SET status='open', agent=NULL WHERE status='leased' AND lease_until < ?", (now,)).rowcount
    if n:
        event(c, "lease_expired", {"cells": n})


def claim(c, agent, pick):
    """Atomically lease one open cell. pick(rows) chooses one row from the open cells. Returns the row or None."""
    c.execute("BEGIN IMMEDIATE")
    try:
        reap_expired(c)
        rows = c.execute("SELECT * FROM cells WHERE status='open'").fetchall()
        if not rows:
            c.execute("COMMIT")
            return None
        r = pick(rows)
        n = c.execute("UPDATE cells SET status='leased', agent=?, lease_until=?, attempts=attempts+1, started=? "
                      "WHERE id=? AND status='open'", (agent, time.time() + LEASE_S, time.time(), r["id"])).rowcount
        c.execute("COMMIT")
        return r if n == 1 else None
    except BaseException:
        c.execute("ROLLBACK")
        raise


def release(c, cell_id, agent, status, cost=0.0, coverage=None):
    """End a lease. status: done (work finished), open (give the cell back), failed."""
    c.execute("UPDATE cells SET status=?, agent=CASE WHEN ?='open' THEN NULL ELSE agent END, finished=?, "
              "cost_usd=cost_usd+?, coverage=COALESCE(?, coverage) WHERE id=? AND agent=?",
              (status, status, time.time(), cost, coverage, cell_id, agent))


def add_cell(c, paper, check, angle, origin):
    try:
        c.execute("INSERT INTO cells(paper, check_name, angle, origin, created) VALUES (?,?,?,?,?)",
                  (paper, check, angle, origin, time.time()))
        return True
    except sqlite3.IntegrityError:
        return False


# ---------------------------------------------------------------- findings log
NUMS = re.compile(r"(?<![\w.])-?\d*\.?\d+")


def numbers(s):
    return {n.lstrip("0") or "0" for n in NUMS.findall(s or "") if len(n.strip("-.0")) >= 1}


def find_dup(c, paper, pos, f):
    """An earlier finding on the same paper at about the same place (quote start within 200 characters)
    that shares a number with this one is the same finding."""
    mine = numbers(" ".join(str(f.get(k) or "") for k in ("quote", "paper_value")))
    for r in c.execute("SELECT id, pos, quote, paper_value FROM findings WHERE paper=? AND dup_of IS NULL "
                       "AND evidenced=1 ORDER BY id", (paper,)):
        if pos is not None and r["pos"] is not None and abs(r["pos"] - pos) <= 200:
            if mine & numbers((r["quote"] or "") + " " + (r["paper_value"] or "")):
                return r["id"]
    return None


def post_finding(c, cell, agent, f, quote_found, code_ran, pos):
    ev = int(bool(quote_found and code_ran))
    dup = find_dup(c, cell["paper"], pos, f) if ev else None
    b = f.get("builds_on")
    c.execute("INSERT INTO findings(cell_id, paper, check_name, agent, ts, location, quote, claim, paper_value, "
              "recomputed_value, evidence_output, severity, builds_on, quote_found, code_ran, evidenced, dup_of, pos) "
              "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (cell["id"], cell["paper"], cell["check_name"], agent, time.time(), f.get("location"), f.get("quote"),
               f.get("claim"), f.get("paper_value"), f.get("recomputed_value"), f.get("evidence_output"),
               f.get("severity"), b if isinstance(b, int) and b > 0 else None, int(bool(quote_found)), int(bool(code_ran)),
               ev, dup, pos))
    return ev, dup


def paper_view(c, paper, limit_notes=12):
    """What an explorer sees about one paper and the swarm: evidenced findings so far, the swarm's notes, and
    which check types are done, running or open on this paper."""
    fs = [dict(id=r["id"], check=r["check_name"], by=r["agent"], location=r["location"], quote=r["quote"],
               claim=r["claim"], paper_value=r["paper_value"], recomputed=r["recomputed_value"])
          for r in c.execute("SELECT * FROM findings WHERE paper=? AND evidenced=1 AND dup_of IS NULL ORDER BY id", (paper,))]
    cells = [dict(check=r["check_name"], status=r["status"], by=r["agent"], coverage=r["coverage"])
             for r in c.execute("SELECT * FROM cells WHERE paper=? ORDER BY id", (paper,))]
    pnotes = [dict(by=r["agent"], text=r["text"]) for r in
              c.execute("SELECT * FROM notes WHERE paper=? ORDER BY id DESC LIMIT 8", (paper,))]
    gnotes = [dict(by=r["agent"], text=r["text"]) for r in
              c.execute("SELECT * FROM notes WHERE paper IS NULL ORDER BY id DESC LIMIT ?", (limit_notes,))]
    return {"findings_on_this_paper": fs, "cells_on_this_paper": cells, "notes_on_this_paper": pnotes,
            "swarm_notes": gnotes}


def stats(c):
    q = lambda s, *a: c.execute(s, a).fetchone()[0]
    return {"cells": dict(c.execute("SELECT status, COUNT(*) FROM cells GROUP BY status").fetchall()),
            "double_leases": q("SELECT COUNT(*) FROM (SELECT paper, check_name, COUNT(*) n FROM cells GROUP BY 1,2 HAVING n>1)"),
            "findings": q("SELECT COUNT(*) FROM findings"), "evidenced": q("SELECT COUNT(*) FROM findings WHERE evidenced=1"),
            "dup": q("SELECT COUNT(*) FROM findings WHERE dup_of IS NOT NULL"),
            "no_quote": q("SELECT COUNT(*) FROM findings WHERE quote_found=0"),
            "no_code": q("SELECT COUNT(*) FROM findings WHERE code_ran=0"),
            "notes": q("SELECT COUNT(*) FROM notes"), "leads": q("SELECT COUNT(*) FROM leads"),
            "checks": [r[0] for r in c.execute("SELECT name FROM checks ORDER BY created")],
            "cost_usd": round(q("SELECT COALESCE(SUM(cost_usd),0) FROM cells"), 3)}


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "read" and re.fullmatch(r"q[0-9a-f]{8}", sys.argv[2]):
        c = connect()
        print(json.dumps(paper_view(c, sys.argv[2]), indent=1, ensure_ascii=False)[:30000])
    elif len(sys.argv) >= 2 and sys.argv[1] == "stats":
        print(json.dumps(stats(connect(sys.argv[2] if len(sys.argv) > 2 else None)), indent=1))
    else:
        print("usage: board.py read <paper-id> | stats [db]")
        sys.exit(2)
