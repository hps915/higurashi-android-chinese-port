# -*- coding: utf-8 -*-
"""第 8 轮：补 tsum_badend1 / tsum_badend2 兜底标签。

这两处 call 位于 `persistent.console_choices`（调试用，正常游玩恒为 False）
的分支里，原移植版就缺标签。为了消除“跳转到不存在的标签 → 安卓上直接杀进程”
的隐患，这里补两个安全的坏结局标签：播一段简短旁白后返回主菜单。
内容按罪灭篇的坏结局基调撰写，不会与正常流程冲突（正常流程永远进不来）。
"""
import io

OUT = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\tsumihoroboshi\tsum_badend.rpy"

BODY = u'''# -*- coding: utf-8 -*-
# 第 8 轮补：罪灭篇坏结局兜底（原移植版 call 了不存在的标签）
# 触发条件 persistent.console_choices = True（调试选项，正常游玩不会进入）


label tsum_badend1:

    $ save_name = __("Tsumihoroboshi-hen.\\nBADEND")
    $ persistent.tsum_badend1 = True

    stop music fadeout 1.0
    stop ambient fadeout 1.0
    scene black with Dissolve(1.5)

    n "……我做出了那个选择。"
    n "{nw}"
    n "那句「没问题的」，成了我最后一次听见自己的声音。"
    nvl clear

    n "第二天，雏见泽的失踪人数又增加了一个。"
    n "{nw}"
    n "报纸上只写了一行小字，没有照片，没有名字。"
    nvl clear

    n "在这个世界里，我终究没能走到最后。"
    n "{nw}"
    n "……但是，还有下一次。"
    nvl clear

    return


label tsum_badend2:

    $ save_name = __("Tsumihoroboshi-hen.\\nBADEND")
    $ persistent.tsum_badend2 = True

    stop music fadeout 1.0
    stop ambient fadeout 1.0
    scene black with Dissolve(1.5)

    n "我喊出的那句话，最终没有传到沙都子那里。"
    n "{nw}"
    n "……时间，到了。"
    nvl clear

    n "爆炸声。热风。然后是长久的寂静。"
    n "{nw}"
    n "雏见泽消失了，连同我所有没能说出口的话。"
    nvl clear

    n "这一次也失败了。"
    n "{nw}"
    n "……但是，只要还能重来。"
    nvl clear

    return
'''


def main():
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(BODY)
    print("wrote", OUT)


if __name__ == '__main__':
    main()
