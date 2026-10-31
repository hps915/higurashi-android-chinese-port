# -*- coding: utf-8 -*-
"""罪灭篇补译：用 difflib 把 rpy 里的英文台词序列与 corpus 的 en 序列做全局对齐，
再取匹配块的 zh 回填。

corpus 的 en 列与 jp/zh 列存在局部错位（英文 PC 脚本折行不同），
所以不能用 en->zh 字典，必须做序列对齐。

用法：
  python zz_tsum_align.py            # dry-run，只报统计
  python zz_tsum_align.py --apply    # 写文件
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


def latin_len(s):
    return len(re.sub(r'[^A-Za-z0-9]', '', re.sub(r'\{[^{}]*\}', '', s)))


def is_untranslated(body):
    return not CJK.search(body) and latin_len(body) >= 12


def load_corpus():
    data = json.load(io.open(CORPUS, encoding='utf-8'))
    # 保持文件顺序 + line 顺序
    order = []
    seen = {}
    for e in data:
        f = e.get('file') or ''
        order.append(f)
    # 语料已是按文件+行的顺序（提取时就按顺序写的），直接用原序
    seq = []
    for e in data:
        en = e.get('en')
        zh = e.get('zh')
        if not en or not zh:
            continue
        if not CJK.search(zh):
            continue
        k = norm(en)
        if len(k) < 4:
            continue
        seq.append((k, zh.strip(), en.strip()))
    return seq


def main():
    apply = '--apply' in sys.argv
    corpus = load_corpus()
    print("corpus seq:", len(corpus))

    # rpy 序列
    files = sorted(f for f in os.listdir(TSUMDIR) if f.endswith('.rpy'))
    rpy_seq = []      # (file, lineno, line_index, ident, body, rawline)
    file_lines = {}
    for f in files:
        p = os.path.join(TSUMDIR, f)
        lines = io.open(p, encoding='utf-8').read().split('\n')
        file_lines[f] = lines
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
            rpy_seq.append((f, i, ident, body, k))

    print("rpy seq:", len(rpy_seq))

    a = [x[4] for x in rpy_seq]
    b = [x[0] for x in corpus]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    blocks = [bl for bl in sm.get_matching_blocks() if bl.size > 0]
    matched = sum(bl.size for bl in blocks)
    print("matching blocks: %d, matched items: %d (%.1f%%)"
          % (len(blocks), matched, 100.0 * matched / max(1, len(a))))

    # 收集替换
    repl = {}   # (file, lineidx) -> zh
    conflicts = 0
    for bl in blocks:
        for k in range(bl.size):
            f, li, ident, body, _ = rpy_seq[bl.a + k]
            zh = corpus[bl.b + k][1]
            if not is_untranslated(body):
                continue
            if (f, li) in repl and repl[(f, li)] != zh:
                conflicts += 1
                continue
            repl[(f, li)] = zh

    per_file = {}
    for (f, li), zh in repl.items():
        per_file[f] = per_file.get(f, 0) + 1
    print("replacements:", len(repl), " conflicts:", conflicts)
    for f in sorted(per_file, key=lambda x: -per_file[x]):
        print("   %-20s %d" % (f, per_file[f]))

    # 仍未译的
    left = {}
    for f, li, ident, body, _ in rpy_seq:
        if is_untranslated(body) and (f, li) not in repl:
            left[f] = left.get(f, 0) + 1
    print()
    print("remaining untranslated:", sum(left.values()))
    for f in sorted(left, key=lambda x: -left[x]):
        print("   %-20s %d" % (f, left[f]))

    if not apply:
        print("\n(dry-run; add --apply to write)")
        return

    # 写文件
    for f, li in sorted(repl):
        lines = file_lines[f]
        m = SAY_RE.match(lines[li].rstrip())
        ident, body = m.group(2), m.group(3)
        zh = repl[(f, li)]
        tags = ''
        for t in re.findall(r'\{[^{}]*\}', body):
            if t in ('{nw}',):
                tags = t
        prefix = m.group(1) + ((ident + ' ') if ident else '')
        lines[li] = u'%s"%s"%s' % (prefix, zh.replace('"', '\\"'), tags)
    for f, lines in file_lines.items():
        io.open(os.path.join(TSUMDIR, f), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print("\nwritten.")


if __name__ == '__main__':
    main()
