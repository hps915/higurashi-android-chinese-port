# -*- coding: utf-8 -*-
"""Scan every .rpy in tsumihoroboshi for lines with an odd number of unescaped quotes."""
import glob
import io
import os
import re

TSUMDIR = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\tsumihoroboshi"
ESCAPE_RE = re.compile(r'\\.')


def main():
    bad = []
    total = 0
    for p in sorted(glob.glob(os.path.join(TSUMDIR, '*.rpy'))):
        for i, raw in enumerate(io.open(p, encoding='utf-8'), 1):
            s = raw.rstrip('\n')
            stripped = s.strip()
            if not stripped or stripped.startswith('#'):
                continue
            total += 1
            # remove escaped chars, then count quotes
            q = ESCAPE_RE.sub('', s).count('"')
            if q % 2 == 1:
                bad.append('%s:%d  %s' % (os.path.basename(p), i, stripped[:130]))
    print('non-comment lines scanned:', total)
    print('odd-quote lines:', len(bad))
    for b in bad:
        print('  ' + b)
    return 0


if __name__ == '__main__':
    main()
