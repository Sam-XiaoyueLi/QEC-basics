# QEC Basics

This repository offers a step-by-step introduction to quantum error correction, starting with the fundamentals of quantum computing. We then explore Shor’s code, the first quantum error-correcting code, before moving to the widely studied rotated surface code, lattice surgery, and what it takes to build a fault-tolerant quantum program.

The written tutorials develop the ideas, while the notebooks let you try them through simulations. Along the way, we introduce decoding and show how to use noisy measurement results to recover a logical answer.

## Concepts covered

- **Encoding:** storing a logical qubit across several physical qubits.
- **Stabilizers and syndromes:** checking for errors without measuring the encoded information itself.
- **Logical operators and code distance:** understanding how information is represented and how much protection a code provides.
- **Repeated checks and detector events:** using measurement history to identify inconsistencies when checks can also fail.
- **Lattice surgery:** performing logical operations by merging and splitting surface-code patches.
- **Decoding:** using detector events and a noise model to infer corrections.
- **Pauli frames:** tracking corrections classically instead of immediately applying physical gates.
- **Fault-tolerant computation:** protecting preparation, gates, storage, and readout, including operations that require decoded results to decide what happens next.
- **Logical failure rates:** measuring how reliably an encoded experiment preserves its intended result.

## Notebooks
Start with [Introduction to quantum computing (PDF)](output/pdf/tut0.pdf) for the fundamentals.

Read the notebooks in order. Basic Python and familiarity with quantum gates are helpful.

| Order | Written tutorial | Notebook | What it covers |
| --- | --- | --- | --- |
| 1 | [Quantum error correction (PDF)](output/pdf/tut1.pdf) | [Shor's code](shor_tutorial.ipynb) | Encoding, stabilizers, a lookup decoder, Pauli frames, and a memory experiment. |
| 2 | [Rotated surface codes and lattice surgery (PDF)](output/pdf/tut2.pdf) | [Surface codes and lattice surgery](surface_code.ipynb) | Rotated patches, noisy memory, and logical GHZ preparation using Loom and Stim. |
| 3 | [Fault-tolerant computation and decoding (PDF)](output/pdf/tut3.pdf) | [Decoding the surface code](decoder.ipynb) | A TQEC CNOT, detector error models, a simple lookup decoder, PyMatching, and Sinter. |

## Run the notebooks

Install Python 3.12 and [uv](https://docs.astral.sh/uv/), then run from the repository root:

```bash
uv sync
uv run jupyter lab
```

Open a notebook and run its cells from top to bottom. In VS Code, select the repository's `.venv` Python environment as the notebook kernel. Sampling cells generate random results, so counts and plots can change between runs.

The CNOT notebook creates local HTML files for its interactive viewers. These generated files are ignored by Git. Static figures used by the notebooks are in `assets/`.
