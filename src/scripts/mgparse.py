# -*- coding: utf-8 -*-
"""MGSC (.mg) compiled script parser for Higurashi (MangaGamer/07th-mod engine).

Binary format (reverse-engineered from 07th-mod/higurashi-assembly C# source):
  Header: b"MGSC" | int32 version(=1) | int32 blockCount | int32 lineCount | int32 dataLen
  Blocks: [7bit-len-prefixed utf8 name + int32 offset] x blockCount   (offsets into data)
  Lines:  int32 offset x lineCount
  Data:   linear command stream

  Commands (int16):
    0 Return | 1 LineNum + int32 | 2 Operation + int16 opcode + params
    3 If + BGIValue(cond) + int32 elseOffset ... 6 Jump + int32 endOffset ...
    4 Declaration + str name + str type + (int16(1) | BGIValue index)
    5 Assignment + BGIValue lhs + BGIValue rhs
    6 Jump + int32

  BGIValue (int16 type):
    1 Null | 2 Int + int32 | 3 String + 7bit-str | 4 Bool + uint8
    5 Variable + str name + BGIValue(member) + uint8 hasRef (+ nested ref)
    6 Operation + int16 opcode + params(self-describing)
    8 Math + int16 mathType + BGIValue + BGIValue
"""
import struct

