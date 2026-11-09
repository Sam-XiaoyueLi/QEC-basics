# Chapter 2. Tomography

Many measurement records do not necessarily identify the input state. The Z detector determines only $`r_z`$ when its known strength is nonzero. For example, $`\rho_+`$ and $`\rho_{\mathrm{mix}}`$ have identical Z statistics but different X statistics.

**State tomography** uses enough measurement settings to distinguish all possible input states. It then estimates the state from the recorded data.

[Learning path](README.md) · Previous: [Compatibility and disturbance](compatibility-and-disturbance.md) · Course: §2.4, pp. 83–90.

## Reconstruction starts with identifiability

Let $`\rho`$ be the unknown density matrix. For each measurement setting $`a`$ and outcome $`s`$, a known effect $`E_{a,s}`$ predicts

```math
p(s\mid a)=\mathrm{tr}(\rho E_{a,s}).
```

The settings are informationally complete if these probabilities uniquely determine $`\rho`$. For a system of dimension $`d`$, the effects must span the real vector space of Hermitian operators. This operator space has dimension $`d^2`$. A trace-one state has $`d^2-1`$ independent real parameters. A single informationally complete POVM therefore needs at least $`d^2`$ outcomes. The count alone does not guarantee independent information.

The experiment uses many identically prepared copies. Measuring X, then Y, then Z on one qubit generally changes its state between measurements. Those results do not directly estimate three components of the original Bloch vector.

For a qubit, separate batches measured along X, Y, and Z supply the three required components.

## Qubit tomography with three settings

A **shot** is one preparation followed by one measurement. Let $`a\in\{x,y,z\}`$ label the Pauli setting. The outcome counts are $`n_{a,+}`$ and $`n_{a,-}`$. Their sum $`N_a=n_{a,+}+n_{a,-}`$ is the number of shots in that setting. Each setting needs $`N_a>0`$. A hat marks an estimate from data:

```math
\hat r_a=\frac{n_{a,+}-n_{a,-}}{N_a},\qquad
\hat\rho=\frac12(I+\hat r_xX+\hat r_yY+\hat r_zZ).
```

For example, take 1,000 shots in each setting. Plus counts of 700, 400, and 800 give $`\hat{\mathbf r}=(0.4,-0.2,0.6)`$. The estimated density matrix is

```math
\hat\rho=\begin{pmatrix}0.8&0.2+0.1i\\0.2-0.1i&0.2\end{pmatrix}.
```

Its Bloch length is $`\sqrt{0.56}<1`$, so the estimate is physical. Three linearly independent spin directions are sufficient. Nearly dependent directions amplify small errors in the observed frequencies.

These sharp measurements need not be jointly measurable because they act on different copies. There is another option: one generalized measurement can collect all three components. It needs more than two outcomes.

## A single four-outcome POVM

For a qubit, four outcomes meet the minimum count $`d^2=4`$. A tetrahedron gives a set of effects with independent information. Let $`k=1,2,3,4`$ label its four unit vectors:

```math
\mathbf n_k\in\frac1{\sqrt3}\{(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)\}.
```

Write $`\boldsymbol\sigma=(X,Y,Z)`$ and define $`E_k=(I+\mathbf n_k\cdot\boldsymbol\sigma)/4`$. Here the dot product means $`n_{k,x}X+n_{k,y}Y+n_{k,z}Z`$. The effects are positive and sum to $`I`$. Their probabilities satisfy

```math
p_k=\frac{1+\mathbf n_k\cdot\mathbf r}{4},\qquad
\mathbf r=3\sum_kp_k\mathbf n_k.
```

The tetrahedron satisfies $`\sum_k\mathbf n_k=0`$ and $`\sum_k\mathbf n_k\mathbf n_k^T=(4/3)I_3`$, where $`I_3`$ is the three-dimensional identity. These identities give the reconstruction formula. This is a symmetric special case of the four-outcome qubit family studied in the course. One apparatus setting can therefore determine all three Bloch components across repeated preparations.

