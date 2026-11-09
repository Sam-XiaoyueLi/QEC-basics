# 4. Complete measurements: instruments and apparatus

A POVM predicts the classical result. An operation describes a state change. A complete measurement model must connect the two. For example, a device can measure $`Z`$ and leave the measured eigenstate. Another device can report the same result and then reset the qubit. Their outcome probabilities agree, but their output states differ.

[Learning path](README.md) · Previous: [Operations and channels](operations-and-channels.md) · Course: §§1.4–1.5.1, pp. 34–47.

## One instrument, three predictions

An **instrument** assigns a CP operation $`\mathcal I_s`$ to each recorded outcome $`s`$. Their sum must be a channel. With Kraus operators $`K_{s\ell}`$, each outcome operation has the form

```math
\mathcal I_s(\rho)=\sum_\ell K_{s\ell}\rho K_{s\ell}^\dagger,
\qquad\sum_{s,\ell}K_{s\ell}^\dagger K_{s\ell}=I.
```

The detector reports $`s`$. The index $`\ell`$ labels terms within that operation; the detector need not resolve them. For input state $`\rho`$, the instrument gives three predictions:

```math
p_s=\mathrm{tr}[\mathcal I_s(\rho)],\qquad
\rho_s=\frac{\mathcal I_s(\rho)}{p_s},\qquad
\Phi(\rho)=\sum_s\mathcal I_s(\rho).
```

Here $`p_s`$ is the outcome probability. The conditional state $`\rho_s`$ describes the system after that result and is defined only when $`p_s>0`$. The channel $`\Phi`$ gives the output when the record is discarded.

Writing the outcome probability as $`p_s=\mathrm{tr}(\rho E_s)`$ identifies the effect $`E_s=\sum_\ell K_{s\ell}^\dagger K_{s\ell}=\mathcal I_s^{\ast}(I)`$. The instrument therefore contains the outcome probabilities as well as the state changes.

A simulator for one shot samples $`s`$ with probability $`p_s`$ and stores $`\rho_s`$. A simulator for all branches keeps each unnormalized matrix $`\mathcal I_s(\rho)`$ and its label. To average normalized branches, it must weight each state by its probability.

We can now complete the tunable Z detector from lesson 2 by choosing its outcome operations.

## Choose an instrument for the running POVM

The detector has effects $`E_s=(I+s\eta Z)/2`$, where $`s=\pm1`$ and $`0\leq\eta\leq1`$. One choice is the **Lüders instrument**, $`\mathcal I_s(\rho)=\sqrt{E_s}\rho\sqrt{E_s}`$. It has one Kraus operator per outcome. Define the coefficients $`a,b`$ as follows:

```math
K_+=\begin{pmatrix}a&0\\0&b\end{pmatrix},\quad
K_-=\begin{pmatrix}b&0\\0&a\end{pmatrix},\qquad
a=\sqrt{\frac{1+\eta}{2}},\quad b=\sqrt{\frac{1-\eta}{2}}.
```

The input Bloch vector is $`(r_x,r_y,r_z)`$. The branch probabilities are $`p_s=(1+s\eta r_z)/2`$. A prime marks a component of the conditional output vector. For a branch with $`p_s>0`$,

```math
r'_{z,s}=\frac{r_z+s\eta}{1+s\eta r_z},\qquad
r'_{x,s}=\frac{\sqrt{1-\eta^2}\,r_x}{1+s\eta r_z},\qquad
r'_{y,s}=\frac{\sqrt{1-\eta^2}\,r_y}{1+s\eta r_z}.
```

For $`\ket{+}`$ and $`\eta=0.6`$, both outcomes have probability $`1/2`$ and the conditional Bloch vectors are $`(0.8,0,\pm0.6)`$. Both states are pure. Ignoring the result averages them to $`(0.8,0,0)`$, which is mixed.

The average also follows directly from summing the two operations. Writing the input entries as $`\rho_{ij}`$ in the computational basis gives

```math
\Phi(\rho)=\begin{pmatrix}\rho_{00}&c\rho_{01}\\c\rho_{10}&\rho_{11}\end{pmatrix},
\qquad c=\sqrt{1-\eta^2}.
```

This is the phase-flip channel from lesson 3: $`\Phi(\rho)=(1-q)\rho+qZ\rho Z`$, with $`q=(1-c)/2`$. For $`\rho_+`$, the diagonal entries stay at $`1/2`$. The off-diagonal entries become $`c/2`$. At $`\eta=1`$, discarding the record gives $`\rho_{\mathrm{mix}}`$.

This instrument links increased measurement strength to loss of coherence. The POVM alone does not require that link. The noisy sharp detector from lesson 2 gives a different state change.

## Same readout statistics, different disturbance

Sharp $`Z`$ measurement followed by classical label errors $`\epsilon=(1-\eta)/2`$ has the outcome operations

```math
\mathcal J_s(\rho)=(1-\epsilon)P_s\rho P_s+\epsilon P_{-s}\rho P_{-s},
\qquad P_s=\frac12(I+sZ).
```

These operations have the same effects $`E_s`$ as the Lüders instrument. However, their sum removes all $`Z`$-basis coherence for every $`\epsilon`$. At $`\eta=0`$, the Lüders instrument leaves the input unchanged. The noisy sharp detector still removes its coherence, although the reported bit contains no state information.

