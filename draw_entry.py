"""Draw the front page for Tuesday 24 November 2026.

A single broadsheet-style page, "The World in One Day", rendered with
Pillow only: no network, no outside files. Run it and it writes
entry.png beside this file, 1024 by 1024 pixels.

The day's stories, all verified against reporting dated Tuesday
24 November 2026 (each from at least two reputable sources): Israel
kills Hamas' internal security chief in Gaza City; a Russian overnight
strike on Zaporizhzhia kills two and wounds forty; Sanofi agrees to
buy Insmed for $41 billion; Real Madrid come from behind to thrash PSV
5-1 in the Champions League; plus briefs on the Ebola team evacuated
in Ituri, Baghdad's move on Kurdish oilfields, and Russian jets
buzzing South Korea's air defence zone.

Stories deliberately left out because their date is not 24 November:
Nvidia reinstating Jensen Huang (Mon 23 Nov), the ICJ's Myanmar
genocide ruling (Thu 19 Nov), the UK's Myanmar sanctions (Mon 23 Nov),
NATO's space press conference (Mon 23 Nov), the COP31 collapse
(Sun 22 Nov), the US losing measles elimination status (17 Nov),
the Grok lawsuits filed by Virginia and Oregon (Mon 23 Nov), the
Germany-Ukraine DELTA signing (Mon 23 Nov), and the Benghazi
corvette strike (Mon 23 Nov).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 239, 223)
INK = (26, 24, 21)
SOFT = (96, 91, 84)
RED = (198, 32, 38)
NAVY = (31, 44, 66)
DUSK = (52, 66, 92)
GOLD = (212, 186, 112)
RULE = (180, 172, 154)

FONTS = "/usr/share/fonts/truetype/dejavu/"
SANS_B = FONTS + "DejaVuSans-Bold.ttf"
SANS = FONTS + "DejaVuSans.ttf"
SERIF_B = FONTS + "DejaVuSerif-Bold.ttf"
SERIF = FONTS + "DejaVuSerif.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))


def face(path, size):
    return ImageFont.truetype(path, size)


def width(d, text, f):
    box = d.textbbox((0, 0), text, font=f)
    return box[2] - box[0]


def wrap_text(d, text, f, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if width(d, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def biggest_fit(d, text, path, max_w, max_lines, start, smallest):
    """Largest size (<= start) where text wraps into max_lines."""
    for size in range(start, smallest - 1, -1):
        f = face(path, size)
        lines = wrap_text(d, text, f, max_w)
        if len(lines) <= max_lines and all(
            width(d, ln, f) <= max_w for ln in lines
        ):
            return f, lines
    raise SystemExit("does not fit: " + text)


def write_lines(d, x, y, lines, f, fill, gap=1.18):
    asc, desc = f.getmetrics()
    step = int((asc + desc) * gap)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += step
    return y


def centred(d, cx, y, text, f, fill):
    d.text((cx - width(d, text, f) // 2, y), text, font=f, fill=fill)


def hline(d, x0, y, x1, w=2):
    d.line((x0, y, x1, y), fill=INK, width=w)


def kick(d, x, y, text):
    d.text((x, y), text, font=face(SANS_B, 19), fill=RED)
    return y + 26


# ------------------------------------------------------------------- artwork

def gaza_panel(d, x0, y0, x1, y1):
    """Gaza City at dusk: navy sky, a red sun, skyline, smoke columns."""
    d.rectangle((x0, y0, x1, y1), fill=NAVY)
    # red sun, low over the skyline
    sx, sy, sr = x1 - 78, y0 + 66, 34
    d.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=RED)
    # skyline: a row of dark blocks of uneven height
    base = y1 - 92
    blocks = [
        (0, 120, 70), (0.13, 90, 110), (0.28, 150, 60), (0.42, 110, 130),
        (0.58, 140, 80), (0.72, 100, 120), (0.86, 120, 66),
    ]
    span = x1 - x0
    for frac, bw, bh in blocks:
        bx = x0 + int(frac * span)
        bw = min(bw, x1 - bx - 4)
        d.rectangle((bx, base - bh, bx + bw, base), fill=DUSK)
        # a few lit windows
        for wy in range(base - bh + 12, base - 8, 26):
            for wx in range(bx + 10, bx + bw - 10, 24):
                if (wx + wy) % 3 == 0:
                    d.rectangle((wx, wy, wx + 6, wy + 8), fill=GOLD)
    # a minaret silhouette rising from the skyline, left of the sun
    min_x = x0 + 180
    d.rectangle((min_x, base - 140, min_x + 10, base), fill=DUSK)
    d.polygon([(min_x - 4, base - 140), (min_x + 14, base - 140),
               (min_x + 5, base - 162)], fill=DUSK)
    # caption strip
    d.rectangle((x0, y1 - 52, x1, y1), fill=INK)
    d.text((x0 + 18, y1 - 42), "GAZA CITY \u2014 7 DEAD TUESDAY",
           font=face(SANS_B, 17), fill=PAPER)


def jet_mark(d, cx, cy, s):
    """A paper-plane dart, nose up-right."""
    d.polygon([(cx - s, cy + s // 2), (cx + s, cy - s // 2),
               (cx + s // 4, cy + s // 4), (cx - s // 4, cy + s)],
              fill=INK)


def cross_mark(d, cx, cy, r):
    """Rescue cross in red inside a ring."""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=RED, width=3)
    d.rectangle((cx - 6, cy - r + 10, cx + 6, cy + r - 10), fill=RED)
    d.rectangle((cx - r + 10, cy - 6, cx + r - 10, cy + 6), fill=RED)


def dollar_mark(d, cx, cy, r):
    """A coin with a dollar sign."""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GOLD)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=INK, width=2)
    d.text((cx - 7, cy - 15), "$", font=face(SANS_B, 26), fill=INK)


def drop_mark(d, cx, cy, r):
    """An oil drop in ink."""
    d.polygon([(cx, cy - r), (cx + r // 2, cy - r // 4),
               (cx + r // 2, cy + r // 2), (cx - r // 2, cy + r // 2),
               (cx - r // 2, cy - r // 4)], fill=INK)
    d.ellipse((cx - r // 2, cy, cx + r // 2, cy + r), fill=INK)


def ball_mark(d, cx, cy, r):
    """Football: a circle with a dark pentagon and seams."""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=INK, width=3)
    d.polygon([(cx, cy - r // 2), (cx + r // 2, cy - r // 6),
               (cx + r // 3, cy + r // 2), (cx - r // 3, cy + r // 2),
               (cx - r // 2, cy - r // 6)], fill=INK)
    for ex, ey in ((cx, cy - r), (cx + r, cy), (cx - r, cy),
                   (cx + r // 2, cy + r), (cx - r // 2, cy + r)):
        d.line((cx, cy - r // 2, ex, ey), fill=INK, width=2)


# ---------------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 36
    RX = W - MX

    # masthead
    hline(d, MX, 24, RX, 3)
    f, lines = biggest_fit(d, "THE WORLD IN ONE DAY", SERIF_B,
                           RX - MX, 1, 64, 40)
    y = 34
    for ln in lines:
        centred(d, W // 2, y, ln, f, INK)
        y += 78
    centred(d, W // 2, 114, "ONE DAY  ·  ONE PAGE  ·  THE WORLD'S NEWS",
            face(SANS_B, 15), SOFT)
    hline(d, MX, 138, RX, 2)

    # date band
    d.rectangle((MX, 146, RX, 184), fill=INK)
    centred(d, W // 2, 154, "TUESDAY,  24  NOVEMBER  2026",
            face(SANS_B, 27), PAPER)

    # ---- lead: Gaza
    ly = 200
    y = kick(d, MX, ly, "LEAD  ·  GAZA")
    f, lines = biggest_fit(d, "ISRAEL KILLS HAMAS SECURITY CHIEF",
                           SERIF_B, 566, 2, 52, 34)
    y = write_lines(d, MX, y + 4, lines, f, INK, 1.02)
    y = write_lines(d, MX, y + 8, ["Seven dead as airstrikes hit Gaza City"],
                    face(SANS_B, 24), INK)
    body = ("An Israeli airstrike kills Naeem Abu Nahel, director of "
            "Hamas' internal security apparatus, in western Gaza City "
            "on Tuesday, along with six others including two police "
            "officers. Benjamin Netanyahu and Defence Minister Israel "
            "Katz say Abu Nahel was \u2018eliminated\u2019.")
    write_lines(d, MX, y + 12, wrap_text(d, body, face(SERIF, 18), 566),
                face(SERIF, 18), INK, 1.18)
    gaza_panel(d, 622, ly, RX, 505)
    hline(d, MX, 520, RX, 2)

    # ---- second row: Zaporizhzhia (left) and Champions League (right)
    ry = 536
    d.line((512, ry, 512, 736), fill=RULE, width=2)
    y = kick(d, MX, ry, "UKRAINE  ·  ZAPORIZHZHIA")
    f, lines = biggest_fit(d, "OVERNIGHT STRIKE KILLS TWO",
                           SERIF_B, 464, 2, 30, 24)
    y = write_lines(d, MX, ry + 34, lines, f, INK, 1.04)
    body = ("A Russian attack on the city of Zaporizhzhia overnight "
            "kills two people and wounds 40, including four children, "
            "regional governor Mykhailo Semikin says. A five-storey "
            "apartment block is partly destroyed and rescuers search "
            "the rubble.")
    write_lines(d, MX, y + 6, wrap_text(d, body, face(SERIF, 16), 464),
                face(SERIF, 16), INK, 1.15)

    ball_mark(d, 548, 552, 16)
    y = kick(d, 576, ry, "SPORT  ·  CHAMPIONS LEAGUE")
    f, lines = biggest_fit(d, "MADRID HIT FIVE IN COMEBACK",
                           SERIF_B, 412, 2, 30, 24)
    y = write_lines(d, 524, ry + 34, lines, f, INK, 1.04)
    body = ("Real Madrid come from a goal down at half-time to thrash "
            "PSV 5\u20131 and keep their perfect start.")
    y = write_lines(d, 524, y + 6,
                    wrap_text(d, body, face(SERIF, 16), 464),
                    face(SERIF, 16), INK, 1.15)
    scores = ("Bod\u00f8/Glimt 1\u20130 LASK  ·  Galatasaray 1\u20130 Villa  ·  "
              "Arsenal 1\u20131 Dortmund  ·  Como 1\u20130 AEK  ·  Feyenoord "
              "0\u20131 Porto  ·  Man City 2\u20132 Napoli  ·  Leipzig 3\u20131 "
              "Lens  ·  Real Madrid 5\u20131 PSV  ·  Bratislava 0\u20132 Betis")
    write_lines(d, 524, y + 8,
                wrap_text(d, scores, face(SANS, 12), 464),
                face(SANS, 12), SOFT, 1.25)
    hline(d, MX, 766, RX, 2)

    # ---- briefs: four columns
    by = 782
    cols = [
        (MX, "BUSINESS  ·  PARIS", "SANOFI BUYS INSMED, $41BN",
         "Sanofi agrees to buy US drugmaker Insmed for $41 billion in "
         "cash \u2014 $175 a share \u2014 the year's biggest pharma deal.",
         "dollar"),
        (272, "HEALTH  ·  DR CONGO", "EBOLA TEAM EVACUATED",
         "WHO staff are evacuated from a hospital in Akwe, Ituri, after "
         "sheltering three days in a maternity ward as fighting raged.",
         "cross"),
        (508, "MIDEAST  ·  BAGHDAD", "IRAQ MOVES ON KURD OIL",
         "Prime Minister Ali al-Zaidi orders Baghdad to take over "
         "Kurdish oilfields and border crossings; the Kurdish region "
         "rejects the move.", "drop"),
        (744, "ASIA  ·  SEOUL", "JETS SCRAMBLED OVER ADIZ",
         "South Korea scrambles F-15Ks as Russian warplanes enter its "
         "air defence zone near Ulleungdo; a shelter alert is lifted "
         "minutes later.", "jet"),
    ]
    for x, kick_text, head, body, icon in cols:
        if icon == "dollar":
            dollar_mark(d, x + 18, by + 18, 18)
        elif icon == "cross":
            cross_mark(d, x + 18, by + 18, 18)
        elif icon == "drop":
            drop_mark(d, x + 18, by + 18, 18)
        else:
            jet_mark(d, x + 18, by + 18, 20)
        d.text((x + 44, by + 8), kick_text, font=face(SANS_B, 13), fill=RED)
        f, lines = biggest_fit(d, head, SERIF_B, 216, 2, 20, 17)
        y = write_lines(d, x, by + 40, lines, f, INK, 1.04)
        write_lines(d, x, y + 6,
                    wrap_text(d, body, face(SERIF, 12), 216),
                    face(SERIF, 12), INK, 1.15)

    # footer
    hline(d, MX, 972, RX, 1)
    centred(d, W // 2, 982,
            "Sources: Reuters  ·  BBC  ·  AP  ·  WSJ  ·  UN News  ·  UEFA",
            face(SANS, 14), SOFT)
    return img


def main():
    img = build()
    img.save(os.path.join(HERE, "entry.png"), optimize=True)


if __name__ == "__main__":
    main()
