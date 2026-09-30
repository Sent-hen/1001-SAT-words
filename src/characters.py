from art import *

def beard_white(length=1.0, anchors=False):
    d = f"M-40,-215 Q-44,-{150-60*(length-1)} 0,-{130-60*(length-1)} Q44,-{150-60*(length-1)} 40,-215 Q30,-190 0,-188 Q-30,-190 -40,-215 Z"
    out = P(d, "#f3f1ea", 3) + P("M-24,-196 Q-12,-206 0,-198 Q12,-206 24,-196", "#f3f1ea", 3)
    if anchors:
        out += P("M-14,-132 v18 m-10,-6 q10,12 20,0", "none", 3, "#8a6418") + P("M14,-132 v18 m-10,-6 q10,12 20,0", "none", 3, "#8a6418")
    return out

def moustache(color="#2b1a10"):
    return P("M0,-204 Q-18,-214 -34,-200 Q-40,-190 -46,-200 Q-38,-222 0,-210 Q38,-222 46,-200 Q40,-190 34,-200 Q18,-214 0,-204 Z", color, 2)

def grey_beard():
    return P("M-36,-212 Q-38,-170 0,-160 Q38,-170 36,-212 Q24,-194 0,-192 Q-24,-194 -36,-212 Z", "#9c9a94", 3)

def knives():
    return "".join(P(f"M{-30+i*12},-176 l6,-14 l4,14 Z", "#d8dde6", 2) for i in range(6)) + P("M-38,-172 L38,-120", "none", 7, "#5a1a1a")

def coin_belt():
    return "".join(C(-40 + i * 10, -112 + (i % 2) * 3, 4, "#f4c542", 1.5) for i in range(9))

def falcon():
    return (P("M-110,-150 Q-120,-190 -96,-200 Q-74,-196 -76,-160 Q-84,-140 -110,-150 Z", "#8a6a4a", 3)
            + P("M-98,-200 Q-88,-212 -80,-200 L-86,-190 Z", "#a33", 2) + P("M-80,-186 l8,4 l-8,4", "#f4c542", 2))

def crescent_pendant():
    return L(-10, -180, 0, -160, "#c9c9d6", 2) + L(10, -180, 0, -160, "#c9c9d6", 2) + P("M-6,-158 A10,10 0 1 0 6,-150 A7,7 0 1 1 -6,-158 Z", "#e8e8f4", 2)

def sugar_rose():
    return C(0, -330, 12, "#ff8fb1", 2.5) + P("M-6,-332 Q0,-340 6,-330 Q0,-324 -6,-332", "none", 2)

def pastry_tray():
    return (E(-78, -110, 40, 10, "#c0c0c8", 3) + "".join(E(-96 + i * 17, -120, 8, 6, "#e3a33b", 2) for i in range(3))
            + C(-60, -128, 4, "#fff", 0, extra='opacity="0.8"'))

def mirror_frame():
    return (E(0, -210, 90, 110, "none", 10, "#c9ccd8") + E(0, -210, 98, 118, "none", 3) + E(0, -210, 82, 102, "none", 3)
            + P("M-14,-96 L-10,-30 L10,-30 L14,-96 Z", "#c9ccd8", 3))

def throne():
    return (P("M-80,-260 Q0,-320 80,-260 L80,-40 L-80,-40 Z", "#1f6f4a", 3) + P("M-96,-120 L96,-120 L96,-40 L-96,-40 Z", "#d9a441", 3)
            + P("M-80,-40 L-80,0 M80,-40 L80,0", "none", 8))

def snore():
    return C(52, -250, 8, "#cfefff", 2) + C(68, -272, 12, "#cfefff", 2) + T(92, -292, "Zzz", 20, "#2b6cb0")

