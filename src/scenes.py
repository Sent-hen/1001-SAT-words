"""Panel backgrounds, speech bubbles and effects. Panel viewBox: 0 0 400 300 (wide panels: 0 0 1200 300)."""
import math, textwrap, random, json, os
VOCAB = {w["word"].lower() for c in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "saga.json"), encoding="utf-8")) for w in c["words"]}
from art import *
from characters import SPECS

def fig(name, x, y, s=0.42, expr="happy", pose=("down", "down"), legpose="stand", flip=False, extra="", rot=0):
    return g(human(SPECS[name], expr, pose, legpose), x, y, s, flip, extra, rot)

# ---------------------------------------------------------------- text
def wrap(text, width):
    return textwrap.wrap(text, width=width)

def bubble(x, y, w, text, tail=None, border=INK, size=12.5, shout=False, scroll=False, bold_words=()):
    chars = max(8, int(w / (size * 0.62)))
    lines = wrap(text, chars)
    h = len(lines) * (size + 3) + 14
    out = ""
    if tail:
        tx, ty = tail
        bx = x + w / 2
        out += P(f"M{bx-10},{y+h/2} L{tx},{ty} L{bx+10},{y+h/2} Z", "#fff", 2.5, border)
    if scroll:
        out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#efe2c0" stroke="{border}" stroke-width="2.5"/>'
        out += C(x, y + h / 2, 7, "#d9c79a", 2, border) + C(x + w, y + h / 2, 7, "#d9c79a", 2, border)
    elif shout:
        pts = []
        cx, cy = x + w / 2, y + h / 2
        for i in range(24):
            a = i * math.pi / 12
            r = 1.18 if i % 2 == 0 else 1.0
            pts.append(f"{cx + (w/2+8)*r*math.cos(a):.1f},{cy + (h/2+8)*r*math.sin(a):.1f}")
        out += f'<polygon points="{" ".join(pts)}" fill="#fff" stroke="{border}" stroke-width="2.5"/>'
    else:
        out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(18, h/2)}" fill="#fff" stroke="{border}" stroke-width="2.5"/>'
    for i, ln in enumerate(lines):
        yy = y + 7 + size + i * (size + 3) - 2
        # emphasize the vocabulary word (written in CAPS)
        parts = []
        for tok in ln.split(" "):
            core = tok.strip(".,!?\"'—:;")
            if core.lower() in VOCAB:
                parts.append(f'<tspan fill="#c0262d" font-weight="900">{tok}</tspan>')
            else:
                parts.append(tok)
        out += f'<text x="{x + w/2}" y="{yy}" font-size="{size}" text-anchor="middle" font-family="\'Comic Neue\',\'Comic Sans MS\',Arial,sans-serif" font-weight="700" fill="{INK}">{" ".join(parts)}</text>'
    return out

def caption(x, y, w, text, size=11.5, fill="#ffe9a8"):
    lines = wrap(text, int(w / (size * 0.52)))
    h = len(lines) * (size + 3) + 10
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
    for i, ln in enumerate(lines):
        out += f'<text x="{x+7}" y="{y + 5 + size + i*(size+3) - 1}" font-size="{size}" font-family="Georgia,serif" font-style="italic" font-weight="600" fill="{INK}">{ln}</text>'
    return out

def sfx(x, y, text, size=34, fill="#ffd23f", rot=-8):
    return T(x, y, text, size, fill, extra=f'stroke="{INK}" stroke-width="3" paint-order="stroke" transform="rotate({rot} {x} {y})" letter-spacing="2"')

def word_tag(x, y, word):
    w = len(word) * 11 + 22
    return (f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="#ffd23f" stroke="{INK}" stroke-width="2.5"/>'
            + T(x + w / 2, y + 19, word.upper(), 16, "#c0262d", extra='letter-spacing="1.5"'))

# ---------------------------------------------------------------- backgrounds
def stars(n=40, seed=1, w=400, h=180):
    r = random.Random(seed)
    return "".join(C(r.randint(5, w - 5), r.randint(5, h), r.choice([1, 1.3, 1.8]), "#fff", 0, extra=f'opacity="{r.uniform(.4,1):.2f}"') for _ in range(n))

def night_sky(w=400, h=300, seed=1, top="#0e1238", bottom="#3b2a6b"):
    return (f'<defs><linearGradient id="ns{seed}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#ns{seed})"/>' + stars(45, seed, w, int(h * 0.6)))

def green_moon(x, y, r=30):
    return (f'<circle cx="{x}" cy="{y}" r="{r*2.2}" fill="#7dff9a" opacity="0.18"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#9dffb0" stroke="#2e8b57" stroke-width="2"/>'
            f'<circle cx="{x+r*0.45}" cy="{y-r*0.15}" r="{r*0.92}" fill="#15183f"/>')

