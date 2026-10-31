# -*- coding: utf-8 -*-
"""短英文行补译：把长度 <12 的英文台词也纳入语料对齐。

复用 zz_tsum_align 的逻辑，但阈值降到 2 个字母，且按文件分组对齐。
用法: python work/scripts/zz_short_align.py <chapter_dir> <corpus>
"""
import difflib
import io
import json
import os
import re
import sys

GAME = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"

CJK = re.compile(u'[\u3000-\u303f\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')
TAG = re.compile(r'\{[^{}]*\}')
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


def norm(s):
    s = TAG.sub('', s)
    s = re.sub(r'<[^<>]*>', '', s)
    s = s.replace('\\"', '"').replace("\\'", "'")
    s = re.sub(r'[^A-Za-z0-9]+', ' ', s)
    return s.strip().lower()


def untranslated(body):
    if CJK.search(body):
        return False
    plain = TAG.sub('', body).strip()
    if not plain or RES_PATH.match(plain):
        return False
    if re.search(r'\.(png|jpe?g|webp|ogg|mp3|wav|ogv|mp4|ttf|otf)$', plain, re.I):
        return False
    return bool(WORD.search(plain))


def load_corpus(path):
    data = json.load(io.open(path, encoding='utf-8'))
    seq = []
    for e in data:
        en, zh = e.get('en'), e.get('zh')
        if not en or not zh or not CJK.search(zh):
            continue
        k = norm(en)
        if len(k) < 1:
            continue
        seq.append((k, zh.strip()))
    return seq


def main():
    chapter = sys.argv[1]
    corpus_path = sys.argv[2]
    apply = '--apply' in sys.argv
    d = os.path.join(GAME, chapter)
    corpus = load_corpus(corpus_path)
    ck = [c[0] for c in corpus]
    print("corpus:", len(ck), "chapter:", chapter)

    total = 0
    for f in sorted(x for x in os.listdir(d) if x.endswith('.rpy')):
        p = os.path.join(d, f)
        lines = io.open(p, encoding='utf-8').read().split('\n')
        items = []
        for i, line in enumerate(lines):
            m = SAY.match(line.rstrip())
            if not m:
                continue
            ident, body = m.group(2), m.group(3)
            if ident and ident.strip() in KEYWORDS:
                continue
            if not untranslated(body):
                continue
            k = norm(body)
            if not k:
                continue
            items.append((i, ident, body, k))
        if not items:
            continue
        keys = [x[3] for x in items]
        sm = difflib.SequenceMatcher(None, keys, ck, autojunk=False)
        hit = 0
        for bl in sm.get_matching_blocks():
            if bl.size < 1:
                continue
            for k in range(bl.size):
                idx, ident, body, _ = items[bl.a + k]
                zh = corpus[bl.b + k][1]
                m = SAY.match(lines[idx].rstrip())
                tags = ''
                for t in TAG.findall(body):
                    if t == '{nw}':
                        tags = t
                prefix = m.group(1) + ((ident + ' ') if ident else '')
                lines[idx] = u'%s"%s"%s' % (prefix, zh.replace('"', '\\"'), tags)
                hit += 1
        if hit:
            total += hit
            print("   %-24s %d" % (f, hit))
            if apply:
                io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print("fixed:", total, "(apply=%s)" % apply)


if __name__ == '__main__':
    main()
