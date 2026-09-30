from scenes import *
from characters import SPECS
import json as _j
VOCAB.clear(); VOCAB.update(w["word"] for w in _j.load(open("../data/saga.json"))[0]["words"])

STYLE = ("Vibrant modern comic-book panel, Arabian Nights fantasy, mythic medieval Baghdad, bold clean ink outlines, cel shading, "
         "warm jewel-tone palette, cinematic angle, aimed at teenagers, no text")

LOCUS_STATIONS = {  # the 10 stations of the Crescent Lighthouse
    1: "the crescent-shaped sea-arch at the entrance", 2: "the worn doorstep with an iron anchor bolted into it",
    3: "the ship-lantern hanging on the left wall", 4: "the compass-rose mosaic on the floor",
    5: "Hakim's great brass telescope in the middle of the room", 6: "the rope-wrapped stone pillar on the right",
    7: "the round porthole window at the back, looking at the city", 8: "the spiral staircase",
    9: "the gallery balcony that rings the top of the tower", 10: "the great fire-mirror at the very top",
}

def crow(x, y, s=1.0):
    return g(P("M-30,0 Q-10,-40 20,-30 Q40,-26 44,-10 L60,-6 L44,0 Q20,12 -30,0 Z", "#15151f", 3, "#000")
             + P("M-10,-14 Q-40,-50 -60,-40 Q-40,-20 -10,-8 Z", "#23233a", 2.5, "#000") + C(30, -18, 4, "#ffe066", 0)
             + L(0, 2, -4, 16, "#f4c542", 3) + L(10, 2, 12, 16, "#f4c542", 3), x, y, s)

def zulmat_float(x, y, s=0.35):
    return f'<circle cx="{x}" cy="{y-110}" r="{130*s*2.4}" fill="#b48cff" opacity="0.18"/>' + g(human(SPECS["zulmat"], "neutral", ("up", "hold")), x, y, s)

def satchel_book(x, y, s=1.0):
    return g(f'<circle cx="0" cy="0" r="34" fill="#ffd84d" opacity="0.35"/>' + P("M-26,-18 h52 v36 h-52 Z", "#6b3a1e", 3) + P("M-22,-14 h44 v28 h-44 Z", "#fff6c9", 1.5)
             + L(0, -14, 0, 14, "#c8a060", 2) + T(-10, 4, "A", 10, "#c0262d") + T(11, 4, "O", 10, "#c0262d"), x, y, s)

def stone_legs(x, y, s):
    return g(P("M-34,-100 L34,-100 L40,0 L-40,0 Z", "#9a9a9a", 3) + P("M-20,-80 l10,20 l-6,20 M14,-60 l8,24", "none", 2, "#666"), x, y, s)

PANELS = []

# ---- 1 ANOMALY — Arch
a = night_sky(seed=11) + green_moon(345, 48, 24) + sea(y=250) + skyline(400, 250, "#221c4a", 5, dome=False)
a += lighthouse_ext(95, 300, 0.74)
a += P("M190,262 L400,262 L400,300 L190,300 Z", "#3a2f63", 3)
a += fig("zayn", 285, 262, 0.37, "shock", ("run_b", "point"), "stand")
a += caption(8, 8, 175, "Baghdad. The Night of the Crescent Eclipse.")
a += bubble(160, 72, 225, "The moon is GREEN? Every other night it's silver. That's an ANOMALY!", tail=(282, 150))
PANELS.append(dict(art=a))

# ---- 2 OMINOUS — Step
a = night_sky(seed=12, top="#0b0d26", bottom="#2a2150") + skyline(400, 210, "#15122e", 9)
a += "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#ffcf6b" opacity="{o}"/>' for x, y, o in [(40, 190, .9), (90, 170, .6), (150, 185, .3), (330, 175, .15)])
a += f'<rect x="0" y="210" width="400" height="90" fill="#6b5a7e"/>' + P("M110,300 L110,215 Q170,150 230,215 L230,300 Z", "#1a1433", 4)
a += P("M80,262 L260,262 L270,284 L70,284 Z", "#b9a88c", 3) + P("M170,250 v24 m-14,-8 q14,16 28,0 m-14,-24 h-8 h16", "none", 4, "#555")
a += crow(215, 250, 0.7) + P("M246,256 l12,10 l-4,-12", "#777", 1.5)
a += fig("layla", 140, 300, 0.36, "scared", ("down", "chin"))
a += fig("zayn", 330, 300, 0.36, "grin", ("down", "hip"), flip=True)
a += caption(8, 8, 190, "One by one, the lamps of the city go dark…")
a += bubble(10, 50, 190, "Crows at midnight… lamps dying… that's OMINOUS. Something bad is coming.", tail=(130, 175), border="#3d3d9e")
a += bubble(250, 70, 140, "Relax. I just deliver stuff.", tail=(325, 180), border="#f28c28")
PANELS.append(dict(art=a))

