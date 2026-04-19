#!/usr/bin/env python3
from PIL import Image, ImageOps
from pathlib import Path

SRC = Path("/Users/saurabhtripathi/Saurabh Personal Website/Photos")
OUT = Path("/Users/saurabhtripathi/Saurabh Personal Website/saurabhtripathi.in/assets/img/portrait")
OUT.mkdir(parents=True, exist_ok=True)


def save_jpg(img, path, w, quality=82):
    if img.width != w:
        h = round(img.height * (w / img.width))
        img = img.resize((w, h), Image.LANCZOS)
    img.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    print(f"  → {path.name}  {img.width}x{img.height}  ({path.stat().st_size/1024:.0f} KB)")


print("Speaking / podium photo (MSME event) — keep full landscape")
src = Image.open(SRC / "IMG_9616~2.JPG")
src = ImageOps.exif_transpose(src).convert("RGB")
print(f"  source {src.width}x{src.height}")
save_jpg(src, OUT / "speaking-1600.jpg", 1600, quality=82)
save_jpg(src, OUT / "speaking-800.jpg", 800, quality=80)

print("\nMic photo — crop out bottom person, keep tall portrait")
src2 = Image.open(SRC / "Screenshot_2022-05-30-22-06-51-295_com.google.android.apps.photos.jpg")
src2 = ImageOps.exif_transpose(src2).convert("RGB")
print(f"  source {src2.width}x{src2.height}")
W, H = src2.size
crop_box = (0, 0, W, int(H * 0.62))
cropped = src2.crop(crop_box)
print(f"  cropped {cropped.width}x{cropped.height}")
save_jpg(cropped, OUT / "mic-1200.jpg", 1200, quality=82)
save_jpg(cropped, OUT / "mic-600.jpg", 600, quality=80)

print("\nDone.")
