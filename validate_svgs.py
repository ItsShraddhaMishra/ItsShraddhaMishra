from pathlib import Path
import xml.etree.ElementTree as ET

ok = True

for svg in sorted(Path("assets").glob("*.svg")):
    try:
        ET.parse(svg)
        print(f"OK  {svg}")
    except Exception as e:
        print(f"BAD {svg}: {e}")
        ok = False

if not ok:
    raise SystemExit("SVG validation failed.")
