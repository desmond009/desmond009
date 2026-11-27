#!/usr/bin/env python3
"""Generate the retro 8-bit SVGs used by README.md.

Edit the content blocks below and run:
    python3 scripts/build_retro.py

Fonts (embedded into each SVG so they render the same everywhere):
  Press Start 2P (CodeMan38) and VT323 (Peter Hull), both SIL Open Font License 1.1.
"""
import base64
import random
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"

# ── palette (PICO-8-ish) ─────────────────────────────────────────────────
BG, PANEL, INK = "#1D1B2E", "#2A2742", "#000000"
WHITE, LAV, GREY = "#F4F4F4", "#83769C", "#5F574F"
RED, ORANGE, YELLOW, GREEN = "#FF004D", "#FFA300", "#FFEC27", "#00E436"
BLUE, PINK, PEACH, BROWN, DGREEN = "#29ADFF", "#FF77A8", "#FFCCAA", "#AB5236", "#008751"

PX_W = 1.0    # Press Start 2P advance = 1em
VT_W = 0.40   # VT323 advance ≈ 0.4em

# ── content ──────────────────────────────────────────────────────────────
PLAYER = [
    ("NAME", "VIJENDER YADAV"),
    ("CLASS", "FULL-STACK ENGINEER"),
    ("GUILD", "HOBBYFI  (INTERN)"),
    ("SCHOOL", "IIIT DHARWAD  (CS)"),
    ("REGION", "INDIA"),
]
MOVES = ["FRAUD DETECTION", "AGENTIC AI", "SYSTEM DESIGN", "WEB3"]

INVENTORY = [
    ("LANG", ["TypeScript", "JavaScript", "Python", "C++", "Solidity", "Java"], YELLOW),
    ("FRONT", ["React", "Next.js", "Tailwind", "Vite", "Redux"], BLUE),
    ("BACK", ["Node.js", "Fastify", "Express", "FastAPI", "WebSockets"], GREEN),
    ("DATA", ["MongoDB", "Postgres", "Redis", "SQLite", "ChromaDB"], ORANGE),
    ("AI", ["LangGraph", "GraphRAG", "LLM agents", "ML pipelines"], PINK),
    ("WEB3", ["Hardhat", "Ethers.js", "OpenZeppelin", "Solana"], LAV),
    ("INFRA", ["Docker", "Kubernetes", "GH Actions", "Linux", "k6"], PEACH),
]

QUESTS = [
    dict(slug="zipp", kind="MAIN QUEST", n="01", name="ZIPP", tag="system design",
         desc="A URL shortener built to study system design. Cached redirects never write to the database; clicks stream through Redis.",
         loot="17,243 req/s  |  p99 5.2 ms", party="Node  Fastify  Redis  MongoDB  k6"),
    dict(slug="ringleader", kind="MAIN QUEST", n="02", name="RINGLEADER", tag="agentic ai",
         desc="An autonomous fraud investigator. A 6-node LangGraph agent explores a TigerGraph network and recommends the next action.",
         loot="20/20 benchmark cases evaluated", party="LangGraph  TigerGraph  ChromaDB  React"),
    dict(slug="scamshield", kind="MAIN QUEST", n="03", name="SCAMSHIELD", tag="fintech + ml",
         desc="Stops UPI payment scams before the money moves. Each payment gets a 0-100 risk score with plain-language reasons.",
         loot="High risk = 10-second safety pause", party="TypeScript  Python  ML  Docker"),
    dict(slug="trusttrail", kind="MAIN QUEST", n="04", name="TRUSTTRAIL", tag="identity",
         desc="Privacy-aware federated login. Each campus service gets only what it has a purpose for, logged to an on-chain-anchored ledger.",
         loot="Keycloak SSO + custom mapper", party="Python  Keycloak  Java  Solidity"),
    dict(slug="queuectl", kind="SIDE QUEST", n="05", name="QUEUECTL", tag="infra + cli",
         desc="A persistent job queue driven from the terminal. Atomic claiming, retries with backoff and a dead-letter queue.",
         loot="Survives SIGKILL via lease recovery", party="Node  SQLite  CLI"),
    dict(slug="orcaearn", kind="SIDE QUEST", n="06", name="ORCAEARN", tag="defi",
         desc="Stake ETH on Sepolia and earn 1 ORCA per second per ETH staked, with a live React rewards dashboard.",
         loot="Live on Sepolia testnet", party="Solidity  OpenZeppelin  React  Ethers"),
]

