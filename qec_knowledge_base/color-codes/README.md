# Color codes: checks, transversal gates, and the Helios experiment

Last updated: 2026-10-28

## Two checks on each face

A 2D **color code** puts data qubits on the vertices of a lattice whose faces can be coloured red, green and blue, with neighbouring faces having different colours. Three edges meet at each bulk vertex. The colours describe geometry, not different physical states of an ion.

**A face is a local checking region; a patch is the whole code block.** A standard triangular patch has three differently coloured boundaries and encodes one logical qubit. “Honeycomb” instead describes its internal tiling. Color codes need not be triangular: other tilings, patches with holes and periodic surfaces are possible. Their logical-qubit count depends on boundaries and topology; the standard color code on a torus encodes four logical qubits. [Foundations, code counting and triangular boundaries](https://arxiv.org/html/quant-ph/0605138v3)

![Triangular color-code patches at distances 3, 5 and 7, with data qubits at vertices and red, green and blue faces.](assets/triangular-patches.png)

**Figure 1.** Larger patches protect one logical qubit using more data qubits. Each coloured region is one face, and every circle is a data qubit. Measurement helpers are omitted. The triangular drawing describes the code connections; ions need not occupy these positions in the trap.

On each face $f$, measure both

$$
S_f^X=\prod_{i\in f}X_i,\qquad S_f^Z=\prod_{i\in f}Z_i.
$$

For a four-qubit face these are $X_1X_2X_3X_4$ and $Z_1Z_2Z_3Z_4$. In the triangular honeycomb family, bulk faces have six qubits and truncated boundary faces have four. These are **CSS stabilizer codes**: separate all $X$ and all $Z$ checks define the protected subspace through their $+1$ eigenvalues.

The checks commute because their supports overlap on an even number of qubits. Exchanging $X$ and $Z$ on one shared qubit gives a minus sign; an even number of such signs cancels. This applies both to the two checks on the same even-sized face and to checks on adjacent faces sharing an edge.

A physical $X_i$ anticommutes with every $Z$ check containing qubit $i$, reversing those check signs while leaving the $X$ checks unchanged. A bulk vertex touches three faces, so one $X$ error flips three neighbouring $Z$ checks. A $Z_i$ error similarly flips neighbouring $X$ checks. These signs reveal error information without revealing the unknown logical amplitudes. Repeated, noisy check measurements require a [decoder using the measurement history](../decoders/README.md#from-syndrome-to-correction).

Color codes were introduced by Bombín and Martin-Delgado in [*Topological Quantum Distillation* (2006)](https://arxiv.org/abs/quant-ph/0605138). Quantinuum implemented an established code family.

## A seven-qubit example

The smallest triangular color code is the Steane $[[7,1,3]]$ code: seven data qubits encode one logical qubit with distance three. One valid numbering gives these six independent checks:

| Face | $X$ check | $Z$ check |
| --- | --- | --- |
| A | $X_1X_2X_3X_4$ | $Z_1Z_2Z_3Z_4$ |
| B | $X_1X_2X_5X_6$ | $Z_1Z_2Z_5Z_6$ |
| C | $X_1X_3X_5X_7$ | $Z_1Z_3Z_5Z_7$ |

![The numbered seven-qubit color code: face A checks qubits 1, 2, 3 and 4; X1 flips all three Z checks; X5X6X7 leaves all Z checks positive.](assets/seven-qubit-checks.png)

**Figure 2.** The same patch shows a face check, a detectable single-qubit error and an undetectable logical operator. Faces A and B share qubits 1 and 2, so their opposite-type checks overlap twice and commute.

Each face has four qubits; each pair shares two. Six independent constraints leave a two-dimensional code space, enough for one logical qubit.

Write a syndrome bit as 1 when a check sign flips. Reading the $Z$ checks in order A, B, C, the errors $X_1,\ldots,X_7$ produce **111, 110, 101, 100, 011, 010, 001**. Thus ideal checks distinguish every single-qubit $X$ error. The $X$ checks provide the corresponding information for $Z$ errors; a $Y$ error affects both sets.

Logical Pauli representatives are

$$
\bar X=X_1X_2X_3X_4X_5X_6X_7,\qquad
\bar Z=Z_1Z_2Z_3Z_4Z_5Z_6Z_7.
$$

They commute with all checks and anticommute with each other. Multiplying $\bar X$ by face A's $X$ check gives the equivalent representative $X_5X_6X_7$. It changes the logical information without changing any check sign. No one- or two-qubit Pauli has that property, so the distance is three. The ability to correct one error assumes suitable syndrome information; noisy extraction circuits need their own fault-tolerant design.

## One logical block and its data cost

For the triangular honeycomb family used here, the notation $[[n,1,d]]$ means $n$ data qubits, one logical qubit and distance $d$, with

$$
n=\frac{3d^2+1}{4},\qquad d\text{ odd}.
$$

A standard rotated surface-code patch also encodes one logical qubit, with $d^2$ data qubits:

| Distance | Triangular honeycomb color code | Rotated surface code |
| --- | --- | --- |
| 3 | 7 data qubits | 9 data qubits |
| 5 | 19 data qubits | 25 data qubits |
| 7 | 37 data qubits | 49 data qubits |

This is an **equal-distance, data-only comparison**. Equal distance does not mean equal logical reliability: check circuits, noise and decoding differ. Measurement helpers, routing, operation time and magic-state production also contribute to the total cost. [Color-code parameters](https://arxiv.org/html/2610.24077v1), [surface-code counting](../denser-planar-surface-code/README.md#separate-rotated-patches-what-is-being-counted)

“One patch, one logical qubit” describes these standard layouts, rather than either entire code family. Different boundaries, holes or topology can support several logical qubits in color and surface codes. The [dense surface-code notes](../denser-planar-surface-code/README.md#twist-defects-shared-information-rather-than-three-isolated-squares) give a concrete example of several logical qubits sharing one connected region.

## What makes the gates special

A **transversal gate** acts separately on each qubit of a block, or on corresponding qubit pairs across blocks. Suitable triangular color codes support a full **Clifford** gate set this way. Clifford gates map Pauli operators to Pauli operators under conjugation and can be generated by $H$, $S$ and CNOT. The phase gate $S$ leaves $|0\rangle$ unchanged and multiplies $|1\rangle$ by $i$.

- **Hadamard:** $HXH=Z$ and $HZH=X$. Applying $H$ to every data qubit exchanges each face's $X$ and $Z$ checks, and exchanges $\bar X$ with $\bar Z$. It therefore implements logical $H$.
- **Phase:** $SXS^\dagger=Y=iXZ$. Physical phase gates must also preserve the check signs. Applying the same $S$ everywhere is insufficient for a six-qubit face, because $i^6=-1$. A honeycomb patch is bipartite: its vertices split into two subsets so every edge joins different subsets. Apply $S$ on one subset and $S^\dagger$ on the other. Each face has equal numbers of the two, cancelling the unwanted phase. The pattern implements logical $S$ or $S^\dagger$, with the choice fixed by its action on the logical operators. In the seven-qubit numbering above, $S$ on 1, 4, 6, 7 and $S^\dagger$ on 2, 3, 5 implements logical $S$.
- **CNOT:** apply physical CNOTs from qubit $i$ in the control block to qubit $i$ in an identical target block. Since $X_c\mapsto X_cX_t$ and $Z_t\mapsto Z_cZ_t$, the logical operators transform exactly as for a logical CNOT, while stabilizers map to stabilizers.

![Seven separate CNOTs connect matching qubit numbers in two code blocks; the third pair is highlighted to show the limited spread of one fault.](assets/transversal-cnot.png)

**Figure 3.** Two $[[7,1,3]]$ blocks contain **14 data qubits**. Their logical CNOT uses **seven physical CNOTs**, one for each matching pair. The rows group qubits by block; each vertical line is a CNOT, with a control dot and a target plus sign.

For two identical blocks with $n$ data qubits each, the construction uses $n$ matching CNOTs. This is the gate count. At the abstract circuit level, the disjoint pairs can all run in one parallel layer, giving CNOT depth one. A real device may serialize some pairs, transport ions or compile each CNOT into native entangling gates and single-qubit rotations. Gate count, parallel depth and elapsed hardware time are different quantities.

For a pairwise CNOT, a fault may affect both blocks, but each qubit participates in just one pair. It cannot fan out through that gate into several qubits of either block. This limits error propagation; physical gates can still fail and repeated correction remains necessary. The [foundational construction](https://arxiv.org/html/quant-ph/0605138v3) explains the lattice conditions behind these gates.

The benefit is a simple implementation of many logical operations. Surface codes also implement Clifford gates, using methods including [lattice surgery](../../surface_code.ipynb), patch transformations and suitable transversal operations. Color codes offer a different balance: fewer data qubits at a given distance and convenient Clifford gates, but more demanding check circuits and decoding. A single bulk error's three-check signature already goes beyond the simplest two-endpoint matching picture. Hardware connectivity, physical error rates, extraction faults and routing costs determine which balance works best.

The full Clifford group does **not** provide arbitrary quantum computation. In particular, this 2D code does not supply a transversal $T$ gate. This gate leaves $|0\rangle$ unchanged and multiplies $|1\rangle$ by $e^{i\pi/4}$. Universal computation needs an additional resource, such as a prepared **magic state** consumed in a measurement-based $T$-gate protocol.

## What Quantinuum measured in October 2026

The [Lavasani et al. preprint, submitted 16 October 2026](https://arxiv.org/html/2610.24077v1), tested the triangular honeycomb family on the Helios trapped-ion processor. Its memory experiments include syndrome helpers as well as the data qubits counted above.

For memory, the experiment prepared each of the six logical Pauli eigenstates ($|0\rangle$, $|1\rangle$, $|\pm\rangle$, $|\pm i\rangle$), performed 20 correction cycles, then measured in the corresponding logical basis. The primary Tesseract-decoded estimates were:

| Distance | Data qubits | Total qubits per memory experiment | Logical error per cycle |
| --- | --- | --- | --- |
| 3 | 7 | 13 | $5.5^{+0.4}_{-0.4}\times10^{-4}$ |
| 5 | 19 | 37 | $3.8^{+1}_{-0.8}\times10^{-5}$ |
| 7 | 37 | 73 | $5^{+4}_{-2}\times10^{-6}$ |

These are Table 1 estimates with **68% Wilson confidence intervals**, statistical intervals for the underlying failure probability under the sampling model. They do not include every possible systematic error or establish how the device will behave over much longer runs.

To read $5^{+4}_{-2}\times10^{-6}$, first take the central value $5\times10^{-6}=0.000005$. The upper endpoint is $(5+4)\times10^{-6}$ and the lower endpoint is $(5-2)\times10^{-6}$. Multiply probabilities by 100 to obtain percentages. The unequal $+4$ and $-2$ express an asymmetric interval, common with rare-event counts. Applying the same arithmetic to all three rows gives:

| Distance | Central probability per cycle | Central percentage | Interval in percent, from the rounded values above |
| --- | --- | --- | --- |
| 3 | 0.00055 | 0.055% | 0.051–0.059% |
| 5 | 0.000038 | 0.0038% | 0.0030–0.0048% |
| 7 | 0.000005 | 0.0005% | 0.0003–0.0009% |

The fitted suppression for a distance increase of two was $\Lambda=12^{+3}_{-2}$; the individual adjacent ratios need not equal 12. This is evidence that, for these circuits and hardware conditions, extra protection outweighed the extra opportunities for faults.

At distance seven there were **3 logical failures in 29,000 runs**, each containing 20 cycles. The paper estimates the per-cycle rate as

$$
p_L\approx\frac{3/29000}{20.5}\approx5.0\times10^{-6},
$$

The whole-run failure fraction is $3/29000$, about **0.0103% per 20-round run**. Dividing by 20.5 gives the approximate **per-cycle** estimate; the extra half-cycle accounts for state preparation. This normalization assumes rare failures and is not a separately measured decay curve over many run lengths. Three failures constrain the rate only loosely: one extra failure would change the raw count by a third. This was not one continuous million-round computation; the [company's “one million operations” framing](https://www.quantinuum.com/blog/quantinuum-closes-in-on-one-million-error-free-operations) extrapolates from a small per-cycle error estimate.

The computation test was **two-qubit Clifford randomized benchmarking**: random logical Cliffords followed by an inverse sequence, so ideal output is known. It tested distances three and five; two distance-seven blocks exceeded the hardware's qubit capacity. At distance five, the fitted error was $7^{+3}_{-3}\times10^{-5}$ **per logical two-qubit Clifford**, with correction after every seven logical Cliffords. This is a compiled benchmark operation, not a bare physical CNOT or a memory cycle. Its improved performance with distance supports this tested Clifford workload, rather than establishing arbitrary universal computation. [Paper, Clifford randomized benchmarking](https://arxiv.org/html/2610.24077v1)

The useful evidence is the combination of declining memory error with distance and improved encoded Clifford performance. A small memory number alone would not show that logical gates preserve that protection. The per-cycle memory estimate, whole-run failure fraction and error per logical Clifford answer different questions and should not be interchanged.

## Why this is a useful hardware match

The result combines **hardware, code, circuits and decoding**. The [Helios component study](https://arxiv.org/abs/2511.05465) documents accurate gates and readout, and transport-enabled connectivity: ions can be moved to the operation regions needed for different partners. This makes matching-pair logical CNOTs and changes of qubit roles accessible. Transport and cooling still cost time and introduce faults; a code's abstract connectivity does not remove those costs.

**Leakage** means population has left the two energy levels chosen as $|0\rangle$ and $|1\rangle$. Helios uses two hyperfine levels of a barium ion, with six nearby levels into which population can leak. A leaked ion is still present, but ordinary qubit gates no longer act on it as intended. It can repeatedly disturb interaction partners. The experiment combines two remedies:

1. **Optical repumping** returns leaked population to the computational levels. It does not recover the original unknown state or identify a flagged erasure. It converts much of the persistent leakage into errors ordinary qubit QEC can handle.
2. **SWAP-superdense extraction** exchanges data and helper roles, allowing previous data carriers to be measured and reset. The rotating schedule refreshes every data carrier within three cycles, removing leakage that survives repumping. On Helios, the SWAP in this construction can be implemented through software relabeling alongside the chosen interaction schedule.

Adding optical repumping to the circuit-level leakage-removal scheme improved observed logical error rates by roughly **4× at distance three and 8× at distance five**. This controlled comparison directly supports the value of leakage management. It does not attribute the entire result to repumping. [Experiment, leakage reduction and Fig. 2](https://arxiv.org/html/2610.24077v1)

Preparation and extraction must also avoid turning one circuit fault into an uncorrectable data error. The experiment initializes data to zero, measures the $X$ checks with a **Bell-flag preparation circuit**, then applies a transversal Clifford to select the logical input state. Flag outcomes provide extra information about potentially spreading faults. Repeated extraction detects subsequent faults, including unreliable measurement outcomes. The superdense and data/helper-exchange ideas build on [earlier extraction circuits](https://arxiv.org/abs/2312.08813) and [CXSWAP-based designs](https://arxiv.org/abs/2510.00370). A decoder must interpret the correlations produced by the actual circuit and noise model, rather than only the drawn lattice.

### Comparison with superconducting hardware

On a planar superconducting chip, local couplers constrain which qubits can interact directly. More involved extraction and inter-block gates can therefore need extra scheduling or routing. Faster gates and extraction clocks reduce elapsed time per operation, but also leave less wall-clock time for classical processing to keep up. Leakage into higher transmon levels, measurement faults and data-qubit idle noise during measurement/reset all matter. The [hardware notes](../quantum-computing-hardware/README.md#superconducting-qubits) explain the physical encoding.

Color codes are viable on this platform too. [Lacroix et al. (2025)](https://www.nature.com/articles/s41586-025-09061-4) demonstrated distance-three-to-five error suppression, transversal single-qubit Clifford benchmarking, magic-state injection with post-selection, and logical teleportation by lattice surgery on a superconducting processor. Thus trapped ions are a favourable match for some color-code operations, rather than a requirement for the code. Cross-platform error rates change the hardware, circuits, clocks and decoders together; they do not isolate a color-code advantage over a surface code.

## Decoding and the remaining computation gap

All decoding in the Helios study was **offline**. Four approaches were tested on recorded memory data:

| Decoder | How it infers a correction or logical outcome | Distance-seven failures, out of 29,000 runs |
| --- | --- | --- |
| **Tesseract** | Google Quantum AI's A* search over fault subsets, with pruning, for a most likely error explanation. | 3 |
| **Frontier** | Pruned dynamic programming: merge compatible partial explanations and retain a limited set of promising states. | 3 |
| **CNN** | A convolutional neural network learns local patterns across space and time. | 3 |
| **Round-token transformer** | Encodes each extraction round as learned numerical features and combines information across rounds. | 5 |

[Tesseract paper](https://arxiv.org/abs/2503.10988), [Frontier paper by Leverrier and Urbanke](https://arxiv.org/abs/2606.20513), [experiment, Table 1 and methods](https://arxiv.org/html/2610.24077v1).

Tesseract and Frontier used a **Stim detector error model** built from a simplified stochastic Pauli model of Helios faults. The neural decoders trained on emulator-generated circuits and were applied to hardware records without further fine-tuning. Thus the decoder is an important part of the result, but success also depends on how well its model or training data captures the circuit's actual faults. Equal counts of three failures do not establish equivalence: they may involve different shots, statistical power is limited, and performance differs at other distances. The [decoder notes](../decoders/README.md#beyond-matching-and-what-companies-build) explain the underlying inference trade-offs.

Separate **streaming timing tests** supplied recorded syndromes one round at a time. Neural timings measured isolated GPU computation on an NVIDIA H100; Frontier's WebAssembly timings ran on a laptop. These tests support feasibility, but exclude the full communication and control path needed for live feedback. Tesseract was the primary accuracy reference, not an integrated real-time decoder in this study.

### Why correction can be deferred

A **Pauli frame** is a classical record of corrections that would otherwise be applied as physical $X$, $Y$ or $Z$ gates. Clifford gates preserve this description. For example, an unapplied $X$ before $H$ becomes an unapplied $Z$ after it, because $HX=ZH$. At a final $Z$ measurement, an unapplied $X$ simply reverses the interpretation of the measured bit.

Consequently, memory and fixed Clifford benchmarks can keep extracting syndromes while postponing decoding and interpreting the final measurement afterward. This is a valid way to assess their logical performance: physical recovery gates need not occur after every round. Neither the decoder nor repumping learns the unknown logical state. [Deferred correction and frames](https://arxiv.org/abs/1704.06662)

Adaptive computation adds deadlines. A later measurement basis or gate may depend on a decoded result, as in a magic-state-based $T$ protocol. That information must arrive before the dependent action, or the machine needs a protocol that buffers or otherwise handles the delay. Sustained decoder throughput, difficult-case latency, communication and controller scheduling all matter. Offline success and a fast isolated decoder do not establish this integrated feedback path.

### From protected components to a useful computation

The demonstrated memory scaling and encoded Clifford performance are substantive progress toward fault-tolerant computation. This experiment does not yet integrate all of the following: many interacting logical qubits, longer runs that test rare failures and drift, live adaptive decoding, high-quality magic-state supply and $T$ injection, and below-threshold full Clifford + $T$ workloads. Some ingredients have been demonstrated in other experiments; the challenge is to combine them reliably at scale.

A practical comparison must match a complete workload and target success probability, counting data and helpers, routing, execution time, classical control and non-Clifford resource production. Compact blocks and transversal Clifford gates can help, while extraction and decoding can offset those gains. [Circuit studies](https://arxiv.org/abs/2312.08813) likewise find that relative code costs depend on noise and decoder assumptions. The company's Apollo 2029 target remains a [roadmap](https://www.quantinuum.com/blog/quantinuum-closes-in-on-one-million-error-free-operations). This October experiment is separate from the September Helix work in the [qLDPC industry overview](../qldpc-codes/README.md#what-major-companies-are-doing).

## Software implications

For QEC software teams, including Entropica, the results suggest several opportunities. These are software design implications, rather than measured improvements from this experiment. Hardware-aware fault-tolerant compilation can jointly choose extraction schedules, transport, role exchanges and correction intervals. Common circuit/decoder benchmarks can compare accuracy and latency on the same noise model and recorded syndromes. End-to-end integration can test when decoded information actually reaches a dependent gate, rather than measuring decoder execution alone.

Syndrome records can also expose control errors and guide model learning. In this experiment they revealed a phase-tracking problem; separate [QEC-based control work](https://www.nature.com/articles/s41586-026-10759-2) used detection events to stabilize a superconducting processor against drift. A useful software comparison would combine such diagnostics with workload-level resource estimates at matched reliability, so that better calibration, compilation or decoding can be translated into an actual computational benefit.
