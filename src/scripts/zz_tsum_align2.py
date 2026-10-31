# -*- coding: utf-8 -*-
"""罪灭篇补译（第二遍）：处理带内联计时/样式标签的行。

第一遍（zz_tsum_align.py）已补 2490 行。剩余行的问题在于原文里夹了
{w=0.8} / {cps=*0.4} / {i} 这类标签，序列对齐时归一化后 token 顺序
与 corpus 的 en 不一致，导致匹配不上。

策略：
 1) 归一化时把 {w=...} {cps=...} {/cps} {nw} 全部剥掉，{i}{/i} 也剥掉；
 2) 再做一次 SequenceMatcher 对齐（以文件为单位，避免跨文件错配）；
 3) 写回时只输出纯中文，不再加内联计时标签（{nw} 保留在末尾）。
"""
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
TAG_RE = re.compile(r'\{[^{}]*\}')
KEYWORDS = {
    "voice", "play", "stop", "queue", "show", "scene", "hide", "jump",
    "call", "label", "image", "with", "pause", "window", "nvl", "menu",
    "if", "elif", "else", "return", "pass", "python", "default", "define",
    "extend", "translate", "old", "new", "style", "text", "textbutton",
    "init", "screen", "use", "for", "while", "include", "options",
}


def norm(s):
    s = TAG_RE.sub('', s)
    # corpus 里的斜体是 HTML <i>/<b>，rpy 里是 Ren'Py {i}/{b}，统一剥掉
    s = re.sub(r'<[^<>]*>', '', s)
    s = s.replace('\\"', '"').replace("\\'", "'")
    s = re.sub(r'[^A-Za-z0-9]+', ' ', s)
    return s.strip().lower()


def is_untranslated(body):
    if CJK.search(body):
        return False
    plain = TAG_RE.sub('', body)
    return len(re.sub(r'[^A-Za-z0-9]', '', plain)) >= 10


def load_corpus():
    data = json.load(io.open(CORPUS, encoding='utf-8'))
    seq = []
    for e in data:
        en, zh = e.get('en'), e.get('zh')
        if not en or not zh or not CJK.search(zh):
            continue
        k = norm(en)
        if len(k) < 4:
            continue
        seq.append((k, zh.strip()))
    return seq


def main():
    apply = '--apply' in sys.argv
    corpus = load_corpus()
    ck = [c[0] for c in corpus]

    total_fixed = 0
    report = []
    for f in sorted(x for x in os.listdir(TSUMDIR) if x.endswith('.rpy')):
        p = os.path.join(TSUMDIR, f)
        lines = io.open(p, encoding='utf-8').read().split('\n')
        idxs = []
        keys = []
        for i, line in enumerate(lines):
            m = SAY_RE.match(line.rstrip())
            if not m:
                continue
            ident, body = m.group(2), m.group(3)
            if ident in KEYWORDS:
                continue
            if not is_untranslated(body):
                continue
            k = norm(body)
            if len(k) < 4:
                continue
            idxs.append((i, ident, body))
            keys.append(k)
        if not keys:
            continue
        sm = difflib.SequenceMatcher(None, keys, ck, autojunk=False)
        fixed = 0
        for bl in sm.get_matching_blocks():
            if bl.size < 1:
                continue
            for k in range(bl.size):
                li, ident, body = idxs[bl.a + k]
                zh = corpus[bl.b + k][1]
                m = SAY_RE.match(lines[li].rstrip())
                tags = ''
                for t in TAG_RE.findall(body):
                    if t == '{nw}':
                        tags = t
                prefix = m.group(1) + ((ident + ' ') if ident else '')
                lines[li] = u'%s"%s"%s' % (prefix, zh.replace('"', '\\"'), tags)
                fixed += 1
        if fixed:
            total_fixed += fixed
            report.append((f, fixed))
            if apply:
                io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))

    print("fixed this pass:", total_fixed, "(apply=%s)" % apply)
    for f, n in report:
        print("   %-24s %d" % (f, n))


if __name__ == '__main__':
    main()