WORLD = [
    ("1-1", "2023", "FOUNDATIONS", "C++ and DSA, 300+ problems"),
    ("1-2", "2024", "FULL-STACK", "Minilink, SoulScript"),
    ("1-3", "2025", "WEB3", "OrcaEarn, TollCrypt"),
    ("1-4", "2026", "HOBBYFI", "Full Stack Developer Intern"),
    ("1-5", "NOW", "FRAUD + AI", "Zipp, RingLeader, ScamShield"),
]

# ── sprites ──────────────────────────────────────────────────────────────
SPRITE_COLORS = {"K": INK, "H": BROWN, "S": PEACH, "E": INK, "M": RED, "B": BLUE,
                 "Y": YELLOW, "P": GREY, "W": WHITE, "G": GREEN, "R": RED, "O": ORANGE, "L": LAV}
HERO = [
    "....KKKKK...",
    "..KKHHHHHKK.",
    ".KHHHHHHHHHK",
    ".KHHSSSSSHHK",
    ".KHSSESSESK.",
    ".KSSSSSSSSK.",
    "..KSSMMSSK..",
    "...KKSSKK...",
    "..KBBBBBBK..",
    ".KBBBYYBBBK.",
    "KSKBBBBBBKSK",
    "KSKBBBBBBKSK",
    ".K.KBBBBK.K.",
    "...KPPPPK...",
    "...KPKKPK...",
    "..KKK..KKK..",
]
HEART = [".RR.RR.", "RRRRRRR", "RRRRRRR", ".RRRRR.", "..RRR..", "...R..."]
COIN = [".KKKK.", "KYYYOK", "KYWYOK", "KYWYOK", "KYYYOK", ".KKKK."]
FLAG = ["WG...", "WGGG.", "WGGGG", "WGG..", "W....", "W....", "W....", "W...."]


def sprite(rows, x, y, s, extra=""):
    out = []
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in SPRITE_COLORS:
                out.append(f'<rect x="{x + i * s}" y="{y + j * s}" width="{s}" height="{s}" fill="{SPRITE_COLORS[ch]}"/>')
    return f'<g shape-rendering="crispEdges" {extra}>{"".join(out)}</g>'


# ── svg helpers ──────────────────────────────────────────────────────────
def _font(name):
    return base64.b64encode((ROOT / "fonts" / name).read_bytes()).decode()


FONTS = f"""@font-face {{ font-family: 'PS2P'; src: url(data:font/woff2;base64,{_font('PressStart2P-latin.woff2')}) format('woff2'); }}
  @font-face {{ font-family: 'VT'; src: url(data:font/woff2;base64,{_font('VT323-latin.woff2')}) format('woff2'); }}"""


