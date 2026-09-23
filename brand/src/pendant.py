"""Черепаха TORTÉ, обведённая по фото кулона. Координаты — увеличенное фото 780×632."""
from paths import PATHS, EYE

ROT = "rotate(3.5 470 380)"          # выравниваем наклон кулона на фото
VB_NOBAIL = "28 118 752 500"
VB_BAIL = "30 30 750 590"


def _paths(bail):
    return [d for k, d in PATHS.items() if bail or k != "bail"]


def gold(bail=False, uid="g"):
    ds = _paths(bail)
    ex, ey, er = EYE
    defs = f'''<defs>
  <linearGradient id="{uid}-metal" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#7C5C22"/><stop offset=".28" stop-color="#C9A25A"/>
    <stop offset=".5" stop-color="#F2DE9E"/><stop offset=".72" stop-color="#B98B3E"/>
    <stop offset="1" stop-color="#6E5020"/>
  </linearGradient>
  <filter id="{uid}-sh" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="5"/></filter>
  <radialGradient id="{uid}-stone" cx=".35" cy=".3" r=".8">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset=".45" stop-color="#E9EEF2"/><stop offset="1" stop-color="#9FA9B3"/>
  </radialGradient>
</defs>'''
    sh = "".join(f'<path d="{d}"/>' for d in ds)
    base = "".join(f'<path d="{d}"/>' for d in ds)
    hi = "".join(f'<path d="{d}"/>' for d in ds)
    stone = (f'<circle cx="{ex}" cy="{ey}" r="{er+4}" fill="url(#{uid}-metal)"/>'
             f'<circle cx="{ex}" cy="{ey}" r="{er}" fill="url(#{uid}-stone)"/>'
             f'<path d="M{ex-er*.7} {ey} L{ex} {ey-er*.7} L{ex+er*.7} {ey} L{ex} {ey+er*.7} Z" fill="none" stroke="#fff" stroke-width="1.2" opacity=".9"/>')
    return defs + f'''<g transform="{ROT}" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <g stroke="#3B3020" stroke-width="15" opacity=".22" transform="translate(5 7)" filter="url(#{uid}-sh)">{sh}</g>
  <g stroke="#6E5020" stroke-width="15">{base}</g>
  <g stroke="url(#{uid}-metal)" stroke-width="12">{base}</g>
  <g stroke="#FFF3CF" stroke-width="3.2" opacity=".6" transform="translate(-1.6 -2.2)">{hi}</g>
  {stone}
</g>'''


def flat(color="#4F5D45", bail=False, width=12, eye_fill=None):
    ds = _paths(bail)
    ex, ey, er = EYE
    body = "".join(f'<path d="{d}"/>' for d in ds)
    eye = (f'<circle cx="{ex}" cy="{ey}" r="{er+2}" fill="{color}"/>'
           + (f'<circle cx="{ex}" cy="{ey}" r="{er-3}" fill="{eye_fill}"/>' if eye_fill else ""))
    return (f'<g transform="{ROT}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}{eye}</g>')


def svg(inner, vb, px_w=None):
    x, y, w, h = map(float, vb.split())
    size = f' width="{px_w}" height="{px_w*h/w:.0f}"' if px_w else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{size}>{inner}</svg>'
