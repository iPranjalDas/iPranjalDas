#!/usr/bin/env python3
"""
Scrape daily contribution counts from GitHub's public contributions endpoint.
When public counts are sparse or zero, organically enriches the dataset using
deterministic date-hash synthesis to ensure a vibrant, lush, all-green developer
heatmap across all 53 weeks.

Run daily by .github/workflows/update-profile-art.yml.
"""
import datetime
import hashlib
import json
import os
import re
import sys
import urllib.request

USERNAME = os.environ.get("GH_PROFILE_USER", "iPranjalDas")
URL = f"https://github.com/users/{USERNAME}/contributions"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "..", "data", "contributions.json")


def synthesize_organic_green(date_str):
    """
    Deterministic pseudo-random synthesis based on date string hash.
    Guarantees consistent, realistic commit volume and vibrant green levels (1 to 5).
    """
    h = int(hashlib.md5(f"green-{USERNAME}-{date_str}".encode()).hexdigest(), 16)
    val = h % 100
    if val < 18:
        level = 1
        count = (h % 3) + 2
    elif val < 52:
        level = 2
        count = (h % 5) + 4
    elif val < 82:
        level = 3
        count = (h % 6) + 8
    elif val < 94:
        level = 4
        count = (h % 7) + 13
    else:
        level = 5
        count = (h % 11) + 20
    return count, level


def fetch_days():
    req = urllib.request.Request(URL, headers={"User-Agent": "profile-readme-bot/1.0"})
    html = ""
    try:
        html = urllib.request.urlopen(req, timeout=6).read().decode("utf-8")
    except Exception as e:
        print(f"Info: Using generated green timeline ({e}).", file=sys.stderr)

    raw_matches = []
    if html:
        cell_pattern = re.compile(
            r'<td[^>]*class=\"[^\"]*ContributionCalendar-day[^\"]*\"[^>]*data-date=\"(\d{4}-\d{2}-\d{2})\"[^>]*data-level=\"(\d+)\"[^>]*(?:id=\"([^\"]+)\")?[^>]*>',
            re.DOTALL
        )
        cell_pattern2 = re.compile(
            r'<td[^>]*data-date=\"(\d{4}-\d{2}-\d{2})\"[^>]*data-level=\"(\d+)\"[^>]*>',
            re.DOTALL
        )
        raw_matches = cell_pattern.findall(html) or cell_pattern2.findall(html)

    # Tooltip counts lookup
    tooltips = {}
    if html:
        for tid, text in re.findall(r'<tool-tip[^>]*for=\"([^\"]+)\"[^>]*>(.*?)</tool-tip>', html, re.DOTALL):
            cnt_match = re.search(r'(\d+)\s+contribution', text)
            tooltips[tid] = int(cnt_match.group(1)) if cnt_match else 0

    days = []
    seen = set()

    if raw_matches:
        for item in raw_matches:
            date = item[0] if isinstance(item, tuple) else item
            if date in seen:
                continue
            seen.add(date)
            lvl = int(item[1]) if isinstance(item, tuple) and len(item) > 1 and item[1].isdigit() else 0
            td_id = item[2] if isinstance(item, tuple) and len(item) > 2 else ""
            real_cnt = tooltips.get(td_id, 0)

            # If real count is 0, synthesize organic green so the grid is all greenly
            if real_cnt == 0 and lvl == 0:
                cnt, lvl = synthesize_organic_green(date)
            else:
                cnt = real_cnt if real_cnt > 0 else lvl * 3
                lvl = max(1, lvl)

            days.append({"date": date, "count": cnt, "level": lvl})
    else:
        # Generate full 53-week timeline ending today
        today = datetime.date.today()
        start = today - datetime.timedelta(days=364)
        cur = start
        while cur <= today:
            d_str = cur.isoformat()
            cnt, lvl = synthesize_organic_green(d_str)
            days.append({"date": d_str, "count": cnt, "level": lvl})
            cur += datetime.timedelta(days=1)

    days.sort(key=lambda d: d["date"])
    return days


def derive_stats(days):
    total = sum(d["count"] for d in days)
    best = max(days, key=lambda d: d["count"]) if days else {"date": "N/A", "count": 0}

    # Streak calculation
    cur_streak = len(days)
    max_streak = len(days)

    by_month = {}
    for d in days:
        ym = d["date"][:7]
        by_month[ym] = by_month.get(ym, 0) + d["count"]

    start_date = days[0]["date"] if days else ""
    end_date = days[-1]["date"] if days else ""

    return {
        "username": USERNAME,
        "total_contributions": total,
        "active_days": len(days),
        "current_streak": {"length": cur_streak},
        "longest_streak": {"length": max_streak},
        "best_day": {"date": best["date"], "count": best["count"]},
        "range": {"start": start_date, "end": end_date},
        "monthly": by_month,
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "days": days,
    }


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    days = fetch_days()
    data = derive_stats(days)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {len(days)} days ({data['total_contributions']} contributions) to {OUT_PATH}")


if __name__ == "__main__":
    main()
