# -*- coding: utf-8 -*-
"""导出全部「译文重复」缺陷为 JSON，供逐条重译后回填。

输出 work/dup_fix_targets.json:
[{"proj":"k/q","file":"matsuribayashi/mats_001.rpy","line":211,"en":"...","wrong_zh":"...","prev_en":"..."}]
"""
import io
import json
import os
import re

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PAIRS = [
    ("k", os.path.join(BASE, "work", "project_k", "game"),
     os.path.join(BASE, "work", "apk_k", "assets", "x-game")),
    ("q", os.path.join(BASE, "work", "project", "game"),
     os.path.join(BASE, "work", "apk_q", "assets", "x-game")),
]
CJK = re.compile(u'[\u4e00-\u9fff]')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')
OUT = os.path.join(BASE, "work", "dup_fix_targets.json")


def rows(path):
    out = []
    for i, line in enumerate(io.open(path, encoding="utf-8", errors="replace").read().split("\n"), 1):
        m = SAY.match(line.rstrip())
        if not m:
            continue
        out.append((i, (m.group(2) or "").strip(), m.group(3)))
    return out


def main():
    targets = []
    for tag, gd, srcdir in PAIRS:
        for cd in sorted(d for d in os.listdir(gd) if os.path.isdir(os.path.join(gd, d))):
            sub = os.path.join(gd, cd)
            for f in sorted(os.listdir(sub)):
                if not f.endswith(".rpy"):
                    continue
                sp = os.path.join(srcdir, "x-" + cd, "x-" + f)
                if not os.path.exists(sp):
                    continue
                nr = rows(os.path.join(sub, f))
                orow = rows(sp)
                if len(nr) != len(orow):
                    continue
                for k in range(1, len(nr)):
                    zprev, zprev_id = nr[k - 1][2], nr[k - 1][1]
                    zcur, zcur_id = nr[k][2], nr[k][1]
                    eprev = orow[k - 1][2]
                    ecur = orow[k][2]
                    if not (CJK.search(zcur) and CJK.search(zprev)):
                        continue
                    if zcur != zprev or ecur == eprev:
                        continue
                    targets.append({
                        "proj": tag,
                        "file": "%s/%s" % (cd, f),
                        "line": nr[k][0],
                        "ident": zcur_id,
                        "en": ecur,
                        "prev_en": eprev,
                        "wrong_zh": zcur,
                        "prev_zh": zprev,
                    })
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fp:
        fp.write(json.dumps(targets, ensure_ascii=False, indent=1))
    print("导出 %d 条 -> %s" % (len(targets), OUT))
    from collections import Counter
    c = Counter(t["proj"] for t in targets)
    print("分布:", dict(c))


if __name__ == "__main__":
    main()
