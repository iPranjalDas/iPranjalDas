#!/usr/bin/env python3
"""
Generate an animated terminal-style ASCII wordmark SVG for PRANJAL:
Features terminal title bar, window controls, typing wipe effect,
cyan/green terminal accents, and subtitle.
Width: 380, Height: 380 to pair with info-card.svg (480) matching
contrib-heatmap.svg (860) cleanly.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "wordmark.svg")

W, H = 380, 380
PAD = 20
TITLEBAR_H = 30

BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"
MUTED = "#7d8590"
INK = "#e6edf3"
ACCENT = "#22d3ee"
GREEN = "#39d353"
GOLD = "#f2cc60"

ASCII_ART = [
    r"  ____  ____     _    _  _     _   _    _     ",
    r" |  _ \|  _ \   / \  | \| | _ | | / \  | |    ",
    r" | |_) | |_) | / _ \ | .` || || |/ _ \ | |    ",
    r" |  __/|  _ < / ___ \| |\ || || / ___ \| |___ ",
    r" |_|   |_| \_/_/   \_|_| \_|\__//_/   \_\_____|",
]

SUBTITLE_LINES = [
    "[+] INFERICS IoT & CV Lab",
    "[+] VEX Robotics Competitor",
    "[+] Embedded Linux Systems",
    "[+] Autonomous Hardware & AI",
]


def render():
    css = """
@keyframes wipe {
  0% { width: 0; }
  100% { width: 100%; }
}
@keyframes blink {
  0%, 49% { opacity: 1; }
  50%, 100% { opacity: 0; }
}
@keyframes pulse {
  0%, 100% { opacity: 0.9; }
  50% { opacity: 0.4; }
}
.cursor { animation: blink 0.9s infinite; }
.line { opacity: 0; animation: wipe 0.5s ease-out forwards; }
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="wbg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#wbg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.5"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.3"/>',
    ]

    # window buttons
    for i, col in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{col}"/>')
    parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
                 f'text-anchor="middle">pranjal@github: ~ (id)</text>')

    # ASCII art block
    art_y = TITLEBAR_H + 45
    line_spacing = 18
    for i, row in enumerate(ASCII_ART):
        y = art_y + i * line_spacing
        delay = 0.15 + i * 0.08
        parts.append(
            f'<text x="{W/2}" y="{y}" fill="{ACCENT}" font-size="12" font-weight="700" '
            f'text-anchor="middle" style="animation: wipe 0.4s ease-out {delay:.2f}s forwards;">'
            f'{html.escape(row)}</text>'
        )

    # Divider
    div_y = art_y + len(ASCII_ART) * line_spacing + 15
    parts.append(f'<line x1="{PAD}" y1="{div_y}" x2="{W - PAD}" y2="{div_y}" '
                 f'stroke="{FRAME}" stroke-dasharray="4,4" stroke-opacity="0.4"/>')

    # Status / Subtitle section
    sub_y = div_y + 26
    for j, sline in enumerate(SUBTITLE_LINES):
        y = sub_y + j * 24
        s_delay = 0.6 + j * 0.1
        accent_col = GREEN if j == 0 else (GOLD if j == 1 else INK)
        parts.append(
            f'<text x="{PAD + 10}" y="{y}" fill="{accent_col}" font-size="12" '
            f'style="opacity:0; animation: wipe 0.3s ease-out {s_delay:.2f}s forwards;">'
            f'{html.escape(sline)}</text>'
        )

    # Shell prompt at bottom
    prompt_y = H - 25
    parts.append(
        f'<text x="{PAD}" y="{prompt_y}" font-size="12" fill="{MUTED}">'
        f'<tspan fill="{GREEN}">❯</tspan> status: <tspan fill="{ACCENT}">online</tspan> '
        f'<tspan class="cursor" fill="{GREEN}">▋</tspan></text>'
    )

    parts.append("</svg>")
    return "".join(parts)


def main():
    svg = render()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
