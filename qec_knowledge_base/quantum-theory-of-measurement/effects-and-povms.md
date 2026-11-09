# 2. Measurement outcomes: effects and POVMs

A measurement produces a **classical record**: a bit, a detector label, or a pointer reading. Given the input density matrix, how do we predict that record? Page 1 answered this for a measurement in a chosen basis. We now extend that rule to detectors with noise, incomplete resolution, or more outcomes than basis states.

[Learning path](README.md) · Previous: [States and subsystems](states-and-subsystems.md) · Course: §§1.2–1.2.3, pp. 17–26.

## One possible outcome: an effect

In a basis measurement, the probability of the outcome associated with a normalized basis vector $`\ket{b}`$ is

```math
p(b\mid\rho)=\bra{b}\rho\ket{b}
=\mathrm{tr}(\rho\ket{b}\bra{b}).
```

This separates two ingredients: $`\rho`$ describes the preparation, and the projector $`\ket{b}\bra{b}`$ describes the detector event. To describe a general event, replace that projector by an operator called an **effect**, $`E`$:

```math
p(E\mid\rho)=\mathrm{tr}(\rho E),\qquad 0\leq E\leq I.
```

Here $`I`$ is the identity. The bounds mean that both $`E`$ and $`I-E`$ are positive semidefinite; they ensure that the event's probability lies between zero and one for every input state. The effect is an operator used to calculate a probability. The recorded outcome is a classical label.

One effect answers whether one event occurs. To describe the whole detector, we must account for every possible result.

## All possible outcomes: a POVM, with PVMs as a special case

Let $`x`$ label mutually exclusive outcomes that exhaust all possibilities. A **POVM** (positive-operator-valued measure) assigns an effect $`E_x`$ to each label:

```math
E_x\geq0,\qquad\sum_xE_x=I,\qquad p(x\mid\rho)=\mathrm{tr}(\rho E_x).
```

The completeness condition $`\sum_xE_x=I`$ makes the probabilities sum to one. A collection of individually valid effects is therefore not enough: it must also form a complete set of outcomes. Include “no click” if the detector can fail to register a result.

The basis measurement we started with is a special POVM. Its effects are orthogonal projectors, so it is called a **PVM** (projection-valued measure), or a sharp measurement. Writing its effects as $`P_x`$, we have $`P_x^2=P_x`$ and $`P_xP_y=0`$ for distinct labels $`x,y`$. Assigning numerical values $`a_x`$ to these outcomes gives the Hermitian observable $`A=\sum_xa_xP_x`$. General POVMs drop the requirement that effects be orthogonal projectors. See IBM's [general-measurement formulation](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/general-measurements/introduction).

What does that extra freedom buy us? We can keep the same two output labels as a sharp qubit measurement while making them less reliable indicators of the input state.

## From sharp Z to a detector with tunable resolution

A sharp Pauli $`Z`$ measurement reports $`s=+1`$ for $`\ket{0}`$ and $`s=-1`$ for $`\ket{1}`$. Its effects are

```math
P_+=\ket{0}\bra{0}=\frac{I+Z}{2},\qquad
P_-=\ket{1}\bra{1}=\frac{I-Z}{2}.
```

Keep those two classical labels, but introduce a parameter $`0\leq\eta\leq1`$ controlling how well their probabilities distinguish the two basis states:

```math
E_s=\frac12(I+s\eta Z),\qquad s=\pm1.
```

These effects sum to $`I`$ and have eigenvalues $`(1\pm\eta)/2`$, which are nonnegative. They therefore form a POVM. At $`\eta=1`$ they reduce to the projectors above; for $`\eta<1`$ they are not projectors. We call $`\eta`$ the measurement strength here, but this parameter specifies the readout statistics; it does not yet specify a physical interaction.

For an input state with Bloch component $`r_z=\mathrm{tr}(\rho Z)`$, the Born rule gives

```math
p(s\mid\rho)=\frac{1+s\eta r_z}{2}.
```

Thus $`\ket{0}`$ reports plus with probability $`(1+\eta)/2`$, while $`\ket{1}`$ reports plus with probability $`(1-\eta)/2`$. At full strength the labels distinguish these inputs perfectly. At zero strength both inputs produce a fair random sign. Intermediate strengths give overlapping distributions. For $`r_z=0.6`$ and $`\eta=0.8`$, the plus and minus probabilities are $`0.74`$ and $`0.26`$.

The two preparations from page 1, $`\rho_+`$ and $`\rho_{\mathrm{mix}}`$, both have $`r_z=0`$, so they remain indistinguishable by this detector at every strength. More shots estimate the same probabilities more precisely; they cannot reveal the missing Bloch components.

We have specified a valid detector statistically. What could cause its imperfect resolution? One possibility requires no new quantum interaction at all: an ideal measurement followed by mistakes in the classical label.

## Readout errors change the effects of the recorded measurement

Suppose a sharp $`Z`$ measurement happens first, but its sign is flipped in the record with probability $`0\leq\epsilon\leq1/2`$. A recorded plus can then come from either a correctly reported plus or an incorrectly reported minus. Adding those two alternatives gives

```math
p(\text{recorded }+\mid\rho)
=(1-\epsilon)\mathrm{tr}(\rho P_+)+\epsilon\mathrm{tr}(\rho P_-).
```

Collecting the terms inside the trace identifies the effect $`F_s`$ for each recorded sign:

```math
F_s=(1-\epsilon)P_s+\epsilon P_{-s}
=\frac12[I+s(1-2\epsilon)Z].
```

