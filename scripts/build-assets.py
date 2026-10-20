#!/usr/bin/env python3
"""
Builds every animated SVG panel in assets/ for the profile README
(all except contribution-snake.svg, which scripts/build-heatmap-svg.mjs
renders from real GitHub data).

Run from the repo root:  python3 scripts/build-assets.py
Standard library only. Edit the palette or the copy here, then re-run.
"""

import base64
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")

# ---- Royal blue palette -------------------------------------------------
BG = "#0B1230"      # card surface
DEEP = "#070B1F"    # deepest navy
HERO = "#12215C"    # hero light centre
GLOW = "#2647C8"    # royal glow fields
MDEEP = "#172B78"   # muted deep blue (fills, secondary badges)
ACC = "#6F8FF7"     # royal accent (labels, strokes)
LIGHT = "#B9CBFF"   # periwinkle highlight
TEXT = "#EEF2FF"    # near-white text
MUTE = "#A5AFCB"    # secondary text
CHIP = "#111D4A"    # chip / tile fill
ROYAL = "#4169E1"   # pure royal blue
GOLD = "#C9A27A"    # warm counter-accent

FONTS = """    .{p}-serif {{ font-family: Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif; }}
    .{p}-mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }}
    .{p}-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}"""


def fonts(p):
    return FONTS.format(p=p)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg.strip() + "\n")
    print(f"wrote assets/{name} ({os.path.getsize(path):,} bytes)")


