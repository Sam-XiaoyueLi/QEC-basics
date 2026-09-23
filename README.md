# QEC Basics

A beginner-friendly, hands-on introduction to quantum error correction (QEC), being manually curated one notebook at a time.

This repository is the `Notebooks/` workspace. The Overleaf source lives in the sibling `Overleaf/` folder of the local `QEC_tutorials/` directory and is managed separately; it is not part of this Git repository. Historical LaTeX files from this branch were moved to `Overleaf/History/`.

`main` is the reviewed collection. It currently contains **zero notebooks**. Notebooks will be selected, completed, executed, and reviewed before being merged into `main`.

## Branches

| Branch | Purpose |
| --- | --- |
| `main` | Completed and reviewed notebooks; initially empty of notebooks. |
| `codex/curation` | Workspace for selecting, completing, and reviewing new material. |
| `codex/archive/previous-tutorials` | Snapshot of notebooks 01–12, the extra stabilizer notebook, and older `archive/` notebooks, including local learner work. |
| `codex/archive/zixiong-tutorials` | Snapshot of `ZiXiong_tutorials/`, including its local edits, assets, dependency files, and license. |

Archive branches are reference snapshots. Their notebooks remain in Git history and on their respective branches. Copy individual files into curation when useful; do not merge archive branches into `main`.

## Learning roadmap

No curated sequence has been published yet. The order and prerequisites will be decided as notebooks are selected and reviewed.

## Setup

The existing Python tooling is retained for future curation. With Python 3.12 and uv installed:

```bash
uv sync
uv run jupyter lab
```

There will be no project notebooks to open until you select or create one on the curation branch. The ZiXiong archive has its own environment in `ZiXiong_tutorials/`.

## Repository guide

- [Branch workflow](docs/BRANCH_WORKFLOW.md): how the cleanup works and how to curate and publish notebooks.
- [Notebook review](docs/NOTEBOOK_REVIEW.md): Claude commands for findings first, approved edits, validation, and review PRs.
- [Project brief](docs/PROJECT_BRIEF.md): audience and authoring approach.
- [Learning path](docs/LEARNING_PATH.md): curated sequence as it develops.
- [Current state](docs/CURRENT_STATE.md): progress and next steps.
- [Authoring guide](CLAUDE.md): instructions for creating and revising learning material.
