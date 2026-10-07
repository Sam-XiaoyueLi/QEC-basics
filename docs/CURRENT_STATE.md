# Current state

## Publication — 7 October 2026

The current collection comprises `shor_tutorial.ipynb`, `surface_code.ipynb`, and `decoder.ipynb`, together with written sources in `overleaf/` from the supplied 7 October export. The README is the current learning roadmap.

The decoder notebook was executed in a fresh kernel after its latest review. This publication adds documentation and LaTeX sources without changing notebook code. The two archive branches retain the older notebook collections.

The notes below describe an earlier revision and do not describe the current surface-code notebook.

## Surface-code revision — 23 September 2026

Author requirements: use Loom without Stim examples; closely follow the written tutorial, especially the measurement sequence and why it matters. The reference is the fresh-export `Overleaf/Current/tut2.tex` (Tutorial 03: Rotated Surface Codes). No Overleaf sources or Shor content were changed.

The notebook now uses Loom 0.4.0 operators, circuits, and its bundled Clifford simulator. NumPy supports exact state/operator algebra. It matches bottom-up row numbering, horizontal logical X / vertical logical Z, the distance-five neighboring-check orders X:5,0,6,1 and Z:6,7,1,2, and the distance-three side-by-side seam. It includes logical states, scheduled checks, hook propagation, error recovery, ideal merge/split frames, logical ZX, and the three-measurement CNOT. The former external-simulator noisy memory sweep and separate factory AuxCNOT example were removed to follow the tutorial's scope; illustrative repeated-readout histories remain explicitly labeled as prescribed examples.

Validation completed:

- Fresh-kernel execution of all 39 cells, with executed outputs saved.
- Visual inspection of all five figures: patch layouts, good/bad neighboring circuits, hook orientation, and seam geometry.
- The good CNOT core matches sequential checks on all 256 basis inputs. A collision-free counterexample differs and has intrinsically random check readouts in Loom.
- Full distance-three and distance-five four-layer schedules have no collisions, including boundary gates.
- The full scheduled distance-three round reports the expected syndromes for all 27 single-qubit errors. An additional check covers all 108 combinations with four logical cardinal states, including preservation of the expected logical observable.
- Lookup corrections restore every single-qubit Pauli error; a two-qubit logical-error counterexample is explicit.
- All merged checks commute, and measuring an incompatible old boundary check makes the next seam readout random.
- An additional Loom check verified all 128 seam/bridge branches with both inputs entangled to reference qubits: the split correction restores all old checks and the expected projected logical/reference correlations.
- Direct logical ZX agrees with the basis-change construction on the demonstrated input.
- The logical CNOT runs in Loom, and the complete matrix identity holds for all eight outcome branches.

Limits: ideal measurements and selected state-preparation branches. No noisy decoder benchmark, compiled physical CNOT fault-distance claim, or proof of fault tolerance. The mixed ZX demonstration is at the logical level, not a physical twisted seam. The notebook remains a draft awaiting author and independent review.

Publish only the reviewed notebook and necessary reader runtime changes to `main` when explicitly requested; keep development-only guides on the work branch.
