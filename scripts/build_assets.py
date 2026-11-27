#!/usr/bin/env python3
"""Generate the terminal-themed SVG assets used by README.md.

Edit the data below (NOW, PROJECTS, STACK, LOG) and run:
    python3 scripts/build_assets.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

# ── palette ──────────────────────────────────────────────────────────────
BG, BAR, BORDER = "#0A0E14", "#11161D", "#1F2630"
TEXT, DIM = "#C9D1D9", "#6E7681"
GREEN, AMBER, CYAN, PURPLE, RED = "#4ADE80", "#F5B841", "#56D4DD", "#D2A8FF", "#FF7B72"
FONT = "ui-monospace, 'SF Mono', 'JetBrains Mono', Menlo, Consolas, 'Liberation Mono', monospace"
CW = 0.6  # approx monospace char width in em

# ── content ──────────────────────────────────────────────────────────────
NOW = [
    ("role", "Full Stack Developer Intern @ HobbyFi"),
    ("building", "fraud detection & agentic AI  (ScamShield, RingLeader)"),
    ("exploring", "system design, identity & privacy, Kubernetes"),
    ("studying", "Computer Science @ IIIT Dharwad"),
    ("based", "India"),
]

PROJECTS = [
    dict(slug="scam-shield", name="ScamShield", tag="fintech · ml",
         desc="Catches UPI payment scams before the money moves. Scores each payment 0-100 with plain-language reasons; high-risk ones get a blocking safety pause.",
         metric="LOW / MEDIUM / HIGH bands · analyst feedback loop",
         stack="typescript · python · ml · docker"),
    dict(slug="zipp", name="Zipp", tag="system design",
         desc="URL shortener built to study system design: cached redirects with zero DB writes, collision-free codes, async analytics on Redis Streams.",
         metric="17,243 req/s · p99 5.2 ms @ 2k rps",
         stack="node · fastify · redis · mongodb · k6"),
    dict(slug="ringleader", name="RingLeader", tag="agentic ai",
         desc="Autonomous fraud-investigation agent and analyst workbench. A 6-node LangGraph agent reasoning over TigerGraph with GraphRAG.",
         metric="20/20 benchmark cases evaluated",
         stack="langgraph · tigergraph · chromadb · react 19"),
    dict(slug="trust-trail", name="TrustTrail", tag="identity · research",
         desc="Privacy-aware federated login with accountable, purpose-bound disclosure. Keycloak SSO plus a tamper-evident ledger anchored on-chain.",
         metric="3 relying services · custom Keycloak mapper",
         stack="python · keycloak · java · solidity"),
    dict(slug="queuectl", name="QueueCTL", tag="infra · cli",
         desc="Persistent background-job queue driven from the CLI. Multi-process workers, atomic claiming, exponential backoff and a dead-letter queue.",
         metric="lease recovery survives SIGKILL",
         stack="node · sqlite (wal) · child processes"),
    dict(slug="orcaearn", name="OrcaEarn", tag="defi",
         desc="Stake ETH and earn ORCA token emissions in real time. Solidity contracts on Sepolia with a live React dashboard.",
         metric="live on sepolia testnet",
         stack="solidity · openzeppelin · react · ethers"),
]

STACK = [
    ("languages", "typescript  javascript  python  c++  solidity  java"),
    ("frontend", "react  next.js  tailwind  vite  redux"),
    ("backend", "node  fastify  express  fastapi  websockets"),
    ("data", "mongodb  postgres  redis  sqlite  chromadb"),
    ("ai", "langgraph  graphrag  llm agents  ml pipelines"),
    ("web3", "hardhat  ethers.js  openzeppelin  solana web3.js"),
    ("infra", "docker  kubernetes  github actions  linux  k6"),
]

LOG = [
    ("e41c0d2", "2026", "HEAD -> main", "fraud, identity & agentic AI", "ScamShield · TrustTrail · RingLeader · Zipp"),
    ("c8f92a1", "2026", "tag: hobbyfi", "Full Stack Developer Intern @ HobbyFi", "web + mobile features, components, APIs"),
    ("7d3e0b4", "2025", "tag: web3", "smart contracts & DeFi", "OrcaEarn · TollCrypt · Sol_Faucet"),
    ("4a821e9", "2024", "tag: fullstack", "first full-stack apps", "Minilink · SoulScript"),
    ("109ac32", "2023", "tag: genesis", "CS foundations", "C++ DSA · 300+ problems on LeetCode & GFG"),
]


# ── helpers ──────────────────────────────────────────────────────────────
def window(w, h, title, body, defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<defs>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#ffffff" opacity="0.018"/></pattern>
  {defs}
</defs>
<style>
  text {{ font-family: {FONT}; }}
  .cur {{ animation: blink 1.05s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
</style>
<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>
<path d="M0.5 36 V10.5 a10 10 0 0 1 10 -10 H{w-10.5} a10 10 0 0 1 10 10 V36 Z" fill="{BAR}"/>
<line x1="0.5" y1="36" x2="{w-0.5}" y2="36" stroke="{BORDER}"/>
<circle cx="20" cy="18" r="6" fill="#FF5F57"/><circle cx="40" cy="18" r="6" fill="#FEBC2E"/><circle cx="60" cy="18" r="6" fill="#28C840"/>
<text x="{w/2}" y="23" fill="{DIM}" font-size="12.5" text-anchor="middle">{escape(title)}</text>
{body}
<rect x="1" y="37" width="{w-2}" height="{h-38}" rx="9" fill="url(#scan)" pointer-events="none"/>
</svg>
"""


