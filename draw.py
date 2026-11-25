#!/usr/bin/env python3
"""news-image-20261125 — renders THE WORLD IN ONE DAY for Wed 25 Nov 2026.

Fresh renderer written 25 Nov 2026 in-session (Python 3 + Pillow, stdlib
only besides Pillow). Draws a 1024x1024 broadsheet front page:
masthead, day-in-numbers strip, region bar, 3 large illustrated leads,
12 illustrated medium cards, 20 one-line briefs, DATE CHECK footer.
Writes entry.png next to this file (and honours MAKEFUN_OUTPUT_DIR).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 16)
RED = (178, 34, 26)
DARKRED = (128, 22, 16)
MUTED = (104, 97, 84)
RULE = (60, 56, 48)
CARD_BG = (255, 255, 255)
CARD_LINE = (198, 190, 172)
GOLD = (176, 132, 34)

FD = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SERIF_R = os.path.join(FD, "DejaVuSerif.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_lines(d, text, fnt, maxw, maxlines):
    lines = wrap(d, text, fnt, maxw)
    return lines[:maxlines]


# ---------------------------------------------------------------- stories
# (region, kicker, headline, deck, scene)
LEADS = [
    ("NORTH AMERICA", "CYBER BREACH AT THE CIA",
     "CIA and spy chief's office hit by cyberattack",
     "Intruders struck a system US intelligence agencies use to sift "
     "open-source information; some unclassified material was exposed.",
     "breach"),
    ("MIDDLE EAST", "GAZA CITY",
     "Israeli strike kills Hamas security chief",
     "Naim Abu Nakhla, head of Hamas's internal security apparatus, "
     "killed in Gaza City; two more strikes kill six. 1,679 dead in "
     "Gaza since the October ceasefire.",
     "gaza"),
    ("MIDDLE EAST", "RIYADH",
     "Houthi drone hits Riyadh's tallest tower; 11 hurt",
     "Saudi civil defence says a drone struck a tower in the capital, "
     "wounding eleven people, as the Yemen war spills deeper into "
     "Saudi Arabia.",
     "tower"),
]

MEDIUMS = [
    ("EUROPE", "UKRAINE WAR",
     "Kyiv confirms it hit a Russian ship in the Gulf of Finland",
     "Zelenskiy owns Saturday's drone strike on a Russian cargo ship.",
     "ship"),
    ("EUROPE", "NATO",
     "NATO to send early-warning aircraft to Poland",
     "Deployment follows reports of missiles landing in Poland.",
     "radar"),
    ("NORTH AMERICA", "US COURTS",
     "Huawei guilty on 10 of 12 US charges",
     "Brooklyn jury convicts on trade-secret theft and bank fraud; "
     "racketeering thrown out. Billions in fines loom; appeal planned.",
     "court"),
    ("ASIA-PACIFIC", "NEPAL",
     "Magnitude 5.6 quake shakes Nepal's Koshi Province",
     "Tremor strikes near the Chinese border; no major damage "
     "reported at first count.",
     "quake"),
    ("ASIA-PACIFIC", "PHILIPPINES",
     "Magnitude 5.1 quake off Antique",
     "Earthquake recorded at 7:29 a.m. off Valderrama, in the "
     "western Visayas.",
     "quake2"),
    ("AFRICA", "CONGO EBOLA",
     "WHO pulls staff from Ebola hospital amid fighting",
     "Staff evacuated from Akwe hospital in Ituri after three days "
     "sheltering from fighting.",
     "hospital"),
    ("NORTH AMERICA", "WHITE HOUSE",
     "Trump gives Giuliani the Medal of Freedom",
     "Former New York mayor and Trump lawyer honoured at the "
     "White House ceremony.",
     "medal"),
    ("EUROPE", "CRICKET",
     "England level T20 series in Australia",
     "Eight-wicket win chasing 185; the five-match series stands 1-1.",
     "cricket"),
    ("ASIA-PACIFIC", "MARKETS",
     "Sensex tumbles 1,484 points",
     "Nifty slips below 25,400 as banks and metals lead a broad "
     "sell-off in Mumbai.",
     "chart"),
    ("ASIA-PACIFIC", "DIPLOMACY",
     "Modi and Merz talk up India-Germany ties",
     "Leaders hold talks on deepening the India-Germany strategic "
     "partnership.",
     "flags"),
    ("ASIA-PACIFIC", "CRYPTO RULES",
     "Seoul drafts sweeping digital-asset law",
     "Big exchange shareholders capped at 20%; won stablecoins and "
     "licences introduced.",
     "coin"),
    ("EUROPE", "SANCTIONS",
     "EU adds new sanctions on Russia",
     "Brussels announces further restrictive measures as the war "
     "in Ukraine grinds on.",
     "stars"),
]

BRIEFS = [
    ("NORTH AMERICA", "Thanksgiving eve: ", "Trump pardons turkeys Freedom and Feathers."),
    ("NORTH AMERICA", "Chicago: ", "radar fault delays flights at O'Hare, FAA says."),
    ("NORTH AMERICA", "Iowa: ", "Army to detonate lead azide; residents told to leave."),
    ("NORTH AMERICA", "Wall Street: ", "Nvidia shares fall 7% as lawmakers demand answers."),
    ("NORTH AMERICA", "AI boom: ", "Dell lifts forecasts after record AI-server quarter."),
    ("NORTH AMERICA", "Streaming: ", "Tidal to delete 29m AI-made tracks from 9 December."),
    ("NORTH AMERICA", "Science: ", "OpenAI says GPT-6 models design proteins in lab tests."),
    ("NORTH AMERICA", "Fort Hood: ", "gunman Hasan seeks stay of execution set for next week."),
    ("MIDDLE EAST", "Gaza aid: ", "UN warns of hardship as help struggles to reach civilians."),
    ("MIDDLE EAST", "At the UN: ", "Russia and Ukraine trade charges over Black Sea shipping."),
    ("MIDDLE EAST", "Yemen: ", "Houthis 'will not take Aden', government forces say."),
    ("MIDDLE EAST", "Yemen: ", "Saudi strikes in the south-west leave dead and missing."),
    ("MIDDLE EAST", "Doha: ", "US and Qatar discuss strategic cooperation."),
    ("ASIA-PACIFIC", "India: ", "BJP and Akali Dal reunite for 2027 Punjab polls."),
    ("ASIA-PACIFIC", "Nepal: ", "PM's India visit hailed a 'historic milestone'."),
    ("ASIA-PACIFIC", "Cricket: ", "India-New Zealand first Test ends in a draw."),
    ("ASIA-PACIFIC", "India: ", "factory output hits a nine-month high."),
    ("ASIA-PACIFIC", "UAE: ", "11 killed in a road crash in Ras Al Khaimah."),
    ("ASIA-PACIFIC", "Finance: ", "BlackRock launches Hong Kong tokenised money fund."),
    ("LATIN AMERICA", "Venezuela: ", "government puts public debt at $237.5bn."),
]

REGIONS = [
    ("NORTH AMERICA", 11, (31, 68, 128)),
    ("ASIA-PACIFIC", 11, (178, 34, 26)),
    ("MIDDLE EAST", 7, (196, 120, 20)),
    ("EUROPE", 4, (42, 110, 70)),
    ("AFRICA", 1, (110, 80, 140)),
    ("LATIN AMERICA", 1, (20, 120, 120)),
]

NUMBERS = [
    ("35", "stories"),
    ("6", "regions"),
    ("2", "quakes 5.1+"),
    ("11", "hurt in Riyadh"),
    ("1,679", "Gaza deaths since ceasefire"),
]

# ---------------------------------------------------------------- scenes
def scene_breach(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 40))
    for i in range(0, w, 14):
        for j in range(0, h, 14):
            if (i // 14 + j // 14) % 3 == 0:
                d.text((x + i + 2, y + j + 1), "01"[(i // 14) % 2],
                       font=font(SANS, 9), fill=(60, 110, 160))
    cx, cy = x + w // 2, y + h // 2 + 4
    d.polygon([(cx, cy - 34), (cx + 30, cy - 14), (cx + 30, cy + 22),
               (cx, cy + 34), (cx - 30, cy + 22), (cx - 30, cy - 14)],
              fill=(178, 34, 26), outline=(255, 220, 200))
    d.rectangle([cx - 8, cy - 6, cx + 8, cy + 12], fill=(247, 243, 234))
    d.ellipse([cx - 6, cy - 14, cx + 6, cy - 2], fill=(247, 243, 234))
    d.line([cx - 26, cy + 30, cx + 26, cy + 30], fill=RED, width=4)


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 190, 120))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(70, 52, 40))
    for bx, bw, bh in [(6, 34, 52), (48, 26, 70), (82, 40, 46), (130, 30, 62),
                       (168, 36, 50), (212, 30, 68), (250, 34, 44), (288, 26, 58)]:
        d.rectangle([x + bx, y + h - 26 - bh, x + bx + bw, y + h - 26],
                    fill=(52, 44, 38))
        for wy in range(y + h - 22 - bh, y + h - 30, 12):
            d.rectangle([x + bx + 5, wy, x + bx + 11, wy + 6],
                        fill=(232, 190, 120))
    d.ellipse([x + w - 78, y + 8, x + w - 18, y + 52], fill=(178, 34, 26))
    d.polygon([(x + w - 48, y + 30), (x + w - 60, y + 66), (x + w - 36, y + 66)],
              fill=(120, 30, 20))
    d.ellipse([x + 30, y + 14, x + 66, y + 40], fill=(120, 110, 100))
    d.ellipse([x + 52, y + 6, x + 82, y + 28], fill=(140, 128, 116))


def scene_tower(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 38, 66))
    d.ellipse([x + w - 60, y + 10, x + w - 24, y + 46], fill=(232, 220, 180))
    tx = x + w // 2
    d.polygon([(tx - 16, y + h - 8), (tx - 10, y + 26), (tx + 10, y + 26),
               (tx + 16, y + h - 8)], fill=(200, 205, 215))
    d.line([tx, y + 8, tx, y + 26], fill=(220, 220, 220), width=3)
    d.ellipse([tx - 3, y + 4, tx + 3, y + 10], fill=(255, 80, 60))
    for wy in range(y + 34, y + h - 16, 14):
        d.rectangle([tx - 8, wy, tx + 8, wy + 5], fill=(250, 200, 60))
    d.ellipse([x + 26, y + 22, x + 44, y + 40], fill=(255, 120, 40))
    d.polygon([(x + 35, y + 31), (x + 18, y + 52), (x + 52, y + 52)],
              fill=(255, 90, 30))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(12, 20, 34))


def scene_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 215))
    d.ellipse([x + w - 40, y + 4, x + w - 16, y + 28], fill=(247, 243, 234))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(28, 80, 130))
    d.polygon([(x + 10, y + h - 12), (x + 46, y + h - 12), (x + 40, y + h - 4),
               (x + 16, y + h - 4)], fill=(40, 44, 52))
    d.rectangle([x + 18, y + h - 22, x + 38, y + h - 12], fill=(178, 34, 26))
    d.rectangle([x + 44, y + h - 19, x + 64, y + h - 12], fill=(196, 120, 20))
    d.ellipse([x + w - 70, y + 6, x + w - 58, y + 18], fill=(40, 44, 52))
    d.line([x + w - 64, y + 18, x + w - 52, y + 26], fill=(40, 44, 52), width=2)


def scene_radar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 42, 30))
    cx, cy = x + w // 2, y + h // 2 + 2
    for r in (18, 12, 6):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(90, 200, 140))
    d.line([cx, cy, cx + 15, cy - 13], fill=(120, 230, 160), width=2)
    d.ellipse([cx + 11, cy - 17, cx + 19, cy - 9], fill=(255, 90, 60))
    d.ellipse([cx - 12, cy + 4, cx - 6, cy + 10], fill=(255, 220, 80))


def scene_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(88, 66, 44))
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(52, 38, 26))
    for px in (8, 26, 44):
        d.rectangle([x + px, y + 16, x + px + 6, y + h - 6], fill=(232, 220, 190))
    d.polygon([(x, y + 16), (x + w // 2, y + 3), (x + w, y + 16)], fill=(200, 180, 140))
    d.rectangle([x + w - 30, y + 20, x + w - 8, y + 30], fill=(60, 40, 28))
    d.ellipse([x + w - 26, y + 13, x + w - 12, y + 21], fill=(200, 180, 140))


def scene_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 196, 160))
    d.polygon([(x, y + h), (x + w * 0.3, y + h * 0.45), (x + w * 0.55, y + h * 0.7),
               (x + w * 0.8, y + h * 0.4), (x + w, y + h * 0.6), (x + w, y + h)],
              fill=(120, 88, 52))
    d.line([x + 6, y + 8, x + 18, y + 18, x + 30, y + 6, x + 44, y + 20,
            x + 58, y + 8, x + 74, y + 18, x + 88, y + 8], fill=(178, 34, 26), width=2)
    d.rectangle([x + 8, y + h - 14, x + 26, y + h - 4], fill=(90, 70, 50))
    d.polygon([(x + 8, y + h - 14), (x + 17, y + h - 21), (x + 26, y + h - 14)],
              fill=(120, 40, 30))


def scene_quake2(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 90, 120))
    d.polygon([(x, y + h * 0.55), (x + w * 0.35, y + h * 0.75), (x + w * 0.6, y + h * 0.5),
               (x + w, y + h * 0.7), (x + w, y + h), (x, y + h)], fill=(20, 50, 70))
    d.line([x + 6, y + 8, x + 20, y + 18, x + 34, y + 6, x + 50, y + 20,
            x + 64, y + 8, x + 80, y + 18, x + 94, y + 8], fill=(255, 220, 80), width=2)
    d.ellipse([x + w - 26, y + 4, x + w - 8, y + 22], fill=(247, 243, 234))
    d.rectangle([x + 10, y + h - 16, x + 28, y + h - 5], fill=(200, 160, 90))
    d.rectangle([x + 34, y + h - 12, x + 48, y + h - 5], fill=(200, 160, 90))


def scene_hospital(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 228, 222))
    d.rectangle([x + 12, y + 6, x + w - 12, y + h - 4], fill=(255, 255, 255))
    d.rectangle([x + w // 2 - 10, y + 9, x + w // 2 - 3, y + 24], fill=(178, 34, 26))
    d.rectangle([x + w // 2 - 14, y + 13, x + w // 2 + 1, y + 20], fill=(178, 34, 26))
    for wy in range(y + 28, y + h - 6, 7):
        d.rectangle([x + 18, wy, x + 28, wy + 3], fill=(120, 160, 150))
        d.rectangle([x + w - 28, wy, x + w - 18, wy + 3], fill=(120, 160, 150))


def scene_medal(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 44, 84))
    d.polygon([(x + w // 2 - 12, y + 3), (x + w // 2 + 12, y + 3),
               (x + w // 2 + 6, y + 18), (x + w // 2 - 6, y + 18)],
              fill=(178, 34, 26))
    d.ellipse([x + w // 2 - 14, y + 15, x + w // 2 + 14, y + 43], fill=(212, 175, 55),
              outline=(255, 230, 140))
    d.text((x + w // 2 - 4, y + 22), "1", font=font(SERIF, 14),
           fill=(120, 84, 10))
    d.ellipse([x + 8, y + 6, x + 18, y + 16], fill=(255, 220, 120))
    d.ellipse([x + w - 18, y + 8, x + w - 8, y + 18], fill=(255, 220, 120))


def scene_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 120, 60))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(120, 90, 50))
    d.rectangle([x + w - 18, y + 10, x + w - 12, y + h - 8], fill=(232, 220, 180))
    d.rectangle([x + w - 10, y + 10, x + w - 4, y + h - 8], fill=(232, 220, 180))
    d.rectangle([x + w - 18, y + 6, x + w - 4, y + 10], fill=(200, 180, 140))
    d.polygon([(x + 12, y + h - 8), (x + 30, y + 12), (x + 38, y + 18), (x + 20, y + h - 8)],
              fill=(190, 140, 80))
    d.ellipse([x + 12, y + 6, x + 26, y + 20], fill=(178, 34, 26))


def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 48))
    for gy in range(y + 8, y + h - 4, 10):
        d.line([x + 6, gy, x + w - 6, gy], fill=(52, 62, 84))
    d.line([x + 8, y + 8, x + 26, y + 14, x + 44, y + 12, x + 62, y + 24,
            x + 80, y + 30, x + w - 8, y + h - 6], fill=(255, 90, 60), width=3)
    d.polygon([(x + w - 18, y + h - 12), (x + w - 8, y + h - 12), (x + w - 8, y + h - 4)],
              fill=(255, 90, 60))
    d.text((x + 8, y + 3), "-1,484", font=font(SANS_B, 12), fill=(255, 120, 90))


def scene_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 220))
    d.rectangle([x + 10, y + 8, x + 42, y + 17], fill=(255, 153, 51))
    d.rectangle([x + 10, y + 17, x + 42, y + 26], fill=(255, 255, 255))
    d.rectangle([x + 10, y + 26, x + 42, y + 35], fill=(19, 136, 8))
    d.ellipse([x + 23, y + 18, x + 29, y + 24], fill=(0, 0, 128))
    d.rectangle([x + w - 42, y + 8, x + w - 10, y + 17], fill=(20, 20, 20))
    d.rectangle([x + w - 42, y + 17, x + w - 10, y + 26], fill=(221, 0, 0))
    d.rectangle([x + w - 42, y + 26, x + w - 10, y + 35], fill=(255, 206, 0))
    d.polygon([(x + w // 2 - 8, y + h - 6), (x + w // 2 + 8, y + h - 6),
               (x + w // 2, y + h - 16)], fill=(178, 34, 26))


def scene_coin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 240, 200))
    d.ellipse([x + w // 2 - 15, y + 5, x + w // 2 + 15, y + 35], fill=(212, 175, 55),
              outline=(140, 100, 20))
    d.text((x + w // 2 - 6, y + 11), "W", font=font(SERIF, 16), fill=(120, 84, 10))
    d.line([x + 8, y + h - 5, x + w - 8, y + h - 5], fill=(120, 84, 10), width=2)


def scene_stars(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 40, 110))
    cx, cy = x + w // 2, y + h // 2
    import math
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        sx, sy = cx + int(17 * math.cos(a)), cy + int(15 * math.sin(a))
        d.polygon([(sx, sy - 3), (sx + 2, sy + 2), (sx - 2, sy + 2)], fill=(255, 220, 60))
    d.rectangle([x + w // 2 - 10, y + h - 8, x + w // 2 + 10, y + h - 4],
                fill=(255, 255, 255))


SCENES = {
    "breach": scene_breach, "gaza": scene_gaza, "tower": scene_tower,
    "ship": scene_ship, "radar": scene_radar, "court": scene_court,
    "quake": scene_quake, "quake2": scene_quake2, "hospital": scene_hospital,
    "medal": scene_medal, "cricket": scene_cricket, "chart": scene_chart,
    "flags": scene_flags, "coin": scene_coin, "stars": scene_stars,
}

# ---------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 24
    CW = W - 2 * MX

    # ---- masthead
    d.line([MX, 16, W - MX, 16], fill=INK, width=3)
    d.line([MX, 20, W - MX, 20], fill=INK, width=1)
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF, 47)
    d.text(((W - d.textlength(title, font=tf)) / 2, 26), title, font=tf, fill=INK)
    sub = "WEDNESDAY 25 NOVEMBER 2026"
    sf = font(SANS_B, 17)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 82), sub, font=sf, fill=RED)
    tag = "35 STORIES  ·  SIX REGIONS  ·  ONE DAY  ·  EVERY STORY HAPPENED OR WAS FIRST REPORTED TODAY"
    tgf = font(SANS, 11)
    d.text(((W - d.textlength(tag, font=tgf)) / 2, 106), tag, font=tgf, fill=MUTED)
    d.line([MX, 126, W - MX, 126], fill=INK, width=2)

    # ---- the day in numbers
    y = 134
    nf = font(SERIF, 20)
    lf = font(SANS, 10)
    seg = CW / len(NUMBERS)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = MX + seg * i + seg / 2
        d.text((cx - d.textlength(num, font=nf) / 2, y), num, font=nf, fill=RED)
        d.text((cx - d.textlength(lab, font=lf) / 2, y + 24), lab, font=lf, fill=MUTED)
        if i:
            d.line([MX + seg * i, y + 2, MX + seg * i, y + 38], fill=CARD_LINE, width=1)
    y = 174
    d.line([MX, y, W - MX, y], fill=RULE, width=1)

    # ---- region bar (segments sum to 35)
    y = 181
    d.text((MX, y), "WHERE THE DAY HAPPENED", font=font(SANS_B, 10), fill=INK)
    total = sum(c for _, c, _ in REGIONS)
    assert total == 35, total
    bx, bw, bh = MX, CW, 13
    by = y + 15
    x = bx
    for name, cnt, col in REGIONS:
        wseg = bw * cnt / total
        d.rectangle([x, by, x + wseg - 1, by + bh], fill=col)
        x += wseg
    ly = by + bh + 5
    lx = MX
    lf2 = font(SANS_B, 10)
    for name, cnt, col in REGIONS:
        d.rectangle([lx, ly + 1, lx + 9, ly + 10], fill=col)
        t = f"{name} {cnt}"
        d.text((lx + 12, ly), t, font=lf2, fill=INK)
        lx += d.textlength(t, font=lf2) + 26
    y = ly + 17
    d.line([MX, y, W - MX, y], fill=RULE, width=1)

    # ---- 3 large leads
    y += 8
    lead_y = y
    gap = 10
    lw = (CW - 2 * gap) // 3
    for i, (region, kicker, head, deck, scene) in enumerate(LEADS):
        x = MX + i * (lw + gap)
        SCENES[scene](d, x, lead_y, lw, 100)
        d.rectangle([x, lead_y, x + lw, lead_y + 100], outline=INK, width=1)
        ky = lead_y + 106
        d.text((x, ky), f"{region} — {kicker}", font=font(SANS_B, 10), fill=RED)
        hy = ky + 15
        lines = fit_lines(d, head, font(SERIF, 19), lw, 2)
        text_block(d, x, hy, lines, font(SERIF, 19), INK, leading=21)
        dy = hy + 2 * 21 + 2
        lines = fit_lines(d, deck, font(SANS, 12), lw, 3)
        text_block(d, x, dy, lines, font(SANS, 12), (40, 38, 34), leading=14)
    leads_end = lead_y + 100 + 6 + 13 + 2 + 42 + 2 + 42
    y = leads_end + 6
    d.line([MX, y, W - MX, y], fill=RULE, width=1)

    # ---- 12 medium cards, 4 x 3
    y += 8
    mgap = 6
    mw = (CW - 3 * mgap) // 4
    mh = 108
    for idx, (region, kicker, head, deck, scene) in enumerate(MEDIUMS):
        r, c = divmod(idx, 4)
        x = MX + c * (mw + mgap)
        cy = y + r * (mh + mgap)
        d.rectangle([x, cy, x + mw, cy + mh], fill=CARD_BG, outline=CARD_LINE, width=1)
        SCENES[scene](d, x + 1, cy + 1, mw - 2, 40)
        ty = cy + 44
        d.text((x + 7, ty), f"{region} · {kicker}", font=font(SANS_B, 9), fill=RED)
        hy = ty + 12
        lines = fit_lines(d, head, font(SANS_B, 12), mw - 14, 2)
        text_block(d, x + 7, hy, lines, font(SANS_B, 12), INK, leading=13)
        dy = hy + 2 * 13 + 1
        lines = fit_lines(d, deck, font(SANS, 10), mw - 14, 2)
        text_block(d, x + 7, dy, lines, font(SANS, 10), (52, 50, 44), leading=12)
    y = y + 3 * mh + 2 * mgap + 8
    d.line([MX, y, W - MX, y], fill=RULE, width=1)

    # ---- 20 briefs, two columns of ten
    y += 7
    d.text((MX, y), "THE REST OF THE DAY — 20 MORE STORIES",
           font=font(SANS_B, 12), fill=INK)
    d.text((W - MX - d.textlength("ALL 25 NOVEMBER 2026", font=font(SANS, 10)), y + 1),
           "ALL 25 NOVEMBER 2026", font=font(SANS, 10), fill=MUTED)
    by = y + 18
    bf = font(SANS, 12)
    bfb = font(SANS_B, 12)
    colw = (CW - 20) // 2
    for i, (region, lead, rest) in enumerate(BRIEFS):
        col, row = divmod(i, 10)
        x = MX + col * (colw + 20)
        yy = by + row * 14
        d.text((x, yy), "▸", font=bfb, fill=RED)
        lx = x + 14
        d.text((lx, yy), lead, font=bfb, fill=INK)
        rx = lx + d.textlength(lead, font=bfb)
        avail = x + colw - rx - 2
        rtext = rest
        while rtext and d.textlength(rtext, font=bf) > avail:
            rtext = rtext.rsplit(" ", 1)[0] + "…"
        d.text((rx, yy), rtext, font=bf, fill=(40, 38, 34))
    y = by + 10 * 14 + 5

    # ---- footer: DATE CHECK
    d.line([MX, y, W - MX, y], fill=INK, width=2)
    y += 6
    d.rectangle([MX, y, W - MX, y + 26], fill=(232, 226, 210), outline=RULE)
    chk = ("DATE CHECK — Every story above happened, or was first reported, on "
           "Wednesday 25 November 2026. Sources: Reuters, CNN, AP, BBC, AFP, USGS, WHO.")
    cf = font(SANS_B, 10)
    while d.textlength(chk, font=cf) > CW - 16:
        chk = chk.rsplit(" ", 1)[0] + "…"
    d.text((MX + 8, y + 7), chk, font=cf, fill=INK)
    y += 32
    foot = "THE WORLD IN ONE DAY  ·  news-image-20261125  ·  @giber-way  ·  make.fun"
    ff = font(SANS, 10)
    d.text(((W - d.textlength(foot, font=ff)) / 2, y), foot, font=ff, fill=MUTED)

    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    path = os.path.join(out, "entry.png") if out else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
