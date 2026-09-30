"""Reusable SVG art kit for THE THOUSAND AND ONE WORDS.
Figures are drawn in a local frame: feet at (0,0), head top near y=-280.
"""
import math

INK = "#1b1b2f"
SKIN = {"brown": "#b97a4f", "tan": "#d19a6a", "light": "#e8b98d", "dark": "#8a5634", "old": "#c89572"}

def g(content, x=0, y=0, s=1.0, flip=False, extra="", rot=0):
    sx = -s if flip else s
    r = f" rotate({rot})" if rot else ""
    return f'<g transform="translate({x:.1f},{y:.1f}){r} scale({sx:.3f},{s:.3f})" {extra}>{content}</g>'

def P(d, fill, sw=3, stroke=INK, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'

def C(cx, cy, r, fill, sw=3, stroke=INK, extra=""):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def E(cx, cy, rx, ry, fill, sw=3, stroke=INK, extra=""):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def L(x1, y1, x2, y2, color=INK, sw=3, extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" {extra}/>'

def T(x, y, txt, size=16, fill=INK, anchor="middle", weight="700", family="'Bangers',Impact,'Arial Black',sans-serif", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" font-family="{family}" {extra}>{txt}</text>'

# ---------------------------------------------------------------- faces
def eyes(expr, dx=17, y=-222, iris="#3a2414", r=9):
    out = []
    for sx in (-1, 1):
        x = sx * dx
        if expr == "sleep":
            out.append(P(f"M{x-9},{y} Q{x},{y+7} {x+9},{y}", "none", 3))
            continue
        ry = r + 3 if expr in ("shock", "scared", "amazed") else r + 1
        out.append(E(x, y, r, ry, "#fff", 2.5))
        py = y + (1 if expr != "look_up" else -4)
        px = x + (3 if expr == "side" else 0)
        pr = r * (0.45 if expr in ("shock", "scared") else 0.62)
        out.append(C(px, py, pr, iris, 0))
        out.append(C(px + pr * 0.3, py - pr * 0.4, pr * 0.35, "#fff", 0))
    # brows
    by = y - r - 8
    for sx in (-1, 1):
        x = sx * dx
        if expr in ("angry", "determined", "smug_angry"):
            out.append(L(x - 10 * sx, by - 2, x + 9 * sx, by + 5, INK, 4) if sx == -1 else L(x - 9, by + 5, x + 10, by - 2, INK, 4))
        elif expr in ("shock", "scared", "amazed"):
            out.append(P(f"M{x-10},{by-2} Q{x},{by-10} {x+10},{by-2}", "none", 3.5))
        elif expr == "skeptic":
            if sx == -1:
                out.append(L(x - 10, by + 2, x + 9, by + 3, INK, 4))
            else:
                out.append(P(f"M{x-10},{by-1} Q{x},{by-11} {x+10},{by-4}", "none", 4))
        elif expr == "sad":
            out.append(L(x - 10 * sx, by + 5, x + 9 * sx, by - 1, INK, 3.5) if sx == -1 else L(x - 9, by - 1, x + 10, by + 5, INK, 3.5))
        else:
            out.append(P(f"M{x-10},{by+1} Q{x},{by-5} {x+10},{by+1}", "none", 3.5))
    return "".join(out)

def mouth(expr, y=-195):
    m = {
        "happy": P(f"M-12,{y-3} Q0,{y+12} 12,{y-3} Z", "#7a1f2b", 2.5),
        "grin": P(f"M-15,{y-5} Q0,{y+14} 15,{y-5} Z", "#fff", 2.5) + L(-12, y - 1, 12, y - 1, INK, 1.5),
        "shock": E(0, y + 2, 7, 10, "#5a1420", 2.5),
        "scared": P(f"M-10,{y+4} Q-5,{y-3} 0,{y+3} Q5,{y-3} 10,{y+4}", "none", 3),
        "amazed": E(0, y + 1, 8, 8, "#5a1420", 2.5),
        "angry": P(f"M-11,{y+4} Q0,{y-4} 11,{y+4}", "none", 3.5),
        "determined": L(-9, y + 1, 9, y - 1, INK, 3.5),
        "skeptic": P(f"M-9,{y+2} Q2,{y} 10,{y-4}", "none", 3.5),
        "smug": P(f"M-10,{y} Q2,{y+7} 12,{y-4}", "none", 3.5),
        "sad": P(f"M-9,{y+4} Q0,{y-3} 9,{y+4}", "none", 3.5),
        "sleep": E(0, y + 2, 4, 3, "#5a1420", 2),
        "neutral": L(-7, y + 1, 7, y + 1, INK, 3),
        "side": P(f"M-6,{y+1} Q4,{y+4} 11,{y-1}", "none", 3.5),
        "look_up": E(0, y + 2, 5, 6, "#5a1420", 2.5),
    }
    return m.get(expr, m["happy"])

# ---------------------------------------------------------------- body parts
def arm(side, pose, sleeve, skin, shoulder=(38, -172), length=1.0):
    sx, sy = shoulder
    sx *= side
    L1 = 50 * length
    poses = {
        "down": (0.15, 0.1), "wave": (-2.4, -0.6), "point": (-1.45, 0), "up": (-2.6, -0.2),
        "hold": (-0.9, 0.9), "run_f": (-1.1, 1.2), "run_b": (0.7, -1.0), "hip": (0.7, 1.9),
        "reach": (-1.9, 0.2), "chin": (-0.4, 2.6), "shield": (-1.3, 1.9),
    }
    a1, a2 = poses.get(pose, poses["down"])
    # angle measured from straight down; positive side-> outward
    ang1 = a1
    ex = sx + side * L1 * math.sin(-ang1) * -1
    ey = sy + L1 * math.cos(ang1)
    ang2 = ang1 + (a2 * 0.5)
    hx = ex + side * L1 * 0.95 * math.sin(ang2) * (1 if a1 >= 0 else -1) * (-1 if a1 < 0 else 1)
    hy = ey + L1 * 0.95 * math.cos(ang2)
    # simpler, explicit endpoints per pose for reliability
    table = {
        "down": ((sx + side * 10, sy + 48), (sx + side * 12, sy + 92)),
        "wave": ((sx + side * 40, sy - 20), (sx + side * 48, sy - 70)),
        "up": ((sx + side * 22, sy - 45), (sx + side * 28, sy - 95)),
        "point": ((sx + side * 48, sy + 4), (sx + side * 96, sy - 2)),
        "reach": ((sx + side * 44, sy - 24), (sx + side * 86, sy - 44)),
        "hold": ((sx + side * 22, sy + 42), (sx - side * 6, sy + 62)),
        "run_f": ((sx + side * 34, sy + 30), (sx + side * 62, sy + 4)),
        "run_b": ((sx - side * 26, sy + 38), (sx - side * 52, sy + 60)),
        "hip": ((sx + side * 32, sy + 38), (sx + side * 12, sy + 70)),
        "chin": ((sx + side * 20, sy + 40), (sx - side * 22, sy - 8)),
        "shield": ((sx + side * 40, sy + 10), (sx + side * 30, sy - 40)),
    }
    (ex, ey), (hx, hy) = table.get(pose, table["down"])
    d = f"M{sx},{sy} Q{ex},{ey} {hx},{hy}"
    return (P(d, "none", 23, INK) + P(d, "none", 17, sleeve) + C(hx, hy, 10, skin, 2.5)), (hx, hy)

def legs(pose, pants, skin, feet="bare", shoe="#6b3e1f"):
    if pose == "run":
        l = "M-14,-96 Q-40,-50 -60,-20"; r = "M14,-96 Q34,-55 30,-5"
        fl, fr = (-64, -16), (36, -2)
    elif pose == "jump":
        l = "M-14,-96 Q-44,-70 -48,-40"; r = "M14,-96 Q50,-80 62,-58"
        fl, fr = (-50, -34), (68, -56)
    elif pose == "sit":
        l = "M-14,-96 Q-30,-96 -40,-60"; r = "M14,-96 Q40,-96 42,-60"
        fl, fr = (-42, -54), (44, -54)
    else:
        l = "M-15,-96 L-17,-10"; r = "M15,-96 L17,-10"
        fl, fr = (-20, -5), (20, -5)
    out = ""
    for d in (l, r):
        out += P(d, "none", 30, INK) + f'<path d="{d}" fill="none" stroke="{pants}" stroke-width="24" stroke-linecap="round"/>'
    for (fx, fy) in (fl, fr):
        out += E(fx, fy, 15, 8, skin if feet == "bare" else shoe, 2.5)
    return out

def tunic(color, trim="#f4c542", long=False, w=1.0, belt=None):
    bw = 44 * w
    bottom = -8 if long else -88
    flare = (bw + (22 if long else 10))
    d = f"M{-36*w},-180 Q0,-192 {36*w},-180 L{bw},-120 L{flare},{bottom} Q0,{bottom+10} {-flare},{bottom} L{-bw},-120 Z"
    out = P(d, color, 3)
    out += P(f"M{-flare+4},{bottom-2} Q0,{bottom+8} {flare-4},{bottom-2}", "none", 4, trim)
    out += P(f"M-12,-183 L0,-162 L12,-183", "none", 3, trim)
    if belt:
        out += P(f"M{-bw+2},-118 Q0,-110 {bw-2},-118 L{bw},-106 Q0,-98 {-bw},-106 Z", belt, 2.5)
    return out

def head(skin, ear=True):
    out = ""
    if ear:
        out += E(-44, -218, 8, 11, skin, 2.5) + E(44, -218, 8, 11, skin, 2.5)
    out += P("M-44,-235 Q-46,-280 0,-282 Q46,-280 44,-235 Q44,-196 24,-180 Q0,-168 -24,-180 Q-44,-196 -44,-235 Z", skin, 3)
    return out

def neck(skin):
    return P("M-10,-186 L-10,-172 L10,-172 L10,-186", skin, 2.5)

# ---------------------------------------------------------------- hair & hats
def hair_back(style, color):
    if style == "curly":
        return "".join(C(x, y, 17, color, 2.5) for x, y in [(-40, -250), (-30, -275), (0, -288), (30, -275), (42, -250), (-46, -225), (46, -225)])
    if style == "long":
        return P("M-48,-240 Q-56,-160 -40,-120 L40,-120 Q56,-160 48,-240 Z", color, 3)
    if style == "braid":
        segs = "".join(E(-40 + i * 2, -170 + i * 22, 9, 12, color, 2.5) for i in range(4))
        return segs
    return ""

def hair_front(style, color):
    if style == "curly":
        return "".join(C(x, y, 13, color, 2.5) for x, y in [(-30, -262), (-12, -270), (8, -270), (26, -262), (38, -248)])
    if style == "mop":
        return "".join(C(x, y, 12, color, 2.5) for x, y in [(-34, -256), (-18, -266), (0, -270), (18, -266), (34, -256)])
    if style == "long":
        return P("M-45,-238 Q-40,-285 0,-284 Q40,-285 45,-238 Q20,-262 0,-258 Q-20,-262 -45,-238 Z", color, 3)
    if style == "streak":
        return P("M-45,-238 Q-40,-285 0,-284 Q40,-285 45,-238 Q20,-262 0,-258 Q-20,-262 -45,-238 Z", color, 3) + P("M10,-280 Q18,-262 16,-248", "none", 5, "#c9c9d6")
    return ""

def headband(color):
    return (P("M-45,-248 Q0,-262 45,-248 L45,-236 Q0,-250 -45,-236 Z", color, 2.5)
            + P("M44,-244 Q80,-250 100,-232 Q84,-238 76,-230 Q88,-222 96,-206 Q70,-226 44,-238 Z", color, 2.5))

def turban(color, stripe=None, tall=1.0, jewel=None):
    h = 60 * tall
    d = f"M-52,-236 Q-60,-{282+h*0.4} 0,-{284+h*0.5} Q60,-{282+h*0.4} 52,-236 Q0,-250 -52,-236 Z"
    out = P(d, color, 3)
    for i in range(3):
        yy = -250 - i * 16 * tall
        out += P(f"M-48,{yy} Q0,{yy-18} 48,{yy}", "none", 2.5, stripe or INK, extra='opacity="0.7"')
    if jewel:
        out += P("M0,-262 L-8,-250 L0,-238 L8,-250 Z", jewel, 2) + P("M0,-262 Q6,-300 -4,-318", "none", 3, "#fff")
    return out

def headscarf(color, inner="#2a2a4a"):
    back = P("M-56,-230 Q-62,-300 0,-302 Q62,-300 56,-230 L64,-150 Q0,-130 -64,-150 Z", color, 3)
    front = P("M-50,-236 Q-48,-290 0,-292 Q48,-290 50,-236 Q30,-270 0,-268 Q-30,-270 -50,-236 Z", color, 3)
    return back, front

def veil_crown(color):
    back = P("M-58,-230 Q-66,-300 0,-306 Q66,-300 58,-230 L70,-120 Q0,-100 -70,-120 Z", color, 3)
    crown = P("M-36,-282 L-30,-306 L-15,-290 L0,-312 L15,-290 L30,-306 L36,-282 Z", "#f4c542", 2.5)
    return back, crown

# ---------------------------------------------------------------- full human figure
def human(spec, expr="happy", pose=("down", "down"), legpose="stand"):
    skin = SKIN.get(spec.get("skin", "tan"), spec.get("skin"))
    out = []
    back_layer, front_layer = "", ""
    if spec.get("scarf"):
        b, f = headscarf(spec["scarf"])
        back_layer += b; front_layer += f
    if spec.get("veil"):
        b, f = veil_crown(spec["veil"])
        back_layer += b; front_layer += f
    if spec.get("cloak"):
        back_layer += P("M-60,-250 Q-70,-300 0,-306 Q70,-300 60,-250 L86,-6 Q0,6 -86,-6 Z", spec["cloak"], 3)
    out.append(back_layer)
    out.append(hair_back(spec.get("hair", ""), spec.get("hair_color", INK)))
    if spec.get("cape"):
        out.append(P("M-40,-182 L-78,-10 Q0,4 78,-10 L40,-182 Z", spec["cape"], 3))
    if not spec.get("long"):
        out.append(legs(legpose, spec.get("pants", "#2e8b8b"), skin, spec.get("feet", "bare"), spec.get("shoe", "#6b3e1f")))
    else:
        out.append(E(-18, -6, 15, 8, spec.get("shoe", "#6b3e1f"), 2.5) + E(18, -6, 15, 8, spec.get("shoe", "#6b3e1f"), 2.5))
    la, lh = arm(-1, pose[0], spec.get("sleeve", skin), skin)
    ra, rh = arm(1, pose[1], spec.get("sleeve", skin), skin)
    out.append(la if pose[0] not in ("hold", "chin") else "")
    out.append(neck(skin))
    out.append(tunic(spec.get("tunic", "#f28c28"), spec.get("trim", "#f4c542"), spec.get("long", False), spec.get("w", 1.0), spec.get("belt")))
    for extra in spec.get("body_extras", []):
        out.append(extra)
    out.append(head(skin, ear=not (spec.get("scarf") or spec.get("veil") or spec.get("cloak"))))
    if spec.get("beard"):
        out.append(spec["beard"])
    if spec.get("mask"):
        out.append(spec["mask"])
    else:
        out.append(eyes(expr, iris=spec.get("iris", "#3a2414")))
        if not spec.get("beard_hides_mouth"):
            out.append(mouth(expr))
        if spec.get("blush"):
            out.append(E(-28, -200, 7, 4, "#e76f6f", 0, extra='opacity="0.5"') + E(28, -200, 7, 4, "#e76f6f", 0, extra='opacity="0.5"'))
        if spec.get("scar"):
            out.append(L(-24, -246, -14, -232, "#7a3a24", 2.5))
    out.append(hair_front(spec.get("hair", ""), spec.get("hair_color", INK)))
    out.append(front_layer)
    if spec.get("hat"):
        out.append(spec["hat"])
    for extra in spec.get("head_extras", []):
        out.append(extra)
    if pose[0] in ("hold", "chin"):
        out.append(la)
    out.append(ra)
    for extra in spec.get("front_extras", []):
        out.append(extra)
    return "".join(out)

# ---------------------------------------------------------------- props
def satchel(color="#7a4a24"):
    return P("M-36,-180 L40,-100", "none", 6, "#5a3418") + P("M24,-118 h38 v34 h-38 Z", color, 2.5) + P("M24,-118 h38 l-4,14 h-30 Z", "#9a6334", 2.5)

def glowbook():
    return (P("M-58,-128 h44 v40 h-44 Z", "#6b3a1e", 2.5) + P("M-54,-124 h36 v32 h-36 Z", "#fff6c9", 1.5)
            + f'<circle cx="-36" cy="-108" r="26" fill="#ffd84d" opacity="0.35"/>' + P("M-40,-180 L-40,-128", "none", 4, "#5a3418"))

def reed_pen():
    return P("M36,-262 L70,-296", "none", 5, "#c8a060") + P("M70,-296 L76,-302", "none", 3, INK)

def spectacles():
    return C(-18, -272, 9, "none", 2.5, "#b8862b") + C(18, -272, 9, "none", 2.5, "#b8862b") + L(-9, -272, 9, -272, "#b8862b", 2.5)

def astrolabe():
    return (L(0, -176, 0, -150, "#b8862b", 2) + C(0, -134, 16, "#d9a441", 2.5) + C(0, -134, 9, "none", 1.5)
            + L(-14, -134, 14, -134, INK, 1.5) + L(0, -148, 0, -120, INK, 1.5))

def sparkle(x, y, r=10, color="#ffe066"):
    d = f"M{x},{y-r} Q{x+r*0.2},{y-r*0.2} {x+r},{y} Q{x+r*0.2},{y+r*0.2} {x},{y+r} Q{x-r*0.2},{y+r*0.2} {x-r},{y} Q{x-r*0.2},{y-r*0.2} {x},{y-r} Z"
    return P(d, color, 1.5, "#b8860b")

def spark(x, y, word=None, r=16, size=13):
    s = f'<circle cx="{x}" cy="{y}" r="{r*2.2}" fill="#ffe066" opacity="0.25"/>' + sparkle(x, y, r)
    if word:
        s += T(x, y + r + size + 2, word.upper(), size, "#fff6c9", extra=f'stroke="{INK}" stroke-width="3" paint-order="stroke"')
    return s

# ---------------------------------------------------------------- creatures
def qalam(expr="happy", s=1.0):
    body = P("M-10,0 Q-60,-30 -40,-90 Q-24,-140 10,-150 Q60,-150 56,-100 Q52,-60 20,-50 Q-10,-40 0,-20 Q10,0 -10,0 Z", "#15152a", 3, "#000")
    swirl = P("M-30,-80 Q-10,-120 26,-110", "none", 3, "#3b3b6e") + P("M0,-40 Q-30,-40 -40,-10 Q-44,10 -70,14", "none", 7, "#15152a") + P("M-70,14 q-12,4 -18,-6 m6,14 q-6,8 -16,4", "none", 3, "#15152a")
    crest = P("M10,-150 L0,-182 L20,-160 L30,-186 L30,-150 Z", "#f4c542", 2.5)
    ey = -112
    if expr == "shock":
        e = E(-2, ey, 11, 14, "#ffe066", 2, "#b8860b") + E(30, ey, 11, 14, "#ffe066", 2, "#b8860b") + E(14, -80, 7, 9, "#000", 2, "#f4c542")
    elif expr == "angry":
        e = P(f"M-12,{ey-6} L10,{ey+2} L8,{ey+10} L-12,{ey+8} Z", "#ffe066", 2, "#b8860b") + P(f"M40,{ey-6} L18,{ey+2} L20,{ey+10} L40,{ey+8} Z", "#ffe066", 2, "#b8860b")
    else:
        e = E(-2, ey, 11, 13, "#ffe066", 2, "#b8860b") + E(30, ey, 11, 13, "#ffe066", 2, "#b8860b") + C(0, ey + 2, 4, "#15152a", 0) + C(32, ey + 2, 4, "#15152a", 0) + P("M2,-86 Q14,-74 28,-86", "none", 3, "#f4c542")
    return g(body + swirl + crest + e, s=s)

def inkwell(cracked=True):
    out = P("M-30,0 L-26,-40 Q0,-50 26,-40 L30,0 Z", "#c8962e", 3) + E(0, -42, 20, 6, "#8a6418", 2.5)
    if cracked:
        out += P("M-8,-40 L-2,-26 L-10,-16 L-4,-4", "none", 2.5)
    return out

def pebble(expr="happy", s=1.0):
    body = E(0, -60, 56, 58, "#e0533b", 3) + P("M-50,-80 Q-80,-60 -60,-30 Q-40,-50 -44,-70 Z", "#f39c3d", 3) + P("M50,-80 Q80,-60 60,-30 Q40,-50 44,-70 Z", "#f39c3d", 3)
    belly = E(0, -40, 32, 30, "#f7c873", 0)
    fluff = "".join(C(x, y, 9, "#e0533b", 0) for x, y in [(-30, -112), (-10, -120), (12, -118), (32, -108)])
    shell = P("M-38,-104 L-30,-122 L-18,-110 L-6,-128 L6,-112 L18,-128 L28,-110 L38,-104 Q0,-86 -38,-104 Z", "#fdf6e3", 2.5)
    beak = P("M-18,-66 Q0,-40 18,-66 Q0,-76 -18,-66 Z", "#f4c542", 3) + L(-16, -64, 16, -64, INK, 2)
    ey = "".join(E(sx * 22, -84, 9, 11, "#fff", 2.5) + C(sx * 22, -82, 5, INK, 0) + C(sx * 22 + 2, -85, 2, "#fff", 0) for sx in (-1, 1))
    feet = P("M-24,0 l-10,6 m10,-6 l0,8 m0,-8 l10,6", "none", 4, "#f4c542") + P("M24,0 l-10,6 m10,-6 l0,8 m0,-8 l10,6", "none", 4, "#f4c542")
    return g(feet + L(-22, -8, -24, 0, "#f4c542", 5) + L(22, -8, 24, 0, "#f4c542", 5) + body + belly + fluff + ey + beak + shell, s=s)

def hushling(s=1.0, alpha=1.0):
    body = P("M-40,0 Q-50,-40 -36,-90 Q-20,-130 0,-130 Q20,-130 36,-90 Q50,-40 40,0 Q30,-10 20,4 Q10,-8 0,6 Q-10,-8 -20,4 Q-30,-10 -40,0 Z", "#0d0d1a", 3, "#000")
    armsd = P("M-34,-70 Q-70,-60 -84,-30 m0,0 l-6,12 m6,-12 l2,14 m-2,-14 l10,8", "none", 7, "#0d0d1a") + P("M34,-70 Q70,-60 84,-30 m0,0 l6,12 m-6,-12 l-2,14 m2,-14 l-10,8", "none", 7, "#0d0d1a")
    drips = "".join(E(x, y, 3, 6, "#0d0d1a", 0) for x, y in [(-30, 14), (6, 18), (28, 12)])
    ey = E(-14, -92, 9, 12, "#d8e6ff", 0, extra='opacity="0.9"') + E(14, -92, 9, 12, "#d8e6ff", 0, extra='opacity="0.9"') + C(-14, -90, 3, "#0d0d1a", 0) + C(14, -90, 3, "#0d0d1a", 0)
    return g(armsd + body + drips + ey, s=s, extra=f'opacity="{alpha}"')

def zulmat_mask():
    return (P("M-40,-250 Q-42,-282 0,-284 Q42,-282 40,-250 Q42,-200 0,-172 Q-42,-200 -40,-250 Z", "#c9ccd8", 3)
            + P("M-28,-230 Q-16,-240 -6,-230 Q-16,-224 -28,-230 Z", INK, 2) + P("M28,-230 Q16,-240 6,-230 Q16,-224 28,-230 Z", INK, 2)
            + C(-16, -231, 3, "#b48cff", 0) + C(16, -231, 3, "#b48cff", 0)
            + P("M-10,-200 Q0,-196 10,-200", "none", 1.5, "#8a8da0") + P("M0,-266 L0,-248", "none", 1.5, "#8a8da0"))

def hush_staff(x=70):
    return (L(x, -300, x, 0, "#3b2a4d", 7) + f'<circle cx="{x}" cy="-318" r="34" fill="#b48cff" opacity="0.25"/>'
            + P(f"M{x-20},-316 Q{x-22},-340 {x},-342 Q{x+24},-338 {x+20},-312 Q{x+10},-294 {x-8},-298 Q{x-22},-300 {x-20},-316 Z", "#0b0b12", 3, "#000")
            + C(x, -318, 26, "none", 2, "#d8c8ff", extra='stroke-dasharray="4 5"'))

def brass_lion(s=1.0):
    mane = "".join(C(40 + 34 * math.cos(a), -150 + 34 * math.sin(a), 16, "#b8862b", 2.5) for a in [i * math.pi / 6 for i in range(12)])
    body = P("M-80,-40 Q-90,-110 -30,-120 L40,-120 Q60,-100 60,-60 L60,0 L40,0 L36,-40 L-40,-40 L-44,0 L-64,0 Z", "#d9a441", 3)
    face = C(40, -150, 30, "#e8b84f", 3) + C(30, -156, 5, "#35e0d0", 1.5) + C(52, -156, 5, "#35e0d0", 1.5) + P("M34,-136 Q41,-130 48,-136", "none", 3)
    tail = P("M-80,-60 Q-110,-90 -100,-120", "none", 5) + C(-100, -124, 8, "#b8862b", 2)
    rivets = "".join(C(x, -80, 2.5, "#8a6418", 0) for x in range(-60, 40, 16))
    return g(tail + body + rivets + mane + face, s=s)

def al_hadid(s=1.0):
    body = P("M-70,-300 L70,-300 L90,-150 L60,-120 L-60,-120 L-90,-150 Z", "#7b3a2a", 4)
    furnace = C(0, -220, 30, "#ff7a1a", 3) + C(0, -220, 16, "#ffe066", 0)
    headd = P("M-34,-370 L34,-370 L40,-300 L-40,-300 Z", "#8c4a36", 4) + P("M-24,-340 L24,-340 L24,-330 L-24,-330 Z", "#ff2a2a", 2)
    legsd = P("M-56,-120 L-60,0 L-20,0 L-16,-120 Z", "#6a3022", 4) + P("M16,-120 L20,0 L60,0 L56,-120 Z", "#6a3022", 4)
    armsd = P("M-70,-290 L-120,-160 L-96,-150 L-60,-250 Z", "#8c4a36", 4) + P("M70,-290 L120,-160 L96,-150 L60,-250 Z", "#8c4a36", 4)
    fists = C(-110, -146, 22, "#5a2a1e", 4) + C(110, -146, 22, "#5a2a1e", 4) + P("M-132,-150 Q-110,-120 -88,-150", "none", 4, "#9a9aa8") + P("M132,-150 Q110,-120 88,-150", "none", 4, "#9a9aa8")
    return g(legsd + armsd + body + furnace + headd + fists, s=s)

def tanin(s=1.0):
    coil = P("M-260,0 Q-220,-120 -120,-60 Q-40,-10 20,-90 Q70,-170 140,-150", "none", 70, INK) + P("M-260,0 Q-220,-120 -120,-60 Q-40,-10 20,-90 Q70,-170 140,-150", "none", 62, "#1f8a8a")
    scales = "".join(C(x, y, 6, "#9fd8cf", 2) for x, y in [(-200, -60), (-120, -60), (-40, -30), (20, -90), (80, -150)])
    headd = P("M110,-190 Q180,-230 250,-190 Q280,-150 240,-120 Q180,-100 120,-120 Q90,-150 110,-190 Z", "#1f8a8a", 4)
    ey = E(200, -180, 16, 10, "#f4d03f", 3) + P("M186,-180 L214,-180", "none", 4)
    whisk = P("M250,-140 Q300,-120 320,-80", "none", 3) + P("M240,-126 Q280,-90 280,-50", "none", 3)
    return g(coil + scales + headd + ey + whisk, s=s)
