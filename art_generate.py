# -*- coding: utf-8 -*-
"""Generate original editorial poster assets for the Fan Zhendong memory app."""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "entry", "src", "main", "resources", "base", "media")
WEB = os.path.join(BASE, "web", "assets")
os.makedirs(OUT, exist_ok=True)
os.makedirs(WEB, exist_ok=True)

W, H = 1080, 1440
S = 2
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_DISPLAY = r"C:\Windows\Fonts\bahnschrift.ttf"
FONT_DISPLAY_B = r"C:\Windows\Fonts\segoeuib.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(size * S))


def text(d, xy, s, size, fill, path=FONT_REG, anchor="mm", spacing=0):
    f = font(path, size)
    if spacing == 0:
        d.text((xy[0] * S, xy[1] * S), s, font=f, fill=fill, anchor=anchor)
        return
    # manual letter spacing
    total = sum(d.textlength(ch, font=f) for ch in s) + spacing * S * (len(s) - 1)
    if anchor[0] == "m":
        x = xy[0] * S - total / 2
    elif anchor[0] == "r":
        x = xy[0] * S - total
    else:
        x = xy[0] * S
    for ch in s:
        d.text((x, xy[1] * S), ch, font=f, fill=fill, anchor="l" + anchor[1])
        x += d.textlength(ch, font=f) + spacing * S


def vgrad(w, h, stops):
    """stops: [(pos, (r,g,b)), ...]"""
    arr = np.zeros((h, w, 3), dtype=np.float32)
    ys = np.linspace(0, 1, h)
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        m = (ys >= p0) & (ys <= p1)
        t = (ys[m] - p0) / max(p1 - p0, 1e-6)
        for k in range(3):
            arr[m, :, k] = c0[k] + (c1[k] - c0[k]) * t[:, None]
    return Image.fromarray(np.uint8(np.clip(arr, 0, 255)), "RGB").convert("RGBA")


def radial_glow(size, center, radius, color, opacity=120):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(*color, opacity))
    return layer.filter(ImageFilter.GaussianBlur(radius * 0.55))


def add_grain(img, amount=7):
    arr = np.array(img).astype(np.int16)
    noise = np.random.normal(0, amount, (arr.shape[0], arr.shape[1], 1))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    return Image.fromarray(np.uint8(arr), "RGBA")


def base_poster(top, bottom, accent, series, no, year):
    img = vgrad(W * S, H * S, [(0.0, top), (0.55, bottom), (1.0, (4, 6, 12))])
    # colored atmospheric glows
    for c, center, r, op in [
        (accent, (820, 250), 520, 60),
        ((255, 255, 255), (180, 1100), 500, 16),
        (accent, (100, 250), 300, 22),
    ]:
        img = Image.alpha_composite(img, radial_glow((W * S, H * S), center, r * S, c, op))
    # translucent graphic layer
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay, "RGBA")
    for x in range(0, W * S, 54 * S):
        od.line([(x, 0), (x, H * S)], fill=(255, 255, 255, 13), width=1 * S)
    for y in range(0, H * S, 54 * S):
        od.line([(0, y), (W * S, y)], fill=(255, 255, 255, 9), width=1 * S)
    od.polygon([(0, 0), (260 * S, 0), (700 * S, H * S), (420 * S, H * S)], fill=(*accent, 12))
    od.polygon([(720 * S, 0), (820 * S, 0), (1080 * S, 900 * S), (1080 * S, 760 * S)], fill=(255, 255, 255, 20))
    m = 38 * S
    od.rectangle([m, m, W * S - m, H * S - m], outline=(255, 255, 255, 40), width=1 * S)
    img = Image.alpha_composite(img, overlay)
    return img


