# -*- coding: utf-8 -*-
"""Generate zz_fix.rpy defining missing images for a port project.

Resolution chain per missing name:
  1. colour-variant suffix -> port's own matrix on the base file
  2. exact file in project dirs -> direct def
  3. sibling file (stem_01 / same-prefix closest number) in project dirs
  4. user's PC game data (07th-mod CG set) -> copy + downscale to 1280x720
  5. fallback: solid black (removes the red error text)
"""
import os
import re
import sys

GAME_ROOT = r"D:\Galgame\寒蝉鸣泣之时"
USER_DIRS = []  # filled in main
VARIANTS = {
    "dark": 'im.matrix.tint(0.6, 0.6, 0.6)',
    "sunset": 'im.matrix.tint(1, 0.924, 0.759)',
    "night": 'im.matrix.tint(0.77, 0.77, 1)',
    "night1": 'im.matrix.tint(0.77, 0.77, 1)',
    "gray": 'im.matrix.desaturate() * im.matrix.tint(0.5, 0.5, 0.5)',
    "red": 'im.matrix.desaturate() * im.matrix.tint(1.0, 0.125, 0.125)',
    "red1": 'im.matrix.desaturate() * im.matrix.tint(1.0, 0.6875, 0.6875)',
    "red2": 'im.matrix.desaturate() * im.matrix.tint(1.0, 0.5, 0.5)',
    "sepia": 'im.matrix.desaturate() * im.matrix.tint(0.71, 0.64, 0.64)',
    "rain": 'im.matrix.tint(0.66, 0.72, 0.84)',
    "dusk": 'im.matrix.tint(1, 0.924, 0.759)',
    "night_rain": 'im.matrix.tint(0.66, 0.72, 0.84) * im.matrix.tint(0.77, 0.77, 1)',
    "inverse": 'im.matrix.invert()',
}
VARIANT_RE = re.compile(r"^(.*)\s+(" + "|".join(VARIANTS) + r")$")

pat_def = re.compile(r'^\s*image\s+([#\w][^\s=]*(?:\s+[^\s=]+)*?)\s*=\s*(.+)$', re.M)
pat_scene = re.compile(r"^\s*scene\s+(?!expression\b)(?!black\b)(?!white\b)([a-z_][\w]*(?:\s+[\w]+)*?)(?:\s+(?:with|at|as|behind|onlayer|zorder)\b.*|\s*$)", re.M)
pat_show = re.compile(r"^\s*show\s+(?!expression\b)([a-z_][\w]*(?:\s+[\w]+)*?)(?:\s+(?:with|at|as|behind|onlayer|zorder)\b.*|\s*$)", re.M)
pat_call = re.compile(r'(scene_difference\w*)\s*\(\s*[\"\']([^"\']+)[\"\']')


def index_files(root):
    """map: relative path -> abs path; and basename(without ext) -> rel path list"""
    rels = {}
    by_base = {}
    for dp, dirs, files in os.walk(root):
        for f in files:
            rel = os.path.relpath(os.path.join(dp, f), root).replace("\\", "/")
            rels[rel] = os.path.join(root, rel)
            by_base.setdefault(os.path.splitext(f)[0], []).append(rel)
    return rels, by_base


