# -*- coding: utf-8 -*-
"""对比两个源 APK 的语音包规模，并核实解题篇语音缺口。"""
import os
import zipfile
from collections import Counter

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
APK_Q = os.path.join(BASE, "downloads", "higurashi_android_118.apk")
APK_K = os.path.join(BASE, "downloads", "higu-kai-android-204.apk")


def voice_stats(apk, label):
    z = zipfile.ZipFile(apk)
    names = z.namelist()
    voice = [n for n in names if n.startswith("assets/x-game/x-voice/")]
    total_bytes = sum(z.getinfo(n).file_size for n in voice)
    c = Counter()
    for n in voice:
        parts = [p[2:] if p.startswith("x-") else p for p in n[len("assets/x-game/"):].split("/")]
        # voice/ps3/sXX/YY/name.ogg
        if len(parts) >= 4:
            c["%s/%s" % (parts[2], parts[3])] += 1
        elif len(parts) >= 3:
            c[parts[2]] += 1
    print("### %s" % label)
    print("  语音文件数:", len(voice))
    print("  语音总大小: %.1f MB" % (total_bytes / 1048576.0))
    print("  按 sXX 分布:")
    for k, v in sorted(c.items()):
        if k.startswith("s") or k.isdigit():
            print("     %-10s %d" % (k, v))
    z.close()
    return len(voice), total_bytes


def main():
    q = voice_stats(APK_Q, "出题篇源 APK")
    print()
    k = voice_stats(APK_K, "解题篇源 APK")
    print()
    print("=== 结论 ===")
    print("出题篇语音 %.1f MB / 解题篇语音 %.1f MB" % (q[1] / 1048576.0, k[1] / 1048576.0))
    z = zipfile.ZipFile(APK_Q)
    qt = sum(i.file_size for i in z.infolist())
    z.close()
    z = zipfile.ZipFile(APK_K)
    kt = sum(i.file_size for i in z.infolist())
    z.close()
    print("出题篇 APK 解压后总计 %.1f MB" % (qt / 1048576.0))
    print("解题篇 APK 解压后总计 %.1f MB" % (kt / 1048576.0))
    print("出题篇语音占比 %.1f%%  解题篇语音占比 %.1f%%"
          % (100.0 * q[1] / qt, 100.0 * k[1] / kt))


if __name__ == "__main__":
    main()
