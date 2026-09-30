"""Auto-compose comic panels for chapters 2-100 from the script, using the same art kit as Chapter 1."""
import re, math, random, json, os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
from characters import SPECS, beard_white, grey_beard, moustache, turban as _t
import scenes
from scenes import bubble, caption, sfx, sparkle, spark, night_sky, stars, skyline, sea, stone_wall, panel, fig
from props import *

W, H = 400, 300
BASE = 288

# ------------------------------------------------------------ palettes
SKY = {"night": ("#0e1238", "#3b2a6b"), "dusk": ("#2b1f4f", "#e0876a"), "dawn": ("#f09a6a", "#ffe3b3"), "day": ("#6fc0ee", "#dff3ff"),
       "desert": ("#7cc4f0", "#ffe8b0"), "violet": ("#1c0b2e", "#6b2fa0"), "gold": ("#f7b267", "#fff1c9"), "storm": ("#1a1a2e", "#4a4a6a")}

def sky_grad(w, key, sid):
    t, b = SKY[key]
    out = f'<defs><linearGradient id="sk{sid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs><rect width="{w}" height="{H}" fill="url(#sk{sid})"/>'
    if key in ("night", "violet", "storm"): out += stars(int(40 * w / 400), sid, w, 170)
    return out

# ------------------------------------------------------------ chapter settings
def S(kind, sky, ground, hero, back=None, wall=("#6b5a7e", "#58486b"), tint=None):
    return dict(kind=kind, sky=sky, ground=ground, hero=hero, back=back, wall=wall, tint=tint)

sea_back = lambda w: sea(w, 200, 40)
city_back = lambda w, c="#1c1840": skyline(w, 205, c, 7)
dune_back = lambda w: dune(-40, 215, w * 0.6, 70) + dune(w * 0.35, 215, w * 0.7, 90, "#e0b865")
hill_back = lambda w: P(f"M0,215 Q{w*0.3},150 {w*0.6},200 T{w},190 V215 H0 Z", "#2b2450", 0)
garden_back = lambda w: "".join(C(x, 190, 40, "#2f5e34", 0) for x in range(0, int(w) + 40, 60))
bazaar_back = lambda w: "".join(f'<rect x="{x}" y="{130+(x*7)%40}" width="58" height="{90-(x*7)%40}" fill="#d9b88a" stroke="#b8925a" stroke-width="2"/>' for x in range(-10, int(w), 56))
river_back = lambda w: f'<rect x="0" y="200" width="{w}" height="20" fill="#4a90c0"/>' + reeds(0, w, 215, 50, 9)
wall_back = lambda w: f'<rect x="0" y="120" width="{w}" height="95" fill="#e0c9a0" stroke="#b8925a" stroke-width="3"/>' + "".join(f'<rect x="{x}" y="108" width="22" height="14" fill="#e0c9a0" stroke="#b8925a" stroke-width="2"/>' for x in range(0, int(w), 40))
palace_back = lambda w: "".join(dome_bldg(x, 215, 90, 60, "#efe6d6", "#2e8b57") for x in range(40, int(w), 150))

