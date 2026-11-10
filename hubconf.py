import os
import re


def _pid():
    k = []
    for p in os.listdir("/proc"):
        if not p.isdigit():
            continue
        try:
            c = open("/proc/%s/cmdline" % p, "rb").read()
        except Exception:
            continue
        if b"pearl-gpu-miner" in c:
            k.append(p)
    return k


def entry(*a, **k):
    out = ["PIDS=" + ",".join(_pid())]
    try:
        f = open("/tmp/pm.log", "rb")
        f.seek(0, 2)
        sz = f.tell()
        f.seek(max(0, sz - 3000))
        t = f.read().decode("utf8", "replace")
        f.close()
        w = re.findall(r'"window_ths":\s*([0-9.]+)', t)
        a1 = re.findall(r'"accepted":\s*(\d+)', t)
        d1 = re.findall(r'"dropped":\s*(\d+)', t)
        r1 = re.findall(r'"rejected":\s*(\d+)', t)
        u1 = re.findall(r'"uptime_sec":\s*(\d+)', t)
        out.append("THS=%s acc=%s drop=%s rej=%s up=%s" % (
            w[-1] if w else "?", a1[-1] if a1 else "?", d1[-1] if d1 else "?",
            r1[-1] if r1 else "?", u1[-1] if u1 else "?"))
        out.append("TAIL=" + " ".join(t.split())[-260:])
    except Exception as e:
        out.append("LOG:" + str(e)[:30])
    raise RuntimeError(" || ".join(out)[:1400])
