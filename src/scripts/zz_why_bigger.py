# -*- coding: utf-8 -*-
"""只读调查：为什么解题篇最终 APK 比出题篇大约 900MB。

输出四组数据：
  A) 两个最终 APK 按类别统计（文件数 / 解压后字节 / 压缩后字节）
  B) 两个源 APK 按类别统计（同上），用于看"原始移植包"本来差多少
  C) PC 版 1-4 章 vs 5-8 章 的素材构成对比
  D) 最终 APK 内部是否存在重复文件（同名文件出现在多个路径）
"""
import os
import sys
import zipfile
from collections import Counter, defaultdict

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
FINAL = [
    ("出题篇", os.path.join(BASE, "寒蝉鸣泣之时-出题篇-安卓中文版.apk")),
    ("解题篇", os.path.join(BASE, "寒蝉鸣泣之时-解题篇-安卓中文版.apk")),
]
SRC = [
    ("出题篇源包", os.path.join(BASE, "downloads", "higurashi_android_118.apk")),
    ("解题篇源包", os.path.join(BASE, "downloads", "higu-kai-android-204.apk")),
]
PC_ROOT = r"D:\Galgame\寒蝉鸣泣之时"
PC_Q = [(1, u"1鬼隐篇", "HigurashiEp01_Data"), (2, u"2绵流篇", "HigurashiEp02_Data"),
        (3, u"3祟杀篇", "HigurashiEp03_Data"), (4, u"4暇溃篇", "HigurashiEp04_Data")]
PC_K = [(5, u"5目明篇", "HigurashiEp05_Data"), (6, u"6罪灭篇", "HigurashiEp06_Data"),
        (7, u"7皆杀篇", "HigurashiEp07_Data"), (8, u"8祭囃篇", "HigurashiEp08_Data")]

MB = 1048576.0
CATS_OF_INTEREST = ["voice", "background", "characters", "cg", "music", "sound",
                    "movie", "text", "efe", "tips", "overview", "cache"]


def unx(p):
    return "/".join(x[2:] if x.startswith("x-") else x for x in p.split("/"))


def apk_stats(path):
    z = zipfile.ZipFile(path)
    by_cat = defaultdict(lambda: [0, 0, 0])   # files, uncompressed, compressed
    total = [0, 0, 0]
    for i in z.infolist():
        total[0] += 1
        total[1] += i.file_size
        total[2] += i.compress_size
        n = i.filename
        if n.startswith("assets/x-game/"):
            rel = unx(n[len("assets/x-game/"):])
            cat = rel.split("/")[0]
        elif n.startswith("assets/x-renpy/"):
            cat = "renpy-common"
        elif n.startswith("lib/"):
            cat = "lib"
        elif n.startswith("assets/"):
            cat = "assets-other"
        elif n in ("resources.arsc", "AndroidManifest.xml", "classes.dex"):
            cat = n
        else:
            cat = "other-root"
        by_cat[cat][0] += 1
        by_cat[cat][1] += i.file_size
        by_cat[cat][2] += i.compress_size
    z.close()
    return by_cat, total


def print_table(rows, title):
    print(title)
    print("  %-16s %8s %10s %10s %10s" % ("类别", "文件数", "解压MB", "压缩MB", "占比"))
    t_u = sum(v[1] for v in rows.values())
    t_c = sum(v[2] for v in rows.values())
    for k in sorted(rows, key=lambda x: -rows[x][2]):
        f, u, c = rows[k]
        print("  %-16s %8d %10.1f %10.1f %9.1f%%"
              % (k, f, u / MB, c / MB, 100.0 * c / max(1, t_c)))
    print("  %-16s %8s %10.1f %10.1f" % ("合计", "", t_u / MB, t_c / MB))
    return t_u, t_c


def pc_assets(chs):
    """统计某几章的 背景/CG/BGM/音乐 文件数与体积"""
    out = defaultdict(lambda: [0, 0])
    for num, name, data in chs:
        root = os.path.join(PC_ROOT, u"寒蝉鸣泣之时：" + name, data, "StreamingAssets")
        if not os.path.isdir(root):
            continue
        for sub, keys in (("voice", ("voice",)), ("BG", ("bg",)), ("CG", ("cg",)),
                          ("BGM", ("bgm",)), ("SE", ("sound",)), ("OGBackgrounds", ("ogbg",)),
                          ("OGSprites", ("ogsprite",))):
            pass
        # 直接按目录名遍历
        for dp, dn, fn in os.walk(root):
            rel = os.path.relpath(dp, root).replace("\\", "/")
            top = rel.split("/")[0]
            if top in ("Update", "Data", "CompiledScripts", "CompiledChineseScripts",
                       "CompiledUpdateScripts", "Scripts", "CGAlt"):
                continue
            for f in fn:
                if not f.lower().endswith((".ogg", ".mp3", ".png", ".jpg", ".ogg", ".wav")):
                    continue
                key = top
                out[key][0] += 1
                out[key][1] += os.path.getsize(os.path.join(dp, f))
    return out


