# make_tron_contributions.py
""" 
0. shift the big rectangle contribution_box() to left and make space for a vertical rectangle year_box(year) which has small table rectangles that has different {years} in the .json. below this contribution_box(), make a horizontal rectangle month_box(month) that depicts 3/4 words of {month} from the .json in the 12 compartments along the length of the big contribution_box() that depicts the years i had been on github . current {year} and {month} can be toggled with the click and it glows neon blue and the grid boxes show the contributions and chnage of number of grid boxes/ days accordingly. in this code, accidentally, the small grids are enclosed in the smallest rectangle which is enclosed by outline rectangles. remove the smallest rectangle and let the inner outline rectangle enclose the small grid boxes. in case user clicks the month for which the data is not available, make those boxes locked untill that month is unlocked. The dark background_box() with faint orange dots is a nice touch. make sure it is bigger than all the other boxes and spectrum_box() combined. background_box() serves as a track for tron_bike(color). 

1. grid_box_behaviours(): the number of grid boxes=number of days in selected {month} of that {year}. The contribution will be indicated in the individual grid box contribution heat map of increasing shade intensity. the contribution shade shall be displayed in theme orange . show that with legend = number of contributions: [shade spectrum] below the month horizontal rectangle. only the current date will have an additional glowing blue neon outline, rest of the unused grids will have get_theme("purple": TronTheme("secondary")) , the used one will be completely filled with the spectrum of get_theme("red"). need to addd more theme shades in red orange please suggest 

THEMES = { "red": TronTheme( name="red", bg_deep="#050505", bg_panel="#050505", bg_inner="#1a0400", primary="#ff3131", secondary="#ff1e1e", accent="#ff7a00", text_main="#ffffff", text_soft="#dddddd", text_muted="#b8b8b8", dark_core="#050505", glow_id="redGlow", soft_glow_id="softRedGlow", border_grad_id="panelBorder", title_grad_id="titleGrad",}. 
the grid_box_behaviours() generates a json that updates after every commit and cron that updates every month, or whenever needed. 

2. trail_line(color): trail line is associated with tron_bike(color) and only exists if tron_bike(color) does. no random trail_line(color) anywhere else. whatever color is, itrail_line(color) is not fading and glowing as whole, but the intensity decreases from the one connected to the bike to the end of it. shade of trail_line(color) is bright neone color . the length of trail_line(color) is fixed and the following tron_bike("red") starts after some distance the trail_line("blue") of tron_bike("blue") ends. The trail_line(color) follows the trail path(). 

3. trail path(): is straight but can take curves, starts from the top left corner of the background_box() with tron_bike("blue") +its trail_line("blue") followed by tron_bike("red") +its trail_line("red") with the tron_bike_gap variable. background_box() serves as a track for tron_bike(color), and the tron_bike(color) trail_line(color) follow the trail path() with in the background_box() out of contribution_box(), month_box() and spectrum_box() from the left and bottom and enters the contribution_box() from the space between the month_box() at the bottom and year_box() at the right of the contribution box from the bottom right diagonal corner to contribution_box(). and goes to the latest contribution in order to the later in order. if there is no contribution, tron_bike(color) randomly drives within the contribution_box within the inner enclosed glass line with its trail_line(color) endlessly without crashing . this entering the contribution_box() happens only once, and after filled contribution boxes are eaten or no filled contribution boxes, the tron_bike(color) drives within the contribution_box() endlessly in straight or curve line randomly with trail_speed. 

4. trail_speed= constant variable

    * tron_bike(color) = separate reusable object
    * trail_line(color) = attached to that bike only
    * bike_vehicle(...) = bike + trail + motion on one route
    * path_policy_blue() = builds the actual route logic
    * path_policy_red() = same route, delayed by TRON_BIKE_GAP
    * TRAIL_SPEED = one constant controlling full-loop motion speed
"""
# make_tron_contributions.py

from __future__ import annotations

import calendar
import json
import os
import random
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from xml.sax.saxutils import escape
import calendar
from ares_tron_theme import (
    TronTheme,
    get_theme,
    make_defs,
    make_filters,
    make_glass_panel,
    make_corner_geometry,
    make_common_style,
)
from readme_config import load_config
from dataclasses import dataclass
import calendar
from typing import List, Tuple

config = load_config()

DATA_PATH = config.data_dir / "contributions.json"
OUT_PATH = config.assets_dir / "tron-contributions.svg"
STATE_OUT_PATH = config.data_dir / "tron-grid-state.json"

YEAR_ENV = "README_CONTRIB_YEAR"
MONTH_ENV = "README_CONTRIB_MONTH"

WIDTH = 1200
HEIGHT = 560

TRAIL_SPEED = 30.5          # full route duration in seconds
TRON_BIKE_GAP = 4        # red starts this much later than blue

TRAIL_LENGTH_BLUE = 170
TRAIL_LENGTH_RED = 150

TRAIL_WIDTH_BLUE = 7.2
TRAIL_WIDTH_RED = 6.6
TRAIL_PATH_UNITS = 1000
TRAIL_SEGMENTS = 22
TRAIL_SPAN_BLUE = 155
TRAIL_SPAN_RED = 135
ROAM_POINT_COUNT = 18
ROAM_PADDING_X = 28
ROAM_PADDING_Y = 22
ROAM_POINT_COUNT = 18
TRAIL_HEAD_OFFSET_BLUE = -90
TRAIL_HEAD_OFFSET_RED = 50
BLUE_ROUTE_DASH = 115
RED_ROUTE_DASH = 95
LEAD_GAP = 14        # pushes the softer body slightly behind the bike
LEAD_CAP_LEN = 20    # short intense segment right behind the bike


CELL = 13
GAP = 5

CONTRIB_X = 92
CONTRIB_Y = 92
CONTRIB_W = 910
CONTRIB_H = 310
#git calender
GRID_LABEL_GUTTER_W = 58
GRID_TOP_LABEL_H = 28

GRID_CELL = 13
GRID_GAP = 4
GRID_RX = 2

GRID_ROWS = 7  # Mon-Sun

#the actual grid area inside contribution_box():
GRID_AREA_X = CONTRIB_X + 18
GRID_AREA_Y = CONTRIB_Y + 14
GRID_AREA_W = CONTRIB_W - 44
GRID_AREA_H = CONTRIB_H - 36

WEEKDAY_LABEL_X = GRID_AREA_X
WEEKDAY_LABEL_W = 54

GRID_X0 = GRID_AREA_X + WEEKDAY_LABEL_W + 10
GRID_Y0 = GRID_AREA_Y + 26
WEEKDAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

BACKGROUND_X = 0
BACKGROUND_Y = 0
BACKGROUND_W = WIDTH
BACKGROUND_H = HEIGHT

CANVAS_X = 0
CANVAS_Y = 0
CANVAS_W = WIDTH
CANVAS_H = HEIGHT



YEAR_BOX_X = 1024
YEAR_BOX_Y = CONTRIB_Y
YEAR_BOX_W = 104
YEAR_BOX_H = CONTRIB_H

MONTH_BOX_X = CONTRIB_X
MONTH_BOX_Y = CONTRIB_Y + CONTRIB_H + 28
MONTH_BOX_W = CONTRIB_W
MONTH_BOX_H = 54

