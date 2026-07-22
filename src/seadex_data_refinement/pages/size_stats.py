from __future__ import annotations

from pathlib import Path

from .. import analytics
from ..models import EnrichedEntry
from ..render import render_page


def build(out: Path, entries: tuple[EnrichedEntry, ...]) -> None:
    stats = analytics.size_stats(entries)
    render_page(Path(__file__), out / "size-statistics.md", stats=stats)
