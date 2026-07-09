#!/usr/bin/env python3
"""
svg_crusader.py

Central sanitizer for SVG/Python corruption caused by formatters/extensions
rewriting SVG className="..." strings into broken className=... fragments.

This script repairs known corruption patterns in generator source files and
generated SVG assets, then fails loudly if dangerous patterns remain.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable


ROOT = Path(".")
ASSET_DIR = ROOT / "assets"

TRON_SOURCE = ROOT / "make_tron_contributions.py"

SOURCE_FILES = [
    ROOT / "make_readme_assets.py",
    ROOT / "make_identity_panel.py",
    ROOT / "make_system_status_panel.py",
    ROOT / "make_current_mission_panel.py",
    ROOT / "make_tech_stack_panel.py",
    ROOT / "make_featured_projects_panel.py",
    ROOT / "make_publication_panel.py",
    ROOT / "make_tron_contributions.py",
    ROOT / "ares_tron_theme.py",
]

DANGEROUS_PATTERNS = [
    re.compile(r"className\s*="),
    re.compile(r"className=il\s+trai"),
    re.compile(r"className=e-he"),
    re.compile(r"\bclass\s*=\s*(nnn|hhh|eee|eIn[0-9]?|tFloat)(\s|>|$)"),
    re.compile(r"BROKEN_CLASSNAME"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def changed(path: Path, old: str, new: str) -> bool:
    if old != new:
        write_text(path, new)
        return True
    return False


def repair_common_text(text: str) -> str:
    """
    Repair corruption patterns that are safe across Python generator strings
    and generated SVG text.
    """

    replacements = {
        # TRON bike/trail corruption.
        '<g className=il trai>':
            '<g className=il trai>',
        '<g id="{color_name}TrailLine" className=il trai>':
            '<g id="{color_name}TrailLine" className=il trai>',
        '<g id="blueTrailLine" className=il trai>':
            '<g id="blueTrailLine" className=il trai>',
        '<g id="redTrailLine" className=il trai>':
            '<g id="redTrailLine" className=il trai>',
        '<g className=e-he>':
            '<g className=e-he>',

        # Generic known className corruption.
        'className=railPulse': 'className=lass="railPul',
        'className=trailPulse': 'className=iii',
        'className=eatFlash': 'className=FFF',
        'className=lineFlow': 'className=eee',
        'className=panelPulse': 'className=elPulse',
        'className=softFloat': 'className=tFloat',
        'className=fadeIn1': 'className=eee',
        'className=fadeIn2': 'className=eee',
        'className=fadeIn3': 'className=eee',
        'className=fadeIn4': 'className=eee',
        'className=edge': 'className=edge',
        'className=scan': 'className=nnn',
        'className=dash': 'className=hhh',
        'className=pulse': 'className=ss="puls',
    }

    for bad, good in replacements.items():
        text = text.replace(bad, good)

    # Legacy broken fragments.
    class_map = {
        "FFF": "eatFlash",
        "iii": "trailPulse",
        "eee": "lineFlow",
        "elPulse": "panelPulse",
        "tFloat": "softFloat",
    }

    for bad, good in class_map.items():
        text = re.sub(rf"className={re.escape(bad)}\b", f'className=oo', text)

    # Broken class= without quotes in generated SVG/source strings.
    text = re.sub(r'\bclass\s*=\s*nnn\b', 'className=nnn', text)
    text = re.sub(r'\bclass\s*=\s*hhh\b', 'className=hhh', text)
    text = re.sub(r'\bclass\s*=\s*eee\b', 'className=eee', text)
    text = re.sub(r'\bclass\s*=\s*tFloat\b', 'className=tFloat', text)

    return text


def repair_tron_source(text: str) -> str:
    """
    TRON-specific robust repair.

    Also ensures the source uses svg_class(...) helper, so the editor cannot
    rewrite literal className="..." strings inside the two fragile bike/trail lines.
    """

    # Repair current corruption first.
    text = repair_common_text(text)

    # Install svg_class helper if missing.
    if "def svg_class(" not in text:
        helper = '''
def svg_class(value: str) -> str:
    """
    Build an SVG class attribute without writing a literal class attribute in
    fragile source locations.
    """
    return "class" + "=" + chr(34) + value + chr(34)

'''
        marker = "\ndef trail_line("
        if marker in text:
            text = text.replace(marker, "\n" + helper + "def trail_line(", 1)
        else:
            # Safe fallback: put before bike_vehicle if trail_line marker changed.
            text = text.replace("\ndef bike_vehicle(", "\n" + helper + "def bike_vehicle(", 1)

    # Replace the two fragile literal class attributes with computed attributes.
    text = text.replace(
        '<g id="{color_name}TrailLine" className=il trai>',
        '<g id="{color_name}TrailLine" {svg_class(f"trail trail-{color_name}")}>',
    )

    text = text.replace(
        '<g className=e-he>',
        '<g {svg_class("bike-head")}>',
    )

    text = text.replace(
        '<g id="spectrumLegend" className=oo>',
        '<g id="spectrumLegend" {svg_class("lineFlow")}>',
    )

    text = text.replace(
        '<g id="spectrumLegend" class="lineFlow">',
        '<g id="spectrumLegend" {svg_class("lineFlow")}>',
    )

    text = text.replace(
        '<rect className=oo',
        '<rect {svg_class("eatFlash")}',
    )

    text = text.replace(
        '<rect class="eatFlash"',
        '<rect {svg_class("eatFlash")}',
    )

    # If the editor already corrupted the computed lines, repair them too.
    text = text.replace(
        '<g id="{color_name}TrailLine" className=il trai>',
        '<g id="{color_name}TrailLine" {svg_class(f"trail trail-{color_name}")}>',
    )

    text = text.replace(
        '<g className=e-he>',
        '<g {svg_class("bike-head")}>',
    )

    text = text.replace(
        '<g id="spectrumLegend" className=oo>',
        '<g id="spectrumLegend" {svg_class("lineFlow")}>',
    )

    text = text.replace(
        '<g id="spectrumLegend" class="lineFlow">',
        '<g id="spectrumLegend" {svg_class("lineFlow")}>',
    )

    text = text.replace(
        '<rect className=oo',
        '<rect {svg_class("eatFlash")}',
    )

    text = text.replace(
        '<rect class="eatFlash"',
        '<rect {svg_class("eatFlash")}',
    )

    return text


def repair_file(path: Path) -> bool:
    if not path.exists():
        return False

    old = read_text(path)

    if path.name == "make_tron_contributions.py":
        new = repair_tron_source(old)
    else:
        new = repair_common_text(old)

    did_change = changed(path, old, new)
    if did_change:
        print(f"REPAIRED {path}")
    return did_change


def iter_svg_assets() -> Iterable[Path]:
    if not ASSET_DIR.exists():
        return []
    return sorted(ASSET_DIR.glob("*.svg"))


def validate_svg(path: Path) -> bool:
    try:
        ET.parse(path)
        print(f"OK  {path}")
        return True
    except ET.ParseError as exc:
        print(f"BAD {path}: {exc}")
        line, col = exc.position
        lines = read_text(path).splitlines()
        start = max(1, line - 5)
        end = min(len(lines), line + 5)

        for i in range(start, end + 1):
            marker = ">>" if i == line else "  "
            print(f"{marker} {i:5d}: {lines[i - 1]}")
            if i == line:
                print(" " * (10 + col) + "^")

        return False


def has_dangerous_pattern(path: Path) -> bool:
    if not path.exists():
        return False

    text = read_text(path)
    bad = False

    for line_no, line in enumerate(text.splitlines(), start=1):
        # Allow safe helper/code references.
        if "svg_class(" in line:
            continue
        if "do not rewrite it to className" in line:
            continue
        if "literal class attribute" in line or "literal SVG class attribute" in line:
            continue

        for pattern in DANGEROUS_PATTERNS:
            if pattern.search(line):
                print(f"BADPATTERN {path}:{line_no}: {line}")
                bad = True
                break

    return bad


def repair_all() -> int:
    print("SVG Crusader: repairing source files...")
    for path in SOURCE_FILES:
        repair_file(path)

    print("SVG Crusader: repairing generated SVG assets...")
    for path in iter_svg_assets():
        repair_file(path)

    return 0


def check_all() -> int:
    print("SVG Crusader: scanning for dangerous corruption patterns...")

    bad = False

    for path in SOURCE_FILES:
        bad = has_dangerous_pattern(path) or bad

    for path in iter_svg_assets():
        bad = has_dangerous_pattern(path) or bad

    if bad:
        print("SVG Crusader: corruption remains.")
        return 1

    print("SVG Crusader: no dangerous corruption patterns found.")
    return 0


def validate_all() -> int:
    print("SVG Crusader: validating SVG XML...")
    ok = True

    for path in iter_svg_assets():
        ok = validate_svg(path) and ok

    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["repair", "check", "validate", "repair-check", "all"],
    )
    args = parser.parse_args()

    if args.command == "repair":
        return repair_all()

    if args.command == "check":
        return check_all()

    if args.command == "validate":
        return validate_all()

    if args.command == "repair-check":
        repair_all()
        return check_all()

    if args.command == "all":
        repair_all()
        check_status = check_all()
        validate_status = validate_all()
        return check_status or validate_status

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
