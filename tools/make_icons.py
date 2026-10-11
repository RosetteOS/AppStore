#!/usr/bin/env python3
"""
Generates the 28x28 PNG app icons shipped in icons/<app_id>.png.

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

SIZE = 28
SS = 8  # supersampling factor for drawn glyphs
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "icons")

RAW = "https://raw.githubusercontent.com/"
UPSTREAM = {
    "octoapp": "https://play-lh.googleusercontent.com/zRKU0gfSHWQ8ltx7MOX7bidP9CazQ6eFr8OzjOGs1siBYmVzftd27eYzn2SElicz65cTVaRLKuyAcDZqfuBr=s0-br30",
    "spoolman": RAW + "Donkie/Spoolman/master/client/public/favicon.svg",
    "mainsail": RAW + "mainsail-crew/mainsail/develop/public/img/icons/icon-192.png",
    "fluidd": RAW + "fluidd-core/fluidd/develop/public/img/icons/android-chrome-192x192.png",
    "mobileraker": RAW + "Clon1998/mobileraker/master/assets/icon/mr_appicon.png",
    "helixscreen": RAW + "prestonbrown/helixscreen/main/assets/images/helix-icon-128.png",
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Rosette-AppStore-Icons/1.0"})
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


def draw_telegram_bot(d, s):
    # Paper airplane silhouette on Telegram blue badge
    d.polygon(
        [
            (s * .14, s * .50),
            (s * .84, s * .22),
            (s * .70, s * .80),
            (s * .47, s * .63),
            (s * .36, s * .74),
            (s * .36, s * .57),
        ],
        fill=WHITE,
    )
    d.line((s * .84, s * .22, s * .36, s * .57), fill=(34, 158, 217, 255), width=int(s * .045))


def draw_cloudflared(d, s):
    # Cloud silhouette on Cloudflare orange badge
    d.ellipse((s * .32, s * .28, s * .68, s * .64), fill=WHITE)
    d.ellipse((s * .18, s * .40, s * .46, s * .68), fill=WHITE)
    d.ellipse((s * .54, s * .38, s * .82, s * .68), fill=WHITE)
    d.rectangle((s * .28, s * .48, s * .72, s * .68), fill=WHITE)


DRAWN = {
    "guppyscreen": ((94, 53, 177, 255), draw_guppyscreen),
    "timelapse": ((0, 121, 107, 255), draw_timelapse),
    "vnc": ((69, 90, 100, 255), draw_vnc),
    "telegram-bot": ((34, 158, 217, 255), draw_telegram_bot),
    "cloudflared": ((244, 129, 32, 255), draw_cloudflared),
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
