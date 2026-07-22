from __future__ import annotations

from pathlib import Path

from pyanilist import Media
from seadex import EntryRecord

from .. import analytics
from ..render import render_page


def build(out: Path, snapshot: tuple[EntryRecord, ...], anilist_map: dict[int, Media]) -> None:
    stats = analytics.size_stats(snapshot)
    render_page(Path(__file__), out / "size-statistics.md", stats=stats)
