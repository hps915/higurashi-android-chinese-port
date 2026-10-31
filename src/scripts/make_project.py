# -*- coding: utf-8 -*-
"""Build a Ren'Py compile project from the extracted APK game dir.

assets/x-game/x-foo/x-bar.png  →  project/game/foo/bar.png
Rule (verified against the APK): every path component carries an 'x-' prefix.
.rpyc files are skipped (we ship .rpy sources; the SDK compiles them).
"""
import os
import shutil
import sys

SRC = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\apk_q\assets\x-game"
DST = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game"


def unx(name):
    return name[2:] if name.startswith("x-") else name


def main():
    if os.path.exists(DST):
        shutil.rmtree(DST)
    os.makedirs(DST)
    n_files = 0
    for root, dirs, files in os.walk(SRC):
        rel = os.path.relpath(root, SRC)
        parts = [unx(p) for p in rel.split(os.sep)] if rel != "." else []
        out_dir = os.path.join(DST, *parts)
        os.makedirs(out_dir, exist_ok=True)
        for f in files:
            if f.endswith(".rpyc"):
                continue
            src = os.path.join(root, f)
            dst = os.path.join(out_dir, unx(f))
            shutil.copy2(src, dst)
            n_files += 1
    print(f"copied {n_files} files -> {DST}")


if __name__ == "__main__":
    main()
