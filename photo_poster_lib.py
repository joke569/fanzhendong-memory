# -*- coding: utf-8 -*-
"""Append photo-based poster generation to art_generate.py (called from main)."""
import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance

# These names are supplied by art_generate.py when this file is exec'd there.
# (Kept as a separate module for readability.)

def photo_poster(src, cfg, crop=(0, 0, 0, 0), focus=(0.5, 0.35)):
    img = Image.open(src).convert("RGB")
    w, h = img.size
    l, t, r, b = crop
    if any(crop):
        img = img.crop((int(w * l), int(h * t), int(w * (1 - r)), int(h * (1 - b))))
    img = ImageOps.fit(img, (W * S, H * S), method=Image.LANCZOS, centering=focus)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(0.88)
    img = img.convert("RGBA")

    # cinematic grade overlays
    grade = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(grade, "RGBA")
    accent = cfg["accent"]
    # bottom fade for legibility
    for i in range(70):
        y = int(H * S * (0.54 + i / 70 * 0.46))
        alpha = int(235 * (i / 70) ** 1.4)
        gd.rectangle([0, y, W * S, H * S], fill=(4, 6, 12, alpha))
    # cool shadow on left, warm glow top-right
    gd.rectangle([0, 0, W * S, H * S], fill=(4, 8, 18, 35))
    img = Image.alpha_composite(img, grade)
    img = Image.alpha_composite(img, radial_glow((W * S, H * S), (860, 220), 520 * S, accent, 55))

    # frame
    txt = Image.new("RGBA", img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(txt, "RGBA")
    m = 38 * S
    td.rectangle([m, m, W * S - m, H * S - m], outline=(255, 255, 255, 42), width=1 * S)
    img = Image.alpha_composite(img, txt)
    return add_grain(img, 4)

