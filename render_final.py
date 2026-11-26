#!/usr/bin/env python3
"""Render FINAL entry.png for news-image-20261126 (World Broadsheet, 1024x1024).
36 stories, 8 regions. Layout + ALL text drawn locally with PIL.
Hero scenes are photorealistic AI images (parent-generated, verified by eye)
pasted into the 3 hero cells with a center-crop that preserves aspect ratio.
Grid: 3 cols x 11 rows, 2-line cells (region code + headline / body + source).
No network, no random, no time - deterministic output."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 33, 61)
RED = (192, 57, 43)
BLUE = (29, 78, 137)
TEAL = (15, 118, 110)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
LIGHT = (185, 201, 214)
GOLD = (150, 110, 10)
PURPLE = (120, 60, 140)
GREEN = (20, 120, 60)
ORANGE = (200, 110, 20)

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
f_code = F("DejaVuSans-Bold.ttf", 13)
f_head = F("DejaVuSans-Bold.ttf", 16)
f_body = F("DejaVuSans.ttf", 13)
f_foot = F("DejaVuSans-Bold.ttf", 13)
f_foot2 = F("DejaVuSans.ttf", 12)
f_small = F("DejaVuSans.ttf", 12)
f_small_b = F("DejaVuSans-Bold.ttf", 12)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- hero photos
HERO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai-hero")
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
    ch = int(w / aspect)
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
center(8, "T H E   W O R L D   I N   O N E   D A Y", f_kicker)
center(30, "THURSDAY 26 NOVEMBER 2026", f_date)
center(86, "36 STORIES  \u00b7  8 REGIONS  \u00b7  ALL VERIFIED 26 NOV 2026", f_sub)
d.rectangle([28, 108, 996, 112], fill=INK)

# ---------------------------------------------------------------- hero row
HX0, HY0, HW, HH = 28, 120, 314, 186
GAP = 14
heroes = [
    dict(x=HX0, scene="eu",
         head="EU SUMMIT ENDS DAY 1 WITH NO DEAL",
         sub="\u20ac1.58tn budget \u00b7 \u20ac45bn loan split",
         src="AP \u00b7 Helsinki Times"),
    dict(x=HX0 + HW + GAP, scene="storm",
         head="THANKSGIVING NOR'EASTER",
         sub="1,000+ flights out \u00b7 1m+ no power",
         src="The Traveler \u00b7 AeroCorner"),
    dict(x=HX0 + 2 * (HW + GAP), scene="macys",
         head="100TH MACY'S PARADE",
         sub="Postponed to Sat \u2014 first time ever",
         src="NY Post \u00b7 CNN"),
]
for h in heroes:
    x, y = h["x"], HY0
    d.rectangle([x, y, x + HW, y + HH], outline=INK, width=2, fill=WHITE)
    sx, sy, sw, sh = x + 6, y + 6, HW - 12, 94  # scene box
    fname, focus = PHOTOS[h["scene"]]
    scene = photo_crop(fname, focus, sw, sh)
    img.paste(scene, (sx, sy))
    d.rectangle([sx, sy, sx + sw, sy + sh], outline=INK, width=1)
    ly = y + 106
    hl = wrap(h["head"], f_hero_h, HW - 20)
    assert len(hl) <= 2, f"hero headline too long: {h['head']}"
    for i, ln in enumerate(hl):
        d.text((x + 10, ly + i * 22), ln, font=f_hero_h, fill=INK)
    sl = wrap(h["sub"], f_hero_s, HW - 20)
    assert len(sl) <= 1, f"hero sub too long: {h['sub']}"
    sub_y = ly + len(hl) * 22 + 2
    d.text((x + 10, sub_y), sl[0], font=f_hero_s, fill=INK)
    d.text((x + 10, sub_y + 18), h["src"], font=f_src, fill=GREY)

# ---------------------------------------------------------------- locator strip
LY0 = 314
d.rectangle([28, LY0, 996, LY0 + 2], fill=INK)
d.text((28, LY0 + 8), "WHERE THE NEWS IS", font=f_tag, fill=INK)
chips_rows = [
    [("EUROPE", "9 stories", INK), ("N. AMERICA", "10 stories", RED),
     ("ASIA", "6 stories", TEAL), ("MIDEAST", "2 stories", GOLD)],
    [("AFRICA", "2 stories", PURPLE), ("OCEANIA", "3 stories", GREEN),
     ("S. AMERICA", "1 story", ORANGE), ("GLOBAL", "3 stories", GREY)],
]
for r, row in enumerate(chips_rows):
    cy = LY0 + 30 + r * 30
    cx = 28
    for name, n, col in row:
        label = f"{name} \u2014 {n}"
        w = text_w(label, f_tag) + 20
        d.rounded_rectangle([cx, cy, cx + w, cy + 26], radius=12, outline=col, width=2)
        d.text((cx + 10, cy + 5), label, font=f_tag, fill=col)
        cx += w + 12

# ---------------------------------------------------------------- timeline strip
TY0 = 398
d.rectangle([28, TY0, 996, TY0 + 2], fill=INK)
d.text((28, TY0 + 8), "UTC TIMELINE", font=f_tag, fill=INK)
tl_y = TY0 + 34
d.line([48, tl_y, 976, tl_y], fill=INK, width=2)
events = [(4.75, "04:45 UCL results", -1), (10.0, "10:00 Cricket SF", 1),
          (13.5, "13:30 Macy's postponed", -1), (14.0, "14:00 EU summit", 1),
          (17.75, "17:45 Europa League", -1), (18.0, "18:00 Bears beat Lions", 1)]
for hr, label, side in events:
    px = 48 + hr / 24 * 928
    d.ellipse([px - 4, tl_y - 4, px + 4, tl_y + 4], fill=RED)
    tw = text_w(label, f_small)
    lx = min(max(px - tw / 2, 28), 996 - tw)
    ly = tl_y - 22 if side < 0 else tl_y + 10
    d.text((lx, ly), label, font=f_small, fill=INK)

# ---------------------------------------------------------------- grid (3 cols x 11 rows)
GY0 = 480
COLW, ROWH, CGAP, RPITCH = 317, 42, 8, 44
REGION_COL = {"EU": INK, "NA": RED, "AS": TEAL, "ME": GOLD,
              "AF": PURPLE, "OC": GREEN, "SA": ORANGE, "GL": GREY}
grid = [
    ("NA", "Thanksgiving: 81.5m travel",
     "81.5m travel; US markets shut (AAA)"),
    ("NA", "Bears stun Lions 39-35",
     "Odunze TD with 3 seconds left (Reuters)"),
    ("EU", "Chess Game 3: draw in 60",
     "Draw in 60 moves; 1.5-1.5 (Chess.com)"),
    ("AS", "SL A win semi by 8 wickets",
     "SL A chase 318/2, win by 8 wickets (ESPN)"),
    ("EU", "Lille stun Bayern 2-1",
     "Lille 2-1 Bayern; PSG 2-2 Roma (UEFA)"),
    ("EU", "Liverpool win 3-0, Barca 4-1",
     "Liverpool 3-0; Barca 4-1; Utd 2-2 (UEFA)"),
    ("EU", "Plzen thrash Benfica 4-0",
     "Plzen 4-0 Benfica; Milan 4-2 (Reuters)"),
    ("AS", "India marks Constitution Day",
     "77th anniversary of adoption (PIB)"),
    ("EU", "Spain votes Sunday; PP leads",
     "Final polls: PP leads; vote Sun (El Pais)"),
    ("ME", "Gaza: 9 killed in strikes",
     "9 killed incl. Hamas minister (Reuters)"),
    ("EU", "113 drones hit Ukraine",
     "113 drones, missiles hit 7 regions (AP)"),
    ("AF", "Ebola cases pass 12,000",
     "12,021 cases, 5,904 dead (Reuters)"),
    ("GL", "Tariff backlash: China, EU",
     "China, Japan, EU protest new US levies (AP)"),
    ("AS", "Asia stocks rebound",
     "Nikkei +0.9%, Hang Seng +1.2% (AP)"),
    ("EU", "Europe rallies on tariff relief",
     "DAX +2.1%, FTSE +1.8%, CAC +1.6% (QNA)"),
    ("GL", "Gold rebounds; Brent $94.71",
     "Gold $3,581; Brent $94.71 (Reuters)"),
    ("EU", "Russian drone enters Poland",
     "NATO jets monitor Polish airspace (Nexus)"),
    ("AS", "13 dead in Indonesia mine",
     "13 dead, 13 trapped in Bogor mine (Reuters)"),
    ("NA", "Gulf crash: ATC had warned",
     "ATC warned pilot of bad weather (LiveATC)"),
    ("OC", "Flinders Island wildfires",
     "Fires raze homes on Flinders Island (AP)"),
    ("OC", "NZ unveils $1.9bn ferries",
     "Two hybrid ferries due 2029; $1.9bn (RNZ)"),
    ("OC", "NZ final count due Friday",
     "Final count Fri; 4 seats close (Reuters)"),
    ("AF", "Guinea-Bissau delays vote",
     "Vote delayed ~2 years after coup (Reuters)"),
    ("SA", "Lula opens Amazon Summit",
     "Amazon Summit in Bogota (Adalytica)"),
    ("NA", "SpaceX: 1m satellites cleared",
     "FCC clears orbital data centres (Neuron)"),
    ("NA", "NY bans AI chatbot toys",
     "NY bans AI chatbot toys 5 yrs (Neuron)"),
    ("NA", "FDA clears Neuralink trial",
     "FDA clears Neuralink ALS trial (AI Weekly)"),
    ("GL", "Pulsar flees supernova",
     "Runaway pulsar at 1,400 km/s (Phys.org)"),
    ("AS", "Tim Burton show opens Tokyo",
     "Burton's Labyrinth opens in Tokyo (AnewZ)"),
    ("NA", "Trump's Thanksgiving rant",
     "Trump lashes foes in holiday post (Reuters)"),
    ("NA", "Trump demands GDP probe",
     "Trump demands GDP data probe (Reuters)"),
    ("ME", "2 Italians killed in Kuwait",
     "2 Italians killed in Kuwait (Reuters)"),
    ("AS", "N. Korea halts missile exports",
     "Pyongyang halts KN-23 shipments (Reuters)"),
]
assert len(grid) == 33, f"grid must be 33 cells, got {len(grid)}"
for i, (code, head, body) in enumerate(grid):
    col, row = i % 3, i // 3
    x = 28 + col * (COLW + CGAP)
    y = GY0 + row * RPITCH
    d.rectangle([x, y, x + COLW, y + ROWH], outline=INK, width=1, fill=WHITE)
    cw = text_w(code, f_code)
    d.text((x + 8, y + 5), code, font=f_code, fill=REGION_COL[code])
    hw = text_w(head, f_head)
    assert hw <= COLW - 20 - cw - 6, f"grid headline too long: {head} ({hw:.0f}px)"
    d.text((x + 8 + cw + 6, y + 3), head, font=f_head, fill=INK)
    bw = text_w(body, f_body)
    assert bw <= COLW - 20, f"grid body too long: {body} ({bw:.0f}px)"
    d.text((x + 8, y + 23), body, font=f_body, fill=INK)

# ---------------------------------------------------------------- footer
FY0 = 970
d.rectangle([28, FY0, 996, FY0 + 2], fill=INK)
center(FY0 + 8, "26 NOVEMBER 2026  \u00b7  36 STORIES  \u00b7  8 REGIONS", f_foot)
center(FY0 + 24, "Sources: Reuters \u00b7 AP \u00b7 UEFA.com \u00b7 Chess.com \u00b7 ESPNcricinfo \u00b7 NY Post \u00b7 AAA \u00b7 PIB \u00b7 EU Insider",
       f_foot2, GREY)
center(FY0 + 40, "All events dated 26 Nov 2026 (any timezone); scores as reported that day.", f_foot2, GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out), "bytes", img.size)
