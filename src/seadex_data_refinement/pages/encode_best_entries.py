from __future__ import annotations

import re
from pathlib import Path

from ..models import EnrichedEntry
from ..render import render_page
from ._common import assemble_rows


def build(out: Path, entries: tuple[EnrichedEntry, ...]) -> None:
    kept: list[EnrichedEntry] = []
    for entry in entries:
        notes = entry.seadex.notes.casefold()
        if notes:
            if "remux" in notes:
                continue
            if re.search(r"web[-\s]?DL", notes.splitlines()[0], re.IGNORECASE):
                continue
        if entry.seadex.is_incomplete:
            continue
        comparisons = [comp for comp in entry.seadex.comparisons if "slow" in comp]
        if not comparisons:
            continue
        if not any(torrent.is_best for torrent in entry.seadex.torrents):
            continue
        kept.append(entry)
    rows = assemble_rows(kept, sort_by="popularity")
    render_page(Path(__file__), out / "encode-best-entries.md", rows=rows)
