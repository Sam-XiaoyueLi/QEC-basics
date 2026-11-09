# 1. States and subsystems

A quantum state describes a preparation through the measurement probabilities it predicts. Two preparations represent the same state if every measurement gives the same probabilities. We first need a mathematical description of that input before we can describe a detector.

[Learning path](README.md) · Course: opening of Chapter 1 and §§1.1–1.1.2, pp. 7–16.

## From a state vector to a density matrix

For a system with $`d`$ basis states, state vectors belong to the Hilbert space $`\mathbb C^d`$. This is a complex vector space with an inner product. Let $`\ket{\psi}`$ and $`\ket{\phi}`$ be two vectors in this space. In a fixed orthonormal basis, their components are $`\psi_j`$ and $`\phi_j`$. The indices $`j,k`$ run from $`0`$ to $`d-1`$.

A ket is a column vector. Its bra is the conjugate-transposed row:

```math
\bra{\psi}=(\ket{\psi})^\dagger.
```

The dagger denotes conjugate transpose. Their **inner product** is the complex scalar

```math
\braket{\phi|\psi}=\sum_{j=0}^{d-1}\overline{\phi_j}\,\psi_j,
```

where the overline means complex conjugation. For normalized vectors, $`|\braket{\phi|\psi}|^2`$ is the probability of projecting the state $`\ket{\psi}`$ onto $`\ket{\phi}`$. The condition $`\braket{\psi|\psi}=1`$ means that the vector is normalized. This is the usual [Dirac inner-product convention](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/quantum-circuits/inner-products-and-projections).

The inner product gives a scalar. Multiplying a ket by its bra gives an **outer product**, which is a matrix. The density matrix of the normalized pure state $`\ket{\psi}`$ is

```math
\rho=\ket{\psi}\bra{\psi},\qquad \rho_{jk}=\psi_j\overline{\psi_k}.
```

A single vector describes a pure state. A preparation can also randomly select between several pure states. Let $`\ell`$ label these choices, with normalized vector $`\ket{\psi_\ell}`$ and probability $`p_\ell`$. The density matrix averages their outer products:

```math
\rho=\sum_\ell p_\ell\ket{\psi_\ell}\bra{\psi_\ell},
\qquad p_\ell\geq0,\quad\sum_\ell p_\ell=1.
```

A normalized linear combination of state vectors describes a coherent superposition. Averaging density matrices describes a statistical mixture. Different ensembles can give the same density matrix. Thus the matrix determines measurement probabilities but does not uniquely identify the preparation procedure.

These constructions give a Hermitian, positive semidefinite matrix with trace one. These are also the conditions that any valid density matrix must satisfy. Hermitian means equal to its conjugate transpose.

Positive semidefinite means all eigenvalues are nonnegative, or equivalently $`\bra{v}\rho\ket{v}\geq0`$ for every column vector $`\ket{v}`$. Here the operator $`\rho`$ acts between the bra and ket.
In finite dimensions, the trace is the sum of diagonal entries.

The **purity** is $`\mathrm{tr}(\rho^2)`$. A pure state satisfies $`\rho^2=\rho`$ and has purity one. A mixed state has purity below one.

The distinction between a superposition and a mixture becomes clear when we compare their measurement probabilities.

## Superposition and mixture predict different measurements

For a qubit, the computational basis is $`\ket{0}=(1,0)^T`$ and $`\ket{1}=(0,1)^T`$. Here $`T`$ means transpose. The following two preparations use this basis.

**The first preparation produces the same superposition on every run.** Its vector is $`\ket{+}`$, and its density matrix $`\rho_+`$ is the outer product:

```math
\ket{+}=\frac{\ket{0}+\ket{1}}{\sqrt2},\qquad
\rho_+=\ket{+}\bra{+}=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}.
```

**The second preparation randomly selects a basis state.** It produces $`\ket{0}`$ or $`\ket{1}`$, each with probability $`1/2`$. The choice is not retained. The density matrix of this mixture is $`\rho_{\mathrm{mix}}`$. The ensemble rule gives

```math
\rho_{\mathrm{mix}}=\frac12\ket{0}\bra{0}+\frac12\ket{1}\bra{1}
=\frac12\begin{pmatrix}1&0\\0&1\end{pmatrix}.
```

These matrices have the same diagonal entries but different off-diagonal entries. To see what that difference means, measure each preparation in the computational basis. The probability of the outcome associated with a normalized basis vector $`\ket{b}`$ is $`p(b)=\bra{b}\rho\ket{b}`$. For a pure state, this is the squared magnitude of the inner product. For a mixture, it averages that probability over the preparations.

Both matrices therefore give $`p(0)=p(1)=1/2`$. This measurement cannot distinguish them.

A basis containing $`\ket{+}`$ can distinguish the preparations. The second vector in this basis must be orthogonal to $`\ket{+}`$. It is

```math
\ket{-}=\frac{\ket{0}-\ket{1}}{\sqrt2},\qquad \braket{-|+}=0.
```

Measuring in the $`\{\ket{+},\ket{-}\}`$ basis asks whether the state lies along the plus or minus direction. For the superposition,

```math
p(+\mid\rho_+)=\bra{+}\rho_+\ket{+}=1,\qquad
p(-\mid\rho_+)=0.
```

For the random preparation, either input basis state gives either sign with probability $`1/2`$, so

```math
p(+\mid\rho_{\mathrm{mix}})=p(-\mid\rho_{\mathrm{mix}})=\frac12.
```

