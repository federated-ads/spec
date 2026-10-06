#!/usr/bin/env python3
"""Generate the Federated Ads brand kit in docs/brand/.

Every file in the kit is derived from the definitions in this script: the
mark's geometry, the colour tokens and the typography. Edit them here and
re-run the script; do not edit the generated SVG or PNG files by hand.

Text in the artwork (wordmark, badges, social cards) is converted to outlines,
so the files render the same everywhere without the fonts installed. The
outlines come from the OFL variable fonts in the google/fonts repository,
which the script downloads into .brandcache/ on first run.

Outputs (all under docs/brand/):
  logo/          symbol, horizontal and stacked lockups in four colourways
                 (SVG), with PNG exports in logo/png/
  web/           favicons, touch and app icons, web app manifest
  social/        Open Graph card (1200x630) and GitHub social preview
                 (1280x640), SVG and PNG
  badges/        "Implements Federated Ads v0" badges and 88x31 buttons
  icons/         diagram icon set (24 px grid, currentColor)
  tokens/        design tokens in the DTCG 2025.10 format, plus tokens.css

Usage:
  scripts/build_brand.py              write SVG and PNG files
  scripts/build_brand.py --svg-only   write SVG, JSON and CSS files only

Requires fontTools, uharfbuzz and Pillow (pip install fonttools uharfbuzz
pillow), and for PNG output the resvg command-line renderer on PATH, or a
compatible command named in the RESVG environment variable.
"""

from __future__ import annotations

import io
import json
import math
import os
import shlex
import subprocess
import sys
import urllib.request
from pathlib import Path

try:
    import uharfbuzz as hb
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
except ImportError:
    sys.exit("build_brand: needs fontTools and uharfbuzz (pip install fonttools uharfbuzz pillow)")


def _repo_root() -> Path:
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        return Path(top)
    except (OSError, subprocess.CalledProcessError):
        return Path(__file__).resolve().parent.parent


ROOT = _repo_root()
OUT = ROOT / "docs/brand"
CACHE = ROOT / ".brandcache"
FONT_SOURCES = {
    "SchibstedGrotesk[wght].ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/schibstedgrotesk/SchibstedGrotesk%5Bwght%5D.ttf",
    "JetBrainsMono[wght].ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
}

# --- Colour tokens (the whitepaper stylesheet uses the same values) --------

LIGHT = {
    "paper": "#f6f7f5", "ink": "#17211f", "ink-soft": "#4b5754", "rule": "#d5dbd8",
    "panel": "#ecefed", "accent": "#1c6b5a", "accent-wash": "#dcece7", "code-bg": "#e9edeb",
}
DARK = {
    "paper": "#121816", "ink": "#e3e9e6", "ink-soft": "#9fada8", "rule": "#2a3431",
    "panel": "#19211e", "accent": "#6cc4ad", "accent-wash": "#1c2f2a", "code-bg": "#1a2320",
}
WHITE = "#ffffff"

# Address printed on the Open Graph card. The proposed domain is federated-ads.org;
# switch to it only once it is registered and serving the site (docs/brand/README.md, "Domain").
SITE_ADDRESS = "github.com/federated-ads/spec"

# Colourways: ring arcs, nodes, wordmark, secondary text.
COLOURWAYS = {
    "colour": (LIGHT["ink"], LIGHT["accent"], LIGHT["ink"], LIGHT["ink-soft"]),
    "ink": (LIGHT["ink"], LIGHT["ink"], LIGHT["ink"], LIGHT["ink"]),
    "white": (WHITE, WHITE, WHITE, WHITE),
    "reversed": (DARK["ink"], DARK["accent"], DARK["ink"], DARK["ink-soft"]),
}

# --- The mark: three peers on a ring, with nothing at the centre ------------
# 32-unit grid. Ring radius 10 around (16, 16); nodes at -90, 30 and 150
# degrees, radius 3.5; arcs span 44 degrees between the nodes, stroke 2.5.

