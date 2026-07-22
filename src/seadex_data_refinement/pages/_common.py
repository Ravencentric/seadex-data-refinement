from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from ..models import EnrichedEntry


@dataclass(frozen=True, slots=True)
class Row:
    seadex_url: str
    anilist_url: str
    title: str
    year: str
    updated_at: str


def assemble_rows(
    kept: list[EnrichedEntry],
    sort_by: Literal["popularity", "updated_at"] = "popularity",
) -> list[Row]:
    if sort_by == "popularity":
        kept = sorted(kept, key=lambda e: e.anilist.popularity or 0, reverse=True)
    else:
        kept = sorted(kept, key=lambda e: e.seadex.updated_at or datetime.min, reverse=True)

    rows: list[Row] = []
    for entry in kept:
        media = entry.anilist
        title = media.title.to_str()
        year = str(media.start_date.year) if media.start_date and media.start_date.year else "-"
        updated = entry.seadex.updated_at.strftime("%d %b %Y") if entry.seadex.updated_at else "-"
        rows.append(
            Row(
                seadex_url=entry.seadex.url,
                anilist_url=f"https://anilist.co/anime/{entry.seadex.anilist_id}",
                title=title,
                year=year,
                updated_at=updated,
            )
        )
    return rows


__all__ = ["Row", "assemble_rows"]
