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

## Learning roadmap

This is the canonical, corrected roadmap for the repository. It restructures the path around classical coding theory (linear codes, the Hamming code, and the CSS/stabilizer trilogy) before ancilla circuits and noisy decoding.

**Learning routine, for every step below:** read the stated source (if any) → complete its consolidation notebook → complete the end-of-notebook exercises → proceed to the next reading.

1. `01` — Stim basics
2. `02` — Classical 3-bit repetition code
3. `03` — Stabilizers and syndromes
4. `04` — Classical linear codes and the [7,4,3] Hamming code
   - Read first: Arthur Pesah, *Classical Error Correction*.
5. `05` — Stabilizer Trilogy I: codes and CSS construction
   - Read first: Arthur Pesah, *Stabilizer Trilogy I*.
6. `06` — Stabilizer Trilogy II: logical operators and code distance
   - Read first: Arthur Pesah, *Stabilizer Trilogy II*.
7. `07` — Stabilizer Trilogy III: quantum parity-check matrices and decoding
   - Read first: Arthur Pesah, *Stabilizer Trilogy III*.
8. `08` — Ancilla syndrome-extraction circuits
9. `09` — Noisy repetition-code decoder
10. `10` — Surface code, then Loom

The next notebook assumes only the concepts made explicit in the preceding notebook. If a concept is unfamiliar, return to the earlier notebook rather than skipping ahead.

### Current learner status

- Completed: notebooks 01–03.
- Already read: Arthur Pesah, *Stabilizer Trilogy I*.
- Current next task: Notebook 04.

## Repository guide

- [Project brief](docs/PROJECT_BRIEF.md): scope, audience, and authoring approach.
- [Learning path](docs/LEARNING_PATH.md): internal mirror of the roadmap above.
- [Current state](docs/CURRENT_STATE.md): current point in the learning path.
- [Contributing guide for Claude](CLAUDE.md): durable instructions for creating or revising learning material.

## Feedback and study habits

Learning QEC is cumulative. A short written explanation in your own words is more useful than racing through every cell. If a notebook leaves a question unresolved, record it in your notes and return to it after the next notebook gives more context.