# opcode -> (name, param signature)  'i'int 's'string 'b'bool 'v'variable; any pos may be Null
OPSIG = {
    0: ("StoreValueToLocalWork", "vi"), 1: ("LoadValueFromLocalWork", "v"),
    2: ("SetLocalFlag", "vi"), 3: ("SetGlobalFlag", "vi"),
    4: ("GetLocalFlag", "v"), 5: ("GetGlobalFlag", "v"),
    6: ("CallScript", "s"), 7: ("JumpScript", "s"),
    8: ("CallSection", "s"), 9: ("JumpSection", "s"),
    10: ("Wait", "i"), 11: ("WaitForInput", ""),
    12: ("SetValidityOfSkipping", "b"), 13: ("SetValidityOfSaving", "b"),
    14: ("SetValidityOfInput", "b"), 15: ("SetValidityOfUserEffectSpeed", "b"),
    16: ("OutputLine", "ssssi"), 17: ("OutputLineAll", "ssi"),
    18: ("ClearMessage", ""), 19: ("SetFontOfMessage", "iii"),
    20: ("SetSpeedOfMessage", "bi"), 21: ("DisableWindow", ""),
    22: ("SpringText", "ii"), 23: ("SetStyleOfMessageSwinging", "i"),
    24: ("Select", "iv"), 25: ("PlayBGM", "isii"), 26: ("StopBGM", "i"),
    27: ("ChangeVolumeOfBGM", "iii"), 28: ("FadeOutBGM", "iib"),
    29: ("FadeOutMultiBGM", "iiib"), 30: ("PlaySE", "isii"), 31: ("StopSE", "i"),
    32: ("FadeOutSE", "ii"), 33: ("WaitToFinishSEPlaying", "i"),
    34: ("PlayVoice", "isi"), 35: ("WaitToFinishVoicePlaying", "i"),
    36: ("PreloadBitmap", "s"),
    37: ("StartShakingOfAllObjects", "iiiiib"), 38: ("TerminateShakingOfAllObjects", "ib"),
    39: ("StartShakingOfWindow", "iiiiib"), 40: ("TerminateShakingOfWindow", "ib"),
    41: ("StartShakingOfBustshot", "iiiiiib"), 42: ("TerminateShakingOfBustshot", "iib"),
    43: ("StartShakingOfSprite", "iiiiiib"), 44: ("TerminateShakingOfSprite", "iib"),
    45: ("ShakeScreen", "iiiii"), 46: ("ShakeScreenSx", "ii"),
    47: ("DrawBG", "sib"), 48: ("FadeBG", "ib"), 49: ("DrawBGWithMask", "ssiib"),
    50: ("DrawScene", "si"), 51: ("DrawSceneWithMask", "ssiii"),
    52: ("ChangeScene", "sii"), 53: ("FadeScene", "i"), 54: ("FadeSceneWithMask", "siii"),
    55: ("DrawBustshot", "isiiibiiiiiiiiib"), 56: ("MoveBustshot", "isiiiiib"),
    57: ("FadeBustshot", "ibiiiiib"), 58: ("DrawBustshotWithFiltering", "issiiibiiiiiiib"),
    59: ("DrawFace", "sib"), 60: ("FadeFace", "ib"), 61: ("ExecutePlannedControl", "b"),
    62: ("DrawSprite", "issiiiiiibbiiiib"), 63: ("DrawSpriteWithFiltering", "issiiibbiiiib"),
    64: ("FadeSprite", "iib"), 65: ("FadeSpriteWithFiltering", "isiib"),
    66: ("MoveSprite", "iiiiiiiiib"), 67: ("MoveSpriteEx", "isiiviiiiib"),
    68: ("ControlMotionOfSprite", "iivi"), 69: ("GetPositionOfSprite", "vi"),
    70: ("EnableHorizontalGradation", "iib"), 71: ("DisableGradation", "ib"),
    72: ("EnlargeScreen", "iiiibib"), 73: ("DisableEffector", "ib"),
    74: ("EnableBlur", "iib"), 75: ("DisableBlur", "ib"), 76: ("DrawFilm", "iiiiiiib"),
    77: ("FadeFilm", "ib"), 78: ("SetValidityOfFilmToFace", "b"),
    79: ("FadeAllBustshots", "ib"), 80: ("FadeBustshotWithFiltering", "isibiiib"),
    81: ("SetDrawingPointOfMessage", "ii"), 82: ("Negative", "ib"),
    83: ("EnableJumpingOfReturnIcon", ""), 84: ("SetValidityOfWindowDisablingWhenGraphicsControl", "b"),
    85: ("SetValidityOfInterface", "b"), 86: ("ViewTips", "i"),
    87: ("ViewChapterScreen", ""), 88: ("ViewExtras", ""), 89: ("ChapterPreview", ""),
    90: ("SavePoint", "ss"), 91: ("PlaceViewTip", "i"), 92: ("PlaceViewTip2", "ii"),
    93: ("DrawStandgraphic", "isbiib"), 94: ("DrawBustFace", "isbi"),
    95: ("PlusStandgraphic1", "is"), 96: ("PlusStandgraphic2", "is"),
    97: ("PlusStandgraphic3", "is"), 98: ("FadeAllBustshots2", "ib"),
    99: ("FadeAllBustshots3", "ib"), 100: ("BlurOffOn", "ii"), 101: ("TitleScreen", ""),
    102: ("OpenGallery", ""), 103: ("HideGallery", ""), 104: ("RevealGallery", ""),
    105: ("CloseGallery", ""), 106: ("SetSkipAll", "b"), 107: ("SetTextFade", "b"),
    108: ("Break", ""), 109: ("LanguagePrompt", ""), 110: ("GetAchievement", "s"),
    111: ("CheckTipsAchievements", ""), 112: ("SetFontId", "i"), 113: ("SetCharSpacing", "i"),
    114: ("SetLineSpacing", "i"), 115: ("SetFontSize", "i"), 116: ("SetWindowPos", "ii"),
    117: ("SetWindowSize", "ii"), 118: ("SetWindowMargins", "iiii"), 119: ("SetNameFormat", "s"),
    120: ("SetScreenAspect", "s"), 121: ("SetGuiPosition", "ii"),
    122: ("ModEnableNVLModeInADVMode", ""), 123: ("ModDisableNVLModeInADVMode", ""),
    124: ("ModADVModeSettingLoad", "siiiiiiiiiiii"), 125: ("ModNVLModeSettingLoad", "siiiiiiiiiiii"),
    126: ("ModNVLADVModeSettingLoad", "siiiiiiiiiiii"), 127: ("ModCallScriptSection", "ss"),
    128: ("ModDrawCharacter", "iissiiibiiiiiiiiib"),
    129: ("ModDrawCharacterWithFiltering", "iisssiiibiiiiiiib"),
    130: ("ModPlayVoiceLS", "iisib"), 131: ("ModPlayMovie", "s"),
    132: ("ModSetConfigFontSize", "i"), 133: ("ModSetChapterJumpFontSize", "ii"),
    134: ("ModSetHighestChapterFlag", "ii"), 135: ("ModGetHighestChapterFlag", "i"),
    136: ("ModSetMainFontOutlineWidth", "i"), 137: ("ModSetLayerFilter", "iis"),
    138: ("ModAddArtset", "sss"), 139: ("ModClearArtsets", ""),
    140: ("ModRyukishiModeSettingLoad", "siiiiiiiiiiii"), 141: ("ModRyukishiSetGuiPosition", "ii"),
    142: ("ModPlayBGM", "isiii"), 143: ("ModFadeOutBGM", "iibi"),
    144: ("ModAddBGMset", "sss"), 145: ("ModAddSEset", "sss"),
    146: ("ModAddAudioset", "ssssiiii"), 147: ("ModGenericCall", "ss"),
}


