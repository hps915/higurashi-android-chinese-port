# -*- coding: utf-8 -*-
"""把 PC 版第 7/8 章的 PS3 语音补进解题篇工程。

只补脚本实际引用、且工程里缺失的文件，不动其他内容。
用法: python zz_voice_backfill.py [--apply]
"""
import io
import os
import re
import shutil
import sys

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJ = os.path.join(BASE, "work", "project_k", "game")
VOICE_ROOT = os.path.join(PROJ, "voice")

PC_ROOT = r"D:\Galgame\寒蝉鸣泣之时"
PC_SOURCES = [
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：5目明篇", "HigurashiEp05_Data", "StreamingAssets", "voice"),
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：6罪灭篇", "HigurashiEp06_Data", "StreamingAssets", "voice"),
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：7皆杀篇", "HigurashiEp07_Data", "StreamingAssets", "voice"),
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：8祭囃篇", "HigurashiEp08_Data", "StreamingAssets", "voice"),
]
VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]+)"', re.M)
PLAY = re.compile(r'^\s*(?:play|queue)\s+\w+\s+"([^"]+)"')


def main():
    apply = "--apply" in sys.argv
    refs = set()
    for root, dirs, files in os.walk(PROJ):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in files:
            if not f.endswith(".rpy"):
                continue
            t = io.open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            for m in VOICE.finditer(t):
                refs.add(m.group(1))
            # play/queue 里也会直接播语音文件（音效通道），同样要补
            for m in PLAY.finditer(t):
                v = m.group(1)
                if os.path.splitext(v)[1]:
                    refs.add(v)
    print("脚本引用语音/音频:", len(refs))

    missing = [p for p in refs
               if not os.path.exists(os.path.join(VOICE_ROOT, *p.split("/")[1:]))]
    print("工程内缺失:", len(missing))

    live = [d for d in PC_SOURCES if os.path.isdir(d)]
    plan = []
    absent = []
    for p in missing:
        parts = p.split("/")
        if parts[0] == "voice":
            parts = parts[1:]
        src = None
        for d in live:
            cand = os.path.join(d, *parts)
            if os.path.exists(cand):
                src = cand
                break
        if src:
            plan.append((src, os.path.join(VOICE_ROOT, *p.split("/")[1:])))
        else:
            absent.append(p)

    print("可补:", len(plan), " 仍缺:", len(absent))
    total = sum(os.path.getsize(s) for s, _ in plan)
    print("总体积: %.1f MB" % (total / 1048576.0))

    if not apply:
        print("(dry-run; --apply 才真拷)")
        for s, d in plan[:5]:
            print("  %s\n    -> %s" % (s, d))
        return

    done = 0
    for src, dst in plan:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        done += 1
        if done % 2000 == 0:
            print("  已拷", done)
    print("拷完:", done)
    with io.open(os.path.join(BASE, "work", "voice_backfill_absent.txt"), "w",
                 encoding="utf-8", newline="\n") as f:
        for p in absent:
            f.write(p + u"\n")
    print("仍缺清单 -> work/voice_backfill_absent.txt")


if __name__ == "__main__":
    main()
