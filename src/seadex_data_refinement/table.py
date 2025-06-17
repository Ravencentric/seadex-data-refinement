from __future__ import annotations

import textwrap
from collections.abc import Iterable

from prettytable import PrettyTable, TableStyle


class MarkdownTable:
    def __init__(
        self,
        fieldnames: Iterable[str],
        rows: Iterable[Iterable[str]],
        header: str | None = None,
        footer: str | None = None,
    ) -> None:
        self.fieldnames = fieldnames
        self.rows = rows
        self.header = header
        self.footer = footer

    def to_str(self) -> str:
        table = PrettyTable()
        table.set_style(TableStyle.MARKDOWN)
        table.align = "l"
        table.field_names = self.fieldnames
        for row in self.rows:
            table.add_row(row) # type: ignore[arg-type]
        out = table.get_formatted_string()

        if self.header:
            out = textwrap.dedent(self.header).strip() + "\n\n" + out

        if self.footer:
            out = out + "\n\n" + textwrap.dedent(self.footer).strip() + "\n"

        return out

    def __str__(self) -> str:
        return self.to_str()
