#!/usr/bin/env python3
"""
Generate a unified, dual-pane terminal hero SVG (860x410) for Pranjal Das:
- Left pane: Monochrome cybernetic ASCII art text portrait generated from
  real GitHub profile picture (pfp.png) with line-by-line typing animation
  and online status prompt.
- Center: Elegant vertical dashed terminal divider rule.
- Right pane: Staggered Neofetch info card (INFERICS, VEX Robotics, Stack, Rig).
- Exactly 860px wide to match contrib-heatmap.svg with zero table borders.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "terminal-hero.svg")

W, H = 860, 410
PAD = 22
TITLEBAR_H = 30
MID_X = 380  # divider line

BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"
FRAME_MUTED = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"
SECTION = "#58a6ff"
GREEN = "#3fb950"
NEON_GREEN = "#56f594"
ACCENT = "#22d3ee"
GOLD = "#f2cc60"

# Tuned ASCII portrait extracted from pfp.png (38 cols x 24 rows)
PFP_ASCII = [
    r"    #*@@@@@@@@@@@@*#%####*###****=    ",
    r"    ##@@@@@@@@@@@@@#@%+=--::...       ",
    r"      +#@**@@@@@@@@@%@@                ",
    r"      +##=#@@@@@@@@@@#                ",
    r"      *--=%@%@@@@@@@@                 ",
    r"      .--=+==++*@@@@-               ..",
    r"   .:+*=#*=-=++%@@@@.         ......::",
    r".:=+@@#=+**+**#@@@@-   ............:::",
    r"+*%#@@#++*###%%#@@*=-. ..........:::::",
    r"**%@@@@@@%@%##%@@@%*#=.......::::-----",
    r"**#@@@@@@@%%##@@@@@%%#=..:::::----====",
    r"%@%%@@@@@@@@@@@@%@@@@%#:::::---===+++= ",
    r"@@%%@@@@@@@@@@@@@@@@@@@=:----====+++++",
    r"@@@@@@@@@@@@@@@@@@@@@@@+---=======+===",
    r"%@@@@@@@@@@@@@@@@@@@@@@+:-------------",
    r"@@@@@@@@@@@@@@@@@@@@@@@*...::::::---==",
    r"@@@@@@@@@@@@@@@@@@@@@@@#: ..:::------:",
    r"@@@@@@@@@@@@@@@@@@@@@@@@+::--:::..   .",
    r"@@@@@@@@@@@@@@@@@@@@@@@@%..      ..:::",
    r"@@@@@@@@@@@@@@@@@@@@@@@@#   ...::::---",
    r"@%@@@@@@@@@@@@@@@@@@@@%*#=.:::-----:::",
    r"#%@@@@%%%%#####%%%@@@@%*+*:::::::::...",
    r"@@%@@#*******######@@@@%*#=.......    ",
    r"@%*#%###**#######*+*@@@@%#+..:      .:",
]

NEOFETCH_ROWS = [
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
@keyframes wipe {
  0% { opacity: 0; transform: translateX(-5px); }
  100% { opacity: 1; transform: translateX(0); }
}
@keyframes blink {
  0%, 49% { opacity: 1; }
  50%, 100% { opacity: 0; }
}
.cursor { animation: blink 0.9s infinite; }
.fade-in { animation: wipe 0.35s ease-out backwards; }
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="thbg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
        '</linearGradient>',
        # Iridescent cyberpunk gradient for ASCII art portrait
        f'<linearGradient id="pfp_grad" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0%" stop-color="{ACCENT}"/>',
        f'<stop offset="55%" stop-color="#38bdf8"/>',
        f'<stop offset="100%" stop-color="{GREEN}"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#thbg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1.2" stroke-opacity="0.55"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.35"/>',
    ]

    # Title bar window buttons
    for i, col in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{col}"/>')
    parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
                 f'text-anchor="middle">pranjal@VoltDeck: ~ (profile pfp &amp; neofetch)</text>')

    # Vertical divider line separating left and right panes
    parts.append(f'<line x1="{MID_X}" y1="{TITLEBAR_H}" x2="{MID_X}" y2="{H}" stroke="{FRAME_MUTED}" stroke-opacity="0.4" stroke-dasharray="4,4"/>')

    # ------------------ LEFT PANE: ASCII PFP PORTRAIT ------------------
    # Header above portrait
    header_y = TITLEBAR_H + 22
    parts.append(
        f'<text class="fade-in" x="{MID_X/2}" y="{header_y}" fill="{SECTION}" font-size="11" font-weight="700" '
        f'text-anchor="middle" style="animation-delay:0.05s;">'
        f'PRANJAL DAS [INFERICS IoT &amp; CV]</text>'
    )

    art_start_y = header_y + 16
    line_spacing = 12.8
    for i, row in enumerate(PFP_ASCII):
        y = art_start_y + i * line_spacing
        delay = 0.08 + i * 0.025
        parts.append(
            f'<text class="fade-in" x="{MID_X/2}" y="{y:.1f}" fill="url(#pfp_grad)" font-size="9.4" '
            f'font-weight="600" text-anchor="middle" style="animation-delay:{delay:.3f}s;">'
            f'{esc(row)}</text>'
        )

    # Terminal prompt under portrait
    prompt_y = H - 16
    parts.append(
        f'<text x="{PAD + 4}" y="{prompt_y}" font-size="11.5" fill="{MUTED}">'
        f'<tspan fill="{GREEN}">❯</tspan> pfp: <tspan fill="{ACCENT}">ascii_render</tspan> · '
        f'status: <tspan fill="{NEON_GREEN}">online</tspan> '
        f'<tspan class="cursor" fill="{GREEN}">▋</tspan></text>'
    )

    # ------------------ RIGHT PANE: NEOFETCH CARD ------------------
    rx = MID_X + 25
    val_rx = rx + 95
    ry = TITLEBAR_H + 24
    r_delay = 0.12

    for row in NEOFETCH_ROWS:
        kind = row[0]
        delay_style = f'style="animation-delay:{r_delay:.2f}s"'

        if kind == "host":
            parts.append(f'<g class="fade-in" {delay_style}>')
            parts.append(f'<text x="{rx}" y="{ry}" font-size="13" font-weight="700">'
                         f'<tspan fill="{ACCENT}">pranjal</tspan>'
                         f'<tspan fill="{MUTED}">@</tspan>'
                         f'<tspan fill="{GREEN}">VoltDeck</tspan></text>')
            rule_y = ry + 7
            parts.append(f'<line x1="{rx}" y1="{rule_y}" x2="{W - PAD}" y2="{rule_y}" '
                         f'stroke="{FRAME_MUTED}" stroke-dasharray="3,3" stroke-opacity="0.4"/>')
            parts.append('</g>')
            ry += 19
            r_delay += 0.05

        elif kind == "kv":
            k, v = row[1], row[2]
            parts.append(f'<g class="fade-in" {delay_style}>'
                         f'<text x="{rx}" y="{ry}" font-size="11.5" fill="{KEY}">{esc(k)}</text>'
                         f'<text x="{val_rx}" y="{ry}" font-size="11.5" fill="{INK}">{esc(v)}</text>'
                         f'</g>')
            ry += 21.5
            r_delay += 0.035

        elif kind == "sec":
            title = row[1]
            parts.append(f'<g class="fade-in" {delay_style}>'
                         f'<text x="{rx}" y="{ry}" font-size="11" font-weight="700" fill="{SECTION}">'
                         f'&#9472;&#9472; {esc(title)} &#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;</text>'
                         f'</g>')
            ry += 20.5
            r_delay += 0.035

        elif kind == "bul":
            text = row[1]
            parts.append(f'<g class="fade-in" {delay_style}>'
                         f'<circle cx="{rx + 4}" cy="{ry - 4}" r="2.5" fill="{GREEN}"/>'
                         f'<text x="{rx + 16}" y="{ry}" font-size="11" fill="{INK}">{esc(text)}</text>'
                         f'</g>')
            ry += 21.5
            r_delay += 0.035

        elif kind == "gap":
            ry += 8

    parts.append("</svg>")
    return "".join(parts)


def main():
    svg = render()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT} ({len(svg)} bytes) - Dual-Pane Terminal Hero with PFP ASCII Art")


if __name__ == "__main__":
    main()
