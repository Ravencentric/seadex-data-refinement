from __future__ import annotations

import os
import shutil
import time
from pathlib import Path

import nox

nox.needs_version = ">=2024.10.9"
nox.options.default_venv_backend = "uv"
nox.options.sessions = ["lint", "build-docs"]


CI = bool(os.getenv("CI"))


def install(session: nox.Session) -> None:
    session.run_install(
        "uv",
        "sync",
        "--locked",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )


@nox.session(venv_backend=None, default=False)
def clean(_: nox.Session) -> None:
    paths = (
        "./.mypy_cache",
        "./.pytest_cache",
        "./src/__pycache__",
        "./__pycache__",
        "./docs/build",
        "./.nox",
    )

    for p in paths:
        try:
            shutil.rmtree(p)
        except Exception:
            pass


@nox.session
def lint(session: nox.Session) -> None:
    install(session)
    if os.getenv("CI"):
        # Do not modify files in CI, simply fail.
        session.run("ruff", "check", ".")
        session.run("ruff", "format", ".", "--check")
    else:
        # Fix any fixable errors if running locally.
        session.run("ruff", "check", ".", "--fix")
        session.run("ruff", "format", ".")


@nox.session(name="build-docs")
def build_docs(session: nox.Session) -> None:
    install(session)

    src = Path.cwd() / "docs"
    build = Path.cwd() / "site"

    def sleep() -> None:
        if CI:
            time.sleep(30)

    session.run("sdr", "get-entries", "unmuxed", "--outfile", src / "unmuxed.md", *session.posargs)
    sleep()
    session.run("sdr", "get-entries", "no-comparisons", "--outfile", src / "no-comparisons.md", *session.posargs)
    sleep()
    session.run("sdr", "get-entries", "marked-incomplete", "--outfile", src / "marked-incomplete.md", *session.posargs)
    sleep()
    session.run("sdr", "get-entries", "public-non-nyaa", "--outfile", src / "public-non-nyaa.md", *session.posargs)
    sleep()
    session.run(
        "sdr",
        "get-entries",
        "private-tracker-only-entries",
        "--outfile",
        src / "private-tracker-only-entries.md",
        *session.posargs,
    )
    sleep()
    session.run(
        "sdr",
        "get-entries",
        "private-tracker-only-torrents",
        "--outfile",
        src / "private-tracker-only-torrents.md",
        *session.posargs,
    )
    sleep()
    session.run(
        "sdr", "get-entries", "public-tracker-only", "--outfile", src / "public-tracker-only.md", *session.posargs
    )
    sleep()
    session.run("sdr", "get-entries", "best-missing-dual", "--outfile", src / "best-missing-dual.md", *session.posargs)
    sleep()
    session.run("sdr", "get-entries", "alt-missing-dual", "--outfile", src / "alt-missing-dual.md", *session.posargs)
    sleep()
    session.run(
        "sdr", "get-entries", "encode-best-entries", "--outfile", src / "encode-best-entries.md", *session.posargs
    )
    sleep()
    session.run("sdr", "get-entries", "patch-required", "--outfile", src / "patch-required.md", *session.posargs)
    sleep()
    session.run("sdr", "get-entries", "broken-entries", "--outfile", src / "broken-entries.md", *session.posargs)
    sleep()
    session.run("sdr", "top-missing", "--count", "500", "--outfile", src / "top-500.md", *session.posargs)
    sleep()
    session.run("sdr", "get-entries", "no-dub", "--outfile", src / "no-dub.md", *session.posargs)

    # No sleep here because these do not hit AniList.
    session.run("sdr", "size-stats", "--outfile", src / "size-statistics.md", *session.posargs)
    session.run("sdr", "leaderboards", "--outfile", src / "leaderboards.md", *session.posargs)
    session.run("sphinx-build", "-M", "html", src, build)
