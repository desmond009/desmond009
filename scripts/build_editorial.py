#!/usr/bin/env python3
"""Generate the editorial / magazine-style SVGs used by README.md.

Edit the content blocks below and run:
    python3 scripts/build_editorial.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

# ── palette & type ───────────────────────────────────────────────────────
PAPER, INK, MUTED, RULE, RED, TINT = "#F4EFE6", "#1A1714", "#6B6257", "#CFC5B4", "#B3261E", "#EBE4D7"
SERIF = "'Iowan Old Style', 'Palatino Linotype', Palatino, Charter, Georgia, 'Times New Roman', serif"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"

# Average glyph width as a fraction of font size (conservative, for wrapping).
W_REG, W_IT, W_BOLD, W_CAPS = 0.50, 0.47, 0.56, 0.68

# ── content ──────────────────────────────────────────────────────────────
ISSUE = "No. 26 · November 2026"
NAME = "Vijender Yadav"
DECK = "Full-stack engineer. Builds fraud detection, AI agents and backends that hold up under load."
BYLINE = "Full Stack Developer Intern, HobbyFi  ·  Computer Science, IIIT Dharwad  ·  India"
CONTENTS = [
    ("01", "Zipp", "17k redirects a second"),
    ("02", "RingLeader", "an agent that investigates fraud"),
    ("03", "ScamShield", "stopping scams before payment"),
    ("04", "TrustTrail", "a login that shares less"),
    ("05", "Briefs", "QueueCTL, OrcaEarn"),
]

COVER = dict(
    kicker="COVER STORY  ·  SYSTEM DESIGN",
    head="17,243 redirects a second, with no database writes",
    stand="Zipp is a URL shortener built as a system design exercise, with load-test numbers to back it up.",
    body=("Every redirect is served from a Redis cache, with negative caching for codes that don't exist, "
          "so the hot path never touches MongoDB. Short codes are generated without a “does it exist?” "
          "lookup, and click analytics flow through Redis Streams instead of the request. Against MongoDB "
          "alone, the same API process managed 6,444 requests a second."),
    stats=[("17,243", "req/s from one API process"), ("5.2 ms", "p99 at a steady 2,000 req/s"), ("99.8%", "cache hit rate")],
    stack="Node.js · TypeScript · Fastify · MongoDB · Redis · React 19 · k6",
)

STORIES = [
    dict(slug="ringleader", page="02", kicker="AGENTIC AI",
         head="Six nodes, one fraud investigation",
         stand=("A LangGraph agent walks a TigerGraph network of accounts, pulls context through GraphRAG "
                "and recommends the next action to an analyst."),
         fact=("20 / 20", "official benchmark cases evaluated"),
         stack="LangGraph · TigerGraph · ChromaDB · FastAPI · React 19"),
    dict(slug="scamshield", page="03", kicker="FINTECH  ·  ML",
         head="Stop the scam before the money moves",
         stand=("Each UPI-style payment gets a 0–100 risk score with plain-language reasons. High-risk ones "
                "trigger a 10-second safety pause and a retyped payee ID."),
         fact=("165k", "synthetic transactions to train and calibrate the model"),
         stack="TypeScript · Python · ML · Docker"),
]

LONGREAD = dict(
    kicker="IDENTITY  ·  RESEARCH", page="04",
    head="Signing in shouldn’t mean handing over everything",
    stand=("TrustTrail is a privacy-aware federated login for a university, built as a follow-up to "
           "Werner, Westphall & Westphall (2017), “Cloud Identity Management: A Survey on Privacy Strategies.”"),
    body=("Students sign in once through Keycloak, and the library, the learning system and the exam portal "
          "each receive only what they have a stated purpose for. A custom Keycloak mapper enforces that "
          "purpose binding. Every disclosure goes into a ledger whose entries are anchored on a local "
          "Hardhat chain, so they can be audited later."),
    quote="Accountable, purpose-bound disclosure.",
    stack="Python · Keycloak · Java · Solidity · Docker",
)

BRIEFS = [
    ("QueueCTL", "A job queue you drive from the terminal",
     "Jobs live in SQLite in WAL mode. Worker processes claim them atomically, failures retry with "
     "exponential backoff and end up in a dead-letter queue. Leases mean a worker killed with SIGKILL "
     "doesn’t lose its job."),
    ("OrcaEarn", "Stake ETH, earn by the second",
     "Stake ETH on Sepolia and earn 1 ORCA per second per ETH staked. Solidity contracts built on "
     "OpenZeppelin, with a React dashboard that tracks rewards live."),
]

TOOLKIT = [
    ("Languages", "TypeScript, JavaScript, Python, C++, Solidity, Java"),
    ("Frontend", "React, Next.js, Tailwind, Vite, Redux"),
    ("Backend", "Node.js, Fastify, Express, FastAPI, WebSockets"),
    ("Data", "MongoDB, PostgreSQL, Redis, SQLite, ChromaDB"),
    ("AI", "LangGraph, GraphRAG, LLM agents, ML pipelines"),
    ("Web3", "Hardhat, Ethers.js, OpenZeppelin, Solana Web3.js"),
    ("Infrastructure", "Docker, Kubernetes, GitHub Actions, Linux, k6"),
]

ARCHIVE = [
    ("2023", "Foundations", "C++ and DSA, 300+ problems on LeetCode and GFG"),
    ("2024", "First full-stack apps", "Minilink, SoulScript"),
    ("2025", "Into Web3", "OrcaEarn, TollCrypt, Sol_Faucet"),
    ("2026", "HobbyFi", "Full Stack Developer Intern"),
    ("Now", "Fraud, identity, agents", "Zipp, RingLeader, ScamShield, TrustTrail"),
]


# ── helpers ──────────────────────────────────────────────────────────────
def page(w, h, label, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
<defs>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.28  0 0 0 0 0.2  0 0 0 0.06 0"/>
  </filter>
</defs>
<rect width="{w}" height="{h}" fill="{PAPER}"/>
<rect width="{w}" height="{h}" filter="url(#grain)"/>
{body}
</svg>
"""


