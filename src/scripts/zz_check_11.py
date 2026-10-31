# -*- coding: utf-8 -*-
"""核查：11 处「缺失图」show/scene 是否都在不可能执行的分支里。

判定依据：
  - 外层有 `if not persistent.graphics_sui:` 且 graphics_sui 默认 True -> 不执行
  - 外层有 `if not persistent.music_sui:` 等其它默认开关
  - 外层有 renpy.loadable 守卫
  - 或位于不可能到达的 label
"""
import io
import os
import re

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
K = os.path.join(BASE, "work", "project_k", "game")

TARGETS = [
    ("minagoroshi/mina_019.rpy", 3100, "sa2b_muhyou_b2_0.png"),
    ("tsumihoroboshi/tsum_005.rpy", 116, "si_daidokoro.png"),
    ("tsumihoroboshi/tsum_005.rpy", 202, "mati10.png"),
    ("tsumihoroboshi/tsum_005.rpy", 447, "ke_denwa.png"),
    ("tsumihoroboshi/tsum_008.rpy", 1226, "mo_g3.png"),
    ("tsumihoroboshi/tsum_013.rpy", 138, "tosyo8.png"),
    ("tsumihoroboshi/tsum_021.rpy", 288, "gk2.png"),
    ("tsumihoroboshi/tsum_022.rpy", 249, "tirasi.png"),
    ("tsumihoroboshi/tsum_022.rpy", 1136, "ma_j1.png"),
    ("tsumihoroboshi/tsum_025.rpy", 2639, "gk3_01.png"),
    ("tsumihoroboshi/tsumihoroboshi_tips.rpy", 1275, "terebi.jpg"),
]

IND = re.compile(r'^(\s*)')


def main():
    print("逐条输出 6 行上下文（缩进可见）：\n")
    for rel, ln, png in TARGETS:
        p = os.path.join(K, *rel.split("/"))
        lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
        print("=" * 88)
        print("%s:%d   target=%s" % (rel, ln, png))
        for i in range(max(0, ln - 7), min(len(lines), ln + 2)):
            marker = ">>" if i == ln - 1 else "  "
            print("%s %4d|%s" % (marker, i + 1, lines[i][:120]))
        print()


if __name__ == "__main__":
    main()
