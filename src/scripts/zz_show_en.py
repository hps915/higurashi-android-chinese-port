# -*- coding: utf-8 -*-
"""定位出题篇所有 adv_extend / extend / say 行里仍是英文的行，并输出上下文。"""
import io
import os
import re
import sys

GAME = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game"
CJK = re.compile(u'[\u3000-\u303f\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]')
TAG = re.compile(r'\{[^{}]*\}')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+)?"((?:[^"\\]|\\.)*)"\s*$')


def is_en(body):
    if CJK.search(body):
        return False
    plain = TAG.sub('', body)
    return len(re.sub(r'[^A-Za-z0-9]', '', plain)) >= 8


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else 'adv_extend'
    for root, dirs, files in os.walk(GAME):
        dirs[:] = [d for d in dirs if d not in ('cache', 'saves', 'tl')]
        for f in sorted(files):
            if not f.endswith('.rpy'):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, GAME).replace('\\', '/')
            lines = io.open(p, encoding='utf-8', errors='replace').read().split('\n')
            for i, line in enumerate(lines):
                st = line.strip()
                if want == 'adv_extend':
                    if not st.startswith('adv_extend "'):
                        continue
                m = SAY.match(line.rstrip())
                if not m or not is_en(m.group(3)):
                    continue
                print("=" * 90)
                print("%s:%d" % (rel, i + 1))
                for j in range(max(0, i - 4), min(len(lines), i + 3)):
                    mark = '>>' if j == i else '  '
                    print("%s %s" % (mark, lines[j][:170]))


if __name__ == '__main__':
    main()
