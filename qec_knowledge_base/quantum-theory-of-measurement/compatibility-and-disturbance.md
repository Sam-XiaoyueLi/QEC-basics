# 5. Multiple measurements: compatibility and disturbance

An instrument gives the state after each result. A second detector then measures that state. We can therefore calculate the whole sequence and compare it with measuring the second observable directly. This comparison defines disturbance.

[Learning path](README.md) · Previous: [Instruments and apparatus](instruments-and-apparatus.md) · Course: §§2.1–2.3, pp. 53–83.

## Calculate a sequence using the unnormalized branch

The input state is $`\rho`$. The first instrument $`\mathcal I_s`$ reports $`s`$. The second POVM $`F_t`$ reports $`t`$. Their joint probability is

```math
p(s,t)=\mathrm{tr}[\mathcal I_s(\rho)F_t].
```

This already includes the probability of the first outcome. Dividing by $`p(s)`$ would give $`p(t\mid s)`$ instead. Using the dual map from page 3, the whole sequence has effects

```math
G_{s,t}=\mathcal I_s^{\ast}(F_t).
```

A **marginal** sums over one of the two outcomes. Summing over $`t`$ recovers the first measurement effect $`E_s=\mathcal I_s^{\ast}(I)`$. Summing over $`s`$ gives the second measurement effect on the original input:

```math
\sum_sG_{s,t}=\Phi^{\ast}(F_t),\qquad \Phi=\sum_s\mathcal I_s.
```

The first measurement is nondisturbing for $`F`$ precisely when $`\Phi^{\ast}(F_t)=F_t`$ for every outcome $`t`$. This condition must hold for every input state. Agreement on one state is insufficient.

The tunable Z instrument lets us calculate this change explicitly. We use a later X measurement because X detects the coherence that the Z instrument can remove.

## Running example: unsharp Z followed by sharp X

The first measurement is the Lüders Z instrument from lesson 4, with strength $`\eta`$ and $`c=\sqrt{1-\eta^2}`$. The second is sharp X, with effects $`F_t=(I+tX)/2`$. Both labels $`s,t`$ take values $`\pm1`$. Direct multiplication gives

```math
G_{s,t}=K_s^\dagger F_tK_s
=\frac14(I+s\eta Z+tcX),
```

so for input Bloch vector $`\mathbf r`$,

```math
p(s,t)=\frac14(1+s\eta r_z+tc r_x).
```

The first marginal is the intended unsharp $`Z`$. The second marginal is $`(I+tcX)/2`$. Thus the sequence measures unsharp $`X`$ on the original input, although the second detector itself is sharp. On $`\ket{+}`$, the final $`X=+1`$ probability is $`(1+c)/2`$. This probability is $`0.9`$ at $`\eta=0.6`$ and $`0.5`$ at $`\eta=1`$. Measuring $`X`$ directly would give probability one.

A later $`Z`$ measurement, by contrast, is undisturbed by this instrument: $`\Phi^{\ast}(Z)=Z`$. Thus disturbance depends on the later observable. However, preserving its average outcome distribution does not guarantee that a repeated measurement returns the same individual result.

## Repeatability is a property of the instrument

**Repeatability** means that an immediate repetition gives the same result with probability one. There is no intervening evolution. A sharp Lüders instrument with projectors $`P_s`$ is repeatable. After result $`s`$, its state lies in the range of $`P_s`$. Since $`P_tP_s=0`$ for $`t\ne s`$, another result is impossible.

A sharp POVM alone does not guarantee repeatability. A device can measure $`Z`$ and then flip the qubit. Its first-outcome POVM is unchanged, but repeating the device gives the opposite sign.

The unsharp Lüders instrument preserves $`Z`$ populations but is not repeatable. For $`0<\eta<1`$, either sign can occur even on a $`Z`$ eigenstate. Different syndrome records can therefore arise from measurement randomness, changes in the system, or readout faults. These causes require different models.

## Joint measurability means preserving both requested marginals

A sequence always produces two labels. Our Z-then-X example showed that those labels can describe altered observables. Joint measurability asks a stricter question: can one measurement reproduce both target distributions on the original input?

POVMs $`E_s`$ and $`F_t`$ are **jointly measurable** if a parent POVM $`G_{s,t}`$ satisfies

```math
\sum_tG_{s,t}=E_s,\qquad\sum_sG_{s,t}=F_t.
```

One parent measurement then produces data for both target observables by classical processing. Two sharp PVMs are jointly measurable exactly when their projections commute. Commutation is sufficient for general POVMs too, but it is not necessary.

