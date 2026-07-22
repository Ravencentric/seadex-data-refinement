from __future__ import annotations

from pathlib import Path

from ..models import EnrichedEntry
from ..render import render_page
from ._common import assemble_rows


def build(out: Path, entries: tuple[EnrichedEntry, ...]) -> None:
    kept = [e for e in entries if not any(comp.startswith("https://slow.pics") for comp in e.seadex.comparisons)]
    rows = assemble_rows(kept, sort_by="popularity")
    render_page(Path(__file__), out / "no-comparisons.md", rows=rows)