ARCS = (
    "M22.16 8.12A10 10 0 0 1 25.9 14.61",
    "M19.75 25.27A10 10 0 0 1 12.25 25.27",
    "M6.1 14.61A10 10 0 0 1 9.84 8.12",
)
NODES = ((16, 6), (24.66, 21), (7.34, 21))
NODE_R, STROKE = 3.5, 2.5
# Visible bounds of the mark inside its 32-unit box.
MX0, MY0, MX1, MY1 = 3.84, 2.5, 28.16, 27.25


def mark(arc: str, node: str, transform: str = "") -> str:
    t = f' transform="{transform}"' if transform else ""
    arcs = "".join(f'<path d="{d}"/>' for d in ARCS)
    nodes = "".join(f'<circle cx="{x}" cy="{y}" r="{NODE_R}"/>' for x, y in NODES)
    return (f'<g{t}><g fill="none" stroke="{arc}" stroke-width="{STROKE}" stroke-linecap="round">'
            f'{arcs}</g><g fill="{node}">{nodes}</g></g>')


def fit_mark(arc: str, node: str, box: float, scale: float, cx: float | None = None,
             cy: float | None = None) -> str:
    """The mark scaled by `scale` (1 = 32-unit box), visibly centred in a square of side `box`."""
    k = box / 32 * scale
    cx = box / 2 if cx is None else cx
    cy = box / 2 if cy is None else cy
    tx = cx - (MX0 + MX1) / 2 * k
    ty = cy - (MY0 + MY1) / 2 * k
    return mark(arc, node, f"translate({n(tx)} {n(ty)}) scale({n(k)})")


