# -*- coding: utf-8 -*-
"""把 PC 版第 5-8 章的 PS3 语音补进解题篇工程（修正版）。

统一约定：
  - 脚本里引用的路径形如 "voice/ps3/sXX/YY/name.ogg"，相对于工程根 game/
  - 目标：work/project_k/game/<该路径>
  - 源：<PC章>/HigurashiEpNN_Data/StreamingAssets/voice/ps3/...（去掉开头的 voice/）
"""
import io
import os
import re
import shutil
import sys

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJ = os.path.join(BASE, "work", "project_k", "game")

PC_ROOT = r"D:\Galgame\寒蝉鸣泣之时"
PC_SOURCES = [
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：5目明篇", "HigurashiEp05_Data", "StreamingAssets", "voice"),
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：6罪灭篇", "HigurashiEp06_Data", "StreamingAssets", "voice"),
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：7皆杀篇", "HigurashiEp07_Data", "StreamingAssets", "voice"),
    os.path.join(PC_ROOT, u"寒蝉鸣泣之时：8祭囃篇", "HigurashiEp08_Data", "StreamingAssets", "voice"),
]
VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]+)"', re.M)
# 注意：必须带 re.M，否则 ^ 只在全文开头匹配，play/queue 语句会被整体漏掉
PLAY = re.compile(r'^\s*(?:play|queue)\s+\w+\s+"([^"]+)"', re.M)


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
            for m in PLAY.finditer(t):
                v = m.group(1)
                if os.path.splitext(v)[1]:
                    refs.add(v)
    print("脚本引用语音/音频:", len(refs))

    def dst_of(p):
        return os.path.join(PROJ, *p.split("/"))

    missing = [p for p in refs if not os.path.exists(dst_of(p))]
    print("工程内缺失:", len(missing))

    live = [d for d in PC_SOURCES if os.path.isdir(d)]
    print("可用 PC 语音目录:", len(live))

    plan = []
    absent = []
    for p in missing:
        parts = p.split("/")
        if parts and parts[0] == "voice":
            parts = parts[1:]
        src = None
        for d in live:
            cand = os.path.join(d, *parts)
            if os.path.exists(cand):
                src = cand
                break
        if src:
            plan.append((src, dst_of(p)))
        else:
            absent.append(p)

    print("可补:", len(plan), " 仍缺:", len(absent))
    if plan:
        total = sum(os.path.getsize(s) for s, _ in plan)
        print("总体积: %.1f MB" % (total / 1048576.0))

    if not apply:
        print("(dry-run)")
        for s, d in plan[:5]:
            print("  %s\n    -> %s" % (s, d))
        return

    done = 0
    for src, dst in plan:
        od = os.path.dirname(dst)
        if not os.path.isdir(od):
            os.makedirs(od)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
        done += 1
        if done % 2000 == 0:
            print("  已处理", done)
    print("完成:", done)
    with io.open(os.path.join(BASE, "work", "voice_backfill_absent.txt"), "w",
                 encoding="utf-8", newline="\n") as f:
        for p in absent:
            f.write(p + u"\n")
    print("仍缺清单 -> work/voice_backfill_absent.txt")


if __name__ == "__main__":
    main()
