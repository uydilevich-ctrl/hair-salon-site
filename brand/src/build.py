"""Собирает SVG-файлы логотипа TORTÉ (все надписи — в контурах)."""
import math, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from torte_mark import mark, CX, BASE, RY

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

FONTS = {
    "cormorant": "CormorantGaramond.ttf",
    "marcellus": "Marcellus.ttf",
    "italiana": "Italiana.ttf",
    "bodoni": "BodoniModa.ttf",
    "jost": "Jost.ttf",
}
_cache = {}


def font(name):
    if name not in _cache:
        _cache[name] = TTFont(os.path.join(HERE, "fonts", FONTS[name]))
    return _cache[name]


def text_path(fname, text, size, tracking=0.0, x=0.0, y=0.0):
    """Текст → (d, ширина). y — базовая линия. tracking — доля кегля."""
    f = font(fname)
    upm = f["head"].unitsPerEm
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    s = size / upm
    pen = SVGPathPen(gs)
    cur = x
    for i, ch in enumerate(text):
        g = cmap.get(ord(ch))
        if g is None:
            raise SystemExit(f"{fname}: нет глифа {ch!r}")
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cur, y)))
        cur += gs[g].width * s
        if i < len(text) - 1:
            cur += tracking * size
    return pen.getCommands(), cur - x


def ink_bounds(fname, text, size, tracking=0.0):
    """Фактические границы начертания (для точного центрирования)."""
    f = font(fname)
    upm = f["head"].unitsPerEm
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    s = size / upm
    bp = BoundsPen(gs)
    cur = 0.0
    for i, ch in enumerate(text):
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(bp, (s, 0, 0, -s, cur, 0)))
        cur += gs[g].width * s + (tracking * size if i < len(text) - 1 else 0)
    return bp.bounds  # xmin, ymin, xmax, ymax (y вниз)


def svg(inner, w, h, bg=None):
    rect = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}">{rect}{inner}</svg>')


def placed_mark(style, x, y, scale, color, stroke=2.4):
    inner, vb = mark(style, stroke=stroke, color=color)
    vx, vy, vw, vh = map(float, vb.split())
    return (f'<g transform="translate({x:.2f} {y:.2f}) scale({scale:.4f}) '
            f'translate({-vx} {-vy})">{inner}</g>'), vw * scale, vh * scale


def wordmark(fname, color, size=120, tracking=0.28):
    d, w = text_path(fname, "TORTÉ", size, tracking)
    x0, y0, x1, y1 = ink_bounds(fname, "TORTÉ", size, tracking)
    pad = 10
    inner = f'<path d="{d}" fill="{color}" transform="translate({pad - x0:.2f} {pad - y0:.2f})"/>'
    return inner, (x1 - x0) + 2 * pad, (y1 - y0) + 2 * pad


def lockup_horizontal(fname, color, accent, sub="HAIR STUDIO"):
    size, tr = 96, 0.26
    x0, y0, x1, y1 = ink_bounds(fname, "TORTÉ", size, tr)
    m, mw, mh = placed_mark("classic", 20, 20, 1.75, color, stroke=2.2)
    tx = 20 + mw + 34
    # базовая линия надписи — на уровне «пуза» черепахи
    belly_y = 20 + (BASE - 30) * 1.75
    d, _ = text_path(fname, "TORTÉ", size, tr, tx - x0, belly_y)
    sd, sw = text_path("jost", sub, 20, 0.5, 0, 0)
    sx0, sy0, sx1, sy1 = ink_bounds("jost", sub, 20, 0.5)
    word_w = x1 - x0
    sub_x = tx + (word_w - (sx1 - sx0)) / 2 - sx0
    sub_y = belly_y + 44
    line_y = belly_y + 20
    inner = (m + f'<path d="{d}" fill="{color}"/>'
             f'<path d="M{tx:.1f} {line_y:.1f} h{word_w:.1f}" stroke="{accent}" stroke-width="1.2"/>'
             f'<path d="{sd}" fill="{color}" transform="translate({sub_x:.2f} {sub_y:.2f})"/>')
    return inner, tx + word_w + 24, 20 + 88 * 1.75 + 20


