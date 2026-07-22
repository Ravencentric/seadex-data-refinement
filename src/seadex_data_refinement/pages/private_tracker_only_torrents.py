from __future__ import annotations

from pathlib import Path

from ..models import EnrichedEntry
from ..render import render_page
from ._common import assemble_rows

_EXCLUSIVE_GROUPS: frozenset[str] = frozenset({"-ZR-", "FraMeSToR", "NAN0", "KEKKU", "Doc", "Kitsune"})


def build(out: Path, entries: tuple[EnrichedEntry, ...]) -> None:
    kept: list[EnrichedEntry] = []
    for entry in entries:
        for torrent in entry.seadex.torrents:
            if not torrent.tracker.is_private() or torrent.release_group in _EXCLUSIVE_GROUPS:
                continue

            mirrored_publicly = any(
                t.tracker.is_public() and t.is_best == torrent.is_best and t.is_dual_audio >= torrent.is_dual_audio
                for t in entry.seadex.torrents
            )

            has_counterpart = any(
                t.release_group == torrent.release_group and t.is_best != torrent.is_best for t in entry.seadex.torrents
            )

            if mirrored_publicly or has_counterpart:
                continue

            kept.append(entry)
            break
    rows = assemble_rows(kept, sort_by="popularity")
    render_page(Path(__file__), out / "private-tracker-only-torrents.md", rows=rows)
