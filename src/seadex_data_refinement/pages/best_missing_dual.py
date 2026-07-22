from __future__ import annotations

from pathlib import Path

from pyanilist import Media
from seadex import EntryRecord

from ..render import render_page
from ._common import assemble_rows


def build(out: Path, snapshot: tuple[EntryRecord, ...], anilist_map: dict[int, Media]) -> None:
    kept: list[EntryRecord] = []
    for entry in snapshot:
        alt_has_dual = any(t for t in entry.torrents if not t.is_best and t.is_dual_audio)
        best_has_dual = any(t for t in entry.torrents if t.is_best and t.is_dual_audio)
        has_best = any(t for t in entry.torrents if t.is_best)
        if alt_has_dual and not best_has_dual and has_best:
            kept.append(entry)
    rows = assemble_rows(kept, anilist_map, sort_by="popularity")
    render_page(Path(__file__), out / "best-missing-dual.md", rows=rows)
