"""Generates placeholder logos. Replace Image/Logo.png and inverseLogo.png with your own branding anytime."""
from PIL import Image, ImageDraw, ImageFont

def make(path, color):
    img = Image.new("RGBA", (800, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.line([(100, 50), (100, 160)], fill=color, width=8)          # pillar
    d.line([(50, 70), (150, 70)], fill=color, width=8)            # beam
    d.line([(60, 160), (140, 160)], fill=color, width=8)          # base
    for cx in (60, 140):                                          # pans
        d.polygon([(cx - 22, 120), (cx + 22, 120), (cx, 105)], outline=color, width=5)
        d.line([(cx, 70), (cx - 22, 120)], fill=color, width=3)
        d.line([(cx, 70), (cx + 22, 120)], fill=color, width=3)
    try:
        font = ImageFont.truetype("DejaVuSerif.ttf", 84)
    except Exception:
        font = ImageFont.load_default(size=84)
    d.text((190, 55), "LegalEase", fill=color, font=font)
    img.save(path)

make("Image/Logo.png", (20, 20, 20, 255))
make("Image/inverseLogo.png", (255, 255, 255, 255))
