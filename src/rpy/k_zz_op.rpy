# -*- coding: utf-8 -*-
# 章节开场动画（自动生成）。
#
# 触发规则（第 7 轮）：从菜单/章节选择进入某章时，入口别名标签把该章名写进
# renpy._zz_op_pending；该章脚本里的锚点 call zz_op_at("xxx") 取用一次即清除。
# 于是"每次从菜单开新档都播"，而"跳关/读档"不经过别名标签，就不播。
#
# 播放规则：
#   * 设置里 OP=关：直接返回，不播也不打断快进；
#   * 到达锚点时若处于快进/自动模式，先自动关掉（快进指示器熄灭）；
#   * 起播后 0.9 秒起步保护：这段交互里没有任何点击行为，吞掉快进末尾残click；
#   * 保护期后换成可关闭的交互：手动点击可立即跳过 OP，不锁死；
#   * 播放全程把 music/ambient/repeated/sound/voice* 暂停（不是销毁），
#     结束后解除暂停，原曲从原位置继续 —— OP 里不会混入游戏 BGM，
#     播完也绝不会静音卡死。

default persistent.opening = True

init 9 python:
    if persistent._zz_op_migrate is None:
        persistent.opening = True
        persistent._zz_op_migrate = True

init -10 python:
    # 每章待播标记。挂在 renpy 模块上：不进存档、不参与回滚，进程内有效。
    if not hasattr(renpy, "_zz_op_pending"):
        renpy._zz_op_pending = set()

    # OP 期间需要静音的声道（movie 通道本身除外）。
    ZzOpChannels = ("music", "ambient", "repeated", "sound", "sound2",
                    "voice", "voice1", "voice2", "voice3", "voice4",
                    "voice5", "voice6", "voice7", "voice8")

    def zz_op_stop_modes():
        # 关掉快进（右下角双三角）与自动模式，返回是否改动过。
        changed = False
        try:
            if renpy.config.skipping:
                renpy.config.skipping = None
                changed = True
        except Exception:
            pass
        try:
            if _preferences.afm_enable:
                _preferences.afm_enable = False
                changed = True
        except Exception:
            pass
        if changed:
            renpy.restart_interaction()
        return changed

    def zz_op_pause_audio():
        # 暂停而不是停止：不销毁队列、不丢播放位置，解除暂停后原样继续。
        for ch in ZzOpChannels:
            try:
                renpy.audio.music.set_pause(True, channel=ch)
            except Exception:
                pass

    def zz_op_resume_audio():
        for ch in ZzOpChannels:
            try:
                renpy.audio.music.set_pause(False, channel=ch)
            except Exception:
                pass

    def zz_op_play(name):
        path = "movie/" + name + ".ogv"
        if not renpy.loader.loadable(path):
            print("ZZOP missing movie: " + path)
            return

        saved_rollback_side = renpy.config.enable_rollback_side
        zz_op_pause_audio()
        try:
            renpy.config.enable_rollback_side = False
            renpy.movie_start_fullscreen(path)

            # ① 起步保护 0.9 秒：只有定时器，没有任何点击行为 → 手点无效。
            renpy.ui.pausebehavior(0.9, False)
            renpy.ui.interact(suppress_overlay=True)

            # ② 正常播放：手点跳过，或视频播完（movie 通道停止）自然结束。
            renpy.ui.saybehavior()
            renpy.ui.soundstopbehavior("movie")
            renpy.ui.interact(suppress_overlay=True)
        finally:
            renpy.config.enable_rollback_side = saved_rollback_side
            try:
                renpy.movie_stop()
            except Exception:
                pass
            zz_op_resume_audio()

    def zz_op_take_pending(name):
        # 取用一次就清除；无论 OP 开关如何都清，避免旧标记留到下次。
        pending = getattr(renpy, "_zz_op_pending", None)
        if pending is None:
            pending = renpy._zz_op_pending = set()
        if name in pending:
            pending.discard(name)
            return True
        return False

    def zz_op_should_play(name):
        taken = zz_op_take_pending(name)
        print("ZZOP at %s: pending=%s opening=%s" % (name, taken, persistent.opening))
        return taken and persistent.opening

label zz_op_at(name):
    if zz_op_should_play(name):
        $ zz_op_stop_modes()
        scene black with Dissolve(0.4)
        $ zz_op_play(name)
        scene black with Dissolve(0.4)
    return


label zz_op_meak:
    $ renpy._zz_op_pending.add("meak")
    jump meakashi_prologue

label zz_op_tsum:
    $ renpy._zz_op_pending.add("tsum")
    jump tsumihoroboshi_prologue

label zz_op_mina:
    $ renpy._zz_op_pending.add("mina")
    jump minagoroshi_prologue

label zz_op_matu:
    $ renpy._zz_op_pending.add("matu")
    jump matsuribayashi_prologue
