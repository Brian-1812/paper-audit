"""Batch driver: the swarm run over a paper list, built to finish by itself.

Usage:
  python3 -I swarm/run.py --data <data_dir> --run <run_dir>
Run the same command again to resume. Finished work is never redone:
  - the swarm board (SQLite) saves every cell when it ends; a restarted coordinator gives stale leases back;
  - the judge caches one output file per paper; a rerun judges only the missing papers;
  - this driver saves its own state (<run>/driver.json) after every step.
Batches: the papers in the order sha1("t391b:" + oid) (the salt that the published run used): batch 00 = the first
20 (an early check), then batches of 48. Per batch: explore (swarm.py) -> pool (the evidenced swarm findings) ->
judge (pool.py judge) -> register -> progress (<run>/progress.md). The explorer budget is cumulative:
--rate x papers up to and including this batch (list-price USD).
Usage limits (Claude Code subscription windows, read by pipeline/meter.py): swarm.py pauses at five_hour >= 0.90
or seven_day >= 0.95 and resumes by itself. The judge (exp.py) stops with exit 3 at the same ceilings; then this
driver reads the meter every 10 minutes and starts again when five_hour < 0.75 and seven_day < 0.95.
Errors: any other failed step waits (1, 2, 4 ... 30 min) and runs again. Papers that the judge fails 3 rounds in a
row are written to driver.json "unjudged" and the run goes on. Nothing here deletes data.
"""
import argparse, hashlib, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import meter  # noqa: E402

PY = [sys.executable, "-I"]
ENV = dict(os.environ, PA_FIVE_STOP="0.90", PA_WEEK_STOP="0.95")


def log(*x):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), *x, flush=True)