def t(x, y, s, size, fill=INK, family=SERIF, weight="400", style="normal", anchor="start", spacing="0", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'font-style="{style}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{spacing}" {extra}>{escape(s)}</text>')


def kicker(x, y, s, anchor="start"):
    return t(x, y, s, 11.5, RED, SANS, "700", spacing="2", anchor=anchor)


def rule(x1, y, x2, color=INK, w=1):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{w}"/>'


def wrap(s, width, size, factor):
    max_chars = max(int(width / (size * factor)), 8)
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > max_chars:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    return lines + ([cur] if cur else [])


def para(x, y, s, width, size, lh, factor=W_REG, **kw):
    out = []
    for i, line in enumerate(wrap(s, width, size, factor)):
        out.append(t(x, y + i * lh, line, size, **kw))
    return out, y + (len(out) - 1) * lh


def dropcap_para(x, y, s, width, size, lh):
    """Paragraph with a 3-line red drop cap."""
    cap, rest = s[0], s[1:]
    cap_w = size * 2.6
    out = [t(x - 2, y + lh * 2 - 2, cap, size * 4.1, RED, SERIF, "700")]
    # first 3 lines indented, then full width
    short = wrap(rest, width - cap_w, size, W_REG)
    first, remaining = short[:3], " ".join(short[3:])
    for i, line in enumerate(first):
        out.append(t(x + cap_w, y + i * lh, line, size))
    yy = y + 3 * lh
    if remaining:
        lines, yy_end = para(x, yy, remaining, width, size, lh)
        out += lines
        return out, yy_end
    return out, yy - lh


def head_lines(x, y, s, width, size, lh, **kw):
    return para(x, y, s, width, size, lh, factor=W_BOLD, weight="700", **kw)


# ── masthead ─────────────────────────────────────────────────────────────
def masthead():
    W, H, M = 1000, 440, 40
    b = []
    b.append(rule(M, 34, W - M, INK, 2.5))
    b.append(t(M, 56, "THE ENGINEERING REVIEW", 12, INK, SANS, "700", spacing="3"))
    b.append(t(W / 2, 56, "github.com/desmond009", 12, MUTED, SANS, anchor="middle", spacing="1"))
    b.append(t(W - M, 56, ISSUE.upper(), 12, INK, SANS, "700", anchor="end", spacing="2"))
    b.append(rule(M, 68, W - M, INK, 0.8))

    lx, lw = M, 600
    b.append(t(lx - 4, 168, NAME, 86, INK, SERIF, "700", spacing="-2"))
    b.append(rule(lx, 196, lx + 90, RED, 3))
    lines, y = para(lx, 236, DECK, lw - 30, 25, 33, W_IT, style="italic")
    b += lines
    b.append(t(lx, y + 52, BYLINE, 13, MUTED, SANS, spacing="0.4"))

    # contents column
    cx = 680
    b.append(f'<line x1="{cx - 22}" y1="96" x2="{cx - 22}" y2="{H - 50}" stroke="{RULE}"/>')
    b.append(kicker(cx, 104, "IN THIS ISSUE"))
    y = 112
    for num, title, sub in CONTENTS:
        y += 52
        b.append(t(cx, y, num, 28, RED, SERIF, "700"))
        b.append(t(cx + 46, y - 9, title, 17, INK, SERIF, "700"))
        b.append(t(cx + 46, y + 11, sub, 13.5, MUTED, SERIF, style="italic"))
    b.append(rule(M, H - 24, W - M, INK, 2.5))
    return page(W, H, f"{NAME}: {DECK}", "\n".join(b))


