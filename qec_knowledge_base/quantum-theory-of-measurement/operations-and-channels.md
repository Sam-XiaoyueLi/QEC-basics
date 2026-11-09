# 3. State changes: operations and channels

The previous lesson described the classical record through a POVM. It left the output state unspecified. To describe that state, we need a map on density matrices. A **quantum channel**, written $`\Phi`$, describes a process without selection on a measurement result. Gates, noise, and reset are examples.

[Learning path](README.md) · Previous: [Effects and POVMs](effects-and-povms.md) · Course: §§1.3–1.3.1, pp. 26–34.

## Why linearity and complete positivity are physical requirements

For input states $`\rho_1,\rho_2`$ and mixing probability $`0\leq t\leq1`$, randomizing the preparation must agree with randomizing the outputs:

```math
\Phi(t\rho_1+(1-t)\rho_2)=t\Phi(\rho_1)+(1-t)\Phi(\rho_2).
```

This rule preserves the meaning of a statistical mixture. The corresponding map on operators is linear.

The output must also remain a valid state. A channel preserves trace and is **completely positive** (CP). Positivity means that positive inputs give positive outputs. Complete positivity requires this property even when the input is entangled with a reference system $`R`$. The joint map is $`\Phi\otimes\mathrm{id}_R`$, where $`\mathrm{id}_R`$ leaves the reference unchanged.

Transposition illustrates why this matters. The map $`\rho\mapsto\rho^T`$ preserves positivity and trace for an isolated system. Applied to one half of a Bell state, however, it produces an operator with eigenvalues $`1/2,1/2,1/2,-1/2`$. It cannot be a deterministic physical channel on arbitrary inputs.

A measurement result selects only some runs of the process. A **quantum operation** describes such a branch. It is CP and cannot increase the trace of a positive input.

For a branch operation $`\Phi`$ and normalized input $`\rho`$, the branch probability is $`p=\mathrm{tr}[\Phi(\rho)]`$. Its normalized conditional state is $`\Phi(\rho)/p`$ when $`p>0`$. The operation remains linear before normalization. Dividing by $`p`$ usually makes the conditional update nonlinear because $`p`$ depends on the input.

These conditions define allowed maps. Kraus operators give a matrix form that satisfies complete positivity and is suitable for computation.

## Kraus operators: the form to implement

A CP map in finite dimensions can be written using matrices $`K_\ell`$, called **Kraus operators**. The index $`\ell`$ labels the terms:

```math
\Phi(\rho)=\sum_\ell K_\ell\rho K_\ell^\dagger.
```

It is an operation if $`\sum_\ell K_\ell^\dagger K_\ell\leq I`$ and a channel if equality holds. The dagger is conjugate transpose. Kraus operators may be rectangular if input and output dimensions differ. Different Kraus sets can describe the same map. A term in the sum does not necessarily correspond to an observed result.

The following channels act on a qubit. Here $`U`$ is a unitary matrix and $`q`$ is a phase-flip probability, with $`0\leq q\leq1`$:

| Process | Kraus operators | Result |
| --- | --- | --- |
| Unitary gate | $`K=U`$, $`U^\dagger U=I`$ | $`U\rho U^\dagger`$ |
| Random phase flip | $`K_0=\sqrt{1-q}I`$, $`K_1=\sqrt q Z`$ | $`(1-q)\rho+qZ\rho Z`$ |
| Reset to zero | $`K_0=\ket{0}\bra{0}`$, $`K_1=\ket{0}\bra{1}`$ | $`\ket{0}\bra{0}\mathrm{tr}\rho`$ |

A phase flip with probability $`q`$ multiplies the off-diagonal entries by $`1-2q`$ and leaves the diagonal unchanged. At $`q=1/2`$, it removes the off-diagonal entries in the $`Z`$ basis. It therefore turns $`\rho_+`$ into $`\rho_{\mathrm{mix}}`$. At $`q=1`$ it is the unitary $`Z`$, not stronger dephasing.

The diagonal entries are the basis-state probabilities, also called **populations**. Phase flips change coherence without changing populations. **Amplitude damping** also changes populations through decay from $`\ket{1}`$ to $`\ket{0}`$. For decay probability $`0\leq\gamma\leq1`$, its Kraus operators are

