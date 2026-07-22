from __future__ import annotations

from pathlib import Path

from pyanilist import Media
from seadex import EntryRecord

from .. import anilist
from ..render import render_page
from ._common import assemble_rows


def build(out: Path, snapshot: tuple[EntryRecord, ...], anilist_map: dict[int, Media]) -> None:
    dubbed = anilist.dubbed_ids({e.anilist_id for e in snapshot})
    kept = [e for e in snapshot if not any(t.is_dual_audio for t in e.torrents) and e.anilist_id not in dubbed]
    rows = assemble_rows(kept, anilist_map, sort_by="popularity")
    render_page(Path(__file__), out / "no-dub.md", rows=rows)
