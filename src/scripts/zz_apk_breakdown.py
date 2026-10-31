# -*- coding: utf-8 -*-
"""两个源 APK 按类别、按语音章号做完整拆解对比。"""
import os
import zipfile
from collections import Counter, defaultdict

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
APK_Q = os.path.join(BASE, "downloads", "higurashi_android_118.apk")
APK_K = os.path.join(BASE, "downloads", "higu-kai-android-204.apk")

CATS = ["voice", "background", "characters", "cg", "music", "sound", "movie",
        "text", "efe", "tips", "overview", "movie"]


def unx(p):
    return "/".join(x[2:] if x.startswith("x-") else x for x in p.split("/"))


def analyze(apk, label):
    z = zipfile.ZipFile(apk)
    info = z.infolist()
    by_cat = defaultdict(lambda: [0, 0])   # count, bytes
    voice_s = defaultdict(lambda: [0, 0])
    voice_ps = defaultdict(lambda: [0, 0])
    total = 0
    for i in info:
        total += i.file_size
        n = i.filename
        if not n.startswith("assets/x-game/"):
            continue
        rel = unx(n[len("assets/x-game/"):])
        top = rel.split("/")[0]
        by_cat[top][0] += 1
        by_cat[top][1] += i.file_size
        if top == "voice":
            parts = rel.split("/")
            # voice/ps3/s06/06/x.ogg  or voice/ps2/00/x.ogg
            if len(parts) >= 4 and parts[1] in ("ps3", "ps2", "org"):
                voice_ps[parts[1]][0] += 1
                voice_ps[parts[1]][1] += i.file_size
                if parts[1] == "ps3":
                    voice_s[parts[2]][0] += 1
                    voice_s[parts[2]][1] += i.file_size
            elif len(parts) >= 2:
                voice_ps[parts[1]][0] += 1
                voice_ps[parts[1]][1] += i.file_size
    z.close()

    print("=" * 88)
    print("### %s   (APK 解压后总计 %.0f MB)" % (label, total / 1048576.0))
    print()
    print("按类别:")
    print("  %-16s %8s %12s" % ("类别", "文件数", "MB"))
    for k in sorted(by_cat, key=lambda x: -by_cat[x][1]):
        c, b = by_cat[k]
        print("  %-16s %8d %12.1f" % (k, c, b / 1048576.0))
    print()
    print("语音按 ps2/ps3:")
    for k in sorted(voice_ps):
        c, b = voice_ps[k]
        print("  %-8s %7d  %9.1f MB" % (k, c, b / 1048576.0))
    print()
    print("语音按章号 sXX:")
    for k in sorted(voice_s):
        c, b = voice_s[k]
        print("  %-6s %7d  %9.1f MB" % (k, c, b / 1048576.0))
    return total


def main():
    analyze(APK_Q, "出题篇源 APK")
    print()
    analyze(APK_K, "解题篇源 APK")


if __name__ == "__main__":
    main()
