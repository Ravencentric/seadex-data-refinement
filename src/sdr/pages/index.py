from datetime import datetime

from seadex import TorrentRecord

from sdr.history import Export, History
from sdr.pages import Page
from sdr.snapshot import Snapshot


def prepare(snapshot: Snapshot, history: History[dict[str, int]]) -> datetime:
    return snapshot.captured


def export(snapshot: Snapshot) -> dict[str, int]:
    torrents: set[TorrentRecord] = set()
    for anime in snapshot.entries.values():
        torrents.update(anime.seadex.torrents)
    groups = {torrent.release_group for torrent in torrents}
    return {"entries": len(snapshot.entries), "torrents": len(torrents), "groups": len(groups)}


def create() -> Page[datetime, dict[str, int]]:
    return Page(title="Home", prepare=prepare, export=Export(type=dict[str, int], collect=export))
