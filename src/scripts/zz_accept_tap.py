# -*- coding: utf-8 -*-
"""连续点击推进剧情，实时抓 ZZOP 日志 + 截图。用于到达目明篇序章末尾的 OP 锚点。"""
import os, subprocess, sys, time
ADB = [r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\docker-android\platform-tools\adb.exe", "-s", "localhost:5555"]
SHOT = r"D:\zz_shot"
os.makedirs(SHOT, exist_ok=True)
def sh(*a, timeout=120):
    return subprocess.run(ADB + list(a), capture_output=True, timeout=timeout)
def tap(x=1520, y=1000):
    sh("shell", "input", "tap", str(x), str(y))
def shot(name):
    with open(os.path.join(SHOT, name + ".png"), "wb") as f:
        f.write(sh("exec-out", "screencap", "-p").stdout)
def zzop():
    out = sh("logcat", "-d", timeout=90).stdout.decode("utf-8", "replace")
    return [l.strip() for l in out.splitlines() if "ZZOP" in l]

start = time.time()
last = len(zzop())
for i in range(150):
    tap()
    time.sleep(1.6)
    if i % 10 == 9:
        lines = zzop()
        if len(lines) != last:
            print("NEW ZZOP:", lines[-3:])
            last = len(lines)
            shot("a05_at_op_%d" % i)
        if i % 30 == 29:
            shot("a06_progress_%d" % i)
            print("t=%.0fs lines=%d" % (time.time() - start, len(lines)))
    if time.time() - start > 260:
        break
print("FINAL ZZOP:", zzop()[-5:])
shot("a07_end")