class Reader:
    __slots__ = ("data", "pos")

    def __init__(self, data, pos=0):
        self.data = data
        self.pos = pos

    def i16(self):
        v = struct.unpack_from("<h", self.data, self.pos)[0]
        self.pos += 2
        return v

    def peek16(self):
        return struct.unpack_from("<h", self.data, self.pos)[0]

    def i32(self):
        v = struct.unpack_from("<i", self.data, self.pos)[0]
        self.pos += 4
        return v

    def u8(self):
        v = self.data[self.pos]
        self.pos += 1
        return v

    def bstr(self):
        """BinaryWriter.Write(string): 7-bit encoded length prefix + UTF-8 bytes."""
        n = 0
        shift = 0
        while True:
            b = self.data[self.pos]
            self.pos += 1
            n |= (b & 0x7F) << shift
            if not (b & 0x80):
                break
            shift += 7
        s = self.data[self.pos:self.pos + n].decode("utf-8")
        self.pos += n
        return s


def set_opsig(table):
    """Swap in a per-chapter opcode table {opcode: (name, sig)}."""
    global OPSIG
    OPSIG = dict(table)


def _opsig_lookup(op):
    if op == -1:
        return ("NullOp", "")
    if op not in OPSIG:
        raise ValueError(f"unknown opcode {op}")
    return OPSIG[op]


def read_value(r):
    """Read one BGIValue, return a plain python representation."""
    t = r.i16()
    if t == 1:
        return None
    if t == 2:
        return r.i32()
    if t == 3:
        return r.bstr()
    if t == 4:
        return bool(r.u8())
    if t == 5:  # variable reference
        return read_reference(r)
    if t == 6:  # nested operation as a value
        op = r.i16()
        name, sig = _opsig_lookup(op)
        params = [read_value(r) for _ in sig]
        return ("call", name, params)
    if t == 8:  # math
        mt = r.i16()
        a = read_value(r)
        b = read_value(r)
        return ("math", mt, a, b)
    raise ValueError(f"unknown BGIValue type {t} at pos {r.pos - 2}")


def read_reference(r):
    name = r.bstr()
    member = read_value(r)
    has_ref = r.u8()
    ref = read_reference(r) if has_ref else None
    return ("var", name, member, ref)


def walk(data, verbose_errors=True):
    """Walk the data segment linearly, return a list of events.
    Events: ('linenum', n) | ('op', opcode, name, params) | ('if', cond) |
            ('jump', off) | ('return',) | ('decl',...) | ('assign', lhs, rhs)
    """
    r = Reader(data)
    events = []
    try:
        while r.pos < len(data):
            cmd = r.i16()
            if cmd == 0:
                events.append(("return",))
            elif cmd == 1:
                events.append(("linenum", r.i32()))
            elif cmd == 2:
                op = r.i16()
                name, sig = _opsig_lookup(op)
                params = [read_value(r) for _ in sig]
                events.append(("op", op, name, params))
            elif cmd == 3:  # If
                cond = read_value(r)
                _else_off = r.i32()
                events.append(("if", cond))
            elif cmd == 4:  # Declaration
                name = r.bstr()
                vtype = r.bstr()
                if r.peek16() == 1:
                    r.i16()
                    idx = None
                else:
                    idx = read_value(r)
                events.append(("decl", name, vtype, idx))
            elif cmd == 5:  # Assignment
                lhs = read_value(r)
                rhs = read_value(r)
                events.append(("assign", lhs, rhs))
            elif cmd == 6:  # Jump
                events.append(("jump", r.i32()))
            else:
                raise ValueError(f"unknown command {cmd} at pos {r.pos - 2}")
    except (ValueError, struct.error) as e:
        if verbose_errors:
            raise ValueError(f"desync at pos {r.pos}: {e}") from e
        events.append(("error", str(e), r.pos))
    return events


def load(path):
    with open(path, "rb") as f:
        raw = f.read()
    if raw[:4] != b"MGSC":
        raise ValueError(f"{path}: bad magic")
    ver, nblocks, nlines, datalen = struct.unpack_from("<4i", raw, 4)
    if ver != 1:
        raise ValueError(f"{path}: unsupported version {ver}")
    r = Reader(raw, 20)
    blocks = {}
    for _ in range(nblocks):
        nm = r.bstr()
        blocks[nm] = r.i32()
    lines = [r.i32() for _ in range(nlines)]
    if r.pos != len(raw) - datalen:
        raise ValueError(f"{path}: header size mismatch pos={r.pos} expected={len(raw) - datalen}")
    data = raw[r.pos:]
    return {"blocks": blocks, "lines": lines, "data": data, "events": walk(data)}


if __name__ == "__main__":
    import sys
    d = load(sys.argv[1])
    from collections import Counter
    c = Counter(e[0] for e in d["events"])
    print("blocks:", list(d["blocks"])[:5], "... total", len(d["blocks"]))
    print("lines:", len(d["lines"]))
    print("event counts:", dict(c))
    # show first OutputLine & voice
    for e in d["events"]:
        if e[0] == "op" and e[2] in ("OutputLine", "ModPlayVoiceLS", "PlayVoice", "OutputLineAll"):
            print(e[2], "→", repr(e[3])[:200])
