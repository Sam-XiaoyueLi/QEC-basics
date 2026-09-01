# CLAUDE.md

Persistent instructions for working in this repository. See also:
- [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md) — what this project is and the learning sequence
- [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md) — what's done, what's in progress, what's next

## What this is

A beginner-friendly, hands-on quantum error correction (QEC) learning repository. Notebooks are the primary artifact; they teach concepts progressively rather than serving as a reference library or production codebase.

## Tooling

- Use `uv` only. Never invoke `pip` directly.
- Run all Python and tools through `uv run` (e.g. `uv run jupyter lab`, `uv run pytest`).
- Dependencies are managed via `pyproject.toml` / `uv.lock`. Add packages with `uv add`, not manual edits to lockfiles.

## Notebook conventions

- Keep notebooks self-contained, concise, and executable top-to-bottom (no hidden state or out-of-order cell dependencies).
- Explain concepts before code: each new idea gets beginner-friendly prose before the cell that implements it.
- Include small prediction questions ("what do you expect to happen if...") before revealing results.
- Include clearly marked `TODO` exercises for the learner to complete.

## Boundaries

- Do not edit unrelated files outside the scope of the current task.
- Do not commit, push, install global tools, or change Git settings unless explicitly asked.
- After making edits, run a targeted verification (e.g. execute the affected notebook or cell with `uv run`, run relevant tests) and report exactly what changed.
