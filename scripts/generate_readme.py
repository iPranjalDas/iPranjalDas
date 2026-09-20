#!/usr/bin/env python3
"""
Generate README.md for iPranjalDas profile:
- Clean terminal hero (terminal-hero.svg, 860px) with NO prompt headings
- All-green animated contribution heatmap (contrib-heatmap.svg, 860px)
- Native Interactive Hover Tooltip Grid: every cell displays tooltip on mouse hover
  showing the exact date and number of contributions (e.g., '2026-09-20: 12 contributions')
- Collapsible detailed table of all recent dates and activity numbers
- Verified badges & bio
"""
import datetime
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "..", "data", "contributions.json")
README_PATH = os.path.join(HERE, "..", "README.md")


def generate():
    days = []
    total = 3246
    streak = 365
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            days = data.get("days", [])
            total = data.get("total_contributions", total)
            streak = data.get("current_streak", {}).get("length", streak)

    # Build interactive hover grid (weeks row-by-row with native markdown tooltips)
    # 7 days per row for the last 5 weeks
    recent_days = days[-35:] if len(days) >= 35 else days
    hover_rows = []
    
    # Header for interactive hover grid
    hover_grid_header = "**Hover over any cell below to view the exact date and contributions count:**\n\n"
    
    grid_lines = []
    # Divide recent_days into chunks of 7 (one row per week)
    for i in range(0, len(recent_days), 7):
        chunk = recent_days[i:i+7]
        row_str = " &nbsp; ".join([
            f'[{ "🟩" if d.get("level", 1) < 4 else "🟢" }](https://github.com/iPranjalDas "{d["date"]}: {d["count"]} contribution{"s" if d["count"]!=1 else ""}")'
            for d in chunk
        ])
        start_d = chunk[0]["date"]
        end_d = chunk[-1]["date"]
        grid_lines.append(f"`{start_d}` &nbsp; {row_str} &nbsp; `{end_d}`")

    interactive_hover_block = "\n<br>\n".join(grid_lines)

    # Build daily log table for recent 35 days
    table_lines = [
        "| Date | Day | Daily Contributions | Intensity |",
        "| :--- | :--- | :---: | :--- |",
    ]
    for d in reversed(recent_days):
        dt = datetime.date.fromisoformat(d["date"])
        wname = dt.strftime("%A")
        lvl = d.get("level", 1)
        cnt = d.get("count", 1)
        bar = "🟩" * lvl
        table_lines.append(f"| `{d['date']}` | {wname} | **{cnt} contributions** | {bar} (Level {lvl}) |")

    daily_table = "\n".join(table_lines)

    content = f"""<div align="center">

<!-- ======================================================== -->
<!-- UNIFIED DUAL-PANE TERMINAL HERO (ASCII + NEOFETCH)       -->
<!-- ======================================================== -->

<img src="./terminal-hero.svg" width="860" alt="Pranjal Das — System Profile & Neofetch Terminal" />

<br>
<br>

<!-- ======================================================== -->
<!-- ALL-GREEN ANIMATED CONTRIBUTION HEATMAP (53 WEEKS)       -->
<!-- ======================================================== -->

<a href="./contrib-heatmap.svg" title="Click to open standalone SVG with native element inspection">
  <img src="./contrib-heatmap.svg" width="860" alt="Pranjal's Live Contribution Heatmap — All Green" />
</a>

<br>
<br>

<!-- ======================================================== -->
<!-- NATIVE HOVER TOOLTIP CALENDAR GRID                       -->
<!-- Hover over any cell to see: Date + Number of Commits     -->
<!-- ======================================================== -->

<p><b>🖱️ Interactive Calendar Matrix (Hover each cell for Date &amp; Commits count):</b></p>

{interactive_hover_block}

<br>
<br>

<!-- ======================================================== -->
<!-- INTERACTIVE DAILY ACTIVITY LOG (DATES & COUNTS)          -->
<!-- ======================================================== -->

<details>
<summary><b>📅 View Complete Daily Activity Log (Exact Dates &amp; Commit Counts)</b></summary>

<br>

> **Total Recorded Contributions:** {total:,} &nbsp;|&nbsp; **Active Streak:** {streak} Days &nbsp;|&nbsp; **Status:** Continuous Deployment

{daily_table}

<br>

<sub><i>Showing recent 35-day active cycle. Auto-refreshed daily by GitHub Actions cron.</i></sub>

</details>

<br>

<!-- ======================================================== -->
<!-- LABS, HONORS & VERIFIED IDENTITIES                       -->
<!-- ======================================================== -->

<p><b>IoT &amp; Computer Vision Researcher · Robotics Engineer · Systems Builder</b></p>

[![INFERICS](https://img.shields.io/badge/Lab-INFERICS-0d1117?style=for-the-badge&logo=electron&logoColor=22d3ee)](https://github.com/iPranjalDas)
[![VEX Robotics](https://img.shields.io/badge/VEX_Robotics-Bronze_Medalist-orange?style=for-the-badge&logo=open-access&logoColor=white)](https://github.com/iPranjalDas)
[![INSPIRE Awards](https://img.shields.io/badge/Govt-INSPIRE_MANAK-58a6ff?style=for-the-badge&logo=shield&logoColor=white)](https://github.com/iPranjalDas)
[![GitHub](https://img.shields.io/badge/GitHub-iPranjalDas-39d353?style=for-the-badge&logo=github&logoColor=white)](https://github.com/iPranjalDas)

<br>

</div>
"""
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote {README_PATH} with interactive hover tooltips")


if __name__ == "__main__":
    generate()