Thus outcome statistics cannot determine disturbance. An apparatus model can explain how a chosen instrument produces both the probabilities and the state changes.

## Ancilla implementation and the physical model

The Lüders instrument has a simple ancilla implementation. Let $`\ket{\psi}`$ be any input system vector. The ancilla starts in $`\ket{0}`$. A unitary $`U`$ acts on this input subspace as follows:

```math
U(\ket{\psi}\otimes\ket{0})
=K_+\ket{\psi}\otimes\ket{0}+K_-\ket{\psi}\otimes\ket{1}.
```

The Kraus identity $`K_+^\dagger K_++K_-^\dagger K_-=I`$ ensures that this action preserves inner products. It therefore extends to a unitary. Measuring the ancilla in its computational basis implements the instrument. Result $`0`$ reports plus; result $`1`$ reports minus. Discarding the ancilla gives the channel $`\Phi`$.

The same construction extends to a general apparatus. Let $`\sigma`$ be its initial probe state, $`U`$ the interaction, and $`Z_s`$ its pointer projections. The outcome operation is

```math
\mathcal I_s(\rho)=\mathrm{tr}_{\mathrm{probe}}\left[
(I\otimes Z_s)U(\rho\otimes\sigma)U^\dagger(I\otimes Z_s)
\right].
```

The course considers instruments whose input and output spaces agree. Every such instrument has this form for a sufficiently large probe. Naimark dilation implements outcome probabilities. Stinespring dilation implements channels. Instrument dilation connects the outcomes and their state changes. Different apparatus models can still implement the same instrument.

In the course's optical model, the apparatus parameter $`\gamma`$ sets $`\eta=\sin(2\gamma)`$. For $`0\leq\gamma\leq\pi/4`$, it gives the Kraus operators used above.

<details>
<summary>Continuous-variable extension: the von Neumann pointer model (§1.4.1)</summary>

A continuous pointer uses the same system–probe structure. Let $`R=\sum_r rP_r`$ be the system observable. Each $`P_r`$ projects onto the eigenspace with value $`r`$. The probe has position coordinate $`q`$, momentum operator $`P`$, and initial normalized wavefunction $`\psi(q)`$.

Set $`\hbar=1`$. For coupling strength $`\Delta>0`$, the interaction is $`U=e^{-i\Delta R\otimes P}`$. On an $`R`$ eigenstate with value $`r`$, it shifts the probe wavefunction to $`\psi(q-\Delta r)`$. The pointer position therefore carries information about $`r`$.

The probability density of the pointer reading is

$`p(q)=\sum_r\mathrm{tr}(\rho P_r)|\psi(q-\Delta r)|^2`$.

Overlapping shifted packets make values difficult to distinguish. Narrower packets relative to their separation improve resolution. The operator density for a pointer reading is $`K(q)=\sum_r\psi(q-\Delta r)P_r`$. For readings in an interval $`B`$, the operation is $`\mathcal I_B(\rho)=\int_BK(q)\rho K(q)^\dagger\,dq`$.

Individual pointer readings have a spread even for a fixed eigenvalue. For discrete eigenvalues, grouping pointer readings can recover an exact PVM if the shifted wave packets have disjoint supports. Gaussian packets always overlap at finite width. They only approximate this limit. This model predicts probabilities and conditional states. It does not explain why one individual outcome occurs.

</details>

## Feedback and QEC: retain the right record

The apparatus now gives both a record and a remaining state. A controller can use that record to select a later operation. If result $`s`$ selects a unitary correction $`U_s`$, the average feedback channel is

```math
\Psi(\rho)=\sum_s U_s\mathcal I_s(\rho)U_s^\dagger.
```

For sharp $`Z`$ measurement, applying $`X`$ after the minus outcome resets the qubit to zero. Discarding the outcome before applying feedback loses the information needed to choose the correction.

QEC also needs measurements that reveal a check value while preserving information inside each check subspace. A two-qubit parity check provides a simple example. Its observable is $`Z\otimes Z`$. Even parity has eigenvalue $`+1`$; odd parity has eigenvalue $`-1`$. Its projectors $`P_s`$ and Lüders operations are

```math
P_s=\frac12(I+sZ\otimes Z),\qquad\mathcal I_s(\rho)=P_s\rho P_s.
```

The ancilla starts in $`\ket{0}`$. Each data qubit controls a CNOT with that ancilla as the target. A final ancilla $`Z`$ measurement reports bit zero for even parity and bit one for odd parity. This distinguishes the two parity subspaces while preserving coherence inside either subspace. Measuring the two data qubits separately and taking their classical parity gives the same parity probabilities but destroys more coherence. In particular, it destroys the coherence of $`(\ket{00}+\ket{11})/\sqrt2`$, which an ideal parity check preserves.

This is why collective check measurements matter in [Gross-code state preparation](../gross-code/README.md#preparing-all-twelve-logical-qubits-in-zero). Fault tolerance also requires analysis of faults that propagate through the ancilla circuit. The ideal instrument alone does not establish fault tolerance.

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

Feedback uses the state left by a measurement. A later measurement also acts on that state. [Compatibility and disturbance](compatibility-and-disturbance.md) calculate how the first measurement changes the later outcome probabilities.

Last updated: 2026-11-09
