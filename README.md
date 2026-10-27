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
Start with [Introduction to quantum computing (PDF)](qec_basic_notes/tut0.pdf) for the fundamentals.

Read the notebooks in order. Basic Python and familiarity with quantum gates are helpful.

| Order | Written tutorial | Notebook | What it covers |
| --- | --- | --- | --- |
| 1 | [Quantum error correction (PDF)](qec_basic_notes/tut1.pdf) | [Shor's code](shor_tutorial.ipynb) | Encoding, stabilizers, a lookup decoder, Pauli frames, and a memory experiment. |
| 2 | [Rotated surface codes and lattice surgery (PDF)](qec_basic_notes/tut2.pdf) | [Surface codes and lattice surgery](surface_code.ipynb) | Rotated patches, noisy memory, and logical GHZ preparation using Loom and Stim. |
| 3 | [Fault-tolerant computation and decoding (PDF)](qec_basic_notes/tut3.pdf) | [Decoding the surface code](decoder.ipynb) | A TQEC CNOT, detector error models, a simple lookup decoder, PyMatching, and Sinter. |

## Knowledge base

The [QEC knowledge base](qec_knowledge_base/README.md) collects concise references on QEC and quantum computing hardware, developed through study and discussion.

- [Gross code](qec_knowledge_base/gross-code/README.md) — Check patterns, logical-state preparation, logical operators and distance, parity-based CNOTs within and across blocks, decoded readout, and hardware constraints.

- [qLDPC codes](qec_knowledge_base/qldpc-codes/README.md) — Definitions, encoding efficiency, practical trade-offs, comparisons with other code approaches, and major companies' QEC work.

- [Quantum computing hardware](qec_knowledge_base/quantum-computing-hardware/README.md) — Physical zero/one states, preparation and gates, protection and coherence, a concise platform comparison, and research directions.

- [Decoders: Beyond Likelihood](qec_knowledge_base/decoders/README.md) — One physical error model used to explain MWPM, correlated matching and BeliefMatching, followed by advanced decoders and company approaches.

- [A denser planar surface code](qec_knowledge_base/denser-planar-surface-code/README.md) — Twist-defect packing, practical measurements, density comparisons, yoking assumptions, and computing with dense memory.

- [Color codes](qec_knowledge_base/color-codes/README.md) — Face checks, a seven-qubit example, transversal Clifford gates, and the promise and limits of Quantinuum's Helios experiment.

## Run the notebooks

Install Python 3.12 and [uv](https://docs.astral.sh/uv/), then run from the repository root:

```bash
uv sync
uv run jupyter lab
```

Open a notebook and run its cells from top to bottom. In VS Code, select the repository's `.venv` Python environment as the notebook kernel. Sampling cells generate random results, so counts and plots can change between runs.

The CNOT notebook creates local HTML files for its interactive viewers. These generated files are ignored by Git. Static figures used by the notebooks are in `assets/`.
