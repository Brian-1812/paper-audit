"""Run one short Python check in a sandbox. The judge model may run only this command.

Usage:  python3 -I /abs/pipeline/sbx.py '<python code>'
        python3 -I /abs/pipeline/sbx.py --selftest

The code runs in new network, mount, PID and IPC namespaces (no network interface except lo, which is down),
as user nobody, with no new privileges. /root, /srv, /home, /tmp, /var and /mnt are hidden under empty
tmpfs mounts. The only extra paths are a read-only copy of sympy, mpmath and numpy (SBX_SITE) and the runner.
Limits: 1 GiB address space, 30 s CPU, 64 processes, 5 MB files, 60 s wall time, 20,000 characters of output.
Every call is logged (code, exit code, output) to the file in $SBX_LOG, so the pipeline can check that a
reported calculation really ran and can run it again.
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get("SBX_SITE", os.path.join(os.path.dirname(HERE), "sandbox", "site"))
RUNNER = r'''
import sys, io, contextlib, traceback, resource
sys.path.insert(0, "/run/sbx/site")
src = sys.stdin.read()
g = {"__name__": "__main__"}
try:
    exec(compile(src, "<check>", "exec"), g)
except SystemExit:
    pass
except BaseException:
    traceback.print_exc(limit=3)
    sys.exit(1)
'''
SETUP = r'''
set -e
mount -t tmpfs -o size=64m,mode=755 tmpfs /run
mkdir -p /run/sbx/site /run/sbx/w
mount --bind "$SITE" /run/sbx/site
mount -o remount,bind,ro /run/sbx/site
printf '%s' "$RUNNER" > /run/sbx/runner.py
chmod 755 /run/sbx; chmod 644 /run/sbx/runner.py; chmod 1777 /run/sbx/w
for d in /root /srv /home /tmp /var /mnt /opt /media; do [ -d "$d" ] && mount -t tmpfs -o size=8m,mode=755 tmpfs "$d"; done
mount -t proc proc /proc
cd /run/sbx/w
exec setpriv --reuid=65534 --regid=65534 --clear-groups --no-new-privs --inh-caps=-all --bounding-set=-all \
  prlimit --as=1073741824 --cpu=30 --nproc=64 --fsize=5000000 --core=0 \
  env -i PATH=/usr/bin:/bin HOME=/run/sbx/w OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  timeout -s KILL 60 python3 -I /run/sbx/runner.py
'''
MAX_OUT = 20000


def run(code):
    env = {"PATH": "/usr/sbin:/usr/bin:/sbin:/bin", "SITE": SITE, "RUNNER": RUNNER}
    t0 = time.time()
    p = subprocess.run(["unshare", "--net", "--mount", "--pid", "--ipc", "--uts", "--fork", "--kill-child",
                        "--propagation", "private", "/bin/sh", "-c", SETUP],
                       input=code, capture_output=True, text=True, env=env, timeout=90)
    out = (p.stdout + ("\n[stderr]\n" + p.stderr if p.stderr.strip() else ""))
    if len(out) > MAX_OUT:
        out = out[:MAX_OUT] + "\n[output cut at 20000 characters]"
    return p.returncode, out, round(time.time() - t0, 2)


def log(code, rc, out, secs):
    path = os.environ.get("SBX_LOG")
    if path:
        with open(path, "a") as f:
            f.write(json.dumps({"ts": time.time(), "code": code, "rc": rc, "out": out, "secs": secs}) + "\n")


SELFTEST = [
    ("import sympy as sp; x=sp.Symbol('x'); print(sp.integrate(x**2,(x,0,3)))", "9"),
    ("import numpy as np; print(round(float(np.mean([1,2,3,4])),2))", "2.5"),
    ("import socket\ntry:\n socket.create_connection(('1.1.1.1',80),timeout=3); print('NET-OPEN')\nexcept OSError as e: print('no-net')", "no-net"),
    ("import os; print(sorted(os.listdir('/root')), os.getuid())", "[] 65534"),
    ("import os\ntry:\n open('/etc/shadow').read(); print('READ')\nexcept OSError: print('denied')", "denied"),
    ("x=bytearray(2*1024**3)", "MemoryError"),
]


def main():
    args = sys.argv[1:]
    if args == ["--selftest"]:
        bad = 0
        for code, want in SELFTEST:
            rc, out, secs = run(code)
            ok = want in out
            bad += not ok
            print("PASS" if ok else "FAIL", repr(code[:50]), "->", out.strip()[-120:], f"({secs}s)")
        sys.exit(1 if bad else 0)
    if not args:
        print("usage: sbx.py '<python code>'"); sys.exit(2)
    code = "\n".join(args)
    rc, out, secs = run(code)
    log(code, rc, out, secs)
    print(out if out.strip() else "(no output; use print())")
    print(f"[exit {rc}]")


if __name__ == "__main__":
    main()
