import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from shutil import copytree

from sdr.pages import discover
from sdr.render import environment, render, slug
from sdr.snapshot import Snapshot


def generate(snapshot: Snapshot) -> dict[str, str]:
    """Render every page into a dict, without writing anything to disk."""
    env = environment()
    documents: dict[str, str] = {}
    for name, page in discover().items():
        stem = "index" if name == "index" else slug(page.title)
        if not stem:
            raise ValueError(f"Page title {page.title!r} must produce a nonempty URL slug")
        filename = f"{stem}.md"
        if filename in documents:
            raise ValueError(f"Page title {page.title!r} produces a duplicate output: {filename}")
        documents[filename] = render(env, name, page, snapshot)
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


def build(snapshot: Snapshot) -> Path:
    """Build the site from a snapshot."""
    project = Path(__file__).resolve().parents[2]
    documents = generate(snapshot)
    write(documents, project / "build" / "docs")
    copytree(project / "javascripts", project / "build" / "docs" / "javascripts", dirs_exist_ok=True)
    subprocess.run(
        [sys.executable, "-m", "zensical", "build", "--strict", "--config-file", str(project / "zensical.toml")],
        cwd=project,
        check=True,
    )
    return project / "site"
