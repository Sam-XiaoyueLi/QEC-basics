# CLAUDE.md

Persistent instructions for working in this repository. See also:

- [README.md](README.md) — the public entry point and canonical learning roadmap
- [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md) — purpose, audience, and instructional design
- [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md) — internal mirror of the README roadmap
- [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md) — what is complete and what comes next

## What this is

A public, beginner-friendly, hands-on quantum error correction (QEC) learning repository. Notebooks are the primary artifact. They form a coherent tutorial for readers who may never see the conversation or generation process that produced them.

The intended reader has basic Python literacy and curiosity about quantum computing, but may have no prior QEC knowledge. Do not assume they know project-specific shorthand, unstated prior discussion, or why a notebook exists.

## Authoring standard

When creating or revising material:

- Treat the README as the starting point. Every notebook must fit its stated learning path.
- Make each notebook understandable from its title, goal, expected outcomes, and stated prerequisites.
- Explain what problem a concept solves before introducing notation, code, or a circuit.
- Define terms at their first use, including symbols and measurement conventions.
- Use short, precise prose and small runnable examples. Explain code before asking the reader to run it.
- State what a reader should already know, and link back to the relevant earlier notebook when a prerequisite matters.
- Use prediction questions, checkpoints, and TODO exercises to turn passive reading into active learning.
- End each notebook with a clear bridge to the next topic.
- Keep claims technically accurate and distinguish intuition from formal statements.
- Never refer to “our discussion,” “the user,” “the generation process,” or unstated context.
- Prefer inclusive phrasing such as “this notebook” and “the reader” over instructions that only make sense for the original author.

## Protect learner work

- Treat filled-in TODO exercises, outputs, and sections titled `My Notes` or `My Notes and Answers` as learner-owned.
- Do not erase, reset, regenerate, or rewrite learner-owned work unless explicitly asked.
- When a notebook needs structural improvements, preserve completed exercises and add only the smallest necessary framing or correction.
- For broad consistency improvements across existing notebooks, propose a scoped plan first; avoid spending tokens on cosmetic batch rewrites during active learning.

## Tooling

- Use `uv` only. Never invoke `pip` directly.
- Run all Python and tools through `uv run` (for example, `uv run jupyter lab` and `uv run pytest`).
- Dependencies are managed via `pyproject.toml` and `uv.lock`. Add packages with `uv add`, not manual lockfile edits.

## Notebook conventions

- A notebook's number is its reading order. A notebook may assume only what earlier-numbered notebooks (or its own stated reading) already established — never a tool, library, or concept first introduced in a later-numbered notebook. When in doubt, check what number a dependency was actually introduced at, rather than assuming.
- Keep notebooks self-contained, concise, and executable top-to-bottom. Do not rely on hidden state or out-of-order execution.
- Give every new notebook a descriptive title, audience/prerequisite note where useful, learning objectives, expected outputs, and a short “how to use this notebook” note.
- Use descriptive notebook titles that name the actual content (e.g. “Shor Code, CSS Codes, and the Steane Code”); never a vague series label such as “Stabilizer Trilogy I.”
- Every notebook begins with `## Read before you begin`, containing direct and specific reading links, exact section names from that reading, and the concrete concepts to extract from each.
- Each notebook must directly consolidate the stated reading through derivations, experiments, code, or simulation — not merely restate it.
- Explain concepts before code. Use Markdown cells to define new ideas and interpret results.
- Include small prediction questions before revealing results, and clearly marked TODO exercises for the learner.
- Every notebook ends with `## Exercises`.
- Keep instructional cells separate from learner-owned answer areas.
- Verify affected notebooks by executing them top-to-bottom before reporting completion.
- Never create a separate “Answers,” “Your Answers,” “Solutions,” “Questions,” reflection, or response section in notebooks.
- Place prediction questions and TODO exercises inline, immediately beside the concept or code they concern.
- Never add blank answer cells or prescribe where the reader must write responses; the reader decides whether and where to record their own answers.

## Boundaries

- Do not edit unrelated files outside the current task.
- Do not install global tools or change Git settings unless explicitly asked.
- After making edits, run targeted verification and report exactly what changed.

## Git workflow

- For every task that changes repository files: verify the changes first, then commit and push the task-scoped changes automatically.
- Before editing, run `git status` and `git pull --ff-only`.
- Stage only files changed for the current task; preserve unrelated user changes.
- Use a concise, descriptive commit message.
- Push normally with `git push`; never force-push.
- If verification, commit, pull, or push fails, stop and report the exact blocker. Do not use destructive Git commands or work around a rejected push.
- If a task makes no file changes, do not create an empty commit.
