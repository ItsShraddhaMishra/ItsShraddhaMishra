from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape


DATA_FILE = Path("data/scholar_publications.json")
README = Path("README.md")


def make_publications_md(data: dict) -> str:
    publications = data.get("publications", [])

    lines = []
    lines.append("<!-- PUBLICATIONS:START -->")
    lines.append("")
    lines.append("| Paper | Year | Citations |")
    lines.append("|---|---:|---:|")

    for pub in publications:
        title = pub.get("title", "Untitled")
        year = pub.get("year", "")
        citations = pub.get("citations", 0)
        url = pub.get("url") or data.get("scholar_url", "")

        safe_title = title.replace("|", "\\|")
        lines.append(f"| [{safe_title}]({url}) | {year} | {citations} |")

    if not publications:
        lines.append("| Scholar data not fetched yet. | — | — |")

    lines.append("")
    lines.append(f"_Updated automatically from Google Scholar: {data.get('updated_at', 'unknown')}._")
    lines.append("")
    lines.append("<!-- PUBLICATIONS:END -->")

    return "\n".join(lines)


def main() -> None:
    if not DATA_FILE.exists():
        raise SystemExit(f"Missing {DATA_FILE}. Run fetch_scholar_publications.py first.")

    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    readme = README.read_text(encoding="utf-8")

    start = "<!-- PUBLICATIONS:START -->"
    end = "<!-- PUBLICATIONS:END -->"

    if start not in readme or end not in readme:
        raise SystemExit("README.md must contain PUBLICATIONS:START and PUBLICATIONS:END markers.")

    before = readme.split(start)[0]
    after = readme.split(end)[1]

    updated = before + make_publications_md(data) + after
    README.write_text(updated, encoding="utf-8")

    print("OK  README.md publications block updated.")


if __name__ == "__main__":
    main()
