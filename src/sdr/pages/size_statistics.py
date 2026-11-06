from collections import Counter
from dataclasses import dataclass

from seadex import TorrentRecord

from sdr.pages import Page
from sdr.snapshot import Snapshot


@dataclass(frozen=True, slots=True, kw_only=True)
class Row:
    name: str
    total: int
    best: int
    count: int

    @property
    def percentage(self) -> float | None:
        return self.best / self.total * 100 if self.total else None

    @property
    def average(self) -> float:
        return self.total / self.count


@dataclass(frozen=True, slots=True, kw_only=True)
class Report:
    total: int
    best: int
    realistic: int
    rows: tuple[Row, ...]

    @property
    def alt(self) -> int:
        return self.total - self.best


def select(snapshot: Snapshot) -> frozenset[TorrentRecord]:
    """Prefer private torrents per entry and group, discarding exact duplicate records."""
    selected: set[TorrentRecord] = set()
    for anime in snapshot.entries.values():
        torrents = anime.seadex.torrents
        private = {torrent.release_group for torrent in torrents if torrent.tracker.is_private()}
        # For every group in an entry with both private and public releases,
        # only consider private releases. Otherwise, keep the public releases.
        selected.update(
            torrent for torrent in torrents if torrent.tracker.is_private() or torrent.release_group not in private
        )
    return frozenset(selected)


def realistic(snapshot: Snapshot) -> int:
    """Estimate downloading one preferred release per anime, counting shared records once."""
    selected: set[TorrentRecord] = set()
    for anime in snapshot.entries.values():
        torrents = anime.seadex.torrents
        preferred = (
            # 1. Best release with dual audio from a private tracker.
            [
                torrent
                for torrent in torrents
                if torrent.is_best and torrent.is_dual_audio and torrent.tracker.is_private()
            ]
            # 2. Best release with dual audio from any tracker.
            or [torrent for torrent in torrents if torrent.is_best and torrent.is_dual_audio]
            # 3. Best release from a private tracker.
            or [torrent for torrent in torrents if torrent.is_best and torrent.tracker.is_private()]
            # 4. Best release from any tracker.
            or [torrent for torrent in torrents if torrent.is_best]
            # 5. Any available release.
            or torrents
        )
        # Preserve source order when several torrents meet the same preference.
        for torrent in preferred:
            selected.add(torrent)
            break
    return sum(file.size for torrent in selected for file in torrent.files)


def count(snapshot: Snapshot) -> Counter[str]:
    """Count each group once per anime and Best/Alt status."""
    counts: Counter[str] = Counter()
    for anime in snapshot.entries.values():
        # Count entries rather than torrents: SubsPlease may have 12 single-episode
        # torrents for one anime. That still counts as one Alt entry for the group.
        # Each exact group name counts at most twice per anime: once per Best/Alt status.
        best: set[str] = set()
        alt: set[str] = set()
        for torrent in anime.seadex.torrents:
            if torrent.is_best:
                best.add(torrent.release_group)
            else:
                alt.add(torrent.release_group)

        counts.update(best)
        counts.update(alt)
    return counts


def measure(snapshot: Snapshot) -> tuple[Row, ...]:
    """Calculate total bytes, Best bytes, and entry counts for every group."""
    counts = count(snapshot)
    totals: Counter[str] = Counter()
    best: Counter[str] = Counter()
    # Sizes count every retained torrent, so 12 single-episode torrents contribute
    # the same bytes as one batch containing those same files.
    for torrent in select(snapshot):
        size = sum(file.size for file in torrent.files)
        totals[torrent.release_group] += size
        if torrent.is_best:
            best[torrent.release_group] += size

    return tuple(Row(name=name, total=totals[name], best=best[name], count=count) for name, count in counts.items())


def rank(groups: tuple[Row, ...]) -> tuple[Row, ...]:
    """Keep the largest 49 groups and combine the rest as Others."""
    rows = sorted(groups, key=lambda row: row.name)
    # Sorting by size preserves alphabetical order for equal totals.
    rows.sort(key=lambda row: row.total, reverse=True)
    if len(rows) > 49:
        others = rows[49:]
        rows = rows[:49]
        rows.append(
            Row(
                name="Others",
                total=sum(row.total for row in others),
                best=sum(row.best for row in others),
                count=sum(row.count for row in others),
            )
        )

    return tuple(rows)


def prepare(snapshot: Snapshot) -> Report:
    """Assemble the overall totals, download estimate, and ranked group breakdown."""
    groups = measure(snapshot)
    return Report(
        total=sum(group.total for group in groups),
        best=sum(group.best for group in groups),
        realistic=realistic(snapshot),
        rows=rank(groups),
    )


def create() -> Page[Report]:
    return Page(title="Size Statistics", prepare=prepare)
