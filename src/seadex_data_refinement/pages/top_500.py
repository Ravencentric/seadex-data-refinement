from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .. import anilist, fetch
from ..models import EnrichedEntry
from ..render import render_page

_TOP_MISSING_COUNT = 100


@dataclass(frozen=True, slots=True)
class MissingRow:
    seadex_url: str
    anilist_url: str
    title: str
    year: str


def build(out: Path, entries: tuple[EnrichedEntry, ...]) -> None:
    seadex_ids = fetch.seadex_anilist_ids()
    top_media = anilist.top_missing(seadex_ids, _TOP_MISSING_COUNT)
    rows = tuple(
        MissingRow(
            seadex_url=f"https://releases.moe/{media.id}/",
            anilist_url=f"https://anilist.co/anime/{media.id}",
            title=media.title.to_str(),
            year=str(media.start_date.year) if media.start_date and media.start_date.year else "-",
        )
        for media in sorted(top_media, key=lambda m: m.popularity or 0, reverse=True)
    )
    render_page(Path(__file__), out / "top-500.md", rows=rows)
