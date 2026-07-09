from pathlib import Path
from xml.sax.saxutils import escape
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


def badge_svg(x: int, y: int, label: str, theme, cls: str) -> str:
    width = max(92, 18 + len(label) * 8)

    return f"""
      <g {cls}="chipFade">
        <rect x="{x}" y="{y}" width="{width}" height="28" rx="7"
              fill="#0D1117"
              stroke="{theme.primary}"
              stroke-width="1.1"
              stroke-opacity="0.85"
              filter="url(#{theme.glow_id})"/>

        <text x="{x + width / 2}" y="{y + 19}" text-anchor="middle"
              font-family="JetBrains Mono, Consolas, monospace"
              font-size="12"
              font-weight="900"
              fill="#FF3131">
          {escape(label)}
        </text>
      </g>
"""


def project_card(
    x: int,
    y: int,
    width: int,
    height: int,
    title: str,
    subtitle: str,
    description: str,
    bullets: list[str],
    badges: list[str],
    theme,
    cls: str,
    fade_class: str,
) -> str:
    bullet_y_start = y + 140
    bullet_gap = 31

    bullet_parts = []

    for idx, bullet in enumerate(bullets):
        by = bullet_y_start + idx * bullet_gap
        bullet_class = f"fadeIn{min(idx + 2, 7)}"

        bullet_parts.append(
            f"""
      <g {cls}="{bullet_class}">
        <circle cx="{x + 42}" cy="{by - 5}" r="4.2"
                fill="{theme.primary}"
                filter="url(#{theme.glow_id})"/>

        <line x1="{x + 53}" y1="{by - 5}" x2="{x + 82}" y2="{by - 5}"
              stroke="{theme.accent}"
              stroke-width="1.7"
              stroke-linecap="round"
              filter="url(#{theme.glow_id})"/>

        <text x="{x + 96}" y="{by}"
              font-family="JetBrains Mono, Consolas, monospace"
              font-size="14.5"
              font-weight="600"
              fill="{theme.text_main}">
          {escape(bullet)}
        </text>
      </g>
"""
        )

    badge_x = x + 38
    badge_y = y + height - 58
    badge_gap = 108

    badge_parts = []
    cursor_x = badge_x

    for badge in badges:
        badge_parts.append(badge_svg(cursor_x, badge_y, badge, theme, cls))
        cursor_x += badge_gap

    return f"""
    <g {cls}="{fade_class}">
      <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="20"
            fill="{theme.bg_inner}"
            fill-opacity="0.72"
            stroke="{theme.primary}"
            stroke-width="1.9"
            stroke-opacity="0.90"
            filter="url(#{theme.soft_glow_id})"/>

      <rect x="{x + 16}" y="{y + 16}" width="{width - 32}" height="{height - 32}" rx="14"
            fill="{theme.bg_panel}"
            fill-opacity="0.62"
            stroke="{theme.secondary}"
            stroke-width="1"
            stroke-opacity="0.45"/>

      <text x="{x + width / 2}" y="{y + 48}" text-anchor="middle"
            font-family="Orbitron, Audiowide, Rajdhani, Arial Black, sans-serif"
            font-size="25"
            font-weight="900"
            letter-spacing="3.2"
            fill="{theme.primary}"
            filter="url(#{theme.glow_id})">
        {escape(title)}
      </text>

      <text x="{x + width / 2}" y="{y + 78}" text-anchor="middle"
            font-family="JetBrains Mono, Consolas, monospace"
            font-size="13"
            font-weight="900"
            letter-spacing="1.2"
            fill="{theme.accent}">
        {escape(subtitle)}
      </text>

      <text x="{x + 38}" y="{y + 112}"
            font-family="JetBrains Mono, Consolas, monospace"
            font-size="14.5"
            font-weight="600"
            fill="{theme.text_soft}">
        {escape(description)}
      </text>

      <path {cls}="lineFlow"
            d="M{x + 38} {y + 94} H{x + width - 38}"
            stroke="{theme.accent}"
            stroke-width="2"
            stroke-opacity="0.75"
            filter="url(#{theme.glow_id})"/>

      {"".join(bullet_parts)}

      {"".join(badge_parts)}
    </g>
"""


def make_featured_projects_panel() -> None:
    width = 1200
    height = 560

    theme = get_theme("blue")
    cls = "class"

    left_x = 38
    right_x = 605
    card_y = 112
    card_w = 570
    card_h = 390

    traceflow = project_card(
        x=left_x,
        y=card_y,
        width=card_w,
        height=card_h,
        title="TraceFlow",
        subtitle="Research Infrastructure · Deep Learning · Side-Channel Analysis",
        description="Extensible framework for reproducible DLSCA experiments.",
        bullets=[
            "Automated experiment orchestration",
            "Dataset-aware training and evaluation",
            "Guessing entropy, rank metrics, and attack evaluation",
            "Model comparison and reproducibility-first design",
            "Built for paper development and systematic experiments",
        ],
        badges=["Python", "PyTorch", "MLOps"],
        theme=theme,
        cls=cls,
        fade_class="lineFlow",
    )

    qsurfnet = project_card(
        x=right_x,
        y=card_y,
        width=card_w,
        height=card_h,
        title="QSurfNet",
        subtitle="Master's Thesis · Quantum Machine Learning",
        description="Research project from my Master's thesis at Tamkang University.",
        bullets=[
            "Research design and implementation",
            "Experimental evaluation",
            "Academic writing and publication pipeline",
            "First-author research experience",
        ],
        badges=["Python", "Research", "quple", "TensorFlow"],
        theme=theme,
        cls=cls,
        fade_class="lineFlow",
    )

    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  {make_defs(theme, width, height)}

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

  <rect x="0" y="0" width="{width}" height="{height}"
        fill="{theme.bg_deep}"
        fill-opacity="0"/>

  <text {cls}="fadeIn1 panelPulse" x="600" y="58" text-anchor="middle"
        font-family="Orbitron, Audiowide, Rajdhani, Arial Black, sans-serif"
        font-size="31"
        font-weight="900"
        letter-spacing="5"
        fill="url(#{theme.title_grad_id})"
        filter="url(#{theme.glow_id})">
    R&amp;D CONTRIBUTIONS
  </text>

  <text {cls}="fadeIn2" x="600" y="86" text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="13"
        font-weight="800"
        letter-spacing="3"
        fill="{theme.text_muted}">
    QUANTUM MACHINE LEARNING · SIDE CHANNEL ANALYSIS · COMPUTER VISION
  </text>

  {traceflow}

  {qsurfnet}

  <text {cls}="softFloat" x="600" y="535" text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="20"
        font-weight="900"
        letter-spacing="3"
        fill="{theme.accent}"
        stroke="{theme.dark_core}"
        stroke-width="0.7"
        filter="url(#{theme.soft_glow_id})">
    R&amp;D CONTRIBUTIONS · RESEARCH CODE · EXPERIMENT DESIGN · PAPER-READY SYSTEMS
  </text>
</svg>"""

    out = OUT / "panel-featured-projects.svg"
    write(out, svg)
    validate_svg(out)


if __name__ == "__main__":
    make_featured_projects_panel()
