# -*- coding: utf-8 -*-
"""分析本轮补入的语音文件构成（按前缀/章节/大小），找出可优化的空间。"""
import os
import re
from collections import defaultdict

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJ = os.path.join(BASE, "work", "project_k", "game")
ABSENT = os.path.join(BASE, "work", "voice_backfill_absent.txt")

VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]+)"', re.M)
PLAY = re.compile(r'^\s*(?:play|queue)\s+\w+\s+"([^"]+)"', re.M)


def main():
    refs = set()
    for root, dirs, files in os.walk(PROJ):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in files:
            if not f.endswith(".rpy"):
                continue
            t = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            for m in VOICE.finditer(t):
                refs.add(m.group(1))
            for m in PLAY.finditer(t):
                v = m.group(1)
                if os.path.splitext(v)[1] and v.startswith("voice/"):
                    refs.add(v)

    by_s = defaultdict(lambda: [0, 0])
    by_pre = defaultdict(lambda: [0, 0])
    total = 0
    n = 0
    for p in refs:
        fp = os.path.join(PROJ, *p.split("/"))
        if not os.path.exists(fp):
            continue
        sz = os.path.getsize(fp)
        total += sz
        n += 1
        parts = p.split("/")
        ch = parts[2] if len(parts) > 2 else "?"
        by_s[ch][0] += 1
        by_s[ch][1] += sz
        name = os.path.basename(p)
        # 前缀：数字型取前 4 位，字母型取字母部分
        m = re.match(r'^([a-z]+)', name)
        pre = m.group(1) if m else "num"
        by_pre[pre][0] += 1
        by_pre[pre][1] += sz

    print("工程内语音文件:", n, " 合计 %.1f MB" % (total / 1048576.0))
    print()
    print("按章节:")
    for k in sorted(by_s, key=lambda x: -by_s[x][1]):
        c, b = by_s[k]
        print("  %-8s %7d  %8.1f MB" % (k, c, b / 1048576.0))
    print()
    print("按文件名前缀:")
    for k in sorted(by_pre, key=lambda x: -by_pre[x][1])[:25]:
        c, b = by_pre[k]
        print("  %-12s %7d  %8.1f MB" % (k, c, b / 1048576.0))


if __name__ == "__main__":
    main()