# ---- 3 IMPETUOUS — Lamp
a = stone_wall() + P("M300,40 L300,120 Q320,100 340,120 L340,40 Z", "#0e1238", 3) + L(320, 50, 324, 110, "#ffe9a8", 4)
a += L(110, 0, 110, 70, "#555", 4) + P("M85,70 h50 l-6,50 h-38 Z", "#d9a441", 3) + f'<circle cx="110" cy="96" r="34" fill="#ffd84d" opacity="0.45"/>'
a += g(human(SPECS["zayn"], "grin", ("up", "up"), "jump"), 104, 205, 0.34, rot=-12)
a += fig("layla", 290, 300, 0.4, "angry", ("down", "point"), flip=True)
a += sfx(60, 170, "SWI-I-ING!", 26, rot=-18)
a += bubble(170, 118, 150, "Get DOWN, you IMPETUOUS goat! You didn't even think!", tail=(282, 188), border="#3d3d9e", shout=False)
a += bubble(150, 18, 130, "Thinking is SLOW!", tail=(120, 70), border="#f28c28")
PANELS.append(dict(art=a))

# ---- 4 AUDACIOUS — Rug
a = night_sky(seed=14, top="#170c3a", bottom="#5a2a6b") + speed_lines(300, 40, 22, 20, 200, "#ffe066", 0.6)
a += "".join(sparkle(x, y, r) for x, y, r in [(260, 30, 8), (330, 70, 9), (220, 80, 6), (360, 20, 7), (290, 110, 6), (180, 40, 5), (380, 110, 6)])
a += f'<circle cx="300" cy="40" r="46" fill="#fff6c9" opacity="0.7"/>'
a += f'<rect x="0" y="200" width="400" height="100" fill="#6b5a7e"/>' + compass_floor(200, 262, 190, 34)
a += g(human(SPECS["zayn"], "determined", ("reach", "run_b"), "run"), 120, 250, 0.33, rot=62)
a += spark(262, 214, None, 12)
a += fig("layla", 360, 300, 0.33, "shock", ("up", "up"), flip=True)
a += sfx(90, 50, "KA-BOOM!", 36, "#ff7a1a", -10)
a += bubble(140, 118, 210, "Catching word-fire bare-handed?! That's AUDACIOUS!", tail=(345, 190), border="#3d3d9e")
PANELS.append(dict(art=a))

# ---- 5 BENEVOLENT — Heart (telescope)
a = stone_wall(c1="#5d4f73", c2="#4a3e5e") + f'<rect x="0" y="230" width="400" height="70" fill="#c7a86a"/>'
a += telescope(300, 190, 0.9)
a += g(inkwell(), 170, 262, 0.7) + g(qalam("happy"), 180, 238, 1.05)
a += "".join(sparkle(x, y, 7) for x, y in [(120, 120), (240, 100), (150, 70), (250, 160)])
a += fig("hakim", 330, 300, 0.36, "happy", ("down", "wave"), flip=True)
a += fig("zayn", 60, 300, 0.33, "amazed", ("shield", "down"))
a += bubble(210, 14, 180, "Fear not. Qalam is a BENEVOLENT djinn. He wishes only good.", tail=(325, 190), border="#1f2f6b")
a += bubble(8, 14, 150, "Say it true, and I'll become it!", tail=(190, 110), border="#15152a")
PANELS.append(dict(art=a))

