from __future__ import annotations

from pathlib import Path
from typing import Literal

import seadex
from cyclopts import App, Group

from .core import MediaEntryCollection
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
    criteria : Literal["unmuxed", "no-comparisons", "marked-incomplete", "public-non-nyaa", "private-tracker-only-torrents", "private-tracker-only-entries", "public-tracker-only", "best-no-dual"]
        The criteria to use for retrieving SeaDex entries.
        - "unmuxed": Unmuxed entries.
        - "no-comparisons": Entries without any comparisons.
        - "marked-incomplete": Entries explicitly marked as incomplete by editors.
        - "public-non-nyaa": Entries that are publicly available but not distributed on Nyaa.
        - "private-tracker-only": Entries exclusively found on private trackers.
        - "public-tracker-only": Entries exclusively found on public trackers.
        -"best-no-dual": Best entries without a dual audio version.
    outfile : Path | None, optional
        Path to write the output to.
    json : bool, optional
        Whether to output results in JSON format.
    """
    entries: dict[int, seadex.EntryRecord] = {}
    header: str | None = None

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

        case "private-tracker-only-torrents":
            header = "# Private tracker only torrents"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    for torrent in entry.torrents:
                        if torrent.tracker.is_private() and torrent.is_best:
                            release_group = torrent.release_group.casefold().strip()
                            if not any(
                                t.tracker.is_public()
                                for t in entry.torrents
                                if t.release_group.casefold().strip() == release_group
                            ):
                                entries[entry.anilist_id] = entry
                                break

        case "private-tracker-only-entries":
            header = "# Private tracker only entries"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    if all(torrent.tracker.is_private() for torrent in entry.torrents):
                        entries[entry.anilist_id] = entry

        case "public-tracker-only":
            header = "# Public tracker only"

            with seadex.SeaDexEntry() as seadex_entry:
                for entry in seadex_entry.iterator():
                    for torrent in entry.torrents:
                        if torrent.tracker.is_public():
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

        case _:  # Won't ever happen because cyclopts already validates the input.
            raise ValueError(criteria)

    collection = MediaEntryCollection.from_entry_records(entries)

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
        outfile.write_text(output.to_markdown_table(header=f"# Top {len(output.entries)} missing shows"), encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    app()