SPECS = {
    "zayn": dict(skin="brown", hair="curly", hair_color="#15110e", tunic="#f28c28", trim="#ffd166", pants="#2e8b8b",
                 scar=True, hat=headband("#ff7a1a"), body_extras=[satchel()]),
    "layla": dict(skin="light", scarf="#3d3d9e", tunic="#2bb3a3", trim="#f4c542", long=True, sleeve="#2bb3a3",
                  hair="braid", hair_color="#15110e", head_extras=[reed_pen(), spectacles()], front_extras=[glowbook()], shoe="#3d3d9e"),
    "tariq": dict(skin="brown", hair="mop", hair_color="#2b1a10", tunic="#8bc34a", trim="#fff", pants="#8a6a4a",
                  hat=P("M-48,-252 Q-50,-296 0,-298 Q50,-296 48,-252 Q0,-266 -48,-252 Z", "#6aa42f", 3) + P("M20,-256 Q70,-262 76,-246 Q50,-244 30,-248 Z", "#6aa42f", 3)),
    "sinbad": dict(skin="old", tunic="#2f6db5", trim="#f4c542", long=True, sleeve="#2f6db5", beard=beard_white(1.3, True),
                   beard_hides_mouth=True, hat=turban("#fff", "#d63a3a", 1.0),
                   head_extras=[C(46, -204, 7, "none", 3, "#f4c542")],
                   front_extras=[L(80, -150, 90, 0, "#f3efe1", 8), C(80, -154, 10, "#f3efe1", 3)]),
    "marjana": dict(skin="tan", hair="long", hair_color="#1d120c", tunic="#c0262d", trim="#f4c542", pants="#c0262d", belt="#3a1010",
                    hat=P("M-48,-246 Q0,-296 48,-246 Q0,-258 -48,-246 Z", "#e03a3a", 3) + P("M44,-250 l26,10 l-22,6 Z", "#e03a3a", 2.5),
                    body_extras=[knives(), coin_belt()], shoe="#3a1010", feet="shoe"),
    "abu_hasan": dict(skin="tan", tunic="#e86aa0", trim="#ffd166", w=1.7, pants="#7a3a8a", sleeve="#e86aa0",
                      beard=moustache(), hat=turban("#ff8fb1", "#fff", 1.4) + sugar_rose(), blush=True,
                      front_extras=[pastry_tray()], feet="shoe", shoe="#7a3a8a"),
    "hakim": dict(skin="old", tunic="#1f2f6b", trim="#dfe6ff", long=True, sleeve="#1f2f6b", beard=beard_white(1.6),
                  beard_hides_mouth=True, hat=P("M-44,-250 Q0,-310 44,-250 Q0,-262 -44,-250 Z", "#1f2f6b", 3),
                  body_extras=[astrolabe()] + [sparkle(x, y, 5, "#dfe6ff") for x, y in [(-30, -60), (24, -40), (-10, -100), (30, -90)]]),
    "shahrazad": dict(skin="old", veil="#6b2fa0", tunic="#6b2fa0", trim="#f4c542", long=True, sleeve="#6b2fa0",
                      body_extras=["".join(C(-34 + (i % 8) * 10, -150 + (i // 8) * 14, 2.2, "#f4c542", 0) for i in range(40))]),
    "caliph": dict(skin="tan", tunic="#2e7d4f", trim="#f4c542", long=True, sleeve="#2e7d4f", beard=grey_beard(), beard_hides_mouth=True,
                   hat=turban("#ffffff", "#c7d2c9", 1.5, "#2ecc71"), head_extras=[snore()]),
    "queen_hind": dict(skin="tan", scarf="#1f2a6b", tunic="#d8b25a", trim="#c0c0c8", long=True, sleeve="#1f2a6b",
                       head_extras=[P("M-40,-206 Q0,-196 40,-206 L36,-170 Q0,-160 -36,-170 Z", "#1f2a6b", 3)],
                       beard_hides_mouth=True, front_extras=[falcon()]),
    "yasmin": dict(skin="light", cloak="#f1f1f6", hair="streak", hair_color="#15110e", tunic="#dcdcec", trim="#9aa0c8", long=True,
                   sleeve="#dcdcec", iris="#6a5acd", body_extras=[crescent_pendant()],
                   head_extras=[P("M-34,-226 l-12,-6 M34,-226 l12,-6", "none", 3, "#c9c9d6")]),
    "zulmat": dict(skin="#a58a7a", cloak="#2a1838", tunic="#3a1f52", trim="#b48cff", long=True, sleeve="#3a1f52",
                   mask=zulmat_mask(), front_extras=[hush_staff()]),
}

EXPR = {"zayn": ("grin", ("down", "wave"), "stand"), "layla": ("skeptic", ("hold", "chin"), "stand"),
        "tariq": ("amazed", ("up", "up"), "stand"), "sinbad": ("happy", ("wave", "down"), "stand"),
        "marjana": ("smug", ("hip", "point"), "stand"), "abu_hasan": ("grin", ("hold", "wave"), "stand"),
        "hakim": ("happy", ("down", "wave"), "stand"), "shahrazad": ("happy", ("down", "down"), "stand"),
        "caliph": ("sleep", ("down", "down"), "stand"), "queen_hind": ("determined", ("shield", "hip"), "stand"),
        "yasmin": ("side", ("chin", "hip"), "stand"), "zulmat": ("neutral", ("down", "hold"), "stand")}

INFO = {
    "zayn": ("ZAYN", "the Wind · hero · 15", "#f28c28"), "layla": ("LAYLA", "the Scribe · hero · 15", "#3d3d9e"),
    "qalam": ("QALAM", "the Ink Djinn", "#15152a"), "tariq": ("TARIQ", "little brother · 10", "#6aa42f"),
    "sinbad": ("SINBAD", "the Sailor · mentor", "#2f6db5"), "pebble": ("PEBBLE", "the baby Roc", "#e0533b"),
    "marjana": ("MARJANA", "leader of the Forty Sparrows", "#c0262d"), "abu_hasan": ("ABU HASAN", "the Jolly merchant", "#e86aa0"),
    "hakim": ("HAKIM IBN NUR", "the Old Astronomer", "#1f2f6b"), "shahrazad": ("SHAHRAZAD", "the Queen Mother", "#6b2fa0"),
    "caliph": ("CALIPH NURUDDIN", "the Sleeping Ruler", "#2e7d4f"), "queen_hind": ("QUEEN HIND", "of the Nomads", "#b8923a"),
    "tanin": ("THE TANIN", "the River Serpent", "#1f8a8a"), "brass_guardians": ("BRASS GUARDIANS", "Lion · Elephant · Eagle · Horse", "#b8862b"),
    "zulmat": ("GRAND VIZIER ZULMAT", "the Silencer · villain", "#3a1f52"), "yasmin": ("YASMIN", "the Mirage · 16", "#8a8fb8"),
    "al_hadid": ("AL-HADID", "the Brass Giant", "#7b3a2a"), "hushling": ("HUSHLINGS", "the Silent Shadows", "#0d0d1a"),
}

def draw(name):
    if name in SPECS:
        e, pose, lp = EXPR[name]
        fig = human(SPECS[name], e, pose, lp)
        extra = ""
        if name == "shahrazad":
            fig = mirror_frame() + fig
        if name == "caliph":
            fig = throne() + fig
        return g(fig, 200, 485, 1.15 if name!="zulmat" else 1.08) + extra
    if name == "qalam":
        return g(inkwell(), 200, 470, 1.6) + g(qalam("happy"), 205, 400, 1.7) + sparkle(90, 160, 14) + sparkle(320, 120, 10)
    if name == "pebble":
        return pebble("happy", 2.3).replace("translate(0.0,0.0)", "translate(200.0,470.0)")
    if name == "hushling":
        return hushling(1.35).replace("translate(0.0,0.0)", "translate(140.0,470.0)") + hushling(1.0, 0.8).replace("translate(0.0,0.0)", "translate(285.0,470.0)")
    if name == "tanin":
        return f'<rect x="0" y="380" width="400" height="140" fill="#3aa0c8" opacity="0.5"/>' + g(tanin(), 110, 480, 0.8)
    if name == "al_hadid":
        return g(al_hadid(), 200, 485, 1.0)
    if name == "brass_guardians":
        lion = brass_lion(0.8)
        eleph = g(E(0, -70, 60, 45, "#d9a441", 3) + C(50, -100, 34, "#e8b84f", 3) + P("M76,-90 Q96,-40 80,-10", "none", 14, "#e8b84f") + C(58, -108, 5, "#35e0d0", 1.5) + P("M24,-120 Q0,-150 20,-70", "#c8962e", 3) + "".join(P(f"M{x},-30 v30", "none", 16, "#d9a441") for x in (-40, -10, 20, 44)), s=0.8)
        eagle = g(P("M-80,-120 Q-40,-160 0,-110 Q40,-160 80,-120 Q40,-100 0,-80 Q-40,-100 -80,-120 Z", "#d9a441", 3) + E(0, -80, 22, 34, "#e8b84f", 3) + C(0, -126, 18, "#e8b84f", 3) + P("M10,-126 l16,6 l-16,4 Z", "#b8862b", 2) + C(-4, -130, 4, "#35e0d0", 1.5) + P("M-10,-46 l-6,40 M10,-46 l6,40", "none", 5), s=0.8)
        horse = g(P("M-60,-80 Q-60,-110 -20,-110 L40,-110 Q60,-160 80,-170 Q100,-160 96,-140 L70,-120 L60,-60 L-50,-60 Z", "#d9a441", 3) + C(86, -156, 4, "#35e0d0", 1.5) + "".join(P(f"M{x},-62 v62", "none", 12, "#d9a441") for x in (-44, -20, 30, 52)) + P("M-60,-90 Q-90,-70 -84,-40", "none", 6, "#b8862b"), s=0.8)
        return (g(lion, 110, 250, 1.0) + g(eleph, 290, 250, 1.0) + g(eagle, 110, 470, 1.0) + g(horse, 280, 470, 1.0)
                + T(110, 270, "LION · logic", 16, "#6b4a10") + T(290, 270, "ELEPHANT · memory", 16, "#6b4a10")
                + T(110, 500, "EAGLE · fairness", 16, "#6b4a10") + T(290, 500, "HORSE · self-control", 16, "#6b4a10"))
    raise KeyError(name)

FONT = "<style>@import url('https://fonts.googleapis.com/css2?family=Bangers&amp;display=swap');</style>"

def card(name):
    title, sub, col = INFO[name]
    body = draw(name)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" width="400" height="600">{FONT}'
            f'<rect width="400" height="600" rx="18" fill="#fbf1dc" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="200" cy="330" r="170" fill="{col}" opacity="0.12"/>'
            f'<g transform="translate(0,30)">{body}</g>'
            f'<rect x="12" y="12" width="376" height="62" rx="10" fill="{col}" stroke="{INK}" stroke-width="3"/>'
            + T(200, 52, title, 30 if len(title) < 14 else 24, "#fff", extra=f'stroke="{INK}" stroke-width="1.5" letter-spacing="1.5"')
            + f'<rect x="12" y="540" width="376" height="46" rx="10" fill="#fff" stroke="{INK}" stroke-width="3"/>'
            + T(200, 571, sub, 20, INK, family="Georgia,serif", weight="600") + "</svg>")

ORDER = ["zayn", "layla", "qalam", "tariq", "sinbad", "pebble", "marjana", "abu_hasan", "hakim", "shahrazad",
         "caliph", "queen_hind", "tanin", "brass_guardians", "zulmat", "yasmin", "al_hadid", "hushling"]

if __name__ == "__main__":
    import os
    os.makedirs("../images/characters", exist_ok=True)
    for n in ORDER:
        open(f"../images/characters/{n}.svg", "w", encoding="utf-8", newline="\n").write(card(n))
    # lineup: 6 columns x 3 rows of scaled cards
    cells = ""
    for i, n in enumerate(ORDER):
        x, y = (i % 6) * 410, (i // 6) * 610
        inner = card(n).split(">", 1)[1].rsplit("</svg>", 1)[0]
        cells += f'<g transform="translate({x},{y})">{inner}</g>'
    open("../images/characters/_cast_lineup.svg", "w", encoding="utf-8", newline="\n").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -10 2470 1840" width="2470" height="1840"><rect x="-10" y="-10" width="2470" height="1840" fill="#2a1f3d"/>{cells}</svg>')
    print("ok")