def skyline(w=400, base=300, color="#1c1840", seed=3, dome=True):
    r = random.Random(seed)
    out, x = "", -10
    while x < w:
        bw, bh = r.randint(30, 60), r.randint(30, 90)
        out += f'<rect x="{x}" y="{base-bh}" width="{bw}" height="{bh}" fill="{color}"/>'
        if r.random() < 0.4:
            out += f'<circle cx="{x+bw/2}" cy="{base-bh}" r="{bw/2.4}" fill="{color}"/>'
        if r.random() < 0.5:
            out += f'<rect x="{x+bw/3}" y="{base-bh+12}" width="5" height="7" fill="#ffcf6b" opacity="0.8"/>'
        x += bw - 2
    if dome:
        cx = w * 0.62
        out += f'<rect x="{cx-26}" y="{base-120}" width="52" height="60" fill="{color}"/><circle cx="{cx}" cy="{base-120}" r="30" fill="#1f5f3f"/>'
    return out

def sea(w=400, y=240, h=60):
    out = f'<rect x="0" y="{y}" width="{w}" height="{h}" fill="#16305c"/>'
    for i in range(0, w, 40):
        out += P(f"M{i},{y+14} q10,-6 20,0 q10,6 20,0", "none", 2, "#4a78b8")
    return out

def stone_wall(w=400, h=300, c1="#6b5a7e", c2="#58486b"):
    out = f'<rect width="{w}" height="{h}" fill="{c1}"/>'
    for row in range(0, h, 30):
        off = 0 if (row // 30) % 2 else 30
        for col in range(-60 + off, w, 60):
            out += f'<rect x="{col}" y="{row}" width="60" height="30" fill="none" stroke="{c2}" stroke-width="2"/>'
    return out

def lighthouse_ext(x=200, base=300, s=1.0):
    t = (P(f"M{-70},0 L{-45},-260 L{45},-260 L{70},0 Z", "#efe6d6", 4) +
         "".join(P(f"M{-70+i*3.6},{-i*52} L{70-i*3.6},{-i*52}", "none", 3, "#c9b89a") for i in range(1, 5)) +
         P("M-34,0 L-34,-70 Q0,-120 34,-70 L34,0 Z", "#2a2350", 4) +
         P("M-50,-260 L50,-260 L40,-300 L-40,-300 Z", "#d9a441", 4) +
         C(0, -318, 28, "#ffd84d", 3) + f'<circle cx="0" cy="-318" r="60" fill="#ffd84d" opacity="0.2"/>' +
         P("M-20,-346 Q0,-372 20,-346", "none", 4, "#d9a441"))
    return g(t, x, base, s)

def compass_floor(cx=200, cy=270, rx=190, ry=40):
    out = E(cx, cy, rx, ry, "#c7a86a", 3) + E(cx, cy, rx * 0.7, ry * 0.7, "#e0c78d", 2)
    for a in range(0, 360, 45):
        ex, ey = cx + rx * 0.68 * math.cos(math.radians(a)), cy + ry * 0.68 * math.sin(math.radians(a))
        out += L(cx, cy, ex, ey, "#8a6418", 2.5)
    out += P(f"M{cx},{cy-ry*0.7} L{cx+14},{cy} L{cx},{cy+ry*0.7} L{cx-14},{cy} Z", "#c0262d", 2)
    return out

def telescope(x, y, s=1.0):
    return g(P("M-80,-20 L70,-90 L84,-64 L-66,6 Z", "#d9a441", 3) + E(78, -76, 12, 16, "#9ad0ff", 3) +
             P("M-10,-30 L-40,60 M-10,-30 L20,60 M-10,-30 L-10,60", "none", 5, "#6b4a10"), x, y, s)

def spiral_stair(x=200, top=0, bottom=300, w=160):
    out = ""
    for i in range(9):
        yy = bottom - i * 36
        sx = x + (w / 2 if i % 2 else -w / 2) * 0.6
        out += P(f"M{x},{yy} L{sx},{yy-14} L{sx},{yy-4} L{x},{yy+10} Z", "#b8a58a", 2.5)
    out += L(x, top, x, bottom, "#8a7a64", 12)
    return out

def arch_frame(w=400, h=300, color="#efe6d6"):
    return P(f"M0,0 H{w} V{h} H{w-50} V110 Q{w/2},-20 50,110 V{h} H0 Z", color, 4)

def window_round(cx, cy, r, inner=""):
    return (f'<clipPath id="wr{cx}{cy}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
            f'<g clip-path="url(#wr{cx}{cy})">{inner}</g>' + C(cx, cy, r, "none", 12, "#b8862b") + C(cx, cy, r + 7, "none", 3))

def rope_pillar(x, top=0, bottom=300, w=46):
    out = f'<rect x="{x-w/2}" y="{top}" width="{w}" height="{bottom-top}" fill="#d8cbb0" stroke="{INK}" stroke-width="3"/>'
    for yy in range(int(top) + 10, int(bottom), 22):
        out += P(f"M{x-w/2},{yy} L{x+w/2},{yy+12}", "none", 5, "#a0703a")
    return out

def gray_wash(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#7a7a7a" opacity="0.55" style="mix-blend-mode:saturation"/>'

def speed_lines(cx, cy, n=18, r1=120, r2=260, color="#fff", op=0.5):
    out = ""
    for i in range(n):
        a = i * 2 * math.pi / n
        out += L(cx + r1 * math.cos(a), cy + r1 * math.sin(a), cx + r2 * math.cos(a), cy + r2 * math.sin(a), color, 2.5, f'opacity="{op}"')
    return out

def panel(content, w=400, h=300):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice"><g>{content}</g><rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" fill="none" stroke="{INK}" stroke-width="5"/></svg>'
