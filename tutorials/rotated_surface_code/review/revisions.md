# Review and revision record

The author requested a complete Overleaf draft, an independent Claude review, and a second editing pass. No existing notebook was changed.

## Independent review

Claude Code reviewed the complete LaTeX and TikZ source with tools disabled, using the request saved in `request.md`. Its response is preserved verbatim in `claude-review.md`. It reviewed source and coordinates, not the rendered PDF. It found no substantive physics error and returned the following items; Codex assessed and applied them all.

| ID | Action taken |
| --- | --- |
| E1 | Moved the elaborated logical-X boundary label to the bottom edge, matching the drawn representative. Both horizontal edges support logical X; this resolves visual ambiguity rather than changing the code. |
| R1 | Corrected the conventional-lattice highlight to surround one complete bulk Z plaquette and explained it in the caption. |
| R2 | Added an arrowhead to every transition in the N/Z schedule, with spacing around the numbered corners. |
| R3 | Replaced the ambiguous term “Z targets” with “data qubits touched”; data are CNOT controls for a Z check. |

## Additional editing and visual pass

- Added a shared-support inset showing qubits 1 and 6, making the commutation example visual.
- Removed crowded repeated edge labels from the small surgery panels; colors retain the boundary convention established in the full patch figure and table.
- Shortened the ancilla readout label to fit within its patch.
- Specified that the CNOT outcome bits are decoded logical outcomes interpreted in the incoming Pauli frame.
- Removed caption hyperlink warnings and inspected the compiled pages for layout, math, labels, and clipping.

## Verification

- `uv run python tutorials/rotated_surface_code/validate.py` passes. It verifies d=3 and d=5 stabilizer commutation and independence, the logical anticommutation relation, the illustrated two-error syndrome, absence of simultaneous data-qubit gate collisions, and actual noiseless Stim extraction of every single-qubit X/Y/Z syndrome in both logical bases.
- Explicit 4-by-4 Kraus-map checks pass for all eight outcomes of the ancillary-patch CNOT. Every corrected branch is proportional to CNOT, with probability 1/8 for arbitrary input. The two-spider tensor contraction also reproduces CNOT up to its scalar.
- The final LaTeX compiles using Tectonic 0.17.0 (XeTeX) with no warnings, undefined references, or overfull/underfull boxes. The self-contained Overleaf ZIP is compiled separately after extraction. The PDF has 11 pages and 9 vector diagrams.
- These checks are author validation. They do not establish circuit-level distance, simulate logical error rates, or verify a physical surgery-gate schedule. No distance-verification section was added.

## Scope retained

The spoken example “Oxenoid” is interpreted as the ancilla-mediated CNOT in the agreed story plan. The tutorial ends at that worked example and its ZX representation. Boundary names are explicitly defined; “Pauli charge” is used for syndrome endpoint content and distinguished from ZX spiders. The ZIP is ready to upload to Overleaf; no online Overleaf project has been created.

Reviewed source SHA256 values (before the second pass):

```text
main.tex: 3c494fe8525518490ba25557a1149b321f69048b813d255e4ba54746a88db352
figures/diagrams.tex: 1f24dda8cd4a99eaad68fd5092dc082cf04760563957bcd133322c04785d27e3
```
