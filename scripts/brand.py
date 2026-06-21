"""Identidad visual ARVION (estilo C aprobado). Compartido por los renders."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")

WHITE = (255, 255, 255, 255)
BLUE  = (110, 190, 255, 255)   # azul ARVION para acentos
GLOW  = (46, 134, 255)         # glow azul
GRAY  = (195, 210, 230, 255)

def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

def F_title(size): return font("Montserrat-800.ttf", size)
def F_body(size):  return font("Sora-600.ttf", size)

def cover_fit(im, W, H):
    im = im.convert("RGBA")
    r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r), int(im.height * r)))
    x = (im.width - W) // 2; y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

def scrim_bottom(img, W, H, frac=0.58, strength=225):
    g = Image.new("L", (1, H), 0)
    for yy in range(H):
        t = max(0, (yy - (1 - frac) * H) / (frac * H))
        g.putpixel((0, yy), int(strength * max(0, min(1, t)) ** 1.3))
    black = Image.new("RGBA", (W, H), (0, 0, 0, 255)); black.putalpha(g.resize((W, H)))
    img.alpha_composite(black)

def text(img, W, H, s, x, y, fnt, fill=WHITE, glow=False):
    if glow:
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(gl).text((x, y), s, font=fnt, fill=GLOW + (255,))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(img)
    d.text((x + 1, y + 2), s, font=fnt, fill=(0, 0, 0, 150))
    d.text((x, y), s, font=fnt, fill=fill)

def accent(img, x, y, w=160):
    ImageDraw.Draw(img).rectangle([x, y, x + w, y + 6], fill=BLUE)
