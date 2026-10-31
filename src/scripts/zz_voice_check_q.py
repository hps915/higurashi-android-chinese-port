# -*- coding: utf-8 -*-
"""出题篇 play/queue 音频引用完整性检查（带 re.M 修正）。"""
import io
import os
import re

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJ = os.path.join(BASE, "work", "project", "game")
PC_ROOT = r"D:\Galgame\寒蝉鸣泣之时"
PC_SOURCES = [
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：%s" % n, "HigurashiEp0%d_Data" % i,
                 "StreamingAssets", "voice")
    for i, n in ((1, u"1鬼隐篇"), (2, u"2绵流篇"), (3, u"3祟杀篇"), (4, u"4暇溃篇"))
]

VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]+)"', re.M)
PLAY = re.compile(r'^\s*(?:play|queue)\s+\w+\s+"([^"]+)"', re.M)


def main():
    refs = set()
    for root, dirs, files in os.walk(PROJ):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in files:
            if not f.endswith(".rpy"):
                continue
            t = io.open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            for m in VOICE.finditer(t):
                refs.add(m.group(1))
            for m in PLAY.finditer(t):
                v = m.group(1)
                if os.path.splitext(v)[1] and v.startswith("voice/"):
                    refs.add(v)
    print("出题篇 语音/音频引用:", len(refs))

    def dst(p):
        return os.path.join(PROJ, *p.split("/"))

    missing = [p for p in refs if not os.path.exists(dst(p))]
    print("工程内缺失:", len(missing))

    live = [d for d in PC_SOURCES if os.path.isdir(d)]
    print("可用 PC 语音目录:", len(live))
    plan, absent = [], []
    for p in missing:
        parts = p.split("/")[1:]
        src = None
        for d in live:
            c = os.path.join(d, *parts)
            if os.path.exists(c):
                src = c
                break
        if src:
            plan.append((src, dst(p)))
        else:
            absent.append(p)
    print("可补:", len(plan), " PC 也没有:", len(absent))
    for p in absent[:20]:
        print("   ", p)


if __name__ == "__main__":
    main()
