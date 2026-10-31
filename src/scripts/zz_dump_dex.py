# -*- coding: utf-8 -*-
# 只读分析：打印 classes.dex 里 activity 生命周期相关方法的字节码
import sys

from androguard.core.dex import DEX

path = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\apk_q\classes.dex"
d = DEX(open(path, "rb").read())

wanted = {
    "Lorg/renpy/android/PythonSDLActivity;",
    "Lorg/renpy/android/PythonSDLActivity$2;",
    "Lorg/libsdl/app/SDLActivity;",
}

for c in d.get_classes():
    cn = c.get_name()
    if cn not in wanted:
        continue
    print("=" * 70)
    print(cn, "extends", c.get_superclassname())
    for m in c.get_methods():
        name = m.get_name()
        if name not in (
            "<init>", "run", "onCreate", "onDestroy", "onPause", "onResume",
            "onStart", "onStop", "onWindowFocusChanged", "preparePython",
            "nativeInit", "nativeQuit", "nativeSetEnv", "getLibraries",
            "startPython", "setWakeLock", "onSaveInstanceState",
        ):
            continue
        print("-" * 60)
        print("  METHOD", name, m.get_descriptor())
        code = m.get_code()
        if code is None:
            print("    <no code>")
            continue
        for ins in code.get_bc().get_instructions():
            print("    ", ins.get_name(), ins.get_output())
