# Current State

This repository was rebuilt around a reading-led roadmap (see [README.md](../README.md) `## Learning roadmap`, mirrored in [LEARNING_PATH.md](LEARNING_PATH.md)). The prior roadmap's notebooks covering ancilla syndrome-extraction circuits and noisy repetition-code decoding are preserved for reference in [`archive/`](../archive/README.md); their topics now belong later in the sequence, applied to the Steane and surface codes instead of the repetition code.

**Completed:**

- `01_stim_basics.ipynb` — introductory Stim and parity measurement.
- `02_classical_3bit_repetition_code.ipynb` — classical repetition code, code distance, detection, and correction.
- `03_stabilizers_and_syndromes.ipynb` — bridges the classical parity checks to the quantum stabilizers on the 3-qubit repetition code.
- `04_classical_linear_codes_and_hamming.ipynb` — Hamming weight/distance, the $[7,4,3]$ Hamming code's $G$/$H$ matrices (pure-Python GF(2) linear algebra), syndrome decoding, and a distance-3 verification, ending with the classical-parity-check-to-quantum-stabilizer bridge.
- `05_shor_code_css_and_steane_code.ipynb` — Shor's $[[9,1,3]]$ code (built and verified computationally, including degeneracy and an exhaustive distance proof), the general CSS construction, and the Steane $[[7,1,3]]$ code built directly from notebook 04's Hamming $H$.
- `06_logical_operators_distance_and_degeneracy.ipynb` — codespace projector and $k=n-m$, centralizer/stabilizer-group/logical-operator relationships, logical equivalence, and a single reusable `code_distance` routine applied to the repetition, Shor, and Steane codes.
- `07_quantum_parity_check_matrices_and_decoding.ipynb` — binary symplectic representation, the quantum parity-check matrix (including the CSS block form), syndromes as matrix-vector products, decoding by error cosets, and a Tanner-graph view — all reproducing notebooks 04–06's results by pure GF(2) linear algebra.
- `08_noisy_steane_code_decoding.ipynb` — reuses notebook 04's Hamming decoder unmodified for both the Steane code's $X$- and $Z$-error channels, an exact closed-form failure-probability formula validated against Monte Carlo, and a real Stim circuit (`X_ERROR`/`Z_ERROR`/`MPP`) reproducing the same syndromes.
- `09_surface_code_foundations.ipynb` — data/measurement qubit roles, $X$-/$Z$-type checks, syndrome defects, and logical-operator strings, built from Stim's own `surface_code:rotated_memory_z` generator (cited to Fowler et al. 2012, sections III–VII) and a $n=d^2$ scaling table.
- `10_surface_code_detectors_and_decoding_with_stim_and_loom.ipynb` — a real Stim detector-error-model → PyMatching decoding pipeline, a threshold-style distance comparison (3/5/7) showing bigger codes winning below threshold, and the identical pipeline applied to a Loom-compiled repetition-code circuit.
- `11_hardware_aware_qec_with_quantinuum_guppy.ipynb` — the repetition code's encode/inject-fault/syndrome/correct workflow as a real, locally-emulated Guppy program, with real-hardware submission scoped to one clearly-marked, non-executed optional cell.

Every notebook from 03 onward includes prediction questions placed inline and non-blank TODO exercises gathered under a final `## Exercises` heading (per [CLAUDE.md](../CLAUDE.md)'s authoring rules), and was executed top to bottom with `uv run jupyter nbconvert --to notebook --execute --inplace` with zero errors.

**Dependencies:** `pymatching` and `el-loom` (Loom's PyPI name) were added to `pyproject.toml` for notebook 10; `guppylang` for notebook 11. All three are required by the reading routine above and are installed via `uv sync`.

**Next:** work through notebooks 04–11 as a learner (predictions, TODOs) before any further generation — this repository's authoring rule is to preserve, not regenerate, completed learner work. No new notebook is currently planned beyond the 11-step roadmap in [README.md](../README.md).
