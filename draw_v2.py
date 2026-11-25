#!/usr/bin/env python3
"""Draw the v2 entry image for make.fun news-image-20261124.

Dense one-page infographic, drawn with PIL at 2x then downscaled to 1024x1024.
All stories are 24 November 2026 events (verified against news sources).
Deterministic: no randomness, no timestamps in the image.
"""
import os
from PIL import Image, ImageDraw, ImageFont

S = 2  # render scale
W, H = 1024 * S, 1024 * S
M = 28 * S  # side margin

PAPER = (247, 242, 230)
INK = (23, 21, 16)
MUTED = (96, 90, 78)
FAINT = (150, 142, 122)
RED = (164, 30, 34)
DARKRED = (120, 20, 24)
BLUE = (31, 78, 121)
TEAL = (14, 107, 107)
PURPLE = (91, 58, 140)
ORANGE = (184, 92, 0)
GREEN = (46, 107, 52)
BROWN = (122, 90, 46)
GOLD = (176, 141, 58)
LINEC = (196, 186, 160)
PARCH = (233, 224, 200)

FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
]


def font_path(*names):
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    raise FileNotFoundError(names)


SERIF_B = font_path("LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf")
SERIF = font_path("LiberationSerif-Regular.ttf", "DejaVuSerif.ttf")
SERIF_I = font_path("LiberationSerif-Italic.ttf", "DejaVuSerif-Italic.ttf")
SANS_B = font_path("LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf")
SANS = font_path("LiberationSans-Regular.ttf", "DejaVuSans.ttf")


def F(path, size):
    return ImageFont.truetype(path, int(round(size * S)))


