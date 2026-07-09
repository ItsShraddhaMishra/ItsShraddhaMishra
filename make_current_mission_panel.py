from pathlib import Path
from xml.sax.saxutils import escape
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


def make_current_mission_panel() -> None:
    width = 1200
    height = 500

    theme = get_theme("red")
    cls = "class"

    panel_dx = 0
    panel_dy = -18

    bg = make_ares_background(
        width=width,
        height=height,
        theme=theme.name,
        prefix="currentMissionPanel",
        wheel_opacity=0.18,
        dense=True,
    )

    missions = [
        "Building TraceFlow — an extensible framework for reproducible deep learning side-channel analysis.",
        "Designing experiment pipelines for model training, evaluation, ranking, and reporting.",
        "Refactoring research code into maintainable infrastructure.",
        "Writing research around reproducibility, automation, and deep learning for SCA.",
        "Preparing for long-term work in AI systems, autonomous decision-making, and research engineering.",
    ]

    row_y_start = 118
    row_gap = 48

    mission_svg = []

    for i, line in enumerate(missions, start=2):
        y = row_y_start + (i - 2) * row_gap
        fade_class = f"fadeIn{i}" if i <= 7 else "fadeIn7"

        bullet_cx = 165
        bullet_cy = y - 6
        beam_x1 = 180
        beam_x2 = 235
        text_x = 200

        begin_pulse = f"{0.25 * (i - 2):.2f}s"
        begin_beam = f"{0.22 * (i - 2):.2f}s"

        mission_svg.append(
            f'''
    <g {cls}="{fade_class}">
      <!-- red laser bullet -->
      <circle cx="{bullet_cx}" cy="{bullet_cy}" r="5.5"
              fill="{theme.primary}"
              filter="url(#{theme.glow_id})"
              opacity="0.95"/>

      <circle cx="{bullet_cx}" cy="{bullet_cy}" r="11"
              fill="none"
              stroke="{theme.primary}"
              stroke-width="1.2"
              filter="url(#{theme.soft_glow_id})"
              opacity="0.55">
        <animate attributeName="r"
                 values="8;11;8"
                 dur="2.2s"
                 begin="{begin_pulse}"
                 repeatCount="indefinite"/>
        <animate attributeName="opacity"
                 values="0.25;0.6;0.25"
                 dur="2.2s"
                 begin="{begin_pulse}"
                 repeatCount="indefinite"/>
      </circle>

      <!-- laser beam -->
      <line x1="{beam_x1}" y1="{bullet_cy}" x2="{beam_x2}" y2="{bullet_cy}"
            stroke="{theme.primary}"
            stroke-width="2.4"
            stroke-linecap="round"
            filter="url(#{theme.glow_id})"
            opacity="0.95">
        <animate attributeName="x2"
                 values="{beam_x1};{beam_x2}"
                 dur="0.45s"
                 begin="{begin_beam}"
                 fill="freeze"/>
        <animate attributeName="opacity"
                 values="0.35;1;0.92"
                 dur="0.45s"
                 begin="{begin_beam}"
                 fill="freeze"/>
      </line>


      <!-- bullet text -->
      <text x="{text_x}" y="{y}"
            font-family="JetBrains Mono, Consolas, monospace"
            font-size="16.5"
            font-weight="600"
            fill="{theme.text_main}">
        {escape(line)}
      </text>
    </g>
'''
        )

    mission_block = "\n".join(mission_svg)

    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  {bg}

  {make_defs(theme, width, height)}

  {make_common_style()}

  <style>
    .missionScan {{
      animation: missionScan 5.2s linear infinite;
    }}

    .missionPulse {{
      animation: missionPulse 3.2s ease-in-out infinite alternate;
    }}

    @keyframes missionScan {{
      0%   {{ transform: translateY(0px); opacity: 0.07; }}
      50%  {{ transform: translateY(245px); opacity: 0.24; }}
      100% {{ transform: translateY(0px); opacity: 0.07; }}
    }}

    @keyframes missionPulse {{
      0%   {{ opacity: 0.72; }}
      100% {{ opacity: 1; }}
    }}
  </style>

  <g transform="translate({panel_dx},{panel_dy})">
    {make_glass_panel(theme)}

    {make_corner_geometry(theme)}


    <!-- scan bar -->
    <rect {cls}="missionScan" x="100" y="130" width="1000" height="18"
          fill="{theme.primary}"
          opacity="0.08"/>

    <!-- mission lines -->
    {mission_block}

    <!-- footer signal -->
    <text {cls}="softFloat" x="600" y="470" text-anchor="middle"
          font-family="JetBrains Mono, Consolas, monospace"
          font-size="20"
          font-weight="900"
          letter-spacing="3.2"
          fill="{theme.bg_deep}"
          stroke="{theme.dark_core}"
          stroke-width="1.5"
          filter="url(#{theme.soft_glow_id})">
      BUILD · EVALUATE · RANK · REPORT · WRITE PAPER
    </text>
  </g>
</svg>"""

    out = OUT / "panel-current-mission.svg"
    write(out, svg)
    validate_svg(out)


if __name__ == "__main__":
    make_current_mission_panel()