# ---- Section titles -----------------------------------------------------
def title(slug, num, label, lead, italic, right):
    p = "t" + slug[:2]
    aria = esc(f"{num} {label.title()}: {lead}{italic}").replace("'", "&#x27;")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" width="1200" height="120" role="img" aria-label="{aria}">
  <defs>
    <linearGradient id="{p}-line" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="1160" y2="0">
      <stop offset="0" stop-color="{ACC}"/><stop offset=".6" stop-color="{GLOW}"/><stop offset="1" stop-color="{GLOW}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="{p}-sheen" gradientUnits="userSpaceOnUse" x1="-300" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="{LIGHT}"/><stop offset=".5" stop-color="#FFFFFF"/><stop offset="1" stop-color="{LIGHT}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;1500 0;1500 0" keyTimes="0;.4;1" dur="7s" begin="1.5s" repeatCount="indefinite"/>
    </linearGradient>
    <radialGradient id="{p}-pulse"><stop offset="0" stop-color="{TEXT}"/><stop offset=".5" stop-color="{LIGHT}" stop-opacity=".6"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></radialGradient>
  </defs>
  <style>
{fonts(p)}
    .{p}-in {{ animation: {p}-in 1.1s cubic-bezier(.16,1,.3,1) both; }}
    .{p}-d2 {{ animation-delay: .2s; }} .{p}-d3 {{ animation-delay: .45s; }}
    .{p}-draw {{ stroke-dasharray: 1200; stroke-dashoffset: 1200; animation: {p}-draw 1.8s cubic-bezier(.65,0,.35,1) .5s forwards; }}
    @keyframes {p}-in {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes {p}-draw {{ to {{ stroke-dashoffset: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .{p}-in {{ animation: none; }} .{p}-draw {{ animation: none; stroke-dashoffset: 0; }} }}
  </style>
  <g class="{p}-in">
    <text class="{p}-mono" x="40" y="34" font-size="12" letter-spacing="3" fill="{ACC}"><tspan fill="{LIGHT}">{num}</tspan>   {esc(label)}</text>
  </g>
  <g class="{p}-in {p}-d2">
    <text class="{p}-serif" x="38" y="84" font-size="44" font-weight="300" letter-spacing="-1" fill="{TEXT}">{esc(lead)}<tspan font-style="italic" fill="url(#{p}-sheen)">{esc(italic)}</tspan></text>
  </g>
  <g class="{p}-in {p}-d3">
    <text class="{p}-mono" x="1160" y="34" text-anchor="end" font-size="10.5" letter-spacing="2.4" fill="{MUTE}">{esc(right)}</text>
  </g>
  <path class="{p}-draw" d="M40 106 H1160" stroke="url(#{p}-line)" stroke-width="1"/>
  <circle cx="40" cy="106" r="7" fill="url(#{p}-pulse)" opacity="0">
    <animate attributeName="cx" values="40;1160" dur="6s" begin="2.3s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".45 0 .55 1"/>
    <animate attributeName="opacity" values="0;1;0" keyTimes="0;.15;1" dur="6s" begin="2.3s" repeatCount="indefinite"/>
  </circle>
</svg>"""


TITLES = [
    ("about", "01", "ABOUT", "Hello, I'm ", "Komal.", "WHO I AM"),
    ("recognition", "02", "RECOGNITION", "Proof, ", "on the record.", "NATIONAL STAGE"),
    ("experience", "03", "EXPERIENCE", "Engineering for ", "live markets.", "INDUSTRY"),
    ("work", "04", "SELECTED WORK", "Built to ", "survive production.", "SHIPPED"),
    ("toolkit", "05", "TOOLKIT", "The tools ", "I reach for.", "STACK"),
    ("commits", "06", "COMMIT LOG", "A year ", "of building.", "LIVE DATA"),
    ("education", "07", "EDUCATION", "Foundations, ", "with distinction.", "ACADEMICS"),
    ("connect", "08", "CONNECT", "Let's build something ", "that ships.", "OPEN INBOX"),
]


# ---- Hero ---------------------------------------------------------------
def hero():
    with open(os.path.join(ROOT, "scripts", "portrait.jpg"), "rb") as f:
        photo = base64.b64encode(f.read()).decode()

    parts = [(560, 120, 1.4, 4.2, 0), (700, 70, 1.1, 5.6, 1), (1120, 380, 1.6, 4.8, 2), (760, 420, 1.2, 6, .5),
             (1060, 60, 1.3, 5, 3), (640, 250, 1, 4.4, 2.5), (480, 60, 1.2, 5.2, 1.7), (1160, 210, 1.1, 4.6, 3.6),
             (720, 180, 1.3, 5.8, 4.1), (420, 440, 1.0, 6.2, 2.2)]
    particles = "\n".join(
        f'      <circle cx="{x}" cy="{y}" r="{r}"><animate attributeName="opacity" values="0;.9;0" dur="{d}s" begin="{b}s" repeatCount="indefinite"/>'
        f'<animate attributeName="cy" values="{y};{y - 24}" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>'
        for x, y, r, d, b in parts)

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 480" width="1200" height="480" role="img" aria-labelledby="hero-title hero-desc">
  <title id="hero-title">Komal Mittal — Agents that listen. Systems that hold.</title>
  <desc id="hero-desc">Agentic AI and backend engineer. B.Tech in Information Technology at Bhagwan Parshuram Institute of Technology, New Delhi, CGPA 9.32. Meesho ScriptedBy Her 2.0 Top 50 and Flipkart GRiD 8.0 Semi-Finalist.</desc>

  <defs>
    <radialGradient id="hero-bg" cx="72%" cy="38%" r="80%">
      <stop offset="0" stop-color="{HERO}"/>
      <stop offset=".55" stop-color="{BG}"/>
      <stop offset="1" stop-color="{DEEP}"/>
    </radialGradient>
    <radialGradient id="hero-light-a" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{GLOW}" stop-opacity=".62"/>
      <stop offset="1" stop-color="{GLOW}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="hero-light-b" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{ACC}" stop-opacity=".26"/>
      <stop offset="1" stop-color="{ACC}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="hero-name-grad" gradientUnits="userSpaceOnUse" x1="60" y1="0" x2="400" y2="0">
      <stop offset="0" stop-color="{TEXT}"/>
      <stop offset=".55" stop-color="{LIGHT}"/>
      <stop offset="1" stop-color="{ACC}"/>
    </linearGradient>
    <linearGradient id="hero-sheen" gradientUnits="userSpaceOnUse" x1="-260" y1="0" x2="-40" y2="0">
      <stop offset="0" stop-color="{TEXT}" stop-opacity="0"/>
      <stop offset=".5" stop-color="#FFFFFF" stop-opacity=".85"/>
      <stop offset="1" stop-color="{TEXT}" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;760 0;760 0" keyTimes="0;.35;1" dur="8s" begin="3s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="hero-scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{LIGHT}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{LIGHT}" stop-opacity=".07"/>
      <stop offset="1" stop-color="{LIGHT}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="hero-rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACC}" stop-opacity="0"/>
      <stop offset=".2" stop-color="{LIGHT}"/>
      <stop offset=".75" stop-color="{ROYAL}"/>
      <stop offset="1" stop-color="{ROYAL}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="hero-orbit-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{LIGHT}" stop-opacity=".6"/>
      <stop offset="1" stop-color="{GLOW}" stop-opacity=".05"/>
    </linearGradient>
    <pattern id="hero-grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{ACC}" stroke-opacity=".08" stroke-width="1"/>
    </pattern>
    <radialGradient id="hero-grid-fade" cx="68%" cy="45%" r="55%">
      <stop offset="0" stop-color="#fff"/>
      <stop offset="1" stop-color="#000"/>
    </radialGradient>
    <mask id="hero-grid-mask">
      <rect width="1200" height="480" fill="url(#hero-grid-fade)"/>
    </mask>
    <filter id="hero-glow" x="-20%" y="-200%" width="140%" height="500%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="hero-arch"><path d="M847 380 V202 A118 118 0 0 1 1083 202 V380 Z"/></clipPath>
    <radialGradient id="hero-photo-wash" cx="50%" cy="30%" r="80%">
      <stop offset="0" stop-color="#E4EAFF"/>
      <stop offset=".6" stop-color="#A3B8F4"/>
      <stop offset="1" stop-color="#3355C4"/>
    </radialGradient>
    <linearGradient id="hero-photo-grade" x1="0" y1="0" x2="0" y2="1">
      <stop offset=".55" stop-color="#0E1A45" stop-opacity="0"/>
      <stop offset=".85" stop-color="#0E1A45" stop-opacity=".45"/>
      <stop offset="1" stop-color="{DEEP}" stop-opacity=".85"/>
    </linearGradient>
    <linearGradient id="hero-photo-sheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset=".5" stop-color="#FFFFFF" stop-opacity=".22"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="hero-frame-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{LIGHT}"/>
      <stop offset=".5" stop-color="{ROYAL}"/>
      <stop offset="1" stop-color="{GOLD}"/>
    </linearGradient>
    <clipPath id="hero-clip"><rect width="1200" height="480" rx="20"/></clipPath>
  </defs>

  <style>
{fonts("hero")}

    .hero-rise {{ animation: hero-rise 1.4s cubic-bezier(.16,1,.3,1) both; }}
    .hero-fade {{ animation: hero-fade 1.6s cubic-bezier(.16,1,.3,1) both; }}
    .d1 {{ animation-delay: .15s; }} .d2 {{ animation-delay: .35s; }} .d3 {{ animation-delay: .6s; }}
    .d4 {{ animation-delay: .9s; }} .d5 {{ animation-delay: 1.2s; }} .d6 {{ animation-delay: 1.5s; }}

    .hero-draw {{ stroke-dasharray: 900; stroke-dashoffset: 900; animation: hero-draw 2.4s cubic-bezier(.65,0,.35,1) .9s forwards; }}
    .hero-signal {{ stroke-dasharray: 500; stroke-dashoffset: 500; animation: hero-draw 2.2s cubic-bezier(.65,0,.35,1) 2.2s forwards; }}

    .hero-portrait {{ animation: hero-photo 1.6s cubic-bezier(.16,1,.3,1) .5s both; }}
    .hero-frame {{ stroke-dasharray: 900; stroke-dashoffset: 900; animation: hero-draw 2.2s cubic-bezier(.65,0,.35,1) 1s forwards; }}
    @keyframes hero-photo {{ from {{ opacity: 0; transform: translateY(22px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes hero-rise {{ from {{ opacity: 0; transform: translateY(18px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes hero-fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes hero-draw {{ to {{ stroke-dashoffset: 0; }} }}

    /* Static, fully visible composition for anyone who prefers no motion */
    @media (prefers-reduced-motion: reduce) {{
      .hero-rise, .hero-fade, .hero-portrait {{ animation: none; }}
      .hero-frame {{ animation: none; stroke-dashoffset: 0; }}
      .hero-draw, .hero-signal {{ animation: none; stroke-dashoffset: 0; }}
    }}
  </style>

  <g clip-path="url(#hero-clip)">
    <!-- Canvas -->
    <rect width="1200" height="480" fill="url(#hero-bg)"/>

    <!-- Slow light fields -->
    <ellipse cx="900" cy="140" rx="420" ry="300" fill="url(#hero-light-a)">
      <animateTransform attributeName="transform" type="translate" values="0 0; -60 30; 0 0" dur="22s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1; .45 0 .55 1"/>
    </ellipse>
    <ellipse cx="180" cy="460" rx="360" ry="220" fill="url(#hero-light-b)">
      <animateTransform attributeName="transform" type="translate" values="0 0; 70 -25; 0 0" dur="28s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1; .45 0 .55 1"/>
    </ellipse>

    <!-- Technical grid -->
    <rect width="1200" height="480" fill="url(#hero-grid)" mask="url(#hero-grid-mask)"/>

    <!-- Slow scan line across the grid -->
    <rect x="0" y="-140" width="1200" height="140" fill="url(#hero-scan)">
      <animate attributeName="y" values="-140;480" dur="11s" begin="2s" repeatCount="indefinite"/>
    </rect>

    <!-- Drifting particles -->
    <g fill="{LIGHT}">
{particles}
    </g>

    <!-- Orbital system circling the portrait -->
    <g transform="translate(965 232)" class="hero-fade d3">
      <circle r="212" fill="none" stroke="{ACC}" stroke-opacity=".12" stroke-dasharray="1 10">
        <animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="140s" repeatCount="indefinite"/>
      </circle>
      <circle r="190" fill="none" stroke="url(#hero-orbit-grad)" stroke-width="1"/>
      <circle r="160" fill="none" stroke="{ACC}" stroke-opacity=".18" stroke-dasharray="2 7"/>
      <g>
        <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="95s" repeatCount="indefinite"/>
        <circle cx="0" cy="160" r="2.5" fill="{TEXT}"/>
        <circle cx="-160" cy="0" r="2" fill="{ACC}" fill-opacity=".7"/>
      </g>
    </g>

    <!-- Portrait -->
    <g class="hero-portrait">
      <path d="M835 392 V202 A130 130 0 0 1 1095 202 V392 Z" fill="none" stroke="{ACC}" stroke-opacity=".25">
        <animate attributeName="stroke-opacity" values=".15;.5;.15" dur="5s" repeatCount="indefinite"/>
      </path>
      <g clip-path="url(#hero-arch)">
        <rect x="847" y="84" width="236" height="296" fill="url(#hero-photo-wash)"/>
        <image href="data:image/jpeg;base64,{photo}" x="847" y="98" width="236" height="296" preserveAspectRatio="xMidYMin slice" style="mix-blend-mode:multiply"/>
        <rect x="847" y="84" width="236" height="296" fill="url(#hero-photo-grade)"/>
        <rect x="700" y="84" width="90" height="296" fill="url(#hero-photo-sheen)" transform="skewX(-14)">
          <animate attributeName="x" values="700;1260;1260" keyTimes="0;.3;1" dur="9s" begin="3.5s" repeatCount="indefinite"/>
        </rect>
      </g>
      <path class="hero-frame" d="M847 380 V202 A118 118 0 0 1 1083 202 V380 Z" fill="none" stroke="url(#hero-frame-grad)" stroke-width="1.5"/>
      <path d="M829 290 v-22 h22" fill="none" stroke="{LIGHT}" stroke-opacity=".8"/>
      <path d="M1101 398 v-22 M1101 398 h-22" fill="none" stroke="{LIGHT}" stroke-opacity=".8"/>
    </g>

    <g transform="translate(965 232)" class="hero-fade d4">
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="70s" repeatCount="indefinite"/>
        <circle cx="190" cy="0" r="3.5" fill="{LIGHT}" filter="url(#hero-glow)"/>
        <circle cx="-134" cy="-134" r="2" fill="{ACC}"/>
      </g>
      <!-- Node labels: the layers I work across -->
      <g class="hero-mono" font-size="10.5" letter-spacing="1.6" fill="{MUTE}">
        <g transform="translate(-118 -152)"><circle r="3" fill="{ACC}"/><text x="10" y="4">AGENTS</text></g>
        <g transform="translate(150 -96)"><circle r="3" fill="{ACC}"/><text x="10" y="4">API</text></g>
        <g transform="translate(150 110)"><circle r="3" fill="{ACC}"/><text x="10" y="4">QUEUE</text></g>
        <g transform="translate(-158 40)"><circle r="3" fill="{ACC}"/><text x="-14" y="4" text-anchor="end">VOICE</text></g>
      </g>
    </g>

    <!-- Signal path drawing itself through the composition -->
    <path class="hero-signal" d="M600 342 C 680 338, 740 330, 780 318 S 828 300, 847 300" fill="none" stroke="{ACC}" stroke-opacity=".5" stroke-width="1.2"/>
    <circle cx="600" cy="342" r="3" fill="{TEXT}" filter="url(#hero-glow)" opacity=".9">
      <animateMotion dur="5s" repeatCount="indefinite" begin="4.4s" path="M0 0 C 80 -4, 140 -12, 180 -24 S 228 -42, 247 -42" keyPoints="0;1" keyTimes="0;1" calcMode="spline" keySplines=".45 0 .55 1"/>
    </circle>

    <!-- Terminal indicator -->
    <g class="hero-fade d1" transform="translate(72 64)">
      <rect width="262" height="34" rx="17" fill="{BG}" stroke="{ACC}" stroke-opacity=".3"/>
      <circle cx="20" cy="17" r="4" fill="{ACC}">
        <animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/>
      </circle>
      <text class="hero-mono" x="34" y="21.5" font-size="12" fill="{MUTE}">~/komal<tspan fill="{ACC}"> $ </tspan><tspan fill="{TEXT}">deploy --agents</tspan></text>
      <rect x="236" y="10" width="7" height="14" fill="{LIGHT}">
        <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/>
      </rect>
    </g>

    <!-- Eyebrow -->
    <g class="hero-rise d2">
      <line x1="72" y1="136" x2="104" y2="136" stroke="{ACC}"/>
      <text class="hero-mono" x="116" y="140" font-size="12.5" letter-spacing="3.4" fill="{ACC}">AGENTIC AI · DISTRIBUTED SYSTEMS · BACKEND</text>
    </g>

    <!-- Name -->
    <text class="hero-serif hero-rise d3" x="66" y="230" font-size="96" font-weight="300" letter-spacing="-2.5" fill="{TEXT}">Komal</text>
    <text class="hero-serif hero-rise d4" x="66" y="318" font-size="96" font-style="italic" font-weight="300" letter-spacing="-2.5" fill="url(#hero-name-grad)">Mittal<tspan fill="{ROYAL}">.</tspan></text>

    <!-- Light sweeping across the name -->
    <g class="hero-fade d6" pointer-events="none">
      <text class="hero-serif" x="66" y="230" font-size="96" font-weight="300" letter-spacing="-2.5" fill="url(#hero-sheen)">Komal</text>
      <text class="hero-serif" x="66" y="318" font-size="96" font-style="italic" font-weight="300" letter-spacing="-2.5" fill="url(#hero-sheen)">Mittal.</text>
    </g>

    <!-- Glowing underline -->
    <path class="hero-draw" d="M72 346 C 220 340, 420 352, 600 342" fill="none" stroke="url(#hero-rule)" stroke-width="2" stroke-linecap="round" filter="url(#hero-glow)"/>

    <!-- Positioning -->
    <text class="hero-mono hero-rise d5" x="72" y="384" font-size="13" letter-spacing="2.6" fill="{TEXT}">AI ENGINEER  ·  BACKEND DEVELOPER  ·  SYSTEMS BUILDER</text>
    <text class="hero-serif hero-rise d6" x="72" y="420" font-size="19" font-style="italic" fill="{MUTE}">Agents that listen. Systems that hold.</text>

    <!-- Meta strip -->
    <g class="hero-fade d6">
      <line x1="72" y1="446" x2="1128" y2="446" stroke="{ACC}" stroke-opacity=".16"/>
      <text class="hero-mono" x="72" y="466" font-size="10.5" letter-spacing="2" fill="{MUTE}">B.TECH IT · BPIT NEW DELHI · CGPA 9.32</text>
      <text class="hero-mono" x="1128" y="466" text-anchor="end" font-size="10.5" letter-spacing="2" fill="{LIGHT}">MEESHO SCRIPTEDBY{{HER}} 2.0 TOP 50 · FLIPKART GRiD 8.0 SEMI-FINALIST</text>
    </g>

    <!-- Frame -->
    <rect x=".5" y=".5" width="1199" height="479" rx="19.5" fill="none" stroke="{ACC}" stroke-opacity=".2"/>
  </g>
</svg>"""


# ---- About: typed terminal + three cards -------------------------------
def about():
    lines = [
        ("whoami", "Komal Mittal · Python & AI Engineer · Backend Developer"),
        ("cat education.txt", "B.Tech IT · Bhagwan Parshuram Institute of Technology · 9.32"),
        ("cat experience.txt", "Python Engineering Intern · Meevick Enterprises · 2026"),
        ("ls ./shipped", "sakhi · tickless · nse-orb-trading-engine"),
        ("echo $PRINCIPLE", "ground every answer · never send an email twice"),
    ]
    clips, rows = [], []
    t = 0.6
    for i, (cmd, out) in enumerate(lines):
        y_cmd, y_out = 128 + i * 50, 153 + i * 50
        w_cmd = round(26 + len(cmd) * 8.6 + 8)
        w_out = round(26 + len(out) * 8.3 + 10)
        d_cmd = round(0.09 + len(cmd) * 0.028, 2)
        clips.append(f'    <clipPath id="ab-c{2*i}"><rect class="ab-type" x="68" y="{y_cmd - 16}" width="{w_cmd}" height="22" style="animation-delay:{t:.2f}s;animation-duration:{d_cmd:.2f}s;animation-timing-function:steps({len(cmd)})"/></clipPath>')
        t += d_cmd + 0.15
        clips.append(f'    <clipPath id="ab-c{2*i+1}"><rect class="ab-type" x="68" y="{y_out - 16}" width="{w_out}" height="22" style="animation-delay:{t:.2f}s;animation-duration:0.53s;animation-timing-function:steps(1)"/></clipPath>')
        t += 0.53 + 0.35
        rows.append(f'      <g clip-path="url(#ab-c{2*i})"><text x="72" y="{y_cmd}" fill="{ACC}">$</text><text x="94" y="{y_cmd}" fill="{TEXT}">{esc(cmd)}</text></g>')
        rows.append(f'      <g clip-path="url(#ab-c{2*i+1})"><text x="72" y="{y_out}" fill="{ROYAL}">→</text><text x="94" y="{y_out}" fill="{MUTE}">{esc(out)}</text></g>')

    cards = [
        ("PRIMARY LANGUAGE", "Python", "agents · FastAPI · trading engine"),
        ("SYSTEMS IN", "TypeScript", "Node.js · BullMQ · Redis locks"),
        ("DRAWN TO", "Agentic AI", "LangGraph · RAG · Hindi voice"),
    ]
    card_svg = "\n".join(f"""    <g class="ab-card" style="animation-delay:{1.2 + k * .5:.1f}s"><g transform="translate(836 {70 + k * 104})">
      <rect width="324" height="88" rx="14" fill="{BG}" stroke="{ACC}" stroke-opacity=".3"/>
      <rect x="0" y="0" width="3" height="88" rx="1.5" fill="{ACC}"/>
      <text class="ab-mono" x="22" y="26" font-size="10" letter-spacing="2" fill="{ACC}">{lab}</text>
      <text class="ab-serif" x="22" y="58" font-size="28" font-weight="300" fill="{TEXT}">{big}</text>
      <text class="ab-sans" x="22" y="78" font-size="12" fill="{MUTE}">{esc(sub)}</text>
    </g></g>""" for k, (lab, big, sub) in enumerate(cards))

    nl = "\n"
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" width="1200" height="420" role="img" aria-labelledby="ab-t ab-d">
  <title id="ab-t">About Komal Mittal</title>
  <desc id="ab-d">Python and AI engineer and backend developer. B.Tech in Information Technology at Bhagwan Parshuram Institute of Technology, New Delhi, CGPA 9.32. Python Engineering Intern at Meevick Enterprises, June to July 2026. Shipped Sakhi, Tickless and an NSE opening-range-breakout trading engine. Primary language Python; systems work in TypeScript; drawn to agentic AI.</desc>
  <defs>
    <linearGradient id="ab-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{DEEP}"/></linearGradient>
    <radialGradient id="ab-glow" cx="80%" cy="20%" r="70%"><stop offset="0" stop-color="{GLOW}" stop-opacity=".5"/><stop offset="1" stop-color="{MDEEP}" stop-opacity="0"/></radialGradient>
    <pattern id="ab-scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="{TEXT}" opacity=".025"/></pattern>
{nl.join(clips)}
  </defs>
  <style>
{fonts("ab")}
    .ab-type {{ transform-box: fill-box; transform-origin: left center; animation-name: ab-type; animation-fill-mode: both; }}
    .ab-card {{ animation: ab-in 1s cubic-bezier(.16,1,.3,1) both; }}
    .ab-fade {{ animation: ab-fade 1s ease both; }}
    @keyframes ab-type {{ 0% {{ transform: scaleX(0); }} 85%, 100% {{ transform: scaleX(1); }} }}
    @keyframes ab-in {{ from {{ opacity: 0; transform: translateX(24px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes ab-fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{ .ab-type, .ab-card, .ab-fade {{ animation: none; }} }}
  </style>
  <rect width="1200" height="420" rx="20" fill="url(#ab-bg)"/>
  <rect width="1200" height="420" rx="20" fill="url(#ab-glow)"/>
  <rect x=".5" y=".5" width="1199" height="419" rx="19.5" fill="none" stroke="{ACC}" stroke-opacity=".18"/>

  <!-- Terminal window -->
  <g class="ab-fade">
    <rect x="40" y="40" width="760" height="340" rx="14" fill="{DEEP}" stroke="{ACC}" stroke-opacity=".32"/>
    <rect x="40" y="40" width="760" height="340" rx="14" fill="url(#ab-scan)"/>
    <path d="M40 54 a14 14 0 0 1 14 -14 H786 a14 14 0 0 1 14 14 V76 H40 Z" fill="{BG}"/>
    <line x1="40" y1="76" x2="800" y2="76" stroke="{ACC}" stroke-opacity=".22"/>
    <circle cx="62" cy="58" r="5" fill="{ROYAL}"/><circle cx="80" cy="58" r="5" fill="{MDEEP}"/><circle cx="98" cy="58" r="5" fill="{MDEEP}"/>
    <text class="ab-mono" x="420" y="62" text-anchor="middle" font-size="11" letter-spacing="1.5" fill="{MUTE}">komal@github: ~</text>
  </g>
  <g class="ab-mono" font-size="13.5">
{nl.join(rows)}
  </g>
  <rect x="72" y="364" width="8" height="16" fill="{LIGHT}" class="ab-fade" style="animation-delay:{t:.1f}s">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>

{card_svg}
</svg>"""


# ---- Recognition --------------------------------------------------------
def recognition():
    strip = [
        ("ACADEMICS", "9.32", "CGPA · B.Tech IT"),
        ("MEESHO HACKATHON", "Top 50", "of 36,000+ developers"),
        ("FLIPKART GRiD 8.0", "165K+", "applicants in the field"),
        ("SAKHI", "11", "LangGraph nodes, 4 agents"),
        ("TICKLESS", "60+", "Vitest unit tests"),
    ]
    strip_svg = "\n".join(f"""    <g transform="translate({36 + k * 230} 300)">
      <circle cx="0" cy="0" r="3.5" fill="{LIGHT}"/>
      <text class="ach-mono" y="34" font-size="11" letter-spacing="2" fill="{ACC}">{esc(lab)}</text>
      <text class="ach-serif" y="78" font-size="40" font-weight="300" fill="{TEXT}">{esc(big)}</text>
      <text y="102">{esc(sub)}</text>
    </g>""" for k, (lab, big, sub) in enumerate(strip))

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 430" width="1200" height="430" role="img" aria-labelledby="ach-title ach-desc">
  <title id="ach-title">Recognition</title>
  <desc id="ach-desc">Meesho ScriptedBy Her 2.0 National Semi-Finalist, ranked Top 50 among 36,000+ women developers. Flipkart GRiD 8.0 Semi-Finalist among 165,000+ applicants. CGPA 9.32. Sakhi: 11-node LangGraph with 4 specialist agents. Tickless: 60+ Vitest unit tests.</desc>

  <defs>
    <linearGradient id="ach-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BG}"/>
      <stop offset="1" stop-color="{DEEP}"/>
    </linearGradient>
    <radialGradient id="ach-glow-a" cx="85%" cy="0%" r="90%">
      <stop offset="0" stop-color="{GLOW}" stop-opacity=".7"/>
      <stop offset="1" stop-color="{MDEEP}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="ach-glow-b" cx="90%" cy="0%" r="90%">
      <stop offset="0" stop-color="{ACC}" stop-opacity=".32"/>
      <stop offset="1" stop-color="{MDEEP}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="ach-hair" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/>
      <stop offset=".4" stop-color="{GOLD}"/>
      <stop offset=".6" stop-color="{LIGHT}"/>
      <stop offset="1" stop-color="{LIGHT}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ach-outline" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{LIGHT}" stop-opacity=".55"/>
      <stop offset="1" stop-color="{LIGHT}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ach-sheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{TEXT}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{TEXT}" stop-opacity=".08"/>
      <stop offset="1" stop-color="{TEXT}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="ach-clip-a"><rect x="0" y="0" width="690" height="250" rx="16"/></clipPath>
    <clipPath id="ach-clip-b"><rect x="0" y="0" width="450" height="250" rx="16"/></clipPath>
    <linearGradient id="ach-trace" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{TEXT}"/><stop offset=".45" stop-color="{LIGHT}"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <style>
{fonts("ach")}
    .ach-in {{ animation: ach-in 1.2s cubic-bezier(.16,1,.3,1) both; }}
    .a1 {{ animation-delay: .1s; }} .a2 {{ animation-delay: .35s; }} .a3 {{ animation-delay: .6s; }}
    .ach-draw {{ stroke-dasharray: 1200; stroke-dashoffset: 1200; animation: ach-draw 2.6s cubic-bezier(.65,0,.35,1) .8s forwards; }}
    @keyframes ach-in {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes ach-draw {{ to {{ stroke-dashoffset: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .ach-in {{ animation: none; }}
      .ach-draw {{ animation: none; stroke-dashoffset: 0; }}
    }}
    .ach-trace-a {{ stroke-dasharray: 340 1540; stroke-dashoffset: 1880; animation: ach-trace-a 6s linear infinite; }}
    .ach-trace-b {{ stroke-dasharray: 260 1140; stroke-dashoffset: 1400; animation: ach-trace-b 6s linear -3s infinite; }}
    @keyframes ach-trace-a {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes ach-trace-b {{ to {{ stroke-dashoffset: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .ach-trace-a, .ach-trace-b {{ display: none; }} }}
  </style>

  <rect width="1200" height="430" rx="20" fill="url(#ach-bg)"/>
  <rect x=".5" y=".5" width="1199" height="429" rx="19.5" fill="none" stroke="{ACC}" stroke-opacity=".18"/>

  <!-- Meesho ScriptedBy{{Her}} 2.0 — hero card -->
  <g class="ach-in a1"><g transform="translate(24 24)">
    <g clip-path="url(#ach-clip-a)">
      <rect width="690" height="250" fill="{BG}"/>
      <rect width="690" height="250" fill="url(#ach-glow-a)"/>
      <text class="ach-serif" x="672" y="124" text-anchor="end" font-size="128" font-weight="300" letter-spacing="-6" fill="url(#ach-outline)">Top 50</text>
      <rect x="-300" y="0" width="260" height="250" fill="url(#ach-sheen)" transform="skewX(-18)">
        <animate attributeName="x" values="-300;900;900" keyTimes="0;.35;1" dur="9s" begin="2s" repeatCount="indefinite"/>
      </rect>
    </g>
    <rect x=".5" y=".5" width="689" height="249" rx="15.5" fill="none" stroke="{ACC}" stroke-opacity=".4"/>
    <rect class="ach-trace-a" x=".5" y=".5" width="689" height="249" rx="15.5" fill="none" stroke="url(#ach-trace)" stroke-width="1.8" stroke-linecap="round"/>
    <rect x="40" y="0" width="300" height="1" fill="url(#ach-hair)"/>
    <text class="ach-mono" x="36" y="154" font-size="12" letter-spacing="2.6" fill="{ACC}">MEESHO · SCRIPTEDBY{{HER}} 2.0 · AGENTIC AI FOR BHARAT</text>
    <text class="ach-serif" x="34" y="204" font-size="46" font-weight="300" letter-spacing="-1" fill="{TEXT}">National Semi-Finalist</text>
    <text class="ach-sans" x="36" y="230" font-size="14" fill="{MUTE}">Top 50 of 36,000+ women developers · India's largest women-only hackathon</text>
  </g></g>

  <!-- Flipkart GRiD 8.0 -->
  <g class="ach-in a2"><g transform="translate(702 24)">
    <g transform="translate(24 0)">
      <g clip-path="url(#ach-clip-b)">
        <rect width="450" height="250" fill="{BG}"/>
        <rect width="450" height="250" fill="url(#ach-glow-b)"/>
        <text class="ach-serif" x="462" y="132" text-anchor="end" font-size="160" font-style="italic" font-weight="300" letter-spacing="-6" fill="none" stroke="{LIGHT}" stroke-opacity=".3">8.0</text>
      </g>
      <rect x=".5" y=".5" width="449" height="249" rx="15.5" fill="none" stroke="{ACC}" stroke-opacity=".32"/>
      <rect class="ach-trace-b" x=".5" y=".5" width="449" height="249" rx="15.5" fill="none" stroke="url(#ach-trace)" stroke-width="1.8" stroke-linecap="round"/>
      <rect x="40" y="0" width="220" height="1" fill="url(#ach-hair)"/>
      <text class="ach-mono" x="32" y="154" font-size="12" letter-spacing="2.6" fill="{ACC}">FLIPKART · GRiD 8.0</text>
      <text class="ach-serif" x="30" y="204" font-size="46" font-weight="300" letter-spacing="-1" fill="{TEXT}">Semi-Finalist</text>
      <text class="ach-sans" x="32" y="230" font-size="14" fill="{MUTE}">165,000+ applicants · India's largest campus challenge</text>
    </g>
  </g></g>

  <!-- Animated connector across the score strip -->
  <path class="ach-draw" d="M24 300 H1176" stroke="{ACC}" stroke-opacity=".38"/>

  <!-- Score strip -->
  <g class="ach-in a3 ach-sans" font-size="13" fill="{MUTE}">
{strip_svg}
  </g>
</svg>"""


# ---- Project / experience cards ----------------------------------------
def chips(p, items, x0=56, y=314):
    out, x = [], x0
    for k, name in enumerate(items):
        w = round(len(name) * 7 + 21)
        out.append(f'<g class="{p}-chip" style="animation-delay:{1 + k * .12:.2f}s"><rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{CHIP}" stroke="{ACC}" stroke-opacity=".38"/>'
                   f'<text class="{p}-mono" x="{x + w / 2:g}" y="{y + 17}" text-anchor="middle" font-size="11.5" fill="{LIGHT}">{esc(name)}</text></g>')
        x += w + 8
    return "".join(out)


def card(p, title_text, eyebrow, name, tag, line, built, stats, chip_list, visual, trace_delay):
    stats_svg = "\n".join(
        f'    <g transform="translate({56 + k * 205} 266)"><text class="{p}-serif" font-size="34" font-weight="300" fill="{TEXT}">{esc(big)}</text>'
        f'<text class="{p}-sans" y="24" font-size="12.5" fill="{MUTE}">{esc(sub)}</text></g>'
        for k, (big, sub) in enumerate(stats))
    tag_svg = f'<tspan class="{p}-serif" font-size="22" font-style="italic" fill="{LIGHT}" dx="14">{esc(tag)}</tspan>' if tag else ""
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 370" width="1200" height="370" role="img" aria-labelledby="{p}-t">
  <title id="{p}-t">{esc(title_text)}</title>
  <defs>
    <linearGradient id="{p}-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{DEEP}"/>
    </linearGradient>
    <radialGradient id="{p}-glow" cx="82%" cy="30%" r="55%">
      <stop offset="0" stop-color="{GLOW}" stop-opacity=".55"/><stop offset="1" stop-color="{MDEEP}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="{p}-grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="{ACC}" stroke-opacity=".08"/>
    </pattern>
    <filter id="{p}-glowf" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="{p}-clip"><rect width="1200" height="370" rx="18"/></clipPath>
    <linearGradient id="{p}-trace" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{TEXT}"/><stop offset=".45" stop-color="{LIGHT}"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
{fonts(p)}
    .{p}-in {{ animation: {p}-in 1.2s cubic-bezier(.16,1,.3,1) both; }}
    .{p}-d1 {{ animation-delay: .15s; }} .{p}-d2 {{ animation-delay: .4s; }}
    .{p}-chip {{ animation: {p}-chip .7s cubic-bezier(.34,1.56,.64,1) both; }}
    @keyframes {p}-chip {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
    .{p}-draw {{ stroke-dasharray: 600; stroke-dashoffset: 600; animation: {p}-draw 2s cubic-bezier(.65,0,.35,1) .5s forwards; }}
    .{p}-draw-late {{ stroke-dasharray: 600; stroke-dashoffset: 600; animation: {p}-draw 2.6s cubic-bezier(.65,0,.35,1) 1.4s forwards; }}
    .{p}-pop {{ animation: {p}-chip .7s cubic-bezier(.34,1.56,.64,1) both; }}
    .{p}-bar {{ transform-box: fill-box; transform-origin: center; animation: {p}-bar 1.1s ease-in-out infinite alternate; }}
    @keyframes {p}-in {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes {p}-draw {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes {p}-bar {{ from {{ transform: scaleY(.25); }} to {{ transform: scaleY(1); }} }}
    @media (prefers-reduced-motion: reduce) {{ .{p}-in, .{p}-chip, .{p}-pop, .{p}-bar {{ animation: none; }} .{p}-draw, .{p}-draw-late {{ animation: none; stroke-dashoffset: 0; }} }}
    .{p}-trace {{ stroke-dasharray: 564 3136; stroke-dashoffset: 3700; animation: {p}-trace 7s linear infinite; }}
    @keyframes {p}-trace {{ to {{ stroke-dashoffset: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .{p}-trace {{ display: none; }} }}
  </style>
  <g clip-path="url(#{p}-clip)">
    <rect width="1200" height="370" fill="url(#{p}-bg)"/>
    <rect x="720" width="480" height="370" fill="url(#{p}-grid)"/>
    <rect width="1200" height="370" fill="url(#{p}-glow)"/>
    <g class="{p}-in {p}-d1">
      <text class="{p}-mono" x="56" y="62" font-size="12" letter-spacing="2.6" fill="{ACC}">{esc(eyebrow)}</text>
      <text class="{p}-serif" x="54" y="126" font-size="52" font-weight="300" letter-spacing="-1.5" fill="{TEXT}">{esc(name)}{tag_svg}</text>
      <text class="{p}-sans" x="56" y="166" font-size="17" fill="{MUTE}">{esc(line)}</text>
      <text class="{p}-mono" x="56" y="200" font-size="12.5" fill="{LIGHT}"><tspan fill="{ACC}">BUILT ›</tspan> {esc(built)}</text>
      <line class="{p}-draw" x1="56" y1="226" x2="680" y2="226" stroke="{ACC}" stroke-opacity=".32"/>
{stats_svg}
      {chips(p, chip_list)}
    </g>
    <g class="{p}-in {p}-d2">
{visual}
    </g>
    <rect x=".5" y=".5" width="1199" height="369" rx="17.5" fill="none" stroke="{ACC}" stroke-opacity=".22"/>
    <rect class="{p}-trace" style="animation-delay:{trace_delay}s" x=".5" y=".5" width="1199" height="369" rx="17.5" fill="none" stroke="url(#{p}-trace)" stroke-width="1.6" stroke-linecap="round"/>
  </g>
</svg>"""


def experience_trading():
    p = "ex"
    # (open, close, high, low) in screen y — smaller y is a higher price
    candles = [(215, 200, 195, 228), (200, 222, 192, 230), (222, 205, 198, 226), (205, 212, 190, 224),
               (212, 198, 194, 218), (198, 204, 193, 212), (204, 176, 170, 208), (176, 168, 160, 182),
               (168, 180, 164, 186), (180, 150, 144, 184), (150, 140, 132, 156), (140, 152, 136, 158),
               (152, 124, 118, 156), (124, 112, 104, 130), (112, 118, 106, 124), (118, 96, 88, 122)]
    candles = [tuple(v + 36 for v in c) for c in candles]  # chart sits below the header row
    X = lambda i: 790 + i * 22
    cs = []
    for i, (o, c, h, l) in enumerate(candles):
        x = X(i)
        up = c < o
        top, bot = min(o, c), max(o, c)
        body = (f'<rect x="{x - 6}" y="{top}" width="12" height="{max(bot - top, 2)}" rx="2" fill="{ROYAL if up else "none"}" '
                f'stroke="{LIGHT if up else ACC}" stroke-opacity="{.9 if up else .7}"/>')
        cs.append(f'<g class="{p}-pop" style="animation-delay:{.9 + i * .09:.2f}s"><line x1="{x}" y1="{h}" x2="{x}" y2="{l}" stroke="{LIGHT if up else ACC}" stroke-opacity=".7"/>{body}</g>')
    closes = " L".join(f"{X(i)} {c}" for i, (_, c, _, _) in enumerate(candles))
    rel = " L".join(f"{X(i) - X(0)} {c - candles[0][1]}" for i, (_, c, _, _) in enumerate(candles))
    # trailing stop ladder: only ever steps up (lower y)
    ladder = f"M{X(6) - 8} 250 H{X(8) + 8} V234 H{X(10) + 8} V206 H{X(12) + 8} V196 H{X(13) + 8} V176 H{X(15) + 10} V164"
    votes = "".join(f'<circle cx="{1110 + k * 13}" cy="88" r="4" fill="{LIGHT if k < 4 else "none"}" stroke="{LIGHT}" stroke-opacity=".7"/>' for k in range(5))
    visual = f"""      <g class="{p}-mono">
        <text x="772" y="92" font-size="10.5" letter-spacing="2.4" fill="{MUTE}">NSE · 10 STOCKS · 5 INDICES</text>
        <text x="1100" y="92" font-size="10" letter-spacing="1.4" fill="{LIGHT}" text-anchor="end">SECTOR VOTE</text>{votes}
        <rect x="{X(0) - 12}" y="226" width="{X(3) - X(0) + 24}" height="40" fill="{ACC}" fill-opacity=".1"/>
        <line x1="{X(0) - 12}" y1="226" x2="1176" y2="226" stroke="{ACC}" stroke-opacity=".45" stroke-dasharray="3 5"/>
        <line x1="{X(0) - 12}" y1="266" x2="{X(5) + 12}" y2="266" stroke="{ACC}" stroke-opacity=".3" stroke-dasharray="3 5"/>
        <text x="{X(0) - 10}" y="284" font-size="9.5" letter-spacing="1.6" fill="{MUTE}">OPENING RANGE</text>
        <line x1="{X(0) - 12}" y1="298" x2="1176" y2="298" stroke="#E07A7A" stroke-opacity=".45" stroke-dasharray="2 6"/>
        <text x="1176" y="290" font-size="9.5" letter-spacing="1.4" fill="#E9A3A3" text-anchor="end">HARD STOP · ₹3,000 · NEVER HIT</text>
        {"".join(cs)}
        <path class="{p}-draw-late" d="{ladder}" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-dasharray="600"/>
        <text x="1176" y="218" font-size="9.5" letter-spacing="1.4" fill="{GOLD}" text-anchor="end">TRAIL SL · 18 RUNGS</text>
        <g class="{p}-pop" style="animation-delay:1.6s"><path d="M{X(6)} 198 v-14 m-4 4 l4 -4 l4 4" fill="none" stroke="{LIGHT}"/><text x="{X(6) - 8}" y="190" font-size="9.5" letter-spacing="1.4" fill="{LIGHT}" text-anchor="end">BREAKOUT</text></g>
        <path d="M{closes}" fill="none" stroke="{TEXT}" stroke-opacity=".18"/>
        <circle cx="{X(0)}" cy="{candles[0][1]}" r="4" fill="{TEXT}" filter="url(#{p}-glowf)">
          <animateMotion dur="5s" begin="2.2s" repeatCount="indefinite" path="M{rel}" calcMode="linear"/>
        </circle>
        <text x="772" y="326" font-size="10.5" letter-spacing="1.5" fill="{MUTE}">paper-traded on live prices · Telegram alerts</text>
      </g>"""
    return card(
        p, "NSE Trading Engine: a 24/7 opening-range-breakout engine for NSE equities, built as Python Engineering Intern at Meevick Enterprises.",
        "EXPERIENCE · MEEVICK ENTERPRISES · JUN – JUL 2026",
        "Trading Engine", "Python Engineering Intern",
        "A 24/7 breakout engine for NSE equities, gated by a sector-index vote.",
        "Upstox REST behind a self-healing 401 replay · rate limits",
        [("18", "rung trailing stop-loss"), ("₹3,000", "hard stop, never breached"), ("24/7", "on AWS EC2 with cron")],
        ["Python", "Pandas", "Upstox API", "AWS EC2", "cron", "Telegram"],
        visual, "0.0")


def project_sakhi():
    p = "p1"
    bars = "".join(
        f'<rect class="{p}-bar" style="animation-delay:{-k * .13:.2f}s;animation-duration:{.7 + (k * 37 % 5) * .12:.2f}s" x="{780 + k * 7}" y="{88 - hgt / 2}" width="3.5" height="{hgt}" rx="1.75" fill="{LIGHT}"/>'
        for k, hgt in enumerate([8, 16, 24, 12, 22, 28, 14, 20, 10, 18]))
    agents = ["Catalog", "Customer", "Growth", "Returns"]
    nodes, wires = [], []
    for k, name in enumerate(agents):
        x = 772 + k * 102
        cx = x + 45
        b = 1.0 + k * .6
        wires.append(f'<path class="{p}-draw" d="M968 172 C 968 196, {cx} 196, {cx} 222" fill="none" stroke="{ACC}" stroke-opacity=".45"/>')
        nodes.append(f"""<g transform="translate({x} 222)">
          <rect width="90" height="40" rx="10" fill="{CHIP}" stroke="{ACC}" stroke-opacity=".35">
            <animate attributeName="fill" values="{CHIP};{ROYAL};{CHIP};{CHIP}" keyTimes="0;.08;.2;1" dur="6s" begin="{b:.1f}s" repeatCount="indefinite"/>
            <animate attributeName="stroke-opacity" values=".35;1;.35;.35" keyTimes="0;.08;.2;1" dur="6s" begin="{b:.1f}s" repeatCount="indefinite"/>
          </rect>
          <text x="45" y="25" font-size="10.5" text-anchor="middle" fill="{TEXT}">{name}</text>
        </g>""")
    visual = f"""      <g class="{p}-mono">
        <rect x="772" y="66" width="396" height="44" rx="14" fill="{TEXT}" fill-opacity=".07" stroke="{ACC}" stroke-opacity=".35"/>
        {bars}
        <text x="866" y="94" font-size="14" fill="{TEXT}">“मेरी नई साड़ी लिस्ट कर दो”</text>
        <text x="1158" y="93" font-size="9.5" letter-spacing="1.4" fill="{MUTE}" text-anchor="end">HINDI</text>
        <path class="{p}-draw" d="M968 110 V132" stroke="{ACC}" stroke-opacity=".5"/>
        <rect x="868" y="132" width="200" height="40" rx="20" fill="{MDEEP}" stroke="{LIGHT}"/>
        <text x="968" y="157" font-size="11" letter-spacing="1.2" text-anchor="middle" fill="{TEXT}">ORCHESTRATOR · 11 NODES</text>
        {"".join(wires)}
        {"".join(nodes)}
        <circle r="4" fill="{TEXT}" filter="url(#{p}-glowf)">
          <animateMotion dur="6s" begin="1s" repeatCount="indefinite" path="M968 110 V172 C 968 196, 817 196, 817 222" keyPoints="0;1;1" keyTimes="0;.18;1" calcMode="linear"/>
        </circle>
        <text x="1168" y="288" font-size="10.5" letter-spacing="1.5" text-anchor="end" fill="{LIGHT}">Sarvam ASR → LangGraph → Bulbul TTS</text>
        <text x="1168" y="308" font-size="9.5" letter-spacing="1.5" text-anchor="end" fill="{MUTE}">RAG · 100-SKU CATALOG · PGVECTOR · 3 HITL GATES</text>
      </g>"""
    return card(
        p, "Sakhi: a Hindi voice-native multi-agent co-pilot for Meesho resellers. Meesho ScriptedBy Her 2.0, Top 50.",
        "01 · AGENTIC AI · MEESHO SCRIPTEDBY{HER} 2.0 · TOP 50",
        "Sakhi", "voice co-pilot for Bharat",
        "Lets Hindi-speaking Meesho resellers run their store by talking.",
        "11-node LangGraph · 4 agents · RAG over pgvector",
        [("11", "LangGraph nodes"), ("4", "specialist agents"), ("5", "model fallback on HTTP 429")],
        ["Python", "FastAPI", "LangGraph", "pgvector", "Gemini", "Docker"],
        visual, "-1.7")


def project_tickless():
    p = "p2"
    jobs = ["c42 · send@09:30", "c42 · send@09:34", "c42 · send@09:38", "c42 · send@09:42"]
    q = []
    for k, j in enumerate(jobs):
        y = 112 + k * 34
        hl = k == 1
        q.append(f"""<g><rect x="772" y="{y}" width="134" height="26" rx="8" fill="{MDEEP if hl else CHIP}" stroke="{LIGHT if hl else ACC}" stroke-opacity="{1 if hl else .35}">
            <animate attributeName="opacity" values="1;.55;1" dur="3s" begin="{k * .4:.1f}s" repeatCount="indefinite"/></rect>
          <text x="784" y="{y + 17}" font-size="10.5" fill="{TEXT if hl else MUTE}">{j}</text></g>""")
    visual = f"""      <g class="{p}-mono">
        <text x="772" y="92" font-size="10.5" letter-spacing="2.4" fill="{MUTE}">BULLMQ DELAYED JOBS · REDIS · ZERO CRON</text>
        {"".join(q)}
        <path d="M906 125 C 932 125, 936 150, 962 158" fill="none" stroke="{ACC}" stroke-opacity=".45" stroke-dasharray="4 6"/>
        <path class="{p}-draw" d="M906 159 H962" fill="none" stroke="{LIGHT}" stroke-width="1.5"/>
        <path d="M906 193 C 932 193, 936 168, 962 160" fill="none" stroke="{ACC}" stroke-opacity=".45" stroke-dasharray="4 6"/>
        <text x="934" y="116" font-size="9" letter-spacing="1" fill="{MUTE}" text-anchor="middle">3 workers</text>
        <rect x="962" y="132" width="104" height="54" rx="12" fill="{CHIP}" stroke="{GOLD}" stroke-opacity=".8"/>
        <path d="M980 152 v-5 a6 6 0 0 1 12 0 v5" fill="none" stroke="{GOLD}" stroke-width="1.6"/>
        <rect x="977" y="152" width="18" height="14" rx="3" fill="{GOLD}"/>
        <text x="1002" y="156" font-size="10.5" fill="{TEXT}">sender</text>
        <text x="1002" y="172" font-size="10" fill="{GOLD}">NX PX</text>
        <path class="{p}-draw" d="M1066 159 H1092" stroke="{LIGHT}" stroke-width="1.5"/>
        <rect x="1092" y="138" width="84" height="42" rx="21" fill="{MDEEP}" stroke="{LIGHT}"/>
        <text x="1134" y="164" font-size="12" text-anchor="middle" fill="{TEXT}">Gmail</text>
        <circle r="4.5" fill="{TEXT}" filter="url(#{p}-glowf)">
          <animateMotion dur="3.6s" repeatCount="indefinite" path="M906 159 H1134" calcMode="spline" keyPoints="0;1" keyTimes="0;1" keySplines=".45 0 .55 1"/>
        </circle>
        <text x="962" y="228" font-size="9.5" letter-spacing="1.6" fill="{MUTE}">HOURLY RATE WINDOW</text>
        <text x="1176" y="262" font-size="9.5" letter-spacing="1" fill="{LIGHT}" text-anchor="end">overflow rolls to the next hour</text>
        <rect x="962" y="238" width="214" height="6" rx="3" fill="{CHIP}"/>
        <rect x="962" y="238" width="0" height="6" rx="3" fill="{ROYAL}">
          <animate attributeName="width" values="0;214;214;0" keyTimes="0;.7;.9;1" dur="6s" begin="1s" repeatCount="indefinite"/>
        </rect>
        <text x="1176" y="300" font-size="10.5" letter-spacing="1.5" text-anchor="end" fill="{MUTE}">idempotent job IDs · atomic claims · orphan scanner</text>
      </g>"""
    return card(
        p, "Tickless: a distributed email scheduler with zero cron jobs. BullMQ delayed jobs in Redis, a Redis sender lock and crash-safe delivery from the user's own Gmail.",
        "02 · DISTRIBUTED SYSTEMS · JOB SCHEDULING",
        "Tickless", "zero cron jobs",
        "A distributed email scheduler that sends from your own Gmail.",
        "Redis SET NX PX lock · atomic hourly rate windows",
        [("0", "cron jobs"), ("60+", "Vitest unit tests"), ("JWT", "auth + OAuth 2.0 Gmail")],
        ["TypeScript", "Node.js", "BullMQ", "Redis", "PostgreSQL", "Prisma", "Next.js"],
        visual, "-3.4")


# ---- Toolkit ------------------------------------------------------------
def toolkit():
    panels = [
        ("01  LANGUAGES", [(40, TEXT, 'Python <tspan font-size="13" class="tc-mono" fill="{a}" dy="-18">PRIMARY</tspan>'), (32, TEXT, "TypeScript"), (22, MUTE, "C++  ·  C  ·  SQL  ·  JavaScript")], None),
        ("02  AI · AGENTS", [(30, TEXT, "LangGraph  ·  RAG"), (24, TEXT, "Multi-Agent Systems"), (22, MUTE, "Embeddings · Vector Search")], "NLP · PANDAS · GEMINI"),
        ("03  BACKEND &amp; APIS", [(32, TEXT, "FastAPI  ·  Node.js"), (24, TEXT, "Express  ·  REST APIs"), (22, MUTE, "BullMQ  ·  WebSockets")], None),
        ("04  DATA", [(32, TEXT, "PostgreSQL  ·  Redis"), (24, TEXT, "pgvector  ·  Prisma"), (22, MUTE, "Distributed locks")], "DBMS · ATOMIC CLAIMS"),
        ("05  CLOUD &amp; DELIVERY", [(32, TEXT, "Docker  ·  AWS EC2"), (24, TEXT, "Git  ·  cron  ·  Vercel"), (22, MUTE, "OAuth 2.0  ·  JWT")], None),
        ("06  FUNDAMENTALS", [(28, TEXT, "DSA in C++  ·  OOPS"), (22, TEXT, "Operating Systems · DBMS"), (22, MUTE, "Unit Testing · Vitest")], "HTML · CSS"),
    ]
    ys = [(96, 146, 180), (90, 130, 164), (90, 132, 170)]
    out = []
    for k, (lab, rows, foot) in enumerate(panels):
        x = [32, 420, 808][k % 3]
        y = 32 if k < 3 else 268
        yy = ys[0] if k == 0 else ys[1] if foot else ys[2]
        lines = "\n".join(
            f'    <text class="tc-serif" x="24" y="{yy[r]}" font-size="{fs}" font-weight="300" fill="{col}">{txt.format(a=ACC)}</text>'
            for r, (fs, col, txt) in enumerate(rows))
        foot_svg = f'\n    <text class="tc-mono" x="24" y="186" font-size="10" letter-spacing="1.4" fill="{MUTE}">{foot}</text>' if foot else ""
        out.append(f"""  <g class="tc-panel tc-p{k + 1}"><g transform="translate({x} {y})">
    <rect width="360" height="200" rx="14" fill="{BG}" fill-opacity=".88" stroke="{ACC}" stroke-opacity=".24"/>
    <rect class="tc-trace" style="animation-delay:{-k * 1.15:.2f}s" width="360" height="200" rx="14" fill="none" stroke="url(#tc-trace)" stroke-width="1.4" stroke-linecap="round"/>
    <text class="tc-mono" x="24" y="38" font-size="11" letter-spacing="2.4" fill="{ACC}">{lab}</text>
{lines}{foot_svg}
  </g></g>""")
    body = "\n".join(out)
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 500" width="1200" height="500" role="img" aria-labelledby="tc-title tc-desc">
  <title id="tc-title">Tech stack</title>
  <desc id="tc-desc">Languages: Python (primary), TypeScript, C++, C, SQL, JavaScript, HTML, CSS. AI and agents: LangGraph, RAG, multi-agent systems, embeddings, vector search, NLP, Pandas, Gemini. Backend: FastAPI, Node.js, Express, REST APIs, BullMQ, WebSockets. Data: PostgreSQL, Redis, pgvector, Prisma. Cloud and delivery: Docker, AWS EC2, Git, OAuth 2.0, JWT. Fundamentals: DSA in C++, OOPS, operating systems, DBMS, unit testing.</desc>
  <defs>
    <linearGradient id="tc-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{DEEP}"/>
    </linearGradient>
    <radialGradient id="tc-glow" cx="50%" cy="50%" r="60%">
      <stop offset="0" stop-color="{MDEEP}" stop-opacity=".9"/><stop offset="1" stop-color="{MDEEP}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="tc-pulse">
      <stop offset="0" stop-color="{TEXT}"/><stop offset=".5" stop-color="{LIGHT}" stop-opacity=".6"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="tc-trace" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{TEXT}"/><stop offset=".45" stop-color="{LIGHT}"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
{fonts("tc")}
    .tc-panel {{ animation: tc-in 1.1s cubic-bezier(.16,1,.3,1) both; }}
    .tc-p1 {{ animation-delay: .05s; }} .tc-p2 {{ animation-delay: .2s; }} .tc-p3 {{ animation-delay: .35s; }}
    .tc-p4 {{ animation-delay: .5s; }} .tc-p5 {{ animation-delay: .65s; }} .tc-p6 {{ animation-delay: .8s; }}
    .tc-web {{ stroke-dasharray: 1800; stroke-dashoffset: 1800; animation: tc-draw 3s cubic-bezier(.65,0,.35,1) 1s forwards; }}
    @keyframes tc-in {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes tc-draw {{ to {{ stroke-dashoffset: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .tc-panel {{ animation: none; }}
      .tc-web {{ animation: none; stroke-dashoffset: 0; }}
    }}
    .tc-trace {{ stroke-dasharray: 201 1120; stroke-dashoffset: 1321; animation: tc-trace 7s linear infinite; }}
    @keyframes tc-trace {{ to {{ stroke-dashoffset: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .tc-trace {{ display: none; }} }}
  </style>

  <rect width="1200" height="500" rx="20" fill="url(#tc-bg)"/>
  <rect width="1200" height="500" rx="20" fill="url(#tc-glow)"/>
  <rect x=".5" y=".5" width="1199" height="499" rx="19.5" fill="none" stroke="{ACC}" stroke-opacity=".18"/>

  <!-- Constellation: gutters linking the six groups -->
  <path class="tc-web" d="M24 250 H1176 M406 24 V476 M794 24 V476" fill="none" stroke="{ACC}" stroke-opacity=".24"/>
  <circle cx="0" cy="250" r="8" fill="url(#tc-pulse)" opacity="0">
    <animate attributeName="cx" values="24;1176" dur="9s" begin="3s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".45 0 .55 1"/>
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="9s" begin="3s" repeatCount="indefinite"/>
  </circle>
  <g fill="{DEEP}" stroke="{LIGHT}">
    <rect x="400" y="244" width="12" height="12" transform="rotate(45 406 250)"/>
    <rect x="788" y="244" width="12" height="12" transform="rotate(45 794 250)"/>
  </g>

{body}
</svg>"""


# ---- Education ----------------------------------------------------------
def education():
    def tile(x, y, w, h, label, dots, inner, delay, edge_delay):
        per = 2 * (w + h)
        dot_svg = "".join(f'<circle cx="{w - 27 - i * 11}" cy="31" r="3.5" fill="{ACC}"/>' for i in range(dots))
        return f"""  <g class="ce-tile" style="animation-delay:{delay:.2f}s"><g transform="translate({x} {y})">
    <rect width="{w}" height="{h}" rx="14" fill="{BG}" stroke="{ACC}" stroke-opacity=".26"/>
    <rect width="{w}" height="{h}" rx="14" fill="none" stroke="url(#ce-edge)" stroke-width="1.2" class="ce-edge" style="stroke-dasharray:{per};stroke-dashoffset:{per};animation-delay:{edge_delay:.2f}s"/>
    <text class="ce-mono" x="22" y="36" font-size="11.5" letter-spacing="2.6" fill="{ACC}">{label}</text>
    {dot_svg}
    <line x1="22" y1="54" x2="{w - 22}" y2="54" stroke="{ACC}" stroke-opacity=".16"/>
{inner}
  </g></g>"""

    btech = f"""    <text class="ce-serif" x="22" y="118" font-size="56" font-weight="300" fill="{TEXT}">9.32</text>
    <text class="ce-mono" x="146" y="96" font-size="11" letter-spacing="2" fill="{LIGHT}">CGPA / 10</text>
    <text class="ce-sans" x="146" y="118" font-size="14" fill="{TEXT}">Bhagwan Parshuram Institute of Technology</text>
    <rect x="22" y="138" width="516" height="5" rx="2.5" fill="{CHIP}"/>
    <rect x="22" y="138" width="481" height="5" rx="2.5" fill="url(#ce-bar)" class="ce-fill"/>
    <text class="ce-mono" x="538" y="160" font-size="10" letter-spacing="1.4" fill="{MUTE}" text-anchor="end">NEW DELHI · 2023 – 2027</text>"""

    def school(score, year):
        return f"""    <text class="ce-serif" x="22" y="112" font-size="44" font-weight="300" fill="{TEXT}">{score}</text>
    <text class="ce-sans" x="22" y="138" font-size="13" fill="{MUTE}">ASN Senior Secondary School</text>
    <text class="ce-mono" x="22" y="158" font-size="10" letter-spacing="1.4" fill="{MUTE}">NEW DELHI · {year}</text>"""

    def two(a, b, c=None):
        s = f'    <text class="ce-sans" x="22" y="86" font-size="14" fill="{TEXT}">{a}</text><text class="ce-sans" x="22" y="108" font-size="14" fill="{TEXT}">{b}</text>'
        if c:
            s += f'<text class="ce-sans" x="22" y="130" font-size="14" fill="{LIGHT}">{c}</text>'
        return s

    tiles = [
        tile(40, 40, 560, 170, "B.TECH · INFORMATION TECHNOLOGY", 4, btech, .2, 2.0),
        tile(620, 40, 260, 170, "CBSE CLASS XII", 2, school("84.6%", "2023"), .32, 2.35),
        tile(900, 40, 260, 170, "CBSE CLASS X", 2, school("94.4%", "2021"), .44, 2.7),
        tile(40, 230, 265, 150, "CORE CS", 3, two("Data Structures &amp;", "Algorithms in C++", "OOPS"), .56, 3.05),
        tile(325, 230, 265, 150, "SYSTEMS", 2, two("Operating Systems", "DBMS", "Distributed Systems"), .68, 3.4),
        tile(610, 230, 265, 150, "ENGINEERING", 2, two("Unit Testing", "REST APIs · OAuth 2.0", "JWT authentication"), .8, 3.75),
        tile(895, 230, 265, 150, "ALWAYS LEARNING", 1, two("Agentic AI for Bharat —", "7-day national build", "Meesho ScriptedBy{Her}"), .92, 4.1),
    ]
    body = "\n".join(tiles)
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" width="1200" height="420" role="img" aria-labelledby="ce-t ce-d">
  <title id="ce-t">Education</title>
  <desc id="ce-d">B.Tech in Information Technology, Bhagwan Parshuram Institute of Technology, New Delhi, 2023 to 2027, CGPA 9.32. CBSE Class XII 84.6% (2023) and Class X 94.4% (2021), ASN Senior Secondary School, New Delhi. Coursework: data structures and algorithms in C++, OOPS, operating systems, DBMS, distributed systems, unit testing.</desc>
  <defs>
    <linearGradient id="ce-bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{DEEP}"/></linearGradient>
    <radialGradient id="ce-glow" cx="15%" cy="100%" r="70%"><stop offset="0" stop-color="{GLOW}" stop-opacity=".45"/><stop offset="1" stop-color="{MDEEP}" stop-opacity="0"/></radialGradient>
    <linearGradient id="ce-edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{TEXT}"/><stop offset=".5" stop-color="{LIGHT}"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></linearGradient>
    <linearGradient id="ce-bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ROYAL}"/><stop offset=".8" stop-color="{LIGHT}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>
  </defs>
  <style>
{fonts("ce")}
    .ce-tile {{ animation: ce-in 1s cubic-bezier(.34,1.3,.64,1) both; }}
    .ce-edge {{ animation: ce-edge 6s cubic-bezier(.65,0,.35,1) infinite; }}
    .ce-fill {{ transform-box: fill-box; transform-origin: left center; animation: ce-fill 2.2s cubic-bezier(.65,0,.35,1) .9s both; }}
    @keyframes ce-in {{ from {{ opacity: 0; transform: translateY(18px) scale(.97); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes ce-edge {{ 40% {{ stroke-dashoffset: 0; opacity: 1; }} 60%, 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
    @keyframes ce-fill {{ from {{ transform: scaleX(0); }} to {{ transform: none; }} }}
    @media (prefers-reduced-motion: reduce) {{ .ce-tile, .ce-fill {{ animation: none; }} .ce-edge {{ display: none; }} }}
  </style>
  <rect width="1200" height="420" rx="20" fill="url(#ce-bg)"/>
  <rect width="1200" height="420" rx="20" fill="url(#ce-glow)"/>
  <rect x=".5" y=".5" width="1199" height="419" rx="19.5" fill="none" stroke="{ACC}" stroke-opacity=".18"/>
{body}
</svg>"""


# ---- Footer signature ---------------------------------------------------
def footer():
    import random
    rnd = random.Random(25)
    sparks = "\n".join(
        f'    <circle cx="{rnd.randint(140, 1060)}" cy="230" r="{rnd.uniform(1, 2):.1f}"><animate attributeName="cy" values="232;{rnd.randint(40, 120)}" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;.85;0" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>'
        for d, b in ((rnd.uniform(4.2, 7.4), rnd.uniform(0, 5.5)) for _ in range(16)))
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 230" width="1200" height="230" role="img" aria-labelledby="sig-title">
  <title id="sig-title">Komal — Agents that listen. Systems that hold.</title>
  <defs>
    <linearGradient id="sig-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{DEEP}"/>
      <stop offset="1" stop-color="{BG}"/>
    </linearGradient>
    <radialGradient id="sig-glow" cx="50%" cy="100%" r="70%">
      <stop offset="0" stop-color="{GLOW}" stop-opacity=".6"/>
      <stop offset="1" stop-color="{MDEEP}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="sig-line" gradientUnits="userSpaceOnUse" x1="100" y1="0" x2="1100" y2="0">
      <stop offset="0" stop-color="{GLOW}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{ACC}"/>
      <stop offset="1" stop-color="{GLOW}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
{fonts("sig")}
    .sig-name {{
      stroke: {LIGHT}; stroke-width: 1; fill: {LIGHT}; fill-opacity: 0;
      stroke-dasharray: 900; stroke-dashoffset: 900;
      animation: sig-write 3.6s cubic-bezier(.65,0,.35,1) .3s forwards;
    }}
    .sig-rule {{ stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: sig-draw 2.4s cubic-bezier(.65,0,.35,1) 1.6s forwards; }}
    .sig-in {{ animation: sig-in 1.4s ease 2.6s both; }}
    @keyframes sig-write {{ 70% {{ stroke-dashoffset: 0; fill-opacity: 0; }} 100% {{ stroke-dashoffset: 0; fill-opacity: 1; }} }}
    @keyframes sig-draw {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes sig-in {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .sig-name {{ animation: none; stroke-dashoffset: 0; fill-opacity: 1; }}
      .sig-rule {{ animation: none; stroke-dashoffset: 0; }}
      .sig-in {{ animation: none; }}
      .sig-sparks {{ display: none; }}
    }}
  </style>

  <rect width="1200" height="230" rx="20" fill="url(#sig-bg)"/>
  <rect width="1200" height="230" rx="20" fill="url(#sig-glow)"/>

  <g class="sig-sparks" fill="{LIGHT}" opacity=".9">
{sparks}
  </g>

  <text class="sig-serif sig-name" x="600" y="104" text-anchor="middle" font-size="76" font-style="italic" font-weight="300" letter-spacing="-1">Komal</text>

  <path class="sig-rule" d="M100 134 H1100" stroke="url(#sig-line)" stroke-width="1"/>
  <circle cx="600" cy="134" r="3" fill="{TEXT}" class="sig-in">
    <animate attributeName="r" values="3;5;3" dur="3.2s" repeatCount="indefinite"/>
  </circle>

  <g class="sig-in">
    <text class="sig-serif" x="600" y="176" text-anchor="middle" font-size="20" font-style="italic" fill="{TEXT}">Agents that listen. Systems that hold.</text>
    <text class="sig-mono" x="600" y="206" text-anchor="middle" font-size="11" letter-spacing="3" fill="{MUTE}">AGENTIC AI · DISTRIBUTED SYSTEMS · NEW DELHI</text>
  </g>
</svg>"""


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    write("komal-hero-portrait.svg", hero())
    for slug, *args in TITLES:
        write(f"title-{slug}.svg", title(slug, *args))
    write("about-intro.svg", about())
    write("recognition.svg", recognition())
    write("experience-trading-engine.svg", experience_trading())
    write("project-sakhi.svg", project_sakhi())
    write("project-tickless.svg", project_tickless())
    write("tech-constellation.svg", toolkit())
    write("education.svg", education())
    write("footer-signature.svg", footer())
