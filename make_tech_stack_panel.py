from pathlib import Path
import xml.etree.ElementTree as ET

from ares_tron_theme import (
    get_theme,
    make_defs,
    make_common_style,
)


OUT = Path("assets")
OUT.mkdir(exist_ok=True)


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def validate_svg(path: Path) -> None:
    ET.parse(path)
    print(f"OK  {path}")


def make_tech_stack_panel() -> None:
    width = 1200
    height = 450

    theme = get_theme("blue")
    cls = "class"

    sections = [
        {
            "title": "Languages",
            "items": ["Python", "C++", "Bash", "LaTeX"],
        },
        {
            "title": "Machine Learning",
            "items": ["Data Science", "Artifact Management", "MLOPs", "Visualization"],
        },
        {
            "title": "Infrastructure",
            "items": ["Docker", "Linux", "CI/CD", "Git"],
        },
    ]

    cols = 3
    card_w = 320
    card_h = 238
    gap_x = 44
    start_x = 86
    start_y = 100

    section_svg = []

    for idx, section in enumerate(sections):
        row = idx // cols
        col = idx % cols

        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + 46)

        title_y = y + 42
        #small boxes which contain the  title (items)
        chips_svg = []
        chip_x = x + 34
        chip_y = y + 62
        chip_w = card_w - 68
        chip_h = 32
        chip_gap = 40

        for item_idx, item in enumerate(section["items"]):
            iy = chip_y + item_idx * chip_gap
            delay = 0.2 + (idx * 0.2) + (item_idx * 0.08)

            chips_svg.append(
                f'''
        <g {cls}="chipFade" style="animation-delay: {delay:.2f}s">
            <rect x="{chip_x}" y="{iy}" width="{chip_w}" height="{chip_h}" rx="8"
                fill="#0D1117"
                stroke="{theme.primary}"
                stroke-width="1.2"
                stroke-opacity="0.80"
                filter="url(#{theme.glow_id})"/>

            <text x="{chip_x + chip_w / 2}" y="{iy + 21}" text-anchor="middle"
                font-family="JetBrains Mono, Consolas, monospace"
                font-size="14"
                font-weight="800"
                fill="#FF3131">
            {item}
            </text>
        </g>
'''
            )

        chips_block = "\n".join(chips_svg)

        section_svg.append(
            f'''
    <g {cls}="fadeIn{min(idx + 2, 7)}">
      <rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="18"
            fill="{theme.bg_inner}"
            fill-opacity="0.72"
            stroke="{theme.primary}"
            stroke-width="1.8"
            stroke-opacity="0.85"
            filter="url(#{theme.soft_glow_id})"/>

      <rect x="{x + 14}" y="{y + 14}" width="{card_w - 28}" height="{card_h - 28}" rx="12"
            fill="#020814"
            fill-opacity="0.62"
            stroke="{theme.secondary}"
            stroke-width="1"
            stroke-opacity="0.45"/>

      <text x="{x + card_w / 2}" y="{title_y}" text-anchor="middle"
            font-family="JetBrains Mono, Consolas, monospace"
            font-size="17"
            font-weight="900"
            letter-spacing="2.4"
            fill="{theme.primary}"
            filter="url(#{theme.glow_id})">
        {section["title"].upper()}
      </text>

      <path {cls}="lineFlow"
            d="M{x + 34} {y + 58} H{x + card_w - 34}"
            stroke="{theme.accent}"
            stroke-width="2"
            stroke-opacity="0.75"
            filter="url(#{theme.glow_id})"/>

      {chips_block}
    </g>
'''
        )

    sections_block = "\n".join(section_svg)

    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
{make_defs(theme, width, height).replace("<defs>", "").replace("</defs>", "")}
  </defs>

  {make_common_style()}

  <style>
    .chipFade {{
      opacity: 0;
      animation: chipFade 0.8s ease-out forwards;
    }}

    @keyframes chipFade {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>

  <rect x="0" y="0" width="{width}" height="{height}" rx="0"
        fill="#020814"
        fill-opacity="0.0"/>


  <text {cls}="fadeIn2" x="600" y="36" text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="26"
        font-weight="800"
        letter-spacing="3"
        fill="{theme.secondary}"
        filter="url(#{theme.glow_id})">
    EXPERIENCE · EXPERTISE · CREATIVITY
  </text>

  {sections_block}

  <text {cls}="softFloat" x="600" y="392" text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="20"
        font-weight="900"
        letter-spacing="3"
        fill="{theme.accent}"
        stroke="{theme.dark_core}"
        stroke-width="0.7"
        filter="url(#{theme.soft_glow_id})">
    BUILDING REPRODUCIBLE RESEARCH SYSTEMS WITH MAINTAINABLE ENGINEERING
  </text>
</svg>"""

    out = OUT / "panel-tech-stack.svg"
    write(out, svg)
    validate_svg(out)


if __name__ == "__main__":
    make_tech_stack_panel()
