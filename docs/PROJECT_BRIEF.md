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

1. **Stim basics: measurements, parity checks, and syndromes** — a first runnable view of parity measurement using an ancilla.
2. **Classical 3-bit repetition code** — redundancy, code distance, syndrome tables, majority-vote decoding, and the distinction between detection and correction.
3. **Stabilizers and syndromes** — the quantum generalization of parity checks: stabilizer eigenvalues and how syndromes reveal errors without revealing the encoded information.
4. **Syndrome-extraction circuits** — concrete circuits that measure stabilizers with ancillas.
5. **Noisy decoding** — decoding syndromes in the presence of realistic noise.
6. **Surface code with Stim, Loom, and Quantinuum Guppy** — applying the concepts to a practical quantum code and modern tooling.

## Scope

- Notebooks are the primary teaching artifact and must be executable from top to bottom.
- The README is the public entry point and should stay aligned with the learning sequence.
- Repository-wide authoring rules live in [CLAUDE.md](../CLAUDE.md).