The reconstruction identities use exact probabilities. An experiment estimates them with frequencies from a finite number of shots.

## Finite shots and measurement noise are different limitations

Finite sampling makes the estimated components fluctuate. For ideal Pauli measurements with independent shots,

```math
\mathrm{Var}(\hat r_a)=\frac{1-r_a^2}{N_a}.
```

Sampling uncertainty decreases with more shots. It does not fix an incorrect detector model or recover an unobserved direction.

Readout noise adds a separate limitation. Let $`\sigma_a`$ be the Pauli matrix for setting $`a`$, with known detector strength $`0<\eta_a\leq1`$. Its effects are $`E_{a,s}=(I+s\eta_a\sigma_a)/2`$, with $`s=\pm1`$.

The sample mean $`\hat m_a`$ estimates $`\eta_a r_a`$. Dividing by the known strength corrects this scale factor. For $`\eta_a<1`$, it also increases the variance:

```math
\hat r_a=\frac{\hat m_a}{\eta_a},\qquad
\mathrm{Var}(\hat r_a)=\frac{1-\eta_a^2r_a^2}{N_a\eta_a^2}.
```

Small $`\eta_a`$ amplifies sampling noise. At $`\eta_a=0`$ the component is unidentifiable. If both the state and detector strength are unknown, the data determine only their product. Separate calibration or additional assumptions are then necessary.

These fluctuations can make the reconstruction formula give $`|\hat{\mathbf r}|>1`$. The estimated matrix then has a negative eigenvalue and is not a valid state.

A fit can enforce validity. One method selects the density matrix that maximizes the multinomial log-likelihood:

```math
\sum_{a,s}n_{a,s}\log\mathrm{tr}(\rho E_{a,s})
\quad\text{subject to}\quad \rho\geq0,\ \mathrm{tr}\rho=1.
```

Projecting an estimate into the Bloch ball is simpler, but generally gives a different estimator. Either method can introduce bias. A valid fitted state can still disagree with the observed frequencies. Agreement with the data and uncertainty in the estimate require separate checks.

## What tomography does and does not validate

The fit depends on the detector model used in the probabilities. State tomography therefore estimates a preparation under that model. It does not also validate the detector or determine a channel. Process tomography uses a spanning set of known input states and reconstructs their outputs. Preparation and readout errors can otherwise appear as process errors.

For $`n`$ qubits a general state has $`4^n-1`$ parameters. Full reconstruction becomes expensive rapidly. Many engineering tasks need only one observable, a parity, or a few correlations. Estimating those quantities directly avoids full state reconstruction.

QEC syndrome records serve this narrower purpose. Ideal syndrome measurements report check values while preserving the encoded quantum information. The required measurement model therefore depends on what information the task needs.

## Check your understanding

1. Why do arbitrarily many $`Z`$ shots fail to distinguish $`\ket{+}`$ from $`\ket{-}`$?
2. With known $`\eta=0.5`$, a measured sign average of $`0.3`$ implies what estimate of $`r_z`$?
3. Reconstruct the state from the tetrahedral probabilities for $`\mathbf r=(0,0,1)`$.

<details>
<summary>Worked answers</summary>

1. Both states have $`r_z=0`$ and hence identical $`Z`$ distributions. The missing information is about the direction being measured, not the number of shots.
2. $`\hat r_z=0.3/0.5=0.6`$. Dividing by the strength also amplifies statistical fluctuations; it is not free error removal.
3. For the two vertices with positive $`z`$, $`p_k=(1+1/\sqrt3)/4`$; for the other two, $`p_k=(1-1/\sqrt3)/4`$. Substituting into $`3\sum_kp_k\mathbf n_k`$ yields $`(0,0,1)`$ and $`\rho=\ket{0}\bra{0}`$.

</details>

Last updated: 2026-11-09
