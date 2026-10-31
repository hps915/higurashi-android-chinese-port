# -*- coding: utf-8 -*-
"""Post-edit QA: dump the 69 new lines and flag non-fullwidth punctuation or leftover English."""
import io
import os
import re
import sys

TSUMDIR = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\tsumihoroboshi"

TARGETS = {
    'tsum_003.rpy': [1987],
    'tsum_005.rpy': [551, 569, 573, 625, 653, 672, 687, 689, 692, 772, 797, 843, 901],
    'tsum_006.rpy': [417, 420, 435, 579, 582, 721, 877, 892, 946, 950, 954, 976],
    'tsum_007.rpy': [994, 1122, 1180, 1251, 1256],
    'tsum_008.rpy': [284, 360, 565, 918, 969, 1055],
    'tsum_009.rpy': [69],
    'tsum_010.rpy': [420],
    'tsum_011.rpy': [1771],
    'tsum_012.rpy': [1234],
    'tsum_013.rpy': [767, 769, 798, 809, 815, 818, 1105, 1106, 1144, 1152],
    'tsum_016.rpy': [631, 821],
    'tsum_017.rpy': [1050, 1124, 1242],
    'tsum_018.rpy': [165, 303, 736, 855],
    'tsum_019.rpy': [644, 646],
    'tsum_020.rpy': [300, 441, 459, 591, 595, 1129],
    'tsum_021.rpy': [940],
}

SAY_RE = re.compile(r'^(\s*)(?:([A-Za-z_]\w*)\s+)?"((?:[^"\\]|\\.)*)"\s*$')
CJK = re.compile(u'[\u3000-\u303f\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]')

# characters that should NOT appear in the translated text (outside tags/escapes)
BAD = {',': '半角逗号', '.': '半角句点', '?': '半角问号', '!': '半角感叹号',
       ':': '半角冒号', ';': '半角分号', '(': '半角括号', ')': '半角括号'}


def main():
    issues = []
    rows = []
    for f in sorted(TARGETS):
        lines = io.open(os.path.join(TSUMDIR, f), encoding='utf-8').read().split('\n')
        for n in TARGETS[f]:
            m = SAY_RE.match(lines[n - 1])
            if not m:
                issues.append('%s:%d unparseable' % (f, n))
                continue
            body = m.group(3)
            plain = re.sub(r'\{[^{}]*\}', '', body).replace('\\"', '')
            rows.append('%s:%d  %s' % (f, n, lines[n - 1].strip()))
            if not CJK.search(plain):
                issues.append('%s:%d no CJK' % (f, n))
            for ch, name in BAD.items():
                if ch in plain:
                    issues.append('%s:%d %s %r in %r' % (f, n, name, ch, plain))
            latin = re.sub(r'[^A-Za-z]', '', plain)
            if latin:
                issues.append('%s:%d leftover latin %r in %r' % (f, n, latin, plain))
            if '“' in plain or '”' in plain:
                issues.append('%s:%d curly quotes inside narration %r' % (f, n, plain))
    out = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zz_final_lines.txt'),
                  'w', encoding='utf-8')
    out.write('\n'.join(rows) + '\n')
    out.close()
    print('lines: %d' % len(rows))
    print('ISSUES: %d' % len(issues))
    for i in issues:
        print('  ' + i)
    return 0


if __name__ == '__main__':
    sys.exit(main())