def t(x, y, s, fill=TEXT, size=15, extra=""):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" xml:space="preserve" {extra}>{escape(s)}</text>'


def spans(x, y, parts, size=15, extra=""):
    inner = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in parts)
    return f'<text x="{x}" y="{y}" font-size="{size}" xml:space="preserve" {extra}>{inner}</text>'


def prompt(path="~"):
    return [("➜ ", GREEN), (f"{path} ", CYAN)]


def reveal(i, begin, body):
    """Group that appears at `begin` seconds (once, then stays)."""
    return (f'<g opacity="0"><set attributeName="opacity" to="1" begin="{begin}s" fill="freeze"/>{body}</g>')


def typed(cid, x, y, cmd, begin, size=15, dur_per_char=0.045):
    """A command that types itself out using an animated clip."""
    width = len(cmd) * size * CW + 4
    dur = max(len(cmd) * dur_per_char, 0.2)
    clip = (f'<clipPath id="{cid}"><rect x="{x}" y="{y-size}" width="0" height="{size+6}">'
            f'<animate attributeName="width" from="0" to="{width:.0f}" begin="{begin}s" dur="{dur:.2f}s" '
            f'calcMode="discrete" values="{";".join(str(round(width*k/len(cmd))) for k in range(len(cmd)+1))}" fill="freeze"/>'
            f'</rect></clipPath>')
    return clip, t(x, y, cmd, TEXT, size, f'clip-path="url(#{cid})"'), begin + dur


def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    return lines + [cur] if cur else lines


# ── hero ─────────────────────────────────────────────────────────────────
def hero():
    W, H, X, LH = 1000, 405, 32, 26
    defs, body = [], []
    y, clock = 74, 0.3

    pre = "➜ ~ "
    body.append(spans(X, y, prompt()))
    c, txt, clock = typed("c1", X + len(pre) * 15 * CW, y, "whoami", clock)
    defs.append(c); body.append(txt)

    clock += 0.25
    y += 58
    body.append(reveal(0, clock, t(X, y, "Vijender Yadav", GREEN, 44, 'font-weight="700" filter="url(#glow)"')))
    y += 32
    body.append(reveal(0, clock + 0.15, spans(X, y, [
        ("full-stack engineer", TEXT), ("  ·  ", DIM), ("web3", PURPLE), ("  ·  ", DIM),
        ("agentic ai", AMBER), ("  ·  ", DIM), ("distributed systems", CYAN)], 16)))

    clock += 0.6
    y += 48
    body.append(reveal(0, clock - 0.05, spans(X, y, prompt())))
    c, txt, clock = typed("c2", X + len(pre) * 15 * CW, y, "cat now.txt", clock)
    defs.append(c); body.append(txt)

    clock += 0.2
    for k, v in NOW:
        y += LH
        body.append(reveal(0, clock, spans(X + 18, y, [(f"{k:<11}", AMBER), (v, TEXT)])))
        clock += 0.12

    y += 40
    body.append(reveal(0, clock + 0.1, spans(X, y, prompt() + [("_", GREEN)])
                       .replace(f'<tspan fill="{GREEN}">_</tspan>', f'<tspan class="cur" fill="{GREEN}">█</tspan>')))

    # right-side status panel
    px = 700
    body.append(f'<rect x="{px}" y="58" width="270" height="148" rx="6" fill="{BAR}" stroke="{BORDER}"/>')
    rows = [("status", "● online", GREEN), ("focus", "fintech · ai · web3", TEXT),
            ("tz", "IST (UTC+5:30)", TEXT), ("editor", "vscode", TEXT)]
    yy = 86
    body.append(t(px + 16, yy, "~/.status", DIM, 12.5))
    for k, v, col in rows:
        yy += 26
        body.append(spans(px + 16, yy, [(f"{k:<9}", DIM), (v, col)], 13.5))
    return window(W, H, "vijender@hobbyfi: ~ — zsh — 120×28", "\n".join(body), "\n".join(defs))


