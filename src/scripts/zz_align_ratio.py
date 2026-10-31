# -*- coding: utf-8 -*-
"""评估自动补译的对齐质量：

思路：如果对齐正确，译文（中文）长度与源英文长度的比值应落在合理区间
（中文字符数 ≈ 英文词数 × 1.5~2.5）。若某行比值极端，说明串行。

同时利用一个更强的信号：语料里 jp 与 zh 都是官方文本，二者比值稳定；
如果某行的 zh 与它**相邻行**的 zh 在语料里也是这个顺序，则认为正确。

这里用可操作的指标：
 1) 计算每行 (中文有效字符数) / (英文词数)，统计分布
 2) 找出比值 < 0.25 或 > 6 的离群行 —— 这些大概率错位
"""
import io
import os
import re
import sys
import statistics

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PAIRS = [
    ("tsum", os.path.join(BASE, "work", "project_k", "game", "tsumihoroboshi"),
     os.path.join(BASE, "work", "apk_k", "assets", "x-game", "x-tsumihoroboshi")),
]

CJK = re.compile(u'[\u4e00-\u9fff\u3040-\u30ff]')
TAG = re.compile(r'\{[^{}]*\}')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')


def rows_of(path):
    out = []
    for i, line in enumerate(io.open(path, encoding="utf-8", errors="replace").read().split("\n"), 1):
        m = SAY.match(line.rstrip())
        if not m:
            continue
        out.append((i, (m.group(2) or "").strip(), m.group(3)))
    return out


def main():
    fname = sys.argv[1] if len(sys.argv) > 1 else None
    total_out = 0
    for label, newdir, olddir in PAIRS:
        files = [fname] if fname else sorted(
            f for f in os.listdir(newdir) if f.endswith(".rpy")
            and os.path.exists(os.path.join(olddir, "x-" + f)))
        for f in files:
            newp = os.path.join(newdir, f)
            oldp = os.path.join(olddir, "x-" + f)
            nr = rows_of(newp)
            orow = rows_of(oldp)
            # 按顺序配对（文件行结构一致才可以；这里用序号配对做粗估）
            if len(nr) != len(orow):
                print("%-24s 行数不一致 new=%d old=%d（跳过比值分析）" % (f, len(nr), len(orow)))
                continue
            ratios = []
            outl = []
            for (nl, nident, nb), (ol, oident, ob) in zip(nr, orow):
                zh = TAG.sub("", nb)
                en = TAG.sub("", ob)
                zhc = len(CJK.findall(zh))
                enw = len(re.findall(r"[A-Za-z']+", en))
                if enw < 3 or zhc < 2:
                    continue
                r = zhc / float(enw)
                ratios.append(r)
                if r < 0.30 or r > 7.0:
                    outl.append((nl, r, ob[:80], nb[:80]))
            if not ratios:
                continue
            med = statistics.median(ratios)
            print("%-24s 中位数=%.2f  样本=%d  离群=%d" % (f, med, len(ratios), len(outl)))
            total_out += len(outl)
            for nl, r, ob, nb in outl[:6]:
                print("    L%d ratio=%.2f" % (nl, r))
                print("       EN %s" % ob)
                print("       ZH %s" % nb)
    print()
    print("离群总数:", total_out)


if __name__ == "__main__":
    main()
