# -*- coding: utf-8 -*-
"""Redraw baked-in English UI images with Chinese text.

For each target image: detect bright text pixels inside given rectangles,
sample the text colour + local background, erase the text area, render the
Chinese replacement with Noto Serif CJK at a matching size.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

TOOLS = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\tools"
SERIF = os.path.join(TOOLS, "NotoSansCJKsc-Bold.otf")


def detect_text_bbox(arr, box, thresh=120):
    x0, y0, x1, y1 = box
    region = arr[y0:y1, x0:x1]
    alpha = region[:, :, 3] > 100
    bright = region[:, :, :3].mean(axis=2) > thresh
    mask = alpha & bright
    if not mask.any():
        return None
    ys, xs = np.where(mask)
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1)


def process(path, entries, out_path=None, font_size=None):
    """entries: list of (rect, chinese_text, align) — rect=(x0,y0,x1,y1) search box."""
    im = Image.open(path).convert("RGBA")
    arr = np.array(im)
    draw = ImageDraw.Draw(im)
    for rect, zh, *_ in entries:
        bbox = detect_text_bbox(arr, rect)
        if not bbox:
            print(f"  !! no text found in {rect} of {os.path.basename(path)}")
            continue
        bx0, by0, bx1, by1 = bbox
        # sample text colour from the bbox
        region = arr[by0:by1, bx0:bx1]
        mask = (region[:, :, 3] > 100) & (region[:, :, :3].mean(axis=2) > 120)
        if mask.any():
            tc = tuple(int(v) for v in region[mask][:, :3].mean(axis=0))
        else:
            tc = (230, 230, 230)
        # background: darkest quartile inside a slightly expanded box
        ex0 = max(0, bx0 - 4); ey0 = max(0, by0 - 4)
        ex1 = min(arr.shape[1], bx1 + 4); ey1 = min(arr.shape[0], by1 + 4)
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
        size = font_size or int(h * 1.25)
        font = ImageFont.truetype(SERIF, size)
        # erase (expand erase box a little to catch anti-aliasing)
        draw.rectangle([bx0 - 6, by0 - 5, bx1 + 6, by1 + 5], fill=bg + (bga,))
        # draw, vertically centred on the old bbox, left-aligned at bx0
        tb = draw.textbbox((0, 0), zh, font=font)
        ty = by0 - (tb[1]) + (h - (tb[3] - tb[1])) // 2
        draw.text((bx0, ty), zh, font=font, fill=tc + (255,))
    im.save(out_path or path)
    print(f"  redrawn {os.path.basename(out_path or path)} ({len(entries)} labels)")


def main_menu_question(efe_dir):
    labels = ["开始游戏", "读取存档", "游戏设置", "附加内容", "退出游戏"]
    entries = []
    for i, lab in enumerate(labels):
        y = 361 + 65 * i
        entries.append(((505, y, 790, y + 49), lab))
    for f in ("main_idle.png", "main_hover.png"):
        process(os.path.join(efe_dir, f), entries)


def main_menu_kai(efe_dir):
    labels = ["开始游戏", "读取存档", "游戏设置", "附加内容", "退出游戏"]
    entries = []
    for i, lab in enumerate(labels):
        y = 237 + 29 * i
        entries.append(((300, y, 1160, y + 22), lab))
    for f in ("main_idle.png", "main_hover.png"):
        process(os.path.join(efe_dir, f), entries, font_size=22)


def gmenu_tabs(efe_dir):
    m = {"gmenu_save_idle": "存档", "gmenu_save_hover": "存档",
         "gmenu_load_idle": "读取", "gmenu_load_hover": "读取",
         "gmenu_config_idle": "设置", "gmenu_config_hover": "设置",
         "gmenu_exit_idle": "退出", "gmenu_exit_hover": "退出",
         "gmenu_schart_idle": "流程图", "gmenu_schart_hover": "流程图",
         "music_config_on": "设置", "music_config_off": "设置"}
    for name, zh in m.items():
        p = os.path.join(efe_dir, name + ".png")
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
            w, h = im.size
            process(p, [((0, 0, w, h), zh)])


def captions(efe_dir, kai=False):
    m = {"caption_save": "存档", "caption_load": "读取", "caption_log": "回顾",
         "caption_tips": "小知识", "caption_cg": "CG模式", "caption_bgm": "音乐模式"}
    if kai:
        m["caption_kakera"] = "碎片"
    for name, zh in m.items():
        p = os.path.join(efe_dir, name + ".png")
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
            w, h = im.size
            process(p, [((0, 0, w, h), zh)])


if __name__ == "__main__":
    Q = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game\efe"
    K = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\efe"
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "q"):
        main_menu_question(Q)
        captions(Q)
        gmenu_tabs(Q)
    if which in ("all", "k"):
        main_menu_kai(K)
        captions(K, kai=True)
        gmenu_tabs(K)
