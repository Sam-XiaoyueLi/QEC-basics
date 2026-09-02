# QEC Basics

A beginner-friendly, hands-on introduction to quantum error correction (QEC).

This repository is a guided, reading-led learning path for readers who are comfortable with basic Python but are new to quantum error correction. It starts with classical error correction, builds through the stabilizer formalism and the CSS/Steane code, and continues to noisy decoding, the surface code, and hardware-aware QEC with real tooling (Stim, Loom, and Quantinuum Guppy).

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

This is the canonical, corrected roadmap for the repository. It is reading-led: most notebooks pair with a specific external article or documentation source, which the notebook then consolidates through derivation, code, or simulation.

**Learning routine, for every step below:** read the stated material → complete the consolidation notebook → complete the end exercises → move forward.

1. `01` — Stim Basics
2. `02` — Classical 3-Bit Repetition Code
3. `03` — Stabilizers, Syndromes, and Parity Measurements
4. `04` — Classical Linear Codes and the Hamming Code
   - Read first: Arthur Pesah, *Classical Error Correction*.
5. `05` — Shor Code, CSS Codes, and the Steane Code
   - Read first: Arthur Pesah, *Stabilizer Formalism I*.
6. `06` — Logical Operators, Code Distance, and Degeneracy
   - Read first: Arthur Pesah, *Stabilizer Formalism II*.
7. `07` — Quantum Parity-Check Matrices and Decoding
   - Read first: Arthur Pesah, *Stabilizer Formalism III*.
8. `08` — Noisy Steane-Code Decoding
9. `09` — Surface-Code Foundations
10. `10` — Surface-Code Detectors and Decoding with Stim and Loom
11. `11` — Hardware-Aware QEC with Quantinuum Guppy

The next notebook assumes only the concepts made explicit in the preceding notebook. If a concept is unfamiliar, return to the earlier notebook rather than skipping ahead. Obsolete or superseded notebooks are kept out of this active sequence in [`archive/`](archive/) for reference only.

### Current learner status

- Completed: notebooks 01, 02, 03.
- Already read: Arthur Pesah's *Stabilizer Formalism I* article (listed above as the prerequisite reading for notebook 05, for learners who reach this repository fresh).
- Current next task: notebook 04.

## Repository guide

- [Project brief](docs/PROJECT_BRIEF.md): scope, audience, and authoring approach.
- [Learning path](docs/LEARNING_PATH.md): internal mirror of the roadmap above.
- [Current state](docs/CURRENT_STATE.md): current point in the learning path.
- [Contributing guide for Claude](CLAUDE.md): durable instructions for creating or revising learning material.

## Feedback and study habits

Learning QEC is cumulative. A short written explanation in your own words is more useful than racing through every cell. If a notebook leaves a question unresolved, record it in your notes and return to it after the next notebook gives more context.
