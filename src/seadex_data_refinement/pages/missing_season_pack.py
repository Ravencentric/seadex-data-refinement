from __future__ import annotations

from pathlib import Path

from ..models import EnrichedEntry
from ..render import render_page
from ._common import assemble_rows


def build(out: Path, entries: tuple[EnrichedEntry, ...]) -> None:
    kept = [e for e in entries if any(t.grouped_url is not None for t in e.seadex.torrents)]
    rows = assemble_rows(kept, sort_by="popularity")
    render_page(Path(__file__), out / "missing-season-pack.md", rows=rows)