SPECTRUM_X = CONTRIB_X
SPECTRUM_Y = 472
SPECTRUM_W = CONTRIB_W
SPECTRUM_H = 42

GRID_PAD_X = 34
GRID_PAD_Y = 46

GRID_X = CONTRIB_X + GRID_PAD_X
GRID_Y = CONTRIB_Y + GRID_PAD_Y

MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def _load_data() -> Dict:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"{DATA_PATH} does not exist. Run fetch_contributions.py first."
        )
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _parse_date(value: str) -> Optional[date]:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        return None


def _today() -> date:
    return date.today()


def _all_days_from_data(data: Dict) -> List[Dict]:
    """
    Supports:
      {"days": [...]}
      {"years": {"2026": [...], "2025": [...]}}
    """
    days: List[Dict] = []

    if isinstance(data.get("years"), dict):
        for year_days in data["years"].values():
            days.extend(year_days)
    else:
        days.extend(data.get("days", []))

    normalized: List[Dict] = []

    for item in days:
        date_text = str(item.get("date", ""))
        parsed = _parse_date(date_text)

        if parsed is None:
            continue

        normalized.append(
            {
                "date": date_text,
                "year": parsed.year,
                "month": parsed.month,
                "day": parsed.day,
                "count": int(item.get("count", item.get("contributionCount", 0))),
                "raw": item,
            }
        )

    normalized.sort(key=lambda d: d["date"])
    return normalized

def weekday_row_y(row_idx: int) -> int:
    return GRID_Y0 + row_idx * (GRID_CELL + GRID_GAP)
  
  
def weekday_label_y(row_idx: int) -> int:
    return weekday_row_y(row_idx) + GRID_CELL * 0.72
  
def week_col_x(col_idx: int) -> int:
    return GRID_X0 + col_idx * (GRID_CELL + GRID_GAP)
  
def week_label_x(col_idx: int) -> float:
    return week_col_x(col_idx) + GRID_CELL / 2
  
def month_layout(year: int, month: int):
    cal = calendar.Calendar(firstweekday=0)  # Monday
    weeks = cal.monthdayscalendar(year, month)
    return weeks

def available_years(days: List[Dict]) -> List[int]:
    years = sorted({int(d["year"]) for d in days})
    if not years:
        years = [_today().year]
    return years

@dataclass(frozen=True)
class CalendarLayout:
    inner_x: float
    inner_y: float
    inner_w: float
    inner_h: float

    weekday_gutter_w: float
    week_header_h: float

    grid_x: float
    grid_y: float
    grid_w: float
    grid_h: float

    cols: int
    rows: int

    col_step: float
    row_step: float
    cell_size: float
    
def build_calendar_layout(num_weeks: int) -> CalendarLayout:
    inner_x = CONTRIB_X + 28
    inner_y = CONTRIB_Y + 28
    inner_w = CONTRIB_W - 56
    inner_h = CONTRIB_H - 56

    weekday_gutter_w = 58
    week_header_h = 30

    rows = 7
    cols = max(4, num_weeks)

    grid_x = inner_x + weekday_gutter_w
    grid_y = inner_y + week_header_h
    grid_w = inner_w - weekday_gutter_w - 18
    grid_h = inner_h - week_header_h - 16

    col_step = grid_w / cols
    row_step = grid_h / rows

    cell_size = min(col_step, row_step) * 0.42
    cell_size = max(11, min(cell_size, 15))

    return CalendarLayout(
        inner_x=inner_x,
        inner_y=inner_y,
        inner_w=inner_w,
        inner_h=inner_h,
        weekday_gutter_w=weekday_gutter_w,
        week_header_h=week_header_h,
        grid_x=grid_x,
        grid_y=grid_y,
        grid_w=grid_w,
        grid_h=grid_h,
        cols=cols,
        rows=rows,
        col_step=col_step,
        row_step=row_step,
        cell_size=cell_size,
    )
def week_center_x(layout: CalendarLayout, col_idx: int) -> float:
    return layout.grid_x + (col_idx + 0.5) * layout.col_step


def weekday_center_y(layout: CalendarLayout, row_idx: int) -> float:
    return layout.grid_y + (row_idx + 0.5) * layout.row_step


def grid_cell_xy(layout: CalendarLayout, week_idx: int, weekday_idx: int) -> Tuple[float, float]:
    """
    Returns top-left corner of the cell centered at the calendar intersection.
    """
    cx = week_center_x(layout, week_idx)
    cy = weekday_center_y(layout, weekday_idx)
    x = cx - layout.cell_size / 2
    y = cy - layout.cell_size / 2
    return x, y

def build_month_matrix(year: int, month: int) -> List[List[int]]:
    cal = calendar.Calendar(firstweekday=0)  # Monday
    return cal.monthdayscalendar(year, month)

def requested_year_month(days: List[Dict]) -> Tuple[int, int]:
    today = _today()
    years = available_years(days)

    env_year = os.getenv(YEAR_ENV)
    env_month = os.getenv(MONTH_ENV)

    if env_year:
        year = int(env_year)
    elif today.year in years:
        year = today.year
    else:
        year = years[-1]

    if env_month:
        month = int(env_month)
    else:
        month = today.month if year == today.year else 12

    month = max(1, min(12, month))
    return year, month


def month_has_data(days: List[Dict], year: int, month: int) -> bool:
    return any(d["year"] == year and d["month"] == month for d in days)

#Weekday Labels
def weekday_labels(layout: CalendarLayout, purple_theme: TronTheme) -> str:
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    parts = ['<g id="weekdayLabels">']

    for row_idx, name in enumerate(names):
        x = layout.inner_x + layout.weekday_gutter_w - 8
        y = weekday_center_y(layout, row_idx) + 3.5

        parts.append(
            f'''
    <text x="{x:.2f}" y="{y:.2f}"
          text-anchor="end"
          font-family="JetBrains Mono, Consolas, monospace"
          font-size="10.5"
          font-weight="700"
          letter-spacing="0.3"
          fill="{purple_theme.accent}">
      {name}
    </text>
'''
        )

    parts.append("</g>")
    return "".join(parts)

# Week labels
def week_labels(num_weeks: int, layout: CalendarLayout, purple_theme: TronTheme) -> str:
    parts = ['<g id="weekLabels">']

    for col_idx in range(num_weeks):
        x = week_center_x(layout, col_idx)
        y = layout.inner_y + 12

        parts.append(
            f'''
    <text x="{x:.2f}" y="{y:.2f}"
          text-anchor="middle"
          font-family="JetBrains Mono, Consolas, monospace"
          font-size="10.5"
          font-weight="700"
          letter-spacing="0.4"
          fill="{purple_theme.accent}">
      Week {col_idx + 1}
    </text>
'''
        )

    parts.append("</g>")
    return "".join(parts)


def grid_slot_xy(week_idx: int, weekday_idx: int) -> tuple[int, int]:
    x = week_col_x(week_idx)
    y = weekday_row_y(weekday_idx)
    return x, y

def build_month_grid(year: int, month: int):
    cal = calendar.Calendar(firstweekday=0)
    return cal.monthdayscalendar(year, month)

