# -*- coding: utf-8 -*-
"""Join multi-physical-line show text strings, inserting the two-character
sequence backslash+n at the join point (Ren'Py newline escape)."""
import os

BS = chr(92)
NL = BS + "n"  # two chars: backslash, n

fixed = 0
for proj in ("project", "project_k"):
    for dp, _, fs in os.walk(os.path.join(proj, "game")):
        for f in fs:
            if not f.endswith(".rpy"):
                continue
            p = os.path.join(dp, f)
            lines = open(p, encoding="utf-8").read().split("\n")
            out = []
            i = 0
            changed = False
            while i < len(lines):
                l = lines[i]
                stripped = l.rstrip()
                # inside an open show text string: odd number of quotes and
                # no line-ending backslash escape
                if (l.lstrip().startswith("show text ") and l.count('"') % 2 == 1
                        and i + 1 < len(lines)):
                    if stripped.endswith(BS) and lines[i + 1].lstrip().startswith("n"):
                        # a \n escape was split across the line break: \ | n...
                        out.append(stripped[:-1] + NL + lines[i + 1].lstrip()[1:])
                    elif stripped.endswith(BS):
                        out.append(stripped[:-1] + lines[i + 1].strip())
                    else:
                        out.append(stripped + NL + lines[i + 1].strip())
                    i += 2
                    changed = True
                    fixed += 1
                    continue
                out.append(l)
                i += 1
            if changed:
                open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("joined:", fixed)

# audit: any show text line still containing a real LF inside the string?
bad = 0
for proj in ("project", "project_k"):
    for dp, _, fs in os.walk(os.path.join(proj, "game")):
        for f in fs:
            if not f.endswith(".rpy"):
                continue
            for l in open(os.path.join(dp, f), encoding="utf-8"):
                if l.lstrip().startswith("show text ") and l.count('"') % 2 == 1:
                    bad += 1
                    print("STILL BROKEN:", l[:80])
                if l.lstrip().startswith("show text ") and (BS + BS + "n") in l:
                    bad += 1
                    print("DOUBLE BS:", l[:80])
print("remaining problems:", bad)
