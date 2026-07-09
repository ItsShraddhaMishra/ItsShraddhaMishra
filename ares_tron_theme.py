#ItsShraddhaMishra\ares_tron_theme.py


from dataclasses import dataclass

@dataclass(frozen=True)
class TronTheme:
    name: str

    bg_deep: str
    bg_panel: str
    bg_inner: str

    primary: str
    secondary: str
    accent: str

    text_main: str
    text_soft: str
    text_muted: str
    dark_core: str

    glow_id: str
    soft_glow_id: str
    border_grad_id: str
    title_grad_id: str

    heat_0: str
    heat_1: str
    heat_2: str
    heat_3: str
    heat_4: str
    heat_5: str

THEMES = {
    "red": TronTheme(
        name="red",
        bg_deep="#050505",
        bg_panel="#050505",
        bg_inner="#1a0400",
        primary="#ff3131",
        secondary="#ff1e1e",
        accent="#ff7a00",
        text_main="#ffffff",
        text_soft="#dddddd",
        text_muted="#b8b8b8",
        dark_core="#050505",
        glow_id="redGlow",
        soft_glow_id="softRedGlow",
        border_grad_id="panelBorder",
        title_grad_id="titleGrad",

        # contribution heat spectrum: dark red -> hot orange
        heat_0="#120202",
        heat_1="#2a0503",
        heat_2="#5d0a0a",
        heat_3="#a81212",
        heat_4="#ff3131",
        heat_5="#ff7a00",
    ),

    "blue": TronTheme(
        name="blue",
        bg_deep="#020814",
        bg_panel="#020814",
        bg_inner="#061827",
        primary="#00e5ff",
        secondary="#00aaff",
        accent="#66f7ff",
        text_main="#ffffff",
        text_soft="#d8f7ff",
        text_muted="#b8d8e8",
        dark_core="#020814",
        glow_id="blueGlow",
        soft_glow_id="softBlueGlow",
        border_grad_id="panelBorder",
        title_grad_id="titleGrad",

        # blue bike / selected-year-month / current-day glow spectrum
        heat_0="#020814",
        heat_1="#061827",
        heat_2="#004466",
        heat_3="#0077aa",
        heat_4="#00aaff",
        heat_5="#00e5ff",
    ),

    "purple": TronTheme(
        name="purple",
        bg_deep="#050008",
        bg_panel="#050008",
        bg_inner="#14001f",
        primary="#d86cff",
        secondary="#b026ff",
        accent="#c77dff",
        text_main="#ffffff",
        text_soft="#d8c7ff",
        text_muted="#b8b8b8",
        dark_core="#050008",
        glow_id="violetGlow",
        soft_glow_id="softVioletGlow",
        border_grad_id="panelBorder",
        title_grad_id="titleGrad",

        # locked / unavailable / unused grid spectrum
        heat_0="#050008",
        heat_1="#100014",
        heat_2="#1c0028",
        heat_3="#3d005a",
        heat_4="#b026ff",
        heat_5="#d86cff",
    ),
}


def get_theme(name: str) -> TronTheme:
    if name not in THEMES:
        raise ValueError(f"Unknown theme: {name}. Choose from: {', '.join(THEMES)}")
    return THEMES[name]


def make_filters(theme: TronTheme) -> str:
    return f"""
    <filter id="{theme.glow_id}" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="{theme.soft_glow_id}" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
"""


def make_panel_gradients(theme: TronTheme, width: int, height: int) -> str:
    return f"""
    <linearGradient id="{theme.border_grad_id}" x1="0" y1="0" x2="{width}" y2="{height}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{theme.primary}"/>
      <stop offset="0.45" stop-color="{theme.secondary}"/>
      <stop offset="1" stop-color="{theme.accent}"/>
    </linearGradient>

    <linearGradient id="{theme.title_grad_id}" x1="250" y1="0" x2="950" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="0.35" stop-color="{theme.primary}"/>
      <stop offset="0.72" stop-color="{theme.secondary}"/>
      <stop offset="1" stop-color="{theme.accent}"/>
    </linearGradient>
"""


def make_common_style() -> str:
    return """
  <style>
    .panelPulse {
      animation: panelPulse 3.8s ease-in-out infinite alternate;
    }

    .lineFlow {
      stroke-dasharray: 24 18;
      animation: lineFlow 4.8s linear infinite;
    }

    .softFloat {
      animation: softFloat 6.8s ease-in-out infinite alternate;
    }

    .fadeIn1 {
      animation: fadeIn 1.2s ease-out both;
    }

    .fadeIn2 {
      animation: fadeIn 1.2s ease-out 0.25s both;
    }

    .fadeIn3 {
      animation: fadeIn 1.2s ease-out 0.45s both;
    }

    .fadeIn4 {
      animation: fadeIn 1.2s ease-out 0.65s both;
    }

    .fadeIn5 {
      animation: fadeIn 1.2s ease-out 0.85s both;
    }

    .fadeIn6 {
      animation: fadeIn 1.2s ease-out 1.05s both;
    }

    .fadeIn7 {
      animation: fadeIn 1.2s ease-out 1.25s both;
    }

    @keyframes panelPulse {
      0%   { opacity: 0.72; }
      100% { opacity: 1; }
    }

    @keyframes lineFlow {
      to { stroke-dashoffset: -180; }
    }

    @keyframes softFloat {
      0%   { transform: translateY(-3px); opacity: 0.72; }
      100% { transform: translateY(3px); opacity: 1; }
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to   { opacity: 1; transform: translateY(0); }
    }
  </style>
"""


def make_defs(theme: TronTheme, width: int, height: int) -> str:
    return f"""
  <defs>
{make_filters(theme)}
{make_panel_gradients(theme, width, height)}
  </defs>
"""


def make_glass_panel(theme: TronTheme, width: int = 1200) -> str:
    return f"""
  <!-- glass panel -->
  <rect x="72" y="48" width="1056" height="318" rx="22"
        fill="{theme.bg_panel}" fill-opacity="0.80"
        stroke="url(#{theme.border_grad_id})" stroke-width="2.5"
        filter="url(#{theme.soft_glow_id})"/>

  <rect x="96" y="74" width="1008" height="266" rx="16"
        fill="{theme.bg_inner}" fill-opacity="0.42"
        stroke="{theme.secondary}" stroke-width="1"
        stroke-opacity="0.90"/>
"""


def make_corner_geometry(theme: TronTheme) -> str:
    cls = "class"

    return f"""
  <!-- corner geometry -->
  <path {cls}="lineFlow" d="M112 112 H270" stroke="{theme.primary}" stroke-width="2.5" filter="url(#{theme.glow_id})"/>
  <path {cls}="lineFlow" d="M930 112 H1088" stroke="{theme.accent}" stroke-width="2.5" filter="url(#{theme.glow_id})"/>
  <path {cls}="lineFlow" d="M112 306 H270" stroke="{theme.accent}" stroke-width="2.5" filter="url(#{theme.glow_id})"/>
  <path {cls}="lineFlow" d="M930 306 H1088" stroke="{theme.primary}" stroke-width="2.5" filter="url(#{theme.glow_id})"/>
"""
