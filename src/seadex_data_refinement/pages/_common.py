from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from pyanilist import Media
from seadex import EntryRecord


@dataclass(frozen=True, slots=True)
class Row:
    seadex_url: str
    anilist_url: str
    title: str
    year: str
    updated_at: str


def assemble_rows(
    kept: list[EntryRecord],
    anilist_map: dict[int, Media],
    sort_by: Literal["popularity", "updated_at"] = "popularity",
) -> list[Row]:
    if sort_by == "popularity":
        kept = sorted(
            kept,
            key=lambda e: (anilist_map[e.anilist_id].popularity if e.anilist_id in anilist_map else None) or 0,
            reverse=True,
        )
    else:
        kept = sorted(kept, key=lambda e: e.updated_at or datetime.min, reverse=True)

    rows: list[Row] = []
    for entry in kept:
        media = anilist_map.get(entry.anilist_id)
        title = media.title.to_str() if media else "Unknown"
        year = str(media.start_date.year) if media and media.start_date and media.start_date.year else "-"
        updated = entry.updated_at.strftime("%d %b %Y") if entry.updated_at else "-"
        rows.append(
            Row(
                seadex_url=entry.url,
                anilist_url=f"https://anilist.co/anime/{entry.anilist_id}",
                title=title,
                year=year,
                updated_at=updated,
            )
        )
    return rows


__all__ = ["Row", "assemble_rows"]
