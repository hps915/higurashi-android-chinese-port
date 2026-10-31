# -*- coding: utf-8 -*-
"""统计工程内所有语音的 Vorbis 流参数分布，确认 Android 解码兼容性。"""
import os
import struct
from collections import Counter


def vorbis_info(path):
    with open(path, 'rb') as f:
        d = f.read(16384)
    i = d.find(b'\x01vorbis')
    if i < 0:
        return None
    q = i + 7
    try:
        ver = struct.unpack('<I', d[q:q + 4])[0]
        ch = d[q + 4]
        rate = struct.unpack('<I', d[q + 5:q + 9])[0]
        bnom = struct.unpack('<i', d[q + 13:q + 17])[0]
        return (ver, ch, rate, bnom)
    except Exception:
        return None


def main():
    roots = [
        (r"出题篇", r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game\voice"),
        (r"解题篇", r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\voice"),
    ]
    for label, root in roots:
        c = Counter()
        bad = []
        n = 0
        for dp, dn, fn in os.walk(root):
            for f in fn:
                if not f.endswith(".ogg"):
                    continue
                p = os.path.join(dp, f)
                n += 1
                info = vorbis_info(p)
                if info is None:
                    if len(bad) < 10:
                        bad.append(f)
                    c["NOT_VORBIS"] += 1
                    continue
                c["ch=%d rate=%d nom=%d" % (info[1], info[2], info[3])] += 1
        print("### %s  文件 %d" % (label, n))
        for k, v in c.most_common(20):
            print("   %-42s %d" % (k, v))
        if bad:
            print("   非 Vorbis 文件样例:", bad)
        print()


if __name__ == "__main__":
    main()
