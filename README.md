# QEC Basics

Learn quantum error correction through written tutorials and runnable Python notebooks. The examples progress from Shor's code to surface-code operations and decoding a noisy logical CNOT.

## Notebooks

Read the notebooks in order. Basic Python and familiarity with quantum gates are helpful.

| Order | Written tutorial | Notebook | What it covers |
| --- | --- | --- | --- |
| 1 | [Quantum error correction (PDF)](output/pdf/tut1.pdf) | [Shor's code](shor_tutorial.ipynb) | Encoding, stabilizers, a lookup decoder, Pauli frames, and a memory experiment. |
| 2 | [Rotated surface codes and lattice surgery (PDF)](output/pdf/tut2.pdf) | [Surface codes and lattice surgery](surface_code.ipynb) | Rotated patches, noisy memory, and logical GHZ preparation using Loom and Stim. |
| 3 | [Fault-tolerant computation and decoding (PDF)](output/pdf/tut3.pdf) | [Decoding the surface code](decoder.ipynb) | A TQEC CNOT, detector error models, a simple lookup decoder, PyMatching, and Sinter. |

## Written tutorials

Start with [Introduction to quantum computing (PDF)](output/pdf/tut0.pdf) for the fundamentals. The companion PDFs for the three notebooks are linked above.

The [Overleaf sources](overleaf/README.md) cover quantum computing fundamentals, quantum error correction, surface codes and lattice surgery, and fault-tolerant computation. Each `.tex` file is a standalone tutorial. The written series and notebook series have separate numbering.

## Run the notebooks

Install Python 3.12 and [uv](https://docs.astral.sh/uv/), then run from the repository root:

```bash
uv sync
uv run jupyter lab
```

Open a notebook and run its cells from top to bottom. In VS Code, select the repository's `.venv` Python environment as the notebook kernel. Sampling cells generate random results, so counts and plots can change between runs.

The CNOT notebook creates local HTML files for its interactive viewers. These generated files are ignored by Git. Static figures used by the notebooks are in `assets/`.