def days_in_selected_month(year: int, month: int) -> List[Dict]:
    last_day = calendar.monthrange(year, month)[1]
    return [
        {
            "date": date(year, month, day).isoformat(),
            "year": year,
            "month": month,
            "day": day,
            "count": 0,
            "raw": {},
        }
        for day in range(1, last_day + 1)
    ]

def render_month_grid(
    year: int,
    month: int,
    month_data: dict,
    red_theme: TronTheme,
    purple_theme: TronTheme,
    blue_theme: TronTheme,
) -> str:
    weeks = build_month_matrix(year, month)
    layout = build_calendar_layout(len(weeks))

    parts = ['<g id="gridBoxes">']

    # today's date if selected month/year is current
    today = date.today()
    is_current_month = (today.year == year and today.month == month)

    for week_idx, week in enumerate(weeks):
        for weekday_idx, day_num in enumerate(week):
            x, y = grid_cell_xy(layout, week_idx, weekday_idx)

            if day_num == 0:
                # empty calendar slot
                fill = purple_theme.secondary
                fill_opacity = 0.12
                stroke = purple_theme.secondary
                stroke_opacity = 0.45
                extra = ""
                title_text = "No date"
            else:
                key = f"{year:04d}-{month:02d}-{day_num:02d}"
                count = int(month_data.get(key, 0))

                fill = contribution_fill(red_theme, purple_theme, count)
                fill_opacity = 1.0 if count > 0 else 0.25
                stroke = purple_theme.accent if count == 0 else red_theme.accent
                stroke_opacity = 0.70 if count > 0 else 0.45

                if is_current_month and today.day == day_num:
                    extra = f'''
      <rect x="{x-2:.2f}" y="{y-2:.2f}"
            width="{layout.cell_size+4:.2f}" height="{layout.cell_size+4:.2f}"
            rx="3.5"
            fill="none"
            stroke="{blue_theme.primary}"
            stroke-width="1.4"
            filter="url(#{blue_theme.glow_id})"/>
'''
                else:
                    extra = ""

                title_text = f"{key}: {count} contribution{'s' if count != 1 else ''}"

            parts.append(
                f'''
    <g>
      <rect x="{x:.2f}" y="{y:.2f}"
            width="{layout.cell_size:.2f}" height="{layout.cell_size:.2f}"
            rx="2.4"
            fill="{fill}"
            fill-opacity="{fill_opacity:.2f}"
            stroke="{stroke}"
            stroke-opacity="{stroke_opacity:.2f}"
            stroke-width="1"/>
      <title>{title_text}</title>
      {extra}
    </g>
'''
            )

    parts.append("</g>")
    return "".join(parts)

def selected_month_days(days: List[Dict], year: int, month: int) -> List[Dict]:
    base = days_in_selected_month(year, month)
    by_date = {d["date"]: dict(d) for d in base}

    for d in days:
        if d["year"] == year and d["month"] == month:
            by_date[d["date"]]["count"] = int(d["count"])
            by_date[d["date"]]["raw"] = d.get("raw", {})

    return [by_date[k] for k in sorted(by_date)]


def grid_dimensions(month_days: List[Dict]) -> Tuple[int, int]:
    count = len(month_days)
    cols = min(16, max(7, count))
    rows = (count + cols - 1) // cols
    return cols, rows


def grid_position(index: int, cols: int) -> Tuple[int, int]:
    col = index % cols
    row = index // cols
    return GRID_X + col * (CELL + GAP), GRID_Y + row * (CELL + GAP)


def grid_cell_center(
    layout: CalendarLayout,
    week_idx: int,
    weekday_idx: int,
) -> Tuple[float, float]:
    x, y = grid_cell_xy(layout, week_idx, weekday_idx)
    return (
        x + layout.cell_size / 2,
        y + layout.cell_size / 2,
    )


def contribution_level(count: int) -> int:
    if count <= 0:
        return 0
    if count == 1:
        return 1
    if count <= 3:
        return 2
    if count <= 6:
        return 3
    if count <= 10:
        return 4
    return 5


def contribution_fill(red_theme: TronTheme, purple_theme: TronTheme, count: int) -> str:
    level = contribution_level(count)

    if level == 0:
        return purple_theme.heat_2

    shades = [
        red_theme.heat_0,
        red_theme.heat_1,
        red_theme.heat_2,
        red_theme.heat_3,
        red_theme.heat_4,
        red_theme.heat_5,
    ]
    return shades[level]


def contribution_opacity(count: int) -> str:
    level = contribution_level(count)
    return ["0.18", "0.42", "0.62", "0.78", "0.92", "1"][level]


def contribution_stroke(theme_red: TronTheme, theme_purple: TronTheme, count: int) -> str:
    if count <= 0:
        return theme_purple.secondary
    return contribution_fill(theme_red, theme_purple, count)

def contribution_inner_bounds() -> Tuple[float, float, float, float]:
    """
    Inner roam-safe region inside contribution_box().
    """
    left = CONTRIB_X + ROAM_PADDING_X
    top = CONTRIB_Y + ROAM_PADDING_Y
    right = CONTRIB_X + CONTRIB_W - ROAM_PADDING_X
    bottom = CONTRIB_Y + CONTRIB_H - ROAM_PADDING_Y
    return left, top, right, bottom


def entry_path_points() -> List[Tuple[float, float]]:
    """
    Entry route:
      - starts top-left inside background_box
      - runs down the left track
      - runs along bottom track outside month/spectrum area
      - enters contribution_box once from bottom-right diagonal
    """
    start_x = BACKGROUND_X + 22
    start_y = BACKGROUND_Y + 34

    left_lane_y = MONTH_BOX_Y + MONTH_BOX_H + 14
    right_lane_x = YEAR_BOX_X - 18
    entry_x = CONTRIB_X + CONTRIB_W - 36
    entry_y = CONTRIB_Y + CONTRIB_H - 30

    return [
        (start_x, start_y),
        (start_x, left_lane_y),
        (right_lane_x, left_lane_y),
        (entry_x, entry_y),
    ]


def roam_path_points(
    month_days: List[Dict],
    count: int = ROAM_POINT_COUNT,
) -> List[Tuple[float, float]]:
    """
    Deterministic roaming points inside contribution_box() after contribution
    cells have been visited, or immediately if no contributions exist.
    """
    left, top, right, bottom = contribution_inner_bounds()

    seed = "roam|" + "|".join(d["date"] for d in month_days)
    rng = random.Random(seed)

    pts: List[Tuple[float, float]] = []
    for _ in range(count):
        x = rng.uniform(left, right)
        y = rng.uniform(top, bottom)
        pts.append((x, y))

    # keep movement readable: left-to-right wave, with some vertical randomness
    pts.sort(key=lambda p: (round(p[0] / 70), p[1]))
    return pts

