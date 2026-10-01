"""Черепаха TORTÉ — векторные варианты знака.

Все знаки рисуются в системе координат 200×130, смотрят влево, как кулон.
"""
import math

CX, BASE = 112, 92          # центр и основание панциря
RX, RY = 52, 50             # полуоси купола


def dome_y(x, rx=RX, ry=RY, cx=CX, base=BASE):
    t = max(0.0, 1 - ((x - cx) / rx) ** 2)
    return base - ry * math.sqrt(t)


def dome(rx=RX, ry=RY, cx=CX, base=BASE):
    """Полуэллипс купола дугой SVG."""
    return f"M{cx-rx:.1f} {base} A{rx} {ry} 0 0 1 {cx+rx:.1f} {base}"


def arch(y0, rise, cx=CX, inset=0.0):
    """Горизонтальная линия решётки: хорда купола на высоте y0, слегка выгнутая."""
    half = RX * math.sqrt(max(0.0, 1 - ((BASE - y0) / RY) ** 2)) - inset
    x1, x2 = cx - half, cx + half
    return f"M{x1:.1f} {y0:.1f} Q{cx} {y0 - rise:.1f} {x2:.1f} {y0:.1f}"


def rib(x0, lean=0.78, inset=0.0):
    """Вертикальное ребро: от основания вверх к куполу, слегка к центру."""
    x1 = CX + (x0 - CX) * lean
    y1 = dome_y(x1) + inset
    xm = CX + (x0 - CX) * 0.97
    ym = (BASE + y1) / 2
    return f"M{x0:.1f} {BASE} Q{xm:.1f} {ym:.1f} {x1:.1f} {y1:.1f}"


HEAD = (
    # двойной контур шеи и головы, как проволока кулона
    "M66 71 C56 69 50 62 48 54 C46 46 40 42 33 43 "
    "C26 44 21 49 22 54 C23 58 28 60 34 59 "
    "C40 58 42 64 44 72 C47 82 54 88 62 88"
)
EYE = (32, 50.5)
LEG_FRONT = "M73 92 C66 101 63 110 69 112.5 C75 115 81 106 86 92"
LEG_BACK = "M139 92 C141 104 147 113 154 111 C161 109 158 99 152 91"
TAIL = "M163 87 C171 88 176 84 174 79 C172 75 167 77 168 81"
RING = "M112 42 L112 37"
BELLY = f"M{CX-RX-4} {BASE} L{CX+RX+4} {BASE}"


def mark(style="classic", stroke=2.4, color="currentColor", eye=True):
    """Возвращает (inner_svg, viewBox)."""
    p = []
    add = lambda d, w=stroke: p.append(
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
    )
    if style == "classic":          # как кулон: решётка 2×4
        add(dome())
        add(BELLY)
        for y0, r in ((74, 5), (57, 4)):
            add(arch(y0, r), stroke * 0.8)
        for x0 in (80, 100, 124, 144):
            add(rib(x0), stroke * 0.8)
        add(HEAD); add(LEG_FRONT); add(LEG_BACK); add(TAIL)
        if eye:
            p.append(f'<circle cx="{EYE[0]}" cy="{EYE[1]}" r="{stroke*0.75:.2f}" fill="{color}"/>')
    elif style == "minimal":        # для мелких размеров: меньше линий, толще
        add(dome(), stroke * 1.3)
        add(BELLY, stroke * 1.3)
        add(arch(68, 6), stroke)
        for x0 in (94, 130):
            add(rib(x0, 0.82), stroke)
        add(HEAD, stroke * 1.3); add(LEG_FRONT, stroke * 1.3); add(LEG_BACK, stroke * 1.3)
        if eye:
            p.append(f'<circle cx="{EYE[0]}" cy="{EYE[1]}" r="{stroke:.2f}" fill="{color}"/>')
    elif style == "globe":          # меридианы сходятся к вершине — панцирь как купол
        add(dome())
        add(BELLY)
        for k in (0.33, 0.66):
            add(dome(RX * k, RY), stroke * 0.75)
        add(arch(70, 7), stroke * 0.75)
        add(HEAD); add(LEG_FRONT); add(LEG_BACK); add(TAIL)
        if eye:
            p.append(f'<circle cx="{EYE[0]}" cy="{EYE[1]}" r="{stroke*0.75:.2f}" fill="{color}"/>')
    elif style == "charm":          # подвеска: классика + колечко-бейл сверху
        inner, _ = mark("classic", stroke, color, eye)
        p.append(inner)
        p.append(f'<circle cx="{CX}" cy="{BASE-RY-6.2}" r="7" fill="none" stroke="{color}" stroke-width="{stroke}"/>')
        return "".join(p), "12 20 172 98"
    elif style == "solid":          # силуэт-штамп: залитый панцирь с прорезями решётки
        # залитый купол, решётка светлыми линиями внутри купола с отступом — остаётся ободок
        clip = f'<clipPath id="shell-in"><path d="{dome(RX - 6, RY - 6, base=BASE - 3)} Z"/></clipPath>'
        lines = "".join(
            f'<path d="{d}" fill="none" stroke="#F6F1E8" stroke-width="{stroke*0.9}" stroke-linecap="round"/>'
            for d in [arch(74, 5), arch(57, 4)] + [rib(x) for x in (80, 100, 124, 144)]
        )
        p.append(f'{clip}<path d="{dome()} Z" fill="{color}"/><g clip-path="url(#shell-in)">{lines}</g>')
        add(BELLY, stroke * 1.2)
        p.append(f'<path d="{HEAD} Z" fill="{color}"/>')
        p.append(f'<circle cx="{EYE[0]}" cy="{EYE[1]}" r="{stroke*0.9:.2f}" fill="#F6F1E8"/>')
        for d in (LEG_FRONT, LEG_BACK):
            p.append(f'<path d="{d} Z" fill="{color}"/>')
        add(TAIL, stroke * 1.2)
    return "".join(p), "12 30 172 88"
