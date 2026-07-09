from pathlib import Path
import xml.etree.ElementTree as ET

from ares_background import make_ares_background
from ares_tron_theme import (
    get_theme,
    make_defs,
    make_common_style,
    make_glass_panel,
    make_corner_geometry,
)


OUT = Path("assets")
OUT.mkdir(exist_ok=True)


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def validate_svg(path: Path) -> None:
    ET.parse(path)
    print(f"OK  {path}")


def make_system_status_panel() -> None:
    width = 1200
    height = 530

    theme = get_theme("red")
    cls = "class"

    # shift the whole panel block
    panel_dx = 0
    panel_dy = -34

    bg = make_ares_background(
        width=width,
        height=height,
        theme=theme.name,
        prefix="systemStatusPanel",
        wheel_opacity=0.18,
        dense=True,
    )

    rows = [
        ("STATUS", "building"),
        ("PROJECT", "TraceFlow"),
        ("MODE", "research infrastructure"),
        ("CORE", "reproducibility · automation · evaluation"),
        ("LOCATION", "Taiwan"),
        ("NEXT TARGET", "paper-ready experimental system"),
    ]

    row_y_start = 135
    row_gap = 34

    row_svg = []

    for i, (label, value) in enumerate(rows, start=2):
        y = row_y_start + (i - 2) * row_gap
        fade_class = f"fadeIn{i}" if i <= 7 else "fadeIn7"

        row_svg.append(
            f'''
  <text {cls}="{fade_class}" x="170" y="{y}"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="18" font-weight="800"
        fill="{theme.primary}">
    {label}
  </text>

  <text {cls}="{fade_class}" x="360" y="{y}"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="18" font-weight="800"
        fill="{theme.accent}">
    :
  </text>

  <text {cls}="{fade_class}" x="390" y="{y}"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="18" font-weight="500"
        fill="{theme.text_main}">
    {value}
  </text>
'''
        )

    row_block = "\n".join(row_svg)

    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  {bg}

  {make_defs(theme, width, height)}

  {make_common_style()}

  <style>
    .scanBar {{
      animation: scanBar 4.2s linear infinite;
    }}

    @keyframes scanBar {{
      0%   {{ transform: translateY(0px); opacity: 0.10; }}
      50%  {{ transform: translateY(205px); opacity: 0.28; }}
      100% {{ transform: translateY(0px); opacity: 0.10; }}
    }}
  </style>

  <g transform="translate({panel_dx},{panel_dy})">
    {make_glass_panel(theme)}

    {make_corner_geometry(theme)}

    <!-- scan bar -->
    <rect {cls}="scanBar" x="100" y="154" width="1000" height="18"
          fill="{theme.primary}" opacity="0.08"/>

    <!-- status rows -->
    {row_block}

    <!-- footer signal -->
    <text {cls}="softFloat" x="600" y="400" text-anchor="middle"
          font-family="JetBrains Mono, Consolas, monospace"
          font-size="20" font-weight="800" letter-spacing="3"
          fill="{theme.text_muted}">
      BUILD PIPELINES · EVALUATION · REPRODUCIBILITY · REPORTING
    </text>
  </g>
</svg>"""

    out = OUT / "panel-system-status.svg"
    write(out, svg)
    validate_svg(out)


if __name__ == "__main__":
    make_system_status_panel()