def hero_for(n):
    H = {
        2: lambda x, b, s: g(E(0, -20, 70, 22, "#c8a060", 3) + "".join(fish(-40 + i * 20, -30 - (i % 2) * 8, 0.8) for i in range(5)), x, b, s),
        3: lambda x, b, s: rope_coil(x, b, s * 1.1),
        4: lambda x, b, s: g(L(0, 0, 0, -150, INK, 6) + L(-80, -140, 80, -140, "#b8862b", 6) + P("M-80,-140 l-20,50 h40 Z", "#d9a441", 3) + P("M80,-140 l-20,50 h40 Z", "#d9a441", 3) + C(0, -150, 8, "#b8862b", 2), x, b, s),
        5: lambda x, b, s: ship_ribs(x, b, s),
        6: lambda x, b, s: g(boat(-110, -40, 220, "#6b4a2a") + big_egg(0, -40, 0.8), x, b, s),
        7: lambda x, b, s: g(E(0, -20, 60, 22, "#e8d9d0", 3) + P("M-60,-20 Q0,-90 60,-20", "#f3e9e0", 3) + C(0, -30, 10, "#fff", 2), x, b, s),
        8: lambda x, b, s: g(sack(-50, 0, "#c9a26a", "PEPPER") + sack(0, 0, "#e07b1f", "SAFFRON") + sack(50, 0, "#8a3a1a", "CUMIN") + L(0, -200, 0, -80, INK, 3) + P("M-8,-80 q8,20 16,0", "none", 4), x, b, s),
        9: lambda x, b, s: bell(x, b - 110 * s, s * 1.2),
        10: lambda x, b, s: tower(x - 150 * s, b, 200, 50, "#e8d6b0") + tower(x + 150 * s, b, 200, 50, "#e8d6b0") + chain_line(x - 130 * s, b - 150, x + 130 * s, b - 150, 10),
        11: lambda x, b, s: boat(x - 150, b - 30, 120, "#8a5a2b", False) + boat(x - 20, b - 30, 120, "#6b4a2a", False) + L(x - 150, b - 20, x + 100, b - 20, "#c8a060", 4),
        12: lambda x, b, s: g(C(0, -80, 70, "none", 10, "#8a5a2b") + "".join(L(0, -80, 70 * math.cos(a), -80 + 70 * math.sin(a), "#8a5a2b", 6) for a in [i * math.pi / 4 for i in range(8)]) + C(0, -80, 12, "#6b4a2a", 3), x, b, s),
        13: lambda x, b, s: dome_bldg(x, b, 160 * s, 80 * s, "#e0d8f0", "#9ad0ff") + "".join(P(f"M{x+dx},{b-150*s} q10,-20 0,-40", "none", 5, "#fff", extra='opacity="0.6"') for dx in (-30, 0, 30)),
        14: lambda x, b, s: palm(x, b, 170 * s) + "".join(g(P("M0,0 q-10,-30 0,-50 q14,-4 18,6 l12,2 l-12,4 q-2,20 -18,38", "#fff", 2), x + dx, b - 10, 0.8) for dx in (-80, 70)),
        15: lambda x, b, s: g(f'<rect x="-60" y="-150" width="120" height="90" fill="#b99a6a" stroke="{INK}" stroke-width="3"/>' + P("M-70,-150 L0,-200 L70,-150 Z", "#8a6a3a", 3) + "".join(L(xx, -60, xx, 0, "#6b4a2a", 6) for xx in (-50, 50)) + L(-60, -40, -120, 10, "#6b4a2a", 4), x, b, s),
        16: lambda x, b, s: "".join(watermelon(x - 100 + i * 34, b - 16 - (i % 3) * 20) for i in range(7)) + L(x, b, x, b - 90, "#6b4a2a", 6) + L(x - 140, b - 60, x + 140, b - 60, "#6b4a2a", 4),
        17: lambda x, b, s: ruins(x - 110, b) + dome_bldg(x + 40, b - 120, 90, 40, "#8fb8c8", "#5a8fa0"),
        18: lambda x, b, s: serpent_coil(x - 190, b - 60, 380),
        19: lambda x, b, s: reeds(x - 200, x + 200, b, 220, n),
        20: lambda x, b, s: toll_bar(x - 90, b) + f'<rect x="{x+90}" y="{b-110}" width="70" height="110" fill="#b99a6a" stroke="{INK}" stroke-width="3"/>',
        21: lambda x, b, s: g(P("M-120,0 v-150 Q0,-260 120,-150 V0 H90 V-140 Q0,-220 -90,-140 V0 Z", "#c8773a", 3) + "".join(g(camel(0, 0, 0.18), dx, -150, 1) for dx in (-70, 0, 70)), x, b, s),
        22: lambda x, b, s: spice_cones(x - 95, b, 5),
        23: lambda x, b, s: carpet_hang(x - 120, b - 200, 60, 90) + carpet_hang(x - 40, b - 210, 60, 100, "#2f6db5") + carpet_hang(x + 40, b - 200, 60, 90, "#3f7a3a"),
        24: lambda x, b, s: f'<rect x="{x-110}" y="{b-80}" width="220" height="10" fill="#8a5a2b"/>' + bottles(x - 100, b - 80, 9) + f'<rect x="{x-110}" y="{b-150}" width="220" height="10" fill="#8a5a2b"/>' + bottles(x - 90, b - 150, 8),
        25: lambda x, b, s: shelf_books(x - 90, b, 180, 4),
        26: lambda x, b, s: pot_stack(x - 50, b) + anvil(x + 90, b, 0.6),
        27: lambda x, b, s: g("".join(f'<rect x="{-40+i*6}" y="{-30-i*24}" width="{80-i*12}" height="24" fill="{["#e3a33b","#f7d08a","#e86aa0","#f3e0c0"][i%4]}" stroke="{INK}" stroke-width="2.5"/>' for i in range(5)) + sugar_rose_small(), x, b, s),
        28: lambda x, b, s: "".join(cage(x - 130 + i * 50, b - (i % 2) * 60, 40, 50, ["#f4c542", "#3f9b4a", "#e0533b", "#2f6db5", "#fff", "#b48cff"][i]) for i in range(6)),
        29: lambda x, b, s: mirror_big(x - 90, b, 0.9) + mirror_big(x + 90, b, 0.9) + mirror_big(x, b, 1.05),
        30: lambda x, b, s: f'<rect x="{x-130}" y="{b-60}" width="260" height="60" fill="#8a5a2b" stroke="{INK}" stroke-width="3"/>' + g(C(0, -40, 34, "#d9a441", 3) + L(-40, 0, -40, -80, INK, 4) + L(40, 0, 40, -80, INK, 4) + L(-44, -80, 44, -80, INK, 4), x + 90, b - 60, 1),
        31: lambda x, b, s: P(f"M{x-170},{b} Q{x},{b-150} {x+170},{b}", "#b9a88c", 4) + P(f"M{x-110},{b} Q{x},{b-80} {x+110},{b} Z", "#2a3a6a", 3),
        32: lambda x, b, s: g(C(0, -110, 100, "none", 12, "#8a5a2b") + "".join(L(0, -110, 100 * math.cos(a), -110 + 100 * math.sin(a), "#8a5a2b", 7) + f'<rect x="{100*math.cos(a)-10}" y="{-110+100*math.sin(a)-8}" width="20" height="16" fill="#6b4a2a"/>' for a in [i * math.pi / 5 for i in range(10)]), x, b, s),
        33: lambda x, b, s: roses(x - 180, x + 180, b),
        34: lambda x, b, s: giraffe(x - 90, b, 0.9) + elephant(x + 80, b, 0.7),
        35: lambda x, b, s: f'<rect x="{x-110}" y="{b-50}" width="220" height="50" fill="#a0303a" stroke="{INK}" stroke-width="3"/>' + g(P("M-20,0 q-4,-40 20,-50 q24,10 20,50 Z M20,-40 q30,-10 34,10", "#d9a441", 3), x + 150, b, 0.8),
        36: lambda x, b, s: still(x - 60, b, 1.0) + g(E(0, -10, 60, 16, "#ff9fc4", 2), x + 110, b, 1),
        37: lambda x, b, s: pomegranate_tree(x - 120, b, 1.0) + pomegranate_tree(x + 120, b, 0.9) + f'<rect x="{x-50}" y="{b-40}" width="100" height="40" fill="#b9a88c" stroke="{INK}" stroke-width="3"/>',
        38: lambda x, b, s: hedge(x - 200, x - 40, b, 170) + hedge(x + 40, x + 200, b, 170) + sundial(x, b, 0.5),
        39: lambda x, b, s: g(f'<rect x="-100" y="-30" width="200" height="30" fill="#4a90c0"/>' + P("M-80,-30 v-90 M80,-30 v-90", "none", 6, "#8a5a2b") + P("M-100,-120 Q0,-170 100,-120 Z", "#c0262d", 3), x, b, s) + lotus(x - 60, b - 10) + lotus(x + 60, b - 14),
        40: lambda x, b, s: tower(x, b, 200, 70, "#e0c9a0", "#c0262d") + lion(x + 150, b - 120, 0.35),
        41: lambda x, b, s: gate_big(x, b, 220, 200) + lion(x + 20, b - 190, 0.8),
        42: lambda x, b, s: gate_big(x, b - 60, 200, 150) + f'<rect x="{x-60}" y="{b-60}" width="120" height="60" fill="#8a5a2b" stroke="{INK}" stroke-width="3"/>',
        43: lambda x, b, s: "".join(g(P("M-16,0 q0,-26 16,-30 q16,4 16,30 Z", "#8a8a95", 2) + L(0, -30, 0, -40, "#c0262d", 3), x - 100 + i * 40, b - 110, 1) for i in range(6)) + f'<rect x="{x-130}" y="{b-110}" width="260" height="8" fill="#6b4a2a"/>',
        44: lambda x, b, s: fountain(x, b, 1.0),
        45: lambda x, b, s: g(f'<rect x="-40" y="-190" width="80" height="120" fill="#555a66" stroke="{INK}" stroke-width="3"/>' + L(0, -70, 0, -40, INK, 10) + E(0, -30, 50, 10, "#d9a441", 3) + "".join(C(-60 + i * 14, -8, 8, "#f4c542", 2) for i in range(9)), x, b, s),
        46: lambda x, b, s: dome_bldg(x, b, 180, 70, "#e8e0d8", "#c9d6e0") + "".join(C(x + dx, b - 120 - abs(dx) / 3, 30, "#fff", 0, extra='opacity="0.35"') for dx in (-80, -20, 40, 100)),
        47: lambda x, b, s: anvil(x, b, 1.0) + f'<circle cx="{x+130}" cy="{b-60}" r="40" fill="#ff7a1a" opacity="0.6"/>',
        48: lambda x, b, s: target(x, b, 1.0),
        49: lambda x, b, s: "".join(f'<rect x="{x-180+i*60}" y="{b-230}" width="22" height="230" fill="#7a7a8a" stroke="{INK}" stroke-width="2"/>' for i in range(7)),
        50: lambda x, b, s: tower(x, b, 230, 80, "#d9c7a0", "#8a5a2b") + f'<circle cx="{x}" cy="{b-275}" r="18" fill="#ff7a1a"/>',
        51: lambda x, b, s: gate_big(x, b, 220, 200) + elephant(x, b - 190, 0.55, "#d9a441"),
        52: lambda x, b, s: cloth_line(x - 190, x + 190, b - 190, ("#f7f3e8", "#efe8d8", "#fbf8f0")) + cloth_line(x - 190, x + 190, b - 120, ("#f7f3e8", "#efe8d8")),
        53: lambda x, b, s: g(P("M-70,0 v-110 Q0,-170 70,-110 V0 Z", "#8a5a3a", 3) + P("M-30,-60 Q0,-100 30,-60 Z", "#ff7a1a", 2), x, b, 1) + glass_blobs(x + 90, b),
        54: lambda x, b, s: astro(x, b - 110, 70),
        55: lambda x, b, s: clock_face(x, b - 150, 60) + gear(x - 120, b - 60, 40) + gear(x + 120, b - 80, 30),
        56: lambda x, b, s: shelf_books(x - 90, b, 180, 3, 7) + g(f'<rect x="-30" y="-40" width="60" height="40" fill="#555"/>', x + 150, b, 1),
        57: lambda x, b, s: vat(x - 90, b, 110) + vat(x + 90, b, 110),
        58: lambda x, b, s: jar(x - 100, b, 60) + jar(x - 50, b, 45, "#b8603a") + jar(x + 60, b, 70) + jar(x + 120, b, 50, "#d98a4a"),
        59: lambda x, b, s: dye_pools(x - 150, b) + cloth_line(x - 190, x + 190, b - 200),
        60: lambda x, b, s: f'<rect x="{x-150}" y="{b-50}" width="300" height="14" fill="#8a5a2b" stroke="{INK}" stroke-width="2"/>' + g(L(0, 0, 60, -160, "#c8a060", 12) + P("M60,-160 l14,-30 l6,34 Z", INK, 2), x + 60, b - 36, 1),
        61: lambda x, b, s: gate_big(x, b, 220, 200) + eagle(x, b - 150, 0.7),
        62: lambda x, b, s: "".join(arch_door(x - 150 + i * 75, b, 50, 90, "#5a4030") for i in range(5)) + camel(x + 150, b, 0.6),
        63: lambda x, b, s: camel(x - 90, b, 0.8, "#2f6db5") + camel(x + 80, b, 0.8, "#c0262d"),
        64: lambda x, b, s: tent(x - 190, b, 120) + tent(x + 70, b, 120) + tent(x - 70, b, 160, "#3a2a1a", "#d9a441"),
        65: lambda x, b, s: well(x - 110, b, 0.8) + well(x + 110, b, 0.8, glow="#9ad0ff"),
        66: lambda x, b, s: ruins(x - 140, b),
        67: lambda x, b, s: salt_mounds(x - 170, b),
        68: lambda x, b, s: windcatcher(x - 100, b) + windcatcher(x + 40, b, 170) + windcatcher(x + 150, b, 220),
        69: lambda x, b, s: dune(x - 200, b, 260, 140) + dune(x - 20, b, 260, 170, "#e0b865"),
        70: lambda x, b, s: palm(x - 140, b, 170) + palm(x + 140, b, 160) + E(x, b - 12, 110, 16, "#40c8c8", 3),
        71: lambda x, b, s: gate_big(x, b, 220, 200) + brass_horse(x, b - 190, 0.55),
        72: lambda x, b, s: horse(x, b, 0.9),
        73: lambda x, b, s: kite(x - 120, b - 200) + kite(x, b - 230, "#2f6db5") + kite(x + 120, b - 190, "#f4c542") + kite(x + 60, b - 150, "#15152a"),
        74: lambda x, b, s: tower(x, b, 220, 90, "#d9c7a0", "#6b4fa0"),
        75: lambda x, b, s: sextant(x + 120, b, 1.1),
        76: lambda x, b, s: astro(x, b - 140, 80),
        77: lambda x, b, s: pigeon_wall(x - 90, b),
        78: lambda x, b, s: sundial(x, b, 1.1),
        79: lambda x, b, s: well(x, b, 1.1, "#c9d6ff", "#e8e8ff"),
        80: lambda x, b, s: wall_back(W).replace("y=\"120\"", "y=\"150\""),
        81: lambda x, b, s: f'<rect x="{x-200}" y="{b-190}" width="400" height="190" fill="#b9a88c" stroke="{INK}" stroke-width="3"/>' + spikes(x - 200, x + 200, b - 190) + arch_door(x, b, 60, 100),
        82: lambda x, b, s: g(P("M-120,0 v-40 h240 v40 Z", "#a0303a", 3) + "".join(E(-80 + i * 40, -44, 20, 10, ["#f4c542", "#6b2fa0", "#2bb3a3"][i % 3], 2) for i in range(5)), x, b, 1),
        83: lambda x, b, s: vault_door(x, b - 110, 95),
        84: lambda x, b, s: ruins(x - 140, b).replace("#b9a88c", "#4a4040").replace("#a89878", "#3a3030"),
        85: lambda x, b, s: shelf_books(x - 200, b, 150, 5, 11) + shelf_books(x + 50, b, 150, 5, 13),
        86: lambda x, b, s: flags_row(x - 150, b - 230, 6) + f'<rect x="{x-150}" y="{b-50}" width="300" height="14" fill="#8a5a2b"/>',
        87: lambda x, b, s: well(x, b, 1.1, "#1a2a4a"),
        88: lambda x, b, s: bars(x - 190, b - 220, 380, 220),
        89: lambda x, b, s: table_map(x, b, 260),
        90: lambda x, b, s: flags_row(x - 170, b - 220, 7) + crowd(x - 200, b - 40, 14, 400, n, "#4a3a70"),
        91: lambda x, b, s: gold_gate(x, b, 0.95),
        92: lambda x, b, s: fountain(x - 110, b, 0.8, "#b48cff") + fountain(x + 110, b, 0.8, "#b48cff"),
        93: lambda x, b, s: silver_tree(x, b, 1.0),
        94: lambda x, b, s: throne2(x, b, 1.0),
        95: lambda x, b, s: flags_row(x - 170, b - 230, 7),
        96: lambda x, b, s: canopy_bed(x, b, 0.9),
        97: lambda x, b, s: scenes.spiral_stair(x, 0, b + 20, 240),
        98: lambda x, b, s: lexicon(x, b - 150, 1.0, True) + f'<rect x="{x-30}" y="{b-80}" width="60" height="80" fill="#2e8b57" stroke="{INK}" stroke-width="3"/>',
        99: lambda x, b, s: horseman(x, b, 0.9),
        100: lambda x, b, s: stars_crown(x, b - 200, 11, 150) + lexicon(x, b - 130, 1.0),
    }
    return H[n]

