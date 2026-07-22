from __future__ import annotations

from pathlib import Path

from pyanilist import Media
from seadex import EntryRecord

from ..render import render_page
from ._common import assemble_rows


def build(out: Path, snapshot: tuple[EntryRecord, ...], anilist_map: dict[int, Media]) -> None:
    kept = [e for e in snapshot if e.is_incomplete]
    rows = assemble_rows(kept, anilist_map, sort_by="popularity")
    render_page(Path(__file__), out / "marked-incomplete.md", rows=rows)
