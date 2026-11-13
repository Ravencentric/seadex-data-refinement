import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from shutil import copytree

from sdr import history, pages, render
from sdr.pages import Page
from sdr.snapshot import Snapshot


def prepare[P, E](page: Page[P, E], snapshot: Snapshot, source: Path) -> P:
    """Prepare a page with history decoded using its export schema."""
    observations = history.load(source, page.export.type)
    return page.prepare(snapshot, observations)


def generate(snapshot: Snapshot, history: Path) -> dict[str, str]:
    """Render every page with saved history, without writing anything to disk."""
    if not history.is_dir():
        if not history.exists():
            raise FileNotFoundError(f"History directory does not exist: {history}")
        raise NotADirectoryError(f"History path is not a directory: {history}")
    env = render.environment()
    documents: dict[str, str] = {}
    for name, page in pages.discover().items():
        stem = render.slug(page.title)
        if not stem:
            raise ValueError(f"Page title {page.title!r} must produce a nonempty URL slug")
        filename = "index.md" if name == "index" else f"{stem}.md"
        if filename in documents:
            raise ValueError(f"Page title {page.title!r} produces a duplicate output: {filename}")
        data = prepare(page, snapshot, history / f"{stem}.jsonl")
        documents[filename] = render.render(env, name, title=page.title, captured=snapshot.captured, data=data)
    return documents


def write(documents: Mapping[str, str], destination: Path) -> None:
    """Write the rendered pages to disk, and delete orphans."""
    destination.mkdir(parents=True, exist_ok=True)
    expected = {destination / name for name in documents}
    for name, markdown in documents.items():
        (destination / name).write_text(markdown, encoding="utf-8")
    for path in destination.rglob("*.md"):
        if path not in expected:
            path.unlink()


def build(snapshot: Snapshot, history: Path) -> Path:
    """Build the site from a snapshot and locally saved page histories."""
    project = Path(__file__).resolve().parents[2]
    documents = generate(snapshot, history)
    write(documents, project / "build" / "docs")
    copytree(project / "javascripts", project / "build" / "docs" / "javascripts", dirs_exist_ok=True)
    copytree(project / "stylesheets", project / "build" / "docs" / "stylesheets", dirs_exist_ok=True)
    subprocess.run(
        [sys.executable, "-m", "zensical", "build", "--strict", "--config-file", str(project / "zensical.toml")],
        cwd=project,
        check=True,
    )
    return project / "site"
