from collections import Counter, defaultdict
from collections.abc import Mapping
from dataclasses import dataclass

from sdr.history import Export, History
from sdr.pages import Page
from sdr.snapshot import Snapshot


@dataclass(frozen=True, slots=True, kw_only=True)
class Row:
    count: int
    groups: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "groups", tuple(sorted(self.groups)))

    @property
    def label(self) -> str:
        amount = 5 if len(self.groups) <= 5 else 4
        joined = " / ".join(self.groups[:amount])
        if amount == 4:
            joined += " & Others"
        return joined


@dataclass(frozen=True, slots=True, kw_only=True)
class Board:
    title: str
    rows: tuple[Row, ...]


def rank(title: str, counts: Mapping[str, int]) -> Board:
    """Group equal counts into one rank, with names sorted alphabetically."""
    # Example: title = "Top 25", counts = Counter({"sam": 128, "CRUCiBLE": 128, "-ZR-": 148})

    # grouped = { 128: ["sam", "CRUCiBLE"], 148: ["-ZR-"] }
    grouped: defaultdict[int, list[str]] = defaultdict(list)
    for group, count in counts.items():
        grouped[count].append(group)

    # distinct = [128, 148, ...] -> Arbitrary length
    distinct = grouped.keys()
    # ordered = [148, 128] -> Upto 25 items
    ordered = sorted(distinct, reverse=True)[:25]
    rows: list[Row] = []

    for count in ordered:
        # grouped[148] == ["-ZR-"]
        # grouped[128] == ["sam", "CRUCiBLE"]
        groups = tuple(grouped[count])
        rows.append(Row(count=count, groups=groups))

    # Board(title=title, rows=(
    #     Row(count=148, groups=("-ZR-",)),
    #     Row(count=128, groups=("CRUCiBLE", "sam")),
    # ))
    return Board(title=title, rows=tuple(rows))


def export(snapshot: Snapshot) -> dict[str, dict[str, int]]:
    """A callable that's supposed to produce page data suitable for serialization."""
    total: Counter[str] = Counter()
    dual: Counter[str] = Counter()
    best: Counter[str] = Counter()
    alt: Counter[str] = Counter()
    for anime in snapshot.entries.values():
        torrents = anime.seadex.torrents
        total.update({torrent.release_group for torrent in torrents})
        dual.update({torrent.release_group for torrent in torrents if torrent.is_best and torrent.is_dual_audio})
        best.update({torrent.release_group for torrent in torrents if torrent.is_best})
        alt.update({torrent.release_group for torrent in torrents if not torrent.is_best})
    return {"total": dict(total), "dual": dict(dual), "best": dict(best), "alt": dict(alt)}


def prepare(snapshot: Snapshot, _: History[dict[str, dict[str, int]]]) -> tuple[Board, ...]:
    """Rank each group once per anime within each leaderboard category."""
    counts = export(snapshot)
    return (
        rank("Total Entries", counts["total"]),
        rank("Best Dual-Audio Entries", counts["dual"]),
        rank("Best Entries", counts["best"]),
        rank("Alt Entries", counts["alt"]),
    )


def create() -> Page[tuple[Board, ...], dict[str, dict[str, int]]]:
    return Page(title="Leaderboards", prepare=prepare, export=Export(type=dict[str, dict[str, int]], collect=export))
