# -*- coding: utf-8 -*-
"""精确统计：解题篇脚本引用的语音，能从 PC 第 7/8 章补多少。"""
import os
import re
from collections import Counter

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJ = os.path.join(BASE, "work", "project_k", "game")
PC = r"D:\Galgame\寒蝉鸣泣之时"
PC7 = os.path.join(PC, "寒蝉鸣泣之时：7皆杀篇", "HigurashiEp07_Data", "StreamingAssets", "voice")
PC8 = os.path.join(PC, "寒蝉鸣泣之时：8祭囃篇", "HigurashiEp08_Data", "StreamingAssets", "voice")

VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]+)"', re.M)


def main():
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

    missing = {p: v for p, v in refs.items()
               if not os.path.exists(os.path.join(PROJ, p.replace("/", os.sep)))}
    print("引用唯一路径:", len(refs), " 工程内缺失:", len(missing))

    # 分章节
    by_s = Counter()
    for p in missing:
        parts = p.split("/")
        by_s[parts[2] if len(parts) > 2 else "?"] += 1
    print("缺失按章节:", dict(sorted(by_s.items(), key=lambda kv: -kv[1])))

    # 逐条在 PC7 / PC8 查
    ok7 = ok8 = nope = 0
    nope_list = []
    for p in missing:
        if os.path.exists(os.path.join(PC7, p.replace("/", os.sep))):
            ok7 += 1
        elif os.path.exists(os.path.join(PC8, p.replace("/", os.sep))):
            ok8 += 1
        else:
            nope += 1
            if len(nope_list) < 25:
                nope_list.append(p)
    print()
    print("可从 PC7(皆杀) 补:", ok7)
    print("可从 PC8(祭囃) 补:", ok8)
    print("PC 版也没有:", nope)
    print("合计可补:", ok7 + ok8, " 覆盖率: %.2f%%"
          % (100.0 * (ok7 + ok8) / max(1, len(missing))))

    if nope_list:
        print()
        print("PC 也没有的样例（前 25）:")
        for p in nope_list:
            print("  ", p)
        cnt = Counter(p.split("/")[2] if len(p.split("/")) > 2 else "?" for p in nope_list)
        print("  这些里面按章节:", dict(cnt))


if __name__ == "__main__":
    main()
