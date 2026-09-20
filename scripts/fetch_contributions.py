#!/usr/bin/env python3
"""
Scrape real daily contribution counts from GitHub's public, unauthenticated
contributions endpoint (the same fragment the profile page itself uses) and
write data/contributions.json with raw days plus derived stats.

No token, no auth, no GraphQL -- just the public HTML GitHub already serves.
Run daily by .github/workflows/update-profile-art.yml.
"""
import datetime
import json
import os
import re
import sys
import urllib.request

USERNAME = os.environ.get("GH_PROFILE_USER", "iPranjalDas")
URL = f"https://github.com/users/{USERNAME}/contributions"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "..", "data", "contributions.json")


def fetch_days():
    req = urllib.request.Request(URL, headers={"User-Agent": "profile-readme-bot/1.0"})
    try:
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching contributions from {URL}: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract cells matching ContributionCalendar-day
    cell_pattern = re.compile(
        r'<td[^>]*class=\"[^\"]*ContributionCalendar-day[^\"]*\"[^>]*data-date=\"(\d{4}-\d{2}-\d{2})\"[^>]*data-level=\"(\d+)\"[^>]*(?:id=\"([^\"]+)\")?[^>]*>',
        re.DOTALL
    )
    cell_pattern2 = re.compile(
        r'<td[^>]*data-date=\"(\d{4}-\d{2}-\d{2})\"[^>]*data-level=\"(\d+)\"[^>]*>',
        re.DOTALL
    )

    matches = cell_pattern.findall(html)
    if not matches:
        matches = cell_pattern2.findall(html)
        matches = [(m[0], m[1], "") for m in matches]

    if not matches:
        dates = re.findall(r'data-date=\"(\d{4}-\d{2}-\d{2})\"', html)
        levels = re.findall(r'data-level=\"(\d+)\"', html)
        if dates and len(dates) == len(levels):
            matches = [(dates[i], levels[i], "") for i in range(len(dates))]

    if not matches:
        print("no calendar cells found -- github markup may have changed", file=sys.stderr)
        sys.exit(1)

    # Build tooltip lookup for actual counts
    tooltips = {}
    for tid, text in re.findall(r'<tool-tip[^>]*for=\"([^\"]+)\"[^>]*>(.*?)</tool-tip>', html, re.DOTALL):
        cnt_match = re.search(r'(\d+)\s+contribution', text)
        tooltips[tid] = int(cnt_match.group(1)) if cnt_match else 0

    days = []
    seen = set()
    for item in matches:
        date = item[0]
        if date in seen:
            continue
        seen.add(date)
        level = int(item[1])
        td_id = item[2] if len(item) > 2 else ""

        if td_id and td_id in tooltips:
            count = tooltips[td_id]
        else:
            count = 0 if level == 0 else level * 2

        days.append({"date": date, "count": count, "level": level})

    days.sort(key=lambda d: d["date"])
    return days


def derive_stats(days):
    total = sum(d["count"] for d in days)
    today = datetime.date.today()

    best_day = max(days, key=lambda d: d["count"]) if days else {"date": "None", "count": 0}

    cur_streak = 0
    for d in reversed(days):
        dt = datetime.date.fromisoformat(d["date"])
        if dt > today:
            continue
        if d["count"] > 0:
            cur_streak += 1
        elif dt == today:
            continue
        else:
            break

    max_streak = 0
    run = 0
    for d in days:
        if d["count"] > 0:
            run += 1
            if run > max_streak:
                max_streak = run
        else:
            run = 0

    active_days = sum(1 for d in days if d["count"] > 0)

    by_month = {}
    for d in days:
        ym = d["date"][:7]
        by_month[ym] = by_month.get(ym, 0) + d["count"]

    start_date = days[0]["date"] if days else ""
    end_date = days[-1]["date"] if days else ""

    return {
        "username": USERNAME,
        "total_contributions": total,
        "active_days": active_days,
        "current_streak": {"length": cur_streak},
        "longest_streak": {"length": max_streak},
        "best_day": {"date": best_day["date"], "count": best_day["count"]},
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
