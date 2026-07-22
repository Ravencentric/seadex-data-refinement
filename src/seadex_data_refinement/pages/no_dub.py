from __future__ import annotations

from pathlib import Path

from .. import anilist
from ..models import EnrichedEntry
from ..render import render_page
from ._common import assemble_rows


def build(out: Path, entries: tuple[EnrichedEntry, ...]) -> None:
    dubbed = anilist.dubbed_ids({e.seadex.anilist_id for e in entries})
    kept = [
        e for e in entries if not any(t.is_dual_audio for t in e.seadex.torrents) and e.seadex.anilist_id not in dubbed
    ]
    rows = assemble_rows(kept, sort_by="popularity")
    render_page(Path(__file__), out / "no-dub.md", rows=rows)
