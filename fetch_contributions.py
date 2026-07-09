# fetch_contributions.py

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

from readme_config import load_config, require_github_token


QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            color
            weekday
          }
        }
      }
    }
  }
}
"""


def main() -> None:
    config = load_config()
    github_token = require_github_token()

    out_path = config.data_dir / "contributions.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    to_dt = datetime.now(timezone.utc)
    from_dt = to_dt - timedelta(days=365)

    variables = {
        "login": config.github_username,
        "from": from_dt.isoformat(),
        "to": to_dt.isoformat(),
    }

    response = requests.post(
        "https://api.github.com/graphql",
        headers={
            "Authorization": f"Bearer {github_token}",
            "Content-Type": "application/json",
        },
        json={"query": QUERY, "variables": variables},
        timeout=30,
    )

    response.raise_for_status()
    payload = response.json()

    if "errors" in payload:
        raise RuntimeError(json.dumps(payload["errors"], indent=2))

    user = payload.get("data", {}).get("user")
    if user is None:
        raise RuntimeError(f"GitHub user not found: {config.github_username}")

    calendar = user["contributionsCollection"]["contributionCalendar"]

    days = []
    for week_index, week in enumerate(calendar["weeks"]):
        for day in week["contributionDays"]:
            days.append(
                {
                    "week": week_index,
                    "weekday": day["weekday"],
                    "date": day["date"],
                    "count": day["contributionCount"],
                    "github_color": day["color"],
                }
            )

    out_path.write_text(
        json.dumps(
            {
                "username": config.github_username,
                "display_name": config.display_name,
                "theme": config.theme,
                "generated_at": to_dt.isoformat(),
                "total_contributions": calendar["totalContributions"],
                "days": days,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
