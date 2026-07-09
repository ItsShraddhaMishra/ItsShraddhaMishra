
from pathlib import Path
import xml.etree.ElementTree as ET

from ares_background import make_ares_background
from make_readme_assets import text_to_paths

OUT = Path("assets")
OUT.mkdir(exist_ok=True)

TRON_FONT = Path(
    "/mnt/c/Users/ruben/Documents/Personal/GitHub/"
    "ItsShraddhaMishra.github.io/fonts/tron_ares/TronAres.woff"
)

def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def validate_svg(path: Path) -> None:
    ET.parse(path)
    print(f"OK  {path}")


def make_identity_panel() -> None:
    width = 1200
    height = 520

    bg = make_ares_background(
        width=width,
        height=height,
        theme="purple",
        prefix="identityPanel",
        wheel_opacity=0.18,
        dense=True,
    )
    principles_paths = text_to_paths(
        text="MODULARITY · ENCAPSULATION · ORCHESTRATION",
        x=600,
        y=500,
        size=25,
        fill="#c77dff",
        letter_spacing=3,
        #filter_id="softVioletGlow",
    )

    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  {bg}

  <defs>
    <filter id="violetGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softVioletGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="panelBorder" x1="0" y1="0" x2="{width}" y2="{height}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#d86cff"/>
      <stop offset="0.45" stop-color="#b026ff"/>
      <stop offset="1" stop-color="#4f1266"/>
    </linearGradient>

    <linearGradient id="titleGrad" x1="250" y1="0" x2="950" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="0.35" stop-color="#d86cff"/>
      <stop offset="0.72" stop-color="#b026ff"/>
      <stop offset="1" stop-color="#ffffff"/>
    </linearGradient>
  </defs>

  <style>
    .panelPulse {{
      animation: panelPulse 3.8s ease-in-out infinite alternate;
    }}

    .lineFlow {{
      stroke-dasharray: 24 18;
      animation: lineFlow 4.8s linear infinite;
    }}

    .softFloat {{
      animation: softFloat 6.8s ease-in-out infinite alternate;
    }}

    .fadeIn1 {{
      animation: fadeIn 1.2s ease-out both;
    }}

    .fadeIn2 {{
      animation: fadeIn 1.2s ease-out 0.35s both;
    }}

    .fadeIn3 {{
      animation: fadeIn 1.2s ease-out 0.7s both;
    }}

    .fadeIn4 {{
      animation: fadeIn 1.2s ease-out 1.05s both;
    }}

    @keyframes panelPulse {{
      0%   {{ opacity: 0.72; }}
      100% {{ opacity: 1; }}
    }}

    @keyframes lineFlow {{
      to {{ stroke-dashoffset: -180; }}
    }}

    @keyframes softFloat {{
      0%   {{ transform: translateY(-4px); opacity: 0.72; }}
      100% {{ transform: translateY(4px); opacity: 1; }}
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(10px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>

  <!-- glass panel -->
  <rect x="58" y="54" width="1084" height="412" rx="22"
        fill="#050008" fill-opacity="0.76"
        stroke="url(#panelBorder)" stroke-width="2.5"
        filter="url(#softVioletGlow)"/>

  <rect x="78" y="76" width="1044" height="368" rx="16"
        fill="#14001f" fill-opacity="0.38"
        stroke="#4f1266" stroke-width="1"
        stroke-opacity="0.85"/>

  <!-- corner geometry -->
  <path class="lineFlow" d="M92 112 H245" stroke="#d86cff" stroke-width="2.5" filter="url(#violetGlow)"/>
  <path class="lineFlow" d="M955 112 H1108" stroke="#b026ff" stroke-width="2.5" filter="url(#violetGlow)"/>
  <path class="lineFlow" d="M92 408 H245" stroke="#b026ff" stroke-width="2.5" filter="url(#violetGlow)"/>
  <path class="lineFlow" d="M955 408 H1108" stroke="#d86cff" stroke-width="2.5" filter="url(#violetGlow)"/>

  <!-- title -->
  <text class="fadeIn1" x="600" y="124" text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="20" font-weight="800" letter-spacing="5"
        fill="#b8b8b8">
    PERMANENCE CODE
  </text>

  <text class="fadeIn1 panelPulse" x="600" y="166" text-anchor="middle"
        font-family="Orbitron, Audiowide, Rajdhani, Arial Black, sans-serif"
        font-size="30" font-weight="900" letter-spacing="4"
        fill="url(#titleGrad)" filter="url(#violetGlow)">
    INTELLIGENT SYSTEMS SAVE COGNITIVE ENERGY
  </text>

  <!-- hook -->
  <text class="fadeIn2" x="600" y="222" text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="18" font-weight="500"
        fill="#ffffff">
    <tspan x="600" dy="0">My creative ideas become code for research that serve the real world —</tspan>
    <tspan x="600" dy="30">where an experiment stops being a temporary run and becomes part of a stable, traceable system.</tspan>
  </text>

  <!-- body -->
  <text class="fadeIn3" x="600" y="300" text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="17" font-weight="500"
        fill="#d8c7ff">
    <tspan x="600" dy="0">I build machine learning research systems in the spirit of </tspan>
    <tspan fill="#d86cff" font-weight="800">permanence code</tspan>
    <tspan>: stable, reproducible,</tspan>
    <tspan x="600" dy="30">auditable, and extensible by design. My work lives in the deep amethyst space between</tspan>
    <tspan x="600" dy="30">human intention and digital execution, where glowing lines of automation turn uncertainty into structure.</tspan>
  </text>

  <!-- Core Coding Principles -->
  <text class="fadeIn4" x="600" y="404" text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="17" font-weight="500"
        fill="#ffffff">
    <tspan x="600" dy="0">My work is grounded in synthesis: </tspan>
    <tspan fill="#d86cff" font-weight="900">intentional purpose</tspan>
    <tspan>, programming stability with human empathy, structure with</tspan>
    <tspan x="600" dy="30">intuition, and precision with reflection for the </tspan>
    <tspan fill="#b026ff" font-weight="900">Users</tspan>
    <tspan>.</tspan>
  </text>

  
  <!-- atmosphere labels -->
  <g class="softFloat" opacity="0">
    <g transform="translate(0,10)" stroke="#050008" stroke-width="1.8">
      {principles_paths}
    </g>
  </g>
</svg>"""


    out = OUT / "panel-identity.svg"
    write(out, svg)
    validate_svg(out)


if __name__ == "__main__":
    make_identity_panel()
