# -*- coding: utf-8 -*-
"""对截图做像素统计，用于判定当前画面状态（黑屏/文字/菜单/视频）。"""
import sys, os
from PIL import Image
def stats(p):
    im = Image.open(p).convert("RGB")
    w, h = im.size
    small = im.resize((160, 80))
    px = list(small.getdata())
    n = len(px)
    mean = tuple(sum(c[i] for c in px) / n for i in range(3))
    bright = sum(1 for r, g, b in px if (r + g + b) / 3 > 40) / float(n)
    # 彩色度：最大通道差
    colorful = sum(1 for r, g, b in px if max(r, g, b) - min(r, g, b) > 40) / float(n)
    # 右下角快捷栏区域亮度（游戏 1235-1277 x 530-715 -> screen 2710-2794 x 1060-1430）
    box = im.crop((2680, 1020, 2830, 1440)).resize((40, 40))
    qpx = list(box.getdata())
    qb = sum(1 for r, g, b in qpx if (r + g + b) / 3 > 110) / float(len(qpx))
    return dict(size=(w, h), mean=tuple(round(x) for x in mean), bright=round(bright, 3),
                colorful=round(colorful, 3), quickbar=round(qb, 3))
if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(os.path.basename(p), stats(p))
