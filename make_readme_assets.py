#ItsShraddhaMishra\make_readme_assets.py


from pathlib import Path
from xml.sax.saxutils import escape

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

from ares_background import make_ares_background


ROOT = Path(".")
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

TRON_FONT = Path(
    "/mnt/c/Users/ruben/Documents/Personal/GitHub/"
    "ItsShraddhaMishra.github.io/fonts/tron_ares/TronAres.woff"
)


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def font_available() -> bool:
    return TRON_FONT.exists()


def validate_svgs() -> bool:
    import xml.etree.ElementTree as ET

    ok = True

    for svg in sorted(OUT.glob("*.svg")):
        try:
            ET.parse(svg)
            print(f"OK  {svg}")
        except Exception as e:
            print(f"BAD {svg}: {e}")
            ok = False

    return ok


def text_to_paths(
    text: str,
    x: float,
    y: float,
    size: float,
    fill: str,
    letter_spacing: float = 4.0,
    filter_id: str = "redGlow",
) -> str:
    if not font_available():
        return (
            f'<text x="{x}" y="{y}" text-anchor="middle" '
            f'font-family="Orbitron, Audiowide, Rajdhani, Arial Black, sans-serif" '
            f'font-size="{size}" font-weight="900" letter-spacing="{letter_spacing}" '
            f'fill="{fill}" filter="url(#{filter_id})">{escape(text)}</text>'
        )

    font = TTFont(str(TRON_FONT))
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    units_per_em = font["head"].unitsPerEm
    scale = size / units_per_em
    hmtx = font["hmtx"].metrics

    glyphs = []
    total_advance = 0.0

    for ch in text:
        if ch == " ":
            advance = hmtx.get("space", (units_per_em * 0.35, 0))[0] * scale
            glyphs.append((None, advance))
            total_advance += advance + letter_spacing
            continue

        glyph_name = cmap.get(ord(ch))
        if glyph_name is None:
            advance = units_per_em * 0.35 * scale
            glyphs.append((None, advance))
            total_advance += advance + letter_spacing
            continue

        advance = hmtx.get(glyph_name, (units_per_em * 0.6, 0))[0] * scale
        glyphs.append((glyph_name, advance))
        total_advance += advance + letter_spacing

    cursor = x - (total_advance / 2.0)
    parts = [f'<g fill="{fill}" filter="url(#{filter_id})">']

    for glyph_name, advance in glyphs:
        if glyph_name is None:
            cursor += advance + letter_spacing
            continue

        pen = SVGPathPen(glyph_set)
        transform = (scale, 0, 0, -scale, cursor, y)
        tpen = TransformPen(pen, transform)
        glyph_set[glyph_name].draw(tpen)
        d = pen.getCommands()

        if d:
            parts.append(f'<path d="{d}"/>')

        cursor += advance + letter_spacing

    parts.append("</g>")
    return "\n".join(parts)


def header() -> None:
    bg = make_ares_background(
        width=1200,
        height=310,
        theme="red",
        prefix="headerBg",
        wheel_opacity=0.24,
        dense=True,
    )

    name_paths = text_to_paths(
        text="SHRADDHA MISHRA",
        x=600,
        y=144,
        size=66,
        fill="url(#nameGrad)",
        letter_spacing=6,
        filter_id="redGlow",
    )

    svg = f"""<svg width="1200" height="310" viewBox="0 0 1200 310" fill="none" xmlns="http://www.w3.org/2000/svg">
  {bg}

  <defs>
    <linearGradient id="nameGrad" x1="270" y1="0" x2="930" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="0.38" stop-color="#ff3131"/>
      <stop offset="0.72" stop-color="#ff1e1e"/>
      <stop offset="1" stop-color="#ff7a00"/>
    </linearGradient>

    <filter id="redGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <g opacity="0.95">
    {name_paths}
  </g>

  <text x="600" y="188" text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="20" font-weight="700" letter-spacing="2"
        fill="#ffffff">
    DESIGNING ML SYSTEMS · REPRODUCIBLE AI RESEARCH · AUTOMATION · INTELLIGENT CI/CD
  </text>

  <text x="600" y="218" text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="14" letter-spacing="5"
        fill="#b8b8b8">
    SYSTEM DESIGN | RESEARCH INFRASTRUCTURE | SYSTEMS UNDER UNCERTAINTY
  </text>
</svg>"""

    write(OUT / "header.svg", svg)


