#!/usr/bin/env python3
"""Pixel RMS between two same-size PNG screenshots."""
import struct
import sys
import zlib


def read_png_rows(path):
    raw = open(path, "rb").read()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    w = h = None
    data = b""
    i = 8
    while i < len(raw):
        ln = struct.unpack(">I", raw[i : i + 4])[0]
        i += 4
        typ = raw[i : i + 4]
        i += 4
        chunk = raw[i : i + ln]
        i += ln + 4
        if typ == b"IHDR":
            w, h = struct.unpack(">II", chunk[:8])
        elif typ == b"IDAT":
            data += chunk
        elif typ == b"IEND":
            break
    img = zlib.decompress(data)
    rows = []
    off = 0
    for _ in range(h):
        off += 1
        rows.append(img[off : off + w * 3])
        off += w * 3
    return w, h, rows


def main():
    w, h, ra = read_png_rows(sys.argv[1])
    w2, h2, rb = read_png_rows(sys.argv[2])
    if (w, h) != (w2, h2):
        raise SystemExit("size mismatch")
    acc = 0.0
    n = w * h * 3
    for y in range(h):
        for x in range(w * 3):
            d = ra[y][x] - rb[y][x]
            acc += d * d
    print((acc / n) ** 0.5)


if __name__ == "__main__":
    main()