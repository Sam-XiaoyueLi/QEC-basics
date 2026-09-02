# Current State

**Completed:**

- `01_stim_basics.ipynb` — introductory Stim and parity measurement.
- `02_classical_3bit_repetition_code.ipynb` — classical repetition code, code distance, detection, and correction.
- `03_stabilizers_and_syndromes.ipynb` — bridges the classical parity checks to the quantum stabilizers $Z_0Z_1$, $Z_1Z_2$ on the 3-qubit repetition code; defines stabilizer, stabilizer group, code space, syndrome, and logical operator; builds the syndrome table for `no error`/$X_0$/$X_1$/$X_2$ via Pauli matrices, explains why $X_0$ and $X_1$ need both stabilizers to be distinguished, and cross-checks with a minimal (explicitly non-fault-tolerant) direct-measurement Stim example.
- `04_syndrome_detection_circuits.ipynb` — builds the real ancilla-based syndrome-extraction circuit (3 data qubits + 2 ancillas) for $Z_0Z_1$/$Z_1Z_2$, with a rendered circuit diagram and a per-qubit role table; establishes the measurement-bit-to-eigenvalue convention; separates extraction from decoding and correction; notes the idealized/non-fault-tolerant scope.
- `05_noisy_repetition_code_decoder.ipynb` — simulates independent $X$ noise with Stim's `X_ERROR`, applies the syndrome lookup-table decoder, plots logical vs. physical failure probability across $p \in [0.01, 0.5]$, explains the $p=0.5$ break-even point, and shows (via Pauli-matrix eigenvalues) that the code is blind to phase-flip ($Z$) errors.

Each of notebooks 03–05 includes 3 prediction questions and 2 TODO exercises (unfilled — learner-owned), and was executed top to bottom with `uv run jupyter nbconvert --to notebook --execute --inplace`, completing in a few seconds each.

**Recommended order for tomorrow:**

1. Work through 03 → 04 → 05 as a learner (fill in predictions, TODOs, and the closed-notebook checklists) before generating new material — this repository's authoring rule is to preserve, not regenerate, completed learner work.
2. Next new notebook: surface code with Stim, Loom, and Quantinuum Guppy (notebook 06+), per the learning sequence in [PROJECT_BRIEF.md](PROJECT_BRIEF.md).

See [PROJECT_BRIEF.md](PROJECT_BRIEF.md) for the full learning sequence this fits into.