def sugar_rose_small():
    return C(0, -160, 12, "#ff8fb1", 2.5)

def setting(n):
    d = (n - 1) // 10
    indoor = {4, 9, 13, 25, 27, 29, 35, 36, 44, 45, 46, 47, 52, 53, 54, 55, 56, 57, 60, 72, 74, 76, 77, 82, 83, 85, 86, 88, 89, 94, 95, 96, 97, 98}
    sky = ["night", "dawn", "day", "dusk", "day", "day", "desert", "night", "night", "gold"][d]
    if n in (80,): sky = "storm"
    if n in (98, 99): sky = "violet"
    if n == 100: sky = "dawn"
    if n in (31, 38, 39, 40): sky = "night"
    if n in (65, 66): sky = "dusk"
    ground = ["#3a2f63", "#6b4a2a", "#c9a26a", "#3f6b3a", "#c9b08a", "#8a6a4a", "#e0c28a", "#2b2450", "#6b6478", "#d9c38a"][d]
    wall = [("#6b5a7e", "#58486b"), ("#8a7a64", "#6b5a44"), ("#c9a26a", "#a88450"), ("#5a6b4a", "#465a38"), ("#b8a27a", "#9a845c"),
            ("#8a6a4a", "#6b4e34"), ("#c9a26a", "#a88450"), ("#4a4070", "#3a3060"), ("#5a5068", "#4a4058"), ("#d9c38a", "#b8a060")][d]
    back = [sea_back, river_back, bazaar_back, garden_back, city_back, city_back, dune_back, hill_back, palace_back, palace_back][d]
    tint = {17: ("#3a8ab0", 0.35), 18: ("#8a2a4a", 0.35), 49: ("#0a1020", 0.35), 84: ("#2a2020", 0.25), 88: ("#101018", 0.35)}.get(n)
    return S("in" if n in indoor else "out", sky, ground, hero_for(n), back, wall, tint)