# ── project card ─────────────────────────────────────────────────────────
def card(p):
    W, H, X = 480, 250, 22
    body = []
    y = 74
    body.append(t(X, y, p["name"], GREEN, 24, 'font-weight="700" filter="url(#glow)"'))
    tag = f"[{p['tag']}]"
    body.append(t(W - X, y - 2, tag, PURPLE, 12.5, 'text-anchor="end"'))
    y += 12
    for line in wrap(p["desc"], 52):
        y += 21
        body.append(t(X, y, line, TEXT, 13.5))
    y = H - 54
    body.append(spans(X, y, [("▲ ", AMBER), (p["metric"], AMBER)], 13))
    y += 24
    body.append(spans(X, y, [("$ ", DIM), (p["stack"], CYAN)], 13))
    body.append(t(W - X, y, "open ↗", DIM, 12.5, 'text-anchor="end"'))
    return window(W, H, f"~/projects/{p['slug']}", "\n".join(body))


# ── stack ────────────────────────────────────────────────────────────────
def stack():
    W, X = 1000, 32
    H = 110 + len(STACK) * 28
    body = [spans(X, 70, prompt() + [("cat ~/.stack.toml", TEXT)])]
    y = 78
    for k, v in STACK:
        y += 28
        parts = [(f"{k:<11}", AMBER), ("= [ ", DIM)]
        items = v.split("  ")
        for i, it in enumerate(items):
            parts.append((f'"{it}"', GREEN if i % 2 == 0 else CYAN))
            if i < len(items) - 1:
                parts.append((", ", DIM))
        parts.append((" ]", DIM))
        body.append(spans(X, y, parts, 14.5))
    return window(W, H, "~/.stack.toml — vim", "\n".join(body))


# ── git log ──────────────────────────────────────────────────────────────
def log():
    W, X = 1000, 32
    H = 112 + len(LOG) * 52
    body = [spans(X, 70, prompt("~/journey") + [("git log --graph --oneline", TEXT)])]
    y = 80
    gx = X + 6
    top = y + 20
    for i, (h, yr, ref, msg, sub) in enumerate(LOG):
        y += 52
        color = GREEN if i == 0 else AMBER
        body.append(f'<circle cx="{gx}" cy="{y-5}" r="5" fill="{BG}" stroke="{color}" stroke-width="2"/>')
        body.append(spans(X + 24, y, [(h + " ", AMBER), (f"[{yr}] ", DIM), (f"({ref}) ", RED if i == 0 else PURPLE), (msg, TEXT)], 14.5))
        body.append(spans(X + 24, y + 20, [("└─ ", DIM), (sub, DIM)], 13.5))
    body.insert(1, f'<line x1="{gx}" y1="{top + 7}" x2="{gx}" y2="{y - 5}" stroke="{BORDER}" stroke-width="2"/>')
    return window(W, H, "~/journey — git", "\n".join(body))


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "hero.svg").write_text(hero())
    (OUT / "stack.svg").write_text(stack())
    (OUT / "log.svg").write_text(log())
    for p in PROJECTS:
        (OUT / f"card-{p['slug']}.svg").write_text(card(p))
    print("wrote", sorted(f.name for f in OUT.glob("*.svg")))


if __name__ == "__main__":
    main()
