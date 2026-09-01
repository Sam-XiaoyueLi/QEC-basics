# CLAUDE.md

Persistent instructions for working in this repository. See also:

- [README.md](README.md) — the public entry point and learning path
- [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md) — purpose, audience, and instructional design
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

- Keep notebooks self-contained, concise, and executable top-to-bottom. Do not rely on hidden state or out-of-order execution.
- Give every new notebook a descriptive title, audience/prerequisite note where useful, learning objectives, expected outputs, and a short “how to use this notebook” note.
- Explain concepts before code. Use Markdown cells to define new ideas and interpret results.
- Include small prediction questions before revealing results, and clearly marked TODO exercises for the learner.
- Keep instructional cells separate from learner-owned answer areas.
- Verify affected notebooks by executing them top-to-bottom before reporting completion.

## Boundaries

- Do not edit unrelated files outside the current task.
- Do not commit, push, install global tools, or change Git settings unless explicitly asked.
- After making edits, run targeted verification and report exactly what changed.