# ── cover story ──────────────────────────────────────────────────────────
def cover():
    W, M = 1000, 40
    b = [kicker(M, 48, COVER["kicker"]), t(W - M, 48, "PAGE 01", 11.5, MUTED, SANS, "700", anchor="end", spacing="2")]
    lines, y = head_lines(M, 104, COVER["head"], 600, 44, 50)
    b += lines
    lines, y = para(M, y + 46, COVER["stand"], 600, 19, 27, W_IT, style="italic", fill=MUTED)
    b += lines
    b.append(rule(M, y + 26, M + 600, RULE))
    lines, y = dropcap_para(M, y + 62, COVER["body"], 600, 16, 25)
    b += lines

    # stat column
    sx = 690
    top = 80
    b.append(f'<rect x="{sx - 24}" y="{top}" width="{W - M - sx + 24}" height="{3 * 108 + 8}" fill="{TINT}"/>')
    yy = top + 8
    for big, small in COVER["stats"]:
        yy += 62
        b.append(t(sx, yy, big, 46, RED, SERIF, "700", spacing="-1"))
        b.append(t(sx, yy + 26, small, 13.5, INK, SERIF, style="italic"))
        yy += 46
    H = max(y, yy) + 70
    b.append(rule(M, H - 46, W - M, INK, 0.8))
    b.append(t(M, H - 22, COVER["stack"], 13, MUTED, SANS, spacing="0.3"))
    b.append(t(W - M, H - 22, "Read the repo →", 13, RED, SANS, "700", anchor="end"))
    return page(W, H, f"Zipp: {COVER['head']}", "\n".join(b))


# ── half-width story ─────────────────────────────────────────────────────
def story(s):
    W, M, H = 490, 30, 430
    b = [kicker(M, 44, s["kicker"]), t(W - M, 44, f"PAGE {s['page']}", 11.5, MUTED, SANS, "700", anchor="end", spacing="2")]
    b.append(rule(M, 58, W - M, INK, 1.5))
    lines, y = head_lines(M, 104, s["head"], W - 2 * M, 31, 37)
    b += lines
    lines, y = para(M, y + 38, s["stand"], W - 2 * M, 16.5, 25, W_IT, style="italic", fill=INK)
    b += lines
    big, small = s["fact"]
    fy = H - 118
    b.append(rule(M, fy - 44, M + 40, RED, 3))
    b.append(t(M, fy, big, 40, RED, SERIF, "700", spacing="-1"))
    b.append(t(M, fy + 26, small, 13.5, MUTED, SERIF, style="italic"))
    b.append(rule(M, H - 46, W - M, RULE))
    b.append(t(M, H - 22, s["stack"], 12, MUTED, SANS, spacing="0.2"))
    return page(W, H, f"{s['head']}", "\n".join(b))


# ── long read ────────────────────────────────────────────────────────────
def longread():
    W, M = 1000, 40
    L = LONGREAD
    b = [kicker(M, 48, L["kicker"]), t(W - M, 48, f"PAGE {L['page']}  ·  THE LONG READ", 11.5, MUTED, SANS, "700", anchor="end", spacing="2")]
    b.append(rule(M, 62, W - M, INK, 1.5))
    lines, y = head_lines(M, 114, L["head"], 900, 40, 46)
    b += lines
    lines, y = para(M, y + 40, L["stand"], 900, 17.5, 26, W_IT, style="italic", fill=MUTED)
    b += lines
    top = y + 50
    lines, y1 = dropcap_para(M, top, L["body"], 560, 16, 25)
    b += lines
    # pull quote
    qx = 650
    b.append(rule(qx, top - 14, W - M, RED, 2.5))
    b.append(t(qx - 4, top + 50, "“", 80, RED, SERIF, "700"))
    ql, qy = para(qx + 34, top + 28, L["quote"], W - M - qx - 34, 25, 33, W_IT, style="italic")
    b += ql
    b.append(t(qx + 34, qy + 32, "— from the README", 13, MUTED, SANS, spacing="0.5"))
    b.append(rule(qx, qy + 54, W - M, RED, 2.5))
    H = max(y1, qy + 54) + 76
    b.append(rule(M, H - 46, W - M, INK, 0.8))
    b.append(t(M, H - 22, L["stack"], 13, MUTED, SANS, spacing="0.3"))
    b.append(t(W - M, H - 22, "Read the repo →", 13, RED, SANS, "700", anchor="end"))
    return page(W, H, f"TrustTrail: {L['head']}", "\n".join(b))


