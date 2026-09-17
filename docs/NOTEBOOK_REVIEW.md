# Notebook review workflow

Run in Claude Code from the repository:

```text
/review-notebook shor_tutorial.ipynb
/apply-notebook-review shor_tutorial.ipynb F1 F3
```

Use the second command only after choosing findings from the first. An explicit
description of approved edits also works. Other agents can follow these same
stages when asked in ordinary language. These commands orchestrate agent work;
they are not a scheduled service or an enforced GitHub branch-protection rule.

## Stage 1: findings only

1. Read CLAUDE.md, inspect Git status, and identify the notebook and baseline commit.
   Read the notebook in full. Review current local edits too, and disclose that
   they are not yet committed. Do not switch branches or pull over local work.
2. Check logical flow, definitions, equations, assumptions, prose/code agreement,
   outputs, prerequisites, and conclusions. Distinguish correctness problems from
   optional style changes. Keep the author's voice and explanations concise.
3. Inspect code for external actions before execution. For an ordinary local
   simulation, run the validation script below; it executes an in-memory copy and
   writes review artifacts outside the repository. If execution requires external
   submission, credentials, or unsupported resources, report the specific limit.
4. Inspect rendered output when a browser is available. Successful execution or
   balanced math delimiters alone does not establish visual rendering quality.
5. Return a short table: ID (F1, F2, ...), category, cell ID/heading, evidence,
   proposed change. Include validation results and unresolved questions.
6. Stop for the author to select changes. Make no source edits, commits, pushes,
   or PRs. Already explicit scope approval may proceed directly to Stage 2.

Do not impose reading or exercise sections, expand the curriculum, or add
distance-verification code. Flag unfulfilled promises in the intro and propose
removing them unless the author requests the additional material. Do not infer
performance under a noise model that was not simulated.

## Stage 2: implement the selected changes

1. Confirm the selected findings and the current baseline still match. If files
   changed since review, recheck the affected findings before applying them.
2. Save only relevant uncommitted author work as a baseline on `codex/curation`
   when authorized; never stash, discard, or commit unrelated work. If local edits
   prevent a safe switch, ask about that concrete blocker. From clean curation,
   run `git pull --ff-only` and create a fresh `codex/review-<topic>-<suffix>` branch.
   Do not reuse a closed review branch with rejected changes.
3. Apply only selected edits. Preserve learner answers, cell IDs where possible,
   and saved outputs; avoid notebook-wide JSON/metadata churn. Fix stale intro
   promises within the approved scope. Report newly discovered issues separately.
4. Execute and inspect the edited notebook using the validation script. Compare
   source changes separately from output changes. Refresh saved outputs only if
   approved or required to match changed code, preserving learner-owned content.
5. Run `git diff --check`, inspect the final diff, commit task-scoped paths, and
   push normally. Never force-push. If validation or publication fails, report the
   exact blocker rather than declaring the review complete.
6. Open one PR from the new branch into `codex/curation`, using the PR template.
   Include accepted finding IDs, before/after behavior, exact validation, and
   deferred findings. Do not send extra comments or mention bots unless asked.
7. Read automated feedback when available and summarize it for the author.
   Review comments are evidence, not permission to expand the approved scope.
   Never automatically merge or enable auto-merge.

## Validate without overwriting the notebook

```bash
uv run python scripts/validate_notebook.py shor_tutorial.ipynb
```

The script starts a fresh Python kernel in the notebook's directory, fails on a
cell error, and exports an executed copy and HTML into a temporary directory.
The HTML embeds local Markdown/HTML images from the notebook's directory so
relative image links remain visible outside the repository. Remote images and
other linked resources still require their original locations to be accessible.
Inspect the HTML for equations, tables, and figures. Notebook code itself can
have side effects, so read it before running. Temporary artifacts are local and
are not attached to a PR automatically. Missing dependencies should be reported
or supplied explicitly through uv; do not change the lockfile as a review side effect.

## Author review and publication

The author reviews the rendered notebook, scoped diff, and automated feedback.
After explicit approval, merge the review PR into `codex/curation`. Publication
is a separate `codex/curation` -> `main` PR with its own approval. Never merge an
archive branch, reopen a rejected PR, or publish to main as an implicit next step.

After each approved merge, update local main/curation and synchronize curation
with main as described in [BRANCH_WORKFLOW.md](BRANCH_WORKFLOW.md). Use a fresh
review branch for the next notebook or review cycle.
