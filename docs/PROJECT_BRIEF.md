# Project Brief

## Purpose

QEC Basics is a public, beginner-friendly, hands-on learning repository for quantum error correction (QEC). Its goal is to help a reader gain the conceptual and practical foundation needed to understand modern QEC tools and codes.

The repository must work for someone who arrives through the README alone. They should not need access to the original author’s notes, prompts, conversations, or development history.

## Intended reader

The intended reader:

- has basic Python literacy;
- is new to QEC and may only have a light introduction to qubits and quantum gates;
- benefits from concrete examples, diagrams, prediction questions, and small exercises;
- wants to understand both the intuition and the operational meaning of syndromes, stabilizers, and decoding.

The repository is not production software and does not aim to replace a full quantum-computing curriculum.

## Instructional approach

Each notebook should:

1. state its purpose, prerequisites, learning objectives, and expected outputs;
2. introduce concepts before notation, circuits, or code;
3. make the reader predict outcomes before observing them;
4. use executable examples to verify the explanation;
5. distinguish what is guaranteed by a code from what is merely likely under a noise model;
6. close with a checkpoint and an explicit connection to the next notebook.

Keep the narrative self-contained. Define new terms at first use and avoid referring to unstated earlier discussion. Existing learner answers and completed TODO work are preserved.

## Learning sequence

The full, current roadmap lives in [README.md](../README.md) under `## Learning roadmap` — README is canonical; this section only summarizes the arc:

1. **Stim basics** and **2. the classical 3-bit repetition code** — parity measurement with an ancilla, then redundancy, code distance, and majority-vote decoding.
2. **Stabilizers, syndromes, and parity measurements** — the quantum generalization of parity checks.
3. **Classical linear codes and the Hamming code**, then the **stabilizer/CSS/Steane trilogy** (Shor's code, CSS construction, the Steane code, logical operators, code distance, degeneracy, quantum parity-check matrices, and coset decoding) — each notebook consolidates a specific Arthur Pesah article.
4. **Noisy Steane-code decoding**, then the **surface code**: foundations, detectors and decoding with Stim and Loom.
5. **Hardware-aware QEC with Quantinuum Guppy** — applying the concepts with modern tooling.

## Scope

- Notebooks are the primary teaching artifact and must be executable from top to bottom.
- The README is the public entry point and should stay aligned with the learning sequence.
- Repository-wide authoring rules live in [CLAUDE.md](../CLAUDE.md).