# ---- 6 SKEPTICAL — Pillar
a = stone_wall(c1="#665780", c2="#51446a") + f'<rect x="0" y="240" width="400" height="60" fill="#c7a86a"/>'
a += rope_pillar(300, 0, 300, 60)
a += fig("layla", 250, 300, 0.4, "skeptic", ("hold", "chin"))
qm = P("M-30,-120 Q-30,-170 10,-170 Q50,-170 50,-130 Q50,-100 10,-86 L10,-50", "none", 26, "#15152a") + C(10, -18, 14, "#15152a", 0)
qm += E(-2, -150, 7, 9, "#ffe066", 0) + E(24, -150, 7, 9, "#ffe066", 0)
a += g(qm, 100, 280, 1.0)
a += bubble(150, 16, 240, "A talking ink-blob that turns into words? I'm SKEPTICAL. Prove it.", tail=(250, 175), border="#3d3d9e")
a += bubble(10, 180, 110, "Tough crowd.", tail=(90, 160), border="#15152a")
PANELS.append(dict(art=a))

# ---- 7 CANDID — Window
city = night_sky(seed=17) + skyline(400, 300, "#2a2a55", 7)
city += '<rect x="200" y="0" width="200" height="300" fill="#888" opacity="0.6" style="mix-blend-mode:saturation"/>'
a = stone_wall(c1="#5d4f73", c2="#4a3e5e") + window_round(200, 110, 88, city)
a += fig("hakim", 200, 300, 0.36, "sad", ("down", "down"))
a += fig("zayn", 60, 300, 0.34, "shock", ("down", "down"))
a += fig("layla", 345, 300, 0.34, "sad", ("chin", "down"), flip=True)
a += bubble(250, 10, 145, "I'll be CANDID: the Great Lexicon has shattered.", tail=(222, 200), border="#1f2f6b")
a += bubble(5, 10, 125, "So… that's bad-bad?", tail=(60, 190), border="#f28c28")
a += bubble(120, 212, 80, "Very bad.", tail=(185, 205), border="#1f2f6b", size=11)
PANELS.append(dict(art=a))

# ---- 8 DILIGENT — Stair
a = stone_wall(c1="#4f4466", c2="#3e3553") + spiral_stair(200, 0, 330, 220)
a += hushling(0.45).replace("translate(0.0,0.0)", "translate(90.0,300.0)") + hushling(0.38, 0.8).replace("translate(0.0,0.0)", "translate(150.0,300.0)")
a += fig("layla", 250, 150, 0.33, "determined", ("hold", "down"), "run", flip=True) + satchel_book(222, 108, 0.8)
a += fig("hakim", 320, 180, 0.33, "determined", ("down", "point"), flip=True)
a += bubble(190, 196, 205, "Layla, you are my most DILIGENT apprentice. Take the Satchel. Record every word!", tail=(310, 150), border="#1f2f6b")
a += bubble(8, 12, 185, "Already writing: ANOMALY, AUDACIOUS…", tail=(215, 100), border="#3d3d9e")
PANELS.append(dict(art=a))

# ---- 9 MALEVOLENT — Balcony
a = night_sky(seed=19, top="#12081f", bottom="#3a1f52") + skyline(400, 250, "#1a1230", 21)
a += zulmat_float(250, 140, 0.33)
a += P("M0,250 H400 V300 H0 Z", "#8a7a9a", 3) + "".join(f'<rect x="{x}" y="222" width="10" height="30" fill="#b9a8c9" stroke="{INK}" stroke-width="2"/>' for x in range(10, 400, 30))
a += P("M0,218 H400 V228 H0 Z", "#d8cbe0", 2.5)
a += hushling(0.35).replace("translate(0.0,0.0)", "translate(40.0,230.0)")
a += fig("hakim", 110, 300, 0.33, "angry", ("point", "down"))
a += stone_legs(110, 300, 0.33)
a += bubble(150, 186, 170, "Zulmat! His heart is MALEVOLENT: he wants every voice silenced but his own!", tail=(118, 212), border="#1f2f6b", size=11.5)
a += bubble(10, 12, 170, "Silence is the only perfect word.", tail=(226, 70), border="#3a1f52", scroll=True)
PANELS.append(dict(art=a))

