# -*- coding: utf-8 -*-
"""直接检查原始解题篇 APK 里到底有多少语音文件。"""
import os
import zipfile

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
APK = os.path.join(BASE, "downloads", "higu-kai-android-204.apk")
PROJ = os.path.join(BASE, "work", "project_k", "game", "voice")

z = zipfile.ZipFile(APK)
names = z.namelist()
print("APK 总条目:", len(names))

voice = [n for n in names if "/voice/" in n.lower() or n.lower().startswith("assets/voice")]
print("含 /voice/ 的条目:", len(voice))

# 统计目录分布
from collections import Counter
c = Counter()
for n in voice:
    parts = n.split("/")
    # 取到 sXX 一级
    key = "/".join(parts[:8])
    c[key] += 1
print()
print("语音条目目录分布（前 25）:")
for k, v in c.most_common(25):
    print("  %-70s %d" % (k, v))

print()
suffix = Counter(os.path.splitext(n)[1].lower() for n in voice)
print("扩展名分布:", dict(suffix))

# 看看 assets 下都有哪些顶层目录
tops = Counter()
for n in names:
    p = n.split("/")
    if len(p) >= 3:
        tops["/".join(p[:3])] += 1
print()
print("assets 顶层三节目录（前 30）:")
for k, v in tops.most_common(30):
    print("  %-60s %d" % (k, v))
z.close()

# 工程里的语音
n_proj = 0
for root, dirs, files in os.walk(PROJ):
    n_proj += sum(1 for f in files if f.endswith(".ogg"))
print()
print("工程内 voice/*.ogg:", n_proj)
