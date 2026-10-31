# -*- coding: utf-8 -*-
"""比对：解题篇脚本引用的 s12（皆杀）/ s13（祭囃）语音，
在 PC 版第 7/8 章 voice 目录里能不能找到。"""
import os
import re
from collections import Counter

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJ = os.path.join(BASE, "work", "project_k", "game")
PC7 = r"D:\Galgame\寒蝉鸣泣之时\寒蝉鸣泣之时：7皆杀篇\HigurashiEp07_Data\StreamingAssets\voice"
PC8 = r"D:\Galgame\寒蝉鸣泣之时\寒蝉鸣泣之时：8祭囃篇\HigurashiEp08_Data\StreamingAssets\voice"

VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]+)"', re.M)


def collect_refs():
    refs = {}
    for root, dirs, files in os.walk(PROJ):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if not f.endswith(".rpy"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, PROJ).replace("\\", "/")
            for i, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
                m = VOICE.match(line.rstrip())
                if m:
                    refs.setdefault(m.group(1), []).append("%s:%d" % (rel, i))
    return refs


def index_pc(root):
    """返回 (set of 相对路径, set of 纯文件名)"""
    rels = set()
    names = set()
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            full = os.path.join(dirpath, f)
            r = os.path.relpath(full, root).replace("\\", "/")
            rels.add(r)
            names.add(f)
    return rels, names


def main():
    refs = collect_refs()
    print("脚本引用唯一语音路径:", len(refs))

    # 按 sXX 分组
    by_s = Counter()
    for p in refs:
        parts = p.split("/")
        key = parts[2] if len(parts) > 2 else "?"
        by_s[key] += 1
    print("按章节分组:", dict(sorted(by_s.items())))

    print("\n索引 PC 版语音...")
    r7, n7 = index_pc(PC7)
    r8, n8 = index_pc(PC8)
    print("  PC7 文件:", len(r7), " PC8 文件:", len(r8))

    # 检查缺失的那些引用能否在 PC 版找到
    lite = os.path.join(BASE, "work", "project_k", "game")
    missing_map = {}
    for p in refs:
        full = os.path.join(lite, p.replace("/", os.sep))
        if os.path.exists(full):
            continue
        missing_map[p] = True
    print("工程内缺失的语音路径:", len(missing_map))

    found_rel = found_name = notfound = 0
    samples = []
    missing_by_s = Counter()
    for p in missing_map:
        parts = p.split("/")
        key = parts[2] if len(parts) > 2 else "?"
        missing_by_s[key] += 1
        fn = os.path.basename(p)
        if p in r7 or p in r8:
            found_rel += 1
        elif fn in n7 or fn in n8:
            found_name += 1
            if len(samples) < 8:
                samples.append((p, "name-only"))
        else:
            notfound += 1
            if len(samples) < 16:
                samples.append((p, "absent"))
    print()
    print("缺失语音在 PC 版中的命运:")
    print("  完整相对路径能对上:", found_rel)
    print("  只有文件名能对上:", found_name)
    print("  PC 版也没有:", notfound)
    print()
    print("按章节统计缺失:", dict(sorted(missing_by_s.items())))
    print()
    for p, k in samples:
        print("  [%s] %s" % (k, p))


if __name__ == "__main__":
    main()
