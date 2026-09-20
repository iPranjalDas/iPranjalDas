#!/usr/bin/env python3
"""
Render data/contributions.json as an all-green, high-density terminal
GitHub-style contribution heatmap SVG:
- 53-week x 7-day grid of rounded boxes in lush, vibrant GitHub green shades
- One-shot diagonal cascade slide-down animation (CSS keyframes)
- Hacker-green accents, terminal title bar, Less->More green legend,
  and dedicated Daily Date & Activity Counts inspector.

Run by .github/workflows/update-profile-art.yml after fetch_contributions.py.
"""
import datetime
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "contrib-heatmap.svg")

# Rich, lush GitHub green palette (0 to 5)
PALETTE = [
    "#0e4429",  # Level 0/1 fallback: deep forest emerald
    "#0e4429",  # Level 1: forest green
    "#006d32",  # Level 2: classic rich green
    "#26a641",  # Level 3: bright grass green
    "#39d353",  # Level 4: vivid lime green
    "#56f594",  # Level 5: glowing neon electric mint
]

CELL = 12
GAP = 3
STEP = CELL + GAP
PAD = 22
LEFT_LABEL_W = 30
TOP_LABEL_H = 20
TITLEBAR_H = 30

BG = "#0a0e14"
BG2 = "#0d161a"
FRAME = "#238636"      # GitHub terminal green border
FRAME_MUTED = "#1e4028"
MUTED = "#7d8590"
TEXT = "#e6edf3"
ACCENT = "#22d3ee"
GREEN = "#39d353"
NEON_GREEN = "#56f594"
GOLD = "#f2cc60"

# Cascade delay timing (diagonal wave)
COL_T = 0.016
ROW_T = 0.040
CELL_DUR = 0.40


def level_for(count):
    if count == 0:
        return 1
    if count <= 4:
        return 1
    if count <= 9:
        return 2
    if count <= 16:
        return 3
    if count <= 24:
        return 4
    return 5


def build_grid(days):
    if not days:
        return []
    first = datetime.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7  # sunday=0
    grid = []
    col = [None] * lead_pad
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        lvl = d.get("level", level_for(d["count"]))
        lvl = max(1, min(5, lvl))  # Guarantee all greenly (1 to 5)
        col.append((d["date"], d["count"], lvl))
        if len(col) == 7:
            grid.append(col)
            col = []
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid


def render(data):
    days = data["days"]
    grid = build_grid(days)
    n_cols = len(grid)
    art_w = n_cols * STEP
    art_h = 7 * STEP

    month_labels = []
    seen_months = set()
    for ci, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = datetime.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((ci, date.strftime("%b")))
            break

    canvas_w = PAD + LEFT_LABEL_W + art_w + PAD
    stats_h = 112
    canvas_h = TITLEBAR_H + TOP_LABEL_H + art_h + stats_h + PAD

    css = f"""
@keyframes cell {{
  0%   {{ opacity: 0; transform: translateY(-7px) scale(0.9); }}
  100% {{ opacity: 1; transform: translateY(0) scale(1); }}
}}
.c {{ opacity: 0; animation: cell {CELL_DUR:.2f}s cubic-bezier(.2,.8,.2,1) forwards; }}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="hbg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="12" fill="url(#hbg)"/>',
        f'<rect x="0.5" y="0.5" width="{canvas_w-1}" height="{canvas_h-1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1.2" stroke-opacity="0.65"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{canvas_w}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.35"/>',
    ]

    # window buttons
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
    parts.append(f'<text x="{canvas_w/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
                 f'text-anchor="middle">pranjal@inferics: ~/contributions --graph --all-green</text>')

    grid_top = TITLEBAR_H + TOP_LABEL_H
    grid_left = PAD + LEFT_LABEL_W

    for ci, label in month_labels:
        x = grid_left + ci * STEP
        parts.append(f'<text x="{x}" y="{TITLEBAR_H + 14}" fill="{MUTED}" font-size="10">{label}</text>')

    for wi, wname in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = grid_top + wi * STEP + CELL * 0.78
        parts.append(f'<text x="{PAD}" y="{y:.1f}" fill="{MUTED}" font-size="9">{wname}</text>')

    # The green boxes
    for ci, column in enumerate(grid):
        gx = grid_left + ci * STEP
        for ri, cell in enumerate(column):
            if cell is None:
                continue
            date_s, count, lvl = cell
            gy = grid_top + ri * STEP
            delay = ci * COL_T + ri * ROW_T
            plural = "s" if count != 1 else ""
            color = PALETTE[lvl]
            parts.append(
                f'<rect class="c" x="{gx}" y="{gy}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill="{color}" style="animation-delay:{delay:.3f}s">'
                f'<title>{date_s}: {count} contribution{plural}</title></rect>'
            )

    # Green legend: Less [][][][][] More
    leg_y = grid_top + art_h + 6
    legend_shades = ["#0e4429", "#006d32", "#26a641", "#39d353", "#56f594"]
    leg_x = canvas_w - PAD - (len(legend_shades) * (CELL - 1) + 70)
    parts.append(f'<text x="{leg_x}" y="{leg_y + CELL*0.8:.1f}" fill="{MUTED}" font-size="10" text-anchor="end">Less</text>')
    lx = leg_x + 8
    for color in legend_shades:
        parts.append(f'<rect x="{lx}" y="{leg_y}" width="{CELL-1}" height="{CELL-1}" rx="2.2" fill="{color}"/>')
        lx += CELL
    parts.append(f'<text x="{lx + 4}" y="{leg_y + CELL*0.8:.1f}" fill="{MUTED}" font-size="10">More</text>')

    sep_y = leg_y + CELL + 14
    parts.append(f'<line x1="0" y1="{sep_y}" x2="{canvas_w}" y2="{sep_y}" stroke="{FRAME}" stroke-opacity="0.3"/>')

    cs = data.get("current_streak", {}).get("length", len(days))
    ls = data.get("longest_streak", {}).get("length", len(days))
    total = data.get("total_contributions", sum(d["count"] for d in days))
    best = data.get("best_day", {"count": 0, "date": "N/A"})
    rng = data.get("range", {"start": "", "end": ""})

    ly = sep_y + 22
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="13" fill="{GREEN}">'
                 f'<tspan font-weight="700">{total:,}</tspan>'
                 f'<tspan fill="{MUTED}"> contributions in the last year</tspan></text>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{MUTED}" text-anchor="end">'
                 f'{rng.get("start", "")} &#8594; {rng.get("end", "")}</text>')
    ly += 22
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="13" fill="{MUTED}">current streak '
                 f'<tspan fill="{NEON_GREEN}" font-weight="700">{cs} days</tspan>'
                 f'<tspan fill="{MUTED}">   &#183;   longest </tspan>'
                 f'<tspan fill="{NEON_GREEN}" font-weight="700">{ls} days</tspan></text>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{MUTED}" text-anchor="end">'
                 f'best day <tspan fill="{GOLD}" font-weight="700">{best.get("count", 0)}</tspan> on {best.get("date", "N/A")}</text>')

    # Activity Inspector line: showing recent dates and exact contribution counts
    ly += 22
    recent_samples = days[-5:] if len(days) >= 5 else days
    sample_text = "   ".join([f'<tspan fill="{MUTED}">{d["date"]}:</tspan> <tspan fill="{NEON_GREEN}" font-weight="700">{d["count"]}c</tspan>' for d in reversed(recent_samples)])
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="11" fill="{MUTED}">'
                 f'<tspan fill="{ACCENT}" font-weight="700">Recent Dates &amp; Counts:</tspan>   {sample_text}</text>')

    parts.append("</svg>")
    return "".join(parts)


def main():
    if not os.path.exists(IN_PATH):
        print(f"Error: {IN_PATH} not found.", file=sys.stderr)
        return
    with open(IN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    svg = render(data)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH} ({len(svg)} bytes) - All Greenly Render Complete")


if __name__ == "__main__":
    main()
