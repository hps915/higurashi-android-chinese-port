# -*- coding: utf-8 -*-
"""验收 a：kai 主菜单 -> 开始游戏 -> 目明篇 -> 不使用 -> 跳过 -> 观察 OP。"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zz_drive import tap, show, sh

print("== step1 开始游戏 ==")
tap(850, 496, 8); show("a1_after_start")
