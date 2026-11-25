#!/usr/bin/env python3
"""News image: one picture summing up Wednesday 25 November 2026.

Draws a newspaper front page (1024x1024 PNG) with six verified stories
reported on 25 November 2026, using only Pillow and the DejaVu fonts
shipped with the system. Fully deterministic: no clock, no random
numbers, no network, no external files. Run: python3 main.py
Output: $MAKEFUN_OUTPUT_DIR/entry.png (default: out/entry.png)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 232)
INK = (20, 28, 46)
RED = (178, 34, 34)
NAVY = (23, 42, 78)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# (kicker, headline, body, accent colour, pictogram key)
STORIES = [
    ("SPACE", "China launches Shenzhou-24",
     "First Pakistani in orbit: Muhammad Zeeshan Ali joins Tang Hongbo "
     "and Wu Yi aboard the Tiangong space station.",
     (31, 90, 140), "rocket"),
    ("UKRAINE WAR", "Zelenskiy confirms ship strike",
     "Ukraine says it hit a Russian cargo ship in the Gulf of Finland; "
     "ally Norway urges caution in such operations.",
     (120, 40, 40), "ship"),
    ("MIDDLE EAST", "Houthi strike hits Riyadh tower",
     "An attack on the Saudi capital's tallest tower wounds 11 people, "
     "Saudi civil defence says.",
     (150, 90, 20), "tower"),
    ("TECH", "Microsoft declares 'Code Red'",
     "Reuters reports memos ordering a reliability overhaul after a "
     "day-long Microsoft 365 outage hit Outlook and Teams.",
     (30, 90, 90), "laptop"),
    ("SPORT", "15-year-old smashes 204 off 53",
     "Vaibhav Suryavanshi hits the fastest List A double hundred in "
     "cricket history.",
     (40, 110, 50), "cricket"),
    ("EUROPE", "Sarkozy case sent to trial",
     "A French court orders ex-president Nicolas Sarkozy and his wife "
     "Carla Bruni to stand trial in a corruption case.",
     (80, 60, 120), "court"),
]

ALSO_TODAY = ("ALSO TODAY:  South Korea's education minister resigns over an "
               "exam-cheating scandal.  |  Gunmen seize hostages in a "
               "Cartagena supermarket after a failed cash-truck robbery.")


def draw_pictogram(d, key, x, y, s, colour):
    """Small flat pictogram drawn from shapes only."""
    if key == "rocket":
        d.polygon([(x + s * .5, y), (x + s * .75, y + s * .55),
                   (x + s * .25, y + s * .55)], fill=colour)
        d.rectangle([x + s * .38, y + s * .5, x + s * .62, y + s * .8],
                    fill=colour)
        d.polygon([(x + s * .15, y + s * .95), (x + s * .38, y + s * .7),
                   (x + s * .38, y + s * .95)], fill=(230, 120, 40))
        d.polygon([(x + s * .85, y + s * .95), (x + s * .62, y + s * .7),
                   (x + s * .62, y + s * .95)], fill=(230, 120, 40))
        d.ellipse([x + s * .42, y + s * .28, x + s * .58, y + s * .44],
                  fill=(255, 255, 255))
    elif key == "ship":
        d.polygon([(x, y + s * .55), (x + s, y + s * .55),
                   (x + s * .85, y + s * .85), (x + s * .15, y + s * .85)],
                  fill=colour)
        d.rectangle([x + s * .45, y + s * .1, x + s * .55, y + s * .55],
                    fill=colour)
        d.polygon([(x + s * .55, y + s * .1), (x + s * .55, y + s * .4),
                   (x + s * .9, y + s * .4)], fill=(230, 120, 40))
        d.rectangle([x, y + s * .9, x + s, y + s], fill=(60, 130, 180))
    elif key == "tower":
        d.rectangle([x + s * .35, y, x + s * .65, y + s], fill=colour)
        d.rectangle([x + s * .2, y + s * .3, x + s * .8, y + s * .38],
                    fill=colour)
        d.polygon([(x + s * .5, y - s * .12), (x + s * .62, y),
                   (x + s * .38, y)], fill=(230, 120, 40))
        for i in range(4):
            d.rectangle([x + s * .42, y + s * (.15 + i * .2),
                         x + s * .58, y + s * (.23 + i * .2)],
                        fill=(255, 220, 120))
    elif key == "laptop":
        d.rectangle([x + s * .1, y + s * .15, x + s * .9, y + s * .7],
                    fill=colour)
        d.rectangle([x + s * .18, y + s * .23, x + s * .82, y + s * .62],
                    fill=(255, 255, 255))
        d.text((x + s * .32, y + s * .32), "!", font=font(FONT_BOLD, 34),
               fill=(178, 34, 34))
        d.rectangle([x, y + s * .7, x + s, y + s * .82], fill=colour)
    elif key == "cricket":
        d.ellipse([x + s * .55, y + s * .1, x + s * .95, y + s * .5],
                  fill=(178, 34, 34))
        d.rectangle([x + s * .3, y + s * .45, x + s * .45, y + s * .9],
                    fill=(190, 150, 90))
        d.rectangle([x + s * .22, y + s * .38, x + s * .53, y + s * .52],
                    fill=(150, 110, 60))
        d.line([x + s * .1, y + s * .95, x + s * .9, y + s * .95],
               fill=colour, width=5)
    elif key == "court":
        d.polygon([(x, y + s * .25), (x + s * .5, y),
                   (x + s, y + s * .25)], fill=colour)
        for i in range(3):
            cx = x + s * (.2 + i * .3)
            d.rectangle([cx - 6, y + s * .3, cx + 6, y + s * .85],
                        fill=colour)
        d.rectangle([x, y + s * .85, x + s, y + s], fill=colour)


def build_image():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # Masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((512, 18), "THE WORLD IN ONE DAY",
           font=font(FONT_SERIF, 52), fill=(255, 255, 255), anchor="ma")
    d.text((512, 78), "WEDNESDAY  25  NOVEMBER  2026",
           font=font(FONT_BOLD, 30), fill=(255, 210, 90), anchor="ma")
    d.rectangle([0, 118, W, 126], fill=RED)
    # Panels: 2 columns x 3 rows
    gx, gy, pw, ph, gap = 24, 142, 476, 236, 12
    f_kick = font(FONT_BOLD, 22)
    f_head = font(FONT_BOLD, 27)
    f_body = font(FONT_REG, 22)
    for i, (kick, head, body, colour, pic) in enumerate(STORIES):
        px = gx + (i % 2) * (pw + gap)
        py = gy + (i // 2) * (ph + gap)
        d.rectangle([px, py, px + pw, py + ph], fill=(255, 255, 255),
                    outline=(200, 195, 180), width=2)
        d.rectangle([px, py, px + pw, py + 34], fill=colour)
        d.text((px + 12, py + 5), kick, font=f_kick, fill=(255, 255, 255))
        draw_pictogram(d, pic, px + pw - 92, py + 48, 72, colour)
        lines = wrap(d, head, f_head, pw - 120)
        y = py + 44
        for ln in lines[:2]:
            d.text((px + 12, y), ln, font=f_head, fill=INK)
            y += 32
        blines = wrap(d, body, f_body, pw - 24)
        y = py + 118
        for ln in blines[:4]:
            d.text((px + 12, y), ln, font=f_body, fill=(50, 50, 50))
            y += 27
    # Footer strip
    fy = gy + 3 * ph + 2 * gap + 8
    d.rectangle([24, fy, W - 24, fy + 64], fill=NAVY)
    flines = wrap(d, ALSO_TODAY, font(FONT_REG, 20), W - 72)
    y = fy + 6
    for ln in flines[:2]:
        d.text((36, y), ln, font=font(FONT_REG, 20), fill=(255, 255, 255))
        y += 26
    # Source line: every story above was reported on 25 November 2026.
    d.text((512, fy + 78),
           "Sources: Reuters, Xinhua, The Hindu — all stories reported "
           "on 25 November 2026.",
           font=font(FONT_REG, 18), fill=(90, 85, 70), anchor="ma")
    return img


def self_check(path):
    """Gate self-check: PNG magic, dimensions, size, and sha256."""
    import hashlib
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG file"
    assert len(data) <= 1048576, "image over 1 MiB"
    img = Image.open(path)
    assert img.size == (1024, 1024), f"unexpected size {img.size}"
    digest = hashlib.sha256(data).hexdigest()
    print(f"self-check PASS: PNG 1024x1024, {len(data)} bytes, "
          f"sha256={digest}")
    return digest


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img = build_image()
    img.save(path, format="PNG")
    size = os.path.getsize(path)
    assert img.size[0] <= 1024 and img.size[1] <= 1024, "image too large"
    assert size <= 1048576, "image over 1 MiB"
    print(f"Wrote {path} ({img.size[0]}x{img.size[1]}, {size} bytes)")
    self_check(path)


if __name__ == "__main__":
    main()