def section(filename: str, title: str, purple: bool = False) -> None:
    theme = "purple" if purple else "red"
    stroke = "#b026ff" if purple else "#ff7a00"
    text_fill = "#d86cff" if purple else "#ff1e1e"
    bg1 = "#120018" if purple else "#1a0400"
    bg2 = "#2b003d" if purple else "#361000"

    bg = make_ares_background(
        width=1200,
        height=76,
        theme=theme,
        prefix=filename.replace(".", "_"),
        wheel_opacity=0.15,
        dense=False,
    )

    title_paths = text_to_paths(
        text=title.upper(),
        x=600,
        y=48,
        size=30,
        fill=text_fill,
        letter_spacing=4,
        filter_id="redGlow",
    )

    svg = f"""<svg width="1200" height="76" viewBox="0 0 1200 76" fill="none" xmlns="http://www.w3.org/2000/svg">
  {bg}

  <defs>
    <linearGradient id="bar" x1="0" y1="0" x2="1200" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{bg1}" stop-opacity="0.86"/>
      <stop offset="0.5" stop-color="{bg2}" stop-opacity="0.72"/>
      <stop offset="1" stop-color="{bg1}" stop-opacity="0.86"/>
    </linearGradient>

    <filter id="redGlow" x="-20%" y="-80%" width="140%" height="260%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-20%" y="-80%" width="140%" height="260%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <style>
    .edge {{
      stroke-dasharray: 14 12;
      animation: dashMove 3.8s linear infinite;
    }}

    .pulse {{
      animation: pulseGlow 2.8s ease-in-out infinite alternate;
    }}

    @keyframes dashMove {{
      to {{ stroke-dashoffset: -120; }}
    }}

    @keyframes pulseGlow {{
      0% {{ opacity: 0.68; }}
      100% {{ opacity: 1; }}
    }}
  </style>

  <rect x="8" y="8" width="1184" height="60" rx="8" fill="url(#bar)" stroke="{stroke}" stroke-width="2"/>
  <rect x="8" y="8" width="1184" height="60" rx="8" fill="none" stroke="{stroke}" stroke-opacity="0.28" stroke-width="1"/>

  <path class="edge" d="M28 38H126" stroke="{stroke}" stroke-width="3" filter="url(#softGlow)"/>
  <path class="edge" d="M1074 38H1172" stroke="{stroke}" stroke-width="3" filter="url(#softGlow)"/>

  <g class="pulse">
    {title_paths}
  </g>
</svg>"""

    write(OUT / filename, svg)


header()

section("section-identity.svg", "Identity Grid", purple=True)
section("section-system-status.svg", "System Status")
section("section-current-mission.svg", "Current Mission")
section("section-tech-stack.svg", "Tech Stack")
section("section-featured-projects.svg", "Featured Projects")
section("section-expertise.svg", "Expertise")
section("section-research-direction.svg", "Research Direction")
section("section-research-publications.svg", "Research Publications")
section("section-github-signal.svg", "Git Signal")
section("section-contact.svg", "Contact")

print("\nValidating generated SVG files...")
svg_ok = validate_svgs()

if not svg_ok:
    raise SystemExit("SVG validation failed. Fix the BAD files above before previewing or committing.")

if font_available():
    print(f"\nGenerated animated README assets using Tron font: {TRON_FONT}")
else:
    print("\nGenerated animated README assets with fallback font. TronAres.woff was not found.")
