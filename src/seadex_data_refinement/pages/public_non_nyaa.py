from __future__ import annotations

from pathlib import Path

import seadex
from pyanilist import Media
from seadex import EntryRecord

from ..render import render_page
from ._common import assemble_rows


def build(out: Path, snapshot: tuple[EntryRecord, ...], anilist_map: dict[int, Media]) -> None:
    kept: list[EntryRecord] = []
    for entry in snapshot:
        for torrent in entry.torrents:
            if torrent.tracker.is_public() and torrent.tracker is not seadex.Tracker.NYAA:
                kept.append(entry)
                break
    rows = assemble_rows(kept, anilist_map, sort_by="popularity")
    render_page(Path(__file__), out / "public-non-nyaa.md", rows=rows)