def draw_player(img, cx, cy, scale, accent, pose="loop", facing=1):
    """Stylized vector athlete. Coordinates in final pixels, scale 1 ~ 400px tall."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    skin = (214, 160, 124, 255)
    skin_dark = (160, 108, 82, 255)
    hair = (24, 18, 16, 255)
    shorts = (12, 15, 24, 255)
    shirt = accent
    shoe = (235, 235, 235, 255)

    def P(x, y):
        return ((cx + facing * x * scale) * S, (cy + y * scale) * S)

    def seg(a, b, w, color):
        d.line([P(*a), P(*b)], fill=color, width=max(1, int(w * scale * S)))
        for q in (a, b):
            r = w * scale * S / 2
            d.ellipse([P(*q)[0] - r, P(*q)[1] - r, P(*q)[0] + r, P(*q)[1] + r], fill=color)

    # ground shadow
    d.ellipse([P(-120, 205)[0], P(-120, 205)[1], P(120, 230)[0], P(120, 230)[1]], fill=(0, 0, 0, 100))

    if pose == "child":
        # small child, oversized paddle, table edge at right
        seg((-10, -20), (-50, 40), 26, skin_dark)  # back leg
        seg((-50, 40), (10, 100), 22, skin_dark)
        seg((15, -20), (55, 35), 26, skin)
        seg((55, 35), (100, 90), 22, skin)
        # shorts / torso
        d.polygon([P(-48, -78), P(38, -78), P(52, -10), P(-55, -10)], fill=shorts)
        d.polygon([P(-55, -165), P(42, -165), P(52, -70), P(-48, -70)], fill=shirt)
        # arms
        seg((-42, -150), (-95, -90), 22, shirt)
        seg((-95, -90), (-120, -30), 18, skin)
        seg((32, -150), (85, -115), 22, shirt)
        seg((85, -115), (118, -50), 18, skin)
        # head
        hx, hy = 6, -200
        d.ellipse([P(hx - 40, hy - 45)[0], P(hx - 40, hy - 45)[1], P(hx + 40, hy + 40)[0], P(hx + 40, hy + 40)[1]], fill=skin)
        d.arc([P(hx - 43, hy - 50)[0], P(hx - 43, hy - 50)[1], P(hx + 43, hy + 25)[0], P(hx + 43, hy + 25)[1]], 185, 350, fill=hair, width=18 * S)
        # paddle oversized at right hand
        draw_paddle_shape(d, P(118, -50), 118 * scale * S, 155 * scale * S, (30, 30, 34, 255), (190, 38, 42, 255), accent, "FZD", angle=22)
    else:
        # legs
        seg((-18, 20), (-55, 105), 34, skin_dark)
        seg((-55, 105), (-70, 190), 26, skin_dark)
        seg((18, 20), (62, 100), 34, skin)
        seg((62, 100), (85, 185), 26, skin)
        # shoes
        d.rounded_rectangle([P(-115, 182)[0], P(-115, 182)[1], P(-35, 215)[0], P(-35, 215)[1]], radius=12 * S, fill=shoe)
        d.rounded_rectangle([P(40, 178)[0], P(40, 178)[1], P(125, 212)[0], P(125, 212)[1]], radius=12 * S, fill=shoe)
        # shorts
        d.polygon([P(-55, -5), P(52, -5), P(42, 55), P(-42, 55)], fill=shorts)
        # torso
        torso = [P(-62, -170), P(38, -178), P(62, -5), P(-55, -5)]
        d.polygon(torso, fill=shirt)
        # jersey side panels
        d.polygon([P(30, -170), P(38, -178), P(62, -5), P(48, -5)], fill=(255, 255, 255, 22))
        # arms / pose
        if pose == "serve":
            # left arm up with ball, right arm back
            seg((-52, -150), (-85, -200), 26, shirt)
            seg((-85, -200), (-70, -255), 20, skin)
            d.ellipse([P(-80, -278)[0], P(-80, -278)[1], P(-56, -254)[0], P(-56, -254)[1]], fill=(255, 255, 255, 245))
            seg((32, -150), (88, -110), 26, shirt)
            seg((88, -110), (112, -55), 20, skin)
            draw_paddle_shape(d, P(112, -55), 62 * scale * S, 82 * scale * S, (22, 22, 25, 255), (180, 35, 40, 255), accent, "FZD", angle=-28)
        elif pose == "cheer":
            seg((-52, -150), (-120, -205), 26, shirt)
            seg((-120, -205), (-150, -280), 20, skin)
            seg((32, -150), (120, -205), 26, shirt)
            seg((120, -205), (150, -280), 20, skin)
            # fists
            d.ellipse([P(-164, -300)[0], P(-164, -300)[1], P(-136, -270)[0], P(-136, -270)[1]], fill=skin)
            d.ellipse([P(136, -300)[0], P(136, -300)[1], P(164, -270)[0], P(164, -270)[1]], fill=skin)
            # paddle in right hand
            draw_paddle_shape(d, P(150, -285), 48 * scale * S, 64 * scale * S, (22, 22, 25, 255), (180, 35, 40, 255), accent, "FZD", angle=30)
        else:
            # loop / attack
            seg((-52, -150), (-105, -95), 26, shirt)
            seg((-105, -95), (-145, -40), 20, skin)
            seg((32, -150), (85, -170), 26, shirt)
            seg((85, -170), (135, -135), 20, skin)
            draw_paddle_shape(d, P(135, -135), 58 * scale * S, 76 * scale * S, (22, 22, 25, 255), (185, 36, 40, 255), accent, "FZD", angle=-35)
        # head
        hx, hy = 4, -205
        d.ellipse([P(hx - 40, hy - 45)[0], P(hx - 40, hy - 45)[1], P(hx + 40, hy + 40)[0], P(hx + 40, hy + 40)[1]], fill=skin)
        d.arc([P(hx - 43, hy - 50)[0], P(hx - 43, hy - 50)[1], P(hx + 43, hy + 25)[0], P(hx + 43, hy + 25)[1]], 185, 350, fill=hair, width=18 * S)
        # neck / collar
        d.polygon([P(-18, -178), P(26, -178), P(22, -150), P(-14, -150)], fill=skin_dark)
    # soft glow behind figure
    glow = layer.filter(ImageFilter.GaussianBlur(22 * S))
    img.alpha_composite(Image.blend(Image.new("RGBA", img.size, (0, 0, 0, 0)), glow, 0.24))
    img.alpha_composite(layer)


def draw_paddle_shape(d, center, w, h, blade, rubber, accent, label="FZD", angle=0):
    """Draw a paddle onto d. center is a pixel tuple; w/h are pixels."""
    cx, cy = center
    layer = Image.new("RGBA", d._image.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer, "RGBA")
    # blade is a superellipse-ish shape, handle below
    bw, bh = w, h
    pts = []
    for i in range(120):
        t = 2 * math.pi * i / 120
        x = math.copysign(abs(math.cos(t)) ** 0.78, math.cos(t)) * bw * 0.5
        y = math.copysign(abs(math.sin(t)) ** 0.86, math.sin(t)) * bh * 0.5
        if y > bh * 0.30:
            y = bh * 0.30 + (y - bh * 0.30) * 0.35
        pts.append((cx + x, cy + y))
    ld.polygon(pts, fill=blade)
    # rubber inset
    inset = 7 * S
    rpts = []
    for i in range(120):
        t = 2 * math.pi * i / 120
        x = math.copysign(abs(math.cos(t)) ** 0.78, math.cos(t)) * (bw * 0.5 - inset)
        y = math.copysign(abs(math.sin(t)) ** 0.86, math.sin(t)) * (bh * 0.5 - inset)
        if y > bh * 0.30:
            y = bh * 0.30 + (y - bh * 0.30) * 0.35
        rpts.append((cx + x, cy + y))
    ld.polygon(rpts, fill=rubber)
    # subtle rubber highlight
    hi = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    hd = ImageDraw.Draw(hi, "RGBA")
    hd.ellipse([cx - bw * 0.42, cy - bh * 0.45, cx + bw * 0.20, cy - bh * 0.02], fill=(255, 255, 255, 18))
    hi = hi.filter(ImageFilter.GaussianBlur(12 * S))
    layer = Image.alpha_composite(layer, hi)
    ld = ImageDraw.Draw(layer, "RGBA")
    # handle
    hw, hh = bw * 0.24, bh * 0.55
    hx, hy = cx - hw / 2, cy + bh * 0.28
    ld.rounded_rectangle([hx, hy, hx + hw, hy + hh], radius=hw * 0.35, fill=(120, 79, 46, 255))
    ld.rounded_rectangle([hx + 2 * S, hy + 2 * S, hx + hw * 0.45, hy + hh - 2 * S], radius=hw * 0.2, fill=(158, 108, 64, 255))
    # edge tape
    ld.line(pts + [pts[0]], fill=(*accent, 180), width=3 * S, joint="curve")
    # logo text
    f = font(FONT_DISPLAY_B, max(10, int(bw * 0.11 / S)))
    ld.text((cx, cy - bh * 0.04), label, font=f, fill=(255, 255, 255, 135), anchor="mm")
    f2 = font(FONT_DISPLAY, max(7, int(bw * 0.055 / S)))
    ld.text((cx, cy + bh * 0.08), "ALC", font=f2, fill=(*accent, 150), anchor="mm")
    if angle:
        layer = layer.rotate(angle, resample=Image.BICUBIC, center=(cx, cy))
    d._image.alpha_composite(layer)


def career_poster(cfg):
    img = base_poster(cfg["top"], cfg["bottom"], cfg["accent"], "CAREER", cfg["no"], cfg["year"])
    d = ImageDraw.Draw(img, "RGBA")
    accent = cfg["accent"]
    # table / net
    table_y = 1080
    d.polygon([(0, 1280 * S), (1080 * S, 1110 * S), (1080 * S, 1240 * S), (0, 1420 * S)], fill=(10, 16, 22, 220))
    d.line([(0, 1280 * S), (1080 * S, 1110 * S)], fill=(*accent, 80), width=2 * S)
    d.line([(760 * S, 1155 * S), (760 * S, 1295 * S)], fill=(255, 255, 255, 60), width=3 * S)
    # trajectory
    for i in range(3):
        d.arc([(520 - i * 20) * S, (280 - i * 12) * S, (1000 + i * 25) * S, (900 + i * 18) * S],
              200, 330, fill=(*accent, 28 + i * 12), width=2 * S)
    # player
    draw_player(img, 420, 790, cfg.get("scale", 1.9), accent, cfg.get("pose", "loop"), 1)
    # ball
    bx, by = cfg.get("ball", (770, 510))
    d.ellipse([(bx - 18) * S, (by - 18) * S, (bx + 18) * S, (by + 18) * S], fill=(255, 250, 240, 245))
    d.ellipse([(bx - 6) * S, (by - 10) * S, (bx + 2) * S, (by - 2) * S], fill=(255, 255, 255, 255))
    return add_grain(img, 5)


def jersey_poster(cfg):
    img = base_poster(cfg["top"], cfg["bottom"], cfg["accent"], "JERSEY", cfg["no"], cfg["year"])
    d = ImageDraw.Draw(img, "RGBA")
    accent = cfg["accent"]
    # jersey mask / gradient
    cx, cy = 540, 700
    body = [
        (390, 450), (455, 420), (505, 400), (540, 455), (575, 400), (625, 420), (690, 450),
        (735, 540), (680, 610), (655, 590), (660, 1030), (420, 1030), (425, 590), (400, 610), (345, 540)
    ]
    mask = Image.new("L", (W * S, H * S), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(x * S, y * S) for x, y in body], fill=255)
    # fabric gradient
    fabric = vgrad(W * S, H * S, [(0, cfg["fabric_top"]), (0.5, cfg["fabric_mid"]), (1, cfg["fabric_bottom"])])
    img.paste(fabric, (0, 0), mask)
    d = ImageDraw.Draw(img, "RGBA")
    # folds / shading
    for x, alpha in [(470, 28), (520, 18), (600, 24), (640, 30)]:
        d.line([(x * S, 480 * S), ((x - 15) * S, 1000 * S)], fill=(0, 0, 0, alpha), width=2 * S)
    for x, alpha in [(430, 24), (660, 20)]:
        d.line([(x * S, 520 * S), ((x + 12) * S, 980 * S)], fill=(255, 255, 255, alpha), width=2 * S)
    # outline
    d.line([(x * S, y * S) for x, y in body] + [(body[0][0] * S, body[0][1] * S)],
           fill=(*accent, 180), width=2 * S, joint="curve")
    # collar
    d.polygon([(500, 405), (540, 470), (580, 405), (560, 390), (540, 430), (520, 390)], fill=(*cfg["trim"], 255))
    # sleeves trim
    d.line([(390, 450), (345, 540)], fill=(*cfg["trim"], 230), width=7 * S)
    d.line([(690, 450), (735, 540)], fill=(*cfg["trim"], 230), width=7 * S)
    # side panels
    d.polygon([(425, 590), (450, 580), (455, 1000), (420, 1030)], fill=(*cfg["trim"], 28))
    d.polygon([(655, 590), (630, 580), (625, 1000), (660, 1030)], fill=(*cfg["trim"], 28))
    # crest / text
    d.ellipse([(500 * S), (535 * S), (580 * S), (615 * S)], outline=(*cfg["trim"], 190), width=2 * S)
    text(d, (540, 575), "CHN", 18, (*cfg["trim"], 230), FONT_DISPLAY_B, "mm", 2.0)
    text(d, (540, 705), "FAN", 90, (255, 255, 255, 238), FONT_DISPLAY_B, "mm", 3.0)
    text(d, (540, 790), "ZHENDONG", 17, (*cfg["trim"], 230), FONT_DISPLAY_B, "mm", 4.0)
    return add_grain(img, 5)


def paddle_poster(cfg):
    img = base_poster(cfg["top"], cfg["bottom"], cfg["accent"], "BLADE", cfg["no"], cfg["year"])
    d = ImageDraw.Draw(img, "RGBA")
    accent = cfg["accent"]
    # trajectory / ball
    d.arc([(500) * S, (260) * S, (960) * S, (720) * S], 190, 320, fill=(*accent, 60), width=2 * S)
    draw_paddle_shape(d, (540 * S, 660 * S), 300 * S, 390 * S, cfg["blade"], cfg["rubber"], accent, "FZD", angle=-12)
    # ball
    bx, by = 820, 400
    d.ellipse([(bx - 20) * S, (by - 20) * S, (bx + 20) * S, (by + 20) * S], fill=(255, 250, 240, 245))
    d.ellipse([(bx - 8) * S, (by - 12) * S, (bx + 2) * S, (by - 2) * S], fill=(255, 255, 255, 255))
    return add_grain(img, 5)


def career_still(cfg):
    img = base_poster(cfg["top"], cfg["bottom"], cfg["accent"], "CAREER", cfg["no"], cfg["year"])
    d = ImageDraw.Draw(img, "RGBA")
    accent = cfg["accent"]
    # table top and warm pool of light
    d.polygon([(0, 1150 * S), (1080 * S, 1040 * S), (1080 * S, 1440 * S), (0, 1440 * S)], fill=(12, 12, 14, 235))
    d.line([(0, 1150 * S), (1080 * S, 1040 * S)], fill=(*accent, 120), width=2 * S)
    glow = radial_glow((W * S, H * S), (540 * S, 880 * S), 430 * S, accent, 45)
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img, "RGBA")
    # paddle lying on table, slightly tilted
    draw_paddle_shape(d, (535 * S, 820 * S), 290 * S, 390 * S, (176, 122, 78, 255), (148, 30, 36, 255), accent, "FZD", angle=10)
    # ball
    bx, by = 790, 500
    d.ellipse([(bx - 20) * S, (by - 20) * S, (bx + 20) * S, (by + 20) * S], fill=(255, 250, 240, 245))
    d.ellipse([(bx - 7) * S, (by - 12) * S, (bx + 3) * S, (by - 2) * S], fill=(255, 255, 255, 255))
    return add_grain(img, 5)


def icon_assets():
    # App icon: dark glass background, gold orbit, table tennis ball, FZD monogram
    size = 1024
    img = Image.new("RGBA", (size, size), (7, 10, 18, 255))
    d = ImageDraw.Draw(img, "RGBA")
    # gradient
    g = vgrad(size, size, [(0, (8, 12, 22)), (0.55, (20, 28, 48)), (1, (6, 8, 14))])
    img.alpha_composite(g)
    # glows
    img.alpha_composite(radial_glow((size, size), (700, 300), 420, (231, 183, 104), 80))
    img.alpha_composite(radial_glow((size, size), (260, 760), 360, (91, 141, 239), 45))
    d = ImageDraw.Draw(img, "RGBA")
    # orbit
    for r, a in [(320, 90), (380, 35)]:
        d.arc([(512 - r), (512 - r), (512 + r), (512 + r)], 200, 410, fill=(231, 183, 104, a), width=3)
    # ball
    d.ellipse([(650, 240), (810, 400)], fill=(255, 250, 240, 245))
    d.ellipse([(686, 262), (724, 300)], fill=(255, 255, 255, 255))
    # monogram FZD
    text(d, (512, 560), "FZD", 238, (255, 255, 255, 242), FONT_DISPLAY_B, "mm", 4.0)
    text(d, (512, 760), "MEMORY  /  1997", 28, (231, 183, 104, 220), FONT_DISPLAY_B, "mm", 5.0)
    img.save(os.path.join(OUT, "app_icon.png"))
    # layered background/foreground: background is the full art; foreground transparent ball+monogram
    fg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fg, "RGBA")
    fd.ellipse([(650, 240), (810, 400)], fill=(255, 250, 240, 245))
    text(fd, (512, 560), "FZD", 238, (255, 255, 255, 242), FONT_DISPLAY_B, "mm", 4.0)
    text(fd, (512, 760), "MEMORY", 26, (231, 183, 104, 220), FONT_DISPLAY_B, "mm", 5.0)
    bg = Image.new("RGBA", (size, size), (8, 11, 20, 255))
    bg.alpha_composite(radial_glow((size, size), (700, 300), 500, (231, 183, 104), 55))
    bg.save(os.path.join(OUT, "icon_background.png"))
    fg.save(os.path.join(OUT, "icon_foreground.png"))
    img.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT, "startIcon.png"))
    for s in (192, 512):
        img.resize((s, s), Image.LANCZOS).save(os.path.join(WEB, f"icon-{s}.png"))


CAREER = [
    dict(id="career_2002", year="2002", no="01", cn="第一块球拍", en="THE FIRST GRIP", accent=(231, 183, 104), top=(9, 14, 26), bottom=(20, 25, 40),
         pose="child", scale=1.15, ball=(300, 430), cn_short="5岁 · 广州海珠区少年宫"),
    dict(id="career_2008", year="2008", no="02", cn="八一队", en="BAYI TEAM", accent=(93, 145, 239), top=(8, 13, 24), bottom=(18, 30, 52),
         pose="loop", scale=1.55, ball=(810, 420), cn_short="11岁 · 入选八一队"),
    dict(id="career_2012", year="2012", no="03", cn="国家队", en="NATIONAL TEAM", accent=(231, 183, 104), top=(10, 12, 22), bottom=(33, 28, 26),
         pose="serve", scale=1.7, ball=(700, 360), cn_short="15岁 · 进入国家二队"),
    dict(id="career_2016", year="2016", no="04", cn="世界杯首冠", en="FIRST WORLD CUP", accent=(210, 74, 78), top=(18, 8, 12), bottom=(42, 22, 25),
         pose="cheer", scale=1.8, ball=(760, 350), cn_short="19岁 · 萨尔布吕肯", line="career"),
    dict(id="career_2021", year="2021", no="05", cn="东京周期", en="TOKYO", accent=(231, 183, 104), top=(8, 12, 22), bottom=(22, 28, 42),
         pose="loop", scale=1.85, ball=(820, 430), cn_short="男团金牌 · 男单银牌", line="career"),
    dict(id="career_2022", year="2022", no="06", cn="成都世乒赛", en="CHENGDU 2022", accent=(231, 183, 104), top=(8, 10, 18), bottom=(20, 22, 30),
         pose="loop", scale=1.8, ball=(800, 380), cn_short="男团冠军 · 主场作战", line="career"),
    dict(id="career_2023", year="2023", no="07", cn="德班封王", en="DURBAN 2023", accent=(93, 145, 239), top=(7, 12, 24), bottom=(14, 26, 44),
         pose="loop", scale=1.85, ball=(800, 380), cn_short="世乒赛男单冠军", line="career"),
    dict(id="career_2024", year="2024", no="08", cn="巴黎登顶", en="PARIS 2024", accent=(231, 183, 104), top=(15, 8, 12), bottom=(46, 22, 20),
         pose="cheer", scale=1.9, ball=(780, 330), cn_short="男单金牌 · 大满贯", line="career"),
    dict(id="career_2025", year="2025", no="09", cn="远行", en="A NEW COURT", accent=(143, 195, 255), top=(7, 13, 24), bottom=(12, 28, 48),
         pose="serve", scale=1.8, ball=(760, 350), cn_short="加盟萨尔布吕肯", line="career"),
    dict(id="career_2026", year="2026", no="10", cn="当下", en="STILL HERE", accent=(231, 183, 104), top=(8, 12, 20), bottom=(24, 24, 32),
         pose="cheer", scale=1.9, ball=(800, 340), cn_short="杜塞尔多夫 · 未完待续", line="career"),
]

JERSEY = [
    dict(id="jersey_2013", year="2013", no="01", cn="初登世界赛场", event="FIRST WORLD CHAMPIONSHIPS",
         accent=(231, 183, 104), top=(16, 8, 12), bottom=(40, 18, 22), fabric_top=(190, 42, 48), fabric_mid=(150, 26, 34), fabric_bottom=(102, 16, 24),
         trim=(243, 213, 154)),
    dict(id="jersey_2016", year="2016", no="02", cn="萨尔布吕肯", event="WORLD CUP  ·  SAARBRÜCKEN",
         accent=(244, 197, 66), top=(18, 8, 10), bottom=(48, 22, 16), fabric_top=(210, 45, 48), fabric_mid=(175, 28, 35), fabric_bottom=(120, 16, 24),
         trim=(244, 197, 66), line="jersey"),
    dict(id="jersey_2021", year="2021", no="03", cn="东京", event="TOKYO 2020  ·  TEAM CHINA",
         accent=(210, 74, 78), top=(14, 16, 24), bottom=(46, 20, 22), fabric_top=(248, 244, 235), fabric_mid=(228, 216, 200), fabric_bottom=(188, 172, 154),
         trim=(178, 30, 38)),
    dict(id="jersey_2022", year="2022", no="04", cn="黑色龙纹", event="CHENGDU 2022  ·  TEAM CHINA",
         accent=(231, 183, 104), top=(8, 8, 10), bottom=(24, 20, 20), fabric_top=(36, 32, 32), fabric_mid=(22, 20, 20), fabric_bottom=(10, 10, 12),
         trim=(231, 183, 104), line="jersey"),
    dict(id="jersey_2023", year="2023", no="05", cn="蓝色客场", event="DURBAN 2023  ·  TEAM CHINA",
         accent=(93, 145, 239), top=(6, 12, 24), bottom=(12, 26, 48), fabric_top=(28, 78, 142), fabric_mid=(18, 52, 104), fabric_bottom=(8, 26, 58),
         trim=(225, 238, 255), line="jersey"),
    dict(id="jersey_2024", year="2024", no="06", cn="巴黎", event="PARIS 2024  ·  GRAND SLAM",
         accent=(231, 183, 104), top=(12, 7, 10), bottom=(44, 12, 16), fabric_top=(116, 18, 28), fabric_mid=(78, 10, 18), fabric_bottom=(38, 6, 12),
         trim=(217, 164, 65), line="jersey"),
    dict(id="jersey_2025", year="2025", no="07", cn="萨尔布吕肯", event="SAARBRÜCKEN  ·  BUNDESLIGA",
         accent=(143, 195, 255), top=(7, 12, 22), bottom=(12, 28, 50), fabric_top=(28, 70, 122), fabric_mid=(16, 45, 84), fabric_bottom=(8, 24, 48),
         trim=(213, 228, 245)),
]

PADDLE = [
    dict(id="paddle_2008", year="2008", no="01", cn="启蒙纯木", en="ALL-WOOD  /  FIVE PLY",
         accent=(231, 183, 104), top=(15, 11, 8), bottom=(38, 25, 16), blade=(172, 118, 72), rubber=(150, 32, 36),
         spec="5-ply wood  ·  control first"),
    dict(id="paddle_2015", year="2015", no="02", cn="外置芳碳", en="ARYLATE CARBON  /  SPEED",
         accent=(217, 160, 102), top=(12, 10, 8), bottom=(35, 22, 14), blade=(196, 154, 108), rubber=(28, 28, 32),
         spec="outer ALC  ·  spin + speed"),
    dict(id="paddle_2021", year="2021", no="03", cn="樊振东 ALC", en="FAN ZHENDONG ALC",
         accent=(231, 183, 104), top=(10, 10, 12), bottom=(30, 18, 18), blade=(28, 28, 32), rubber=(166, 30, 38),
         spec="FH  Hurricane 3  ·  BH  Dignics 09C"),
    dict(id="paddle_2024", year="2024", no="04", cn="巴黎之刃", en="SUPER ALC  /  PARIS",
         accent=(231, 183, 104), top=(10, 8, 8), bottom=(34, 12, 14), blade=(20, 20, 24), rubber=(120, 12, 24),
         spec="FH  Hurricane 3 Blue  ·  BH  Dignics 09C"),
    dict(id="paddle_2026", year="2026", no="05", cn="杜塞尔多夫", en="DÜSSELDORF  /  NOW",
         accent=(143, 195, 255), top=(7, 12, 20), bottom=(12, 26, 44), blade=(18, 26, 42), rubber=(150, 28, 34),
         spec="FH  Hurricane 3 Blue  ·  BH  Dignics 09C"),
]


def main():
    random.seed(7)
    exec(open(os.path.join(BASE, "photo_poster_lib.py"), encoding="utf-8-sig").read(), globals())
    photo_map = {
        "career_2016": ("extra_3_c.jpg", (0.0, 0.0, 0.0, 0.05), (0.5, 0.35)),
        "career_2021": ("extra_1_c.jpg", (0.0, 0.0, 0.0, 0.12), (0.5, 0.35)),
        "career_2022": ("photo_3.jpg", (0.0, 0.02, 0.0, 0.02), (0.55, 0.28)),
        "career_2023": ("photo_4.jpg", (0.0, 0.0, 0.0, 0.08), (0.52, 0.35)),
        "career_2024": ("photo_6_conv.jpg", (0.0, 0.0, 0.0, 0.02), (0.52, 0.30)),
        "career_2025": ("extra_6.jpg", (0.0, 0.0, 0.0, 0.48), (0.5, 0.18)),
        "jersey_2016": ("extra_3_c.jpg", (0.0, 0.0, 0.0, 0.05), (0.5, 0.35)),
        "jersey_2022": ("photo_3.jpg", (0.0, 0.0, 0.0, 0.03), (0.55, 0.28)),
        "jersey_2023": ("photo_4.jpg", (0.0, 0.0, 0.0, 0.10), (0.52, 0.32)),
        "jersey_2024": ("photo_2.jpg", (0.0, 0.12, 0.0, 0.01), (0.5, 0.35)),
    }
    for cfg in CAREER:
        if cfg["id"] == "career_2002":
            img = career_still(cfg)
        elif cfg["id"] in photo_map:
            src, crop, focus = photo_map[cfg["id"]]
            img = photo_poster(os.path.join(BASE, "raw_assets", src), cfg, crop, focus)
        else:
            img = career_poster(cfg)
        img.resize((W, H), Image.LANCZOS).convert("RGB").save(os.path.join(OUT, cfg["id"] + ".jpg"), quality=88, optimize=True)
    for cfg in JERSEY:
        if cfg["id"] in photo_map:
            src, crop, focus = photo_map[cfg["id"]]
            img = photo_poster(os.path.join(BASE, "raw_assets", src), cfg, crop, focus)
        else:
            img = jersey_poster(cfg)
        img.resize((W, H), Image.LANCZOS).convert("RGB").save(os.path.join(OUT, cfg["id"] + ".jpg"), quality=88, optimize=True)
    for cfg in PADDLE:
        img = paddle_poster(cfg)
        img.resize((W, H), Image.LANCZOS).convert("RGB").save(os.path.join(OUT, cfg["id"] + ".jpg"), quality=88, optimize=True)
    icon_assets()
    # copy to web
    for cfg in CAREER + JERSEY + PADDLE:
        src = os.path.join(OUT, cfg["id"] + ".jpg")
        dst = os.path.join(WEB, cfg["id"] + ".jpg")
        Image.open(src).save(dst, quality=86, optimize=True)
    # covers
    for src_name, dst_name in [("career_2024.jpg", "cover.jpg"), ("career_2002.jpg", "cover_career.jpg"),
                               ("jersey_2024.jpg", "cover_jersey.jpg"), ("paddle_2024.jpg", "cover_paddle.jpg")]:
        Image.open(os.path.join(OUT, src_name)).save(os.path.join(WEB, dst_name), quality=88, optimize=True)
    print("generated", len(CAREER) + len(JERSEY) + len(PADDLE), "posters")


if __name__ == "__main__":
    main()





