# -*- coding: utf-8 -*-
"""用 voice 文件名做锚点校验台词对齐。

原理：voice 引用（如 170300092.ogg）在原始 APK 与工程里应逐行一一对应，
且相邻行顺序一致。若某行中文台词对应的 voice 与原始 APK 同位置的 voice 不同，
说明该行台词被错位填充。

更直接的检查：把「原始 APK 的英文台词」与「工程的中文台词」按 voice 锚点对齐，
然后只看由本轮自动补译的行（即原 APK 是英文、现在是中文的行），
检查其 ratio 是否与整体分布一致。
"""
import io
import os
import re
import statistics
import sys

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
NEWDIR = os.path.join(BASE, "work", "project_k", "game", "tsumihoroboshi")
OLDDIR = os.path.join(BASE, "work", "apk_k", "assets", "x-game", "x-tsumihoroboshi")

CJK = re.compile(u'[\u4e00-\u9fff]')
TAG = re.compile(r'\{[^{}]*\}')
VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]+)"')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')


def blocks(path):
    """返回 [(voice, [(line, ident, body), ...])]，按 voice 分组。"""
    out = []
    cur = None
    cur_v = None
    for i, line in enumerate(io.open(path, encoding="utf-8", errors="replace").read().split("\n"), 1):
        s = line.rstrip()
        m = VOICE.match(s)
        if m:
            if cur:
                out.append((cur_v, cur))
            cur_v = m.group(1)
            cur = []
            continue
        m = SAY.match(s)
        if m:
            if cur is None:
                cur = []
                cur_v = None
            cur.append((i, (m.group(2) or "").strip(), m.group(3)))
    if cur:
        out.append((cur_v, cur))
    return out


def main():
    fname = sys.argv[1] if len(sys.argv) > 1 else None
    files = [fname] if fname else sorted(
        f for f in os.listdir(NEWDIR)
        if f.endswith(".rpy") and os.path.exists(os.path.join(OLDDIR, "x-" + f)))
    tot_blocks = tot_mis = 0
    for f in files:
        nb = blocks(os.path.join(NEWDIR, f))
        ob = blocks(os.path.join(OLDDIR, "x-" + f))
        # 用 voice 名做 key 对齐
        omap = {}
        for v, rows in ob:
            if v:
                omap.setdefault(v, rows)
        ratios = []
        mis = []
        for v, rows in nb:
            if not v or v not in omap:
                continue
            orows = omap[v]
            # 逐句配对
            for k in range(min(len(rows), len(orows))):
                nl, nid, nbody = rows[k]
                ol, oid, obody = orows[k]
                zh = TAG.sub("", nbody)
                en = TAG.sub("", obody)
                zhc = len(CJK.findall(zh))
                enw = len(re.findall(r"[A-Za-z']+", en))
                if enw < 3 or zhc < 2:
                    continue
                r = zhc / float(enw)
                ratios.append(r)
                if r < 0.35 or r > 6.0:
                    mis.append((v, nl, r, obody[:70], nbody[:70]))
        tot_blocks += len(omap)
        tot_mis += len(mis)
        if not ratios:
            continue
        med = statistics.median(ratios)
        print("%-22s voice锚点=%d 配对=%d 中位=%.2f 离群=%d"
              % (f, len(omap), len(ratios), med, len(mis)))
        for v, nl, r, ob, nb in mis[:8]:
            print("    %s L%d ratio=%.2f" % (v, nl, r))
            print("       EN %s" % ob)
            print("       ZH %s" % nb)
    print()
    print("voice 锚点总数:", tot_blocks, " 离群:", tot_mis)


if __name__ == "__main__":
    main()
