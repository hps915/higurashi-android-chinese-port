# -*- coding: utf-8 -*-
"""稳健驱动：截图->ASCII->按阶段操作。每次操作后打印状态摘要。"""
import os, subprocess, sys, time
from PIL import Image
ADB = [r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\docker-android\platform-tools\adb.exe", "-s", "localhost:5555"]
SHOT = r"D:\zz_shot"
CH = " .:-=+*#%@"
os.makedirs(SHOT, exist_ok=True)

def sh(*a, timeout=180):
    return subprocess.run(ADB + list(a), capture_output=True, timeout=timeout)

def shot(name):
    p = os.path.join(SHOT, name + ".png")
    with open(p, "wb") as f:
        f.write(sh("exec-out", "screencap", "-p").stdout)
    return p

def ascii_of(p, w=60, h=22):
    im = Image.open(p).convert("L").resize((w, h))
    px = list(im.getdata())
    rows = []
    for y in range(h):
        rows.append("".join(CH[min(9, px[y*w+x]*10//256)] for x in range(w)))
    return rows

def stats(p):
    im = Image.open(p).convert("RGB").resize((160, 80))
    px = list(im.getdata()); n = len(px)
    bright = sum(1 for r,g,b in px if (r+g+b)/3 > 40)/float(n)
    colorful = sum(1 for r,g,b in px if max(r,g,b)-min(r,g,b) > 40)/float(n)
    return bright, colorful

def tap(x, y, wait=2.0):
    sh("shell", "input", "tap", str(x), str(y)); time.sleep(wait)

def show(name):
    p = shot(name)
    b, c = stats(p)
    print("--- %s bright=%.3f colorful=%.3f" % (name, b, c))
    for r in ascii_of(p):
        print(r)
    return p

if __name__ == "__main__":
    show(sys.argv[1] if len(sys.argv) > 1 else "probe")
