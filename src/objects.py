"""Object library for the Memory Cards: small drawings keyed by noun.

Every drawing lives in a local frame with its bottom-centre at (0, 0) and is about 80 units
tall (y from -80 to 0) and at most ~90 wide.  draw(noun, x, y, scale, mods) places it.

Built from the existing art kit (art.py, props.py, characters.SPECS, ch001.crow, autoart.npc_spec)
plus a few factories (quad / bird / bug / person) so one shape family covers many nouns.
Unknown nouns fall back to a labelled thought bubble, so nothing ever crashes.
"""
import math, re, sys, os, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import INK, g, P, C, E, L, T, sparkle, human, qalam, hushling, pebble, brass_lion, headband
import props
from characters import SPECS

esc = lambda s: html.escape(s, quote=False)

COLORS = {"red": "#e0533b", "green": "#3f9b4a", "blue": "#2f6db5", "gold": "#f4c542", "golden": "#f4c542", "silver": "#c9ccd8",
          "black": "#23233a", "white": "#f7f3e8", "pink": "#ff8fc0", "purple": "#8a4fc8", "orange": "#f39c3d", "yellow": "#ffd23f",
          "brown": "#8a5a2b", "grey": "#9a9aa8", "gray": "#9a9aa8", "teal": "#1f8a8a", "violet": "#8a4fc8", "rainbow": "url(#none)",
          "stone": "#a8a29a", "iron": "#6b6b78", "brass": "#d9a441", "wooden": "#a0703a", "crystal": "#bfefff", "rusty": "#b8603a"}

# ------------------------------------------------------------------ small helpers
def face(x, y, s=1.0, expr="happy", eye="#fff"):
    """Cartoon face: two eyes (+ brows for moods) and a mouth, centred at (x, y)."""
    r = 4.2 * s
    o = ""
    for sx in (-1, 1):
        ex = x + sx * 6 * s
        if expr == "sleepy":
            o += P(f"M{ex-r},{y} Q{ex},{y+r*0.8} {ex+r},{y}", "none", 1.6 * s)
            continue
        o += E(ex, y, r, r * 1.15, eye, 1.4 * s) + C(ex + 0.8 * s, y + 0.6 * s, r * 0.5, INK, 0)
        if expr in ("angry", "mean"):
            o += L(ex - sx * r * 1.1, y - r * 1.9, ex + sx * r * 0.9, y - r * 1.2, INK, 1.8 * s)
        elif expr in ("sad", "crying"):
            o += L(ex - sx * r, y - r * 1.2, ex + sx * r, y - r * 1.9, INK, 1.6 * s)
        elif expr in ("shock", "scared"):
            o += P(f"M{ex-r},{y-r*1.7} Q{ex},{y-r*2.5} {ex+r},{y-r*1.7}", "none", 1.5 * s)
    my = y + 8 * s
    if expr in ("angry", "mean"):
        o += P(f"M{x-5*s},{my+2*s} Q{x},{my-2*s} {x+5*s},{my+2*s}", "none", 1.8 * s)
    elif expr in ("sad", "crying"):
        o += P(f"M{x-4*s},{my+2*s} Q{x},{my-2*s} {x+4*s},{my+2*s}", "none", 1.6 * s)
        if expr == "crying": o += E(x - 7 * s, y + 6 * s, 1.6 * s, 2.6 * s, "#63aee0", 0) + E(x + 7 * s, y + 7 * s, 1.6 * s, 2.6 * s, "#63aee0", 0)
    elif expr in ("shock", "scared", "gasp"):
        o += E(x, my + 1 * s, 2.8 * s, 3.8 * s, "#5a1420", 1.2 * s)
    elif expr == "sleepy":
        o += E(x, my, 2 * s, 1.5 * s, "#5a1420", 0)
    else:
        o += P(f"M{x-5*s},{my-1*s} Q{x},{my+5*s} {x+5*s},{my-1*s} Z", "#7a1f2b", 1.3 * s)
    return o

def gs(content, x=0, y=0, s=1.0, rot=0, flip=False):
    return g(content, x, y, s, flip, "", rot)

def shade(c, k=0.75):
    """Darken (k<1) or lighten (k>1) a #rrggbb colour."""
    if not c.startswith("#") or len(c) != 7: return c
    v = [int(c[i:i + 2], 16) for i in (1, 3, 5)]
    v = [min(255, int(x * k)) if k < 1 else min(255, int(x + (255 - x) * (k - 1))) for x in v]
    return "#" + "".join(f"{x:02x}" for x in v)

# ------------------------------------------------------------------ factories
def quad(c="#c8864a", ears="round", tail="thin", horns=None, spots=None, snout=None, head_c=None, expr="happy",
         mane=None, long_legs=False, big=1.0, extra=""):
    """Four-legged animal facing right. Body ~70 wide, ~60 tall."""
    hc = head_c or c
    leg = 24 if long_legs else 16
    by = -leg - 14
    o = ""
    # tail
    if tail == "thin": o += P(f"M-30,{by-4} Q-44,{by-18} -40,{by-30}", "none", 3, INK)
    elif tail == "curl": o += P(f"M-30,{by} q-10,-4 -8,-12 q6,-6 8,2", "none", 3, INK)
    elif tail == "bushy": o += P(f"M-28,{by} Q-52,{by-10} -46,{by-30} Q-34,{by-20} -26,{by-6} Z", c, 2.5) + P(f"M-46,{by-30} l-2,8 l8,-2 Z", "#fff", 1.5)
    elif tail == "tuft": o += P(f"M-30,{by} Q-44,{by+6} -48,{by-6}", "none", 3) + E(-49, by - 9, 4, 6, shade(c, 0.6), 1.5)
    for lx in (-20, -8, 12, 22):
        o += f'<rect x="{lx-4}" y="{-leg}" width="8" height="{leg}" rx="3" fill="{shade(c, 0.85) if lx in (-8, 22) else c}" stroke="{INK}" stroke-width="2.5"/>'
    o += E(0, by, 32 * big, 17 * big, c, 3)
    if spots: o += "".join(E(sx, by + sy, 6, 4.5, spots, 0) for sx, sy in [(-14, -4), (4, 4), (14, -6), (-4, -8)])
    hx, hy = 30, by - 16
    if mane: o += C(hx, hy, 18, mane, 2.5)
    # ears behind head
    if ears == "pointy": o += P(f"M{hx-10},{hy-6} L{hx-8},{hy-22} L{hx},{hy-11} Z", hc, 2.5) + P(f"M{hx+2},{hy-10} L{hx+10},{hy-22} L{hx+11},{hy-5} Z", hc, 2.5)
    elif ears == "round": o += C(hx - 9, hy - 10, 6, hc, 2.5) + C(hx + 9, hy - 10, 6, hc, 2.5)
    elif ears == "floppy": o += E(hx - 11, hy + 2, 5, 10, shade(hc, 0.75), 2.5) + E(hx + 11, hy + 2, 5, 10, shade(hc, 0.75), 2.5)
    elif ears == "long": o += E(hx - 5, hy - 20, 4.5, 13, hc, 2.5) + E(hx + 6, hy - 20, 4.5, 13, hc, 2.5)
    elif ears == "big": o += C(hx - 12, hy - 8, 10, hc, 2.5) + C(hx + 12, hy - 8, 10, hc, 2.5) + C(hx - 12, hy - 8, 5, "#ff9fc4", 0) + C(hx + 12, hy - 8, 5, "#ff9fc4", 0)
    if horns == "small": o += P(f"M{hx-8},{hy-10} l-4,-8 M{hx+8},{hy-10} l4,-8", "none", 3.5, "#f3efe1")
    elif horns == "bull": o += P(f"M{hx-9},{hy-8} Q{hx-24},{hy-12} {hx-22},{hy-26}", "none", 5, "#f3efe1") + P(f"M{hx+9},{hy-8} Q{hx+24},{hy-12} {hx+22},{hy-26}", "none", 5, "#f3efe1")
    elif horns == "curl": o += P(f"M{hx-6},{hy-10} q-14,-10 -6,-20 q8,4 4,12", "none", 4, "#d9c7a0") + P(f"M{hx+6},{hy-10} q14,-10 6,-20 q-8,4 -4,12", "none", 4, "#d9c7a0")
    elif horns == "antlers": o += P(f"M{hx-6},{hy-12} l-6,-16 m3,8 l-8,-4 M{hx+6},{hy-12} l6,-16 m-3,8 l8,-4", "none", 3, "#8a5a2b")
    o += C(hx, hy, 14, hc, 3)
    if snout == "pig": o += E(hx + 1, hy + 5, 6, 4.5, "#ff9fc4", 2) + C(hx - 1, hy + 5, 1.2, INK, 0) + C(hx + 3, hy + 5, 1.2, INK, 0)
    elif snout == "muzzle": o += E(hx + 2, hy + 6, 8, 5.5, "#f3e2c0", 2) + E(hx + 2, hy + 3, 2.5, 1.8, INK, 0)
    elif snout == "cow": o += E(hx + 1, hy + 7, 9, 6, "#ffb3c8", 2) + C(hx - 2, hy + 7, 1.3, INK, 0) + C(hx + 4, hy + 7, 1.3, INK, 0)
    elif snout == "fox": o += P(f"M{hx+6},{hy+2} L{hx+20},{hy+6} L{hx+6},{hy+10} Z", "#fff", 2) + C(hx + 19, hy + 6, 1.8, INK, 0)
    elif snout == "whisker": o += P(f"M{hx+4},{hy+6} l12,-3 M{hx+4},{hy+8} l12,2 M{hx-4},{hy+6} l-12,-3 M{hx-4},{hy+8} l-12,2", "none", 1, INK) + C(hx, hy + 5, 1.8, "#ff7a9a", 0)
    o += face(hx, hy - 3, 0.75, expr)
    return o + extra

def bird(c="#e0533b", wing=None, beak="#f4c542", crest=None, tail=None, big_eyes=False, long_legs=False, belly=None, expr="happy", flat_bill=False):
    """Standing bird facing right, ~75 tall."""
    leg = 22 if long_legs else 10
    o = P(f"M-4,-{leg} l-3,{leg} M6,-{leg} l3,{leg}", "none", 3, "#e0a030")
    if tail == "fan":
        o += "".join(P(f"M-6,-{leg+24} L{-6+46*math.cos(a):.1f},{-leg-24+46*math.sin(a):.1f}", "none", 7, "#1f8a8a") + C(-6 + 44 * math.cos(a), -leg - 24 + 44 * math.sin(a), 5, "#2f6db5", 1.5, "#f4c542")
                     for a in [math.radians(d) for d in range(-170, -10, 22)])
    elif tail == "long": o += P(f"M-14,-{leg+18} L-40,-{leg+4} L-36,-{leg+14} Z", shade(c, 0.8), 2.5)
    else: o += P(f"M-14,-{leg+16} L-28,-{leg+10} L-24,-{leg+22} Z", shade(c, 0.8), 2.5)
    o += E(0, -leg - 22, 20, 22, c, 3)
    if belly: o += E(4, -leg - 16, 11, 13, belly, 0)
    o += P(f"M-12,-{leg+28} Q-4,-{leg+10} 12,-{leg+18} Q2,-{leg+32} -12,-{leg+28} Z", wing or shade(c, 0.8), 2.5)
    hy = -leg - 50
    if crest: o += P(f"M4,{hy-10} l-4,-12 l6,6 l2,-12 l4,12 Z", crest, 2)
    o += C(6, hy, 13, c, 3)
    if flat_bill: o += E(21, hy + 3, 9, 4, beak, 2)
    else: o += P(f"M16,{hy-2} L28,{hy+3} L16,{hy+7} Z", beak, 2)
    if big_eyes: o += C(2, hy - 2, 5.5, "#fff", 1.5) + C(12, hy - 2, 5.5, "#fff", 1.5) + C(3, hy - 1, 2.5, INK, 0) + C(13, hy - 1, 2.5, INK, 0)
    else:
        o += C(10, hy - 3, 3.5, "#fff", 1.3) + C(11, hy - 2.5, 1.8, INK, 0)
        if expr in ("angry", "mean"): o += L(5, hy - 9, 14, hy - 5, INK, 2)
    return o