def wrap(d, text, font, max_w):
    """Word-wrap text to fit max_w (in render px). Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def hline(d, x0, x1, y, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=int(round(width * S)))


def vline(d, x, y0, y1, fill=LINEC, width=1):
    d.line([(x, y0), (x, y1)], fill=fill, width=int(round(width * S)))


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- top bar
f_top = F(SANS_B, 10.5)
y = 13 * S
text(d, M, y, "THE WORLD IN ONE DAY", f_top)
text(d, W // 2, y, "DAY 328 OF 2026", f_top, fill=RED, anchor="ma")
text(d, W - M, y, "TUESDAY 24 NOV", f_top, anchor="ra")
hline(d, M, W - M, 30 * S, width=1.2)

# ---------------------------------------------------------------- masthead
f_mast = F(SERIF_B, 56)
text(d, W // 2, 36 * S, "Tuesday 24 November 2026", f_mast, anchor="ma")
hline(d, M, W - M, 96 * S, width=1)
f_sub = F(SANS_B, 12)
text(d, W // 2, 100 * S, "29 STORIES  \u00b7  7 REGIONS  \u00b7  EVERY ONE DATED TUESDAY 24 NOVEMBER 2026",
     f_sub, anchor="ma")
hline(d, M, W - M, 117 * S, width=2.2)

# ---------------------------------------------------------------- stat strip
stats = [
    ("699", "Ukrainian drones\nRussia says it downed"),
    ("6,500+", "Rohingya Malaysia\nwill return"),
    ("$41bn", "Sanofi's cash deal\nfor Insmed"),
    ("350k", "EU yearly cap on\nChinese hybrids"),
    ("+7%", "Kospi rebound\non chip stocks"),
]
f_stat_n = F(SERIF_B, 27)
f_stat_l = F(SANS, 9)
col_w = (W - 2 * M) // 5
for i, (num, lab) in enumerate(stats):
    x0 = M + i * col_w
    cx = x0 + col_w // 2
    text(d, cx, 122 * S, num, f_stat_n, fill=RED if i == 0 else INK, anchor="ma")
    for j, ln in enumerate(lab.split("\n")):
        text(d, cx, (148 + j * 11) * S, ln, f_stat_l, fill=MUTED, anchor="ma")
    if i:
        vline(d, x0, 124 * S, 168 * S)
hline(d, M, W - M, 172 * S, width=1)

# ---------------------------------------------------------------- hero illustrations
def hero_drones(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=PARCH, outline=INK, width=max(1, S // 2))
    w, h = x1 - x0, y1 - y0
    # land polygons (schematic Ukraine / Poland / Russia)
    poland = [(0.02, 0.28), (0.20, 0.20), (0.28, 0.40), (0.22, 0.60), (0.04, 0.62)]
    ukraine = [(0.28, 0.40), (0.50, 0.32), (0.60, 0.50), (0.52, 0.70), (0.32, 0.72), (0.22, 0.60)]
    russia = [(0.50, 0.06), (0.98, 0.06), (0.98, 0.70), (0.60, 0.50), (0.50, 0.32)]
    for poly, fill in ((poland, (222, 214, 188)), (ukraine, (233, 220, 150)),
                       (russia, (214, 206, 184))):
        d.polygon([(x0 + px * w, y0 + py * h) for px, py in poly], fill=fill,
                  outline=(170, 160, 130))
    # Black Sea
    d.ellipse([x0 + 0.46 * w, y0 + 0.78 * h, x0 + 0.66 * w, y0 + 0.98 * h],
              fill=(120, 165, 195))
    f_lab = F(SANS_B, 8)
    text(d, x0 + 0.08 * w, y0 + 0.45 * h, "POLAND", f_lab, fill=MUTED)
    text(d, x0 + 0.30 * w, y0 + 0.62 * h, "UKRAINE", f_lab, fill=MUTED)
    text(d, x0 + 0.76 * w, y0 + 0.52 * h, "RUSSIA", f_lab, fill=MUTED)
    # drones: small dark diamonds with red trails, heading for Moscow
    mx, my = x0 + 0.74 * w, y0 + 0.30 * h
    drones = [(0.32, 0.50), (0.40, 0.44), (0.48, 0.56), (0.54, 0.42),
              (0.58, 0.52), (0.44, 0.64), (0.62, 0.40), (0.50, 0.62)]
    for px, py in drones:
        dx, dy = x0 + px * w, y0 + py * h
        d.line([(dx, dy), (dx + (mx - dx) * 0.14, dy + (my - dy) * 0.14)],
               fill=RED, width=max(1, S // 2))
        r = 2.2 * S
        d.polygon([(dx, dy - r), (dx + r, dy), (dx, dy + r), (dx - r, dy)], fill=INK)
    # Moscow
    d.ellipse([mx - 4 * S, my - 4 * S, mx + 4 * S, my + 4 * S], fill=RED)
    text(d, mx - 6 * S, my - 5 * S, "MOSCOW", F(SANS_B, 8.5), fill=DARKRED,
         anchor="ra")
    # 699 badge (bottom-right, over the sea)
    bx, by = x1 - 62 * S, y1 - 32 * S
    d.rectangle([bx, by, bx + 56 * S, by + 26 * S], fill=RED)
    text(d, bx + 28 * S, by + 2 * S, "699", F(SERIF_B, 17), fill=(255, 255, 255),
         anchor="ma")
    text(d, bx + 56 * S, by - 9 * S, "DRONES DOWNED", F(SANS_B, 6.5), fill=DARKRED,
         anchor="ra")
    # AWACS glyph over Poland
    ax, ay = x0 + 0.14 * w, y0 + 0.14 * h
    d.polygon([(ax, ay - 3 * S), (ax + 10 * S, ay + 3 * S), (ax - 10 * S, ay + 3 * S)],
              fill=(255, 255, 255), outline=BLUE)
    text(d, ax - 12 * S, ay + 5 * S, "NATO AWACS", F(SANS_B, 7), fill=BLUE)


def hero_hormuz(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(207, 224, 234), outline=INK, width=max(1, S // 2))
    w, h = x1 - x0, y1 - y0
    horizon = y0 + 0.42 * h
    d.rectangle([x0, horizon, x1, y1], fill=(46, 111, 142))
    f_lab = F(SANS_B, 8.5)
    text(d, x0 + 8 * S, y0 + 6 * S, "STRAIT OF HORMUZ", f_lab, fill=(40, 70, 95))
    # dashed shipping lane
    for i in range(14):
        sx = x0 + (0.04 + i * 0.068) * w
        d.line([(sx, horizon + 0.55 * (y1 - horizon)),
                (sx + 0.035 * w, horizon + 0.55 * (y1 - horizon))],
               fill=(255, 255, 255, 160), width=max(1, S // 2))
    # tankers
    def tanker(cx, cy, scale, burning):
        hw, hh = 46 * S * scale, 13 * S * scale
        d.rectangle([cx - hw, cy - hh, cx + hw, cy + hh], fill=(30, 34, 40))
        d.rectangle([cx + hw * 0.55, cy - hh - 9 * S * scale,
                     cx + hw * 0.85, cy - hh], fill=(200, 60, 50))
        d.rectangle([cx - hw * 0.85, cy - hh - 5 * S * scale,
                     cx - hw * 0.55, cy - hh], fill=(230, 225, 210))
        if burning:
            bx, by = cx - hw * 0.4, cy - hh - 8 * S * scale
            for ang, ln in ((0, 10), (45, 7), (90, 12), (135, 7), (180, 10),
                            (225, 7), (270, 12), (315, 7)):
                import math
                ex = bx + ln * S * scale * math.cos(math.radians(ang))
                ey = by - ln * S * scale * math.sin(math.radians(ang))
                d.line([(bx, by), (ex, ey)], fill=(255, 150, 30), width=2 * S)
            d.ellipse([bx - 3 * S, by - 3 * S, bx + 3 * S, by + 3 * S],
                      fill=(255, 200, 60))
    tanker(x0 + 0.26 * w, horizon + 0.30 * (y1 - horizon), 0.9, True)
    tanker(x0 + 0.60 * w, horizon + 0.62 * (y1 - horizon), 1.1, True)
    tanker(x0 + 0.86 * w, horizon + 0.28 * (y1 - horizon), 0.7, False)
    # mine markers
    for mx, my in ((0.44, 0.62), (0.72, 0.80)):
        px, py = x0 + mx * w, horizon + my * (y1 - horizon)
        d.ellipse([px - 3 * S, py - 3 * S, px + 3 * S, py + 3 * S],
                  fill=INK, outline=(255, 255, 255))
    text(d, x0 + 8 * S, y1 - 14 * S, "TANKERS HIT MINES", F(SANS_B, 8.5),
         fill=(255, 255, 255))


def hero_sanofi(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(238, 242, 240), outline=INK, width=max(1, S // 2))
    w, h = x1 - x0, y1 - y0
    # shelf + flasks
    d.rectangle([x0 + 0.06 * w, y0 + 0.52 * h, x0 + 0.60 * w, y0 + 0.56 * h],
                fill=(120, 120, 115))
    flask_cols = [(14, 140, 140), (220, 120, 40), (60, 100, 180)]
    for i, fc in enumerate(flask_cols):
        fx = x0 + (0.12 + i * 0.16) * w
        fw, fh = 16 * S, 22 * S
        d.rectangle([fx - 2 * S, y0 + 0.52 * h - fh - 8 * S, fx + 2 * S,
                     y0 + 0.52 * h - fh], fill=(200, 205, 200))
        d.rectangle([fx - fw // 2, y0 + 0.52 * h - fh, fx + fw // 2, y0 + 0.52 * h],
                    fill=fc, outline=INK)
    # bench
    d.rectangle([x0, y0 + 0.78 * h, x1, y1], fill=(205, 200, 185))
    # big capsule (rotated): draw as two half-rounded rects via polygon + circles
    cx, cy = x0 + 0.74 * w, y0 + 0.42 * h
    cap_w, cap_h = 52 * S, 20 * S
    d.rounded_rectangle([cx - cap_w, cy - cap_h, cx + cap_w, cy + cap_h],
                        radius=cap_h, fill=(255, 255, 255), outline=INK,
                        width=max(1, S // 2))
    d.rounded_rectangle([cx - cap_w, cy - cap_h, cx, cy + cap_h],
                        radius=cap_h, fill=RED)
    d.rectangle([cx - cap_h, cy - cap_h, cx, cy + cap_h], fill=RED)
    d.rounded_rectangle([cx - cap_w, cy - cap_h, cx + cap_w, cy + cap_h],
                        radius=cap_h, outline=INK, width=max(1, S // 2))
    text(d, cx, cy + cap_h + 8 * S, "LUNG DRUGS", F(SANS_B, 8), fill=MUTED,
         anchor="ma")
    # molecule dots
    for mx, my, mr in ((0.06, 0.32, 4), (0.12, 0.26, 3), (0.03, 0.26, 3)):
        d.ellipse([x0 + mx * w - mr * S, y0 + my * h - mr * S,
                   x0 + mx * w + mr * S, y0 + my * h + mr * S], fill=TEAL)
    # $41bn tag
    tx, ty = x1 - 66 * S, y0 + 6 * S
    d.rectangle([tx, ty, tx + 60 * S, ty + 24 * S], fill=BLUE)
    text(d, tx + 30 * S, ty + 2 * S, "$41bn", F(SERIF_B, 15), fill=(255, 255, 255),
         anchor="ma")
    text(d, x0 + 8 * S, y0 + 6 * S, "PARIS \u00b7 BIGGEST PHARMA DEAL OF 2026",
         F(SANS_B, 8), fill=MUTED)


# ---------------------------------------------------------------- hero row
heroes = [
    (1, "EUROPE \u00b7 WAR", BLUE, hero_drones,
     "Drone war: 699 downed, Poland on alert",
     "Russia says it shot down 699 Ukrainian drones overnight, 355 of them headed "
     "for Moscow. Warsaw will summon the ambassador; NATO sends an AWACS to Poland.",
     "AFP \u00b7 REUTERS"),
    (2, "MIDDLE EAST \u00b7 SHIPPING", DARKRED, hero_hormuz,
     "Iran: tankers hit mines in Hormuz",
     "Iran's Guards say tankers caught fire after hitting mines in the Strait of "
     "Hormuz; Brent holds near $69. Washington has not confirmed the claim.",
     "IRGC VIA IRNA \u00b7 REUTERS"),
    (3, "BUSINESS \u00b7 PHARMA", TEAL, hero_sanofi,
     "Sanofi buys Insmed for $41bn",
     "France's Sanofi agrees its biggest deal in years, paying $175 a share in cash "
     "for the US biotech's lung drugs \u2014 the year's largest pharma deal.",
     "SANOFI \u00b7 WSJ"),
]
f_hkick = F(SANS_B, 10)
f_hhead = F(SERIF_B, 20)
f_hbody = F(SANS, 10.5)
f_hsrc = F(SANS_B, 8)
gap = 12 * S
hero_w = (W - 2 * M - 2 * gap) // 3
hero_y = 178 * S
ILL_H = 108 * S
for i, (num, kicker, kc, ill, head, body, src) in enumerate(heroes):
    x0 = M + i * (hero_w + gap)
    x1 = x0 + hero_w
    ill((x0, hero_y, x1, hero_y + ILL_H))
    ky = hero_y + ILL_H + 8 * S
    d.rectangle([x0, ky, x0 + 16 * S, ky + 13 * S], fill=kc)
    text(d, x0 + 8 * S, ky - 1 * S, str(num), F(SANS_B, 9.5),
         fill=(255, 255, 255), anchor="ma")
    text(d, x0 + 21 * S, ky, kicker, f_hkick, fill=kc)
    hy = ky + 17 * S
    for j, ln in enumerate(wrap(d, head, f_hhead, hero_w)):
        text(d, x0, hy + j * 22 * S, ln, f_hhead)
    by = hy + len(wrap(d, head, f_hhead, hero_w)) * 22 * S + 4 * S
    for j, ln in enumerate(wrap(d, body, f_hbody, hero_w)):
        text(d, x0, by + j * 13 * S, ln, f_hbody, fill=(50, 48, 42))
    sy = by + len(wrap(d, body, f_hbody, hero_w)) * 13 * S + 3 * S
    text(d, x0, sy, src, f_hsrc, fill=MUTED)
hline(d, M, W - M, 412 * S, width=1)


# ---------------------------------------------------------------- grid (12 stories)
grid = [
    (4, "MIDDLE EAST \u00b7 OIL", DARKRED, "4", "PROVINCES",
     "Baghdad seizes Kurdish-held oilfields",
     "PM al-Zaidi puts fields in Kirkuk, Diyala, Salahuddin and Nineveh under "
     "Baghdad. Erbil calls it unacceptable.",
     "AL JAZEERA \u00b7 REUTERS"),
    (5, "ASIA \u00b7 REFUGEES", PURPLE, "6,500+", "TO RETURN",
     "Malaysia to send 6,500 Rohingya back",
     "Anwar tells parliament over 6,500 will be returned, 1,500 by navy ship "
     "in Dec, 5,303 by air.",
     "AL JAZEERA"),
    (6, "EUROPE \u00b7 TRADE", BLUE, "350k", "A YEAR",
     "EU caps Chinese hybrid cars",
     "Import quotas adopted: 350,000 a year for China from 1 Dec.",
     "EU"),
    (7, "ASIA \u00b7 MARKETS", ORANGE, "+7%", "KOSPI",
     "Chip stocks lift Asia",
     "Kospi up about 7%, Nikkei about 4%; Hang Seng slips.",
     "KOSPI"),
    (8, "MIDDLE EAST \u00b7 WAR", DARKRED, "7", "KILLED",
     "Strikes kill 7; meningitis warning",
     "Israeli strikes hit Khan Younis and near Netzarim as doctors warn of an "
     "outbreak.",
     "MEDICS"),
    (9, "ASIA \u00b7 DISASTER", PURPLE, "6", "DEAD",
     "Restaurant gas blast kills six",
     "Explosion in Dong Da district at about 8am; 10 injured.",
     "HANOI"),
    (10, "ASIA \u00b7 POLITICS", ORANGE, "16 Dec", "PLANNED RETURN",
     "Hasina says she will fly home 16 Dec",
     "Sentenced to death in absentia; Dhaka says only on extradition.",
     "DHAKA"),
    (11, "OCEANIA \u00b7 SECURITY", TEAL, "2022", "PACT ENDS",
     "Solomons swaps China pact for Australia",
     "PM Wale arrives to sign a treaty; Honiara ends its 2022 China security deal.",
     "CANBERRA"),
    (12, "AMERICAS \u00b7 JUSTICE", GREEN, "NO", "EXTRADITION",
     "Mexico to try \u201cEl Chapo Isidro\u201d at home",
     "It turns down the US extradition request for the captured cartel boss.",
     "MEXICO CITY"),
    (13, "ASIA \u00b7 SECURITY", BLUE, "3 MIN", "SHELTER ALERT",
     "Russian jets enter Korea's ADIZ",
     "Seoul scrambles jets; a Russian jet sent Ulleung island into a 3-minute "
     "shelter alert.",
     "SEOUL"),
    (14, "ASIA \u00b7 QUAKE", BROWN, "M5.6", "NO CASUALTIES",
     "Quake shakes Taplejung, no casualties",
     "A 5.6-magnitude quake shook eastern Nepal.",
     "NEMRC"),
    (15, "OCEANIA \u00b7 INDEPENDENCE", TEAL, "97.7%", "SAID YES IN 2019",
     "Bougainville votes on nationhood",
     "PNG's parliament began voting on the 2019 referendum result \u2014 97.7% chose "
     "independence.",
     "PORT MORESBY"),
]
f_gkick = F(SANS_B, 8.5)
f_gstat = F(SERIF_B, 19)
f_gstat_sm = F(SERIF_B, 16.5)
f_gstatl = F(SANS_B, 6.5)
f_ghead = F(SERIF_B, 13.5)
f_gbody = F(SANS, 9.5)
f_gsrc = F(SANS_B, 7.5)
GRID_Y = 418 * S
GRID_H = 102 * S
GRID_GAP = 5 * S
grid_w = (W - 2 * M - 3 * gap) // 4
for idx, (num, kicker, kc, stat, statl, head, body, src) in enumerate(grid):
    r, c = divmod(idx, 4)
    x0 = M + c * (grid_w + gap)
    y0 = GRID_Y + r * (GRID_H + GRID_GAP)
    x1 = x0 + grid_w
    d.line([(x0, y0), (x1, y0)], fill=kc, width=3 * S)
    ky = y0 + 5 * S
    d.rectangle([x0, ky, x0 + 13 * S, ky + 11 * S], fill=kc)
    text(d, x0 + 6.5 * S, ky - 1 * S, str(num), F(SANS_B, 8),
         fill=(255, 255, 255), anchor="ma")
    text(d, x0 + 17 * S, ky, kicker, f_gkick, fill=kc)
    # stat block (left) + headline/body (right)
    sw = 60 * S
    fs = f_gstat_sm if len(stat) > 5 else f_gstat
    text(d, x0, ky + 15 * S, stat, fs, fill=INK)
    for j, ln in enumerate(wrap(d, statl, f_gstatl, sw)[:2]):
        text(d, x0, ky + 36 * S + j * 8 * S, ln, f_gstatl, fill=MUTED)
    tx = x0 + sw + 4 * S
    tw = x1 - tx
    hl = wrap(d, head, f_ghead, tw)
    for j, ln in enumerate(hl):
        text(d, tx, ky + 15 * S + j * 16 * S, ln, f_ghead)
    by = ky + 15 * S + len(hl) * 16 * S + 2 * S
    bl = wrap(d, body, f_gbody, tw)
    for j, ln in enumerate(bl[:3]):
        text(d, tx, by + j * 11.5 * S, ln, f_gbody, fill=(50, 48, 42))
    text(d, tx, by + min(len(bl), 3) * 11.5 * S + 2 * S, src, f_gsrc, fill=MUTED)
hline(d, M, W - M, 738 * S, width=1)

# ---------------------------------------------------------------- world map (dotted)
MAP_Y = 742 * S
f_sect = F(SANS_B, 11)
text(d, M, MAP_Y, "WHERE IT HAPPENED", f_sect)
text(d, M + 150 * S, MAP_Y, "pins carry the story numbers", F(SANS, 9.5),
     fill=MUTED)
map_x0, map_y0 = M, MAP_Y + 16 * S
map_w, map_h = W - 2 * M, 104 * S
# land mask: 20 rows x 90 cols, intervals per row (col = (lon+180)/4)
LAND = [
    [(4, 21), (30, 40), (52, 89)],
    [(3, 30), (31, 41), (48, 89)],
    [(10, 28), (43, 45), (46, 89)],
    [(12, 30), (43, 89)],
    [(13, 27), (42, 52), (56, 78), (80, 81)],
    [(14, 26), (42, 80)],
    [(15, 24), (42, 60), (62, 75)],
    [(17, 23), (40, 59), (62, 72)],
    [(18, 24), (40, 55), (63, 65), (68, 72), (75, 75)],
    [(22, 32), (40, 57), (69, 74)],
    [(25, 36), (47, 57), (68, 82)],
    [(24, 36), (47, 55), (71, 79)],
    [(25, 36), (48, 55), (73, 80)],
    [(27, 36), (48, 54), (56, 57), (73, 81)],
    [(27, 35), (49, 53), (73, 83)],
    [(27, 32), (49, 52), (73, 82), (88, 89)],
    [(26, 30), (80, 82), (86, 89)],
    [(26, 28), (86, 88)],
    [(26, 28)],
    [],
]
cell_w, cell_h = map_w / 90, map_h / 20
dot_r = 2.1 * S
for r, intervals in enumerate(LAND):
    cy = map_y0 + (r + 0.5) * cell_h
    for a, b in intervals:
        for c in range(a, b + 1):
            cx = map_x0 + (c + 0.5) * cell_w
            d.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r],
                      fill=(182, 162, 118))
# pins: (story number, lon, lat, dx, dy nudge in px@1024)
PINS = [
    (1, 28, 50, 0, 0), (2, 56, 26, 0, 0), (3, 2, 49, 0, 0), (4, 44, 33, 0, 0),
    (5, 102, 3, 0, 0), (6, 4, 51, -12, -10), (7, 127, 37, 0, 0), (8, 34, 31, 0, 0),
    (9, 106, 21, 0, 0), (10, 90, 24, 6, -8), (11, 160, -9, 0, 0),
    (12, -99, 19, 0, 0), (13, 131, 37, 10, 8), (14, 85, 28, -12, 8),
    (15, 155, -6, 0, 0),
]
f_pin = F(SANS_B, 7)
for num, lon, lat, dx, dy in PINS:
    px = map_x0 + (lon + 180) / 360 * map_w + dx * S
    py = map_y0 + (71 - lat) / 130 * map_h + dy * S
    pr = 5.5 * S
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=RED,
              outline=(255, 255, 255), width=max(1, S // 2))
    text(d, px, py - pr + 1 * S, str(num), f_pin, fill=(255, 255, 255),
         anchor="ma")
hline(d, M, W - M, 866 * S, width=1)

# ---------------------------------------------------------------- also list
ALSO_Y = 870 * S
d.rectangle([M, ALSO_Y, W - M, ALSO_Y + 14 * S], fill=INK)
text(d, M + 5 * S, ALSO_Y + 1 * S, "ALSO ON TUESDAY 24 NOV", F(SANS_B, 10),
     fill=(255, 255, 255))
also = [
    (16, "UN: 47,000 women killed by partners in 2025", "UNODC / UN WOMEN"),
    (17, "China sentences ex-official to death for spying", "BEIJING"),
    (18, "Banten factory-fire toll rises to 26", "XINHUA / AP"),
    (19, "Car bomb hits governor's office in Villavicencio; 23 hurt", "EL TIEMPO / AFP"),
    (20, "Indonesia names two VP candidates", "PRESIDENTIAL PALACE"),
    (21, "World chess title match opens in Geneva", "FIDE"),
    (22, "UN debates AI and the future of war", "NEW YORK"),
    (23, "CAS restores Senegal as AFCON champions", "LAUSANNE"),
    (24, "Russian strike on Zaporizhzhia kills 2, wounds 40", "KYIV"),
    (25, "Odesa left without power, heat or water after strikes", "ODESA"),
    (26, "Delta system failure grounds 3,000+ flights", "ATLANTA"),
    (27, "Vanuatu hit by 6.5 quake; no tsunami warning", "PORT VILA"),
    (28, "UN urges probe into Benghazi port strike", "UNSMIL"),
    (29, "TAIEX jumps 8.99% on chip rally", "TAIPEI"),
]
f_also = F(SANS, 9)
f_also_b = F(SANS_B, 9)
f_also_s = F(SANS, 8)
col2_w = (W - 2 * M) // 2
for i, (num, head, src) in enumerate(also):
    col = 0 if i % 2 == 0 else 1
    row = i // 2
    x0 = M + col * col2_w
    y = ALSO_Y + 17 * S + row * 9 * S
    text(d, x0, y, f"{num}", f_also_b, fill=RED)
    nx = x0 + d.textlength(f"{num}  ", font=f_also_b)
    avail = col2_w - (nx - x0) - 4 * S
    # shrink headline if needed to fit one line
    hl = head
    while d.textlength(hl + "  \u2014 " + src, font=f_also) > avail and len(hl) > 20:
        hl = hl[:-1].rstrip(" ,;")
    text(d, nx, y, hl, f_also)
    sx = nx + d.textlength(hl + "  ", font=f_also)
    text(d, sx, y, "\u2014 " + src, f_also_s, fill=MUTED)

# ---------------------------------------------------------------- date check + footer
DC_Y = 958 * S
hline(d, M, W - M, DC_Y, width=1)
d.rectangle([M, DC_Y + 4 * S, M + 74 * S, DC_Y + 17 * S], fill=RED)
text(d, M + 5 * S, DC_Y + 5 * S, "DATE CHECK", F(SANS_B, 9.5),
     fill=(255, 255, 255))
dc = ("Left out on purpose \u2014 other days' news: COP31 collapse (Sun 22 Nov) \u00b7 "
      "Huang returns to Nvidia (Mon 23 Nov) \u00b7 ICJ Myanmar genocide ruling "
      "(Thu 19 Nov) \u00b7 Grok image lawsuits (Mon 23 Nov) \u00b7 EU 22nd Russia "
      "sanctions (Mon 23 Nov)")
f_dc = F(SANS, 9)
for j, ln in enumerate(wrap(d, dc, f_dc, W - 2 * M - 80 * S)):
    text(d, M + 80 * S, DC_Y + 4 * S + j * 11 * S, ln, f_dc, fill=(50, 48, 42))
f_foot = F(SANS, 8)
text(d, W // 2, 992 * S,
     "Every story here happened, or was first reported, on Tuesday 24 November 2026, "
     "as the named outlets reported it. Maps and drawings are original vector-style art.",
     f_foot, fill=MUTED, anchor="ma")

# ---------------------------------------------------------------- save
img1024 = img.resize((1024, 1024), Image.LANCZOS)
img1024.save("/home/hatch/workspace/makefun/entry-v2.png")
img1024.convert("RGB").save("/home/hatch/workspace/makefun/entry-v2.jpg",
                            quality=88, optimize=True)
import hashlib
for p in ("/home/hatch/workspace/makefun/entry-v2.png",
          "/home/hatch/workspace/makefun/entry-v2.jpg"):
    b = open(p, "rb").read()
    print(p, len(b), "bytes, sha256", hashlib.sha256(b).hexdigest()[:16])
print("done")