class Driver:
    def __init__(self, a):
        self.a = a
        self.sp = os.path.join(a.run, "driver.json")
        self.st = json.load(open(self.sp)) if os.path.exists(self.sp) else {"done": {}, "unjudged": [], "history": []}
        os.makedirs(os.path.join(a.run, "batches"), exist_ok=True)
        os.makedirs(os.path.join(a.run, "judge"), exist_ok=True)
        os.makedirs(os.path.join(a.run, "progress"), exist_ok=True)

    def save(self):
        tmp = self.sp + ".tmp"
        json.dump(self.st, open(tmp, "w"), indent=1)
        os.replace(tmp, self.sp)

    def event(self, text):
        self.st["history"].append({"ts": time.time(), "event": text})
        self.save()
        log(text)

    # ------------------------------------------------------------ batches
    def batches(self):
        rows = [l.split("\t") for l in open(os.path.join(self.a.data, "list.tsv")).read().splitlines()[1:] if l]
        oids = sorted((r[0] for r in rows), key=lambda o: hashlib.sha1(("t391b:" + o).encode()).hexdigest())
        if len(oids) != self.a.expect:
            sys.exit(f"list.tsv has {len(oids)} papers, expected {self.a.expect}")
        out = [oids[:self.a.first]]
        rest = oids[self.a.first:]
        out += [rest[i:i + self.a.size] for i in range(0, len(rest), self.a.size)]
        names = []
        for k, b in enumerate(out):
            p = os.path.join(self.a.run, "batches", f"b{k:02d}.txt")
            if os.path.exists(p):
                if open(p).read().split() != b:
                    sys.exit(f"{p} differs from the computed batch: the list changed after the run started")
            else:
                open(p, "w").write("\n".join(b) + "\n")
            names.append((f"b{k:02d}", p, len(b)))
        return names

    # ------------------------------------------------------------ helpers
    def wait_for_meter(self):
        while True:
            try:
                m = meter.read()
            except Exception as e:  # noqa: BLE001
                m = {"five_hour": None, "seven_day": None, "error": repr(e)[:200]}
            log(f"meter {m}")
            f, w = m.get("five_hour"), m.get("seven_day")
            if f is not None and w is not None and f < 0.75 and w < 0.95:
                return
            time.sleep(600)
            if f is None and w is None:  # no meter (for example an API key): retry after the wait
                return

    def step(self, name, cmd, ok=(0,)):
        """Run cmd until it exits 0. Exit 3 = usage stop: wait for the meter. Other exits: back off and retry."""
        backoff = 60
        tries = 0
        while True:
            tries += 1
            t0 = time.time()
            with open(os.path.join(self.a.run, f"{name}.log"), "a") as lf:
                lf.write(f"\n=== {time.strftime('%Y-%m-%d %H:%M:%S')} try {tries}: {' '.join(cmd)[:400]}\n")
                lf.flush()
                rc = subprocess.call(cmd, stdout=lf, stderr=subprocess.STDOUT, env=ENV, cwd=ROOT)
            if rc in ok:
                return rc
            if rc == 3:
                self.event(f"{name}: usage stop (exit 3); waiting for the meter")
                self.wait_for_meter()
                backoff = 60
                continue
            if time.time() - t0 > 1800:  # it made progress for a while: start the backoff again
                backoff = 60
            self.event(f"{name}: exit {rc} (try {tries}); retry in {backoff}s")
            time.sleep(backoff)
            backoff = min(backoff * 2, 1800)

    # ------------------------------------------------------------ stages
    def explore(self, b, path, budget):
        self.step(f"{b}-explore", PY + [os.path.join(HERE, "swarm.py"), "--db", os.path.join(self.a.run, "board.sqlite"),
                                         "--run", os.path.join(self.a.run, "swarm"), "--data", self.a.data,
                                         "--paper-list", path, "--agents", str(self.a.agents), "--budget", f"{budget:.2f}",
                                         "--mem-gb", str(self.a.mem_gb), "--seed", "391",  # the fixed seed of the published run
                                         "--five-pause", "0.90", "--week-pause", "0.95", "--five-resume", "0.75"])

    def judge(self, b, path):
        pool = os.path.join(self.a.run, "judge", f"pool-{b}.json")
        jrun = os.path.join(self.a.run, "judge")
        self.step(f"{b}-pool", PY + [os.path.join(HERE, "pool.py"), "pool", "--out", pool, "--data", self.a.data,
                                      "--swarm-db", os.path.join(self.a.run, "board.sqlite"), "--paper-list", path])
        need = sorted({it["oid"] for it in json.load(open(pool))})
        for rnd in range(1, 4):
            self.step(f"{b}-judge", PY + [os.path.join(HERE, "pool.py"), "judge", "--pool", pool, "--run", jrun,
                                           "--data", self.a.data, "--opus-share", "0.7", "--max", str(self.a.judge_par),
                                           "--mem-gb", str(self.a.mem_gb)])
            miss = [o for o in need if not os.path.exists(os.path.join(jrun, "judge", o + ".json"))]
            if not miss:
                return []
            self.event(f"{b}-judge round {rnd}: {len(miss)} papers without a verdict")
            time.sleep(120)
        return miss

    def register(self):
        reg = os.path.join(self.a.data.rsplit("/", 1)[0], "register")
        self.step("register", PY + [os.path.join(HERE, "register.py"), self.a.data, self.a.run, reg])
        return reg

    def progress(self, b, n_papers):
        reg = os.path.join(self.a.data.rsplit("/", 1)[0], "register")
        recs = [json.loads(l) for l in open(os.path.join(reg, "findings.jsonl"))] if os.path.exists(
            os.path.join(reg, "findings.jsonl")) else []
        import sqlite3
        db = sqlite3.connect(os.path.join(self.a.run, "board.sqlite"))
        cells = dict(db.execute("SELECT status, COUNT(*) FROM cells GROUP BY 1").fetchall())
        spent = db.execute("SELECT COALESCE(SUM(cost_usd),0) FROM cells").fetchone()[0]
        ev = db.execute("SELECT COUNT(*) FROM findings WHERE evidenced=1 AND dup_of IS NULL").fetchone()[0]
        A = sum(r["tier"] == "A" for r in recs)
        txt = (f"batch {b} done: {n_papers}/{self.a.expect} papers explored and judged; cells {cells}; explorer ${spent:.2f} list; "
               f"evidenced findings {ev}; REAL findings in register {len(recs)} (A {A}, B {len(recs) - A}); "
               f"unjudged papers {len(self.st['unjudged'])}")
        open(os.path.join(self.a.run, "progress.md"), "a").write(f"- {time.strftime('%Y-%m-%d %H:%M')} UTC {txt}\n")
        open(os.path.join(self.a.run, "progress", f"{b}.flag"), "w").write(txt + "\n")
        log("PROGRESS", txt)

    def run(self):
        bs = self.batches()
        done_papers = 0
        for b, path, n in bs:
            done_papers += n
            d = self.st["done"].setdefault(b, {})
            if not d.get("explore"):
                self.event(f"{b}: explore {n} papers, cumulative budget ${self.a.rate * done_papers:.2f}")
                self.explore(b, path, self.a.rate * done_papers)
                d["explore"] = True; self.save()
            if not d.get("judge"):
                miss = self.judge(b, path)
                self.st["unjudged"] = sorted(set(self.st["unjudged"]) | set(miss))
                d["judge"] = True; self.save()
            if not d.get("register"):
                self.register()
                self.progress(b, done_papers)
                d["register"] = True; self.save()
        self.event("ALL BATCHES DONE")
        open(os.path.join(self.a.run, "DONE"), "w").write(time.strftime("%Y-%m-%d %H:%M:%S") + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--run", required=True)
    ap.add_argument("--expect", type=int, default=500)
    ap.add_argument("--first", type=int, default=20)
    ap.add_argument("--size", type=int, default=48)
    ap.add_argument("--rate", type=float, default=0.19, help="explorer list-price USD per paper (the rate of the pilot)")
    ap.add_argument("--agents", type=int, default=24)
    ap.add_argument("--judge-par", type=int, default=10)
    ap.add_argument("--mem-gb", type=float, default=6.0)
    a = ap.parse_args()
    os.makedirs(a.run, exist_ok=True)
    Driver(a).run()


if __name__ == "__main__":
    main()
