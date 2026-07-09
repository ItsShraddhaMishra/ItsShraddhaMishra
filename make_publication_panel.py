# ItsShraddhaMishra\make_publication_panel.py

"""
This module compiles: 
SVG panel = visual publication + citation bar chart
Markdown table = clickable paper hyperlinks
GitHub Actions = daily update
"""
from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

from ares_tron_theme import (
    get_theme,
    make_defs,
    make_common_style,
)


DATA_FILE = Path("data/scholar_publications.json")
OUT = Path("assets")
OUT.mkdir(exist_ok=True)


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def validate_svg(path: Path) -> None:
    ET.parse(path)
    print(f"OK  {path}")


def load_data() -> dict:
    if not DATA_FILE.exists():
        return {
            "updated_at": "not fetched yet",
            "scholar_url": "https://scholar.google.com/citations?user=O5pkUdUAAAAJ&hl=en",
            "name": "Shraddha Mishra",
            "total_citations": 0,
            "h_index": 0,
            "i10_index": 0,
            "cites_per_year": {},
            "publications": [],
        }

    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def make_publication_rows(publications: list[dict], theme, cls: str) -> str:
    rows = []

    max_rows = 5
    y0 = 170
    gap = 42

    for idx, pub in enumerate(publications[:max_rows]):
        y = y0 + idx * gap
        title = escape(pub.get("title", "Untitled"))
        year = escape(str(pub.get("year", "")))
        citations = escape(str(pub.get("citations", 0)))
        fade = f"fadeIn{min(idx + 2, 7)}"

        # Keep title visually short inside SVG.
        short_title = title
        if len(short_title) > 78:
            short_title = short_title[:75] + "..."

        rows.append(
            f"""
    <g {cls}="{fade}">
      <circle cx="105" cy="{y - 6}" r="4.2"
              fill="{theme.primary}"
              filter="url(#{theme.glow_id})"/>

      <line x1="118" y1="{y - 6}" x2="150" y2="{y - 6}"
            stroke="{theme.accent}"
            stroke-width="1.7"
            stroke-linecap="round"
            filter="url(#{theme.glow_id})"/>

      <text x="170" y="{y}"
            font-family="JetBrains Mono, Consolas, monospace"
            font-size="14.5"
            font-weight="700"
            fill="{theme.text_main}">
        {short_title}
      </text>

      <text x="940" y="{y}"
            font-family="JetBrains Mono, Consolas, monospace"
            font-size="14"
            font-weight="800"
            fill="{theme.accent}">
        {year}
      </text>

      <text x="1045" y="{y}"
            font-family="JetBrains Mono, Consolas, monospace"
            font-size="14"
            font-weight="800"
            fill="{theme.primary}"
            filter="url(#{theme.glow_id})">
        {citations}
      </text>
    </g>
"""
        )

    if not rows:
        rows.append(
            f"""
    <text x="600" y="210" text-anchor="middle"
          font-family="JetBrains Mono, Consolas, monospace"
          font-size="16"
          font-weight="700"
          fill="{theme.text_muted}">
      Scholar data has not been fetched yet.
    </text>
"""
        )

    return "\n".join(rows)


def make_citation_bars(cites_per_year: dict, theme, cls: str) -> str:
    if not cites_per_year:
        return ""

    items = [(str(y), int(c)) for y, c in cites_per_year.items()]
    items = items[-10:]

    max_cites = max([c for _, c in items] + [1])

    chart_x = 120
    chart_y = 420
    chart_w = 960
    chart_h = 120

    bar_gap = 10
    bar_w = (chart_w - bar_gap * (len(items) - 1)) / max(len(items), 1)

    bars = [
        f"""
  <line x1="{chart_x}" y1="{chart_y}" x2="{chart_x + chart_w}" y2="{chart_y}"
        stroke="{theme.secondary}"
        stroke-opacity="0.35"
        stroke-width="1"/>
  <text x="{chart_x + chart_w / 2}" y="{chart_y - chart_h - 170}"
        text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="14"
        font-weight="900"
        letter-spacing="2.5"
        fill="{theme.primary}"
        filter="url(#{theme.glow_id})">
    CITATIONS PER YEAR
  </text>
"""
    ]

    for idx, (year, count) in enumerate(items):
        x = chart_x + idx * (bar_w + bar_gap)
        h = (count / max_cites) * chart_h
        y = chart_y - h

        bars.append(
            f"""
  <g {cls}="fadeIn{min(idx + 2, 7)}">
    <rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" rx="5" text-anchor="middle"
          fill="{theme.primary}"
          fill-opacity="0.65"
          stroke="{theme.accent}"
          stroke-width="1"
          filter="url(#{theme.soft_glow_id})"/>

    <text x="{x + bar_w / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle"
          font-family="JetBrains Mono, Consolas, monospace"
          font-size="11"
          font-weight="800"
          fill="{theme.text_main}">
      {count}
    </text>

    <text x="{x + bar_w / 2:.1f}" y="{chart_y + 22}" text-anchor="middle"
          font-family="JetBrains Mono, Consolas, monospace"
          font-size="11"
          font-weight="800"
          fill="{theme.text_muted}">
      {year}
    </text>
  </g>
"""
        )

    return "\n".join(bars)


def make_publication_panel() -> None:
    width = 1200
    height = 590

    theme = get_theme("blue")
    cls = "class"

    data = load_data()

    publications = data.get("publications", [])
    cites_per_year = data.get("cites_per_year", {})
    total_citations = data.get("total_citations", 0)
    h_index = data.get("h_index", 0)
    i10_index = data.get("i10_index", 0)
    updated_at = escape(str(data.get("updated_at", "unknown")))

    rows_svg = make_publication_rows(publications, theme, cls)
    chart_svg = make_citation_bars(cites_per_year, theme, cls)

    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  {make_defs(theme, width, height)}

  {make_common_style()}

  <rect x="0" y="0" width="{width}" height="{height}"
        fill="{theme.bg_deep}"
        fill-opacity="0"/>

  <text {cls}="fadeIn1 panelPulse" x="600" y="58" text-anchor="middle"
        font-family="Orbitron, Audiowide, Rajdhani, Arial Black, sans-serif"
        font-size="20"
        font-weight="900"
        letter-spacing="5"
        fill="url(#{theme.title_grad_id})"
        filter="url(#{theme.glow_id})">
    GOOGLE SCHOLAR · PUBLICATIONS · CITATION TRAJECTORY
  </text>



  <rect x="70" y="112" width="1060" height="340" rx="20"
        fill="{theme.bg_inner}"
        fill-opacity="0.68"
        stroke="{theme.primary}"
        stroke-width="1.8"
        stroke-opacity="0.9"
        filter="url(#{theme.soft_glow_id})"/>





  <text x="90" y="182"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="13"
        font-weight="800"
        fill="{theme.text_muted}">
    total citations: {total_citations} · h-index: {h_index} · i10-index: {i10_index}
  </text>

  <text x="90" y="205"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="11"
        font-weight="700"
        fill="{theme.text_muted}">
    updated: {updated_at}
  </text>

  {chart_svg}
</svg>"""

    out = OUT / "panel-research-publications.svg"
    write(out, svg)
    validate_svg(out)


if __name__ == "__main__":
    make_publication_panel()
