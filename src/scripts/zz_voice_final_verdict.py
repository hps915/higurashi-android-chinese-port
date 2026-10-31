# -*- coding: utf-8 -*-
"""对两个工程缺失的语音，逐条在 PC 1-8 章全部语音目录里做最终裁定。

输出三分类：
  A) 能在 PC 某章找到 -> 应补（列出确切来源）
  B) PC 全都没有 -> 真缺（登记）
"""
import io
import os
import re

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PC_ROOT = r"D:\Galgame\寒蝉鸣泣之时"

PC_CHAPTERS = [
    ("Ep01", u"寒蝉鸣泣之时：1鬼隐篇", "HigurashiEp01_Data"),
    ("Ep02", u"寒蝉鸣泣之时：2绵流篇", "HigurashiEp02_Data"),
    ("Ep03", u"寒蝉鸣泣之时：3祟杀篇", "HigurashiEp03_Data"),
    ("Ep04", u"寒蝉鸣泣之时：4暇溃篇", "HigurashiEp04_Data"),
    ("Ep05", u"寒蝉鸣泣之时：5目明篇", "HigurashiEp05_Data"),
    ("Ep06", u"寒蝉鸣泣之时：6罪灭篇", "HigurashiEp06_Data"),
    ("Ep07", u"寒蝉鸣泣之时：7皆杀篇", "HigurashiEp07_Data"),
    ("Ep08", u"寒蝉鸣泣之时：8祭囃篇", "HigurashiEp08_Data"),
]

VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]+)"', re.M)
PLAY = re.compile(r'^\s*(?:play|queue)\s+\w+\s+"([^"]+)"', re.M)


def all_voice_roots():
    out = []
    for tag, name, data in PC_CHAPTERS:
        r = os.path.join(PC_ROOT, name, data, "StreamingAssets", "voice")
        if os.path.isdir(r):
            out.append((tag, r))
    return out


def refs_of(game_dir):
    refs = set()
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in files:
            if not f.endswith(".rpy"):
                continue
            t = io.open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            for rx in (VOICE, PLAY):
                for m in rx.finditer(t):
                    v = m.group(1)
                    if v.startswith("voice/") and os.path.splitext(v)[1]:
                        refs.add(v)
    return refs


def main():
    roots = all_voice_roots()
    print("PC 语音目录:", [t for t, _ in roots])
    for label, gd in (("出题篇", os.path.join(BASE, "work", "project", "game")),
                      ("解题篇", os.path.join(BASE, "work", "project_k", "game"))):
        refs = refs_of(gd)
        missing = [p for p in sorted(refs)
                   if not os.path.exists(os.path.join(gd, *p.split("/")))]
        print()
        print("=" * 88)
        print("### %s  引用 %d  缺失 %d" % (label, len(refs), len(missing)))
        fixable, unfixable = [], []
        for p in missing:
            parts = p.split("/")
            if parts[0] == "voice":
                parts = parts[1:]
            hit = None
            for tag, r in roots:
                c = os.path.join(r, *parts)
                if os.path.exists(c):
                    hit = (tag, c)
                    break
            if hit:
                fixable.append((p, hit[0], hit[1]))
            else:
                unfixable.append(p)
        print("  可补 %d，PC 全无 %d" % (len(fixable), len(unfixable)))
        for p, tag, src in fixable:
            print("    FIX  [%s] %s" % (tag, p))
        for p in unfixable:
            print("    NONE       %s" % p)


if __name__ == "__main__":
    main()