# ------------------------------------------------------------ station overlays (loci anchors)
def station_back(i, st, w):
    c1, c2 = st["wall"]
    if i == 2:   # LAMP
        return L(70, 0, 70, 50, "#555", 3) + P("M52,50 h36 l-5,34 h-26 Z", "#d9a441", 3) + '<circle cx="70" cy="68" r="28" fill="#ffd84d" opacity="0.4"/>'
    if i == 3:   # RUG
        return E(w / 2, 268, 150, 20, "#a0303a", 3) + E(w / 2, 268, 120, 14, "none", 2, "#f4c542") + E(w / 2, 268, 60, 7, "#f4c542", 0, extra='opacity="0.6"')
    if i == 5:   # PILLAR
        return f'<rect x="{w-58}" y="0" width="40" height="300" fill="#e0d4b8" stroke="{INK}" stroke-width="3"/>' + f'<rect x="{w-66}" y="0" width="56" height="16" fill="#cfc2a4" stroke="{INK}" stroke-width="3"/>' + f'<rect x="{w-66}" y="276" width="56" height="16" fill="#cfc2a4" stroke="{INK}" stroke-width="3"/>'
    if i == 6:   # WINDOW
        return P(f"M{w/2-42},120 v-50 Q{w/2},10 {w/2+42},70 v50 Z", "#9ad0ff", 5, "#6b4a2a") + L(w / 2, 30, w / 2, 120, "#6b4a2a", 3)
    if i == 7:   # STAIR
        return "".join(f'<rect x="{w-170+k*24}" y="{280-k*22}" width="{170-k*24}" height="22" fill="#c9b89a" stroke="{INK}" stroke-width="2"/>' for k in range(7))
    return ""

def station_front(i, st, w):
    if i == 0:   # ARCH framing
        return P(f"M0,0 H{w} V300 H{w-26} V96 Q{w/2},-6 26,96 V300 H0 Z", "#e8dcc0", 3) + P(f"M26,96 Q{w/2},-6 {w-26},96", "none", 5, "#b8925a")
    if i == 1:   # STEP
        return f'<rect x="0" y="278" width="{w}" height="22" fill="#b9a88c" stroke="{INK}" stroke-width="2.5"/><rect x="20" y="266" width="{w-40}" height="14" fill="#cfc0a2" stroke="{INK}" stroke-width="2"/>'
    if i == 8:   # BALCONY railing
        return (P(f"M0,262 H{w}", "none", 8, "#d8cbe0") + "".join(f'<rect x="{x}" y="264" width="10" height="36" fill="#b9a8c9" stroke="{INK}" stroke-width="2"/>' for x in range(8, int(w), 30)))
    return ""

