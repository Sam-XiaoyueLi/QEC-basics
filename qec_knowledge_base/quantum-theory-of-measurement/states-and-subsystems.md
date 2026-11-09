# 1. States and subsystems

A state summarizes everything about a preparation that affects measurement probabilities. If two preparation procedures give the same probabilities for every possible measurement, they represent the same state. This operational definition is why a density matrix can describe both a deliberately randomized preparation and a subsystem entangled with something else.

[Learning path](README.md) · Course: opening of Chapter 1 and §§1.1–1.1.2, pp. 7–16.

## From a state vector to a density matrix

Let $`\ket{\psi}`$ and $`\ket{\phi}`$ be two state vectors in the same $`d`$-dimensional Hilbert space. In a fixed orthonormal basis, their components are $`\psi_j`$ and $`\phi_j`$, with component indices $`j,k=0,\ldots,d-1`$. Each ket is a column vector; its bra is the conjugate-transposed row:

```math
\bra{\psi}=(\ket{\psi})^\dagger.
```

The dagger denotes conjugate transpose. Their **inner product** is the complex scalar

```math
\braket{\phi|\psi}=\sum_{j=0}^{d-1}\overline{\phi_j}\,\psi_j,
```

where the overline means complex conjugation. For normalized vectors, $`|\braket{\phi|\psi}|^2`$ is the probability of projecting the state $`\ket{\psi}`$ onto $`\ket{\phi}`$. The self-inner-product $`\braket{\psi|\psi}=1`$ expresses normalization; it is a special case, not the general overlap between two states. This is the usual [Dirac inner-product convention](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/quantum-circuits/inner-products-and-projections).

Reversing the order gives an **outer product**, which is a matrix. The density matrix of the normalized pure state $`\ket{\psi}`$ is

```math
\rho=\ket{\psi}\bra{\psi},\qquad \rho_{jk}=\psi_j\overline{\psi_k}.
```

An operator is Hermitian when it equals its conjugate transpose.

For an ensemble of normalized states $`\ket{\psi_\ell}`$, where $`\ell`$ labels preparations and $`p_\ell`$ is the probability of preparation $`\ell`$, use

```math
\rho=\sum_\ell p_\ell\ket{\psi_\ell}\bra{\psi_\ell},
\qquad p_\ell\geq0,\quad\sum_\ell p_\ell=1.
```

You average the density matrices, not the state vectors. Adding vectors describes coherent superposition; averaging density matrices describes statistical mixing. Different ensembles can give the same density matrix, so its decomposition does not uniquely identify how it was prepared.

A valid density matrix is Hermitian, positive semidefinite, and has trace one. Positive semidefinite means all eigenvalues are nonnegative, or equivalently $`\bra{v}\rho\ket{v}\geq0`$ for every column vector $`\ket{v}`$. Here the operator $`\rho`$ acts between the bra and ket. In finite dimensions, the trace is the sum of diagonal entries. For a pure state $`\rho^2=\rho`$ and $`\mathrm{tr}(\rho^2)=1`$; for a mixed state the purity $`\mathrm{tr}(\rho^2)`$ is smaller than one.

For a qubit, the computational basis is $`\ket{0}=(1,0)^T`$ and $`\ket{1}=(0,1)^T`$, where $`T`$ denotes transpose. Compare the coherent superposition $`\ket{+}`$ with an equal mixture of these basis states:

```math
\ket{+}=\frac{\ket{0}+\ket{1}}{\sqrt2},\qquad
\rho_+=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix},\qquad
\rho_{\mathrm{mix}}=\frac12\begin{pmatrix}1&0\\0&1\end{pmatrix}.
```

Here $`\ket{-}=(\ket{0}-\ket{1})/\sqrt2`$. Both give equal probabilities for $`0`$ and $`1`$ in the computational basis. But measuring in the $`\{\ket{+},\ket{-}\}`$ basis always gives $`+`$ for $`\rho_+`$ and gives either sign equally for $`\rho_{\mathrm{mix}}`$. The off-diagonal entries encode coherence relative to the chosen basis. Coherence is basis-dependent; purity is not.

## One qubit in three real numbers

Define

```math
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
```

With $`I`$ denoting the identity matrix, every qubit state can be written as

```math
\rho=\frac12(I+r_xX+r_yY+r_zZ)
=\frac12\begin{pmatrix}1+r_z&r_x-ir_y\\r_x+ir_y&1-r_z\end{pmatrix}.
```

