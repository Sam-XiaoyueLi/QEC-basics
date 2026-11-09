# 3. State changes: operations and channels

Knowing the probability of a detector result does not tell us what happens to the qubit. We need a map acting on density matrices. A deterministic physical process, including noise or reset, is a quantum channel $`\Phi`$.

[Learning path](README.md) · Previous: [Effects and POVMs](effects-and-povms.md) · Course: §§1.3–1.3.1, pp. 26–34.

## Why linearity and complete positivity are physical requirements

For input states $`\rho_1,\rho_2`$ and mixing probability $`0\leq t\leq1`$, randomizing the preparation must agree with randomizing the outputs:

```math
\Phi(t\rho_1+(1-t)\rho_2)=t\Phi(\rho_1)+(1-t)\Phi(\rho_2).
```

The extension to operators is linear. A channel preserves trace and is completely positive (CP). Positivity alone means positive inputs yield positive outputs. Complete positivity requires $`\Phi\otimes\mathrm{id}_R`$ to remain positive for every reference system $`R`$, where $`\mathrm{id}_R`$ is the identity map that leaves that system unchanged. A local operation must remain valid if its input is entangled with an untouched reference.

Transposition illustrates why this matters. The map $`\rho\mapsto\rho^T`$ preserves positivity and trace for an isolated system. Applied to one half of a Bell state, however, it produces an operator with eigenvalues $`1/2,1/2,1/2,-1/2`$. It cannot be a deterministic physical channel on arbitrary inputs.

A quantum operation is CP and trace-nonincreasing on positive inputs. It describes a possible branch, such as successful detection. For normalized $`\rho`$, the branch weight is $`p=\mathrm{tr}[\Phi(\rho)]`$. Its normalized conditional state is $`\Phi(\rho)/p`$ when $`p>0`$. This normalized update is generally nonlinear in $`\rho`$ because the denominator depends on the input; the unnormalized operation remains linear.

## Kraus operators: the form to implement

Every finite-dimensional CP map has a representation

```math
\Phi(\rho)=\sum_\ell K_\ell\rho K_\ell^\dagger.
```

It is an operation if $`\sum_\ell K_\ell^\dagger K_\ell\leq I`$ and a channel if equality holds. The dagger is conjugate transpose. Kraus operators may be rectangular if input and output dimensions differ. The representation is not unique; the map is the physical object. A Kraus index is not automatically an experimentally available record.

The following examples show what a channel can represent:

| Process | Kraus operators | Result |
| --- | --- | --- |
| Unitary gate | $`K=U`$, $`U^\dagger U=I`$ | $`U\rho U^\dagger`$ |
| Random phase flip | $`K_0=\sqrt{1-q}I`$, $`K_1=\sqrt q Z`$ | $`(1-q)\rho+qZ\rho Z`$ |
| Reset to zero | $`K_0=\ket{0}\bra{0}`$, $`K_1=\ket{0}\bra{1}`$ | $`\ket{0}\bra{0}\mathrm{tr}\rho`$ |

A phase flip with probability $`q`$ multiplies the off-diagonal entries by $`1-2q`$ and leaves the diagonal unchanged. At $`q=1/2`$ it completely dephases in the $`Z`$ basis: applied to $`\rho_+`$, it removes the off-diagonal entries and produces $`\rho_{\mathrm{mix}}`$. At $`q=1`$ it is the unitary $`Z`$, not stronger dephasing.

As an energy-relaxation example, amplitude damping with decay probability $`0\leq\gamma\leq1`$ has

```math
K_0=\begin{pmatrix}1&0\\0&\sqrt{1-\gamma}\end{pmatrix},\qquad
K_1=\begin{pmatrix}0&\sqrt\gamma\\0&0\end{pmatrix}.
```

It transfers excited-state population to $`\ket{0}`$ and multiplies coherence by $`\sqrt{1-\gamma}`$. Verify $`K_0^\dagger K_0+K_1^\dagger K_1=I`$ before using it.

## Stinespring dilation: where the apparent randomness can come from

