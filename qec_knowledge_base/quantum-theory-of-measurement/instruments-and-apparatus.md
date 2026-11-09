# 4. Complete measurements: instruments and apparatus

One device measures $`Z`$ and leaves the corresponding eigenstate. Another reports the same outcome and then resets the qubit to zero. Their POVMs agree, but their output states differ. To describe a complete measurement we must associate a state transformation with each recorded result.

[Learning path](README.md) · Previous: [Operations and channels](operations-and-channels.md) · Course: §§1.4–1.5.1, pp. 34–47.

## One instrument, three predictions

An instrument is a collection of CP operations $`\{\mathcal I_s\}`$ whose sum is a channel. Write each outcome operation as

```math
\mathcal I_s(\rho)=\sum_\ell K_{s\ell}\rho K_{s\ell}^\dagger,
\qquad\sum_{s,\ell}K_{s\ell}^\dagger K_{s\ell}=I.
```

The outcome label $`s`$ is observed; $`\ell`$ can represent unresolved alternatives within that outcome. The instrument gives

```math
p_s=\mathrm{tr}[\mathcal I_s(\rho)],\qquad
\rho_s=\frac{\mathcal I_s(\rho)}{p_s},\qquad
\Phi(\rho)=\sum_s\mathcal I_s(\rho).
```

A branch is the part of the output associated with one recorded result. Use $`\rho_s`$ only when $`p_s>0`$. Use $`\Phi(\rho)`$ when the record is discarded. The corresponding effect is $`E_s=\sum_\ell K_{s\ell}^\dagger K_{s\ell}=\mathcal I_s^{\ast}(I)`$.

A simulator following one experimental shot samples $`s`$ with weight $`p_s`$ and stores $`\rho_s`$. An exact branching simulator retains every unnormalized branch $`\mathcal I_s(\rho)`$ and its label. Averaging normalized branches with equal weights is generally wrong: each branch must be weighted by its probability.

## Choose an instrument for the running POVM

For $`E_s=(I+s\eta Z)/2`$, choose the Lüders instrument $`\mathcal I_s(\rho)=\sqrt{E_s}\rho\sqrt{E_s}`$. Its single Kraus operator per outcome is

```math
K_+=\begin{pmatrix}a&0\\0&b\end{pmatrix},\quad
K_-=\begin{pmatrix}b&0\\0&a\end{pmatrix},\qquad
a=\sqrt{\frac{1+\eta}{2}},\quad b=\sqrt{\frac{1-\eta}{2}}.
```

For an input Bloch vector $`(r_x,r_y,r_z)`$, the branch probabilities remain $`p_s=(1+s\eta r_z)/2`$. On a nonzero-probability branch,

```math
r'_{z,s}=\frac{r_z+s\eta}{1+s\eta r_z},\qquad
r'_{x,s}=\frac{\sqrt{1-\eta^2}\,r_x}{1+s\eta r_z},\qquad
r'_{y,s}=\frac{\sqrt{1-\eta^2}\,r_y}{1+s\eta r_z}.
```

For $`\ket{+}`$ and $`\eta=0.6`$, both outcomes have probability $`1/2`$ and the conditional Bloch vectors are $`(0.8,0,\pm0.6)`$. Both states are pure. Ignoring the result averages them to $`(0.8,0,0)`$, which is mixed.

In general the discarded-record channel is

```math
\Phi(\rho)=\begin{pmatrix}\rho_{00}&c\rho_{01}\\c\rho_{10}&\rho_{11}\end{pmatrix},
\qquad c=\sqrt{1-\eta^2}.
```

Equivalently, $`\Phi(\rho)=(1-q)\rho+qZ\rho Z`$ with $`q=(1-c)/2`$. Here stronger measurement suppresses more $`Z`$-basis coherence. This relation belongs to this instrument, not to every implementation of the POVM.

## Same readout statistics, different disturbance

Sharp $`Z`$ measurement followed by classical label errors $`\epsilon=(1-\eta)/2`$ has the outcome operations

```math
\mathcal J_s(\rho)=(1-\epsilon)P_s\rho P_s+\epsilon P_{-s}\rho P_{-s},
\qquad P_s=\frac12(I+sZ).
```

It has the same effects $`E_s`$, but $`\sum_s\mathcal J_s(\rho)`$ completely removes $`Z`$-basis coherence for every $`\epsilon`$. At $`\eta=0`$, the chosen Lüders instrument leaves the input unchanged, whereas this implementation completely dephases it while reporting an uninformative bit. An uninformative record does not guarantee an undisturbed state.

## Ancilla implementation and the physical model

Prepare an ancilla in $`\ket{0}`$ and choose a unitary whose action on that input subspace is

```math
U(\ket{\psi}\otimes\ket{0})
=K_+\ket{\psi}\otimes\ket{0}+K_-\ket{\psi}\otimes\ket{1}.
```

