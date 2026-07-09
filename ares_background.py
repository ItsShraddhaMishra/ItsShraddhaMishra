#ItsShraddhaMishra\ares_background.py


from typing import Tuple


def _theme(theme: str) -> Tuple[str, str, str, str, str, str]:
    """
    Returns:
    bg_start, bg_mid, bg_end, primary, secondary, grid
    """
    if theme == "purple":
        return (
            "#050008",  # bg_start
            "#14001f",  # bg_mid
            "#2b003d",  # bg_end
            "#d86cff",  # primary
            "#b026ff",  # secondary
            "#4f1266",  # grid
        )

    # default red/orange Ares theme
    return (
        "#020202",  # bg_start
        "#110000",  # bg_mid
        "#2d0000",  # bg_end
        "#ff3131",  # primary
        "#ff7a00",  # secondary
        "#5d0a0a",  # grid
    )


def make_ares_background(
    width: int,
    height: int,
    theme: str = "red",
    prefix: str = "ares",
    wheel_opacity: float = 0.22,
    dense: bool = True,
) -> str:
    """
    Returns SVG markup (defs + background layers) for a Tron:Ares-style animated background.
    Safe to insert directly inside an SVG string.
    """
    bg_start, bg_mid, bg_end, primary, secondary, grid = _theme(theme)

    cx = int(width * 0.78)
    cy = int(height * 0.42)
    r1 = int(min(width, height) * 0.18)
    r2 = int(min(width, height) * 0.27)
    r3 = int(min(width, height) * 0.36)

    left_cx = int(width * 0.18)
    left_cy = int(height * 0.70)
    left_r = int(min(width, height) * 0.14)

    grid_size = 38 if dense else 52

    return f"""
  <defs>
    <linearGradient id="{prefix}_bg" x1="0" y1="0" x2="{width}" y2="{height}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{bg_start}"/>
      <stop offset="0.45" stop-color="{bg_mid}"/>
      <stop offset="0.78" stop-color="{bg_end}"/>
      <stop offset="1" stop-color="{secondary}"/>
    </linearGradient>

    <radialGradient id="{prefix}_wheelGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{primary}" stop-opacity="0.18"/>
      <stop offset="0.55" stop-color="{primary}" stop-opacity="0.08"/>
      <stop offset="1" stop-color="{primary}" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="{prefix}_wheelGlow2" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{secondary}" stop-opacity="0.15"/>
      <stop offset="0.65" stop-color="{secondary}" stop-opacity="0.06"/>
      <stop offset="1" stop-color="{secondary}" stop-opacity="0"/>
    </radialGradient>

    <pattern id="{prefix}_grid" width="{grid_size}" height="{grid_size}" patternUnits="userSpaceOnUse">
      <path d="M {grid_size} 0 L 0 0 0 {grid_size}" fill="none" stroke="{grid}" stroke-width="1" opacity="0.45"/>
    </pattern>

    <linearGradient id="{prefix}_scanLine" x1="0" y1="0" x2="{width}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{primary}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{primary}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{primary}" stop-opacity="0"/>
    </linearGradient>

    <filter id="{prefix}_glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="{prefix}_softGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <style>
    .{prefix}_scan {{
      animation: {prefix}_scanMove 4.8s linear infinite;
    }}

    .{prefix}_pulse {{
      animation: {prefix}_pulse 2.8s ease-in-out infinite alternate;
    }}

    .{prefix}_pulseSlow {{
      animation: {prefix}_pulseSlow 5.2s ease-in-out infinite alternate;
    }}

    .{prefix}_spinCW {{
      transform-origin: {cx}px {cy}px;
      animation: {prefix}_spinCW 16s linear infinite;
    }}

    .{prefix}_spinCCW {{
      transform-origin: {cx}px {cy}px;
      animation: {prefix}_spinCCW 22s linear infinite;
    }}

    .{prefix}_spinLeft {{
      transform-origin: {left_cx}px {left_cy}px;
      animation: {prefix}_spinLeft 18s linear infinite;
    }}

    .{prefix}_dash {{
      stroke-dasharray: 14 12;
      animation: {prefix}_dashMove 4s linear infinite;
    }}

    .{prefix}_float {{
      animation: {prefix}_float 6s ease-in-out infinite alternate;
    }}

    @keyframes {prefix}_scanMove {{
      0%   {{ transform: translateY(-60px); opacity: 0; }}
      12%  {{ opacity: 0.9; }}
      50%  {{ opacity: 0.5; }}
      100% {{ transform: translateY({height + 80}px); opacity: 0; }}
    }}

    @keyframes {prefix}_pulse {{
      0%   {{ opacity: 0.45; }}
      100% {{ opacity: 1; }}
    }}

    @keyframes {prefix}_pulseSlow {{
      0%   {{ opacity: 0.18; }}
      100% {{ opacity: 0.52; }}
    }}

    @keyframes {prefix}_spinCW {{
      from {{ transform: rotate(0deg); }}
      to   {{ transform: rotate(360deg); }}
    }}

    @keyframes {prefix}_spinCCW {{
      from {{ transform: rotate(360deg); }}
      to   {{ transform: rotate(0deg); }}
    }}

    @keyframes {prefix}_spinLeft {{
      from {{ transform: rotate(0deg); }}
      to   {{ transform: rotate(-360deg); }}
    }}

    @keyframes {prefix}_dashMove {{
      to {{ stroke-dashoffset: -120; }}
    }}

    @keyframes {prefix}_float {{
      0%   {{ transform: translateX(-12px); opacity: 0.55; }}
      100% {{ transform: translateX(12px); opacity: 0.95; }}
    }}
  </style>

  <rect width="{width}" height="{height}" fill="url(#{prefix}_bg)"/>
  <rect width="{width}" height="{height}" fill="url(#{prefix}_grid)" opacity="0.72"/>

  <rect class="{prefix}_scan" x="0" y="0" width="{width}" height="22" fill="url(#{prefix}_scanLine)" opacity="0.75"/>

  <!-- ambient glow fields -->
  <circle class="{prefix}_pulseSlow" cx="{cx}" cy="{cy}" r="{r3}" fill="url(#{prefix}_wheelGlow)"/>
  <circle class="{prefix}_pulseSlow" cx="{left_cx}" cy="{left_cy}" r="{left_r}" fill="url(#{prefix}_wheelGlow2)"/>

  <!-- main wheel -->
  <g class="{prefix}_spinCW" opacity="{wheel_opacity}">
    <circle cx="{cx}" cy="{cy}" r="{r1}" fill="none" stroke="{primary}" stroke-width="2" filter="url(#{prefix}_glow)"/>
    <circle cx="{cx}" cy="{cy}" r="{r2}" fill="none" stroke="{secondary}" stroke-width="2" filter="url(#{prefix}_glow)"/>
    <circle cx="{cx}" cy="{cy}" r="{r3}" fill="none" stroke="{primary}" stroke-width="1.5" opacity="0.7" filter="url(#{prefix}_softGlow)"/>

    <line x1="{cx-r3}" y1="{cy}" x2="{cx+r3}" y2="{cy}" stroke="{primary}" stroke-width="1.5" opacity="0.6"/>
    <line x1="{cx}" y1="{cy-r3}" x2="{cx}" y2="{cy+r3}" stroke="{secondary}" stroke-width="1.5" opacity="0.6"/>
    <line x1="{cx-r2}" y1="{cy-r2}" x2="{cx+r2}" y2="{cy+r2}" stroke="{primary}" stroke-width="1.2" opacity="0.45"/>
    <line x1="{cx-r2}" y1="{cy+r2}" x2="{cx+r2}" y2="{cy-r2}" stroke="{secondary}" stroke-width="1.2" opacity="0.45"/>
  </g>

  <!-- counter-rotating wheel segments -->
  <g class="{prefix}_spinCCW" opacity="{wheel_opacity}">
    <path d="M {cx-r2} {cy} A {r2} {r2} 0 0 1 {cx} {cy-r2}" fill="none" stroke="{primary}" stroke-width="3" filter="url(#{prefix}_glow)"/>
    <path d="M {cx} {cy-r2} A {r2} {r2} 0 0 1 {cx+r2} {cy}" fill="none" stroke="{secondary}" stroke-width="3" filter="url(#{prefix}_glow)"/>
    <path d="M {cx+r2} {cy} A {r2} {r2} 0 0 1 {cx} {cy+r2}" fill="none" stroke="{primary}" stroke-width="3" filter="url(#{prefix}_glow)"/>
    <path d="M {cx} {cy+r2} A {r2} {r2} 0 0 1 {cx-r2} {cy}" fill="none" stroke="{secondary}" stroke-width="3" filter="url(#{prefix}_glow)"/>
  </g>

  <!-- secondary left wheel -->
  <g class="{prefix}_spinLeft" opacity="{wheel_opacity}">
    <circle cx="{left_cx}" cy="{left_cy}" r="{left_r}" fill="none" stroke="{secondary}" stroke-width="1.8" filter="url(#{prefix}_glow)"/>
    <circle cx="{left_cx}" cy="{left_cy}" r="{int(left_r*0.62)}" fill="none" stroke="{primary}" stroke-width="1.3" filter="url(#{prefix}_glow)"/>
    <line x1="{left_cx-left_r}" y1="{left_cy}" x2="{left_cx+left_r}" y2="{left_cy}" stroke="{secondary}" stroke-width="1"/>
    <line x1="{left_cx}" y1="{left_cy-left_r}" x2="{left_cx}" y2="{left_cy+left_r}" stroke="{primary}" stroke-width="1"/>
  </g>

  <!-- horizon / laser terrain -->
  <path class="{prefix}_pulse" d="M0 {int(height*0.80)} C {int(width*0.15)} {int(height*0.70)} {int(width*0.22)} {int(height*0.88)} {int(width*0.36)} {int(height*0.78)} C {int(width*0.55)} {int(height*0.65)} {int(width*0.67)} {int(height*0.86)} {int(width*0.82)} {int(height*0.76)} C {int(width*0.92)} {int(height*0.70)} {int(width*0.97)} {int(height*0.75)} {width} {int(height*0.68)} V {height} H 0 Z"
        fill="{primary}" opacity="0.10"/>

  <path class="{prefix}_dash" d="M0 {int(height*0.84)} C {int(width*0.18)} {int(height*0.72)} {int(width*0.26)} {int(height*0.92)} {int(width*0.40)} {int(height*0.81)} C {int(width*0.58)} {int(height*0.67)} {int(width*0.72)} {int(height*0.89)} {int(width*0.88)} {int(height*0.79)} C {int(width*0.95)} {int(height*0.74)} {int(width*0.98)} {int(height*0.72)} {width} {int(height*0.70)}"
        fill="none" stroke="{primary}" stroke-width="2.4" opacity="0.95" filter="url(#{prefix}_glow)"/>

  <line class="{prefix}_float" x1="{int(width*0.08)}" y1="{int(height*0.18)}" x2="{int(width*0.92)}" y2="{int(height*0.18)}" stroke="{primary}" stroke-width="1.8" opacity="0.65" filter="url(#{prefix}_glow)"/>
  <line class="{prefix}_float" x1="{int(width*0.16)}" y1="{int(height*0.72)}" x2="{int(width*0.84)}" y2="{int(height*0.72)}" stroke="{secondary}" stroke-width="1.6" opacity="0.55"/>
"""
