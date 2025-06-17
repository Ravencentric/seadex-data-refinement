from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from functools import cached_property

from prettytable import PrettyTable, TableStyle
from pydantic import BaseModel, ByteSize
from seadex import EntryRecord, SeaDexEntry, TorrentRecord


class GroupSizeRecord(BaseModel):
    name: str
    """Name of the group."""
    total_size: ByteSize
    """Total size of the torrents under this group."""
    best_size: ByteSize
    """Total size of the torrents marked as best under this group."""
    total_entries: int
    """Total number of entries (best+alt) under this group."""

    @cached_property
    def best_size_percentage(self) -> float:
        return (self.best_size / self.total_size) * 100

    @cached_property
    def average_torrent_size(self) -> ByteSize:
        return ByteSize(self.total_size / self.total_entries)


class SeaDexSizeCalculator:
    def __init__(self) -> None:
        pass

    @cached_property
    def entries(self) -> tuple[EntryRecord, ...]:
        with SeaDexEntry() as se:
            return tuple(se.iterator())

    @cached_property
    def filtered_trs(self) -> tuple[TorrentRecord, ...]:
        return self.filter_trs(self.entries)

    @staticmethod
    def filter_trs(entries: Iterable[EntryRecord]) -> tuple[TorrentRecord, ...]:
        trs: set[TorrentRecord] = set()

        for entry in entries:
            groups = {t.release_group for t in entry.torrents}
            for group in groups:
                # For every group in an entry, that has both a PT and Public release,
                # only consider the PT release. If a group does not have a PT release,
                # then we fallback to public releases.
                filtered = [t for t in entry.torrents if t.release_group == group and t.tracker.is_private()] or [
                    t for t in entry.torrents if t.release_group == group
                ]
                trs.update(filtered)

        return tuple(trs)

    @cached_property
    def total_size(self) -> ByteSize:
        sizes: list[int] = []

        for torrent in self.filtered_trs:
            sizes.extend(file.size for file in torrent.files)

        return ByteSize(sum(sizes))

    @cached_property
    def best_size(self) -> ByteSize:
        sizes: list[int] = []

        for torrent in self.filtered_trs:
            if torrent.is_best:
                sizes.extend(file.size for file in torrent.files)

        return ByteSize(sum(sizes))

    @cached_property
    def alt_size(self) -> ByteSize:
        return ByteSize(self.total_size - self.best_size)

    @cached_property
    def realistic_size(self) -> ByteSize:
        """
        The realistic size stat tries to emulate a scenario
        where a user will likely download the best dual audio release for an entry,
        fallback to the best single audio release if that's not present,
        and again fallback to whatever there is if neither exist.
        """
        torrents: set[TorrentRecord] = set()

        for entry in self.entries:
            filtered = (
                # 1. Best release with dual audio from private tracker
                [t for t in entry.torrents if t.is_best and t.is_dual_audio and t.tracker.is_private()]
                # 2. Best release with dual audio from any tracker
                or [t for t in entry.torrents if t.is_best and t.is_dual_audio]
                # 3. Best release from private tracker
                or [t for t in entry.torrents if t.is_best and t.tracker.is_private()]
                # 4. Best release from any tracker
                or [t for t in entry.torrents if t.is_best]
                # 5. Any available release
                or entry.torrents
            )

            for torrent in filtered:
                torrents.add(torrent)
                break

        sizes: list[int] = []

        for torrent in torrents:
            sizes.append(sum(f.size for f in torrent.files))

        return ByteSize(sum(sizes))

    def sizes_by_group(self) -> tuple[GroupSizeRecord, ...]:
        data: dict[str, dict[str, int]] = defaultdict(lambda: {"total_size": 0, "best_size": 0, "total_entries": 0})

        # Count the total entries from each group.
        # We do not count the torrents because that can heavily skew results.
        # For example, SubsPlease doesn't batch their torrents, so
        # a single entry might have 12 single episode torrents.
        # So we only count the fact that SubsPlease appears once as an alt entry
        # and ignore the fact that there are 12 torrents under that one alt entry.
        for entry in self.entries:
            # Each group is considered a maximum of two times per entry: once for best and once for alt.
            best_groups = list({t.release_group for t in entry.torrents if t.is_best})
            alt_groups = list({t.release_group for t in entry.torrents if not t.is_best})
            groups = best_groups + alt_groups

            for group in groups:
                data[group]["total_entries"] += 1

        # For sizes, we do want to count every torrent because the total size should
        # be accurate regardless of how the files are packaged. For example, if SubsPlease
        # has 12 single episode torrents or 1 batch with those same 12 episodes,
        # the total size should be the same. So we iterate through every torrent
        # and sum up their file sizes.
        for torrent in self.filtered_trs:
            name = torrent.release_group.strip()
            total_size = data[name]["total_size"] + sum(f.size for f in torrent.files)
            best_size = data[name]["best_size"] + sum(f.size for f in torrent.files if torrent.is_best)
            data[name].update(total_size=total_size, best_size=best_size)

        # Sort by total size in descending order
        sorted_data = sorted(data.items(), key=lambda x: x[1]["total_size"], reverse=True)

        # Split into top entries and others
        top_entries = sorted_data[:49]
        other_entries = sorted_data[49:]

        # Sum up stats for others
        others_stats = {
            "total_size": sum(stats["total_size"] for _, stats in other_entries),
            "best_size": sum(stats["best_size"] for _, stats in other_entries),
            "total_entries": sum(stats["total_entries"] for _, stats in other_entries),
        }
        top_entries.append(("Others", others_stats))

        return tuple(GroupSizeRecord(name=name, **stats) for name, stats in top_entries)  # type: ignore[arg-type]

    def generate_markdown_report(self) -> str:
        sizes_by_group = self.sizes_by_group()

        # assert self.total_size == sum(x.total_size for x in sizes_by_group)
        # assert self.best_size == sum(x.best_size for x in sizes_by_group)

        markdown_output = "# Size Statistics\n\n"
        markdown_output += (
            "These statistics are NOT 100% accurate, but they likely are as realistic as (reasonably) possible.\n\n"
            'The definition of an entry (or a "complete" torrent) is quite murky. '
            "SeaDex defines it as an AniList entry, but every private tracker has their own definition "
            "(typically, they follow AniDB or TVDB), while Nyaa does not enforce a specific definition. "
            "Every release can quite possibly have slightly different torrents across trackers, "
            "or a single torrent on Nyaa can include several SeaDex entries. "
            "A Nyaa torrent might contain an entire franchise, but only a single file out of it might be relevant.\n\n"
            "All of this and more means that we need to settle on a method to calculate these statistics. "
            "This was essentially calculated by iterating over every SeaDex entry, "
            "and if an entry has both private tracker torrent and public torrent from the same group, "
            "only the former is considered; otherwise, all torrents are considered. "
            "The `total_entries` metric counts how many times a group appears across entries, "
            "with each group counted up to twice per entry—once for best torrents and once for alt torrents. "
            "This avoids skewing results from entries with multiple torrents "
            "(e.g., a single entry with 12 torrents counts as one for `total_entries`). "
            "Exact duplicates are also discarded."
        )
        markdown_output += "\n\n## Overview\n\n"
        markdown_output += f"- Total size: `{self.total_size.human_readable(separator=' ')}`\n"
        markdown_output += f"- Best size: `{self.best_size.human_readable(separator=' ')}`\n"
        markdown_output += f"- Alt size: `{self.alt_size.human_readable(separator=' ')}`\n"
        markdown_output += f"- Realistic size: `{self.realistic_size.human_readable(separator=' ')}`\n\n"
        markdown_output += (
            "The `Realistic size` stat tries to emulate a scenario where a user will likely download the best dual audio release for an entry, "
            "falling back to the best single audio release if that's not present, "
            "and again falling back to whatever is available if neither exists.\n"
        )

        table = PrettyTable()
        table.set_style(TableStyle.MARKDOWN)
        table.align = "l"
        table.field_names = ["Rank", "Group", "Total Size", "Best Size", "Total Entries"]
        for rank, entry in enumerate(sizes_by_group, start=1):
            table.add_row(
                [
                    rank,
                    entry.name,
                    entry.total_size.human_readable(separator=" "),
                    f"{entry.best_size.human_readable(separator=' ')} ({entry.best_size_percentage:.2f}%)",
                    f"{entry.total_entries} (~{entry.average_torrent_size.human_readable(separator=' ')} each)",
                ],
            )

        markdown_output += "\n\n## Breakdown by Group\n\n"
        markdown_output += table.get_formatted_string()
        return f"{markdown_output}\n"
