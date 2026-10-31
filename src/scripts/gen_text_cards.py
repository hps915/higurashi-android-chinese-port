# -*- coding: utf-8 -*-
"""Regenerate text/*.png story cards with Chinese.

The English of the 97 sub-chapter cards is baked into the PNGs (referenced by
`show text <name>` / `scene text <name>`); translations come from
poems_extra.POEMS_EXTRA.  For each card: detect the original text blocks,
erase them (flat background fill), and re-render the Chinese centered on the
original text area with a matching serif font.  Zero .rpy changes needed.
"""
import importlib.util
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

TOOLS = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\tools"
F_SERIF = os.path.join(TOOLS, "NotoSerifCJKsc-Bold.otf")
WORK = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work"

spec = importlib.util.spec_from_file_location(
    "poems_extra", os.path.join(WORK, "scripts", "poems_extra.py"))
PE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PE)
EXTRA = PE.POEMS_EXTRA

MAX_W = 980          # max pixel width of the rendered text column
LINE_SPACING = 1.55  # multiple of font size between lines
STANZA_GAP = 0.85    # extra multiple of font size at blank lines


def font(sz):
    return ImageFont.truetype(F_SERIF, sz)


def text_blocks(a):
    """Rows containing text pixels, grouped into blocks. Returns (blocks,
    text_mask, bg_is_dark).

    Handles both card families: black background with white text (purity by
    luminance) and white background with red/black text (purity by saturation
    when the card is overwhelmingly white)."""
    lum = a[:, :, :3].astype(np.float32).mean(axis=2)
    bright = lum > 115
    dark = lum < 115
    nb, nd = int(bright.sum()), int(dark.sum())
    # text pixels are the minority (background dominates every card)
    if nb <= nd:
        mask, bg_is_dark = bright, True
    else:
        mask, bg_is_dark = dark, False
    # White-bg cards whose text is RED: red pixels have luminance ~76, so the
    # plain `lum < 115` mask works, but coloured fringe pixels lighter than 115
    # would be missed. Add saturated pixels when the card is mostly white.
    if not bg_is_dark and bright.sum() > a.shape[0] * a.shape[1] * 0.8:
        sat = a[:, :, :3].max(axis=2) - a[:, :, :3].min(axis=2)
        mask = mask | (sat > 24)
    rows = mask.sum(axis=1)
    textrows = rows > 3
    blocks = []
    y = 0
    H = a.shape[0]
    while y < H:
        if textrows[y]:
            y2 = y
            while y2 < H and (textrows[y2] or (y2 - y < 12 and y2 + 1 < H and textrows[min(H - 1, y2 + 1)])):
                y2 += 1
            blocks.append((y, y2))
            y = y2
        y += 1
    blocks = [(b0, b1) for b0, b1 in blocks if b1 - b0 > 6]
    return blocks, mask, bg_is_dark


def table_pairs():
    """(key, proj) pairs from the KEY -> SOURCE table in poems_extra.py.
    Range rows like `meaed1..7` expand to meaed1..meaed7.

    The table is aligned with padded spaces (`nort5   | project_k |`), so the
    separator must be `\\s*\\|\\s*` — a single literal space silently dropped
    nort5/19/26/27/43 (their cards stayed in English).

    Rows whose key carries an explicit project suffix (`tyuui@project_k`) have
    no project column, so they are matched by a second pattern."""
    import re
    src = open(os.path.join(WORK, "scripts", "poems_extra.py"), encoding="utf-8").read()
    out = []
    for m in re.finditer(r'^(\S+)\s*\|\s*(project(?:_k)?)\s*\|', src, re.M):
        key, proj = m.group(1), m.group(2)
        rm = re.match(r'^(.*?)(\d+)\.\.(\d+)$', key)
        if rm:
            pre, a, b = rm.group(1), int(rm.group(2)), int(rm.group(3))
            w = len(rm.group(2))
            out += [(pre + str(i).zfill(w), proj) for i in range(a, b + 1)]
        else:
            out.append((key, proj))
    # rows like:  tyuui@project_k | mats_op.rpy:14 ... (no project column)
    for m in re.finditer(r'^(\S+@project(?:_k)?)\s*\|', src, re.M):
        out.append((m.group(1), m.group(1).split("@", 1)[1]))
    return out


