#!/usr/bin/env python3
"""Render HYBRID entry.png for news-image-20261126 (World Broadsheet, 1024x1024).
Layout + ALL text drawn locally with PIL (exact spelling/numbers).
Hero scenes are photorealistic AI images (parent-generated, verified by eye:
no text, no faces, no wrong flags) pasted into the 3 hero cells with a
center-crop that preserves aspect ratio (never stretched).
Stories: 11 verified (M1-M11) + UCL Wed results (R1, verified via
UEFA.com/AP/Flashscore 26 Nov 07:10 WIB) = 12 stories, 3 regions.
Draft only: final image comes after the evening refresh pass (36-40 stories).
No network, no random, no time — deterministic output."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 33, 61)        # navy
RED = (192, 57, 43)
BLUE = (29, 78, 137)
TEAL = (15, 118, 110)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
LIGHT = (185, 201, 214)
GOLD = (212, 160, 23)
SKY = (214, 230, 242)
CLOUD = (120, 130, 140)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def F(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

f_kicker = F("DejaVuSans-Bold.ttf", 20)
f_date = F("DejaVuSans-Bold.ttf", 52)
f_sub = F("DejaVuSans.ttf", 14)
f_hero_h = F("DejaVuSans-Bold.ttf", 20)
f_hero_s = F("DejaVuSans.ttf", 14)
f_src = F("DejaVuSans.ttf", 12)
f_tag = F("DejaVuSans-Bold.ttf", 13)
f_head = F("DejaVuSans-Bold.ttf", 17)
f_body = F("DejaVuSans.ttf", 13)
f_foot = F("DejaVuSans-Bold.ttf", 13)
f_foot2 = F("DejaVuSans.ttf", 12)
f_small = F("DejaVuSans.ttf", 12)
f_small_b = F("DejaVuSans-Bold.ttf", 12)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- hero photos
HERO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai-hero")
# (filename, vertical focus as fraction of photo height — the crop window is
# centred on this point so the subject is never cut: EU flag ~0.41,
# lightning ~0.42, Macy's balloon ~0.30 so its top is kept whole.)
PHOTOS = {
    "eu": ("media-generation-hero-eu-summit-photo-0-a9d1c776-e06c-4eda-af39-75b7d925d7ac.png", 0.41),
    "storm": ("media-generation-hero-noreaster-photo-0-57005af2-8dc0-4bbc-87d7-394d6b14842d.png", 0.42),
    "macys": ("media-generation-hero-macys-parade-photo-0-62793082-b46f-44a4-a196-3896a5765fd4.png", 0.30),
}

def photo_crop(fname, focus_y, tw, th):
    """Crop a photo to the target aspect ratio (never stretched) and resize
    to the cell. Full-width crop; the window is centred vertically on
    focus_y so the subject stays in frame."""
    im = Image.open(os.path.join(HERO_DIR, fname)).convert("RGB")
    w, h = im.size
    aspect = tw / th
    ch = int(w / aspect)  # crop height for a full-width crop
    if ch > h:
        cw = int(h * aspect)
        x0 = (w - cw) // 2
        box = (x0, 0, x0 + cw, h)
    else:
        cy = int(focus_y * h)
        y0 = min(max(cy - ch // 2, 0), h - ch)
        box = (0, y0, w, y0 + ch)
    return im.crop(box).resize((tw, th), Image.LANCZOS)

def text_w(s, font):
    return d.textlength(s, font=font)

def wrap(s, font, max_w):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def center(y, s, font, color=INK):
    d.text(((W - text_w(s, font)) / 2, y), s, font=font, fill=color)

# ---------------------------------------------------------------- masthead
center(10, "T H E   W O R L D   I N   O N E   D A Y", f_kicker)
center(32, "THURSDAY 26 NOVEMBER 2026", f_date)
center(88, "12 STORIES  \u00b7  3 REGIONS  \u00b7  ALL VERIFIED 26 NOV 2026", f_sub)
d.rectangle([28, 112, 996, 115], fill=INK)

# ---------------------------------------------------------------- hero row
HX0, HY0, HW, HH = 28, 124, 314, 212
GAP = 14
heroes = [
    dict(x=HX0, scene="eu",
         head="EU SUMMIT OPENS IN BRUSSELS",
         sub="\u20ac1.78tn budget \u00b7 \u20ac45bn Ukraine loan",
         src="EU Insider"),
    dict(x=HX0 + HW + GAP, scene="storm",
         head="THANKSGIVING NOR'EASTER",
         sub="81.5m travel \u00b7 gusts to 55 mph",
         src="AAA \u00b7 NY Post \u2014 forecast"),
    dict(x=HX0 + 2 * (HW + GAP), scene="macys",
         head="100TH MACY'S PARADE",
         sub="Balloons may be grounded (forecast)",
         src="NY Post"),
]
for h in heroes:
    x, y = h["x"], HY0
    d.rectangle([x, y, x + HW, y + HH], outline=INK, width=2, fill=WHITE)
    sx, sy, sw, sh = x + 6, y + 6, HW - 12, 118  # scene box
    fname, focus = PHOTOS[h["scene"]]
    scene = photo_crop(fname, focus, sw, sh)
    img.paste(scene, (sx, sy))
    d.rectangle([sx, sy, sx + sw, sy + sh], outline=INK, width=1)
    ly = y + 132
    hl = wrap(h["head"], f_hero_h, HW - 20)
    assert len(hl) <= 2, f"hero headline too long: {h['head']}"
    for i, ln in enumerate(hl):
        d.text((x + 10, ly + i * 22), ln, font=f_hero_h, fill=INK)
    sl = wrap(h["sub"], f_hero_s, HW - 20)
    assert len(sl) <= 1, f"hero sub too long: {h['sub']}"
    d.text((x + 10, ly + 46), sl[0], font=f_hero_s, fill=INK)
    d.text((x + 10, ly + 64), h["src"], font=f_src, fill=GREY)

# ---------------------------------------------------------------- locator strip
LY0 = 344
d.rectangle([28, LY0, 996, LY0 + 2], fill=INK)
d.text((28, LY0 + 10), "WHERE THE NEWS IS", font=f_tag, fill=INK)
chips = [("EUROPE", "6 stories", INK), ("NORTH AMERICA", "4 stories", RED),
         ("ASIA", "2 stories", TEAL)]
cx = 28
for name, n, col in chips:
    label = f"{name} \u2014 {n}"
    w = text_w(label, f_tag) + 20
    d.rounded_rectangle([cx, LY0 + 32, cx + w, LY0 + 58], radius=12, outline=col, width=2)
    d.text((cx + 10, LY0 + 37), label, font=f_tag, fill=col)
    cx += w + 12
d.line([60, LY0 + 96, 964, LY0 + 96], fill=LIGHT, width=3)
cities = [("New York", -74, True), ("Madrid", -3.7, False), ("Brussels", 4.4, True),
          ("Doha", 51.5, False), ("New Delhi", 77.2, True)]
for name, lon, above in cities:
    px = 60 + (lon + 80) / 160 * 904
    d.ellipse([px - 6, LY0 + 90, px + 6, LY0 + 102], fill=RED)
    tw = text_w(name, f_small_b)
    lx = min(max(px - tw / 2, 28), 996 - tw)
    d.text((lx, LY0 + 70 if above else LY0 + 106), name, font=f_small_b, fill=INK)

# ---------------------------------------------------------------- timeline strip
TY0 = 470
d.rectangle([28, TY0, 996, TY0 + 2], fill=INK)
d.text((28, TY0 + 8), "26 NOV 2026 \u2014 UTC TIMELINE", font=f_tag, fill=INK)
tl_y = TY0 + 58
d.line([48, tl_y, 976, tl_y], fill=INK, width=2)
events = [(4.75, "04:45  UCL results", -1), (10.0, "10:00  Cricket SF, Doha", 1),
          (13.5, "13:30  Macy's parade, NYC", -1), (17.75, "17:45  Europa League", 1)]
for hr, label, side in events:
    px = 48 + hr / 24 * 928
    d.ellipse([px - 4, tl_y - 4, px + 4, tl_y + 4], fill=RED)
    tw = text_w(label, f_small)
    lx = min(max(px - tw / 2, 28), 996 - tw)
    ly = tl_y - 22 if side < 0 else tl_y + 10
    d.text((lx, ly), label, font=f_small, fill=INK)

# ---------------------------------------------------------------- grid
GY0 = 554
COLW, ROWH, CGAP, RGAP = 480, 96, 8, 6
REGION_COL = {"EUROPE": INK, "N. AMERICA": RED, "ASIA": TEAL}
grid = [
    ("N. AMERICA", "USA Today", "NFL Thanksgiving tripleheader",
     "Bears-Lions, Eagles-Cowboys, Chiefs-Bills \u2014 three games today"),
    ("EUROPE", "Bogner Chess", "Chess title Game 3 in Geneva",
     "Sindarov v Gukesh, score level 1-1; youngest title match ever"),
    ("ASIA", "Indian Television", "Asia Cup Rising Stars semi-final",
     "Unbeaten Sri Lanka A face India A in Doha"),
    ("EUROPE", "UEFA.com", "Lille stun Bayern 2-1",
     "PSG held 2-2 by Roma \u2014 perfect record ends"),
    ("EUROPE", "UEFA.com", "Liverpool win 3-0, Barcelona 4-1",
     "Man Utd held 2-2 at Sporting; nine games Wednesday night"),
    ("EUROPE", "UEFA.com", "Europa League: 18 games tonight",
     "Matchday 5 \u2014 Plzen-Benfica, Dinamo-Leverkusen, Juve-Omonia"),
    ("ASIA", "PIB", "India marks Constitution Day",
     "77th anniversary of adoption; preamble read in 23 languages"),
    ("EUROPE", "EU Insider", "Spain votes on Sunday",
     "Campaign's final weekend; general election 29 Nov"),
]
for i, (region, src, head, body) in enumerate(grid):
    col, row = i % 2, i // 2
    x = 28 + col * (COLW + CGAP)
    y = GY0 + row * (ROWH + RGAP)
    d.rectangle([x, y, x + COLW, y + ROWH], outline=INK, width=1, fill=WHITE)
    d.text((x + 10, y + 7), f"[{region} \u00b7 {src}]", font=f_tag, fill=REGION_COL[region])
    hl = wrap(head, f_head, COLW - 20)
    assert len(hl) <= 2, f"grid headline too long: {head}"
    for j, ln in enumerate(hl):
        d.text((x + 10, y + 26 + j * 19), ln, font=f_head, fill=INK)
    bl = wrap(body, f_body, COLW - 20)
    assert len(bl) <= 1, f"grid body too long: {body}"
    d.text((x + 10, y + 66), bl[0], font=f_body, fill=INK)

# ---------------------------------------------------------------- footer
FY0 = 964
d.rectangle([28, FY0, 996, FY0 + 2], fill=INK)
center(FY0 + 8, "26 NOVEMBER 2026  \u00b7  12 STORIES  \u00b7  3 REGIONS", f_foot)
center(FY0 + 26, "Sources: EU Insider \u00b7 NY Post \u00b7 AAA \u00b7 USA Today \u00b7 Bogner Chess \u00b7 Indian Television \u00b7 UEFA.com \u00b7 PIB",
       f_foot2, GREY)
center(FY0 + 42, "All events dated 26 Nov 2026 (any timezone); forecasts labelled as forecast.", f_foot2, GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out), "bytes", img.size)
