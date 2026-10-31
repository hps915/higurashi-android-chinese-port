# -*- coding: utf-8 -*-
"""抽查 zz_tsum_align 的替换结果：随机抽 N 条，打印英文原句 + 拟用译文 + corpus 邻域。"""
import difflib
import io
import json
import os
import re
import sys

GAME = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"
CORPUS = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\corpus\ch6.json"
TSUMDIR = os.path.join(GAME, "tsumihoroboshi")

CJK = re.compile(u'[\u3000-\u303f\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]')
SAY_RE = re.compile(r'^(\s*)(?:([A-Za-z_]\w*)\s+)?"((?:[^"\\]|\\.)*)"\s*$')
KEYWORDS = {
    "voice", "play", "stop", "queue", "show", "scene", "hide", "jump",
    "call", "label", "image", "with", "pause", "window", "nvl", "menu",
    "if", "elif", "else", "return", "pass", "python", "default", "define",
    "extend", "translate", "old", "new", "style", "text", "textbutton",
    "init", "screen", "use", "for", "while", "include", "options",
}


def norm(s):
    s = re.sub(r'\{[^{}]*\}', '', s)
    s = s.replace('\\"', '"').replace("\\'", "'")
    s = re.sub(r'[^A-Za-z0-9]+', ' ', s)
    return s.strip().lower()


def is_untranslated(body):
    if CJK.search(body):
        return False
    plain = re.sub(r'\{[^{}]*\}', '', body)
    return len(re.sub(r'[^A-Za-z0-9]', '', plain)) >= 12


def build():
    data = json.load(io.open(CORPUS, encoding='utf-8'))
    corpus = []
    for e in data:
        en, zh = e.get('en'), e.get('zh')
        if not en or not zh or not CJK.search(zh):
            continue
        k = norm(en)
        if len(k) < 4:
            continue
        corpus.append((k, zh.strip(), en.strip(), e.get('jp') or ''))
    rpy = []
    for f in sorted(x for x in os.listdir(TSUMDIR) if x.endswith('.rpy')):
        lines = io.open(os.path.join(TSUMDIR, f), encoding='utf-8').read().split('\n')
        for i, line in enumerate(lines):
            m = SAY_RE.match(line.rstrip())
            if not m:
                continue
            ident, body = m.group(2), m.group(3)
            if ident in KEYWORDS:
                continue
            k = norm(body)
            if len(k) < 4:
                continue
            rpy.append((f, i + 1, ident, body, k))
    return corpus, rpy


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    corpus, rpy = build()
    a = [x[4] for x in rpy]
    b = [x[0] for x in corpus]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    pairs = []
    for bl in sm.get_matching_blocks():
        for k in range(bl.size):
            f, ln, ident, body, _ = rpy[bl.a + k]
            if not is_untranslated(body):
                continue
            zh = corpus[bl.b + k][1]
            jp = corpus[bl.b + k][3]
            pairs.append((f, ln, body, zh, jp))
    print("total pairs:", len(pairs))
    step = max(1, len(pairs) // n)
    for idx in range(0, len(pairs), step):
        f, ln, body, zh, jp = pairs[idx]
        print("=" * 100)
        print("%s:%d" % (f, ln))
        print("  EN :", body[:180])
        print("  JP :", jp[:90])
        print("  ZH :", zh[:180])


if __name__ == '__main__':
    main()
