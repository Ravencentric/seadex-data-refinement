from collections import Counter
from dataclasses import dataclass, replace
from datetime import timedelta

import msgspec
from seadex import TorrentRecord

from sdr.history import Export, History
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
    alt: int
    realistic: int
    rows: tuple[Row, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class GrowthPerDay:
    total: float
    best: float
    alt: float
    realistic: float


@dataclass(frozen=True, slots=True, kw_only=True)
class Timeline:
    """The ranked report and complete history used for the chart and growth rates."""

    current: Report
    history: History[Report]

    def to_uplot(self) -> str:
        """
        Serialize history for the data argument of new uPlot(options, data, container).

        The Python equivalent will probably look something like this:

            def uplot(
                options: Options,
                data: tuple[list[float], list[float], list[float], list[float], list[float]],
                container: HTMLElement,
            ) -> UPlot: ...

        The five aligned columns are [timestamps, total, best, alt, realistic].
        Each column has one value per observation, ordered by capture time.
        Timestamps are Unix seconds. We convert sizes to TiB here to keep
        the JavaScript focused on rendering.

        Lastly, convert the whole thing to JSON so we can feed it to JS over the boundary.
        """
        times = [observation.captured.timestamp() for observation in self.history]
        total = [observation.data.total / 1024**4 for observation in self.history]
        best = [observation.data.best / 1024**4 for observation in self.history]
        alt = [observation.data.alt / 1024**4 for observation in self.history]
        realistic = [observation.data.realistic / 1024**4 for observation in self.history]
        return msgspec.json.encode((times, total, best, alt, realistic)).decode()

    @property
    def growth(self) -> GrowthPerDay:
        """Average daily net growth for each size measure across the complete history."""
        # Arbitrary number for sanity check
        assert len(self.history) > 100, "Expected more than 100 size observations"
        first = self.history[0]
        last = self.history[-1]
        days = (last.captured - first.captured) / timedelta(days=1)
        return GrowthPerDay(
            total=(last.data.total - first.data.total) / days,
            best=(last.data.best - first.data.best) / days,
            alt=(last.data.alt - first.data.alt) / days,
            realistic=(last.data.realistic - first.data.realistic) / days,
        )


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


def export(snapshot: Snapshot) -> Report:
    """A callable that's supposed to produce page data suitable for serialization."""
    groups = tuple(sorted(measure(snapshot), key=lambda row: row.name))
    total = sum(group.total for group in groups)
    best = sum(group.best for group in groups)
    return Report(total=total, best=best, alt=total - best, realistic=realistic(snapshot), rows=groups)


def prepare(snapshot: Snapshot, history: History[Report]) -> Timeline:
    """Rank the current report and use saved observations as supplied."""
    report = export(snapshot)
    return Timeline(current=replace(report, rows=rank(report.rows)), history=history)


def create() -> Page[Timeline, Report]:
    return Page(title="Size Statistics", prepare=prepare, export=Export(type=Report, collect=export))
