# -*- coding: utf-8 -*-
"""全量扫描：找出所有「字符串里一个中文字都没有、但有英文字母」的台词行。
不用长度阈值，只要求至少有一个英文单词（>=2 个字母）。

用法: python work/scripts/zz_audit_short.py <game_dir> [--detail]
"""
import io
import os
import re
import sys

CJK = re.compile(u'[\u3000-\u303f\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]')
TAG = re.compile(r'\{[^{}]*\}')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')
WORD = re.compile(r'[A-Za-z]{2,}')
KEYWORDS = {
    "voice", "play", "stop", "queue", "show", "scene", "hide", "jump",
    "call", "label", "image", "with", "pause", "window", "nvl", "menu",
    "if", "elif", "else", "return", "pass", "python", "default", "define",
    "extend", "translate", "old", "new", "style", "text", "textbutton",
    "init", "screen", "use", "for", "while", "include", "options",
    "adv_extend", "nvl_extend",
}
RES_PATH = re.compile(r'^(efe|sound|tips|music|voice|background|characters|cg|movie|text|'
                      r'save|images)/', re.I)


def main():
    game = sys.argv[1]
    detail = '--detail' in sys.argv
    hits = {}
    for root, dirs, files in os.walk(game):
        dirs[:] = [d for d in dirs if d not in ('cache', 'saves', 'tl')]
        for f in sorted(files):
            if not f.endswith('.rpy'):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, game).replace('\\', '/')
            for i, line in enumerate(io.open(p, encoding='utf-8', errors='replace'), 1):
                m = SAY.match(line.rstrip())
                if not m:
                    continue
                ident, body = m.group(2), m.group(3)
                if ident and ident.strip() in KEYWORDS:
                    continue
                if CJK.search(body):
                    continue
                plain = TAG.sub('', body).strip()
                if not plain:
                    continue
                if RES_PATH.match(plain):
                    continue
                if re.search(r'\.(png|jpe?g|webp|ogg|mp3|wav|ogv|mp4|ttf|otf)$', plain, re.I):
                    continue
                if not WORD.search(plain):
                    continue
                hits.setdefault(rel, []).append((i, plain))
    tot = sum(len(v) for v in hits.values())
    for rel in sorted(hits, key=lambda x: -len(hits[x])):
        print("%5d  %s" % (len(hits[rel]), rel))
        if detail:
            for ln, txt in hits[rel]:
                print("        %d: %s" % (ln, txt[:120]))
    print()
    print("TOTAL:", tot)


if __name__ == '__main__':
    main()
