# -*- coding: utf-8 -*-
"""核心核查：被「实际显示」且图片文件不存在的图像。

方法：
  1) 解析所有 image 定义 -> name -> 资源路径
  2) 找出路径不存在的定义（坏定义）
  3) 遍历所有 show/scene，解析目标图像名（前缀元组匹配），
     若命中的定义是「坏定义」即视为「会显示黑块的场景」
  4) 同时也检查 renpy.loadable 守卫
"""
import io
import os
import re
from collections import defaultdict

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJECTS = [
    ("出题篇", os.path.join(BASE, "work", "project", "game")),
    ("解题篇", os.path.join(BASE, "work", "project_k", "game")),
]
CJK = re.compile(u'[\u4e00-\u9fff]')
IMG_DEF = re.compile(
    r'^\s*image\s+([A-Za-z0-9_]+(?:\s+[A-Za-z0-9_]+)*)\s*=\s*'
    r'(?:[^"\']*?)["\']([^"\']+)["\']', re.M)
RENPY_IMAGE = re.compile(
    r"renpy\.image\(\s*['\"]([^'\"]+)['\"]\s*,\s*(?:[^)]*?)['\"]([^'\"]+)['\"]")
SHOW = re.compile(r'^\s*(?:show|scene)\s+([A-Za-z0-9_]+(?:\s+[A-Za-z0-9_]+)*)')
SKIP_TAGS = {"expression", "screen", "layer", "text", "vtext", "imagemap",
             "solid", "null", "frame", "window", "grid", "vbox", "hbox",
             "fixed", "side", "transform", "aspect", "imagebutton"}
EXT = (".png", ".jpg", ".jpeg", ".webp", ".ogg", ".mp3", ".ogv", ".mp4")


def iter_rpy(gd):
    for root, dirs, files in os.walk(gd):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if f.endswith(".rpy"):
                yield os.path.join(root, f)


def main():
    for label, gd in PROJECTS:
        # 1) 建 image 定义表
        defs = {}   # tuple(name) -> (path, rel, line)
        for p in iter_rpy(gd):
            rel = os.path.relpath(p, gd).replace("\\", "/")
            t = io.open(p, encoding="utf-8", errors="replace").read()
            for m in IMG_DEF.finditer(t):
                nm = tuple(m.group(1).split())
                defs.setdefault(nm, (m.group(2), rel, t[:m.start()].count("\n") + 1))
            for m in RENPY_IMAGE.finditer(t):
                nm = tuple(m.group(1).split())
                defs.setdefault(nm, (m.group(2), rel, t[:m.start()].count("\n") + 1))

        # 2) 坏定义
        bad = {}
        for nm, (path, rel, ln) in defs.items():
            if not path.lower().endswith(EXT):
                continue
            if not os.path.exists(os.path.join(gd, *path.split("/"))):
                bad[nm] = (path, rel, ln)
        print("### %s" % label)
        print("  image 定义 %d，其中指向不存在的文件 %d" % (len(defs), len(bad)))

        # 3) 遍历 show/scene，看命中的是不是坏定义
        shown_bad = []
        guard_cnt = 0
        for p in iter_rpy(gd):
            rel = os.path.relpath(p, gd).replace("\\", "/")
            lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
            for i, line in enumerate(lines):
                m = SHOW.match(line.rstrip())
                if not m:
                    continue
                parts = m.group(1).split()
                if parts[0] in SKIP_TAGS:
                    continue
                hit = None
                for k in range(len(parts), 0, -1):
                    if tuple(parts[:k]) in defs:
                        hit = tuple(parts[:k])
                        break
                if hit is None or hit not in bad:
                    continue
                ctx = "\n".join(lines[max(0, i - 6):i + 1])
                pth = bad[hit][0]
                if "loadable(" in ctx and pth in ctx:
                    guard_cnt += 1
                    continue
                shown_bad.append((rel, i + 1, " ".join(parts), pth))

        print("  会显示缺失图的 show/scene：已守卫 %d，未守卫 %d" % (guard_cnt, len(shown_bad)))
        seen = set()
        for rel, ln, name, pth in shown_bad:
            key = pth
            if key in seen:
                continue
            seen.add(key)
            print("     %s:%d  show「%s」 → %s" % (rel, ln, name, pth))
        print("  受影响的不同图片文件: %d" % len(seen))
        # 列出全部
        print("  全部坏定义:")
        for nm, (path, rel, ln) in sorted(bad.items(), key=lambda kv: kv[1][0]):
            print("     %-40s %s  (%s:%d)" % (" ".join(nm), path, rel, ln))
        print()


if __name__ == "__main__":
    main()