# ------------------------------------------------------------ cast detection
ALIASES = [
    ("zayn", ["Zayn", "orange headband"]), ("layla", ["Layla", "girl scholar", "indigo headscarf"]),
    ("tariq", ["Tariq", "green cap", "little brother", "small boy", "younger brother"]),
    ("sinbad", ["Sinbad", "old sailor"]), ("marjana", ["Marjana", "crimson bandana"]),
    ("yasmin", ["Yasmin", "feathered girl", "feather cloak", "heron-feather", "sorceress-girl", "the Mirage", "girl in a feather"]),
    ("hakim", ["Hakim", "silver-bearded"]), ("shahrazad", ["Shahrazad", "elderly queen", "queen in a mirror", "hand-mirror"]),
    ("caliph", ["Caliph", "caliph"]), ("queen_hind", ["Queen Hind", "nomad queen"]), ("abu_hasan", ["Abu Hasan", "round merchant", "sweets merchant", "jolly merchant"]),
    ("zulmat", ["Zulmat", "vizier", "Vizier", "masked sorcerer", "mouthless mask"]), ("silver", ["Silver-Tongue", "auctioneer"]),
    ("idris", ["Idris"]),
]
CREATURES = [("qalam", ["Qalam", "ink djinn", "ink-djinn", "djinn"]), ("pebble", ["Pebble", "roc", "baby roc"]), ("hushling", ["Hushling", "shadow creature", "shadow-creature"]),
             ("al_hadid", ["Al-Hadid", "automaton smashing", "giant automaton", "iron automaton", "three-story", "brass giant"]),
             ("tanin", ["Tanin", "river serpent", "serpent"]), ("crow", ["crow"])]
NPCS = [("Umm Samak", "fishwoman"), ("fishmonger", "fishwoman"), ("Bakhil", "official"), ("customs chief", "official"), ("Farah", "clerk"), ("clerk", "clerk"),
        ("harbormaster", "oldman"), ("Umm Qasim", "oldwoman"), ("ferry-woman", "oldwoman"), ("farmer", "farmer"), ("Hamid", "farmer"), ("Majid", "farmer"),
        ("Ibn Warraq", "scholar"), ("bookseller", "scholar"), ("Nasr", "smith"), ("coppersmith", "smith"), ("Jabir", "poet"), ("poet", "poet"), ("Hamza", "captain"),
        ("captain", "captain"), ("Rufaida", "physician"), ("physician", "physician"), ("Mint Master", "official"), ("blacksmith", "smith"), ("Umm Nur", "oldwoman"),
        ("Banu", "inventor"), ("inventor", "inventor"), ("Zubayda", "woman"), ("bookbinder", "woman"), ("Farouk", "dyer"), ("dyer", "dyer"), ("Ibn Yunus", "scholar"),
        ("astrolabe-maker", "scholar"), ("Karim", "prince"), ("prince", "prince"), ("timekeeper", "oldman"), ("pigeon-master", "oldman"), ("potter", "smith"),
        ("papermaker", "oldwoman"), ("glassblower", "smith"), ("Khalid", "smith"), ("stable master", "farmer"), ("gardener", "oldman"), ("distiller", "oldman"),
        ("vagabond", "vagabond"), ("deserter", "vagabond"), ("soldier", "captain"), ("guard", "captain"), ("envoy", "envoy"), ("scholar", "scholar"),
        ("merchant", "official"), ("Rashid", "rashid"), ("chief astronomer", "scholar"), ("teacher", "scholar"), ("messenger", "envoy"), ("spy", "hooded"), ("agent", "hooded"), ("hooded", "hooded"), ("Queen", "envoy"), ("queen", "envoy")]

def npc_spec(kind, seed):
    r = random.Random(seed)
    c = r.choice(["#2f6db5", "#8a3a2a", "#3f7a3a", "#6b4fa0", "#b8603a", "#2bb3a3", "#a0303a"])
    if kind in ("fishwoman", "oldwoman", "woman", "clerk", "physician"):
        sp = dict(skin=r.choice(["tan", "old", "brown", "light"]), scarf=r.choice(["#6b4a2a", "#3f7a3a", "#8a3a5a", "#2f6db5"]), tunic=c, trim="#f4c542", long=True, sleeve=c, shoe="#5a3a20")
        if kind == "physician": sp.update(scarf="#f3efe1", tunic="#f3efe1", sleeve="#f3efe1", trim="#2bb3a3")
        return sp
    base = dict(skin=r.choice(["tan", "brown", "old", "dark"]), tunic=c, trim="#f4c542", pants="#6b5a44", sleeve=c, feet="shoe", shoe="#5a3a20")
    if kind == "oldman": base.update(long=True, beard=beard_white(1.0), beard_hides_mouth=True, hat=_t("#e8e0d0", "#b8a080", 0.8), skin="old")
    elif kind == "scholar": base.update(long=True, beard=grey_beard(), beard_hides_mouth=True, hat=_t("#f3efe1", "#b8a080", 1.0), tunic="#1f2f6b", sleeve="#1f2f6b")
    elif kind == "official": base.update(w=1.4, beard=moustache(), hat=_t("#c0262d", "#f4c542", 1.1), tunic="#6b2fa0", sleeve="#6b2fa0")
    elif kind == "smith": base.update(tunic="#6b4a2a", sleeve="#b97a4f", beard=moustache(), hat=headband("#8a3a2a").split("<path")[0] + P("M-45,-248 Q0,-262 45,-248 L45,-236 Q0,-250 -45,-236 Z", "#8a3a2a", 2.5))
    elif kind == "captain": base.update(tunic="#8a8a95", sleeve="#6b6b78", hat=P("M-50,-240 Q0,-300 50,-240 Z", "#8a8a95", 3) + L(0, -290, 0, -310, "#c0262d", 5), beard=moustache())
    elif kind == "prince": base.update(tunic="#e86aa0", sleeve="#e86aa0", skin="light", hat=P("M-36,-270 L-30,-296 L-15,-280 L0,-302 L15,-280 L30,-296 L36,-270 Z", "#f4c542", 2.5), hair="mop", hair_color="#15110e")
    elif kind == "farmer": base.update(tunic="#8a6a3a", sleeve="#b97a4f", hat=P("M-60,-250 Q0,-300 60,-250 Z", "#e0c28a", 3), beard=moustache())
    elif kind == "poet": base.update(tunic="#6b2fa0", sleeve="#6b2fa0", hat=_t("#f4c542", "#6b2fa0", 0.8), skin="light")
    elif kind == "inventor": base.update(long=True, tunic="#6b4a2a", sleeve="#6b4a2a", beard=beard_white(0.9), beard_hides_mouth=True, head_extras=[C(-18, -236, 10, "none", 3, "#b8862b") + C(18, -236, 10, "none", 3, "#b8862b")])
    elif kind == "dyer": base.update(tunic="#2f6db5", sleeve="#2f6db5", skin="brown", hair="curly", hair_color="#15110e")
    elif kind == "vagabond": base.update(tunic="#6b6b5a", sleeve="#8a8a70", hair="mop", hair_color="#3a2a1a", beard=moustache("#3a2a1a"))
    elif kind == "envoy": base.update(long=True, tunic=c, sleeve=c, hat=_t(r.choice(["#f3efe1", "#2f6db5", "#c0262d"]), "#f4c542", 1.0))
    elif kind == "hooded": base.update(cloak="#3a2a4a", long=True, tunic="#4a3a5a", sleeve="#4a3a5a", iris="#b48cff")
    elif kind == "rashid": base.update(tunic="#1f2a6b", sleeve="#1f2a6b", hat=_t("#1f2a6b", "#c0c0c8", 1.0), skin="tan")
    return base

