# -*- coding: utf-8 -*-
"""Verify applied edits: indent/speaker unchanged, tag sequence identical, quotes balanced."""
import io
import os
import re
import sys

TSUMDIR = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\tsumihoroboshi"
BAK = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\backup_tsum_before_autotrans"

TARGETS = {
    'tsum_005.rpy': [551, 569, 573, 625, 653, 672, 687, 689, 692, 772, 797, 843, 901],
    'tsum_006.rpy': [417, 420, 435, 579, 582, 721, 877, 892, 946, 950, 954, 976],
    'tsum_013.rpy': [767, 769, 798, 809, 815, 818, 1105, 1106, 1144, 1152],
    'tsum_020.rpy': [300, 441, 459, 591, 595, 1129],
    'tsum_008.rpy': [284, 360, 565, 918, 969, 1055],
    'tsum_007.rpy': [994, 1122, 1180, 1251, 1256],
    'tsum_018.rpy': [165, 303, 736, 855],
    'tsum_017.rpy': [1050, 1124, 1242],
    'tsum_019.rpy': [644, 646],
    'tsum_016.rpy': [631, 821],
    'tsum_021.rpy': [940],
    'tsum_012.rpy': [1234],
    'tsum_011.rpy': [1771],
    'tsum_010.rpy': [420],
    'tsum_009.rpy': [69],
    'tsum_003.rpy': [1987],
}

SAY_RE = re.compile(r'^(\s*)(?:([A-Za-z_]\w*)\s+)?"((?:[^"\\]|\\.)*)"\s*$')
TAG_RE = re.compile(r'\{[^{}]*\}')
ESC_QUOTE = re.compile(r'\\"')


def main():
    problems = []
    checked = 0
    for f, ns in TARGETS.items():
        cur = io.open(os.path.join(TSUMDIR, f), encoding='utf-8').read().split('\n')
        old = io.open(os.path.join(BAK, f), encoding='utf-8').read().split('\n')
        for n in ns:
            a = SAY_RE.match(old[n - 1])
            b = SAY_RE.match(cur[n - 1])
            checked += 1
            if not b:
                problems.append('%s:%d NOT a valid say line now: %r' % (f, n, cur[n - 1]))
                continue
            if a is None:
                problems.append('%s:%d old line was not a say line' % (f, n))
                continue
            if a.group(1) != b.group(1) or (a.group(2) or '') != (b.group(2) or ''):
                problems.append('%s:%d indent/speaker changed' % (f, n))
            ta, tb = TAG_RE.findall(a.group(3)), TAG_RE.findall(b.group(3))
            if ta != tb:
                problems.append('%s:%d TAG DIFF\n    old %s\n    new %s' % (f, n, ta, tb))
            body = b.group(3)
            if body.count('{') != body.count('}'):
                problems.append('%s:%d unbalanced braces' % (f, n))
            qa, qb = len(ESC_QUOTE.findall(a.group(3))), len(ESC_QUOTE.findall(body))
            if qa != qb:
                problems.append('%s:%d escaped-quote count %d -> %d' % (f, n, qa, qb))
            if qb % 2:
                problems.append('%s:%d odd number of escaped quotes (%d)' % (f, n, qb))
            if '%' in body:
                problems.append('%s:%d contains a raw %% (Ren' % (f, n))
    print('checked %d lines' % checked)
    print('PROBLEMS: %d' % len(problems))
    for p in problems:
        print('  ' + p)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