# ---- 0 RESILIENT — Top (wide)
W = 1200
a = night_sky(W, 300, 20, "#0b0d26", "#2c3d7a") + sea(W, 250, 50)
a += "".join(sparkle(x, y, r) for x, y, r in [(820, 40, 8), (900, 90, 10), (980, 30, 7), (1060, 110, 9), (1140, 60, 8), (700, 60, 6)])
# left: fire mirror + half-stone Hakim
a += P("M0,230 H380 V300 H0 Z", "#d9a441", 3) + C(90, 150, 60, "#ffd84d", 4) + f'<circle cx="90" cy="150" r="110" fill="#ffd84d" opacity="0.22"/>'
a += fig("hakim", 230, 300, 0.38, "determined", ("down", "point")) + stone_legs(230, 300, 0.38)
a += '<rect x="185" y="190" width="95" height="110" fill="#999" opacity="0.55" style="mix-blend-mode:saturation"/>'
a += bubble(10, 10, 360, "Only one who uses a word truly can catch its spark. Catch all thousand… then find the thousand-and-first. Be RESILIENT: when you fall, bounce back!", tail=(232, 170), border="#1f2f6b", size=12)
# middle: leap
a += g(human(SPECS["zayn"], "grin", ("up", "reach"), "jump"), 560, 230, 0.36, rot=20)
a += g(human(SPECS["layla"], "scared", ("up", "up"), "jump"), 640, 250, 0.34, rot=30)
a += g(qalam("shock"), 700, 150, 0.5)
a += bubble(430, 20, 150, "Faster than a rumor!", tail=(560, 120), border="#f28c28")
a += bubble(640, 40, 150, "I HATE HEIGHTS!!", tail=(655, 150), border="#3d3d9e", shout=True)
# right: fish market below
a += "".join(P(f"M{x},250 L{x+40},210 L{x+80},250 Z", c, 3) for x, c in [(880, "#e0533b"), (960, "#f4c542"), (1040, "#2bb3a3"), (1120, "#e0533b")])
a += sfx(1010, 200, "SPLASH!", 40, "#63aee0", -6)
a += caption(880, 262, 310, "NEXT ▶ Chapter 2: A Djinn in the Fish Basket", 12.5, "#ffd23f")
PANELS.append(dict(art=a, wide=True))