def main():
    root = os.path.abspath(sys.argv[1])
    out = sys.argv[2]
    rels, by_base = index_files(root)

    # user PC data index (all chapters, CG/CGAlt subdirs)
    user_files = {}
    for d in sorted(os.listdir(GAME_ROOT)):
        full = os.path.join(GAME_ROOT, d)
        if not os.path.isdir(full) or "：" not in d:
            continue
        mch = re.search(r"：(\d)", d)
        if not mch:
            continue
        for sub in ("CG", "CGAlt"):
            sdir = os.path.join(full, f"HigurashiEp0{mch.group(1)}_Data",
                                "StreamingAssets", sub)
            if os.path.isdir(sdir):
                for dp, dirs, files in os.walk(sdir):
                    for f in files:
                        user_files.setdefault(os.path.splitext(f)[0],
                                               os.path.join(dp, f))

    defs = {}
    refs = {}
    for dp, dirs, files in os.walk(root):
        for f in files:
            if not f.endswith(".rpy"):
                continue
            p = os.path.join(dp, f)
            txt = open(p, encoding="utf-8", errors="replace").read()
            for m in pat_def.finditer(txt):
                defs[m.group(1).strip()] = m.group(2).strip()
            for m in pat_scene.finditer(txt):
                refs.setdefault(m.group(1).strip(), set()).add(p)
            for m in pat_show.finditer(txt):
                refs.setdefault(m.group(1).strip(), set()).add(p)
            for m in pat_call.finditer(txt):
                refs.setdefault(m.group(2).strip(), set()).add(p)

    def file_of_def(name, depth=0):
        if depth > 6:
            return None
        d = defs.get(name)
        if d is None:
            rel = name.replace(" ", "/")
            for ext in (".png", ".jpg", ".webp"):
                if rel + ext in rels:
                    return rel + ext
            return None
        m = re.search(r'"([^"]+\.(?:png|jpg|webp))"', d)
        if m:
            return m.group(1)
        words = d.strip().strip('"')
        if re.match(r"^[\w ]+$", words):
            return file_of_def(words, depth + 1)
        return None

    def sibling(stem):
        """closest sibling among indexed basenames (exact / _01 / strip _NN / family)"""
        # 1. exact
        if stem in by_base:
            return by_base[stem][0]
        # 2. add _01
        if stem + "_01" in by_base:
            return by_base[stem + "_01"][0]
        # 3. strip trailing _NN
        core = re.sub(r"_[0-9]+$", "", stem)
        if core != stem and core in by_base:
            return by_base[core][0]
        if core + "_01" in by_base:
            return by_base[core + "_01"][0]
        # 4. number family on the core
        m = re.match(r"^(.*?)(\d+)$", core)
        if m:
            prefix, num = m.group(1), int(m.group(2))
            cands = []
            for base in by_base:
                mm = re.match(r"^(.*?)(\d+)(?:_[0-9]+)?$", base)
                if mm and mm.group(1) == prefix:
                    cands.append((abs(int(mm.group(2)) - num), len(base), base))
            if cands:
                dist, _, best = sorted(cands)[0]
                return by_base[best][0]
        # 5. prefix containment
        for base in sorted(by_base):
            if base.startswith(stem) or stem.startswith(base):
                return by_base[base][0]
        return None

    from PIL import Image
    copied = []

    def copy_from_user(stem):
        for probe in (stem, re.sub(r"_[0-9]+$", "", stem), stem + "_01"):
            src = user_files.get(probe)
            if src:
                break
        else:
            return None
        # target: background/ for bg-*, characters/ otherwise by source dir name
        sdir = os.path.basename(os.path.dirname(src))
        tdir = {"background": "background", "sprite": "characters",
                "portrait": "characters"}.get(sdir, "cg")
        os.makedirs(os.path.join(root, tdir), exist_ok=True)
        rel = tdir + "/" + stem + ".png"
        dst = os.path.join(root, rel)
        if not os.path.exists(dst):
            im = Image.open(src)
            if im.size != (1280, 720) and im.size[0] > 1280:
                im = im.resize((1280, 720), Image.LANCZOS)
            im.save(dst)
            copied.append(rel)
        return rel

    fixes = {}
    unresolved = []
    for ref in sorted(refs):
        name = ref
        if name.startswith("expression") or name == "None":
            continue
        if name.startswith("gb "):
            name = "bg " + name[3:]
        if name in defs:
            continue
        first = name.split(" ")[0]
        if first in defs and not name.startswith(("bg ", "gb ", "sepia_bg ", "inverse_bg ")):
            continue
        vm = VARIANT_RE.match(name)
        base, variant = (vm.group(1), vm.group(2)) if vm else (name, None)
        # 1. base defined
        bf = file_of_def(base)
        if bf and variant:
            fixes[name] = f'im.MatrixColor("{bf}", {VARIANTS[variant]})'
            continue
        if bf and not variant:
            continue
        # 2/3. exact or sibling file for whole name or base
        stem_flat = base.replace(" ", "_").replace("bg_", "", 1) if base.startswith("bg ") else base.replace(" ", "_")
        for probe in (base.replace(" ", "/"), stem_flat):
            for ext in (".png", ".jpg", ".webp"):
                if probe + ext in rels:
                    expr = f'"{probe + ext}"'
                    if variant:
                        expr = f'im.MatrixColor("{probe + ext}", {VARIANTS[variant]})'
                    elif name.startswith("sepia_bg "):
                        expr = f'im.MatrixColor("{probe + ext}", {VARIANTS["sepia"]})'
                    elif name.startswith("inverse_bg "):
                        expr = f'im.MatrixColor("{probe + ext}", im.matrix.invert())'
                    fixes[name] = expr
                    break
            if name in fixes:
                break
        if name in fixes:
            continue
        # sibling within project
        sib = sibling(stem_flat)
        if sib:
            expr = f'"{sib}"'
            if variant:
                expr = f'im.MatrixColor("{sib}", {VARIANTS[variant]})'
            elif name.startswith("sepia_bg "):
                expr = f'im.MatrixColor("{sib}", {VARIANTS["sepia"]})'
            elif name.startswith("inverse_bg "):
                expr = f'im.MatrixColor("{sib}", im.matrix.invert())'
            fixes[name] = expr
            continue
        # 4. user data
        uf = copy_from_user(stem_flat) or copy_from_user(base.replace(" ", "_"))
        if uf:
            expr = f'"{uf}"'
            if variant:
                expr = f'im.MatrixColor("{uf}", {VARIANTS[variant]})'
            fixes[name] = expr
            continue
        # 4.5 sprite attr remap: 'fam N attr' -> closest defined 'fam N attr2'
        msp = re.match(r"^(\S+)\s+(\S+)\s+(.+)$", name)
        if msp and not name.startswith(("bg ", "sepia_bg ", "inverse_bg ")):
            fam, num, attr = msp.groups()
            pat_attr = re.compile(r"^" + re.escape(fam) + r"\s+" + re.escape(num) + r"\s+(.+)$")
            best = None
            for dn in defs:
                mm = pat_attr.match(dn)
                if mm:
                    common = 0
                    for a, b in zip(mm.group(1), attr):
                        if a != b:
                            break
                        common += 1
                    if best is None or common > best[0]:
                        best = (common, dn)
            if best:
                bf = file_of_def(best[1])
                if bf:
                    expr = f'"{bf}"'
                    if variant:
                        expr = f'im.MatrixColor("{bf}", {VARIANTS[variant]})'
                    fixes[name] = expr
                    continue
        # 5. black fallback
        unresolved.append(name)
        fixes[name] = 'Solid("#000")'

    lines = ["# -*- coding: utf-8 -*-",
             "# 缺失图像补全（自动生成：变体矩阵/同族映射/用户素材/黑块兜底）",
             "init 20 python:"]
    for name, expr in sorted(fixes.items()):
        lines.append(f'    renpy.image({name!r}, {expr})')
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"zz_fix: {len(fixes)} definitions ({len(copied)} user files copied) -> {out}")
    print(f"black-fallback (no source found): {len(unresolved)}")
    for n in unresolved:
        print("  ", n)


if __name__ == "__main__":
    main()