The Bloch vector $`\mathbf r=(r_x,r_y,r_z)`$ has length at most one. Its components are $`r_j=\mathrm{tr}(\rho\sigma_j)`$, where $`\sigma_x=X`$, $`\sigma_y=Y`$, and $`\sigma_z=Z`$. The eigenvalues are $`(1\pm|\mathbf r|)/2`$, which explains the length constraint. Pure states lie on the unit sphere; mixed states lie inside it.

Our running measurement will first reveal only $`r_z`$. The other two components will matter when we ask what the measurement disturbs and whether its data suffice for reconstruction.

## Composite systems and the partial trace

Let $`\mathcal H_A`$ and $`\mathcal H_B`$ be the state-vector spaces of systems $`A`$ and $`B`$. Their joint space is $`\mathcal H_A\otimes\mathcal H_B`$. For independent preparations the joint state is $`\rho_A\otimes\rho_B`$. A joint state is separable if it is a probabilistic mixture of product states; otherwise it is entangled. A pure joint state is entangled exactly when it cannot be written as a product vector. In a two-qubit implementation, fix the basis order explicitly; here it is $`\ket{00},\ket{01},\ket{10},\ket{11}`$, with $`A`$ first.

Let $`\rho_{AB}`$ be the joint density matrix, with basis indices $`a,a'`$ for $`A`$ and $`b`$ for $`B`$. If we can access only $`A`$, its state is

```math
\rho_A=\mathrm{tr}_B(\rho_{AB}),\qquad
(\rho_A)_{a,a'}=\sum_b(\rho_{AB})_{ab,a'b}.
```

The partial trace sums over matching indices of the discarded system. For any measurement effect $`E_A`$ on $`A`$, and identity $`I_B`$ on $`B`$, it preserves the local prediction:

```math
\mathrm{tr}[\rho_{AB}(E_A\otimes I_B)]
=\mathrm{tr}(\rho_AE_A).
```

For the Bell state $`\ket{\Phi^+}=(\ket{00}+\ket{11})/\sqrt2`$, the joint state is pure but either reduced state is $`I/2`$. The information needed to distinguish the Bell state from other joint states lies in correlations. A mixed reduced state does not mean that the global state was a classical mixture.

Discarding $`B`$ is different from measuring $`B`$ and retaining its result. Discarding gives one reduced state; retaining a result gives a conditional state and a classical record. [Instruments](instruments-and-apparatus.md) will make this distinction precise.

## Why the Hilbert-space material is here

A Hilbert space is an inner-product vector space complete under its induced norm. For finite-dimensional software examples, it is simply $`\mathbb C^d`$ with its usual inner product. Completeness and boundedness require more care for wavefunctions and infinite-dimensional systems.

The tensor product combines subsystems and multiplies dimensions. A direct sum, $`\mathcal H_1\oplus\mathcal H_2`$, combines orthogonal sectors and adds dimensions. Direct sums help construct outcome sectors in dilation proofs. A direct sum alone does not forbid coherence between sectors; interpreting a sector label as classical also restricts the relevant states or observables.

The course's $`L^2(\mathbb R)`$ consists of square-integrable wavefunctions and supports position, momentum, and a moving pointer. Its harmonic-oscillator basis and its wavefunction description are representations of the same Hilbert space. Understanding these roles is enough for the finite-dimensional path.

## Check your understanding

1. Why can a $`Z`$ measurement not distinguish $`\rho_+`$ from $`I/2`$? Which measurement can?
2. Trace out $`B`$ from $`\ket{\Phi^+}\bra{\Phi^+}`$. Which terms disappear, and why?
3. Is $`\rho=(I+0.8X+0.8Z)/2`$ a valid state?

<details>
<summary>Worked answers</summary>

1. Their computational-basis diagonals agree. An $`X`$ measurement gives $`+`$ with probability one for $`\rho_+`$ and one half for $`I/2`$.
2. The diagonal terms give $`\ket{0}\bra{0}/2`$ and $`\ket{1}\bra{1}/2`$. The cross terms contain $`\ket{0}\bra{1}`$ or its adjoint on $`B`$, each with trace zero. The result is $`I/2`$.
3. No. The Bloch length is $`\sqrt{1.28}>1`$, giving one negative eigenvalue.

</details>

Next: [Effects and POVMs](effects-and-povms.md) turn the state into detector probabilities.

Last updated: 2026-11-09