This is exactly our tunable POVM with $`\eta=1-2\epsilon`$. The same formula that described an unsharp detector can therefore describe a sharp detector with noisy readout.

The same reasoning applies to any classical processing. If an original outcome $`x`$ is recorded as $`y`$ with conditional probability $`\beta(y\mid x)`$, then the original effects $`E_x`$ become

```math
F_y=\sum_x\beta(y\mid x)E_x,
\qquad\beta(y\mid x)\geq0,\quad\sum_y\beta(y\mid x)=1.
```

Merging several labels into one is **coarse graining**; randomly misclassifying labels gives a confusion matrix. Both change the POVM describing the final record. For a continuous pointer, we similarly ask for the probability that its reading lies in an interval or measurable set $`B`$: an effect $`E(B)`$ gives $`p(B\mid\rho)=\mathrm{tr}[\rho E(B)]`$. Effects add for disjoint sets. An exact point may have probability zero even when the probability density there is nonzero.

Once the effects for the final record are known, we can calculate any statistic of that record. But replacing the full distribution by its mean can hide some of the detector's randomness.

## Why the average readout is not a complete measurement model

For our detector, each recorded value $`s`$ is either $`+1`$ or $`-1`$. Its mean and variance are therefore

```math
\mathbb E[s]=\eta r_z,\qquad
\mathrm{Var}(s)=1-\eta^2r_z^2.
```

The mean equals the expectation of the Hermitian operator $`\eta Z`$. Does that mean the detector simply measures $`\eta Z`$ sharply? No: a sharp measurement of that operator outputs $`\pm\eta`$, whereas our detector outputs $`\pm1`$. The means agree, but the sharp measurement's variance is $`\eta^2(1-r_z^2)`$. Our detector has an additional variance $`1-\eta^2`$.

For a POVM with numerical outcome values $`x`$, this distinction is captured by its first and second **moment operators**:

```math
E[1]=\sum_x xE_x,\qquad E[2]=\sum_x x^2E_x.
```

They give

```math
\mathbb E[x]=\mathrm{tr}(\rho E[1]),\qquad
\mathrm{Var}(x)=\mathrm{tr}(\rho E[2])-[\mathrm{tr}(\rho E[1])]^2.
```

For a PVM, orthogonality makes $`E[2]=E[1]^2`$. For a general POVM these can differ. Their difference $`N_E=E[2]-E[1]^2`$ is positive semidefinite and quantifies the extra variance relative to a sharp measurement of $`E[1]`$:

```math
\mathrm{Var}(x)=\mathrm{Var}_\rho(E[1])+\mathrm{tr}(\rho N_E),
```

where $`\mathrm{Var}_\rho(A)=\mathrm{tr}(\rho A^2)-[\mathrm{tr}(\rho A)]^2`$. In our example, $`E[1]=\eta Z`$, $`E[2]=I`$, and $`N_E=(1-\eta^2)I`$, reproducing the difference above. The full labeled POVM specifies the outcome distribution; its first moment alone generally does not.

We now know how to specify outcomes, model readout errors, and calculate statistics. One physical question remains: can every valid POVM be realized by a quantum apparatus, as our noisy Z example can?

## Naimark dilation: a sharp measurement on a larger system

Yes. A finite-outcome POVM can be implemented by embedding the input in a larger quantum system and measuring orthogonal outcome sectors there. This is **Naimark dilation**. It explains how effects that are not projectors on the input can arise from projectors on the input plus an apparatus.

For an input vector $`\ket{\psi}`$, introduce an outcome register with orthonormal basis states $`\ket{x}`$, one per label. Define the embedding $`J`$ by

```math
J\ket{\psi}=\sum_x\sqrt{E_x}\ket{\psi}\otimes\ket{x}.
```

The positive square root $`\sqrt{E_x}`$ is obtained by diagonalizing $`E_x`$ and taking the nonnegative square roots of its eigenvalues. Because $`\sum_xE_x=I`$, this embedding satisfies $`J^\dagger J=I`$: it preserves inner products and normalization, so it is an isometry.

On the larger space, let $`Q_x=I\otimes\ket{x}\bra{x}`$ be the projector for reading label $`x`$ from the register. Then

```math
J^\dagger Q_xJ=E_x,
```

so measuring the register gives exactly the desired probability $`\bra{\psi}E_x\ket{\psi}`$. A sharp readout of the apparatus thus realizes a general POVM on the input system.

This construction establishes that the probabilities are physically realizable. It does not make the POVM a complete description of the apparatus: different implementations can give the same record probabilities and leave different system states. Our noisy sharp Z measurement and a gentler interaction can share the same effects. To distinguish them, we need the state transformations described by [operations and channels](operations-and-channels.md), then associate each transformation with its recorded outcome using an [instrument](instruments-and-apparatus.md).

## Check your understanding

For $`\eta=0.6`$, calculate the probabilities on $`\ket{0}`$ and $`\ket{+}`$, the equivalent symmetric readout-flip probability, and the variance on $`\ket{0}`$. Does this specify the output state?

<details>
<summary>Worked answer</summary>

On $`\ket{0}`$, $`p_+=0.8`$ and $`p_-=0.2`$. On $`\ket{+}`$, both are $`0.5`$. The flip probability is $`\epsilon=(1-\eta)/2=0.2`$. On $`\ket{0}`$, the outcome mean is $`0.6`$ and the variance is $`1-0.6^2=0.64`$. These calculations specify the recorded statistics. They do not determine the output state, which depends on the instrument implementing the POVM.

</details>

Last updated: 2026-11-09
