# Project Brief

## Purpose

A beginner-friendly, hands-on learning repository for quantum error correction (QEC). The goal is to build intuition by working through concepts progressively, from classical error correction up to real quantum codes and tooling, with runnable notebooks at each stage.

## Learning sequence

1. **Classical repetition code** — the simplest error-correcting code, using only classical bits, to build intuition for redundancy and majority-vote decoding.
2. **Stabilizers and syndromes** — the quantum generalization of parity checks: stabilizer formalism and how syndromes reveal errors without collapsing the encoded information.
3. **Syndrome circuits** — concrete quantum circuits that measure stabilizers/syndromes.
4. **Noisy decoding** — decoding syndromes in the presence of realistic noise.
5. **Surface code with Stim, Loom, and Quantinuum Guppy** — applying the concepts to the surface code using real QEC tooling.

## Scope

- This repo is for learning and exploration, not production QEC software.
- Notebooks should be self-contained and readable by someone new to the topic, per the conventions in `CLAUDE.md`.