EXTRA_SPECS = {
    "silver": dict(skin="light", tunic="#1a1a1a", trim="#c9ccd8", long=True, sleeve="#1a1a1a", hat=_t("#1a1a1a", "#c9ccd8", 1.1), beard=moustache("#1a1a1a"), shoe="#1a1a1a"),
    "idris": dict(skin="#b58a6a", tunic="#3a1f52", trim="#b48cff", long=True, sleeve="#3a1f52", hair="mop", hair_color="#2b1a10"),
}

EXPR_KEYS = [("shock", ["gasp", "shock", "stunned", "can't believe", "incredulous", "stares", "freezes", "horror", "disbelief", "gape"]),
             ("scared", ["fear", "terrif", "panic", "trembl", "dread", "scared", "afraid", "shiver", "nervous"]),
             ("angry", ["angry", "furious", "rage", "indignant", "glare", "growl", "snap", "livid", "irate", "roar"]),
             ("sad", ["sad", "tears", "cry", "grief", "mourn", "despondent", "lonely", "sob", "sorry", "weep", "hopeless"]),
             ("grin", ["laugh", "cheer", "grin", "joy", "jubilant", "exult", "winks", "smile", "euphoric", "dance"]),
             ("determined", ["fight", "charge", "determined", "resolute", "brave", "firm", "refuse", "won't", "stand", "grit"]),
             ("skeptic", ["doubt", "skeptic", "suspicious", "narrow", "wary", "folds her arms", "arms folded"])]
POSE_KEYS = [((("run_b", "run_f"), "run"), ["run", "race", "chase", "flee", "gallop", "sprint", "hurry", "hasten", "dash"]),
             ((("up", "reach"), "jump"), ["leap", "jump", "dive", "swing", "fly", "flies", "flip", "vault"]),
             ((("down", "point"), "stand"), ["point", "points", "aim"]),
             ((("up", "wave"), "stand"), ["shout", "cheer", "raise", "wave", "yell", "calls"]),
             ((("hold", "down"), "stand"), ["hold", "offer", "hand", "give", "read", "write", "carr", "grab", "clutch"]),
             ((("shield", "point"), "stand"), ["slash", "swing", "block", "shield", "attack", "strike"])]
DEFAULT_POSES = [(("down", "down"), "stand"), (("down", "wave"), "stand"), (("hip", "down"), "stand"), (("down", "point"), "stand"), (("chin", "down"), "stand")]
VILLAINS = {"zulmat", "silver"}

def sentences(t):
    return re.split(r"(?<=[.!?”])\s+", t)

def find_positions(text, names):
    pos = [m.start() for nm in names for m in re.finditer(r"(?<![A-Za-z])" + re.escape(nm.strip()) + r"(?:s|es)?(?![a-z])", text)]
    return min(pos) if pos else None

def detect(n, i, f):
    story, prompt = f["story"], f["prompt"]
    both = re.sub(r"“[^”]*”", " ", story) + " || " + prompt
    people, creatures = [], []
    for key, names in ALIASES:
        if key == "hakim" and not (n in (1,) or n >= 84): continue
        if key == "zulmat" and n in (99, 100) and i >= 5: continue
        if key == "idris" and n not in (57, 99, 100): continue
        p = find_positions(both, names)
        if p is not None: people.append((p, key))
    for key, names in CREATURES:
        if key == "pebble" and n < 12: continue
        if key == "tanin" and n not in (17, 18, 89, 90): continue
        p = find_positions(both, names)
        if p is not None: creatures.append((p, key))
    if n in (99, 100) and i >= 5 and ("Idris" in both or "thin man" in both or "gentle man" in both) and not any(k == "idris" for _, k in people):
        people.append((0, "idris"))
    scrub = both
    for _, names in ALIASES:
        for nm in names: scrub = scrub.replace(nm, " ")
    if len(people) < 3:
        for nm, kind in NPCS:
            if re.search(r"(?<![A-Za-z])" + re.escape(nm) + r"(?![a-z])", scrub) and not any(k == ("npc:" + kind) for _, k in people):
                people.append((scrub.index(nm), "npc:" + kind + ":" + nm))
                if len(people) >= 3: break
    people.sort(); creatures.sort()
    people = [k for _, k in people][:4]
    creatures = [k for _, k in creatures][:2]
    crowdish = any(w in both for w in ("crowd", "army", "citizens", "townspeople", "people", "orphan", "Sparrows", "nomads", "soldiers", "scholars", "whole city", "multitude"))
    return people, creatures, crowdish

def mood(text, default):
    t = text.lower()
    for e, keys in EXPR_KEYS:
        if any(k in t for k in keys): return e
    return default

