# -*- coding: utf-8 -*-
"""Ren'Py 7.3 的旧式 % 替换 (config.old_substitutions=True) 会对 say 台词做
`s % dict`——中文注入丢掉了原版脚本的 %% 转义（或新引入了 %），导致
ValueError: unsupported format character '…' 直接崩溃（tsum_001.rpy:663 等）。

本脚本对两个项目所有 say 型台词字符串做幂等修复：把裸 `%` 规范成 `%%`。
- 只处理 `说话人 "…"` / `extend "…"` / `centered "…"` 形态的行；
- 不碰 voice/play/scene/show 等语句行（show text 不做 % 替换，转义反而会显示 %%）；
- 已存在的 `%%` 保持不变（按连续 % 段处理：n 个 % → 2*ceil(n/2) 个，天然幂等）；
- 特例：hima_003_04.rpy 的注入残留前导 % 直接删除（原英文无 %）。
"""
import os
import re

WORK = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work"
PROJECTS = ("project", "project_k")

KEYWORDS = {"voice", "play", "stop", "queue", "show", "scene", "hide", "jump",
            "call", "label", "image", "with", "pause", "window", "nvl",
            "menu", "if", "return", "pass", "python", "default", "define"}

STRIP_PREFIX = re.compile(r'^\s*([A-Za-z_]\w*)\s+"')
STR_RE = re.compile(r'^(\s*[A-Za-z_]\w*\s+")(.*?)("\s*)$')


def norm_percents(body):
    """连续 n 个 % → 2*ceil(n/2) 个：1→2（转义）、2→2（已转义）、3→4。幂等。"""
    if "%" not in body:
        return body, False
    out = re.sub(r'%+', lambda m: '%' * (2 * ((len(m.group(0)) + 1) // 2)), body)
    return out, out != body


def fix_line(line):
    m = STRIP_PREFIX.match(line)
    if not m or m.group(1) in KEYWORDS:
        return line, False
    sm = STR_RE.match(line)
    if not sm:
        return line, False
    new_body, ch = norm_percents(sm.group(2))
    if not ch:
        return line, False
    return sm.group(1) + new_body + sm.group(3), True


def main():
    total = 0
    for proj in PROJECTS:
        root = os.path.join(WORK, proj, "game")
        for dp, _dn, fs in os.walk(root):
            for f in fs:
                if not f.endswith(".rpy"):
                    continue
                p = os.path.join(dp, f)
                lines = open(p, encoding="utf-8").read().split("\n")
                changed = False
                for i, l in enumerate(lines):
                    nl, ch = fix_line(l)
                    if ch:
                        lines[i] = nl
                        changed = True
                        total += 1
                if changed:
                    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    # 特例：hima_003_04.rpy 的注入残留前导 %（原英文无 %，转义会显示字面 %）
    p = os.path.join(WORK, "project", "game", "himatsubushi", "hima_003_04.rpy")
    if os.path.exists(p):
        lines = open(p, encoding="utf-8").read().split("\n")
        for i, l in enumerate(lines):
            if re.match(r'^\s*n "%+随着', l):
                lines[i] = re.sub(r'^(\s*n ")+(%+)', r'\1', l)
                open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
                total += 1
                print("special: hima_003_04 stray leading % removed")
                break
    print(f"percent-escape: {total} lines fixed")


if __name__ == "__main__":
    main()
