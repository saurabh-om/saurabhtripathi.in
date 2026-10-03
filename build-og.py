#!/usr/bin/env python3
"""Compose the Open Graph / Twitter social preview image.

Output: assets/img/og/og-image.png at 1200x630.
Uses the site's self-hosted fonts, so it runs anywhere Pillow does.
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PORTRAIT = os.path.join(ROOT, "assets/img/portrait/saurabh-sticker-1200.jpg")
ARROW = os.path.join(ROOT, "assets/img/logo/arrow.png")
ARCHIVO = os.path.join(ROOT, "assets/fonts/archivo-latin.woff2")
GEIST = os.path.join(ROOT, "assets/fonts/geist-latin.woff2")
OUT = os.path.join(ROOT, "assets/img/og/og-image.png")

W, H = 1200, 630
BG = (14, 14, 14)        # #0E0E0E
FG = (242, 239, 233)     # #F2EFE9
MUTED = (154, 149, 141)  # #9A958D
LINE = (52, 51, 49)
ACCENT = (255, 117, 31)  # #FF751F
LEFT = 64


def font(path, size, weight, width=None):
    f = ImageFont.truetype(path, size)
    axes = [weight] if width is None else [weight, width]
    f.set_variation_by_axes(axes)
    return f


def tracked(d, xy, text, f, fill, tracking):
    """Draw text with letter-spacing, keeping the font's own kerning."""
    x, y = xy
    for i, ch in enumerate(text):
        d.text((x + f.getlength(text[:i]) + i * tracking, y), ch, font=f, fill=fill)


canvas = Image.new("RGB", (W, H), BG)

# Portrait on the right, anchored to the bottom edge. Its background is
# already graded to the page tone, so it sits on the canvas without a frame.
port = Image.open(PORTRAIT).convert("RGB")
size = 640
port = port.resize((size, size), Image.LANCZOS)
canvas.paste(port, (W - size + 40, H - size + 40))

d = ImageDraw.Draw(canvas)

# Arrow mark, top right
arrow = Image.open(ARROW).convert("RGBA")
arrow.thumbnail((44, 44), Image.LANCZOS)
canvas.paste(arrow, (W - 44 - 56, 52), arrow)

# Label
tracked(d, (LEFT, 62), "SAURABHTRIPATHI.IN", font(GEIST, 17, 600), ACCENT, 1.2)

# Name, two lines
name = font(ARCHIVO, 112, 800, 100)
tr = -0.045 * 112
tracked(d, (LEFT - 4, 104), "Saurabh", name, FG, tr)
tracked(d, (LEFT - 4, 206), "Tripathi", name, FG, tr)

# Tagline
tag = font(GEIST, 30, 500)
d.text((LEFT, 350), "Digital marketer. Builder.", font=tag, fill=FG)
d.text((LEFT, 390), "Founder of Opus Momentum.", font=tag, fill=FG)

# Lede
lede = font(GEIST, 21, 400)
d.text((LEFT, 452), "Ten years of figuring out what actually moves", font=lede, fill=MUTED)
d.text((LEFT, 482), "numbers for businesses online.", font=lede, fill=MUTED)

# Bottom rule + metadata
d.line([(LEFT, H - 92), (LEFT + 520, H - 92)], fill=LINE, width=1)
d.rectangle([LEFT, H - 66, LEFT + 8, H - 58], fill=ACCENT)
d.text((LEFT + 20, H - 72), "Bhopal · India · Working across time zones", font=font(GEIST, 17, 400), fill=MUTED)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
canvas.save(OUT, "PNG", optimize=True)
print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes)")
