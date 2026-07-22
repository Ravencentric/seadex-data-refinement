from __future__ import annotations

from pathlib import Path

from ..models import EnrichedEntry
from ..render import render_page
from ._common import assemble_rows


def build(out: Path, entries: tuple[EnrichedEntry, ...]) -> None:
    kept: list[EnrichedEntry] = []
    for entry in entries:
        alt_has_dual = any(t for t in entry.seadex.torrents if not t.is_best and t.is_dual_audio)
        best_has_dual = any(t for t in entry.seadex.torrents if t.is_best and t.is_dual_audio)
        has_best = any(t for t in entry.seadex.torrents if t.is_best)
        if alt_has_dual and not best_has_dual and has_best:
            kept.append(entry)
    rows = assemble_rows(kept, sort_by="popularity")
    render_page(Path(__file__), out / "best-missing-dual.md", rows=rows)
