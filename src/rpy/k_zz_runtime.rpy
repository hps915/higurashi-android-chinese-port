# -*- coding: utf-8 -*-
# 运行时修补：
#  1) 安卓端视频软解（否则 Movie(channel='movie') 在 hw_video=True 时直接抛异常，OP 无法播放）
#  2) 切后台策略：暂停住进程、回来直接继续（不再杀进程冷启动）
#  3) 缺失图像兜底：不再显示红色 "Image not found" 文本，改为记录日志 + 黑块占位

init -50 python:
    config.hw_video = False

    # 第 8 轮：切后台不再 quit。
    # 旧策略是 save_on_mobile_background + quit_on_mobile_background，
    # 切后台直接 sys.exit(0)，回来要冷启动重载 2GB 资源（9~10 秒纯黑），
    # 用户体感就是"切后台回来黑屏/卡死"；而且存档若恰好发生在 OP 播放或
    # 转场中途，读回来的状态可能不一致，也会黑屏。
    # 现在保留进程：引擎在 APP_WILLENTERBACKGROUND 里会 pause_all 音频、
    # 存一份 _reload-1 兜底（进程万一被系统杀掉仍能恢复），回前台时
    # unpause_all + 重置显示，做到秒回。
    config.save_on_mobile_background = True
    config.quit_on_mobile_background = False

init 999 python:
    _zz_orig_find_target = renpy.display.image.ImageReference.find_target

    def _zz_find_target(self):
        try:
            rv = _zz_orig_find_target(self)
        except Exception:
            rv = False
        target = getattr(self, "target", None)
        notfound = getattr(target, "text", None)
        if rv is False or (isinstance(notfound, str) and "not found" in notfound):
            try:
                nm = self.name
                if not isinstance(nm, tuple):
                    nm = tuple(str(nm).split())
                renpy.log("ZZMISSING: " + " ".join(nm))
            except Exception:
                pass
            try:
                self.target = renpy.display.imagelike.Solid("#101010")
            except Exception:
                self.target = None
            return True
        return rv

    renpy.display.image.ImageReference.find_target = _zz_find_target


# ---------------------------------------------------------------------------
# 回前台兜底清理
# 引擎从后台恢复时只做 unpause_all + display_reset + restart_interaction。
# 如果切后台那一刻正在快进，回来会继续疯狂快进把剧情冲过去；这里在每次
# 交互开始时清掉"后台期间遗留的快进/自动标记"，但只在标记是后台期间产生
# 的情况下才清（用时间戳判断），避免干扰玩家主动开启的快进。
# 注意：绝不在这里碰 movie 通道——OP 正在播时它就是被占用的，停掉会黑屏。
# ---------------------------------------------------------------------------

init 1000 python:
    import time as _zz_time
    _zz_bg_last_fg = [_zz_time.time()]

    def _zz_bg_sanitize():
        now = _zz_time.time()
        prev = _zz_bg_last_fg[0]
        _zz_bg_last_fg[0] = now
        # 相邻交互间隔超过 8 秒 = 中间大概率经历了切后台/锁屏
        if now - prev > 8.0:
            try:
                if renpy.config.skipping:
                    renpy.config.skipping = None
            except Exception:
                pass
            try:
                if _preferences.afm_enable:
                    _preferences.afm_enable = False
            except Exception:
                pass

    config.start_interact_callbacks.append(_zz_bg_sanitize)
