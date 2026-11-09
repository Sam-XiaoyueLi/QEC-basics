# 1. States and subsystems

A state summarizes everything about a preparation that affects measurement probabilities. If two preparation procedures give the same probabilities for every possible measurement, they represent the same state. This operational definition is why a density matrix can describe both a deliberately randomized preparation and a subsystem entangled with something else.

[Learning path](README.md) · Course: opening of Chapter 1 and §§1.1–1.1.2, pp. 7–16.

## From a state vector to a density matrix

In matrix notation, $`|\psi\rangle`$ is a column vector, $`\langle\psi|`$ is its conjugate-transposed row, and $`\langle\phi|\psi\rangle`$ is their inner product. The outer product $`|\psi\rangle\langle\psi|`$ is a matrix. Normalization means $`\langle\psi|\psi\rangle=1`$. An operator is Hermitian when it equals its conjugate transpose.

A normalized vector $`|\psi\rangle`$ represents a pure state. Its density matrix is

```math
\rho=|\psi\rangle\langle\psi|.
```

If preparation $`j`$ is selected with probability $`p_j`$, use

```math
\rho=\sum_jp_j|\psi_j\rangle\langle\psi_j|,
\qquad p_j\geq0,\quad\sum_jp_j=1.
```

You average the density matrices, not the state vectors. Adding vectors describes coherent superposition; averaging density matrices describes statistical mixing. Different ensembles can give the same density matrix, so its decomposition does not uniquely identify how it was prepared.

A valid density matrix is Hermitian, positive semidefinite, and has trace one. Positive semidefinite means all eigenvalues are nonnegative, or equivalently $`\langle v|\rho|v\rangle\geq0`$ for every vector $`v`$. In finite dimensions, the trace is the sum of diagonal entries. For a pure state $`\rho^2=\rho`$ and $`\mathrm{tr}(\rho^2)=1`$; for a mixed state the purity $`\mathrm{tr}(\rho^2)`$ is smaller than one.

Consider

```math
|+\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2},\qquad
\rho_+=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix},\qquad
\rho_{\mathrm{mix}}=\frac12\begin{pmatrix}1&0\\0&1\end{pmatrix}.
```

Here $`|-\rangle=(|0\rangle-|1\rangle)/\sqrt2`$. Both give equal probabilities for $`0`$ and $`1`$ in the computational basis. But measuring in the $`\{|+\rangle,|-\rangle\}`$ basis always gives $`+`$ for $`\rho_+`$ and gives either sign equally for $`\rho_{\mathrm{mix}}`$. The off-diagonal entries encode coherence relative to the chosen basis. Coherence is basis-dependent; purity is not.

## One qubit in three real numbers

Define

```math
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
```

Every qubit state can be written as

```math
\rho=\frac12(I+r_xX+r_yY+r_zZ)
=\frac12\begin{pmatrix}1+r_z&r_x-ir_y\\r_x+ir_y&1-r_z\end{pmatrix}.
```

The Bloch vector $`\mathbf r=(r_x,r_y,r_z)`$ has length at most one. Its components are $`r_j=\mathrm{tr}(\rho\sigma_j)`$, where $`\sigma_x=X`$, $`\sigma_y=Y`$, and $`\sigma_z=Z`$. The eigenvalues are $`(1\pm|\mathbf r|)/2`$, which explains the length constraint. Pure states lie on the unit sphere; mixed states lie inside it.

Our running measurement will first reveal only $`r_z`$. The other two components will matter when we ask what the measurement disturbs and whether its data suffice for reconstruction.

## Composite systems and the partial trace

Two systems $`A`$ and $`B`$ live in $`\mathcal H_A\otimes\mathcal H_B`$. For independent preparations the joint state is $`\rho_A\otimes\rho_B`$. A joint state is separable if it is a probabilistic mixture of product states; otherwise it is entangled. A pure joint state is entangled exactly when it cannot be written as a product vector. In a two-qubit implementation, fix the basis order explicitly; here it is $`|00\rangle,|01\rangle,|10\rangle,|11\rangle`$, with $`A`$ first.

If we can access only $`A`$, its state is

```math
\rho_A=\mathrm{tr}_B(\rho_{AB}),\qquad
(\rho_A)_{a,a'}=\sum_b(\rho_{AB})_{ab,a'b}.
```

The partial trace sums over matching indices of the discarded system. It is defined so that every local prediction is preserved:

```math
\mathrm{tr}[\rho_{AB}(E_A\otimes I_B)]
=\mathrm{tr}(\rho_AE_A).
```

For the Bell state $`|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2`$, the joint state is pure but either reduced state is $`I/2`$. The information needed to distinguish the Bell state from other joint states lies in correlations. A mixed reduced state does not mean that the global state was a classical mixture.

Discarding $`B`$ is different from measuring $`B`$ and retaining its result. Discarding gives one reduced state; retaining a result gives a conditional state and a classical record. [Instruments](instruments-and-apparatus.md) will make this distinction precise.

## Why the Hilbert-space material is here

A Hilbert space is an inner-product vector space complete under its induced norm. For finite-dimensional software examples, it is simply $`\mathbb C^d`$ with its usual inner product. Completeness and boundedness require more care for wavefunctions and infinite-dimensional systems.

The tensor product combines subsystems and multiplies dimensions. A direct sum, $`\mathcal H_1\oplus\mathcal H_2`$, combines orthogonal sectors and adds dimensions. Direct sums help construct outcome sectors in dilation proofs. A direct sum alone does not forbid coherence between sectors; interpreting a sector label as classical also restricts the relevant states or observables.

The course's $`L^2(\mathbb R)`$ consists of square-integrable wavefunctions and supports position, momentum, and a moving pointer. Its harmonic-oscillator basis and its wavefunction description are representations of the same Hilbert space. Understanding these roles is enough for the finite-dimensional path.

## Check your understanding

1. Why can a $`Z`$ measurement not distinguish $`\rho_+`$ from $`I/2`$? Which measurement can?
2. Trace out $`B`$ from $`|\Phi^+\rangle\langle\Phi^+|`$. Which terms disappear, and why?
3. Is $`\rho=(I+0.8X+0.8Z)/2`$ a valid state?

<details>
<summary>Worked answers</summary>

1. Their computational-basis diagonals agree. An $`X`$ measurement gives $`+`$ with probability one for $`\rho_+`$ and one half for $`I/2`$.
2. The diagonal terms give $`|0\rangle\langle0|/2`$ and $`|1\rangle\langle1|/2`$. The cross terms contain $`|0\rangle\langle1|`$ or its adjoint on $`B`$, each with trace zero. The result is $`I/2`$.
3. No. The Bloch length is $`\sqrt{1.28}>1`$, giving one negative eigenvalue.

</details>

Next: [Effects and POVMs](effects-and-povms.md) turn the state into detector probabilities.

Last updated: 2026-11-09
