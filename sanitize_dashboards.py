"""
Dashboard image sanitizer.

Replaces public-facing dashboard images with anonymized versions:
- Heavy Gaussian blur (text becomes unreadable)
- Subtle warm cream wash (signals 'this is a preview, not raw data')
- Small caption: 'INDICATIVE LAYOUT — NUMBERS ANONYMIZED'

Originals are preserved in `_originals_backup/` so this is reversible.

Run from anywhere:
    py sanitize_dashboards.py
"""

import os
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---- Settings ---------------------------------------------------------------

REPO = Path(__file__).resolve().parent
DASHBOARDS_DIR = REPO / "assets" / "projects" / "dashboards"
BACKUP_DIR = DASHBOARDS_DIR / "_originals_backup"

BLUR_RADIUS = 13                                # higher = more illegible
TINT_RGB = (255, 251, 245)                      # cream
TINT_AMOUNT = 0.08                              # 0..1
CAPTION = "INDICATIVE LAYOUT  —  NUMBERS ANONYMIZED"
CAPTION_BG = (15, 41, 66, 235)                  # navy
CAPTION_FG = (255, 251, 245, 255)               # cream
CAPTION_ACCENT = (198, 139, 63, 255)            # amber

# ---- Helpers ----------------------------------------------------------------

def _load_font(size: int):
    """Load a Windows serif/sans font; fall back to default if none found."""
    candidates = [
        r"C:\Windows\Fonts\georgiab.ttf",  # Georgia Bold
        r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\seguisb.ttf",   # Segoe UI Semibold
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()

# ---- Core -------------------------------------------------------------------

def sanitize(jpg_path: Path):
    """Sanitize one image in place, backing up the original first."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / jpg_path.name
    if not backup.exists():
        shutil.copy2(jpg_path, backup)

    src = Image.open(backup).convert("RGB")
    w, h = src.size

    # 1. Heavy blur to make text unreadable
    img = src.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))

    # 2. Subtle cream tint
    tint = Image.new("RGB", (w, h), TINT_RGB)
    img = Image.blend(img, tint, TINT_AMOUNT)

    # 3. Caption pill, bottom-left
    img = img.convert("RGBA")
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = max(16, h // 36)
    font = _load_font(font_size)
    bbox = draw.textbbox((0, 0), CAPTION, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    pad_x, pad_y = int(font_size * 1.2), int(font_size * 0.7)
    box_w, box_h = tw + 2 * pad_x, th + 2 * pad_y

    # Position bottom-left with margin
    margin = max(20, h // 40)
    x = margin
    y = h - box_h - margin

    # Pill background
    radius = box_h // 2
    draw.rounded_rectangle(
        (x, y, x + box_w, y + box_h),
        radius=radius,
        fill=CAPTION_BG,
    )

    # Amber dot accent
    dot_r = max(3, font_size // 4)
    dot_cx = x + pad_x // 2 + dot_r
    dot_cy = y + box_h // 2
    draw.ellipse(
        (dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r),
        fill=CAPTION_ACCENT,
    )

    # Caption text
    draw.text((x + pad_x + dot_r, y + pad_y - bbox[1]), CAPTION, fill=CAPTION_FG, font=font)

    img = Image.alpha_composite(img, overlay).convert("RGB")
    img.save(jpg_path, "JPEG", quality=86, optimize=True)
    print(f"  [done] {jpg_path.name}  ({w}x{h})")


def main():
    if not DASHBOARDS_DIR.exists():
        raise SystemExit(f"Dashboards directory not found: {DASHBOARDS_DIR}")

    targets = [p for p in DASHBOARDS_DIR.glob("*.jpg") if not p.name.startswith("_")]
    if not targets:
        raise SystemExit("No .jpg files found to sanitize.")

    print(f"Sanitizing {len(targets)} dashboard image(s)...")
    print(f"  Originals preserved in: {BACKUP_DIR}")
    print()

    for p in sorted(targets):
        sanitize(p)

    print()
    print("Done. To revert, copy files from _originals_backup/ back over the originals.")


if __name__ == "__main__":
    main()