For a channel with Kraus operators $`K_\ell`$, choose an orthonormal ancilla basis $`\{\ket{\ell}\}`$. For any input vector $`\ket{\psi}`$, define the isometry $`V`$ by

```math
V\ket{\psi}=\sum_\ell K_\ell\ket{\psi}\otimes\ket{\ell}.
```

The Kraus normalization ensures $`V^\dagger V=I`$. Then

```math
\Phi(\rho)=\mathrm{tr}_{\mathrm{anc}}(V\rho V^\dagger).
```

An isometry can be realized by preparing an ancilla and extending the action to a unitary on a sufficiently large system. Correlations with the discarded ancilla produce mixed reduced states, even when the combined evolution is unitary. This is the practical content of Stinespring dilation. For a trace-decreasing operation, the corresponding $`V`$ is a contraction, and a deterministic realization needs additional branches completing the process.

## Choi matrices: checking a map with one matrix

Fix an input basis $`\ket{i}`$ of dimension $`d`$. We use the unnormalized convention, with input reference first and output second:

```math
J_\Phi=\sum_{i,j}\ket{i}\bra{j}\otimes\Phi(\ket{i}\bra{j}).
```

In finite dimensions, $`\Phi`$ is CP exactly when $`J_\Phi\geq0`$. It is trace-preserving exactly when $`\mathrm{tr}_{\mathrm{out}}J_\Phi=I_{\mathrm{in}}`$. Thus a channel has $`\mathrm{tr}J_\Phi=d`$. For an operation the partial trace is bounded above by $`I_{\mathrm{in}}`$.

The course uses a normalized entangled vector in its finite-dimensional construction. With equal reference weights, its Choi operator is $`J_\Phi/d`$. Mixing these conventions produces incorrect normalization checks. The basis and tensor order matter too. IBM's [Choi API definition](https://quantum.cloud.ibm.com/docs/en/api/qiskit/2.2/qiskit.quantum_info.Choi) explicitly specifies its convention; always inspect a library's convention before exchanging matrices.

## Moving a process from states to observables

For an output observable $`A`$, the dual, or Heisenberg, map $`\Phi^{\ast}`$ is defined by

```math
\mathrm{tr}[\Phi(\rho)A]=\mathrm{tr}[\rho\Phi^{\ast}(A)],\qquad
\Phi^{\ast}(A)=\sum_\ell K_\ell^\dagger A K_\ell.
```

It answers: which observable on the input reproduces a measurement made after the process? Trace preservation becomes $`\Phi^{\ast}(I)=I`$. This is the tool we will use to calculate how one measurement alters a later one.

## Numerical checks for an implementation

Check Hermiticity before using a Hermitian eigensolver, and use a small tolerance for roundoff when checking eigenvalues, trace, and Kraus completeness. Substantial negative eigenvalues or trace drift indicate a problem. Do not silently normalize every intermediate matrix: an operation's trace carries its branch probability. Tensor order and conjugate transpose deserve explicit checks when moving between libraries.

## Check your understanding

1. Apply amplitude damping to $`\ket{1}\bra{1}`$ and to $`\ket{+}\bra{+}`$.
2. Why is a reset not a unitary gate on the qubit alone?
3. Why does testing a map on several single-qubit states not establish complete positivity?

<details>
<summary>Worked answers</summary>

1. The outputs are $`\mathrm{diag}(\gamma,1-\gamma)`$ and

$`\frac12\begin{pmatrix}1+\gamma&\sqrt{1-\gamma}\\\sqrt{1-\gamma}&1-\gamma\end{pmatrix}`$.

2. Reset maps two orthogonal inputs to the same output. A unitary preserves inner products and is invertible. Reset can still arise from a larger unitary process by discarding a system carrying the input information.
3. Even positivity on every isolated input would not test entangled extensions. The transpose map is the counterexample. A valid Kraus representation or a positive Choi matrix provides a finite-dimensional CP check.

</details>

Next: [Instruments and apparatus](instruments-and-apparatus.md) associate operations with recorded outcomes.

Last updated: 2026-11-09
