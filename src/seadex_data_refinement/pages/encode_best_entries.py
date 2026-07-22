from __future__ import annotations

import re
from pathlib import Path

from pyanilist import Media
from seadex import EntryRecord

from ..render import render_page
from ._common import assemble_rows


def build(out: Path, snapshot: tuple[EntryRecord, ...], anilist_map: dict[int, Media]) -> None:
    kept: list[EntryRecord] = []
    for entry in snapshot:
        notes = entry.notes.casefold()
        if notes:
            if "remux" in notes:
                continue
            if re.search(r"web[-\s]?DL", notes.splitlines()[0], re.IGNORECASE):
                continue
        if entry.is_incomplete:
            continue
        comparisons = [comp for comp in entry.comparisons if "slow" in comp]
        if not comparisons:
            continue
        if not any(torrent.is_best for torrent in entry.torrents):
            continue
        kept.append(entry)
    rows = assemble_rows(kept, anilist_map, sort_by="popularity")
    render_page(Path(__file__), out / "encode-best-entries.md", rows=rows)