def point_path(
    points: List[Tuple[float, float]],
    curve: bool = True,
) -> str:
    """
    Build an SVG path from route points.

    - Supports float coordinates.
    - Uses straight lines when curve=False.
    - Uses smooth quadratic curves when curve=True.
    - Safe for bike routes, contribution-cell routes, and roaming routes.
    """
    if not points:
        return ""

    if len(points) == 1:
        x, y = points[0]
        return f"M {x:.2f} {y:.2f}"

    if not curve:
        commands = [f"M {points[0][0]:.2f} {points[0][1]:.2f}"]
        for x, y in points[1:]:
            commands.append(f"L {x:.2f} {y:.2f}")
        return " ".join(commands)

    commands = [f"M {points[0][0]:.2f} {points[0][1]:.2f}"]

    # Smooth route: each intermediate point acts like a soft control point.
    for i in range(1, len(points) - 1):
        cx, cy = points[i]
        nx, ny = points[i + 1]

        mid_x = (cx + nx) / 2.0
        mid_y = (cy + ny) / 2.0

        commands.append(
            f"Q {cx:.2f} {cy:.2f} {mid_x:.2f} {mid_y:.2f}"
        )

    # Finish cleanly at the final point.
    last_x, last_y = points[-1]
    commands.append(f"T {last_x:.2f} {last_y:.2f}")

    return " ".join(commands)


def active_grid_indices(
    month_days: List[Dict],
    weeks: List[List[int]],
) -> List[Tuple[int, int, int]]:
    """
    Return active contribution cells in calendar coordinates.

    Returns:
      [
        (day_number, week_idx, weekday_idx),
        ...
      ]

    week_idx    = Week 1, Week 2, ...
    weekday_idx = Mon=0 ... Sun=6
    """

    by_day_number: Dict[int, Dict] = {
        int(day["day"]): day
        for day in month_days
    }

    active: List[Tuple[int, int, int]] = []

    for week_idx, week in enumerate(weeks):
        for weekday_idx, day_number in enumerate(week):
            if day_number == 0:
                continue

            day = by_day_number.get(day_number)
            if day is None:
                continue

            if int(day.get("count", 0)) > 0:
                active.append((day_number, week_idx, weekday_idx))

    return active

def random_drive_indices(
    month_days: List[Dict],
    weeks: List[List[int]],
    max_points: int = 80,
) -> List[Tuple[int, int, int]]:
    """
    Return pseudo-random drivable calendar cells.

    Returns:
      [
        (day_number, week_idx, weekday_idx),
        ...
      ]

    This matches active_grid_indices(), so path_policy_blue()
    can treat active and random cells the same way.
    """

    if not month_days:
        return []

    valid_cells: List[Tuple[int, int, int]] = []

    for week_idx, week in enumerate(weeks):
        for weekday_idx, day_number in enumerate(week):
            if day_number == 0:
                continue

            valid_cells.append((day_number, week_idx, weekday_idx))

    if not valid_cells:
        return []

    seed = "|".join(day["date"] for day in month_days)
    rng = random.Random(seed)

    sample_size = min(max_points, len(valid_cells))
    sampled = rng.sample(valid_cells, sample_size)

    # Keep motion somewhat readable:
    # mostly left-to-right by week, with small chaos.
    sampled.sort(
        key=lambda cell: (
            cell[1] + rng.randint(-1, 1),  # week_idx
            cell[2] + rng.randint(-1, 1),  # weekday_idx
        )
    )

    return sampled


def entry_path_points() -> List[Tuple[int, int]]:
    """
    Track starts at top-left of full background_box, moves around outside boxes,
    then enters contribution_box from the bottom-right diagonal space.
    """
    return [
        (BACKGROUND_X + 28, BACKGROUND_Y + 42),
        (BACKGROUND_X + 28, BACKGROUND_Y + BACKGROUND_H - 88),
        (CONTRIB_X + 120, BACKGROUND_Y + BACKGROUND_H - 74),
        (YEAR_BOX_X + YEAR_BOX_W + 20, BACKGROUND_Y + BACKGROUND_H - 96),
        (YEAR_BOX_X + YEAR_BOX_W + 20, MONTH_BOX_Y - 10),
        (CONTRIB_X + CONTRIB_W - 18, CONTRIB_Y + CONTRIB_H - 24),
    ]


def path_policy_blue(
    month_days: List[Dict],
    layout: CalendarLayout,
    weeks: List[List[int]],
) -> Tuple[str, List[Tuple[int, int, int]]]:
    """
    Blue bike path:
      1. enters from top-left of background_box
      2. moves along external track
      3. enters contribution_box once from bottom-right diagonal
      4. visits contribution cells in chronological order
      5. then roams forever inside contribution_box
    """
    active_cells = sorted(
        active_grid_indices(month_days, weeks),
        key=lambda item: item[0],   # day_number
    )

    route_points = entry_path_points()

    if active_cells:
        route_points.extend(
            grid_cell_center(layout, week_idx, weekday_idx)
            for _day_number, week_idx, weekday_idx in active_cells
        )

    route_points.extend(roam_path_points(month_days, count=ROAM_POINT_COUNT))

    return point_path(route_points, curve=True), active_cells


def path_policy_red(
    month_days: List[Dict],
    layout: CalendarLayout,
    weeks: List[List[int]],
) -> str:
    """
    Red/orange chaser follows the same path.
    The chase delay is controlled in bike_layers() with TRON_BIKE_GAP.
    """
    blue_path, _ = path_policy_blue(month_days, layout, weeks)
    return blue_path




def tron_bike(
    symbol_id: str,
    theme: TronTheme,
    nose_color: str,
) -> str:
    """
    Separate reusable TRON bike symbol.
    Forward direction is +X.
    """
    return f"""
  <g id="{symbol_id}">
    <!-- glow core -->
    <circle cx="0" cy="0" r="2.2"
            fill="{theme.text_main}"
            filter="url(#{theme.glow_id})"/>

    <!-- bike body -->
    <path d="M -8 -3 L 2 -3 L 9 0 L 2 3 L -8 3 L -4 0 Z"
          fill="{nose_color}"
          fill-opacity="0.95"
          filter="url(#{theme.glow_id})"/>

    <!-- inner light blade -->
    <path d="M -5 -1.1 L 3 -1.1 L 6 0 L 3 1.1 L -5 1.1 Z"
          fill="{theme.text_main}"
          fill-opacity="0.85"/>

    <!-- rear fin -->
    <path d="M -10 -4 L -7 0 L -10 4"
          fill="none"
          stroke="{nose_color}"
          stroke-width="1.3"
          stroke-linecap="round"
          stroke-linejoin="round"
          filter="url(#{theme.glow_id})"/>

    <!-- front highlight -->
    <circle cx="8.4" cy="0" r="1.5"
            fill="{theme.text_main}"
            fill-opacity="0.96"/>
  </g>
"""

def svg_class(value: str) -> str:
    """
    Build SVG class attribute without writing literal className="..."
    in source, so formatters/extensions do not rewrite it to className.
    """
    return "class" + "=" + chr(34) + value + chr(34)

def seconds_value(value: str) -> float:
    if value.endswith("s"):
        return float(value[:-1])
    return float(value)

