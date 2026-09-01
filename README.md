# QEC Basics

A beginner-friendly, hands-on introduction to quantum error correction (QEC).

This repository is a guided learning path for readers who are comfortable with basic Python but are new to quantum error correction. It starts with familiar classical error correction, then builds toward stabilizers, syndrome-extraction circuits, noisy decoding, and the surface code.

You do not need to know how this repository was created to use it. Start here, follow the notebooks in order, and treat the prediction questions and exercises as part of the lesson.

## Who this is for

This is for a curious learner who:

- can read and run simple Python;
- is willing to pause and reason through short exercises;
- may have encountered qubits, gates, or measurements but does not yet understand QEC;
- wants conceptual intuition alongside runnable examples.

It is not a production QEC library or a complete quantum-computing course.

## Before you begin

You need Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/Sam-XiaoyueLi/QEC-basics.git
cd QEC-basics
uv sync
uv run jupyter lab
```

Open the notebooks in numerical order and select the project's `.venv` Python interpreter if Jupyter asks.

## How to learn from each notebook

1. Read the goal and expected outcomes.
2. Run cells from top to bottom.
3. Before every **Prediction**, write down your answer before revealing the result.
4. Complete `TODO` exercises yourself. They are intentionally part of the learning path.
5. Use the checkpoint at the end to decide whether to continue or review.

Your own notes and completed exercises are learning records. Keep them when updating the repository.

## Learning path

| Notebook | Topic | What you will gain |
|---|---|---|
| 01 | Stim basics: measurement, parity, and a first syndrome | A concrete picture of parity measurement with an ancilla |
| 02 | Classical 3-bit repetition code | Redundancy, code distance, syndromes, detection, and correction |
| 03 | Stabilizers and syndromes | The quantum meaning of the classical parity checks |
| 04 | Syndrome-extraction circuits | How ancillas measure stabilizers without reading the logical state |
| 05 | Noisy decoding | How physical noise becomes logical failure |
| 06+ | Surface code with Stim, Loom, and Quantinuum Guppy | Applying the ideas to a practical QEC code |

The next notebook assumes only the concepts made explicit in the preceding notebook. If a concept is unfamiliar, return to the earlier notebook rather than skipping ahead.

## Repository guide

- [Project brief](docs/PROJECT_BRIEF.md): scope, audience, and authoring approach.
- [Current state](docs/CURRENT_STATE.md): current point in the learning path.
- [Contributing guide for Claude](CLAUDE.md): durable instructions for creating or revising learning material.

## Feedback and study habits

Learning QEC is cumulative. A short written explanation in your own words is more useful than racing through every cell. If a notebook leaves a question unresolved, record it in your notes and return to it after the next notebook gives more context.
