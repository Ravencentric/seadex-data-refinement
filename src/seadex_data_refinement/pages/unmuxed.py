from __future__ import annotations

from pathlib import Path

from ..models import EnrichedEntry
from ..render import render_page
from ._common import assemble_rows


def build(out: Path, entries: tuple[EnrichedEntry, ...]) -> None:
    kept = [e for e in entries if e.seadex.theoretical_best is not None]
    rows = assemble_rows(kept, sort_by="popularity")
    render_page(Path(__file__), out / "unmuxed.md", rows=rows)
