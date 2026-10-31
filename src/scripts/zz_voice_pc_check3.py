# -*- coding: utf-8 -*-
"""解题篇缺失语音 → PC 版补齐能力评估（干净版）。"""
import io
import os
import re
from collections import Counter

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJ = os.path.join(BASE, "work", "project_k", "game")

PC_ROOT = r"D:\Galgame\寒蝉鸣泣之时"
PC_VOICE_DIRS = [
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：5目明篇", "HigurashiEp05_Data", "StreamingAssets", "voice"),
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：6罪灭篇", "HigurashiEp06_Data", "StreamingAssets", "voice"),
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：7皆杀篇", "HigurashiEp07_Data", "StreamingAssets", "voice"),
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：8祭囃篇", "HigurashiEp08_Data", "StreamingAssets", "voice"),
]
VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]+)"', re.M)


def main():
    refs = {}
    for root, dirs, files in os.walk(PROJ):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if not f.endswith(".rpy"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, PROJ).replace("\\", "/")
            for i, line in enumerate(io.open(p, encoding="utf-8", errors="replace"), 1):
                m = VOICE.match(line.rstrip())
                if m:
                    refs.setdefault(m.group(1), []).append("%s:%d" % (rel, i))

    missing = {p: v for p, v in refs.items()
               if not os.path.exists(os.path.join(PROJ, *p.split("/")))}
    print("引用唯一路径:", len(refs))
    print("工程内缺失:", len(missing))

    live = [d for d in PC_VOICE_DIRS if os.path.isdir(d)]
    print("可用 PC voice 目录:", len(live))
    for d in live:
        n = sum(len(fs) for _, _, fs in os.walk(d))
        print("   %-70s %d" % (d.replace(PC_ROOT + os.sep, ""), n))

    by_src = Counter()
    absent = []
    for p in missing:
        # 脚本里写的是 "voice/ps3/s.../x.ogg"，而 PC 的 d 已经是 .../StreamingAssets/voice
        # 所以要把开头的 voice/ 去掉
        parts = p.split("/")
        if parts and parts[0] == "voice":
            parts = parts[1:]
        hit = None
        for d in live:
            if os.path.exists(os.path.join(d, *parts)):
                hit = d
                break
        if hit:
            by_src[os.path.basename(os.path.dirname(os.path.dirname(hit)))] += 1
        else:
            absent.append(p)

    print()
    print("可从 PC 补齐:", sum(by_src.values()), "/", len(missing))
    for k, v in by_src.most_common():
        print("   %-30s %d" % (k, v))
    print("PC 版也没有:", len(absent))

    if absent:
        c = Counter(p.split("/")[2] if len(p.split("/")) > 2 else "?" for p in absent)
        print("   按章节:", dict(c.most_common()))
        print("   样例:")
        for p in absent[:20]:
            print("     ", p)


if __name__ == "__main__":
    main()