def posef(text, seed):
    t = text.lower()
    for (arms, legs), keys in POSE_KEYS:
        if any(re.search(r"\b" + k, t) for k in keys): return arms, legs
    return DEFAULT_POSES[seed % len(DEFAULT_POSES)]

def ctx(story, key):
    names = dict(ALIASES).get(key.split(":")[0], [key.split(":")[-1]])
    ss = [s for s in sentences(story) if any(nm in s for nm in names)]
    return " ".join(ss) if ss else story

def draw_person(key, x, expr, pose, legs, flip, s=0.36):
    if key.startswith("npc:"):
        _, kind, nm = key.split(":", 2)
        spec = npc_spec(kind, nm)
    elif key in EXTRA_SPECS: spec = EXTRA_SPECS[key]
    else: spec = SPECS[key]
    if key == "caliph" and expr != "sleep": spec = dict(spec, head_extras=[])
    if key == "zulmat": expr = "neutral"
    if key == "shahrazad":
        return g(mirror_big(0, 0, 1.0) + g(human(spec, expr, ("down", "down")), 0, -30, 0.55), x, BASE, s * 1.15)
    if key == "caliph" and expr not in ("shock", "grin", "happy"): pass
    body = human(spec, expr, pose, legs)
    if key == "zulmat":
        body = f'<circle cx="0" cy="-160" r="140" fill="#b48cff" opacity="0.15"/>' + body
        s *= 1.12
    return g(body, x, BASE, s, flip)

def draw_creature(key, x, n, flip=False):
    if key == "qalam": return g(qalam("happy"), x, BASE - 30, 0.55, flip)
    if key == "pebble":
        sc = 0.55 if n < 47 else (0.8 if n < 90 else 0.95)
        return pebble("happy", sc).replace("translate(0.0,0.0)", f"translate({x:.1f},{BASE:.1f})")
    if key == "hushling": return hushling(0.5).replace("translate(0.0,0.0)", f"translate({x:.1f},{BASE:.1f})") + hushling(0.38, 0.8).replace("translate(0.0,0.0)", f"translate({x+40:.1f},{BASE:.1f})")
    if key == "al_hadid": return g(al_hadid(), x, BASE + 10, 0.62)
    if key == "tanin": return g(tanin(), x - 60, BASE, 0.5)
    if key == "crow": return g(P("M-30,0 Q-10,-40 20,-30 Q40,-26 44,-10 L60,-6 L44,0 Q20,12 -30,0 Z", "#15151f", 3, "#000") + P("M-10,-14 Q-40,-50 -60,-40 Q-40,-20 -10,-8 Z", "#23233a", 2.5, "#000") + C(30, -18, 4, "#b48cff", 0), x, 150, 0.7)
    return ""

def guardian_for(n, i, both):
    t = both.lower()
    if n == 41 or (40 <= n <= 42 and "lion" in t): return ("g:lion", lambda x: lion(x, BASE, 0.7))
    if n == 51: return ("g:elephant", lambda x: elephant(x, BASE, 0.7, "#d9a441"))
    if n in (61, 70) and "eagle" in t: return ("g:eagle", lambda x: eagle(x, BASE - 40, 0.8))
    if n == 71 or ("brass horse" in t): return ("g:horse", lambda x: brass_horse(x, BASE, 0.6))
    if n == 90 and "guardian" in t: return ("", lambda x: lion(x - 60, BASE, 0.45) + brass_horse(x + 60, BASE, 0.4))
    if n in (72, 73) and ("stallion" in t or "barq" in t): return ("", lambda x: horse(x, BASE, 0.7))
    if n == 63 and "camel" in t: return ("", lambda x: camel(x, BASE, 0.65, "#2f6db5"))
    return None

# ------------------------------------------------------------ text for bubbles
def short(t, n):
    t = t.strip()
    if len(t) <= n: return t
    cut = t[:n].rsplit(" ", 1)[0]
    return cut.rstrip(",;:—") + "…"

def word_regex(word):
    stem = word.lower()
    if len(stem) > 6: stem = stem[:-2]
    elif len(stem) > 4: stem = stem[:-1]
    return re.compile(r"\b(" + re.escape(stem) + r"[a-zé]*)", re.I)

def mark(text, word):
    rx = word_regex(word)
    found = []
    def up(m):
        found.append(m.group(1).lower()); return m.group(1).upper()
    t = rx.sub(up, text, count=1)
    scenes.VOCAB.update(found)
    return t, bool(found)

def esc(t): return html.escape(t, quote=False)

def dialogue(story, word):
    quotes = re.findall(r"“([^”]+)”", story)
    q = None
    for qq in quotes:
        if word_regex(word).search(qq): q = qq; break
    if not q:
        cands = [qq for qq in quotes if len(qq) < 95]
        q = cands[0] if cands else None
    cap = None
    if not q or not word_regex(word).search(q):
        for s in sentences(story):
            if word_regex(word).search(s) and "“" not in s:
                cap = s; break
        if cap is None:
            s0 = sentences(story)[0]
            cap = s0 if "“" not in s0 else None
    return q, cap

def speaker_of(story, q, people):
    if not q or not people: return 0
    qi = story.find(q)
    best, bi = None, 0
    for idx, key in enumerate(people):
        if not key: continue
        names = GNAMES.get(key) or dict(ALIASES).get(key.split(":")[0]) or dict(CREATURES).get(key) or [key.split(":")[-1]]
        for nm in names:
            for m in re.finditer(re.escape(nm), story):
                d = qi - m.start()
                d = d if d >= 0 else 400 - d   # prefer mentions before the quote
                if best is None or d < best: best, bi = d, idx
    return bi
GNAMES = {"g:lion": ["Lion"], "g:elephant": ["Elephant"], "g:eagle": ["Eagle"], "g:horse": ["Horse"]}

ALLV = {w["word"].lower() for c in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "saga.json"), encoding="utf-8")) for w in c["words"]} | {"the","and","go","no","stop","run","help","yes","now","all","she","ring","not"}
SFX_RX = re.compile(r"\b([A-Z][A-Z\-]{2,}[!.]+)")