def bug(c="#23233a", segs=3, legs=6, wings=False, stripes=None, antenna=True, expr="happy", round_body=False):
    """Insect/arachnid seen from the side, ~50 tall; drawn big so it reads."""
    o = ""
    if round_body:
        for k in range(legs // 2):
            x = -14 + k * 9
            o += P(f"M{x},-26 q-6,10 -10,26 M{x+6},-26 q8,10 12,26", "none", 3, INK)
        o += E(0, -30, 28, 22, c, 3)
        o += C(24, -40, 12, shade(c, 1.3), 3) + face(26, -42, 0.7, expr)
        return o
    xs = [-26, -4, 22][:segs] if segs == 3 else [-16, 16]
    for k in range(legs // 2):
        x = -8 + k * 8
        o += P(f"M{x},-22 l-8,22 M{x+2},-22 l6,22", "none", 2.5, INK)
    if wings: o += E(-6, -46, 12, 18, "#dff3ff", 2, extra='opacity="0.85"') + E(6, -48, 10, 16, "#dff3ff", 2, extra='opacity="0.85"')
    for k, x in enumerate(xs):
        r = 14 if k == 0 else 11 if k < len(xs) - 1 else 12
        o += E(x, -26, r + 2, r, c, 3)
    if stripes: o += "".join(L(xs[0] - 8 + 6 * k, -38, xs[0] - 10 + 6 * k, -14, stripes, 4) for k in range(3))
    hx = xs[-1]
    if antenna: o += P(f"M{hx},-36 q2,-14 10,-18 M{hx+4},-34 q8,-10 16,-10", "none", 2, INK)
    o += face(hx + 2, -28, 0.7, expr)
    return o

ROLE = {  # person role -> (npc kind or SPECS key, extra hat/prop)
    "rancher": ("npc:farmer", None), "violinist": ("npc:poet", "notes"), "climber": ("npc:captain", None), "president": ("npc:official", "scroll"),
    "emperor": ("caliph", None), "wrestler": ("npc:smith", None), "delegate": ("npc:official", "chefhat"),
    "curator": ("npc:scholar", "magnifier"), "interpreter": ("npc:envoy", "scroll"), "mime": ("npc:dyer", "clown"), "hedonist": ("npc:prince", None),
    "bride": ("npc:woman", "queencrown"), "fortune-teller": ("npc:hooded", None), "accuser": ("npc:official", None),
    "butler": ("npc:official", None), "auctioneer": ("npc:official", "gavel"), "reaper": ("npc:hooded", "spear"), "hypnotist": ("npc:poet", "wizardhat"),
    "host": ("npc:envoy", None), "racer": ("npc:dyer", None), "taster": ("npc:official", "chefhat"),
    "artisan": ("npc:woman", "hammer"), "tailor": ("npc:woman", "scroll"), "collector": ("npc:scholar", "scroll"), "jeweler": ("npc:official", "magnifier"),
    "composer": ("npc:poet", "notes"), "conductor": ("npc:poet", "notes"),
    "trainer": ("npc:captain", "whistle"), "manager": ("npc:official", None), "caveman": ("npc:vagabond", "hammer"), "mentor": ("npc:oldman", "scroll"),
    "gambler": ("npc:vagabond", None), "artist": ("npc:dyer", "brush"), "politician": ("npc:envoy", "scroll"),
    "glutton": ("npc:official", None), "mechanic": ("npc:inventor", "hammer"), "swimmer": ("npc:dyer", None),
    "nomad": ("npc:vagabond", None),
    "miner": ("npc:smith", "hammer"),
    "man": ("npc:vagabond", None), "woman": ("npc:woman", None), "kid": ("npc:dyer", "small"), "child": ("npc:dyer", "small"), "boy": ("npc:dyer", "small"),
    "girl": ("npc:clerk", "small"), "baby": ("baby", None), "grandpa": ("npc:oldman", None), "grandma": ("npc:oldwoman", None), "oldman": ("npc:oldman", None),
    "king": ("caliph", None), "caliph": ("caliph", None), "sultan": ("caliph", None), "queen": ("npc:envoy", "queencrown"), "princess": ("npc:woman", "queencrown"),
    "prince": ("npc:prince", None), "sailor": ("npc:captain", None), "pirate": ("npc:vagabond", "eyepatch"), "captain": ("npc:captain", None),
    "knight": ("npc:captain", "sword"), "soldier": ("npc:captain", "spear"), "guard": ("npc:captain", "spear"), "warrior": ("npc:captain", "sword"),
    "judge": ("npc:scholar", "gavel"), "scholar": ("npc:scholar", None), "professor": ("npc:scholar", None), "teacher": ("npc:scholar", None),
    "scientist": ("npc:inventor", "flask"), "inventor": ("npc:inventor", None), "doctor": ("npc:physician", None), "physician": ("npc:physician", None),
    "detective": ("npc:hooded", "magnifier"), "spy": ("npc:hooded", None), "thief": ("npc:hooded", "sack"), "ninja": ("npc:hooded", None),
    "chef": ("npc:official", "chefhat"), "baker": ("npc:official", "chefhat"), "cook": ("npc:official", "chefhat"), "merchant": ("npc:official", "coinbag"),
    "farmer": ("npc:farmer", None), "gardener": ("npc:farmer", None), "smith": ("npc:smith", None), "blacksmith": ("npc:smith", None),
    "poet": ("npc:poet", "scroll"), "singer": ("npc:poet", "notes"), "rapper": ("npc:dyer", "notes"), "orator": ("npc:envoy", "scroll"),
    "diplomat": ("npc:envoy", None), "envoy": ("npc:envoy", None), "messenger": ("npc:dyer", None), "courier": ("npc:dyer", None), "clown": ("npc:dyer", "clown"),
    "dancer": ("npc:woman", None), "athlete": ("npc:dyer", None), "weightlifter": ("npc:smith", "barbell"), "wizard": ("npc:inventor", "wizardhat"),
    "rebel": ("npc:vagabond", None), "bully": ("npc:vagabond", None), "dude": ("npc:dyer", None), "owner": ("npc:official", None), "wanderer": ("npc:vagabond", None),
    "hermit": ("npc:oldman", None), "sage": ("npc:oldman", None), "mayor": ("npc:official", None), "official": ("npc:official", None), "banker": ("npc:official", "coinbag"),
    "miser": ("npc:official", "coinbag"), "lawyer": ("npc:scholar", "scroll"), "hero": ("npc:dyer", "sword"), "villain": ("npc:hooded", None), "vizier": ("zulmat", None),
    "sorcerer": ("npc:hooded", "wizardhat"), "witch": ("npc:hooded", "wizardhat"), "monk": ("npc:hooded", None), "priest": ("npc:scholar", None), "student": ("npc:clerk", "scroll"),
    "librarian": ("npc:clerk", "scroll"), "gymnast": ("npc:woman", None), "acrobat": ("npc:dyer", None), "explorer": ("npc:captain", None), "fisherman": ("npc:fishwoman", None),
    "nurse": ("npc:physician", None), "carpenter": ("npc:smith", "hammer"), "builder": ("npc:smith", "hammer"), "painter": ("npc:dyer", "brush"),
    "musician": ("npc:poet", "notes"), "drummer": ("npc:dyer", "drum"), "referee": ("npc:official", "whistle"), "coach": ("npc:official", "whistle"),
    "person": ("npc:vagabond", None), "guy": ("npc:vagabond", None), "lady": ("npc:woman", None), "family": ("family", None), "crowd": ("crowd", None),
    "team": ("crowd", None), "band": ("crowd", "notes"), "army": ("crowd", "spear"), "group": ("crowd", None), "everyone": ("crowd", None), "audience": ("crowd", None),
}

def _role_spec(key, seed=3):
    if key.startswith("npc:"):
        import autoart
        return autoart.npc_spec(key[4:], seed)
    return SPECS[key]

def person(role="man", expr="happy", c=None, **kw):
    kind, extra = ROLE.get(role, ("npc:vagabond", None))
    if kind == "crowd":
        return "".join(gs(_crowd_body(k, c), dx, 0, s) for k, (dx, s) in enumerate([(-26, 0.8), (26, 0.8), (0, 0.95)])) + (_extra(extra, 0, -60) if extra else "")
    if kind == "family":
        return (gs(person("man", expr), -22, 0, 0.9) + gs(person("woman", expr), 20, 0, 0.85) + gs(person("kid", expr), 0, 0, 0.55))
    if kind == "baby":
        return (E(0, -18, 18, 16, c or "#f7f3e8", 3) + C(0, -46, 15, "#e8b98d", 3) + face(0, -48, 0.9, expr) + P("M-3,-60 q3,-6 6,0", "none", 2))
    small = extra == "small"
    if small: extra = None
    spec = dict(_role_spec(kind))
    if c: spec.update(tunic=c, sleeve=c)
    pose = {"judge": ("down", "up"), "knight": ("down", "up"), "soldier": ("down", "up"), "singer": ("down", "wave"), "orator": ("down", "point")}.get(role, ("down", "wave"))
    body = human(spec, "angry" if expr in ("mean", "angry") else "shock" if expr in ("shock", "scared", "gasp") else "sad" if expr in ("sad", "crying") else "happy", pose)
    sc = 0.2 if small else 0.27
    o = gs(body, 0, 0, sc)
    if extra: o += _extra(extra, 0, -300 * sc + 3)
    return o

def _crowd_body(k, c):
    cols = ["#2f6db5", "#e0533b", "#3f9b4a"]
    col = c or cols[k % 3]
    return E(0, -24, 14, 24, col, 2.5) + C(0, -58, 12, "#d19a6a", 2.5) + face(0, -58, 0.7, "happy")

def _extra(kind, x, top):
    """Role props, placed relative to a person's head top (x, top)."""
    if kind == "queencrown": return P(f"M{x-12},{top+6} L{x-14},{top-10} L{x-6},{top-2} L{x},{top-14} L{x+6},{top-2} L{x+14},{top-10} L{x+12},{top+6} Z", "#f4c542", 2)
    if kind == "chefhat": return P(f"M{x-10},{top+8} v-8 q-8,-10 2,-14 q6,-10 14,0 q10,2 2,14 v8 Z", "#fff", 2)
    if kind == "wizardhat": return P(f"M{x-14},{top+6} L{x+2},{top-24} L{x+14},{top+6} Z", "#6b2fa0", 2) + sparkle(x + 2, top - 8, 4)
    if kind == "clown": return C(x + 10, top + 38, 4, "#e0533b", 1.5) + P(f"M{x-10},{top+4} L{x},{top-14} L{x+10},{top+4} Z", "#ffd23f", 2)
    if kind == "sword": return L(x + 28, top + 44, x + 32, top - 4, "#c9ccd8", 3.5) + L(x + 23, top + 40, x + 35, top + 38, INK, 3)
    if kind == "spear": return L(x + 28, top + 70, x + 30, top - 8, "#8a5a2b", 3) + P(f"M{x+30},{top-16} l-4,10 h8 Z", "#c9ccd8", 1.5)
    if kind == "gavel": return f'<rect x="{x+22}" y="{top+6}" width="16" height="8" rx="2" fill="#8a5a2b" stroke="{INK}" stroke-width="1.5"/>' + L(x + 30, top + 14, x + 30, top + 30, "#8a5a2b", 3)
    if kind == "magnifier": return C(x + 30, top + 30, 7, "#dff3ff", 2.5) + L(x + 26, top + 36, x + 22, top + 44, "#8a5a2b", 3)
    if kind == "flask": return P(f"M{x+26},{top+24} h6 v6 l6,12 h-18 l6,-12 Z", "#9cff57", 1.5)
    if kind == "sack": return E(x - 24, top + 50, 10, 12, "#c9a26a", 2)
    if kind == "scroll": return f'<rect x="{x+20}" y="{top+22}" width="16" height="20" fill="#efe2c0" stroke="{INK}" stroke-width="1.5"/>'
    if kind == "notes": return T(x + 26, top + 8, "♪", 14, "#f4c542") + T(x + 36, top + 20, "♫", 12, "#f4c542")
    if kind == "barbell": return L(x - 34, top + 20, x + 34, top + 20, INK, 3) + C(x - 34, top + 20, 7, "#555", 2) + C(x + 34, top + 20, 7, "#555", 2)
    if kind == "eyepatch": return L(x - 12, top + 18, x + 12, top + 10, INK, 1.5)
    if kind == "coinbag": return E(x - 24, top + 52, 9, 10, "#d9a441", 2) + T(x - 24, top + 56, "$", 9, INK)
    if kind == "hammer": return L(x + 28, top + 40, x + 30, top + 18, "#8a5a2b", 3) + f'<rect x="{x+22}" y="{top+12}" width="16" height="7" fill="#6b6b78" stroke="{INK}" stroke-width="1.5"/>'
    if kind == "brush": return L(x + 28, top + 40, x + 34, top + 16, "#8a5a2b", 3) + C(x + 34, top + 14, 4, "#e0533b", 1.5)
    if kind == "drum": return E(x + 26, top + 58, 12, 5, "#e0533b", 2) + f'<rect x="{x+14}" y="{top+58}" width="24" height="12" fill="#e0533b" stroke="{INK}" stroke-width="2"/>'
    if kind == "whistle": return C(x + 16, top + 36, 3, "#c9ccd8", 1.5)
    return ""

# ------------------------------------------------------------------ the library
def _crow(c=None, **k):
    return gs(P("M-30,0 Q-10,-40 20,-30 Q40,-26 44,-10 L60,-6 L44,0 Q20,12 -30,0 Z", c or "#15151f", 3, "#000")
              + P("M-10,-14 Q-40,-50 -60,-40 Q-40,-20 -10,-8 Z", "#23233a", 2.5, "#000") + C(30, -18, 4, "#ffe066", 0)
              + (L(22, -26, 34, -22, "#ffe066", 2) if k.get("expr") in ("mean", "angry") else "")
              + L(0, 2, -4, 16, "#f4c542", 3) + L(10, 2, 12, 16, "#f4c542", 3), -6, -18, 1.1)

def _gnome(c=None, expr="happy", **k):
    return (E(0, -4, 20, 5, "#6b8a3a", 0) + P("M-16,-4 Q-18,-34 0,-36 Q18,-34 16,-4 Z", c or "#2f6db5", 3) + L(-16, -18, 16, -18, "#8a5a2b", 4)
            + C(0, -44, 12, "#e8b98d", 3) + P("M-12,-40 Q-14,-20 0,-18 Q14,-20 12,-40 Q0,-34 -12,-40 Z", "#f7f3e8", 2.5)
            + face(0, -47, 0.62, expr) + P("M-13,-50 L2,-82 L13,-50 Z", "#e0533b", 3) + C(0, -40, 3, "#ffb3a0", 1.2))

def _imp(c=None, expr="grin", **k):
    c = c or "#e0533b"
    return (P("M-8,-6 l-6,6 M8,-6 l6,6", "none", 3) + P("M14,-26 Q30,-20 28,-6 l6,-2 l-4,6", "none", 3, INK)
            + E(0, -22, 13, 16, c, 3) + C(0, -46, 14, c, 3) + P("M-10,-56 l-6,-14 l10,8 Z M10,-56 l6,-14 l-10,8 Z", "#fff6c9", 2)
            + P("M-9,-44 l6,-3 M9,-44 l-6,-3", "none", 2) + C(-5, -41, 2.4, INK, 0) + C(5, -41, 2.4, INK, 0)
            + P("M-7,-35 Q0,-29 7,-35", "#fff", 1.8) + P("M-14,-26 l-12,-10", "none", 3.5, c))

def _bread(c=None, **k):
    return (P("M-34,0 Q-38,-34 0,-36 Q38,-34 34,0 Z", c or "#d9a05a", 3) + "".join(P(f"M{x},-30 q6,6 4,14", "none", 2.5, "#8a5a2b") for x in (-16, -2, 12))
            + E(-20, -6, 6, 3, "#fff6c9", 0, extra='opacity="0.5"'))

def _tick(c=None, expr="skeptic", monocle=True, **k):
    c = c or "#6b4a3a"
    o = "".join(P(f"M{x},-24 q{-8 if x < 0 else 8},8 {-10 if x < 0 else 10},24", "none", 3) for x in (-18, -8, 8, 18))
    o += E(0, -34, 30, 26, c, 3) + P("M-20,-48 Q0,-62 20,-48", "none", 2.5, shade(c, 0.7)) + C(22, -48, 10, shade(c, 0.8), 3)
    o += E(14, -44, 5, 6, "#fff", 1.5) + C(15, -43, 2.5, INK, 0) + E(28, -46, 5, 6, "#fff", 1.5) + C(29, -45, 2.5, INK, 0)
    o += L(9, -54, 19, -52, INK, 2) + P("M23,-55 Q28,-60 33,-54", "none", 2)
    if monocle: o += C(28, -46, 7, "none", 2, "#f4c542") + P("M28,-39 q-2,10 4,18", "none", 1.2, "#f4c542")
    return o

def _candy(c=None, expr="shock", **k):
    c = c or "#ff5fa2"
    return (P("M-34,-28 l-14,-10 v26 Z", c, 2.5) + P("M34,-28 l14,-10 v26 Z", c, 2.5)
            + E(0, -28, 34, 22, c, 3) + "".join(P(f"M{x},-48 q10,20 0,40", "none", 5, "#fff", extra='opacity="0.7"') for x in (-20, 0, 20))
            + face(0, -30, 0.95, expr))

def _pickle(c=None, expr="happy", tophat=False, **k):
    c = c or "#6fae3a"
    o = P("M-16,-4 Q-24,-40 -8,-70 Q6,-82 16,-66 Q26,-36 14,-4 Q0,4 -16,-4 Z", c, 3)
    o += "".join(C(x, y, 2.2, shade(c, 0.7), 0) for x, y in [(-10, -20), (6, -30), (-4, -46), (10, -52), (-12, -36)])
    o += face(2, -50, 0.75, expr)
    if tophat: o += f'<rect x="-12" y="-96" width="24" height="18" fill="#15152a" stroke="{INK}" stroke-width="2"/>' + L(-18, -78, 18, -78, INK, 4) + L(-12, -82, 12, -82, "#c0262d", 3)
    return o

def _monster(c=None, expr="angry", **k):
    c = c or "#6b2fa0"
    spikes = "".join(P(f"M{x-6},{-60+abs(x)/3} L{x},{-80+abs(x)/3} L{x+6},{-60+abs(x)/3} Z", "#f4c542", 2) for x in (-24, -8, 8, 24))
    return (spikes + P("M-34,0 Q-40,-64 0,-66 Q40,-64 34,0 Z", c, 3) + P("M-34,-30 l-14,10 M34,-30 l14,10", "none", 6, c)
            + face(0, -40, 1.1, expr) + P("M-12,-24 l4,6 l4,-6 l4,6 l4,-6 l4,6", "#fff", 1.5)
            + "".join(C(x, y, 3, shade(c, 0.7), 0) for x, y in [(-20, -14), (18, -18), (-6, -8)]))

def _ball(c=None, expr="grin", **k):
    c = c or "#e0533b"
    return C(0, -30, 30, c, 3) + P("M-30,-30 Q0,-14 30,-30", "none", 3, "#fff") + P("M-20,-52 Q-8,-40 -2,-58", "none", 3, "#fff", extra='opacity="0.6"') + face(0, -32, 0.9, expr)

def _fish(c=None, expr="shock", **k):
    c = c or "#63aee0"
    return (P("M28,-34 L50,-52 L48,-16 Z", shade(c, 0.8), 3) + E(0, -34, 34, 24, c, 3) + P("M-4,-56 q10,-12 20,0", shade(c, 0.8), 2.5)
            + C(-14, -40, 6, "#fff", 2) + C(-13, -40, 3, INK, 0) + (E(-30, -30, 6, 9, "#5a1420", 2) if expr in ("shock", "gasp") else P("M-34,-30 q4,4 8,0", "none", 2))
            + "".join(P(f"M{x},-44 q6,10 0,20", "none", 1.5, shade(c, 0.7)) for x in (4, 14)))

def _king(c=None, expr="shock", **k):
    return person("king", expr, c)

def _crown(c=None, **k):
    c = c or "#f4c542"
    return (P("M-30,0 L-34,-40 L-18,-22 L0,-48 L18,-22 L34,-40 L30,0 Z", c, 3) + C(0, -14, 5, "#e0533b", 2) + C(-18, -12, 3.5, "#2f6db5", 1.5) + C(18, -12, 3.5, "#3f9b4a", 1.5)
            + C(0, -50, 4, "#fff6c9", 1.5))

def _robot(c=None, expr="happy", **k):
    c = c or "#9aa8b8"
    return (f'<rect x="-16" y="-24" width="10" height="24" fill="{shade(c,0.8)}" stroke="{INK}" stroke-width="2.5"/><rect x="6" y="-24" width="10" height="24" fill="{shade(c,0.8)}" stroke="{INK}" stroke-width="2.5"/>'
            f'<rect x="-22" y="-54" width="44" height="32" rx="4" fill="{c}" stroke="{INK}" stroke-width="3"/>' + C(0, -38, 5, "#e0533b", 2)
            + P("M-22,-48 l-12,14 M22,-48 l12,14", "none", 4, shade(c, 0.8)) + f'<rect x="-16" y="-80" width="32" height="24" rx="4" fill="{c}" stroke="{INK}" stroke-width="3"/>'
            + f'<rect x="-11" y="-74" width="22" height="10" rx="3" fill="#1b1b2f"/>' + C(-5, -69, 2.5, "#00e5ff", 0) + C(5, -69, 2.5, "#00e5ff", 0)
            + L(0, -80, 0, -88, INK, 2) + C(0, -90, 3, "#e0533b", 1.5))

def _cake(c=None, **k):
    c = c or "#ff9fc4"
    return (f'<rect x="-32" y="-26" width="64" height="26" rx="3" fill="#f3d9a0" stroke="{INK}" stroke-width="3"/><rect x="-24" y="-48" width="48" height="22" rx="3" fill="{c}" stroke="{INK}" stroke-width="3"/>'
            + P("M-32,-26 q8,8 16,0 q8,8 16,0 q8,8 16,0 q8,8 16,0", "#fff", 2) + L(0, -48, 0, -62, "#fff6c9", 4) + P("M0,-62 q-5,-6 0,-12 q5,6 0,12 Z", "#ffb020", 1.5))

def _door(c=None, **k):
    c = c or "#8a5a2b"
    return P("M-24,0 V-56 Q0,-84 24,-56 V0 Z", c, 3) + L(0, -70, 0, 0, shade(c, 0.7), 2) + C(12, -30, 3, "#f4c542", 1.5)

def _key(c=None, **k):
    c = c or "#f4c542"
    return C(-20, -30, 14, c, 3) + C(-20, -30, 5, "#2a1450", 2) + f'<rect x="-6" y="-34" width="44" height="8" fill="{c}" stroke="{INK}" stroke-width="2.5"/>' + P("M26,-26 v10 h6 v-10 M36,-26 v8", c, 2.5)

def _coin(c=None, **k):
    c = c or "#f4c542"
    return C(0, -32, 28, c, 3) + C(0, -32, 20, "none", 2, shade(c, 0.7)) + T(0, -23, "¢", 26, shade(c, 0.55))

def _money(c=None, **k):
    return "".join(E(dx, -6 - 7 * i, 18, 6, "#f4c542", 2.5) for dx, n in ((-18, 3), (18, 2)) for i in range(n)) + P("M-12,-18 Q-16,-56 0,-58 Q16,-56 12,-18 Z", "#3f9b4a", 2.5) + T(0, -30, "$", 16, "#fff")

def _clock(c=None, expr="happy", **k):
    return props.clock_face(0, -36, 30) + L(-18, -8, -24, 0, INK, 3) + L(18, -8, 24, 0, INK, 3)

def _shoe(c=None, expr="happy", **k):
    c = c or "#8a3a2a"
    return P("M-34,0 V-22 Q-30,-40 -14,-40 L-6,-26 Q10,-20 30,-16 Q40,-12 38,0 Z", c, 3) + L(-34, -4, 38, -4, "#1b1b2f", 4) + P("M-10,-32 l8,4 M-12,-26 l8,4", "none", 2, "#fff")

def _mountain(c=None, **k):
    c = c or "#8a7a9a"
    return P("M-44,0 L-8,-76 L10,-48 L20,-60 L46,0 Z", c, 3) + P("M-18,-56 L-8,-76 L2,-56 L-4,-60 L-10,-54 Z", "#fff", 2)

def _volcano(c=None, **k):
    return P("M-44,0 L-14,-60 L14,-60 L44,0 Z", c or "#6b4a3a", 3) + P("M-14,-60 q-6,-16 4,-20 q4,-12 14,-4 q10,-6 10,6 Z", "#ff7a1a", 2) + P("M-10,-60 l4,18 l6,-10 l6,14", "none", 3, "#ff7a1a")

def _train(c=None, **k):
    c = c or "#c0262d"
    return (f'<rect x="-40" y="-40" width="56" height="30" rx="3" fill="{c}" stroke="{INK}" stroke-width="3"/><rect x="10" y="-60" width="26" height="50" rx="3" fill="{shade(c,0.8)}" stroke="{INK}" stroke-width="3"/>'
            + f'<rect x="-34" y="-54" width="10" height="14" fill="#555" stroke="{INK}" stroke-width="2"/>' + C(-28, -64, 6, "#ddd", 0, extra='opacity=".8"') + C(-20, -74, 8, "#ddd", 0, extra='opacity=".6"')
            + "".join(C(x, -8, 8, "#444", 2.5) for x in (-30, -6, 24)) + f'<rect x="16" y="-54" width="14" height="12" fill="#bfefff" stroke="{INK}" stroke-width="2"/>')

def _boat(c=None, **k):
    return props.boat(-44, -26, 88, c or "#8a5a2b")

def _car(c=None, **k):
    c = c or "#2f6db5"
    return P("M-40,-10 V-26 Q-38,-32 -26,-32 L-16,-48 H16 L28,-32 Q40,-32 40,-24 V-10 Z", c, 3) + P("M-12,-44 H12 L20,-32 H-20 Z", "#bfefff", 2) + C(-22, -8, 8, "#333", 2.5) + C(22, -8, 8, "#333", 2.5)

def _rocket(c=None, **k):
    c = c or "#e0533b"
    return (P("M0,-84 Q16,-64 14,-20 H-14 Q-16,-64 0,-84 Z", "#f7f3e8", 3) + C(0, -52, 7, "#63aee0", 2.5) + P("M-14,-30 L-26,-10 L-14,-18 Z M14,-30 L26,-10 L14,-18 Z", c, 2.5)
            + P("M-10,-20 L0,4 L10,-20 Z", "#ff9a1a", 2) + P("M0,-84 Q8,-76 10,-66 H-10 Q-8,-76 0,-84 Z", c, 2))

def _house(c=None, **k):
    c = c or "#e8d6b0"
    return f'<rect x="-30" y="-44" width="60" height="44" fill="{c}" stroke="{INK}" stroke-width="3"/>' + P("M-38,-44 L0,-78 L38,-44 Z", "#c0262d", 3) + P("M-8,0 v-22 h16 v22", "#6b4a2a", 2.5) + f'<rect x="12" y="-34" width="12" height="12" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'

def _castle(c=None, **k):
    c = c or "#c9b89a"
    tow = lambda x, h: f'<rect x="{x-9}" y="{-h}" width="18" height="{h}" fill="{c}" stroke="{INK}" stroke-width="2.5"/>' + P(f"M{x-11},{-h} L{x},{-h-14} L{x+11},{-h} Z", "#c0262d", 2)
    return f'<rect x="-30" y="-44" width="60" height="44" fill="{c}" stroke="{INK}" stroke-width="3"/>' + tow(-32, 64) + tow(32, 64) + P("M-8,0 v-18 q8,-10 16,0 v18", "#4a3a2a", 2)

def _star(c=None, expr="happy", **k):
    c = c or "#ffd23f"
    pts = " ".join(f"{(34 if j % 2 == 0 else 15) * math.cos(math.radians(-90 + j * 36)):.1f},{-38 + (34 if j % 2 == 0 else 15) * math.sin(math.radians(-90 + j * 36)):.1f}" for j in range(10))
    return f'<polygon points="{pts}" fill="{c}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>' + face(0, -36, 0.7, expr)

def _crescent(r1=34, cx2=16, cy2=-46, r2=30, cy1=-38):
    """Crescent path: circle (0,cy1,r1) minus circle (cx2,cy2,r2)."""
    dx, dy = cx2, cy2 - cy1
    d = math.hypot(dx, dy)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(r1 * r1 - a * a, 0))
    mx, my = a * dx / d, cy1 + a * dy / d
    p1 = (mx + h * dy / d, my - h * dx / d)
    p2 = (mx - h * dy / d, my + h * dx / d)
    return f"M{p1[0]:.1f},{p1[1]:.1f} A{r1},{r1} 0 1 0 {p2[0]:.1f},{p2[1]:.1f} A{r2},{r2} 0 0 1 {p1[0]:.1f},{p1[1]:.1f} Z"

def _moon(c=None, expr="sleepy", **k):
    c = c or "#9dffb0"
    return P(_crescent(), c, 3) + face(-16, -36, 0.55, expr)

def _sun(c=None, expr="happy", **k):
    return "".join(L(34 * math.cos(a), -38 + 34 * math.sin(a), 44 * math.cos(a), -38 + 44 * math.sin(a), "#ff9a1a", 4) for a in [j * math.pi / 6 for j in range(12)]) + C(0, -38, 26, c or "#ffd23f", 3) + face(0, -38, 0.9, expr)

def _cloud(c=None, expr="happy", **k):
    c = c or "#f7f3e8"
    return "".join(C(x, y, r, c, 3) for x, y, r in [(-22, -24, 16), (0, -34, 22), (22, -24, 16)]) + f'<rect x="-22" y="-26" width="44" height="18" fill="{c}"/>' + L(-36, -8, 36, -8, INK, 3) + face(0, -28, 0.7, expr)

def _flower(c=None, expr="happy", **k):
    c = c or "#ff5fa2"
    return L(0, 0, 0, -44, "#3f9b4a", 5) + P("M0,-20 q16,-10 22,4 q-14,6 -22,-4 Z", "#3f9b4a", 2) + "".join(C(16 * math.cos(a), -58 + 16 * math.sin(a), 11, c, 2.5) for a in [j * math.pi / 3 for j in range(6)]) + C(0, -58, 11, "#ffd23f", 2.5) + face(0, -58, 0.5, expr)

def _tree(c=None, **k):
    return f'<rect x="-7" y="-36" width="14" height="36" fill="#8a5a2b" stroke="{INK}" stroke-width="2.5"/>' + "".join(C(x, y, r, c or "#3f9b4a", 3) for x, y, r in [(-18, -46, 18), (18, -46, 18), (0, -64, 22)])

def _cactus(c=None, expr="happy", **k):
    c = c or "#3f9b4a"
    return P("M-10,0 V-64 Q0,-78 10,-64 V0 Z", c, 3) + P("M-10,-30 H-22 V-50", "none", 9, c) + P("M10,-40 H22 V-56", "none", 9, c) + face(0, -52, 0.55, expr)

def _book(c=None, expr=None, **k):
    c = c or "#8a3a2a"
    o = P("M-34,-8 L-34,-56 Q-18,-62 0,-54 Q18,-62 34,-56 L34,-8 Q18,-14 0,-6 Q-18,-14 -34,-8 Z", "#fff6c9", 3) + L(0, -54, 0, -6, INK, 2)
    o += P("M-36,-6 L-36,-58 M36,-6 L36,-58", "none", 4, c) + "".join(L(-28, y, -6, y + 2, "#9a8a6a", 1.5) + L(6, y + 2, 28, y, "#9a8a6a", 1.5) for y in (-46, -38, -30, -22))
    return o + (face(0, -34, 0.6, expr) if expr else "")

def _scroll(c=None, **k):
    return f'<rect x="-26" y="-60" width="52" height="50" fill="#efe2c0" stroke="{INK}" stroke-width="3"/>' + E(-26, -35, 5, 26, "#d9c79a", 2.5) + E(26, -35, 5, 26, "#d9c79a", 2.5) + "".join(L(-16, y, 16, y, "#9a8a6a", 1.5) for y in (-48, -40, -32, -24))

def _mirror(c=None, **k):
    return E(0, -46, 24, 32, c or "#d9a441", 3) + E(0, -46, 17, 25, "#bfefff", 2) + P("M-8,-60 l10,-8 M-10,-50 l14,-12", "none", 2, "#fff") + L(0, -14, 0, 0, INK, 5)

def _bell(c=None, **k):
    return props.bell(0, -40, 0.9, c or "#d9a441")

def _egg(c=None, **k):
    return props.big_egg(0, 0, 0.62)

def _lamp(c=None, **k):
    return P("M-30,-14 Q-26,-30 0,-30 Q26,-30 40,-40 L34,-30 Q30,-12 0,-10 Q-26,-10 -30,-14 Z", c or "#d9a441", 3) + P("M-28,-14 l-14,-6", "none", 3) + P("M40,-40 q10,-20 -4,-34 q-4,14 -8,20", "#bfefff", 2, extra='opacity=".7"')

def _genie(c=None, expr="happy", **k):
    c = c or "#63aee0"
    return (_lamp() + P("M36,-38 Q20,-50 24,-64 Q14,-80 -2,-82 Q-20,-80 -18,-62 Q-16,-48 4,-44", c, 3) + C(-4, -76, 12, c, 3)
            + face(-4, -78, 0.6, expr) + P("M-16,-86 Q-4,-98 8,-86 Z", "#e0533b", 2))

def _ghost(c=None, expr="shock", **k):
    c = c or "#f7f3e8"
    return P("M-26,0 V-44 Q-26,-76 0,-76 Q26,-76 26,-44 V0 L18,-8 L9,0 L0,-8 L-9,0 L-18,-8 Z", c, 3, extra='opacity=".92"') + face(0, -50, 0.9, expr)

def _dragon(c=None, expr="angry", **k):
    c = c or "#3f9b4a"
    return (P("M-40,-10 Q-50,-20 -44,-34", "none", 6, c) + P("M-10,-60 L-26,-84 L4,-66 Z", shade(c, 0.8), 2.5) + E(-10, -28, 30, 20, c, 3)
            + P("M4,-40 Q14,-60 24,-62", "none", 12, c) + C(28, -64, 13, c, 3) + P("M38,-62 L50,-58 L38,-54", "#ff7a1a", 1.5) + face(28, -66, 0.6, expr)
            + "".join(P(f"M{x},-46 l4,-8 l4,8", shade(c, 0.7), 1.5) for x in (-30, -18, -6)) + P("M-24,-10 v10 M6,-10 v10", "none", 7, c))

def _snake(c=None, expr="happy", **k):
    c = c or "#3f9b4a"
    return P("M-40,-8 Q-20,-30 0,-8 Q20,14 30,-20 Q34,-40 20,-50", "none", 12, INK) + P("M-40,-8 Q-20,-30 0,-8 Q20,14 30,-20 Q34,-40 20,-50", "none", 8, c) + E(18, -54, 12, 9, c, 2.5) + C(20, -57, 2.5, INK, 0) + P("M28,-52 l8,2 m-8,-2 l8,-3", "none", 1.5, "#e0533b")

def _octopus(c=None, expr="happy", **k):
    c = c or "#b85ac8"
    return "".join(P(f"M{x},-26 q{s*8},12 {s*4},26", "none", 7, c) for x, s in [(-20, -1), (-10, -1), (0, 1), (10, 1), (20, 1)]) + P("M-26,-24 Q-30,-74 0,-76 Q30,-74 26,-24 Z", c, 3) + face(0, -48, 0.9, expr)

def _whale(c=None, expr="happy", **k):
    c = c or "#2f6db5"
    return P("M-46,-26 Q-44,-60 0,-60 Q40,-60 40,-28 Q36,-6 0,-6 Q-30,-6 -46,-26 L-58,-40 L-56,-14 Z", c, 3) + P("M-30,-20 Q0,-10 34,-22", "none", 2, "#bfefff") + C(18, -40, 3, INK, 0) + P("M6,-60 q-4,-14 -12,-18 M6,-60 q4,-14 12,-18", "none", 2.5, "#63aee0")

def _shark(c=None, expr="mean", **k):
    c = c or "#8a94a6"
    return P("M-46,-24 Q-20,-44 20,-40 L-2,-66 L6,-40 Q34,-38 46,-24 Q30,-10 -20,-12 L-44,-2 L-38,-24 Z", c, 3) + P("M24,-24 l4,-4 l4,4 l4,-4 l4,4", "#fff", 1.5) + C(26, -34, 3, INK, 0) + L(20, -40, 30, -36, INK, 2)

def _eel(c=None, **k):
    c = c or "#6b8a3a"
    return P("M-44,-20 Q-24,-44 -4,-20 Q16,4 36,-24", "none", 14, INK) + P("M-44,-20 Q-24,-44 -4,-20 Q16,4 36,-24", "none", 10, c) + C(36, -28, 3, "#fff", 1) + C(37, -28, 1.5, INK, 0)

def _crab(c=None, expr="happy", **k):
    c = c or "#e0533b"
    return ("".join(P(f"M{x},-18 l{s*10},16", "none", 3, c) for x, s in [(-14, -1), (-6, -1), (6, 1), (14, 1)]) + E(0, -26, 26, 16, c, 3)
            + P("M-22,-34 Q-40,-50 -32,-62 l8,6 l-6,6", c, 2.5) + P("M22,-34 Q40,-50 32,-62 l-8,6 l6,6", c, 2.5) + face(0, -28, 0.7, expr))

def _turtle(c=None, **k):
    return P("M-34,-8 Q-30,-46 0,-48 Q30,-46 34,-8 Z", c or "#3f9b4a", 3) + P("M-14,-40 L0,-28 L14,-40 M-24,-16 L-12,-26 L12,-26 L24,-16", "none", 2, shade(c or "#3f9b4a", 0.6)) + C(40, -18, 9, "#9acd6a", 2.5) + C(42, -20, 2, INK, 0) + P("M-24,-8 v8 M20,-8 v8", "none", 6, "#9acd6a")

def _frog(c=None, expr="happy", **k):
    c = c or "#5cbf3a"
    return E(0, -20, 28, 20, c, 3) + C(-12, -40, 9, c, 3) + C(12, -40, 9, c, 3) + C(-12, -40, 5, "#fff", 1.5) + C(12, -40, 5, "#fff", 1.5) + C(-12, -39, 2.5, INK, 0) + C(12, -39, 2.5, INK, 0) + P("M-12,-22 Q0,-12 12,-22", "none", 2.5) + P("M-28,-4 l-10,4 M28,-4 l10,4", "none", 4, c)

def _snail(c=None, **k):
    return P("M-40,0 Q-20,-8 20,-4 Q34,-4 36,-18", "#d9c79a", 3) + C(-4, -30, 24, c or "#c8864a", 3) + P("M-4,-30 m-4,0 a4,4 0 1 1 8,0 a10,10 0 1 1 -20,0 a16,16 0 1 1 32,0", "none", 2.5) + L(34, -18, 38, -34, INK, 2) + C(38, -36, 3, INK, 0)

def _jellyfish(c=None, expr="happy", **k):
    c = c or "#ff9fc4"
    return "".join(P(f"M{x},-36 q-6,12 2,20 q6,10 -2,16", "none", 3, c) for x in (-16, -6, 4, 14)) + P("M-26,-36 Q-26,-72 0,-72 Q26,-72 26,-36 Z", c, 3, extra='opacity=".9"') + face(0, -50, 0.7, expr)

def _seal(c=None, expr="happy", **k):
    c = c or "#8a94a6"
    return P("M-40,-4 Q-44,-30 0,-34 Q14,-50 26,-54 Q42,-50 36,-34 Q30,-20 22,-10 Q10,0 -40,-4 L-50,-14 Z", c, 3) + face(28, -46, 0.6, expr) + C(34, -40, 2, INK, 0) + P("M0,-8 l10,8", "none", 5, shade(c, 0.8))

def _spider(c=None, expr="mean", **k):
    return bug(c or "#23233a", legs=8, round_body=True, expr=expr)

def _butterfly(c=None, **k):
    c = c or "#ff8fc0"
    return E(-16, -48, 16, 20, c, 2.5) + E(16, -48, 16, 20, c, 2.5) + E(-12, -22, 11, 13, shade(c, 0.8), 2.5) + E(12, -22, 11, 13, shade(c, 0.8), 2.5) + E(0, -36, 4, 22, INK, 0) + P("M0,-58 q-4,-12 -10,-14 M0,-58 q4,-12 10,-14", "none", 1.5)

def _worm(c=None, expr="happy", **k):
    c = c or "#ff9fc4"
    return P("M-36,-6 Q-24,-24 -12,-6 Q0,12 12,-6 Q20,-20 26,-30", "none", 12, INK) + P("M-36,-6 Q-24,-24 -12,-6 Q0,12 12,-6 Q20,-20 26,-30", "none", 8, c) + face(26, -34, 0.5, expr)

def _sponge(c=None, expr="happy", **k):
    c = c or "#ffd23f"
    return f'<rect x="-28" y="-56" width="56" height="50" rx="4" fill="{c}" stroke="{INK}" stroke-width="3"/>' + "".join(E(x, y, 3, 4, shade(c, 0.75), 0) for x, y in [(-18, -46), (14, -48), (-8, -20), (18, -16), (0, -36)]) + face(0, -34, 0.8, expr) + P("M-12,-6 v6 M12,-6 v6", "none", 3)

def _soap(c=None, **k):
    return f'<rect x="-30" y="-30" width="60" height="30" rx="10" fill="{c or "#bfe8ff"}" stroke="{INK}" stroke-width="3"/>' + "".join(C(x, y, r, "#fff", 1.5, "#63aee0") for x, y, r in [(-14, -40, 7), (4, -50, 9), (20, -40, 5)])

def _eraser(c=None, **k):
    return P("M-34,-10 L-18,-34 L34,-34 L18,-10 Z", c or "#ff8fc0", 3) + P("M-34,-10 V0 H18 V-10", "#fff", 3) + L(18, -10, 34, -34, INK, 2)

def _net(c=None, **k):
    return L(20, 0, 8, -34, "#8a5a2b", 4) + E(-4, -48, 22, 18, "none", 3, "#c9a26a") + "".join(L(-24 + 8 * j, -60, -24 + 8 * j + 6, -34, "#c9a26a", 1.2) for j in range(6))

def _magnet(c=None, **k):
    return P("M-24,-70 V-34 Q-24,-6 0,-6 Q24,-6 24,-34 V-70 H10 V-34 Q10,-20 0,-20 Q-10,-20 -10,-34 V-70 Z", c or "#e0533b", 3) + f'<rect x="-24" y="-70" width="14" height="12" fill="#c9ccd8" stroke="{INK}" stroke-width="2"/><rect x="10" y="-70" width="14" height="12" fill="#c9ccd8" stroke="{INK}" stroke-width="2"/>'

def _stamp(c=None, **k):
    return f'<rect x="-22" y="-14" width="44" height="14" fill="{c or "#c0262d"}" stroke="{INK}" stroke-width="3"/><rect x="-6" y="-50" width="12" height="36" fill="#8a5a2b" stroke="{INK}" stroke-width="2.5"/>' + C(0, -58, 12, "#8a5a2b", 2.5)

def _camera(c=None, **k):
    return f'<rect x="-32" y="-44" width="64" height="40" rx="5" fill="{c or "#3a3a4a"}" stroke="{INK}" stroke-width="3"/><rect x="-12" y="-52" width="20" height="10" fill="#3a3a4a" stroke="{INK}" stroke-width="2"/>' + C(2, -24, 13, "#63aee0", 3) + C(2, -24, 6, INK, 0) + C(-22, -36, 3, "#ffd23f", 0)

def _phone(c=None, **k):
    return f'<rect x="-18" y="-72" width="36" height="68" rx="6" fill="{c or "#23233a"}" stroke="{INK}" stroke-width="3"/><rect x="-13" y="-64" width="26" height="46" fill="#63aee0"/>' + C(0, -11, 3, "#888", 0)

def _tv(c=None, expr="happy", **k):
    return f'<rect x="-34" y="-58" width="68" height="46" rx="6" fill="{c or "#6b4a3a"}" stroke="{INK}" stroke-width="3"/><rect x="-26" y="-52" width="44" height="34" rx="4" fill="#9ad0ff" stroke="{INK}" stroke-width="2"/>' + P("M-14,-58 l-10,-16 M10,-58 l10,-16", "none", 2.5) + P("M-24,-12 l-4,12 M24,-12 l4,12", "none", 3) + face(-4, -38, 0.6, expr)

def _sword(c=None, **k):
    return P("M-3,-86 L3,-86 L4,-26 L-4,-26 Z", c or "#c9ccd8", 2.5) + f'<rect x="-16" y="-26" width="32" height="6" fill="#d9a441" stroke="{INK}" stroke-width="2"/>' + L(0, -20, 0, -4, "#8a5a2b", 6) + C(0, -2, 4, "#d9a441", 1.5)

def _shield(c=None, **k):
    return P("M-28,-72 H28 V-40 Q28,-10 0,0 Q-28,-10 -28,-40 Z", c or "#2f6db5", 3) + P("M0,-66 V-8 M-22,-44 H22", "none", 4, "#f4c542")

def _anchor(c=None, **k):
    c = c or "#6b6b78"
    return L(0, -74, 0, -8, c, 7) + C(0, -78, 7, "none", 4, c) + L(-14, -60, 14, -60, c, 6) + P("M-30,-26 Q-24,0 0,-6 Q24,0 30,-26", "none", 7, c)

def _drum(c=None, **k):
    return E(0, -50, 30, 10, "#f7f3e8", 3) + P("M-30,-50 V-12 Q0,2 30,-12 V-50", c or "#e0533b", 3) + P("M-30,-44 L-10,-8 L10,-44 L30,-8", "none", 2, "#f4c542") + L(20, -64, 40, -84, "#8a5a2b", 3) + L(-20, -64, -40, -84, "#8a5a2b", 3)

def _guitar(c=None, **k):
    c = c or "#c8773a"
    return C(-8, -18, 18, c, 3) + C(6, -38, 13, c, 3) + C(-2, -28, 5, INK, 0) + P("M12,-46 L34,-78", "none", 6, "#6b4a2a") + P("M30,-82 l8,4 l2,-6", "none", 3)

def _trumpet(c=None, **k):
    c = c or "#f4c542"
    return P("M-36,-34 h40 l24,-16 v36 l-24,-16 h-40 Z", c, 3) + C(-8, -44, 3, c, 1.5) + C(0, -44, 3, c, 1.5) + T(34, -58, "♪", 16, "#fff")

def _balloon(c=None, **k):
    c = c or "#e0533b"
    return P("M0,-34 Q-4,-18 4,-8 Q-4,0 0,6", "none", 1.5) + E(0, -58, 20, 24, c, 3) + P("M-3,-34 h6 l-3,4 Z", c, 1.5) + E(-7, -66, 4, 7, "#fff", 0, extra='opacity=".6"')

def _gift(c=None, **k):
    c = c or "#e0533b"
    return f'<rect x="-28" y="-44" width="56" height="44" fill="{c}" stroke="{INK}" stroke-width="3"/>' + L(0, -44, 0, 0, "#ffd23f", 7) + L(-28, -24, 28, -24, "#ffd23f", 7) + P("M0,-44 q-16,-16 -18,-4 q2,6 18,4 q16,2 18,-4 q-2,-12 -18,4", "#ffd23f", 2)

def _letter(c=None, **k):
    return f'<rect x="-32" y="-46" width="64" height="40" fill="{c or "#fff6c9"}" stroke="{INK}" stroke-width="3"/>' + P("M-32,-46 L0,-22 L32,-46", "none", 2.5) + C(0, -24, 6, "#c0262d", 1.5)

def _card(c=None, **k):
    return f'<rect x="-22" y="-66" width="44" height="62" rx="5" fill="#fff" stroke="{INK}" stroke-width="3"/>' + T(-12, -50, "A", 12, c or "#c0262d") + P("M0,-44 q-10,-10 -10,2 q0,8 10,16 q10,-8 10,-16 q0,-12 -10,-2 Z", c or "#c0262d", 1.5)

def _puzzle(c=None, **k):
    c = c or "#3f9b4a"
    return P("M-26,-6 V-30 q-10,-4 -10,-10 q0,-8 10,-6 V-58 H-6 q-4,-10 6,-12 q10,2 6,12 H26 V-34 q10,-2 10,6 q0,8 -10,6 V-6 Z", c, 3)

def _dice(c=None, **k):
    return f'<rect x="-26" y="-54" width="50" height="50" rx="8" fill="{c or "#fff"}" stroke="{INK}" stroke-width="3"/>' + "".join(C(x, y, 4, INK, 0) for x, y in [(-14, -42), (0, -29), (14, -16), (14, -42), (-14, -16)])

def _pizza(c=None, **k):
    return P("M-34,-8 L0,-74 L34,-8 Q0,4 -34,-8 Z", "#f4c542", 3) + P("M-34,-8 Q0,4 34,-8 L30,-14 Q0,-4 -30,-14 Z", "#d9a05a", 2) + "".join(C(x, y, 5, "#c0262d", 1.5) for x, y in [(-8, -30), (8, -40), (0, -18), (12, -20)])

def _apple(c=None, expr="happy", **k):
    return P("M0,-56 Q-30,-66 -28,-34 Q-24,-2 0,-6 Q24,-2 28,-34 Q30,-66 0,-56 Z", c or "#e0533b", 3) + L(0, -56, 2, -68, "#6b4a2a", 3) + P("M2,-64 q12,-10 18,0 q-10,6 -18,0 Z", "#3f9b4a", 2) + face(0, -34, 0.7, expr)

def _banana(c=None, expr="happy", **k):
    return P("M-36,-40 Q-30,-6 6,-4 Q34,-6 40,-30 Q30,-16 6,-16 Q-24,-16 -30,-44 Z", c or "#ffd23f", 3) + face(4, -12, 0.45, expr)

def _carrot(c=None, **k):
    return P("M-10,-60 L10,-60 L0,0 Z", c or "#f39c3d", 3) + P("M0,-60 l-10,-16 M0,-60 l0,-18 M0,-60 l10,-16", "none", 4, "#3f9b4a")

def _popsicle(c=None, expr="happy", **k):
    return f'<rect x="-3" y="-20" width="6" height="20" fill="#d9a05a" stroke="{INK}" stroke-width="2"/>' + P("M-16,-20 V-66 Q0,-80 16,-66 V-20 Z", c or "#ff5fa2", 3) + P("M-16,-50 Q0,-44 16,-50 M-16,-34 Q0,-28 16,-34", "none", 2.5, "#fff") + face(0, -58, 0.5, expr)

def _icecream(c=None, **k):
    return P("M-16,-40 L0,0 L16,-40 Z", "#d9a05a", 3) + C(0, -48, 16, c or "#ff9fc4", 3) + C(0, -66, 11, "#fff6c9", 2.5) + C(0, -80, 4, "#e0533b", 1.5)

def _cheese(c=None, **k):
    return P("M-34,-4 L-34,-34 L30,-50 L34,-4 Z", c or "#ffd23f", 3) + "".join(C(x, y, r, shade(c or "#ffd23f", 0.75), 0) for x, y, r in [(-20, -22, 5), (6, -18, 4), (18, -34, 3)])

def _pot(c=None, **k):
    return P("M-32,-44 H32 V-12 Q32,0 20,0 H-20 Q-32,0 -32,-12 Z", c or "#6b6b78", 3) + L(-40, -40, -32, -40, INK, 4) + L(32, -40, 40, -40, INK, 4) + "".join(P(f"M{x},-50 q6,-8 0,-16", "none", 2, "#ddd") for x in (-10, 10))

def _cup(c=None, **k):
    return P("M-22,-44 H22 L18,-6 Q0,2 -18,-6 Z", c or "#f7f3e8", 3) + P("M22,-36 q14,0 12,12 q-2,8 -14,6", "none", 3) + E(0, -44, 22, 5, "#c8864a", 2)

def _bottle(c=None, **k):
    c = c or "#9cff57"
    return P("M-6,-70 H6 V-56 Q20,-50 20,-36 V-4 H-20 V-36 Q-20,-50 -6,-56 Z", c, 3, extra='opacity=".95"') + f'<rect x="-7" y="-78" width="14" height="8" fill="#8a5a2b" stroke="{INK}" stroke-width="2"/>' + C(-6, -24, 4, "#fff", 0, extra='opacity=".6"')

def _jar(c=None, **k):
    return props.jar(0, 0, 60, c or "#c86f3a")

def _bucket(c=None, **k):
    return P("M-26,-50 H26 L20,0 H-20 Z", c or "#9aa8b8", 3) + P("M-26,-50 Q0,-82 26,-50", "none", 2.5) + E(0, -50, 26, 5, "#63aee0", 2)

def _ladder(c=None, **k):
    c = c or "#a0703a"
    return L(-16, 0, -12, -84, c, 5) + L(16, 0, 12, -84, c, 5) + "".join(L(-15, y, 15, y, c, 4) for y in (-12, -30, -48, -66))

def _hammer(c=None, **k):
    return L(0, 0, 0, -60, "#8a5a2b", 7) + f'<rect x="-22" y="-78" width="44" height="20" rx="3" fill="{c or "#6b6b78"}" stroke="{INK}" stroke-width="3"/>'

def _umbrella(c=None, **k):
    return P("M-40,-50 Q0,-96 40,-50 Q30,-58 20,-50 Q10,-58 0,-50 Q-10,-58 -20,-50 Q-30,-58 -40,-50 Z", c or "#e0533b", 3) + L(0, -50, 0, -8, INK, 3) + P("M0,-8 q0,8 -8,6", "none", 3)

def _firework(c=None, **k):
    c = c or "#ffd23f"
    return "".join(L(0, -44, 36 * math.cos(a), -44 + 36 * math.sin(a), [c, "#ff5fa2", "#00e5ff"][j % 3], 3) + C(38 * math.cos(a), -44 + 38 * math.sin(a), 3, "#fff", 0) for j, a in enumerate([k2 * math.pi / 6 for k2 in range(12)]))

def _bomb(c=None, **k):
    return C(0, -28, 26, c or "#23233a", 3) + P("M14,-50 q10,-14 20,-10", "none", 3, "#8a5a2b") + sparkle(36, -62, 8, "#ff9a1a")

def _statue(c=None, expr="happy", **k):
    stone = re.sub(r'fill="#[0-9a-fA-F]{6}"', 'fill="#b8b2a8"', person("man", expr))
    return f'<rect x="-24" y="-12" width="48" height="12" fill="#9a948a" stroke="{INK}" stroke-width="2.5"/>' + gs(stone, 0, -12, 0.85)

def _snowman(c=None, expr="happy", **k):
    return C(0, -18, 18, "#fff", 3) + C(0, -46, 13, "#fff", 3) + face(0, -48, 0.6, expr) + P("M2,-46 l10,2 l-10,2 Z", "#f39c3d", 1) + f'<rect x="-10" y="-74" width="20" height="14" fill="#23233a" stroke="{INK}" stroke-width="2"/>'

def _unicorn(c=None, expr="happy", **k):
    return quad(c or "#fff", ears="pointy", tail="bushy", mane="#ff8fc0", long_legs=True, expr=expr) + P("M30,-68 l4,-20 l4,20 Z", "#ffd23f", 2)

def _alien(c=None, expr="happy", **k):
    c = c or "#9cff57"
    return E(0, -20, 14, 20, c, 3) + E(0, -52, 22, 18, c, 3) + E(-9, -52, 7, 5, INK, 0) + E(9, -52, 7, 5, INK, 0) + P("M-8,-68 l-8,-14 M8,-68 l8,-14", "none", 2.5) + C(-16, -84, 3, c, 1.5) + C(16, -84, 3, c, 1.5)

def _skeleton(c=None, expr="grin", **k):
    return L(0, -52, 0, -18, "#f7f3e8", 5) + "".join(L(-12, y, 12, y, "#f7f3e8", 3) for y in (-46, -38, -30)) + P("M0,-18 l-10,18 M0,-18 l10,18", "none", 4, "#f7f3e8") + C(0, -64, 13, "#f7f3e8", 3) + C(-5, -66, 3.5, INK, 0) + C(5, -66, 3.5, INK, 0) + P("M-5,-56 h10", "none", 2)

def _mummy(c=None, expr="sleepy", **k):
    return P("M-16,0 V-56 Q-16,-78 0,-78 Q16,-78 16,-56 V0 Z", "#efe2c0", 3) + "".join(L(-16, y, 16, y + 4, "#b9a88c", 2) for y in (-60, -46, -32, -18)) + C(-5, -62, 3, INK, 0) + C(5, -62, 3, INK, 0)

def _vampire(c=None, expr="mean", **k):
    return P("M-30,0 L-20,-60 L0,-40 L20,-60 L30,0 Z", "#6b1a2a", 3) + person("man", expr, "#23233a")

def _bathtub(c=None, **k):
    return P("M-40,-40 H40 V-16 Q40,-4 26,-4 H-26 Q-40,-4 -40,-16 Z", c or "#f7f3e8", 3) + P("M-30,-4 l-4,6 M30,-4 l4,6", "none", 4) + "".join(C(x, -44, r, "#fff", 1.5, "#63aee0") for x, r in [(-20, 7), (0, 9), (18, 6)])

def _bed(c=None, **k):
    return f'<rect x="-40" y="-26" width="80" height="16" fill="{c or "#6b4fa0"}" stroke="{INK}" stroke-width="3"/>' + f'<rect x="-40" y="-50" width="8" height="50" fill="#8a5a2b" stroke="{INK}" stroke-width="2.5"/>' + E(-24, -30, 10, 6, "#fff", 2) + L(34, -10, 34, 0, INK, 4)

def _chair(c=None, **k):
    c = c or "#a0703a"
    return L(-16, 0, -16, -70, c, 5) + L(14, 0, 14, -30, c, 5) + L(-16, -30, 16, -30, c, 7) + L(-16, -52, -16, -70, c, 5) + f'<rect x="-18" y="-72" width="6" height="24" fill="{c}" stroke="{INK}" stroke-width="2"/>'

def _table(c=None, **k):
    c = c or "#a0703a"
    return f'<rect x="-40" y="-44" width="80" height="8" fill="{c}" stroke="{INK}" stroke-width="3"/>' + L(-32, -36, -32, 0, c, 6) + L(32, -36, 32, 0, c, 6)

def _throne(c=None, **k):
    return f'<rect x="-26" y="-80" width="52" height="54" rx="8" fill="{c or "#6b2fa0"}" stroke="{INK}" stroke-width="3"/><rect x="-32" y="-30" width="64" height="16" fill="#d9a441" stroke="{INK}" stroke-width="3"/>' + L(-26, -14, -26, 0, INK, 5) + L(26, -14, 26, 0, INK, 5) + C(0, -84, 6, "#f4c542", 2)

def _tower(c=None, **k):
    return props.tower(0, 0, 70, 30, c or "#e8d6b0")

def _wall(c=None, **k):
    c = c or "#c9b89a"
    return f'<rect x="-44" y="-50" width="88" height="50" fill="{c}" stroke="{INK}" stroke-width="3"/>' + "".join(L(-44, y, 44, y, shade(c, 0.75), 2) for y in (-38, -26, -14)) + "".join(L(x + (8 if (j % 2) else 0), -50 + 12 * j, x + (8 if (j % 2) else 0), -38 + 12 * j, shade(c, 0.75), 2) for j in range(4) for x in (-28, -4, 20))

def _rock(c=None, expr=None, **k):
    return P("M-36,0 Q-40,-30 -14,-40 Q10,-50 30,-30 Q42,-12 36,0 Z", c or "#9a9aa8", 3) + (face(0, -22, 0.7, expr) if expr else P("M-14,-28 l10,4", "none", 2, "#6b6b78"))

def _crystal(c=None, **k):
    c = c or "#bfefff"
    return P("M-12,0 L-20,-40 L-6,-70 L8,-40 Z", c, 3) + P("M4,0 L10,-50 L22,-30 L18,0 Z", shade(c, 0.85), 3) + P("M-6,-70 L-6,-40", "none", 1.5, "#fff")

def _potion(c=None, **k):
    c = c or "#b48cff"
    return E(0, -24, 22, 22, c, 3) + f'<rect x="-6" y="-58" width="12" height="16" fill="#dff3ff" stroke="{INK}" stroke-width="2.5"/>' + E(0, -60, 8, 3, "#8a5a2b", 2) + "".join(C(x, y, 3, "#fff", 0, extra='opacity=".7"') for x, y in [(-8, -28), (6, -18), (2, -34)])

def _feather(c=None, **k):
    return P("M-20,0 Q-20,-50 20,-80 Q16,-30 -20,0 Z", c or "#f7f3e8", 3) + P("M-20,0 Q0,-40 18,-76", "none", 2)

def _heart(c=None, expr="happy", **k):
    return P("M0,-6 Q-40,-34 -30,-60 Q-18,-80 0,-60 Q18,-80 30,-60 Q40,-34 0,-6 Z", c or "#e0533b", 3) + face(0, -44, 0.7, expr)

def _brain(c=None, **k):
    return P("M-30,-20 Q-40,-50 -16,-60 Q0,-72 16,-60 Q40,-50 30,-20 Q20,-6 0,-10 Q-20,-6 -30,-20 Z", c or "#ff9fc4", 3) + P("M0,-66 V-12 M-18,-52 q8,6 0,14 M18,-50 q-8,6 0,14", "none", 2)

def _eye(c=None, **k):
    return E(0, -34, 34, 22, "#fff", 3) + C(0, -34, 14, c or "#2f6db5", 2) + C(0, -34, 7, INK, 0) + C(4, -38, 3, "#fff", 0)

def _hand(c=None, **k):
    c = c or "#e8b98d"
    return P("M-18,0 V-40 M-18,-40 Q-18,-60 -10,-60 V-44 M-10,-60 Q-6,-74 2,-66 V-44 M2,-66 Q8,-74 12,-62 V-40 M12,-60 Q18,-66 20,-54 V-30 Q20,0 0,0 Z", c, 3)

def _nose(c=None, **k):
    return P("M-10,-70 Q-6,-30 -24,-14 Q-10,0 0,-8 Q10,0 24,-14 Q6,-30 10,-70 Z", c or "#e8b98d", 3) + E(-8, -12, 4, 3, "#7a3a24", 0) + E(8, -12, 4, 3, "#7a3a24", 0)

def _gear(c=None, **k):
    return props.gear(0, -36, 30, c or "#b8862b") + C(0, -36, 9, "#2a1450", 2)

def _machine(c=None, expr="happy", **k):
    c = c or "#b8862b"
    return f'<rect x="-36" y="-54" width="72" height="50" rx="4" fill="{c}" stroke="{INK}" stroke-width="3"/>' + props.gear(-16, -60, 14, "#d9a441") + props.gear(14, -64, 10, "#c9ccd8") + C(-16, -30, 8, "#63aee0", 2.5) + C(14, -30, 8, "#63aee0", 2.5) + L(-36, -14, 36, -14, INK, 2) + C(-24, -4, 5, "#444", 2) + C(24, -4, 5, "#444", 2)

def _clay(c=None, **k):
    return P("M-30,0 Q-36,-30 -10,-40 Q0,-60 16,-40 Q36,-30 30,0 Z", c or "#c8773a", 3) + P("M-10,-26 q10,-6 20,0", "none", 2, shade(c or "#c8773a", 0.7))

def _pillow(c=None, **k):
    return P("M-36,-8 Q-40,-30 -34,-44 Q0,-52 34,-44 Q40,-30 36,-8 Q0,0 -36,-8 Z", c or "#ff9fc4", 3) + P("M-34,-44 l-6,-6 M34,-44 l6,-6 M-36,-8 l-6,6 M36,-8 l6,6", "none", 2.5)

def _skirt(c=None, **k):
    return P("M-14,-60 H14 L36,-4 Q0,6 -36,-4 Z", c or "#e0533b", 3) + P("M-24,-30 L-28,-4 M0,-60 V-2 M24,-30 L28,-4", "none", 2, shade(c or "#e0533b", 0.7))

def _hat(c=None, **k):
    return f'<rect x="-16" y="-50" width="32" height="40" fill="{c or "#23233a"}" stroke="{INK}" stroke-width="3"/>' + L(-30, -10, 30, -10, INK, 6) + L(-16, -18, 16, -18, "#c0262d", 5)

def _glasses(c=None, **k):
    return C(-18, -30, 14, "#bfefff", 3) + C(18, -30, 14, "#bfefff", 3) + L(-4, -30, 4, -30, INK, 3)

def _flag(c=None, **k):
    return L(-20, 0, -20, -84, "#8a5a2b", 4) + P("M-20,-84 Q0,-94 20,-82 Q34,-74 40,-80 V-50 Q30,-44 20,-52 Q0,-62 -20,-54 Z", c or "#e0533b", 2.5)

def _torch(c=None, **k):
    return L(0, 0, 0, -44, "#8a5a2b", 7) + P("M-8,-44 h16 l-2,6 h-12 Z", "#6b6b78", 2) + P("M0,-84 Q-16,-62 -8,-48 H8 Q16,-62 0,-84 Z", "#ff9a1a", 2) + P("M0,-70 Q-6,-58 -2,-50 H2 Q6,-58 0,-70 Z", "#ffe066", 0)

def _candle(c=None, **k):
    return f'<rect x="-10" y="-50" width="20" height="50" fill="{c or "#f7f3e8"}" stroke="{INK}" stroke-width="3"/>' + L(0, -50, 0, -56, INK, 2) + P("M0,-74 Q-8,-62 -4,-56 H4 Q8,-62 0,-74 Z", "#ff9a1a", 1.5)

def _tent(c=None, **k):
    return props.tent(-40, 0, 80, c or "#e0533b", "#f4c542")

def _kite(c=None, **k):
    return props.kite(0, -58, c or "#e0533b", 0.9)

def _cage(c=None, **k):
    return props.cage(-24, 0, 48, 64, c or "#f4c542")

def _chest(c=None, **k):
    c = c or "#8a5a2b"
    return f'<rect x="-34" y="-36" width="68" height="36" fill="{c}" stroke="{INK}" stroke-width="3"/>' + P("M-34,-36 Q0,-62 34,-36 Z", shade(c, 1.2), 3) + f'<rect x="-6" y="-42" width="12" height="14" fill="#f4c542" stroke="{INK}" stroke-width="2"/>' + L(-34, -18, 34, -18, "#f4c542", 3)

def _map(c=None, **k):
    return P("M-36,-60 L-12,-66 L12,-58 L36,-64 V-8 L12,-2 L-12,-10 L-36,-4 Z", c or "#efe2c0", 3) + L(-12, -66, -12, -10, "#9a8a6a", 1.5) + L(12, -58, 12, -2, "#9a8a6a", 1.5) + P("M-26,-44 q14,-4 20,8 q10,12 22,4", "none", 2.5, "#c0262d", extra='stroke-dasharray="4 4"') + T(20, -34, "X", 12, "#c0262d")

def _compass(c=None, **k):
    return C(0, -34, 30, c or "#d9a441", 3) + C(0, -34, 22, "#fff6c9", 2) + P("M0,-54 L6,-34 L0,-14 L-6,-34 Z", "#c0262d", 1.5) + T(0, -58, "N", 9)

def _hourglass(c=None, **k):
    return f'<rect x="-22" y="-78" width="44" height="8" fill="#8a5a2b" stroke="{INK}" stroke-width="2"/><rect x="-22" y="-8" width="44" height="8" fill="#8a5a2b" stroke="{INK}" stroke-width="2"/>' + P("M-16,-70 H16 Q16,-50 2,-40 Q16,-30 16,-8 H-16 Q-16,-30 -2,-40 Q-16,-50 -16,-70 Z", "#dff3ff", 2.5) + P("M-10,-8 Q0,-24 10,-8 Z M-8,-64 H8 Q6,-54 0,-48 Q-6,-54 -8,-64 Z", c or "#f4c542", 0)

def _scales(c=None, **k):
    c = c or "#d9a441"
    return L(0, -4, 0, -70, c, 5) + L(-34, -64, 34, -64, c, 4) + P("M-44,-40 L-34,-64 L-24,-40 Z M24,-40 L34,-64 L44,-40 Z", "none", 1.5) + E(-34, -40, 12, 4, c, 2.5) + E(34, -40, 12, 4, c, 2.5) + L(-16, -2, 16, -2, c, 6)

def _trophy(c=None, **k):
    c = c or "#f4c542"
    return P("M-24,-74 H24 Q24,-40 0,-34 Q-24,-40 -24,-74 Z", c, 3) + P("M-24,-68 q-14,0 -12,12 q2,10 14,8 M24,-68 q14,0 12,12 q-2,10 -14,8", "none", 3) + L(0, -34, 0, -14, c, 6) + f'<rect x="-16" y="-14" width="32" height="12" fill="{shade(c,0.8)}" stroke="{INK}" stroke-width="2.5"/>'

def _medal(c=None, **k):
    return P("M-12,-80 L0,-52 L12,-80", "none", 6, "#2f6db5") + C(0, -34, 20, c or "#f4c542", 3) + T(0, -27, "1", 18, shade(c or "#f4c542", 0.55))

def _lightbulb(c=None, **k):
    return f'<circle cx="0" cy="-50" r="34" fill="#ffe066" opacity=".3"/>' + C(0, -50, 22, c or "#fff6a0", 3) + f'<rect x="-10" y="-30" width="20" height="16" fill="#9aa8b8" stroke="{INK}" stroke-width="2.5"/>' + P("M-6,-44 l6,-8 l6,8", "none", 2)

def _pencil(c=None, **k):
    return P("M-6,-80 H6 V-16 L0,0 L-6,-16 Z", c or "#ffd23f", 3) + P("M-6,-16 L0,0 L6,-16 Z", "#f3d9a0", 2) + f'<rect x="-6" y="-88" width="12" height="8" fill="#ff8fc0" stroke="{INK}" stroke-width="2"/>'

def _paintbrush(c=None, **k):
    return L(0, -86, 0, -30, "#a0703a", 6) + f'<rect x="-6" y="-32" width="12" height="10" fill="#c9ccd8" stroke="{INK}" stroke-width="2"/>' + P("M-7,-22 Q0,4 7,-22 Z", c or "#e0533b", 2)

def _painting(c=None, **k):
    return f'<rect x="-38" y="-70" width="76" height="58" fill="#d9a441" stroke="{INK}" stroke-width="3"/><rect x="-30" y="-62" width="60" height="42" fill="#9ad0ff" stroke="{INK}" stroke-width="2"/>' + P("M-30,-24 L-12,-44 L2,-30 L14,-42 L30,-24 Z", "#3f9b4a", 1.5) + C(18, -52, 5, "#ffd23f", 0)

def _paint(c=None, **k):
    return _bucket(c or "#e0533b") + P("M-26,-50 q-4,20 -2,30 M-10,-50 q-2,10 0,18", "none", 5, c or "#e0533b")

def _sandwich(c=None, **k):
    return P("M-36,-14 Q0,-6 36,-14 L36,-4 Q0,4 -36,-4 Z", "#d9a05a", 2.5) + P("M-38,-20 Q0,-12 38,-20", "none", 5, "#3f9b4a") + P("M-36,-24 Q0,-16 36,-24", "none", 4, "#e0533b") + P("M-36,-28 Q-34,-50 0,-50 Q34,-50 36,-28 Q0,-20 -36,-28 Z", "#d9a05a", 2.5)

def _soup(c=None, **k):
    return P("M-36,-30 H36 Q34,0 0,0 Q-34,0 -36,-30 Z", c or "#f7f3e8", 3) + E(0, -30, 36, 7, "#e0a030", 2) + "".join(P(f"M{x},-40 q6,-8 0,-16", "none", 2, "#ddd") for x in (-12, 8))

def _broom(c=None, **k):
    return L(-4, -84, 4, -26, "#a0703a", 5) + P("M-12,-28 H16 L22,0 H-18 Z", c or "#e0c28a", 2.5) + "".join(L(x, -24, x * 1.2, 0, "#b8925a", 1.5) for x in (-10, -2, 6, 14))

def _rope(c=None, **k):
    return props.rope_coil(0, 0, 0.7)

def _chain(c=None, **k):
    return "".join(E(-30 + j * 15, -30, 9, 6, "none", 4, c or "#9aa8b8") for j in range(5))

def _lock(c=None, **k):
    return P("M-14,-44 V-60 Q-14,-76 0,-76 Q14,-76 14,-60 V-44", "none", 6, "#9aa8b8") + f'<rect x="-24" y="-46" width="48" height="42" rx="5" fill="{c or "#d9a441"}" stroke="{INK}" stroke-width="3"/>' + C(0, -30, 5, INK, 0) + L(0, -30, 0, -18, INK, 3)

def _box(c=None, **k):
    c = c or "#c8a060"
    return P("M-32,-44 L0,-58 L32,-44 L0,-30 Z", shade(c, 1.2), 3) + P("M-32,-44 V-8 L0,6 V-30 Z", c, 3) + P("M32,-44 V-8 L0,6 V-30 Z", shade(c, 0.8), 3)

def _fan(c=None, **k):
    c = c or "#e0533b"
    return "".join(P(f"M0,-8 L{40*math.cos(a):.1f},{-8+40*math.sin(a):.1f} L{40*math.cos(a+0.26):.1f},{-8+40*math.sin(a+0.26):.1f} Z", c if j % 2 else shade(c, 1.3), 2) for j, a in enumerate([math.radians(d) for d in range(-165, -15, 15)]))

def _wave(c=None, **k):
    c = c or "#2f6db5"
    return P("M-44,0 Q-40,-60 0,-72 Q30,-76 36,-50 Q20,-60 10,-44 Q24,-40 20,-24 Q40,-10 44,0 Z", c, 3) + P("M0,-72 q20,-6 30,6", "none", 3, "#fff")

def _river(c=None, **k):
    return P("M-44,-4 Q-20,-24 0,-12 Q20,0 44,-22 V-8 Q20,12 0,2 Q-20,-10 -44,10 Z", c or "#63aee0", 3)

def _island(c=None, **k):
    return E(0, -8, 42, 12, "#e8c77d", 3) + props.palm(0, -12, 60)

def _pool(c=None, **k):
    return E(0, -16, 42, 14, c or "#63aee0", 3) + E(0, -16, 32, 8, "#bfefff", 0, extra='opacity=".6"') + L(30, -16, 34, -50, "#9aa8b8", 3) + L(40, -16, 44, -50, "#9aa8b8", 3)

def _desert(c=None, **k):
    return props.dune(-44, 0, 60, 40) + props.dune(-10, 0, 56, 30, "#e0b865")

def _city(c=None, **k):
    return "".join(f'<rect x="{x}" y="{-h}" width="16" height="{h}" fill="{c or "#6b4fa0"}" stroke="{INK}" stroke-width="2.5"/>' + f'<rect x="{x+5}" y="{-h+8}" width="6" height="6" fill="#ffd23f"/>' for x, h in [(-40, 46), (-22, 70), (-4, 56), (14, 80), (32, 50)])

def _lab(c=None, **k):
    return _table("#6b6b78") + gs(_bottle("#9cff57"), -20, -44, 0.5) + gs(_potion(), 16, -44, 0.55)

def _gym(c=None, **k):
    return L(-40, -40, 40, -40, INK, 5) + "".join(f'<rect x="{x}" y="-58" width="10" height="36" rx="3" fill="#555" stroke="{INK}" stroke-width="2"/>' for x in (-42, -30, 20, 32)) + E(0, -6, 30, 6, "#e0533b", 2)

def _shop(c=None, **k):
    return props.stall(-40, 0, c or "#e0533b", "#f4c542", 80)

def _party(c=None, **k):
    return gs(_balloon("#e0533b"), -20, 0, 0.8) + gs(_balloon("#2f6db5"), 0, -8, 0.8) + gs(_balloon("#ffd23f"), 20, 0, 0.8) + "".join(C(x, y, 2.5, col, 0) for x, y, col in [(-30, -10, "#ff5fa2"), (30, -16, "#00e5ff"), (8, -4, "#9cff57")])

def _note(c=None, **k):
    return P("M-6,-8 V-70 L26,-78 V-18", "none", 5, c or INK) + E(-14, -8, 10, 7, c or INK, 0) + E(18, -18, 10, 7, c or INK, 0)

def _song(c=None, **k):
    return _note(c) + T(-30, -50, "♪", 18, "#f4c542")

def _web(c=None, **k):
    return "".join(L(0, -40, 40 * math.cos(a), -40 + 40 * math.sin(a), "#dfe6f0", 1.5) for a in [j * math.pi / 4 for j in range(8)]) + "".join(C(0, -40, r, "none", 1.5, "#dfe6f0") for r in (12, 24, 36))

def _bubble(c=None, **k):
    return C(0, -40, 34, "#dff3ff", 2.5, "#63aee0", 'fill-opacity=".35"') + P("M-18,-58 q8,-10 20,-10", "none", 3, "#fff")

def _fire(c=None, **k):
    return P("M-26,0 Q-34,-40 -10,-60 Q-12,-40 0,-36 Q-4,-60 14,-80 Q14,-50 28,-40 Q36,-16 26,0 Z", c or "#ff7a1a", 3) + P("M-12,0 Q-14,-22 0,-30 Q4,-16 14,-12 Q16,-4 12,0 Z", "#ffe066", 0)

def _ice(c=None, **k):
    return _crystal(c or "#dff3ff")

def _lightning(c=None, **k):
    return P("M6,-86 L-18,-36 H0 L-10,0 L22,-50 H4 Z", c or "#ffe066", 3)

def _rainbow(c=None, **k):
    return "".join(P(f"M{-44+j*5},0 A{44-j*5},{44-j*5} 0 0 1 {44-j*5},0", "none", 5, col) for j, col in enumerate(["#e0533b", "#f39c3d", "#ffd23f", "#3f9b4a", "#2f6db5", "#8a4fc8"]))

# ---- library growth · batch 1 (chapters 1-10)
def _crypt(c=None, **k):
    c = c or "#8a8a95"
    return (f'<rect x="-34" y="-50" width="68" height="50" fill="{c}" stroke="{INK}" stroke-width="3"/>' + P("M-40,-50 L0,-72 L40,-50 Z", shade(c, 0.8), 3)
            + P("M-12,0 V-24 Q0,-38 12,-24 V0 Z", "#1b1b2f", 2.5) + T(-22, -30, "?", 14, "#b48cff") + T(24, -34, "?", 12, "#b48cff"))

def _tile(c=None, **k):
    c = c or "#e0c28a"
    return "".join(f'<rect x="{x}" y="{y}" width="22" height="22" fill="{c if (x+y) % 44 else shade(c, 0.8)}" stroke="{INK}" stroke-width="2.5" transform="rotate({r} {x+11} {y+11})"/>'
                   for x, y, r in [(-34, -24, -8), (-10, -26, 6), (14, -22, -4), (-22, -50, 12), (4, -48, -10)])

def _jelly(c=None, expr="scared", **k):
    c = c or "#ff5fa2"
    return (E(0, -4, 38, 6, "#f7f3e8", 2.5) + P("M-30,-6 Q-34,-40 -20,-48 Q0,-60 20,-48 Q34,-40 30,-6 Z", c, 3, extra='opacity=".9"')
            + P("M-20,-48 Q-10,-40 0,-50 Q10,-40 20,-48", "none", 2, "#fff") + C(0, -58, 5, "#e0533b", 2) + face(0, -28, 0.7, expr))

def _lever(c=None, **k):
    c = c or "#d9a441"
    return f'<rect x="-30" y="-14" width="60" height="14" fill="#8a5a2b" stroke="{INK}" stroke-width="3"/>' + L(0, -14, 26, -76, c, 7) + C(28, -80, 9, "#e0533b", 3) + C(0, -14, 6, "#6b6b78", 2)

def _screw(c=None, **k):
    c = c or "#c9ccd8"
    return (E(0, -64, 20, 7, c, 3) + L(-8, -66, 8, -62, INK, 2.5) + P("M-9,-60 H9 L2,0 H-2 Z", c, 3)
            + "".join(L(-8 + j * 1.4, -52 + j * 10, 8 - j * 1.4, -48 + j * 10, INK, 1.8) for j in range(5)))

def _twins(c=None, expr="skeptic", **k):
    return gs(person("kid", expr, c), -18, 0, 0.9) + gs(person("kid", expr, c), 18, 0, 0.9, flip=True)

def _number(c=None, expr="happy", **k):
    c = c or "#2f6db5"
    return P("M-6,0 V-58 L-20,-48 V-62 L2,-80 H12 V0 Z", c, 3) + f'<rect x="-22" y="-10" width="46" height="10" fill="{c}" stroke="{INK}" stroke-width="3"/>' + face(3, -40, 0.55, expr)

def _vending(c=None, expr="grin", **k):
    c = c or "#c0262d"
    return (f'<rect x="-30" y="-84" width="60" height="84" rx="4" fill="{c}" stroke="{INK}" stroke-width="3"/><rect x="-22" y="-74" width="30" height="46" fill="#bfefff" stroke="{INK}" stroke-width="2"/>'
            + "".join(f'<rect x="{-20+dx}" y="{-70+dy}" width="8" height="8" fill="{col}"/>' for dx, dy, col in [(2, 2, "#ffd23f"), (14, 2, "#9cff57"), (2, 18, "#ff5fa2"), (14, 18, "#00e5ff"), (2, 32, "#f39c3d")])
            + f'<rect x="14" y="-70" width="10" height="4" fill="{INK}"/>' + C(19, -54, 4, "#f4c542", 1.5) + f'<rect x="-20" y="-20" width="40" height="10" fill="{INK}"/>')

def _ear(c=None, **k):
    c = c or "#e8b98d"
    return P("M-10,-80 Q30,-86 30,-46 Q30,-20 10,-12 Q4,0 -10,-4 Q-20,-8 -14,-18 Q0,-26 4,-40 Q6,-56 -8,-58 Q-20,-58 -22,-50 Q-30,-74 -10,-80 Z", c, 3) + P("M0,-66 Q18,-66 18,-48 Q18,-34 6,-30", "none", 2.5, shade(c, 0.7))

def _sock(c=None, **k):
    c = c or "#e0533b"
    return P("M-10,-80 H14 V-30 Q14,-16 26,-12 Q40,-8 36,0 H-4 Q-14,0 -12,-14 Z", c, 3) + "".join(L(-10, y, 14, y, "#fff", 4) for y in (-72, -60)) + P("M22,-12 q12,0 14,10", "none", 2, shade(c, 0.7))

def _bowl(c=None, expr="grin", **k):
    c = c or "#2f6db5"
    return E(0, -40, 36, 9, "#f3d9a0", 3) + "".join(C(x, y, 5, col, 1.5) for x, y, col in [(-20, -44, "#f39c3d"), (-6, -46, "#ffd23f"), (10, -44, "#e0533b"), (22, -42, "#f39c3d")]) + P("M-36,-40 Q-34,0 0,0 Q34,0 36,-40 Z", c, 3) + face(0, -22, 0.7, expr)

def _cart(c=None, **k):
    c = c or "#a0703a"
    return P("M-40,-50 H30 L24,-16 H-34 Z", c, 3) + L(30, -50, 42, -62, INK, 4) + C(-24, -8, 9, "#555", 2.5) + C(14, -8, 9, "#555", 2.5) + "".join(L(x, -48, x - 2, -18, shade(c, 0.7), 2) for x in (-20, -4, 12))

def _hose(c=None, **k):
    c = c or "#3f9b4a"
    return (P("M-40,-6 Q-40,-40 -10,-40 Q20,-40 20,-60", "none", 11, INK) + P("M-40,-6 Q-40,-40 -10,-40 Q20,-40 20,-60", "none", 7, c)
            + f'<rect x="12" y="-78" width="16" height="18" rx="3" fill="#c9ccd8" stroke="{INK}" stroke-width="2.5"/>'
            + "".join(P(f"M20,-80 q{dx},-14 {dx*2},-4", "none", 2.5, "#63aee0") for dx in (-10, 0, 10)))

def _submarine(c=None, **k):
    c = c or "#ffd23f"
    return (E(0, -26, 42, 18, c, 3) + f'<rect x="-10" y="-58" width="22" height="18" rx="4" fill="{c}" stroke="{INK}" stroke-width="3"/>' + L(6, -58, 6, -70, INK, 3)
            + L(6, -70, 16, -70, INK, 3) + "".join(C(x, -26, 6, "#63aee0", 2.5) for x in (-22, -4, 14)) + P("M40,-26 l10,-10 v20 Z", shade(c, 0.8), 2.5))

def _buoy(c=None, **k):
    return E(0, -10, 34, 10, c or "#e0533b", 3) + P("M-26,-12 L-12,-50 H12 L26,-12", "#f7f3e8", 3) + L(-18, -30, 18, -30, "#e0533b", 5) + C(0, -58, 8, "#ffd23f", 2.5)

def _pearl(c=None, expr=None, **k):
    return C(0, -30, 28, c or "#f7f3e8", 3) + C(-8, -40, 8, "#fff", 0, extra='opacity=".8"') + (face(4, -26, 0.8, expr) if expr and expr != "happy" else "")

def _hole(c=None, **k):
    return E(0, -16, 44, 16, c or "#0b0b18", 3) + E(0, -14, 34, 10, "#000", 0) + T(0, -40, "HISS", 13, "#b48cff", extra=f'stroke="{INK}" stroke-width="2" paint-order="stroke"')

def _nut(c=None, expr="happy", **k):
    c = c or "#c8773a"
    return P("M-24,-40 Q-26,-6 0,0 Q26,-6 24,-40 Z", c, 3) + P("M-30,-40 Q-28,-62 0,-62 Q28,-62 30,-40 Z", shade(c, 0.7), 3) + L(0, -62, 2, -72, "#6b4a2a", 3) + face(0, -24, 0.6, expr)

def _chariot(c=None, **k):
    c = c or "#d9a441"
    return P("M-30,-56 H20 Q30,-56 30,-40 V-20 H-30 Z", c, 3) + C(-8, -16, 16, "none", 4, "#8a5a2b") + L(-24, -16, 8, -16, "#8a5a2b", 2) + L(-8, -32, -8, 0, "#8a5a2b", 2) + L(30, -30, 48, -30, "#8a5a2b", 4)

def _rollercoaster(c=None, **k):
    c = c or "#e0533b"
    return (P("M-44,0 Q-30,-80 -8,-40 Q8,-10 20,-60 Q30,-90 44,-20", "none", 5, c) + "".join(L(x, 0, x, y, "#8a5a2b", 2.5) for x, y in [(-36, -40), (-20, -52), (6, -22), (26, -58), (40, -34)])
            + f'<rect x="12" y="-74" width="18" height="10" rx="3" fill="#2f6db5" stroke="{INK}" stroke-width="2" transform="rotate(-50 20 -68)"/>')

def _pepper(c=None, expr="angry", **k):
    c = c or "#e0533b"
    return P("M-6,-66 Q-22,-60 -20,-30 Q-16,-4 4,0 Q10,-20 12,-40 Q14,-62 -6,-66 Z", c, 3) + P("M-6,-66 q2,-10 10,-12", "none", 4, "#3f9b4a") + face(-3, -40, 0.55, expr) + P("M18,-60 q8,-6 6,-14 M22,-48 q10,-2 10,-10", "none", 2, "#f39c3d")

def _smoke(c=None, expr="crying", **k):
    c = c or "#8a94a6"
    return "".join(C(x, y, r, c, 2.5, extra='opacity=".92"') for x, y, r in [(-20, -20, 16), (4, -30, 20), (22, -18, 14), (-6, -52, 16), (14, -60, 12)]) + face(2, -32, 0.7, expr)

def _waterfall(c=None, **k):
    return (f'<rect x="-40" y="-84" width="80" height="12" fill="#8a7a6a" stroke="{INK}" stroke-width="2.5"/>' + P("M-30,-72 H30 L36,0 H-36 Z", c or "#63aee0", 3)
            + "".join(L(x, -70, x * 1.2, -4, "#fff", 2, 'opacity=".7"') for x in (-20, -6, 8, 22)) + E(0, -2, 44, 6, "#bfefff", 2))

def _calendar(c=None, **k):
    return (f'<rect x="-30" y="-70" width="60" height="64" rx="4" fill="#fff" stroke="{INK}" stroke-width="3"/><rect x="-30" y="-70" width="60" height="16" rx="4" fill="{c or "#c0262d"}" stroke="{INK}" stroke-width="3"/>'
            + "".join(f'<rect x="{-24+j%4*13}" y="{-48+j//4*13}" width="9" height="9" fill="#dfe6f0"/>' for j in range(12)) + L(-16, -76, -16, -64, INK, 3) + L(16, -76, 16, -64, INK, 3))

def _tack(c=None, **k):
    c = c or "#e0533b"
    return C(0, -56, 22, c, 3) + E(0, -40, 12, 5, shade(c, 0.7), 2.5) + P("M-2,-36 L0,0 L2,-36 Z", "#c9ccd8", 2) + C(-8, -62, 5, "#fff", 0, extra='opacity=".5"')

def _tuningfork(c=None, **k):
    c = c or "#c9ccd8"
    return (P("M-14,-84 V-40 Q-14,-26 0,-26 Q14,-26 14,-40 V-84", "none", 7, c) + L(0, -26, 0, 0, c, 7)
            + "".join(P(f"M{s*24},-70 q{s*8},10 0,20 M{s*32},-74 q{s*10},14 0,28", "none", 2, "#ffd23f") for s in (-1, 1)))

def _speaker(c=None, **k):
    return (f'<rect x="-26" y="-76" width="52" height="76" rx="4" fill="{c or "#3a3a4a"}" stroke="{INK}" stroke-width="3"/>' + C(0, -22, 16, "#555", 3) + C(0, -22, 6, INK, 0) + C(0, -58, 9, "#555", 2.5)
            + "".join(P(f"M{30+j*8},-50 q8,12 0,26", "none", 2.5, "#ffd23f") for j in range(3)))

def _clam(c=None, expr="angry", **k):
    c = c or "#f3d9c8"
    return P("M-34,-8 Q-34,-40 0,-44 Q34,-40 34,-8 Z", c, 3) + P("M-34,-8 Q0,6 34,-8 Q0,-4 -34,-8 Z", shade(c, 0.85), 3) + "".join(L(0, -8, x, -38, shade(c, 0.7), 1.5) for x in (-22, -10, 10, 22)) + face(0, -26, 0.6, expr)

def _tricycle(c=None, **k):
    c = c or "#e0533b"
    return C(-26, -14, 12, "none", 4, INK) + C(22, -24, 22, "none", 4, INK) + P("M-26,-14 L0,-30 L22,-24 M0,-30 L4,-62 M-8,-64 H16", "none", 5, c) + f'<rect x="-14" y="-38" width="20" height="8" rx="3" fill="{INK}"/>'

def _sign(c=None, **k):
    c = c or "#c0262d"
    pts = " ".join(f"{26*math.cos(math.radians(22.5+45*j)):.1f},{-58+26*math.sin(math.radians(22.5+45*j)):.1f}" for j in range(8))
    return L(0, -34, 0, 0, "#9aa8b8", 6) + f'<polygon points="{pts}" fill="{c}" stroke="{INK}" stroke-width="3"/>' + T(0, -53, "STOP", 12, "#fff", family="Arial,sans-serif", weight="900")

def _tightrope(c=None, **k):
    return L(-44, -60, -44, 0, "#8a5a2b", 5) + L(44, -60, 44, 0, "#8a5a2b", 5) + P("M-44,-58 Q0,-50 44,-58", "none", 2, "#d9c79a") + "".join(gs(_crowd_body(j, None), x, -54, 0.32) for j, x in enumerate((-22, 0, 22)))

LIB_BATCH1 = {"crypt": _crypt, "tomb": _crypt, "tile": _tile, "jelly": _jelly, "lever": _lever, "screw": _screw, "twins": _twins, "twin": _twins,
              "number": _number, "integer": _number, "vending-machine": _vending, "vending": _vending, "ear": _ear, "sock": _sock, "bowl": _bowl,
              "cart": _cart, "hose": _hose, "submarine": _submarine, "sub": _submarine, "buoy": _buoy, "pearl": _pearl, "hole": _hole, "pit": _hole,
              "abyss": _hole, "nut": _nut, "acorn": _nut, "chariot": _chariot, "rollercoaster": _rollercoaster, "roller-coaster": _rollercoaster,
              "pepper": _pepper, "chili": _pepper, "smoke": _smoke, "waterfall": _waterfall, "calendar": _calendar, "tack": _tack, "thumbtack": _tack,
              "fork": _tuningfork, "tuning-fork": _tuningfork, "speaker": _speaker, "loudspeaker": _speaker, "clam": _clam, "oyster": _clam,
              "tricycle": _tricycle, "sign": _sign, "stop-sign": _sign, "tightrope": _tightrope}

# ---- library growth · batch 2 (chapters 11-20)
def _vase(c=None, **k):
    c = c or "#2f6db5"
    return P("M-10,-80 H10 Q8,-66 18,-54 Q34,-30 22,-8 Q14,0 0,0 Q-14,0 -22,-8 Q-34,-30 -18,-54 Q-8,-66 -10,-80 Z", c, 3) + P("M-24,-36 Q0,-26 24,-36", "none", 3, "#f4c542") + P("M-18,-52 Q0,-46 18,-52", "none", 2, "#fff")

def _teddy(c=None, expr="sleepy", **k):
    c = c or "#b8804a"
    return (E(0, -22, 24, 22, c, 3) + E(0, -20, 12, 12, shade(c, 1.4), 0) + C(-22, -8, 9, c, 2.5) + C(22, -8, 9, c, 2.5)
            + C(-18, -66, 8, c, 2.5) + C(18, -66, 8, c, 2.5) + C(0, -54, 18, c, 3) + E(0, -48, 8, 6, shade(c, 1.4), 1.5) + face(0, -56, 0.6, expr))

def _bicycle(c=None, **k):
    c = c or "#2f6db5"
    return C(-26, -18, 16, "none", 4, INK) + C(26, -18, 16, "none", 4, INK) + P("M-26,-18 L-6,-46 L20,-46 L26,-18 M-6,-46 L0,-18 L20,-46 M-10,-54 H2 M20,-46 L24,-58 H32", "none", 4, c)

def _pricetag(c=None, **k):
    c = c or "#f4c542"
    return P("M-30,-70 H14 L34,-44 L14,-18 H-30 Z", c, 3) + C(18, -44, 5, "#2a1450", 2) + T(-8, -38, "$$$", 15, "#c0262d") + P("M22,-44 q20,-10 14,-30", "none", 2)

def _pyramid(c=None, **k):
    c = c or "#e0c28a"
    return P("M-46,0 L0,-78 L46,0 Z", c, 3) + P("M0,-78 L14,0 H46 Z", shade(c, 0.8), 0) + L(0, -78, 14, 0, INK, 2) + "".join(L(-46 + 6 * j, -10 * j, 46 - 6 * j, -10 * j, shade(c, 0.7), 1.2) for j in range(1, 7))

def _vest(c=None, **k):
    c = c or "#c0262d"
    return P("M-26,-72 L-10,-72 L0,-40 L10,-72 L26,-72 L30,-6 H4 L0,-30 L-4,-6 H-30 Z", c, 3) + "".join(C(-6, y, 2.5, "#f4c542", 0) for y in (-26, -16)) + P("M-24,-60 Q-20,-40 -26,-20", "none", 2, "#f4c542")

def _whirlpool(c=None, expr="mean", **k):
    c = c or "#2f6db5"
    return E(0, -20, 44, 20, c, 3) + "".join(P(f"M{-r},-20 A{r},{r*0.45} 0 1 1 {r*0.8},-{20 + r*0.2}", "none", 2.5, "#bfefff") for r in (34, 24, 14)) + E(0, -20, 6, 3, INK, 0) + face(0, -30, 0.6, expr)

def _cannon(c=None, **k):
    c = c or "#3a3a4a"
    return P("M-30,-26 L34,-56 L40,-44 L-24,-12 Z", c, 3) + E(37, -50, 5, 7, INK, 0, extra='transform="rotate(-25 37 -50)"') + C(-14, -12, 14, "#8a5a2b", 3) + C(-14, -12, 4, INK, 0) + "".join(C(50 + j * 10, -62 - j * 6, 4, INK, 0) for j in range(3))

def _maze(c=None, **k):
    c = c or "#3f9b4a"
    return (f'<rect x="-38" y="-72" width="76" height="68" fill="{shade(c,1.5)}" stroke="{INK}" stroke-width="3"/>'
            + P("M-38,-58 H22 M-24,-58 V-30 H8 M22,-44 V-16 H-24 M-10,-44 H8 V-30 M-38,-16 H-24 M22,-30 H38", "none", 5, c))

def _tray(c=None, **k):
    c = c or "#c9ccd8"
    return E(0, -24, 40, 10, c, 3) + E(0, -26, 32, 6, shade(c, 1.2), 0) + C(-14, -32, 8, "#e0533b", 2) + P("M4,-30 L20,-36 L22,-28 Z", "#f4c542", 2) + E(0, -24, 40, 10, "none", 3)

def _broccoli(c=None, expr="happy", **k):
    c = c or "#3f9b4a"
    return P("M-8,0 L-4,-30 H4 L8,0 Z", "#9acd6a", 2.5) + "".join(C(x, y, r, c, 2.5) for x, y, r in [(-16, -40, 12), (14, -40, 12), (0, -54, 15), (-20, -56, 10), (20, -56, 10)]) + face(0, -44, 0.55, expr)

def _bus(c=None, **k):
    c = c or "#ffd23f"
    return (f'<rect x="-42" y="-58" width="84" height="46" rx="8" fill="{c}" stroke="{INK}" stroke-width="3"/>' + "".join(f'<rect x="{x}" y="-50" width="14" height="14" fill="#bfefff" stroke="{INK}" stroke-width="2"/>' for x in (-34, -16, 2, 20))
            + C(-24, -10, 9, "#333", 2.5) + C(24, -10, 9, "#333", 2.5) + L(-42, -30, 42, -30, "#c0262d", 3))

def _question(c=None, **k):
    c = c or "#ffd23f"
    return P("M-18,-60 Q-18,-84 2,-84 Q24,-84 24,-62 Q24,-46 6,-40 V-24", "none", 13, INK) + P("M-18,-60 Q-18,-84 2,-84 Q24,-84 24,-62 Q24,-46 6,-40 V-24", "none", 8, c) + C(6, -8, 7, c, 3)

def _cave(c=None, **k):
    c = c or "#8a7a6a"
    return P("M-44,0 Q-44,-50 -10,-70 Q20,-80 40,-50 Q48,-30 44,0 Z", c, 3) + P("M-20,0 Q-22,-34 0,-40 Q22,-34 20,0 Z", "#1b1b2f", 2.5) + P("M-12,-38 l4,8 l4,-8 M4,-38 l4,8 l4,-8", "#f7f3e8", 1)

def _stairs(c=None, **k):
    c = c or "#c9b89a"
    return "".join(f'<rect x="{-40+j*16}" y="{-16-j*16}" width="{80-j*16}" height="16" fill="{c if j % 2 == 0 else shade(c,0.85)}" stroke="{INK}" stroke-width="2.5"/>' for j in range(5)) + P("M-8,-48 h12 v6 h-12 Z", INK, 0)

LIB_BATCH2 = ({"vase": _vase, "teddy": _teddy, "teddy-bear": _teddy, "bicycle": _bicycle, "bike": _bicycle, "price-tag": _pricetag, "tag": _pricetag,
            "price": _pricetag, "pyramid": _pyramid, "vest": _vest, "whirlpool": _whirlpool, "vortex": _whirlpool, "cannon": _cannon, "maze": _maze,
            "labyrinth": _maze, "tray": _tray, "broccoli": _broccoli, "bus": _bus, "question": _question, "question-mark": _question, "quiz": _question,
            "riddle": _question, "cave": _cave, "stairs": _stairs, "staircase": _stairs, "stair": _stairs, "steps": _stairs})

# ---- library growth · batch 3 (chapters 21-30)
def _carpet(c=None, **k):
    c = c or "#a0303a"
    return (P("M-44,-30 Q-20,-44 0,-34 Q20,-24 44,-38 L40,-14 Q20,0 0,-10 Q-20,-20 -44,-6 Z", c, 3) + P("M-36,-24 Q-18,-34 0,-26 Q18,-18 36,-30", "none", 2, "#f4c542")
            + "".join(L(-44 + j * 0, -30 + j * 6, -52, -32 + j * 6, "#f4c542", 2) for j in range(4)) + P("M-10,-26 l6,-4 l6,4 l-6,4 Z", "#f4c542", 1.5))

def _lure(c=None, **k):
    c = c or "#ffd23f"
    return L(0, -86, 0, -60, "#9aa8b8", 1.5) + P("M-18,-58 Q0,-70 18,-58 Q10,-40 0,-36 Q-10,-40 -18,-58 Z", c, 3) + C(-8, -56, 3, INK, 0) + P("M0,-36 V-14 Q0,-2 -10,-6", "none", 3, "#9aa8b8") + sparkle(22, -66, 6)

def _beehive(c=None, **k):
    c = c or "#f0b030"
    return (L(0, -84, 0, -76, "#6b4a2a", 3) + "".join(E(0, y, w, 8, c, 2.5) for y, w in [(-70, 16), (-56, 26), (-40, 32), (-24, 30), (-10, 22)])
            + P("M-6,-10 Q0,-22 6,-10 Z", "#6b4a2a", 1.5) + gs(bug("#ffd23f", segs=2, wings=True, stripes=INK), 34, -50, 0.35))

def _gong(c=None, **k):
    c = c or "#d9a441"
    return L(-36, 0, -36, -84, "#8a5a2b", 5) + L(36, 0, 36, -84, "#8a5a2b", 5) + L(-40, -82, 40, -82, "#8a5a2b", 6) + L(-10, -82, -8, -70, INK, 1.5) + L(10, -82, 8, -70, INK, 1.5) + C(0, -44, 26, c, 3) + C(0, -44, 10, shade(c, 0.75), 2)

def _tape(c=None, **k):
    c = c or "#9aa8b8"
    return C(0, -34, 28, c, 3) + C(0, -34, 12, "#fff", 2.5) + P("M24,-20 L46,-6 L40,4 L18,-10", c, 2.5)

def _tire(c=None, expr=None, **k):
    return C(0, -36, 34, c or "#2a2a33", 3) + C(0, -36, 16, "#9aa8b8", 3) + "".join(L(22 * math.cos(a), -36 + 22 * math.sin(a), 32 * math.cos(a), -36 + 32 * math.sin(a), "#555", 3) for a in [j * math.pi / 5 for j in range(10)]) + (face(0, -36, 0.5, expr) if expr and expr != "happy" else "")

def _press(c=None, **k):
    c = c or "#6b6b78"
    return (f'<rect x="-40" y="-84" width="80" height="12" fill="{c}" stroke="{INK}" stroke-width="3"/>' + L(-34, -72, -34, 0, c, 6) + L(34, -72, 34, 0, c, 6)
            + L(0, -72, 0, -44, "#9aa8b8", 8) + f'<rect x="-28" y="-44" width="56" height="12" fill="{shade(c,0.8)}" stroke="{INK}" stroke-width="3"/>'
            + f'<rect x="-30" y="-8" width="60" height="8" fill="#e0c28a" stroke="{INK}" stroke-width="2.5"/>' + "".join(P(f"M{x},-18 l3,6 l3,-6", "none", 2, "#fff") for x in (-20, 0, 18)))

def _sausage(c=None, expr="happy", **k):
    c = c or "#c0503a"
    return P("M-40,-20 Q-44,-44 -20,-44 H20 Q44,-44 40,-20 Q36,-6 20,-8 H-20 Q-36,-6 -40,-20 Z", c, 3) + "".join(C(x, -28, 2.5, "#f3d9c8", 0) for x in (-24, -8, 10, 26)) + face(0, -30, 0.55, expr)

LIB_BATCH3 = {"carpet": _carpet, "magic-carpet": _carpet, "rug": _carpet, "lure": _lure, "bait": _lure, "beehive": _beehive, "hive": _beehive,
              "gong": _gong, "tape": _tape, "duct-tape": _tape, "tire": _tire, "tyre": _tire, "press": _press, "sausage": _sausage, "salami": _sausage}

# ---- library growth · batch 5 (chapters 41-50)
def _loom(c=None, **k):
    c = c or "#8a5a2b"
    return (L(-38, 0, -38, -84, c, 6) + L(38, 0, 38, -84, c, 6) + L(-42, -80, 42, -80, c, 6) + L(-42, -20, 42, -20, c, 6)
            + "".join(L(x, -78, x, -22, "#dfe6f0", 1.2) for x in range(-30, 34, 6)) + f'<rect x="-34" y="-58" width="68" height="20" fill="#e0533b" opacity=".85"/>'
            + P("M-34,-52 H34 M-34,-44 H34", "none", 2, "#ffd23f"))

def _mask(c=None, expr="angry", **k):
    c = c or "#6b8a3a"
    return (P("M-30,-72 Q0,-86 30,-72 Q34,-40 20,-16 Q0,-2 -20,-16 Q-34,-40 -30,-72 Z", c, 3) + P("M-22,-58 l12,6 l-12,6 Z M22,-58 l-12,6 l12,6 Z", INK, 1)
            + P("M-12,-26 l4,-6 l4,6 l4,-6 l4,6 l4,-6", "#fff", 1.5) + P("M-30,-66 l-10,-10 M30,-66 l10,-10", "none", 3, shade(c, 0.7)) + C(-4, -40, 3, shade(c, 0.6), 0))

def _plunger(c=None, **k):
    return P("M-24,0 Q-24,-26 0,-28 Q24,-26 24,0 Z", c or "#e0533b", 3) + L(0, -28, 0, -86, "#a0703a", 7)

def _mint(c=None, expr="happy", **k):
    c = c or "#9cff9a"
    return C(0, -32, 28, "#fff", 3) + "".join(P(f"M0,-32 L{28*math.cos(a):.1f},{-32+28*math.sin(a):.1f} A28,28 0 0 1 {28*math.cos(a+0.52):.1f},{-32+28*math.sin(a+0.52):.1f} Z", "#e0533b" if c == "#9cff9a" else c, 0) for a in [j * math.pi / 3 for j in range(6)]) + C(0, -32, 28, "none", 3) + face(0, -32, 0.6, expr)

def _mitt(c=None, **k):
    c = c or "#e0533b"
    return P("M-20,0 V-50 Q-20,-78 4,-78 Q26,-78 26,-54 V-40 Q40,-48 42,-36 Q40,-24 26,-20 V0 Z", c, 3) + "".join(P(f"M-20,{y} H26", "none", 2, "#fff") for y in (-12, -6))

def _window(c=None, **k):
    c = c or "#8a5a2b"
    return P("M-30,0 V-52 Q-30,-84 0,-84 Q30,-84 30,-52 V0 Z", c, 3) + P("M-24,-6 V-52 Q-24,-76 0,-76 Q24,-76 24,-52 V-6 Z", "#9ad0ff", 2) + L(0, -76, 0, -6, c, 3) + L(-24, -40, 24, -40, c, 3)

def _jet(c=None, **k):
    c = c or "#c9ccd8"
    return (P("M-44,-40 Q-10,-50 30,-46 Q46,-44 46,-40 Q46,-36 30,-34 Q-10,-30 -44,-40 Z", c, 3) + P("M-4,-44 L-24,-74 L-12,-74 L14,-44 Z", shade(c, 0.85), 2.5)
            + P("M-4,-36 L-22,-10 L-10,-10 L14,-36 Z", shade(c, 0.85), 2.5) + P("M-44,-40 L-52,-58 L-36,-44 Z", c, 2.5) + P("M-60,-40 q-20,-6 -30,6", "none", 5, "#fff", 'opacity=".6"'))

def _arrow(c=None, **k):
    c = c or "#8a5a2b"
    return L(-40, -10, 30, -66, c, 5) + P("M30,-66 L22,-50 L40,-72 L18,-62 Z", "#c9ccd8", 2) + P("M-40,-10 l-6,-12 M-40,-10 l-12,-4 M-34,-16 l-6,-12 M-34,-16 l-12,-4", "none", 3, "#e0533b")

def _spur(c=None, **k):
    c = c or "#c9ccd8"
    pts = " ".join(f"{20+(16 if j % 2 == 0 else 6)*math.cos(j*math.pi/5):.1f},{-30+(16 if j % 2 == 0 else 6)*math.sin(j*math.pi/5):.1f}" for j in range(10))
    return _shoe("#8a5a2b").replace("M-34,0 V-22", "M-34,0 V-22") + L(-34, -18, 6, -30, c, 4) + f'<polygon points="{pts}" fill="{c}" stroke="{INK}" stroke-width="2"/>'

LIB_BATCH5 = {"spur": _spur, "loom": _loom, "mask": _mask, "plunger": _plunger, "mint": _mint, "peppermint": _mint, "mitt": _mitt, "oven-mitt": _mitt,
              "window": _window, "jet": _jet, "plane": _jet, "airplane": _jet, "arrow": _arrow}

# ---- library growth · batch 6 (chapters 51-60)
def _stain(c=None, **k):
    c = c or "#23233a"
    return P("M-30,-20 Q-40,-40 -20,-44 Q-14,-64 6,-54 Q24,-66 30,-44 Q46,-36 32,-20 Q36,-2 14,-6 Q0,6 -14,-4 Q-34,2 -30,-20 Z", c, 3) + "".join(C(x, y, r, c, 0) for x, y, r in [(-38, -50, 4), (40, -58, 3), (44, -10, 4)])

def _jeans(c=None, **k):
    c = c or "#2f6db5"
    return P("M-26,-80 H26 L30,0 H6 L0,-44 L-6,0 H-30 Z", c, 3) + L(-26, -72, 26, -72, shade(c, 0.7), 3) + P("M-20,-66 q6,8 14,0 M20,-66 q-6,8 -14,0", "none", 1.5, "#f4c542")

def _galaxy(c=None, **k):
    c = c or "#b48cff"
    return (f'<circle cx="0" cy="-40" r="40" fill="{c}" opacity=".25"/>' + "".join(P(f"M0,-40 Q{24*math.cos(a):.1f},{-40+24*math.sin(a):.1f} {38*math.cos(a+1):.1f},{-40+38*math.sin(a+1):.1f}", "none", 5, c) for a in (0, 2.1, 4.2))
            + C(0, -40, 7, "#fff6c9", 2) + "".join(C(x, y, 1.6, "#fff", 0) for x, y in [(-30, -60), (28, -20), (22, -70), (-24, -14)]))

def _scissors(c=None, **k):
    c = c or "#c9ccd8"
    return P("M-6,-40 L30,-78 M6,-40 L-30,-78", "none", 6, c) + C(-16, -22, 10, "none", 4, "#e0533b") + C(16, -22, 10, "none", 4, "#e0533b") + C(0, -44, 3, INK, 0) + L(-8, -32, -6, -40, "#e0533b", 4) + L(8, -32, 6, -40, "#e0533b", 4)

def _bridge(c=None, **k):
    c = c or "#a0703a"
    return P("M-46,-30 Q0,-70 46,-30", "none", 7, c) + L(-46, -30, -46, 0, c, 6) + L(46, -30, 46, 0, c, 6) + "".join(L(x, -30 - (44 - abs(x)) * 0.5 * 0.9, x, -26, shade(c, 0.7), 2) for x in range(-36, 40, 12)) + L(-48, -28, 48, -28, c, 4)

def _sprout(c=None, expr="happy", **k):
    return E(0, -8, 22, 8, "#8a5a2b", 2.5) + P("M0,-10 Q-2,-34 0,-44", "none", 4, "#3f9b4a") + P("M0,-40 Q-22,-56 -26,-40 Q-12,-32 0,-40 Z", c or "#9cff57", 2) + P("M0,-44 Q20,-62 26,-46 Q12,-38 0,-44 Z", c or "#9cff57", 2) + face(0, -20, 0.4, expr)

def _club(c=None, **k):
    c = c or "#8a5a2b"
    return P("M-6,0 L-10,-40 Q-22,-74 0,-82 Q22,-74 12,-40 L6,0 Z", c, 3) + "".join(C(x, y, 2.5, shade(c, 0.6), 0) for x, y in [(-6, -64), (4, -56), (-2, -46)])

def _blob(c=None, expr="happy", **k):
    c = c or "#9cff57"
    return P("M-34,0 Q-44,-30 -24,-46 Q-12,-66 8,-56 Q34,-62 36,-34 Q46,-12 30,0 Z", c, 3, extra='opacity=".92"') + face(0, -30, 0.8, expr) + E(18, -46, 6, 4, "#fff", 0, extra='opacity=".6"')

def _poster(c=None, expr="angry", **k):
    return f'<rect x="-28" y="-80" width="56" height="72" fill="{c or "#ffd23f"}" stroke="{INK}" stroke-width="3" transform="rotate(-4 0 -44)"/>' + T(0, -66, "!!", 16, "#c0262d") + face(0, -40, 0.8, expr) + C(-22, -76, 3, "#e0533b", 1)

def _plant(c=None, expr="happy", **k):
    return P("M-18,-24 H18 L14,0 H-14 Z", "#c8773a", 3) + P("M0,-24 Q-4,-50 0,-60", "none", 4, "#3f9b4a") + "".join(E(x, y, 10, 6, c or "#3f9b4a", 2, extra=f'transform="rotate({r} {x} {y})"') for x, y, r in [(-12, -44, -30), (12, -48, 30), (-8, -62, -50), (10, -66, 40)])

def _salvagecrane(c=None, **k):
    c = c or "#ffd23f"
    return (f'<rect x="-40" y="-20" width="36" height="20" fill="{c}" stroke="{INK}" stroke-width="3"/>' + P("M-26,-20 L-10,-84 L40,-60", "none", 5, c)
            + L(40, -60, 40, -30, INK, 1.5) + P("M34,-30 h12 l-2,8 h-8 Z", "#6b6b78", 1.5) + "".join(L(-24 + j * 4, -24 - j * 14, -18 + j * 4, -24 - j * 14, INK, 1) for j in range(4)))

LIB_BATCH6 = {"stain": _stain, "blot": _stain, "ink-stain": _stain, "jeans": _jeans, "trousers": _jeans, "pants": _jeans, "galaxy": _galaxy, "nebula": _galaxy,
              "scissors": _scissors, "bridge": _bridge, "sprout": _sprout, "seedling": _sprout, "seed": _sprout, "club": _club, "blob": _blob, "slime": _blob,
              "poster": _poster, "plant": _plant, "salvage-crane": _salvagecrane, "crane-machine": _salvagecrane}

# ---- library growth · batch 7 (chapters 61-70)
def _grapes(c=None, **k):
    c = c or "#8a4fc8"
    return L(0, -80, 2, -70, "#6b4a2a", 3) + P("M2,-74 q14,-8 20,2 q-12,4 -20,-2 Z", "#3f9b4a", 1.5) + "".join(C(x, y, 8, c, 2) for x, y in [(-12, -62), (0, -64), (12, -62), (-6, -48), (6, -48), (0, -34), (0, -20)])

def _windmill(c=None, **k):
    c = c or "#e8d6b0"
    return (P("M-16,0 L-10,-56 H10 L16,0 Z", c, 3) + P("M-12,-56 L0,-68 L12,-56 Z", "#c0262d", 2.5) + P("M-6,0 v-14 h12 v14", "#6b4a2a", 2)
            + "".join(P(f"M0,-60 L{40*math.cos(a):.1f},{-60+40*math.sin(a):.1f} L{40*math.cos(a+0.3):.1f},{-60+40*math.sin(a+0.3):.1f} Z", "#f7f3e8", 2) for a in (0.4, 2.0, 3.5, 5.1)) + C(0, -60, 4, INK, 0))

def _log(c=None, **k):
    c = c or "#a0703a"
    return f'<rect x="-40" y="-40" width="72" height="30" rx="4" fill="{c}" stroke="{INK}" stroke-width="3"/>' + E(32, -25, 9, 15, "#e0c28a", 3) + C(32, -25, 5, "none", 1.5, shade(c, 0.7)) + L(-30, -32, 20, -32, shade(c, 0.7), 1.5) + L(-26, -20, 16, -20, shade(c, 0.7), 1.5)

LIB_BATCH7 = {"grapes": _grapes, "grape": _grapes, "windmill": _windmill, "log": _log, "timber": _log, "wood": _log}

# ---- library growth · batch 8 (chapters 71-80)
def _burrito(c=None, expr="grin", **k):
    c = c or "#f3d9a0"
    return P("M-40,-20 Q-44,-46 -16,-50 L30,-44 Q46,-30 34,-14 L-14,-8 Q-38,-6 -40,-20 Z", c, 3) + P("M30,-44 Q40,-40 40,-30 Q32,-26 24,-30", "#3f9b4a", 2) + P("M34,-26 q6,4 4,10", "none", 3, "#e0533b") + face(-6, -30, 0.6, expr)

def _newspaper(c=None, **k):
    return (f'<rect x="-34" y="-72" width="62" height="64" fill="#f7f3e8" stroke="{INK}" stroke-width="3" transform="rotate(-6 0 -40)"/>'
            + f'<g transform="rotate(-6 0 -40)">' + T(-3, -58, "LIES!", 14, c or "#c0262d") + "".join(L(-28, y, 22, y, "#9a9aa8", 2) for y in (-48, -40, -32, -24, -16)) + "</g>")

def _yarn(c=None, **k):
    c = c or "#e0533b"
    return C(0, -30, 28, c, 3) + "".join(P(f"M{-24+j*8},{-48+j*2} Q{j*3},-30 {-20+j*10},{-10}", "none", 2, shade(c, 0.75)) for j in range(5)) + P("M24,-18 Q40,-4 30,0", "none", 2.5, c)

def _conveyor(c=None, **k):
    c = c or "#6b6b78"
    return f'<rect x="-44" y="-34" width="88" height="16" rx="8" fill="{c}" stroke="{INK}" stroke-width="3"/>' + "".join(C(x, -26, 5, "#9aa8b8", 2) for x in (-34, -12, 10, 32)) + L(-36, -18, -36, 0, INK, 4) + L(36, -18, 36, 0, INK, 4) + gs(_letter(), 0, -34, 0.5)

def _spoon(c=None, expr=None, **k):
    c = c or "#c9ccd8"
    return E(0, -66, 14, 18, c, 3) + L(0, -48, 0, -2, c, 7) + L(0, -48, 0, -2, INK, 0.1) + P("M-6,-72 q4,-6 10,-4", "none", 2, "#fff") + (face(0, -66, 0.5, expr) if expr and expr != "happy" else "")

LIB_BATCH8 = {"burrito": _burrito, "wrap": _burrito, "newspaper": _newspaper, "news": _newspaper, "headline": _newspaper, "yarn": _yarn,
              "conveyor": _conveyor, "conveyor-belt": _conveyor, "belt": _conveyor, "spoon": _spoon}

# ---- library growth · batch 9 (chapters 81-90)
def _sieve(c=None, **k):
    c = c or "#9aa8b8"
    return E(0, -40, 32, 10, c, 3) + P("M-32,-40 Q-30,-6 0,-6 Q30,-6 32,-40", "#dfe6f0", 3) + "".join(C(x, y, 1.6, INK, 0) for x in range(-20, 24, 8) for y in (-30, -20)) + L(32, -42, 48, -52, "#8a5a2b", 5)

def _parachute(c=None, **k):
    c = c or "#e0533b"
    return (P("M-42,-50 Q-40,-90 0,-90 Q40,-90 42,-50 Q30,-58 20,-50 Q10,-58 0,-50 Q-10,-58 -20,-50 Q-30,-58 -42,-50 Z", c, 3)
            + P("M-20,-86 Q-10,-70 -20,-50 M20,-86 Q10,-70 20,-50", "none", 2, "#fff") + "".join(L(x, -50, 0, -14, INK, 1.2) for x in (-42, -20, 0, 20, 42))
            + f'<rect x="-7" y="-16" width="14" height="14" rx="3" fill="#8a5a2b" stroke="{INK}" stroke-width="2"/>')

def _battery(c=None, expr="grin", **k):
    c = c or "#3f9b4a"
    return (f'<rect x="-18" y="-72" width="36" height="68" rx="5" fill="{c}" stroke="{INK}" stroke-width="3"/><rect x="-8" y="-80" width="16" height="8" fill="#c9ccd8" stroke="{INK}" stroke-width="2"/>'
            + f'<rect x="-18" y="-28" width="36" height="24" rx="3" fill="#23233a"/>' + T(0, -58, "+", 14, "#fff") + face(0, -42, 0.55, expr) + P("M24,-60 l8,-6 l-4,10 l10,-4", "none", 2, "#ffd23f"))

def _fries(c=None, expr="happy", **k):
    c = c or "#e0533b"
    return "".join(f'<rect x="{x}" y="{-80+abs(x)%9}" width="7" height="44" fill="#ffd23f" stroke="{INK}" stroke-width="1.5" transform="rotate({x/3:.0f} {x} -50)"/>' for x in range(-18, 20, 7)) + P("M-24,-42 H24 L18,0 H-18 Z", c, 3) + face(0, -22, 0.6, expr)

def _popcorn(c=None, **k):
    c = c or "#e0533b"
    return "".join(C(x, y, 9, "#fff6c9", 2) for x, y in [(-16, -56), (0, -62), (16, -56), (-8, -68), (10, -70)]) + P("M-24,-52 H24 L18,0 H-18 Z", "#fff", 3) + "".join(f'<rect x="{x}" y="-52" width="7" height="52" fill="{c}"/>' for x in (-16, -2, 12)) + P("M-24,-52 H24 L18,0 H-18 Z", "none", 3)

def _chess(c=None, **k):
    c = c or "#f7f3e8"
    return (f'<rect x="-24" y="-12" width="48" height="12" rx="3" fill="{c}" stroke="{INK}" stroke-width="3"/>' + P("M-16,-12 Q-14,-30 -8,-40 Q-22,-50 -16,-66 Q-6,-86 12,-78 Q24,-70 20,-50 Q18,-30 16,-12 Z", c, 3)
            + C(4, -66, 3, INK, 0) + P("M-8,-40 Q0,-44 8,-40", "none", 2))

LIB_BATCH9 = {"sieve": _sieve, "strainer": _sieve, "parachute": _parachute, "battery": _battery, "fries": _fries, "french-fry": _fries, "fry": _fries,
              "popcorn": _popcorn, "chess": _chess, "chess-piece": _chess, "chessboard": _chess}

# ---- library growth · batch 10 (chapters 91-100)
def _tie(c=None, **k):
    c = c or "#c0262d"
    return P("M-10,-84 H10 L6,-72 L16,-20 L0,-2 L-16,-20 L-6,-72 Z", c, 3) + P("M-10,-84 H10 L6,-72 H-6 Z", shade(c, 0.8), 2) + T(0, -40, "ENEMY", 7, "#fff", family="Arial,sans-serif", weight="900", extra='transform="rotate(-90 0 -40)"')

def _clothesiron(c=None, **k):
    c = c or "#9aa8b8"
    return P("M-40,-10 Q-36,-44 10,-44 Q36,-40 44,-10 Z", c, 3) + P("M-20,-44 Q-18,-66 6,-66 Q22,-64 20,-44", "none", 6, INK) + f'<rect x="-40" y="-14" width="84" height="6" fill="#dfe6f0" stroke="{INK}" stroke-width="2"/>' + "".join(P(f"M{x},-2 q4,-6 0,-12", "none", 1.5, "#fff") for x in (-24, -8, 8))

LIB_BATCH10 = {"tie": _tie, "necktie": _tie, "clothes-iron": _clothesiron, "iron": _clothesiron}

def _thought(noun):
    """Fallback: a labelled thought bubble with the noun written inside."""
    word = noun.replace("-", " ").upper()
    w = max(56, min(96, len(word) * 8.5 + 20))
    fs = 13 if len(word) <= 9 else max(8, 13 - (len(word) - 9) * 0.5)
    return ("".join(C(x, y, r, "#fff", 2.5) for x, y, r in [(-w / 2 + 10, -34, 14), (w / 2 - 10, -34, 14), (-w / 4, -48, 16), (w / 4, -48, 16), (0, -24, 16)])
            + E(0, -38, w / 2, 16, "#fff", 0) + C(-8, -4, 4, "#fff", 2) + C(-2, 4, 2.5, "#fff", 1.5)
            + T(0, -33, esc(word), fs, "#6b2fa0", family="'Bangers',Impact,sans-serif"))

# quadrupeds / birds / bugs / people as small lambdas over the factories
LIB = {
    "gnome": _gnome, "crow": _crow, "imp": _imp, "bread": _bread, "tick": _tick, "candy": _candy, "pickle": _pickle, "monster": _monster,
    "ball": _ball, "fish": _fish, "king": _king, "crown": _crown, "robot": _robot, "cake": _cake, "door": _door, "key": _key, "coin": _coin,
    "money": _money, "clock": _clock, "shoe": _shoe, "mountain": _mountain, "volcano": _volcano, "train": _train, "boat": _boat, "ship": _boat,
    "car": _car, "van": _car, "rocket": _rocket, "house": _house, "castle": _castle, "fort": _castle, "star": _star, "moon": _moon, "sun": _sun,
    "cloud": _cloud, "flower": _flower, "rose": _flower, "tree": _tree, "cactus": _cactus, "book": _book, "dictionary": _book, "scroll": _scroll,
    "mirror": _mirror, "bell": _bell, "egg": _egg, "lamp": _lamp, "genie": _genie, "ghost": _ghost, "dragon": _dragon, "snake": _snake,
    "serpent": _snake, "octopus": _octopus, "whale": _whale, "shark": _shark, "eel": _eel, "crab": _crab, "turtle": _turtle, "tortoise": _turtle,
    "frog": _frog, "toad": _frog, "snail": _snail, "jellyfish": _jellyfish, "seal": _seal, "spider": _spider, "butterfly": _butterfly, "worm": _worm,
    "sponge": _sponge, "soap": _soap, "eraser": _eraser, "net": _net, "magnet": _magnet, "stamp": _stamp, "camera": _camera, "phone": _phone,
    "tv": _tv, "television": _tv, "sword": _sword, "shield": _shield, "anchor": _anchor, "drum": _drum, "guitar": _guitar, "trumpet": _trumpet,
    "horn": _trumpet, "balloon": _balloon, "gift": _gift, "present": _gift, "letter": _letter, "message": _letter, "envelope": _letter, "card": _card,
    "puzzle": _puzzle, "dice": _dice, "die": _dice, "pizza": _pizza, "apple": _apple, "banana": _banana, "carrot": _carrot, "popsicle": _popsicle,
    "ice-cream": _icecream, "icecream": _icecream, "cheese": _cheese, "pot": _pot, "cauldron": _pot, "cup": _cup, "teacup": _cup, "mug": _cup,
    "bottle": _bottle, "jar": _jar, "bucket": _bucket, "ladder": _ladder, "hammer": _hammer, "umbrella": _umbrella, "firework": _firework,
    "bomb": _bomb, "snowman": _snowman, "unicorn": _unicorn, "alien": _alien, "skeleton": _skeleton, "mummy": _mummy, "vampire": _vampire,
    "bathtub": _bathtub, "bed": _bed, "chair": _chair, "table": _table, "throne": _throne, "tower": _tower, "wall": _wall, "rock": _rock,
    "stone": _rock, "boulder": _rock, "crystal": _crystal, "gem": _crystal, "jewel": _crystal, "diamond": _crystal, "potion": _potion,
    "feather": _feather, "heart": _heart, "brain": _brain, "eye": _eye, "hand": _hand, "nose": _nose, "gear": _gear, "machine": _machine,
    "clay": _clay, "pillow": _pillow, "skirt": _skirt, "hat": _hat, "glasses": _glasses, "flag": _flag, "torch": _torch, "candle": _candle,
    "tent": _tent, "kite": _kite, "cage": _cage, "chest": _chest, "treasure": _chest, "map": _map, "compass": _compass, "hourglass": _hourglass,
    "scales": _scales, "scale": _scales, "trophy": _trophy, "medal": _medal, "lightbulb": _lightbulb, "bulb": _lightbulb, "pencil": _pencil,
    "pen": _pencil, "brush": _paintbrush, "paintbrush": _paintbrush, "painting": _painting, "picture": _painting, "paint": _paint,
    "sandwich": _sandwich, "soup": _soup, "broom": _broom, "rope": _rope, "chain": _chain, "lock": _lock, "padlock": _lock, "box": _box,
    "fan": _fan, "wave": _wave, "river": _river, "island": _island, "pool": _pool, "desert": _desert, "city": _city, "lab": _lab,
    "gym": _gym, "shop": _shop, "store": _shop, "party": _party, "note": _note, "song": _song, "web": _web, "bubble": _bubble,
    "fire": _fire, "flame": _fire, "ice": _ice, "lightning": _lightning, "rainbow": _rainbow, "statue": _statue,
    # props from the story art kit
    "lion": lambda c=None, **k: props.lion(0, 0, 0.62, c or "#d9a441"), "camel": lambda c=None, **k: props.camel(0, 0, 0.62),
    "horse": lambda c=None, **k: props.horse(-10, 0, 0.45, c or "#8a5a2b"), "elephant": lambda c=None, **k: props.elephant(-18, 0, 0.55, c or "#8a8a95"),
    "eagle": lambda c=None, **k: props.eagle(0, 10, 0.5, c or "#d9a441"), "giraffe": lambda c=None, **k: props.giraffe(-12, 0, 0.42),
    "palm": lambda c=None, **k: props.palm(0, 0, 70), "fountain": lambda c=None, **k: props.fountain(0, 0, 0.5), "well": lambda c=None, **k: props.well(0, 0, 0.5),
    "anvil": lambda c=None, **k: props.anvil(0, 0, 0.6), "target": lambda c=None, **k: props.target(0, 0, 0.45), "barrel": lambda c=None, **k: props.barrel(-20, 0, c or "#8a5a2b"),
    "sack": lambda c=None, **k: props.sack(0, 0, c or "#c9a26a"), "bag": lambda c=None, **k: props.sack(0, 0, c or "#c9a26a"),
    "watermelon": lambda c=None, **k: props.watermelon(0, -20, 22), "lotus": lambda c=None, **k: props.lotus(0, -10),
    "djinn": lambda c=None, **k: qalam("happy", 0.45), "ink": lambda c=None, **k: qalam("happy", 0.45),
    "shadow": lambda c=None, **k: hushling(0.55), "hushling": lambda c=None, **k: hushling(0.55),
    "roc": lambda c=None, **k: pebble("happy", 0.6), "chick": lambda c=None, **k: pebble("happy", 0.55),
    # quadrupeds
    "cat": lambda c=None, expr="happy", **k: quad(c or "#f39c3d", "pointy", "thin", snout="whisker", expr=expr),
    "kitten": lambda c=None, expr="happy", **k: quad(c or "#f7c873", "pointy", "thin", snout="whisker", expr=expr, big=0.8),
    "dog": lambda c=None, expr="happy", **k: quad(c or "#c8864a", "floppy", "thin", snout="muzzle", expr=expr),
    "puppy": lambda c=None, expr="happy", **k: quad(c or "#e0b070", "floppy", "thin", snout="muzzle", expr=expr, big=0.8),
    "wolf": lambda c=None, expr="mean", **k: quad(c or "#8a94a6", "pointy", "bushy", snout="fox", expr=expr),
    "fox": lambda c=None, expr="happy", **k: quad(c or "#f07a2a", "pointy", "bushy", snout="fox", expr=expr),
    "cow": lambda c=None, expr="happy", **k: quad(c or "#f7f3e8", "round", "tuft", "small", "#23233a", "cow", expr=expr),
    "bull": lambda c=None, expr="angry", **k: quad(c or "#8a5a2b", "round", "tuft", "bull", None, "cow", expr=expr),
    "ox": lambda c=None, expr="happy", **k: quad(c or "#a0703a", "round", "tuft", "bull", None, "cow", expr=expr),
    "goat": lambda c=None, expr="happy", **k: quad(c or "#f7f3e8", "pointy", "curl", "curl", None, "muzzle", expr=expr),
    "sheep": lambda c=None, expr="happy", **k: quad(c or "#f7f3e8", "floppy", "curl", None, None, None, "#3a3a4a", expr=expr),
    "ram": lambda c=None, expr="angry", **k: quad(c or "#f7f3e8", "floppy", "curl", "curl", None, None, "#3a3a4a", expr=expr),
    "deer": lambda c=None, expr="happy", **k: quad(c or "#b8804a", "pointy", "curl", "antlers", "#f7f3e8", "muzzle", expr=expr, long_legs=True),
    "pig": lambda c=None, expr="happy", **k: quad(c or "#ff9fc4", "pointy", "curl", snout="pig", expr=expr),
    "bear": lambda c=None, expr="happy", **k: quad(c or "#7a4a2a", "round", "curl", snout="muzzle", expr=expr, big=1.15),
    "mouse": lambda c=None, expr="happy", **k: quad(c or "#9a9aa8", "big", "thin", snout="whisker", expr=expr, big=0.8),
    "rat": lambda c=None, expr="mean", **k: quad(c or "#6b6b78", "big", "thin", snout="whisker", expr=expr, big=0.85),
    "rabbit": lambda c=None, expr="happy", **k: quad(c or "#f7f3e8", "long", "curl", snout="whisker", expr=expr),
    "bunny": lambda c=None, expr="happy", **k: quad(c or "#f7f3e8", "long", "curl", snout="whisker", expr=expr),
    "hippo": lambda c=None, expr="happy", **k: quad(c or "#9a86b8", "round", "thin", snout="cow", expr=expr, big=1.2),
    "rhino": lambda c=None, expr="angry", **k: quad(c or "#9a9aa8", "round", "thin", snout="cow", expr=expr, big=1.2, extra=P("M44,-44 l10,-12 l-4,14 Z", "#f3efe1", 2)),
    "donkey": lambda c=None, expr="happy", **k: quad(c or "#9a9aa8", "long", "tuft", snout="cow", expr=expr, long_legs=True),
    "mule": lambda c=None, expr="angry", **k: quad(c or "#8a7a6a", "long", "tuft", snout="cow", expr=expr, long_legs=True),
    "sloth": lambda c=None, expr="sleepy", **k: quad(c or "#a08060", "round", "curl", snout="muzzle", expr="sleepy"),
    "tiger": lambda c=None, expr="angry", **k: quad(c or "#f39c3d", "round", "thin", None, None, "whisker", expr=expr, extra="".join(P(f"M{x},-44 q4,10 0,20", "none", 3, INK) for x in (-12, 0, 12))),
    "leopard": lambda c=None, expr="happy", **k: quad(c or "#f0c060", "round", "thin", None, "#8a5a2b", "whisker", expr=expr),
    "panda": lambda c=None, expr="happy", **k: quad(c or "#f7f3e8", "round", "curl", None, "#23233a", "muzzle", expr=expr, big=1.1),
    "squirrel": lambda c=None, expr="happy", **k: quad(c or "#c8773a", "pointy", "bushy", snout="whisker", expr=expr, big=0.8),
    "monkey": lambda c=None, expr="grin", **k: quad(c or "#8a5a2b", "round", "curl", None, None, "muzzle", "#e8b98d", expr=expr),
    "ape": lambda c=None, expr="angry", **k: quad(c or "#4a3a3a", "round", "thin", None, None, "muzzle", "#8a7a6a", expr=expr, big=1.2),
    "gorilla": lambda c=None, expr="angry", **k: quad(c or "#3a3a4a", "round", "thin", None, None, "muzzle", "#6b6b78", expr=expr, big=1.2),
    "kangaroo": lambda c=None, expr="happy", **k: quad(c or "#c8864a", "long", "thin", snout="muzzle", expr=expr, long_legs=True),
    "hedgehog": lambda c=None, expr="happy", **k: quad(c or "#8a6a4a", "round", None, snout="fox", expr=expr, big=0.8, extra="".join(P(f"M{x},-40 l3,-10 l3,10", "none", 2) for x in range(-24, 20, 6))),
    "llama": lambda c=None, expr="happy", **k: quad(c or "#f3e2c0", "long", "curl", snout="muzzle", expr=expr, long_legs=True),
    "zebra": lambda c=None, expr="happy", **k: quad(c or "#f7f3e8", "pointy", "tuft", snout="cow", expr=expr, long_legs=True, extra="".join(P(f"M{x},-58 q3,8 0,18", "none", 3, INK) for x in (-16, -6, 4, 14))),
    "beaver": lambda c=None, expr="happy", **k: quad(c or "#8a5a2b", "round", None, snout="muzzle", expr=expr, extra=E(-40, -20, 12, 6, "#6b4a2a", 2)),
    "otter": lambda c=None, expr="happy", **k: quad(c or "#8a6a4a", "round", "thin", snout="whisker", expr=expr),
    "raccoon": lambda c=None, expr="mean", **k: quad(c or "#8a94a6", "pointy", "bushy", snout="fox", expr=expr),
    "skunk": lambda c=None, expr="happy", **k: quad(c or "#23233a", "pointy", "bushy", snout="fox", expr=expr),
    # birds
    "parrot": lambda c=None, expr="happy", **k: bird(c or "#3f9b4a", "#e0533b", "#f4c542", "#ffd23f", "long", expr=expr),
    "owl": lambda c=None, expr="happy", **k: bird(c or "#8a5a2b", None, "#f4c542", "#6b4a2a", big_eyes=True, belly="#f3e2c0"),
    "duck": lambda c=None, expr="happy", **k: bird(c or "#ffd23f", None, "#f39c3d", flat_bill=True, expr=expr),
    "goose": lambda c=None, expr="angry", **k: bird(c or "#f7f3e8", None, "#f39c3d", flat_bill=True, expr=expr, long_legs=True),
    "swan": lambda c=None, expr="happy", **k: bird(c or "#f7f3e8", None, "#f39c3d", expr=expr),
    "seagull": lambda c=None, expr="happy", **k: bird(c or "#f7f3e8", "#9a9aa8", "#ffd23f", expr=expr),
    "gull": lambda c=None, expr="happy", **k: bird(c or "#f7f3e8", "#9a9aa8", "#ffd23f", expr=expr),
    "pigeon": lambda c=None, expr="happy", **k: bird(c or "#9a9aa8", "#6b6b78", "#f39c3d", expr=expr),
    "dove": lambda c=None, expr="happy", **k: bird(c or "#f7f3e8", "#dfe6f0", "#f39c3d", expr=expr),
    "chicken": lambda c=None, expr="happy", **k: bird(c or "#f7f3e8", None, "#f4c542", "#e0533b", expr=expr),
    "hen": lambda c=None, expr="happy", **k: bird(c or "#c8773a", None, "#f4c542", "#e0533b", expr=expr),
    "rooster": lambda c=None, expr="happy", **k: bird(c or "#e0533b", "#3f9b4a", "#f4c542", "#e0533b", "long", expr=expr),
    "peacock": lambda c=None, expr="happy", **k: bird(c or "#2f6db5", "#1f8a8a", "#f4c542", "#1f8a8a", "fan", expr=expr),
    "penguin": lambda c=None, expr="happy", **k: bird(c or "#23233a", None, "#f39c3d", belly="#fff", expr=expr),
    "flamingo": lambda c=None, expr="happy", **k: bird(c or "#ff8fc0", None, "#23233a", long_legs=True, expr=expr),
    "bird": lambda c=None, expr="happy", **k: bird(c or "#2f6db5", None, "#f4c542", expr=expr),
    "hawk": lambda c=None, expr="mean", **k: bird(c or "#8a5a2b", None, "#f4c542", expr=expr),
    "falcon": lambda c=None, expr="mean", **k: bird(c or "#8a5a2b", None, "#f4c542", expr=expr),
    "vulture": lambda c=None, expr="mean", **k: bird(c or "#4a3a3a", None, "#e8b98d", expr=expr),
    "phoenix": lambda c=None, expr="happy", **k: bird(c or "#ff7a1a", "#ffd23f", "#f4c542", "#ffd23f", "fan", expr=expr),
    "turkey": lambda c=None, expr="happy", **k: bird(c or "#8a5a2b", None, "#f4c542", "#e0533b", "fan", expr=expr),
    "bat": lambda c=None, expr="mean", **k: P("M-40,-50 Q-30,-66 -12,-54 Q0,-64 12,-54 Q30,-66 40,-50 Q30,-44 24,-34 Q14,-40 0,-30 Q-14,-40 -24,-34 Q-30,-44 -40,-50 Z", c or "#3a2a4a", 2.5) + face(0, -48, 0.5, expr),
    # bugs
    "ant": lambda c=None, expr="happy", **k: bug(c or "#c0262d", expr=expr),
    "bee": lambda c=None, expr="happy", **k: bug(c or "#ffd23f", segs=2, wings=True, stripes=INK, expr=expr),
    "wasp": lambda c=None, expr="mean", **k: bug(c or "#ffd23f", segs=2, wings=True, stripes=INK, expr=expr),
    "fly": lambda c=None, expr="happy", **k: bug(c or "#3a3a4a", segs=2, wings=True, expr=expr),
    "mosquito": lambda c=None, expr="mean", **k: bug(c or "#6b6b78", segs=2, wings=True, expr=expr),
    "beetle": lambda c=None, expr="happy", **k: bug(c or "#1f8a8a", legs=6, round_body=True, expr=expr),
    "ladybug": lambda c=None, expr="happy", **k: bug(c or "#e0533b", legs=6, round_body=True, expr=expr),
    "cockroach": lambda c=None, expr="mean", **k: bug(c or "#6b3a1a", legs=6, round_body=True, expr=expr),
    "flea": lambda c=None, expr="happy", **k: bug(c or "#6b3a1a", legs=6, round_body=True, expr=expr),
    "caterpillar": lambda c=None, expr="happy", **k: "".join(C(-30 + 12 * j, -14, 9, c or "#9cff57", 2.5) for j in range(5)) + face(20, -16, 0.5, expr),
    # people
    **{r: (lambda r: lambda c=None, expr="happy", **k: person(r, expr, c))(r) for r in ROLE},
    # characters of the saga (their existing designs)
    "zayn": lambda c=None, expr="happy", **k: gs(human(SPECS["zayn"], "grin", ("down", "wave")), 0, 0, 0.27),
    "layla": lambda c=None, expr="happy", **k: gs(human(SPECS["layla"], "happy", ("down", "down")), 0, 0, 0.27),
    "sinbad": lambda c=None, expr="happy", **k: gs(human(SPECS["sinbad"], "happy", ("down", "wave")), 0, 0, 0.27),
    "hakim": lambda c=None, expr="happy", **k: gs(human(SPECS["hakim"], "happy", ("down", "down")), 0, 0, 0.27),
    "qalam": lambda c=None, **k: qalam("happy", 0.45), "pebble": lambda c=None, **k: pebble("happy", 0.6),
    "zulmat": lambda c=None, **k: gs(human(SPECS["zulmat"], "neutral", ("up", "hold")), 0, 0, 0.25),
    "brass-lion": lambda c=None, **k: brass_lion(0.4),
}

ALIAS = {
    "loaves": "bread", "loaf": "bread", "baguette": "bread", "crows": "crow", "raven": "crow", "blackbird": "crow", "sweet": "candy", "lollipop": "candy",
    "mall-monster": "monster", "beast": "monster", "ogre": "monster", "troll": "monster", "giant": "monster", "blob": "monster", "goblin": "imp", "devil": "imp",
    "sprite": "imp", "elf": "gnome", "dwarf": "gnome", "leprechaun": "gnome", "cucumber": "pickle", "gherkin": "pickle", "whim-sicle": "popsicle",
    "lolly": "popsicle", "ice-pop": "popsicle", "tennis": "ball", "football": "ball", "balls": "ball", "cash": "money", "gold": "money", "dollar": "money",
    "wallet": "money", "purse": "money", "boot": "shoe", "sneaker": "shoe", "slipper": "shoe", "sandal": "shoe", "hill": "mountain", "peak": "mountain",
    "locomotive": "train", "hovercraft": "boat", "craft": "boat", "canoe": "boat", "raft": "boat", "yacht": "boat", "submarine": "boat", "barge": "boat",
    "truck": "car", "bus": "car", "taxi": "car", "cart": "car", "wagon": "car", "tractor": "car", "bicycle": "car", "bike": "car", "spaceship": "rocket",
    "palace": "castle", "fortress": "castle", "temple": "castle", "mosque": "castle", "hut": "house", "cottage": "house", "home": "house", "building": "house",
    "planet": "moon", "comet": "star", "petal": "flower", "tulip": "flower", "daisy": "flower", "lily": "flower", "bush": "tree", "oak": "tree", "forest": "tree",
    "novel": "book", "diary": "book", "notebook": "book", "encyclopedia": "book", "manual": "book", "list": "scroll", "contract": "scroll", "document": "scroll",
    "paper": "scroll", "treaty": "scroll", "law": "scroll", "poem": "scroll", "speech": "scroll", "promise": "scroll", "agreement": "scroll", "vow": "scroll",
    "spell": "potion", "medicine": "potion", "lemonade": "bottle", "syrup": "bottle", "juice": "bottle", "milk": "bottle", "acid": "potion", "perfume": "bottle",
    "tea": "teacup", "coffee": "cup", "glass": "cup", "vase": "jar", "genie-us": "genie", "phantom": "ghost", "spirit": "ghost", "specter": "ghost",
    "lizard": "dragon", "dinosaur": "dragon", "crocodile": "dragon", "alligator": "dragon", "cobra": "snake", "python": "snake", "viper": "snake",
    "squid": "octopus", "dolphin": "whale", "orca": "whale", "stingray": "shark", "piranha": "fish", "goldfish": "fish", "salmon": "fish", "tuna": "fish",
    "sardine": "fish", "cod": "fish", "carp": "fish", "lobster": "crab", "shrimp": "crab", "walrus": "seal", "tadpole": "frog", "slug": "snail",
    "tarantula": "spider", "moth": "butterfly", "hornet": "wasp", "sponge-cake": "cake", "cupcake": "cake", "pie": "cake", "cookie": "cake", "donut": "cake",
    "muffin": "cake", "pastry": "cake", "dessert": "cake", "hamburger": "sandwich", "burger": "sandwich", "taco": "sandwich", "stew": "soup",
    "porridge": "soup", "noodle": "soup", "spaghetti": "soup", "lemon": "apple", "orange": "apple", "peach": "apple", "pear": "apple", "plum": "apple",
    "cherry": "apple", "grape": "apple", "tomato": "apple", "berry": "apple", "mango": "apple", "melon": "watermelon", "pumpkin": "apple",
    "potato": "rock", "onion": "apple", "corn": "carrot", "radish": "carrot", "bean": "carrot", "pea": "apple", "bone": "skeleton", "skull": "skeleton",
    "shovel": "broom", "mop": "broom", "rake": "broom", "axe": "hammer", "saw": "hammer", "tool": "hammer", "wrench": "hammer", "drill": "hammer",
    "blade": "sword", "dagger": "sword", "knife": "sword", "spear": "sword", "arrow": "sword", "bow": "sword", "cannon": "bomb", "gun": "bomb",
    "dynamite": "bomb", "grenade": "bomb", "cracker": "firework", "sparkler": "firework", "confetti": "party", "disco": "party", "festival": "party",
    "wedding": "party", "circus": "tent", "carnival": "party", "concert": "song", "melody": "song", "tune": "song", "music": "song", "choir": "band",
    "orchestra": "band", "piano": "guitar", "violin": "guitar", "harp": "guitar", "lute": "guitar", "flute": "trumpet", "tuba": "trumpet", "whistle": "trumpet",
    "megaphone": "trumpet", "microphone": "trumpet", "radio": "tv", "computer": "tv", "screen": "tv", "tablet": "phone", "robot-arm": "robot", "android": "robot",
    "cyborg": "robot", "engine": "machine", "gadget": "machine", "device": "machine", "contraption": "machine", "factory": "machine", "computer-brain": "brain",
    "cog": "gear", "wheel": "gear", "spring": "gear", "watch": "clock", "alarm": "clock", "timer": "hourglass", "sundial": "clock", "calendar": "scroll",
    "rug": "pillow", "carpet": "pillow", "blanket": "pillow", "cushion": "pillow", "mattress": "bed", "sofa": "bed", "couch": "bed", "hammock": "bed",
    "stool": "chair", "bench": "chair", "desk": "table", "counter": "table", "altar": "table", "podium": "table", "stage": "table",
    "tub": "bathtub", "bath": "bathtub", "sink": "bucket", "pail": "bucket", "basket": "bucket", "bowl": "soup", "plate": "pizza", "pan": "pot",
    "kettle": "pot", "teapot": "pot", "oven": "machine", "fridge": "box", "crate": "box", "package": "gift", "parcel": "gift", "suitcase": "chest",
    "safe": "chest", "vault": "chest", "trunk": "chest", "coffin": "chest", "tomb": "castle", "crypt": "castle", "pyramid": "mountain", "cave": "mountain",
    "cliff": "mountain", "glacier": "ice", "iceberg": "ice", "icicle": "ice", "snowflake": "ice", "snow": "snowman", "storm": "cloud", "rain": "cloud",
    "fog": "cloud", "mist": "cloud", "tornado": "cloud", "wind": "cloud", "thunder": "lightning", "flood": "wave", "tsunami": "wave", "ocean": "wave",
    "sea": "wave", "lake": "pool", "pond": "pool", "puddle": "pool", "well-water": "well", "stream": "river", "canal": "river", "waterfall": "river",
    "beach": "island", "sand": "desert", "dune": "desert", "oasis": "palm", "jungle": "tree", "garden": "flower", "field": "flower", "farm": "house",
    "village": "city", "town": "city", "market": "shop", "bazaar": "shop", "stall": "shop", "bank": "chest", "school": "house", "library": "book",
    "museum": "castle", "hospital": "house", "prison": "cage", "jail": "cage", "trap": "cage", "zoo": "cage", "laboratory": "lab", "studio": "painting",
    "photo": "camera", "photograph": "camera", "portrait": "painting", "canvas": "painting", "sculpture": "statue", "idol": "statue", "monument": "statue",
    "gargoyle": "statue", "trophy-cup": "trophy", "prize": "trophy", "award": "medal", "badge": "medal", "ribbon": "medal", "idea": "lightbulb",
    "crayon": "pencil", "quill": "pencil", "marker": "pencil", "ink-pot": "jar", "inkwell": "jar", "stamp-pad": "stamp", "seal-stamp": "stamp",
    "sticker": "card", "ticket": "card", "coupon": "card", "postcard": "letter", "mail": "letter", "note-card": "card", "sign": "flag", "banner": "flag",
    "lantern": "lamp", "lamp-post": "torch", "flashlight": "torch", "spotlight": "lightbulb", "candlestick": "candle", "match": "candle",
    "helmet": "hat", "cap": "hat", "turban": "hat", "wig": "hat", "mask": "glasses", "monocle": "glasses", "goggles": "glasses", "spectacles": "glasses",
    "dress": "skirt", "tutu": "skirt", "gown": "skirt", "robe": "skirt", "cape": "skirt", "cloak": "skirt", "jacket": "skirt", "coat": "skirt",
    "shirt": "skirt", "sock": "shoe", "glove": "hand", "fist": "hand", "finger": "hand", "arm": "hand", "foot": "shoe", "leg": "shoe", "mouth": "nose",
    "tongue": "nose", "tooth": "nose", "ear": "nose", "face": "heart", "head": "brain", "mind": "brain", "genius": "brain", "thought": "brain",
    "pearl": "crystal", "ruby": "crystal", "emerald": "crystal", "sapphire": "crystal", "ring": "crown", "necklace": "crown", "tiara": "crown",
    "jewelry": "crown", "hoop": "ball", "marble": "ball", "globe": "ball", "orb": "ball", "bead": "ball", "snowball": "ball", "pebble-stone": "rock",
    "brick": "wall", "fence": "wall", "gate": "door", "hatch": "door", "window": "door", "portal": "door", "bridge": "wall", "staircase": "ladder",
    "stairs": "ladder", "elevator": "box", "chimney": "tower", "lighthouse": "tower", "minaret": "tower", "skyscraper": "tower", "windmill": "tower",
    "tentacle": "octopus", "claw": "crab", "wing": "feather", "egg-shell": "egg", "nest": "egg", "cocoon": "egg", "seed": "egg", "acorn": "egg",
    "nut": "egg", "hive": "bee", "honey": "jar", "jam": "jar", "butter": "cheese", "salt": "sack", "sugar": "sack", "flour": "sack", "rice": "sack",
    "pepper": "sack", "spice": "sack", "sack-of": "sack", "puppet": "person", "doll": "person", "mannequin": "statue", "scarecrow": "person",
    "cowboy": "man", "gentleman": "man", "husband": "man", "father": "man", "dad": "man", "uncle": "man", "boss": "official", "chief": "official",
    "emperor": "king", "pharaoh": "king", "lord": "king", "duke": "king", "empress": "queen", "mother": "woman", "mom": "woman", "aunt": "woman", "wife": "woman",
    "grandmother": "grandma", "grandfather": "grandpa", "granny": "grandma", "toddler": "baby", "infant": "baby", "twin": "kid", "son": "kid", "daughter": "girl",
    "pupil": "student", "genius-kid": "kid", "nerd": "student", "champion": "athlete", "runner": "athlete", "boxer": "athlete", "wrestler": "weightlifter",
    "strongman": "weightlifter", "bodybuilder": "weightlifter", "swimmer": "athlete", "skater": "athlete", "surfer": "athlete", "jockey": "athlete",
    "ballerina": "dancer", "dj": "rapper", "comedian": "clown", "jester": "clown", "magician": "wizard", "sorceress": "witch", "fairy": "sprite",
    "angel": "fairy", "mermaid": "fish", "cop": "guard", "police": "guard", "sheriff": "guard", "general": "soldier", "officer": "soldier",
    "samurai": "knight", "gladiator": "knight", "viking": "warrior", "archer": "soldier", "pilot": "captain", "astronaut": "captain", "sailor-man": "sailor",
    "fisher": "fisherman", "butcher": "chef", "waiter": "chef", "grocer": "merchant", "seller": "merchant", "salesman": "merchant", "vendor": "merchant",
    "trader": "merchant", "shopkeeper": "merchant", "customer": "person", "tourist": "person", "traveler": "wanderer", "nomad": "wanderer", "tramp": "wanderer",
    "beggar": "wanderer", "hobo": "wanderer", "outlaw": "thief", "robber": "thief", "burglar": "thief", "crook": "thief", "villain-man": "villain",
    "tyrant": "villain", "dictator": "villain", "senator": "diplomat", "politician": "diplomat", "ambassador": "diplomat", "president": "mayor",
    "minister": "vizier", "advisor": "vizier", "counselor": "sage", "wise": "sage", "philosopher": "sage", "prophet": "sage", "monk-man": "monk",
    "nun": "monk", "servant": "person", "slave": "person", "butler": "person", "maid": "woman", "nanny": "woman", "worker": "builder",
    "engineer": "inventor", "mechanic": "inventor", "architect": "inventor", "mathematician": "professor", "historian": "professor", "writer": "poet",
    "author": "poet", "storyteller": "poet", "reporter": "detective", "journalist": "detective", "critic": "judge", "jury": "judge", "umpire": "referee",
    "competitor": "athlete", "rival": "athlete", "partner": "person", "friend": "person", "stranger": "person", "neighbor": "person", "fan": "person",
    "players": "team", "players-team": "team", "gang": "crowd", "mob": "crowd", "people": "crowd", "tribe": "crowd", "club": "crowd", "committee": "crowd",
    "council": "crowd", "class": "crowd", "crew": "crowd", "choir-group": "band", "parade": "crowd", "guest": "person", "host": "person",
    "hero-man": "hero", "superhero": "hero", "idol-singer": "singer", "star-singer": "singer", "pop-star": "singer",
    "horse-rider": "horse", "pony": "horse", "stallion": "horse", "mare": "horse", "kitty": "cat", "tomcat": "cat", "hound": "dog", "poodle": "dog",
    "bulldog": "dog", "pup": "puppy", "lamb": "sheep", "calf": "cow", "buffalo": "bull", "bison": "bull", "yak": "ox", "moose": "deer", "elk": "deer",
    "reindeer": "deer", "antelope": "deer", "gazelle": "deer", "hare": "rabbit", "piglet": "pig", "hog": "pig", "boar": "pig", "koala": "bear",
    "grizzly": "bear", "hamster": "mouse", "gerbil": "mouse", "mole": "mouse", "guinea-pig": "mouse", "chimp": "monkey", "chimpanzee": "monkey",
    "baboon": "monkey", "orangutan": "ape", "cheetah": "leopard", "jaguar": "leopard", "panther": "leopard", "lioness": "lion", "cub": "lion",
    "hyena": "wolf", "jackal": "fox", "coyote": "wolf", "badger": "raccoon", "weasel": "otter", "ferret": "otter", "mongoose": "otter",
    "porcupine": "hedgehog", "armadillo": "turtle", "alpaca": "llama", "dromedary": "camel", "mammoth": "elephant", "cockatoo": "parrot",
    "macaw": "parrot", "hummingbird": "bird", "sparrow": "bird", "robin": "bird", "canary": "bird", "finch": "bird", "woodpecker": "bird",
    "stork": "flamingo", "heron": "flamingo", "crane": "flamingo", "pelican": "seagull", "albatross": "seagull", "ostrich": "flamingo", "emu": "flamingo",
    "chick-bird": "chick", "duckling": "duck", "cockerel": "rooster", "peahen": "peacock", "kiwi": "bird", "toucan": "parrot", "magpie": "crow",
    "grasshopper": "ant", "cricket": "ant", "termite": "ant", "firefly": "fly", "dragonfly": "fly", "gnat": "fly", "centipede": "caterpillar",
    "millipede": "caterpillar", "larva": "worm", "maggot": "worm", "leech": "worm", "scorpion": "crab", "bug": "beetle", "insect": "beetle",
    "germ": "alien", "virus": "alien", "microbe": "alien", "martian": "alien", "zombie": "mummy", "werewolf": "wolf", "witch-hat": "witch",
    "yeti": "ape", "bigfoot": "ape", "kraken": "octopus", "sea-monster": "dragon", "griffin": "eagle", "pegasus": "unicorn", "centaur": "horse",
    "cyclops": "monster", "minotaur": "bull", "sphinx": "lion", "hydra": "dragon", "golem": "statue", "gargoyle-statue": "statue", "titan": "monster",
    "hat-trick": "hat", "top-hat": "hat",
}

LIB.update(LIB_BATCH1); LIB.update(LIB_BATCH2); LIB.update(LIB_BATCH3); LIB.update(LIB_BATCH5); LIB.update(LIB_BATCH6); LIB.update(LIB_BATCH7); LIB.update(LIB_BATCH8); LIB.update(LIB_BATCH9); LIB.update(LIB_BATCH10)
ALIAS.update({"locksmith": "smith", "burro": "donkey", "louse": "flea", "doorman": "guard", "door-man": "guard", "skater": "athlete",
              "bonfire": "fire", "tissue": "mummy", "chain-mail": "chain", "handcuffs": "chain", "fetter": "chain", "shackle": "chain",
              "tutu-imp": "imp", "pancake": "cake", "tortes": "cake", "torte": "cake", "cereal": "bowl", "stick-figure": "carrot", "root": "carrot",
              "wildebeest": "bull", "gnu": "bull", "stag": "deer", "labrador": "dog", "parsnip": "carrot", "spire": "tower",
              "charmer": "musician", "snake-charmer": "musician", "barber": "smith", "dictator": "official", "santa": "grandpa", "sandal": "shoe",
              "fax": "machine", "printer": "machine", "melon": "watermelon", "collie": "dog", "jackal": "fox", "wagon": "cart",
              "salami-cat": "cat", "doctors": "doctor", "flour": "sack", "hummingbird": "bird", "copper": "clay",
              "lemon": "apple", "cone": "icecream", "insole": "shoe", "poodle": "dog", "quill": "pencil", "harp": "guitar", "music-box": "chest",
              "viking": "warrior", "marshal": "soldier", "fire-truck": "car", "firetruck": "car", "hermit-crab": "crab", "olive": "apple",
              "soda": "bottle", "squid-wander": "octopus", "dunk-tank": "pool", "ember": "fire", "campfire": "fire", "patient": "man", "lady": "woman",
              "cling-film": "tape", "cupcake": "cake", "juice": "bottle", "album": "book", "swamp": "pool", "dinosaur": "dragon", "icon": "statue",
              "prune": "apple", "clementine": "apple", "chimera": "monster", "apparition": "ghost", "hallway": "door", "vandal": "painter",
              "cable": "rope", "empress": "queen", "grim-reaper": "reaper", "fig": "apple", "dough": "bread", "morse": "letter",
              "chameleon": "lizard", "missile": "rocket", "filter": "cup", "sandcastle": "castle", "hovercraft": "boat", "plum": "apple",
              "breeches": "jeans", "torpedo": "rocket", "raven": "crow", "debris": "rock", "junk": "box", "bun": "bread", "radish": "carrot",
              "knee": "skeleton", "jug": "jar", "spark": "firework", "glow-stick": "torch", "menu": "scroll", "espresso": "cup", "latte": "cup",
              "outfit": "skirt", "feast": "cake", "liver": "heart", "incense": "candle", "hostel": "house", "scoreboard": "tv", "terrier": "dog",
              "dynasty": "king", "hedge": "tree", "certificate": "scroll", "living-room": "chair", "toll-gate": "door", "stew": "soup",
              "clownfish": "fish", "verge": "flower", "shed": "house", "junction": "train", "knot": "rope", "quintuplet": "chef", "flavor": "icecream",
              "figure-eight": "rollercoaster", "vagrant": "wanderer", "lava": "volcano", "thrall": "crowd", "office": "painting", "gruel": "bowl",
              "pinecone": "nut", "coaster": "rollercoaster", "megaphone-cart": "cart", "wheelbarrow": "cart"})

def resolve(noun):
    """Library key for a noun, or None (-> thought-bubble fallback)."""
    n = noun.lower().strip().replace(" ", "-")
    for cand in (n, n.rstrip("s"), n[:-2] if n.endswith("es") else n, re.sub(r"ies$", "y", n)):
        if cand in LIB: return cand
        if cand in ALIAS:
            a = ALIAS[cand]
            while a in ALIAS and a not in LIB: a = ALIAS[a]
            if a in LIB: return a
    # hyphenated compounds: try each part from the right ("mall-monster" -> "monster")
    if "-" in n:
        for part in reversed(n.split("-")):
            r = resolve(part) if part != n else None
            if r: return r
    return None

# ------------------------------------------------------------------ mods & placement
HATS = {"moon": lambda: f'<circle cx="0" cy="-14" r="22" fill="#7dff9a" opacity="0.2"/>' + g(P(_crescent(), "#9dffb0", 4), 0, 2, 0.42),
        "top": lambda: f'<rect x="-10" y="-22" width="20" height="18" fill="#15152a" stroke="{INK}" stroke-width="2"/>' + L(-16, -4, 16, -4, INK, 4),
        "crown": lambda: P("M-14,0 L-16,-18 L-8,-10 L0,-22 L8,-10 L16,-18 L14,0 Z", "#f4c542", 2),
        "party": lambda: P("M-10,0 L0,-24 L10,0 Z", "#ff5fa2", 2) + C(0, -25, 3, "#ffd23f", 1),
        "chef": lambda: _extra("chefhat", 0, 4),
        "wizard": lambda: _extra("wizardhat", 0, 2),
        "turban": lambda: P("M-14,0 Q-16,-18 0,-20 Q16,-18 14,0 Z", "#f7f3e8", 2),
        "tutu": lambda: P("M-16,0 L-22,10 L22,10 L16,0 Z", "#ff9fc4", 2)}

def parse_mods(mods):
    if isinstance(mods, str): mods = [m.strip() for m in mods.split(",") if m.strip()]
    return [m.lower() for m in (mods or [])]

def draw(noun, x, y, scale=1.0, mods=None, expr=None):
    """Draw `noun` with its bottom-centre at (x, y). Returns (svg, key_or_None)."""
    mods = parse_mods(mods)
    key = resolve(noun)
    color = next((COLORS[m] for m in mods if m in COLORS), None)
    if expr is None:
        expr = next((e for m in mods for e in ("mean", "angry", "sad", "crying", "sleepy", "shock", "scared") if e in m.split("-") or m == e), "happy")
    if key:
        f = LIB[key]
        try: body = f(c=color, expr=expr)
        except TypeError: body = f(c=color)
    else:
        body = _thought(noun)
    s = scale * (1.35 if "giant" in mods or "huge" in mods else 0.7 if "tiny" in mods or "little" in mods else 1)
    rot = -80 if any(m in ("lying", "fallen", "sideways") for m in mods) else 180 if "upside-down" in mods else 0
    top = -80
    extras = ""
    if "glowing" in mods or "magic" in mods: body = f'<circle cx="0" cy="-40" r="46" fill="#ffe066" opacity="0.28"/>' + body
    for m in mods:
        for h, fn in HATS.items():
            if h in m and ("hat" in m or h in ("crown", "tutu", "turban")):
                extras += g(fn(), 0, top + (38 if h == "tutu" else 2), 1)
        if m in ("flaming", "burning", "on-fire"): extras += g(_fire(), 0, top + 10, 0.35)
        if m in ("frozen", "icy"): body += '<rect x="-44" y="-84" width="88" height="86" rx="10" fill="#bfefff" opacity="0.35"/>'
        if m in ("talking", "singing", "shouting", "yelling"): extras += T(30, top + 4, "♪" if m == "singing" else "!!", 16, "#fff", extra=f'stroke="{INK}" stroke-width="2" paint-order="stroke"')
        if m in ("sunglasses", "cool"): extras += P("M-16,-58 h32 v6 q-4,6 -12,0 h-8 q-8,6 -12,0 Z", INK, 1)
        if m == "monocle": extras += C(6, -54, 6, "none", 2, "#f4c542")
        if m in ("bow-tie", "tuxedo"): extras += P("M-8,-28 l8,4 l8,-4 v8 l-8,-4 l-8,4 Z", "#c0262d", 1.5)
    inner = body + extras
    if rot == 180: inner = f'<g transform="translate(0,-40) rotate(180) translate(0,40)">{inner}</g>'
    elif rot: inner = f'<g transform="translate(0,-22) rotate({rot}) translate(0,36)">{inner}</g>'
    if "many" in mods:
        svg = (g(inner, x - 26 * s, y - 4 * s, s * 0.62) + g(inner, x + 26 * s, y - 8 * s, s * 0.62) + g(inner, x, y + 2 * s, s * 0.72))
    else:
        svg = g(inner, x, y, s)
    return svg, key
