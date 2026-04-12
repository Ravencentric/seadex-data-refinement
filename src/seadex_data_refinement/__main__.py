from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import Final, Literal, assert_never

import seadex
from cyclopts import App, Group

from .core import EXCLUSIVE_GROUPS, MediaEntryCollection, remove_entries_without_dub
from .leaderboard import SeaDexLeaderboard
from .size import SeaDexSizeCalculator

app = App("SeaDex Data Refinement", help_format="markdown")

# Hide default help/version flags
hidden = Group(show=False)
app["--help"].group = hidden
app["--version"].group = hidden


@app.command
def get_entries(
    criteria: Literal[
        "unmuxed",
        "no-comparisons",
        "marked-incomplete",
        "public-non-nyaa",
        "private-tracker-only-torrents",
        "private-tracker-only-entries",
        "public-tracker-only",
        "best-missing-dual",
        "alt-missing-dual",
        "no-dub",
        "encode-best-entries",
        "patch-required",
        "broken-entries",
        "missing-season-pack",
    ],
    /,
    *,
    outfile: Path | None = None,
    json: bool = False,
) -> None:
    """
    Retrieve SeaDex entries based on the specified criteria.

    Parameters
    ----------
    criteria : Literal[...]
        The criteria to use for retrieving SeaDex entries.
    outfile : Path | None, optional
        Path to write the output to.
    json : bool, optional
        Whether to output results in JSON format.
    """
    entries: dict[int, seadex.EntryRecord] = {}
    header: str | None = None
    sort_by: Literal["popularity", "updated_at"] = "popularity"

    match criteria:
        case "unmuxed":
            header = "# Unmuxed"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    if entry.theoretical_best is not None:
                        entries[entry.anilist_id] = entry

        case "no-comparisons":
            header = "# No comparisons"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    if not any(comp.startswith("https://slow.pics") for comp in entry.comparisons):
                        entries[entry.anilist_id] = entry

        case "marked-incomplete":
            header = "# Marked incomplete"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    if entry.is_incomplete:
                        entries[entry.anilist_id] = entry

        case "public-non-nyaa":
            header = "# Public - non-Nyaa"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    for torrent in entry.torrents:
                        if torrent.tracker.is_public() and torrent.tracker is not seadex.Tracker.NYAA:
                            entries[entry.anilist_id] = entry
                            break

        case "patch-required":
            header = "# Patch required"
            header += "\n\nAn entry appears here if at least one of its releases requires a patch to be applied.\n\n"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    for torrent in entry.torrents:
                        if seadex.Tag.PATCH_REQUIRED in torrent.tags:
                            entries[entry.anilist_id] = entry
                            break

        case "broken-entries":
            header = "# Broken entries"
            header += "\n\nAn entry appears here if at least one of its releases is marked as broken.\n\n"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    for torrent in entry.torrents:
                        if seadex.Tag.BROKEN in torrent.tags:
                            entries[entry.anilist_id] = entry
                            break

        case "private-tracker-only-torrents":
            header = "# Private tracker only torrents\n\n"

            header += "This list excludes groups that do not want their releases mirrored to public trackers.\n\n"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    groups = []
                    for torrent in entry.torrents:
                        if torrent.tracker.is_private() and torrent.release_group not in EXCLUSIVE_GROUPS:
                            release_group = torrent.release_group.casefold().strip()
                            if (release_group + str(torrent.is_best)) in groups:
                                continue
                            if not any(
                                (t.tracker.is_public() and t.is_best == torrent.is_best)
                                or (t.release_group == torrent.release_group and t.is_best != torrent.is_best)
                                for t in entry.torrents
                            ):
                                entries[entry.anilist_id] = entry
                                groups.append(release_group + str(torrent.is_best))
                                continue

        case "private-tracker-only-entries":
            header = "# Private tracker only entries"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    if all(torrent.tracker.is_private() for torrent in entry.torrents):
                        entries[entry.anilist_id] = entry

        case "public-tracker-only":
            header = "# Public tracker only"
            header += "\n\nThis list excludes torrents that have been manually verified to break AB rules.\n\n"
            cutoff_date: Final = dt.datetime(2026, 2, 17, tzinfo=dt.UTC)
            sort_by = "updated_at"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    # Skip entries older than the cutoff date
                    if entry.updated_at < cutoff_date:
                        continue
                    for torrent in entry.torrents:
                        if torrent.tracker.is_public() and seadex.Tag.INCOMPLETE not in torrent.tags:
                            release_group = torrent.release_group.casefold().strip()
                            if not any(
                                t.tracker.is_private()
                                for t in entry.torrents
                                if t.release_group.casefold().strip() == release_group
                            ):
                                entries[entry.anilist_id] = entry
                                break

        case "best-missing-dual" | "alt-missing-dual":
            header = f"# {(criteria.startswith('best') and 'Best') or 'Alt'} missing dual-audio\n\n"

            header += (
                f"An entry appears here if its designated '{(criteria.startswith('best') and 'best') or 'alt'}' version lacks dual audio, "
                f"but at least one {(criteria.startswith('best') and 'alt') or 'best'} release for the same entry "
                "includes a dual audio option.\n\n"
            )

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    alt_has_dual = any(t for t in entry.torrents if not t.is_best and t.is_dual_audio)
                    best_has_dual = any(t for t in entry.torrents if t.is_best and t.is_dual_audio)
                    has_best = any(t for t in entry.torrents if t.is_best)
                    has_alt = any(t for t in entry.torrents if not t.is_best)

                    if alt_has_dual and not best_has_dual and has_best and criteria == "best-missing-dual":
                        entries[entry.anilist_id] = entry
                    elif not alt_has_dual and best_has_dual and has_alt and criteria == "alt-missing-dual":
                        entries[entry.anilist_id] = entry
        case "no-dub":
            header = "# No dub\n\n"
            header += "This list contains all entries that have a dub according to AniList but have no dual-audio entries.\n\n"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    has_dual = any(t for t in entry.torrents if t.is_dual_audio)

                    if not has_dual:
                        entries[entry.anilist_id] = entry

            remove_entries_without_dub(entries)

        case "encode-best-entries":
            header = "# Encode best entries"

            def predicate(entry: seadex.EntryRecord, /) -> bool:
                if notes := entry.notes.casefold():
                    if "remux" in notes:
                        return False

                    if re.search(r"web[-\s]?DL", notes.splitlines()[0], re.IGNORECASE):
                        return False

                if entry.is_incomplete:
                    return False

                comparisons = [comp for comp in entry.comparisons if "slow" in comp]
                if not comparisons:
                    return False

                return any(torrent.is_best for torrent in entry.torrents)

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    if predicate(entry):
                        entries[entry.anilist_id] = entry

        case "missing-season-pack":
            header = "# Missing season pack\n\n"
            header += "Entries that do not have a complete season pack available.\n\n"
            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    for torrent in entry.torrents:
                        if torrent.grouped_url is not None:
                            entries[entry.anilist_id] = entry
                            break

        case unknown:
            assert_never(unknown)

    collection = MediaEntryCollection.from_entry_records(entries, sort_by)

    if json:
        output = collection.to_json()
    else:
        output = collection.to_markdown_table(header=header)

    if outfile:
        outfile.write_text(output, encoding="utf-8")
    else:
        print(output)


