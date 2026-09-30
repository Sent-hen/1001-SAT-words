"""Landmark props and background painters for auto-composed panels.
Every prop is drawn at (x, base) with scale s; base = ground line y."""
import math, random
from art import *

def _g(c, x, y, s): return g(c, x, y, s)

# ------------------------------------------------------------ generic pieces
def awning(x, y, w, c1, c2="#fff"):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="18" fill="{c1}" stroke="{INK}" stroke-width="2"/>'
    for i in range(0, int(w), 16):
        out += f'<rect x="{x+i}" y="{y}" width="8" height="18" fill="{c2}" opacity="0.55"/>'
    out += "".join(P(f"M{x+i},{y+18} q8,10 16,0", c1, 2) for i in range(0, int(w) - 8, 16))
    return out

def stall(x, base, c="#e0533b", goods="#f4c542", w=90):
    return (awning(x, base - 110, w, c) + f'<rect x="{x+6}" y="{base-92}" width="6" height="92" fill="#6b4a2a"/><rect x="{x+w-12}" y="{base-92}" width="6" height="92" fill="#6b4a2a"/>'
            + f'<rect x="{x}" y="{base-40}" width="{w}" height="40" fill="#a0703a" stroke="{INK}" stroke-width="2"/>'
            + "".join(C(x + 12 + i * 16, base - 46, 8, goods, 1.5) for i in range(int(w / 16) - 1)))

def tower(x, base, h=180, w=60, c="#e8d6b0", roof="#c0262d", dome=False):
    out = f'<rect x="{x-w/2}" y="{base-h}" width="{w}" height="{h}" fill="{c}" stroke="{INK}" stroke-width="3"/>'
    out += P(f"M{x-10},{base-h+30} v20 h20 v-20 Q{x},{base-h+18} {x-10},{base-h+30} Z", "#2a2350", 2)
    if dome: out += P(f"M{x-w/2-4},{base-h} Q{x},{base-h-w} {x+w/2+4},{base-h} Z", roof, 3)
    else: out += P(f"M{x-w/2-6},{base-h} L{x},{base-h-40} L{x+w/2+6},{base-h} Z", roof, 3)
    return out

def dome_bldg(x, base, w=120, h=70, c="#e8d6b0", dc="#2e8b57"):
    return (f'<rect x="{x-w/2}" y="{base-h}" width="{w}" height="{h}" fill="{c}" stroke="{INK}" stroke-width="3"/>'
            + P(f"M{x-w/2+8},{base-h} Q{x},{base-h-w*0.75} {x+w/2-8},{base-h} Z", dc, 3)
            + P(f"M{x-12},{base} v-34 Q{x},{base-50} {x+12},{base-34} v34 Z", "#2a2350", 2))

def palm(x, base, h=150, s=1.0):
    t = P(f"M{x},{base} Q{x+10},{base-h/2} {x+4},{base-h}", "none", 10, "#7a5230")
    for a in (-160, -120, -60, -20, -90):
        r = math.radians(a)
        t += P(f"M{x+4},{base-h} Q{x+4+40*math.cos(r)},{base-h-30+40*math.sin(r)} {x+4+75*math.cos(r)},{base-h+10+60*math.sin(r)+30}", "none", 9, "#3f9b4a")
    return t

def boat(x, y, w=120, c="#8a5a2b", sail=True):
    out = P(f"M{x},{y} L{x+w},{y} L{x+w-18},{y+26} L{x+18},{y+26} Z", c, 3)
    if sail:
        out += L(x + w / 2, y, x + w / 2, y - 80, INK, 4) + P(f"M{x+w/2},{y-78} L{x+w/2+50},{y-12} L{x+w/2},{y-12} Z", "#f3efe1", 2.5)
    return out

def dune(x, base, w, h, c="#e8c77d"):
    return P(f"M{x},{base} Q{x+w/2},{base-h} {x+w},{base} Z", c, 2, "#c9a55a")

def tent(x, base, w=110, c="#2a2a2a", stripe="#b8923a"):
    return (P(f"M{x},{base} L{x+w/2},{base-80} L{x+w},{base} Z", c, 3) + P(f"M{x+w/2},{base-80} L{x+w/2-12},{base} L{x+w/2+12},{base} Z", "#1a1a1a", 2)
            + L(x + 10, base - 20, x + w - 10, base - 20, stripe, 4))

