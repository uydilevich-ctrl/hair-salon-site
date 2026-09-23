import sys, os, base64
sys.path.insert(0, os.path.abspath('../logo'))
os.chdir('../logo'); import build as B; os.chdir('../trace')
from pendant import gold, flat, VB_NOBAIL, VB_BAIL, svg
from PIL import Image
import io

OL, IV, GO = "#4F5D45", "#F6F1E8", "#C5A66A"
os.makedirs('out', exist_ok=True)

def mark_group(inner, vb, x, y, w):
    vx, vy, vw, vh = map(float, vb.split())
    s = w / vw
    return f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.4f}) translate({-vx} {-vy})">{inner}</g>', vh * s

def stacked(mark_inner, vb, text_color, sub_color, fname="cormorant", W=620):
    mw = 420
    g, mh = mark_group(mark_inner, vb, (W - mw) / 2, 30, mw)
    size, tr = 104, 0.26
    x0, y0, x1, y1 = B.ink_bounds(fname, "TORTÉ", size, tr)
    base = 30 + mh + 40 - y0
    d, _ = B.text_path(fname, "TORTÉ", size, tr, (W - (x1 - x0)) / 2 - x0, base)
    sub = "HAIR STUDIO · MOSCOW"
    sx0, _, sx1, _ = B.ink_bounds("jost", sub, 16, 0.42)
    sd, _ = B.text_path("jost", sub, 16, 0.42, (W - (sx1 - sx0)) / 2 - sx0, base + 46)
    inner = (g + f'<path d="{d}" fill="{text_color}"/>'
             f'<path d="M{W/2-22:.1f} {base+20:.1f} h44" stroke="{GO}" stroke-width="1.4"/>'
             f'<path d="{sd}" fill="{sub_color}"/>')
    return B.svg(inner, W, base + 72)

def horizontal(mark_inner, vb, text_color, fname="cormorant"):
    g, mh = mark_group(mark_inner, vb, 16, 16, 260)
    size, tr = 92, 0.26
    x0, y0, x1, y1 = B.ink_bounds(fname, "TORTÉ", size, tr)
    tx = 16 + 260 + 36
    base = 16 + mh * 0.62
    d, _ = B.text_path(fname, "TORTÉ", size, tr, tx - x0, base)
    sub = "HAIR STUDIO"
    sx0, _, sx1, _ = B.ink_bounds("jost", sub, 18, 0.5)
    sd, _ = B.text_path("jost", sub, 18, 0.5, tx + ((x1 - x0) - (sx1 - sx0)) / 2 - sx0, base + 42)
    inner = (g + f'<path d="{d}" fill="{text_color}"/>'
             f'<path d="M{tx:.1f} {base+19:.1f} h{x1-x0:.1f}" stroke="{GO}" stroke-width="1.2"/>'
             f'<path d="{sd}" fill="{text_color}"/>')
    return B.svg(inner, tx + (x1 - x0) + 20, 16 + mh + 16)

F = {
 "turtle-gold.svg": svg(gold(uid="a"), VB_NOBAIL, 900),
 "turtle-gold-charm.svg": svg(gold(True, "b"), VB_BAIL, 900),
 "turtle-olive.svg": svg(flat(OL, eye_fill=None), VB_NOBAIL, 900),
 "turtle-ivory.svg": svg(flat(IV, eye_fill=None), VB_NOBAIL, 900),
 "lockup-gold-stacked.svg": stacked(gold(uid="c"), VB_NOBAIL, OL, OL),
 "lockup-gold-stacked-dark.svg": stacked(gold(uid="d"), VB_NOBAIL, IV, IV),
 "lockup-gold-stacked-marcellus.svg": stacked(gold(uid="e"), VB_NOBAIL, OL, OL, "marcellus"),
 "lockup-olive-stacked.svg": stacked(flat(OL), VB_NOBAIL, OL, OL),
 "lockup-gold-horizontal.svg": horizontal(gold(uid="f"), VB_NOBAIL, OL),
 "lockup-olive-horizontal.svg": horizontal(flat(OL), VB_NOBAIL, OL),
}
for n, c in F.items():
    open(f'out/{n}', 'w').write(c)

# фото кулона для сравнения
im = Image.open('/tmp/claude-0/-home-user-hair-salon-site/4b29f3cd-44e3-538d-bc38-b6c5cbfe1d8e/images/2.png').convert('RGB').crop((40, 80, 262, 270)).resize((444, 380), Image.LANCZOS)
buf = io.BytesIO(); im.save(buf, 'JPEG', quality=86)
open('out/photo.b64', 'w').write(base64.b64encode(buf.getvalue()).decode())
print(sorted(F))
