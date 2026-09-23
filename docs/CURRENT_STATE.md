# Current state

- `main` contains the published Shor notebook and reader runtime files.
- `codex/surface-code-tutorial` contains the completed `surface_code.ipynb` draft and the development tools and guides.
- `docs/NOTEBOOK_STYLE.md` distills the Shor notebook's style into reusable authoring guidance; `CLAUDE.md` links to it.
- The two `codex/archive/...` branches preserve the older notebook collections.
- The Overleaf project remains in the sibling `Overleaf/` folder, outside this Git repository.

## Surface-code draft validation — 23 September 2026

The notebook has 49 cells. It uses Stim 1.16.0, PyMatching 2.4.0 and Loom 0.4.0. The whole notebook executed without cell errors in a fresh kernel, with verified outputs saved. The memory sweep uses 20,000 shots per point over five rounds, for two distances and two readout bases. Figures and representative rendered Markdown/equations were visually inspected.

Checks passed:

- All stabilizer commutations and logical-Pauli relations in the stated convention.
- Ideal lookup recovery for all 27 single-qubit Pauli errors.
- An additional check confirmed that the serial ancilla round preserves all 108 error eigenstates obtained from those errors on four logical input states.
- Generated memory check supports agree with the numbered patch after relabeling; CNOT layers have no qubit collisions.
- The seam product equals logical ZZ; the modified merged checks commute.
- An additional exact stabilizer check tested every one of 128 seam/bridge outcome combinations with both logical inputs entangled to reference qubits. After the stated frame, each branch equals the intended ZZ projection.
- The full two-logical-qubit matrix identity holds for all eight ideal CNOT branches.
- The compiled Loom circuit passes all four Z-basis truth-table cases and Bell-state correlations in both X and Z bases.

Limits: noisy performance is demonstrated for memory only. Seam measurements and CNOT demonstrations are ideal/noiseless. This is a completed draft, not an independent review or a proof of the compiled surgery circuit's fault distance. The Shor notebook was not edited.

Next: author review of the surface-code draft, then independent findings-only review. Publish only the reviewed notebook and necessary reader runtime changes to `main` when explicitly requested; keep development-only guides and tooling on the work branch.
