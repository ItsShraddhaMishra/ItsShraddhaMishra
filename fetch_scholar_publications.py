from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scholarly import scholarly


SCHOLAR_USER_ID = "O5pkUdUAAAAJ"
OUT = Path("data")
OUT.mkdir(exist_ok=True)

OUT_FILE = OUT / "scholar_publications.json"


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def fetch_publications() -> dict[str, Any]:
    author = scholarly.search_author_id(SCHOLAR_USER_ID)
    author = scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])

    publications = []

    for pub in author.get("publications", []):
        filled = scholarly.fill(pub)
        bib = filled.get("bib", {})

        title = bib.get("title", "Untitled")
        year = safe_int(bib.get("pub_year"), 0)
        citations = safe_int(filled.get("num_citations"), 0)

        # Google Scholar's cluster URL is often the most stable fallback.
        pub_url = filled.get("pub_url") or filled.get("eprint_url") or ""
        if not pub_url and filled.get("author_pub_id"):
            pub_url = f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={SCHOLAR_USER_ID}&citation_for_view={filled['author_pub_id']}"

        publications.append(
            {
                "title": title,
                "year": year,
                "citations": citations,
                "url": pub_url,
            }
        )

    publications.sort(key=lambda p: (p["year"], p["citations"], p["title"]), reverse=True)

    cites_per_year = author.get("cites_per_year", {})
    cites_per_year = {
        str(year): safe_int(count)
        for year, count in sorted(cites_per_year.items(), key=lambda kv: int(kv[0]))
    }

    return {
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scholar_url": f"https://scholar.google.com/citations?user={SCHOLAR_USER_ID}&hl=en",
        "name": author.get("name", "Shraddha Mishra"),
        "total_citations": safe_int(author.get("citedby"), 0),
        "h_index": safe_int(author.get("hindex"), 0),
        "i10_index": safe_int(author.get("i10index"), 0),
        "cites_per_year": cites_per_year,
        "publications": publications,
    }


def main() -> None:
    data = fetch_publications()
    OUT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK  {OUT_FILE}")
    print(f"Publications: {len(data['publications'])}")
    print(f"Total citations: {data['total_citations']}")


if __name__ == "__main__":
    main()