def n(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def svg(w: float, h: float, body: str, title: str, extra: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{n(w)}" height="{n(h)}" '
            f'viewBox="0 0 {n(w)} {n(h)}" role="img" aria-labelledby="title"{extra}>'
            f'<title id="title">{title}</title>{body}</svg>\n')


# --- Text to outlines ---------------------------------------------------------

class Face:
    def __init__(self, path: Path, wght: float):
        tt = instancer.instantiateVariableFont(TTFont(path), {"wght": wght})
        data = io.BytesIO()
        tt.save(data)
        self.hb = hb.Font(hb.Face(data.getvalue()))
        self.glyphs = tt.getGlyphSet()
        self.order = tt.getGlyphOrder()
        self.upm = tt["head"].unitsPerEm
        self.cap = tt["OS/2"].sCapHeight

    def text(self, s: str, size: float, x: float, baseline: float, fill: str,
             tracking: float = 0.0, anchor: str = "start") -> tuple[str, float]:
        """An SVG path drawing `s`, and its advance width. Tracking is in em."""
        buf = hb.Buffer()
        buf.add_str(s)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        k = size / self.upm
        glyphs, pen = [], 0.0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            glyphs.append((self.order[info.codepoint], pen + pos.x_offset, pos.y_offset))
            pen += pos.x_advance + tracking * self.upm
        width = (pen - tracking * self.upm) * k
        if anchor == "middle":
            x -= width / 2
        parts = []
        for name, gx, gy in glyphs:
            p = SVGPathPen(self.glyphs, ntos=n)
            self.glyphs[name].draw(TransformPen(p, (k, 0, 0, -k, x + gx * k, baseline - gy * k)))
            parts.append(p.getCommands())
        return f'<path fill="{fill}" d="{" ".join(q for q in parts if q)}"/>', width

    def width(self, s: str, size: float, tracking: float = 0.0) -> float:
        return self.text(s, size, 0, 0, "none", tracking)[1]

    def cap_height(self, size: float) -> float:
        return self.cap * size / self.upm


def fonts() -> dict[str, Face]:
    CACHE.mkdir(exist_ok=True)
    for name, url in FONT_SOURCES.items():
        if not (CACHE / name).exists():
            print(f"build_brand: downloading {name}")
            (CACHE / name).write_bytes(urllib.request.urlopen(url).read())
    sg = CACHE / "SchibstedGrotesk[wght].ttf"
    jb = CACHE / "JetBrainsMono[wght].ttf"
    return {"display": Face(sg, 800), "display-medium": Face(sg, 500), "mono": Face(jb, 400),
            "mono-bold": Face(jb, 600)}


# --- Logo lockups ---------------------------------------------------------------

WORDMARK = "Federated Ads"
WORD_TRACK = -0.02
PAD = 2  # margin so anti-aliasing never clips the artwork at the file's edge


def pad(body: str) -> str:
    return f'<g transform="translate({PAD} {PAD})">{body}</g>'


def symbol(way: str) -> str:
    arc, node, _, _ = COLOURWAYS[way]
    return svg(32, 32, mark(arc, node), "Federated Ads")


def horizontal(F: dict[str, Face], way: str) -> str:
    arc, node, ink, _ = COLOURWAYS[way]
    size = 64
    k = size * 1.625 / 32                 # mark scale per 32-unit box
    mw, mh = (MX1 - MX0) * k, (MY1 - MY0) * k
    gap = 0.42 * size
    cap = F["display"].cap_height(size)
    baseline = mh / 2 + cap / 2
    word, ww = F["display"].text(WORDMARK, size, mw + gap, baseline, ink, WORD_TRACK)
    body = mark(arc, node, f"translate({n(-MX0 * k)} {n(-MY0 * k)}) scale({n(k)})") + word
    return svg(mw + gap + ww + 2 * PAD, mh + 2 * PAD, pad(body), "Federated Ads")


def stacked(F: dict[str, Face], way: str) -> str:
    arc, node, ink, soft = COLOURWAYS[way]
    size = 52
    k = size * 2.15 / 32
    mw, mh = (MX1 - MX0) * k, (MY1 - MY0) * k
    ww = F["display"].width(WORDMARK, size, WORD_TRACK)
    sub_size, sub_track = size * 0.42, 0.16
    sw = F["mono"].width("PROTOCOL", sub_size, sub_track)
    width = max(mw, ww, sw)
    cx = width / 2
    word_base = mh + 0.42 * size + F["display"].cap_height(size)
    sub_base = word_base + 0.62 * size + F["mono"].cap_height(sub_size)
    word, _ = F["display"].text(WORDMARK, size, cx, word_base, ink, WORD_TRACK, "middle")
    sub, _ = F["mono"].text("PROTOCOL", sub_size, cx, sub_base, soft, sub_track, "middle")
    body = mark(arc, node, f"translate({n(cx - 16 * k)} {n(-MY0 * k)}) scale({n(k)})") + word + sub
    return svg(width + 2 * PAD, sub_base + 2 * PAD, pad(body), "Federated Ads Protocol")


# --- Web icons ------------------------------------------------------------------

def icon_svg() -> str:
    """Favicon that follows the browser's light or dark scheme."""
    style = (f"<style>.a{{stroke:{LIGHT['ink']}}}.n{{fill:{LIGHT['accent']}}}"
             f"@media (prefers-color-scheme:dark){{.a{{stroke:{DARK['ink']}}}.n{{fill:{DARK['accent']}}}}}</style>")
    arcs = "".join(f'<path d="{d}"/>' for d in ARCS)
    nodes = "".join(f'<circle cx="{x}" cy="{y}" r="{NODE_R}"/>' for x, y in NODES)
    body = (f'{style}<g class="a" fill="none" stroke-width="{STROKE}" stroke-linecap="round">{arcs}</g>'
            f'<g class="n">{nodes}</g>')
    return svg(32, 32, body, "Federated Ads")


def tile(size: float, scale: float, radius: float) -> str:
    """Dark tile with the reversed mark: favicon.ico, touch and app icons."""
    arc, node, _, _ = COLOURWAYS["reversed"]
    rect = f'<rect width="{n(size)}" height="{n(size)}" rx="{n(radius)}" fill="{LIGHT["ink"]}"/>'
    return svg(size, size, rect + fit_mark(arc, node, size, scale), "Federated Ads")


def manifest() -> str:
    return json.dumps({
        "name": "Federated Ads Protocol",
        "short_name": "Federated Ads",
        "description": "An open, federated, owner-controlled protocol for advertising on the open web.",
        "start_url": "../../",
        "display": "browser",
        "background_color": LIGHT["paper"],
        "theme_color": LIGHT["ink"],
        "icons": [
            {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }, indent=2) + "\n"


# --- Social cards -----------------------------------------------------------------

def og_card(F: dict[str, Face]) -> str:
    W, H = 1200, 630
    L = LIGHT
    parts = [f'<rect width="{W}" height="{H}" fill="{L["paper"]}"/>',
             mark(L["rule"], L["accent"], "translate(750 35) scale(17.5)"),
             mark(L["ink"], L["accent"], "translate(80 72) scale(1.375)")]
    parts.append(F["display"].text(WORDMARK, 28, 138, 104, L["ink"], WORD_TRACK)[0])
    parts.append(F["display"].text("The Federated Ads", 68, 78, 262, L["ink"], -0.025)[0])
    parts.append(F["display"].text("Protocol", 68, 78, 332, L["ink"], -0.025)[0])
    parts.append(F["display-medium"].text("An open, federated, owner-controlled protocol", 28, 80, 398, L["ink-soft"])[0])
    parts.append(F["display-medium"].text("for advertising on the open web", 28, 80, 434, L["ink-soft"])[0])
    parts.append(F["mono"].text(f"Discussion draft · Not a standard · {SITE_ADDRESS}",
                                18, 80, 558, L["ink-soft"])[0])
    return svg(W, H, "".join(parts),
               "The Federated Ads Protocol: an open, federated, owner-controlled protocol for advertising on the open web")


def github_card(F: dict[str, Face]) -> str:
    W, H = 1280, 640
    D = DARK
    parts = [f'<rect width="{W}" height="{H}" fill="{D["paper"]}"/>',
             mark(D["ink"], D["accent"], "translate(80 170) scale(9.375)")]
    x = 452
    parts.append(F["mono"].text("federated-ads / spec", 22, x, 232, D["accent"])[0])
    parts.append(F["display"].text(WORDMARK, 76, x, 318, D["ink"], -0.025)[0])
    parts.append(F["display-medium"].text("Whitepaper, Internet-Draft and vocabulary for", 28, x, 380, D["ink-soft"])[0])
    parts.append(F["display-medium"].text("an open, federated advertising protocol", 28, x, 416, D["ink-soft"])[0])
    return svg(W, H, "".join(parts),
               "Federated Ads: whitepaper, Internet-Draft and vocabulary for an open, federated advertising protocol")


# --- Badges -------------------------------------------------------------------------

def badge(F: dict[str, Face], theme: str, profile: str | None) -> str:
    P = LIGHT if theme == "light" else DARK
    bg = WHITE if theme == "light" else P["paper"]
    title = "Implements Federated Ads v0" + (f", {profile} profile" if profile else "")
    h = 76 if profile else 64
    tx = 68
    l1 = F["mono"].text("IMPLEMENTS", 11, tx, 24 if profile else 26, P["ink-soft"], 0.1)
    l2 = F["display"].text("Federated Ads v0", 22, tx, 48 if profile else 50, P["ink"], -0.01)
    lines = [l1, l2]
    if profile:
        lines.append(F["mono"].text(f"{profile} profile", 12, tx, 65, P["accent"]))
    w = math.ceil(tx + max(width for _, width in lines) + 18)
    body = (f'<rect x="1" y="1" width="{n(w - 2)}" height="{h - 2}" fill="{bg}" stroke="{P["ink"]}" stroke-width="2"/>'
            + fit_mark(P["ink"], P["accent"], 40, 1, 14 + 20, h / 2)
            + "".join(path for path, _ in lines))
    return svg(w, h, body, title)


def button(F: dict[str, Face], theme: str) -> str:
    if theme == "light":
        bg, line, arc, node, ink = WHITE, LIGHT["ink"], LIGHT["ink"], LIGHT["accent"], LIGHT["ink"]
    else:
        bg, line, arc, node, ink = LIGHT["ink"], LIGHT["ink"], DARK["ink"], DARK["accent"], DARK["ink"]
    body = (f'<rect x=".5" y=".5" width="87" height="30" fill="{bg}" stroke="{line}"/>'
            + fit_mark(arc, node, 22, 1, 15, 15.5)
            + F["display"].text("Federated", 10, 30, 14, ink, -0.01)[0]
            + F["display"].text("Ads v0", 10, 30, 25, ink, -0.01)[0])
    return svg(88, 31, body, "Implements Federated Ads v0")


# --- Diagram icons (24 px grid, 1.75 stroke, round joins) -----------------------------

DIAGRAM_ICONS = {
    "publisher": ("Publisher (selling node)", '<rect x="4.5" y="3" width="15" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>'),
    "advertiser": ("Advertiser (buying node)", '<path d="M3.5 10v4h3l7.5 4.5v-13L6.5 10z"/><path d="M17 9a4 4 0 0 1 0 6M19.5 6.5a7.5 7.5 0 0 1 0 11"/>'),
    "intermediary": ("Intermediary (optional, replaceable)", '<path d="M4 8h14M15 5l3 3-3 3M20 16H6M9 13l-3 3 3 3"/>'),
    "creative": ("Creative (licensed, revocable)", '<rect x="3" y="4" width="18" height="14" rx="2"/><circle cx="8.5" cy="9" r="1.5"/><path d="M21 14l-4.5-4.5L8 18"/>'),
    "receipt": ("Signed receipt", '<path d="M6 3h12v18l-2-1.5-2 1.5-2-1.5-2 1.5-2-1.5-2 1.5z"/><path d="M9 11l2 2 4-4.5"/>'),
    "log": ("Transparency log (append-only)", '<rect x="4" y="3.5" width="16" height="4.5" rx="1"/><rect x="4" y="10" width="16" height="4.5" rx="1"/><path d="M4 18.5h16" stroke-dasharray="2 2.5"/>'),
    "signing-key": ("Signing key", '<circle cx="8" cy="15.5" r="4"/><path d="M10.9 12.6L19 4.5M16 7.5l2.5 2.5M13.8 9.7l1.8 1.8"/>'),
    "person": ("Person who sees the ad", '<circle cx="12" cy="8" r="4"/><path d="M4.5 20.5a7.5 7.5 0 0 1 15 0"/>'),
    "measurement": ("Measurement module", '<path d="M4 17a8 8 0 1 1 16 0"/><path d="M12 17l4-5"/><circle cx="12" cy="17" r="1"/>'),
    "settlement": ("Settlement on any payment rail", '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 14.5h4"/>'),
    "report": ("Report an ad", '<path d="M5 21V4"/><path d="M5 4h12l-2.5 4L17 12H5"/>'),
    "ad-free": ("Ad-free option", '<path d="M12 3l7.5 3v5.5c0 4.5-3.2 8-7.5 9.5-4.3-1.5-7.5-5-7.5-9.5V6z"/><path d="M9 12l2 2 4-4.5"/>'),
}


def diagram_icon(title: str, body: str) -> str:
    return svg(24, 24, f'<g fill="none" stroke="currentColor" stroke-width="1.75" '
                       f'stroke-linecap="round" stroke-linejoin="round">{body}</g>', title)


# --- Design tokens (DTCG 2025.10) -------------------------------------------------------

def colour_token(hexv: str, desc: str | None = None) -> dict:
    rgb = [round(int(hexv[i:i + 2], 16) / 255, 4) for i in (1, 3, 5)]
    tok = {"$value": {"colorSpace": "srgb", "components": rgb, "hex": hexv}}
    if desc:
        tok["$description"] = desc
    return tok


COLOUR_NOTES = {
    "paper": "Page background",
    "ink": "Body text and the ring of the mark",
    "ink-soft": "Secondary text",
    "rule": "Rules and borders; decoration only, below 3:1",
    "panel": "Panels and hover backgrounds",
    "accent": "Links, the nodes of the mark, verified states",
    "accent-wash": "Background for notes and seals",
    "code-bg": "Code background",
}


def theme_tokens(palette: dict[str, str]) -> str:
    group = {"$type": "color"}
    for name, value in palette.items():
        group[name] = colour_token(value, COLOUR_NOTES[name])
    return json.dumps({"color": group}, indent=2) + "\n"


def base_tokens() -> str:
    return json.dumps({
        "font": {
            "family": {
                "$type": "fontFamily",
                "display": {"$value": ["Schibsted Grotesk", "Helvetica Neue", "Arial", "sans-serif"],
                            "$description": "Headings and the wordmark"},
                "body": {"$value": ["Source Serif 4", "Georgia", "Times New Roman", "serif"],
                         "$description": "Body text"},
                "mono": {"$value": ["JetBrains Mono", "ui-monospace", "Menlo", "Consolas", "monospace"],
                         "$description": "Code, labels and metadata"},
            },
            "weight": {
                "$type": "fontWeight",
                "regular": {"$value": 400}, "medium": {"$value": 500}, "semibold": {"$value": 600},
                "bold": {"$value": 700}, "extrabold": {"$value": 800},
            },
        },
        "mark": {
            "$type": "dimension",
            "min-size-symbol": {"$value": {"value": 16, "unit": "px"},
                                "$description": "Smallest size for the symbol on its own"},
            "min-width-horizontal": {"$value": {"value": 112, "unit": "px"},
                                     "$description": "Smallest width for the horizontal lockup"},
        },
    }, indent=2) + "\n"


def resolver() -> str:
    return json.dumps({
        "$schema": "https://www.designtokens.org/schemas/2025.10/resolver.json",
        "sets": {"base": {"sources": [{"$ref": "base.tokens.json"}]}},
        "modifiers": {
            "theme": {
                "description": "Colour theme",
                "contexts": {
                    "light": [{"$ref": "theme/light.tokens.json"}],
                    "dark": [{"$ref": "theme/dark.tokens.json"}],
                },
                "default": "light",
            }
        },
        "resolutionOrder": [{"$ref": "#/sets/base"}, {"$ref": "#/modifiers/theme"}],
    }, indent=2) + "\n"


def tokens_css() -> str:
    def block(p: dict[str, str]) -> str:
        return " ".join(f"--{k}: {v};" for k, v in p.items())
    return (
        "/* Federated Ads colour and type tokens. Generated by scripts/build_brand.py\n"
        "   from the same values as tokens/*.tokens.json. Fonts: ../../assets/fonts/fonts.css */\n"
        ":root {\n"
        f"  {block(LIGHT)}\n"
        '  --display: "Schibsted Grotesk", "Helvetica Neue", Arial, sans-serif;\n'
        '  --body: "Source Serif 4", Georgia, "Times New Roman", serif;\n'
        '  --mono: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;\n'
        "  color-scheme: light;\n"
        "}\n"
        "@media (prefers-color-scheme: dark) {\n"
        f'  :root:not([data-theme="light"]) {{ {block(DARK)} color-scheme: dark; }}\n'
        "}\n"
        f':root[data-theme="dark"] {{ {block(DARK)} color-scheme: dark; }}\n'
    )


# --- Writing and rendering ------------------------------------------------------------

written: list[Path] = []


def write(rel: str, text: str) -> Path:
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    written.append(path)
    return path


def resvg_cmd() -> list[str] | None:
    env = os.environ.get("RESVG")
    if env:
        return shlex.split(env)
    from shutil import which
    return ["resvg"] if which("resvg") else None


def png(src: Path, rel: str, w: int, h: int, cmd: list[str]) -> Path:
    out = OUT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([*cmd, "-w", str(w), "-h", str(h), str(src), str(out)], check=True)
    written.append(out)
    return out


def main() -> int:
    svg_only = "--svg-only" in sys.argv[1:]
    cmd = None if svg_only else resvg_cmd()
    if not svg_only and cmd is None:
        print("build_brand: resvg not found; install it or set RESVG, or pass --svg-only", file=sys.stderr)
        return 1
    F = fonts()

    sources: dict[str, tuple[Path, float, float]] = {}

    def vector(rel: str, text: str) -> Path:
        p = write(rel, text)
        import re
        m = re.search(r'width="([\d.]+)" height="([\d.]+)"', text)
        sources[rel] = (p, float(m.group(1)), float(m.group(2)))
        return p

    for way in COLOURWAYS:
        vector(f"logo/federated-ads-symbol-{way}.svg", symbol(way))
        vector(f"logo/federated-ads-horizontal-{way}.svg", horizontal(F, way))
        vector(f"logo/federated-ads-stacked-{way}.svg", stacked(F, way))

    vector("web/icon.svg", icon_svg())
    vector("web/favicon-tile.svg", tile(32, 0.86, 7))
    vector("web/apple-touch-icon.svg", tile(180, 0.8, 0))
    vector("web/icon-app.svg", tile(512, 0.8, 112))
    vector("web/icon-maskable.svg", tile(512, 0.74, 0))
    write("web/site.webmanifest", manifest())

    vector("social/og-image.svg", og_card(F))
    vector("social/github-social-preview.svg", github_card(F))

    for theme in ("light", "dark"):
        vector(f"badges/implements-federated-ads-v0-{theme}.svg", badge(F, theme, None))
        for profile in ("core", "extended"):
            vector(f"badges/implements-federated-ads-v0-{profile}-{theme}.svg", badge(F, theme, profile))
        vector(f"badges/button-88x31-{theme}.svg", button(F, theme))

    for name, (title, body) in DIAGRAM_ICONS.items():
        write(f"icons/{name}.svg", diagram_icon(title, body))

    write("tokens/base.tokens.json", base_tokens())
    write("tokens/theme/light.tokens.json", theme_tokens(LIGHT))
    write("tokens/theme/dark.tokens.json", theme_tokens(DARK))
    write("tokens/brand.resolver.json", resolver())
    write("tokens/tokens.css", tokens_css())

    if cmd:
        for rel, (p, w, h) in sources.items():
            stem = Path(rel).stem
            if rel.startswith("logo/federated-ads-symbol"):
                for size in (64, 128, 256, 512, 1024):
                    png(p, f"logo/png/{stem}-{size}.png", size, size, cmd)
            elif rel.startswith("logo/"):
                for width in (600, 1200):
                    png(p, f"logo/png/{stem}-{width}w.png", width, round(h * width / w), cmd)
            elif rel.startswith(("social/", "badges/")):
                png(p, rel.replace(".svg", ".png"), round(w * (1 if rel.startswith("social/") else 2)),
                    round(h * (1 if rel.startswith("social/") else 2)), cmd)
        png(sources["web/apple-touch-icon.svg"][0], "web/apple-touch-icon.png", 180, 180, cmd)
        png(sources["web/icon-app.svg"][0], "web/icon-192.png", 192, 192, cmd)
        png(sources["web/icon-app.svg"][0], "web/icon-512.png", 512, 512, cmd)
        png(sources["web/icon-maskable.svg"][0], "web/icon-maskable-512.png", 512, 512, cmd)
        try:
            from PIL import Image
        except ImportError:
            print("build_brand: Pillow not installed; favicon.ico skipped", file=sys.stderr)
        else:
            sizes = (16, 32, 48)
            frames = [png(sources["web/favicon-tile.svg"][0], f"web/.favicon-{s}.png", s, s, cmd) for s in sizes]
            images = [Image.open(f) for f in frames]
            ico = OUT / "web/favicon.ico"
            images[-1].save(ico, format="ICO", sizes=[(s, s) for s in sizes], append_images=images[:-1])
            for f in frames:
                f.unlink()
                written.remove(f)
            written.append(ico)

    print(f"build_brand: wrote {len(written)} files under {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