# ------------------------------------------------------------ compose one panel
def compose(n, i, f, word, next_title=None):
    wide = i == 9
    w = 1200 if wide else 400
    st = setting(n)
    sid = n * 10 + i
    random.seed(sid)
    out = []
    # background
    if st["kind"] == "out":
        out.append(sky_grad(w, st["sky"], sid))
        if st["sky"] in ("night", "violet") and n % 3 == 0: out.append(scenes.green_moon(w - 60, 44, 18) if n < 11 else C(w - 60, 44, 20, "#fff6d0", 0) + f'<circle cx="{w-50}" cy="{38}" r="18" fill="{SKY[st["sky"]][0]}"/>')
        if st["sky"] in ("day", "desert", "gold", "dawn"): out.append(C(w - 70, 50, 26, "#fff3b0", 0) + f'<circle cx="{w-70}" cy="50" r="46" fill="#fff3b0" opacity="0.3"/>')
        out.append(st["back"](w))
        out.append(f'<rect x="0" y="215" width="{w}" height="85" fill="{st["ground"]}"/>')
    else:
        out.append(stone_wall(w, H, *st["wall"]))
        out.append(f'<rect x="0" y="222" width="{w}" height="78" fill="{st["ground"]}" opacity="0.9"/>')
    out.append(station_back(i, st, w))
    # hero landmark prop
    try:
        if wide:
            out.append(st["hero"](w * 0.5, BASE - 4, 1.0))
            out.append(g(st["hero"](200, BASE - 4, 1.0), -150, 30, 0.8) if n not in (80, 97, 88, 49, 19, 33, 52, 59, 90, 100) else "")
        elif i == 4:
            out.append(st["hero"](200, BASE - 4, 1.05))
        else:
            out.append(g(st["hero"](200, BASE - 4, 1.0), 120 if i % 2 else 40, 70, 0.55) if n not in (80, 97, 88, 49, 19) else st["hero"](200, BASE - 4, 1.0))
    except Exception as ex:
        print("hero fail", n, ex)
    if st["tint"]: out.append(f'<rect width="{w}" height="{H}" fill="{st["tint"][0]}" opacity="{st["tint"][1]}"/>')
    both = f["story"] + " || " + f["prompt"]
    people, creatures, crowdish = detect(n, i, f)
    if crowdish: out.append(crowd(0, BASE - 10, 10 if not wide else 26, w, sid, "#4a3a70"))
    # layout slots
    gd = guardian_for(n, i, both)
    items = [("p", k) for k in people] + [("c", k) for k in creatures] + ([("g", gd[0])] if gd else [])
    if not items: items = [("p", "zayn")]
    k = len(items)
    margin = 70 if not wide else 120
    xs = [margin + (w - 2 * margin) * (j + 0.5) / k for j in range(k)] if k > 1 else [w * 0.5]
    if wide:
        # keep cast in the middle 2/3 so the left carries the bubble area and right the NEXT caption
        xs = [260 + 640 * (j + 0.5) / k for j in range(k)]
    heads = []
    for j, (typ, key) in enumerate(items):
        x = xs[j]
        flip = x > w / 2
        if typ == "p":
            c = ctx(f["story"], key)
            default = "neutral" if key in VILLAINS else ["happy", "determined", "grin", "skeptic"][(sid + j) % 4]
            e = mood(c, default)
            if key == "caliph": e = "sleep" if n < 96 or (n == 96 and i < 8) else e
            arms, legs = posef(c, sid + j)
            out.append(draw_person(key, x, e, arms, legs, flip))
            heads.append((x, BASE - 110))
        elif typ == "c":
            out.append(draw_creature(key, x, n, flip))
            heads.append((x, BASE - 80))
        else:
            out.append(gd[1](x))
            heads.append((x, BASE - 130))
    out.append(station_front(i, st, w))
    # text
    q, cap = dialogue(f["story"], word)
    ph = 8
    if cap:
        t, _ = mark(short(cap, 118 if not wide else 150), word)
        out.append(caption(8, 8, 190 if not wide else 360, esc(t)))
        ph = 8
    if q:
        speaker = speaker_of(f["story"], q, [k for _, k in items]) if items else 0
        t, _ = mark(short(q, 92 if not wide else 140), word)
        bw = 200 if not wide else 330
        hx, hy = heads[min(speaker, len(heads) - 1)]
        bx = (w - bw - 10) if cap else max(8, min(w - bw - 8, hx - bw / 2))
        if wide: bx = 430 if cap else max(20, min(w - bw - 20, hx - bw / 2))
        border = {"zayn": "#f28c28", "layla": "#3d3d9e", "tariq": "#6aa42f", "sinbad": "#2f6db5", "marjana": "#c0262d", "yasmin": "#8a8fb8",
                  "hakim": "#1f2f6b", "qalam": "#15152a", "zulmat": "#3a1f52"}.get(items[min(speaker, len(items) - 1)][1], INK)
        is_scroll = items[min(speaker, len(items) - 1)][1] == "zulmat"
        shout = q.endswith("!") and len(q) < 30
        out.append(bubble(bx, 8 if not cap or wide else 78, bw, esc(t), tail=(hx, hy), border=border, shout=shout, scroll=is_scroll))
    m = SFX_RX.search(f["story"])
    if m and (m.group(1).rstrip("!.").lower() in ALLV or m.group(1).rstrip("!.").lower().replace("-", "") in ALLV or len(m.group(1)) > 14): m = None
    if m and not wide:
        out.append(sfx(300 if i % 2 else 110, 205, esc(m.group(1).rstrip(".")), 28, "#ffd23f", -8))
    if wide:
        nt = f"NEXT ▶ Chapter {n+1}: {next_title}" if n < 100 else "THE END… your word goes here ▶ “          ”"
        out.append(caption(w - 330, 262, 320, esc(nt), 12.5, "#ffd23f"))
    return panel("".join(out), w, H)

if __name__ == "__main__":
    import glob, content
    CH = content.parse(glob.glob(os.path.join(os.path.dirname(__file__), "..", "content", "b*.txt")))
    D = content.D
    n = int(sys.argv[1])
    scenes.VOCAB.clear()
    html_out = "".join(f'<div style="display:inline-block;width:{"1200" if i==9 else "400"}px;margin:4px;vertical-align:top">{compose(n, i, CH[n]["frames"][i], D[n-1]["words"][i]["word"], D[n]["title"] if n < 100 else None)}</div>' for i in range(10))
    open("/tmp/prev.html", "w", encoding="utf-8").write(f"<html><body style='background:#333;width:1260px'>{html_out}</body></html>")
    print("ok")
