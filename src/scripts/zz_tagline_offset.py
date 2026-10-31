# -*- coding: utf-8 -*-
"""精确定位「{w=} 独立行」造成的偏移缺陷（只读）。

根因：源包里句子被拆成
  extend "...前半"
  n "{w=0.8}"        <- 纯计时行
  extend "...后半"
而工程把中文错位了一格。

检出方法（按 say 行序号严格对齐）：
  对每个文件，把 工程 say 行 与 源包 say 行 按序号配对，
  找出源包该行内容为「纯 {w=...} / 纯 {nw} / 空」但工程该行却是实质中文的位置。
"""
import io
import os
import re

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
K = os.path.join(BASE, "work", "project_k", "game", "tsumihoroboshi")
SRC = os.path.join(BASE, "work", "apk_k", "assets", "x-game", "x-tsumihoroboshi")

SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')
CJK = re.compile(u'[\u4e00-\u9fff]')
ONLY_TAG = re.compile(r'^(\s*\{[^{}]*\})+\s*$')


def rows(p):
    out = []
    for i, l in enumerate(io.open(p, encoding="utf-8", errors="replace").read().split("\n"), 1):
        m = SAY.match(l.rstrip())
        if m:
            out.append((i, m.group(2) or "", m.group(3)))
    return out


def main():
    hits = []
    for f in sorted(os.listdir(K)):
        if not f.endswith(".rpy"):
            continue
        sp = os.path.join(SRC, "x-" + f)
        if not os.path.exists(sp):
            continue
        zh = rows(os.path.join(K, f))
        en = rows(sp)
        if len(zh) != len(en):
            print("!! 行数不一致 %s: zh=%d en=%d" % (f, len(zh), len(en)))
            continue
        for k in range(len(zh)):
            zl, zid, zbody = zh[k]
            el, eid, ebody = en[k]
            # 源包该行是纯标签/空，但工程是中文
            if ONLY_TAG.match(ebody) and CJK.search(zbody):
                hits.append((f, zl, ebody.strip(), zbody.strip()[:70]))
    print("发现 %d 处「源为纯标签、工程为中文」的错位点：" % len(hits))
    for f, ln, e, z in hits:
        print("  %-22s L%-5d  源=%s  工程=%s" % (f, ln, e, z))


if __name__ == "__main__":
    main()