def lockup_stacked(fname, color, accent, sub="HAIR STUDIO · MOSCOW"):
    W = 560
    m, mw, mh = placed_mark("classic", 0, 24, 1.7, color)
    m = m.replace('translate(0.00 24.00)', f'translate({(W - mw) / 2:.2f} 24.00)')
    size, tr = 104, 0.26
    x0, y0, x1, y1 = ink_bounds(fname, "TORTÉ", size, tr)
    base = 24 + mh + 36 - y0
    d, _ = text_path(fname, "TORTÉ", size, tr, (W - (x1 - x0)) / 2 - x0, base)
    sx0, sy0, sx1, sy1 = ink_bounds("jost", sub, 16, 0.42)
    sd, _ = text_path("jost", sub, 16, 0.42, (W - (sx1 - sx0)) / 2 - sx0, base + 46)
    inner = (m + f'<path d="{d}" fill="{color}"/>'
             f'<path d="M{W/2-22:.1f} {base+20:.1f} h44" stroke="{accent}" stroke-width="1.4"/>'
             f'<path d="{sd}" fill="{color}"/>')
    return inner, W, base + 70


def seal(color, accent, fname="cormorant"):
    """Круглая печать: знак в центре, надпись по кругу (каждая буква — контур)."""
    S, c, r = 420, 210, 150
    text = "TORTÉ · HAIR STUDIO · MOSCOW · "
    f = font(fname if fname != "jost" else "jost")
    fn = "jost"
    size, tr = 30, 0.22
    fj = font(fn)
    upm = fj["head"].unitsPerEm
    cmap, gs = fj.getBestCmap(), fj.getGlyphSet()
    s = size / upm
    widths = [gs[cmap[ord(ch)]].width * s + tr * size for ch in text]
    total = sum(widths)
    k = (2 * math.pi * r) / total           # растягиваем трекинг до полного круга
    parts, ang = [], -math.pi / 2
    for ch, w in zip(text, widths):
        adv = w * k
        mid = ang + (adv / 2) / r
        gw = gs[cmap[ord(ch)]].width * s
        pen = SVGPathPen(gs)
        gs[cmap[ord(ch)]].draw(TransformPen(pen, (s, 0, 0, -s, -gw / 2, 0)))
        x = c + r * math.cos(mid)
        y = c + r * math.sin(mid)
        rot = math.degrees(mid) + 90
        parts.append(f'<path d="{pen.getCommands()}" transform="translate({x:.2f} {y:.2f}) rotate({rot:.2f})"/>')
        ang += adv / r
    m, mw, mh = placed_mark("minimal", 0, 0, 1.2, color, stroke=2.6)
    m = m.replace("translate(0.00 0.00)", f"translate({c - mw / 2:.2f} {c - mh / 2 + 4:.2f})")
    inner = (f'<circle cx="{c}" cy="{c}" r="{r + 44}" fill="none" stroke="{color}" stroke-width="2"/>'
             f'<circle cx="{c}" cy="{c}" r="{r - 22}" fill="none" stroke="{accent}" stroke-width="1.4"/>'
             f'<g fill="{color}">{"".join(parts)}</g>' + m)
    return inner, S, S


OLIVE, IVORY, GOLD, SAGE = "#4F5D45", "#F6F1E8", "#C5A66A", "#A8B89A"

files = {}
for st in ("classic", "charm", "minimal", "globe", "solid"):
    inner, vb = mark(st, color=OLIVE)
    vx, vy, vw, vh = map(float, vb.split())
    files[f"mark-{st}.svg"] = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" '
                              f'width="{vw*3:.0f}" height="{vh*3:.0f}">{inner}</svg>')
for fn in ("cormorant", "marcellus", "italiana", "bodoni", "jost"):
    inner, w, h = wordmark(fn, OLIVE)
    files[f"wordmark-{fn}.svg"] = svg(inner, w, h)
for fn in ("cormorant", "marcellus"):
    inner, w, h = lockup_horizontal(fn, OLIVE, GOLD)
    files[f"lockup-horizontal-{fn}.svg"] = svg(inner, w, h)
    inner, w, h = lockup_stacked(fn, OLIVE, GOLD)
    files[f"lockup-stacked-{fn}.svg"] = svg(inner, w, h)
inner, w, h = seal(OLIVE, GOLD)
files["seal.svg"] = svg(inner, w, h)
# инверсия для тёмного фона
inner, w, h = lockup_stacked("cormorant", IVORY, GOLD)
files["lockup-stacked-cormorant-ivory.svg"] = svg(inner, w, h)
# фавикон: минимальный знак на оливковом круге
inner, vb = mark("minimal", stroke=3.2, color=IVORY, eye=True)
files["favicon.svg"] = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
                        f'<circle cx="32" cy="32" r="32" fill="{OLIVE}"/>'
                        f'<g transform="translate(5 16) scale(0.315) translate(-12 -30)">{inner}</g></svg>')

for name, content in files.items():
    open(os.path.join(OUT, name), "w").write(content)
print("\n".join(sorted(files)))
