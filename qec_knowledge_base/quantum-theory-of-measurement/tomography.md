# 6. Learning from measurement: tomography

A detector can produce arbitrarily many bits without identifying a quantum state. Our running $`Z`$ measurement determines only $`r_z`$ when its calibrated strength is nonzero. Tomography asks which measurements distinguish all possible input states and how to reconstruct a state from finite data.

[Learning path](README.md) · Previous: [Compatibility and disturbance](compatibility-and-disturbance.md) · Course: §2.4, pp. 83–90.

## Reconstruction starts with identifiability

For each measurement setting $`a`$ and outcome $`s`$, a known effect $`E_{a,s}`$ predicts

```math
p(s\mid a)=\mathrm{tr}(\rho E_{a,s}).
```

The settings are informationally complete if these probabilities uniquely determine $`\rho`$. In dimension $`d`$, the effects collectively must span the real vector space of Hermitian operators, of dimension $`d^2`$. A trace-one state has $`d^2-1`$ independent real parameters. For a single informationally complete POVM, at least $`d^2`$ outcomes are needed; merely having that many does not guarantee independent information.

The experiment uses many identically prepared copies. Measuring $`X`$, then $`Y`$, then $`Z`$ on the same qubit generally probes an evolving state, not three independent components of its original Bloch vector.

## Qubit tomography with three settings

Measure $`X,Y,Z`$ on separate batches. A shot is one preparation followed by its measurement. If $`n_{a,+}`$ and $`n_{a,-}`$ are the counts in setting $`a`$, with $`N_a=n_{a,+}+n_{a,-}`$, then

```math
\hat r_a=\frac{n_{a,+}-n_{a,-}}{N_a},\qquad
\hat\rho=\frac12(I+\hat r_xX+\hat r_yY+\hat r_zZ).
```

For example, in 1,000 shots per setting, plus counts of 700, 400, and 800 give the estimated Bloch vector $`\hat{\mathbf r}=(0.4,-0.2,0.6)`$. Thus

```math
\hat\rho=\begin{pmatrix}0.8&0.2+0.1i\\0.2-0.1i&0.2\end{pmatrix}.
```

Its Bloch length is $`\sqrt{0.56}<1`$, so the estimate is physical. More generally, three spin directions suffice when they are linearly independent; nearly dependent directions amplify small errors in the observed frequencies.

The measurements need not be jointly measurable on one copy. Different settings use different copies. Conversely, one suitable generalized POVM can be informationally complete on repeated copies even though each individual result is random.

## A single four-outcome POVM

Choose four unit vectors $`\mathbf n_k`$ pointing to a tetrahedron's vertices:

```math
\mathbf n_k\in\frac1{\sqrt3}\{(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)\}.
```

Define $`E_k=(I+\mathbf n_k\cdot\boldsymbol\sigma)/4`$, where $`\boldsymbol\sigma=(X,Y,Z)`$. The effects are positive and sum to $`I`$. Their probabilities satisfy

```math
p_k=\frac{1+\mathbf n_k\cdot\mathbf r}{4},\qquad
\mathbf r=3\sum_kp_k\mathbf n_k.
```

The reconstruction follows from $`\sum_k\mathbf n_k=0`$ and $`\sum_k\mathbf n_k\mathbf n_k^T=(4/3)I_3`$. This is a symmetric special case of the four-outcome qubit family studied in the course. It demonstrates why generalized measurements are useful: one apparatus setting can capture all three Bloch components across repeated preparations.

## Finite shots and measurement noise are different limitations

For ideal Pauli measurements with independent shots,

```math
\mathrm{Var}(\hat r_a)=\frac{1-r_a^2}{N_a}.
```

Sampling uncertainty decreases with more shots. It does not fix an incorrect detector model or recover an unobserved direction.

If the calibrated measurement has $`E_{a,s}=(I+s\eta_a\sigma_a)/2`$ with known $`\eta_a>0`$, the sample outcome mean $`\hat m_a`$ estimates $`\eta_a r_a`$. Divide by the calibrated strength:

```math
\hat r_a=\frac{\hat m_a}{\eta_a},\qquad
\mathrm{Var}(\hat r_a)=\frac{1-\eta_a^2r_a^2}{N_a\eta_a^2}.
```

Small $`\eta_a`$ amplifies sampling noise. At $`\eta_a=0`$ the component is unidentifiable. If both the state and detector strength are unknown, their product alone does not distinguish them; independent calibration or additional assumptions are required.

Finite-shot linear inversion can yield $`|\hat{\mathbf r}|>1`$, giving a negative eigenvalue. One physical reconstruction method maximizes the multinomial log-likelihood

```math
\sum_{a,s}n_{a,s}\log\mathrm{tr}(\rho E_{a,s})
\quad\text{subject to}\quad \rho\geq0,\ \mathrm{tr}\rho=1.
```

Projecting an estimate back into the Bloch ball is a simpler choice, but generally is not the same statistical estimator. Either correction can introduce bias. A physical fitted matrix is not by itself evidence that the measurement model fits the data; compare predicted frequencies with observations and quantify uncertainty.

## What tomography does and does not validate

State tomography estimates a preparation using an assumed measurement model. It does not automatically characterize a channel or validate a measurement instrument. For process tomography, prepare a spanning set of known inputs and reconstruct outputs; errors in preparation and readout can then be confused with process errors unless modeled separately.

For $`n`$ qubits a general state has $`4^n-1`$ parameters. Full reconstruction becomes expensive rapidly. If the engineering question is one observable, a parity, or a few correlations, estimate those quantities directly rather than reconstructing an unrestricted state. The same distinction applies in QEC: syndrome records answer selected check questions and are not intended to reveal the full encoded state.

## Check your understanding

1. Why do arbitrarily many $`Z`$ shots fail to distinguish $`|+\rangle`$ from $`|-\rangle`$?
2. With known $`\eta=0.5`$, a measured sign average of $`0.3`$ implies what estimate of $`r_z`$?
3. Reconstruct the state from the tetrahedral probabilities for $`\mathbf r=(0,0,1)`$.

<details>
<summary>Worked answers</summary>

1. Both states have $`r_z=0`$ and hence identical $`Z`$ distributions. The missing information is about the direction being measured, not the number of shots.
2. $`\hat r_z=0.3/0.5=0.6`$. Dividing by the strength also amplifies statistical fluctuations; it is not free error removal.
3. For the two vertices with positive $`z`$, $`p_k=(1+1/\sqrt3)/4`$; for the other two, $`p_k=(1-1/\sqrt3)/4`$. Substituting into $`3\sum_kp_k\mathbf n_k`$ yields $`(0,0,1)`$ and $`\rho=|0\rangle\langle0|`$.

</details>

Last updated: 2026-11-09
