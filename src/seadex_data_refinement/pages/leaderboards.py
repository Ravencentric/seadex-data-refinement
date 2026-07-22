from __future__ import annotations

from pathlib import Path

from .. import analytics
from ..models import EnrichedEntry
from ..render import render_page


def build(out: Path, entries: tuple[EnrichedEntry, ...]) -> None:
    buckets = analytics.leaderboards(entries)
    render_page(Path(__file__), out / "leaderboards.md", buckets=buckets)
