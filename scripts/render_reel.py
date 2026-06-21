#!/usr/bin/env python3
"""Render de reel ARVION (estilo C) desde JSON: overlays nitidos + transiciones + musica.
Uso: python3 render_reel.py config.json
Config:
{
  "out": "output/reel.mp4",
  "size": [720,1280], "clip_dur": 5.0, "xfade": 0.5,
  "music": "assets/music/01-calm-aspirational.mp3",
  "scenes": [
    {"video":"s1.mp4","fade":"in","accent_y":0.625,
     "overlay":[{"lines":[["Mientras ",0],["duermes…",1]],"y":0.66,"size":54}]},
    {"video":"s2.mp4","accent_y":0.585,
     "overlay":[{"lines":[["tu IA atiende,",0]],"y":0.62,"size":48},
                {"lines":[["agenda y ",0],["vende.",1]],"y":0.685,"size":48}]},
    {"video":"s3.mp4","fade":"out","accent_y":0.545,"brand":true,
     "overlay":[{"lines":[["Despiertas con",0]],"y":0.58,"size":46},
                {"lines":[["clientes ",0],["nuevos.",1]],"y":0.645,"size":46}]}
  ]
}
"""
import sys, os, json, subprocess
from PIL import Image, ImageDraw, ImageFilter
from brand import font, F_title, WHITE, BLUE, GLOW, GRAY

def draw_line(img, W, H, segs, y_frac, size, tracking=1):
    f = font("Sora-600.ttf", size)
    txt = "".join(s[0] for s in segs); widths = [f.getlength(c) for c in txt]
    total = sum(widths) + tracking * (len(txt) - 1); x = (W - total) / 2; y = int(H * y_frac)
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
    cx = x; idx = 0
    for seg in segs:
        for c in seg[0]:
            if seg[1]: gd.text((cx, y), c, font=f, fill=GLOW + (255,))
            cx += widths[idx] + tracking; idx += 1
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(9)))
    d = ImageDraw.Draw(img); cx = x; idx = 0
    for seg in segs:
        col = BLUE if seg[1] else WHITE
        for c in seg[0]:
            d.text((cx + 2, y + 3), c, font=f, fill=(0, 0, 0, 150))
            d.text((cx, y), c, font=f, fill=col); cx += widths[idx] + tracking; idx += 1

def build_overlay(scene, W, H, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # velo inferior para legibilidad
    g = Image.new("L", (1, H), 0)
    for yy in range(H):
        t = max(0, (yy - 0.45 * H) / (0.55 * H)); g.putpixel((0, yy), int(205 * max(0, min(1, t))))
    blk = Image.new("RGBA", (W, H), (0, 0, 0, 255)); blk.putalpha(g.resize((W, H))); img.alpha_composite(blk)
    if "accent_y" in scene:
        ay = int(H * scene["accent_y"]); ImageDraw.Draw(img).rectangle([90, ay, 90 + int(W * 0.14), ay + 4], fill=BLUE)
    for ln in scene["overlay"]:
        draw_line(img, W, H, ln["lines"], ln["y"], ln["size"])
    if scene.get("brand"):
        draw_line(img, W, H, [["A R V I O N", 0]], 0.80, 46, tracking=6)
        draw_line(img, W, H, [["arviongroup.com.co", 0]], 0.852, 22, tracking=2)
    img.save(path)

def render(cfg):
    W, H = cfg.get("size", [720, 1280]); dur = cfg.get("clip_dur", 5.0); xf = cfg.get("xfade", 0.5)
    base = os.path.dirname(os.path.abspath(cfg["__path__"]))
    out = os.path.join(base, cfg["out"]); os.makedirs(os.path.dirname(out), exist_ok=True)
    scenes = cfg["scenes"]; N = len(scenes)
    ov_paths = []
    for i, s in enumerate(scenes):
        p = os.path.join(os.path.dirname(out), f"_ov{i}.png"); build_overlay(s, W, H, p); ov_paths.append(p)
    # inputs: videos, overlays, music
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for s in scenes: cmd += ["-i", os.path.join(base, s["video"])]
    for p in ov_paths: cmd += ["-i", p]
    cmd += ["-i", os.path.join(base, cfg["music"])]
    fc = []
    for i, s in enumerate(scenes):
        ov = N + i; chain = f"[{i}:v]fps=30,scale={W}:{H},setsar=1[b{i}];[b{i}][{ov}:v]overlay=0:0"
        if s.get("fade") == "in":  chain += ",fade=t=in:st=0:d=0.7"
        if s.get("fade") == "out": chain += f",fade=t=out:st={dur-0.6:.2f}:d=0.6"
        chain += f",format=yuv420p[v{i}]"; fc.append(chain)
    prev = "v0"
    for k in range(1, N):
        off = k * (dur - xf); lbl = "vout" if k == N - 1 else f"x{k}"
        fc.append(f"[{prev}][v{k}]xfade=transition=fade:duration={xf}:offset={off:.2f}[{lbl}]"); prev = lbl
    total = N * dur - (N - 1) * xf
    aidx = 2 * N
    fc.append(f"[{aidx}:a]afade=t=out:st={total-1:.2f}:d=1[aout]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", out]
    subprocess.run(cmd, check=True)
    for p in ov_paths: os.remove(p)
    print("REEL OK ->", out)

if __name__ == "__main__":
    path = sys.argv[1]; cfg = json.load(open(path)); cfg["__path__"] = path; render(cfg)
