#!/usr/bin/env python3
"""
Build a neofetch-style info card SVG tailored for Pranjal Das:
Terminal title bar, colored key/value rows for research, robotics honors,
tech stack, and system architecture.

Lines fade and slide in on a short stagger so the panel appears to type
in real-time alongside the wordmark/portrait.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")

W, H = 480, 380
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 98
LINE_H = 21

BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"       # orange keys (neofetch style)
SECTION = "#58a6ff"   # blue section headers
GREEN = "#3fb950"
ACCENT = "#22d3ee"

ROWS = [
    ("host",),
    ("kv", "Role", "IoT & CV Researcher @ INFERICS"),
    ("kv", "Honors", "Bronze Medalist @ VEX Robotics"),
    ("kv", "Global", "Representing India in VEX Robotics"),
    ("kv", "Govt", "Ambassador @ INSPIRE Awards - MANAK"),
    ("gap",),
    ("sec", "Core Engineering Stack"),
    ("kv", "Languages", "Python, C++, C, JavaScript, Bash"),
    ("kv", "Vision & AI", "OpenCV, Computer Vision, Deep Learning"),
    ("kv", "Embedded", "ESP32, Arduino, Raspberry Pi, Robotics"),
    ("kv", "Systems", "Linux Kernel / WSL2, Docker, Sysinternals"),
    ("gap",),
    ("sec", "Primary Rig"),
    ("bul", "VoltDeck: AMD Ryzen 7 7445HS · RTX 3050 6GB"),
    ("bul", "Autonomous 24/7 Cloud Architecture"),
]


def esc(s):
    return html.escape(s)


def render():
    css = """
@keyframes line {
  0%   { opacity: 0; transform: translateX(-8px); }
  100% { opacity: 1; transform: translateX(0); }
}
.row { opacity: 0; animation: line 0.4s cubic-bezier(.2,.8,.2,1) forwards; }
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="cbg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#cbg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.5"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.3"/>',
    ]

    # window buttons
    for i, col in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{col}"/>')
    parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
                 f'text-anchor="middle">pranjal@VoltDeck: ~</text>')

    y = TITLEBAR_H + 24
    delay = 0.1

    for row in ROWS:
        kind = row[0]
        delay_style = f'style="animation-delay:{delay:.2f}s"'

        if kind == "host":
            parts.append(f'<g class="row" {delay_style}>')
            parts.append(f'<text x="{KEY_X}" y="{y}" font-size="13" font-weight="700">'
                         f'<tspan fill="{ACCENT}">pranjal</tspan>'
                         f'<tspan fill="{MUTED}">@</tspan>'
                         f'<tspan fill="{GREEN}">VoltDeck</tspan></text>')
            # dashed separator
            rule_y = y + 7
            parts.append(f'<line x1="{KEY_X}" y1="{rule_y}" x2="{W - PAD}" y2="{rule_y}" '
                         f'stroke="{FRAME}" stroke-dasharray="3,3" stroke-opacity="0.4"/>')
            parts.append('</g>')
            y += 18
            delay += 0.07

        elif kind == "kv":
            k, v = row[1], row[2]
            parts.append(f'<g class="row" {delay_style}>'
                         f'<text x="{KEY_X}" y="{y}" font-size="11.5" fill="{KEY}">{esc(k)}</text>'
                         f'<text x="{VAL_X}" y="{y}" font-size="11.5" fill="{INK}">{esc(v)}</text>'
                         f'</g>')
            y += LINE_H
            delay += 0.05

        elif kind == "sec":
            title = row[1]
            parts.append(f'<g class="row" {delay_style}>'
                         f'<text x="{KEY_X}" y="{y}" font-size="11" font-weight="700" fill="{SECTION}">'
                         f'&#9472;&#9472; {esc(title)} &#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;</text>'
                         f'</g>')
            y += LINE_H - 1
            delay += 0.05

        elif kind == "bul":
            text = row[1]
            parts.append(f'<g class="row" {delay_style}>'
                         f'<circle cx="{KEY_X + 4}" cy="{y - 4}" r="2.5" fill="{GREEN}"/>'
                         f'<text x="{KEY_X + 16}" y="{y}" font-size="11" fill="{INK}">{esc(text)}</text>'
                         f'</g>')
            y += LINE_H
            delay += 0.05

        elif kind == "gap":
            y += 6

    parts.append("</svg>")
    return "".join(parts)


def main():
    svg = render()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