def trail_line(
    color_name: str,
    theme: TronTheme,
    gradient_id: str,
    route_id: str,
    begin: str,
    trail_length: float,
    trail_width: float,
    segment_count: int = 18,
) -> str:
    """
    Bike-attached afterburner trail.

    This guarantees the bike itself always has a visible fading neon tail.
    The larger route blaze is handled by neon_route_trail().
    """
    return f'''
    <g id="{color_name}BikeAfterburner">
      <!-- large attached glow -->
      <path d="M {-trail_length:.2f} 0 L 0 0"
            fill="none"
            stroke="url(#{gradient_id})"
            stroke-width="{trail_width * 3.8:.2f}"
            stroke-linecap="round"
            opacity="0.42"
            filter="url(#{theme.soft_glow_id})">
        <animateMotion dur="{TRAIL_SPEED}s"
                       begin="{begin}"
                       repeatCount="indefinite"
                       rotate="auto">
          <mpath href="#{route_id}"/>
        </animateMotion>
      </path>

      <!-- bright attached trail -->
      <path d="M {-trail_length:.2f} 0 L 0 0"
            fill="none"
            stroke="url(#{gradient_id})"
            stroke-width="{trail_width:.2f}"
            stroke-linecap="round"
            opacity="0.96"
            filter="url(#{theme.glow_id})">
        <animateMotion dur="{TRAIL_SPEED}s"
                       begin="{begin}"
                       repeatCount="indefinite"
                       rotate="auto">
          <mpath href="#{route_id}"/>
        </animateMotion>
      </path>

      <!-- hot white edge near bike -->
      <path d="M -36 0 L 0 0"
            fill="none"
            stroke="{theme.text_main}"
            stroke-width="{max(1.8, trail_width * 0.30):.2f}"
            stroke-linecap="round"
            opacity="0.82"
            filter="url(#{theme.glow_id})">
        <animateMotion dur="{TRAIL_SPEED}s"
                       begin="{begin}"
                       repeatCount="indefinite"
                       rotate="auto">
          <mpath href="#{route_id}"/>
        </animateMotion>
      </path>
    </g>
'''

def bike_vehicle(
    vehicle_id: str,
    bike_symbol_id: str,
    route_id: str,
    color_name: str,
    theme: TronTheme,
    gradient_id: str,
    trail_length: float,
    trail_width: float,
    begin: str,
) -> str:
    """
    One bike vehicle = path-following trail + bike head.

    Important:
    The bike and trail are related/generated together, but they each animate
    on the same route. This is what makes the trail follow the actual path
    instead of staying as one tiny straight line behind the bike.
    """
    return f"""
  <g id="{vehicle_id}">
    {trail_line(
        color_name=color_name,
        theme=theme,
        gradient_id=gradient_id,
        route_id=route_id,
        begin=begin,
        trail_length=trail_length,
        trail_width=trail_width,
    )}

    <g id="{color_name}BikeHead" {svg_class("bike-head")}>
      <use href="#{bike_symbol_id}"/>

      <animateMotion dur="{TRAIL_SPEED}s"
                     begin="{begin}"
                     repeatCount="indefinite"
                     rotate="auto">
        <mpath href="#{route_id}"/>
      </animateMotion>
    </g>
  </g>
"""

def trail_gradients(
    blue_theme: TronTheme,
    red_theme: TronTheme,
) -> str:
    """
    Blazing neon trail gradients.

    Tail side fades out.
    Bike side becomes hot neon/white.
    """
    return f"""
    <linearGradient id="blueTrailGradient"
                    x1="-{TRAIL_LENGTH_BLUE}" y1="0"
                    x2="0" y2="0"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{blue_theme.bg_deep}" stop-opacity="0.00"/>
      <stop offset="28%" stop-color="{blue_theme.secondary}" stop-opacity="0.25"/>
      <stop offset="62%" stop-color="{blue_theme.primary}" stop-opacity="0.82"/>
      <stop offset="88%" stop-color="{blue_theme.accent}" stop-opacity="1.00"/>
      <stop offset="100%" stop-color="{blue_theme.text_main}" stop-opacity="1.00"/>
    </linearGradient>

    <linearGradient id="redTrailGradient"
                    x1="-{TRAIL_LENGTH_RED}" y1="0"
                    x2="0" y2="0"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{red_theme.bg_deep}" stop-opacity="0.00"/>
      <stop offset="28%" stop-color="{red_theme.secondary}" stop-opacity="0.30"/>
      <stop offset="62%" stop-color="{red_theme.primary}" stop-opacity="0.86"/>
      <stop offset="88%" stop-color="{red_theme.accent}" stop-opacity="1.00"/>
      <stop offset="100%" stop-color="{red_theme.text_main}" stop-opacity="1.00"/>
    </linearGradient>
"""

def bike_symbol_defs(
    blue_theme: TronTheme,
    red_theme: TronTheme,
) -> str:
    return f"""
    {tron_bike("bikeBlue", blue_theme, blue_theme.primary)}
    {tron_bike("bikeRed", red_theme, red_theme.accent)}
"""

def defs_block(
    red_theme: TronTheme,
    blue_theme: TronTheme,
    purple_theme: TronTheme,
) -> str:
    return f"""
  {make_defs(red_theme, WIDTH, HEIGHT)}

  <defs>
    {make_filters(blue_theme)}
    {make_filters(purple_theme)}

    <filter id="gridCellGlow" x="-90%" y="-90%" width="900%" height="300%">
      <feGaussianBlur stdDeviation="2.4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    {trail_gradients(blue_theme, red_theme)}

    <pattern id="backgroundCircuit" width="50" height="50" patternUnits="userSpaceOnUse">
      <path d="M4 8 H32 V20 H60"
            fill="none"
            stroke="{red_theme.primary}"
            stroke-opacity="0.13"
            stroke-width="1"/>
      <path d="M18 36 H48 V28 H80"
            fill="none"
            stroke="{red_theme.accent}"
            stroke-opacity="0.20"
            stroke-width="1"/>
      <circle cx="32" cy="20" r="1.8"
              fill="{red_theme.primary}"
              fill-opacity="0.25"/>
      <circle cx="60" cy="20" r="1.5"
              fill="{red_theme.accent}"
              fill-opacity="0.16"/>
    </pattern>

    <pattern id="scanlines" width="6" height="6" patternUnits="userSpaceOnUse">
      <path d="M 0 0 H 6"
            stroke="{red_theme.text_main}"
            stroke-opacity="0.035"
            stroke-width="1"/>
    </pattern>

    {bike_symbol_defs(blue_theme, red_theme)}
  </defs>
"""

def style_block() -> str:
    return f"""
  {make_common_style()}
  <style>
    .trailPulse {{
      animation: trailPulse 1.35s ease-in-out infinite alternate;
    }}

    .railPulse {{
      animation: railPulse 2.8s ease-in-out infinite alternate;
    }}

    .eatFlash {{
      animation: eatFlash 1.1s ease-in-out infinite;
    }}

    @keyframes trailPulse {{
      0%   {{ opacity: 0.52; }}
      100% {{ opacity: 1; }}
    }}

    @keyframes railPulse {{
      0%   {{ opacity: 0.18; }}
      100% {{ opacity: 0.70; }}
    }}

    @keyframes eatFlash {{
      0%   {{ opacity: 0; }}
      35%  {{ opacity: 1; }}
      100% {{ opacity: 0; }}
    }}
  </style>
"""


