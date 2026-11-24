"""Render a pinned UTC news edition with the Python standard library."""
import argparse
import base64
import json
import os
import re
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
W = H = 1024

def chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))

def run(day, destination):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        raise ValueError("Expected an ISO edition date")
    folder = ROOT / "editions" / day
    edition = json.loads((folder / "news.json").read_bytes())
    if edition["utc_date"] != day:
        raise ValueError("Edition date mismatch")
    pixels = bytearray(zlib.decompress((folder / "plate.rgbz").read_bytes()))
    if len(pixels) != W * H * 3:
        raise ValueError("Invalid illustration plate")
    atlas = json.loads(zlib.decompress((folder / "type.jsonz").read_bytes()))
    for role, x, y, color, line in edition["lines"]:
        face = atlas[role]
        red, green, blue = bytes.fromhex(color)
        cursor = x * 64
        for char in line:
            advance, dx, dy, width, height, encoded = face[char]
            left = (cursor + 32) // 64 + dx
            top = y + dy
            if left < 0 or top < 0 or left + width > W or top + height > H:
                raise ValueError("Clipped line: " + line)
            mask = base64.b64decode(encoded)
            for row in range(height):
                pos = ((top + row) * W + left) * 3
                for col in range(width):
                    alpha = mask[row * width + col]
                    if alpha:
                        offset = pos + col * 3
                        inv = 255 - alpha
                        for channel, target in enumerate((red, green, blue)):
                            pixels[offset+channel] = (inv*pixels[offset+channel] + alpha*target + 127)//255
            cursor += advance
    scanlines = b"".join(b"\0" + pixels[y*W*3:(y+1)*W*3] for y in range(H))
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", W,H,8,2,0,0,0))
    png += chunk(b"IDAT", zlib.compress(scanlines,9)) + chunk(b"IEND", b"")
    if len(png) > 1024**2:
        raise ValueError("Image exceeds the edition's 1 MiB limit")
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "entry.png").write_bytes(png)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=(ROOT / "edition.txt").read_text().strip())
    parser.add_argument("--out", type=Path, default=Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")))
    args = parser.parse_args()
    run(args.date, args.out)
