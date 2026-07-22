from __future__ import annotations

from pathlib import Path

import seadex

from ..models import EnrichedEntry
from ..render import render_page
from ._common import assemble_rows


def build(out: Path, entries: tuple[EnrichedEntry, ...]) -> None:
    kept: list[EnrichedEntry] = []
    for entry in entries:
        for torrent in entry.seadex.torrents:
            if torrent.tracker.is_public() and torrent.tracker is not seadex.Tracker.NYAA:
                kept.append(entry)
                break
    rows = assemble_rows(kept, sort_by="popularity")
    render_page(Path(__file__), out / "public-non-nyaa.md", rows=rows)
