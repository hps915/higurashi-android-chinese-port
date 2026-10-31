# -*- coding: utf-8 -*-
"""用 corpus 的 en/zh 对齐表自动补译罪灭篇未翻译行。

流程：
 1) 读 work/corpus/ch6.json（罪灭篇），建 en -> zh 映射
 2) 扫描 tsumihoroboshi/*.rpy 里未翻译的 say 行
 3) 精确匹配 -> 直接替换；模糊匹配（归一化空白/标点）-> 替换
 4) 输出统计与剩余未匹配清单
默认 dry-run，加 --apply 才写文件。
"""
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
    s = s.replace(u'\\"', u'"').replace(u"\\'", u"'")
    s = re.sub(r'[^A-Za-z0-9]+', ' ', s)
    return s.strip().lower()


def is_untranslated(body):
    if CJK.search(body):
        return False
    plain = re.sub(r'\{[^{}]*\}', '', body)
    latin = re.sub(r'[^A-Za-z0-9]', '', plain)
    return len(latin) >= 12


def load_map():
    data = json.load(io.open(CORPUS, encoding='utf-8'))
    exact = {}
    fuzzy = {}
    for e in data:
        en, zh = e.get('en'), e.get('zh')
        if not en or not zh:
            continue
        if not CJK.search(zh):
            continue
        exact.setdefault(en.strip(), zh.strip())
        k = norm(en)
        if k:
            fuzzy.setdefault(k, zh.strip())
    return exact, fuzzy


def main():
    apply = '--apply' in sys.argv
    exact, fuzzy = load_map()
    print("corpus exact=%d fuzzy=%d" % (len(exact), len(fuzzy)))

    tot = hit_e = hit_f = miss = 0
    miss_lines = []
    files_done = 0
    for f in sorted(os.listdir(TSUMDIR)):
        if not f.endswith('.rpy'):
            continue
        p = os.path.join(TSUMDIR, f)
        lines = io.open(p, encoding='utf-8').read().split('\n')
        changed = 0
        for i, line in enumerate(lines):
            m = SAY_RE.match(line.rstrip())
            if not m:
                continue
            ident, body = m.group(2), m.group(3)
            if ident in KEYWORDS:
                continue
            if not is_untranslated(body):
                continue
            tot += 1
            zh = exact.get(body.strip())
            if zh:
                hit_e += 1
            else:
                zh = fuzzy.get(norm(body))
                if zh:
                    hit_f += 1
            if not zh:
                miss += 1
                miss_lines.append("%s:%d  %s" % (f, i + 1, body[:120]))
                continue
            prefix = m.group(1) + ((ident + ' ') if ident else '')
            # 保留原有文本标签（如 {nw}）在末尾
            tags = re.findall(r'\{[^{}]*\}', body)
            suffix = ''.join(t for t in tags if t in ('{nw}',))
            new_body = zh.replace('"', u'\\"')
            lines[i] = u'%s"%s"%s' % (prefix, new_body, suffix)
            changed += 1
        if changed:
            files_done += 1
            if apply:
                io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))

    print("untranslated total:", tot)
    print("  exact hit:", hit_e)
    print("  fuzzy hit:", hit_f)
    print("  miss:", miss)
    print("files changed:", files_done, "(apply=%s)" % apply)
    if miss_lines:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zz_tsum_miss.txt')
        io.open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(miss_lines) + '\n')
        print("miss list ->", out)


if __name__ == '__main__':
    main()