def image_file_map(proj):
    """image <any tag> <name> = "text/<file>.png" definitions from script.rpy.
    Covers `image text si_x = ...` as well as `image chapter meak_1 = ...`
    (the chapter number cards title_mea*/title_tsumi*/title_mina*)."""
    import re
    p = os.path.join(WORK, proj, "game", "script.rpy")
    if not os.path.exists(p):
        return {}
    src = open(p, encoding="utf-8").read()
    # `image text NAME = "text/FILE"` -> keyed by NAME
    m = dict(re.findall(r'image text (\w+) = "text/([^"]+)"', src))
    # `image chapter NAME = "text/FILE"` -> keyed by the FILE stem, which is
    # what the POEMS_EXTRA table uses (title_mea, title_tsumi, title_mina)
    for tag, _name, f in re.findall(r'image (chapter) (\w+) = "text/([^"]+)"', src):
        m.setdefault(os.path.splitext(os.path.basename(f))[0], os.path.basename(f))
    return m


def render_card(proj, key, zh_raw):
    if "@" in key:
        k2, p2 = key.split("@", 1)
        if p2 != proj:
            return None
        key = k2
    fname = image_file_map(proj).get(key, key)
    apk = "apk_q" if proj == "project" else "apk_k"
    src = os.path.join(WORK, apk, "assets", "x-game", "x-text", "x-" + fname)
    p = os.path.join(WORK, proj, "game", "text", fname)
    if not os.path.exists(src):
        src = p
    if not os.path.exists(src):
        return None
    im = Image.open(src).convert("RGBA")
    a = np.array(im)
    H, W = a.shape[:2]
    blocks, mask, bg_is_dark = text_blocks(a)
    if not blocks:
        return None
    # 排除右下角签名块（如 Frederica Bernkastel，x 中心 > 0.7W）——否则会把
    # 整个版面中心带偏到右下（曾导致 8 张诗卡偏移 + 签名被裁掉）
    main_blocks = []
    for b0, b1 in blocks:
        bx = np.where(mask[b0:b1].any(axis=0))[0]
        bcx = (bx.min() + bx.max()) / 2 if len(bx) else 0
        if bcx <= W * 0.7:
            main_blocks.append((b0, b1))
    if not main_blocks:
        main_blocks = blocks
    y0, y1 = main_blocks[0][0], main_blocks[-1][1]
    xs = np.where(mask[y0:y1].any(axis=0))[0]
    cx = W // 2
    cy = (y0 + y1) // 2
    # text colour = mean of text pixels; background = modal colour per row
    tp = a[y0:y1][mask[y0:y1]]
    tcol = tuple(int(v) for v in tp[:, :3].mean(axis=0)) if len(tp) else (255, 255, 255)
    tcol = tcol + (255,)
    # erase: every row containing (or near) text pixels gets the flat
    # background colour — the cards have plain black/white backgrounds.
    # Rows are also selected by a LOW-threshold fringe mask (>14 from bg), not
    # only by the >115 "bright" mask: the anti-aliased 20..110 grey halo
    # around every old glyph lives below the bright threshold and used to
    # survive as visible dirt.
    out = a.copy()
    lum = a[:, :, :3].astype(np.float32).mean(axis=2)
    nonmask = ~mask
    if nonmask.any():
        vals, counts = np.unique(a[nonmask].reshape(-1, a.shape[-1]), axis=0, return_counts=True)
        bgc = vals[counts.argmax()]
    else:
        bgc = np.zeros(a.shape[-1], dtype=a.dtype)
    bglum = float(bgc[:3].mean())
    # any pixel that differs from the flat background is either a glyph body
    # (already in `mask`) or its anti-aliased fringe -> both belong to a text
    # row and must be painted out.
    fringe = np.abs(lum - bglum) > 14
    eraserows = (mask | fringe).sum(axis=1) > 1
    for y in range(H):
        lo = max(0, y - 6)
        hi = min(H, y + 7)
        if not eraserows[lo:hi].any():
            continue
        row = out[y]
        non = row[~mask[y]] if mask[y].any() else row
        if len(non) == 0:
            continue
        vals, counts = np.unique(non.reshape(-1, non.shape[-1]), axis=0, return_counts=True)
        row[:] = vals[counts.argmax()]
    # segments: literal backslash-n in the value = newline
    segs = zh_raw.replace("\\r", "").split("\\n")
    # font size: match the median single-line block height
    heights = sorted(b1 - b0 for b0, b1 in blocks)
    if len(heights) > 2:
        med = heights[len(heights) // 2]
    else:
        med = heights[0] if heights else 40
    fs = int(max(18, min(44, med * 1.02)))

    def wrap(fs_):
        f_ = font(fs_)
        out_lines = []
        for s in segs:
            if not s:
                out_lines.append("")
                continue
            while f_.getlength(s) > MAX_W and len(s) > 2:
                k = len(s)
                while k > 1 and f_.getlength(s[:k]) > MAX_W:
                    k -= 1
                out_lines.append(s[:k])
                s = s[k:]
            out_lines.append(s)
        return f_, out_lines

    def height_of(fs_, lines_):
        lh_ = int(fs_ * LINE_SPACING)
        total_ = 0
        for idx, s in enumerate(lines_):
            total_ += fs_ if idx == len(lines_) - 1 else lh_ + (0 if s else int(fs_ * STANZA_GAP))
        return total_

    # shrink until the block fits the canvas with PAD top and bottom; a long
    # poem (si_meakasi, 11 lines) at the original size overflowed 720px and its
    # last line was cut in half at the bottom edge.
    PAD = 14
    f, lines = wrap(fs)
    total = height_of(fs, lines)
    while total > H - 2 * PAD and fs > 14:
        fs -= 1
        f, lines = wrap(fs)
        total = height_of(fs, lines)
    lh = int(fs * LINE_SPACING)
    top = cy - total // 2
    top = max(PAD, min(H - total - PAD, top))
    im2 = Image.fromarray(out)
    d = ImageDraw.Draw(im2)
    y = top
    for s in lines:
        if s:
            w = f.getlength(s)
            d.text((cx - w / 2, y), s, font=f, fill=tcol)
        y += lh + (int(fs * STANZA_GAP) if not s else 0)
    im2.save(p)
    return fs


def main():
    """Regenerate cards.

    PROJECTS controls which games are written. It defaults to project_k only:
    this port is the Kai (解题篇) release, and rewriting the question-arc
    project overwrote its shipped cards (they are byte-identical to the APK as
    long as they are not touched). Pass extra project names as argv to opt in,
    e.g. `python gen_text_cards.py project project_k`.
    """
    projects = set(sys.argv[1:]) or {"project_k"}
    n = 0
    misses = []
    for key, proj in table_pairs():
        if proj not in projects:
            continue
        zh = EXTRA.get(f"{key}@{proj}", EXTRA.get(key))
        if zh is None:
            misses.append((proj, key, "no translation"))
            continue
        r = render_card(proj, key, zh)
        if r is None:
            misses.append((proj, key, "no png / no blocks"))
        else:
            n += 1
    print(f"cards rendered: {n}  (projects: {', '.join(sorted(projects))})")
    for proj, k, why in misses:
        print("  miss:", proj, k, why)


if __name__ == "__main__":
    main()