For example, let $`a`$ be the strength of unsharp $`Z`$, and let $`b`$ be the strength of unsharp $`X`$. Both strengths lie between zero and one. The effects

```math
G_{s,t}=\frac14(I+saZ+tbX)
```

sum to $`I`$ and have the desired marginals. Their eigenvalues are $`(1\pm\sqrt{a^2+b^2})/4`$, so this construction works when $`a^2+b^2\leq1`$. These observables are **unbiased**: they give equal outcome probabilities on the maximally mixed state. For this orthogonal qubit pair, the condition is also necessary. See [Busch and Heinosaari, Approximate joint measurements of qubit observables](https://arxiv.org/abs/0706.1415).

The running sequential construction has $`a=\eta`$ and $`b=\sqrt{1-\eta^2}`$, exactly on the boundary. Sharp $`Z`$ and sharp $`X`$ would require $`a=b=1`$, which is impossible. The ability to perform two operations in sequence does not make their original sharp observables jointly measurable.

Compatibility guarantees that some joint implementation exists. It does not mean that any chosen instrument for the first POVM preserves the second. Even a sharp measurement can be followed by an extra unitary that disturbs otherwise commuting observables.

## Three different meanings of uncertainty

The bound above limits how sharply one device can measure both observables. It is a measurement constraint. It differs from uncertainty already present in an input state, and from disturbance caused by an earlier measurement.

| Concept | What varies or is compared? | Engineering question |
| --- | --- | --- |
| Preparation uncertainty | Distributions of sharp observables in one prepared state | How predictable are ideal outcomes on this state? |
| Measurement imprecision | Actual measurement statistics versus a target observable | How accurately does the detector implement its specification? |
| Disturbance | Later statistics with versus without an earlier process | What has the earlier measurement changed? |

For Hermitian $`A,B`$, the Robertson preparation relation is

```math
\Delta_\rho A\,\Delta_\rho B\geq\frac12|\mathrm{tr}(\rho[A,B])|,
```

where $`[A,B]=AB-BA`$ and $`\Delta_\rho A`$ is the standard deviation of ideal $`A`$ outcomes. For Pauli $`X,Z`$ this lower bound is $`|r_y|`$. The bound can be zero even though $`X`$ and $`Z`$ are incompatible. It therefore does not test compatibility. This inequality does not directly describe detector error or measurement backaction.

A measurement-uncertainty relation must specify how approximation error is measured. The course uses Wasserstein distances to compare outcome distributions. These distances measure the minimum cost of moving probability between outcomes, using the distances between their numerical values. The course then compares observables across input states. For our qubit pair, increasing one measurement strength limits the other. Any error–disturbance formula needs its own error definitions and assumptions.

## Where continuous position and momentum fit

The same distinction matters for continuous measurements. Sections 2.1.1 and 2.2.1 apply it to position and momentum in phase space. A phase-space POVM reports approximate position and momentum together. Its marginals are broadened versions of the sharp position and momentum distributions. An auxiliary quantum state constrains how narrow both broadening distributions can be. A sequential position measurement can likewise broaden later momentum statistics through its interaction with the probe.

The calculation follows the qubit case. A POVM or instrument determines the marginals, which can then be compared with the target distributions. Continuous variables also require integration and explicit operator domains.

## Check your understanding

1. For $`\ket{+}`$ and $`\eta=0.6`$, calculate all four probabilities $`p(s,t)`$.
2. Can unbiased unsharp $`Z`$ and $`X`$, both with strength $`0.8`$, be jointly measured?
3. If sharp $`Z`$ happens not to change $`X`$ statistics on $`I/2`$, does that establish nondisturbance?

<details>
<summary>Worked answers</summary>

1. With $`c=0.8`$, each $`s`$ has $`p(s,+)=0.45`$ and $`p(s,-)=0.05`$. The second marginal is $`(0.9,0.1)`$.
2. No: $`0.8^2+0.8^2=1.28>1`$. Equal strengths must be at most $`1/\sqrt2`$.
3. No. Nondisturbance requires preservation for every input. The input $`\ket{+}`$ provides a counterexample: sharp $`Z`$ changes subsequent $`X`$ probabilities from $`(1,0)`$ to $`(1/2,1/2)`$.

</details>

A sequence can change the state before later data are collected. [Tomography](tomography.md) instead uses repeated preparations to infer the original state from several measurement settings.

Last updated: 2026-11-09
