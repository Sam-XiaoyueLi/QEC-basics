# Written tutorials

These are the LaTeX sources from the Overleaf export supplied on 7 October 2026. Each tutorial is a standalone document.

| Order | PDF | Source | Topic |
| --- | --- | --- | --- |
| 1 | [Read PDF](../output/pdf/tut0.pdf) | [tut0.tex](tut0.tex) | Introduction to quantum computing |
| 2 | [Read PDF](../output/pdf/tut1.pdf) | [tut1.tex](tut1.tex) | Quantum error correction |
| 3 | [Read PDF](../output/pdf/tut2.pdf) | [tut2.tex](tut2.tex) | Rotated surface codes and lattice surgery |
| 4 | [Read PDF](../output/pdf/tut3.pdf) | [tut3.tex](tut3.tex) | Fault-tolerant computation and decoding |

## Build in Overleaf

Upload these files with the `figures/` directory intact. Select the tutorial you want as the main document and use XeLaTeX. `tut2.tex` includes `figures/diagrams.tex`.

The written tutorials and notebooks have separate numbering. The three notebooks cover Shor's code, surface codes and lattice surgery, and decoding, respectively.

GitHub and Overleaf are separate copies. Changes made on either side must be transferred explicitly. This source snapshot does not configure automatic synchronization.

## Rebuild the PDFs locally

From the repository root, using [Tectonic](https://tectonic-typesetting.github.io/):

```bash
mkdir -p output/pdf
for tutorial in tut0 tut1 tut2 tut3; do
  tectonic -X compile "overleaf/$tutorial.tex" --outdir output/pdf
done
```

Rebuild and commit the PDFs when updating the corresponding sources.
