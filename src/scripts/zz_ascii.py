# -*- coding: utf-8 -*-
"""把截图转成 ASCII 缩略图，直观判断画面布局。"""
import sys, os
from PIL import Image
CH = " .:-=+*#%@"
def render(p, w=76, h=34):
    im = Image.open(p).convert("L").resize((w, h))
    px = list(im.getdata())
    print("=" * 20, os.path.basename(p))
    for y in range(h):
        row = ""
        for x in range(w):
            v = px[y * w + x]
            row += CH[min(len(CH) - 1, v * len(CH) // 256)]
        print(row)
for p in sys.argv[1:]:
    render(p)
