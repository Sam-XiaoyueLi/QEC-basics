# Gross code: check patterns, logical operators, and computation

Status: Working notes
Last updated: 2026-10-13

## Overview

The Gross code stores twelve logical qubits in 144 data qubits, with distance twelve: $[[144,12,12]]$. Its original memory implementation adds 144 check ancillas, for 288 physical qubits. “Gross” means twelve dozen. The code belongs to the bivariate bicycle family introduced by IBM researchers in a 2023 preprint and published in 2024. [Original paper](https://www.nature.com/articles/s41586-024-07107-7)

This page assumes the stabilizers, logical operators, and syndrome measurements covered in the [basic QEC tutorial](../../qec_basic_notes/tut1.pdf). We focus on what changes when moving from a surface code to Gross code: the connections, the twelve logical qubits sharing one block, and the resulting gate and readout procedures.

## Check pattern recipes

There are two groups of data qubits, called $L$ and $R$. Each has a periodic $12\times6$ set of addresses:

$$
L(i,j),\quad R(i,j),\qquad i=0,\ldots,11,\quad j=0,\ldots,5.
$$

Increasing $i$ past 11 returns to 0; increasing $j$ past 5 also returns to 0. Thus there are $2\times12\times6=144$ data qubits. There is also one `X` check and one `Z` check per address.

We need a compact way to specify the six data qubits touched by each check. Let $x$ mean “increase the first address by one” and $y$ mean “increase the second address by one.” Define two **check pattern recipes**:

$$
A=x^3+y+y^2,\qquad B=y^3+x+x^2.
$$

**Algebraic addresses are not the drawn Cartesian positions.** The drawing interleaves four kinds of vertices: $L$ data, $R$ data, `X` checks, and `Z` checks. Consequently, increasing an address does not necessarily mean stepping to the next dot on the page. Follow the vertex labels when interpreting $x$ and $y$.

Each term selects one data qubit relative to the check's address. The plus signs collect these positions; they are not extra gates. An `X` check uses recipe $A$ in the $L$ group and recipe $B$ in the $R$ group:

$$
S_X(i,j)=X_{L(i+3,j)}X_{L(i,j+1)}X_{L(i,j+2)}
X_{R(i,j+3)}X_{R(i+1,j)}X_{R(i+2,j)}.
$$

For the corner check $S_X(0,0)$, the table below separates the **qubit address** selected by the recipe from its **position in Figure 1**. The drawing has columns 0–23 and rows 0–11, with rows counted upward from the bottom. Its placement rules are

$$
L(i,j)\longrightarrow(2i,2j-3),\qquad
R(i,j)\longrightarrow(2i-3,2j),
$$

wrapping drawing columns modulo 24 and drawing rows modulo 12. For example, $L(0,1)$ is placed at $(0,-1)$, which wraps to drawing position $(0,11)$; it is not the qubit address $L(0,11)$.

| Recipe | Term | Selected qubit address | Drawing position (column, row) |
| --- | --- | --- | --- |
| $A$ | $x^3$ | $L(3,0)$ | $(6,9)$ |
| $A$ | $y$ | $L(0,1)$ | $(0,11)$ |
| $A$ | $y^2$ | $L(0,2)$ | $(0,1)$ |
| $B$ | $y^3$ | $R(0,3)$ | $(21,6)$ |
| $B$ | $x$ | $R(1,0)$ | $(23,0)$ |
| $B$ | $x^2$ | $R(2,0)$ | $(1,0)$ |

The next **blue data qubit below** $L(0,1)$ is $L(0,0)$, at drawing position $(0,9)$, with a pink check between them at row 10. Continuing down the blue column gives addresses $L(0,5),L(0,4),L(0,3),L(0,2)$ at rows 7, 5, 3, and 1. These other blue sites orient the drawing; they are not additional data qubits selected by the corner check.

![Figure 1: a corner check, its six neighbors, paired boundary crossings, and the resulting torus](assets/check-pattern.png)

Blue and orange circles are $L$ and $R$ data; pink and green squares are `X` and `Z` checks. Dashed edges follow $A$, and solid edges follow $B$. The gray grid shows the short connections; other checks' extra connections are omitted for clarity.

The four non-cubic terms give four short connections in this drawing. Two of those cross the cut: the edge to $L(0,1)$ leaves at **a** and returns at **a**, while the edge to $R(1,0)$ leaves at **c** and returns at **c**. They are short on the periodic grid even though their endpoints appear on opposite sides of the rectangle. The cubic terms give the two extra connections, which also cross the cut here, at **b** and **d**.

The blue left and right boundaries are the same seam; the purple bottom and top boundaries are the other seam. Joining left to right makes a cylinder, and joining its two circular ends makes a torus. The inset represents the connectivity, not the physical shape required of a chip.

The same recipes work everywhere. For example, applying $A$ and $B$ at address $(11,5)$ selects $L(2,5),L(11,0),L(11,1),R(11,2),R(0,5),R(1,5)$: the address arithmetic wraps in both directions.

### The Z-check recipe and why it commutes with the X checks

To construct a `Z` check, exchange the recipes between $L$ and $R$ and reverse their shifts. Thus $x^3$ becomes a shift by minus three, and similarly for the other terms:

$$
S_Z(i,j)=Z_{L(i,j-3)}Z_{L(i-1,j)}Z_{L(i-2,j)}
Z_{R(i-3,j)}Z_{R(i,j-1)}Z_{R(i,j-2)}.
$$

All addresses are still periodic. Compare the corner `X` check with $S_Z(3,3)$:

| Check | $L$ data positions | $R$ data positions |
| --- | --- | --- |
| $S_X(0,0)$ | $(3,0),(0,1),(0,2)$ | $(0,3),(1,0),(2,0)$ |
| $S_Z(3,3)$ | $(3,0),(2,3),(1,3)$ | $(0,3),(3,2),(3,1)$ |

They share exactly $L(3,0)$ and $R(0,3)$. Exchanging `X` and `Z` on either shared qubit gives a minus sign; the two minus signs cancel.

![An X check and a Z check share two qubits, so their minus signs cancel](assets/commuting-checks.png)

There is also a simple reason this pairing works for **every** check. Suppose an `X` check is at address $u$, and a `Z` check is at address $v$. Use $a$ for one of the three shifts in $A$ and $b$ for one of the three shifts in $B$.

- A shared $L$ qubit has address $u+a=v-b$, so $v=u+a+b$.
- That same pair of shifts gives a shared $R$ qubit: $u+b=v-a$.

Every overlap in $L$ therefore has a matching overlap in $R$. For these particular recipes, the nine possible summed shifts $a+b$ are distinct even after wrapping, so any given `X`–`Z` check pair shares either zero or two data qubits. Either way, the checks commute. Reversing and exchanging the recipes is what guarantees this pairing. [Check construction](https://arxiv.org/html/2407.18393v2#S4)

Why choose these shifts rather than some other six connections? Commuting checks are only the first requirement. Different choices can store different numbers of logical qubits or admit short logical errors. These recipes and periodic dimensions were selected through a search for a useful combination of storage efficiency, protection, and hardware connectivity. The torus alone does not determine the parameters.

## Why there are twelve logical qubits

There are 72 `X` checks and 72 `Z` checks, but they do not impose 144 independent constraints. Some can be obtained by multiplying others. For the Gross pattern, only **66 checks of each type are independent**; there are six redundant relations in each set.

Using the stabilizer counting rule from the basic tutorial,

$$
\text{logical qubits}=144-66-66=12.
$$

The important Gross-specific point is that these twelve logical qubits occupy the **same block**. They are not twelve separate surface-code patches. Their logical operators can use overlapping sets of physical qubits, provided they have the appropriate commutation relations.

The counts come from checking dependencies among the actual stabilizer patterns, not from counting holes in the pictured torus. An ordinary toric code has two logical qubits; the Gross code's extra connections change the constraints. [Code-parameter calculation](https://arxiv.org/html/2308.07915#S4)

## What logical operators look like

A Gross logical operator is a pattern of physical Paulis that escapes all stabilizer checks but acts on encoded information. It need not resemble a single string running around the torus.

Here is one published logical `Z` pattern. Apply `Z` on these twelve data qubits:

| Group | Data addresses |
| --- | --- |
| $L$ | $(2,3),(2,5),(3,0),(3,3),(3,4),(3,5)$ |
| $R$ | $(1,3),(1,5),(2,0),(2,4),(3,2),(3,4)$ |

Its paired logical `X` uses the sixteen sites shown in the top row of the next figure. Every stabilizer has the required even overlap with the opposite-type logical pattern, so neither pattern creates a syndrome.

![A logical X and Z pair, distributed across the L and R data groups](assets/logical-operators.png)

The two logical patterns share only $R(1,5)$, circled in black. Their odd overlap means they anticommute, as `X` and `Z` must for one logical qubit. It also proves these are not stabilizers: a stabilizer would commute with every pattern that escapes all checks. These representatives are given in equations (64)–(67) of [Cross et al.](https://arxiv.org/html/2407.18393v2#S4.SS1); we call the pair logical qubit 1.

### How to find a logical pattern

Conceptually, a search works by placing Pauli marks on data qubits and enforcing two conditions:

1. **No syndrome:** a candidate `Z` pattern must overlap every `X` check an even number of times; exchange `X` and `Z` for an `X` pattern.
2. **Nontrivial action:** discard patterns that are merely products of stabilizers. Those also have no syndrome, but do not change encoded information.

To find a paired `X`, require an odd overlap with the chosen logical `Z`. To find the other logical qubits, keep patterns whose action cannot be reproduced by multiplying the logical patterns already retained and the stabilizers. Pair them so that each logical `X` anticommutes with its own `Z` and commutes with the other eleven logical `Z` operators.

For 144 data qubits this is a computer calculation, not a practical exercise in guessing dots. The published pair above provides a concrete example whose overlaps can be checked directly; the [accompanying script](build_examples.py) verifies it and constructs a complete twelve-pair set.

Multiplying a logical representative by a stabilizer changes its physical pattern without changing its encoded action. Consequently there are many equivalent shapes. Finding a useful logical basis and finding the smallest representatives are separate tasks.

## Why the distance is twelve

The smallest nontrivial logical pattern touches twelve data qubits. The displayed logical `Z` supplies a twelve-qubit example, but that alone establishes only that the distance is **at most** twelve. To conclude that it is twelve, smaller nontrivial patterns must also be ruled out.

The original paper reports that this final distance calculation was performed using integer programming: a computer searches for the smallest pattern satisfying the no-syndrome and nontrivial-action requirements. It distinguishes that calculation from the faster heuristic searches used to screen code candidates. We rely on the paper for exclusion of smaller logical patterns; our examples verify the displayed twelve-qubit pattern. [Table 3 and Section 6](https://arxiv.org/html/2308.07915)

### Why twelve gives a five-error guarantee

If two error explanations each touch at most five data qubits, their difference touches at most ten. If they give the same syndrome, that difference is invisible to the checks. With distance twelve, it cannot be a nontrivial logical operator: the explanations must have the same encoded effect, and recovery can correct either.

Six errors cannot be guaranteed. Divide our twelve-site logical `Z` into two sets of six. Applying `Z` on the first set and applying it on the second set give the same syndrome, because their difference is the full logical `Z`. Yet the two explanations differ logically, so recovery cannot always distinguish them.

Thus distance twelve guarantees correction of up to five arbitrary data-qubit errors with ideal syndrome information and appropriate recovery. This is a general distance result, not an experimental performance claim for Gross code. [Quantum error-correction conditions](https://arxiv.org/html/quant-ph/9705052)

## CNOTs between encoded qubits

### What a logical CNOT must do

Choose a logical control qubit $c$ and target qubit $t$. A logical CNOT must flip the target when the control is 1, while preserving the control and acting coherently on superpositions. In the logical computational basis,

$$
|c,t\rangle_L\longrightarrow|c,t\oplus c\rangle_L.
$$

Here $c,t$ inside the ket denote the logical bit values 0 or 1, and $\oplus$ means addition modulo two.

To determine whether a physical circuit implements this gate, we can check its action on the logical Pauli operators. These are **tests of the circuit's action**, not additional gates we apply to implement CNOT.

In the rules below, an arrow means: applying the operator on the left **before** the circuit has the same effect as applying the operator on the right **after** it. A logical CNOT must satisfy all four rules:

$$
\begin{aligned}
\bar X_c&\longrightarrow\bar X_c\bar X_t,\\
\bar Z_c&\longrightarrow\bar Z_c,\\
\bar X_t&\longrightarrow\bar X_t,\\
\bar Z_t&\longrightarrow\bar Z_c\bar Z_t.
\end{aligned}
$$

For example, the first rule compares two hypothetical sequences: flip the logical control and then perform CNOT, or perform CNOT and then flip both logical qubits. Flipping the control before the gate changes whether the target is flipped, so the two sequences have the same effect. **Neither sequence is the recipe for implementing CNOT**; their equivalence describes what CNOT does to a control flip.

Checking all four rules establishes the gate's logical action, up to an irrelevant global phase. An encoded implementation must also preserve the code space and have the intended action on any other logical qubits.

### Implementing twelve paired CNOTs between two Gross blocks

Take two Gross blocks, $C$ and $T$, each with 144 data qubits. Choose the same logical definitions in both blocks, so that corresponding logical operators occupy matching physical sites.

The physical gate sequence is simple: **apply one CNOT from every data qubit in block $C$ to its matching partner in block $T$**. This means $L(i,j)$ controls the matching $L(i,j)$ in the other block, and similarly for $R(i,j)$. There are 144 such physical CNOTs. No extra physical or logical `X` or `Z` gates are required by the operator-transformation test.

Now verify what this gate sequence implements. Each physical CNOT obeys the same four Pauli rules as above, with physical operators replacing the logical ones. A logical `X` is a product of physical `X` operations on its marked sites. Each marked control `X` transforms into `X` on both matching sites; taken together, the transformed pattern is the original logical `X` in $C$ times the matching logical `X` in $T$.

The other three rules follow in the same way. For each logical pair $a=1,\ldots,12$, the physical circuit therefore gives

$$
\begin{aligned}
\bar X_{a,C}&\longrightarrow\bar X_{a,C}\bar X_{a,T},\\
\bar Z_{a,C}&\longrightarrow\bar Z_{a,C},\\
\bar X_{a,T}&\longrightarrow\bar X_{a,T},\\
\bar Z_{a,T}&\longrightarrow\bar Z_{a,C}\bar Z_{a,T}.
\end{aligned}
$$

These are precisely the required logical CNOT rules. The physical circuit also maps stabilizers into stabilizers or products of matching stabilizers, preserving the code space. It therefore performs the twelve paired logical gates $1_C\to1_T,\ldots,12_C\to12_T$. Applying matching gates across two blocks this way is called a **transversal CNOT**. [CSS-code gate construction](https://arxiv.org/html/quant-ph/9705052#S5.SS3)

Thus the implementation is the 144 matching physical CNOTs; the logical Pauli rules verify their encoded effect. They do not instruct us to apply a control `X` first or to copy an unknown quantum state.

The number 144 counts **physical matching pairs**, not possible logical control–target choices. Within one twelve-qubit logical register, there are $12\times11=132$ directed choices. The factor of two for direction is already included: equivalently, there are 66 unordered pairs and two directions for each. The transversal circuit performs twelve specific pairs across two blocks, not all possible choices within one block.

This construction requires the 144 inter-block couplings or a way to implement them. The sparse inter-module Gross architecture instead uses joint logical measurements. A gate on just one selected logical pair is a different physical procedure, described next.

### A CNOT on two selected logical qubits uses joint parities

To act on just a chosen control $c$ and target $t$, introduce an ancilla logical qubit $a$ in $|+\rangle_L$ and perform:

| Step | Measurement | Outcome bit |
| --- | --- | --- |
| 1 | $\bar Z_c\bar Z_a$ | $u$ |
| 2 | $\bar X_a\bar X_t$ | $v$ |
| 3 | $\bar Z_a$ | $w$ |

Here $+1$ means bit 0 and $-1$ means bit 1. Finish by applying or tracking

$$
\bar Z_c^{\,v}\bar X_t^{\,u\oplus w}.
$$

The resulting operation on $c,t$ is exactly CNOT; $a$ is consumed. The joint measurements learn parities without learning the individual input values, preserving the coherence needed for the gate.

![Selected logical CNOT from joint parity measurements](assets/measurement-cnot.png)

### What the physical hardware measures

In a protected Gross implementation, a logical-parity box is built from auxiliary qubits and many small checks. The useful idea is that the product of the new check operators equals the logical observable being measured.

For example, the following three-site illustration has two auxiliary qubits $e_1,e_2$ and checks

$$
Q_1=Z_{q_1}X_{e_1},\qquad
Q_2=Z_{q_2}X_{e_1}X_{e_2},\qquad
Q_3=Z_{q_3}X_{e_2}.
$$

Multiplying them cancels the auxiliary Paulis, because each occurs twice:

$$
Q_1Q_2Q_3=Z_{q_1}Z_{q_2}Z_{q_3}.
$$

![Auxiliary checks whose product is the desired data parity](assets/parity-measurement.png)

The auxiliary qubits begin in $|0\rangle$, so the individual new checks do not reveal individual data-qubit `Z` values. Their product reveals the desired parity. This cancellation picture extends to larger logical supports.

The original stabilizers must also be modified so that they commute with the new checks. The temporary enlarged code is measured repeatedly, then the auxiliary qubits are measured out and the original code restored, with the necessary corrections tracked. This is **code deformation**, closely related to surface-code lattice surgery. The simple path pictured here illustrates the cancellation mechanism; it does not by itself preserve distance or give a fault-tolerant circuit.

Published constructions choose the auxiliary connections and modified checks carefully. Their compact hardware exposes a limited set of logical measurement ports; additional physical permutations that preserve the code, called **automorphisms**, change which logical combinations are accessible. A selected CNOT is compiled into those available operations. In the cited compact gate scheme, one logical qubit is reserved for synthesis, leaving eleven logical data qubits for computation. Twelve-qubit memory capacity therefore does not imply twelve fully independent hardware gate ports. [Gross-code measurement and gate scheme](https://arxiv.org/html/2407.18393v2#S4); [modular architecture and physical measurement protocols](https://arxiv.org/html/2506.03094v1#S2.SS3)

For a gate-by-gate learning example, [selected_cnot_ideal.stim](selected_cnot_ideal.stim) implements a selected CNOT within one Gross block using two extra physical ancillas. It was checked on encoded truth-table inputs and an encoded Bell pair. Its unencoded ancilla and high-weight parity measurements make it **an ideal demonstration, not a fault-tolerant Gross hardware circuit**. A full protected physical schedule for an arbitrary requested logical pair remains a separate compilation task.

## Reading out logical data

For final readout in the `Z` basis, measure all 144 data qubits in `Z`. For each logical `Z`, multiply the measured signs on its marked sites. For the twelve-site example,

$$
\bar z_1^{\rm raw}=\prod_{q\ \text{in the logical pattern}}m_q,
\qquad m_q\in\{+1,-1\}.
$$

The individual outcomes can be random even for a known encoded computational-basis state; the collective parities give the twelve logical results. The decoder uses the preceding syndrome history and compatible final check parities to decide which raw logical results need flipping. No physical corrections are required after this destructive readout. Whole-block `X` readout works in the corresponding basis.

To read one logical qubit while preserving the others, use the collective auxiliary measurement described above. Measuring every physical qubit on its support individually would reveal more information than the chosen logical parity. [Logical measurement protocols and whole-block readout](https://arxiv.org/html/2506.03094v1)

### A single-error readout example

Prepare all twelve logical qubits in $|0\rangle_L$. Every correct logical `Z` result is then $+1$. Now inject `X` on $R(1,5)$, the circled site of our logical pair.

The reversed `Z` recipe shows that this data qubit participates in exactly these checks:

$$
S_Z(1,0),\qquad S_Z(1,1),\qquad S_Z(4,5).
$$

All three signs flip. Because $R(1,5)$ belongs to the displayed logical `Z` pattern, its raw readout parity also flips to $-1$. In this noiseless-syndrome, single-error example, exactly one data-qubit `X` error explains the three changed checks: the error at $R(1,5)$. The decoder flips the raw logical answer back to $+1$.

With noisy check measurements and continuing data errors, we need the repeated history rather than this single-round lookup. This is the same distinction emphasized in the [decoding tutorial](../../decoder.ipynb).

## Why the required connections are hard to build

A periodic drawing declares two opposite edges adjacent. A flat chip still has to carry the interaction between those physical locations. The extra bulk connections pose the same problem: their microwave paths must pass other qubits, couplers, and control lines.

| Hardware issue | Why it affects the code |
| --- | --- |
| Crossing routes | Independent microwave paths cannot simply intersect as joined metal wires. They need bridges, shielding, vias, or routing layers. |
| Added loss | Longer structures and extra interfaces can expose the quantum state to more imperfect material, reducing coherence or gate quality. |
| Unwanted interactions | Couplers and control pulses can affect other qubits, producing crosstalk and correlated errors during parallel checks. |
| Extra modes and frequency constraints | Long microwave structures have electromagnetic modes that must be engineered alongside qubit and gate frequencies. |
| Indirect routing | Replacing a direct gate with SWAPs or a measurement-based connection adds operations, latency, and sometimes ancillas. |

The difficulty is not that a long-range gate is fundamentally impossible. It is making all required interactions reliable and fast enough throughout repeated error-check cycles. One detailed Gross-code routing study uses the qubit tier plus four higher tiers under its chosen layout constraints; that is an example of engineering overhead, not a universal layer requirement. [Multilayer hardware study](https://arxiv.org/html/2507.23011)

Code distance also does not count faulty circuit operations. An ancilla fault can spread through several data interactions, so gate order and correlated faults matter. The original Gross extraction circuit has a reported circuit-distance upper bound of ten despite code distance twelve. The five-data-error guarantee therefore cannot be read as a five-circuit-fault guarantee. [Original circuit analysis](https://arxiv.org/html/2308.07915)

IBM reports progress toward the required connectivity, routing layers, long couplers, and reset components. These component results do not by themselves establish the full original Gross-code memory experiment. The primary sources checked for these notes do not report a demonstration of that full memory. [IBM engineering update](https://www.ibm.com/quantum/blog/qdc-2025); [March 2026 device overview](https://research.ibm.com/publications/toward-realization-of-quantum-ldpc-devices)

## Further study and reproducible examples

The next useful step is to follow one named control–target pair through the published protected auxiliary system and its physical gate schedule. This would connect the parity-measurement picture to actual time and qubit costs. It is not yet worked through here.

The [example script](build_examples.py) reproduces the figures, checks all stabilizer overlaps and twelve logical pairs, verifies every outcome branch of the CNOT gadget, and runs the single-error readout example. It does not reproduce the paper's full distance lower-bound computation or simulate noisy fault-tolerant operation. Run it from the repository root with:

```bash
.venv/bin/python qec_knowledge_base/gross-code/build_examples.py
```

Useful connections to the basic material:

- [Shor-code notebook](../../shor_tutorial.ipynb): independent stabilizers, logical pairs, and tracked corrections.
- [Surface-code and lattice-surgery notebook](../../surface_code.ipynb): the joint-parity measurement idea behind logical gates.
- [Decoding notebook](../../decoder.ipynb): correcting a logical answer using syndrome history rather than trying to observe the encoded state directly.

## References

1. Sergey Bravyi et al., [*High-threshold and low-overhead fault-tolerant quantum memory*](https://www.nature.com/articles/s41586-024-07107-7), *Nature* 627, 778–782 (2024). [Expanded arXiv version](https://arxiv.org/html/2308.07915): code construction, distance calculation, and extraction circuits.
2. Daniel Gottesman, [*Stabilizer Codes and Quantum Error Correction*](https://arxiv.org/html/quant-ph/9705052) (1997): general recovery guarantees and CSS gate constructions.
3. Andrew Cross et al., [*Improved QLDPC Surgery: Logical Measurements and Bridging Codes*](https://arxiv.org/html/2407.18393v2): explicit Gross logical patterns and protected logical measurement schemes.
4. Theodore Yoder et al., [*Tour de gross: A modular quantum computer based on bivariate bicycle codes*](https://arxiv.org/html/2506.03094v1) (2025): Gross-code computing instructions, auxiliary systems, and physical schedules.
5. Melvin Mathews et al., [*Placing and routing quantum LDPC codes in multilayer superconducting hardware*](https://arxiv.org/html/2507.23011): physical routing constraints and example layouts.
