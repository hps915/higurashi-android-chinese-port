# -*- coding: utf-8 -*-
"""Redraw config_ground.png with Chinese labels (box list from detection)."""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

TOOLS = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\tools"
FONT = os.path.join(TOOLS, "NotoSansCJKsc-Bold.otf")

TRANS = {
    0: "播放语音", 1: "播放音效", 2: "播放BGM", 3: "自动播放", 4: "跳过未读文本",
    5: "ADV模式", 6: "NVL模式", 7: "口型同步", 8: "隐藏文本窗口", 9: "仅语音模式",
    10: "播放语音", 11: "BGM音量", 12: "播放音效", 13: "音效音量", 14: "播放BGM",
    15: "自动推进时间", 16: "语音音量", 17: "自动播放", 18: "文字速度",
    19: "画面特效", 20: "永久 开/关", 21: "VM等级", 22: "ADV模式",
}


def main(src, boxes_json, outs):
    boxes = json.load(open(boxes_json))
    im = Image.open(src).convert("RGBA")
    arr = np.array(im)
    draw = ImageDraw.Draw(im)
    for i, zh in TRANS.items():
        if i >= len(boxes):
            continue
        bx0, by0, bx1, by1 = boxes[i]
        region = arr[by0:by1, bx0:bx1]
        mask = (region[:, :, 3] > 100) & (region[:, :, :3].mean(axis=2) > 110)
        if mask.any():
            tc = tuple(int(v) for v in region[mask][:, :3].mean(axis=0))
        else:
            tc = (220, 220, 220)
        ex0 = max(0, bx0 - 5); ey0 = max(0, by0 - 5)
        ex1 = min(arr.shape[1], bx1 + 5); ey1 = min(arr.shape[0], by1 + 5)
        er = arr[ey0:ey1, ex0:ex1]
        emask = er[:, :, 3] > 100
        if emask.any():
            vals = er[emask][:, :3].mean(axis=1)
            order = np.argsort(vals)
            n = max(1, len(order) // 4)
            bg = tuple(int(v) for v in er[emask][order[:n]][:, :3].mean(axis=0))
            bga = 255
        else:
            bg, bga = (20, 18, 16), 0
        h = by1 - by0
        size = int(h * 1.1)
        font = ImageFont.truetype(FONT, size)
        draw.rectangle([bx0 - 7, by0 - 6, bx1 + 7, by1 + 6], fill=bg + (bga,))
        tb = draw.textbbox((0, 0), zh, font=font)
        ty = by0 - tb[1] + (h - (tb[3] - tb[1])) // 2
        draw.text((bx0, ty), zh, font=font, fill=tc + (255,))
    for out in outs:
        im.save(out)
        print("saved", out)


if __name__ == "__main__":
    src = sys.argv[1]
    boxes = sys.argv[2]
    outs = sys.argv[3:]
    main(src, boxes, outs)
