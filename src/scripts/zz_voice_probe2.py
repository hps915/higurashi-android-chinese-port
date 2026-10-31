# -*- coding: utf-8 -*-
"""详细看解题篇源 APK 的 x-voice 目录结构与脚本引用的匹配情况。"""
import os
import re
import zipfile
from collections import Counter

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
APK = os.path.join(BASE, "downloads", "higu-kai-android-204.apk")
PROJ = os.path.join(BASE, "work", "project_k", "game")

z = zipfile.ZipFile(APK)
names = [n for n in z.namelist() if n.startswith("assets/x-game/x-voice/")]
print("x-voice 条目:", len(names))

# 目录层级（去掉 x- 前缀 + 还原）
c = Counter()
for n in names:
    rel = n[len("assets/x-game/"):]
    parts = [p[2:] if p.startswith("x-") else p for p in rel.split("/")]
    c["/".join(parts[:-1])] += 1
print()
print("语音目录分布（前 40）:")
for k, v in c.most_common(40):
    print("  %-42s %d" % (k, v))

# 脚本里引用的语音路径前缀分布
VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]+)"', re.M)
refs = Counter()
refset = set()
for root, dirs, files in os.walk(PROJ):
    dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
    for f in files:
        if not f.endswith(".rpy"):
            continue
        t = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
        for m in VOICE.finditer(t):
            p = m.group(1)
            refset.add(p)
            refs["/".join(p.split("/")[:-1])] += 1

print()
print("脚本引用的语音目录（前 40）:")
for k, v in refs.most_common(40):
    have = c.get(k, 0)
    flag = "" if have else "   <== 源 APK 无此目录!"
    print("  %-42s 引用%-6d 源APK有 %-6d%s" % (k, v, have, flag))

print()
print("脚本引用唯一语音路径:", len(refset))
# 真实存在性
exist = 0
for p in refset:
    if p in z.namelist() or ("assets/x-game/" + "/".join(
            ("x-" + x) for x in p.split("/"))) in z.namelist():
        exist += 1
print("其中源 APK 里存在的:", exist)
print("缺失:", len(refset) - exist)
z.close()
