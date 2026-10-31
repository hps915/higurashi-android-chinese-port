# -*- coding: utf-8 -*-
"""v3 UI image generator: regenerate port UI images with Chinese text.

Design specs were extracted from the pristine images via vision analysis:
- Q main menu: dark capsules, thin white border + soft glow, white text
- K main menu: right-aligned thin white text rows; hover = red speed-line banner
- K gmenu tabs: glossy dark-red buttons with icon + white text (erase/redraw text)
- Captions: red pill banner with main text + latin sub-text
- day_completed: blue-gradient double-border buttons
- chapter select: red streak + text entries
Run:  python gen_ui_images.py q|k|all
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

TOOLS = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\tools"
F_BOLD = os.path.join(TOOLS, "NotoSansCJKsc-Bold.otf")
F_REG = os.path.join(TOOLS, "NotoSansCJKsc-Regular.otf")
WORK = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_wh(fnt, s):
    b = ImageDraw.Draw(Image.new("RGBA", (10, 10))).textbbox((0, 0), s, font=fnt)
    return b[2] - b[0], b[3] - b[1], b


def draw_text(im, xy, s, fnt, fill, anchor="la", shadow=None):
    d = ImageDraw.Draw(im)
    if shadow:
        d.text((xy[0] + shadow[0], xy[1] + shadow[1]), s, font=fnt, fill=shadow[2], anchor=anchor)
    d.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def glow_layer(size, draw_fn, blur, color):
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(lay))
    lay = lay.filter(ImageFilter.GaussianBlur(blur))
    return lay


def rounded(im, box, r, fill, outline=None, ow=2, glow=None, gblur=6):
    """Draw rounded rect with optional outer glow; box=(x0,y0,x1,y1)."""
    x0, y0, x1, y1 = box
    if glow:
        g = glow_layer(im.size, lambda d: d.rounded_rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], r, outline=glow, width=3), gblur, glow)
        im.alpha_composite(g)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=ow)
    return im


# ---------- auto measurement ----------
def bright_bbox(im, box, thresh=170):
    """Bounding box of bright pixels inside box (text detection)."""
    x0, y0, x1, y1 = box
    a = np.array(im.crop(box))
    if a.shape[2] == 4:
        mask = (a[:, :, 3] > 60) & (a[:, :, :3].mean(axis=2) > thresh)
    else:
        mask = a[:, :, :3].mean(axis=2) > thresh
    if not mask.any():
        return None
    ys, xs = np.where(mask)
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1)


def scanline_erase(im, box, thresh=150, grow=2):
    """Erase text: bright pixels are replaced by horizontal interpolation between
    the nearest non-bright neighbours on the same row (preserves gradients).
    The old modal-row fill turned any row whose white pixels dominated into a
    solid white streak."""
    x0, y0, x1, y1 = box
    a = np.array(im)
    H, W = a.shape[:2]
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if x1 <= x0 or y1 <= y0:
        return im
    lum = a[:, :, :3].astype(np.float32).mean(axis=2)
    m = np.zeros((H, W), bool)
    m[y0:y1, x0:x1] = lum[y0:y1, x0:x1] > thresh
    for _ in range(grow):
        m2 = m.copy()
        m2[1:, :] |= m[:-1, :]
        m2[:-1, :] |= m[1:, :]
        m2[:, 1:] |= m[:, :-1]
        m2[:, :-1] |= m[:, 1:]
        m = m2
    # restrict to (slightly padded) box so we never eat neighbouring art
    box_m = np.zeros((H, W), bool)
    box_m[max(0, y0 - 4):min(H, y1 + 4), max(0, x0 - 4):min(W, x1 + 4)] = True
    m &= box_m
    out = a.copy()
    todo = np.zeros((H, W), bool)
    for y in range(y0, y1):
        xs = np.where(m[y])[0]
        if len(xs) == 0:
            continue
        for run in np.split(xs, np.where(np.diff(xs) > 1)[0] + 1):
            i, j = int(run[0]), int(run[-1])
            li = i - 1
            while li >= 0 and m[y, li]:
                li -= 1
            ri = j + 1
            while ri < W and m[y, ri]:
                ri += 1
            if li < 0 and ri >= W:
                todo[y, i:j + 1] = True
                continue
            left = a[y, li].astype(np.float32) if li >= 0 else a[y, ri].astype(np.float32)
            right = a[y, ri].astype(np.float32) if ri < W else left
            span = max(1, ri - li)
            t = (np.arange(i - li, j + 1 - li) / float(span))[:, None]
            out[y, i:j + 1] = (left + (right - left) * t).astype(np.uint8)
    # vertical fallback for rows with no background on either side
    for x in range(x0, x1):
        ys = np.where(todo[:, x])[0]
        if len(ys) == 0:
            continue
        for run in np.split(ys, np.where(np.diff(ys) > 1)[0] + 1):
            i, j = int(run[0]), int(run[-1])
            ti = i - 1
            while ti >= 0 and todo[ti, x]:
                ti -= 1
            bi = j + 1
            while bi < H and todo[bi, x]:
                bi += 1
            top = out[ti, x].astype(np.float32) if ti >= 0 else out[bi, x].astype(np.float32)
            bot = out[bi, x].astype(np.float32) if bi < H else top
            span = max(1, bi - ti)
            t = (np.arange(i - ti, j + 1 - ti) / float(span))[:, None]
            out[i:j + 1, x] = (top + (bot - top) * t).astype(np.uint8)
    return Image.fromarray(out)


# ---------- 1. question main menu ----------
def q_main(efe):
    labels = ["开始游戏", "读取存档", "游戏设置", "附加内容", "退出游戏"]
    for kind in ("idle", "hover"):
        im = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
        for i, lab in enumerate(labels):
            y = 361 + 65 * i
            box = (505, y, 790, y + 49)
            if kind == "idle":
                rounded(im, box, 24, (16, 14, 22, 185), (255, 255, 255, 205), 2,
                        glow=(255, 255, 255, 38), gblur=5)
                fill = (255, 255, 255, 235)
            else:
                rounded(im, box, 24, (34, 28, 44, 225), (255, 255, 255, 255), 2,
                        glow=(255, 255, 255, 95), gblur=7)
                fill = (255, 255, 255, 255)
            f = font(F_BOLD, 27)
            w, h, _ = text_wh(f, lab)
            draw_text(im, ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2), lab, f,
                      fill, anchor="mm", shadow=(1, 2, (0, 0, 0, 160)))
        im.save(os.path.join(efe, f"main_{kind}.png"))
    print("q main menus done")


# ---------- 2. kai main menu ----------
def k_main(efe, efe_pristine):
    labels = ["开始游戏", "读取存档", "游戏设置", "附加内容", "退出游戏"]
    # measure right edge from pristine idle
    ref = Image.open(os.path.join(efe_pristine, "x-main_idle.png")).convert("RGBA")
    edges = []
    for i in range(5):
        y = 237 + 29 * i
        bb = bright_bbox(ref, (0, y, 1160, y + 22), 150)
        edges.append(bb[2] if bb else 1160)
    rx = int(np.median(edges))
    for kind in ("idle", "hover"):
        im = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
        for i, lab in enumerate(labels):
            y = 237 + 29 * i
            f = font(F_REG, 21)
            w, h, _ = text_wh(f, lab)
            tx = rx
            if kind == "hover":
                # red speed-line banner: solid rounded band + trailing thin lines
                band = (tx - w - 46, y - 4, min(1168, tx + 10), y + 26)
                g = glow_layer(im.size, lambda d, b=band: d.rounded_rectangle(b, 8, fill=(255, 60, 60, 130)), 8, None)
                im.alpha_composite(g)
                d = ImageDraw.Draw(im)
                d.rounded_rectangle(band, 8, fill=(196, 26, 34, 235))
                for k in range(7):
                    ln = 90 + k * 42
                    ly = band[1] + 5 + k * 3
                    alpha = 200 - k * 26
                    d.rectangle([band[0] - ln, ly, band[0] - 12, ly + 2], fill=(196, 26, 34, max(24, alpha)))
                draw_text(im, (tx, y + 10), lab, f, (255, 255, 255, 255), anchor="rm",
                          shadow=(1, 1, (0, 0, 0, 170)))
            else:
                draw_text(im, (tx, y + 10), lab, f, (240, 240, 240, 215), anchor="rm",
                          shadow=(1, 1, (0, 0, 0, 150)))
        im.save(os.path.join(efe, f"main_{kind}.png"))
    print("k main menus done, right edge =", rx)


# ---------- 3. kai gmenu tabs: erase text, keep icon art ----------
def k_gmenu(efe, efe_pristine):
    labels = {"gmenu_save": "存档", "gmenu_load": "读取", "gmenu_config": "设置",
              "gmenu_exit": "退出", "gmenu_schart": "返回",
              "music_config": "音乐设置"}
    for base, zh in labels.items():
        for kind in ("idle", "hover"):
            name = f"{base}_{kind}.png" if not base.startswith("music") else f"{base}_{'on' if kind=='hover' else 'off'}.png"
            src = os.path.join(efe_pristine, "x-" + name)
            if not os.path.exists(src):
                continue
            im = Image.open(src).convert("RGBA")
            W, H = im.size
            # text = bright pixels in right 65% of image
            bb = bright_bbox(im, (int(W * 0.35), 2, W - 2, H - 2), 160)
            if bb is None:
                im.save(os.path.join(efe, name))
                continue
            pad = 4
            im = scanline_erase(im, (max(0, bb[0] - pad), max(0, bb[1] - pad),
                                     min(W, bb[2] + pad), min(H, bb[3] + pad)))
            # redraw Chinese, centered in the erased zone, size ~ old height*1.15
            oh = bb[3] - bb[1]
            size = max(16, int(oh * 1.18))
            f = font(F_BOLD, size)
            draw_text(im, ((bb[0] + bb[2]) // 2, (bb[1] + bb[3]) // 2), zh, f,
                      (255, 255, 255, 240), anchor="mm", shadow=(1, 1, (0, 0, 0, 150)))
            im.save(os.path.join(efe, name))
    print("k gmenu tabs done")


# ---------- 3b. question game menu strip (sysmenu.png): Save/Load/Config/Title ----------
def q_sysmenu(efe, efe_pristine):
    labels = ["存档", "读取", "设置", "标题"]
    src = Image.open(os.path.join(efe_pristine, "x-sysmenu.png")).convert("RGBA")
    W, H = src.size
    a = np.array(src)
    for i in range(4):
        y0, y1 = 80 * i + 12, 80 * (i + 1) - 12
        for hx0, hx1 in ((0, 264), (264, 528)):
            # wipe the whole text zone (right of the icon); the sheen is a
            # horizontally uniform vertical gradient, so fill each row with a
            # robust (25th pct) colour taken from the zone row itself — the
            # background dominates even on rows crossing thick glyph strokes
            tx0, tx1 = hx0 + 58, hx1 - 10
            refs = []
            for y in range(y0, y1):
                zone = a[y, tx0:tx1, :4].astype(np.float32)
                refs.append(np.percentile(zone, 25, axis=0))
            refs = np.array(refs)
            for k, y in enumerate(range(y0, y1)):
                lo, hi = max(0, k - 1), min(len(refs), k + 2)
                a[y, tx0:tx1, :4] = refs[lo:hi].mean(axis=0).astype(np.uint8)
    im = Image.fromarray(a)
    for i, zh in enumerate(labels):
        f = font(F_BOLD, 34)
        cx = (62 + 254) // 2
        draw_text(im, (cx, 80 * i + 40), zh, f, (255, 255, 255, 235), anchor="mm",
                  shadow=(1, 2, (30, 4, 6, 190)))
        cx2 = 264 + (62 + 254) // 2
        draw_text(im, (cx2, 80 * i + 40), zh, f, (235, 232, 228, 215), anchor="mm",
                  shadow=(1, 2, (30, 4, 6, 150)))
    im.save(os.path.join(efe, "sysmenu.png"))
    print("q sysmenu done")


# ---------- 4. captions (pill banners) ----------
def captions(efe, kai=False):
    m = [("caption_save", "存档", "SAVE"), ("caption_load", "读取", "LOAD"),
         ("caption_log", "回顾", "BACKLOG"), ("caption_tips", "小知识", "TIPS"),
         ("caption_cg", "CG模式", "CG MODE"), ("caption_bgm", "音乐模式", "MUSIC")]
    if kai:
        m.append(("caption_kakera", "碎片", "KAKERA"))
    for name, zh, sub in m:
        W, H = 400, 96
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        # vertical red gradient pill
        grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ga = np.array(grad)
        for y in range(H):
            t = abs(y - H * 0.38) / (H * 0.62)
            r = int(178 - 58 * t)
            g = int(38 - 18 * t)
            b = int(42 - 20 * t)
            ga[y, :] = (r, g, b, 235)
        grad = Image.fromarray(ga)
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).rounded_rectangle([1, 1, W - 2, H - 2], 47, fill=255)
        im.paste(grad, (0, 0), mask)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([1, 1, W - 2, H - 2], 47, outline=(70, 14, 16, 255), width=2)
        d.rounded_rectangle([5, 5, W - 6, H - 6], 43, outline=(255, 120, 110, 70), width=1)
        f1 = font(F_BOLD, 36)
        draw_text(im, (W // 2, 38), zh, f1, (255, 255, 255, 255), anchor="mm",
                  shadow=(2, 2, (60, 8, 10, 200)))
        f2 = font(F_REG, 13)
        draw_text(im, (W // 2, 66), " ".join(sub), f2, (255, 210, 200, 170), anchor="mm")
        im.save(os.path.join(efe, name + ".png"))
    print("captions done" + (" (kai)" if kai else ""))


# ---------- 5. day_completed buttons ----------
def next_buttons(efe):
    labels = [("查看 TIPS", 193), ("保存游戏", 321), ("继续", 449)]
    for kind in ("idle", "hover"):
        im = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
        for lab, y in labels:
            x0, y0, x1, y1 = 460, y, 819, y + 78
            grad = Image.new("RGBA", (x1 - x0, y1 - y0))
            ga = np.array(grad)
            h = y1 - y0
            for yy in range(h):
                t = yy / h
                if kind == "idle":
                    r = int(96 - 30 * t); g = int(140 - 46 * t); b = int(200 - 66 * t)
                else:
                    r = int(130 - 34 * t); g = int(180 - 52 * t); b = int(240 - 66 * t)
                ga[yy, :] = (r, g, b, 235)
            btn = Image.fromarray(ga)
            mask = Image.new("L", btn.size, 0)
            ImageDraw.Draw(mask).rounded_rectangle([1, 1, btn.size[0] - 2, btn.size[1] - 2], 14, fill=255)
            layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
            layer.paste(btn, (x0, y0), mask)
            # glow
            gcol = (160, 220, 255, 70 if kind == "idle" else 130)
            gl = glow_layer(im.size, lambda d, b=(x0, y0, x1, y1): d.rounded_rectangle(b, 14, outline=gcol, width=4), 6, gcol)
            im.alpha_composite(gl)
            im.alpha_composite(layer)
            d = ImageDraw.Draw(im)
            d.rounded_rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], 14, outline=(255, 255, 255, 225), width=2)
            d.rounded_rectangle([x0 + 5, y0 + 5, x1 - 5, y1 - 5], 10, outline=(255, 255, 255, 60), width=1)
            f = font(F_BOLD, 30)
            draw_text(im, ((x0 + x1) // 2, (y0 + y1) // 2), lab, f, (255, 255, 255, 255),
                      anchor="mm", shadow=(2, 2, (10, 20, 50, 170)))
        im.save(os.path.join(efe, f"next_{kind}.png"))
    print("next buttons done")


# ---------- 6. chapter select (question) ----------
def scenario(efe, efe_pristine):
    zh = ["鬼隐篇 ～开幕～", "绵流篇 ～核心的真相～", "祟杀篇 ～最短的剧本～", "暇溃篇 ～最后的谜题～"]
    # base: erase "SCENARIO SELECT" on the red flag
    base = Image.open(os.path.join(efe_pristine, "x-scenario_b.png")).convert("RGBA")
    W, H = base.size
    bb = bright_bbox(base, (0, 0, W // 2, H), 200)
    if bb:
        base = scanline_erase(base, (bb[0] - 6, bb[1] - 6, bb[2] + 6, bb[3] + 6))
        f = font(F_BOLD, bb[3] - bb[1] - 2)
        draw_text(base, ((bb[0] + bb[2]) // 2, (bb[1] + bb[3]) // 2), "章节选择", f,
                  (255, 255, 255, 255), anchor="mm", shadow=(2, 2, (40, 0, 0, 200)))
    base.save(os.path.join(efe, "scenario_b.png"))
    # idle/hover: find entry rows, erase old text, draw streak + Chinese
    for kind in ("idle", "hover"):
        im = Image.open(os.path.join(efe_pristine, f"x-scenario_{kind}.png")).convert("RGBA")
        W, H = im.size
        # rows with content: scan y for bright pixel density
        a = np.array(im)
        rowmask = (a[:, :, :3].mean(axis=2) > 150) & (a[:, :, 3] > 60)
        rows = []
        y = 100
        while y < H - 40:
            if rowmask[y, :900].sum() > 15:
                y2 = y
                while y2 < H - 1 and rowmask[y2, :900].sum() > 3:
                    y2 += 1
                if y2 - y > 24:
                    rows.append((y, y2))
                y = y2 + 30
            else:
                y += 1
        rows = rows[:8]
        # merge adjacent rows (main line + English subtitle line) into entries
        merged = []
        for r in rows:
            if merged and r[0] - merged[-1][1] < 42:
                merged[-1] = (merged[-1][0], r[1])
            else:
                merged.append(r)
        rows = merged[:4]
        for i, (ry0, ry1) in enumerate(rows):
            if i >= len(zh):
                break
            # text bbox in this row band (main title line)
            bb = bright_bbox(im, (0, ry0, 1000, ry1), 140)
            if bb is None:
                continue
            # erase main line + AA edges (rows expanded) + the English subtitle
            # line below the band (dimmer than the main text, right edge wider)
            x_erase = max(0, bb[0] - 150)
            x_right = min(W, max(bb[2] + 8, 470))
            im = scanline_erase(im, (x_erase, max(0, ry0 - 6), x_right, min(H, ry1 + 42)),
                                thresh=120)
            # redraw streak: solid red band at left + trailing lines
            d = ImageDraw.Draw(im)
            text_h = bb[3] - bb[1]
            f = font(F_BOLD, max(24, min(32, int(text_h * 0.62))))
            w, h, _ = text_wh(f, zh[i])
            band = (bb[0] - 26, ry0 + 1, min(W - 4, bb[0] - 20 + 22 + w + 14), ry1 - 1)
            d.rounded_rectangle(band, 5, fill=(196, 26, 34, 235))
            for k in range(5):
                ln = 70 + k * 34
                ly = band[1] + 4 + k * ((band[3] - band[1]) // 6)
                d.rectangle([band[0] - ln, ly, band[0] - 10, ly + 2],
                            fill=(196, 26, 34, max(24, 190 - k * 30)))
            draw_text(im, (band[0] + 12, (band[1] + band[3]) // 2), zh[i], f,
                      (255, 255, 255, 255), anchor="lm", shadow=(1, 1, (60, 0, 0, 180)))
        im.save(os.path.join(efe, f"scenario_{kind}.png"))
    print("scenario done, entries:", len(rows))


# ---------- 7. quick menu labels ----------
def quick_menu(efe, efe_pristine):
    labels = ["自动", "跳过", "回顾", "菜单"]
    for name in ("quick_menu_idle", "quick_menu_hover", "quick_menu_insensitive"):
        srcp = os.path.join(efe_pristine, "x-" + name + ".png")
        if not os.path.exists(srcp):
            continue
        im = Image.open(srcp).convert("RGBA")
        for i, lab in enumerate(labels):
            y = 530 + 48 * i
            box = (1229, y + 22, 1279, y + 42)
            bb = bright_bbox(im, box, 110) or (1233, y + 28, 1277, y + 40)
            im = scanline_erase(im, (bb[0] - 3, bb[1] - 2, min(1279, bb[2] + 3), bb[3] + 2))
            f = font(F_BOLD, 13)
            draw_text(im, (1253, y + 32), lab, f, (215, 215, 215, 235), anchor="mm",
                      shadow=(1, 1, (0, 0, 0, 160)))
        im.save(os.path.join(efe, name + ".png"))
    print("quick menu done")
def menu_capsules(efe):
    for kind in ("idle", "hover"):
        W, H = 360, 78
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if kind == "idle":
            rounded(im, (2, 2, W - 3, H - 3), 16, (36, 62, 108, 165), (150, 205, 255, 190), 2,
                    glow=(120, 180, 255, 40), gblur=5)
        else:
            rounded(im, (2, 2, W - 3, H - 3), 16, (60, 105, 175, 200), (200, 235, 255, 255), 2,
                    glow=(140, 200, 255, 110), gblur=7)
        im.save(os.path.join(efe, f"zz_capsule_{kind}.png"))
    print("capsules done")


# ---------- 9. preferences panel ----------
def prefs_panel(efe):
    W, H = 1180, 660
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rounded(im, (3, 3, W - 4, H - 4), 18, (14, 12, 20, 238), (198, 178, 128, 130), 2,
            glow=(0, 0, 0, 160), gblur=10)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, W - 11, H - 11), 13, outline=(255, 255, 255, 26), width=1)
    im.save(os.path.join(efe, "zz_prefs_panel.png"))
    print("prefs panel done")


# ---------- 10. tips popup card ----------
def tips_card(efe):
    W, H = 760, 330
    im = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
    x0, y0, x1, y1 = (1280 - W) // 2, (720 - H) // 2, (1280 + W) // 2, (720 + H) // 2
    rounded(im, (x0, y0, x1, y1), 20, (12, 10, 18, 240), (215, 190, 135, 170), 2,
            glow=(0, 0, 0, 190), gblur=12)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0 + 8, y0 + 8, x1 - 8, y1 - 8), 15, outline=(255, 255, 255, 22), width=1)
    d.rounded_rectangle((x0 + 18, y0 + 16, x0 + 152, y0 + 48), 16, fill=(180, 30, 36, 235))
    f = font(F_BOLD, 20)
    draw_text(im, (x0 + 85, y0 + 32), "新 TIPS 解锁", f, (255, 255, 255, 255), anchor="mm")
    im.save(os.path.join(efe, "zz_tips_card.png"))
    print("tips card done")




# ---------- 11. small capsule for prefs buttons ----------
def small_capsules(efe):
    for kind in ("idle", "hover"):
        W, H = 150, 46
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if kind == "idle":
            rounded(im, (1, 1, W - 2, H - 2), 12, (30, 34, 52, 200), (170, 185, 220, 170), 1,
                    glow=(120, 150, 220, 30), gblur=3)
        else:
            rounded(im, (1, 1, W - 2, H - 2), 12, (52, 62, 96, 220), (230, 240, 255, 255), 2,
                    glow=(150, 180, 240, 90), gblur=5)
        im.save(os.path.join(efe, f"zz_small_{kind}.png"))
    print("small capsules done")


# ---------- 12. dialog panel ----------
def dialog_panel(efe):
    W, H = 740, 260
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rounded(im, (2, 2, W - 3, H - 3), 18, (18, 15, 24, 245), (210, 190, 140, 160), 2,
            glow=(0, 0, 0, 200), gblur=9)
    ImageDraw.Draw(im).rounded_rectangle((9, 9, W - 10, H - 10), 13, outline=(255, 255, 255, 24), width=1)
    im.save(os.path.join(efe, "zz_dialog.png"))
    print("dialog panel done")




# ---------- 13. kai chapter select (blue bands) ----------
def k_scenario(efe, efe_pristine):
    names = ["目明篇", "罪灭篇", "皆杀篇", "祭囃篇"]
    subs = ["～挚爱的杀人魔～", "～最初的坠落～", "～最终的真相～", "～至少让一切终结于美梦～"]
    ys = [189, 283, 377, 611]
    # flag: erase SCENARIO SELECT, draw 章节选择
    # K 的底图是不透明天空+月亮，自动 bbox 会被月亮撑爆（曾画出 386px 巨字）；
    # 实测两作 "SCENARIO SELECT" 都在 (45,66)-(533,102)，固定使用该几何。
    fb = os.path.join(efe_pristine, "x-scenario_b.png")
    if os.path.exists(fb):
        base = Image.open(fb).convert("RGBA")
        bb = (45, 66, 533, 102)
        base = scanline_erase(base, (bb[0] - 6, bb[1] - 6, bb[2] + 6, bb[3] + 6), thresh=200)
        f = font(F_BOLD, bb[3] - bb[1] - 2)
        draw_text(base, ((bb[0] + bb[2]) // 2, (bb[1] + bb[3]) // 2), "章节选择", f,
                  (255, 255, 255, 255), anchor="mm", shadow=(2, 2, (40, 0, 0, 200)))
        base.save(os.path.join(efe, "scenario_b.png"))
    for kind in ("idle", "hover"):
        src = os.path.join(efe_pristine, f"x-scenario_kai_{kind}.png")
        if not os.path.exists(src):
            print("  !! no", src)
            continue
        im = Image.open(src).convert("RGBA")
        for i, y in enumerate(ys):
            bb = bright_bbox(im, (0, y + 2, 660, y + 76), 150)
            if bb is None:
                continue
            im = scanline_erase(im, (0, max(0, bb[1] - 4), min(660, bb[2] + 8), min(im.size[1], bb[3] + 4)))
            f1 = font(F_BOLD, 30)
            f2 = font(F_REG, 21)
            draw_text(im, (44, y + 12), names[i], f1, (255, 255, 255, 245), anchor="lm",
                      shadow=(1, 1, (0, 0, 40, 170)))
            draw_text(im, (46, y + 48), subs[i], f2, (225, 232, 255, 235), anchor="lm",
                      shadow=(1, 1, (0, 0, 40, 150)))
        im.save(os.path.join(efe, f"scenario_kai_{kind}.png"))
    print("k scenario done")


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    qefe = os.path.join(WORK, "project", "game", "efe")
    kefe = os.path.join(WORK, "project_k", "game", "efe")
    qprim = os.path.join(WORK, "apk_q", "assets", "x-game", "x-efe")
    kprim = os.path.join(WORK, "apk_k", "assets", "x-game", "x-efe")
    if which in ("all", "q"):
        q_main(qefe)
        q_sysmenu(qefe, qprim)
        captions(qefe)
        next_buttons(qefe)
        scenario(qefe, qprim)
        quick_menu(qefe, qprim)
        menu_capsules(qefe)
        prefs_panel(qefe)
        small_capsules(qefe)
        dialog_panel(qefe)
        tips_card(qefe)
    if which in ("all", "k"):
        k_main(kefe, kprim)
        k_gmenu(kefe, kprim)
        k_scenario(kefe, kprim)
        captions(kefe, kai=True)
        next_buttons(kefe)
        quick_menu(kefe, kprim)
        menu_capsules(kefe)
        prefs_panel(kefe)
        tips_card(kefe)
        small_capsules(kefe)
        dialog_panel(kefe)


if __name__ == "__main__":
    main()