def background_box(red_theme: TronTheme) -> str:
    """
    Full-canvas dark TRON track.

    This must cover the entire SVG canvas so there is no transparent gap
    above/beside the asset when stacked under section-github-signal.svg.
    """
    return f"""
  <rect x="{CANVAS_X}" y="{CANVAS_Y}"
        width="{CANVAS_W}" height="{CANVAS_H}"
        fill="{red_theme.dark_core}"/>

  <rect x="{BACKGROUND_X}" y="{BACKGROUND_Y}"
        width="{BACKGROUND_W}" height="{BACKGROUND_H}"
        rx="0"
        fill="{red_theme.dark_core}"/>

  <rect x="{BACKGROUND_X}" y="{BACKGROUND_Y}"
        width="{BACKGROUND_W}" height="{BACKGROUND_H}"
        rx="0"
        fill="url(#backgroundCircuit)"
        opacity="0.88"/>

  <rect x="{BACKGROUND_X}" y="{BACKGROUND_Y}"
        width="{BACKGROUND_W}" height="{BACKGROUND_H}"
        rx="0"
        fill="url(#scanlines)"
        opacity="0.70"/>

  <rect x="28" y="28"
        width="{WIDTH - 56}" height="{HEIGHT - 56}"
        rx="10"
        fill="none"
        stroke="{red_theme.secondary}"
        stroke-opacity="0.18"
        stroke-width="1"/>
"""


def contribution_box(red_theme: TronTheme) -> str:
    """
    Big contribution box shifted left.
    No smallest extra rectangle around the grid.
    The inner glass line directly encloses grid boxes.
    """
    inner_x = CONTRIB_X + 18
    inner_y = CONTRIB_Y + 28
    inner_w = CONTRIB_W - 36
    inner_h = CONTRIB_H - 56

    return f"""
  <rect x="{CONTRIB_X}" y="{CONTRIB_Y}"
        width="{CONTRIB_W}" height="{CONTRIB_H}"
        rx="18"
        fill="{red_theme.bg_panel}"
        fill-opacity="0.80"
        stroke="url(#{red_theme.border_grad_id})"
        stroke-width="2.4"
        filter="url(#{red_theme.soft_glow_id})"/>

  <rect x="{inner_x}" y="{inner_y}"
        width="{inner_w}" height="{inner_h}"
        rx="10"
        fill="{red_theme.bg_inner}"
        fill-opacity="0.30"
        stroke="{red_theme.secondary}"
        stroke-width="1"
        stroke-opacity="0.90"/>
"""


