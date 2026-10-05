#!/usr/bin/env python3
"""
Generates the 64x64 PNG app icons shipped in icons/<app_id>.png.

Icons are shown by the GuppyScreen App Store panel. Where the upstream project
publishes a logo it is downloaded and resized; for apps without a usable logo a
simple glyph is drawn. Requires Pillow (and cairosvg for SVG sources):

    python3 -m venv /tmp/iconenv && /tmp/iconenv/bin/pip install pillow cairosvg
    /tmp/iconenv/bin/python tools/make_icons.py
"""

import io
import os
import urllib.request

from PIL import Image, ImageDraw

SIZE = 64
SS = 8  # supersampling factor for drawn glyphs
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "icons")

RAW = "https://raw.githubusercontent.com/"
UPSTREAM = {
    "spoolman": RAW + "Donkie/Spoolman/master/client/public/favicon.svg",
    "mainsail": RAW + "mainsail-crew/mainsail/develop/public/img/icons/icon-192.png",
    "fluidd": RAW + "fluidd-core/fluidd/develop/public/img/icons/android-chrome-192x192.png",
    "mobileraker": RAW + "Clon1998/mobileraker/master/assets/icon/mr_appicon.png",
    "helixscreen": RAW + "prestonbrown/helixscreen/main/assets/images/helix-icon-128.png",
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "OpenKE-AppStore-Icons/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def from_upstream(url: str) -> Image.Image:
    data = fetch(url)
    if url.endswith(".svg"):
        import cairosvg
        data = cairosvg.svg2png(bytestring=data, output_width=SIZE * 4, output_height=SIZE * 4)
    img = Image.open(io.BytesIO(data)).convert("RGBA")
    # Fit inside a square canvas preserving aspect ratio
    img.thumbnail((SIZE, SIZE), Image.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.paste(img, ((SIZE - img.width) // 2, (SIZE - img.height) // 2), img)
    return canvas


def badge(color, draw_fn) -> Image.Image:
    s = SIZE * SS
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, s - 1, s - 1), radius=s // 5, fill=color)
    draw_fn(d, s)
    return img.resize((SIZE, SIZE), Image.LANCZOS)


WHITE = (255, 255, 255, 255)


def draw_octoapp(d, s):
    # Octopus-like head with tentacles
    d.ellipse((s * .2, s * .15, s * .8, s * .7), fill=WHITE)
    for i in range(4):
        x = s * (.24 + i * .17)
        d.rounded_rectangle((x, s * .55, x + s * .11, s * .85), radius=s * .05, fill=WHITE)
    for x in (.37, .6):
        d.ellipse((s * x - s * .05, s * .35 - s * .05, s * x + s * .05, s * .35 + s * .05), fill=(0, 137, 123, 255))


def draw_guppyscreen(d, s):
    # Guppy: body, tail, eye
    d.ellipse((s * .15, s * .3, s * .7, s * .7), fill=WHITE)
    d.polygon([(s * .62, s * .5), (s * .88, s * .28), (s * .88, s * .72)], fill=WHITE)
    d.ellipse((s * .27, s * .4, s * .35, s * .48), fill=(94, 53, 177, 255))


def draw_timelapse(d, s):
    cx = cy = s / 2
    r = s * .34
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=WHITE, width=int(s * .07))
    d.line((cx, cy, cx, cy - r * .65), fill=WHITE, width=int(s * .07))
    d.line((cx, cy, cx + r * .5, cy + r * .2), fill=WHITE, width=int(s * .07))


def draw_vnc(d, s):
    d.rounded_rectangle((s * .15, s * .2, s * .85, s * .65), radius=s * .05, outline=WHITE, width=int(s * .06))
    d.rectangle((s * .43, s * .65, s * .57, s * .78), fill=WHITE)
    d.rounded_rectangle((s * .3, s * .78, s * .7, s * .85), radius=s * .03, fill=WHITE)


DRAWN = {
    "octoapp": ((0, 137, 123, 255), draw_octoapp),
    "guppyscreen": ((94, 53, 177, 255), draw_guppyscreen),
    "timelapse": ((0, 121, 107, 255), draw_timelapse),
    "vnc": ((69, 90, 100, 255), draw_vnc),
}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for app_id, url in UPSTREAM.items():
        try:
            img = from_upstream(url)
        except Exception as e:  # network/format problem: keep any existing icon
            print(f"WARN: {app_id}: upstream logo unavailable ({e})")
            continue
        img.save(os.path.join(OUT_DIR, f"{app_id}.png"), optimize=True)
        print(f"OK: {app_id} (upstream)")
    for app_id, (color, fn) in DRAWN.items():
        badge(color, fn).save(os.path.join(OUT_DIR, f"{app_id}.png"), optimize=True)
        print(f"OK: {app_id} (generated)")


if __name__ == "__main__":
    main()