# ------------------------------------------------------------------ teaching text
FRAMES = [
 dict(story="Night of the Crescent Eclipse. Zayn, rooftop courier, lands on the lighthouse arch with a package for old Hakim and freezes: the moon is glowing GREEN. It's never green. It's an anomaly: something that breaks the normal pattern.",
      hook="a-NOM-a-ly ≈ “a GNOME, a LIE”",
      link="1→2 · A lying garden GNOME (anomaly), the one odd statue in a row of perfect ones, swells up as tall as the lighthouse (Out of proportion) and opens his mouth. A thousand MEAN black crows burst out cawing “OH-MEAN-US!” and blot out the moon (Action + Substitution: omin-ous ≈ oh, mean us).",
      loci="Station 1 · ARCH. In the crescent keystone of the lighthouse doorway sits the lying gnome, wearing the green moon as a hat. He's the one thing that doesn't fit = ANOMALY.",
      prompt="Night harbor of a mythic Baghdad, a white crescent-shaped lighthouse; a 15-year-old courier boy with curly black hair and an orange headband stands on a rooftop ledge pointing up in shock at a glowing GREEN crescent moon; everything else is silver-blue"),
 dict(story="Layla opens the lighthouse door. A crow drops onto the doorstep, and across the city the lamps start going dark, one district at a time. “That's ominous,” she whispers. It feels like a warning that something bad is coming. Zayn shrugs it off.",
      hook="OMIN-ous ≈ OMEN-ous: full of bad omens",
      link="2→3 · The MEAN crows (ominous) dive-bomb the tower, but a tiny red IMP jumps onto one without looking (Action), rides it like a rocket and crashes headfirst into the stars (Exaggeration). “IMP-PET-YOU-us!” He pets you, then shoves you off the roof before anyone can think.",
      loci="Station 2 · STEP. On the anchor-bolted doorstep, a mean black crow stands dropping grey feathers, a bad omen right where you'd trip = OMINOUS.",
      prompt="Close-up of a lighthouse doorway at night, a black crow on the stone doorstep beside an iron anchor, a scholarly girl in an indigo headscarf peeking out nervously, behind them city lamps going dark one by one"),
 dict(story="A crack of light flashes over the Green Dome. Without thinking, Zayn leaps onto the hanging ship-lantern for a better look, and it swings wildly. Layla: “You impetuous goat!” Impetuous means acting fast without thinking.",
      hook="IMP-ET-uous ≈ an IMP who acts first",
      link="3→4 · The rocket-riding IMP (impetuous) smashes onto the Caliph's turban, snatches his crown and wears it as a tutu while dancing on the king's nose (Out of proportion + Substitution: AUD-acious ≈ ODD-daring). No one has ever dared something so bold.",
      loci="Station 3 · LAMP. The ship-lantern on the left wall swings like crazy with a red imp riding it, one who jumped before he looked = IMPETUOUS.",
      prompt="Inside a stone lighthouse, a boy swinging from a hanging brass ship-lantern like a monkey, the lantern light swaying; an annoyed scholar girl below points up at him; through a slit window a crack of golden light appears over a distant green dome"),
 dict(story="KA-BOOM! Above the city, the Great Lexicon explodes into a thousand golden sparks. One shoots straight into the lighthouse, and Zayn dives across the compass floor and catches it bare-handed. That's audacious: boldly daring, almost shockingly so.",
      hook="AUD-acious ≈ “OUT-DARE-cious”: the one who out-dares everyone",
      link="4→5 · The AUDACIOUS imp in his crown-tutu is chased by BENNY the Volunteer, a giant smiling baker as tall as a minaret (Out of proportion). Instead of punishing him, Benny showers him with a thousand warm loaves (Action + Exaggeration). BENE = good, VOL = wish: Benny wishes you well.",
      loci="Station 4 · RUG. Across the compass-rose mosaic, Zayn slides on his belly, catching a ball of fire in his bare hand. He out-dared the floor = AUDACIOUS.",
      prompt="Dynamic action shot: a thousand golden sparks explode across a purple night sky over mythic Baghdad; a boy dives horizontally across a compass-rose mosaic floor catching one glowing spark bare-handed; a girl behind him gasps, hands up"),
 dict(story="Zayn's package bursts open. From a cracked brass inkwell pours Qalam, a djinn made of living ink. He forms a giant hand to shield them. Hakim smiles: “Qalam is benevolent. He wishes only good.”",
      hook="BENE-volent ≈ BENNY the VOLUNTEER: good + wishing",
      link="5→6 · Benny's thousand loaves (benevolent) rain down on a giant TICK wearing a monocle (Substitution: skep-TICK-al). He squints, pokes every loaf with a magnifying glass, and says “Free bread? I DOUBT it” (Action + Exaggeration).",
      loci="Station 5 · HEART. From the lens of Hakim's great telescope in the middle of the room, a huge friendly ink-hand hands out bread to everyone = BENEVOLENT.",
      prompt="Old astronomer with a long silver beard beside a great brass telescope; a cracked brass inkwell on the floor from which a friendly djinn made of black calligraphy ink rises with glowing golden eyes, forming a protective giant hand over a startled boy"),
 dict(story="Layla folds her arms behind the rope-wrapped pillar. “A talking ink-blob that turns into words? I'm skeptical. Prove it.” Skeptical means doubting and not easily convinced. Qalam, stumped, becomes a giant question mark.",
      hook="SKEP-TICK-al ≈ the SKEPTIC TICK who doubts everything",
      link="6→7 · The doubting TICK (skeptical) pokes a giant piece of CANDY so hard it bursts and blurts out the plain truth: “CANDY DID IT! I ate your homework!” (Substitution: CAND-id ≈ candy-did; Action). No sugar-coating from this candy.",
      loci="Station 6 · PILLAR. Climbing the rope-wrapped pillar on the right, a monocled tick squints at every knot, doubting it will hold = SKEPTICAL.",
      prompt="A skeptical 15-year-old girl scholar in an indigo headscarf, arms crossed, raised eyebrow, leaning on a rope-wrapped stone pillar; opposite her a small ink djinn has twisted itself into a question-mark shape"),
 dict(story="Through the round window the kids watch the city turn grey. Hakim speaks candidly, honest and direct: “The Great Lexicon has shattered. Without its words, the city will forget how to think.”",
      hook="CAND-id ≈ “CANDY DID it”: an honest confession",
      link="7→8 · The honest candy (candid) is gulped by a DILL pickle gentleman in a top hat (Substitution: DIL-igent ≈ dill-gent) who then works all night with eight arms, sorting every single sprinkle by color and never stopping (Exaggeration + Action).",
      loci="Station 7 · WINDOW. A giant candy is pressed against the round porthole window, yelling the truth through the glass: “Candy DID it!” = CANDID.",
      prompt="Silhouettes of an old astronomer and two teenagers looking out a round brass porthole window; outside, half of a colorful Arabian-Nights city skyline is draining to grey"),
 dict(story="Hushlings (mouthless ink-shadows) ooze up the spiral stair. Hakim hands Layla the Satchel of Empty Pages: “You are my most diligent apprentice. Record every word!” She's already writing while running. Diligent means hard-working and careful.",
      hook="DILI-gent ≈ the DILL-pickle GENTleman who never stops working",
      link="8→9 · The pickle's perfect sprinkle-piles (diligent) are kicked over by a spiky MALL-MONSTER (Substitution: MAL-evolent ≈ mall-violent) who stomps through the building wishing harm on everyone (Action + Out of proportion). MAL = bad, VOL = wish: the opposite of Benny.",
      loci="Station 8 · STAIR. On every step of the spiral stair a dill-pickle scribe is writing, writing, writing without a break = DILIGENT.",
      prompt="A spiral stone staircase inside a lighthouse; shadowy black ink creatures with no mouths and glowing hollow eyes ooze up from below; at the top a determined girl runs while writing in a glowing leather book as an old astronomer hands her its strap"),
 dict(story="On the balcony they see him: Grand Vizier Zulmat, floating above the Green Dome in a violet glow. “His heart is malevolent,” Hakim growls. “He wants every voice silenced but his own.” The Hushlings grab Hakim's feet, and he starts turning to stone.",
      hook="MAL-evolent ≈ MALL-VIOLENT: bad + wishing",
      link="9→10 · The MALL-monster (malevolent) stomps a rubber ball flat. It pops right back up (“RE-SILLY-ENT!”), boings him all the way to the moon, and keeps bouncing (Action + Exaggeration + Substitution: re-SIL-ient ≈ re-silly-bounce).",
      loci="Station 9 · BALCONY. Leaning over the balcony rail is a spiky mall-monster wearing Zulmat's mouthless silver mask, dripping ink and wishing harm = MALEVOLENT.",
      prompt="From a lighthouse balcony at night, a tall masked sorcerer-vizier in violet-black robes floats menacingly above a distant green dome, glowing with pale violet light; an angry old astronomer points at him while his feet begin turning to grey stone and an ink creature climbs the railing"),
 dict(story="At the fire-mirror on the very top, half-stone Hakim gives them the rule of the quest: “Only one who uses a word truly can catch its spark. Catch all thousand, then find the thousand-and-first. Be resilient!” Resilient means able to bounce back. Zayn grabs Layla and leaps into the night.",
      hook="re-SIL-ient ≈ RE-SILLY-ENT: the silly ball that always bounces back",
      link="10→11 (to Chapter 2) · The bouncing ball (resilient) splashes down into a fish basket, and a giant fish's jaw drops so wide in disbelief (IN-CRED-ulous: gives it no credit) that the whole ball rolls inside (Out of proportion). You'll meet him at the Fish Market.",
      loci="Station 10 · TOP. On the blazing fire-mirror at the summit, a rubber ball keeps bouncing back up no matter how many times it's knocked off = RESILIENT.",
      prompt="Wide cinematic panel: left, a half-stone old astronomer at a blazing golden fire-mirror atop a lighthouse; center, a boy with an orange headband grabs a screaming girl scholar and leaps off the top into the night, a small ink djinn tumbling after them; right, golden sparks rain over a harbor fish market with striped awnings far below"),
]
