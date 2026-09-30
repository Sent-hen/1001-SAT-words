import json, math
from art import INK, T, P, C, E, L, sparkle

D = json.load(open("../data/saga.json"))
W, H = 1500, 1160
CX, CY = 640, 470
R_WALL, R_OUT, R_IN, R_HEART = 250, 308, 185, 100

DISTRICTS = [
    ("Harbor of a Thousand Sails", "#2f6db5"), ("Bridge of Boats &amp; Islands", "#1f8a8a"), ("Karkh Bazaar", "#e0533b"),
    ("Garden Quarter &amp; Sarat Canal", "#3f9b4a"), ("Basra Gate · Brass Lion", "#d18b1f"), ("Kufa Gate · Brass Elephant", "#8a5a2b"),
    ("Syrian Gate · Brass Eagle", "#b8923a"), ("Khurasan Gate · Brass Horse", "#6b4fa0"), ("The Inner Ring", "#c0262d"),
    ("The Heart · Green Dome", "#157a4f"),
]

def along(pts, n=10):
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(seg); out = []
    for k in range(n):
        t = total * (k + 0.5) / n
        for i, s in enumerate(seg):
            if t <= s:
                f = t / s
                out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)); break
            t -= s
    return out

def arc(r, a0, a1, n=10, cx=CX, cy=CY):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * (k + 0.5) / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * (k + 0.5) / n))) for k in range(n)]

def spiral(n=10):
    out = []
    for k in range(n):
        a = math.radians(-10 + k * 64)
        r = R_HEART - 12 - k * 7.4
        out.append((CX + r * math.cos(a), CY + r * math.sin(a)))
    return out

routes = [
    along([(1180, 1120), (1175, 1000), (1185, 880), (1175, 790)]),               # harbor S->N east bank
    along([(1160, 760), (1090, 720), (1040, 770), (990, 720), (930, 760)]),      # bridge E->W through islands
    along([(920, 1045), (360, 1045)]),                                             # bazaar E->W
    along([(340, 900), (560, 925), (820, 905)]),                                 # gardens W->E
    arc(R_OUT, 45, 125), arc(R_OUT, 135, 215), arc(R_OUT, 225, 305), arc(R_OUT, 315, 395),
    arc(R_IN, 0, 324, 10), spiral(),
]

