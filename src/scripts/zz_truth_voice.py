# -*- coding: utf-8 -*-
"""地面真值调查：PC 版 1-8 章的语音目录构成 + 两个工程的语音引用分布。

只做只读分析，不做任何修改。
输出用于判断：
  1) 每章 PC 版到底有多少语音文件、多大
  2) 每个工程引用到的 sXX 分别对应哪一章
  3) 缺失的引用在 PC 版哪一章能找到
"""
import io
import os
import re
from collections import Counter, defaultdict

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PC_ROOT = r"D:\Galgame\寒蝉鸣泣之时"

PC_CHAPTERS = [
    (1, u"1鬼隐篇", "HigurashiEp01_Data"),
    (2, u"2绵流篇", "HigurashiEp02_Data"),
    (3, u"3祟杀篇", "HigurashiEp03_Data"),
    (4, u"4暇溃篇", "HigurashiEp04_Data"),
    (5, u"5目明篇", "HigurashiEp05_Data"),
    (6, u"6罪灭篇", "HigurashiEp06_Data"),
    (7, u"7皆杀篇", "HigurashiEp07_Data"),
    (8, u"8祭囃篇", "HigurashiEp08_Data"),
]

PROJECTS = [
    ("出题篇", os.path.join(BASE, "work", "project", "game")),
    ("解题篇", os.path.join(BASE, "work", "project_k", "game")),
]

VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]+)"', re.M)
PLAY = re.compile(r'^\s*(?:play|queue)\s+\w+\s+"([^"]+)"', re.M)


def pc_voice_root(ch):
    i, name, data = ch
    return os.path.join(PC_ROOT, u"寒蝉鸣泣之时：" + name, data, "StreamingAssets", "voice")


def scan_pc():
    """返回 {(sXX, sub): [count, bytes]} 按章分组"""
    out = {}
    for ch in PC_CHAPTERS:
        i = ch[0]
        root = pc_voice_root(ch)
        if not os.path.isdir(root):
            out[i] = None
            continue
        d = defaultdict(lambda: [0, 0])
        total = [0, 0]
        for dp, dn, fn in os.walk(root):
            for f in fn:
                if not f.lower().endswith(".ogg"):
                    continue
                p = os.path.join(dp, f)
                sz = os.path.getsize(p)
                rel = os.path.relpath(p, root).replace("\\", "/")
                parts = rel.split("/")
                # ps3/sXX/YY/f.ogg  |  ps2/YY/f.ogg  |  org/...
                if len(parts) >= 3 and parts[0] in ("ps3", "ps2", "org"):
                    key = "%s/%s" % (parts[0], parts[1]) if len(parts) >= 4 else "%s/%s" % (parts[0], parts[1])
                else:
                    key = parts[0]
                d[key][0] += 1
                d[key][1] += sz
                total[0] += 1
                total[1] += sz
        out[i] = (d, total)
    return out


def scan_project(game_dir):
    """返回 refs(set), 以及 each sXX 的引用计数"""
    refs = set()
    by_s = Counter()
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in files:
            if not f.endswith(".rpy"):
                continue
            t = io.open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            for rx in (VOICE, PLAY):
                for m in rx.finditer(t):
                    v = m.group(1)
                    if not v.startswith("voice/"):
                        continue
                    if not os.path.splitext(v)[1]:
                        continue
                    refs.add(v)
    for p in refs:
        parts = p.split("/")
        # voice/ps3/sXX/YY/... or voice/ps2/YY/...
        if len(parts) >= 3 and parts[1] == "ps3":
            by_s["ps3/" + parts[2]] += 1
        elif len(parts) >= 3 and parts[1] == "ps2":
            by_s["ps2/" + parts[2]] += 1
        else:
            by_s[parts[1] if len(parts) > 1 else "?"] += 1
    return refs, by_s


def main():
    print("=" * 96)
    print("【一】PC 版 1-8 章语音构成")
    print("=" * 96)
    pcs = scan_pc()
    for ch in PC_CHAPTERS:
        i = ch[0]
        r = pcs[i]
        if r is None:
            print("  第%d章 %s : 目录不存在" % (i, ch[1]))
            continue
        d, (cnt, byt) = r
        print("  第%d章 %-10s 语音 %6d 个 / %7.1f MB" % (i, ch[1], cnt, byt / 1048576.0))
        for k in sorted(d):
            print("      %-12s %6d 个 / %7.1f MB" % (k, d[k][0], d[k][1] / 1048576.0))

    print()
    print("=" * 96)
    print("【二】两个工程的语音引用分布")
    print("=" * 96)
    proj = {}
    for label, gd in PROJECTS:
        refs, by_s = scan_project(gd)
        proj[label] = (refs, by_s)
        total_exist = sum(1 for p in refs if os.path.exists(os.path.join(gd, *p.split("/"))))
        print("  %s : 唯一引用 %d，其中工程内存在 %d，缺失 %d"
              % (label, len(refs), total_exist, len(refs) - total_exist))
        for k in sorted(by_s, key=lambda x: -by_s[x]):
            print("      %-14s %5d 处引用" % (k, by_s[k]))
        print()


if __name__ == "__main__":
    main()
