"""Run one pipeline/exp.py stage until it finishes. Pause on usage limits and resume by itself.

Usage: python3 -I swarm/until_done.py <run_dir> -- python3 -I pipeline/exp.py <stage> --run <run_dir> ...
exp.py caches every finished call, so a rerun does only the missing calls. exp.py exits 3 when it stops at a
usage limit. Then this wrapper reads the meter every 10 minutes and starts exp.py again when five_hour < 0.30 and
seven_day < 0.95. Any other non-zero exit is retried after 60 s; the same exit 3 times in a row with no progress
(no new output file) ends the wrapper with exit 4 (blocked).
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "pipeline"))
import meter  # noqa: E402


def n_outputs(run):
    return sum(len([f for f in fs if f.endswith(".json") and not f.endswith(".in.json")]) for _, _, fs in os.walk(run))


def main():
    run, cmd = sys.argv[1], sys.argv[sys.argv.index("--") + 1:]
    same, last_rc = 0, None
    while True:
        before = n_outputs(run)
        stopped = os.path.join(run, "STOPPED")
        if os.path.exists(stopped):
            os.rename(stopped, stopped + f".{int(time.time())}")
        rc = subprocess.call(cmd)
        print(f"{time.strftime('%H:%M:%S')} exit {rc}", flush=True)
        if rc == 0:
            return 0
        progress = n_outputs(run) > before
        same = 1 if (rc != last_rc or progress) else same + 1
        last_rc = rc
        if same >= 3:
            print("BLOCKED: same exit 3 times without progress", flush=True)
            return 4
        if rc == 3:
            while True:
                time.sleep(600)
                m = meter.read()
                print(f"{time.strftime('%H:%M:%S')} paused, meter {m}", flush=True)
                if (m["five_hour"] or 0) < 0.30 and (m["seven_day"] or 0) < 0.95:
                    break
        else:
            time.sleep(60)


if __name__ == "__main__":
    sys.exit(main())