@app.command
def size_stats(outfile: Path | None = None) -> None:
    """
    Generate a markdown report of SeaDex size statistics.

    Parameters
    ----------
    outfile : Path | None, optional
        Path to write the output to.
    """
    output = SeaDexSizeCalculator().generate_markdown_report()

    if outfile:
        outfile.write_text(output, encoding="utf-8")
    else:
        print(output)


@app.command
def leaderboards(outfile: Path | None = None) -> None:
    """
    Generate a markdown leaderboard for SeaDex entries.

    Parameters
    ----------
    outfile : Path | None, optional
        Path to write the output to.
    """
    output = SeaDexLeaderboard().generate_markdown_report()

    if outfile:
        outfile.write_text(output, encoding="utf-8")
    else:
        print(output)


@app.command
def top_missing(count: int, outfile: Path | None = None) -> None:
    """
    Generate a markdown of top shows not on SeaDex

    Parameters
    ----------
    count : Int
        The amount of releases x50
    outfile : Path | None, optional
        Path to write the output to.
    """
    output = MediaEntryCollection.top_x_anilist_not_on_dex(count)

    if outfile:
        outfile.write_text(
            output.to_markdown_table(header=f"# Top {len(output.entries)} missing shows"), encoding="utf-8"
        )
    else:
        print(output)


if __name__ == "__main__":
    app()
