#!/usr/bin/env python3
"""
Render subtitle lines to transparent PNGs for ffmpeg `overlay`.

Why this exists: many macOS ffmpeg builds lack libass/drawtext, so we render
text with Pillow (which handles Korean via AppleSDGothicNeo) and composite the
PNGs with overlay+enable gating. One PNG per subtitle line, full-frame, so the
overlay is a trivial 0:0 composite.

Usage:
    python3 gen_subs.py subs.json [out_dir] [--w 1280] [--h 720] [--margin 56] [--size 44]

    16:9 project (default):  --w 1280 --h 720
    9:16 vertical project:   --w 720 --h 1280 --margin 190
      (the raised bottom margin keeps lines above the shorts/reels player UI —
       progress bar, caption strip, action buttons)

    Font size is fixed (dlg 44px / narr 36px) regardless of canvas width — on a
    720-wide 9:16 canvas that is intentionally a larger relative size, matching
    the big-caption look of shorts/reels. Override with --size <px> (dlg size;
    narr scales to ~82%) if a project needs it.

subs.json format:
    [
      {"id": "c1a", "text": "〔 평범한 아침 〕",            "type": "narr"},
      {"id": "c1b", "text": "[대표] 내일까지 완성!",          "type": "dlg"},
      ...
    ]
  type: "dlg"  -> white, larger (spoken dialogue)
        "narr" -> warm yellow, smaller (narration / labels / descriptions)

Output: <out_dir>/<id>.png  (default out_dir = ./subs_png)
"""
import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont

# Korean-capable system font; override with env SUB_FONT if needed.
FONT_PATH = os.environ.get("SUB_FONT", "/System/Library/Fonts/AppleSDGothicNeo.ttc")


def wrap(draw, text, font, maxw):
    # space-based first; Korean often has long space-less runs, so any chunk
    # that still exceeds maxw gets broken at character level (otherwise the
    # line overflows the canvas silently)
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
            continue
        if cur:
            lines.append(cur)
        while draw.textlength(w, font=font) > maxw:
            k = len(w)
            while k > 1 and draw.textlength(w[:k], font=font) > maxw:
                k -= 1
            lines.append(w[:k])
            w = w[k:]
        cur = w
    if cur:
        lines.append(cur)
    return lines or [text]


def render(item, out_dir, W, H, margin, base_size=44):
    typ = item.get("type", "dlg")
    size = base_size if typ == "dlg" else int(base_size * 36 / 44)
    color = (255, 255, 255, 255) if typ == "dlg" else (255, 212, 121, 255)
    font = ImageFont.truetype(FONT_PATH, size, index=0)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lines = wrap(d, item["text"].strip(), font, W - 200)
    asc, desc = font.getmetrics()
    lh = asc + desc + 8
    total_h = lh * len(lines)
    y0 = H - margin - total_h
    maxw = max(d.textlength(ln, font=font) for ln in lines)
    pad = 24
    box = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(box).rounded_rectangle(
        [(W - maxw) / 2 - pad, y0 - 14, (W + maxw) / 2 + pad, y0 + total_h + 10],
        radius=20, fill=(0, 0, 0, 130))
    img = Image.alpha_composite(img, box)
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=font)
        d.text(((W - tw) / 2, y0 + i * lh), ln, font=font, fill=color,
               stroke_width=4, stroke_fill=(0, 0, 0, 255))
    img.save(os.path.join(out_dir, item["id"] + ".png"))
    print("saved", item["id"], typ, "lines:", len(lines))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    manifest = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "subs_png"
    W = H = M = S = None
    if "--w" in sys.argv:
        W = int(sys.argv[sys.argv.index("--w") + 1])
    if "--h" in sys.argv:
        H = int(sys.argv[sys.argv.index("--h") + 1])
    if "--margin" in sys.argv:
        M = int(sys.argv[sys.argv.index("--margin") + 1])
    if "--size" in sys.argv:
        S = int(sys.argv[sys.argv.index("--size") + 1])
    W, H, M, S = W or 1280, H or 720, M or 56, S or 44
    os.makedirs(out_dir, exist_ok=True)
    with open(manifest, encoding="utf-8") as f:
        items = json.load(f)
    for it in items:
        render(it, out_dir, W, H, M, S)
    print("DONE ->", out_dir)


if __name__ == "__main__":
    main()
