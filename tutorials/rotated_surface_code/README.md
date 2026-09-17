# Rotated surface code tutorial

An Overleaf-ready tutorial following the concise, equation-led style of the Shor notebook. It covers local stabilizer codes, rotated patches, boundaries, check schedules, error strings and charges, memory experiments, lattice surgery, and a parity-measurement CNOT with a ZX diagram.

## Open in Overleaf

1. Download `rotated-surface-code-overleaf.zip` from the repository's `output/overleaf` directory.
2. In Overleaf, choose **New Project → Upload Project** and select the ZIP.
3. Set the main document to `main.tex`. Use **pdfLaTeX** (standard packages only) or **XeLaTeX**.
4. Recompile. All figures are editable TikZ in `figures/diagrams.tex`; no external images, shell escape, Python, or bibliography build is needed.

The compiled preview is `output/pdf/rotated-surface-code-tutorial.pdf` at the repository root. The source can also be compiled with `latexmk -pdf main.tex` from this directory, or with `tectonic main.tex`.

## Conventions

- X checks and X patch edges: orange. Z checks and Z patch edges: teal.
- Boundary labels name the logical operator **along** the edge. An X edge absorbs Z-string endpoints; a Z edge absorbs X-string endpoints.
- Black dots in lattice figures are data qubits; letters mark checks.
- The CNOT example uses an ancillary **logical patch**, distinct from physical syndrome-measurement ancillas.
- The patch-level surgery figures intentionally omit physical bridge-qubit and interface-gate details; they are not executable hardware schedules.

## Review and validation

`review/claude-review.md` records the independent Claude review; `review/revisions.md` records the subsequent edits and checks. Reviewer advice is kept separate from the teaching text.

From the repository root, run:

```sh
uv run python tutorials/rotated_surface_code/validate.py
```

This checks the illustrated stabilizer supports, logical algebra, gate scheduling and actual syndrome extraction, all CNOT measurement branches, and the final ZX map. It does not simulate logical error rates or establish circuit-level distance.
