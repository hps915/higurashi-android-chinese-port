# -*- coding: utf-8 -*-
"""精确量化：解题篇工程相对 PC 版 5-8 章语音全集的缺口（只读）。

不按脚本引用算，而是按 PC 版全集算：
  - PC 5-8 章 voice 目录里所有文件
  - 工程里有没有对应路径
这样能看出移植包到底删了多少，以及脚本没引用但剧情可能需要的。
"""
import io
import os
from collections import defaultdict

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PC_ROOT = r"D:\Galgame\寒蝉鸣泣之时"
PROJ_K = os.path.join(BASE, "work", "project_k", "game")
PROJ_Q = os.path.join(BASE, "work", "project", "game")

PC_5_8 = [
    ("第5章目明", u"寒蝉鸣泣之时：5目明篇", "HigurashiEp05_Data"),
    ("第6章罪灭", u"寒蝉鸣泣之时：6罪灭篇", "HigurashiEp06_Data"),
    ("第7章皆杀", u"寒蝉鸣泣之时：7皆杀篇", "HigurashiEp07_Data"),
    ("第8章祭囃", u"寒蝉鸣泣之时：8祭囃篇", "HigurashiEp08_Data"),
]
PC_1_4 = [
    ("第1章鬼隐", u"寒蝉鸣泣之时：1鬼隐篇", "HigurashiEp01_Data"),
    ("第2章绵流", u"寒蝉鸣泣之时：2绵流篇", "HigurashiEp02_Data"),
    ("第3章祟杀", u"寒蝉鸣泣之时：3祟杀篇", "HigurashiEp03_Data"),
    ("第4章暇溃", u"寒蝉鸣泣之时：4暇溃篇", "HigurashiEp04_Data"),
]


def pc_files(chs):
    out = {}
    for label, name, data in chs:
        root = os.path.join(PC_ROOT, u"寒蝉鸣泣之时：" + name.replace(u"寒蝉鸣泣之时：", ""),
                            data, "StreamingAssets", "voice")
        root = os.path.join(PC_ROOT, name, data, "StreamingAssets", "voice")
        if not os.path.isdir(root):
            print("  [跳过] 目录不存在:", root)
            continue
        for dp, dn, fn in os.walk(root):
            for f in fn:
                if not f.lower().endswith(".ogg"):
                    continue
                rel = os.path.relpath(os.path.join(dp, f), root).replace("\\", "/")
                out[rel] = label
    return out


def proj_files(game_dir):
    root = os.path.join(game_dir, "voice")
    out = set()
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.lower().endswith(".ogg"):
                continue
            out.add(os.path.relpath(os.path.join(dp, f), root).replace("\\", "/"))
    return out


def report(label, chs, game_dir):
    print("=" * 92)
    print("### %s  vs PC 语音全集" % label)
    pc = pc_files(chs)
    pj = proj_files(game_dir)
    print("  PC 全集文件: %d   工程内: %d" % (len(pc), len(pj)))
    missing = [p for p in pc if p not in pj]
    extra = [p for p in pj if p not in pc]
    print("  PC 有、工程没有: %d" % len(missing))
    print("  工程有、PC 没有: %d" % len(extra))
    # 按目录聚合缺失
    by_dir = defaultdict(int)
    by_size = defaultdict(int)
    for p in missing:
        parts = p.split("/")
        key = "/".join(parts[:-1]) if len(parts) > 1 else "(根)"
        by_dir[key] += 1
        by_size[key] += os.path.getsize(os.path.join(
            PC_ROOT, chs and "" or "", *p.split("/"))) if False else 0
    print()
    print("  缺失按目录（前 30）:")
    for k in sorted(by_dir, key=lambda x: -by_dir[x])[:30]:
        print("     %-22s %5d" % (k, by_dir[k]))
    if extra:
        print()
        print("  工程多出的样例:", extra[:5])
    return len(pc), len(pj), len(missing)


def main():
    report("解题篇", PC_5_8, PROJ_K)
    print()
    report("出题篇", PC_1_4, PROJ_Q)


if __name__ == "__main__":
    main()