def arch_door(x, base, w=70, h=110, c="#2a2350"):
    return P(f"M{x-w/2},{base} v-{h-w/2} Q{x},{base-h-w/3} {x+w/2},{base-h+w/2} v{h-w/2} Z", c, 3)

def crowd(x, base, n=8, w=380, seed=1, c="#3a2f55"):
    r = random.Random(seed); out = ""
    for i in range(n):
        cx = x + w * (i + 0.5) / n + r.randint(-8, 8); hh = r.randint(40, 60)
        out += E(cx, base - hh + 8, 13, hh / 2, c, 0) + C(cx, base - hh - 10, 10, c, 0)
    return f'<g opacity="0.75">{out}</g>'

def gear(x, y, r, c="#b8862b"):
    pts = []
    for i in range(24):
        a = i * math.pi / 12; rr = r if i % 2 == 0 else r * 0.8
        pts.append(f"{x+rr*math.cos(a):.1f},{y+rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{c}" stroke="{INK}" stroke-width="2.5"/>' + C(x, y, r * 0.3, "#5a4210", 2)

def book(x, y, w=26, h=34, c="#8a3a2a"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{c}" stroke="{INK}" stroke-width="2"/><line x1="{x+4}" y1="{y}" x2="{x+4}" y2="{y+h}" stroke="#f4c542" stroke-width="2"/>'

def shelf_books(x, base, w=150, rows=3, seed=2):
    r = random.Random(seed); out = f'<rect x="{x}" y="{base-rows*42-6}" width="{w}" height="{rows*42+6}" fill="#6b4a2a" stroke="{INK}" stroke-width="3"/>'
    cols = ["#8a3a2a", "#2f6db5", "#3f9b4a", "#b8923a", "#6b2fa0", "#c0262d"]
    for rr in range(rows):
        yy = base - rows * 42 + rr * 42
        xx = x + 4
        while xx < x + w - 14:
            bw = r.randint(9, 15)
            out += f'<rect x="{xx}" y="{yy+4}" width="{bw}" height="34" fill="{r.choice(cols)}" stroke="{INK}" stroke-width="1.2"/>'
            xx += bw + 1
    return out

def jar(x, base, h=50, c="#c86f3a"):
    return P(f"M{x-10},{base-h} h20 q18,{h*0.35} 12,{h*0.8} q-4,{h*0.2} -22,{h*0.2} q-18,0 -22,-{h*0.2} q-6,-{h*0.45} 12,-{h*0.8} Z", c, 2.5)

def cage(x, base, w=40, h=50, bird="#f4c542"):
    out = P(f"M{x},{base} v-{h-12} Q{x+w/2},{base-h-10} {x+w},{base-h+12} v{h-12} Z", "none", 2.5, "#b8862b")
    out += "".join(L(x + i, base, x + i, base - h + 6, "#b8862b", 1.5) for i in range(8, int(w), 8))
    return E(x + w / 2, base - 18, 9, 8, bird, 2) + out

def fountain(x, base, s=1.0, water="#63aee0"):
    return _g(E(0, -10, 80, 16, "#d9d0c0", 3) + P("M-70,-10 L-60,0 L60,0 L70,-10", "#c9c0b0", 3) + E(0, -14, 64, 10, water, 2)
              + f'<rect x="-8" y="-70" width="16" height="58" fill="#d9d0c0" stroke="{INK}" stroke-width="3"/>' + E(0, -72, 30, 8, "#d9d0c0", 3)
              + P("M0,-80 Q-30,-120 -44,-70 M0,-80 Q30,-120 44,-70 M0,-80 L0,-118", "none", 4, water), x, base, s)

def rope_coil(x, base, s=1.0):
    return _g("".join(E(0, -8 - i * 12, 46 - i * 4, 12, "#c8a060", 2.5) for i in range(4)), x, base, s)

def sack(x, base, c="#c9a26a", label=""):
    return P(f"M{x-24},{base} q-6,-40 8,-52 l-4,-10 h40 l-4,10 q14,12 8,52 Z", c, 2.5) + (T(x, base - 20, label, 10, "#7a2a1a") if label else "")

def barrel(x, base, c="#8a5a2b"):
    return E(x, base - 30, 24, 32, c, 3) + L(x - 24, base - 42, x + 24, base - 42, INK, 2) + L(x - 24, base - 18, x + 24, base - 18, INK, 2)

def anvil(x, base, s=1.0):
    return _g(P("M-50,-60 h80 q20,0 30,-10 v14 q-14,10 -30,14 v12 h-10 v22 h20 v8 h-70 v-8 h20 v-22 h-10 v-12 q-16,0 -20,-10 Z", "#4a4a55", 3), x, base, s)

def target(x, base, s=1.0):
    return _g(C(0, -70, 50, "#f3efe1", 3) + C(0, -70, 36, "#c0262d", 2) + C(0, -70, 22, "#f3efe1", 2) + C(0, -70, 9, "#c0262d", 2)
              + L(-30, 0, -20, -30, "#6b4a2a", 6) + L(30, 0, 20, -30, "#6b4a2a", 6), x, base, s)

def telescope2(x, base, s=1.0):
    return _g(P("M-60,-60 L50,-110 L60,-92 L-50,-42 Z", "#d9a441", 3) + E(56, -100, 9, 12, "#9ad0ff", 2) + P("M0,-70 L-26,0 M0,-70 L26,0 M0,-70 L0,0", "none", 5, "#6b4a10"), x, base, s)

def astro(x, y, r=40):
    return C(x, y, r, "#d9a441", 3) + C(x, y, r * 0.75, "none", 2) + E(x, y, r, r * 0.35, "none", 2) + L(x - r, y, x + r, y, INK, 2) + L(x, y - r, x, y + r, INK, 2) + C(x, y, 5, INK, 0)

def sundial(x, base, s=1.0):
    return _g(E(0, -10, 90, 20, "#e8d6b0", 3) + P("M-6,-10 L50,-110 L60,-104 L6,-10 Z", "#b8862b", 3) + "".join(L(80 * math.cos(math.radians(a)), -10 + 16 * math.sin(math.radians(a)), 70 * math.cos(math.radians(a)), -10 + 13 * math.sin(math.radians(a)), INK, 2) for a in range(0, 360, 30)), x, base, s)

def well(x, base, s=1.0, water="#63aee0", glow=None):
    out = E(0, -40, 50, 14, water, 3) + P("M-50,-40 v36 q50,16 100,0 v-36", "#b9a88c", 3) + "".join(L(-50 + i * 20, -40, -50 + i * 20, -6, "#8a7a64", 1.5) for i in range(1, 5))
    out += L(-44, -40, -44, -110, "#6b4a2a", 6) + L(44, -40, 44, -110, "#6b4a2a", 6) + P("M-54,-110 L0,-140 L54,-110 Z", "#8a5a2b", 3)
    if glow: out = f'<circle cx="0" cy="-40" r="70" fill="{glow}" opacity="0.3"/>' + out
    return _g(out, x, base, s)

def bars(x, y, w, h, c="#555"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{c}" stroke-width="5"/>' + "".join(L(x + i, y, x + i, y + h, c, 5) for i in range(14, int(w), 16))

def throne2(x, base, s=1.0, c="#2e7d4f"):
    return _g(P("M-50,-170 Q0,-210 50,-170 L50,-50 L-50,-50 Z", c, 3) + P("M-64,-70 L64,-70 L64,-10 L-64,-10 Z", "#d9a441", 3) + P("M-50,-10 v10 M50,-10 v10", "none", 8) + C(0, -175, 8, "#2ecc71", 2), x, base, s)

def silver_tree(x, base, s=1.0):
    out = P("M-12,0 Q-8,-80 -2,-120 Q0,-160 -40,-200 M0,-130 Q30,-170 60,-190 M-4,-150 Q-10,-190 10,-230", "none", 12, "#c9ccd8")
    out = P("M-12,0 L12,0 L6,-120 L-6,-120 Z", "#c9ccd8", 3) + out
    for bx, by in [(-40, -200), (60, -190), (10, -230), (-60, -160), (40, -150)]:
        out += E(bx, by, 14, 9, "#e8e8f4", 2) + P(f"M{bx+12},{by} l10,-4 l-2,8 Z", "#f4c542", 1.5) + C(bx - 6, by - 2, 2, INK, 0)
    return _g(out, x, base, s)

def gate_big(x, base, w=220, h=210, c="#d9a441", door="#6b4a2a"):
    return (f'<rect x="{x-w/2-30}" y="{base-h}" width="{w+60}" height="{h}" fill="#e8d6b0" stroke="{INK}" stroke-width="3"/>'
            + P(f"M{x-w/2+20},{base} v-{h-70} Q{x},{base-h-10} {x+w/2-20},{base-h+70} v{h-70} Z", door, 3)
            + L(x, base, x, base - h + 20, INK, 3) + "".join(C(x + dx, base - 60 - i * 40, 4, c, 0) for dx in (-40, 40) for i in range(3)))

def mirror_big(x, base, s=1.0):
    return _g(E(0, -110, 55, 90, "#cfe8ff", 6, "#b8862b") + P("M-30,-160 Q-10,-150 -20,-100", "none", 6, "#fff", extra='opacity="0.7"'), x, base, s)

def horseman(x, base, s=1.0):
    return _g(P("M-60,-80 Q-60,-110 -20,-110 L40,-110 Q60,-160 80,-170 Q100,-160 96,-140 L70,-120 L60,-60 L-50,-60 Z", "#8a6a3a", 3)
              + "".join(P(f"M{xx},-62 v62", "none", 12, "#8a6a3a") for xx in (-44, -20, 30, 52))
              + P("M-10,-110 L-6,-170 L14,-170 L18,-110 Z", "#8a6a3a", 3) + C(4, -182, 12, "#8a6a3a", 3) + L(18, -150, 90, -230, "#5a4210", 5), x, base, s)

def lexicon(x, y, s=1.0, broken=False):
    out = f'<circle cx="0" cy="0" r="70" fill="#ffe066" opacity="0.25"/>' + P("M-50,-30 L0,-40 L50,-30 L50,30 L0,20 L-50,30 Z", "#bfe9ff", 3) + L(0, -40, 0, 20, INK, 2)
    if broken: out += P("M-20,-34 L-8,-6 L-24,10 L-10,26", "none", 3)
    return _g(out, x, y, s)

def kite(x, y, c="#e0533b", s=1.0):
    return _g(P("M0,-30 L22,0 L0,40 L-22,0 Z", c, 2.5) + L(0, -30, 0, 40, INK, 1.5) + L(-22, 0, 22, 0, INK, 1.5) + P("M0,40 q10,20 -4,40 q-10,20 6,40", "none", 1.5), x, y, s)

def camel(x, base, s=1.0, saddle="#c0262d"):
    return _g(P("M-60,-60 Q-50,-100 -20,-90 Q-5,-120 20,-92 Q40,-80 52,-90 L70,-120 Q84,-130 88,-116 L70,-80 Q60,-56 40,-56 L-50,-56 Z", "#c9a26a", 3)
              + "".join(P(f"M{xx},-58 v58", "none", 9, "#c9a26a") for xx in (-44, -24, 20, 38)) + P("M-24,-96 q20,-12 40,0 v12 h-40 Z", saddle, 2), x, base, s)

def horse(x, base, s=1.0, c="#2a1a12"):
    return _g(P("M-60,-80 Q-60,-110 -20,-110 L40,-110 Q60,-160 80,-170 Q100,-160 96,-140 L70,-120 L60,-60 L-50,-60 Z", c, 3)
              + "".join(P(f"M{xx},-62 v62", "none", 11, c) for xx in (-44, -20, 30, 52)) + P("M-60,-90 Q-90,-70 -84,-40", "none", 7, c) + C(84, -156, 3, "#fff", 0), x, base, s)

def giraffe(x, base, s=1.0):
    return _g(P("M-40,-60 h70 v-10 l10,-110 q4,-20 20,-14 l6,10 l-12,6 l-8,108 v10 Z", "#f0b848", 3) + "".join(C(xx, yy, 5, "#a0602a", 0) for xx, yy in [(-20, -52), (0, -48), (18, -54), (44, -100), (48, -140)])
              + "".join(P(f"M{xx},-60 v60", "none", 7, "#f0b848") for xx in (-34, -16, 10, 24)), x, base, s)

def elephant(x, base, s=1.0, c="#8a8a95"):
    return _g(E(0, -70, 60, 45, c, 3) + C(50, -100, 32, c, 3) + P("M76,-90 Q96,-40 80,-10", "none", 14, c) + C(58, -108, 4, INK, 0) + P("M24,-120 Q0,-150 20,-70", c, 3)
              + "".join(P(f"M{xx},-30 v30", "none", 16, c) for xx in (-40, -10, 20, 44)), x, base, s)

def lion(x, base, s=1.0, c="#d9a441", mane="#b8862b", eye="#35e0d0"):
    mn = "".join(C(40 + 30 * math.cos(a), -110 + 30 * math.sin(a), 14, mane, 2) for a in [i * math.pi / 6 for i in range(12)])
    return _g(P("M-70,-30 Q-80,-90 -30,-96 L40,-96 Q56,-80 56,-50 L56,0 L38,0 L34,-30 L-36,-30 L-40,0 L-58,0 Z", c, 3) + mn + C(40, -110, 26, c, 3)
              + C(32, -116, 4, eye, 1) + C(50, -116, 4, eye, 1) + P("M34,-98 Q41,-92 48,-98", "none", 3), x, base, s)

def eagle(x, base, s=1.0, c="#d9a441"):
    return _g(P("M-90,-120 Q-40,-170 0,-110 Q40,-170 90,-120 Q40,-100 0,-80 Q-40,-100 -90,-120 Z", c, 3) + E(0, -80, 22, 34, c, 3) + C(0, -128, 18, c, 3)
              + P("M10,-128 l16,6 l-16,4 Z", "#b8862b", 2) + C(-4, -132, 4, "#35e0d0", 1.5) + P("M-10,-46 l-6,40 M10,-46 l6,40", "none", 5), x, base, s)

def brass_horse(x, base, s=1.0):
    return _g(P("M-60,-100 Q-60,-130 -20,-130 L30,-130 Q50,-190 80,-200 Q104,-190 98,-166 L72,-146 L62,-80 L-50,-80 Z", "#d9a441", 3)
              + P("M-44,-82 L-60,-20 M-20,-82 L-24,0 M36,-82 L60,-150 M54,-82 L80,-140", "none", 11, "#d9a441") + C(86, -184, 4, "#35e0d0", 1.5)
              + P("M-60,-110 Q-90,-90 -84,-60", "none", 6, "#b8862b"), x, base, s)

def serpent_coil(x, y, w=380):
    return P(f"M{x},{y} q{w/6},-60 {w/3},0 t{w/3},0 t{w/3},0", "none", 34, "#1f8a8a") + "".join(C(x + w * i / 6, y - 10 * (i % 2), 5, "#9fd8cf", 2) for i in range(1, 6))

def clock_face(x, y, r=46):
    return C(x, y, r, "#f3efe1", 4) + "".join(L(x + (r - 8) * math.cos(a), y + (r - 8) * math.sin(a), x + r * math.cos(a), y + r * math.sin(a), INK, 2) for a in [i * math.pi / 6 for i in range(12)]) + L(x, y, x, y - r * 0.6, INK, 4) + L(x, y, x + r * 0.45, y, INK, 3)

def vat(x, base, w=100, c="#15152a"):
    return E(x, base - 60, w / 2, 14, c, 3) + P(f"M{x-w/2},{base-60} v50 q{w/2},16 {w},0 v-50", "#6b4a2a", 3) + "".join(C(x - 20 + i * 18, base - 64, 5, "#3b3b6e", 0) for i in range(3))

def cloth_line(x1, x2, y, cols=("#c0262d", "#2f6db5", "#f4c542", "#3f9b4a", "#6b2fa0")):
    out = P(f"M{x1},{y} Q{(x1+x2)/2},{y+14} {x2},{y}", "none", 2)
    n = int((x2 - x1) / 36)
    for i in range(n):
        cx = x1 + 12 + i * 36
        out += f'<rect x="{cx}" y="{y+6}" width="28" height="{40+(i%3)*10}" fill="{cols[i%len(cols)]}" stroke="{INK}" stroke-width="1.5"/>'
    return out

def windcatcher(x, base, h=200):
    return f'<rect x="{x-30}" y="{base-h}" width="60" height="{h}" fill="#e0c28a" stroke="{INK}" stroke-width="3"/>' + "".join(f'<rect x="{x-22+i*16}" y="{base-h+8}" width="10" height="36" fill="#6b4a2a"/>' for i in range(3))

def pigeon_wall(x, base, w=180, h=180):
    out = f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="#d9c7a0" stroke="{INK}" stroke-width="3"/>'
    for r in range(4):
        for c in range(5):
            cx, cy = x + 20 + c * 34, base - h + 26 + r * 40
            out += P(f"M{cx-10},{cy+10} v-10 q10,-12 20,0 v10 Z", "#3a2f25", 1.5)
    return out

def spikes(x1, x2, y):
    return "".join(P(f"M{x},{y} l6,-24 l6,24 Z", "#555", 2) for x in range(int(x1), int(x2), 14))

def vault_door(x, y, r=90):
    return C(x, y, r, "#8a8a95", 5) + C(x, y, r * 0.7, "#a5a5b0", 3) + "".join(L(x, y, x + r * 0.6 * math.cos(a), y + r * 0.6 * math.sin(a), INK, 5) for a in [i * math.pi / 3 for i in range(6)]) + C(x, y, 12, "#555", 3)

def canopy_bed(x, base, s=1.0):
    return _g(P("M-120,-60 h240 v40 h-240 Z", "#e8e0f0", 3) + P("M-120,-20 v20 M120,-20 v20", "none", 8) + P("M-120,-60 v-120 M120,-60 v-120", "none", 6, "#b8862b")
              + P("M-130,-180 Q0,-230 130,-180 L120,-150 Q0,-190 -120,-150 Z", "#2e7d4f", 3) + E(-80, -68, 30, 12, "#fff", 2), x, base, s)

def stars_crown(x, y, n=9, r=60):
    return "".join(sparkle(x + r * math.cos(math.pi + i * math.pi / (n - 1)), y + r * 0.5 * math.sin(math.pi + i * math.pi / (n - 1)), 9) for i in range(n))

def moat(y, w=400):
    return f'<rect x="0" y="{y}" width="{w}" height="{300-y}" fill="#2a6b7a"/>' + "".join(E(40 + i * 90, y + 24, 8, 5, "#ffe066", 0, extra='opacity="0.8"') for i in range(int(w / 90)))

def reeds(x1, x2, base, h=150, seed=4):
    r = random.Random(seed)
    return "".join(P(f"M{x},{base} Q{x+r.randint(-10,10)},{base-h/2} {x+r.randint(-14,14)},{base-h+r.randint(-20,20)}", "none", 4, r.choice(["#6b8f3a", "#8aa94a", "#577a2e"])) for x in range(int(x1), int(x2), 7))

def lotus(x, y):
    return E(x, y + 6, 26, 8, "#3f9b4a", 2) + "".join(P(f"M{x},{y} q{dx},-26 {dx*1.4},0", "#ff9fc4", 2) for dx in (-14, -6, 6, 14))

def pomegranate_tree(x, base, s=1.0):
    return _g(P("M-8,0 L8,0 L4,-80 L-4,-80 Z", "#7a5230", 3) + C(0, -110, 60, "#3f7a3a", 3) + "".join(C(xx, yy, 8, "#c0262d", 2) for xx, yy in [(-30, -110), (20, -130), (30, -90), (-10, -80), (0, -140)]), x, base, s)

def hedge(x1, x2, base, h=150):
    return f'<rect x="{x1}" y="{base-h}" width="{x2-x1}" height="{h}" rx="14" fill="#2f6b30" stroke="{INK}" stroke-width="3"/>' + "".join(C(x, base - h + 6, 12, "#3a7d3a", 0) for x in range(int(x1) + 12, int(x2), 22))

def roses(x1, x2, base, faces=True):
    out = ""
    for i, x in enumerate(range(int(x1), int(x2), 40)):
        y = base - 60 - (i % 2) * 20
        out += L(x, base, x, y, "#2f6b30", 4) + C(x, y, 14, "#d6334b", 2.5)
        if faces: out += C(x - 4, y - 2, 2, INK, 0) + C(x + 4, y - 2, 2, INK, 0) + P(f"M{x-5},{y+5} q5,-4 10,0", "none", 1.5)
    return out

def still(x, base, s=1.0):
    return _g(E(0, -50, 46, 44, "#c87f3a", 3) + P("M20,-90 Q60,-130 90,-80 L90,-10", "none", 8, "#c87f3a") + E(90, -10, 14, 10, "#ff9fc4", 2)
              + f'<rect x="-30" y="-10" width="60" height="10" fill="#555"/>' + P("M-20,-2 q6,-14 12,0 q6,-14 12,0 q6,-14 12,0", "#ff7a1a", 1.5), x, base, s)

def sextant(x, base, s=1.0):
    return _g(P("M-160,0 A160,160 0 0 1 0,-160 L0,-130 A130,130 0 0 0 -130,0 Z", "#e8d6b0", 3) + "".join(L(-145 * math.cos(math.radians(a)), -145 * math.sin(math.radians(a)), -130 * math.cos(math.radians(a)), -130 * math.sin(math.radians(a)), INK, 2) for a in range(0, 91, 10)), x, base, s)

def watermelon(x, y, r=18):
    return E(x, y, r * 1.3, r, "#2e8b3a", 2.5) + P(f"M{x-r},{y-4} q{r},-6 {r*2},0 M{x-r},{y+5} q{r},6 {r*2},0", "none", 2, "#8fd48a")

def fish(x, y, s=1.0, c="#c9d6e0"):
    return _g(E(0, 0, 22, 9, c, 2) + P("M20,0 l12,-9 v18 Z", c, 2) + C(-12, -2, 2, INK, 0), x, y, s)

def pier_posts(y, w=400):
    return f'<rect x="0" y="{y}" width="{w}" height="14" fill="#8a5a2b" stroke="{INK}" stroke-width="2"/>' + "".join(f'<rect x="{x}" y="{y+14}" width="10" height="{300-y}" fill="#6b4a2a"/>' for x in range(20, w, 70))

def ship_ribs(x, base, s=1.0):
    return _g("".join(P(f"M{-120+i*30},0 Q{-130+i*30},-100 {-110+i*30},-150", "none", 7, "#8a6a4a") for i in range(9)) + P("M-130,-20 Q0,20 130,-20", "none", 8, "#6b4a2a"), x, base, s)

def big_egg(x, base, s=1.0, cracked=False):
    out = E(0, -60, 44, 58, "#f3e2c0", 3) + "".join(C(xx, yy, 5, "#e0533b", 0) for xx, yy in [(-20, -80), (10, -40), (18, -90), (-6, -60), (-24, -30)])
    if cracked: out += P("M-30,-70 l12,8 l8,-10 l12,10 l10,-8 l12,8", "none", 3) + f'<circle cx="0" cy="-60" r="70" fill="#ffe066" opacity="0.25"/>'
    return _g(E(0, -4, 60, 10, "#c8a060", 2) + out, x, base, s)

def bell(x, y, s=1.0, c="#b8862b"):
    return _g(P("M-40,40 Q-38,-30 0,-34 Q38,-30 40,40 Z", c, 3) + C(0, 44, 9, c, 3) + L(0, -34, 0, -60, INK, 4), x, y, s)

def chain_line(x1, y1, x2, y2, n=10):
    out = ""
    for i in range(n):
        t = (i + 0.5) / n
        out += E(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, 14, 8, "#555a66", 3)
    return out

def toll_bar(x, base):
    return f'<rect x="{x-8}" y="{base-80}" width="16" height="80" fill="#6b4a2a" stroke="{INK}" stroke-width="2"/>' + "".join(f'<rect x="{x+10+i*24}" y="{base-78}" width="24" height="12" fill="{"#c0262d" if i%2 else "#f3efe1"}" stroke="{INK}" stroke-width="1.5"/>' for i in range(8))

def carpet_hang(x, y, w=60, h=90, c="#a0303a", c2="#f4c542"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="{INK}" stroke-width="2"/>' + P(f"M{x+w/2},{y+10} l{w/3},{h/2-10} l-{w/3},{h/2-10} l-{w/3},-{h/2-10} Z", c2, 1.5) + "".join(L(x + i, y + h, x + i, y + h + 8, c2, 1.5) for i in range(4, w, 6))

def bottles(x, base, n=6):
    cols = ["#ff9fc4", "#9ad0ff", "#b48cff", "#8fe0b0", "#ffd166"]
    return "".join(P(f"M{x+i*22},{base} v-24 q0,-8 6,-10 v-8 h6 v8 q6,2 6,10 v24 Z", cols[i % 5], 2) for i in range(n))

def spice_cones(x, base, n=5):
    cols = ["#d6332b", "#f4c542", "#e07b1f", "#8a3a1a", "#6b8f3a"]
    return "".join(P(f"M{x+i*38},{base} l18,-50 l18,50 Z", cols[i % 5], 2.5) for i in range(n))

def pot_stack(x, base):
    return "".join(E(x + dx, base - dy, 20, 8, "#c87f3a", 2) + P(f"M{x+dx-20},{base-dy} q20,24 40,0", "#c87f3a", 2) for dx, dy in [(0, 12), (44, 12), (22, 40), (88, 12)])

def glass_blobs(x, base):
    cols = ["#8fe0ff", "#b48cff", "#8fe0b0", "#ffd166"]
    return "".join(C(x + i * 30, base - 20 - (i % 2) * 14, 14, cols[i % 4], 2, extra='opacity="0.85"') for i in range(5))

def dye_pools(x, base):
    cols = ["#d6332b", "#2f6db5", "#f4c542", "#3f9b4a", "#6b2fa0"]
    return "".join(E(x + i * 70, base - 10, 32, 10, cols[i], 3) for i in range(5))

def salt_mounds(x, base):
    return "".join(P(f"M{x+i*80},{base} q40,-{50+(i%2)*20} 80,0 Z", "#f7f7f2", 2, "#c9c9c0") for i in range(4))

def ruins(x, base):
    return (P(f"M{x},{base} v-120 h24 v120 Z", "#b9a88c", 3) + P(f"M{x+80},{base} v-80 h24 v80 Z", "#b9a88c", 3)
            + P(f"M{x-6},{base-120} h50 l-10,12 h-34 Z", "#a89878", 3) + P(f"M{x+160},{base} v-150 q30,-40 60,0 v150 h-20 v-120 q-10,-14 -20,0 v120 Z", "#b9a88c", 3))

def gold_gate(x, base, s=1.0):
    return _g(f'<circle cx="0" cy="-120" r="150" fill="#ffe066" opacity="0.25"/>' + gate_big(0, 0, 200, 220, "#fff6c9", "#f4c542"), x, base, s)

def flags_row(x, y, n=6):
    cols = ["#c0262d", "#2f6db5", "#f4c542", "#3f9b4a", "#6b2fa0", "#f3efe1"]
    return "".join(L(x + i * 60, y, x + i * 60, y + 90, "#6b4a2a", 3) + P(f"M{x+i*60},{y} h36 l-8,12 l8,12 h-36 Z", cols[i % 6], 2) for i in range(n))

def table_map(x, base, w=240):
    return (P(f"M{x-w/2},{base-60} h{w} l20,30 h-{w+40} Z", "#d9c7a0", 3) + P(f"M{x-w/2-20},{base-30} v30 M{x+w/2+20},{base-30} v30", "none", 8, "#6b4a2a")
            + C(x, base - 45, 18, "none", 2, "#157a4f") + "".join(C(x - 60 + i * 30, base - 42 + (i % 2) * 6, 4, ["#c0262d", "#2f6db5"][i % 2], 0) for i in range(5)))

PROP_OF = {  # chapter -> list of (func, relative placement) : drawn in back layer
}