The right side preserves inner products because $`K_+^\dagger K_++K_-^\dagger K_-=I`$, so it can be extended to a unitary. Measuring the ancilla in its computational basis realizes the instrument, with $`0`$ reporting $`+`$ and $`1`$ reporting $`-`$. Tracing it out realizes $`\Phi`$.

More generally, with probe state $`\sigma`$, interaction $`U`$, and pointer projections $`Z_s`$,

```math
\mathcal I_s(\rho)=\mathrm{tr}_{\mathrm{probe}}\left[
(I\otimes Z_s)U(\rho\otimes\sigma)U^\dagger(I\otimes Z_s)
\right].
```

The measurement-dilation theorem says that every instrument in the course's same-input/output setting has such a realization with a sufficiently large probe. Naimark dilation realizes statistics; Stinespring realizes transformations; instrument dilation realizes both. Different apparatus models can realize the same instrument.

The course's optical example uses $`\eta=\sin(2\gamma)`$; over $`0\leq\gamma\leq\pi/4`$, its Kraus operators coincide with the ones above. This connects the abstract parameter to a tunable apparatus.

<details>
<summary>Continuous-variable extension: the von Neumann pointer model (§1.4.1)</summary>

Let the system observable be $`R=\sum_r rP_r`$ and let the probe have position coordinate $`q`$ and momentum operator $`P`$. In units with $`\hbar=1`$, the coupling, with strength $`\Delta>0`$, is $`U=e^{-i\Delta R\otimes P}`$. On an $`R`$ eigenstate with value $`r`$, it shifts the probe wavefunction from $`\psi(q)`$ to $`\psi(q-\Delta r)`$.

The pointer density is therefore

```math
p(q)=\sum_r\mathrm{tr}(\rho P_r)|\psi(q-\Delta r)|^2.
```

Overlapping shifted packets make values difficult to distinguish. Narrower packets relative to their separation improve resolution. The unnormalized conditional update has operator density $`K(q)=\sum_r\psi(q-\Delta r)P_r`$; an interval $`B`$ gives $`\mathcal I_B(\rho)=\int_BK(q)\rho K(q)^\dagger\,dq`$.

Raw continuous pointer readings remain smeared. For discrete eigenvalues, coarse graining can recover an exact discrete PVM if the shifted packets have disjoint supports; Gaussian packets overlap at every finite width, so they only approximate this limit. This physical model supplies operational probabilities and conditional states, rather than resolving the interpretational question of why an individual outcome occurs.

</details>

## Feedback and QEC: retain the right record

If outcome $`s`$ triggers a unitary correction $`U_s`$, the overall feedback channel is

```math
\Psi(\rho)=\sum_s U_s\mathcal I_s(\rho)U_s^\dagger.
```

For sharp $`Z`$ measurement, applying $`X`$ after the minus outcome resets the qubit to zero. Discarding the outcome before applying feedback loses the information needed to choose the correction.

For an ideal two-qubit parity check, the effects and Lüders operations are

```math
P_s=\frac12(I+sZ\otimes Z),\qquad\mathcal I_s(\rho)=P_s\rho P_s.
```

Prepare an ancilla in $`\ket{0}`$, apply CNOTs from both data qubits to the ancilla, and measure its $`Z`$. Even parity gives bit zero; odd parity gives bit one. This distinguishes the two parity subspaces while preserving coherence inside either subspace. Measuring the two data qubits separately and taking their classical parity gives the same parity probabilities but destroys more coherence. In particular, it destroys the coherence of $`(\ket{00}+\ket{11})/\sqrt2`$, which an ideal parity check preserves.

This is why collective check measurements matter in [Gross-code state preparation](../gross-code/README.md#preparing-all-twelve-logical-qubits-in-zero). A fault-tolerant implementation must additionally account for faults propagating through the ancilla circuit; an ideal instrument alone does not establish fault tolerance.

## Check your understanding

1. Reproduce the conditional and discarded-record states for $`\ket{+}`$ at $`\eta=0.6`$.
2. Give two instruments with the same $`Z`$ PVM and different outputs.
3. Why does measuring individual bits and retaining only their parity differ from an ideal parity check?

<details>
<summary>Worked answers</summary>

1. The conditional matrices are $`\frac12\begin{pmatrix}1\pm0.6&0.8\\0.8&1\mp0.6\end{pmatrix}`$. Averaging with probabilities $`1/2`$ gives $`\frac12\begin{pmatrix}1&0.8\\0.8&1\end{pmatrix}`$.
2. Use $`\mathcal I_s(\rho)=P_s\rho P_s`$ and $`\mathcal J_s(\rho)=\mathrm{tr}(P_s\rho)\ket{0}\bra{0}`$. Both report the same probabilities, but only the second always outputs zero.
3. Separate measurements physically resolve $`00`$ from $`11`$. Deleting that classical distinction afterwards does not restore the coherence already lost. The parity instrument never resolves it.

</details>

Next: [Compatibility and disturbance](compatibility-and-disturbance.md).

Last updated: 2026-11-09