```math
K_0=\begin{pmatrix}1&0\\0&\sqrt{1-\gamma}\end{pmatrix},\qquad
K_1=\begin{pmatrix}0&\sqrt\gamma\\0&0\end{pmatrix}.
```

The probability in $`\ket{1}`$ decreases, and the off-diagonal entries are multiplied by $`\sqrt{1-\gamma}`$. The identity $`K_0^\dagger K_0+K_1^\dagger K_1=I`$ confirms trace preservation.

These channels can turn pure states into mixed states. To see how this can follow from unitary evolution, we must include the environment.

## Stinespring dilation: including the environment

For a channel, an **ancilla** supplies an additional quantum system. It has an orthonormal basis $`\{\ket{\ell}\}`$, with one vector per Kraus operator. For an input vector $`\ket{\psi}`$, define

```math
V\ket{\psi}=\sum_\ell K_\ell\ket{\psi}\otimes\ket{\ell}.
```

The Kraus normalization gives $`V^\dagger V=I`$, so $`V`$ is an isometry: it preserves inner products. Taking the partial trace over the ancilla gives

```math
\Phi(\rho)=\mathrm{tr}_{\mathrm{anc}}(V\rho V^\dagger).
```

Preparing an ancilla and applying a larger unitary can implement this isometry. Correlations with the discarded ancilla can leave the system in a mixed state. This is **Stinespring dilation**: a channel is a reduced description of a larger unitary process.

For an operation that decreases trace, the same construction instead gives $`V^\dagger V\leq I`$. Such a map is a contraction. A complete physical process must include the other branches.

A Kraus representation proves that a map is CP. If software gives us the map in another form, a Choi matrix provides a direct validity check.

## Choi matrices: checking a map with one matrix

Let $`\{\ket{i}\}`$ be an orthonormal input basis of dimension $`d`$. Both indices $`i,j`$ run over this basis. The **Choi matrix** stores the map applied to every basis operator. Here the input reference comes first, and the output comes second:

```math
J_\Phi=\sum_{i,j}\ket{i}\bra{j}\otimes\Phi(\ket{i}\bra{j}).
```

In finite dimensions, $`\Phi`$ is CP exactly when $`J_\Phi\geq0`$. It preserves trace exactly when $`\mathrm{tr}_{\mathrm{out}}J_\Phi=I_{\mathrm{in}}`$, where $`I_{\mathrm{in}}`$ is the input identity. Thus a channel has $`\mathrm{tr}J_\Phi=d`$. For an operation the partial trace is bounded above by $`I_{\mathrm{in}}`$.

The course uses a normalized entangled vector in its finite-dimensional construction. With equal reference weights, its Choi operator is $`J_\Phi/d`$. Mixing these conventions produces incorrect normalization checks. The basis and tensor order matter too. IBM's [Choi API definition](https://quantum.cloud.ibm.com/docs/en/api/qiskit/2.2/qiskit.quantum_info.Choi) specifies the convention used by that library.

## Checking a numerical implementation

The conditions above become checks in a simulator. Check Hermiticity before using a Hermitian eigensolver. Allow a small tolerance for roundoff when checking eigenvalues, trace, and Kraus completeness. Substantial negative eigenvalues or trace drift indicate a problem.

Keep the trace of each unnormalized branch. Normalizing it too early removes the branch probability. Tensor order and conjugate transpose deserve explicit checks when moving between libraries.

## Predicting a later measurement with the dual map

After checking that a channel is valid, we can predict a measurement on its output. There are two equivalent calculations. We can transform the state first, or transform the observable back to the input.

For an output observable $`A`$, the **dual map** $`\Phi^{\ast}`$ makes these calculations agree:

```math
\mathrm{tr}[\Phi(\rho)A]=\mathrm{tr}[\rho\Phi^{\ast}(A)],\qquad
\Phi^{\ast}(A)=\sum_\ell K_\ell^\dagger A K_\ell.
```

Thus $`\Phi^{\ast}(A)`$ is the input observable with the same expected value as $`A`$ after the process. Trace preservation becomes $`\Phi^{\ast}(I)=I`$. This is the tool we will use to calculate how one measurement alters a later one.

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

A channel describes the output when we keep no result. An operation can describe one selected result. [Instruments and apparatus](instruments-and-apparatus.md) connect these maps to the classical labels of a POVM.

Last updated: 2026-11-09
