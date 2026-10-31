# -*- coding: utf-8 -*-
"""验收 a：kai 目明篇开新档 -> 开跳过文字:全部 -> 点跳过 -> 观察 OP 处快进是否自动关。"""
import os, subprocess, sys, time
ADB = [r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\docker-android\platform-tools\adb.exe", "-s", "localhost:5555"]
SHOT = r"D:\zz_shot"
os.makedirs(SHOT, exist_ok=True)
def sh(*a, **kw):
    return subprocess.run(ADB + list(a), capture_output=True, timeout=kw.pop("timeout", 180))
def tap(x, y, wait=1.0):
    sh("shell", "input", "tap", str(x), str(y)); time.sleep(wait)
def shot(name):
    p = os.path.join(SHOT, name + ".png")
    with open(p, "wb") as f:
        f.write(sh("exec-out", "screencap", "-p", timeout=120).stdout)
    print("shot", p); return p
def log():
    out = sh("logcat", "-d", "-s", "python:I", "Ren'Py:I", timeout=60).stdout.decode("utf-8", "replace")
    return [l for l in out.splitlines() if "ZZOP" in l][-12:]

PKG = "com.ps3.higurashi_kai"
sh("shell", "am", "force-stop", PKG)
sh("shell", "logcat", "-c")
sh("shell", "monkey", "-p", PKG, "-c", "android.intent.category.LAUNCHER", "1")
time.sleep(40)
shot("a01_main")
# 开始游戏
tap(850, 496, 8); shot("a02_chaptersel")
# 目明篇 第一行
tap(850, 456, 6); shot("a03_modeprompt")
# 使用（跳关）? -> 我们要开新档：选“不使用” (1520,864)
tap(1520, 864, 10); shot("a04_story")
print("ZZOP lines:", log())
