#!/usr/bin/env python3
"""Render de carrusel ARVION (estilo C) desde un JSON de config.
Uso: python3 render_carousel.py config.json
Config:
{
  "out_dir": "output/carousel-1",
  "size": [1080,1350],
  "slides": [
    {"type":"cover","image":"img1.png",
     "title":[["5 tareas",false],["que la IA ya hace",false],["por tu empresa",true]],
     "sub":"Guárdalo para no olvidarlo"},
    {"type":"content","image":"img2.png","num":1,"title":"Responde",
     "sub":["clientes 24/7,","sin mover un dedo."]},
    {"type":"cta","image":"img7.png",
     "title":[["¿Quieres esto",false],["en tu empresa?",true]],
     "sub":"Síguenos y escríbenos."}
  ]
}
"""
import sys, os, json
from PIL import Image
from brand import (cover_fit, scrim_bottom, text, accent, F_title, F_body,
                   WHITE, BLUE, GRAY)

def footer(img, W, H):
    text(img, W, H, "@arvion", 90, H - 95, F_body(32), GRAY)
    f = F_body(32); t = "arviongroup.com.co"
    text(img, W, H, t, W - 90 - int(f.getlength(t)), H - 95, f, GRAY)

def render(cfg):
    W, H = cfg.get("size", [1080, 1350])
    out = cfg["out_dir"]; os.makedirs(out, exist_ok=True)
    base = os.path.dirname(os.path.abspath(cfg["__path__"]))
    paths = []
    for i, s in enumerate(cfg["slides"], 1):
        img = cover_fit(Image.open(os.path.join(base, s["image"])), W, H)
        img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 40)))
        if s["type"] == "content":
            scrim_bottom(img, W, H)
            text(img, W, H, str(s["num"]), 90, H - 640, F_title(140), BLUE, glow=True)
            accent(img, 90, H - 430)
            text(img, W, H, s["title"], 90, H - 390, F_title(82), WHITE)
            y = H - 250
            for ln in s["sub"]:
                text(img, W, H, ln, 90, y, F_body(42), GRAY); y += 60
        else:  # cover / cta
            scrim_bottom(img, W, H, 0.62, 235)
            is_cover = s["type"] == "cover"
            size = 104 if is_cover else 80
            y = int(H * (0.40 if is_cover else 0.46))
            accent(img, 90, y - 46)
            for seg, blue in s["title"]:
                text(img, W, H, seg, 90, y, F_title(size), BLUE if blue else WHITE, glow=blue)
                y += int(size * 1.15)
            text(img, W, H, s["sub"], 90, y + 14, F_body(40), GRAY)
            if s["type"] == "cta":
                f = F_title(48); t = "A R V I O N"
                text(img, W, H, t, (W - int(f.getlength(t))) // 2, H - 180, f, WHITE)
        footer(img, W, H)
        p = os.path.join(out, f"slide{i}.png"); img.convert("RGB").save(p, quality=92); paths.append(p)
    print("CARRUSEL OK:", len(paths), "slides ->", out)
    return paths

if __name__ == "__main__":
    path = sys.argv[1]
    cfg = json.load(open(path)); cfg["__path__"] = path
    render(cfg)
