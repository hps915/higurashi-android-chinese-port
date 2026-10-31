# -*- coding: utf-8 -*-
"""只读：对比 PC 版各素材目录的分辨率，判断 640x480 是不是缩略图。"""
import glob
import os
import struct

PC = r"D:\Galgame\寒蝉鸣泣之时\寒蝉鸣泣之时：5目明篇\HigurashiEp05_Data\StreamingAssets"


def dim(p):
    try:
        with open(p, 'rb') as f:
            d = f.read(33)
        if d[:8] == b'\x89PNG\r\n\x1a\n':
            return struct.unpack('>II', d[16:24])
        if d[:3] == b'\xff\xd8\xff':
            return ('jpeg',)
    except Exception:
        return None
    return None


def main():
    subdirs = ["CG", "OGBackgrounds", "OGSprites/sprite", "OGSprites/portrait",
              "CG/sprite", "CG/portrait", "CGAlt"]
    for sub in subdirs:
        p = os.path.join(PC, sub)
        if not os.path.isdir(p):
            print("--- %-22s [目录不存在]" % sub)
            continue
        files = sorted(glob.glob(os.path.join(p, "*.png")) +
                       glob.glob(os.path.join(p, "*.jpg")))
        print("--- %-22s %d 个文件" % (sub, len(files)))
        # 统计分辨率分布
        from collections import Counter
        c = Counter()
        for f in files:
            c[str(dim(f))] += 1
        for k, v in c.most_common(8):
            print("      %-20s %d" % (k, v))
        for f in files[:4]:
            print("      e.g. %-30s %s  %dKB"
                  % (os.path.basename(f), dim(f), os.path.getsize(f) // 1024))
    print()
    print("=== 目标的三张在 CG 里 ===")
    for n in ("mati10.png", "tosyo8.png", "gk2.png"):
        p = os.path.join(PC, "CG", n)
        if os.path.exists(p):
            print("  %-14s %s  %dKB" % (n, dim(p), os.path.getsize(p) // 1024))
        else:
            print("  %-14s 不在 CG/" % n)


if __name__ == "__main__":
    main()
