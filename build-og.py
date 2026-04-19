#!/usr/bin/env python3
"""Compose the Open Graph / Twitter social preview image.

Output: assets/img/og/og-image.png at 1200x630.
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PORTRAIT = os.path.join(ROOT, "assets/img/portrait/saurabh-1200.jpg")
ARROW = os.path.join(ROOT, "assets/img/logo/arrow.png")
OUT = os.path.join(ROOT, "assets/img/og/og-image.png")

W, H = 1200, 630
BG = (250, 247, 242)   # #FAF7F2 cream
INK = (26, 26, 26)     # #1A1A1A
MUTED = (107, 104, 98) # #6B6862
ACCENT = (255, 117, 31) # #FF751F

FONT_SERIF = "/System/Library/Fonts/NewYork.ttf"
FONT_SERIF_ITALIC = "/System/Library/Fonts/NewYorkItalic.ttf"
FONT_SANS = "/System/Library/Fonts/Helvetica.ttc"

canvas = Image.new("RGB", (W, H), BG)

# --- Left column: portrait, cropped to a tall rectangle
port = Image.open(PORTRAIT).convert("RGB")
# Center-crop to 420x520 from a square source
target_w, target_h = 420, 520
ratio = max(target_w / port.width, target_h / port.height)
new_w, new_h = int(port.width * ratio), int(port.height * ratio)
port = port.resize((new_w, new_h), Image.LANCZOS)
# center crop, biased upward so the face stays in frame
left = (new_w - target_w) // 2
top = max(0, int((new_h - target_h) * 0.3))
port = port.crop((left, top, left + target_w, top + target_h))

# Soft rounded corners via a mask
mask = Image.new("L", (target_w, target_h), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle((0, 0, target_w, target_h), radius=10, fill=255)
# Paste portrait with a 14px orange accent frame behind
frame_pad = 14
# Accent frame (offset to bottom-right slightly)
frame_x, frame_y = 78, 60
accent_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
ad = ImageDraw.Draw(accent_layer)
ad.rounded_rectangle((0, 0, target_w, target_h), radius=10, outline=ACCENT, width=3)
canvas.paste(accent_layer, (frame_x + frame_pad, frame_y + frame_pad), accent_layer)
canvas.paste(port, (frame_x, frame_y), mask)

# --- Right column: text
right_x = 560
# Arrow mark (small, accent color) in top-right
try:
    arrow = Image.open(ARROW).convert("RGBA")
    arrow.thumbnail((56, 56), Image.LANCZOS)
    canvas.paste(arrow, (W - 56 - 60, 48), arrow)
except Exception:
    pass

d = ImageDraw.Draw(canvas)

# Eyebrow
try:
    eyebrow = ImageFont.truetype(FONT_SANS, 18, index=0)
except Exception:
    eyebrow = ImageFont.load_default()
d.text((right_x, 70), "SAURABHTRIPATHI.IN", font=eyebrow, fill=ACCENT, spacing=2)

# Name — large serif
title_font = ImageFont.truetype(FONT_SERIF, 78)
d.text((right_x, 110), "Saurabh Tripathi", font=title_font, fill=INK)

# Tagline — serif italic
tag_font = ImageFont.truetype(FONT_SERIF_ITALIC, 34)
d.text((right_x, 212), "Digital marketer. Builder.", font=tag_font, fill=INK)
d.text((right_x, 254), "Founder of Opus Momentum.", font=tag_font, fill=INK)

# Lede — sans
lede_font = ImageFont.truetype(FONT_SANS, 22, index=0)
lede_line1 = "Ten years of figuring out what actually moves"
lede_line2 = "numbers for businesses online."
d.text((right_x, 340), lede_line1, font=lede_font, fill=MUTED)
d.text((right_x, 372), lede_line2, font=lede_font, fill=MUTED)

# Bottom rule + metadata
d.line([(right_x, H - 110), (W - 60, H - 110)], fill=(26, 26, 26, 60), width=1)
footer_font = ImageFont.truetype(FONT_SANS, 18, index=0)
d.text((right_x, H - 84), "Bhopal · India · Working across time zones", font=footer_font, fill=MUTED)

# Save
os.makedirs(os.path.dirname(OUT), exist_ok=True)
canvas.save(OUT, "PNG", optimize=True)
print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes)")
