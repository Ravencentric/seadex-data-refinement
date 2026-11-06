# Working on SDR

SDR generates a Zensical site from SeaDex and AniList data.
This file records enduring workflow and coding preferences. Keep feature
decisions and their rationale with the relevant implementation.

## Workflow

- Use `uv`, the existing lockfile, and the project's configured tooling.
  Discuss additional dependencies before installing them.
- `uv run sdr fetch` acquires data; `uv run sdr build` builds it;
  `uv run zensical serve` previews it. Stop the preview before a strict build.
- Reuse `snapshot.json` during development. Builds must stay offline. Use real
  data for verification; do not fabricate snapshots or demo results.
- Batch source requests and reuse fetched data. Measure request counts and runtime
  when changing acquisition.
- Preserve the saved snapshot and environment during cleanup. Keep generated
  output, caches, `.venv`, and snapshots out of commits.

Run the relevant checks:

```powershell
uv run --offline --locked pyrefly check
uv run --offline --locked ruff check .
uv run --offline --locked ruff format --check .
uv run --offline --locked sdr build
```

Choose validation appropriate to the change. Inspect generated output when
changing reports, and check selections against their criteria using real data.

## Code Style

- Prefer straightforward loops and named intermediate values over clever
  expressions. Use `reverse=True` for descending sorts.
- Follow the surrounding code and comment style, including explanatory
  walkthroughs where useful.
- Prefer clear single-word names. Use underscores only when necessary,
  including Python special names and dependency-defined names.
- Keep strong types and reuse existing records; avoid unnecessary wrappers.
- Fail clearly on broken invariants. Handle nullable source data explicitly
  rather than concealing missing required data with defaults.
- Docstrings explain purpose and contracts. Update only those affected by the change.
  Preserve useful reasoning comments.
- Preserve source text and escape it appropriately for its output format.
- Simplify heuristics around realistic cases. Check actual results before claiming
  accuracy is preserved.
- Preserve contribution guidance, exclusions, and caveats when changing report
  mechanics.
- Write documentation for its audience. Keep implementation details out of
  user-facing copy.
