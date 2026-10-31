# -*- coding: utf-8 -*-
"""统计/定位未翻译的 say 行。

判定：以 `ident "..."` 或 `"..."` 开头的台词行，字符串内**没有任何中日文字符**，
且长度 > 12 个纯拉丁字符（过滤掉「**」「—」「？」等纯符号行）。
输出按文件汇总，并可选输出明细（--detail）。
"""
import io
import os
import re
import sys

CJK = re.compile(u'[\u3000-\u303f\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]')
SAY_RE = re.compile(r'^(\s*)(?:([A-Za-z_]\w*)\s+)?"((?:[^"\\]|\\.)*)"\s*$')
KEYWORDS = {
    "voice", "play", "stop", "queue", "show", "scene", "hide", "jump",
    "call", "label", "image", "with", "pause", "window", "nvl", "menu",
    "if", "elif", "else", "return", "pass", "python", "default", "define",
    "extend", "translate", "old", "new", "style", "text", "textbutton",
    "init", "screen", "use", "for", "while", "include", "options",
}


def scan_file(path):
    out = []
    for i, raw in enumerate(io.open(path, encoding='utf-8', errors='replace'), 1):
        line = raw.rstrip('\n').rstrip()
        m = SAY_RE.match(line)
        if not m:
            continue
        ident, body = m.group(2), m.group(3)
        if ident in KEYWORDS:
            continue
        if CJK.search(body):
            continue
        # strip renpy text tags
        plain = re.sub(r'\{[^{}]*\}', '', body)
        # 排除纯资源路径（idle/hover/add/ground 等属性值）
        if re.search(r'\.(png|jpg|jpeg|webp|ogg|mp3|wav|ogv|mp4|ttf|otf)$', plain.strip(), re.I):
            continue
        if plain.strip().startswith(('efe/', 'sound/', 'tips/', 'music/', 'voice/', 'background/',
                                     'characters/', 'cg/', 'movie/', 'text/')):
            continue
        latin = re.sub(r'[^A-Za-z0-9]', '', plain)
        if len(latin) < 12:
            continue
        out.append((i, line.strip()))
    return out


def main():
    game = sys.argv[1]
    detail = '--detail' in sys.argv
    only = None
    for a in sys.argv[2:]:
        if a.startswith('--dir='):
            only = a[6:]
    files = []
    for root, dirs, fs in os.walk(game):
        dirs[:] = [d for d in dirs if d not in ('cache', 'saves', 'tl')]
        if only:
            parts = os.path.relpath(root, game).replace('\\', '/').split('/')
            if only not in parts:
                continue
        for f in fs:
            if f.endswith('.rpy'):
                files.append(os.path.join(root, f))
    total = 0
    rows = []
    for p in sorted(files):
        hits = scan_file(p)
        if hits:
            rel = os.path.relpath(p, game).replace('\\', '/')
            rows.append((len(hits), rel, hits))
            total += len(hits)
    rows.sort(reverse=True)
    for n, rel, hits in rows:
        print("%5d  %s" % (n, rel))
        if detail:
            for ln, txt in hits:
                print("        %d: %s" % (ln, txt[:150]))
    print()
    print("TOTAL untranslated say lines:", total)


if __name__ == '__main__':
    main()