def svg():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         "<style>@import url('https://fonts.googleapis.com/css2?family=Bangers&amp;display=swap');</style>",
         f'<rect width="{W}" height="{H}" fill="#f1dfb4"/>',
         '<defs><pattern id="sand" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="1.2" fill="#d9c08a"/></pattern></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#sand)"/>']
    # desert NW
    o.append(P("M0,0 L420,0 Q300,90 180,120 Q80,160 0,260 Z", "#e8c77d", 2, "#c9a55a"))
    o.append(T(130, 70, "DESERT · to Syria", 22, "#8a6a2a"))
    # river Tigris
    river = "M1060,-10 Q1010,160 1060,330 Q1120,520 1060,700 Q1010,900 1090,1170"
    o.append(P(river, "none", 120, "#3a86b8")); o.append(P(river, "none", 104, "#63aee0"))
    for y in range(60, 1060, 90):
        o.append(P(f"M{1030 + 20*math.sin(y)},{y} q14,-8 28,0 q14,8 28,0", "none", 2, "#e8f6ff"))
    o.append(T(1115, 150, "RIVER TIGRIS", 26, "#1c4f78", extra='transform="rotate(80 1115 150)"'))
    # islands
    for x, y, r in [(1085, 705, 26), (1035, 795, 22), (1000, 690, 18)]:
        o.append(E(x, y, r, r * 0.7, "#8cc46a", 3))
    # bridge of boats
    o.append(P("M1160,760 L1090,720 L1040,770 L990,720 L930,760", "none", 14, "#8a5a2b"))
    o.append(P("M1160,760 L1090,720 L1040,770 L990,720 L930,760", "none", 4, "#e0b36a", extra='stroke-dasharray="6 6"'))
    # harbor docks east bank
    o.append(P("M1150,1160 L1150,780 L1500,780 L1500,1160 Z", "#d9c7a0", 2))
    for y in (840, 920, 1000, 1080):
        o.append(P(f"M1150,{y} h-40", "none", 10, "#8a5a2b"))
        o.append(P(f"M1105,{y-18} q12,22 30,0 l-6,-6 h-18 Z", "#fff", 2))
    o.append(T(1330, 830, "HARBOR", 30, "#2f6db5"))
    # Karkh bazaar block & gardens
    o.append(P("M330,1010 h620 v70 h-620 Z", "#f0b48a", 2)); o.append(T(640, 1105, "KARKH BAZAAR", 26, "#a8321c"))
    o.append(P("M320,870 Q560,850 850,870 L850,945 Q560,965 320,945 Z", "#a9d68f", 2))
    o.append(P("M290,955 Q560,975 930,945", "none", 10, "#63aee0"))
    o.append(T(280, 960, "SARAT CANAL", 16, "#1c4f78", anchor="end"))
    # round city
    o.append(C(CX, CY, R_WALL + 22, "#63aee0", 4))  # moat
    o.append(C(CX, CY, R_WALL + 6, "#e7cf9a", 0))
    o.append(C(CX, CY, R_WALL, "#e9d5a8", 10, "#a47b3c"))
    o.append(C(CX, CY, R_IN + 32, "none", 6, "#a47b3c"))
    o.append(C(CX, CY, R_HEART + 22, "#d8ecd8", 5, "#157a4f"))
    # four roads
    for a in (45, 135, 225, 315):
        x1, y1 = CX + (R_WALL + 60) * math.cos(math.radians(a)), CY + (R_WALL + 60) * math.sin(math.radians(a))
        x2, y2 = CX + (R_HEART + 22) * math.cos(math.radians(a)), CY + (R_HEART + 22) * math.sin(math.radians(a))
        o.append(L(x1, y1, x2, y2, "#c9a55a", 14))
    gates = [(45, "BASRA GATE", "LION"), (135, "KUFA GATE", "ELEPHANT"), (225, "SYRIAN GATE", "EAGLE"), (315, "KHURASAN GATE", "HORSE")]
    for a, name, beast in gates:
        x, y = CX + R_WALL * math.cos(math.radians(a)), CY + R_WALL * math.sin(math.radians(a))
        o.append(f'<rect x="{x-20}" y="{y-20}" width="40" height="40" rx="6" fill="#d9a441" stroke="{INK}" stroke-width="3" transform="rotate({a} {x} {y})"/>')
        lx, ly = CX + (R_WALL + 150) * math.cos(math.radians(a)), CY + (R_WALL + 150) * math.sin(math.radians(a))
        if a == 45: lx, ly = 905, 815
        o.append(T(lx, ly, name, 19, "#6b4a10") + T(lx, ly + 18, f"Brass {beast.title()}", 13, "#6b4a10", family="Georgia,serif"))
    # green dome
    o.append(C(CX, CY + 2, 22, "#2ecc71", 3))
    o.append(L(CX, CY - 32, CX, CY - 56, INK, 3)); o.append(sparkle(CX, CY - 64, 12))
    o.append(T(CX, CY + R_HEART + 44, "GREEN DOME", 16, "#0d5a39"))
    # route line
    allpts = [p for r in routes for p in r]
    path = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in allpts)
    o.append(P(path, "none", 5, "#7a2a1a", extra='stroke-dasharray="3 9" opacity="0.7"'))
    # dots
    for d, pts in enumerate(routes):
        col = DISTRICTS[d][1]
        for k, (x, y) in enumerate(pts):
            n = d * 10 + k + 1
            rr = (11 if n > 90 else 13) if n < 100 else 17
            o.append(C(round(x), round(y), rr, col, 2.5, "#fff"))
            o.append(T(round(x), round(y) + 5, str(n), 13 if n < 100 else 14, "#fff", family="Arial,sans-serif", weight="800"))
    # start/finish
    o.append(T(1200, 1150, "START ▲ Ch.1 Lighthouse", 18, "#2f6db5"))
    # compass
    o.append(C(1420, 80, 40, "#fff8e6", 3)); o.append(P("M1420,48 L1430,80 L1420,112 L1410,80 Z", "#c0262d", 2)); o.append(T(1420, 36, "N", 18))
    # title
    o.append(f'<rect x="20" y="1050" width="300" height="94" rx="12" fill="#fff8e6" stroke="{INK}" stroke-width="3"/>')
    o.append(T(170, 1088, "MADINAT AL-SALAM", 26, "#3a1f52") + T(170, 1116, "the Round City of legend", 16, INK, family="Georgia,serif", weight="600")
             + T(170, 1136, "100 landmarks · 1000 words", 14, "#7a2a1a", family="Georgia,serif", weight="600"))
    # legend
    o.append(f'<rect x="1180" y="130" width="300" height="330" rx="12" fill="#fff8e6" stroke="{INK}" stroke-width="3"/>')
    o.append(T(1330, 162, "THE ROUTE", 24, "#3a1f52"))
    for i, (nm, col) in enumerate(DISTRICTS):
        y = 192 + i * 26
        o.append(C(1200, y - 5, 9, col, 2, "#fff") + T(1216, y, f"{i*10+1}–{i*10+10}  {nm}", 13, INK, anchor="start", family="Arial,sans-serif", weight="700"))
    o.append(T(1330, 452, "Lions Eat Every Horse ↻", 15, "#7a2a1a"))
    o.append("</svg>")
    return "".join(o)

if __name__ == "__main__":
    open("../images/city_map.svg", "w").write(svg())
    json.dump([[d * 10 + k + 1, round(x), round(y)] for d, r in enumerate(routes) for k, (x, y) in enumerate(r)], open("../data/map_points.json", "w"))
    print("map ok")
