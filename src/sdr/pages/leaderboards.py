from collections import Counter, defaultdict
from dataclasses import dataclass

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


def rank(title: str, counts: Counter[str]) -> Board:
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


def prepare(snapshot: Snapshot) -> tuple[Board, ...]:
    """Count each group once per anime within each leaderboard category."""
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
    return (
        rank("Total Entries", total),
        rank("Best Dual-Audio Entries", dual),
        rank("Best Entries", best),
        rank("Alt Entries", alt),
    )


def create() -> Page[tuple[Board, ...]]:
    return Page(title="Leaderboards", prepare=prepare)