def year_box(years: List[int], selected_year: int, red_theme: TronTheme, blue_theme: TronTheme) -> str:
    if not years:
        years = [selected_year]

    row_gap = 8
    row_h = min(32, max(22, (YEAR_BOX_H - 32 - row_gap * (len(years) - 1)) // max(1, len(years))))
    start_y = YEAR_BOX_Y + 18

    parts = [
        f"""
  <rect x="{YEAR_BOX_X}" y="{YEAR_BOX_Y}"
        width="{YEAR_BOX_W}" height="{YEAR_BOX_H}"
        rx="14"
        fill="{red_theme.bg_panel}"
        fill-opacity="0.82"
        stroke="{red_theme.accent}"
        stroke-width="1.6"
        filter="url(#{red_theme.soft_glow_id})"/>
"""
    ]

    for idx, year in enumerate(years):
        y = start_y + idx * (row_h + row_gap)
        is_selected = year == selected_year
        stroke_theme = blue_theme if is_selected else red_theme
        fill_theme = blue_theme if is_selected else red_theme
        opacity = "0.38" if is_selected else "0.14"
        stroke_w = "2.2" if is_selected else "1"

        parts.append(
            f"""
  <rect x="{YEAR_BOX_X + 14}" y="{y}"
        width="{YEAR_BOX_W - 28}" height="{row_h}"
        rx="6"
        fill="{fill_theme.bg_inner}"
        fill-opacity="{opacity}"
        stroke="{stroke_theme.primary}"
        stroke-width="{stroke_w}"
        filter="url(#{stroke_theme.glow_id})"/>

  <text x="{YEAR_BOX_X + YEAR_BOX_W // 2}" y="{y + row_h // 2 + 5}"
        text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="12"
        font-weight="700"
        fill="{stroke_theme.text_main}">
    {year}
  </text>
"""
        )

    return "\n".join(parts)


def month_box(
    available_months: Iterable[int],
    selected_month: int,
    red_theme: TronTheme,
    blue_theme: TronTheme,
    purple_theme: TronTheme,
) -> str:
    available = set(int(m) for m in available_months)
    cell_w = MONTH_BOX_W / 12

    parts = [
        f"""
  <rect x="{MONTH_BOX_X}" y="{MONTH_BOX_Y}"
        width="{MONTH_BOX_W}" height="{MONTH_BOX_H}"
        rx="10"
        fill="{red_theme.bg_panel}"
        fill-opacity="0.78"
        stroke="{red_theme.secondary}"
        stroke-width="1.2"
        filter="url(#{red_theme.soft_glow_id})"/>
"""
    ]

    for idx, name in enumerate(MONTH_NAMES):
        month = idx + 1
        x = MONTH_BOX_X + idx * cell_w + 5
        y = MONTH_BOX_Y + 10
        w = cell_w - 10
        h = MONTH_BOX_H - 20

        is_selected = month == selected_month
        is_available = month in available

        if is_selected:
            theme = blue_theme
            fill_opacity = "0.34"
            stroke_w = "2.0"
        elif is_available:
            theme = red_theme
            fill_opacity = "0.18"
            stroke_w = "1.0"
        else:
            theme = purple_theme
            fill_opacity = "0.10"
            stroke_w = "1.0"

        parts.append(
            f"""
  <rect x="{x}" y="{y}"
        width="{w}" height="{h}"
        rx="5"
        fill="{theme.bg_inner}"
        fill-opacity="{fill_opacity}"
        stroke="{theme.primary}"
        stroke-width="{stroke_w}"
        stroke-opacity="0.86"
        filter="url(#{theme.glow_id})"/>

  <text x="{x + w / 2}" y="{y + h / 2 + 4}"
        text-anchor="middle"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="10"
        font-weight="700"
        fill="{theme.text_main}"
        opacity="{'1' if is_available else '0.45'}">
    {name}
  </text>
"""
        )

        if not is_available:
            parts.append(
                f"""
  <path d="M {x + 8} {y + h - 8} H {x + w - 8}"
        stroke="{purple_theme.secondary}"
        stroke-width="1"
        stroke-opacity="0.65"/>
"""
            )

    return "\n".join(parts)


def spectrum_box(red_theme: TronTheme) -> str:
    """
    Compact GitHub-style contribution legend:
    Less [shade boxes] More

    Positioned at the bottom-right corner inside background_box().
    """

    # anchor to bottom-right of background_box()
    box_w = 210
    box_h = 28
    x = BACKGROUND_X + BACKGROUND_W - box_w - 24
    y = BACKGROUND_Y + BACKGROUND_H - box_h - 18

    # 5-box legend like GitHub
    shades = [
        red_theme.heat_0,
        red_theme.heat_2,
        red_theme.heat_3,
        red_theme.heat_4,
        red_theme.heat_5,
    ]

    square_size = 12
    square_gap = 6

    # first square starts after the "Less" label
    squares_x = x + 40
    squares_y = y + 8

    parts = [
        f"""
  <g id="spectrumLegend" {svg_class("lineFlow")}>
    <text x="{x}" y="{y + 18}"
          font-family="JetBrains Mono, Consolas, monospace"
          font-size="11"
          fill="{red_theme.text_soft}">
      Less
    </text>
"""
    ]

    for idx, color in enumerate(shades):
        sx = squares_x + idx * (square_size + square_gap)
        parts.append(
            f"""
    <rect x="{sx}" y="{squares_y}"
          width="{square_size}" height="{square_size}"
          rx="3"
          fill="{color}"
          stroke="{red_theme.accent}"
          stroke-opacity="0.55"
          stroke-width="0.8"
          filter="url(#{red_theme.glow_id})"/>
"""
        )

    more_x = squares_x + len(shades) * (square_size + square_gap) + 8
    parts.append(
        f"""
    <text x="{more_x}" y="{y + 18}"
          font-family="JetBrains Mono, Consolas, monospace"
          font-size="11"
          fill="{red_theme.text_soft}">
      More
    </text>
  </g>
"""
    )

    return "".join(parts)


def grid_box_behaviours(
    month_days: List[Dict],
    selected_year: int,
    selected_month: int,
    red_theme: TronTheme,
    blue_theme: TronTheme,
    purple_theme: TronTheme,
    layout: CalendarLayout,
    weeks: List[List[int]],
) -> Tuple[str, Dict]:
    """
    Render monthly contribution grid boxes as a proper calendar.

    Layout:
      columns = Week 1, Week 2, ...
      rows    = Mon, Tue, Wed, Thu, Fri, Sat, Sun

    Grid boxes are placed at the intersection of week columns and weekday rows.
    Date numbers are rendered beside real calendar cells.
    """

    today = _today()

    by_day_number: Dict[int, Dict] = {
        int(day["day"]): day
        for day in month_days
    }

    parts: List[str] = []
    state_days: List[Dict] = []

    date_font_size = max(8.5, min(layout.cell_size, 12))
    date_gap = max(5, layout.cell_size * 0.45)

    for week_idx, week in enumerate(weeks):
        for weekday_idx, day_number in enumerate(week):
            x, y = grid_cell_xy(layout, week_idx, weekday_idx)

            if day_number == 0:
                fill = purple_theme.heat_1
                stroke = purple_theme.secondary
                opacity = "0.10"
                stroke_opacity = "0.28"
                glow = ""
                title_text = "No date"
                count = 0
                date_text = ""
                is_today = False
                date_label_svg = ""

            else:
                day = by_day_number.get(day_number)

                if day is None:
                    date_text = date(
                        selected_year,
                        selected_month,
                        day_number,
                    ).isoformat()
                    count = 0
                else:
                    date_text = day["date"]
                    count = int(day["count"])

                is_today = (
                    selected_year == today.year
                    and selected_month == today.month
                    and day_number == today.day
                )

                fill = contribution_fill(red_theme, purple_theme, count)
                stroke = contribution_stroke(red_theme, purple_theme, count)
                opacity = contribution_opacity(count)
                stroke_opacity = "0.84"

                # Glow only for filled contribution cells, but no flashing.
                glow = 'filter="url(#gridCellGlow)"' if count > 0 else ""

                title_text = f"{date_text}: {count} contributions"

                date_label_svg = f"""
    <text x="{x + layout.cell_size + date_gap:.2f}"
          y="{y + layout.cell_size * 0.78:.2f}"
          text-anchor="start"
          font-family="JetBrains Mono, Consolas, monospace"
          font-size="{date_font_size:.2f}"
          font-weight="700"
          fill="{purple_theme.text_soft}"
          opacity="0.88">
      {day_number}
    </text>
"""

            parts.append(
                f"""
    <rect x="{x:.2f}" y="{y:.2f}"
          width="{layout.cell_size:.2f}" height="{layout.cell_size:.2f}"
          rx="2.4"
          fill="{fill}"
          fill-opacity="{opacity}"
          stroke="{stroke}"
          stroke-opacity="{stroke_opacity}"
          stroke-width="0.9"
          {glow}>
      <title>{escape(title_text)}</title>
    </rect>
{date_label_svg}
"""
            )


            if day_number != 0:
                state_days.append(
                    {
                        "date": date_text,
                        "day": day_number,
                        "count": count,
                        "week_index": week_idx,
                        "weekday_index": weekday_idx,
                        "x": round(x, 2),
                        "y": round(y, 2),
                        "is_today": is_today,
                    }
                )

    state = {
        "selected_year": selected_year,
        "selected_month": selected_month,
        "weeks": len(weeks),
        "weekdays": 7,
        "cell_size": round(layout.cell_size, 2),
        "grid_x": round(layout.grid_x, 2),
        "grid_y": round(layout.grid_y, 2),
        "grid_w": round(layout.grid_w, 2),
        "grid_h": round(layout.grid_h, 2),
        "days": state_days,
    }

    return "\n".join(parts), state
def neon_route_trail(
    trail_id: str,
    path_d: str,
    theme: TronTheme,
    color: str,
    hot_color: str,
    dash_len: float,
    width: float,
    begin: str,
    offset_from: float,
    offset_to: float,
    tail_segments: int = 5,
) -> str:
    """
    Softer and lighter TRON trail.

    Goals:
    - visibly present trail
    - toned down intensity
    - reduced lag by using fewer animated segments
    """
    parts = [f'<g id="{trail_id}">']

    # soft glow aura
    parts.append(
        f'''
  <path d="{path_d}"
        pathLength="{TRAIL_PATH_UNITS}"
        fill="none"
        stroke="{color}"
        stroke-width="{width * 2.6:.2f}"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-dasharray="{dash_len:.2f} {TRAIL_PATH_UNITS -20 - dash_len:.2f}"
        stroke-dashoffset="{offset_from:.2f}"
        opacity="0.12"
        filter="url(#{theme.soft_glow_id})">
    <animate attributeName="stroke-dashoffset"
             from="{offset_from:.2f}"
             to="{offset_to:.2f}"
             dur="{TRAIL_SPEED}s"
             begin="{begin}"
             repeatCount="indefinite"/>
  </path>

  <path d="{path_d}"
        pathLength="{TRAIL_PATH_UNITS}"
        fill="none"
        stroke="{color}"
        stroke-width="{width * 1.35:.2f}"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-dasharray="{dash_len:.2f} {TRAIL_PATH_UNITS - dash_len:.2f}"
        stroke-dashoffset="{offset_from:.2f}"
        opacity="0.34"
        filter="url(#{theme.glow_id})">
    <animate attributeName="stroke-dashoffset"
             from="{offset_from:.2f}"
             to="{offset_to:.2f}"
             dur="{TRAIL_SPEED}s"
             begin="{begin}"
             repeatCount="indefinite"/>
  </path>

  <path d="{path_d}"
        pathLength="{TRAIL_PATH_UNITS}"
        fill="none"
        stroke="{hot_color}"
        stroke-width="{max(1.4, width * 0.48):.2f}"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-dasharray="{dash_len * 0.76:.2f} {TRAIL_PATH_UNITS - dash_len * 0.76:.2f}"
        stroke-dashoffset="{offset_from:.2f}"
        opacity="0.48">
    <animate attributeName="stroke-dashoffset"
             from="{offset_from:.2f}"
             to="{offset_to:.2f}"
             dur="{TRAIL_SPEED}s"
             begin="{begin}"
             repeatCount="indefinite"/>
  </path>
'''
    )

    # reduced tail fade segments
    for i in range(1, tail_segments + 1):
        t = i / tail_segments
        lag = i * 18
        seg_dash = max(10, dash_len * (1.0 - 0.08 * i))
        seg_width = max(1.0, width * (1.0 - 0.14 * i))
        seg_opacity = max(0.04, 0.22 * ((1.0 - t) ** 1.35))

        parts.append(
            f'''
  <path d="{path_d}"
        pathLength="{TRAIL_PATH_UNITS}"
        fill="none"
        stroke="{color}"
        stroke-width="{seg_width:.2f}"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-dasharray="{seg_dash:.2f} {TRAIL_PATH_UNITS - seg_dash:.2f}"
        stroke-dashoffset="{offset_from + lag:.2f}"
        opacity="{seg_opacity:.3f}">
    <animate attributeName="stroke-dashoffset"
             from="{offset_from + lag:.2f}"
             to="{offset_to + lag:.2f}"
             dur="{TRAIL_SPEED}s"
             begin="{begin}"
             repeatCount="indefinite"/>
  </path>
'''
        )

    parts.append("</g>")
    return "\n".join(parts)
def bike_layers(
    blue_path: str,
    red_path: str,
    blue_theme: TronTheme,
    red_theme: TronTheme,
) -> str:
    return f"""
  <path id="blueRoute"
        d="{blue_path}"
        pathLength="{TRAIL_PATH_UNITS}"
        fill="none"
        stroke="none"
        opacity="0"/>

  <path id="redRoute"
        d="{red_path}"
        pathLength="{TRAIL_PATH_UNITS}"
        fill="none"
        stroke="none"
        opacity="0"/>

  {neon_route_trail(
        trail_id="blueRouteTrail",
        path_d=blue_path,
        theme=blue_theme,
        color=blue_theme.primary,
        hot_color=blue_theme.text_main,
        dash_len=92,
        width=TRAIL_WIDTH_BLUE,
        begin="0s",
        offset_from=TRAIL_PATH_UNITS - TRAIL_HEAD_OFFSET_BLUE,
        offset_to=0 - TRAIL_HEAD_OFFSET_BLUE,
        tail_segments=5,
    )}

  {neon_route_trail(
        trail_id="redRouteTrail",
        path_d=red_path,
        theme=red_theme,
        color=red_theme.accent,
        hot_color=red_theme.text_main,
        dash_len=78,
        width=TRAIL_WIDTH_RED,
        begin=f"{TRON_BIKE_GAP}s",
        offset_from=TRAIL_PATH_UNITS + 130 - TRAIL_HEAD_OFFSET_RED,
        offset_to=130 - TRAIL_HEAD_OFFSET_RED,
        tail_segments=5,
    )}

  {bike_vehicle(
        vehicle_id="blueVehicle",
        bike_symbol_id="bikeBlue",
        route_id="blueRoute",
        color_name="blue",
        theme=blue_theme,
        gradient_id="blueTrailGradient",
        trail_length=TRAIL_LENGTH_BLUE,
        trail_width=TRAIL_WIDTH_BLUE,
        begin="0s",
    )}

  {bike_vehicle(
        vehicle_id="redVehicle",
        bike_symbol_id="bikeRed",
        route_id="redRoute",
        color_name="red",
        theme=red_theme,
        gradient_id="redTrailGradient",
        trail_length=TRAIL_LENGTH_RED,
        trail_width=TRAIL_WIDTH_RED,
        begin=f"{TRON_BIKE_GAP}s",
    )}
"""
def current_date_flash(
    selected_year: int,
    selected_month: int,
    layout: CalendarLayout,
    weeks: List[List[int]],
    blue_theme: TronTheme,
) -> str:
    """
    Flash only the current date cell.

    This replaces eat_flashes(active_cells, ...), because active contribution
    cells should stay solid heat-map cells. Only today's cell should pulse blue.
    """

    today = _today()

    if selected_year != today.year or selected_month != today.month:
        return ""

    for week_idx, week in enumerate(weeks):
        for weekday_idx, day_number in enumerate(week):
            if day_number != today.day:
                continue

            x, y = grid_cell_xy(layout, week_idx, weekday_idx)

            return f"""
    <rect {svg_class("eatFlash")}
          x="{x - 2:.2f}" y="{y - 2:.2f}"
          width="{layout.cell_size + 4:.2f}" height="{layout.cell_size + 4:.2f}"
          rx="3.4"
          fill="none"
          stroke="{blue_theme.primary}"
          stroke-width="1.8"
          filter="url(#{blue_theme.glow_id})">
      <animate attributeName="opacity"
               values="0.25;1;0.25"
               dur="1.15s"
               repeatCount="indefinite"/>
      <animate attributeName="stroke-width"
               values="1.2;2.4;1.2"
               dur="1.15s"
               repeatCount="indefinite"/>
    </rect>
"""

    return ""
def main() -> None:
    data = _load_data()
    all_days = _all_days_from_data(data)

    selected_year, selected_month = requested_year_month(all_days)
    years = available_years(all_days)

    red_theme = get_theme("red")
    blue_theme = get_theme("blue")
    purple_theme = get_theme("purple")

    month_days = selected_month_days(
        all_days,
        selected_year,
        selected_month,
    )

    available_months = [
        month
        for month in range(1, 13)
        if month_has_data(all_days, selected_year, month)
    ]

    # Calendar layout for selected month.
    weeks = build_month_grid(selected_year, selected_month)
    num_weeks = len(weeks)
    layout = build_calendar_layout(num_weeks)

    # Month grid render.
    # This assumes grid_box_behaviours has been refactored to use the
    # calendar layout/intersection system.
    grid_svg, grid_state = grid_box_behaviours(
        month_days=month_days,
        selected_year=selected_year,
        selected_month=selected_month,
        red_theme=red_theme,
        blue_theme=blue_theme,
        purple_theme=purple_theme,
        layout=layout,
        weeks=weeks,
    )

    # Bike path render.
    # This assumes path_policy_blue/path_policy_red also use the same calendar layout.
    blue_path, active_indices = path_policy_blue(
        month_days=month_days,
        layout=layout,
        weeks=weeks,
    )

    red_path = path_policy_red(
        month_days=month_days,
        layout=layout,
        weeks=weeks,
    )

    svg = f"""<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="TRON light bikes contribution graph">
  {defs_block(red_theme, blue_theme, purple_theme)}
  {style_block()}

  {background_box(red_theme)}

  {contribution_box(red_theme)}
  
  <g id="calendarLabels">
    {week_labels(num_weeks, layout, purple_theme)}
    {weekday_labels(layout, purple_theme)}
  </g>

  <g id="contributionGrid">
    {grid_svg}
  </g>
  <g id="currentDateFlash">
    {current_date_flash(selected_year, selected_month, layout, weeks, blue_theme)}
  </g>
  {year_box(years, selected_year, red_theme, blue_theme)}
  {month_box(available_months, selected_month, red_theme, blue_theme, purple_theme)}
  {spectrum_box(red_theme)}



  <g id="bikeLayers">
    {bike_layers(blue_path, red_path, blue_theme, red_theme)}
  </g>
</svg>
"""

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(svg, encoding="utf-8")

    STATE_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_OUT_PATH.write_text(json.dumps(grid_state, indent=2), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")
    print(f"Wrote {STATE_OUT_PATH}")


if __name__ == "__main__":
    main()
