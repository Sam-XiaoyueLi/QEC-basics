# QEC Basics

A beginner-friendly, hands-on introduction to quantum error correction (QEC), being manually curated one notebook at a time.

This repository is the `Notebooks/` workspace. The Overleaf source lives in the sibling `Overleaf/` folder of the local `QEC_tutorials/` directory and is managed separately; it is not part of this Git repository. Historical LaTeX files from this branch were moved to `Overleaf/History/`.

`main` contains the Shor-code tutorial, [`shor_tutorial.ipynb`](shor_tutorial.ipynb). New tutorials are developed on topic branches and added to `main` after review.

## Branches

| Branch | Purpose |
| --- | --- |
| `main` | Published notebook collection, starting with the Shor-code tutorial. |
| `codex/surface-code-tutorial` | Working branch for the next surface-code notebook. |
| `codex/archive/previous-tutorials` | Snapshot of notebooks 01–12, the extra stabilizer notebook, and older `archive/` notebooks, including local learner work. |
| `codex/archive/zixiong-tutorials` | Snapshot of `ZiXiong_tutorials/`, including its local edits, assets, dependency files, and license. |

Archive branches are reference snapshots. Their notebooks remain in Git history and on those branches. Copy individual files into a topic branch when useful; do not merge an archive branch into `main`.

## Learning roadmap

Start with the Shor-code tutorial on `main`. The next surface-code notebook is in development; its place in the sequence will be recorded after review.

## Setup

The existing Python tooling is retained for future curation. With Python 3.12 and uv installed:

```bash
uv sync
uv run jupyter lab
```

Open `shor_tutorial.ipynb` on `main`. The ZiXiong archive has its own environment in `ZiXiong_tutorials/`.

## Repository guide

- [Branch workflow](docs/BRANCH_WORKFLOW.md): how the cleanup works and how to curate and publish notebooks.
- [Notebook review](docs/NOTEBOOK_REVIEW.md): Claude commands for findings first, approved edits, validation, and review PRs.
- [Project brief](docs/PROJECT_BRIEF.md): audience and authoring approach.
- [Learning path](docs/LEARNING_PATH.md): curated sequence as it develops.
- [Current state](docs/CURRENT_STATE.md): progress and next steps.
- [Authoring guide](CLAUDE.md): instructions for creating and revising learning material.