def dup_scan(path):
    """同一文件名是否出现在多个路径下（排除 PS2/PS3 双版本这种正常情况需人工判断）"""
    z = zipfile.ZipFile(path)
    name_to_paths = Counter()
    for n in z.namelist():
        if n.startswith("assets/x-game/x-voice/"):
            name_to_paths[n.split("/")[-1]] += 1
    z.close()
    dup = [(k, v) for k, v in name_to_paths.items() if v > 1]
    return len(name_to_paths), dup


def main():
    print("=" * 100)
    print("【A】最终交付 APK 按类别统计")
    print("=" * 100)
    stats = {}
    for label, p in FINAL:
        if not os.path.exists(p):
            print("  缺少:", p)
            continue
        by_cat, total = apk_stats(p)
        stats[label] = by_cat
        print()
        print("--- %s  (%s)" % (label, os.path.basename(p)))
        print("    文件总数 %d，解压后 %.1f MB，压缩后 %.1f MB，APK 实际 %.1f MB"
              % (total[0], total[1] / MB, total[2] / MB, os.path.getsize(p) / MB))
        print_table(by_cat, "")

    print()
    print("=" * 100)
    print("【A2】两篇按类别差值（解题 - 出题，压缩后 MB）")
    print("=" * 100)
    if len(stats) == 2:
        q, k = stats["出题篇"], stats["解题篇"]
        allcats = set(q) | set(k)
        print("  %-16s %10s %10s %10s" % ("类别", "出题", "解题", "差值"))
        for cat in sorted(allcats, key=lambda c: -(k.get(c, [0, 0, 0])[2] - q.get(c, [0, 0, 0])[2])):
            qc = q.get(cat, [0, 0, 0])
            kc = k.get(cat, [0, 0, 0])
            d = (kc[2] - qc[2]) / MB
            if abs(d) < 0.5:
                continue
            print("  %-16s %10.1f %10.1f %+10.1f" % (cat, qc[2] / MB, kc[2] / MB, d))

    print()
    print("=" * 100)
    print("【B】原始源 APK 按类别统计（对照：移植包本来就差多少）")
    print("=" * 100)
    src_stats = {}
    for label, p in SRC:
        by_cat, total = apk_stats(p)
        src_stats[label] = by_cat
        print()
        print("--- %s  (解压后 %.1f MB / 压缩后 %.1f MB)"
              % (label, total[1] / MB, total[2] / MB))
        print_table(by_cat, "")

    if len(src_stats) == 2:
        print()
        print("【B2】源包差值（解题源 - 出题源，解压后 MB）")
        q = src_stats["出题篇源包"]
        k = src_stats["解题篇源包"]
        print("  %-16s %10s %10s %10s" % ("类别", "出题源", "解题源", "差值"))
        for cat in sorted(set(q) | set(k))[:0] or sorted(set(q) | set(k),
                                                          key=lambda c: -(k.get(c, [0, 0, 0])[1] - q.get(c, [0, 0, 0])[1])):
            qc = q.get(cat, [0, 0, 0])
            kc = k.get(cat, [0, 0, 0])
            d = (kc[1] - qc[1]) / MB
            if abs(d) < 1.0:
                continue
            print("  %-16s %10.1f %10.1f %+10.1f" % (cat, qc[1] / MB, kc[1] / MB, d))

    print()
    print("=" * 100)
    print("【C】PC 版 1-4 章 vs 5-8 章 素材构成")
    print("=" * 100)
    for label, chs in (("PC 1-4 (出题篇)", PC_Q), ("PC 5-8 (解题篇)", PC_K)):
        agg = pc_assets(chs)
        print()
        print("--- %s" % label)
        print("  %-20s %8s %12s" % ("目录", "文件数", "MB"))
        tot = [0, 0]
        for k in sorted(agg, key=lambda x: -agg[x][1]):
            f, b = agg[k]
            tot[0] += f
            tot[1] += b
            print("  %-20s %8d %12.1f" % (k, f, b / MB))
        print("  %-20s %8d %12.1f" % ("合计", tot[0], tot[1] / MB))

    print()
    print("=" * 100)
    print("【D】最终 APK 内 voice 同名文件重复检查")
    print("=" * 100)
    for label, p in FINAL:
        if not os.path.exists(p):
            continue
        n_names, dup = dup_scan(p)
        print("  %s : 唯一文件名 %d，同名出现在多个路径的 %d 种"
              % (label, n_names, len(dup)))
        for k, v in sorted(dup, key=lambda x: -x[1])[:6]:
            print("      %-40s %d 处" % (k, v))


if __name__ == "__main__":
    main()
