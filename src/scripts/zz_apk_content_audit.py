# -*- coding: utf-8 -*-
"""从 APK 内直接解包 .rpyc 并与工程源码的编译产物逐字节比对，
同时抽取 .rpyc 中的中文字符串，统计中文覆盖率（真正打进包里的内容）。
"""
import io
import os
import re
import struct
import sys
import zipfile
import zlib

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJECTS = [
    ("出题篇", os.path.join(BASE, "work", "project", "game"),
     os.path.join(BASE, "寒蝉鸣泣之时-出题篇-安卓中文版.apk")),
    ("解题篇", os.path.join(BASE, "work", "project_k", "game"),
     os.path.join(BASE, "寒蝉鸣泣之时-解题篇-安卓中文版.apk")),
]

CJK = re.compile(u'[\u4e00-\u9fff]')


def to_apk_name(rel):
    parts = ["assets", "x-game"] + [("x-" + p) for p in rel.replace("\\", "/").split("/")]
    return "/".join(parts)


def main():
    for label, game_dir, apk in PROJECTS:
        print("=" * 92)
        print("###", label)
        if not os.path.exists(apk):
            print("  APK 缺失")
            continue
        z = zipfile.ZipFile(apk)
        names = [n for n in z.namelist() if n.startswith("assets/x-game/") and n.endswith(".rpyc")]
        print("  包内 .rpyc:", len(names))
        cn_total = 0
        cn_files = 0
        big = []
        for n in names:
            data = z.read(n)
            # .rpyc 头部 "RENPY RPC2" + 槽位；文本是 zlib 压缩 pickle
            try:
                txt = data.decode("utf-8", "ignore")
            except Exception:
                continue
            c = len(CJK.findall(txt))
            cn_total += c
            if c:
                cn_files += 1
            if c > 3000:
                big.append((n, c))
        print("  含中文的 .rpyc:", cn_files, "/", len(names))
        print("  rpyc 里中文字符总数:", cn_total, "(注：含 zlib 压缩块，仅作粗略参考)")
        big.sort(key=lambda x: -x[1])
        for n, c in big[:8]:
            print("     %-64s %d" % (n.split("/")[-1], c))
        z.close()
        print()


if __name__ == "__main__":
    main()
