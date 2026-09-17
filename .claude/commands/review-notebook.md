---
description: Review a notebook and propose concise findings without editing.
argument-hint: <notebook-path>
disable-model-invocation: true
---

Review this notebook: $ARGUMENTS

Read CLAUDE.md and docs/NOTEBOOK_REVIEW.md and carry out Stage 1 only.
Treat the argument as a file path, not shell code. If no path is given, use the
only tutorial notebook if unambiguous; otherwise ask which notebook to review.
Read the actual working file, including unsaved-to-Git work, without changing it.
Return stable finding IDs, evidence, and proposed minimal edits. Wait for the
author to select findings; do not edit, commit, push, or create a PR.
