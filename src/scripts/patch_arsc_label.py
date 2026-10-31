# -*- coding: utf-8 -*-
"""Patch the app label string inside resources.arsc (binary surgery).

The label lives in the global UTF-8 string pool. Chinese text is longer
than the original English, so we append the new string at the end of the
string-pool chunk and repoint the existing offset entry (old bytes become
dead data). Chunk + table sizes are updated accordingly.

Usage: patch_arsc_label.py <in.arsc> <out.arsc> <old> <new>
"""
import struct
import sys


def pool_utf8_str(data, abs_off):
    """Read a UTF-8 pool string (two u16v lengths + bytes + 0)."""
    p = abs_off
    char_len = 0
    shift = 0
    while True:
        b = data[p]
        p += 1
        char_len |= (b & 0x7F) << shift
        if not b & 0x80:
            break
        shift += 7
        if shift > 21:
            return None
    byte_len = 0
    shift = 0
    while True:
        b = data[p]
        p += 1
        byte_len |= (b & 0x7F) << shift
        if not b & 0x80:
            break
        shift += 7
        if shift > 21:
            return None
    if byte_len > 4096:
        return None
    try:
        return data[p:p + byte_len].decode("utf-8"), byte_len
    except UnicodeDecodeError:
        return None


def encode_pool_utf8(s):
    b = s.encode("utf-8")
    char_len = len(s)
    byte_len = len(b)
    out = b""
    for v in (char_len, byte_len):
        if v > 0x7F:
            out += bytes([(v & 0x7F) | 0x80, v >> 7])
        else:
            out += bytes([v])
    return out + b + b"\x00"


def main():
    src, dst, old, new = sys.argv[1:5]
    data = bytearray(open(src, "rb").read())

    # ResTable_header = 12 bytes, then global string pool chunk
    sp_off = 12
    sp_type, sp_hdr, sp_size = struct.unpack_from("<HHI", data, sp_off)
    assert sp_type == 0x0001, f"first chunk not string pool: {sp_type:#x}"
    (str_count, style_count, flags, strings_start, styles_start) = struct.unpack_from(
        "<IIIII", data, sp_off + 8)
    assert flags & 0x100, "pool is not UTF-8"

    offsets = list(struct.unpack_from("<%dI" % str_count, data, sp_off + sp_hdr))

    targets = []
    for i in range(str_count):
        if offsets[i] == 0xFFFFFFFF:
            continue
        r = pool_utf8_str(data, sp_off + strings_start + offsets[i])
        if r and r[0] == old:
            targets.append(i)
    if not targets:
        raise SystemExit(f"label string not found in pool: {old!r}")
    print(f"found {len(targets)} pool entries for {old!r}: indices {targets}")

    # append the new string at the very end of the pool chunk (4-byte aligned)
    new_enc = encode_pool_utf8(new)
    pad = (4 - (len(new_enc) % 4)) % 4
    new_enc += b"\x00" * pad
    append_at = sp_off + sp_size  # absolute
    # offset (relative to stringsStart) of the appended string start:
    new_offset = (append_at - sp_off) - strings_start

    data[append_at:append_at] = new_enc

    # patch the target offset entries
    for i in targets:
        struct.pack_into("<I", data, sp_off + sp_hdr + 4 * i, new_offset)

    # grow chunk size + table size
    struct.pack_into("<I", data, sp_off + 4, sp_size + len(new_enc))
    table_size = struct.unpack_from("<I", data, 4)[0]
    struct.pack_into("<I", data, 4, table_size + len(new_enc))

    open(dst, "wb").write(bytes(data))
    print(f"patched: {old!r} -> {new!r} (appended {len(new_enc)} bytes)")


if __name__ == "__main__":
    main()