The off-diagonal entries of $`\rho_+`$ describe **coherence relative to the computational basis**. They affect the probabilities measured in another basis. Their absence in $`\rho_{\mathrm{mix}}`$ is why the two preparations are physically different despite identical computational-basis probabilities. Coherence depends on the basis used to write the matrix. Purity is independent of the basis: $`\mathrm{tr}(\rho_+^2)=1`$ and $`\mathrm{tr}(\rho_{\mathrm{mix}}^2)=1/2`$.

These two measurement bases reveal different information about one qubit. The Bloch vector organizes this information into three real numbers.

## One qubit in three real numbers

The two measurements above are called Pauli $`Z`$ and Pauli $`X`$ measurements. Together with Pauli $`Y`$, their matrices are

```math
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
```

The eigenvectors of $`Z`$ are $`\ket{0},\ket{1}`$, with outcomes $`+1,-1`$. The eigenvectors of $`X`$ are $`\ket{+},\ket{-}`$, with the same outcome labels. Thus the previous example compared a $`Z`$ measurement with an $`X`$ measurement.

With $`I`$ denoting the identity matrix, every qubit state can be written as

```math
\rho=\frac12(I+r_xX+r_yY+r_zZ)
=\frac12\begin{pmatrix}1+r_z&r_x-ir_y\\r_x+ir_y&1-r_z\end{pmatrix}.
```

The Bloch vector $`\mathbf r=(r_x,r_y,r_z)`$ has length at most one. Its components are $`r_j=\mathrm{tr}(\rho\sigma_j)`$, where $`\sigma_x=X`$, $`\sigma_y=Y`$, and $`\sigma_z=Z`$. The eigenvalues are $`(1\pm|\mathbf r|)/2`$, which explains the length constraint. Pure states lie on the unit sphere. Mixed states lie inside it.

For the two preparations above, $`\rho_+`$ has Bloch vector $`(1,0,0)`$ and $`\rho_{\mathrm{mix}}=I/2`$ has Bloch vector $`(0,0,0)`$. Their equal $`r_z`$ explains their identical $`Z`$ statistics. Their different $`r_x`$ explains their different $`X`$ statistics.

The detector in the next lesson measures information about $`r_z`$. Later, we use $`r_x`$ and $`r_y`$ to track disturbance and reconstruct the input state.

First, we need to include systems outside the measured qubit. A qubit can interact with an apparatus or be entangled with another qubit.

## Composite systems and the partial trace

Let $`\mathcal H_A`$ and $`\mathcal H_B`$ be the state-vector spaces of systems $`A`$ and $`B`$. Their joint space is $`\mathcal H_A\otimes\mathcal H_B`$. For independent preparations the joint state is $`\rho_A\otimes\rho_B`$.

A joint state is **separable** if it is a probabilistic mixture of product states. Otherwise, it is **entangled**. A pure joint state is entangled exactly when it cannot be written as a product vector. The basis order here is $`\ket{00},\ket{01},\ket{10},\ket{11}`$, with system $`A`$ first.

Let $`\rho_{AB}`$ be the joint density matrix, with basis indices $`a,a'`$ for $`A`$ and $`b`$ for $`B`$. If we can access only $`A`$, its state is

```math
\rho_A=\mathrm{tr}_B(\rho_{AB}),\qquad
(\rho_A)_{a,a'}=\sum_b(\rho_{AB})_{ab,a'b}.
```

The partial trace sums over matching indices of the discarded system. Let $`A_0`$ be an observable on system $`A`$, and let $`I_B`$ be the identity on $`B`$. The reduced state preserves the expected value:

```math
\mathrm{tr}[\rho_{AB}(A_0\otimes I_B)]
=\mathrm{tr}(\rho_AA_0).
```

The Bell vector $`\ket{\Phi^+}=(\ket{00}+\ket{11})/\sqrt2`$ describes a pure joint state. Each reduced state is $`I/2=\rho_{\mathrm{mix}}`$. Every measurement on that qubit alone therefore gives the same statistics as the random preparation above. Its correlations distinguish it from joint states with the same reduced states. A mixed reduced state does not mean that the global state was a classical mixture.

Discarding $`B`$ is different from measuring $`B`$ and retaining its result. Discarding gives one reduced state. Keeping a measurement result gives a classical record and a state conditioned on that record. [Instruments](instruments-and-apparatus.md) will make this distinction precise.

## Extending the state space beyond qubits

The apparatus can include a continuous pointer instead of another qubit. Its state then needs a larger Hilbert space. Its inner product defines distances between vectors. Completeness ensures that sequences whose vectors eventually stay arbitrarily close have a limit in the space. This property is automatic in finite dimensions. In infinite dimensions, the space and operator domains need more care.

An apparatus model can require two different ways to combine spaces. The tensor product combines subsystems and multiplies their dimensions. A direct sum, $`\mathcal H_1\oplus\mathcal H_2`$, combines orthogonal sectors and adds dimensions. Direct sums help construct outcome sectors in dilation proofs. A direct sum alone still allows coherence between sectors. Treating a sector label as classical also requires restrictions on the states or observables.

The course's $`L^2(\mathbb R)`$ consists of square-integrable wavefunctions and supports position, momentum, and a moving pointer. Its harmonic-oscillator basis and its wavefunction description are representations of the same Hilbert space. The state space changes, but the purpose remains the same: predict the probabilities of measurement records.

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