# ── briefs ───────────────────────────────────────────────────────────────
def briefs():
    W, M = 1000, 40
    b = [kicker(M, 48, "PAGE 05  ·  IN BRIEF")]
    b.append(rule(M, 62, W - M, INK, 1.5))
    colw = (W - 2 * M - 50) / 2
    ys = []
    for i, (name, head, body) in enumerate(BRIEFS):
        x = M + i * (colw + 50)
        b.append(t(x, 104, name.upper(), 12, RED, SANS, "700", spacing="2"))
        hl, y = head_lines(x, 136, head, colw, 23, 29)
        b += hl
        pl, y = para(x, y + 32, body, colw, 15.5, 24)
        b += pl
        ys.append(y)
    b.append(f'<line x1="{W / 2}" y1="92" x2="{W / 2}" y2="{max(ys)}" stroke="{RULE}"/>')
    H = max(ys) + 40
    return page(W, H, "In brief: QueueCTL and OrcaEarn", "\n".join(b))


# ── toolkit ──────────────────────────────────────────────────────────────
def toolkit():
    W, M = 1000, 40
    b = [kicker(M, 48, "THE TOOLKIT"), t(W - M, 48, "WHAT GOES INTO THE WORK", 11.5, MUTED, SANS, "700", anchor="end", spacing="2")]
    b.append(rule(M, 62, W - M, INK, 1.5))
    y = 62
    for i, (k, v) in enumerate(TOOLKIT):
        y += 44
        b.append(t(M, y, k, 19, INK, SERIF, "700"))
        b.append(t(250, y, v, 18, INK, SERIF, style="italic"))
        if i < len(TOOLKIT) - 1:
            b.append(rule(M, y + 17, W - M, RULE, 0.8))
    H = y + 40
    return page(W, H, "Toolkit: " + "; ".join(f"{k}: {v}" for k, v in TOOLKIT), "\n".join(b))


# ── archive ──────────────────────────────────────────────────────────────
def archive():
    W, M, H = 1000, 40, 220
    b = [kicker(M, 48, "BACK ISSUES"), t(W - M, 48, "THE ARCHIVE, 2023 – NOW", 11.5, MUTED, SANS, "700", anchor="end", spacing="2")]
    b.append(rule(M, 62, W - M, INK, 1.5))
    n = len(ARCHIVE)
    colw = (W - 2 * M) / n
    for i, (yr, title, sub) in enumerate(ARCHIVE):
        x = M + i * colw
        col = RED if i == n - 1 else INK
        b.append(t(x, 112, yr, 34, col, SERIF, "700"))
        b.append(t(x, 142, title, 15, INK, SERIF, "700"))
        sl, _ = para(x, 164, sub, colw - 22, 13, 19, W_IT, style="italic", fill=MUTED)
        b += sl
        if i:
            b.append(f'<line x1="{x - 14}" y1="84" x2="{x - 14}" y2="{H - 24}" stroke="{RULE}"/>')
    return page(W, H, "Archive: " + "; ".join(f"{a} {b_}" for a, b_, _ in ARCHIVE), "\n".join(b))


# ── section header & colophon ────────────────────────────────────────────
def section(title, right):
    W, M, H = 1000, 40, 70
    b = [kicker(M, 40, title), t(W - M, 40, right, 11.5, MUTED, SANS, "700", anchor="end", spacing="2"),
         rule(M, 54, W - M, INK, 1.5)]
    return page(W, H, title, "\n".join(b))


def colophon():
    W, M, H = 1000, 40, 190
    b = [rule(M, 30, W - M, INK, 2.5), kicker(M, 64, "LETTERS TO THE EDITOR")]
    b.append(t(M, 112, "Working on payments, fraud, AI agents or Web3?", 30, INK, SERIF, "700"))
    b.append(t(M, 146, "Write in. The links are just below.", 19, MUTED, SERIF, style="italic"))
    b.append(rule(M, H - 20, W - M, INK, 2.5))
    return page(W, H, "Letters to the editor", "\n".join(b))


def main():
    OUT.mkdir(exist_ok=True)
    files = {
        "ed-masthead.svg": masthead(),
        "ed-cover-zipp.svg": cover(),
        "ed-longread-trusttrail.svg": longread(),
        "ed-briefs.svg": briefs(),
        "ed-toolkit.svg": toolkit(),
        "ed-archive.svg": archive(),
        "ed-numbers.svg": section("BY THE NUMBERS", "FROM GITHUB, UPDATED LIVE"),
        "ed-colophon.svg": colophon(),
    }
    for s in STORIES:
        files[f"ed-story-{s['slug']}.svg"] = story(s)
    for name, svg in files.items():
        (OUT / name).write_text(svg)
    print("wrote", sorted(files))


if __name__ == "__main__":
    main()
