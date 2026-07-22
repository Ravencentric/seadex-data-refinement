from __future__ import annotations

from . import (
    alt_missing_dual,
    best_missing_dual,
    broken_entries,
    encode_best_entries,
    leaderboards,
    marked_incomplete,
    missing_season_pack,
    no_comparisons,
    no_dub,
    patch_required,
    private_tracker_only_entries,
    private_tracker_only_torrents,
    public_non_nyaa,
    public_tracker_only,
    size_stats,
    top_500,
    unmuxed,
)

PAGES = (
    unmuxed,
    no_comparisons,
    marked_incomplete,
    public_non_nyaa,
    private_tracker_only_entries,
    private_tracker_only_torrents,
    public_tracker_only,
    best_missing_dual,
    alt_missing_dual,
    no_dub,
    encode_best_entries,
    patch_required,
    broken_entries,
    missing_season_pack,
    top_500,
    leaderboards,
    size_stats,
)

__all__ = ["PAGES"]
