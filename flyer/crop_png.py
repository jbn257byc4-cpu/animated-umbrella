#!/usr/bin/env python3
"""Crop a PNG to its top N rows, in place. Standard library only.

Headless Chromium reserves part of --window-size for window chrome, so the
painted viewport is shorter than the requested height and a screenshot taken at
exactly the poster height loses its last rows. render.sh works around that by
capturing a taller window; this trims the surplus back to the poster height.

Keeping the *top* rows means every retained scanline's filter still refers only
to rows that are also retained, so the image data needs no unfiltering.
"""
import struct
import sys
import zlib


def crop_top(path, keep_height):
    with open(path, 'rb') as fh:
        data = fh.read()

    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise SystemExit(f'{path}: not a PNG')

    chunks = []
    pos = 8
    while pos < len(data):
        (length,) = struct.unpack('>I', data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        chunks.append((ctype, body))
        pos += 12 + length

    width, height, depth, colour, _, _, interlace = struct.unpack(
        '>IIBBBBB', dict(chunks)[b'IHDR'])
    if interlace:
        raise SystemExit(f'{path}: interlaced PNGs are not supported')
    if keep_height >= height:
        return height

    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[colour]
    stride = 1 + (width * channels * depth + 7) // 8

    raw = zlib.decompress(b''.join(b for t, b in chunks if t == b'IDAT'))
    raw = raw[:keep_height * stride]

    out = [b'\x89PNG\r\n\x1a\n']
    written_idat = False
    for ctype, body in chunks:
        if ctype == b'IHDR':
            body = struct.pack('>II', width, keep_height) + body[8:]
        elif ctype == b'IDAT':
            if written_idat:
                continue
            body = zlib.compress(raw, 9)
            written_idat = True
        out.append(struct.pack('>I', len(body)) + ctype + body
                   + struct.pack('>I', zlib.crc32(ctype + body) & 0xFFFFFFFF))

    with open(path, 'wb') as fh:
        fh.write(b''.join(out))
    return keep_height


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: crop_png.py <file.png> <keep-height>')
    crop_top(sys.argv[1], int(sys.argv[2]))
