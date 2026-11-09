# 2. Measurement outcomes: effects and POVMs

A detector event asks a yes–no question about a prepared system. An effect $`E`$ encodes its probability through the Born rule:

```math
p(E\mid\rho)=\mathrm{tr}(\rho E),\qquad 0\leq E\leq I.
```

The bounds mean that both $`E`$ and $`I-E`$ are positive semidefinite, ensuring valid probabilities for every state. An effect specifies probabilities, not a post-measurement state.

[Learning path](README.md) · Previous: [States and subsystems](states-and-subsystems.md) · Course: §§1.2–1.2.3, pp. 17–26.

## A whole measurement is a collection of effects

A POVM, or positive-operator-valued measure, assigns an effect $`E_x`$ to each outcome $`x`$:

```math
E_x\geq0,\qquad\sum_xE_x=I,\qquad p_x=\mathrm{tr}(\rho E_x).
```

Positivity prevents negative probabilities; summing to $`I`$ makes the probabilities sum to one. A detector's failure to click must be included as an outcome if it can occur. Otherwise the model describes only a selected subset of runs.

For a projective measurement, or projection-valued measure (PVM), the effects are orthogonal projections $`P_x`$ satisfying $`P_x^2=P_x`$ and $`P_xP_y=0`$ for distinct outcomes. A Hermitian observable $`A=\sum_xa_xP_x`$ encodes the sharp measurement with values $`a_x`$. General POVMs allow unsharp measurements and need not be spectral projections of one Hermitian operator. See also IBM's [general-measurement formulation](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/general-measurements/introduction).

## Running example: a tunable Z measurement

Let $`s=\pm1`$ and define

```math
E_s=\frac12(I+s\eta Z),\qquad 0\leq\eta\leq1.
```

Each effect has eigenvalues $`(1\pm\eta)/2`$, so this is a valid POVM. For the Bloch state from page 1,

```math
p_s=\frac{1+s\eta r_z}{2}.
```

At $`\eta=1`$ we measure sharp $`Z`$. At $`\eta=0`$ we get a fair random bit with no state information. At intermediate strengths the two $`Z`$ eigenstates give different, overlapping distributions. For $`r_z=0.6`$ and $`\eta=0.8`$, $`p_+=0.74`$ and $`p_-=0.26`$.

This detector cannot distinguish states with the same $`r_z`$, whatever their $`r_x`$ and $`r_y`$. More shots improve the estimate of $`\eta r_z`$ but reveal no missing components.

## Classical post-processing and readout errors

Suppose the physical outcome is $`x`$, but the recorded label is $`y`$ with conditional probability $`\beta(y\mid x)`$. Then

```math
F_y=\sum_x\beta(y\mid x)E_x,
\qquad \beta(y\mid x)\geq0,\quad\sum_y\beta(y\mid x)=1.
```

Forgetting distinctions between outcomes is coarse graining. Random misclassification is a more general post-processing. Both act on the classical record.

Write $`P_s=(I+sZ)/2`$ for the sharp $`Z`$ projections. If an ideal $`Z`$ result is flipped with probability $`0\leq\epsilon\leq1/2`$, the reported effects are

```math
F_s=(1-\epsilon)P_s+\epsilon P_{-s}
=\frac12[I+s(1-2\epsilon)Z].
```

Thus the running POVM can arise from sharp measurement followed by label noise, with $`\eta=1-2\epsilon`$. It can also arise from a gentler quantum interaction. These implementations have the same reported statistics but can have different state changes. Do not infer backaction from a confusion matrix.

## Means do not specify the entire measurement

For numerical outcomes $`x`$, define moment operators $`E[1]=\sum_xxE_x`$ and $`E[2]=\sum_xx^2E_x`$. Then

```math
\mathbb E[x]=\mathrm{tr}(\rho E[1]),\qquad
\mathrm{Var}(x)=\mathrm{tr}(\rho E[2])-[\mathrm{tr}(\rho E[1])]^2.
```

For a general POVM, $`E[2]`$ need not equal $`E[1]^2`$. Their difference $`N_E=E[2]-E[1]^2`$ is positive, and

```math
\mathrm{Var}(x)=\mathrm{Var}_\rho(E[1])+\mathrm{tr}(\rho N_E).
```

Here $`\mathrm{Var}_\rho(A)=\mathrm{tr}(\rho A^2)-[\mathrm{tr}(\rho A)]^2`$ refers to the sharp observable $`A`$. For our $`\pm1`$ outcomes, $`E[1]=\eta Z`$, $`E[2]=I`$, and $`N_E=(1-\eta^2)I`$. The comparison is to sharp $`\eta Z`$, whose numerical values are $`\pm\eta`$, not to sharp $`Z`$ with unchanged labels.

## Naimark dilation: realizing probabilities on a larger space

Any finite-outcome POVM admits projections $`P_x`$ on a larger Hilbert space and an isometry $`J`$ such that

```math
E_x=J^\dagger P_xJ,\qquad J^\dagger J=I.
```

The positive square root $`\sqrt{E_x}`$ is obtained by diagonalizing $`E_x`$ and taking the nonnegative square roots of its eigenvalues. One construction is $`J|\psi\rangle=\sum_x\sqrt{E_x}|\psi\rangle\otimes|x\rangle`$, with $`P_x=I\otimes|x\rangle\langle x|`$. The identity $`\sum_xE_x=I`$ ensures that $`J`$ preserves norms. Projecting the outcome register gives probability $`\langle\psi|E_x|\psi\rangle`$.

This proves that generalized probabilities can be implemented by embedding the system and measuring a sharp pointer. It does not select a unique disturbance. Page 4 will turn this particular construction into a complete instrument.

For a continuous detector, replace single-outcome effects by effects $`E(B)`$ for measurable sets of readings $`B`$, with $`p(B)=\mathrm{tr}[\rho E(B)]`$. Sums over disjoint events become countably additive measures. An exact point can have zero probability even when its probability density is nonzero.

## Check your understanding

For $`\eta=0.6`$, calculate the probabilities on $`|0\rangle`$ and $`|+\rangle`$, the equivalent symmetric readout-flip probability, and the variance on $`|0\rangle`$. Does this specify the output state?

<details>
<summary>Worked answer</summary>

On $`|0\rangle`$, $`p_+=0.8`$ and $`p_-=0.2`$. On $`|+\rangle`$, both are $`0.5`$. The flip probability is $`\epsilon=(1-\eta)/2=0.2`$. On $`|0\rangle`$, the outcome mean is $`0.6`$ and the variance is $`1-0.6^2=0.64`$. None of these calculations specifies an output state: that requires an instrument.

</details>

Next: [Operations and channels](operations-and-channels.md) describe state changes before we combine them with the outcome record.

Last updated: 2026-11-09
