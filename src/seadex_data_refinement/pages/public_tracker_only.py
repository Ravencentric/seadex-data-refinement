from __future__ import annotations

import datetime as dt
from pathlib import Path

import seadex
from pyanilist import Media
from seadex import EntryRecord

from ..render import render_page
from ._common import assemble_rows

_AB_RULE_CUTOFF: dt.datetime = dt.datetime(2026, 6, 27, tzinfo=dt.UTC)


def build(out: Path, snapshot: tuple[EntryRecord, ...], anilist_map: dict[int, Media]) -> None:
    kept: list[EntryRecord] = []
    for entry in snapshot:
        if entry.updated_at < _AB_RULE_CUTOFF:
            continue
        for torrent in entry.torrents:
            if not torrent.tracker.is_public() or seadex.Tag.INCOMPLETE in torrent.tags:
                continue
            release_group = torrent.release_group.casefold().strip()
            has_private_counterpart = any(
                t.tracker.is_private() for t in entry.torrents if t.release_group.casefold().strip() == release_group
            )
            if not has_private_counterpart:
                kept.append(entry)
                break
    rows = assemble_rows(kept, anilist_map, sort_by="updated_at")
    render_page(Path(__file__), out / "public-tracker-only.md", rows=rows)
