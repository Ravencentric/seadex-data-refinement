from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from seadex import TorrentRecord

from .models import EnrichedEntry


@dataclass(frozen=True, slots=True)
class LeaderRow:
    rank: int
    groups: tuple[str, ...]
    count: int


@dataclass(frozen=True, slots=True)
class LeaderBucket:
    label: str
    rows: tuple[LeaderRow, ...]


@dataclass(frozen=True, slots=True)
class SizeStats:
    total: int
    best: int
    alt: int
    realistic: int
    groups: tuple[GroupSizeRow, ...]


@dataclass(frozen=True, slots=True)
class GroupSizeRow:
    rank: int
    name: str
    total_size: int
    best_size: int
    total_entries: int


def leaderboards(entries: tuple[EnrichedEntry, ...]) -> tuple[LeaderBucket, ...]:
    return (
        _leaderboard_bucket("Total entries", entries, _count_total),
        _leaderboard_bucket("Best dual audio entries", entries, _count_best_dual),
        _leaderboard_bucket("Best entries", entries, _count_best),
        _leaderboard_bucket("Alt entries", entries, _count_alt),
    )


def _leaderboard_bucket(
    label: str,
    entries: tuple[EnrichedEntry, ...],
    counter: Callable[[EnrichedEntry], set[str]],
) -> LeaderBucket:
    counts: dict[str, int] = defaultdict(int)
    for entry in entries:
        for group in counter(entry):
            counts[group] += 1

    grouped: dict[int, list[str]] = defaultdict(list)
    for name, count in counts.items():
        grouped[count].append(name)
    sorted_dict = {k: sorted(grouped[k]) for k in sorted(grouped, reverse=True)}

    rows = tuple(
        LeaderRow(rank=rank, groups=tuple(names), count=count)
        for rank, (count, names) in enumerate(sorted_dict.items(), start=1)
    )
    return LeaderBucket(label=label, rows=rows)


def _count_total(entry: EnrichedEntry) -> set[str]:
    return {t.release_group for t in entry.seadex.torrents}


def _count_best_dual(entry: EnrichedEntry) -> set[str]:
    return {t.release_group for t in entry.seadex.torrents if t.is_best and t.is_dual_audio}


def _count_best(entry: EnrichedEntry) -> set[str]:
    return {t.release_group for t in entry.seadex.torrents if t.is_best}


def _count_alt(entry: EnrichedEntry) -> set[str]:
    return {t.release_group for t in entry.seadex.torrents if not t.is_best}


def size_stats(entries: tuple[EnrichedEntry, ...]) -> SizeStats:
    filtered = _filter_torrents(entries)
    total = sum(t.size for t in filtered)
    best = sum(t.size for t in filtered if t.is_best)
    alt = total - best
    realistic = _realistic_size(entries)
    return SizeStats(
        total=total,
        best=best,
        alt=alt,
        realistic=realistic,
        groups=_by_group(entries, filtered),
    )


def _filter_torrents(entries: tuple[EnrichedEntry, ...]) -> tuple[TorrentRecord, ...]:
    trs: set[TorrentRecord] = set()
    for entry in entries:
        groups = {t.release_group for t in entry.seadex.torrents}
        for group in groups:
            filtered = [t for t in entry.seadex.torrents if t.release_group == group and t.tracker.is_private()] or [
                t for t in entry.seadex.torrents if t.release_group == group
            ]
            trs.update(filtered)
    return tuple(trs)


def _realistic_size(entries: tuple[EnrichedEntry, ...]) -> int:
    torrents: set[TorrentRecord] = set()
    for entry in entries:
        filtered = (
            [t for t in entry.seadex.torrents if t.is_best and t.is_dual_audio and t.tracker.is_private()]
            or [t for t in entry.seadex.torrents if t.is_best and t.is_dual_audio]
            or [t for t in entry.seadex.torrents if t.is_best and t.tracker.is_private()]
            or [t for t in entry.seadex.torrents if t.is_best]
            or list(entry.seadex.torrents)
        )
        for torrent in filtered:
            torrents.add(torrent)
            break
    return sum(t.size for t in torrents)


def _by_group(entries: tuple[EnrichedEntry, ...], filtered: Iterable[TorrentRecord]) -> tuple[GroupSizeRow, ...]:
    data: dict[str, dict[str, int]] = defaultdict(lambda: {"total_size": 0, "best_size": 0, "total_entries": 0})

    for entry in entries:
        best_groups = list({t.release_group for t in entry.seadex.torrents if t.is_best})
        alt_groups = list({t.release_group for t in entry.seadex.torrents if not t.is_best})
        for group in best_groups + alt_groups:
            data[group]["total_entries"] += 1

    for torrent in filtered:
        name = torrent.release_group.strip()
        data[name]["total_size"] += torrent.size
        if torrent.is_best:
            data[name]["best_size"] += torrent.size

    sorted_data = sorted(data.items(), key=lambda x: x[1]["total_size"], reverse=True)
    top_entries = sorted_data[:49]
    other_entries = sorted_data[49:]

    others = {
        "total_size": sum(stats["total_size"] for _, stats in other_entries),
        "best_size": sum(stats["best_size"] for _, stats in other_entries),
        "total_entries": sum(stats["total_entries"] for _, stats in other_entries),
    }
    top_entries.append(("Others", others))

    return tuple(
        GroupSizeRow(
            rank=rank,
            name=name,
            total_size=stats["total_size"],
            best_size=stats["best_size"],
            total_entries=stats["total_entries"],
        )
        for rank, (name, stats) in enumerate(top_entries, start=1)
    )


__all__ = [
    "GroupSizeRow",
    "LeaderBucket",
    "LeaderRow",
    "SizeStats",
    "leaderboards",
    "size_stats",
]