def svg(w, h, label, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
<style>
  {FONTS}
  .p {{ font-family: 'PS2P', 'Courier New', monospace; }}
  .v {{ font-family: 'VT', 'Courier New', monospace; }}
  .blink {{ animation: blink 1s steps(1) infinite; }}
  .bob {{ animation: bob 0.8s steps(1) infinite; }}
  .tw {{ animation: tw 2.4s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @keyframes bob {{ 50% {{ transform: translateY(-4px); }} }}
  @keyframes tw {{ 0%, 70% {{ opacity: 1; }} 71%, 100% {{ opacity: 0.15; }} }}
</style>
<rect width="{w}" height="{h}" fill="{BG}"/>
{body}
</svg>
"""


def p(x, y, s, size, fill=WHITE, anchor="start", extra=""):
    cls = "p blink" if 'class="p blink"' in extra else "p"
    extra = extra.replace('class="p blink"', "")
    return f'<text class="{cls}" x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'


def v(x, y, s, size, fill=WHITE, anchor="start", extra=""):
    return f'<text class="v" x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" xml:space="preserve" {extra}>{escape(s)}</text>'


def shadow_p(x, y, s, size, fill, shade, off, anchor="start"):
    return p(x + off, y + off, s, size, shade, anchor) + p(x, y, s, size, fill, anchor)


def box(x, y, w, h, title=None, title_color=YELLOW, fill=PANEL):
    """RPG dialog box: notched white border, dark fill, optional title tab."""
    b = 4
    out = [
        f'<g shape-rendering="crispEdges">',
        f'<rect x="{x + b}" y="{y}" width="{w - 2 * b}" height="{h}" fill="{WHITE}"/>',
        f'<rect x="{x}" y="{y + b}" width="{w}" height="{h - 2 * b}" fill="{WHITE}"/>',
        f'<rect x="{x + b}" y="{y + b}" width="{w - 2 * b}" height="{h - 2 * b}" fill="{INK}"/>',
        f'<rect x="{x + 2 * b}" y="{y + 2 * b}" width="{w - 4 * b}" height="{h - 4 * b}" fill="{fill}"/>',
        "</g>",
    ]
    if title:
        tw = len(title) * 12 + 24
        out.append(f'<rect x="{x + 20}" y="{y - 8}" width="{tw}" height="20" fill="{INK}" shape-rendering="crispEdges"/>')
        out.append(p(x + 32, y + 8, title, 12, title_color))
    return "".join(out)


def wrap(s, width, size, adv):
    n = max(int(width / (size * adv)), 8)
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    return lines + ([cur] if cur else [])


def stars(w, h, n, seed=7, avoid=None):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y = rnd.randrange(0, w, 4), rnd.randrange(0, h, 4)
        s = rnd.choice([2, 2, 2, 4])
        c = rnd.choice([WHITE, WHITE, LAV, YELLOW, BLUE])
        delay = rnd.random() * 2.4
        out.append(f'<rect class="tw" style="animation-delay:-{delay:.2f}s" x="{x}" y="{y}" width="{s}" height="{s}" fill="{c}"/>')
    return f'<g shape-rendering="crispEdges">{"".join(out)}</g>'


def ground(w, y, h):
    out = [f'<rect x="0" y="{y}" width="{w}" height="8" fill="{GREEN}"/>',
           f'<rect x="0" y="{y + 8}" width="{w}" height="4" fill="{DGREEN}"/>',
           f'<rect x="0" y="{y + 12}" width="{w}" height="{h - y - 12}" fill="{BROWN}"/>']
    for i in range(0, w, 32):
        off = 16 if (i // 32) % 2 else 0
        out.append(f'<rect x="{i + off}" y="{y + 22}" width="4" height="4" fill="#7E2553"/>')
        out.append(f'<rect x="{i + 16 - off}" y="{y + 36}" width="4" height="4" fill="#7E2553"/>')
    return f'<g shape-rendering="crispEdges">{"".join(out)}</g>'


# ── title screen ─────────────────────────────────────────────────────────
def title():
    W, H = 1000, 460
    b = [stars(W, 330, 70)]
    b.append(p(30, 40, "1UP", 14, RED) + p(30, 62, "DESMOND009", 14, WHITE))
    b.append(p(W / 2, 40, "HI-SCORE", 14, RED, "middle") + p(W / 2, 62, "17243", 14, WHITE, "middle"))
    b.append(p(W - 30, 40, "CREDIT", 14, RED, "end") + p(W - 30, 62, "01", 14, WHITE, "end"))

    b.append(shadow_p(W / 2, 150, "VIJENDER", 60, YELLOW, RED, 6, "middle"))
    b.append(shadow_p(W / 2, 228, "YADAV", 60, YELLOW, RED, 6, "middle"))
    b.append(p(W / 2, 274, "FULL-STACK ENGINEER", 16, BLUE, "middle"))
    b.append(p(W / 2, 318, "PRESS START", 18, WHITE, "middle", 'class="p blink"'))
    ax = W / 2 - 130
    tri = "".join(f'<rect x="{ax}" y="{300 + i * 4}" width="{(3 - abs(i - 2)) * 4 + 2}" height="4" fill="{YELLOW}"/>' for i in range(5))
    b.append(f'<g class="blink" shape-rendering="crispEdges">{tri}</g>')

    # hero + props on the ground
    gy = 380
    b.append(ground(W, gy, H))
    b.append(sprite(HERO, 130, gy - 16 * 5, 5, 'class="bob"'))
    b.append(sprite(FLAG, W - 170, gy - 8 * 7, 7))
    for i, x in enumerate((240, 284, 328)):
        b.append(sprite(COIN, x, 336, 5, f'class="bob" style="animation-delay:-{i * 0.2:.1f}s"'))
    b.append(p(W / 2, H - 18, "(C) 2026 VIJENDER YADAV  ·  IIIT DHARWAD  ·  HOBBYFI", 10, WHITE, "middle"))
    return svg(W, H, "Title screen: Vijender Yadav, full-stack engineer. Press start.", "\n".join(b))


# ── character sheet ──────────────────────────────────────────────────────
def character():
    W = 1000
    b = []
    # left: player
    lx, lw = 20, 420
    rows = []
    y = 160
    for k, val in PLAYER:
        rows.append(v(lx + 30, y, f"{k:<7}", 26, LAV) + v(lx + 120, y, val, 26, WHITE))
        y += 32
    y += 18
    rows.append(p(lx + 30, y, "SPECIAL MOVES", 12, PINK))
    for m in MOVES:
        y += 30
        rows.append(f'<rect x="{lx + 32}" y="{y - 12}" width="8" height="8" fill="{YELLOW}" shape-rendering="crispEdges"/>')
        rows.append(v(lx + 50, y, m, 24, WHITE))
    left_h = y + 30 - 20

    # right: inventory
    rx, rw = 460, 520
    inv, iy = [], 70
    for label, items, color in INVENTORY:
        iy += 6
        inv.append(p(rx + 26, iy + 20, label, 11, color))
        cx = rx + 110
        for it in items:
            tw = len(it) * 20 * VT_W + 16
            if cx + tw > rx + rw - 22:
                cx = rx + 110
                iy += 34
            inv.append(f'<rect x="{cx}" y="{iy}" width="{tw:.0f}" height="28" fill="{INK}" stroke="{color}" stroke-width="2" shape-rendering="crispEdges"/>')
            inv.append(v(cx + 8, iy + 20, it, 20, WHITE))
            cx += tw + 8
        iy += 38
    right_h = iy + 12 - 20

    H = max(left_h, right_h) + 40
    b.append(box(lx, 20, lw, H - 40, "PLAYER 1"))
    b.append(sprite(HERO, lx + 30, 50, 5, 'class="bob"'))
    b.append(p(lx + 110, 74, "HP", 12, LAV))
    for i in range(5):
        b.append(sprite(HEART, lx + 110 + i * 34, 90, 4))
    b.append(p(lx + 110, 126, "STATUS", 10, LAV) + p(lx + 190, 126, "BUILDING", 10, GREEN))
    b += rows
    b.append(box(rx, 20, rw, H - 40, "INVENTORY"))
    b += inv
    return svg(W, H, "Character sheet: " + ", ".join(f"{k} {v_}" for k, v_ in PLAYER), "\n".join(b))


# ── quest card ───────────────────────────────────────────────────────────
def quest(q):
    W, H = 490, 290
    main = q["kind"] == "MAIN QUEST"
    b = [box(8, 16, W - 16, H - 24, f"{q['kind']} {q['n']}", YELLOW if main else BLUE)]
    b.append(shadow_p(34, 78, q["name"], 22, YELLOW if main else BLUE, RED if main else LAV, 3))
    b.append(v(W - 34, 76, f"[{q['tag']}]", 22, PINK, "end"))
    y = 112
    for line in wrap(q["desc"], W - 68, 22, VT_W):
        b.append(v(34, y, line, 22, WHITE))
        y += 22
    ly = H - 84
    b.append(sprite(COIN, 34, ly - 16, 3))
    b.append(p(58, ly - 4, "LOOT", 10, YELLOW) + v(116, ly - 2, q["loot"], 22, YELLOW))
    b.append(p(34, ly + 28, "PARTY", 10, BLUE) + v(116, ly + 30, q["party"], 22, BLUE))
    b.append(p(W - 34, H - 26, "A: OPEN", 10, WHITE, "end", 'class="p blink"'))
    return svg(W, H, f"{q['kind']} {q['n']}: {q['name']}. {q['desc']}", "\n".join(b))


# ── world map ────────────────────────────────────────────────────────────
def world():
    W, H = 1000, 330
    b = [stars(W, H, 30, seed=3), box(20, 20, W - 40, H - 40, "WORLD MAP")]
    n = len(WORLD)
    x0, x1, ny = 110, W - 110, 170
    step = (x1 - x0) / (n - 1)
    # dotted path
    dots = []
    x = x0
    while x < x1:
        dots.append(f'<rect x="{x:.0f}" y="{ny - 2}" width="8" height="4" fill="{LAV}"/>')
        x += 16
    b.append(f'<g shape-rendering="crispEdges">{"".join(dots)}</g>')
    for i, (lvl, yr, name, sub) in enumerate(WORLD):
        cx = x0 + i * step
        last = i == n - 1
        col = YELLOW if last else GREEN
        b.append(f'<rect x="{cx - 14}" y="{ny - 14}" width="28" height="28" fill="{INK}" shape-rendering="crispEdges"/>')
        b.append(f'<rect x="{cx - 10}" y="{ny - 10}" width="20" height="20" fill="{col}" shape-rendering="crispEdges"/>')
        b.append(p(cx, ny - 60, lvl, 12, WHITE, "middle"))
        b.append(p(cx, ny - 38, yr, 14, col, "middle"))
        b.append(p(cx, ny + 46, name, 11, col, "middle"))
        sy = ny + 72
        for line in wrap(sub, step - 16, 20, VT_W):
            b.append(v(cx, sy, line, 20, LAV, "middle"))
            sy += 20
        if not last:
            b.append(p(cx, ny + 4, "OK", 7, INK, "middle"))
    hx = x0 + (n - 1) * step
    b.append(sprite(HERO, hx + 22, ny + 14 - 64, 4, 'class="bob"'))
    b.append(p(hx + 22, ny - 66, "YOU ARE", 8, WHITE, "start", 'class="p blink"'))
    b.append(p(hx + 22, ny - 54, "HERE", 8, WHITE, "start", 'class="p blink"'))
    return svg(W, H, "World map: " + "; ".join(f"{yr} {name}" for _, yr, name, _ in WORLD), "\n".join(b))


# ── banners ──────────────────────────────────────────────────────────────
def banner(text, color, right=""):
    W, H = 1000, 70
    b = [sprite(COIN, 24, 22, 4), shadow_p(64, 46, text, 18, color, RED, 3)]
    if right:
        b.append(p(W - 24, 44, right, 10, LAV, "end"))
    b.append(f'<g shape-rendering="crispEdges">' + "".join(
        f'<rect x="{x}" y="{H - 6}" width="8" height="4" fill="{LAV}"/>' for x in range(24, W - 24, 16)) + "</g>")
    return svg(W, H, text, "\n".join(b))


def continue_screen():
    W, H = 1000, 250
    b = [stars(W, H, 40, seed=11)]
    b.append(shadow_p(W / 2, 96, "CONTINUE?", 40, WHITE, RED, 5, "middle"))
    # 9..0 countdown, loops every 10 s
    for i, d in enumerate(range(9, -1, -1)):
        b.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="0;{i/10:.2f};{(i+1)/10:.2f};1" '
                 f'calcMode="discrete" dur="10s" repeatCount="indefinite"/>{p(W / 2, 170, str(d), 52, YELLOW, "middle")}</g>')
    b.append(p(W / 2, 222, "INSERT COIN TO CONNECT", 14, PINK, "middle", 'class="p blink"'))
    return svg(W, H, "Continue? Insert coin to connect.", "\n".join(b))


def main():
    OUT.mkdir(exist_ok=True)
    files = {
        "rt-title.svg": title(),
        "rt-character.svg": character(),
        "rt-world.svg": world(),
        "rt-quests.svg": banner("QUEST LOG", YELLOW, "SELECT A QUEST TO OPEN THE REPO"),
        "rt-scores.svg": banner("HIGH SCORES", YELLOW, "LIVE FROM GITHUB"),
        "rt-continue.svg": continue_screen(),
    }
    for q in QUESTS:
        files[f"rt-quest-{q['slug']}.svg"] = quest(q)
    for name, s in files.items():
        (OUT / name).write_text(s)
    print("wrote", len(files), "files")


if __name__ == "__main__":
    main()
